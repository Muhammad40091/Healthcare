# DenialIQ Engine — PRIVATE

**⚠️ This repository must remain private.** It contains the full production
architecture skeleton: all 9 agents, HITL governance runtime, payer
adversarial intelligence, contract underpayment detection, and client
parameterization framework for real hospital deployments.

The public portfolio repo (`denialiq-public`) contains a stripped-down,
synthetic-data-only demo of the two-stage risk model and orchestrator
pattern, safe for public/recruiter viewing. **Nothing in this repo should
be copied to the public repo without review** — in particular:

- No real client data, contract rates, or payer-specific configs
- No fine-tuned model weights or prompts tuned on real denial data
- No production HITL thresholds if they've been client-calibrated
- No client_config/ contents beyond the anonymized template

## Why This Is Private

| Reason | Detail |
|---|---|
| Client confidentiality | `client_config/` will hold real EHR endpoints, payer contract rates, NDA'd parameters per engagement |
| Competitive moat | Payer adversarial intelligence timeline, override-learning calibration data, and RAG corpus curation are the actual IP |
| Regulatory exposure | Misconfigured HITL thresholds or governance gaps in a public repo could mislead someone into deploying unsafely |
| Compliance | Audit log schema and PHI tokenization boundary should not be fully public — reduces attack surface for reverse-engineering PHI boundaries |

## Repository Map

```
src/denialiq_engine/
  agents/                     One package per module, each with agent.py, prompts.py, tools.py
    cdi_intelligence/
    coding_accuracy/
    prior_auth/
    claim_orchestrator/        Full 9-agent LangGraph wiring (production)
    appeal_intelligence/
    payer_adversarial_intelligence/
    ar_aging/
    pfx/                       Patient Financial Experience
    payer_contract_intelligence/
  risk_model/                  Two-stage model: XGBoost + fine-tuned LLM reasoning layer
  rag/                         Live CMS/payer policy ingestion, Qdrant index, WISeR corpus
  governance/                  Audit log, RBAC, drift detector, fairness monitor,
                                PHI tokenizer, pipeline integrity monitor, safe mode,
                                HITL router, override-learning RL loop
  integration/
    fhir/  hl7/  x12/          EHR + clearinghouse adapters
  schemas/                     Full production Pydantic contracts (superset of public schemas)
  client_config/                Per-client parameterization templates (Phase 0 output)
infra/
  k8s/                          Deployment manifests, scaling config per client tier
  docker/                       Dockerfiles, docker-compose for local dev
  terraform/                    Cloud infra as code
docs/                           Internal architecture notes, runbooks, incident response
scripts/                        Deployment, migration, model promotion scripts
```

## Module Status Legend

Each agent package contains a `STATUS.md` marking implementation maturity:
- `interface-only` — Pydantic contracts + method signatures, no logic yet
- `prototype` — working logic against synthetic/sandbox data, not production-hardened
- `production` — deployed and validated at a client site

## Getting Started (internal)

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp src/denialiq_engine/client_config/template.yaml src/denialiq_engine/client_config/local-dev.yaml
# edit local-dev.yaml with sandbox values only — never commit real client config
pytest -v
```

## Access Control

- Repo visibility: **Private**
- Collaborators: architect + explicitly NDA'd evaluators only
- Branch protection on `main`: required PR review before merge
- Secrets (API keys, client endpoints): managed via GitHub Actions secrets /
  vault, never committed — see `docs/secrets-policy.md`
