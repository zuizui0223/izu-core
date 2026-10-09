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
