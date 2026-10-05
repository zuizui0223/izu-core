# Continuous replenishment and realized evolution: declared extension

This extends the current finite-ABM experiment over the same 13 coordinates already used for local selection. The displayed ecological axis is successful visitor-type establishment per update, lambda = 0.24 exp(-d), not island area or a calibrated kilometre distance. Plant capacity stays 48. It is a common-source model, not an inter-island network.

The original 64 history seeds, eight demographic repeats, founders, rules, two joint reproductive settings and 1,000-update horizon are retained. Positive mutation 0.01 with step SD 0.05 is fixed. The new work adds 11 intermediate coordinates (11,264 cases); 2,048 endpoint cases are reused after receipt verification. This is distinct from the stopped high-resolution density/PDE calculation, which remains stopped.

Eight endpoint trajectories (both settings, both endpoints, two history seeds) were independently regenerated before production; all ten recorded columns at all 1,001 times matched exactly, including missing extinct traits. The source snapshot and design hashes identify the execution. The run checkpoints individual case arrays and hashes. Do not restart a live process or summarize selected partial outcomes.

The planned readout retains all rates, periods 200/400/1,000, within-population and paired high-supply contrasts, pointwise history-bootstrap uncertainty, and survivor denominators. Timing uses changes 0.025/0.05/0.10 held 20 updates, ties within five; unreached events are censored. These conventions do not define a biological phase transition. Local gradient order is not substituted for realized order.

Status at declaration: production launched after exact endpoint replay. No result from the intermediate rates has been interpreted. Read live process state plus outputs/model3_replenishment_evolution_20261005/progress.json for current status; this paragraph is not a persistent live-process claim.

Run commands from repository root:

```powershell
$env:PYTHONUTF8='1'
python -m scripts.run_model3_replenishment_evolution --preflight-only
python -m scripts.run_model3_replenishment_evolution --workers 4
python -m scripts.summarize_model3_replenishment_evolution
python -m scripts.verify_model3_replenishment_raw_curves
python -m scripts.verify_model3_replenishment_readout
python -m scripts.figure_model3_replenishment_evolution
```

The summarizer refuses an incomplete campaign. A successful mean trend does not establish universal order, independence from reproductive assumptions, or an admitted positive-mutation deterministic/PDE comparison. The prior cost/depression sensitivity remains local-selection evidence and is not replaced by this fixed-parameter evolution gradient.

The separate raw-curve verifier reconstructs each history at every update by selecting its surviving repeats explicitly. It checks all 13,312 case identities and hashes, both 1,001-update trait contrasts, and occupied/paired denominators. This is independent of the production aggregation helper, not an independent biological simulator. The subsequent readout verifier checks threshold classification and interval calculations from the verified curves. Calling the raw verifier during production was deliberately rejected before loading outcomes, confirming its incomplete-campaign guard. Numerical verification is still pending the completed campaign; preparing these checks does not certify unfinished results.
