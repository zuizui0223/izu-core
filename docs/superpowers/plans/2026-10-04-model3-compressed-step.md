# Integrate exact small-grid compressed reproductive step

Implement joint weighting by phenotype matrix times assurance vector using
full SVD (no singular-value truncation), reduced QR and bounded tensor
contraction. Sum reproductive channels by QR of concatenated factor bases,
then transform/add cores without allocating a block-diagonal expanded core.
Preserve all joint associations. A conservative explicit-array budget rejects
oversized contractions; this does not bound library workspace or peak RAM.

Wire ecological_weights, weighted selfed births, every visitor's outcross
channel and capacity retention together. Current validation scope is evolving
assurance and no plant immigration, exactly the full-mutation campaign scope;
reject fixed assurance rather than silently mutating that locus. Include
surviving adults using the existing survival parameter. No mutation mask or
biological rule is changed. No rounding is introduced yet.

TDD: weighting and channel sums against explicit correlated tensors; complete
step against frozen density_step for both settings, absent/present visitors,
jump/heat_fv, and positive mutation. Absolute full-state tolerance1e-9. Keep
production sources and live runs intact. Success validates one small-grid
step only; long trajectories, rank control and high-resolution feasibility
remain separate gates before any full-grid rerun.
