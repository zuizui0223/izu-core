# Methodological novelty — self-audit

What is genuinely new here, versus a standard island-syndrome study, and where
each contribution lives. This doubles as a check that the analyses centre the
novel methods (anti-cline threshold, simulation) rather than re-describing a
single cline.

## 1. Anti-cline threshold detection (not just a cline)

Standard practice reports a monotonic mainland→island cline (a correlation).
We instead ask whether a trait **steps** at a specific pollinator-regime
boundary. `channel_id/gradient_shape.py` selects none/cline/**step** by AICc
(sized for the small per-species n) and returns the breakpoint location.

- Result: *Campanula* autonomous selfing is a **step at the Ōshima→Toshima
  bumblebee-loss boundary** (order ≈ 1.5), while corolla length is a smooth
  cline and climate is flat or steps elsewhere. The reproductive-assurance
  switch is localised to the pollinator boundary — invisible to a correlation.
- Novelty for the meta-analysis: a **shared breakpoint across independent
  specialists** is far stronger evidence of a common driver than any single
  cline, and cannot be produced by an unstructured environmental gradient.
  This is the "anti-cline" test the whole comparison is built around.

## 2. Comprehensive detectability simulation (not one benchmark)

`paper/comprehensive_sweep.py` sweeps pollinator-loss depth × environmental
confound × island number × analysis mode (90 cells). It shows recovery of the
true mechanism is 95–99% **with** environmental calibration but collapses to 0%
**without** it — worst exactly where the syndrome is strongest. This turns
"confounding" from a caveat into a quantified precondition and tells any future
field campaign what it must measure (an interaction-level channel; ~90
plant-units/island). Reused from, and generalising, the seed workflow's
`izu_gradient_benchmark`.

## 3. Evidence-ranked, multi-source synthesis (transparent confidence)

Every observation carries an A–E rank and weight (`evidence_ranks.csv`), pooled
at full and A/B-only weight, with a deliberate low-confidence web/flora tier (D)
to expand coverage without letting it drive conclusions. Rank rules are enforced
in CI (`validate_meta_inputs.py`; e.g. rank A ⇒ an effect size exists).

## 4. Pollination-moderator falsification (built-in negative control)

The moderator (`classify_functional_groups.py`) splits 156 species into
specialist vs generalist vs large-flower. The prediction is directional (island
rule): specialists reduce, generalists ≈ 0, large non-bee flowers enlarge. The
generalist group is an explicit **negative control** — a result where
generalists also shifted would falsify the pollinator-loss interpretation.

## 5. Public-data-only, reproducible assembly

The entire test is assembled from GBIF/iNaturalist/literature with no
first-party fieldwork, run by one command (`run_all.py`), tested (269 tests),
and CI-reproduced. The novelty is not any single number but a **falsifiable,
mechanism-resolved, reproducibly-graded** framework for asking whether an island
floral response generalises.

## Honest scope

Contributions 1–2 are the methodological core the user asked to foreground.
Contributions 3–5 make the comparison auditable. None of them manufactures data:
the synthesis is run to the public-data ceiling and that ceiling is documented.
