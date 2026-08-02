# Placeholder Terraform root module.
# Fill in per client's cloud provider (AWS/GCP/Azure) during Phase 1.
# Should provision: Kubernetes cluster/namespace, Qdrant instance or
# managed vector DB, Kafka cluster or managed equivalent, secrets manager,
# and network policy isolating the PHI tokenization boundary.

terraform {
  required_version = ">= 1.5"
}
