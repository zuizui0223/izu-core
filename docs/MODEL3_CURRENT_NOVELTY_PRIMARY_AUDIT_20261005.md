# Current Ch2: primary-literature novelty and presentation audit

Checked 2026-10-05. Targeted nearest-precedent search, not an exhaustive systematic review or certification of priority. No simulations, biological settings or frozen results changed. The user stopped the high-resolution 1,000-update campaign: full positive-mutation ABM/density/PDE corroboration is not an available result. Earlier completed experiments retain their own scope.

## Immediate bibliographic correction

The earlier continuum audit attributes **Reproductive assurance weakens pollinator-mediated selection on flower size in an annual mixed-mating species** to Rodger et al. (2019). Its authors are **Alberto L. Teixido and Marcelo A. Aizen**, DOI [10.1093/aob/mcz014](https://doi.org/10.1093/aob/mcz014). Correct manuscript references wherever this attribution propagated. This audit changes only this file.

## Primary precedents and what they rule out

Access labels: `abstract` means publisher/author-institution abstract; `indexed text` means text retrieved by web search from the primary paper, with direct PMC access blocked by CAPTCHA; `full HTML` means publisher full article was available. These levels should not be described as a complete equation-by-equation literature review.

| Primary study | Verified content and access | Consequence for Ch2 |
|---|---|---|
| [Bodbyl Roels & Kelly 2011](https://academic.oup.com/evolut/article-abstract/65/9/2541/6854748), DOI 10.1111/j.1558-5646.2011.01326.x | Publisher abstract. Five generations of bee/no-bee experimental evolution; autonomous reproduction improved; authors explicitly interpret a sequential selfing syndrome. | Selfing-first is not a new general hypothesis. Our threshold-crossing result should establish order in the declared model and then be contrasted with a necessity intervention. |
| [Sakai 1995](https://doi.org/10.1111/j.1558-5646.1995.tb02287.x) | Publisher abstract. Resource allocation, attraction, competing/delayed selfing and inbreeding depression jointly determine evolutionarily stable allocations. | Neither attraction costs nor joint selfing/attraction optimization is new. The present inequalities are useful model-specific derivations, not the first trade-off theory. |
| [Charlesworth & Charlesworth 1987](https://academic.oup.com/evolut/article/41/5/948/6870541), DOI 10.1111/j.1558-5646.1987.tb05869.x | Publisher abstract. Male/female fitness and attraction allocation already linked, including resource-limited maturation. | Inclusion of male function strengthens adequacy, not novelty by itself. |
| [Harder & Aizen 2010](https://pubmed.ncbi.nlm.nih.gov/20047878/), DOI 10.1098/rstb.2009.0226 | Primary abstract and indexed primary text. Pollen limitation allows several reproductive responses; fertilization, offspring production and genetic contribution differ; adaptive routes are context dependent. | Do not claim first discovery that low pollen need not uniquely select selfing or small flowers, or that seed numbers differ from fitness. |
| [Teixido & Aizen 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6589515/), DOI 10.1093/aob/mcz014 | Indexed primary abstract. Tuberaria guttata field manipulation: reproductive assurance weakens flower-size selection; inbreeding depression prevents complete alleviation of pollen limitation. | Compensation with a remaining viability deficit has direct empirical precedent. Use our intervention to quantify its relation to investment returns, not present the general idea as unexpected. |
| [Van Etten et al. 2015](https://pure.psu.edu/en/publications/the-compounding-effects-of-high-pollen-limitation-selfing-rates-a/), DOI 10.1093/aob/mcv118 | Author-institution abstract and [indexed primary methods/results](https://pmc.ncbi.nlm.nih.gov/articles/PMC4590329/). New Zealand Sophora: pollen limitation, substantial selfing and inbreeding depression leave low viable output; total visits and effective bird visits need not predict the same deficit. | This is a particularly relevant island-region precedent. Seed/deficit metrics cannot automatically stand for viable recruitment, and visitor identity matters. |
| [Busch et al. 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC9543508/), DOI 10.1111/evo.14572 | Indexed primary methods/discussion. Nine-generation pollinator exclusion, selfing evolution, loss of genomic variation; stochastic loss can make replicated adaptation nonparallel. | Loss of adaptive variation after pollinator loss is known. Our genetic-state comparison is a mechanistic/numerical explanation, not first evidence of that phenomenon. |
| [Morgan, Wilson & Knight 2005](https://scholars.duke.edu/publication/806453), DOI 10.1086/431317 | Author-institution abstract. Pollinator foraging, Allee effects, selfing and population dynamics jointly alter persistence and evolutionary outcomes. | Eco-evolutionary feedback and selfing-mediated persistence thresholds are not empty theoretical territory. |
| [Zell et al. 2025](https://nph.onlinelibrary.wiley.com/doi/10.1111/nph.20234) | Publisher full HTML. Global island colonization analysis already combines breeding system, lifespan, symmetry and arrival opportunity, separating arrival, establishment and subsequent evolution conceptually. | Do not frame all global floral/island trait analysis as absent. For Q1, claim the specific colour-inclusive, seven-trait coverage only after its own comparative scope audit. For Q2, ongoing visitor replenishment in an established plant population differs from plant-colonization filtering. |

Searches included exact titles above and combinations of island colonization/extinction, floral evolution, selfing, simulation, variable pollination environments, allocation and viable offspring. The search also found Morgan & Wilson (2005), **Self-fertilization and the escape from pollen limitation in variable pollination environments**, DOI 10.1111/j.0014-3820.2005.tb01050.x. The [publisher issue record](https://academic.oup.com/evolut/issue/59/5?browseBy=volume) verifies the reference; its equations were not reviewed here. It is a priority follow-up before any claim that environmental variability is new.

## Strongest current contribution

The defensible contribution is **separating three questions under one explicitly generated island exposure: what selection favours, what changes first, and what change requires another trait to evolve**. Persistent isolation acts on visitor replenishment; it does not prescribe a floral optimum. This links island assembly to reproductive economics. It does not prove that the combination has never appeared elsewhere.

Current evidence inspected in repository documentation: `MODEL3_PERSISTENT_PROCESS_RESULTS_20261005.md`, `MODEL3_ASSURANCE_INTERVENTION_RESULTS_20261005.md`, `MODEL3_POLLEN_FITNESS_PATHWAYS_20261005.md`, `MODEL3_TRAIT_POLLEN_RESULTS_20261005.md`, `MODEL3_PDE_CLOSEOUT_20261004.md`. This literature audit does not independently reconstruct raw arrays.

### Priority 1: sequence does not identify necessity

Capacity reaches the declared change threshold first in 51/64 delayed-plus-cost far-history means, with 13 ties. The separate fixed-capacity intervention nevertheless retains investment decline. Show these together, not as two disconnected claims. This makes the useful result the distinction between temporal order and mechanistic necessity. Fixed capacity remains 0.5 and realized selfing can change; do not label this a no-selfing treatment or a complete mediation experiment. Nor is equal numerical change on two abstract axes guaranteed biologically comparable.

Suggested headline: **Selfing capacity can change first, but its evolution is not required for attraction investment to fall.**

### Priority 2: reproductive economics, not simply visitor counts

At unchanged plant state, the delayed-setting investment derivative changes from +0.5793 to -0.7004 between near/far visitor exposures at snapshot 400. The outcross contribution declines substantially; the selfed component partly offsets that difference. These components include allocation effects and must not be called pure benefits and pure costs. Visitor number and identity change together. This provides an upstream explanation for investment decline without first invoking evolved selfing capacity.

Suggested headline: **Isolation changes the return on attraction, even before plant traits evolve.** Attach “in the model” in the caption.

### Priority 3: less deficit need not mean more viable offspring

In the whole-population fixed-trait assay, higher investment under far exposure slightly reduces fractional viable pollen deficit but lowers viable maternal offspring (delayed: -15.72, descriptive interval [-17.05,-14.13], all 48 plants). This is a clear communication hook because it distinguishes a relative shortage metric from an absolute reproductive outcome. Its existence is consistent with older allocation theory; its value here is the explicit controlled contrast connecting the syndrome discussion to Q1 H3/H4. It is not a rare-mutant selection estimate or an evolutionary trajectory.

Suggested headline: **Better pollen receipt is not necessarily a better reproductive return.** Explain the cost/denominator, rather than implying a paradox in pollen biology.

### Priority 4: conditions, not a universal syndrome rule

The corrected joint local inequalities specify when attraction decreases and assurance increases, including male function and fixed-resident competition. They turn an assumed syndrome arrow into a conditional region. The 900 finite-difference checks validate implementation, not ecological generality. Use one diagram of two conditions overlapping; retain formulas and assumptions in paper methods/SI. Do not use the old population-output derivative as an invasion criterion.

### Priority 5: genetic-state and finite-population qualifications

The homozygote/heterozygote counterexample proves that identical present phenotype distributions need not generate identical offspring variance. Its strongest role is explaining why the reproductive model retains genetics. It is not proof that drift caused a particular observed island difference. The completed zero-mutation bounded-support comparisons and reduced mutation diagnostics can support this explanation at their documented scope. Stopped high-grid long calculations cannot support a full positive-mutation convergence claim. PDE is a mutation approximation inside the larger sexual-inheritance model, not a fourth independent ecological result.

## Paper and poster arrangement

**Paper:** lead with persistent isolation and the reproductive-return mechanism; put sequence and the fixed-capacity intervention in one figure; next show pollen deficit versus viable output; then present finite/deterministic results with the admitted scope. Threshold derivation is a mechanistic main-text result with detailed equations in methods. Place approximation diagnostics, failed gates and stopped high-grid scope in SI, not in the abstract as a completed comparison.

**Poster:** one causal strip (isolation -> fewer successful replenishments -> changed pollen transfer -> two reproductive payoffs), then three evidence panels: (A) changed investment return, (B) sequence beside fixed-capacity control, (C) fractional deficit versus viable offspring. A small threshold inset explains that both arrows are conditional. Do not spend equal area on ABM/density/PDE terminology; label methods by the ecological question they answer. Retain Q1's independent observational claims and avoid equating investment with literal colour or matching position with floral accessibility.

The selfed component's partial offset, the order/necessity distinction, and the deficit/output divergence are informative qualifications that should survive simplifying the poster. A standalone claim that “isolation favours selfing and smaller flowers” loses most of the contribution.

## Claim ceiling

No supported priority claim here is “first selfing-first sequence”, “first pollen-limitation trade-off model”, “first finite-population constraint on adaptation”, “PDE proves island endpoints”, or “global island floral traits were never studied”. The contribution is a coherent, controlled model-based explanation of **when related syndrome components share an ecological driver yet differ in timing, necessity and reproductive consequences**. Its scope is the declared visitor-arrival contrast and reproductive rules; natural geographic calibration and historical reconstruction remain separate.
