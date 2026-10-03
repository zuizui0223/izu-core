# Chapter 2 deterministic-density interpretation audit — 2026-10-03

**Status:** stop-ship interpretation audit; numerical bridge results retained, causal interpretation narrowed.

## Trigger

The prospective 6,400-season diagnostic exposed sub-individual deterministic density mass in the long-horizon extension. This raised a propagation question for the frozen 200-season bridge: can the deterministic genotype-density layer be interpreted as the stochastic expectation or large-population target of the finite ABM?

The implementation itself already gives a strict boundary. `scripts/model3_island/density.py` describes the genotype-density process as a **conditional deterministic closure, not the stochastic mean**.

Therefore the following interpretation is not licensed by the model definition alone:

> finite ABM effect = deterministic expected effect attenuated by finite population size.

Likewise, movement of a capacity-192 finite mean toward the density value is not by itself evidence of convergence to a stochastic or infinite-population expectation.

## Frozen numerical results that remain valid

At the original 200-season bridge and inbreeding depression 0.50:

- finite ABM far-minus-near investment effect: **-0.1446**;
- deterministic density closure: **-0.4510**;
- capacity 192 finite mean: **-0.2716**;
- finite mixed histories fall strongly when capacity increases.

These are valid model outputs. What is under audit is their **cross-layer interpretation**.

## Immediate wording correction

Until population-scale comparability is established:

1. call the density layer a **conditional deterministic closure**;
2. do not call it the finite model's expected trajectory;
3. do not interpret the finite/density magnitude gap as a finite-population attenuation coefficient;
4. retain the 41.5% gap closure only as a descriptive arithmetic fact;
5. retain capacity effects on mixed-label/repeat instability as finite-demographic sensitivity, without using the density mean as an asymptotic target.

## Exact 200-season population-scale audit

A separate locked diagnostic on `chapter2/el-repeatability-20261003` reruns the frozen natural near/far bridge with the exact source snapshot, all 128 histories, three starting states and eight demographic seeds.

It records:

- finite terminal population;
- deterministic terminal density mass;
- occupancy;
- the finite and density inherited-investment changes.

The audit must first reproduce the published bridge means (-0.1446 and -0.4510). It then compares finite replicate-mean population with deterministic mass for the same history × starting state.

### Decision

If far-arm finite populations remain occupied while deterministic mass is orders of magnitude smaller, the cross-layer magnitude comparison is not interpretable as finite-size attenuation/convergence.

If population scales are comparable, only the semantic boundary remains: the density layer is still a conditional closure rather than the stochastic mean, but the stronger population-scale concern is not supported.

## Scope

This audit does not alter the biological operator, the frozen bridge outcomes, or natural-island claims. It corrects the interpretation of the relation between two synthetic model layers.
