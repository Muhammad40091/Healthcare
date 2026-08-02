"""Safe Mode Controller.

STATUS: interface-only. On integrity breach or confidence collapse, this
module suspends the AI layer system-wide while billing continues on
deterministic rules only (see docs/failure-modes.md for the four
operating modes: Full AI, Degraded AI, Safe Mode, Bypass Mode).
"""
from __future__ import annotations

from enum import Enum


class OperatingMode(str, Enum):
    FULL_AI = "full_ai"
    DEGRADED_AI = "degraded_ai"
    SAFE_MODE = "safe_mode"
    BYPASS_MODE = "bypass_mode"


_current_mode = OperatingMode.FULL_AI


def get_mode() -> OperatingMode:
    return _current_mode


def trigger_safe_mode(reason: str) -> None:
    global _current_mode
    _current_mode = OperatingMode.SAFE_MODE
    # TODO(architect): page on-call, write incident record, notify RCM Director
    print(f"[SAFE MODE TRIGGERED] {reason}")


def restore_full_ai(approved_by: str) -> None:
    global _current_mode
    _current_mode = OperatingMode.FULL_AI
    print(f"[FULL AI MODE RESTORED] approved by {approved_by}")
