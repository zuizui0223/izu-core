# Journal of Ecology submission metadata checklist

Updated: 2026-08-26

Scientific status: **submission paused pending scientific reassessment.**

The author-metadata workflow remains prepared, but it is not the active gate. Before any submission bundle can be created, complete the response-geometry and parameter-robustness gate in:

- `docs/SCIENTIFIC_REASSESSMENT_AFTER_CRITIQUE_20260826.md`
- `data/design/manuscript_reassessment_gate_20260826.json`

The final submission builder is intentionally blocked while that gate is open.

## Scientific work required first

- expose the complete model equations and parameterization in the manuscript;
- report `5 of 12` rather than pseudo-precise `0.4167` as the headline design count;
- demote H2 from `replicated minimal generator` to model-specific response decomposition;
- rename `local support` as local context / availability filtering;
- demote H5 `11/11 coverage` from validation to comparative grounding;
- map response-sign geometry across plant starting position and pollinator-community change;
- sweep key perturbation/matching parameters;
- map local-context sign changes and assurance sign-rescue thresholds;
- remove workflow/debug prose and resolve uncited references.

## Author metadata retained for later

Once the scientific gate is closed, populate `data/design/island_ecology_submission_metadata_template.json` with:

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

but it will raise an error while the scientific reassessment gate remains open.

## Double-anonymous boundary

When submission readiness is restored, title-page and author information remain separate from the anonymous manuscript and reviewer archive.
