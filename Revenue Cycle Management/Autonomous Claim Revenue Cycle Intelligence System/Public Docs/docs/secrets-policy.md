# Secrets Policy

- No API keys, client EHR endpoints, contract rates, or credentials are
  ever committed to this repository.
- Local development uses `client_config/local-dev.yaml` (gitignored) with
  sandbox values only.
- Production secrets are managed via [GitHub Actions secrets / cloud
  secrets manager — fill in for your actual deployment target].
- `client_config/<real_client_id>.yaml` files must never be committed —
  add a `.gitignore` rule per client if a local copy is ever created for
  debugging, and delete it afterward.
- Rotate any secret immediately if accidentally committed, then scrub git
  history (e.g. via `git filter-repo`) before this repo is shared with
  any additional collaborator.
