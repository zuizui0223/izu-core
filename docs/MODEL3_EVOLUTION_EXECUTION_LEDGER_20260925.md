# Model 3 evolution execution ledger

## Scope and rulings

User amended scope: independent island ecology; Q1 is inspiration only, not a regional-pattern fitting or validation target. This supersedes the older goal wording requesting four-region concordance. The intended question concerns resident visitor functional turnover/activity, plant reproduction, inherited floral response, and life history.

The prospective draft of 8 replicates and80/160years was replaced BEFORE campaign outcomes. Final256 primary replicates and64 population-sensitivity replicates are precision choices; durations come from declared ecological/demographic timescale comparisons informed by primary natural-history evidence. They are not estimates of actual island residence or geological age.

Natural-history review: adult replacement proxy1/(1-s) is1 or4 reproductive seasons, functional visitor residence1/p is20 or6.67, arrival interval1/a is3.33 or10. Expected type count tends to6 or2/3. The community treatment changes richness and turnover jointly; it does not isolate richness. No empirical-rate calibration claimed.

Independent reviewer found no execution blocker in inheritance, donor-recipient orientation, extinction, density thinning, source freeze or grouping. Review requirements incorporated: pollen DOSE not literal grains; non-limiting separate autonomous self pollen; separate self/outcross totals in neutral control; paired survival denominators; disjoint founder-support claim ceiling; coupled survival/effort life-history interpretation; Python/NumPy provenance. Allele-count trajectories added so phenotypic variance is not misreported as genetic fixation.

## Frozen campaign

- Commit: `28d56f82f238bd2ecd7fcf3d8e368c3a560c36c3` (pushed, remote verified).
- Design: `data/design/model3_evolution_20260925.json`.
- Design checksum: `57c0e52f87cb1b7d6db003f8acd93a6b2ec2670e6c23d724083893101c5f5324`.
- Cases28,672; output cells160. Primary96cells x256; capacity sensitivity64cells x64.
- All trajectories400reproductive seasons. Common-calendar10/50/100 and life-history replacement checkpoints annual10/50/100 versus perennial40/200/400. Nested times are not independent replicates.
- Launched2026-09-25 17:35:35 Japan time; process263176, tool session14729. Output `data/results/model3_evolution_20260925`; progress log `../model3-evolution-campaign.log`.
- The campaign has not yet been scientifically summarized or admitted as complete. Require terminal manifest plus independent hash/state/replay verification.

## Verification completed before/as execution began

- 65 focused model/reproduction/exposure/freeze tests passed before freeze and run.
- Complete suite at frozen implementation:1720passed,1skipped,279.52seconds. Log `../model3-evolution-full.log`; process281464/session74381 completed exit0.
- Only known test-generated changes to `functional_exposure_harmonization_gate.json` and `izu_pollinator_proboscis_recovery_audit.json` were restored.
- GitHub CI for frozen commit: https://github.com/zuizui0223/izu-core/actions/runs/36114122441 verified completed/success at exact28d56f8.

## Postprocessing and distribution comparator

These are separate from frozen simulation sources. `validate_model3_evolution.py` requires a complete manifest, checks every case and demographic/genetic invariants, and optionally exactly replays firstcase of eachcell. Use `--replay` for final admission. `summarize_model3_evolution.py` reads verified artifacts, retains extinction and paired survivor counts, and reports uncertainty. Access-distance reduction is a descriptive within-founder-support statistic, not a common optimum or evolutionary branching theorem.

`model3_distribution.py` implements exact conditional one-step expected count and trait totals. Three tests include analytical Poisson-cap truncation and4096individual transitions. It is NOT a completed long-run mean-field/PDE comparison; arbitrary diffusion/centroid substitution is not authorized by the derivation. Mathematical basis and remaining steps: `MODEL3_DISTRIBUTION_COUNTERPART_20260925.md`.

Still required: terminal campaign evidence, complete independent validation/replay, source-backed results/report/figures, appropriate paired contrasts and uncertainty, finalized mathematical comparator scope, final branch push and currentCI verification. Do not mark the goal complete on this ledger or the earlier foundation tests.

Postprocessing review reproduced four false-acceptance examples on synthetic inputs (no campaign arrays inspected): out-of-founder-support intermediate means, NaN allele counts, fractional visitor counts, and reproduction after extinction. Added failing regression tests, strengthened these invariants plus exact recruitment identity and founder-support variance/count bounds; all12new distribution/validation/summary tests now pass. Running frozen simulation sources were not changed. Exact one-step expected-transition formula and survivor pairing received no review findings.
