# Initial iNaturalist generalist-photo availability audit — 2026-07-03

## Source snapshot

- Workflow: `Izu Generalist Photo Availability Audit`, run `28652998948`.
- Artifact: `inat-generalist-photo-availability`, digest `sha256:a2eb953341249da1a7b196ea9243ca0a6aa3330a8c602e5caef12980c075ca65`.
- Query scope: research-grade iNaturalist observations with photos, evaluated within declared radii around island proxy points for 16 protected generalist-control candidates.
- Boundary: the counts are source-specific availability metadata only. They do **not** verify island membership, flowering stage, wild status, trait visibility, pollination, effective visitor identity, or biological absence.

## Result

Five taxa had complete retrieval and records in at least four island-proxy cells:

| Candidate | cells with records | returned records | Immediate next action |
|---|---:|---:|---|
| *Pittosporum tobira* | 5/6 | 24 | build a blinded image queue; define a comparable floral trait before scoring |
| *Ajania pacifica* | 5/6 | 19 | build a blinded image queue; distinguish open heads from vegetative/fruit images |
| *Angelica keiskei* | 5/6 | 6 | inspect flower visibility before treating as a photo-tier candidate |
| *Hydrangea macrophylla* | 4/6 | 15 | predeclare fertile-flower versus sterile-display-sepal trait definition |
| *Hydrangea involucrata* | 4/6 | 6 | predeclare fertile-flower versus sterile-display-sepal trait definition |

No conclusion about trait direction follows from these counts. The file `inat_generalist_photo_availability_20260703_summary.csv` preserves all 16 candidate summaries.

## Failure and sparsity handling

Six species had three HTTP failures in the first job and are marked `retry_required`, never zero. The remaining complete but sparse taxa are not discarded; they are classified as unsuitable for a **single-source** photo test and remain candidates for literature, GBIF-media, YAMAP or targeted field evidence. The audit script now records query URLs, timestamps, HTTP status and retry attempts so the next snapshot can distinguish rate limiting from genuine source sparsity.
