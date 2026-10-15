# Repository navigation — current scientific surface

This is a navigation and evidence-rank map, **not** an additional scientific result or a change to any frozen analysis. It was audited against `main` at `a412b456b435f10dd9c71014b53f3e1f37634b41` on 2026-10-15. For later commits, re-check the machine-readable route and active manuscript; do not treat a dated statement below as automatically current.

## Start with one of these five entry points

| Goal | Read first | Authority / limitation |
| --- | --- | --- |
| Understand the **one current Chapter 2 paper** | [Unified manuscript](CHAPTER2_UNIFIED_EVOLUTION_PERSISTENCE_MANUSCRIPT_20261010.md) and [Supporting Information](CHAPTER2_UNIFIED_EL_SUPPORTING_INFORMATION_20261010.md) | The manuscript on **main** is the active submission draft; it is not a submitted article. Branch-only revisions do not supersede it. |
| Check the declared publication route and unit of replication | [One-paper route JSON](../data/design/chapter2_one_paper_route_20261010.json) | Machine-readable `status=active_unified_manuscript_not_submitted`, manuscript count 1, distinct study cohorts and explicit inferential boundaries. |
| Evaluate claims and counterclaims | [Four-question claim audit](CHAPTER2_CENTRAL_FOUR_QUESTION_AUDIT_20261014.md), [four-question ledger](four_question_resolution_20261011/FOUR_QUESTION_LEDGER.md), [assurance coupling scope](CHAPTER2_ASSURANCE_COUPLING_SCOPE_20261015.md) | Results for Q1 returns/thresholds, Q2 order, Q3 finite realization and Q4 persistence are **not** a demonstrated single historical causal chain. |
| Reproduce or audit evidence | [REPRODUCE.md](../REPRODUCE.md) and [data-deposit readiness](CHAPTER2_UNIFIED_DATA_DEPOSIT_READINESS_20261011.md) | Use source receipts, original data identities, independent-unit counts and readback checks; `outputs/` is generated work, not the source registry. |
| Find historical work | [Legacy archive policy](../legacy/README.md) and [thesis positioning](../THESIS_CHAPTER_POSITIONING.md) | Model 2, older journal routes and earlier narratives are provenance, not the current submission. Some thesis passages retain explicitly historical statements. |

## Which directories do what?

| Location | Function | Maintenance rule |
| --- | --- | --- |
| `scripts/model3_island/` | Active Model 3 biology and deterministic / finite-population machinery | Changes need biological-contract review and relevant tests. |
| `scripts/` (other files) | Frozen-case readers, focused audits, source retrieval, analysis, figures, manuscript/render and packaging tools | Do not delete or move by filename/age alone; check imports, tests, workflows, manifests and original SHA references. |
| `tests/` | Behavioral, regression, scientific-claim and provenance guards | Retain source-locked controls, including negative results. |
| `data/design/`, `data/designs/` | Registered or historically frozen study definitions and routing | Do not rewrite old designs to match a newer story. |
| `data/results/`, `results/chapter2/` | Stored readouts, projections, cohort summaries and audit receipts | Preserve each independent denominator, source SHA, admission rank and original-vs-derived distinction. |
| `data/submission/` | Deposit readiness and original archive receipts | A prepared/retrieved archive is not a public DOI deposit. |
| `docs/`, `figures/` | Current and historical documentation, scientific interpretation and rendered/stored figures | Prefer this index and the route JSON to guessing status from a dated filename. |
| `.github/workflows/` | General CI, scientific gate and individually scoped research/reproduction workflows | Do not disable archived-looking workflows until the consumers and recorded source runs have been audited. |
| `legacy/` | Explicitly retired models, manuscript routes and development provenance | Keep intact unless independent provenance and references are addressed. |

## Evidence and paper boundaries

1. **Original observations / readouts / historical receipts** are evidence with their own sampling units; newer narrative documents cannot retroactively make them a different experiment.
2. **Model 3 simulation** is synthetic. Reproductive return, realized trait order, finite inheritance and demographic persistence are measured in distinct interventions/cohorts. Annual censuses, nested repeats, archived genomes and case records are not extra independent ecological histories.
3. **Natural island observations** motivate and test transportability; they are not fitted to synthetic `near/far` coordinates, and the current model does not identify a historical `Bombus` cause in Izu.
4. **Pending PRs** can contain newer source checks, corrections or manuscripts, but cannot be cited as merged `main` evidence. Use the [2026-10-15 open-PR overlap audit](PR_CONSOLIDATION_AUDIT_20261015.md) to determine what is duplicated and what is unique.
5. **Raw external deposit** is incomplete as recorded in the active route and readiness materials. Reviewer ZIP generation and private/public release assets are not a journal submission or DOI publication.

## Short verification route

```bash
python -m pip install -e '.[dev]'
pytest -q
# For the complete manuscript package instructions and source checks:
# see REPRODUCE.md
```

`CI` ([workflow](../.github/workflows/ci.yml)) runs tests for Python 3.10, 3.11 and 3.12. The [Chapter 2 scientific gate](../.github/workflows/chapter2-scientific-gate.yml) has its own scope and must also be checked when triggered. A green result on a predecessor commit does **not** validate an updated PR head.

## Safe cleanup policy

- **Now:** maintain an explicit current-paper entry point, mark superseded routes, compare overlapping PR files by exact blob SHA, and centralize navigation.
- **Before any physical move or deletion:** enumerate references in Markdown, source imports, tests, workflow triggers, package/receipt manifests, exact-commit historical replay and reviewer ZIP members; then prove clean reproduction at the candidate final head.
- **Do not:** drop negative findings, rewrite frozen originals, silently consolidate distinct sample denominators, claim an unmerged draft as accepted evidence, or delete branches with unreviewed unique source/results.

No source code, registered experiment, frozen data or historical paper is reclassified by this navigation document.
