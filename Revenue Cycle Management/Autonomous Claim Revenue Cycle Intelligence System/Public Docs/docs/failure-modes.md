# Failure Resilience — The System Never Stops the Hospital

| Mode | Description |
|---|---|
| Full AI Mode | All 9 agents active; full inference + HITL governance |
| Degraded AI Mode | Critical-path agents active; non-critical queued |
| Safe Mode | AI layer suspended; deterministic rules only |
| Bypass Mode | Manual billing workflow; AI layer completely bypassed |
| Circuit Breaker | Auto-triggered on integrity breach or confidence collapse; Safe Mode activates instantly |

See `src/denialiq_engine/governance/safe_mode.py`.
