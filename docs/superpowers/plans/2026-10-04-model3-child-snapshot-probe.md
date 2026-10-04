# Empirical child-factor probe on existing model distributions

Use all8 archived n9/1000 dense-roundtrip cases, baseline checkpoint200,
history76001 and visitor channel0 of period200 (common-environment entry).
If no visitors or zero channel mass, report not_evaluable, never substitute a
different channel/time selected by its outcome. Verify NPZ hashes first.

Represent each baseline and weighted donor/recipient density with the current
core rounding tolerance1e-8. This input-rounding is outside the child-factor
bound. Compare the child-reduced operator with the original tensor_births
applied to exactly those same reconstructed donor/recipient inputs, thereby
isolating only child-factor truncation error.

Use child error budget1e-8 times donor_mass*recipient_mass, recorded absolute
bound and max16million values for diagnostic contraction only. No full
biological rerun. Record parental/child ranks, observed error, bound, runtime,
source/NPZ hashes; preserve resource failures. Pass means observed L1 <= bound
plus1e-10 times max(1,channel mass), with truncation bound within its budget.
This checks usefulness at n9 only; no65-node sufficiency claim.
