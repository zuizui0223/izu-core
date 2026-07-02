# Pollinator-regime evidence audit

## Question

The island model currently uses four bounded visitor-regime inputs:

```text
bombus_diversus
bombus_ardens
halictid_pollinator
megachilid_pollinator
```

Those are availability/context indicators, not flower-specific measures of
effective pollination. The key audit question is therefore not “is a zero
indicator true absence?” but rather:

> What does the directly transcribed Inoue 1986 table actually report for this
> group and island, given its declared observation effort?

## Evidence states

| audit state | permitted interpretation |
|---|---|
| `positive_rate_reported` | A positive visitor rate was reported. It supports presence/context coding, not pollination effectiveness. |
| `not_reported_in_rate_table_after_recorded_effort` | The group does not appear as a positive-rate row while the table records observation effort for that island. This is a non-report, **not** proof of zero capture, absence, or ineffectiveness. |
| `no_inoue1986_effort_row_for_unit` | The island/unit has no Inoue 1986 effort row. The model indicator may reflect other sources, but it must not be described as an Inoue 1986 non-detection. |

The audit deliberately does not reconstruct integer captures from rounded
per-hour rates and does not fabricate zeros from omitted taxa.

## Current direct-table implication

- Oshima has 9 recorded observation hours and a positive *Bombus ardens* rate
  of 1.1 per observation hour.
- Niijima, Kozushima, and Hachijo have named observation effort in the table,
  but no positive *B. ardens* row.
- Toshima has no Inoue 1986 effort row, so its binary regime coding lies outside
  that table's direct detection coverage.

Thus the sharp defensible wording is:

> *Bombus ardens* was directly recorded in the Oshima visitor-rate table, and
> was not listed as a positive-rate group in the effort-recorded Niijima,
> Kozushima, and Hachijo rows.

The wording “*B. ardens* was absent from those islands” is not licensed by this
transcription alone.

## Run

```bash
python scripts/audit_pollinator_regime_evidence.py \
  --output-csv artifacts/pollinator_regime_evidence_audit.csv \
  --output-md artifacts/pollinator_regime_evidence_audit.md
```

The CSV preserves each model indicator's direct-rate support state and is
uploaded with the source-level analysis artifacts.
