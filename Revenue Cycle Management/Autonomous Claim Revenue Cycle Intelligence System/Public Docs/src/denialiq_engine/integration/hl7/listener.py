"""HL7 v2 message listener (ADT, ORU feeds).

STATUS: interface-only. Feeds into Debezium CDC + Kafka streaming per
Phase 1 architecture.
"""
from __future__ import annotations


def parse_hl7_message(raw_message: str) -> dict:
    raise NotImplementedError("Wire to an HL7 v2 parsing library (e.g. python-hl7)")
