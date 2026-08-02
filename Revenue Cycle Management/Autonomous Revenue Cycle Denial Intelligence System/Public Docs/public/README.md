# ARCI — Public Simulation & Demo Layer

Safe-to-share portfolio artifacts: synthetic data generation, a claim lifecycle simulation,
and a static dashboard mockup. No real payer, patient, or clinical data is used anywhere here.

## Contents

- `simulation/` — synthetic claims data generator + end-to-end claim lifecycle simulator
- `demo/` — static HTML dashboard mockup + a written walkthrough of the simulated flow

## Quickstart

```bash
cd simulation
pip install -r requirements.txt
python synthetic_data_generator.py        # writes sample_data/synthetic_claims.csv
python claim_lifecycle_simulation.py      # runs the simulated intake -> submission -> denial -> appeal flow
```

Then open `demo/dashboard_mockup/index.html` in a browser to view the mock revenue
intelligence dashboard populated with the simulation output.
