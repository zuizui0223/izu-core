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
