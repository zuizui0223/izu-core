# Guide review progress monitor

This monitor reads completed-or-partially-completed geographic review and blind
trait sheets through the audit layer. It provides two reports.

- `guide_review_next_actions.csv` gives every source-record unit one next action.
- `guide_review_island_readiness.csv` counts only units with accepted geography,
  accepted taxonomy, and a declared verified island.

A proxy queue position is never counted as an island record. Pending trait review
is a workflow state, not guide evidence.

For each verified island, the monitor reports the eligible shortfall to the
predeclared unit threshold and the potential shortfall if all currently pending
verified units pass review. Thus `pending_existing_verified_units` means review
completion could reach the threshold, whereas
`needs_additional_independent_verified_source_records` means it could not.

`ready_for_manual_pairwise_direction_check` is not permission to update model
constraints. It only means a single island has reached the review-unit threshold;
source photos, reviewer notes, pairwise direction, and the public-photo boundary
remain subject to manual biological confirmation.
