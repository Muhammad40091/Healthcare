"""PHI Tokenizer — replaces PHI fields with consistent synthetic tokens
before any data reaches the model pipelines.

STATUS: interface-only. Production version must use a deterministic,
salted, one-way tokenization scheme (e.g. HMAC with a client-specific key
stored in a secrets manager) so the same patient always maps to the same
token within a client's data, but tokens are not reversible without the
key. Do NOT implement with reversible encryption for this module — the
model pipeline should never need to reverse the token.
"""
from __future__ import annotations

import hashlib
import hmac


def tokenize(raw_identifier: str, client_salt: str) -> str:
    """Deterministic, salted one-way token. client_salt must come from a
    per-client secret, never hardcoded or committed."""
    return hmac.new(client_salt.encode(), raw_identifier.encode(), hashlib.sha256).hexdigest()[:16]
