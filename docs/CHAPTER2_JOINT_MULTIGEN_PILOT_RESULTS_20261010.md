# Model3 #420 × #451 connection: 80-update synthetic multigeneration preflight (2026-10-10)

**Evidence:** Exploratory **engineering demonstration**, not a new preregistered ecological confirmation. Runs the canonical, unmodified full-diploid Model3 `advance` and previously validated `reproduce_kb` + postzygotic seed gate, from **one fixed eight-founder synthetic genotype source** retaining standing variation at all three loci. No A-first/I-first expression histories were assigned, no archived visitor RNG histories or confirmation cohorts were accessed, and no ecological field data were used.

## Source-locked execution

- Original source SHA **`40811ecbeddfc0f69aa43da381cb6fd27f46f634`**
- GitHub Actions CI run **[38011492391](https://github.com/zuizui0223/izu-core/actions/runs/38011492391)**, Python 3.11 step **“Run source-matched synthetic 80-generation pilot” SUCCESS** and upload step **SUCCESS**.
- Original [JSON artifact ID 11653441514](https://github.com/zuizui0223/izu-core/actions/runs/38011492391/artifacts/11653441514), 19,224 uncompressed JSON bytes; exact JSON SHA256 **`fdc240f65cfa5a962dc1d700ca4f0c4b2342f895f0e688e85e478a1cf9b61670`**. Original artifact zip SHA256 **`f6580d18da0984316563f75662750368af5d0bee6755c0f72421b621260f59c5`**.
- Machine-extracted compact permanent receipt: `data/results/chapter2_joint_multigen_synthetic_pilot_receipt_20261010.json`.
- Exact source reproduction: `python -m scripts.audit_chapter2_joint_multigen_engineering --draws 48 --years 80 --out chapter2-joint-engineering-pilot.json`. Both K arms use identical eight diploid founder genotypes and fixed B48. All 48 demographic repeat identities have matched RNG seeds across arms.
- Conditions: no mutation, no adult survival, no seed immigration, **prior selfing**, 3-ovule budget, 80 reproductive updates, K8 versus K48, three gates (baseline / half viable self / half viable outcross), and **two explicitly hand-authored STATIC visitor regimes** (two fixed visitor phenotypes or no visitors). **These are not 96 independent ecological histories.**

## Actual unconditional occupancy counts after 80 updates

Each cell contains **occupied simulated demographic paths out of 48** under one fixed engineered visitor condition:

| Regime | K | Baseline | Half viable self | Half viable outcross |
|---|---:|---:|---:|---:|
| Two hand-authored visitors | 8 | **0/48** | **0/48** | **0/48** |
| Two hand-authored visitors | 48 | **7/48** | **0/48** | **6/48** |
| No visitors | 8 | **0/48** | **0/48** | **0/48** |
| No visitors | 48 | **3/48** | **0/48** | **3/48** |

**Strong negative diagnosis / fundamental design limitation:** The 3-ovule stress and 80-update horizon cause an **occupancy floor at K8 across every tested arm** in this small simulation. Thus an observed zero K8 baseline-minus-gate effect is *uninformative* about whether viable selfed seeds could affect small-population survival under a different regime. It cannot be read as zero true causal sensitivity or a contradiction of the #451 independent K8-vs-K48 A/I *interaction*. Both endpoints and interventions differ.

At K48, viable-self seed halving is associated with **zero survivors in all 48 demographic paths** in either artificial visitor regime, compared with 7/48 or 3/48 untreated survivors. Those are descriptive Monte Carlo counts, **not** population-level effect estimates with independent ecological replicates. Reproductive recruit totals accumulate over different path lengths and cannot be promoted to causal mediation.

The **mechanism-specific negative control worked**: in a visitor-free environment all outcross seed ledgers have zero mass, so the half-outcross gate is null. Under paired streams, baseline and half-outcross outcomes are *identical* across all 48 demographic repetitions at both capacities. By comparison, visitor-present outcross ablation yields 7/48 versus 6/48 at K48; the one-survivor net difference with 4 favorable and 3 unfavorable paired discordances is not evidence of a reproducible directional effect.

## The genetic-versus-persistence observation

At the SAME starting founder genotype and each visitor environment, initial one-generation *expected* allele-frequency direction of the **assurance locus** is positive (rounded values from the original source):

- No visitors: assurance **+0.0512**; matching **−0.0007**; investment **−0.0076** (same expected direction for all seed gates because no outcross route exists).
- Two visitors: baseline assurance **+0.0431**; matching **−0.0005**; investment **−0.0052**. Half-self gives assurance **+0.0367**, half-outcross **+0.0469**.

The first-step expected assurance-high direction is **K-invariant** under fixed B and identical parents, as analytically established by the one-step preflight. Yet **none of the 48 K8 paths in either visitor condition persisted for 80 updates at this budget**. This directly illustrates why a positive one-generation transmission expectation and the empirical finite-horizon occupancy of a population are **non-equivalent mathematical outcomes**. It **does not establish** that genetically increasing assurance causes extinction or that natural selfing evolution is maladaptive: seed survival, demographic stochasticity, cumulative future genetic states, founder support and severe census cap all act simultaneously.

**No genetic allele frequency has been set to zero after extinction.** Surviving endpoint genetic means are reported only for actual surviving paths; the K8 mean is null, not a manufactured number.

## What next and why this preflight is not a publication claim

1. **Diagnostic occupancy surface:** before selecting a confirmatory parameter or claiming effect absence, vary the stress budget and/or horizon *in a clearly post-outcome engineering grid*, retaining the SAME founder/visitor arms and prerecording the entire grid. This tests whether a reasonable range avoids 0/48 floor and 48/48 ceiling simultaneously. Do not cherry-pick the budget with the best-looking effect.
2. **Joint mechanistic gate:** if a nondegenerate region exists, separately freeze allele transmission, complete genotype distribution, state-dependent selection, and unconditional occupancy estimands. Keep outcross-gate and visitor-null controls.
3. **Novel genuinely independent science:** only after engineering/power diagnostics, seal new visitor histories and analysis threshold *before* generating outcomes. For direct comparison to #451's `tau`, the randomized A-first/I-first schedule must be explicitly included and not silently replaced by spontaneous inherited allele order.
4. **Scope:** This is one model family under uncalibrated artificial ecology. No actual island calibration, SDE/SPDE validation, causal mediation or external transfer has been established.

**Integration update:** #420's exact source self/outcross transmission terms can now be connected to the *same-source* finite recruitment and occupancy process **computationally**. But this first experiment detects a strong K8 survival floor, rather than furnishing a clean answer to the proposed direction-versus-persistence discordance hypothesis. This negative finding should be retained in full.
