# ARCI Simulation Walkthrough

1. **Generate synthetic claims** — `simulation/synthetic_data_generator.py` creates a
   fake 837-style claims file (`sample_data/synthetic_claims.csv`) with random payers,
   CPT codes, billed amounts, and a baseline ~15% denial rate.

2. **Run the lifecycle simulation** — `simulation/claim_lifecycle_simulation.py` pushes
   every synthetic claim through:
   - a toy scrubbing step that flags high-risk claims from a risk score,
   - a toy appeal step that simulates an overturn outcome for denied claims.

3. **Review the summary** — the script prints and saves a JSON summary
   (`sample_data/simulation_results.json`) with denial rate, appeal success rate, and
   how many claims were flagged high-risk.

4. **View the mock dashboard** — open `dashboard_mockup/index.html` in a browser. It's a
   static HTML/CSS/JS mockup (no backend) that renders example metrics in the same shape
   the real ARCI Revenue Intelligence Dashboard would use.

This walkthrough only demonstrates the *shape* of the workflow described in the ARCI
case study — it is not a predictive model and does not connect to any real EHR, payer,
or claims system.
