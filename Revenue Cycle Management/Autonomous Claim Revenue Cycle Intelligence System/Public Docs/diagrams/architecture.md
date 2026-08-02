# Full Architecture (private/internal detail level)

See `denialiq-public/diagrams/architecture.md` for the shareable version.
This file is for internal notes on production-only wiring — e.g. exact
Kafka topic names, Qdrant collection names per client, and model registry
promotion flow — fill in as the system matures.

```mermaid
flowchart TD
    EHR[EHR: Epic/Cerner/Meditech] -->|FHIR R4| Ingest[Ingestion: Debezium CDC + Kafka]
    Clearinghouse[Clearinghouse 837/835] -->|X12| Ingest
    Ingest --> PHI[PHI Tokenizer]
    PHI --> Orchestrator[9-Agent LangGraph Orchestrator]
    Orchestrator --> RiskModel[Two-Stage Risk Model]
    RiskModel --> HITL[HITL Router]
    HITL --> Submission[Claim Submission]
    Submission --> Remittance[835 Remittance]
    Remittance --> Appeal[Appeal Intelligence]
    Remittance --> ContractIntel[Payer Contract Intelligence]
    Orchestrator --> RAG[RAG Payer Policy Engine]
    RAG --> Qdrant[(Qdrant Vector Store)]
    Orchestrator --> Governance[Governance Layer]
    Governance --> AuditLog[(Audit Log - hash chained)]
    Governance --> ModelRegistry[(Model Registry)]
```
