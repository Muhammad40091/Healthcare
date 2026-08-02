"""FHIR R4 integration client — EHR endpoint (Epic / Cerner / Meditech).

STATUS: interface-only. Endpoint config comes from client_config during
Phase 1 (Data & Integration Foundation).
"""
from __future__ import annotations


class FhirClient:
    def __init__(self, base_url: str, auth_config: dict):
        self.base_url = base_url
        self.auth_config = auth_config

    def get_clinical_notes(self, patient_token: str) -> list[dict]:
        raise NotImplementedError("Wire to FHIR R4 DocumentReference/Observation endpoints")

    def get_encounter(self, encounter_id: str) -> dict:
        raise NotImplementedError
