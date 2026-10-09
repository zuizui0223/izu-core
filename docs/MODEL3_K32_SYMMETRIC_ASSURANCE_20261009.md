
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
