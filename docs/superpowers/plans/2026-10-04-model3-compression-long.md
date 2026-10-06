# Long-horizon compression diagnostic

The eight forty-period cases passed. Extend exactly the same eight cases to
1000 periods, covering the far-to-common environment switch after200. Keep
nodes9, mutation.01/.05, history76001, founder74001, two reproductive settings,
near/far and jump/heat_fv. No additional history is selected by outcome.
Per-step compression tolerance remains1e-8. Gates remain full-path relative
L1<=1e-5, maximum trait gap<=1e-6, mass gap<=1e-5 and no occupancy mismatch.
Retain all failures and all periods; do not tune compression tolerance during
execution. One worker, one BLAS thread, alongside the existing13 run.

Save paired density checkpoints at200/400/1000, per-period measured errors,
source hashes, snapshot source archive and checkpoint hashes. This is still
dense-update/recompression and cannot establish direct compressed-operator
feasibility or high-resolution sufficiency. Failure identifies propagation
instability under this tolerance; passing only admits development/testing of
operators that act directly on the compressed joint distribution.
