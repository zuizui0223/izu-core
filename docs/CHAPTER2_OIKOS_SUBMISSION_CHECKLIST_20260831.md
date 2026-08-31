# Chapter 2 Oikos submission checklist

Updated: 2026-08-31

## Active route

- Journal: **Oikos**
- Article type: **Research Paper**
- Scientific tier: **Tier B — mechanistically resolved synthetic response geometry with bounded empirical confrontation**
- Story: **simulation → world confrontation → process-measurement bottleneck → Izu mechanistic-resolution zoom**
- Fallback: **Journal of Ecology Research Article**

The scientific and manuscript-integration gates are closed. No additional simulation, world projection or Chapter 3 empirical result is required for the active Chapter 2 submission route.

## Oikos initial-submission requirements already implemented

- double-anonymous manuscript rendering;
- separate identity-bearing title page;
- abstract capped at 300 words by the active manuscript contract;
- dedicated Significance statement;
- Data Availability / archiving statement;
- reviewer-ready frozen data, code and audit materials in the anonymous review archive;
- figures regenerated fail-closed against frozen scientific results before the relational Oikos overlay;
- supporting information and source-locked Izu structural audit included;
- no dissertation-internal Chapter 1/2/3 routing in the blinded manuscript or rendered Supporting Information.

The active submission manifest is:

`data/design/chapter2_oikos_submission_manifest_20260831.json`

The active metadata template is:

`data/design/island_ecology_submission_metadata_template.json`

## Scientific claim ceiling retained at submission

The submission must continue to state that:

- the model defines conditional response possibilities, not natural prevalence;
- partner loss/arrival coefficients are fixed-surface diagnostics, not field-causal estimates;
- response direction is relational rather than intrinsic: starting state matters through its relation to the community actually realized;
- the exact baseline variance shares are finite-ensemble diagnostics, not stable population magnitudes;
- realized community remains the largest additive component across the prespecified seed and structural-horizon sensitivities, while starting state alone remains weak and state × community nonadditivity remains consequential;
- mixed geometry persists at zero trait adjustment and under equal initial pollinator richness; the latter supports only that richness reduction is not necessary for mixed geometry;
- external island systems establish response diversity and a process-measurement bottleneck, not validation coverage;
- the audited literature is outcome-rich but process-poor: direct response outcomes occur in 21/25 entries but partner arrival/replacement in only 2/25;
- 0/25 audited research entries meet the full outcome-independent external-prediction contract, so formal held-out prediction is `not_evaluable`;
- Izu raw matching is structured at the source-state/background-community-composition level;
- null-corrected beyond-composition sorting is unsupported;
- the prespecified Oshima-source bridge is unsupported;
- Chapter 3 phenotype is not Chapter 2 validation.

## Author-supplied metadata still required

Populate the metadata template with:

1. final author order;
2. each author's affiliations;
3. corresponding-author email and postal address;
4. ORCID(s), if used;
5. acknowledgements, explicitly including `None` if none;
6. funding, explicitly including `None` if none;
7. author contributions;
8. inclusion / EDI statement;
9. conflict-of-interest statement;
10. explicit submission-declaration booleans.

These values are intentionally not inferred from repository history.

## Final build

When the author-supplied fields are complete:

```bash
python scripts/build_island_ecology_submission_metadata.py \
  --metadata data/design/island_ecology_submission_metadata_template.json

python scripts/build_island_ecology_submission_bundle.py \
  --metadata data/design/island_ecology_submission_metadata_template.json
```

Expected bundle:

`dist/chapter2_oikos_submission_bundle.zip`

It contains the blinded manuscript, corrected Supporting Information, separate title page, Oikos Significance statement, relationally aligned cover letter, deterministic figures, active Oikos manifest and anonymous reviewer archive.

Until the identity metadata and declarations are supplied, the builder remains fail-closed by design.
