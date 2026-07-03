# Prediction-locked two-threshold comparative workflow

## Aim

This workflow tests a **predeclared prediction** derived from the source-locked
*Campanula microdonta* system:

```text
large Bombus → B. ardens → no effective Bombus
```

The intended signature is temporally staggered.

1. Floral-size adjustment can begin at the first transition.
2. In specialist-like flowers, effective *B. ardens* service can preserve
   outcrossing and visual-signal benefit through the first transition.
3. Loss of effective Bombus service predicts a second-step decline in
   outcrossing and visual signal, and increased autonomous reproductive
   capacity.
4. Open generalist flowers are a negative control: they are **not** predicted to
   show the specialist second threshold in visible floral signal.

The workflow asks whether the corresponding observed directions are supported
in a calibration system and then in independent holdout lineages. It does not
reconstruct historical events or identify causal effects from photographs.

## Partitions

### Calibration

`Campanula microdonta` is the calibration lineage. Its rows are generated from
`data/inoue_literature_island_traits.csv` by:

```bash
python paper/build_campanula_calibration_observations.py \
  --out data/predictive_meta/campanula_calibration_observations.csv
```

Three source-locked channels remain separate:

- flower length;
- multilocus outcrossing; and
- bagged capsule set, which measures autonomous reproductive capacity rather
  than realized selfing.

A fourth, lower-ranked calibration channel is now predeclared: blinded
public-photo scoring of *C. microdonta* inner guide strength. Its score enters
as C-rank ordinal image evidence only after the geographical key is joined.

The calibration result can select which predeclared pollinator scenario is most
compatible with the locked source summaries. It must not be counted as an
independent replication in the holdout test.

### Holdout

Independent direct-source data and blinded photo scores enter the `holdout`
partition. Each lineage contributes at most one prespecified trait per trait
family and regime. Several images from the same taxon are first aggregated;
they do not become several evolutionary replicates.

## Four scenario contracts

The CSV contract is:

`data/predictive_meta/two_breakpoint_prediction_contract.csv`

| Scenario | First transition | Second transition |
|---|---|---|
| `environment_only` | Not ranked from regime contrasts alone | Not ranked until an explicit environment likelihood is added |
| `body_size_only` | Floral size can change | No required guide, outcrossing, or autonomous-assurance threshold |
| `small_bee_substitution` | First size change possible | Full small-bee substitution predicts no new signal/outcrossing/assurance threshold |
| `ardens_replacement_loss` | Specialist flower size can change while other channels remain approximately stable | Specialist visible signal and outcrossing decrease; autonomous assurance increases; generalist visible signal remains flat |

`environment_only` is not treated as a weak straw-person. It is deliberately
left unranked by the regime-only scorer until climate, area, isolation and other
predeclared environmental covariates can enter a separate likelihood.

## Photo protocol

`data/predictive_meta/photo_cohort_manifest.csv` fixes each taxon's analysis
group and a 0–3 **within-taxon** visible-signal scale before any regional card
is scored. Scores cannot be compared as absolute colours or sizes between taxa.
Only each taxon's mainland/ardens/no-Bombus contrast is used.

Before scoring, an iNaturalist research-grade photo availability audit screens
candidate specialist taxa under the fixed regional proxies. The first audit of
20 preclassified specialist-bee candidates, stored in
`data/predictive_meta/specialist_photo_coverage_20260703.csv`, found exactly
one with at least two available photos in each regime bin: *Viola grypoceras*
(10 mainland, 4 Oshima, 3 pooled no-Bombus). This is a limitation, not a reason
to relax the criterion or count one-card contrasts. The other specialist
lineages remain original-source recovery targets. Photo evidence therefore
serves three restricted jobs:

1. *Campanula* guide-strength calibration;
2. a *Viola grypoceras* specialist holdout test; and
3. generalist negative controls, where balanced cards are available.

Build blinded sheets:

```bash
python paper/build_prediction_photo_bundle.py \
  --manifest data/predictive_meta/photo_cohort_manifest.csv
```

Do not open the matching `*_key.csv` while filling the blind sheet. Then join a
completed sheet only once:

```bash
python paper/compile_blind_photo_scores.py \
  --blind paper/photo_sheets/<taxon>_blind_sheet.csv \
  --key paper/photo_sheets/<taxon>_key.csv \
  --manifest data/predictive_meta/photo_cohort_manifest.csv \
  --taxon "<taxon>" \
  --out data/predictive_meta/holdout_<taxon>.csv \
  --audit-out artifacts/predictive_meta/<taxon>_photo_audit.json
```

Cards must be open flowers, show the focal structure, pass the declared
comparability gate, and have a score inside the manifest range. Missing or
ineligible cards are not zero values. Any photo-derived regime contrast requires
at least two eligible, scored cards in each contributing regime bin before it
is treated as a holdout unit.

## Run the scorer

```bash
python scripts/run_predictive_meta_analysis.py \
  --observations data/predictive_meta/campanula_calibration_observations.csv \
  --contract data/predictive_meta/two_breakpoint_prediction_contract.csv \
  --partition calibration \
  --output-dir artifacts/predictive_meta/calibration
```

For holdout, concatenate source-extracted and blinded-photo observation rows
that share the common observation schema, then use `--partition holdout`.

The output contains:

- a scenario-level support/contradiction table;
- an auditable CSV of every lineage × trait-family × transition decision; and
- no environmental scenario ranking until environmental inputs have been added.

## Boundary

A positive holdout alignment supports a **prediction of the two-threshold model**.
It does not prove that a historical Bombus replacement occurred, prove a photo
records a pollinator interaction, or turn bagged capsule set into realized
selfing. The environmental and colonization-history alternatives remain
explicit models to add, not explanations silently discarded.
