
# K=32 source same-heterozygote symmetric perturbation

## Why this matters

Previous one-copy assurance perturbation results used potentially
different **individual genotype backgrounds** for high->low and low->high
flips, because available allele copies were sampled independently.
An apparent asymmetry in source-minus-control slope could therefore
reflect different multilocus backgrounds rather than nonlinear
mating/fecundity response to assurance dosage.

This diagnostic removes that specific confounding source by selecting
the SAME baseline parent genotype copy, heterozygous at assurance,
and constructing TWO separate counterfactual source states:

- Exactly one heterozygote low/high becomes low/low.
- Exactly the same baseline heterozygote low/high becomes high/high.

All other parental genotype copies, all other loci, N, visitor state,
reproductive setting, and original Model 3 biology remain identical.

## Fixed input and analytic source kernel

K=32; original prior_selfing sexual reproduction; full three-locus
diploid joint-genotype inheritance; mutation rate=0, adult survival=0,
seed immigration=0, 8 annual time steps. Only old history 26110601,
near. Two existing resource levels: ovule budgets 8 and 3. Use 128
independent nested demographic histories per budget, inspecting parent
censuses before updates at years 3,5,7,8.

Each perturbation changes assurance frequency by ±1/(2N), and
source next-generation conditional allele frequency is evaluated
analytically using original reproduce and the complete Mendelian
kernel. No additional one-step offspring sampling or prospective
visitor history is introduced.

The counterfactual **directional null** uses neutral equal-parent
Mendelian mating with a calibrated assurance-dosage exponential tilt.
That tilt is selected ONLY for the unperturbed source genotype state,
so the baseline expected source and control child assurance frequencies
are identical. The same theta is frozen for BOTH perturbed states.

The source central response slope is the average of local upward and
downward source slopes. The control central slope is defined similarly.
The finite central response contrast is source minus control.

Second difference (curvature) in conditional next-generation
frequency is:

    source_Q(high) + source_Q(low) - 2*source_Q(baseline).

This has allele-frequency units and is NOT a normalized selection
gradient. Report the analogous control second difference and
source-minus-control difference. The exact source-state identity
holds separately for the two symmetric flips.

## Guardrails and interpretation

If no assurance-heterozygote copies are present at a checkpoint, the
paired symmetric intervention is ineligible: count it explicitly.
If baseline assurance frequency is fixed at 0 or 1, a baseline control
tilt is unidentifiable. Do not substitute theta=0 and treat the
comparison as valid.

A nonzero response or curvature contrast beyond the single tilted
Mendelian null can show local sensitivity to the source's more complex
reproduction operator; it does NOT uniquely identify stabilizing
natural selection, full eight-generation variance regulation or
a real-plant fitness mechanism. One archived visitor history with
128 nested genetic/demographic paths remains n_ecological=1.
The comparator deliberately changes mating biology, whereas original
Model3 biological source files remain untouched.

## Reproducibility

    pytest -q tests/test_model3_k32_symmetric_assurance_curvature.py
    python -m scripts.audit_model3_k32_symmetric_assurance_curvature --out symmetric-budget8.json --budget 8 --draws 128
    python -m scripts.audit_model3_k32_symmetric_assurance_curvature --out symmetric-budget3.json --budget 3 --draws 128

CI job model3-k32-symmetric-assurance is PR#420 scoped and archives
results. Results are engineering simulations, not ecological
independent cohort confirmation. No SDE/SPDE or geographic analysis.

The 8-year directional response, local response, and curvature tests
must NOT be promoted to adaptive causation without an explicit
mechanistic or empirical intervention independent of these fitted
comparator models.

## Source-verified symmetric numerical results (2026-10-09)

CI dedicated job model3-k32-symmetric-assurance **success** on source
SHA 76e83d2917024da9dced0ce59bfbb224b2b92550,
[GitHub Actions run 37889777989](https://github.com/zuizui0223/izu-core/actions/runs/37889777989);
[raw two-budget JSON artifact 11598345415](https://github.com/zuizui0223/izu-core/actions/runs/37889777989/artifacts/11598345415).
Machine-readable source-lock:
data/results/model3_k32_symmetric_assurance_response_20261009.json.

Main endpoint is SOURCE central slope minus baseline mean-matched
directionally tilted Mendelian control central slope, with the SAME
heterozygous individual genotype mutated separately low and high:

| Source states BEFORE generation | budget8 usable / 128 | budget8 mean source minus control central slope (MC SE) | budget3 usable / 128 | budget3 mean difference (MC SE) |
|---|---:|---:|---:|---:|
| 3 | 128 | -0.04598 (0.00894) | 122 | -0.06474 (0.00753) |
| 5 | 119 | -0.09338 (0.00948) | 90 | -0.13426 (0.01116) |
| 7 | 75 | -0.16797 (0.01014) | 41 | -0.20514 (0.01602) |
| 8 | 49 | -0.16881 (0.01354) | 23 | -0.24757 (0.01598) |

The source response is less sensitive to the specified one-copy
intervention than this simplified mean-matched control at every
examined source checkpoint/condition. The curvature contrast is also
positive, about 0.00755-0.00851 (budget8) or 0.01305-0.01726
(budget3) offspring-frequency units under the finite two-sided swap.

**However**, the eligible subset shrinks drastically towards fixation,
especially for budget3 where only 23/128 parent states retain one
assurance-heterozygote in generation 8. Therefore the larger late
slope gap **must not** be interpreted automatically as stronger
adaptive restoration through time: the estimand changes with
heterozygote availability. No result is defined for fully fixed parent
states in this comparator construction.

This improves identifiability relative to separate high-to-low
and low-to-high comparisons by eliminating the different-perturbed-
genotype-background confound; nevertheless the genotype's association
with the other two loci and the original source reproductive fitness
and mating rules remain jointly involved. The null is one particular
directionally tilted Mendelian operator fitted to each baseline,
not an independent observation or unbiased ecological reference.

**Verdict:** source-specific local numerical response beyond
the chosen baseline-matched simplified comparator is supported
*within this one frozen model and old visitor history*. Source-specific
global terminal variance regulation, causal adaptive stabilization,
independent ecological confirmation and any continuous-time SDE/SPDE
interpretation remain **NOT identified**.
