# K32 source-matched directional comparator: demographic calibration holdout

## Location and purpose

This extends [the post-outcome source-mean matched control](MODEL3_K32_MEAN_MATCHED_CEILING_20261009.md).
The previous numerical comparison calibrated eight separate yearly tilt parameters
on the same 512 demographic realizations subsequently evaluated. That design
can fit simulation noise. This experiment freezes a demographic **train /
holdout split before calibrating** and tests whether the conclusions reproduce
in unseen demographic realizations under the same old visitor environment.

It is a methodological holdout, **not an independent ecological history**.
There is ONE source visitor history (26110601/near); source K=32,
mutation=0, eight yearly generations, survival=0, seed immigration=0,
canonical Chapter 2 prior_selfing settings and engineered 27-class joint
diploid genotype support. Frozen confirmatory visitor seeds remain unread.

## Protocol

- Train indices 0..255 and demographic holdout indices 256..511 (fixed
  halves of 512 independent demographic streams). The groups share
  the old 26110601 visitor trajectory, not genetic realization streams.
- Run unmodified source Model 3 reproduction, capped-Poisson recruitment
  and full diploid Mendelian segregation separately on all 512 paths.
- Comparator uses exact full 3-locus Mendelian neutral parental-gamete
  probabilities with an **externally calibrated assurance-dosage tilt**,
  intentionally different source mating biology.
- At year t, compute the source high-allele mean from TRAIN source surviving
  endpoints only. Compute training comparator parental genotype laws only,
  and fit a **single** tilt theta_t by matching the analytical TRAIN
  comparator mean to the TRAIN source target.
- **Do not read any holdout source/neutral endpoint, fit quality or
  genotype to calibrate theta_t**. Apply frozen theta_t to both train and
  holdout controls at the current year. For each trajectory force comparator
  recruitment census to its source's realized N(t).
- Extinction is absorbing; fully lost alleles cannot reappear. If target
  mean is unattainable on training support, stop with
  TRAINING_MEAN_UNATTAINABLE instead of silently fixing/reinitializing it.
- For training and holdout separately, compare mean high-allele frequency,
  endpoint variance, fixation, direction/sampling 2*covariance, and paired
  nested-demographic percentile MC error. Keep all source and control
  distributions separate from the biological evidence registry.

## What this answers

The split addresses only re-use of demographic outcomes during calibration
and evaluation. If negative covariance also appears in holdout simulations
and the source/comparator contrast persists, it is **less dependent on
in-sample demographic noise tuning**, but remains:
1. dependent on one shared visitor-history ecological environment;
2. a post-outcome model family, chosen after prior findings;
3. conditional on source demographic censuses and survival;
4. sensitive to different multilocus genotype structure and mean fit;
5. NOT a neutral drift-only or actual ecological fitness experiment.

A small holdout mean mismatch should be reported as **generalization
error**, not patched by re-fitting on the holdout.

## Run and guard

```bash
pytest -q tests/test_model3_k32_mean_matched_holdout.py
python -m scripts.audit_model3_k32_mean_matched_holdout --budget 8 --draws 512 --out holdout-budget8.json
python -m scripts.audit_model3_k32_mean_matched_holdout --budget 3 --draws 512 --out holdout-budget3.json
```

The core CI includes PR420-only `model3-k32-demographic-holdout`,
checks locked visitor/history source and calibration firewall, and archives
raw records. This does not edit the canonical Model 3 biological code.

**Scientific stop:** No new causal selection/drift mechanism, natural
island validation, external visitor-history confirmation, geographical
INLA fit or complete SDE/SPDE is established.
