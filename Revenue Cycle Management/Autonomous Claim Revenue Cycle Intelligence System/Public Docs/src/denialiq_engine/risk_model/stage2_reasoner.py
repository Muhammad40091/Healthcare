"""Stage 2 — LLM reasoning layer for medium/high-risk claims (production).

STATUS: interface-only. Invoked only for claims scoring above the Stage 1
threshold (~35% of volume per case study estimate). Combines claim
context + RAG-retrieved payer policy excerpts + CDI findings into a
policy-grounded denial risk rationale and ranked correction
recommendations. Output must be validated by the deterministic rule
engine before surfacing to a biller (see docs/hallucination-guardrails.md).
"""
from __future__ import annotations


class Stage2Reasoner:
    def __init__(self, llm_client, rag_retriever):
        self.llm_client = llm_client
        self.rag_retriever = rag_retriever

    def reason(self, claim_context: dict) -> dict:
        raise NotImplementedError(
            "Implement: retrieve policy context -> prompt fine-tuned reasoning LLM "
            "-> validate structured output -> cross-check against rule engine"
        )
