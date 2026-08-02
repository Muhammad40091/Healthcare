# Status: interface-only

**Module:** cdi_intelligence

Fixes documentation gaps before the claim is built. Transformer-based NLP over structured/unstructured notes; HCC gap detection; documentation specificity scoring; medical necessity alignment check against RAG corpus.

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
