# Status: prototype

Full 9-agent LangGraph orchestration: routes claims through CDI ->
Coding Accuracy -> Prior Auth -> Two-Stage Risk Model -> HITL Router ->
Submission -> (on denial) Appeal Intelligence -> AR Aging / Payer Contract
Intelligence, with Payer Adversarial Intelligence running continuously
in the background as a monitoring loop rather than in the per-claim path.

## Implementation checklist
- [x] State machine shape defined (matches diagrams/architecture.md)
- [ ] Each agent's `agent.py` implemented and promoted from interface-only
- [ ] Retry/failure handling per node (falls back to Safe Mode on repeated failure)
- [ ] Shadow-mode toggle (Cold-Start Protocol: 90-day observe-only period)
- [ ] Load testing at target client claim volume
