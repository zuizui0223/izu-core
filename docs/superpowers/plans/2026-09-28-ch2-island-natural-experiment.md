# Execution plan: Ch2 island natural experiment

Execution: native in this thread, user authorized completion. Spec: `docs/superpowers/specs/2026-09-28-ch2-island-natural-experiment.md`.

## Tasks

1. **Pin and audit current evidence.** Read island corrected selector and manuscript from its immutable remote commit. Produce Ch1 motivation audit; retain acquisition work. Inspect latest unified Model 3 and projection surfaces. Completed calculations are not restarted.
2. **Build empirical atlas with meaningful validation.** `scripts/build_chapter2_island_atlas.py` consumes six coordinate JSONs, Izu exposure/pollen JSONs and cross-channel CSV, matrix/current-state receipts. `build_atlas(root: Path) -> dict` validates independent unit labels, source counts and numeric bounds; includes SHA256 for every input. `write_outputs(root, out)` writes compact JSON/table and actual-data PNG/PDF. Tests in `tests/test_chapter2_island_atlas.py` cover full count/source identities, invalid values, interval semantics, preserved negative Izu deletion, and no conflation of the two 42 denominators.
3. **Integrate scientific narrative.** Update active manuscript introduction, empirical methods/results/discussion, figure links, and clear latest Ch1/Ch2 handoff. User's reported research motivation is stated as origin of question, not fabricated field experience. All historic analysis receipts remain unchanged.
4. **Verify and deliver.** Run new and affected scientific-contract tests plus repository artifact-budget guard; inspect real output figures, check claim/source coverage, regenerate relevant submission surfaces if affected. Push explicit branch only, no unsolicited PR; verify remote SHA and exact-head CI. Record limitations and complete goal only after all required outputs exist and are checked.

## Review focus

- 42 observation systems versus 42 literature entries: separate named denominators.
- Seasonal samples versus independent histories: preserve site/study/time nesting.
- Izu stage coefficients have incompatible units: separate panels; no products.
- Source selection and site-deletion failures: retain full source roster and negative signs.
- Model/natural coordinate incompatibility: no outcome calibration, k mapping, latent branching or 200-generation prediction claim.

Completion progress lives in `.superpowers/sdd/2026-09-28-ch2-island-natural-experiment/`; this plan is not itself completion evidence.
