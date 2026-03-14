"""
utils/call_plan.py
Single source of truth for the 51-call outline plan.

Imported by:
  - 02_pipeline/run_outline.py  — drives the API calls
  - 02_pipeline/run.py          — resolves spine ID → layer/part folder name

Each entry: (call_name, domain_value, start_id, target_count)
"""

from __future__ import annotations

import re


# ---------------------------------------------------------------------------
# The 51-call plan
# ---------------------------------------------------------------------------

CALL_PLAN: list[tuple[str, str, int, int]] = [
    # Layer 1 — Foundations (50 spines)
    ("Layer 1 Part 1: The 8 Big Ideas of Cloud and AWS",                  "Cloud Concepts",                1,   20),
    ("Layer 1 Part 2: AWS Design Philosophy and Global Infrastructure",   "Cloud Concepts",                21,  20),
    ("Layer 1 Part 3: Shared Responsibility and the Cost Model",          "Cloud Concepts",                41,  10),
    # Layer 2 — Core Mechanisms (100 spines)
    ("Layer 2 Part 1: IAM and Security Mechanisms",                       "Security and Compliance",       51,  20),
    ("Layer 2 Part 2: Networking and VPC Mechanisms",                     "Cloud Technology and Services", 71,  20),
    ("Layer 2 Part 3: Compute and Serverless Mechanisms",                 "Cloud Technology and Services", 91,  20),
    ("Layer 2 Part 4: Storage and Database Mechanisms",                   "Cloud Technology and Services", 111, 20),
    ("Layer 2 Part 5: Integration, Messaging and Delivery Mechanisms",    "Cloud Technology and Services", 131, 20),
    # Layer 3 — Service Mastery (350 spines)
    ("Layer 3 Part 1: EC2 — Elastic Compute Cloud",                       "Cloud Technology and Services", 151, 20),
    ("Layer 3 Part 2: Containers and Serverless Compute",                 "Cloud Technology and Services", 171, 20),
    ("Layer 3 Part 3: S3 — Simple Storage Service",                       "Cloud Technology and Services", 191, 20),
    ("Layer 3 Part 4: Block, File and Archival Storage",                  "Cloud Technology and Services", 211, 20),
    ("Layer 3 Part 5: RDS and Relational Databases",                      "Cloud Technology and Services", 231, 20),
    ("Layer 3 Part 6: DynamoDB and NoSQL Databases",                      "Cloud Technology and Services", 251, 20),
    ("Layer 3 Part 7: Speciality Databases and Data Migration",           "Cloud Technology and Services", 271, 20),
    ("Layer 3 Part 8: VPC and Core Networking",                           "Cloud Technology and Services", 291, 20),
    ("Layer 3 Part 9: Content Delivery and DNS",                          "Cloud Technology and Services", 311, 20),
    ("Layer 3 Part 10: IAM, KMS and Core Security Services",              "Security and Compliance",       331, 20),
    ("Layer 3 Part 11: Threat Detection, Compliance and Audit Services",  "Security and Compliance",       351, 20),
    ("Layer 3 Part 12: SQS, SNS, EventBridge and Messaging",              "Cloud Technology and Services", 371, 20),
    ("Layer 3 Part 13: API Gateway, Step Functions and Workflow",         "Cloud Technology and Services", 391, 20),
    ("Layer 3 Part 14: Analytics — Kinesis, Athena, EMR, Glue",          "Cloud Technology and Services", 411, 20),
    ("Layer 3 Part 15: BI, ML and AI Services",                           "Cloud Technology and Services", 431, 20),
    ("Layer 3 Part 16: Developer Tools and CI/CD",                        "Cloud Technology and Services", 451, 20),
    ("Layer 3 Part 17: Management, Monitoring and Governance Services",   "Cloud Technology and Services", 471, 20),
    ("Layer 3 Part 18: Billing, Cost and Support Services",               "Billing, Pricing, and Support", 491, 10),
    # Layer 4 — Decision Patterns (250 spines)
    ("Layer 4 Part 1: Resilience and High Availability Decisions",        "Cross-Domain",                  501, 20),
    ("Layer 4 Part 2: Fault Tolerance and Disaster Recovery Decisions",   "Cross-Domain",                  521, 20),
    ("Layer 4 Part 3: Scalability and Performance Decisions",             "Cross-Domain",                  541, 20),
    ("Layer 4 Part 4: Compute Selection Decisions",                       "Cross-Domain",                  561, 20),
    ("Layer 4 Part 5: Storage Selection Decisions",                       "Cross-Domain",                  581, 20),
    ("Layer 4 Part 6: Database Selection Decisions",                      "Cross-Domain",                  601, 20),
    ("Layer 4 Part 7: Networking and Connectivity Decisions",             "Cross-Domain",                  621, 20),
    ("Layer 4 Part 8: Security Architecture Decisions",                   "Cross-Domain",                  641, 20),
    ("Layer 4 Part 9: Integration and Messaging Decisions",               "Cross-Domain",                  661, 20),
    ("Layer 4 Part 10: Cost Optimisation Decisions",                      "Cross-Domain",                  681, 20),
    ("Layer 4 Part 11: Serverless vs Container vs EC2 Decisions",         "Cross-Domain",                  701, 20),
    ("Layer 4 Part 12: Data and Analytics Decisions",                     "Cross-Domain",                  721, 20),
    ("Layer 4 Part 13: Migration Strategy Decisions",                     "Cross-Domain",                  741, 10),
    # Layer 5 — Architectural Patterns (180 spines)
    ("Layer 5 Part 1: Web Application Patterns",                          "Cross-Domain",                  751, 20),
    ("Layer 5 Part 2: Serverless and Event-Driven Patterns",              "Cross-Domain",                  771, 20),
    ("Layer 5 Part 3: Data Lake and Analytics Patterns",                  "Cross-Domain",                  791, 20),
    ("Layer 5 Part 4: Microservices and Decoupling Patterns",             "Cross-Domain",                  811, 20),
    ("Layer 5 Part 5: Disaster Recovery and Business Continuity Patterns","Cross-Domain",                  831, 20),
    ("Layer 5 Part 6: Hybrid and On-Premises Integration Patterns",       "Cross-Domain",                  851, 20),
    ("Layer 5 Part 7: Multi-Account and Governance Patterns",             "Cross-Domain",                  871, 20),
    ("Layer 5 Part 8: Migration and Modernisation Patterns",              "Cross-Domain",                  891, 20),
    ("Layer 5 Part 9: Cost Optimisation at Scale Patterns",               "Cross-Domain",                  911, 20),
    # Layer 6 — Exam and Interview Bridges (70 spines)
    ("Layer 6 Part 1: CCP Exam Bridges and Common Traps",                 "Cross-Domain",                  931, 20),
    ("Layer 6 Part 2: SAA Exam Bridges and Scenario Frameworks",          "Cross-Domain",                  951, 20),
    ("Layer 6 Part 3: SAP and Interview Bridges",                         "Cross-Domain",                  971, 30),
]


# ---------------------------------------------------------------------------
# Folder name helpers
# ---------------------------------------------------------------------------

def _slugify(text: str) -> str:
    """Convert call name prefix to a folder-safe string."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return text.strip("_")


def get_part_folder(spine_id: int) -> str:
    """
    Return the nested folder name for a spine, e.g. 'layer_3/part_7'.
    Derived by finding which call in CALL_PLAN the spine_id falls into.
    Raises ValueError if spine_id is out of range for all calls.
    """
    for call_name, _domain, start_id, target in CALL_PLAN:
        end_id = start_id + target - 1
        if start_id <= spine_id <= end_id:
            # Parse layer and part numbers from the call name
            # e.g. "Layer 3 Part 7: Speciality Databases..."
            m = re.match(r"Layer\s+(\d+)\s+Part\s+(\d+)", call_name, re.IGNORECASE)
            if m:
                layer = int(m.group(1))
                part  = int(m.group(2))
                return f"layer_{layer}/part_{part}"
            # Fallback: slugify the prefix before the colon
            prefix = call_name.split(":")[0].strip()
            return _slugify(prefix)
    raise ValueError(f"spine_id={spine_id} not found in any CALL_PLAN entry")


def get_call_for_spine(spine_id: int) -> tuple[str, str, int, int]:
    """Return the full CALL_PLAN entry for a given spine_id."""
    for entry in CALL_PLAN:
        call_name, domain, start_id, target = entry
        if start_id <= spine_id <= start_id + target - 1:
            return entry
    raise ValueError(f"spine_id={spine_id} not found in CALL_PLAN")