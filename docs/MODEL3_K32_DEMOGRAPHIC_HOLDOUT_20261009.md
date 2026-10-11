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

## Two-fold source-run outcome (2026-10-09)

Dedicated model3-k32-demographic-holdout CI succeeded on source
90840e8cdde8537992199a1cd924be1edaae4703:
[Actions run 37887877707](https://github.com/zuizui0223/izu-core/actions/runs/37887877707),
[raw four-JSON artifact 11597416175](https://github.com/zuizui0223/izu-core/actions/runs/37887877707/artifacts/11597416175).
Source-locked result: data/results/model3_k32_twofold_demographic_holdout_20261009.json.

### Held-out predictions only (not training-set scores)

| Budget | Train half | Evaluation survived | Source - comparator endpoint variance | Paired demographic MC 95% percentile | Source - comparator 2 × cumulative covariance | Paired MC 95% percentile |
|---|---|---:|---:|---|---:|---|
| 8 | first | 256 | +0.001158 | [+0.000223, +0.002278] | -0.01556 | [-0.02191, -0.00889] |
| 8 | second | 256 | +0.000190 | [-0.000527, +0.001097] | -0.00410 | [-0.01140, +0.00275] |
| 3 | first | 250 | **+0.001219** | [+0.000317, +0.002430] | -0.02091 | [-0.03072, -0.01089] |
| 3 | second | 253 | **-0.001253** | [-0.002523, -0.000120] | -0.00667 | [-0.01994, +0.00513] |

**Falsifying constraint on prior interpretation:** at budget 3 the
held-out variance gap reverses sign under reversal of calibration/evaluation
halves, and the two simple percentile MC intervals exclude zero in
OPPOSITE directions. Thus it is not defensible to identify a robust
source-specific allele-frequency variance-reduction mechanism from
these old-history results. Budget 8 shows weaker, but still evident,
fold sensitivity for covariance and variance difference.

The actual held-out source and comparator allele-frequency means are
not identical despite source-training per-generation analytical
calibration. Example: budget 3 first-half trained: 0.987584 source
versus 0.993698 control on holdout. Reversing folds: 0.987808 source
versus 0.979045 control. Near the p=1 ceiling, this mean mismatch
can materially change the available endpoint variance.

As a descriptive bound normalization, for any P in [0,1] we have
Var(P) <= mu*(1-mu). The ratio Var(P)/[mu*(1-mu)] removes this simple
upper-bound scale, though it does not isolate selection. For budget 3
the source/comparator ratios are 0.1289 / 0.0578 (first train) versus
0.0802 / 0.1082 (second train): the sign still reverses.

The matched-mean comparator's apparent explanatory power is thus
**retrospective, fold-dependent and not causally identifying**.
The older inference about strong source directional mean evolution
versus an unweighted neutral Mendelian martingale remains valid within
its fixed source settings; it is a different question.

Never turn these demographic partitions into independent ecological
sample size: both reuse only historical visitor history 26110601.
No natural island data, frozen confirmatory histories, mutation-enabled
SDE/SPDE, or externally validated stabilizing selection was added.

**Admissibility verdict:** keep #420 in Draft. Report exact finite
Markov law and pathwise sampling identities as mathematical methods,
and report mean-matched covariance/variance controls as exploratory
negative/sensitivity results.
