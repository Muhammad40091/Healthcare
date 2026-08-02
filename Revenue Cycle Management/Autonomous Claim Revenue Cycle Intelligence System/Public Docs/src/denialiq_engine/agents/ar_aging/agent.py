"""ar_aging agent — production implementation.

Autonomous 14-day threshold monitoring with collectability-ranked work queues. HITL-governed.

STATUS: interface-only (see STATUS.md). This class defines the contract the
orchestrator (agents/claim_orchestrator) invokes. Fill in `run()` with real
tool calls, prompt invocation, and rule-engine cross-validation before
promoting this module status to prototype/production.
"""
from __future__ import annotations

from denialiq_engine.schemas.claim import AgentOutput, Claim
from denialiq_engine.governance.audit_log import log_agent_action


class ArAgingAgent:
    name = "ar_aging"

    def __init__(self, config: dict | None = None):
        self.config = config or {}

    def run(self, claim: Claim) -> AgentOutput:
        """Process a claim and return a validated AgentOutput.

        TODO(architect): implement real logic. Every production call must:
          1. Retrieve any needed RAG / tool context
          2. Invoke the reasoning LLM (or deterministic rule engine) with a
             reviewed prompt from prompts.py
          3. Validate the structured output against AgentOutput
          4. Call log_agent_action() before returning
        """
        raise NotImplementedError(f"{self.name} agent logic not yet implemented — see STATUS.md")

    def _log(self, claim_id: str, output: AgentOutput) -> None:
        log_agent_action(agent_name=self.name, claim_id=claim_id, output=output)
