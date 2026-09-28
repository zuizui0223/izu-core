# Source-level sensitivity and Monte Carlo diagnostics

## Why this report exists

A marginal compatibility value is an integral over prior parameter draws. A neat
ranking can be misleading for two separate reasons:

1. the ranking may reverse under plausible assumptions about observational
   error or among-flower/plant overdispersion;
2. a small number of prior draws may carry nearly all importance weight, making
   the numerical integral itself under-resolved.

This workflow reports both problems explicitly.

## Swept observation-scale assumptions

The default nine settings vary one component at a time around the central
setting and add a joint precise and joint conservative corner.

| Component | Low / precise | Central | High / conservative |
|---|---:|---:|---:|
| Outcrossing residual, logit SD | 0.50 | 0.70 | 1.00 |
| Bagging beta-binomial concentration | 20 | 8 | 4 |
| Flower between-population residual, mm | 2.0 | 3.5 | 6.0 |

Higher bagging concentration means less overdispersion. The other two higher
values mean more residual heterogeneity. None of these values are estimated
from the existing source summaries; they are sensitivity settings, not results.

## Importance-sampling ESS

For normalized importance weights \(w_d\), the diagnostic is:

\[
ESS = \frac{1}{\sum_d w_d^2}.
\]

- `ESS ≈ draws` means many prior draws contribute.
- `ESS` close to 1 means one rare prior draw carries the result.
- An ESS warning does not support a competing ecological scenario. It says the
  current numerical integration is too concentrated to treat its score or
  posterior-weighted predictions as stable.

The workflow flags `ESS < 10` and `ESS / draws < 1%`. Those flags are prompts
for larger or adapted sampling, not universal evidence thresholds.

## Run

```bash
python scripts/run_source_level_sensitivity.py \
  --output-csv artifacts/source_level_sensitivity.csv \
  --output-json artifacts/source_level_sensitivity.json \
  --output-md artifacts/source_level_sensitivity.md
```

The default is nine settings × three seeds × four scenarios. The slower full
3×3×3 scale grid is available with `--factorial`.

## What to report

Do not report only the scenario that ranks first in the central setting. Report:

1. rank-one frequency across the declared grid;
2. rank reversals, if any;
3. ESS range for each scenario;
4. whether the rank-one result remains after each evidence-channel ablation;
5. the separate fact that guide/spot constraints are absent until reviewed
   source-locatable comparisons are entered.
