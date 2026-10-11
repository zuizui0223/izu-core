# Model3 K32: expected allele change as self, father and mother marginals

## Question

The source-locked K32 full factorial showed that the three encoded loci respond differently to the same set of donor/routing/maternal weight interventions: matching high alleles persist more often, investment high alleles disappear more often, and assurance high alleles approach fixation. This follow-up asks which reproductive-parent allele marginals make the exact next-generation frequency move.

## Exact source reproductive identity

Let W_ij be the viable seed-weight matrix with original father rows and mother columns, as returned by unchanged canonical reproduce(). Off-diagonal elements are outcross and diagonal elements are viable self seeds. For a living population of n individual parents, let b_il ∈ {0, 0.5, 1} be individual i's high-allele diploid dosage at locus l, p_l = mean_i(b_il), T = sum(W), s_i = self seed intensity, r_i = outcross row sums and c_j = outcross column sums.

The exact Mendelian offspring high-allele expectation is

    q_l = [sum_i (r_i+s_i)*b_il + sum_j (c_j+s_j)*b_jl] / (2*T).

Writing S=sum(s)/T, O=sum(outcross)/T gives

    q_l - p_l =
        [sum_i s_i*b_il/T - S*p_l]             SELF
      + [sum_i r_i*b_il/(2*T) - O*p_l/2]       OUTCROSS FATHER
      + [sum_j c_j*b_jl/(2*T) - O*p_l/2]       OUTCROSS MOTHER.

This is an exact *reproductive accounting* of each locus's expected allele direction under the original viable-seed distribution. It is neither Gaussian approximation nor a causal partition of pollinator selection. A change to mating-pair associations that keeps both father and mother allele-weighted marginals fixed cannot change the next-generation mean allele frequency, although it can change the offspring multilocus genotype distribution and later genotype-mediated selection.

## Seven same-parent counterfactual masks

Evaluate all seven declared donor export, visitor routing and maternal provisioning masks at EXACTLY the same source parental genotype-count state in each year. Every mask preserves the source's selfed viable-seed weights, total outcross seed intensity and original support of mating edges at that parental state. Thus the SELF term cancels exactly from each source-to-control one-step allele-direction contrast; every difference is the sum of outcross father and mother contributions.

This is NOT an autonomous eight-year comparison. The original source-only genotype-count Markov chain advances all source parent states each year; altered masks never advance an independently altered genotype state in this study. Previous autonomous eight-year intervention results measure a different quantity and need not have the same sign or magnitude.

## Source and evidence limitations

K=32, mutation 0, adult survival 0, immigration 0, complete 27-class, three-locus diploid genotypes, engineered four-founder initial state and canonical Chapter2 prior_selfing reproduction. The only ecological environment is old archived near visitor history 26110601, eight years, with 512 nested demographic paths per resource budget (8 and 3). Original Model3 genetic and reproductive source code is untouched. Frozen prospective confirmatory visitor histories, natural plant genotyping, geographic INLA, full Ito SDE/SPDE validation, and independent island history inference are excluded.

The father/mother and self quantities depend on source-genotype-dependent mating weights, not independently manipulated field mechanisms. Correlations with other loci or prior state can induce an allele shift, and no independent causal selection coefficient is identified by this identity alone.

## Reproduction

    pytest -q tests/test_model3_k32_parental_marginal_direction.py
    python -m scripts.audit_model3_k32_parental_marginal_direction --budget 8 --draws 512 --out parent-marginals-budget8.json
    python -m scripts.audit_model3_k32_parental_marginal_direction --budget 3 --draws 512 --out parent-marginals-budget3.json

The existing core CI includes a PR420-only model3-k32-parental-marginals job testing these exact identities. Do not promote numerical claims until source-matched CI and its archived results succeed.


## Validated source-run parental marginal results

Source SHA `37bc04a64e1dc2070dc47fbba93ca3d33d2301d4`
successfully passed dedicated `model3-k32-parental-marginals`
in [GitHub Actions 37903183921](https://github.com/zuizui0223/izu-core/actions/runs/37903183921).
Raw [budget8 and budget3 archive 11603825393](https://github.com/zuizui0223/izu-core/actions/runs/37903183921/artifacts/11603825393)
has SHA256 `58248a8b91d9b9eca3c13af225139eb0412ca7bedf42bca2982a85aaad1e35ac`.
Compact source-lock:
`data/results/model3_k32_parental_marginal_direction_20261009.json`.
Mass, all-three-locus Mendelian offspring means, eight intervention
masks and father + mother + self identities passed on a frozen
original Model3 source, K32, 0 mutation, same 8-year OLD visitor
history 26110601/near, nested 512 source demographic trajectories.

### Exact same-original-parent contrasts, at year eight

For each locus, this is the mean *change in the expected next
high-allele frequency shift* under the all-three equalized
outcross-mating operator minus canonical Model3, with parent
genotypes, original viable-self seed weights and total outcross
seed mass HELD IDENTICAL at each source state.

| Locus | Budget8 difference | Budget3 difference |
|---|---:|---:|
| Matching high allele | **+0.004151 ±0.000225 MC SE** | **+0.002467 ±0.000183** |
| Investment high allele | **−0.008229 ±0.000304** | **−0.004955 ±0.000251** |
| Assurance high allele | **+0.002541 ±0.000211** | **+0.001308 ±0.000148** |

At budget8, the matching contrast comprises +0.000856
father-outcross and **+0.003295 mother-outcross**;
the maternal term is about 79% of this contrast.
The investment contrast comprises −0.004069 father and
−0.004160 mother, approximately equally.
The assurance contrast comprises +0.000332 father and
+0.002209 mother. Source minus control self contributions
are EXACTLY zero by the declared comparison construction.

At budget3, matching's +0.002467 consists of +0.000544
father and +0.001923 mother; investment −0.004955
consists of −0.002471 father and −0.002485 mother; assurance
+0.001308 consists of +0.000152 father and +0.001156 mother.

The source-only expected direction at year8 is
`[+0.005533,-0.024501,+0.013156]` for budget8,
and `[+0.006607,-0.023128,+0.011766]`
for budget3 (matching, investment, assurance order).
Importantly, these are **one-step reproductive gradients at the
evolved parental state**, not the historical cumulative change
from original founder frequencies.

### Source matching high-allele direction reverses during eight years

The original Model3 expected next-generation matching high-allele
direction starts at **−0.062815** in the initial year, and
becomes **+0.006582** at year7 and **+0.005533** at year8
under budget8. Under resource budget3 it becomes positive
by year5 (+0.000204), rising to +0.006607 at year8.

At budget8, source selfed-seed contribution to the matching
allele direction changes from **−0.03489 (year1)**
to **+0.01198 (year8)**, whereas outcross father and
mother contributions remain negative even at year8,
approximately −0.00323 and −0.00322.
At budget3 the self contribution moves from −0.03489
(year1) to +0.01033 (year8), while father and mother
remain around −0.00186 each at year8.

This strongly qualifies any summary claiming the matching
allele is monotonically disfavored: its instantaneous
source reproductive direction depends on **parental
genotype state and year-specific visitor history**.
A positive late direction need not imply that cumulative
matching-high frequency returned to its initial level,
because early negative shifts may have already removed
alleles from some demographic trajectories.

**The sign reversal is not yet causally attributed to changes
in pollinator ecology versus changed genotype state.**
The old visitor sequence and current genotype distributions
both differ across years. Isolating these explanations would
require a separate crossed state-by-visitor counterfactual
in which either the source state or visitor condition is
held fixed, without new prospective histories. This is an
identified NEXT QUESTION, not a claimed result.

### Scope and interpretability

One source ecological visitor history, no independently
observed islands or field reproduction, no confirmed
population-genetic selection coefficient or validated
continuous-time SDE/SPDE. The seven controls intentionally
change viable-outcross mating weights; the original source
biological files are untouched. Father and mother
marginals are exact successful-parent gene-transmission
accounting, **not** independent physiological pollen
or maternal-fecundity effects. The earlier full factorial
autonomous eight-year allelic-diversity responses remain
different estimands from these one-step same-parent
expected allele changes.
