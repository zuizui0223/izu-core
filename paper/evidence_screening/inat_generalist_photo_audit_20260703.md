# iNaturalist generalist-photo availability audit - 2026-07-03

## Source snapshots

- Initial audit workflow run `28652998948`, artifact digest `sha256:a2eb953341249da1a7b196ea9243ca0a6aa3330a8c602e5caef12980c075ca65`.
- Retried audit workflow run `28653414921`, artifact digest `sha256:d099f4b68f5f7df0c7a7fe4085c33a71db0dcd2080c002e63f6cc673dedc3d6d`.
- Query scope: research-grade iNaturalist observations with photos inside declared radii around six island proxy points for 16 protected generalist-control candidates.
- Boundary: these are source-specific availability counts. They do **not** verify true island assignment, wild status, flowering stage, trait visibility, pollination, effective visitor identity, or biological absence.

## Retry result

The retry completed all **96 of 96** proxy queries with HTTP 200. The first-run failures were therefore retrieval failures, not zeroes.

| Candidate | proxy cells with records | returned records | Next action |
|---|---:|---:|---|
| *Pittosporum tobira* | 5/6 | 24 | build blinded image queue; predeclare floral trait |
| *Ajania pacifica* | 5/6 | 19 | build blinded image queue; retain flowering-stage decision |
| *Angelica keiskei* | 5/6 | 6 | inspect flower visibility and taxon/geometry before scoring |
| *Hydrangea macrophylla* | 4/6 | 15 | predeclare fertile-flower versus sterile-display-sepal trait |
| *Hydrangea involucrata* | 4/6 | 6 | predeclare fertile-flower versus sterile-display-sepal trait |
| *Farfugium japonicum* | 3/6 | 18 | redo phenology screen before any trait score |
| *Rubus trifidus* | 3/6 | 12 | inspect flower visibility before scoring |
| *Peucedanum japonicum* | 3/6 | 4 | limited candidate; inspect before further collection |

The remaining eight species have at most two cells with records, and *Elaeagnus umbellata* has none in this source snapshot. They remain literature, GBIF-media, YAMAP or field targets; they are not biological absences.

## Island-level sparsity

Across the 16 candidates, returned records were uneven: Oshima 54, Toshima 1, Niijima 7, Kozushima 14, Miyake 29, and Hachijo 11. The sole Toshima record was *Angelica keiskei*. This confirms that single-source iNaturalist cannot carry a full step-versus-cline test across the chain, especially at the critical Oshima-Toshima boundary.

No conclusion about trait direction follows from availability counts. The next eligible operation is a blinded image-quality and phenology review for the eight candidates above, with original coordinates and taxon labels checked before any island assignment or trait score.
