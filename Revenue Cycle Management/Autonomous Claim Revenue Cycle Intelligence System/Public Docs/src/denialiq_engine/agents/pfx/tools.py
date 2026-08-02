"""Tool registry for the pfx agent.

STATUS: placeholder. List and implement the deterministic tools (DB
lookups, rule-engine calls, RAG retrieval, external API calls) this agent
is permitted to invoke. Every tool call must pass the RBAC Engine gate
(see governance/rbac.py) before execution.
"""

TOOL_REGISTRY: dict = {}
