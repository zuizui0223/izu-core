# R2 follow-up: convergent A endpoints do not imply convergent floral investment I

**2026-10-23 — retrospective direct readback of the ORIGINAL 384 Model 3 exploratory trajectories; no new biological simulation, registration or hypothesis test.** This supplements the exact matched-pair cofixation audit in PR #630. The original frozen R1–R5 registered endpoints and the fresh-founder R2 **overall INCONCLUSIVE** result are unchanged.

## Biological question and source

The archived 384 paths used the same 12 independent founder sources, four nested demographic repeats, two prior pollen-effectiveness settings, two initial-A levels, and matched control/90%-visitor-activity-decline futures after 30 common updates. The original [Actions source ZIP](https://github.com/zuizui0223/izu-core/actions/runs/39233450099) is SHA256 **10bb8bdd52b53b32429e350c2f392ed2aeaa791683ede1d563ae6627c5ecb35e**, original source commit **eb785dc6865ca1842ec9d6c7d511778c74e03478**. The direct A-cofixation audit confirmed **103/192** matched futures with exactly zero terminal A treatment contrast, *all* of which have equal numerically fixed A allele values.

A remaining ecological question is whether populations with a converged assurance trait also necessarily retain the **same investment trait, I**, after contemporary pollination differs. This matters because the island-floral simplification hypothesis contains **at least two** dimensions that need not share the same selection constraint or inherited endpoint.

## Source-exact A versus I contrast

For each of the 192 original source pairs, we compute `dA=A80_decline−A80_control` and independently `dI=I80_decline−I80_control`, including diploid I allele-value counts and A fixation stage. All 384 survive. Zero is **exact numerical equality**, not a threshold for biological importance.

| Starting A | Pollen prehistory | Pairs with exactly dA=0 | Of those, dI negative | dI zero | dI positive | Mean dI, conditional on dA=0 |
|---:|---|---:|---:|---:|---:|---:|
| 0.3 | Strong limitation | 45 | **23** | 19 | 3 | **−0.069734** |
| 0.3 | Weak limitation | 8 | 2 | 0 | **6** | **+0.037109** |
| 0.5 | Strong limitation | 42 | **14** | 27 | 1 | **−0.033420** |
| 0.5 | Weak limitation | 8 | 1 | 3 | **4** | **+0.017904** |
| **All** | | **103** | **40** | **49** | **14** | — |

Thus **54/103 A-converged pairs have nonzero investment I treatment contrasts**, with **different I allele-value support** in every one of those 54 source pairs. This includes **36 of the 69** A-zero pairs that *still had segregating A at the imposed activity decline*, so the observation is not restricted to sources already A-fixed at the shock.

For historically strong limitation, **41 of 87** dA-zero pairs have nonzero I, mostly negative (**37 negative, 4 positive**). For historically weak limitation, **13 of 16** dA-zero pairs have nonzero I, mostly positive (**10 positive, 3 negative**). These are **observed conditional signs** and are not a prospective sampling contrast or a selective causal decomposition.

This is a **trait-specific finite-source endpoint pattern**, not proof that I evolved without any influence of A or that the A and I loci are mechanistically independent. The pairs can have different **intermediate A histories**, matching traits M, population genetic covariance and offspring sampling even when terminal A is the same. Conditioning on terminal dA=0 is post-treatment conditioning and can itself select particular histories.

## Strict no-A/no-M-evolution negative control within the same paired futures

We additionally inspected the **source state at the moment of imposed pollinator decline (census 30)**, not just terminal A equality. Of 192 paired source futures, **34** already had A fixed at that point (strong-limit A0=.3: 22; weak-limit A0=.3: 1; strong-limit A0=.5: 10; weak-limit A0=.5: 1). The native 384 design has **zero mutation and no immigration**, so these sources retain a constant numerical A allele/phenotype during *both* subsequent futures.

**18 of those 34 already-A-fixed pairs still developed nonzero I treatment differences**, all from sources with I segregating at census 30. Of those 18, **14 pairs also had numerically fixed matching trait M at census 30**, while I remained polymorphic. Both A and M therefore stayed numerically invariant during their paired 50-update futures; yet the I endpoints diverged.

| Initial A | Prior pollen limitation | A fixed before shock /48 | Of these, I differs at t80 | Strict subset: A and M fixed but I segregating at t30, I differs at t80 | Strict I sign |
|---:|---|---:|---:|---:|---|
| 0.3 | Strong | 22 | **12** | **10** | 10 negative |
| 0.3 | Weak | 1 | **1** | **1** | 1 negative |
| 0.5 | Strong | 10 | **4** | **2** | 2 negative |
| 0.5 | Weak | 1 | **1** | **1** | 1 positive |
| **Total** | | **34** | **18** | **14** | **13 negative, 1 positive** |

The 14 strict pairs come from **9 of the original 12 founder IDs**, with demographic repeats still nested within founders. The distinction establishes **existence**, under one frozen native model, of a florally differentiated response when the *expressed A and M traits cannot evolve during the shock period*. It is a stronger structural negative control for necessity than conditioning only on identical terminal A. It is **not** 14 independent evolutionary replications, nor a measurement of a general selective coefficient. Within-pair future stochastic streams are shared initially but realized offspring can diverge after treatment changes reproduction; whether the I contrast arises from selective sorting versus finite demographic/genetic randomness remains unresolved. The result complements, without upgrading, the separate original R1 four-setting fixed-A non-necessity result.

This is a **retrospective source-stratified analysis**: selecting sources with shock-time fixation is conditioning on genetic states produced during the earlier 30 updates, and the 14 pairs were chosen after observing I endpoints. Neither proportion should be described as a prospective ecological treatment effect or a general law for natural islands.

## Second original-source discriminator: A nonzero does not mostly mean alternative fixed A alleles

The other **89/192** source pairs have nonzero final A treatment contrasts. Their *direct endpoint A genetic-support states* divide as follows:

| A endpoint classification | Original source pairs |
|---|---:|
| Both future arms still A-polymorphic | **44** |
| One arm A-fixed, the other still polymorphic | **44** (24 control-fixed; 20 decline-fixed) |
| Both A-fixed but to **different numerical A allele values** | **1** |
| **Total nonzero dA** | **89** |

Consequently, the nonzero A contrasts in this finite 80-update source primarily accompany **ongoing A segregation and unequal completion of fixation**, rather than contrasting completed monomorphic A endpoints. The eventual evolutionary fate after the observation horizon cannot be inferred and may differ once new mutation, demographic and mating rules are allowed.

Together, the two comparisons refine the R2 reading: *the same fixed A trait value can accompany different finite I endpoints, while most nonzero A treatment differences have not reached alternative fixed endpoints*. Neither finding resolves whether the causes are changing source genetic access, pollen service, mate competition, finite drift, or another source-specific pathway.

## Inference boundaries

This **does not promote** a new natural-island law, an independent biological replication, a source-state-matched mediation result, a new model class, a prospective R2 success, or any fresh p-values. Repeated futures are nested in **12** founders and shared source settings; groups partitioned by terminal dA=0 are *selected after outcomes*. Identical A allele values are not identity by descent, and different I allele-value support does not isolate a specific genetic or ecological mechanism.

The existing source-bound static maternal and parental-inheritance gradients tell which local direction can have an immediate positive return in fixed synthetic reporter states, **not** which gradient caused these 192 evolving trajectories. A discriminatory follow-up requires new independent crossed sources and full diploid state/pollen-specific matching, not just equal total pollen export or global activity.

## Reproduce and preserve source

- Original exact A-pair admission: `scripts/audit_chapter2_r2_original_384_pair_convergence_20261023.py`
- This direct A/I source reader: `scripts/audit_chapter2_r2_cross_locus_outcomes_20261023.py`
- Compact frozen receipt: `docs/audits/CHAPTER2_R2_CROSS_LOCUS_ORIGINAL_384_20261023.json`
- Regression and negative controls: `tests/test_chapter2_r2_cross_locus_outcomes_20261023.py`

```bash
python -m scripts.audit_chapter2_r2_cross_locus_outcomes_20261023 \
  --zip /path/to/original-GitHub-Actions-baseline-pollen-384.zip
CHAPTER2_R2_384_ORIGINAL_ZIP=/path/to/original-GitHub-Actions-baseline-pollen-384.zip \
  python -m pytest -q tests/test_chapter2_r2_cross_locus_outcomes_20261023.py
```

The original 1.86MB Actions ZIP is deliberately **not** recommitted to this repository. The ZIP reader inherits complete original source ZIP, internal manifest, protocol, 192 pairing and A-cofixation guards. Default CI tests the machine-readable receipt against the preceding source-bound A audit plus synthetic negative controls. End-to-end binary source replay is explicitly optional unless the authenticated original ZIP is provided.
