# Status: interface-only

**Module:** appeal_intelligence

Autonomous appeal drafting triggered on 835 denial receipt. Root-cause mapping, RAG-retrieved appeal requirements, draft within 2 hours. Human review required before filing.

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
