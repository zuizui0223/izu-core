# What prevents an expected reproductive return from becoming the same inherited trait response?

**Focused Chapter 2 Q3 mechanism audit — 10 October 2026.** The manuscript-ready four-setting result and the separate capacity/persistence companion are merged into main. The enormous source-only PR #452 is NOT merged. This file begins a new, bounded diagnostic of **one-generation finite realization**, not a new evolutionary history or an assertion that a positive source selection coefficient must lead to a negative long-run response.

## Source and observation level

The frozen source is Model 3's \`scripts/model3_island/reproduction.py\` and \`scripts/model3_island/population.py\`. The first computes a viable offspring parent matrix (outcross donor i × mother j; selfed contribution is added to the diagonal). The second draws a retained number of resident recruits, samples a parental pair independently for each recruit proportional to viable seed weight, and then transmits one random allele at each locus from each parent.

For a focal locus, let adult i have allele values \((a_{i1},a_{i2})\), phenotype \(z_i=(a_{i1}+a_{i2})/2\) and gamete variance \(v_i=(a_{i1}-a_{i2})^2/4\). Let \(Q_{ij}\) be the **normalized source donor×mother viable-offspring pair probabilities** (including source viable selfing on the diagonal). A single resident offspring from donor i and mother j has expected phenotype

\[
m_{ij}=(z_i+z_j)/2
\]

and variance conditional on its sampled parents

\[
s_{ij}^2=(v_i+v_j)/4 .
\]

Hence the one-step offspring trait variance has an **exact law-of-total-variance decomposition**:

\[
\mu=\sum_{ij}Q_{ij}m_{ij},\qquad
V_{\mathrm{offspring}}
=\underbrace{\sum_{ij}Q_{ij}(m_{ij}-\mu)^2}_{\text{parent-pair sampling / parentage lottery}}
+\underbrace{\sum_{ij}Q_{ij}s_{ij}^2}_{\text{Mendelian segregation}}.
\]

Conditional on an already observed survivor set of size S with sum of phenotypes \(Z_S\) and **R retained resident offspring**, with zero immigrant recruits and zero new mutations:

\[
E[\bar z'|S,R]=\frac{Z_S+R\mu}{S+R},\qquad
\mathrm{Var}(\bar z'|S,R)
=\frac{R\,V_{\mathrm{offspring}}}{(S+R)^2}.
\]

These equalities are conditional on the source model's random-choice order; they are not unconditional first-year (or thousand-year) predictions. The source's **Binomial survival, Poisson resident birth attempts, K-limited recruitment, immigrant competition and genetic mutation** remain outside this controlled variance identity. Survivor and recruit counts must therefore be separately modeled to extend to future occupancy or a true evolutionary consequence.

## The paired null: identical outward floral trait, different hidden genetics

A direct source reproduction fixture has four adults with exactly the same *observed* phenotypes at all three loci: matching 0.5, investment 0.35 and assurance 0.5, with four identical visitor functional types, pollen parameters and demographic K=48. Only the hidden matching-locus diploid configuration differs:

- **Homozygous:** every adult has matching alleles 0.5 / 0.5.
- **Heterozygous:** every adult has matching alleles 0 / 1.

Because the source pollen-transfer and ovule functions use the **expressed trait mean**, these two starting states must have identical visitor matching, maternal/paternal/self contributions, group expected viable seeds, the parental-pair lottery and **mean expected offspring phenotype 0.5**.

However the conditional variance differs:

| Number R of retained residents, S=0 | Homozygous: Var(mean) | Heterozygous: Var(mean) |
|---:|---:|---:|
| 1 | 0 | 0.125 |
| 2 | 0 | 0.0625 |
| 4 | 0 | 0.03125 |
| 8 | 0 | 0.015625 |

In the heterozygous state, an individual offspring has a 0, 0.5 or 1 matching phenotype with respective probabilities 0.25, 0.5 and 0.25. For four retained offspring, the **exact conditional probability that the next-generation mean is at or below the original 0.5 is 0.63671875**, using a B(8,0.5) gametic-allele count. The homozygous mean remains exactly 0.5.

**Interpretation:** even perfect knowledge of adult phenotypic means and expected reproductive seed output does not identify how variable the finite offspring mean will be. The required additional information is the underlying diploid heterozygosity and parental-pair reproductive weights. This can help explain variation in realized responses **but the fixture has zero expected selected directional change**. It therefore CANNOT be advertised as an observed failure of favourable natural selection or the cause of the original 128-history branch labels.

The law of total variance and binomial arithmetic are standard mathematics; the contribution here is a **source-compatible decomposition and validation scaffold**, not a newly discovered theorem.

## A second, deliberately selected source case: expected improvement without a guaranteed realized improvement

After a separate small exploratory formula pilot, a **new post-discovery deterministic scenario** was frozen on the same source model (not predeclared independent confirmation): four plants with matching alleles `[0/0, 0/0, 0/1, 0/1]`, all floral investments 0.35 and assurances 0.5, and four visitor optima `[0.45,0.50,0.55,0.60]` at breadth 0.18. It uses the original reproductive-viability ledger with pollen-background K48, and conditions on **no adult survivors, exactly eight retained resident offspring, no immigrants and no mutation**.

This native-source ledger gives original parental adult mean matching phenotype **0.25** and source expected next offspring mean approximately **0.25456**, a signed increase **+0.00456**. Yet the exact per-gamete allele-count polynomial gives **P(realized next matching mean ≤ 0.25 | S=0,R=8) ≈0.60584**. In this particular example both parental-pair sampling and Mendelian segregation have positive conditional variance, with contributions to `Var(next mean)` approximately **0.007809** and **0.007955** respectively. Thus a *positive expected one-step trait response is not the same as guaranteed positive finite realization*. The nonpositive probability is high partly because the expected shift is small compared with finite variance and because equal-or-lower is a discrete event, not because the model has established opposing selection over many generations.

This example is more informative than the phenotype-identity null, but its evidence level is narrower than the Chapter 2 experiments: **one pilot-chosen synthetic genotype/visitor condition, no new independent histories, no occupancy calculation and no unconditional selection-invasion coefficient**. It demonstrates source-consistent nonrealization probability under a declared conditional recruitment count. It does not attribute the original finite ABM history variability to any percentage of genotype segregation, or show that better reproductive performance is eliminated by demographic extinction.

## How this sharpens question 3 and relates to questions 2/4

1. **Already distinguished:** the conditional *expected genetic contribution* of viable offspring is distinct from a realized finite allele/trait shift. At fixed survivor/R conditions, random parental draws and allele segregation are two separable sources of trait variability.
2. **Still unresolved:** the fractions of actual stochastic 80-/1000-update Model 3 response heterogeneity attributable to parentage, segregation, viable seed supply, survivor lottery, immigration and density-vacancy competition. Repeated state-years in #452 are not independent histories, and deterministic-density versus ABM differences cannot automatically be called drift.
3. **Required next discriminating test:** take fully verified *same-source* native genotype states and visitor contexts; predeclare a focal trait with a favourable expected one-step change, then use common source parental ledgers to compute conditional expected response and variance, and compare with untouched realized histories. **Do not use a post-outcome selected sign or retune a decision threshold to declare positive selection.** One-step decomposition itself makes no statement about induced population extinction or survival rescue.
4. **Chapter 1 bridge:** the global self-compatibility association is a present-day island-flora pattern. Differences in hidden segregating genetic variance among lineages can condition future offspring variance without requiring that identical present-day floral appearance identifies past evolutionary causes.

## Reproducibility

Source: \`scripts/audit_chapter2_one_step_realization_moments.py\`, contract: \`data/design/chapter2_conditional_one_step_variance_20261010.json\`, regression: \`tests/test_chapter2_one_step_realization_moments.py\`.

\`\`\`bash
python -m scripts.audit_chapter2_one_step_realization_moments --out /tmp/chapter2-one-step-variance.json
pytest -q tests/test_chapter2_one_step_realization_moments.py
\`\`\`

**Evidence policy:** analytic/source-operator demonstration, conditional on S/R with no synthetic independent histories. Neither a new ecological sampling unit nor proof of heritable adaptation, non-realization in finite source ABM histories, or a missing persistence mechanism.
