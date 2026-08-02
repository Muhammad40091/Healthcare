# ARCI — Autonomous Revenue Cycle Denial Intelligence System (Portfolio / Simulation)

This repository contains a **simulation-based, portfolio-grade** reference architecture for a
multi-agent healthcare Revenue Cycle Intelligence system. It is built entirely on
**open-source patterns and synthetic data** — no real PHI, no production payer connections,
no live EHR credentials.

## Repo layout

```
arci-repo/
├── public/     # Safe to open-source: synthetic simulation + demo mockups
└── private/    # Keep in a private repo/branch: architecture, agent code, AI/RAG, deployment, docs
```

- **public/** maps to the case study's Appendix "Simulation Layer" and "Demo Layer" —
  content intended for open portfolio evaluation.
- **private/** maps to "Architecture Layer", "Code Layer", "AI Layer", "Deployment Layer",
  and "Documentation Layer" — deeper design material meant for qualified evaluation only.

## Suggested GitHub setup

1. Create **two repos**:
   - `arci-public` (public visibility) → push contents of `public/`
   - `arci-private` (private visibility) → push contents of `private/`
2. Or keep one private repo with both folders, and use a GitHub Action / git filter to
   mirror only `public/` into a public repo when you want to share it externally.

## Disclaimer

All performance figures (denial reduction %, appeal success rates, revenue recovery estimates)
referenced anywhere in this repo are **simulation-based estimates** using synthetic datasets,
not measured production outcomes.
