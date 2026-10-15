# Lepers (2014) full-text check and Q3 priority correction — 2026-10-15

**Evidence rank:** original paper embedded as Chapter 3 of the author's 2015 doctoral thesis (Université de Lille, 130 PDF pages). This corrects the nearest-prior-art characterization in `CHAPTER2_NOVELTY_ASYMMETRY_GATE_20261015.md`; it **does not rewrite** the frozen original Model 3 results, the single active Ecology Letters draft, or claim worldwide priority.

## Verifiable original full text

- Author-deposited thesis: https://pepite-depot.univ-lille.fr/LIBRE/EDSMRE/2015/50376-2015-Lepers.pdf
- Lepers, Dufay & Billiard (2014), *Evolution* 68:3581–3598, DOI https://doi.org/10.1111/evo.12533, reproduced in thesis PDF pages **57–73** (zero-indexed PDF pages; article's own printed pages 1–17).
- **PDF page 63**, section “DESCRIPTION OF THE MODEL OF SELFING EVOLUTION”: resident with prior selfing fraction `s`, invading phenotypic mutant `s′`, ecological equilibrium and small-effect mutation / adaptive dynamics. The paper **also explicitly reports individual-based simulations** with stronger mutations and multiple simultaneous mutants (page 63).
- **PDF pages 72–73**, Appendix B “Algorithm of the Stochastic Model”: each individual has **phenotype `s_i`**, a prior-selfing fraction; plant/pollinator births and deaths are stochastic events; mutant newborn phenotype is sampled around the parental selfing phenotype. Mutation probability `10^-3`, Gaussian step SD `10^-2` or `0.1`; ten replicate simulations per parameter set; population size deliberately large enough to avoid extinction from demographic stochasticity in constant-selfing controls. They explicitly state the stochastic individual-based results **were similar to the deterministic results** (page 73).
- **PDF page 72**, Appendix A: the paper calls its model *phenotypic*, with half resident/half mutant type from crosses. The paper's floral investment/pollination cost appears as **`F[s]`, a phenotypic function of the selfing trait**, rather than an independently inherited diploid floral-investment locus (PDF pages 62–63, 72). This is a distinction in the examined genetic architecture, **not evidence** that every genetically explicit two-trait model is original.
- Lepers’ principal outcome is evolutionarily stable **prior-selfing fraction** (including mixed mating and evolutionary suicide), not a factorial **evolvable assurance capacity A × independently inherited investment I × imposed visitor sequence**, threshold-defined *order* and genotype-specific access to a **future** I decrease.

## Mandatory correction of previous priority matrix

| Previous shortcut | Correct full-text statement | Consequence |
|---|---|---|
| “Sakai / Lepers / Spigler: deterministic; ours: finite individual-based” | **False for Lepers.** It included stochastic individual-based simulations, Appendix B. | No claim of introducing stochastic IBM to mating-system/pollinator theory. |
| “Lepers assumes infinitesimal mutations only” | Adaptive-dynamics analysis uses small-effect invasion, **but its IBM also uses larger-effect mutations and coexistence of mutants**. | Cannot distinguish on mutations being strong or concurrent alone. |
| “Lepers coevolves floral investment and selfing as two inherited traits” | Floral pollination cost/investment depends on `F[s]` in their phenotypic selfing system; a separately segregating diploid I locus was not identified in the inspected chapter. | More defensible *architecture-specific* difference: two independently inheritable A/I dimensions, standing genotype support, Mendelian sampling and pathwise ordering. |
| “Deterministic versus finite disagreement is novel by itself” | Their stochastic comparison showed **agreement** in their tested, deliberately large-population settings. | The candidate is **the ecological/genetic boundary of forecast failure** for specific A/I responses at low visitor supply, **not the comparison method itself**. |

## Source-specific boundaries retained

1. The original Model 3 Q3 finite-versus-density 3/32 and 2/32 order outcomes came from **different cohorts** than the original four-setting far E−F I experiment. They are **not an identified cause** of that far-side sign.
2. The 64×8 four-setting far E−F endpoint has positive **relative preservation**, but both treatment arms’ far investment decline from the founder is negative. Its one-repeat t200 and t400 checkpoints do not identify the annual cause.
3. In the absence of delivered pollen, the original Model 3 local investment log-gradient is `−2*c_I*I`, **not zero**. Assurance no longer changes that *local gradient* but selection against costly investment remains. “Assurance evolves so investment selection stops” is not supported.
4. An equivalent mathematically specific treatment in other literature **has not been exhaustively ruled out**. Access to this full primary paper closes the largest *named* priority gap, not global novelty review.

## Decision for the one-letter manuscript

- **Q1** explains the reproductive selection background, citing Sakai and Lepers as substantive antecedents.
- **Q2** reports contingent response order and genetic access. Sequence is not necessity.
- **Q3** is the leading candidate for a nontrivial contribution: explicit genetic accessibility and finite inherited realization can prevent an expected two-trait response **while the population still exists**; this is bounded to matched, stated model contexts and thresholds, not universal drift estimates.
- **Q4** is a separate conditional survival consequence, not an estimated A-first-mediated rescue effect.
- The far relative preservation is a **mechanistic puzzle**, not a demonstrated genetic law; test it with the frozen 2×2 t200 origin × future policy design described in `docs/protocols/chapter2_far_t200_history_swap_20261015.json`.

No journal claim/DOI, source manuscript headline change or new ecological confirmation is made by this note.
