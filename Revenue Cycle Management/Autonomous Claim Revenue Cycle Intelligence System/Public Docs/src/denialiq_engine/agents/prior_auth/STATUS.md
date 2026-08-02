# Status: interface-only

**Module:** prior_auth

Prior authorization requirement detection with 72-hour SLA tracking and escalation at hour 48. WISeR-aware routing.

## Implementation checklist
- [ ] Pydantic I/O contract finalized in `schemas/`
- [ ] Prompt templates drafted and reviewed (`prompts.py`)
- [ ] Tool registry wired (`tools.py`)
- [ ] Unit tests against synthetic fixtures
- [ ] HITL routing thresholds calibrated (if applicable)
- [ ] Shadow-mode validation plan defined
- [ ] Client Phase-0 parameterization hook added

## Notes
Real prompts, tool implementations, and calibration data are added
per-client during Phase 1-2 of the DFY engagement. This skeleton defines
the contract and orchestration hook only.
