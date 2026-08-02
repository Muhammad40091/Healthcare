"""
Claim Lifecycle Simulation
---------------------------
Runs a simplified, fully synthetic simulation of a claim moving through:
intake -> pre-submission scrub -> submission -> payer response -> (denial -> appeal) -> resolution.

This is a portfolio demonstration of the *shape* of the ARCI workflow, not a
production denial-prediction model.
"""

import csv
import json
import random
from pathlib import Path

DATA_PATH = Path(__file__).parent / "sample_data" / "synthetic_claims.csv"
OUTPUT_PATH = Path(__file__).parent / "sample_data" / "simulation_results.json"

random.seed(7)


def load_claims():
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            "Run synthetic_data_generator.py first to create sample_data/synthetic_claims.csv"
        )
    with open(DATA_PATH) as f:
        return list(csv.DictReader(f))


def scrub_claim(claim):
    """Toy 'scrubbing agent': flags a claim as high-risk using its risk_score."""
    risk = float(claim["risk_score"])
    claim["scrub_flag"] = "high_risk" if risk > 0.7 else "pass"
    return claim


def simulate_appeal(claim):
    """Toy 'appeal agent': simulates an appeal outcome for denied claims."""
    if claim["denied"] == "True":
        overturned = random.random() < 0.83  # simulated 83% overturn rate
        claim["appeal_filed"] = True
        claim["appeal_overturned"] = overturned
    else:
        claim["appeal_filed"] = False
        claim["appeal_overturned"] = None
    return claim


def run_simulation():
    claims = load_claims()
    results = []
    for claim in claims:
        claim = scrub_claim(claim)
        claim = simulate_appeal(claim)
        results.append(claim)

    total = len(results)
    denied = sum(1 for c in results if c["denied"] == "True")
    overturned = sum(1 for c in results if c.get("appeal_overturned") is True)

    summary = {
        "total_claims": total,
        "denied_claims": denied,
        "denial_rate_pct": round(100 * denied / total, 2),
        "appeals_filed": denied,
        "appeals_overturned": overturned,
        "appeal_success_rate_pct": round(100 * overturned / denied, 2) if denied else 0,
        "high_risk_flagged": sum(1 for c in results if c["scrub_flag"] == "high_risk"),
    }

    with open(OUTPUT_PATH, "w") as f:
        json.dump({"summary": summary, "claims": results}, f, indent=2)

    print("Simulation complete. Summary:")
    print(json.dumps(summary, indent=2))
    print(f"Full results written to {OUTPUT_PATH}")


if __name__ == "__main__":
    run_simulation()
