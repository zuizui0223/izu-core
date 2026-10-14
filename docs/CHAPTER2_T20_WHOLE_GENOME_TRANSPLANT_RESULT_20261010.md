# Genotype-history transplant at year 20: selected genetic source, future capacity and future parentage (2026-10-10)

**Status: COMPLETE post-outcome mechanistic source replay, not a new independent ecological confirmation.** This result is a conditional finite Model3 experiment within PR #452. It must not be reported as a prospectively supported model-universal survival effect, complete causal mediation fraction or island-plant evolutionary suicide.

## Research question and admissible original source

Previous independent (within-model) 64-visitor-history source #452 comparison contrasted canonical genotype-fitness-biased inheritance with a genotype-neutralized conditional self/outcross recruitment operator. At year80 none of eight within-cohort source contrasts met the preregistered conservative 95% / ±5pp decision threshold, but the selected source often retained higher assurance allele dosage among survivor-only pairs.

**New mechanistic question:** If the *previous* selected versus neutral inheritance operator creates different **joint three-locus diploid genotype distributions** over the first 20 updates, will that difference persist as a group survival effect after placing each genome distribution into an *otherwise identical* future demographic environment?

This experiment **reuses the already exposed original visitor RNG histories 61024001…61024064** and replays exactly the original first 20 update source biology at **K48, B48, ovule budget8, viable-self-offspring 50% reduction, no mutation, no immigration, zero adult survival**, once with original selected parentage and once with genome-neutral-within-self/outcross parentage.

The exact original age20 occupancy comparison is re-derived: **selected source 58/64 alive, neutral source 52/64 alive, and BOTH alive 50/64**. Results can be interpreted **only among those pre-exposure original 50 paired survivors**; the remaining 14 are documented in the full original archive and not treated as 50 additional independent failures or substituted donors. The original difference in t20 survival is **not** a genetic-transplant effect; it was produced before donor selection.

## Genotype transfer and factorial experiment

For each eligible original history and each of the two t20 donor-genotype distributions:

1. Uniformly resample **eight entire individuals with replacement**, carrying over all original three-locus diploid allele pairs together, allele origins and mutation flags. Do not sample independent alleles by locus or manufacture alleles outside source support.
2. Give these eight recipient individuals unique synthetic IDs and the same chronological t20 birth year. **Both future K arms start with N0=8** and use identical original source visitor trajectories at years20–79; background pollen normalization remains **B=48**.
3. Run **both future K=8 and K=48** × **future inheritance selected or genotype-neutral within mating channel**, with matched fresh future demographic RNG streams for all donor/K/operator cells per source visitor history. Source reproduction, selfed viable seed reduction and native birth/census law remain unchanged; in the neutral-parentage future only inherited genome parent choice is counterfactually reassigned while matching source realized self/outcross recruit counts.
4. Record unconditional **survival from admission at t20 to t80** for each transplanted source, all outcomes included irrespective of extinction; genomic phenotypes after extinction are undefined.

This yields **50 source visitor-history units × 2 t20 donor sources × 2 recipient K × 2 future transmission modes = 400 future paths**. Full original 64 donor source statuses and resampling-index provenance are retained.

**Source:** scientific runner `scripts/audit_chapter2_t20_joint_genome_transplant.py`, design `data/design/chapter2_t20_joint_genome_transplant_original_history_v1_20261010.json`, tests `tests/test_chapter2_t20_joint_genome_transplant.py`; original execution commit `15edd960520b553a74dd43f916fd3e18fb4aad29`, [Actions #38017510920](https://github.com/zuizui0223/izu-core/actions/runs/38017510920) source-only smoke and exact original 58/52/50 count gate / entire experiment / archive upload PASS. Full original [artifact #11656184670](https://github.com/zuizui0223/izu-core/actions/runs/38017510920/artifacts/11656184670), raw JSON SHA256 `1c15f1921817f573662615343623e3890c5dce99413484fdd41bb4c07ab52eaf`, ZIP SHA256 `ae0961f182d0bea8a996b4d5dd9551b91fd78cfd1fddf0ee276306a69cfe59e0`, design SHA256 `9b11b1d103c46390716cf6977a33164d7f10a50a8c78790d9f45618c8a4d9bb6`. Machine-readable permanent compact receipt `data/results/chapter2_t20_joint_genome_transplant_receipt_20261010.json`.

## Complete K × G × future-parentage results (occupied at t80 out of 50)

| t20 genomic source | Future K=8, original inheritance | Future K=8, neutral inheritance | Future K=48, original inheritance | Future K=48, neutral inheritance |
|---|---:|---:|---:|---:|
| **Source selected from t0 to t20** | **36/50** | 32/50 | **49/50** | 46/50 |
| **Source parentage neutralized from t0 to t20** | **15/50** | 14/50 | **41/50** | 39/50 |

**Predeclared primary comparator**: t20 genome-origin selected-minus-neutral under original future selected parentage and K48 is **+8/50 = +16 percentage points**, conservative paired 95% **[−2.08,+31.03] percentage points**: **inconclusive**. No selective redefinition of K8 as the primary is permitted after inspecting data.

At future K8 with original future selected inheritance, the donor-genome-origin contrast is **36/50 versus 15/50**, net **+21/50 = +42pp** (paired 24 selected-only vs 3 neutral-only), conservative unadjusted 95% interval **[+13.65,+63.49]pp**. Under neutral future parentage at K8, donor-source contrast is **32 versus 14**, Δ=+36pp, unadjusted interval [+6.44,+59.79]pp. Both are **secondary post-outcome** analyses, not an independently replicated ecological result.

At future K48, source-genome effects have positive point estimates (+16pp under selected future parentage, +14pp under neutral future parentage) but conservative unadjusted intervals crossing zero. New *future* selected-versus-neutral parentage contrasts at a fixed transplanted genome also have small point estimates (+2 to +8pp), all inconclusive.

### Descriptive factorial separation, not a unique causal mediation ratio

Taking a balanced average across all other factor cells over the SAME 50 eligible visitor histories gives:

- Genomic source **selected vs neutral t20**: **+0.27 absolute occupied probability**.
- Future K **48 vs 8 at matched N0=8**: **+0.39**.
- Future transmission **selected vs neutral**: **+0.05**.

These are factorial standardized **differences in 80-update model persistence conditional on survival to t20**. They are not contributions that sum to one, and cannot be called percentage shares of all island extinctions. Large G × K interactions and state-dependent floors/ceilings are possible. A Shapley two-order average allocates overlapping interactions; it does not establish independent physical genetic vs demographic mediation.

At K48 with a **neutral-genomic-source t20 donor**, changing future recipient K8→48 changes occupancy **15→41/50** with original future parentage, Δ=+52pp. This passes nominal exact 95% and a stricter family-wide 12-comparison check. With neutral future parentage it changes **14→39/50** (+50pp), also family-wise robust. Because starting t20 census is the same N0=8, these are valid contrasts of *future carrying-capacity regulation within this source simulation*. They are nevertheless not evidence of an actual natural-island area effect.

## What evolved in the source, and what remained unassigned

Among the exact same 50 original paired-source histories where both donor source populations survived, the mean full t20 diploid traits before resampling were:

| Locus | Selected-source donor mean | Neutral-source donor mean | Selected − neutral |
|---|---:|---:|---:|
| Matching | 0.28530 | 0.29914 | −0.01385 |
| Floral investment | 0.44451 | 0.45701 | −0.01249 |
| **Reproductive assurance** | **0.66533** | **0.58266** | **+0.08267** |

After uniform eight-whole-genotype resampling, approximate recipient means averaged across eligible histories were selected-source **[0.28521, 0.44243, 0.66309]** and neutral-source **[0.30229, 0.45881, 0.58363]**. Hence source selection creates materially distinct genotype states, especially a higher assurance mean in this finite source setting. **This does not isolate the assurance locus**: donor treatments also differ at matching and investment loci, genome variance, allelic support, and potentially three-locus covariance. Without a separately declared locus-specific transplant, no percentage of survival advantage can be assigned to assurance versus other source-genetic effects.

## Multiplicity and evidential status

The original pre-execution-declared twelve per-cell paired comparisons used conservative 95% Clopper–Pearson/Bonferroni component intervals, **one 95% interval per contrast**. This is *not* automatically a 95% family-wide interval across 12 secondary comparisons.

A clearly **post-outcome** family-wise sensitivity therefore allocates total alpha=.05 across all 12 contrasts and both discordance categories (component alpha=0.05/24) without assuming different contrasts are independent. The adjusted CI for the **K8 original future parentage genome-origin difference +42pp** is approximately **[+3.2,+69.4]pp**: its lower endpoint stays positive but lies **below the declared +5pp meaningful-effect threshold**, so it is **inconclusive** by the prospectively defined ROPE rule. The secondary K8-neutral-future genome-origin difference is approximately [−4.2,+66.5]pp and inconclusive. Two future-capacity differences using **neutral t20 source genomes** remain greater than +5pp under this family-wise diagnostic, while the originally designated K48 genotype-origin primary remains inconclusive.

The detailed exact family-wise readout is implemented in `scripts/audit_chapter2_t20_transplant_familywise.py`, with regression tests `tests/test_chapter2_t20_transplant_familywise.py`. **None of this sensitivity analysis constitutes a newly registered ecological confirmation.**

## Interpretation and next discriminating test

This result directly demonstrates within one finite biological simulator, conditional on paired t20 survival and one whole-genotype resampling per source/history, that **selection-built initial genotype distributions can give greater later survival** even when subsequent future parentage mode is matched. Source selection also correlates with a higher assurance allele value, compatible with a reproductive-assurance mechanism.

However:
1. Selection into the both-alive original t20 donor subset (50/64) makes the treatment inherently survivor-conditioned. The source's original early extinction cannot be explained away or assigned to genomic legacy without a separate experiment using unconditional t0 eligibility.
2. Only **one resampling draw of eight genomes per original donor history** was made. The absolute effect can vary with within-donor genotype sampling variance, particularly at K8. A separate nested multiple-draw robustness study is necessary before declaring an exact evolutionary genetic effect.
3. Reused source visitor histories and the known earlier experimental outcome mean there is **zero new ecological independent validation**. Source-model confidence bounds reflect numerical variation of paths, not transportability to other ecological mechanisms or real island systems.
4. Genomic source G is a whole **joint three-locus** difference. An assurance-locus-specific intervention, possibly with a matched locus-sham, is required to attribute mechanisms.
5. Genetically biased source parental transmission remains linked to ecological fecundity, selfed seed viability and the density bottleneck. This neither proves that individual-selected traits can harm the group nor identifies a real evolutionary-suicide scenario.

**Recommendation for the next bounded experiment:** preserve this exploratory positive result and prerecord an assurance-specific genotype-source-swap test alongside full-genome G controls, a within-donor same-genotype sham and multiple genome draws, with new unused future visitor RNG if independent within-model transfer is required. No post-hoc result-based cell searching or invented causal mediation percentage.
