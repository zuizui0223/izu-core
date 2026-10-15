# Assurance × pollen availability: source-only scope audit (2026-10-15)

**Status: read-only diagnostic, NOT a new biological simulation, prospective confirmation or manuscript claim promotion.**

## Question and why this audit is necessary

The four-setting Model 3 experiment showed that permitting evolution of autonomous reproductive assurance (A) compresses the between-environment floral-investment (I) contrast. The post-confirmation arm decomposition showed more additional investment loss on near (higher visitor replenishment) than on far (lower replenishment). This can be misread as claiming that the **total evolved investment decline is larger where pollinators are common**. That reading is false.

We distinguish three separate quantities:

1. **Total investment response** in a fixed-A or evolving-A history, relative to the founder.
2. **Within-environment A-evolution intervention effect:** terminal I in evolving-A minus terminal I in fixed-A, in the same arm.
3. **Fixed-resident rare-mutant coupling:** change in the local I selection gradient when A is changed artificially at an identical plant and visitor state.

They are different estimands. Quantity (3) is not an identified mediation decomposition of (2).

## Historical four-setting checks: the apparent paradox is specific to (2)

The existing prospectively frozen 8,192 positive-mutation histories plus 256 zero-mutation controls are unchanged. The original source readout and decomposition are [generality result](../data/results/chapter2_assurance_generality_20261006.json), [common-replicate arm decomposition](../data/results/chapter2_assurance_attenuation_decomposition_20261006.json), and [fixed-resident components](../data/results/chapter2_assurance_gradient_components_20261006.json). There are 64 independent visitor histories per setting, eight nested demographic repeats, complete terminal occupancy, and 128 exact zero-mutation matched fixed/evolving controls.

| Original mating setting | Near E−F endpoint I | Far E−F endpoint I | Δβ_I(A .75−.25), near snapshot400 | Δβ_I(A .75−.25), far snapshot400 |
|---|---:|---:|---:|---:|
| Delayed/no assurance cost | −0.1253 | +0.0352 | −0.4343 | −0.0549 |
| Prior selfing | −0.1985 | +0.0215 | −0.5886 | −0.0655 |
| Pollen discount | −0.1699 | +0.0216 | −0.5251 | −0.0590 |
| Assurance allocation cost | −0.0789 | +0.0218 | −0.4343 | −0.0549 |

E−F means **evolving A minus fixed A**, not evolutionary change from the founder. The absolute far investment changes are strongly negative in both modes. A itself increases **more** in far than near in every setting. The greater *additional* near investment loss therefore does not contradict an isolation-related total decline in I or greater A evolution under low visitor replenishment.

The far terminal E−F investment effect is **positive** even though the A-high-minus-low static gradient effect is **negative** there. The static negative gradient is not sufficient to explain the positive endpoint difference. This discrepancy is a legitimate question for the inherited multigenerational process, but it cannot be assigned solely to allele covariance, drift, parent sampling, or other particular mediators from four arm means.

## Structural null and post-hoc mathematical envelope

The source code is [reproduction.py](../scripts/model3_island/reproduction.py) and the corrected [rare-mutant selection.py](../scripts/model3_island/selection.py). In the source model with **no delivered pollen**, F=P=0 and positive viable selfing S gives parental-genome contribution W=S. Because the investment allocation cost is multiplicative and independent of A, its local investment gradient is exactly

\[
\beta_I = \partial_I \log W = -2 c_I I.
\]

So changing A does **not** further change that local gradient at no pollen. This is a genuine algebraic zero in the model, not evidence for a novel ecological effect.

The companion script evaluates the unmodified *rare-mutant* source equations for one deliberately artificial community with four visitor optima (0.35, 0.45, 0.55, 0.65), resident matching=I=0.5, A=0.25/0.75 and **pollen-budget** multipliers (0, 0.25, 1, 2, 4, 8, 16, 64). This grid was selected after the established main result for *diagnostic shape checking only*. It does not change visitor replenishment, reproduce the original near/far histories, or generate evolution.

Representative mathematical values (rounded; rerun source script for full machine output):

| Mating setting | Δβ_I at no pollen | Δβ_I at 1× | Δβ_I at 8× | Δβ_I at 64× |
|---|---:|---:|---:|---:|
| Delayed/no cost | 0 | −0.4983 | −0.0293 | ≈0 |
| Prior selfing | 0 | −0.8151 | −0.4870 | −0.4618 |
| Pollen discount | 0 | −0.7022 | −0.0676 | ≈0 |
| Assurance cost | 0 | −0.4983 | −0.0293 | ≈0 |

The independent rare-mutant finite-difference implementation is checked against the source analytic gradient for **every** artificial grid cell. At 64× this **artificial** community has source outcross fraction >0.9999. It is **not** a claim that the original near histories were pollen saturated. Prior selfing remains a counterexample to a universal statement that assurance coupling vanishes at saturation: preemptive selfing continues to change the balance of female, paternal and selfed contributions even when q is near one.

**Therefore a simple universal maximum-at-intermediate-pollination hypothesis is not established.** Different mating rules already have different near-saturation limits in the same model family; the pollen-discount curve may also have tiny sign changes within the artificial envelope. Do not choose a favorable optimum a posteriori and claim prospective support.

The already completed **original near-history** feasibility audit [2026-10-10](CHAPTER2_HIGH_REPLENISHMENT_POLLEN_LIMITATION_FEASIBILITY_20261010.md) scaled source pollen budget 1,2,4,8,16 and **failed** its required near sufficiency gate even at 16×: mean outcross fraction **0.8871**, with only **48/64** histories at ≥0.90 (required 60/64 and a mean ≥0.90). Fifty original far histories had zero visitor types and cannot be restored merely by increasing pollen budget. Its 640 rows are not an evolutionary experiment.

## Scientific disposition

- **No verified source sign/normalization bug found in the audited endpoints and native rare-mutant equations.** This read-only check does not constitute a complete new all-array ABM replay or a guarantee against all implementation errors.
- **Strongest old result retained:** with A fixed, low replenishment already causes total I decline; allowing A to evolve attenuates the near–far I contrast in all four declared settings.
- **New causal claim NOT established:** why allowing A evolution produces a small positive relative I shift on far. Source data indicate static selection alone is insufficient; multigenerational inherited-population attribution remains unidentified.
- **High-pollen generalization NOT established:** original near remains pollen-limited under the previous 16× feasibility grid; the artificial mathematically saturated visitor group does not show the results of evolved trajectories.
- Do not promote this audit into the existing Ecology Letters manuscript as independent positive evidence. Preserve the original primary, later failed gates, and separate Ch1 evidence rank.

## Reproduce

From repository root:

    python -m scripts.audit_chapter2_assurance_coupling_scope_20261015
    pytest -q tests/test_chapter2_assurance_coupling_scope_20261015.py

The command reads only frozen result/design JSON and the existing native rare-mutant equations. It produces a report to stdout and writes no tracked data. Optional --out writes a report to a **new** path only (refuses overwrite). No population advance, simulation, or new offspring/genome history is invoked.
