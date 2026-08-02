"""EDI X12 837 (claim) / 835 (remittance) parser.

STATUS: interface-only. 835 parsing feeds CARC/RARC codes into the
Appeal Intelligence Agent and Payer Contract Intelligence module.
"""
from __future__ import annotations


def parse_837_claim(raw_x12: str) -> dict:
    raise NotImplementedError("Wire to an X12 837 parsing library")


def parse_835_remittance(raw_x12: str) -> dict:
    """Returns dict with paid_amount, carc_codes, rarc_codes, claim_id."""
    raise NotImplementedError("Wire to an X12 835 parsing library")
