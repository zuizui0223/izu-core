# From Model 3 payoff feedback to an empirically falsifiable island test

**2026-10-08 status:** This is an evidence/measurement handoff, **not a completed ecological validation or new numerical simulation**. Four-setting assurance-mediated divergence compression was prospectively confirmed in merged PR #411. The many later PR #413 persistence and trait-order experiments include explicitly failed preregistered tests and synthetic post-outcome stress grids. Their success/failure labels are retained and they do not alter the active Ecology Letters manuscript.

## Where the three chapters actually stand

| Source | Observed unit and completed evidence | What it can test | What is still missing |
|---|---|---|---|
| `zuizui0223/island` (Ch1, current post-2026-10-04 traitwise surface) | Contemporary species/island flora, corrected geography, four strata; separately published GloPL supplementation studies. Self-compatibility is a recurrent positive isolation correlate and pollen limitation rises with isolation. | Recurrence of reproductive function, geographic heterogeneity and independent pollen constraint | Same-population ancestral state, effective visitor contact, realized mating, genetic selection and future persistence |
| `zuizui0223/izu-core` (Ch2, merged #411) | Controlled synthetic visitor histories, reproductive payoffs, female/male/selfing accounting, inheritance and finite ABM; 64 independent histories across four prespecified reproductive settings | Assurance evolution is *not necessary* for far-side floral-investment decline and can compress environmental divergence, mostly through additional near-side investment decline | A real-world scale and identified natural trait mapping. No natural-island long-term rescue rate |
| `zuizui0223/shimahotarubukuro` (Ch3) | Directly reviewed `Campanula microdonta` specimens: **218 flowers from 125 plants** across Oshima/Toshima/Niijima/Shikinejima/Kozushima. Plant-level and site-corrected island differences in body size, mouth, organ and nectar guide; strong common size/allometry factor with some residual departures | The *phenotypic endpoint* that actually differs within one Izu lineage | Those particular tagged plants' complete visitor effectiveness, selfed/outcross genetic parentage, maternal+paternal fitness and past-pollinator transitions |

**Do not substitute** the old 2026-09-17 Ch1 manuscript for its active 2026-10-04 corrected source-matched, traitwise submission. Ch3's flower labels cannot be interpreted as 218 independent plant-level samples; 125 plants and sites are the hierarchy. Ch3's nectar-guide and mouth changes do *not* establish historic Bombus loss. Chapter 1's present species-island composition cannot separate arrival filtering from local evolution.

## Testable island ecology question

A regional flower syndrome might appear weak because assurance evolution has pulled *less pollinator-limited* populations toward smaller investment, not because there was no selection. The mechanistic prediction is **not** that isolated islands must have small flowers; it is that assurance capacity changes the marginal value of attraction most strongly when functional outcross pollen transfer remains effective.

For field confrontation, on the **same observation units**, first independently measure:

1. **Effective pollination**: stigma/anther contact and transferred compatible pollen, not simple visitor count, species occurrence or geographic distance.
2. **Assurance capacity**: autonomous self seed set using isolation controls, and self-compatibility / realized selfing / inbreeding depression assessed *separately* with bagged, controlled self, controlled cross and progeny viability evidence.
3. **Floral investment**: a *predefined* plant-level proxy (e.g. corolla area or visual-guide investment) from the existing Ch3 measurement system, checked for scale and allometry. This is a proxy only; Model 3's abstract I encompasses reproductive investment, not corolla area, pigmentation or access by identity.
4. **Total viable parental return**: viable selfed seed output, viable maternal outcross output and a legitimately attributable paternal outcross component. At present, the existing corolla and GloPL archives do **not** provide this complete joint panel.
5. **Repeat or pedigree evidence**: enough time/genetic transition information to distinguish post-establishment selection from founders, immigration and extinction filtering. Without this, the direct model mechanism cannot be assigned historically to a named island.

The falsifiable *baseline-model* prediction is an interaction, not an island-distance coefficient. In notation, let `beta_I(A,V)` be the marginal parental-fitness return to investment at assurance state A and measured pollinator service V. A candidate contrast is:

`[beta_I(A_high,V_high)-beta_I(A_low,V_high)] - [beta_I(A_high,V_low)-beta_I(A_low,V_low)] < 0`.

This corresponds to the local rare-mutant baseline asymmetry, **not** to a universal inequality for all parameter values. The expression should be applied to natural data only after measurement validity, species/site replication and an appropriate selection estimator are established. Natural covariance alone would show association, not counterfactual selection; a direct causal claim would require interventions or identified parentage design.

## What would count against the mechanism

- Measured compatible pollen transfer does not differ between apparently contrasting sites/islands, invalidating the visitor-replenishment proxy.
- Strong assay-defined assurance changes the attraction-return gradient equally or more in the less limited group, contrary to the declared local gradient asymmetry.
- Future common-environment populations with different historical regimes show no inherited differences once ancestry and island founder sorting are independently controlled.
- Within-lineage genetic/phenotypic change differs substantially from the prospective sign predicted by a fitted transport model; neither geographic isolation nor the sign of a corolla-area difference rescues a failed test.

**No result is currently available** for this new joint empirical sign test. A lack of field columns is a measurement gap, not confirming evidence.

## Progress and decision

- Completed now: cross-repository evidence inventory; a machine-readable pre-outcome contract `data/design/chapter2_island_empirical_mechanism_contract_20261008.json`.
- Research stop on synthetic branch: the A-allele dispersion ablation produced a pooled **+0.49 percentage-point** `q=0` minus `q=1` occupancy difference across 1,024 matched conditions, with only **four previously exposed independent visitor histories**, so it neither identifies genetic-variance mediation nor justifies another opportunistically tuned shock experiment.
- **Primary future data task:** build a tagged-plant, site-linked observation table for effective pollination, controlled self/cross breeding outcomes, mature viable seed output and pollen-donor assignment linked to the existing Ch3 trait observations. First report column availability and missingness **without fitting** a model.
- Only after new prospective field data pass completeness and validity gates should an ecological selection-gradient comparison be fit. Distinguish the empirical field paper from the already confirmed Ch2 simulation claim.

The field handoff is intentionally **unsubmitted and falsifiable**; do not call it an EL-level verified island prediction.
