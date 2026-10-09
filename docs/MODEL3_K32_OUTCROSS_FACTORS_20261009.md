# PR #420: Exactly factor the canonical outcross weights (export / visitor routing / maternal seeds)

## Motivation and fixed evidence scope

The source-locked K32 conditional decomposition found that differences in
viable selfing/outcross **mixture** account algebraically for much of the
matched-mean child heterozygosity contrast, with a negative
**within-outcross** component partly offsetting it. The next question is
whether the latter comes primarily from donor pollen export, visitor
routing among donor/recipient plants, or maternal recruitment/allocation.

The ONLY biological source is frozen scripts/model3_island/reproduction.py
and its full 3-locus Mendelian child law. Source conditions: K=32, mutation
0, adult survival 0, seed immigration 0, eight generations, Chapter 2
prior_selfing, artificial four-founder/27-genotype support and ONE old
archived visitor history 26110601 ("near"). The 512 demographic paths
per budget (ovule budgets 8 and 3) are NOT 512 independent environments
or observed plants. None of the frozen prospective confirmatory visitor
histories are accessed.

## Exact original-pair factorization

The canonical Ledger fields specify outcross donor row i, maternal
recipient column j. Denote:

- \`e_i = ledger.exported[i]\`: **donor exported pollen**. Importantly
  this source variable includes donor investment/assurance and
  donor-to-visitor affinity already; it is NOT a pure pollen-production
  parameter manipulated independently.
- \`T_ij = ledger.delivered[i,j]\`: visitor-mediated pollen delivery
  (diagonal zero). Define \`R_ij=T_ij/e_i\` if \`e_i>0\`, zero otherwise.
  This is a **visitor routing/receipt factor**, including both donor
  channel preferences, visitor effectiveness, recipient affinity, and
  source competition/background normalization.
- \`F_j = ledger.maternal[j] - ledger.self_viable[j]\` is expected
  outcross viable seeds of mother j. \`r_j=sum_i T_ij\`.
  Define \`M_j=F_j/r_j\` if \`r_j>0\`, zero otherwise.
  This is **maternal seed production per received pollen**, including
  ovule resources, assurance preemption, and non-linear pollen
  saturation, NOT independent maternal fecundity alone.

For i != j:

\`\`\`text
ledger.outcross[i,j] = e_i * R_ij * M_j.
\`\`\`

All zero support and diagonal restrictions are retained. Every
intermediate weight matrix is normalized ONLY as a mathematical
condition on outcross offspring. Original reproduce() is never
edited or replaced.

## A four-term, order-robust contrast

The previous mean-matched full-parent-pair neutral control applied
an artificial **offspring assurance-dosage tilt**. Thus its conditional
outcross heterozygosity H_null,out is NOT the same as the uniform
unweighted outcross-parent baseline H_uniform. To avoid assigning
this artificial reweighting to any biological mechanism, explicitly
report the separate contrast:

\`\`\`text
H_uniform - H_null,out  [null genotype-tilt reference term].
\`\`\`

For the source three factors e_i, R_ij, M_j, evaluate the exact
Mendelian heterozygote probability in all 2^3 parent-matrix
configurations, starting from uniform off-diagonal parent pairing.
The three Shapley values each average over all six introduction orders:

\`\`\`text
phi_k = sum_{S subset of {E,R,M}\{k}}
     |S|! * (2-|S|)! / 3! * [H(S union {k}) - H(S)].
\`\`\`

The resulting identity is exact:

\`\`\`text
H_source,out - H_null,out
 = (H_uniform - H_null,out)
   + phi_export + phi_routing + phi_maternal.
\`\`\`

Multiply each term by
\`-(1-s_source) * E[1/N|N>0,C]/4\` (where s_source is the
canonical viable selfing-seed share). Their sum MUST equal the
**within-outcross mating-weighting** conditional next-frequency
variance component previously calculated from the canonical ledger.

The Shapley average makes the allocation *invariant to one arbitrary
factor order*, but does not make it a unique causal decomposition.
Different null mating matrices or definitions of exported and routed
pollen would yield different components.

## Interpretation boundaries

Even if the "routing" component is large, it is an internal
source-model factorization, **not** a causal estimate of species-specific
pollinator preference: the route mixes donor flower traits,
visitor channels/effectiveness, recipient affinities, competition,
and the abundance of potential recipient plants. Likewise, M_j
includes source mate availability and ovule-related nonlinearity.
None is randomized. The result does not establish biological
adaptation, fixation stabilization, evolutionary memory, field
evidence, continuous Ito SDE or SPDE.

This comparison is only at IDENTICAL original parent states and uses
the same source capped Poisson next-census law; it is not an
autonomous eight-year intervention or ecosystem prediction.

## Execution

\`\`\`bash
pytest -q tests/test_model3_k32_outcross_factors.py
python -m scripts.audit_model3_k32_outcross_factors --budget 8 --draws 512 --out outcross-factors-budget8.json
python -m scripts.audit_model3_k32_outcross_factors --budget 3 --draws 512 --out outcross-factors-budget3.json
\`\`\`

PR420-only job \`model3-k32-outcross-factors\` in existing
\`.github/workflows/ci.yml\` tests this identity, old history
firewall and the two case results. Do not claim numerical
component outcomes until the source-head job succeeds and its
raw artifact is inspected.
