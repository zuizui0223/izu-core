# Data and code availability

## Manuscript statement

All primary simulation analyses, frozen design contracts, result summaries, state-separability diagnostics, falsification tables, figure-data exporters and deterministic SVG renderers are version controlled in the public `zuizui0223/izu-core` repository. The primary manuscript does not require a new unpublished field dataset.

The analysis is reproducible from committed frozen outputs and source-traceability files. In particular:

- the original and independent branch-generator results are committed under `data/results/` with the independent run provenance under `data/provenance/`;
- state-generation and state-separability summaries are committed as machine-readable JSON;
- the reusable intervention-based diagnostic implementation is `channel_id/state_separability.py`;
- manuscript figure data are exported deterministically from frozen results and Fig1–Fig4 have repository renderers;
- the 13-system external challenge has a machine-readable source/reference matrix and source-audit paths.

External empirical datasets and publications remain governed by their original repositories, publishers and licenses. The manuscript does not redistribute source files where stable lawful bytes were not recovered. Source DOIs, dataset identifiers, provenance limits and admission boundaries are recorded in the repository audits.

The separate Issue #91 field protocol and the empirical visitor-rate × per-visit-effectiveness (`V_k × E_k`) mapping programme are prospective/optional empirical extensions and are not required to reproduce the primary methodological simulation result.

## Recommended submission wording

> **Data and code availability.** Code, frozen simulation designs, machine-readable results, reproducibility tests, figure-generation scripts and the external-system source registry supporting this study are available in the public `zuizui0223/izu-core` GitHub repository. The primary analysis is a simulation study and requires no new unpublished field dataset. External empirical data remain available from the original publications/repositories under their respective access conditions; source DOIs and provenance constraints are documented in the repository. A versioned archival DOI should be minted for the exact submission release before publication.

## Pre-submission archival action

Before final journal submission, create a tagged release for the accepted submission package and archive that release in a DOI-issuing service such as Zenodo if available. The repository URL alone is sufficient for internal reproducibility during drafting, but an immutable release DOI is preferable for publication.
