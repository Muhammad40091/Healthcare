"""
Synthetic Healthcare Claims Data Generator
-------------------------------------------
Generates a synthetic (fake) claims dataset that mimics the shape of an 837
professional claim feed, purely for portfolio simulation purposes.

No real patient, payer, or clinical data is used or referenced.
"""

import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

random.seed(42)

PAYERS = ["Aetna", "Cigna", "UnitedHealthcare", "Humana", "BlueCross-Synthetic"]
CPT_CODES = ["99213", "99214", "99215", "93000", "80053", "71046", "36415"]
DENIAL_REASONS = [
    "Missing prior authorization",
    "Medical necessity not established",
    "Duplicate claim",
    "Incorrect modifier",
    "Timely filing limit exceeded",
    None,  # None == not denied
]

OUT_DIR = Path(__file__).parent / "sample_data"
OUT_DIR.mkdir(exist_ok=True)


def random_date(start_days_ago=180, end_days_ago=1):
    days = random.randint(end_days_ago, start_days_ago)
    return (datetime.now() - timedelta(days=days)).date().isoformat()


def generate_claims(n=500):
    rows = []
    for i in range(1, n + 1):
        payer = random.choice(PAYERS)
        cpt = random.choice(CPT_CODES)
        denied = random.random() < 0.15  # ~15% baseline denial rate
        reason = random.choice(DENIAL_REASONS[:-1]) if denied else ""
        rows.append(
            {
                "claim_id": f"CLM-{i:05d}",
                "payer": payer,
                "cpt_code": cpt,
                "billed_amount": round(random.uniform(80, 2500), 2),
                "submission_date": random_date(),
                "denied": denied,
                "denial_reason": reason,
                "risk_score": round(random.uniform(0, 1), 3),
            }
        )
    return rows


def write_csv(rows, filename="synthetic_claims.csv"):
    path = OUT_DIR / filename
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} synthetic claims to {path}")


if __name__ == "__main__":
    write_csv(generate_claims())
