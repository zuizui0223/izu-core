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

## Exact 200-season population-scale audit — result

The exact source snapshot from the original successful bridge production run was recovered and rerun.

### Original focal condition: depression 0.50

Across all 128 histories × three starting states:

- deterministic far density mass at season 200 is **48.0 in every cell** to floating-point precision;
- finite demographic replicate 101 has mean far population **47.992**, median **48**, minimum **45**, and 100% occupancy;
- the frozen bridge already establishes 100% occupancy across all eight repeats (3,072/3,072 far and 3,072/3,072 near).

**Decision:** the sub-individual population-scale concern does **not** apply to the original -0.4510 focal density result. The finite and density layers are on comparable population scales at depression 0.50 and season 200.

The semantic boundary nevertheless remains: the density closure is not the stochastic mean of the ABM, so -0.1446 versus -0.4510 is not an identified finite-size attenuation coefficient and the 41.5% capacity-gap closure is descriptive only.

### Later sensitivity: depression 0.75

Across the same 128 histories × three starts:

- far density mass median: **0.000301**;
- **98.18%** of density cells are below one individual at season 200;
- in finite demographic replicate 101, **384/384** far populations are extinct by season 200;
- median extinction season is **61**.

**Decision:** the depression-0.75 deterministic 116/11/1 history classification is a mathematical closure sensitivity after the persistence boundary, not evidence about repeatability among persisting populations.

## Scope

This audit does not alter the biological operator, the frozen bridge outcomes, or natural-island claims. It corrects the interpretation of the relation between two synthetic model layers.
