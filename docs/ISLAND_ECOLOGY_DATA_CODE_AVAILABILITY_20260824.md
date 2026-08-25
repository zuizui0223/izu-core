# Data and code availability — island ecology manuscript

Updated: 2026-08-25

## Anonymous peer-review statement

All primary numerical results in this study derive from frozen simulation outputs, matched intervention summaries and source-audited qualitative external-system assignments. The code required to reproduce the primary analyses, the frozen result files used for figures and tables, figure-generation scripts, source-audit matrices, falsification records and regression tests will be provided to reviewers in an **anonymized review archive** or suitable private peer-review repository.

The current primary claims require **no new unpublished field dataset**. The external island systems are literature-derived qualitative state challenges; their source references and claim boundaries are documented in the Supplementary Reference Matrix. External sources were not used to choose model parameters, random seeds or mechanisms.

Author-identifying public repository links are omitted from the anonymous review manuscript. Reviewer access will contain the scientific materials needed to evaluate and reproduce the submitted analysis without exposing author identity.

## Final publication statement

Before final publication, the exact accepted code and frozen analysis materials should be deposited in an immutable versioned archive with a persistent DOI. The final public Data Availability statement should cite that DOI and, where appropriate, the public source repository. The archived release should correspond to the accepted manuscript state rather than a moving development branch.

## Minimum review archive contents

- `docs/ISLAND_ECOLOGY_JECOLOGY_SUBMISSION_DRAFT_V2_20260824.md` or its anonymous formatted derivative;
- `docs/ISLAND_ECOLOGY_JECOLOGY_SUPPLEMENT_20260824.md`;
- frozen primary simulation result summaries used in the manuscript;
- independent branch-generator replication result and its frozen design;
- network-context and assurance robustness results;
- `data/results/simulation_manuscript_figure_data_frozen.json`;
- `data/design/simulation_manuscript_external_system_reference_matrix.json`;
- `data/results/simulation_manuscript_falsification_table_frozen.json`;
- ecology-first Fig1–Fig4 renderers and plotting inputs;
- Supplementary FigS1 state-separability renderer/input;
- exact-regeneration and claim-boundary regression tests;
- a README explaining reproduction commands and the distinction between synthetic mechanism results and qualitative external challenges.

## Scope boundary

The review archive is intentionally limited to materials needed to evaluate the claims made in this manuscript. Independent research programmes, prospective field studies, and observation-design work that are not used by the submitted analyses are outside the paper package and are neither dependencies nor validation requirements for this study.
