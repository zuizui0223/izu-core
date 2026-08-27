# Journal of Ecology submission metadata checklist

Updated: 2026-08-27

Scientific status: **the scientific and manuscript-integration gates are closed.**

Author-supplied metadata and declarations are the active blocker. The completed response-geometry, parameter-robustness and conditional-WHY diagnostics are recorded in:

- `data/results/chapter2_scientific_gate_decision_frozen_20260827.json`
- `data/results/chapter2_conditional_why_diagnostics_frozen_20260827.json`
- `data/design/chapter2_active_manuscript_mainline_20260827.json`

The final submission builder is intentionally blocked until all required identity metadata and declarations are supplied.

## Completed scientific and manuscript work

- expose the complete model equations and parameterization in the manuscript;
- report `5 of 12` rather than pseudo-precise `0.4167` as the headline design count;
- demote H2 from `replicated minimal generator` to model-specific response decomposition;
- rename `local support` as local context / availability filtering;
- demote H5 `11/11 coverage` from validation to comparative grounding;
- map response-sign geometry across plant starting position and pollinator-community change;
- sweep key perturbation/matching parameters;
- map local-context sign changes and assurance sign-rescue thresholds;
- remove workflow/debug prose and resolve uncited references.

These items are implemented in the active manuscript and supporting information and are validated by the review-archive build.

## Author metadata required now

Populate `data/design/island_ecology_submission_metadata_template.json` with:

1. final author order and affiliations;
2. corresponding-author email and postal address;
3. ORCID(s), if used;
4. acknowledgements and funding;
5. author contributions;
6. inclusion statement;
7. conflict-of-interest statement;
8. explicit submission declarations.

These values must still be supplied explicitly rather than inferred.

## Builders

Identity-bearing metadata files can still be validated with:

```bash
python scripts/build_island_ecology_submission_metadata.py \
  --metadata data/design/island_ecology_submission_metadata_template.json
```

The final bundle command is:

```bash
python scripts/build_island_ecology_submission_bundle.py \
  --metadata data/design/island_ecology_submission_metadata_template.json
```

It will raise an error until all required metadata and declarations are supplied.

## Double-anonymous boundary

When submission readiness is restored, title-page and author information remain separate from the anonymous manuscript and reviewer archive.
