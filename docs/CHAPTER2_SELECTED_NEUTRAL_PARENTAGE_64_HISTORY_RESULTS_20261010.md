# Selected versus genotype-neutral Mendelian transmission: source-locked 64-history experiment

**2026-10-10. Model-internal mechanism experiment. The completed study is NOT a genotype-frozen vs fully evolving experiment, nor an empirical island extinction result.**

## Scientific purpose

The larger research question is whether individual reproductive advantage, decomposed into maternal outcross F, paternal outcross P and viable self S, coincides with population-level benefit and persistence. Previous #452 work found **14/384 local finite beta-negative / group viable-seed Gamma-positive** synthetic cells, and an independent matching analytic K48 rare-mutant sign in 6/6 such K48 cells, but failed to resolve the unconditional 80-update persistence gradient under small group-expression shifts. The t20 investment-mean-expression feedback knockout also failed to resolve a long-run difference in its separate 64-history cohort.

**This experiment tests a more direct, but different and narrower, part of the genetic pathway**: conditional on the exact realized number of viable selfed and outcrossed recruits, does allowing parental reproductive success to determine inheritance improve the chance that the population remains occupied 80 updates later?

## What the source actually does

Both arms:
- Start at **exactly the same eight source individuals with standing joint three-locus diploid allele variation**, B fixed at 48, carrying capacity K=8 or 48 (starting census N0=8 in both).
- Use exactly the same four visitor phenotypes at year0, then 80 years of shared stochastic visitor arrivals/loss in the same original Model3 source generator.
- Use `reproduce_kb` and the ORIGINAL `population.advance` unchanged for potential seed production, population-size survival (none), Poisson recruitment, source self versus outcross offspring counts, and three-locus Mendelian inheritance.
- Hold mutation=0, seed immigration=0, adult survival=0 and fixed inbreeding depression. Four factorial settings = two ovule budgets (6,8) × two postzygotic seed-survival gates (baseline and 50% viable-self).
- Keep the original `visitor_history` and root demographic random streams paired across selected and counterfactual arms.

`selected_source`: keep the source-selected Mendelian offspring genome, including biased maternal/paternal genotype-parent choices.

`neutral_within_mating_channel`: after ORIGINAL `advance` sets the realized count of recruits and the EXACT realized numbers of viable selfed/outcrossed recruited offspring, discard the newly produced offspring's genotype values only; replace them with independent Mendelian offspring from **uniformly sampled whole-individual parents**, conditional on the same realized mating mode. Selfed children have one uniformly sampled parent twice; outcross children have an ordered pair of distinct, uniformly sampled parents. Their allele-origin genealogy and diploid heterozygosity are then inherited from those new neutral source parents using the same canonical `inherit` operator, and the original recruited offspring IDs and birth years are required to remain identical.

Thus the comparison uses **exactly the same immediate source viable seed intensity and mating-channel realization conditional on an identical state**, but their genetic states and therefore later fecundity, mating-channel mixture and census can diverge. This neutral inheritance operator is **not** a biologically physical recalculation of maternal ovule ownership, and it is NOT a freeze of allele frequencies, genetic drift or natural evolution as a whole. It specifically removes the *within-channel genotype-dependent parent selection component*. Under any nonempty parental genotype state, uniform route-conditioned parent sampling has both maternal and paternal expected genotype marginals equal to the source parent mean. Consequently, without mutation,

```text
E[mean three-locus offspring allele dosage | parents, N>0,
  realized n_self, n_outcross, neutral operator]
= parental mean three-locus allele dosage.
```

Source test gates verify exact self-vs-outcross counts, every-locus conditional neutral expectation, canonical child namespaces/census, genotype standing variation and exact demographic occupancy parity for fully monomorphic negative-control source populations.

## Design lock, sources and reproducibility

- All choices of visitor seeds, founder genotype seed, simulation budget, K/B, parental operator, inference unit and significance bounds were committed in `data/design/chapter2_selected_neutral_parentage_new64_20261010.json` **before any outcomes were read**.
- Source execution SHA **`48eb9da3f709f40523c8bc13ce3068dc2dd97cf4`**, [Actions #38016780391](https://github.com/zuizui0223/izu-core/actions/runs/38016780391). Dedicated source-only gate, 64 visitor histories × 2 K × 2 ovule budgets × 2 seed gates × 2 inheritance arms **= 1,024 future trajectories** and GitHub archive step all PASS.
- Original [raw complete JSON artifact #11656058352](https://github.com/zuizui0223/izu-core/actions/runs/38016780391/artifacts/11656058352), JSON SHA-256 **`d643ae6601ac0457984a89664617f5bc2d777c76a0f2523049527190d3540107`**, ZIP SHA-256 **`cd1dda99baaf5fa021dec33ef0081b3fa0b3ef410a12ac308753f8ef722d9998`**, source design SHA-256 **`3aaa12452a05197c9150ebec22f100ccf7e372d0a63f21704381c45c0dd8c1f7`**.
- Code: `scripts/audit_chapter2_selected_vs_neutral_parentage_new64.py`; tests: `tests/test_chapter2_selected_vs_neutral_parentage_new64.py`; repository-preserved machine-retrieved source digest/summary: `data/results/chapter2_selected_neutral_parentage_64_history_receipt_20261010.json`.
- Each visitor history seed 61024001…61024064 is one independently generated *RNG history from the SAME stochastic Model3 generator*. There are **zero independent natural ecological island systems**. At most one demographic repetition per visitor history and exactly 64 independent within-model visitor histories.
- One 95% conservative paired CI is calculated per endpoint and cell by separate exact Clopper–Pearson binomial bounds for mutually exclusive `selected_only` and `neutral_only` event probabilities, Bonferroni combined. A prespecified ±0.05 absolute probability difference region is used. All original extinctions are retained (with final allele means undefined, not zero).

## Complete H80 results, including all negative and unresolved cases

Surviving model populations out of 64 visitor histories:

| Ovule budget | K | Viable-self gate | Original selected parentage | Genotype-neutral parentage | Observed Δ (selected − neutral) | Exact conservative 95% |
|---|---:|---|---:|---:|---:|---|
| 6 | 8 | Baseline | 62 | 59 | +3/64 | [−0.0994, +0.1850] |
| 6 | 8 | Self half | 2 | 0 | +2/64 | [−0.0635, +0.1210] |
| 8 | 8 | Baseline | 64 | 64 | 0 | [−0.0662, +0.0662] |
| 8 | 8 | Self half | 25 | 18 | +7/64 | [−0.1340, +0.3390] |
| 6 | 48 | Baseline | 64 | 64 | 0 | [−0.0662, +0.0662] |
| 6 | 48 | Self half | 14 | 5 | +9/64 | [−0.0072, +0.2665] |
| 8 | 48 | Baseline | 64 | 64 | 0 | [−0.0662, +0.0662] |
| 8 | 48 | Self half | 58 | 48 | +10/64 | [−0.0295, +0.3189] |

**All eight H80 effects are inconclusive under the source-locked decision standard.** The four self-halved-source cells point toward better survival with genotype-dependent selection, but the wide paired exact intervals all cover zero. Apparent zeros in 64/64 versus 64/64 baseline arms are ceilings, not proof of a true zero difference or practical equivalence.

The strongest descriptive survival difference, K48/budget8/self-half, is **58 versus 48 populations out of 64** (+15.625 percentage points), but the conservative interval is [−2.95, +31.89] percentage points. These same 64 ecological history IDs also showed selected-only survival in 12 and neutral-only in 2, so the difference is not an exact pathwise monotone law.

At H20, similarly **all eight cells were inconclusive**, including K48/budget8/self-half selected58 vs neutral52. No cumulative generation20→80 intervention interaction has been prospectively tested.

## Genotype outcomes: meaningful indication, not proven mediation

Among **pairs where BOTH populations survived** to generation80, source selection generally retained higher reproductive-assurance allelic values than neutral parentage. Examples of descriptive paired mean difference in assurance allele dosage:

| Ovule budget | K | Gate | Both survive | Selected minus neutral assurance-allele mean |
|---|---:|---|---:|---:|
| 6 | 48 | Baseline | 64 | +0.1284 |
| 8 | 48 | Baseline | 64 | +0.1202 |
| 8 | 48 | Self half | 46 | +0.1124 |
| 8 | 8 | Baseline | 64 | +0.0809 |
| 8 | 8 | Self half | 8 | +0.0356 |

These conditional differences are compatible with the model's source assurance trait being favored by parentage selection, but **cannot be converted into the fraction of extinction prevented by assurance selection**: survival itself changes the denominator and which genetic states exist. There is no deleterious load, adaptive mutation or independent alternative biological model in this experiment.

## Interpretation for the individual-versus-group evolutionary hypothesis

**Current pattern within this finite Model3 source:** Removing genotype-fitness-biased parentage while preserving original self/outcross reproductive routes appears to lower long-term population occupancy in some selfed-seed-viability-stressed cells, rather than showing the sought scenario in which individual selection drives extinction. However, **zero H80 source cells resolves a 5pp population effect under conservative confidence limits**. A modest directional model result is not evidence of field-evolved island selfing or of absence of evolutionary suicide in other regimes.

The source-selection operator affects which genotype is inherited; it does not eliminate environmentally caused selection on total fecundity or make neutral ancestral fitness identical between source and modified trajectories. The two operators create different allele trajectories, then those trajectories feed back on demographic recruitment. A direct causal decomposition of genotype advantage versus absolute N using this contrast alone is **not identified**.

**Next possible independent follow-up** should not simply add more simulations to the same post-outcome cells and call them confirmation. It needs a distinct preregistered design with sufficient expected precision, independent visitor-history sample, jointly matched founder/N0/K/B and a physically interpretable selection knockout or whole-genotype transfer. A fully frozen-genotype arm would need explicit rounding, sham sampling and inheritance provenance, rather than secretly redrawing genotypes and calling it a no-drift control.

**Disposition:** PR #452 remains Draft, #411 and #451 scientific claims intact, #420 remains a separate exploratory finite genetics source. This is a source-verified new Chapter2 mechanistic demonstration, not a completed evolutionary-suicide manuscript.
