"""Pipeline Integrity Monitor — checksum validation, anomaly detection,
and data-poisoning detection on ingestion streams (835 remittance, claim
feeds).

STATUS: interface-only. On integrity breach, this module must trigger the
Safe Mode Controller (see safe_mode.py) rather than allow degraded data to
reach the model pipeline.
"""
from __future__ import annotations

import hashlib


def checksum(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def verify_checksum(payload: bytes, expected: str) -> bool:
    return checksum(payload) == expected


class IntegrityBreach(Exception):
    pass


def validate_ingestion_batch(payload: bytes, expected_checksum: str) -> None:
    if not verify_checksum(payload, expected_checksum):
        raise IntegrityBreach("Checksum mismatch on ingestion batch — triggering Safe Mode")
