# ABM scenario recovery

`channel_id/abm_recovery.py` asks whether observations from one declared synthetic Izu world are classified back to the world that generated them.

The benchmark has two independent stages:

1. build scenario centroids from reference ABM replicates;
2. generate held-out replicates, degrade them through an observation design, and classify by standardized distance.

The observation design controls:

- `island_fraction`: fraction of islands observed, with mainland retained as an anchor;
- `missing_rate`: feature-level missingness after island sampling;
- `measurement_sd`: Gaussian error on transformed observations.

Features currently include island-level population size, lineage richness, mean specialization, mean autonomous selfing, and global lineage summaries. Counts are log-transformed before classification.

The classifier is intentionally transparent. It uses the root-mean-square standardized distance to each scenario centroid over available overlapping features. This is a baseline identifiability diagnostic, not a claim that nearest-centroid classification is the final inferential method.

Run a complete-design benchmark:

```bash
python scripts/run_abm_recovery.py \
  --reference-replicates 12 \
  --test-replicates 20 \
  --generations 60 \
  --founders 140 \
  --output results/abm-recovery-complete.json
```

Run a degraded observation design:

```bash
python scripts/run_abm_recovery.py \
  --reference-replicates 12 \
  --test-replicates 20 \
  --island-fraction 0.5 \
  --missing-rate 0.25 \
  --measurement-sd 0.10 \
  --output results/abm-recovery-degraded.json
```

Primary outputs are:

- `overall_accuracy`;
- `recovery_matrix`;
- scenario-specific accuracy;
- dominant off-diagonal confusions;
- classification margins and feature overlap for every held-out replicate.

Interpretation is restricted to the declared model family. High recovery means the synthetic mechanisms are distinguishable under the selected observation design; it does not establish that any scenario is historically true for the real Izu Islands.
