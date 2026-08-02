"""Production 9-agent LangGraph orchestrator.

STATUS: prototype. This wires the full module set described in the case
study. Individual agent nodes call into agents/<module>/agent.py, which
are currently interface-only (see each module's STATUS.md) and must be
implemented before this graph can run end-to-end against real claims.

Shadow Mode: per the Cold-Start Protocol, new client deployments run this
graph in observe-only mode for 90 days (score and log, but do not surface
recommendations or route to HITL) before going live. Toggle via
client_config.

Docstring:
    See diagrams/architecture.md (`## 2. Agent Orchestration`) for the
    visual state machine this implements.
"""
from __future__ import annotations

from typing import TypedDict

from langgraph.graph import END, StateGraph

from denialiq_engine.agents.cdi_intelligence.agent import CdiIntelligenceAgent
from denialiq_engine.agents.coding_accuracy.agent import CodingAccuracyAgent
from denialiq_engine.agents.prior_auth.agent import PriorAuthAgent
from denialiq_engine.agents.appeal_intelligence.agent import AppealIntelligenceAgent
from denialiq_engine.agents.ar_aging.agent import ArAgingAgent
from denialiq_engine.agents.payer_contract_intelligence.agent import PayerContractIntelligenceAgent
from denialiq_engine.governance.hitl_router import route as hitl_route
from denialiq_engine.governance.safe_mode import get_mode, OperatingMode
from denialiq_engine.risk_model.stage1_scorer import Stage1Scorer
from denialiq_engine.schemas.claim import Claim, ClaimStatus


class EngineState(TypedDict, total=False):
    claim: Claim
    shadow_mode: bool


def build_production_graph(client_config: dict) -> StateGraph:
    """Build the full orchestration graph for a given client's parameterized
    configuration (EHR type, payer mix, specialty, thresholds, etc.)."""

    cdi = CdiIntelligenceAgent(config=client_config)
    coding = CodingAccuracyAgent(config=client_config)
    prior_auth = PriorAuthAgent(config=client_config)
    appeal = AppealIntelligenceAgent(config=client_config)
    ar_aging = ArAgingAgent(config=client_config)
    contract_intel = PayerContractIntelligenceAgent(config=client_config)
    scorer = Stage1Scorer(model_path=client_config["model_path"], model_version=client_config["model_version"])

    def cdi_node(state: EngineState) -> EngineState:
        cdi.run(state["claim"])
        return state

    def coding_node(state: EngineState) -> EngineState:
        coding.run(state["claim"])
        return state

    def prior_auth_node(state: EngineState) -> EngineState:
        prior_auth.run(state["claim"])
        return state

    def risk_scoring_node(state: EngineState) -> EngineState:
        # TODO: build feature vector from claim + Stage1Scorer.score()
        raise NotImplementedError

    def hitl_node(state: EngineState) -> EngineState:
        if state.get("shadow_mode"):
            return state  # observe-only, no routing surfaced
        # TODO: hitl_route(state["claim"], risk_score) once risk_scoring_node is implemented
        raise NotImplementedError

    def submit_node(state: EngineState) -> EngineState:
        state["claim"].status = ClaimStatus.SUBMITTED
        return state

    def route_after_submit(state: EngineState) -> str:
        # TODO: branch to "denied" or "paid" based on 835 remittance webhook
        return END

    def appeal_node(state: EngineState) -> EngineState:
        appeal.run(state["claim"])
        return state

    def ar_aging_node(state: EngineState) -> EngineState:
        ar_aging.run(state["claim"])
        return state

    def contract_intel_node(state: EngineState) -> EngineState:
        contract_intel.run(state["claim"])
        return state

    graph = StateGraph(EngineState)
    graph.add_node("cdi", cdi_node)
    graph.add_node("coding", coding_node)
    graph.add_node("prior_auth", prior_auth_node)
    graph.add_node("risk_scoring", risk_scoring_node)
    graph.add_node("hitl", hitl_node)
    graph.add_node("submit", submit_node)
    graph.add_node("appeal", appeal_node)
    graph.add_node("ar_aging", ar_aging_node)
    graph.add_node("contract_intel", contract_intel_node)

    graph.set_entry_point("cdi")
    graph.add_edge("cdi", "coding")
    graph.add_edge("coding", "prior_auth")
    graph.add_edge("prior_auth", "risk_scoring")
    graph.add_edge("risk_scoring", "hitl")
    graph.add_edge("hitl", "submit")
    graph.add_conditional_edges("submit", route_after_submit)
    graph.add_edge("appeal", "ar_aging")
    graph.add_edge("ar_aging", "contract_intel")
    graph.add_edge("contract_intel", END)

    return graph


def guarded_invoke(graph, state: EngineState):
    """Wrapper that checks Safe Mode before invoking the graph."""
    if get_mode() != OperatingMode.FULL_AI:
        raise RuntimeError(f"Engine not in FULL_AI mode (current: {get_mode()}). Billing continues on deterministic rules only.")
    return graph.invoke(state)
