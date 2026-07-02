# Flower-length comparability audit

## Why this audit is necessary

The current source-level flower table contains six direct summaries from one
paper, but they do not all enter one shared experimental comparison.

| source row | reported experimental context | role in a between-island comparison |
|---|---|---|
| Hachijo | Tokyo experiment | comparable within Tokyo set |
| Niijima | Tokyo experiment | comparable within Tokyo set; n = 2 |
| Toshima | Tokyo experiment | comparable within Tokyo set |
| Oshima | Tokyo experiment | comparable within Tokyo set |
| Kiyosumi | Tokyo experiment | comparable within Tokyo set |
| Nikko | Nikko experiment | singleton context; no within-context island contrast in the retained table |

A singleton experiment can describe a phenotype but cannot separately identify
an island effect from an experiment effect without an additional calibration or
shared reference. It must therefore not silently act as an equally comparable
mainland anchor in a cross-island likelihood.

## Declared analysis sets

The sensitivity runner reports all sets rather than selecting one after seeing a
result.

- `legacy_all_rows`: the original six-row compatibility input, retained solely
  for reproducibility of the earlier result.
- `within_experiment_comparable`: Tokyo rows only; excludes the Nikko singleton.
- `within_experiment_n_ge_10`: Tokyo rows with n at least 10; also excludes the
  Niijima n = 2 summary, which is retained in other sets but explicitly tested
  for leverage.
- `leave_one_comparable_row_out:<island>`: removes one of the five Tokyo rows at
  a time.

These are data-comparability and leverage checks, not alternative evolutionary
mechanisms. They do not turn flower length into evidence of pollinator
mechanism.

## Reading the output

A model rank that changes after excluding the Nikko singleton means the prior
result depends on cross-experiment anchoring. A rank that changes after excluding
the Niijima n = 2 row means the result depends on a low-sample-size summary.
Neither outcome proves a model wrong; each locates the measurement condition that
needs independent replication.

## Boundary

The source table records common-garden pollination experiments, not a replicated
multi-site trait survey with an explicit experiment-block model. This audit can
protect against inappropriate pooling, but it cannot recover an unreported
experiment effect or establish the cause of flower-size divergence.

## Reproducible screening

The workflow runs the declared sets with the same five candidate models and
tempered-SMC machinery. It emits both a machine-readable JSON report and a
Markdown table of retained/excluded source rows.
