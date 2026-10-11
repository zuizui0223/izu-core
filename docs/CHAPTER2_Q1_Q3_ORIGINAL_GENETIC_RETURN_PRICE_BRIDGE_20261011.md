# Chapter 2 Q1→Q3: what does local parental fitness actually predict about inherited change?

**Date 2026-10-11. Status: post-discovery exact mathematical audit of the original synthetic Model 3. No new stochastic ecological histories or prospective confirmation.** The four-question order is **閾値 → 順序 → 実現 → 帰結**.

## Current answer

**The sign of a local marginal investment-fitness derivative by itself does NOT determine the next population's mean inherited investment.** In the original zero-survival, no-immigration, no-mutation source biology, the exact one-generation conditional expectation is governed by the covariance between each *existing parent's genotype* and its **FULL** reproductive genetic return, with both sexes and selfing included.

For diploid parent `i` write `g_i` for its average investment allele. The unchanged original `reproduce_kb` ledger has maternal outcross `F_i = sum_father outcross[father,i]`, paternal outcross `P_i = sum_mother outcross[i,mother]`, and viable selfed offspring `S_i`. Thus

```text
W_i = 0.5 F_i + 0.5 P_i + S_i
mu = sum_i W_i = total expected viable maternal offspring

Pr(father=i,mother=j | offspring retained) =
  [outcross(i,j) + 1(i=j) self_viable(j)] / mu

E[mean inherited investment at next census | N_next>0]
    = sum_i (W_i / mu) * g_i

E[delta gbar | N_next>0]
    = Cov_N(g_i,W_i) / mean_N(W_i).
```

These are **standard Price/quantitative-genetics accounting identities**, not a new biological theorem, selection coefficient or novel evolutionary mechanism. They hold because the retained offspring are sampled from the original parent-pair lottery, each offspring inherits one homolog per parent independently, adults do not survive, immigrants/mutations are absent, and at least one offspring is recruited. Extinct next-generation trait *mean* is missing rather than zero.

**Mathematical distinction from Q1 local beta:** The finite one-individual local mutation-gradient `beta_i=d log W_i/dI_i` is a derivative of focal return under an artificial unilateral phenotypic perturbation. The Price covariance above is evaluated across **existing standing diploid genotypes and their actual source parental returns**. A local negative beta is insufficient to infer the sign of `Cov(g,W)`; conversely, an expected nonzero covariance does not guarantee a particular realized offspring mean in a small population.

## Source validation and coverage

The new original-operator auditor evaluates 8 previously discussed genotype-count source compositions (three genetically homogeneous, five mixed) × four original mating settings × two previously exposed resource budgets (6/8) × three four-visitor functional states (matched, half shifted, shifted) = **192 source operator evaluations**. These are **192 correlated synthetic calculations in ONE model family**, not replicate populations or island archipelago observations.

For each source it checks:

1. Father-row/mother-column pollen ledger, `sum F=sum P`, `sum W=mu`, exact direct expected offspring genotype and Price covariance identity.
2. **Conditional trait mean when N_next>0** and independent **unconditional inherited allele-copy mass**, incorporating the original K8 `min(Poisson(mu),8)` recruitment count. No near-extinction trait means coded as zero.
3. Genetic source populations with no standing genotypic variance have zero expected directional genetic change under these assumptions regardless of functional matching (Mendelian noise may still occur if genetically heterozygous).
4. The original full #462 heterogeneous 8-adult diploid fixture: `E[delta gbar | next occupied] = -0.001406981` in the source matched four visitors/delayed/budget6 case, with model-predicted conditional next genetic mean **SD ≈ 0.04209** at K8. The expected directional signal is much smaller than the finite offspring lottery noise. The new direct F/P/S genetic-return identity is checked against the already merged #462 independent moments computation.

## Interpretation for the four questions

- **Q1 閾値:** identify *where a focal change affects its W* (and where other mothers gain through transferred pollen), while respecting density and functional-trait matching.
- **Q2 順序:** this identity alone says nothing about an assigned expression schedule, spontaneous ordering of genetic changes or #418's practical-equivalence result.
- **Q3 実現:** once a specific finite standing-allele distribution exists, the original full parentage ledger determines the **expected** one-generation genetic response exactly through `Cov(g,W)`, but Mendelian/demographic noise and extinction determine finite realized histories.
- **Q4 帰結:** the identity describes inherited mean change, not a causal effect on total viable seeds or 80-year population survival. Later feedback requires longitudinal matched histories. #461–#469 provide distinct demographic and functional-matching counterfactuals, **not** an identified multi-generation genetic mediator.

This is a useful **inferential firewall**, not the new lead biological discovery. The next high-value independent test must follow *the actual* founder, full F/P/S, genetic parentage, realized alleles, visitor functional composition, recruitment and survival through the **same prospective independent environmental histories**. Reusing the present post-discovery 192 model-source calculations as statistical biological replication would be incorrect.

## Files and original source

- `scripts/audit_chapter2_q1q3_genetic_price_identity_20261011.py`: original `reproduce_kb`, exact father/mother full W, Price covariance, capped Poisson unconditional allele-copy expectation.
- `tests/test_chapter2_q1q3_genetic_price_identity_20261011.py`: all 192 source states, three no-diversity controls, direct F/P/S conservation, original #462 heterogeneous reference and fail-closed inputs.
- Original [#462 Q3 moments](https://github.com/zuizui0223/izu-core/pull/462), [#464 exact genotype recruitment](https://github.com/zuizui0223/izu-core/pull/464), [#468 matched/shifted visitor source](https://github.com/zuizui0223/izu-core/pull/468), and [#411 prospective primary](https://github.com/zuizui0223/izu-core/pull/411).
- No original biology, established #411/#442 inference rank, manuscript wording or ecological survey is modified.
