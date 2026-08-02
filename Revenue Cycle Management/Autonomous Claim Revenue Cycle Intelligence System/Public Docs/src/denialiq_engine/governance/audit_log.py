"""Audit Log Service.

Every agent action, HITL decision, and override is written to an
immutable, append-only event store. STATUS: prototype — this reference
implementation writes newline-delimited JSON to a local file; production
deployments should back this with an append-only store (e.g. an
event-sourced DB, WORM S3 bucket, or dedicated audit log service) with
tamper-evidence (hash chaining) suitable for OIG/payer audit defense.
"""
from __future__ import annotations

import hashlib
import json
import pathlib
from datetime import datetime
from typing import Any

from denialiq_engine.schemas.claim import AgentOutput

AUDIT_LOG_PATH = pathlib.Path("var/audit_log.ndjson")
_last_hash = "0" * 64


def _event_hash(event: dict[str, Any], prev_hash: str) -> str:
    payload = json.dumps(event, sort_keys=True, default=str) + prev_hash
    return hashlib.sha256(payload.encode()).hexdigest()


def log_agent_action(agent_name: str, claim_id: str, output: AgentOutput) -> None:
    """Append an agent decision to the audit log with hash chaining."""
    global _last_hash
    event = {
        "type": "agent_action",
        "agent_name": agent_name,
        "claim_id": claim_id,
        "confidence": output.confidence,
        "rationale": output.rationale,
        "tool_calls": output.tool_calls,
        "timestamp": datetime.utcnow().isoformat(),
    }
    event["prev_hash"] = _last_hash
    event["hash"] = _event_hash(event, _last_hash)
    _last_hash = event["hash"]
    _append(event)


def log_hitl_decision(claim_id: str, tier: int, override: bool, rationale: str | None) -> None:
    global _last_hash
    event = {
        "type": "hitl_decision",
        "claim_id": claim_id,
        "tier": tier,
        "override": override,
        "rationale": rationale,
        "timestamp": datetime.utcnow().isoformat(),
    }
    event["prev_hash"] = _last_hash
    event["hash"] = _event_hash(event, _last_hash)
    _last_hash = event["hash"]
    _append(event)


def _append(event: dict[str, Any]) -> None:
    AUDIT_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with AUDIT_LOG_PATH.open("a") as f:
        f.write(json.dumps(event, default=str) + "\n")


def verify_chain_integrity(log_path: pathlib.Path = AUDIT_LOG_PATH) -> bool:
    """Recompute the hash chain and confirm no events were altered/removed."""
    if not log_path.exists():
        return True
    prev = "0" * 64
    with log_path.open() as f:
        for line in f:
            event = json.loads(line)
            recorded_hash = event.pop("hash")
            expected = _event_hash(event, prev)
            if expected != recorded_hash:
                return False
            prev = recorded_hash
    return True
