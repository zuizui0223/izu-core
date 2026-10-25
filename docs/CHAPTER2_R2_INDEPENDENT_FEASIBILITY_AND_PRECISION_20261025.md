# R2 independent confirmation: genetic accessibility identifiability and crossed-source precision review

**2026-10-25 — DESIGN FEASIBILITY ONLY / NO BIOLOGICAL DISPATCH.** This note supports [Issue #638](https://github.com/zuizui0223/izu-core/issues/638). It is **not** a preregistration, an authorized sample size, a demonstrated power analysis, a new simulation cohort, or an additional positive result from natural island plants. Original R1–R5, the registered R4 G/S, and the fresh-founder four-setting R2 **overall INCONCLUSIVE** status stay unchanged.

## 1. Why another split of the original 384 paths is not confirmation

The original 2026-10-19 Model 3 baseline-pollen experiment used **12 independent founder IDs**, four nested demography repeats, and **384 trajectories / 192 matched futures**. The subsequent exact readbacks showed that A and M may be fixed while I still segregates. Among a post-outcome strong-prior-pollen subset, **22 paired source states from 11 founders** had negative immediate expected investment-I contrasts under lower pollinator activity; the decline arm ultimately fixed the lowest available I value in **20/22**. The two exceptions had only **4/96 or 6/96** low-I allele copies at the shock and lost those alleles even though their expected low-I genetic transmission remained positive at each segregating census. Full census30/80 genomes and the original 50-update paths were SHA-verified in [PRs #630–#637](https://github.com/zuizui0223/izu-core/pull/637).

This supports a *testable model-specific separation* between immediate parental-genetic sorting, standing genetic accessibility, and finite realized transmission. It does **not** estimate a universally meaningful critical frequency, selection-versus-drift causal share, or adaptation in natural isolated flora. The previously exposed 384 trajectories and their post-selected subcohorts **must not** be counted as independent fresh confirmation.

## 2. Fundamental identification problem: changing low-I frequency also changes I

For a closed K=48 population, there are 96 diploid I allele copies. If only two numerical I values are possible, `I_low=.25` and `I_high=.50`, and c is the number of low copies, then

[
\bar I = I_{high} - (I_{high}-I_{low})\frac{c}{96}
       = 0.5 - 0.25\frac{c}{96}.
]

Thus a proposal to vary **only** c while holding mean I unchanged in this two-allele closed population is *mathematically impossible*. As purely illustrative examples, c=12,24,36 give mean I **0.46875, 0.43750, 0.40625**. An experiment that simply compares these frequencies would also change the starting floral phenotype/ovule budget, and cannot call the result a pure effect of genetic accessibility.

A possible *algebraic* compensation uses three numerical I values `(.25,.50,.75)` and copy counts:

| Hypothetical low-I copies | I=.25 copies | I=.50 copies | I=.75 copies | Mean I | Allelic value variance |
|---:|---:|---:|---:|---:|---:|
| 12/96 | 12 | 72 | 12 | 0.5000 | 0.015625 |
| 24/96 | 24 | 48 | 24 | 0.5000 | 0.031250 |
| 36/96 | 36 | 24 | 36 | 0.5000 | 0.046875 |

This preserves the **allele-level mean but necessarily changes variance**. It does not specify the 48 complete diploid plant genomes, heterozygosity, A/M covariances, maternal/paternal phenotype-genotype associations, ancestry or history. No such populations were generated here, and these illustrative levels **are not original 4/96, 6/96, 16/96 post-hoc critical-frequency candidates**. Genotype realization and the scientific interpretation of this multivariate intervention require independent method review before authorizing a new cohort.

## 3. Two genuinely independent crossed sources, with nested realization

A future study would cross **independently drawn founder genomes** with **independently drawn visitor-history identities**. Demographic replicates are nested inside each founder×visitor cell; two current visitor-activity arms share the exact same census30 genome at each assignment. At every census retain the full `N×3×2` alleles, genetic origins, A/M/I values and support, population N, visitor matching and per-mother outcross fertilization `q`, as well as maternal viable selfing, paternal pollen contribution, and extinction. Nominal visitor activity or aggregate pollen export must **not** be treated as equivalent to matched actual per-mother q.

Two **illustrative**, not yet frozen, outcome families are:
- An **all-allocated, within-source visitor decline minus maintained** indicator for first loss of the low-I allele by update80, with prior extinction explicitly reported as a *competing event*, not coded as zero I.
- A difference-of-differences of that paired loss indicator between high and low *hypothetically constructed* standing-access arms. This is conditional on a properly specified genotype-construction intervention and must not be called an isolated frequency effect if initial variance, covariances or parental phenotype distribution also change.

The first contrast lies in **[−1,+1]**; the second in **[−2,+2]**. The old source's **exact-zero final phenotype contrasts must not be coded as lack of expected parental selection**. Multiple testing, the biologically meaningful smallest effect (SESOI), the exact prospective source distribution, and treatment selection remain undecided.

## 4. Workload and sensitivity: no false independence, no invented power

For candidate counts F independent founder genomes, V independent visitor histories and R nested demographic repeats, **if later authorized** a grid with two historical pollen regimes, three hypothetical genetic-access arms and two paired future visitor-activity treatments would use:

[
\begin{aligned}
N_{prefix} &= FVR\times 2,\\
N_{future} &= N_{prefix}\times3\times2,\\
U_{unique} &= 30N_{prefix} + 50N_{future}.
\end{aligned}
]

This counts original history prefixes **once per source cell** and does not call any of the ensuing terminal trajectories a new independent founder. The script performs **zero** of these biological updates and does not reserve any future seeds.

A **Normal proxy only** for a crossed-source matched source-level contrast, using completely hypothetical nonnegative variance components, is

[
V_{proxy}=\frac{v_F}{F}+\frac{v_V}{V}
+\frac{v_{F\times V}}{FV}+\frac{v_{nested}}{FVR}.
]

The sensitivity calculation uses two explicitly **unmeasured hypothetical** component sets (moderate/adverse) and two co-primary families, with a *nominal* two-sided 97.5% marginal multiplier (familywise .05 Bonferroni). **Neither this Normal formula nor the input variances are validated uncertainty bounds, causal variance decompositions or power estimates for the proposed new study.** R does not reduce the F or V terms.

| Hypothetical new F×V, R=2 | If authorized: future paths | If authorized: unique updates | Moderate half-width: paired low-I loss | Adverse half-width: paired low-I loss | Moderate half-width: access interaction | Adverse half-width: access interaction |
|---|---:|---:|---:|---:|---:|---:|
| 8×8 | 1,536 | 84,480 | 0.231 | 0.424 | 0.454 | 0.739 |
| 16×16 | 6,144 | 337,920 | 0.151 | 0.288 | 0.299 | 0.496 |
| 32×32 | 24,576 | 1,351,680 | 0.102 | 0.199 | 0.203 | 0.341 |
| 64×64 | 98,304 | 5,406,720 | 0.070 | 0.139 | 0.140 | 0.238 |

These rows show **why 384 nested trajectories do not constitute a high-precision sample of independent founder/visitor effects**. They are not recommended F/V/R values. The final sample size must be chosen from prespecified scientifically defensible effects, precision goals, verified new-source component distributions, computational cost and reviewed prospective operating characteristics—not optimized to make the old 22/22 or 20/22 result significant.

## 5. Non-executable gate and next discriminating step

The original protocol `docs/protocols/CHAPTER2_R2_HISTORY_POLLEN_STATE_NEXT_STUDY_PROPOSAL_20261023.json` remains `DESIGN_ONLY_NOT_AUTHORIZED_NOT_PREREGISTERED`. Its *entire* `run_gate` remains **false**, including `should_dispatch_actions`. The reviewer also checks the Git blob SHA of that protocol and the original source receipts; any change fails closed.

**Open, substantive pre-execution tasks:** scientifically justify the smallest relevant difference in low-I loss risk and the exact two co-primary hypotheses; choose the independent founder/visitor source-generating distribution and variance-estimation pilot; identify whether the genotype copy intervention should intentionally change variance or requires a different construction; validate at the level of full genotypes that A/M/I covariance and parental q are not falsely described as held fixed; precommit the source namespaces and all-start/competing-event analysis; then separately seek formal author approval. An independently powered biological campaign is **not** authorized by this review.

Reproduce this **pure mathematical readback** from repo root:

```bash
python -m scripts.review_chapter2_r2_independent_feasibility_20261025
python -m pytest -q tests/test_chapter2_r2_independent_feasibility_20261025.py
```

The scientific author-review gate archives the audit JSON; it does not dispatch any biological jobs. Existing R1–R5 results and the original 384 source ZIP remain untouched.
