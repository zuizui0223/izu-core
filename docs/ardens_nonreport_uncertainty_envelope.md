# *Bombus ardens* non-report uncertainty envelope

## Why this check is needed

The original pollinator-hierarchy counterfactual uses a simple ordered input:

```text
mainland large Bombus -> Oshima B. ardens bridge -> non-Bombus bee regime
```

That pattern is useful as a declared counterfactual, but the Inoue 1986
visitor-rate table does not license a stronger statement that every island
without a positive *B. ardens* row had a biological absence. The accompanying
pollinator-regime audit separates:

1. a positive rate reported;
2. no positive row after named observation effort;
3. no Inoue 1986 effort row for the island/unit.

The envelope tests the consequence of that distinction without pretending to
fit an occupancy or detection model.

## What is varied

For each non-mainland island with `bombus_ardens = 0` whose direct-table status
is either:

```text
not_reported_in_rate_table_after_recorded_effort
no_inoue1986_effort_row_for_unit
```

the script enumerates both 0 and 1 as **availability/context coding** in the
small hierarchy counterfactual. Oshima stays fixed because it has a direct
positive rate row; Honshu is not varied because the hierarchy definition gives
large-*Bombus* mainland records stage zero regardless of the *B. ardens* field.

The current input yields five varied islands, hence \(2^5 = 32\) configurations.

## Current locked-input result

In the current artifact, `pollinator_hierarchy` is **never** a co-winner or
unique winner across the 32 configurations. Its rank is 2 in every case:

```text
isolation_order       rank 1 in every configuration, MAE = 0.1252
pollinator_hierarchy  rank 2 in every configuration, MAE = 0.1370–0.3081
environment_only      rank 3 in every configuration, MAE = 0.3390
```

Therefore this simple deterministic pattern test does **not** support the bridge
hierarchy as the best explanation relative to the island-order benchmark. It
shows only that the hierarchy pattern is consistently closer to these locked
trait channels than the declared climate-only benchmark.

This result must be kept separate from the source-level multichannel likelihood
and profile analyses, which answer a different question using different
observation models and ecological restrictions. Agreement or disagreement across
those analyses is a model-comparison result to report, not a reason to select one
post hoc.

## What it does not do

The configurations are not equally probable scenarios. They do not estimate:

- occurrence or occupancy;
- imperfect-detection probability;
- true absence;
- abundance;
- effective pollination;
- historical colonization or loss.

A context code of 1 means only “test this alternative handling of a non-positive
rate-table state in the existing transparent pattern scorer.”

## Output interpretation

The report records the rank of `pollinator_hierarchy` against the existing
`environment_only` and `isolation_order` pattern checks for every configuration.

Do not translate the rank stability into a claim that *B. ardens* was present or
absent on any particular island. In particular, the finding that hierarchy stays
rank 2 is not evidence for island occupancy; it is a limitation of the simple
ordered pattern formulation.

## Run

```bash
python scripts/score_ardens_nonreport_envelope.py \
  --input data/inoue_literature_island_traits.csv \
  --pollinator-rates data/two_breakpoint_evidence/inoue1986_pollinator_rates.csv \
  --observation-effort data/two_breakpoint_evidence/inoue1986_observation_effort.csv \
  --output-csv artifacts/ardens_nonreport_envelope.csv \
  --output-json artifacts/ardens_nonreport_envelope.json \
  --output-md artifacts/ardens_nonreport_envelope.md
```

The counterfactual workflow runs this alongside the locked-input pattern score
and uploads all outputs as one artifact.
