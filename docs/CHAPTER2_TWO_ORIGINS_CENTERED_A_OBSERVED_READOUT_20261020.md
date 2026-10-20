# Observed third-source A-expression intervention: 3840 technical paths

**2026-10-20 | Source-admitted ENGINEERING readout, not scientific confirmation or a field colonization estimate.** All data in this note are based on the successful [Chapter 2 scientific-gate Actions run #39281432251](https://github.com/zuizui0223/izu-core/actions/runs/39281432251), `scientific-gate` job `118156720195`, source HEAD `bd262063fb0be6d497f4fa15071e3ae936b3d2fe`. That same original HEAD also had **general CI success** (run #39281431898). The experiment has 24 artificial new source genotypes in a THIRD disjoint source namespace, 4 artificial B×visitor environmental cells, 8 nested repeat histories, 768 original source×environment×repeat candidate assignments, and 5 post-establishment phenotype policies = **3840 trajectories**. It is not 3840 independently sourced taxa or islands. Source code was `scripts/chapter2_two_origins_technical_20261019.py` and `scripts/chapter2_two_origins_postestablishment_probe_20261019.py` at the stated source HEAD.

## Question and intervention

**Does the initial state of A predict short-term population fate, or does a change in the *mean expressed A* after settlement contribute to six-update survival within an already established synthetic source lineage?**

Exactly the same artificial source genotype, arrival draw, one native Model3 establishment event and genotype at the policy fork are used for **native**, **clamp_A**, **clamp_I**, **clamp_A_I**, and **center_A_mean**. All branches initialize separate generators with the same random-stream master. Random-number consumption can diverge once the trajectories differ.

- `native`: express current inherited diploid A/I traits in the original Model3 reproduction ledger, where the alleles segregate.
- `clamp_A`: replace expressed A in **every individual** by the original source *population* mean A while inherited A alleles remain segregating; standing phenotypic among-individual differences are lost.
- `center_A_mean`: shift all **expressed** A alleles by the common offset `A_source − A_current`, retaining each current allele's and individual's deviation around the mean. The true, unshifted A alleles continue to be inherited. This acts on expression only; zero mutation/immigration and clipping is disallowed (fail-closed if any shifted allele exits [0,1]).
- `clamp_I` and `clamp_A_I`: comparable expression treatments for I and for both loci, with inherited genotypes untouched.

None of these is a selective suppression of **A mutation, A Mendelian genetic evolution, or all post-colonization selection**. Moreover the source genotype pool is artificial and had two founding individuals per source. All policies share a short six-reproductive-update horizon.

## Original numerical outcomes: source-registered counts

| Resource | Visitors | Native alive /192 | Flat-A clamp alive /192 | Centered-A mean clamp alive /192 | Native versus centered: both survive | Native only | Centered only | Neither |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| B4.5 | 0 | **50** | **50** | **50** | 49 | 1 | 1 | 141 |
| B4.5 | 4 | **67** | **67** | **67** | 67 | 0 | 0 | 125 |
| B8 | 0 | **91** | **91** | **91** | 90 | 1 | 1 | 100 |
| B8 | 4 | **118** | **118** | **118** | 118 | 0 | 0 | 74 |
| **Totals** | — | **326/768** | **326/768** | **326/768** | **324** | **2** | **2** | **440** |

All five columns' event counts were read from the original source Actions technical-run log. The paired-survivor overlap sums to 324; four original candidate assignments have discordant survival outcomes for native versus centered-A expression, **despite** equal aggregate survival. For **native versus the original flat-A clamp**, the gate printed *identical four sets of marginal and paired 2×2 counts* (49/1/1/141, 67/0/0/125, 90/1/1/100, 118/0/0/74). Equality of these contingency **counts does NOT itself prove that flat and centered clamps selected the exact same individual lineage–reset identities**; this needs a direct paired policy-to-policy test, not an inference from matching aggregate cells.

In the 324 **native/centered co-survivor** branches the native−centered mean A displayed in the original job was +0.003161, −0.004024, +0.003262, +0.000198 across the four contexts respectively (unweighted within each context's matched survivor set; these are **survivor-conditioned, post-treatment-selected trait contrasts**, not mean treatment causal effects). Small values can reflect both short horizon and limited original founder variation. At B8/no visitors the flat policy had one extra survivor relative to native in the low-A hint stratum but one fewer in the middle stratum, cancelling aggregate effects. The source ranks shown elsewhere are conditional on these 24 artificial genotypes, not an independent replicated mainland dataset.

## What can and cannot be concluded

**Evidence compatible with initial-state filtering:** In the 24+24 artificial source-disjoint pilot, source-A categories improved six-update survival forecasts (held-out Brier 0.224204 ecology-only, 0.179435 ecology+A and 0.222697 ecology+I). In the separate third technical source sample, allowing A expression to track genotypes or keeping the expressed A *mean* at its original source value had **equal observed marginal occupancy counts** in each environment over six updates. The centered-A intervention reduces a confound of the original flat clamp by preserving contemporary allelic/individual expression differences.

**Explicit limitations:** The comparison still does **not** causally identify mainland import versus post-establishment genetic evolution; original founding was native in every arm, the mean-expressed-A intervention may affect individual viability and reproductive competition, and allele frequencies continue to change. Equal marginal occupancy counts under just four synthetic B×visitor conditions do not establish biological equivalence, zero genetic selection effect, or a general theorem. No long-horizon or mutation/immigration-enabled test was performed. The original Model3 80-update survival contrasts in PR #609 use other source genotypes, different policies and different ecological history; do not compare them as though only time differs.

**Decision:** The proposed asymmetric origin hypothesis remains **not confirmed**. More strongly, short-horizon I evolution was weak in the earlier source-disjoint pilot, so the exclusive proposed “A sorted; I evolved after settlement” story is currently incomplete. A causally cleaner full-history disaggregation and an independent-source/island experimental design with realistic Ch1 measured SC/floral proxies remain necessary.

## Verification and next gate

- The original source job passed dedicated [policy tests](../tests/test_chapter2_two_origins_postestablishment_probe_20261019.py), including preservation of A allele/individual deviations, common initial assignments, stage/count conservation and four-policy source fork.
- This document states **the exact displayed source counts**; an additional regression can protect them from future tool/code changes, but rerunning the native generator is not another independent scientific confirmation.
- A fully new true genotype-evolution-blocked control (not just an expression clamp) is future work requiring a distinct design; avoid silently changing the original biological study.
