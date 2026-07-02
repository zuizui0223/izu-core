# Blinded guide review audit

This audit runs after geographic and taxonomic confirmation plus two blinded
trait reviews. It creates an unblinded ledger explaining why every source-record
unit was accepted for manual review or excluded.

## Required gates

- accepted geographic review
- accepted taxon review
- valid declared island
- two completed trait-review rows
- visible and comparable open inner corolla
- valid 0--3 ordinal scores
- distinct nonblank reviewer IDs
- reviewer score difference no larger than the declared threshold

Every failed gate is stored as an explicit exclusion code. Nothing is silently
dropped.

## Outputs

- `review_unit_decision_ledger.csv`: all source-record units, gates, scores, and
  dispositions
- `review_agreement_and_exclusion_summary.csv`: descriptive agreement and
  exclusion counts
- `README.md`: boundary statement

The agreement report is descriptive only: number of scorable pairs, exact
agreement, agreement within the allowed score difference, and mean absolute
score difference. It intentionally omits chance-corrected reliability estimates
because the expected ordinal sample is small.

A unit marked `eligible_for_manual_constraint_review` is still not a model
constraint or biological conclusion. Source record, photo views, reviewer notes,
and island sample size must be checked before any manual constraint update.
