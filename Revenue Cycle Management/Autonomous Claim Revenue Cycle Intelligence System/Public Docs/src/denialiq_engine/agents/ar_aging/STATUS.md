# Status: interface-only

**Module:** ar_aging

Autonomous 14-day threshold monitoring with collectability-ranked work queues. HITL-governed.

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
