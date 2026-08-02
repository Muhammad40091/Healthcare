"""Client config loader.

STATUS: prototype. Loads and validates a client parameterization file
against a schema before the orchestrator graph is built. Real client
config files should never be committed to git — load from a secrets
manager / encrypted config store in production.
"""
from __future__ import annotations

import pathlib

import yaml


def load_client_config(path: pathlib.Path) -> dict:
    with open(path) as f:
        config = yaml.safe_load(f)
    _validate(config)
    return config


def _validate(config: dict) -> None:
    required = ["client_id", "ehr", "payer_mix", "hitl_thresholds"]
    missing = [k for k in required if k not in config]
    if missing:
        raise ValueError(f"Client config missing required keys: {missing}")
    if config["client_id"] == "REPLACE_ME":
        raise ValueError("Client config still has placeholder client_id — fill in template.yaml")
