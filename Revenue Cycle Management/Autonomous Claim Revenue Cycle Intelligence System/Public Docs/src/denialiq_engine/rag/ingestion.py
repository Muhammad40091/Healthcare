"""Live payer policy ingestion pipeline.

STATUS: interface-only. Weekly delta-indexing from the CMS API: only
changed documents are re-embedded, not a full re-index. Corpus includes
CMS LCDs/NCDs, NCCI edits, private payer policies, and a separately
versioned WISeR coverage-criteria corpus.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class PolicyDocument:
    doc_id: str
    source: str  # "cms_lcd" | "cms_ncd" | "ncci" | "payer_policy" | "wiser"
    version: str
    text: str
    last_updated: datetime


def fetch_cms_updates(since: datetime) -> list[PolicyDocument]:
    raise NotImplementedError("Wire to CMS API polling client")


def delta_index(documents: list[PolicyDocument]) -> int:
    """Re-embed only changed documents. Returns count re-indexed."""
    raise NotImplementedError("Wire to Qdrant upsert with chunking/embedding pipeline")
