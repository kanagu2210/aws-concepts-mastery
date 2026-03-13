"""
utils/api.py
Thin wrapper around the Anthropic Messages API.

All stages use a single user message — the full prompt with injected
content is passed as one combined string. No system prompt is used.

Returns (response_text, input_tokens, output_tokens).

Usage:
    from utils.api import call_claude
    text, in_tok, out_tok = call_claude(user_content)
"""

from __future__ import annotations

import time

import anthropic

from utils.config import config

# ---------------------------------------------------------------------------
# Retry settings
# ---------------------------------------------------------------------------
_MAX_RETRIES    = 5
_BASE_DELAY_S   = 2.0   # seconds — doubles on each retry
_MAX_DELAY_S    = 60.0

# HTTP status codes that warrant a retry
_RETRYABLE_STATUS = {429, 500, 502, 503, 529}


# ---------------------------------------------------------------------------
# Client — created once at import time
# ---------------------------------------------------------------------------
_client = anthropic.Anthropic(api_key=config.api_key)


# ---------------------------------------------------------------------------
# Public interface
# ---------------------------------------------------------------------------

def call_claude(
    user_content: str,
    model: str | None = None,
    max_tokens: int | None = None,
) -> tuple[str, int, int]:
    """
    Call the Anthropic Messages API with a single user message.

    The full prompt (with any injected variables and input content)
    is passed as one combined string in the user turn.

    Args:
        user_content:  Complete message — prompt + input content combined.
        model:         Override config.model if needed.
        max_tokens:    Override config.max_tokens if needed.

    Returns:
        (response_text, input_tokens, output_tokens)

    Raises:
        RuntimeError after _MAX_RETRIES exhausted.
        anthropic.APIStatusError for non-retryable 4xx errors.
    """
    model_name = model or config.model
    max_tok    = max_tokens or config.max_tokens

    delay      = _BASE_DELAY_S
    last_error: Exception | None = None

    for attempt in range(1, _MAX_RETRIES + 1):
        try:
            response = _client.messages.create(
                model      = model_name,
                max_tokens = max_tok,
                messages   = [{"role": "user", "content": user_content}],
            )

            text = _extract_text(response)
            return text, response.usage.input_tokens, response.usage.output_tokens

        except anthropic.RateLimitError as e:
            last_error = e
            _log_retry(attempt, "rate limit", delay)

        except anthropic.APIStatusError as e:
            if e.status_code in _RETRYABLE_STATUS:
                last_error = e
                _log_retry(attempt, f"HTTP {e.status_code}", delay)
            else:
                # Non-retryable (400 bad request, 401 auth, etc.) — raise immediately
                raise

        except anthropic.APIConnectionError as e:
            last_error = e
            _log_retry(attempt, "connection error", delay)

        if attempt < _MAX_RETRIES:
            time.sleep(min(delay, _MAX_DELAY_S))
            delay *= 2

    raise RuntimeError(
        f"Claude API call failed after {_MAX_RETRIES} attempts. "
        f"Last error: {last_error}"
    )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _extract_text(response: anthropic.types.Message) -> str:
    """Extract plain text from a response, joining multiple text blocks."""
    parts: list[str] = []
    for block in response.content:
        if hasattr(block, "text"):
            parts.append(block.text)
    return "\n".join(parts).strip()


def _log_retry(attempt: int, reason: str, next_delay: float) -> None:
    print(
        f"  [api] attempt {attempt}/{_MAX_RETRIES} failed ({reason}) — "
        f"retrying in {min(next_delay, _MAX_DELAY_S):.0f}s"
    )