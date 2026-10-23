# R2: Is a weak incremental assurance response rare, small, or both?

**2026-10-23 — source-bound, post-outcome descriptive reanalysis.** This note does not introduce new Model 3 population steps, new independent founders, a prespecified test, p-values or a fixation-mediation claim. It supplements—but does not revise—the present R1–R5 manuscript. R2 remains **original-four-setting attenuation supported, fresh-founder all-four generality INCONCLUSIVE**.

## What the original 384-path experiment measured

The source cohort contains **12 founder genomes**, four demographic repeats nested in each founder, two nominal starting-A strata (A=0.3/0.5), strong versus weak prior pollen limitation, and paired future visitor-activity decline versus maintenance: 12×4×2×2×2 = **384 complete trajectories**. Within each original 48-pair baseline/initial-A stratum, the future decline and control share exactly the same census-30 population and RNG, and every trajectory survives. The original reported `A80_decline − A80_control` is a *signed terminal contrast*, **not realized-selfing percentage points**.

The earlier independent saved-data reviewer checked original bytes/protocol, 384 source identities, per-update reproduction records, 48 pair contrast counts per stratum, and census-30 fixation. This new note uses only those already source-admitted summaries. The unchanged original experiment found much larger incremental A responses after weak than strong baseline limitation, but **baseline history and current absolute pollen fertilization differed together**.

## New descriptive partition of response frequency versus conditional magnitude

Define `D=A80_decline−A80_maintained`. For each 48-pair stratum:
- `p_nonzero = count(D != 0)/48` is the **exact-numerical-nonzero share**, not a biologically meaningful response probability.
- `mean(D | D != 0) = 48 * mean(D)/count(D != 0)` is an arithmetic signed mean **conditional on an observed nonzero**; it can include positive and negative contrasts and is not a causal subgroup effect.
- Since every census-30 monomorphic A cohort remained unchanged in both no-mutation/no-immigration futures, `mean(D | A polymorphic at 30) = 48 * mean(D)/(48−count(prefix fixed))`. This is also descriptive selection on a source-defined state, not proof that polymorphism causes the contrast.

| Starting A | Pollen-limitation prehistory | D exactly zero /48 | D nonzero /48 | Census-30 A fixed /48 | Zero despite A-polymorphic at shock /48 | Full 48-pair mean D | Mean signed D among exact-nonzero |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| **0.3** | Strong | **45** | **3** | **22** | **23** | +0.008735 | **+0.139757** |
| 0.3 | Weak | 8 | 40 | 1 | 7 | +0.112413 | +0.134896 |
| **0.5** | Strong | **42** | **6** | **10** | **32** | +0.004612 | +0.036892 |
| 0.5 | Weak | 8 | 40 | 1 | 7 | +0.088162 | +0.105794 |

For A=0.3, the **unconditional** signed effect differs greatly, while **nonzero conditional signed means are similar** (strong +0.1398 versus weak +0.1349). The descriptive contrast is largely one of how often nonzero trajectories occur. For A=0.5, both the incidence of nonzero contrasts and their conditional means differ.

The key constraint is more specific than "fixation explains memory": in strong baseline A=0.3, **45** zero contrasts coexist with only **22** already fixed prefixes. Thus at least **23 pairs still had segregating A at the shock yet ended with zero decline-minus-maintained A contrast**. For A=0.5 the corresponding count is **42−10=32**. In weak baseline the analogous counts are **8−1=7** in both nominal starting A strata.

These 23/32 nonfixed-at-shock pairs with zero terminal policy contrast are an explicit reason **not to attribute all baseline-response attenuation to prefix fixation**. Shared endpoints after alternative trajectories, source-specific pollen availability and selection responses, later fixation or low observable effect are all candidates; their relative contributions have not been identified. In particular, a zero **paired difference** need not mean that neither arm's A changed.

## Exact descriptive two-factor partition (not causal mediation)

Because `mean(D) = p_nonzero × mean(D | D!=0)`, the observed weak-minus-strong difference can be split **symmetrically and arithmetically** into a term associated with nonzero-response frequency and a term associated with mean signed size among nonzero responses. This is the two-order average of a product identity, **not** an intervention on incidence, a fixed threshold or a biological mediation fraction.

| Initial A | Weak−strong overall D | Nonzero-frequency component | Conditional signed-magnitude component |
| ---: | ---: | ---: | ---: |
| **0.3** | **+0.103678** | **+0.105856** | −0.002177 |
| **0.5** | **+0.083550** | **+0.050535** | **+0.033015** |

The terms sum exactly to the original corresponding 384-path contrasts. A decomposition can have a component larger than the total when the other contribution opposes it, as for A=0.3. The fraction of initial A variation lost before the shock can be included in a separate *arithmetic composition identity*, but that identity still does **not** identify the causal effect of fixation: strong/weak source groups have different A distributions, recipient pollen q and histories.

Using the *prefix polymorphic proportion* rather than the exact-nonzero fraction in the same symmetric identity, the two parts are respectively **+0.028641 and +0.075037** (starting A=0.3), and **+0.008987 and +0.074563** (starting A=0.5). This second partition underscores that differences in how many sources were already fixed **cannot numerically exhaust** the whole observed strong-versus-weak contrast. The remaining conditional difference is not uniquely assigned to any alternative biological mediator.

Both identities are retrospective transformations of **the same original 48 pairs within each stratum**. Neither provides new confidence intervals, independent experimental replications or a test of a population-level ecological threshold.

## What remains supported, and what must not be promoted

- **R1 retains its supported statement:** investment I can decline without evolving A, even in an independent 8×8 fresh-founder comparison. Holding A fixed is **not** removing all selfing.
- **R2 retains its qualification:** original 4/4 near–far I attenuation was supported for the original shared founder; the **prospective fresh-founder combined 4-setting criterion was inconclusive**, with direct A cost unconfirmed. This response-sparsity analysis comes from a different *exploratory* 384-case experiment and is not an independent confirmation of the 4-setting rule.
- **R3 retains its distinction:** consistent endpoints, weak known-ID predictor skill for I and finite stochastic realization are different objects; zero in 45/48 paired R2 contrasts cannot establish an absence of directional selection.
- **R4 and R5 remain unchanged:** preregistered G/S contrasts and the post-outcome resource-dependent net alive-and-high-I-support sign reversal remain in their original separate 160×160 cohort. Transfer outcomes are nested exploratory futures, not independent island recolonizations.

**Principal new defensible statement:** In the original explored baseline-384 setting, reduced A response after strong prior pollen limitation occurs mainly through a high frequency of zero incremental-treatment contrasts; already-fixed A explains some but **not all** of that sparsity. This is an inference from observed source contrast counts, not an identified causal path or an externally validated island principle.

## Discriminating R2 experiment to run next (design only; NOT approved or executed here)

Aim: separate the **fate of standing A variation** from **instantaneous pollen delivery** and **source-history state**, rather than fit a retrospective single "evolutionary memory" parameter.

1. **Independent source axes:** new founders and visitor-history schedules generated independently of the archived twelve. Match paired low/high prehistories within source identity and archive every census-30 genotype and realized `q`, `A`, `M`, `I`, population size and allelic diversity. Do not treat nested demographic repeats as independent founders.
2. **State-based and equal-pollen controls:** evaluate natural current-visitor service *and*, separately, an explicitly defined external pollen-receipt intervention that matches per-recipient `q` or receipt vector. A global activity multiplier or equal total exported/delivered pollen is **not** sufficient in heterogeneous diploids (see prior [delivery-matched audit](CHAPTER2_DELIVERED_POLLEN_MATCHED_SOURCE_20261010.md)).
3. **Genetic support/fixation factorial:** compare original donor states to an explicitly declared source-state exchange or mixed-A intervention, matched by founder and other-locus state where possible. A = already monomorphic cannot regain alleles without mutation/immigration. Mixing donor genetic states changes covariances; describe it as a **new artificial intervention**, not the original native Model 3.
4. **Prespecify three different endpoints before new source outcomes:** (i) probability of a meaningful absolute change in A, with an a priori threshold distinct from exact nonzero, (ii) signed magnitude conditional on being above threshold, and (iii) all-start signed A and I contrasts with occupancy. Include current `q`, pollen routing and paternal export; no survival-conditioned silent exclusions.
5. **Discriminating interpretation:** if equal-pollen controls erase baseline differences, current service is sufficient *for that intervention*. If differences persist but collapse under genetically matched source states, the retained state is important; in the native Markov model there is no separately encoded "memory" after fixing complete current state plus future exogenous schedule and stochastic seeds. A factorial cannot uniquely assign mediation without carefully defined manipulable state components.

Pre-execution work still required: document exact new intervention kernel/source version, feasibility/positivity for matching per-recipient pollen, independent two-axis power, unique seeds, fixed budget, a biological minimum A contrast, and fail-closed blinded source checks. The old 384 outcomes **must not be reused as a prospective registration**.

## Reproduction

```bash
python -m scripts.audit_chapter2_r2_response_sparsity_20261023
python -m pytest -q tests/test_chapter2_r2_response_sparsity_20261023.py
```

The runner reads [original admitted 384 table](audits/CHAPTER2_BASELINE_POLLEN_384_AUDIT_20261019.json) and [independent review](audits/CHAPTER2_BASELINE_POLLEN_384_INDEPENDENT_REVIEW_20261019.json); it refuses mismatched original source protocol SHA, fixed-pair counts, sample denominators or mean A contrasts. No new population simulation, new statistical inference or external island generalization is performed.
