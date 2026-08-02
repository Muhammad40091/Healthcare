"""RBAC Engine — tool-call access control gate.

STATUS: prototype. No agent tool call executes without passing this gate.
Production version should back roles/permissions with the client's IAM
system (e.g. SSO group claims) rather than the static map below.
"""
from __future__ import annotations

from functools import wraps
from typing import Callable

# agent_name -> set of tool names it is permitted to call
ROLE_PERMISSIONS: dict[str, set[str]] = {
    "cdi_intelligence": {"read_clinical_notes", "read_hcc_reference"},
    "coding_accuracy": {"read_ncci_edits", "read_cpt_reference"},
    "prior_auth": {"check_prior_auth_status", "read_wiser_criteria"},
    "appeal_intelligence": {"read_835_remittance", "read_payer_appeal_requirements", "draft_appeal_letter"},
    "payer_adversarial_intelligence": {"read_denial_history", "read_payer_behavior_timeline"},
    "ar_aging": {"read_ar_ledger", "score_collectability"},
    "pfx": {"read_patient_financial_profile", "generate_payment_plan"},
    "payer_contract_intelligence": {"read_contract_rates", "read_835_remittance"},
}


class RBACDenied(PermissionError):
    pass


def require_permission(agent_name: str, tool_name: str) -> None:
    allowed = ROLE_PERMISSIONS.get(agent_name, set())
    if tool_name not in allowed:
        raise RBACDenied(f"Agent '{agent_name}' is not permitted to call tool '{tool_name}'")


def gated_tool(agent_name: str) -> Callable:
    """Decorator: wraps a tool function with an RBAC check for the calling agent."""

    def decorator(tool_fn: Callable) -> Callable:
        @wraps(tool_fn)
        def wrapper(*args, **kwargs):
            require_permission(agent_name, tool_fn.__name__)
            return tool_fn(*args, **kwargs)

        return wrapper

    return decorator
