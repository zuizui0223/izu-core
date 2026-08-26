# Izu Core — state-dependent island plant responses

`izu-core` is the reproducible analysis and manuscript repository for an island-ecology study asking:

> **Why does island-associated simplification or reorganization of pollinator function produce divergent plant responses rather than one universal post-establishment trajectory?**

## Current state

**Chapter 2 is scientifically complete and frozen for submission.**

Primary target: **Journal of Ecology**  
Fallbacks: **Functional Ecology**, **Oikos**

Working title:

> **One perturbation, multiple island responses: state-dependent branching under pollinator functional simplification**

No new simulation, field dataset, external-system search, parameter retuning, or external research programme is required for the paper. The editorial V3 submission route has passed the repository test suite on Python 3.10, 3.11 and 3.12.

Canonical files and routes:

- Reviewer-facing manuscript: **editorial V3**, generated as `docs/ISLAND_ECOLOGY_JECOLOGY_SUBMISSION_DRAFT_V3_20260826.md`
- Frozen manuscript source: [`docs/ISLAND_ECOLOGY_JECOLOGY_SUBMISSION_DRAFT_V2_20260824.md`](docs/ISLAND_ECOLOGY_JECOLOGY_SUBMISSION_DRAFT_V2_20260824.md)
- V3 builder: [`scripts/build_island_ecology_manuscript_v3.py`](scripts/build_island_ecology_manuscript_v3.py)
- Supporting Information: [`docs/ISLAND_ECOLOGY_JECOLOGY_SUPPLEMENT_20260824.md`](docs/ISLAND_ECOLOGY_JECOLOGY_SUPPLEMENT_20260824.md)
- H2 analytical sign decomposition: [`docs/ISLAND_ECOLOGY_H2_SIGN_DECOMPOSITION_20260825.md`](docs/ISLAND_ECOLOGY_H2_SIGN_DECOMPOSITION_20260825.md)
- Submission manifest: [`data/design/island_ecology_jecology_submission_manifest.json`](data/design/island_ecology_jecology_submission_manifest.json)
- Canonical study state: [`data/design/simulation_study_mainline_20260824.json`](data/design/simulation_study_mainline_20260824.json)
- Current submission state: [`docs/ISLAND_ECOLOGY_SUBMISSION_STATE_20260825.md`](docs/ISLAND_ECOLOGY_SUBMISSION_STATE_20260825.md)

V3 is a deterministic editorial render from the frozen V2 source. It sharpens the island-syndrome/post-establishment gap and integrates the already-frozen H2 sign decomposition into the Abstract, Methods, Results, Discussion and Conclusion. It does **not** rerun or change the scientific analysis.

## Ecological story

The paper separates three processes often grouped under the plant **island syndrome**:

1. **Colonization / assembly filtering** — which lineages arrive, establish and persist.
2. **In-situ evolutionary change** — how established island lineages evolve relative to source lineages.
3. **Post-establishment interaction response** — how established lineages respond when pollinator functional composition and interaction context change.

This paper focuses on the third layer.

```text
MAINLAND SOURCE POOL
        ↓
COLONIZATION / ASSEMBLY FILTER
        ↓
ESTABLISHED ISLAND FLORA
        ↓
POLLINATOR FUNCTIONAL CHANGE
        ↓
starting functional state → branch potential
local interaction context → branch allocation / rescue / worsening
reproductive assurance → magnitude attenuation
        ↓
MULTIPLE LINEAGE TRAJECTORIES
```

The synthesis is:

> **Aggregate island syndromes can coexist with lineage-level branching because colonization and persistence determine which states arrive, whereas functional starting state and local ecological context determine how established lineages respond after pollinator environments change.**

## H1–H5

| Hypothesis | Current result |
|---|---|
| **H1 — universal post-establishment response** | **rejected** |
| **H2 — state-dependent branching** | **supported within the declared ABM, independently replicated, and analytically sign-decomposed** |
| **H3 — context-dependent propagation** | **supported bidirectionally** |
| **H4 — autonomous-assurance buffering** | **partially supported: robust magnitude attenuation, no robust sign rescue** |
| **H5 — cross-island recurrence** | **supported at the qualitative response-state level** |

## Main frozen results

### H2 — branch generation

Mixed-sign branching occurred in **0.4167** of matched runs in both the original and independently seeded blocks. Removing pre-existing functional-position heterogeneity reduced within-run mixed-sign branching to **0**, whereas the other tested residual single-factor removals retained branching.

The frozen v12 endpoint equations were then unpacked analytically. Under the matched endpoint comparison,

```text
sign(Δ reproduction) = sign(Δ service) = sign(Δ functional opportunity)
```

because the downstream service and reproduction transforms are monotonic under the declared v12 conditions. Thus the downstream transforms preserve rather than manufacture the response sign; the branching originates upstream in lineage-specific functional-opportunity change. This is a model-internal identity, not an empirical assignment of the synthetic coordinate to one named floral trait.

### H3 — local interaction context

- local-support removal changed **105/288** paired lineage response signs;
- local context produced **16/96** sign rescues among eligible declines;
- **85/96** eligible declines were attenuated;
- **11/96** were worsened.

Stable interpretation:

> **network context is a bidirectional branch allocator with buffering capacity, not a universal buffer.**

### H4 — autonomous assurance

Among **216** lineages with upstream service decline, autonomous assurance attenuated reproductive decline in **207/216** cases but produced **0** sign rescues in the independent block. A broadened envelope likewise produced **0/525** sign rescues.

Stable interpretation:

> **autonomous assurance mainly attenuates response magnitude rather than reliably reversing response sign.**

## External island challenge

The literature screen retained **54 geographic/system units**. Thirteen met the strict external state-challenge contract:

| External state | Systems |
|---|---:|
| branching | 3 |
| same-direction propagation | 6 |
| buffering / alternative | 2 |
| reproductive-axis decoupling constraint | 1 |
| retained falsification | 1 |
| **total** | **13** |

All **11 generative challenges** were covered or sign-compatible with response classes already present in the frozen model. The 13-system set is a **strict challenge set, not a prevalence sample**.

Protected exceptions remain:

- **Puerto Rico–Mona `Guaiacum sanctum`** — reproductive-axis decoupling, not generic whole-reproduction buffering.
- **Dominica `Heliconia`** — retained failed signed-position projection; it **was not retuned** after failure.

Cross-island recurrence therefore supports the generality of the **response architecture**, not one shared empirical mechanism across all islands.

## Island-syndrome literature synthesis

- Review: [`docs/ISLAND_SYNDROME_DEEP_LITERATURE_REVIEW_20260824.md`](docs/ISLAND_SYNDROME_DEEP_LITERATURE_REVIEW_20260824.md)
- Claim matrix: [`data/design/island_syndrome_literature_claim_matrix_20260824.json`](data/design/island_syndrome_literature_claim_matrix_20260824.json)

Key boundary: the paper rejects a universal **post-establishment trajectory**, not the existence of recurrent island syndromes. Assembly filtering, in-situ evolution and post-establishment interaction response are kept distinct.

## Main paper architecture

1. **Fig. 1 — ecological response architecture**
2. **Fig. 2 — replicated minimal branch generator**
3. **Fig. 3 — network-context branch allocation versus assurance attenuation**
4. **Fig. 4 — cross-island response-state challenge**

State-separability diagnostics are Supporting Information only (`Fig. S1` / `Table S2`). They are inference guards, not the biological headline.

## Claim boundaries

This paper does **not** claim that:

- plant island syndromes are false;
- all island plants follow one post-establishment trajectory;
- all 13 external systems share one empirical mechanism;
- the 13-system challenge estimates global prevalence;
- the synthetic functional coordinate is automatically one named empirical trait;
- state compatibility is empirical causal identification;
- Dominica should be retuned until it fits.

**These are claim boundaries of this paper, not pointers to an external research programme.**

## Reproducibility

Primary numerical claims are stored in frozen JSON artifacts and figures are rendered deterministically from those artifacts.

Render editorial V3 directly:

```bash
python scripts/build_island_ecology_manuscript_v3.py
```

Build the anonymous reviewer archive:

```bash
python scripts/build_island_ecology_review_archive.py
```

The archive renders V3 from the frozen V2 source and excludes title-page information, author-identifying links and unrelated research programmes.

## Submission workflow

The scientific and editorial manuscript package is complete. Only **author-supplied identity/submission metadata** remain unresolved.

Populate:

[`data/design/island_ecology_submission_metadata_template.json`](data/design/island_ecology_submission_metadata_template.json)

The metadata validator fails closed rather than guessing author identity, order, affiliations, ORCIDs, contributions, acknowledgements, funding, inclusion statement, conflict of interest or declarations.

Generate identity-bearing files:

```bash
python scripts/build_island_ecology_submission_metadata.py \
  --metadata data/design/island_ecology_submission_metadata_template.json
```

Generate the complete Journal of Ecology submission bundle with editorial V3:

```bash
python scripts/build_island_ecology_submission_bundle.py \
  --metadata data/design/island_ecology_submission_metadata_template.json
```

Output:

```text
dist/island_ecology_jecology_submission_bundle.zip
```

The final bundle contains editorial V3 plus the title page and cover letter **outside** a nested anonymous reviewer archive. Packaging renders prose deterministically but does not rerun or modify the scientific analysis.

Metadata checklist: [`docs/ISLAND_ECOLOGY_SUBMISSION_METADATA_CHECKLIST_20260825.md`](docs/ISLAND_ECOLOGY_SUBMISSION_METADATA_CHECKLIST_20260825.md)

## Remaining external input

Only the following must be supplied by the authors themselves:

- final author order and affiliations;
- corresponding-author email and postal address;
- ORCID(s), if used;
- acknowledgements and funding;
- author contributions;
- inclusion statement;
- conflict-of-interest statement;
- explicit submission declarations.

A final immutable public archive/DOI is a publication-stage item and is not a scientific blocker for Chapter 2.

## Historical material

Older field-design, empirical-bridge and method-first files remain only for provenance. They are not part of the current manuscript or submission package when they conflict with the canonical state above.

When older documentation conflicts with the current paper state, prefer:

1. [`data/design/simulation_study_mainline_20260824.json`](data/design/simulation_study_mainline_20260824.json)
2. [`data/design/island_ecology_jecology_submission_manifest.json`](data/design/island_ecology_jecology_submission_manifest.json)
3. [`scripts/build_island_ecology_manuscript_v3.py`](scripts/build_island_ecology_manuscript_v3.py) + frozen V2 source [`docs/ISLAND_ECOLOGY_JECOLOGY_SUBMISSION_DRAFT_V2_20260824.md`](docs/ISLAND_ECOLOGY_JECOLOGY_SUBMISSION_DRAFT_V2_20260824.md)
4. [`docs/ISLAND_ECOLOGY_JECOLOGY_SUPPLEMENT_20260824.md`](docs/ISLAND_ECOLOGY_JECOLOGY_SUPPLEMENT_20260824.md)
5. [`docs/ISLAND_ECOLOGY_SUBMISSION_STATE_20260825.md`](docs/ISLAND_ECOLOGY_SUBMISSION_STATE_20260825.md)
