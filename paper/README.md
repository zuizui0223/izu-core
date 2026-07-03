# Izu multi-species floral-response meta-analysis (`paper/`)

A reproducible, public-data workflow testing whether pollinator-loss-driven
floral reduction/selfing **generalises across the Izu island flora**, framed as
a mechanism-resolved test of the flower-size island rule. *Campanula microdonta*
is the fully-measured calibration seed; the question is comparative.

## Reproduce everything

```bash
pip install -e .
python paper/run_all.py          # runs the whole pipeline -> artifacts/RESULTS.md
python -m pytest                 # 269 tests (Windows: add --basetemp=C:/pt)
```

Individual stages:

| Stage | Script / record | Output |
|---|---|---|
| Candidate pool (GBIF) | `gbif_coverage` / `gbif_filter` logic → `izu_entomophilous_candidates.csv` | 156 gradient-spanning entomophilous angiosperms |
| Expanded screening | `evidence_screening/README.md` + four stratified dockets | auditable path from the 156-species pilot to the full 319-species parent universe |
| Moderator | `classify_functional_groups.py` | `functional_group_classification.csv` (30 specialist / 89 generalist) |
| Anti-cline threshold | `threshold_analysis.py` (uses `channel_id/gradient_shape.py`) | step/cline/none per trait + breakpoint |
| Evidence hierarchy | `evidence_ranks.csv`, `evidence_observations.csv`, `validate_meta_inputs.py` | A–E graded observations |
| Synthesis | `meta_synthesis.py` | quantitative anchor + rank-weighted direction by group |
| Detectability | `comprehensive_sweep.py` | 90-cell calibrated-vs-naive recovery map |
| Photo tier | `build_photo_scoring_sheet.py`, `photo_scores.csv` | blinded per-island photo scoring |

## Evidence hierarchy (every observation is graded)

A peer-reviewed quantitative (1.0) · B peer-reviewed qualitative (0.7) ·
C blinded photo score (0.5) · D web/flora description (0.25) · E occurrence (0.0).
Synthesis is reported at full weight **and** rank-A/B-only, so conclusions never
rest on low-confidence text.

## Evidence-status boundary

The present synthesis is a reproducible pilot, not the completed public-data
ceiling. The 156-species entomophilous table is a prefiltered analysis cohort,
whereas the reported parent universe contains 319 mainland + >=2-island plants.
`evidence_screening/` fixes the next work unit: a protected 40-species pilot
docket followed by an auditable reconstruction and systematic screen of the
full parent universe. Peer-reviewed generalist floral series may remain scarce,
but that conclusion is only defensible after the registry records the searches,
source-level exclusions, and image/region coverage. See `NOVELTY.md` for the
methodological contributions and `meta_analysis_design.md` for the full design.
