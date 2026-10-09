# PR #420: Selfing and pollen-mediated outcross contributions to genetic noise

## Status, question and source firewall

The previous exact same-parent experiment showed that **at identical
parent genotype state, mean offspring allele frequency and capped-Poisson
recruitment**, canonical Model3 yields fewer offspring heterozygotes
than a uniform-gamete mean-matched comparator, hence greater
conditional one-generation allele-frequency variance.

This study resolves the next narrower question: How much of that
offspring-heterozygosity contrast is algebraically associated with
(a) self-versus-outcross mixture fractions,
(b) genotype-specific contributions *within selfing*, and
(c) pollen-mediated parent-pair weights *within outcross*?

All calculations start from **unaltered canonical reproduce() ledger**,
whose `self_viable` terms refer to identical individual father/mother,
and whose `outcross` matrix uses donor rows and recipient columns with
zero diagonal. Original mating, pollen delivery, maternal resources,
inbreeding depression, sex-specific gamete segregation and capped-Poisson
offspring recruitment stay unchanged in the source.

K=32, mutation=0, survival=0, immigration=0, 8 generations,
prior_selfing, old visitor history **26110601 / near**. Four engineered
source genotypes expanded to 32 adults, full joint 27-class diploid
genetic support; reproductive budgets 8 and 3. No prospective frozen
confirmatory visitor histories, real island observation or independent
ecological history. The 512 demographic source draws are nested within
a single fixed visitor environment.

## Exact pair-mixture decomposition

The original source ledger weights are (w_{ij}) for outcross father
i and mother j, i≠j, plus `self_viable` on the diagonal. Let s be
the source fraction of all **viable expected seeds** with self parents.
For allele dosage (b in {0,1/2,1}) in one offspring:

[
H_{m source} = s H_{m self,source}
                 +(1-s)H_{m out,source}.
]

The artificial comparator first draws two uniformly weighted gametes
from the same parental individual set **with replacement** (including
same-parent pairs), retains exact Mendelian genotype support, and tilts
offspring genotypes by (exp(	heta b)) to match original source
(E[b]) for that exact parental genotype state. It retains the
source capped-Poisson recruitment intensity. Crucially, reweighting
changes the comparator's *effective* self-parent mixing fraction (s_0).
The normalized self and outcross strata of the tilted comparator have
heterozygosities (H_{m self,0}, H_{m out,0}).

The exact **three-component telescoping identity** is:

[
egin{aligned}
H_{m source}-H_0
= &(s-s_0)(H_{m self,0}-H_{m out,0})\\
 &+s(H_{m self,source}-H_{m self,0})\\
 &+(1-s)(H_{m out,source}-H_{m out,0}).
end{aligned}
]

The three terms are:
1. **Self-vs-outcross composition contrast** relative to the declared
   reweighted comparator, not a causal selfing intervention.
2. **Within-self parent contribution contrast** (source assurance
   intensity and maternal genotype allocation; *not* only selfing rate).
3. **Within-outcross pollen/mating contribution contrast**, including
   visitor preferences, donor export, recipient allocation, and maternal
   seed provisioning; not individually causally resolved.

Because both total offspring distributions have the same assurance
mean and the same census law conditional on surviving N>0,

[
Delta mathrm{Var}(ar b mid C,N>0)
 = - 	frac14 left(H_{m source}-H_0ight)
 mathrm E[1/Nmid C,N>0].
]

Thus multiplying every component above by
(-rac14mathrm E[1/Nmid C,N>0]) gives exactly additive
contributions to the matched-mean one-generation **genetic variance
contrast**. No unobserved parameter or approximate Gaussian closure is
needed.

When no outcross mating is possible (a single adult or zero delivered
pollen), the outcross term is multiplied by zero and does not invent
nonexistent offspring. Complete allele fixation is handled by the
support-limited exact endpoint of the tilt; genetic classes absent
in the source parent are never invented.

## Why it does NOT identify a unique causal mechanism

The decomposition is **relative to the chosen artificial comparator
and algebraic ordering**. It is valid for the given source rule,
not a unique decomposition of the effects of self-fertilization,
pollinator identity or adaptation. Within-outcross effects bundle
mating pairs and different mother/father marginals. A subsequent
causal ablation would need clearly defined, separate biological
operators and matched demographic feedback, reported as different
biology.

It also does **not** explain the eight-generation terminal
between-population variance or prove adaptive stabilizing selection,
which earlier demographic train/holdout reversal did not robustly
identify. No plant field observations, new visitor histories, SDE/SPDE
numerical validity or geographic INLA analysis.

## Reproduction

```bash
pytest -q tests/test_model3_k32_self_outcross_mechanism.py
python -m scripts.audit_model3_k32_self_outcross_mechanism --budget 8 --draws 512 --out self-outcross-budget8.json
python -m scripts.audit_model3_k32_self_outcross_mechanism --budget 3 --draws 512 --out self-outcross-budget3.json
```

The existing CI has a PR420-only job
`model3-k32-self-outcross`, which validates the source/history
guards, three-term exact identity, and archives both raw JSON outputs.
**Do not infer actual numeric component magnitudes before successful
source-linked CI and raw artifact inspection.**


## Source-run eight-generation results

The dedicated self-outcross analysis and mathematical regression tests
**PASSED** in
[GitHub Actions run 37890587796](https://github.com/zuizui0223/izu-core/actions/runs/37890587796),
job `model3-k32-self-outcross`, at source SHA
`920f111dd79402ef497cdb5751f6469d458ef404`.
The [full executed two-case JSON artifact](https://github.com/zuizui0223/izu-core/actions/runs/37890587796/artifacts/11598138261)
has SHA256
`11174966941835982b9ade745ab263cc19266132903bb000d2996a4b9729e8f8`.
The compact committed source-lock is
`data/results/model3_k32_self_outcross_20261009.json`.

### Year-8 parent states, exact conditional contrast

| Mean statistic | Budget 8 | Budget 3 |
|---|---:|---:|
| Usable source parent states | 512 | 509 |
| Original source viable-selfed-seed share | 0.938361 | 0.957483 |
| Matched artificial comparator self-pair share | 0.031410 | 0.075905 |
| Self-versus-outcross composition term, delta variance | **+0.000207058** | **+0.000228765** |
| Within-self parent weighting term | +0.000001631 | +0.000000796 |
| Within-outcross pollen/mating weights term | **−0.000043738** | **−0.000032410** |
| Sum: source minus comparator next-frequency variance | **+0.000164951** | **+0.000197151** |
| Max absolute reconstruction error | 5.94e-17 | 6.16e-17 |

The self/outcross fraction term is LARGER than the final positive
contrast: the negative within-outcross term partially offsets it.
Numerical identity is exact to floating precision; state means and
rates are ensemble averages of 512 source-demographic paths nested
under the SAME fixed visitor history.

The source viable selfing fraction rises from 0.7861 in generation 1
to 0.9384 by generation 8 at budget 8, or 0.9575 at budget 3.
The matched-mean null's self-pair proportions also vary with the
offspring dosage tilt; they are **not** a natural biological selfing
frequency prediction.

### Interpretation

Within the chosen reference, the high source fraction of selfed
viable seeds is mathematically the leading *composition* difference
associated with greater next-generation allele-frequency noise and
lower offspring heterozygosity. The negative within-outcross
component shows that pollen-mediated weighting may partially
counterbalance the source self-mating contrast.

**Do not substitute the word "causal" for "algebraic".** The source
selfing share, viable seed intensity, maternal fecundity, visitor
affinity and paternal export all depend on parental genetic
assurance/investment and visitor history. The comparator's self rate
also changes because it is retrospectively reweighted to the exact
source allele mean. One cannot attribute a 94%-96% difference or
the +0.000207 / +0.000229 terms to a biological intervention on
selfing alone, without new controlled payoff ablations.

This is a stricter mechanism accounting within the original genetic
operator, **not** evidence that the source's small between-population
eight-year endpoint variance is adaptive stabilization. The earlier
cross-fitted endpoint variance gap reversed sign when the
demographic halves were swapped, and this one-step calculation does
not repair that identification failure.

No source biological files, frozen visitor confirmatory histories,
natural island data, environmental geography, or full SDE/SPDE
approximations were modified or newly evaluated.
