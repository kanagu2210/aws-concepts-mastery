#!/usr/bin/env python3
"""
02_pipeline/build_dashboard.py

Generates a self-contained dashboard.html from concept_spines.yaml
and the output directories. Open the HTML file in a browser to browse
all spines, open narration pages, and open whiteboards.

Usage:
    python 02_pipeline/build_dashboard.py
    python 02_pipeline/build_dashboard.py --out dashboard.html
    python 02_pipeline/build_dashboard.py --open
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from utils.config import config  # noqa: F401
from pipeline_common import (
    _load_spines,
    _part_subdir,  # noqa: F401
    narrated_path,
    whiteboard_path,
    rendered_path,
)


LAYER_NAMES = {
    1: "Foundations",
    2: "Core Mechanisms",
    3: "Service Mastery",
    4: "Decision Patterns",
    5: "Architectural Patterns",
    6: "Exam & Interview Bridges",
}

LAYER_COLORS = {
    1: ("#e8f5e9", "#2e7d32", "#a5d6a7"),
    2: ("#e3f2fd", "#1565c0", "#90caf9"),
    3: ("#fff8e1", "#f57f17", "#ffe082"),
    4: ("#fce4ec", "#880e4f", "#f48fb1"),
    5: ("#ede7f6", "#4527a0", "#b39ddb"),
    6: ("#e0f7fa", "#006064", "#80deea"),
}

SPINE_TYPE_LABELS = {
    "mental_model": "Model",
    "concept": "Concept",
    "contrast": "Contrast",
    "pattern": "Pattern",
    "bridge": "Bridge",
}


def build_spine_data(spines: list[dict]) -> list[dict]:
    """Enrich each spine with output file existence flags and relative paths."""
    result = []
    for s in spines:
        sid = s["id"]
        slug = s["slug"]

        r_path = rendered_path(sid, slug)
        w_path = whiteboard_path(sid, slug)
        n_path = narrated_path(sid, slug)

        result.append(
            {
                **s,
                "has_narration": n_path.exists(),
                "has_render": r_path.exists(),
                "has_whiteboard": w_path.exists(),
                "render_path": str(r_path) if r_path.exists() else None,
                "whiteboard_path": str(w_path) if w_path.exists() else None,
            }
        )
    return result


def generate_html(spines: list[dict]) -> str:
    import json as _json

    total = len(spines)
    with_render = sum(1 for s in spines if s["has_render"])
    with_wb = sum(1 for s in spines if s["has_whiteboard"])
    with_narrate = sum(1 for s in spines if s["has_narration"])

    js_spines = _json.dumps(
        [
            {
                "id": s["id"],
                "title": s.get("title", ""),
                "layer": s.get("layer", 0),
                "layer_name": s.get("layer_name", ""),
                "domain": s.get("domain", "General"),
                "service": s.get("aws_service", "General"),
                "slug": s.get("slug", ""),
                "spine_type": s.get("spine_type", "concept"),
                "exams": s.get("exams") or [],
                "tier": s.get("concept_tier", ""),
                "has_render": s["has_render"],
                "has_whiteboard": s["has_whiteboard"],
                "has_narration": s["has_narration"],
                "render_path": s["render_path"] or "",
                "whiteboard_path": s["whiteboard_path"] or "",
            }
            for s in spines
        ],
        indent=None,
    )

    return f"""<!doctype html>
<html lang="en" data-theme="slate">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AWS Concept Mastery</title>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;1,9..40,300&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
:root {{
  --accent:    #6c5ce7;
  --accent2:   #a29bfe;
  --green:     #00b894;
  --green2:    #55efc4;
  --amber:     #fdcb6e;
  --red:       #e17055;
  --radius-sm: 6px;
  --radius:    10px;
  --radius-lg: 14px;
}}

[data-theme="warm"] {{
  --bg:        #fdf6ee;
  --surface:   #ffffff;
  --surface2:  #faf3ea;
  --surface3:  #f0e8dc;
  --border:    rgba(0,0,0,0.07);
  --border2:   rgba(0,0,0,0.13);
  --text:      #1c1510;
  --text2:     #6b5e52;
  --text3:     #a8998c;
}}

[data-theme="slate"] {{
  --bg:        #eef1f7;
  --surface:   #ffffff;
  --surface2:  #e6eaf3;
  --surface3:  #d8ddef;
  --border:    rgba(0,0,0,0.08);
  --border2:   rgba(0,0,0,0.15);
  --text:      #1a1e2e;
  --text2:     #5a6080;
  --text3:     #9098b8;
}}

[data-theme="light"] {{
  --bg:        #f7f5f0;
  --surface:   #ffffff;
  --surface2:  #f0ede8;
  --surface3:  #e8e4dd;
  --border:    rgba(0,0,0,0.08);
  --border2:   rgba(0,0,0,0.14);
  --text:      #1a1a2e;
  --text2:     #5a5a78;
  --text3:     #9898b0;
}}

*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

body {{
  font-family: 'DM Sans', sans-serif;
  background: var(--bg);
  color: var(--text);
  min-height: 100vh;
  font-size: 18px;
  line-height: 1.7;
  -webkit-font-smoothing: antialiased;
}}

::-webkit-scrollbar {{ width: 5px; height: 5px; }}
::-webkit-scrollbar-track {{ background: transparent; }}
::-webkit-scrollbar-thumb {{ background: var(--surface3); border-radius: 3px; }}

.shell {{ display: flex; flex-direction: column; height: 100vh; overflow: hidden; }}
.body {{
  flex: 1;
  display: flex;
  overflow: hidden;
  transition: margin-right 0.3s cubic-bezier(0.4,0,0.2,1);
}}
.body.panel-open {{ margin-right: 80vw; }}

.topbar {{
  display: flex;
  flex-direction: column;
  background: var(--surface);
  border-bottom: 1px solid var(--border);
  flex-shrink: 0;
  z-index: 50;
  box-shadow: 0 1px 0 rgba(0,0,0,0.08);
}}
.topbar-row1 {{
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
  padding: 12px 20px 10px;
  border-bottom: 1px solid var(--border);
}}
.topbar-row2 {{
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
  padding: 8px 20px;
}}

.brand {{
  display: flex;
  align-items: baseline;
  gap: 6px;
  font-size: 19px;
  font-weight: 600;
  letter-spacing: -0.02em;
  white-space: nowrap;
}}
.brand-aws {{
  background: linear-gradient(135deg, #6c5ce7, #a29bfe);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}}
.brand-sub {{
  color: var(--text2);
  font-weight: 300;
  font-size: 15px;
}}

.theme-switcher {{
  display: flex;
  align-items: center;
  gap: 3px;
  background: var(--surface2);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  padding: 3px;
}}
.theme-btn {{
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 28px;
  border-radius: 5px;
  cursor: pointer;
  border: none;
  background: transparent;
  transition: all 0.15s;
  font-size: 15px;
  line-height: 1;
}}
.theme-btn:hover {{ background: var(--surface3); }}
.theme-btn.active {{
  background: var(--surface3);
  box-shadow: 0 0 0 1px var(--border2);
}}

.settings-gear {{
  padding: 7px 10px;
  border-radius: var(--radius-sm);
  background: var(--surface2);
  border: 1px solid var(--border);
  color: var(--text2);
  font-size: 16px;
  cursor: pointer;
  transition: all 0.15s;
}}
.settings-gear:hover {{
  background: var(--surface3);
  color: var(--text);
}}

.search-wrap {{
  position: relative;
  flex: 1;
  max-width: 260px;
  min-width: 140px;
}}
.search-wrap input {{
  width: 100%;
  padding: 7px 10px 7px 32px;
  background: var(--surface2);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  color: var(--text);
  font-family: 'DM Sans', sans-serif;
  font-size: 15px;
  outline: none;
  transition: border-color 0.2s;
}}
.search-wrap input::placeholder {{ color: var(--text3); }}
.search-wrap input:focus {{ border-color: var(--accent); }}
.search-ico {{
  position: absolute;
  left: 10px;
  top: 50%;
  transform: translateY(-50%);
  width: 14px;
  height: 14px;
  color: var(--text3);
  pointer-events: none;
}}

.view-btns {{
  display: flex;
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  overflow: hidden;
}}
.vbtn {{
  padding: 8px 16px;
  font-size: 14px;
  font-weight: 500;
  background: transparent;
  color: var(--text2);
  border: none;
  cursor: pointer;
  font-family: 'DM Sans', sans-serif;
  transition: all 0.15s;
}}
.vbtn.active {{
  background: var(--surface3);
  color: var(--text);
}}

.filter-label {{
  font-size: 14px;
  color: var(--text3);
  margin-right: 2px;
}}
.fpill {{
  padding: 5px 12px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 500;
  border: 1px solid var(--border);
  background: transparent;
  color: var(--text2);
  cursor: pointer;
  font-family: 'DM Sans', sans-serif;
  transition: all 0.15s;
  white-space: nowrap;
}}
.fpill:hover {{
  border-color: var(--border2);
  color: var(--text);
}}
.fpill.active {{
  background: var(--surface3);
  border-color: var(--border2);
  color: var(--text);
}}

.rev-meter {{
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 5px 12px;
  border-radius: var(--radius-sm);
  background: rgba(0,184,148,0.08);
  border: 1px solid rgba(0,184,148,0.2);
}}
.rev-meter-label {{
  font-size: 14px;
  color: var(--green);
  font-weight: 500;
}}
.rev-track {{
  width: 72px;
  height: 4px;
  border-radius: 2px;
  background: rgba(0,0,0,0.08);
  overflow: hidden;
}}
.rev-fill {{
  height: 100%;
  border-radius: 2px;
  background: var(--green);
  transition: width 0.4s ease;
  width: 0%;
}}
.rev-pct {{
  font-size: 14px;
  font-weight: 500;
  font-family: 'DM Mono', monospace;
  color: var(--green);
  min-width: 42px;
}}

.stat-pills {{ display: flex; gap: 2px; }}
.stat-pill {{
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 5px 12px;
  border-radius: var(--radius-sm);
  background: var(--surface2);
  border: 1px solid var(--border);
}}
.stat-n {{
  font-size: 20px;
  font-weight: 600;
  font-family: 'DM Mono', monospace;
  line-height: 1.1;
}}
.stat-l {{
  font-size: 12px;
  color: var(--text3);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}}
.stat-total .stat-n {{ color: var(--accent2); }}
.stat-rendered .stat-n {{ color: #74b9ff; }}
.stat-boards .stat-n {{ color: #a29bfe; }}
.stat-revised .stat-n {{ color: var(--green); }}

.sidenav {{
  width: 200px;
  min-width: 200px;
  flex-shrink: 0;
  background: var(--surface);
  border-right: 1px solid var(--border);
  overflow-y: auto;
  padding: 12px 0;
}}

.sn-layer-item {{
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 7px 14px;
  cursor: pointer;
  user-select: none;
  border-left: 2px solid transparent;
  transition: all 0.12s;
  font-size: 15px;
  font-weight: 500;
  color: var(--text2);
}}
.sn-layer-item:hover {{
  background: var(--surface2);
  color: var(--text);
}}
.sn-layer-item.expanded {{ color: var(--text); }}
.sn-ldot {{
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}}
.sn-lname {{
  flex: 1;
  line-height: 1.3;
}}
.sn-lcount {{
  font-family: 'DM Mono', monospace;
  font-size: 13px;
  color: var(--text3);
}}
.sn-chevron {{
  font-size: 13px;
  color: var(--text3);
  transition: transform 0.15s;
  flex-shrink: 0;
}}
.sn-layer-item.expanded .sn-chevron {{ transform: rotate(90deg); }}

.sn-children {{
  display: none;
  padding: 2px 0 4px 0;
}}
.sn-layer-item.expanded + .sn-children {{ display: block; }}

.sn-domain-item {{
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 5px 14px 5px 28px;
  cursor: pointer;
  font-size: 14px;
  color: var(--text3);
  transition: all 0.1s;
}}
.sn-domain-item:hover {{
  color: var(--text2);
  background: var(--surface2);
}}
.sn-domain-item.sel {{ color: var(--text); }}
.sn-domain-item.expanded {{ color: var(--text2); }}
.sn-domain-dot {{
  width: 5px;
  height: 5px;
  border-radius: 50%;
  flex-shrink: 0;
  opacity: 0.5;
}}
.sn-dname {{ flex: 1; }}
.sn-dcount {{
  font-family: 'DM Mono', monospace;
  font-size: 13px;
}}

.sn-svc-children {{
  display: none;
  padding: 2px 0;
}}
.sn-domain-item.expanded + .sn-svc-children {{ display: block; }}

.sn-svc-item {{
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 4px 14px 4px 42px;
  cursor: pointer;
  font-size: 13px;
  color: var(--text3);
  transition: all 0.1s;
}}
.sn-svc-item:hover {{ color: var(--text2); }}
.sn-svc-item.sel {{
  color: var(--accent2);
  font-weight: 500;
}}
.sn-svc-dot {{
  width: 3px;
  height: 3px;
  border-radius: 50%;
  background: currentColor;
  opacity: 0.6;
  flex-shrink: 0;
}}

.main {{
  flex: 1;
  overflow-y: auto;
  padding: 20px 24px;
}}

.breadcrumb {{
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  color: var(--text3);
  margin-bottom: 16px;
  min-height: 20px;
}}
.bc-item {{
  cursor: pointer;
  transition: color 0.1s;
}}
.bc-item:hover {{ color: var(--text); }}
.bc-current {{
  color: var(--text2);
  cursor: default;
}}
.bc-sep {{
  opacity: 0.4;
  font-size: 14px;
}}

.layer-block {{ margin-bottom: 28px; }}

.layer-hdr {{
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border-radius: var(--radius);
  margin-bottom: 12px;
  cursor: pointer;
  user-select: none;
  transition: opacity 0.15s;
  border: 1px solid transparent;
}}
.layer-hdr:hover {{ opacity: 0.9; }}

.layer-num {{
  font-family: 'DM Mono', monospace;
  font-size: 30px;
  font-weight: 500;
  line-height: 1;
  flex-shrink: 0;
}}
.layer-info {{ flex: 1; }}
.layer-name {{
  font-size: 18px;
  font-weight: 600;
  letter-spacing: -0.01em;
}}
.layer-meta {{
  font-size: 14px;
  margin-top: 2px;
  opacity: 0.7;
}}

.layer-meters {{
  display: flex;
  flex-direction: column;
  gap: 4px;
  min-width: 140px;
}}
.meter-row {{
  display: flex;
  align-items: center;
  gap: 6px;
}}
.meter-lbl {{
  font-size: 13px;
  width: 62px;
  flex-shrink: 0;
  opacity: 0.7;
}}
.meter-track {{
  flex: 1;
  height: 3px;
  border-radius: 2px;
  background: rgba(0,0,0,0.2);
  overflow: hidden;
}}
.meter-fill {{
  height: 100%;
  border-radius: 2px;
  transition: width 0.5s ease;
}}
.meter-n {{
  font-size: 13px;
  font-family: 'DM Mono', monospace;
  opacity: 0.8;
  width: 36px;
  text-align: right;
}}

.layer-chevron {{
  font-size: 17px;
  opacity: 0.6;
  transition: transform 0.2s;
  flex-shrink: 0;
}}
.layer-block.collapsed .layer-chevron {{ transform: rotate(-90deg); }}
.layer-block.collapsed .layer-body {{ display: none; }}

.domain-block {{ margin-bottom: 14px; }}

.domain-hdr {{
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 7px 12px;
  border-radius: var(--radius-sm);
  cursor: pointer;
  user-select: none;
  background: var(--surface);
  border: 1px solid var(--border);
  transition: border-color 0.15s;
  margin-bottom: 8px;
}}
.domain-hdr:hover {{ border-color: var(--border2); }}
.domain-accent {{
  width: 7px;
  height: 7px;
  border-radius: 50%;
  flex-shrink: 0;
}}
.domain-name {{
  font-size: 16px;
  font-weight: 600;
  flex: 1;
  letter-spacing: 0.01em;
}}
.domain-count {{
  font-size: 14px;
  color: var(--text3);
  font-family: 'DM Mono', monospace;
}}
.domain-chevron {{
  font-size: 12px;
  color: var(--text3);
  transition: transform 0.15s;
}}
.domain-block.collapsed .domain-chevron {{ transform: rotate(-90deg); }}
.domain-block.collapsed .domain-body {{ display: none; }}

.service-block {{
  margin-bottom: 12px;
  padding-left: 8px;
}}

.service-hdr {{
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 5px 8px;
  cursor: pointer;
  margin-bottom: 8px;
  user-select: none;
}}
.service-tag {{
  font-size: 14px;
  font-weight: 500;
  padding: 5px 14px;
  border-radius: 20px;
  background: var(--surface3);
  border: 1px solid var(--border2);
  color: var(--text2);
  font-family: 'DM Mono', monospace;
  letter-spacing: 0.02em;
}}
.service-count {{
  font-size: 14px;
  color: var(--text3);
  font-family: 'DM Mono', monospace;
}}
.service-chevron {{
  font-size: 12px;
  color: var(--text3);
  margin-left: auto;
  transition: transform 0.15s;
}}
.service-block.collapsed .service-chevron {{ transform: rotate(-90deg); }}
.service-block.collapsed .service-cards {{ display: none; }}

.cards-grid {{
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 14px;
  padding-left: 4px;
}}
.cards-grid.flat-grid {{ padding-left: 0; }}

.spine-card {{
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 20px 22px;
  display: flex;
  flex-direction: column;
  gap: 0;
  transition: border-color 0.15s, transform 0.15s, background 0.2s;
}}
.spine-card:hover {{
  border-color: var(--border2);
  transform: translateY(-1px);
}}
.spine-card.pass1 {{ border-color: rgba(253,203,110,0.35); }}
.spine-card.pass2 {{ border-color: rgba(116,185,255,0.35); }}
.spine-card.pass3 {{
  background: rgba(0,184,148,0.04);
  border-color: rgba(0,184,148,0.3);
}}

.card-top {{
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
  margin-bottom: 12px;
}}
.card-id {{
  font-family: 'DM Mono', monospace;
  font-size: 13px;
  color: var(--text3);
}}

.status-dot {{
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}}
.sd-full {{
  background: var(--green);
  box-shadow: 0 0 6px rgba(0,184,148,0.4);
}}
.sd-partial {{ background: var(--amber); }}
.sd-none {{
  background: var(--surface3);
  border: 1px solid var(--border2);
}}

.type-tag {{
  font-size: 12px;
  font-weight: 500;
  padding: 3px 10px;
  border-radius: 20px;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}}
.tt-mental_model {{ background: rgba(253,203,110,0.15); color: #b57c14; border: 1px solid rgba(253,203,110,0.25); }}
.tt-concept      {{ background: rgba(116,185,255,0.12); color: #1565c0; border: 1px solid rgba(116,185,255,0.2); }}
.tt-contrast     {{ background: rgba(232,67,147,0.12);  color: #c2185b; border: 1px solid rgba(232,67,147,0.2); }}
.tt-pattern      {{ background: rgba(162,155,254,0.12); color: #6c5ce7; border: 1px solid rgba(162,155,254,0.2); }}
.tt-bridge       {{ background: rgba(0,184,148,0.12);   color: #009664; border: 1px solid rgba(0,184,148,0.2); }}

.card-title {{
  font-size: 18px;
  font-weight: 600;
  line-height: 1.4;
  color: var(--text);
  letter-spacing: -0.02em;
  margin-bottom: 12px;
}}

.card-meta {{
  display: flex;
  align-items: center;
  gap: 6px;
  flex-wrap: wrap;
  padding-bottom: 14px;
  border-bottom: 1px solid var(--border);
  margin-bottom: 14px;
}}
.exam-tag {{
  font-size: 12px;
  font-weight: 600;
  padding: 3px 9px;
  border-radius: 20px;
  letter-spacing: 0.04em;
  color: #fff;
}}
.et-ccp {{ background: #00a65a; }}
.et-saa {{ background: #0063b1; }}
.et-sap {{ background: #5c35a8; }}
.tier-badge {{
  font-size: 13px;
  color: var(--text3);
  margin-left: auto;
  text-transform: capitalize;
  font-family: 'DM Mono', monospace;
}}

.card-actions {{
  display: flex;
  gap: 8px;
}}
.action-btn {{
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 11px 14px;
  border-radius: var(--radius-sm);
  font-size: 15px;
  font-weight: 500;
  text-decoration: none;
  border: 1px solid var(--border2);
  background: var(--surface2);
  color: var(--text2);
  transition: all 0.15s;
  cursor: pointer;
  font-family: 'DM Sans', sans-serif;
}}
.action-btn:hover {{
  background: var(--surface3);
  color: var(--text);
  border-color: var(--border2);
}}
.action-btn.read {{
  background: rgba(108,92,231,0.1);
  border-color: rgba(108,92,231,0.3);
  color: var(--accent2);
}}
.action-btn.read:hover {{ background: rgba(108,92,231,0.2); }}
.action-btn.board {{
  background: rgba(162,155,254,0.08);
  border-color: rgba(162,155,254,0.25);
  color: #7c6fe0;
}}
.action-btn.board:hover {{ background: rgba(162,155,254,0.15); }}
.action-btn.disabled {{
  opacity: 0.25;
  cursor: not-allowed;
  pointer-events: none;
}}
.action-icon {{
  width: 15px;
  height: 15px;
  flex-shrink: 0;
}}

.empty {{
  text-align: center;
  padding: 60px 20px;
  color: var(--text3);
  font-size: 16px;
}}
.empty-icon {{
  font-size: 32px;
  margin-bottom: 12px;
  opacity: 0.4;
}}

.spine-list-wrap {{
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 18px 20px;
}}
.spine-list {{
  list-style: decimal;
  padding-left: 28px;
  margin: 0;
}}
.spine-list-item {{
  padding: 12px 0;
  border-bottom: 1px solid var(--border);
}}
.spine-list-item:last-child {{ border-bottom: none; }}
.spine-list-row {{
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}}
.spine-list-id {{
  font-family: 'DM Mono', monospace;
  font-size: 13px;
  color: var(--text3);
  min-width: 58px;
}}
.spine-list-title {{
  font-size: 16px;
  font-weight: 600;
  color: var(--text);
  flex: 1;
  min-width: 260px;
}}
.spine-list-meta {{
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
  margin-top: 6px;
  color: var(--text3);
  font-size: 13px;
}}
.spine-mini-tag {{
  padding: 3px 8px;
  border-radius: 999px;
  border: 1px solid var(--border2);
  background: var(--surface2);
  color: var(--text2);
  font-size: 12px;
  font-weight: 500;
}}
.spine-list-actions {{
  display: flex;
  gap: 8px;
  margin-left: auto;
}}
.spine-mini-btn {{
  padding: 7px 10px;
  border-radius: var(--radius-sm);
  border: 1px solid var(--border2);
  background: var(--surface2);
  color: var(--text2);
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  font-family: 'DM Sans', sans-serif;
  transition: all 0.15s;
}}
.spine-mini-btn:hover {{
  background: var(--surface3);
  color: var(--text);
}}
.spine-mini-btn.disabled {{
  opacity: 0.3;
  cursor: not-allowed;
  pointer-events: none;
}}

.viewer-scrim {{
  display: none;
  position: fixed;
  inset: 0;
  z-index: 199;
  background: rgba(0,0,0,0);
  transition: background 0.3s;
}}
.viewer-scrim.open {{
  display: block;
  background: rgba(0,0,0,0.18);
}}

.viewer-panel {{
  position: fixed;
  top: 0;
  right: 0;
  bottom: 0;
  width: 80vw;
  background: var(--surface);
  border-left: 1px solid var(--border2);
  display: flex;
  flex-direction: column;
  z-index: 200;
  transform: translateX(100%);
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: -12px 0 40px rgba(0,0,0,0.35);
}}
.viewer-panel.open {{ transform: translateX(0); }}

.viewer-bar {{
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 11px 16px;
  background: var(--surface2);
  border-bottom: 1px solid var(--border);
  flex-shrink: 0;
}}
.viewer-close {{
  width: 30px;
  height: 30px;
  border-radius: var(--radius-sm);
  background: transparent;
  border: 1px solid var(--border);
  color: var(--text2);
  font-size: 20px;
  cursor: pointer;
  line-height: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.15s;
  font-family: 'DM Sans', sans-serif;
  flex-shrink: 0;
}}
.viewer-close:hover {{
  background: rgba(225,112,85,0.15);
  border-color: var(--red);
  color: var(--red);
}}
.viewer-type {{
  font-size: 11px;
  font-weight: 600;
  padding: 3px 9px;
  border-radius: 20px;
  white-space: nowrap;
  flex-shrink: 0;
}}
.viewer-type.read {{
  background: rgba(108,92,231,0.15);
  color: var(--accent2);
  border: 1px solid rgba(108,92,231,0.3);
}}
.viewer-type.board {{
  background: rgba(162,155,254,0.12);
  color: #7c6fe0;
  border: 1px solid rgba(162,155,254,0.25);
}}
.viewer-title {{
  flex: 1;
  font-size: 16px;
  font-weight: 500;
  color: var(--text);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}}
.viewer-zoom-wrap {{
  display: flex;
  align-items: center;
  gap: 5px;
  flex-shrink: 0;
}}
.viewer-zoom-label {{
  font-size: 14px;
  color: var(--text3);
}}
.viewer-zoom-btn {{
  width: 26px;
  height: 26px;
  border-radius: var(--radius-sm);
  background: var(--surface3);
  border: 1px solid var(--border2);
  color: var(--text);
  font-size: 16px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.1s;
  font-family: 'DM Sans', sans-serif;
}}
.viewer-zoom-btn:hover {{ background: var(--border2); }}
.viewer-zoom-val {{
  font-size: 14px;
  font-family: 'DM Mono', monospace;
  color: var(--text2);
  min-width: 42px;
  text-align: center;
}}

.viewer-rev {{
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 20px;
  background: var(--surface2);
  border-bottom: 1px solid var(--border);
  flex-shrink: 0;
  flex-wrap: wrap;
}}
.viewer-rev-info {{
  display: flex;
  flex-direction: column;
  gap: 2px;
}}
.viewer-rev-title {{
  font-size: 13px;
  font-weight: 600;
  color: var(--text2);
}}
.viewer-rev-sub {{
  font-size: 12px;
  color: var(--text3);
}}
.viewer-pass-btns {{
  display: flex;
  gap: 6px;
  margin-left: auto;
  flex-wrap: wrap;
}}
.pass-btn {{
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 7px 14px;
  border-radius: var(--radius-sm);
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  border: 1.5px solid transparent;
  font-family: 'DM Sans', sans-serif;
  transition: all 0.15s;
}}
.pass-btn:disabled {{
  opacity: 0.3;
  cursor: not-allowed;
}}
.pass-btn.p1 {{
  background: rgba(253,203,110,0.1);
  color: #b08020;
  border-color: rgba(253,203,110,0.3);
}}
.pass-btn.p1:hover:not(:disabled) {{ background: rgba(253,203,110,0.2); }}
.pass-btn.p2 {{
  background: rgba(116,185,255,0.1);
  color: #1565c0;
  border-color: rgba(116,185,255,0.3);
}}
.pass-btn.p2:hover:not(:disabled) {{ background: rgba(116,185,255,0.2); }}
.pass-btn.p3 {{
  background: rgba(0,184,148,0.1);
  color: #009664;
  border-color: rgba(0,184,148,0.3);
}}
.pass-btn.p3:hover:not(:disabled) {{ background: rgba(0,184,148,0.2); }}
.pass-btn.done {{
  opacity: 0.45;
  text-decoration: line-through;
  cursor: default;
}}
.pass-btn.current {{
  box-shadow: 0 0 0 2px currentColor;
  opacity: 1;
}}
.pass-btn-undo {{
  padding: 7px 10px;
  border-radius: var(--radius-sm);
  font-size: 13px;
  background: transparent;
  border: 1.5px solid var(--border2);
  color: var(--text3);
  cursor: pointer;
  font-family: 'DM Sans', sans-serif;
  transition: all 0.15s;
}}
.pass-btn-undo:hover {{
  border-color: var(--red);
  color: var(--red);
  background: rgba(225,112,85,0.08);
}}

.viewer-frame-wrap {{
  flex: 1;
  position: relative;
  background: var(--bg);
  padding: 18px;
  overflow: auto;
}}

.viewer-frame {{
  width: 100%;
  height: 100%;
  border: none;
  background: white;
  border-radius: 10px;
  box-shadow: 0 6px 18px rgba(0,0,0,0.12);
  transform-origin: top left;
  display: block;
}}

.footer-bar {{
  flex-shrink: 0;
  background: var(--surface);
  border-top: 1px solid var(--border);
  padding: 14px 24px;
  display: flex;
  align-items: center;
  gap: 24px;
  z-index: 10;
}}
.footer-overall {{
  display: flex;
  align-items: center;
  gap: 12px;
  flex-shrink: 0;
}}
.footer-overall-label {{
  font-size: 14px;
  font-weight: 600;
  color: var(--text2);
  white-space: nowrap;
}}
.footer-pct {{
  font-size: 28px;
  font-weight: 700;
  font-family: 'DM Mono', monospace;
  color: var(--green);
  line-height: 1;
  min-width: 72px;
}}
.footer-sub {{
  font-size: 13px;
  color: var(--text3);
  margin-top: 2px;
}}
.footer-big-bar {{
  flex: 1;
  height: 10px;
  border-radius: 5px;
  background: var(--surface3);
  overflow: hidden;
  display: flex;
}}
.footer-seg {{
  height: 100%;
  transition: width 0.5s ease;
  width: 0%;
}}
.footer-seg.s1 {{ background: #fdcb6e; }}
.footer-seg.s2 {{ background: #74b9ff; }}
.footer-seg.s3 {{ background: var(--green); }}
.footer-layers {{
  display: flex;
  gap: 16px;
  flex-shrink: 0;
}}
.footer-layer-stat {{
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}}
.footer-layer-dot {{
  width: 8px;
  height: 8px;
  border-radius: 50%;
}}
.footer-layer-bar-wrap {{
  width: 40px;
  height: 4px;
  border-radius: 2px;
  background: var(--surface3);
  overflow: hidden;
}}
.footer-layer-fill {{
  height: 100%;
  border-radius: 2px;
  transition: width 0.5s ease;
}}
.footer-layer-label {{
  font-size: 11px;
  font-family: 'DM Mono', monospace;
  color: var(--text3);
  white-space: nowrap;
}}

.settings-overlay {{
  display: none;
  position: fixed;
  inset: 0;
  z-index: 300;
  background: rgba(0,0,0,0.5);
  align-items: center;
  justify-content: center;
}}
.settings-overlay.open {{ display: flex; }}
.settings-box {{
  background: var(--surface);
  border: 1px solid var(--border2);
  border-radius: var(--radius-lg);
  padding: 28px 32px;
  width: 520px;
  max-width: 92vw;
  box-shadow: 0 20px 60px rgba(0,0,0,0.3);
}}
.settings-title {{
  font-size: 18px;
  font-weight: 600;
  color: var(--text);
  margin-bottom: 6px;
}}
.settings-sub {{
  font-size: 14px;
  color: var(--text3);
  margin-bottom: 24px;
}}
.settings-section {{
  margin-bottom: 20px;
  padding-bottom: 20px;
  border-bottom: 1px solid var(--border);
}}
.settings-section:last-of-type {{
  border-bottom: none;
  margin-bottom: 0;
  padding-bottom: 0;
}}
.settings-section-title {{
  font-size: 13px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--text3);
  margin-bottom: 12px;
}}
.settings-row {{
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 10px;
}}
.settings-row:last-child {{ margin-bottom: 0; }}
.settings-row-label {{
  flex: 1;
  font-size: 15px;
  color: var(--text);
}}
.settings-row-sub {{
  font-size: 13px;
  color: var(--text3);
  margin-top: 2px;
}}
.reset-btn {{
  padding: 8px 18px;
  border-radius: var(--radius-sm);
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  font-family: 'DM Sans', sans-serif;
  transition: all 0.15s;
  border: 1.5px solid;
}}
.reset-btn.danger {{
  background: rgba(225,112,85,0.1);
  color: var(--red);
  border-color: rgba(225,112,85,0.3);
}}
.reset-btn.danger:hover {{ background: rgba(225,112,85,0.2); }}
.reset-btn.warning {{
  background: rgba(253,203,110,0.1);
  color: #b08020;
  border-color: rgba(253,203,110,0.3);
}}
.reset-btn.warning:hover {{ background: rgba(253,203,110,0.2); }}
.reset-btn.neutral {{
  background: var(--surface2);
  color: var(--text2);
  border-color: var(--border2);
}}
.reset-btn.neutral:hover {{ background: var(--surface3); }}
</style>
</head>
<body>
<div class="shell">

  <header class="topbar">
    <div class="topbar-row1">
      <div class="brand">
        <span class="brand-aws">AWS</span>
        <span>Concept Mastery</span>
        <span class="brand-sub">/ Dashboard</span>
      </div>

      <div class="theme-switcher" title="Switch theme">
        <button class="theme-btn active" id="tbtn-slate" onclick="setTheme('slate')" title="Slate blue">🔵</button>
        <button class="theme-btn" id="tbtn-light" onclick="setTheme('light')" title="Light">🌤</button>
        <button class="theme-btn" id="tbtn-warm" onclick="setTheme('warm')" title="Warm cream">🌅</button>
      </div>

      <button class="settings-gear" onclick="openSettings()" title="Admin">⚙ Admin</button>

      <div class="stat-pills">
        <div class="stat-pill stat-total">
          <span class="stat-n" id="st-total">{total}</span>
          <span class="stat-l">Total</span>
        </div>
        <div class="stat-pill stat-rendered">
          <span class="stat-n" id="st-rendered">{with_render}</span>
          <span class="stat-l">Narration</span>
        </div>
        <div class="stat-pill stat-boards">
          <span class="stat-n" id="st-boards">{with_wb}</span>
          <span class="stat-l">Boards</span>
        </div>
        <div class="stat-pill stat-revised">
          <span class="stat-n" id="st-revised">0</span>
          <span class="stat-l">Completed</span>
        </div>
      </div>

      <div class="rev-meter">
        <span class="rev-meter-label">Started</span>
        <div class="rev-track"><div class="rev-fill" id="rev-fill"></div></div>
        <span class="rev-pct" id="rev-pct">0%</span>
      </div>

      <div style="margin-left:auto; display:flex; align-items:center; gap:10px;">
        <div class="search-wrap">
          <svg class="search-ico" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5">
            <circle cx="6.5" cy="6.5" r="4.5"/><path d="M10.5 10.5L14 14" stroke-linecap="round"/>
          </svg>
          <input type="text" id="search-input" placeholder="Search title, id, service…" autocomplete="off">
        </div>

        <div class="view-btns">
          <button class="vbtn active" id="vbtn-grouped" onclick="setView('grouped')">Grouped</button>
          <button class="vbtn" id="vbtn-flat" onclick="setView('flat')">All cards</button>
          <button class="vbtn" id="vbtn-list" onclick="setView('list')">Spine ID List</button>
        </div>
      </div>
    </div>

    <div class="topbar-row2">
      <span class="filter-label">Show</span>
      <button class="fpill active" data-sf="all">All</button>
      <button class="fpill" data-sf="narration">Narration</button>
      <button class="fpill" data-sf="board">With board</button>
      <button class="fpill" data-sf="pending">Pending</button>
      <button class="fpill" data-sf="pass1">Pass 1 ●</button>
      <button class="fpill" data-sf="pass2">Pass 2 ●</button>
      <button class="fpill" data-sf="pass3">Pass 3 ●</button>
      <button class="fpill" data-sf="torevise">To revise</button>
    </div>
  </header>

  <div class="body">
    <nav class="sidenav" id="sidenav"></nav>

    <main class="main" id="main">
      <div class="breadcrumb" id="breadcrumb"></div>
      <div id="content"></div>
    </main>
  </div>

  <footer class="footer-bar" id="footer-bar">
    <div class="footer-overall">
      <div>
        <div class="footer-pct" id="footer-pct">0%</div>
        <div class="footer-sub" id="footer-sub">0 of 0 completed</div>
      </div>
      <div class="footer-overall-label">Overall<br>Completed</div>
    </div>
    <div class="footer-big-bar">
      <div class="footer-seg s1" id="footer-seg1"></div>
      <div class="footer-seg s2" id="footer-seg2"></div>
      <div class="footer-seg s3" id="footer-seg3"></div>
    </div>
    <div style="display:flex;gap:12px;font-size:12px;color:var(--text3);align-items:center;flex-shrink:0">
      <span style="display:flex;align-items:center;gap:4px"><span style="width:8px;height:8px;border-radius:50%;background:#fdcb6e;display:inline-block"></span>Pass 1</span>
      <span style="display:flex;align-items:center;gap:4px"><span style="width:8px;height:8px;border-radius:50%;background:#74b9ff;display:inline-block"></span>Pass 2</span>
      <span style="display:flex;align-items:center;gap:4px"><span style="width:8px;height:8px;border-radius:50%;background:#00b894;display:inline-block"></span>Pass 3</span>
    </div>
    <div class="footer-layers" id="footer-layers"></div>
  </footer>
</div>

<div class="settings-overlay" id="settings-overlay" onclick="closeSettingsOnOverlay(event)">
  <div class="settings-box">
    <div class="settings-title">Admin Panel</div>
    <div class="settings-sub">Manage your narration progress and revision controls.</div>

    <div class="settings-section">
      <div class="settings-section-title">Narration progress</div>

      <div class="settings-row">
        <div>
          <div class="settings-row-label">Reset Pass 3 to Pass 2</div>
          <div class="settings-row-sub">Move all Pass 3 concepts back to Pass 2</div>
        </div>
        <button class="reset-btn warning" onclick="resetToPass(3,2)">Reset Pass 3</button>
      </div>

      <div class="settings-row">
        <div>
          <div class="settings-row-label">Reset Pass 2 to Pass 1</div>
          <div class="settings-row-sub">Move all Pass 2+ concepts back to Pass 1</div>
        </div>
        <button class="reset-btn warning" onclick="resetToPass(2,1)">Reset Pass 2</button>
      </div>

      <div class="settings-row">
        <div>
          <div class="settings-row-label">Reset everything to Pass 1</div>
          <div class="settings-row-sub">Keep Pass 1 completions, reset Pass 2 and Pass 3</div>
        </div>
        <button class="reset-btn warning" onclick="resetToPass(0,1)">Keep Pass 1 only</button>
      </div>

      <div class="settings-row">
        <div>
          <div class="settings-row-label">Reset all narration progress</div>
          <div class="settings-row-sub">All concepts go back to not started</div>
        </div>
        <button class="reset-btn danger" onclick="resetAllRevisions()">Reset everything</button>
      </div>
    </div>

    <div class="settings-section">
      <div class="settings-section-title">Pass descriptions</div>
      <div style="font-size:14px;color:var(--text2);line-height:1.8">
        <div><span style="color:#b08020;font-weight:600">Pass 1</span> — First narration review. Understand what the concept is.</div>
        <div><span style="color:#1565c0;font-weight:600">Pass 2</span> — Second narration review. Reinforce the idea and key details.</div>
        <div><span style="color:#009664;font-weight:600">Pass 3</span> — Final narration review. You should be able to explain it confidently.</div>
      </div>
    </div>

    <div style="display:flex;justify-content:flex-end;margin-top:24px;">
      <button class="reset-btn neutral" onclick="closeSettings()">Close</button>
    </div>
  </div>
</div>

<div class="viewer-scrim" id="viewer-scrim" onclick="closePanel()"></div>
<div class="viewer-panel" id="viewer-panel">
  <div class="viewer-bar">
    <button class="viewer-close" onclick="closePanel()" title="Close (Esc)">&#x2715;</button>
    <span class="viewer-type read" id="viewer-type-badge">Narration</span>
    <span class="viewer-title" id="viewer-title">Loading…</span>
    <div class="viewer-zoom-wrap">
      <span class="viewer-zoom-label">Zoom</span>
      <button class="viewer-zoom-btn" onclick="adjustZoom(-10)">&#x2212;</button>
      <span class="viewer-zoom-val" id="viewer-zoom-val">100%</span>
      <button class="viewer-zoom-btn" onclick="adjustZoom(10)">&#x2b;</button>
    </div>
  </div>

  <div class="viewer-rev" id="viewer-rev">
    <div class="viewer-rev-info">
      <div class="viewer-rev-title" id="viewer-rev-title">Not started</div>
      <div class="viewer-rev-sub" id="viewer-rev-sub">Mark your narration progress through the 3 passes</div>
    </div>
    <div class="viewer-pass-btns">
      <button class="pass-btn p1" id="pbtn-1" onclick="setPassFromPanel(1)">Pass 1 — Narration</button>
      <button class="pass-btn p2" id="pbtn-2" onclick="setPassFromPanel(2)">Pass 2 — Narration Again</button>
      <button class="pass-btn p3" id="pbtn-3" onclick="setPassFromPanel(3)">Pass 3 — Final Narration</button>
      <button class="pass-btn-undo" id="pbtn-undo" onclick="setPassFromPanel(-1)" title="Undo last pass">↩</button>
    </div>
  </div>

  <div class="viewer-frame-wrap" id="viewer-frame-wrap">
    <iframe class="viewer-frame" id="viewer-iframe" src="about:blank"></iframe>
  </div>
</div>

<script>
const SPINES = {js_spines};

const LS_KEY = "awsm_passes_v1";

function loadPasses() {{
  try {{
    const raw = JSON.parse(localStorage.getItem(LS_KEY) || "{{}}");
    const m = new Map();
    Object.entries(raw).forEach(([k, v]) => m.set(parseInt(k), v));
    return m;
  }} catch {{
    return new Map();
  }}
}}

function savePasses(m) {{
  try {{
    const obj = {{}};
    m.forEach((v, k) => {{
      if (v > 0) obj[k] = v;
    }});
    localStorage.setItem(LS_KEY, JSON.stringify(obj));
  }} catch {{}}
}}

let passes = loadPasses();

function getPass(id) {{
  return passes.get(id) || 0;
}}

function setPass(id, n) {{
  if (n <= 0) passes.delete(id);
  else passes.set(id, Math.min(3, n));
  savePasses(passes);
}}

const LAYER_META = {{
  1: {{ name:"Foundations",              color:"#00b894", bg:"rgba(0,184,148,0.08)",  border:"rgba(0,184,148,0.2)" }},
  2: {{ name:"Core Mechanisms",          color:"#74b9ff", bg:"rgba(116,185,255,0.07)", border:"rgba(116,185,255,0.18)" }},
  3: {{ name:"Service Mastery",          color:"#fdcb6e", bg:"rgba(253,203,110,0.08)", border:"rgba(253,203,110,0.2)" }},
  4: {{ name:"Decision Patterns",        color:"#fd79a8", bg:"rgba(253,121,168,0.07)", border:"rgba(253,121,168,0.18)" }},
  5: {{ name:"Architectural Patterns",   color:"#a29bfe", bg:"rgba(162,155,254,0.08)", border:"rgba(162,155,254,0.2)" }},
  6: {{ name:"Exam & Interview Bridges", color:"#55efc4", bg:"rgba(85,239,196,0.07)",  border:"rgba(85,239,196,0.18)" }},
}};

const DOMAIN_COLORS = {{
  "Cloud Concepts":"#a29bfe",
  "Compute":"#74b9ff",
  "Storage":"#fdcb6e",
  "Networking":"#fd79a8",
  "Database":"#55efc4",
  "Security":"#e17055",
  "Integration":"#00b894",
  "Architecture":"#6c5ce7",
  "General":"#8b90a8",
}};

let activeFilter = {{ layer:null, domain:null, service:null }};
let statusFilter = "all";
let searchQuery = "";
let viewMode = "grouped";
let currentZoom = 100;
let currentPanelId = null;

const PASS_TITLES = ["Not started", "Pass 1 done", "Pass 2 done", "Pass 3 done ✓"];
const PASS_SUBS = [
  "Mark your narration progress through the 3 passes",
  "Pass 1 complete — ready for second narration review",
  "Pass 2 complete — ready for final narration review",
  "All 3 narration passes complete!"
];

function escapeHtml(s) {{
  return String(s ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}}

function escapeAttr(s) {{
  return escapeHtml(s);
}}

function escapeJs(s) {{
  return String(s ?? "")
    .replace(/\\\\/g, "\\\\\\\\")
    .replace(/'/g, "\\\\'")
    .replace(/"/g, '&quot;')
    .replace(/\\n/g, " ")
    .replace(/\\r/g, " ");
}}

function typeLabel(t) {{
  return {{
    mental_model:"Model",
    concept:"Concept",
    contrast:"Contrast",
    pattern:"Pattern",
    bridge:"Bridge"
  }}[t] || t;
}}

function sdClass(s) {{
  if (s.has_render && s.has_whiteboard) return "sd-full";
  if (s.has_render || s.has_whiteboard) return "sd-partial";
  return "sd-none";
}}

function sdTitle(s) {{
  if (s.has_render && s.has_whiteboard) return "Narration + Board";
  if (s.has_render) return "Narration only";
  if (s.has_whiteboard) return "Board only";
  return "Not yet available";
}}

function docIcon() {{
  return `<svg class="action-icon" viewBox="0 0 14 14" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round">
    <rect x="2" y="1" width="10" height="12" rx="1.5"/>
    <path d="M4.5 5h5M4.5 7.5h5M4.5 10h3"/>
  </svg>`;
}}

function boardIcon() {{
  return `<svg class="action-icon" viewBox="0 0 14 14" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round">
    <rect x="1" y="1" width="12" height="9" rx="1.5"/>
    <path d="M5 13h4M7 10v3"/>
  </svg>`;
}}

function makeCard(s) {{
  const pass = getPass(s.id);
  const exams = (s.exams || []).map(e => `<span class="exam-tag et-${{String(e).toLowerCase()}}">${{escapeHtml(e)}}</span>`).join("");
  const readClick = s.has_render ? `onclick="openPanel('${{s.render_path}}','${{escapeJs(s.title)}}','read',${{s.id}})"` : "";
  const boardClick = s.has_whiteboard ? `onclick="openPanel('${{s.whiteboard_path}}','${{escapeJs(s.title)}}','board',${{s.id}})"` : "";
  const passClass = pass===0 ? "" : pass===1 ? " pass1" : pass===2 ? " pass2" : " pass3";

  return `<div class="spine-card${{passClass}}" data-id="${{s.id}}">
    <div class="card-top">
      <span class="card-id">#${{String(s.id).padStart(4,"0")}}</span>
      <span class="status-dot ${{sdClass(s)}}" title="${{sdTitle(s)}}"></span>
      <span class="type-tag tt-${{escapeAttr(s.spine_type)}}">${{escapeHtml(typeLabel(s.spine_type))}}</span>
    </div>

    <div class="card-title">${{escapeHtml(s.title)}}</div>

    <div class="card-meta">
      ${{exams}}
      <span class="tier-badge">${{escapeHtml(s.tier || "")}}</span>
    </div>

    <div class="card-actions">
      <button class="action-btn read${{s.has_render ? "" : " disabled"}}" ${{readClick}}>
        ${{docIcon()}} Narration
      </button>
      <button class="action-btn board${{s.has_whiteboard ? "" : " disabled"}}" ${{boardClick}}>
        ${{boardIcon()}} Board
      </button>
    </div>
  </div>`;
}}

function makeListRow(s) {{
  const pass = getPass(s.id);

  const readBtn = s.has_render
    ? `<button class="spine-mini-btn" onclick="openPanel('${{s.render_path}}','${{escapeJs(s.title)}}','read',${{s.id}})">Narration</button>`
    : `<button class="spine-mini-btn disabled">Narration</button>`;

  const boardBtn = s.has_whiteboard
    ? `<button class="spine-mini-btn" onclick="openPanel('${{s.whiteboard_path}}','${{escapeJs(s.title)}}','board',${{s.id}})">Board</button>`
    : `<button class="spine-mini-btn disabled">Board</button>`;

  const passLabel = ["Not started", "Pass 1", "Pass 2", "Pass 3"][pass];

  return `
    <li class="spine-list-item">
      <div class="spine-list-row">
        <span class="spine-list-id">#${{String(s.id).padStart(4, "0")}}</span>
        <span class="spine-list-title">${{escapeHtml(s.title)}}</span>
        <div class="spine-list-actions">
          ${{readBtn}}
          ${{boardBtn}}
        </div>
      </div>
      <div class="spine-list-meta">
        <span class="spine-mini-tag">L${{s.layer}}</span>
        <span class="spine-mini-tag">${{escapeHtml(s.domain)}}</span>
        <span class="spine-mini-tag">${{escapeHtml(s.service)}}</span>
        <span class="spine-mini-tag">${{escapeHtml(typeLabel(s.spine_type))}}</span>
        <span class="spine-mini-tag">${{passLabel}}</span>
      </div>
    </li>
  `;
}}

function matchesFilters(s) {{
  if (activeFilter.layer && s.layer !== activeFilter.layer) return false;
  if (activeFilter.domain && s.domain !== activeFilter.domain) return false;
  if (activeFilter.service && s.service !== activeFilter.service) return false;

  const p = getPass(s.id);

  if (statusFilter === "narration" && !s.has_render) return false;
  if (statusFilter === "board" && !s.has_whiteboard) return false;
  if (statusFilter === "pending" && s.has_render) return false;
  if (statusFilter === "pass1" && p !== 1) return false;
  if (statusFilter === "pass2" && p !== 2) return false;
  if (statusFilter === "pass3" && p !== 3) return false;
  if (statusFilter === "torevise" && (p >= 3 || !s.has_render)) return false;

  if (searchQuery) {{
    const q = searchQuery;
    const hit =
      String(s.title || "").toLowerCase().includes(q) ||
      String(s.id).includes(q) ||
      String(s.domain || "").toLowerCase().includes(q) ||
      String(s.service || "").toLowerCase().includes(q) ||
      String(s.spine_type || "").toLowerCase().includes(q);

    if (!hit) return false;
  }}

  return true;
}}

function renderContent() {{
  const content = document.getElementById("content");
  const visible = SPINES.filter(matchesFilters);

  if (!visible.length) {{
    content.innerHTML = `<div class="empty"><div class="empty-icon">◎</div>No concepts match your current filters.</div>`;
    updateStats(visible);
    return;
  }}

  if (viewMode === "flat") {{
    content.innerHTML = `<div class="cards-grid flat-grid">${{visible.map(makeCard).join("")}}</div>`;
    updateStats(visible);
    return;
  }}

  if (viewMode === "list") {{
    const ordered = [...visible].sort((a, b) => a.id - b.id);
    content.innerHTML = `
      <div class="spine-list-wrap">
        <ol class="spine-list">
          ${{ordered.map(makeListRow).join("")}}
        </ol>
      </div>
    `;
    updateStats(visible);
    return;
  }}

  const byLayer = {{}};
  visible.forEach(s => {{
    if (!byLayer[s.layer]) byLayer[s.layer] = {{}};
    if (!byLayer[s.layer][s.domain]) byLayer[s.layer][s.domain] = {{}};
    if (!byLayer[s.layer][s.domain][s.service]) byLayer[s.layer][s.domain][s.service] = [];
    byLayer[s.layer][s.domain][s.service].push(s);
  }});

  let html = "";

  Object.keys(byLayer).sort((a, b) => a - b).forEach(ln => {{
    const L = LAYER_META[ln] || {{
      name: "Layer " + ln,
      color: "#888",
      bg: "rgba(128,128,128,0.08)",
      border: "rgba(128,128,128,0.2)"
    }};

    const allLayerSpines = SPINES.filter(s => s.layer == ln);
    const nPct = allLayerSpines.length ? Math.round(allLayerSpines.filter(s => s.has_render).length / allLayerSpines.length * 100) : 0;
    const bPct = allLayerSpines.length ? Math.round(allLayerSpines.filter(s => s.has_whiteboard).length / allLayerSpines.length * 100) : 0;
    const dPct = allLayerSpines.length ? Math.round(allLayerSpines.filter(s => getPass(s.id) >= 3).length / allLayerSpines.length * 100) : 0;
    const visCount = visible.filter(s => s.layer == ln).length;

    html += `<div class="layer-block" id="lb-${{ln}}">
      <div class="layer-hdr" style="background:${{L.bg}};border-color:${{L.border}}" onclick="toggleCollapse('lb-${{ln}}')">
        <span class="layer-num" style="color:${{L.color}}">L${{ln}}</span>
        <div class="layer-info">
          <div class="layer-name">${{escapeHtml(L.name)}}</div>
          <div class="layer-meta" style="color:${{L.color}}">${{visCount}} concept${{visCount!==1?"s":""}}</div>
        </div>
        <div class="layer-meters">
          <div class="meter-row">
            <span class="meter-lbl" style="color:${{L.color}}">Narration</span>
            <div class="meter-track"><div class="meter-fill" style="width:${{nPct}}%;background:${{L.color}}"></div></div>
            <span class="meter-n" style="color:${{L.color}}">${{nPct}}%</span>
          </div>
          <div class="meter-row">
            <span class="meter-lbl" style="color:${{L.color}}">Boards</span>
            <div class="meter-track"><div class="meter-fill" style="width:${{bPct}}%;background:${{L.color}};opacity:0.55"></div></div>
            <span class="meter-n" style="color:${{L.color}}">${{bPct}}%</span>
          </div>
          <div class="meter-row">
            <span class="meter-lbl" style="color:#00b894">Done</span>
            <div class="meter-track"><div class="meter-fill" style="width:${{dPct}}%;background:#00b894"></div></div>
            <span class="meter-n" style="color:#00b894">${{dPct}}%</span>
          </div>
        </div>
        <span class="layer-chevron">›</span>
      </div>
      <div class="layer-body">`;

    Object.keys(byLayer[ln]).sort().forEach(dn => {{
      const dc = DOMAIN_COLORS[dn] || "#8b90a8";
      const domainVisible = Object.values(byLayer[ln][dn]).flat().length;
      const domainKey = dn.replace(/[^a-zA-Z0-9]/g, "_");

      html += `<div class="domain-block" id="db-${{ln}}-${{domainKey}}">
        <div class="domain-hdr" onclick="toggleCollapse('db-${{ln}}-${{domainKey}}')">
          <span class="domain-accent" style="background:${{dc}}"></span>
          <span class="domain-name">${{escapeHtml(dn)}}</span>
          <span class="domain-count">${{domainVisible}}</span>
          <span class="domain-chevron">›</span>
        </div>
        <div class="domain-body">`;

      Object.keys(byLayer[ln][dn]).sort().forEach(svc => {{
        const svcCards = byLayer[ln][dn][svc];
        const svcKey = svc.replace(/[^a-zA-Z0-9]/g, "_");

        html += `<div class="service-block" id="sb-${{ln}}-${{domainKey}}-${{svcKey}}">
          <div class="service-hdr" onclick="toggleCollapse('sb-${{ln}}-${{domainKey}}-${{svcKey}}')">
            <span class="service-tag">${{escapeHtml(svc)}}</span>
            <span class="service-count">${{svcCards.length}} concept${{svcCards.length!==1?"s":""}}</span>
            <span class="service-chevron">›</span>
          </div>
          <div class="service-cards">
            <div class="cards-grid">${{svcCards.map(makeCard).join("")}}</div>
          </div>
        </div>`;
      }});

      html += `</div></div>`;
    }});

    html += `</div></div>`;
  }});

  content.innerHTML = html;
  updateStats(visible);
  updateBreadcrumb();
}}

function toggleCollapse(id) {{
  document.getElementById(id)?.classList.toggle("collapsed");
}}

function updateStats(visible) {{
  const v = visible || SPINES.filter(matchesFilters);

  document.getElementById("st-total").textContent = v.length;
  document.getElementById("st-rendered").textContent = v.filter(s => s.has_render).length;
  document.getElementById("st-boards").textContent = v.filter(s => s.has_whiteboard).length;

  const completedCount = SPINES.filter(s => getPass(s.id) >= 3).length;
  const anyPassCount = SPINES.filter(s => getPass(s.id) > 0).length;
  const pct = SPINES.length ? Math.round(completedCount / SPINES.length * 100) : 0;
  const startedPct = SPINES.length ? Math.round(anyPassCount / SPINES.length * 100) : 0;

  document.getElementById("st-revised").textContent = completedCount;
  document.getElementById("rev-fill").style.width = startedPct + "%";
  document.getElementById("rev-pct").textContent = pct + "% ✓";

  updateFooter();
}}

function updateFooter() {{
  const total = SPINES.length;
  const p1count = SPINES.filter(s => getPass(s.id) === 1).length;
  const p2count = SPINES.filter(s => getPass(s.id) === 2).length;
  const p3count = SPINES.filter(s => getPass(s.id) === 3).length;
  const started = p1count + p2count + p3count;

  const p1w = total ? (p1count / total * 100).toFixed(1) : 0;
  const p2w = total ? (p2count / total * 100).toFixed(1) : 0;
  const p3w = total ? (p3count / total * 100).toFixed(1) : 0;

  document.getElementById("footer-pct").textContent = (total ? Math.round(p3count / total * 100) : 0) + "%";
  document.getElementById("footer-sub").textContent =
    p3count + " completed all 3 narrations · " +
    p2count + " pass 2 · " +
    p1count + " pass 1 · " +
    (total - started) + " not started";

  const s1 = document.getElementById("footer-seg1");
  const s2 = document.getElementById("footer-seg2");
  const s3 = document.getElementById("footer-seg3");
  if (s1) s1.style.width = p1w + "%";
  if (s2) s2.style.width = p2w + "%";
  if (s3) s3.style.width = p3w + "%";

  const layersEl = document.getElementById("footer-layers");
  if (!layersEl) return;

  const layerNums = [...new Set(SPINES.map(s => s.layer))].sort((a, b) => a - b);
  const L_COLORS = {{
    1:"#00b894",
    2:"#74b9ff",
    3:"#fdcb6e",
    4:"#fd79a8",
    5:"#a29bfe",
    6:"#55efc4"
  }};

  layersEl.innerHTML = layerNums.map(ln => {{
    const ls = SPINES.filter(s => s.layer === ln);
    const lDone = ls.filter(s => getPass(s.id) >= 3).length;
    const lPct = ls.length ? Math.round(lDone / ls.length * 100) : 0;
    const color = L_COLORS[ln] || "#888";

    return `<div class="footer-layer-stat">
      <span class="footer-layer-dot" style="background:${{color}}"></span>
      <div class="footer-layer-bar-wrap">
        <div class="footer-layer-fill" style="width:${{lPct}}%;background:${{color}}"></div>
      </div>
      <span class="footer-layer-label">L${{ln}} ${{lDone}}/${{ls.length}}</span>
    </div>`;
  }}).join("");
}}

function updateBreadcrumb() {{
  const bc = document.getElementById("breadcrumb");
  const parts = [];

  if (activeFilter.layer || activeFilter.domain || activeFilter.service) {{
    parts.push(`<span class="bc-item" onclick="clearFilter('all')">All layers</span>`);
  }} else {{
    parts.push(`<span class="bc-current">All layers</span>`);
  }}

  if (activeFilter.layer) {{
    const L = LAYER_META[activeFilter.layer];
    if (activeFilter.domain || activeFilter.service) {{
      parts.push(`<span class="bc-sep">›</span>`);
      parts.push(`<span class="bc-item" onclick="clearFilter('domain')">L${{activeFilter.layer}} ${{escapeHtml(L?.name || "")}}</span>`);
    }} else {{
      parts.push(`<span class="bc-sep">›</span>`);
      parts.push(`<span class="bc-current">L${{activeFilter.layer}} ${{escapeHtml(L?.name || "")}}</span>`);
    }}
  }}

  if (activeFilter.domain) {{
    if (activeFilter.service) {{
      parts.push(`<span class="bc-sep">›</span>`);
      parts.push(`<span class="bc-item" onclick="clearFilter('service')">${{escapeHtml(activeFilter.domain)}}</span>`);
    }} else {{
      parts.push(`<span class="bc-sep">›</span>`);
      parts.push(`<span class="bc-current">${{escapeHtml(activeFilter.domain)}}</span>`);
    }}
  }}

  if (activeFilter.service) {{
    parts.push(`<span class="bc-sep">›</span>`);
    parts.push(`<span class="bc-current">${{escapeHtml(activeFilter.service)}}</span>`);
  }}

  bc.innerHTML = parts.join(" ");
}}

function clearFilter(level) {{
  if (level === "all") activeFilter = {{ layer:null, domain:null, service:null }};
  if (level === "domain") activeFilter = {{ layer:activeFilter.layer, domain:null, service:null }};
  if (level === "service") activeFilter = {{ layer:activeFilter.layer, domain:activeFilter.domain, service:null }};
  renderContent();
  buildSidenav();
}}

function setFilter(layer, domain, service) {{
  activeFilter = {{ layer: layer || null, domain: domain || null, service: service || null }};
  renderContent();
}}

function setView(v) {{
  viewMode = v;
  document.getElementById("vbtn-grouped").classList.toggle("active", v === "grouped");
  document.getElementById("vbtn-flat").classList.toggle("active", v === "flat");
  document.getElementById("vbtn-list").classList.toggle("active", v === "list");
  renderContent();
}}

function updateCardBadge(id) {{
  const card = document.querySelector(`.spine-card[data-id="${{id}}"]`);
  if (!card) return;

  const p = getPass(id);
  card.className = card.className.replace(/\\bpass[123]\\b/g, "").trim();
  if (p === 1) card.classList.add("pass1");
  if (p === 2) card.classList.add("pass2");
  if (p === 3) card.classList.add("pass3");
}}

function buildSidenav() {{
  const nav = document.getElementById("sidenav");
  const layerNums = [...new Set(SPINES.map(s => s.layer))].sort((a, b) => a - b);

  nav.innerHTML = layerNums.map(ln => {{
    const L = LAYER_META[ln] || {{ name: "Layer " + ln, color: "#888" }};
    const domains = [...new Set(SPINES.filter(s => s.layer === ln).map(s => s.domain))].sort();
    const isLayerActive = activeFilter.layer === ln;

    return `<div class="sn-section">
      <div class="sn-layer-item${{isLayerActive ? " expanded" : ""}}"
        style="${{isLayerActive ? "border-left-color:" + L.color : ""}}"
        onclick="toggleSnLayer(this, ${{ln}})">
        <span class="sn-ldot" style="background:${{L.color}}"></span>
        <span class="sn-lname">L${{ln}} ${{escapeHtml(L.name)}}</span>
        <span class="sn-lcount">${{SPINES.filter(s => s.layer === ln).length}}</span>
        <span class="sn-chevron">›</span>
      </div>
      <div class="sn-children">
        ${{domains.map(dn => {{
          const svcs = [...new Set(SPINES.filter(s => s.layer === ln && s.domain === dn).map(s => s.service))].sort();
          const isDomActive = activeFilter.domain === dn && activeFilter.layer === ln;
          const dc = DOMAIN_COLORS[dn] || "#8b90a8";

          return `<div class="sn-domain-item${{isDomActive ? " expanded sel" : ""}}"
            onclick="toggleSnDomain(this, ${{ln}}, '${{escapeJs(dn)}}')">
            <span class="sn-domain-dot" style="background:${{dc}}"></span>
            <span class="sn-dname">${{escapeHtml(dn)}}</span>
            <span class="sn-dcount">${{SPINES.filter(s => s.layer === ln && s.domain === dn).length}}</span>
            <span class="sn-chevron" style="font-size:13px">›</span>
          </div>
          <div class="sn-svc-children">
            ${{svcs.map(sv => {{
              const isActive = activeFilter.service === sv && activeFilter.domain === dn;
              return `<div class="sn-svc-item${{isActive ? " sel" : ""}}"
                onclick="setFilter(${{ln}}, '${{escapeJs(dn)}}', '${{escapeJs(sv)}}')">
                <span class="sn-svc-dot"></span>${{escapeHtml(sv)}}
              </div>`;
            }}).join("")}}
          </div>`;
        }}).join("")}}
      </div>
    </div>`;
  }}).join("");
}}

function toggleSnLayer(el, ln) {{
  const isExpanded = el.classList.contains("expanded");
  if (isExpanded) {{
    el.classList.remove("expanded");
    clearFilter("all");
  }} else {{
    el.classList.add("expanded");
    setFilter(ln, null, null);
    buildSidenav();
  }}
}}

function toggleSnDomain(el, ln, dn) {{
  const isExpanded = el.classList.contains("expanded");
  if (isExpanded) {{
    el.classList.remove("expanded");
    setFilter(ln, null, null);
    buildSidenav();
  }} else {{
    setFilter(ln, dn, null);
    buildSidenav();
  }}
}}

function openSettings() {{
  document.getElementById("settings-overlay").classList.add("open");
}}

function closeSettings() {{
  document.getElementById("settings-overlay").classList.remove("open");
}}

function closeSettingsOnOverlay(e) {{
  if (e.target === document.getElementById("settings-overlay")) closeSettings();
}}

function resetAllRevisions() {{
  if (!confirm("Reset ALL narration progress? This cannot be undone.")) return;

  passes.clear();
  savePasses(passes);

  document.querySelectorAll(".spine-card").forEach(card => {{
    const id = parseInt(card.dataset.id);
    updateCardBadge(id);
  }});

  updateStats();
  renderContent();
  closeSettings();
}}

function resetToPass(fromPass, toPass) {{
  let msg;
  if (fromPass === 0) msg = "Reset all Pass 2 and Pass 3 down to Pass 1?";
  else if (fromPass === 2) msg = "Reset all Pass 2+ back to Pass 1?";
  else msg = `Reset all Pass ${{fromPass}} down to Pass ${{toPass}}?`;

  if (!confirm(msg)) return;

  passes.forEach((v, k) => {{
    if (fromPass === 0) {{
      if (v > 1) setPass(k, 1);
    }} else {{
      if (v >= fromPass) setPass(k, toPass);
    }}
  }});

  savePasses(passes);

  document.querySelectorAll(".spine-card").forEach(card => {{
    updateCardBadge(parseInt(card.dataset.id));
  }});

  updateStats();
  renderContent();
  closeSettings();
}}

const LS_THEME = "awsm_theme";

function setTheme(t) {{
  document.documentElement.setAttribute("data-theme", t);
  localStorage.setItem(LS_THEME, t);
  ["slate","light","warm"].forEach(n => {{
    document.getElementById("tbtn-" + n)?.classList.toggle("active", n === t);
  }});
}}

(function initTheme() {{
  const saved = localStorage.getItem(LS_THEME) || "slate";
  setTheme(saved);
}})();

function refreshPanelPassUI() {{
  const p = getPass(currentPanelId);
  const title = document.getElementById("viewer-rev-title");
  const sub = document.getElementById("viewer-rev-sub");

  if (title) title.textContent = PASS_TITLES[p];
  if (sub) sub.textContent = PASS_SUBS[p];

  [1,2,3].forEach(n => {{
    const btn = document.getElementById("pbtn-" + n);
    if (!btn) return;
    btn.className = "pass-btn p" + n;
    if (p >= n) btn.classList.add("done");
    else if (p === n - 1) btn.classList.add("current");
  }});

  const undo = document.getElementById("pbtn-undo");
  if (undo) undo.disabled = (p === 0);
}}

function openPanel(filePath, title, type, spineId) {{
  const panel = document.getElementById("viewer-panel");
  const scrim = document.getElementById("viewer-scrim");
  const body = document.querySelector(".body");
  const iframe = document.getElementById("viewer-iframe");
  const badge = document.getElementById("viewer-type-badge");
  const ttl = document.getElementById("viewer-title");

  currentPanelId = spineId;

  badge.textContent = type === "read" ? "Narration" : "Board";
  badge.className = "viewer-type " + type;
  ttl.textContent = title;

  refreshPanelPassUI();
  iframe.src = "file://" + filePath;

  panel.classList.add("open");
  scrim.classList.add("open");
  body.classList.add("panel-open");

  setTimeout(() => applyZoom(currentZoom), 30);
}}

function setPassFromPanel(n) {{
  if (currentPanelId === null) return;

  if (n === -1) {{
    const p = getPass(currentPanelId);
    if (p > 0) setPass(currentPanelId, p - 1);
  }} else {{
    setPass(currentPanelId, n);
  }}

  updateCardBadge(currentPanelId);
  refreshPanelPassUI();
  updateStats();

  if (["pass1","pass2","pass3","torevise"].includes(statusFilter)) {{
    renderContent();
  }}
}}

function closePanel() {{
  const panel = document.getElementById("viewer-panel");
  const scrim = document.getElementById("viewer-scrim");
  const body = document.querySelector(".body");
  const iframe = document.getElementById("viewer-iframe");

  panel.classList.remove("open");
  scrim.classList.remove("open");
  body.classList.remove("panel-open");

  setTimeout(() => {{
    iframe.src = "about:blank";
  }}, 320);
}}

function adjustZoom(delta) {{
  currentZoom = Math.min(200, Math.max(60, currentZoom + delta));
  applyZoom(currentZoom);
}}

function applyZoom(pct) {{
  currentZoom = pct;
  document.getElementById("viewer-zoom-val").textContent = pct + "%";

  const iframe = document.getElementById("viewer-iframe");
  const wrap = document.getElementById("viewer-frame-wrap");

  const wrapStyle = getComputedStyle(wrap);
  const padX = parseFloat(wrapStyle.paddingLeft) + parseFloat(wrapStyle.paddingRight);
  const padY = parseFloat(wrapStyle.paddingTop) + parseFloat(wrapStyle.paddingBottom);

  const availW = Math.max(200, wrap.clientWidth - padX);
  const availH = Math.max(200, wrap.clientHeight - padY);
  const scale = pct / 100;

  iframe.style.width = Math.round(availW / scale) + "px";
  iframe.style.height = Math.round(availH / scale) + "px";
  iframe.style.transform = `scale(${{scale}})`;
}}

window.addEventListener("resize", () => {{
  if (document.getElementById("viewer-panel").classList.contains("open")) {{
    applyZoom(currentZoom);
  }}
}});

document.addEventListener("keydown", e => {{
  if (e.key === "Escape") {{
    closePanel();
    closeSettings();
  }}
}});

document.getElementById("search-input").addEventListener("input", e => {{
  searchQuery = e.target.value.toLowerCase().trim();
  renderContent();
}});

document.querySelectorAll(".fpill[data-sf]").forEach(btn => {{
  btn.addEventListener("click", () => {{
    document.querySelectorAll(".fpill[data-sf]").forEach(b => b.classList.remove("active"));
    btn.classList.add("active");
    statusFilter = btn.dataset.sf;
    renderContent();
  }});
}});

buildSidenav();
renderContent();
updateBreadcrumb();
updateFooter();
</script>

</body>
</html>"""


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate dashboard.html from concept_spines.yaml")
    parser.add_argument("--out", default=None, help="Output HTML file (default: output/dashboard.html)")
    parser.add_argument("--open", action="store_true", help="Open in browser after building")
    args = parser.parse_args()

    print("Loading spines…")
    spines = _load_spines()
    print(f"  {len(spines)} spines loaded")

    print("Checking output files…")
    enriched = build_spine_data(spines)
    rendered_count = sum(1 for s in enriched if s["has_render"])
    wb_count = sum(1 for s in enriched if s["has_whiteboard"])
    narration_count = sum(1 for s in enriched if s["has_narration"])
    print(f"  {rendered_count} narration pages  |  {wb_count} whiteboards  |  {narration_count} narration files")

    print("Generating HTML…")
    html = generate_html(enriched)

    root = Path(__file__).resolve().parent.parent
    default_out = root / "output" / "dashboard.html"
    out_path = Path(args.out) if args.out else default_out
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")
    print(f"  Written → {out_path.resolve()}")

    if args.open:
        import webbrowser
        webbrowser.open(out_path.resolve().as_uri())
        print("  Opened in browser")


if __name__ == "__main__":
    main()