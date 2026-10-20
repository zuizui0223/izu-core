# A source-mean phenotype intervention that preserves within-population A variability

**2026-10-20 — technical counterfactual specification, not original scientific registration, new evolutionary genetic estimate, ecological validation or independent confirmation.**

## Why one more policy is needed

In the original [third-source postestablishment technical readout](CHAPTER2_TWO_ORIGINS_POSTESTABLISHMENT_POLICY_READOUT_20261020.md), allowing native A expression and forcing **every descendant** to express the *source population mean* A yielded identical aggregate survival counts in all four synthetic B×visitor environments over six updates. However, the source-mean flat clamp removes **standing heterogeneity among individuals in A expression** as soon as it is applied. The contrast is NOT only the effect of blocking subsequent genetic mean evolution. The original diploid A genotype still segregates in both policies.

The original technical source cohort (24 third-namespace seed genotypes, four artificial environments and eight nested stochastic resets) must be reused **only as a paired sensitivity**, not passed off as a fourth independent experiment or a natural insular lineage sample.

## Matched optional new intervention

Add the optional policy `center_A_mean` to the original first-establishment source fork in [`scripts/chapter2_two_origins_technical_20261019.py`](../scripts/chapter2_two_origins_technical_20261019.py). Leave the four historical default policies and their source/arrival RNG namespace unchanged.

In every descendant reproductive update, calculate from the **true inherited, unmodified** diploid A alleles `a_{i1},a_{i2}` the current allele mean `m_t`, and let `m_0` be the original source population's mean A. For reproduction **only**, feed the native maternal/paternal/self ledger:

`a_{ik}^{expressed}(t) = a_{ik}^{inherited}(t) + (m_0 - m_t), k=1,2.`

The intervention has three exact technical properties **when all shifted alleles remain in [0,1]**:

1. `mean_{i,k} a_{ik}^{expressed}(t) = m_0` — the population **mean expressed** A does not evolve;
2. `a_{ik}^{expressed}(t) - mean_{i,k} a_{ik}^{expressed}(t) = a_{ik}^{inherited}(t) - m_t` — the **whole current allelic spread and individual rankings** are preserved during reproduction;
3. The next generation inherits from the **unmodified original parent state**, not the shifted expression array. This is a controlled reproductive expression policy, not an allele-frequency freeze or direct manipulation of Mendelian inheritance.

If any shifted allele would fall outside [0,1], the experimental intervention **raises ValueError rather than clipping**, and the affected path cannot be quietly excluded from a scientific outcome denominator. An unbounded long-horizon study would require a prospective domain-safe intervention rather than hiding failures.

All five postestablishment arms (**native**, **clamp_A** flat, **clamp_I**, **clamp_A_I**, **center_A_mean**) share original source genotypes and first establishment, original all-candidate stage denominator and the same master RNG source; RNG event-by-event trajectories may diverge with the intervention.

## Evidence standard and expected interpretation

The updated technical source cohort comprises **24 artificial source genotypes ×4 artificial B×visitor conditions ×8 demographic/arrival resets =768 candidate source×environment×reset assignments**, forked into **5 expression policies =3,840 arm paths**. This is NOT 3,840 independent islands, not a new scientific confirmation and not independently sampled new source genotypes.

Report **paired** fate counts against native (both survive, native only, comparator only, neither) along with original all-start survival counts per island, before discussing averages. If the centered control differs from native but the flat clamp does not, flat-clamp heterogeneity suppression was masking an effect. If both coincide in a six-update fixture, that establishes **only a short technical model comparison**; it does not imply no future A evolution effects in the original 80-update Model3 or in natural island colonization.

A mutation/immigration-enabled and truly allele-frequency-fixed alternative would be a different biological experiment and **is not implemented**. The current `center_A_mean` policy can permit allele-frequency change, within-group variance change due drift, individual heterozygosity and lineage selection, while holding the *expressed population mean* constant. Consequently native−center_A_mean is not a natural direct/indirect decomposition of "imported A" versus "post-settlement evolved A."

All results remain separate from the ongoing source-registered Chapter 2 [paper PR #609](https://github.com/zuizui0223/izu-core/pull/609).

## Engineering admission test

Run `pytest -q -s tests/test_chapter2_two_origins_postestablishment_probe_20261019.py` in the existing Chapter 2 gate. The explicit unit test `test_center_A_mean_preserves_allele_and_individual_deviations` verifies mean centering, exact preservation of deviations, unmodified inheritance genotype, no alterations to M/I and fail-closed boundary behavior. The paired fate table must be source-admitted from the first successful postchange CI run before being reported as empirical results.
