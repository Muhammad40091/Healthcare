"""Dynamic knowledge graph: CPT/ICD nodes with payer constraint edges and
denial probability weighting.

STATUS: interface-only.
"""
from __future__ import annotations


class PolicyKnowledgeGraph:
    def __init__(self):
        self.nodes: dict[str, dict] = {}
        self.edges: list[tuple[str, str, dict]] = []

    def add_code_node(self, code: str, code_type: str) -> None:
        self.nodes[code] = {"type": code_type}

    def add_payer_constraint_edge(self, code_a: str, code_b: str, payer: str, denial_weight: float) -> None:
        self.edges.append((code_a, code_b, {"payer": payer, "denial_weight": denial_weight}))
