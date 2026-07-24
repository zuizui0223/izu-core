# ABM observation design audit

This layer converts scenario recovery into an observation-design decision table.

Each candidate design declares:

- fraction of islands observed;
- feature missingness;
- measurement error.

For every design, the workflow regenerates independent reference and test worlds, reports overall and worst-scenario recovery, and records dominant confusions.

A design meets the target only when both overall accuracy and the least recoverable true world reach the declared threshold. The reported `minimum_design` is the lowest-burden tested design that clears both conditions.

The burden score is intentionally simple and declared in code. It is not a monetary field-cost estimate. Rankings are conditional on the synthetic world family, observation features, tested grid, and random replication.

Run:

```bash
python scripts/run_abm_design_audit.py \
  --target-accuracy 0.70 \
  --reference-replicates 8 \
  --test-replicates 10 \
  --output results/abm-design-audit.json
```
