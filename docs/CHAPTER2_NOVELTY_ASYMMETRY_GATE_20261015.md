# Chapter 2 novelty gate: coevolving assurance and the far-side floral-investment asymmetry (2026-10-15)

**Status:** source-grounded, retrospective scientific/literature assessment. This file does not replace the active paper, create a new hypothesis family, change Model 3, reclassify a registered null, or establish worldwide priority. The open current-main paper revisions (#544, #542, #543, #536–538) have separate merge/CI gates; this note is intentionally limited to a new independent documentation/audit branch.

## Decision first

**Existing headline is confirmed but not conceptually unprecedented:** reproductive assurance changes how selection favors floral attraction. Fixed-versus-evolvable assurance **is an informative causal Model 3 contrast**, not proof of a new selfing-syndrome law. The strongest *currently verified nontrivial observation* is more specific:

> Allowing assurance capacity A to evolve adds substantial *negative* floral investment I change in the relatively high-replenishment near arm, but *positive relative I preservation* in the more limited far arm, even while total far I declines from the founder under both policies.

This is a **terminal between-treatment comparison**, not absolute investment growth in far. It needs an explanatory historical mechanism before presenting it as a new ecological principle. Local fixed-genotype selection and existing one-repeat original-genome checkpoints do **not** yet identify that mechanism.

### Frozen-source signs: 64 independent visitor histories per reproductive rule × eight nested demographic repeats

Values are raw I units; E−F = assurance *capacity evolvable* minus assurance capacity *fixed at 0.5*. **Fixed A still permits selfing.**

| Source mating regime | Near E−F I at t1000 | Far E−F I at t1000 | Difference of environmental contrasts: Far E−F minus Near E−F | Far I change from founder with A fixed / evolving |
| --- | ---: | ---: | ---: | ---: |
| delayed control | −0.1253 | **+0.0352** | **+0.1605** | −0.3193 / −0.2841 |
| prior selfing | −0.1985 | **+0.0215** | **+0.2200** | −0.3316 / −0.3102 |
| pollen discount | −0.1699 | **+0.0216** | **+0.1915** | −0.3347 / −0.3132 |
| direct assurance cost | −0.0789 | **+0.0218** | **+0.1007** | −0.3146 / −0.2927 |

**The predeclared 4/4 positive interaction and fixed-A isolation contrast are confirmed.** The E−F far intervals in the original decomposition are also positive in each setting. The 78–90% near-side contribution describes an arithmetic difference of final means, **not** a causal mediation fraction. Near is still pollen limited (in a separate fixed-state t400 assay ~22% of ovules receive successful outcross pollen, far ~1%); it is not a pollen-saturated mainland. Far and near are imposed visitor replenishment, **not kilometres, island size or a field guild**.

Source: [four-setting primary readout](../data/results/chapter2_assurance_generality_20261006.json), [source-matched arm decomposition](../data/results/chapter2_assurance_attenuation_decomposition_20261006.json), [fixed-resident gradients](../data/results/chapter2_assurance_gradient_components_20261006.json).

### What the original genomes already exclude (one of eight nested repeats ONLY)

- In authenticated diploid checkpoints for the *first repeat*, E−F far is already positive at t200 (0.0272–0.0599) in all four settings, stays positive t400 and t1000. **Not just a subtraction error or one terminal event.**
- But at far t400 the **expected one-step Price response** E−F is **negative** in all four (−0.00001711 to −0.00012697); the local rare-mutant A-high-minus-A-low I gradient is also negative in far. These are **different estimands**, so the signs do not contradict one another mathematically; the local/one-step estimands do not *explain* the terminal difference.
- Exactly 50/64 far source visitor histories at t400 have no visitors. In the zero-pollen limit the original kernel factorizes as parental W proportional to exp(−c_I I²)×A exp(−c_A A²), and at a monomorphic resident state the local I log gradient is −2 c_I I, **independent of A**. Nonzero pollen or within-population genotype associations change this statement; it is a source-equation limiting case, not a new general law.
- The original one-repeat zero-visitor A–I weighting alignment was tiny and varied in sign, so it is *not an identified universal explanation* of far E−F positivity.

Source: [authentic-checkpoint / one-step Price audit](CHAPTER2_FAR_ASSURANCE_ORIGINAL_GENOME_PRICE_AUDIT_20261015.md) and [algebraic rare-mutant scope audit](CHAPTER2_ASSURANCE_COUPLING_SCOPE_20261015.md) (the latter may be on a separate pending branch at time of reading). The archived source audit does not contain a complete 1,000-step longitudinal genotype/visitor/parentage replay across eight repeats.

## Nearest prior work and exactly where novelty remains undecided

| Literature | Already established | Non-overclaiming distinction / what requires further inspection |
| --- | --- | --- |
| Sakai (1995), *Evolution*, DOI [10.1111/j.1558-5646.1995.tb02287.x](https://doi.org/10.1111/j.1558-5646.1995.tb02287.x) | Co-optimization of attraction allocation and mating system under reproductive costs, nonlinearity and depression. | Not first joint selfing/flower allocation model. Its abstract is not a proof of identical t1000 E/F near/far interaction. |
| Lepers, Dufay & Billiard (2014), *Evolution* 68:3581–3598, DOI [10.1111/evo.12533](https://doi.org/10.1111/evo.12533) | Adaptive-dynamics model of **prior selfing, floral investment, and plant/pollinator population dynamics**, including mixed mating and potential evolutionary suicide. | Closest **theoretical** rival. The retrieved publisher/PubMed abstract confirms broad overlap. **Full paper and supplements were NOT accessible for a complete figure/equation-level check**; cannot certify absence of an equivalent evolving-versus-fixed-A × visitor-contrast or asymmetry. Their pollinator demography is explicitly coupled, whereas here visitor replenishment is imposed exogenously. Our model does **not** establish evolutionary suicide. |
| Bodbyl Roels & Kelly (2011), *Evolution*, DOI [10.1111/j.1558-5646.2011.01326.x](https://doi.org/10.1111/j.1558-5646.2011.01326.x) | Experimental pollinator-removal sequence (selfing traits shift before corolla-size reduction). | Event chronology is not necessity; the fixed-A evolution test is a cleaner *bounded counterfactual*, not a refutation of this natural history. |
| Teixido & Aizen (2019), *Ann. Bot.*, DOI [10.1093/aob/mcz014](https://doi.org/10.1093/aob/mcz014) | In three field populations, delayed selfing weakens pollinator-mediated selection for larger flowers; its importance varies strongly with observed pollination. | Cannot claim discovery of context-dependent assurance weakening attraction selection. Their **field phenotypic selection** is not the same estimand as long-run **genetic evolutionary permission E−F**. No claim our higher-replenishment near effect contradicts their low-visitation effect: the measured variables and interventions differ. |
| Sicard & Lenhard (2011), *Ann. Bot.*, DOI [10.1093/aob/mcr023](https://doi.org/10.1093/aob/mcr023) | Selfing syndrome may arise via multiple selection directions, not necessarily a single selfing-first serial path. | Parallel floral selection hypothesis itself is not new. |
| Busch et al. (2022), *Evolution*, DOI [10.1111/evo.14572](https://doi.org/10.1111/evo.14572) | Real pollinator-removal evolution yields more selfing and rapid genome-wide variation loss; selection, linkage and inbreeding complicate a pure-Ne explanation. | Finite transmission/allele loss is known in principle. Original source-specific **loss of a threshold-required I allele class** under joint sex-specific parental weighting is a narrower model demonstration, not evidence for universal drift shares or a mediation of the far E−F effect. |

**Not established by this audit:** no earlier publication has examined a superficially or mathematically equivalent evolutionary interaction; novelty across all theoretical models; an identified allele covariance / founder / time-lag cause of far relative I preservation; a wild-island phenotype or extinction effect.

## Three falsifiable explanations for the far relative preservation

These explanations are **candidate mechanisms, not new positive results**. None can be distinguished uniquely with just t0/t200/t400/t1000 means from one nested repeat.

1. **State-dependent, multigenerational selection:** early visitor histories create a difference in reproductive weighting which changes as populations move through genotype states. A negative t400 *one-step* difference does not determine the accumulated 1,000-step contrast. Prediction: original annual full-genome, parentage, F/P/S and environmental records show identifiable time windows when treatment differences accumulate; static t400-only extrapolation fails.
2. **Standing-genotype accessibility / sampling:** evolution-permitted A changes which I alleles are present or are transmitted in finite populations, changing reachable outcomes. Prediction: matched checkpoint future experiments with the **same starting diploid genotypes** but different A-expression/evolvability policies change subsequent inherited I trajectories; parent/gamete accounting explains part of that conditional effect. Original separate 2,304-case low-I-allele-loss cohort is **not** already evidence that it caused far E−F in the main cohort.
3. **Bounded-response geometry and genetic composition:** different I starting/distribution states, finite horizon, and response floor/ceiling could produce an apparently positive E−F far contrast without a novel selection reversal. Prediction: genotype-matched contrasts and full per-history distributions show whether relief arises from a few bounded or genetically inaccessible fixed-A paths; the mean by itself cannot rule this out.

### Minimum discriminating experiment *before* claiming a new ecological mechanism

**Do not re-run a broad parameter search just to find a stronger p-value.** First freeze a narrowly identified counterfactual design, parameter choices, controls, inferential unit and a null outcome.

A useful candidate (NOT executed or preregistered by this document):

- Use authenticated original t200 genomes as starting sources (64 matched visitor histories per setting; **do not call saved source histories independent new ecological replicates**). With each **same** diploid founding state and externally held visitor sequence, compare continuation to t1000 under future native versus clamped A expression/evolution policies. Cross the original *evolved-A versus fixed-A t200 population state* with the *future A policy*; both origins receive both futures. Keep random streams, original matching/investment genomes and explicit parentage tracking matched.
- Primary conditional comparison: how much does **future A policy** alter subsequent I change within the identical t200 source population, separately near/far and across all four rules? A second contrast asks whether the **earlier genetic state** changes future I trajectories even when the future policy is common. Preserve both signs, zero-effects and nested histories; do not equate them with the original t0→1000 total causal mediation.
- Record annual **maternal F, paternal P, viable selfing S**, actual sampled parental genomes, Mendelian transmission, mutation and I-allele support. Test exact annual Price/realized accounting; avoid reducing a temporal path to one endpoint or handwaving “drift”.
- Stop claims at the level identified: this design is conditional on *post-treatment source genotypes* and a selected simulation model; it is not natural-history randomization, a complete original treatment mediation fraction, or proof of island adaptation. Replicate in independent founder/visitor families only after feasibility and predeclared stopping/failure rules.

**Literature stop gate:** before claiming uniqueness of the far-side asymmetry, obtain **Lepers et al. (2014) full Methods, figures and supplement** and map its phenotype/trait state, pollination manipulation, coevolution permission, finite vs equilibrium estimand and demographic feedback against this design. The currently retrievable abstracts do not permit a negative “they did not test X” claim.

## Ranked submission/ESJ conclusion as of this audit

- **Confirmed headline (bounded):** under four predeclared Model 3 mating regimes, blocking A evolution does not eliminate low-replenishment I decline; allowing A evolution compresses the between-visitor-regime divergence.
- **Most specific unexpected observation:** additional near investment loss + slight far relative preservation when A can evolve; the early original-genotype far sign and t400 local/Price mismatch make a compelling **unresolved dynamics question**.
- **Separate genetic result:** necessary I allele support can disappear before full locus fixation; in retrospectively selected transitions, even positive expected frequency need not ensure retained copies. Different cohort, not a proven cause of far relative preservation.
- **Separate demographic result:** pilot-informed independently checked conditional stress-history interaction, not pure history-mediated A alleles or evolutionary suicide; this is not a direct novel mechanism for the far sign.

**Decision:** treat the current four-setting confirmation as a publishable model-specific test, **not yet a demonstrated novel ecological principle**. A higher-priority mechanistic contribution remains possible, but requires (i) an identified cause of far relative preservation, (ii) direct comparison to the full closest theoretical antecedent, and (iii) transparent treatment of negative/inconclusive cases.

## Machine-check

\`python -m scripts.audit_chapter2_novelty_asymmetry_20261015\` reads **only** the frozen result JSONs and source-authenticated checkpoint text, prints the distinct effect estimates and their inference scopes, and fails closed if any of the four-source sign/provenance identities changes. \`pytest -q tests/test_chapter2_novelty_asymmetry_20261015.py\` protects these claims. **This script does not make new biological trajectories or validate bibliographic priority.**
