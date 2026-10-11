# Q3→Q4: all-genotype-state equal-pollen functional-mismatch falsifier

**2026-10-11 — exploratory, deterministic source-model intervention. Not an independent ecological experiment, no observed island systems, and not a field-calibrated fitness effect.** Work follows the fixed-richness visitor substitution in merged #468 and the founder-only delivered-pollen negative control in Draft #469.

## Ecological question and causal boundary

The user-directed ecological variable is **declining functional-trait matching between flower and visitor**, not the mere absence of visitor taxa. With four visitor functional types present and the floral matching trait held at 0.20, Model 3's original `reproduce_kb` predicts lower pollen delivery when the visitor optimum profile changes from `matched4` to `shifted4`. PR #469 matched founder **total delivered pollen** under the original community by lowering visitor effectiveness with one fixed factor.

But later genotypes and census sizes can produce new pollen-delivery differences. This PR provides a more stringent **statewise counterfactual**:

For every living Model 3 genotype-count source state `s=(n_low,n_hetero,n_high)`, every fixed synthetic visitor profile, and separately for the native or expression-clamped investment regime:

```text
D_shift(s) = total pollen delivered by four shifted-optimum visitor types
D_ref(s)   = total pollen delivered by four original-optimum visitor types

equality_scale(s) = D_shift(s) / D_ref(s),  when D_ref(s)>0

Compare:
  shifted visitor composition, effectiveness 1
  original visitor composition, effectiveness equality_scale(s)

D_shift(s) = D_equalized(s)  for EACH source genotype/census state.
```

When the current census is one, the original diagonal pollen-transfer exclusion makes both total deliveries exactly zero; the implementation uses a neutral multiplier of 1 and checks that no unrecognized zero occurs.

The two ecological source arms retain **four functional visitor types** and the same original pollen background B48, K8 demographic capacity, pollen-breadth 0.18, visitor activity/configuration, and 0.20 floral matching genotype, with original low/hetero/high floral investment classes and no mutations, surviving adults or plant immigration.

**This is a mathematical intervention, not a feasible static pollinator environment.** The reference visitor's effectiveness is recalibrated separately for each changing genotype, census and expression condition. It could not be imposed as one fixed biological community, and its effects must not be presented as natural causal mediation.

## What can now be tested more sharply?

This is not merely comparing plant populations that start with matched pollen deposition. It guarantees identical **aggregate** delivered pollen in every reproductive state separately. Nonetheless:

- Maternal **recipient-specific pollen** can differ at fixed aggregate total, because the original visitor matching kernel allocates transfer nonuniformly.
- The parentage distribution `q` and **total viable maternal seed output** `mu` can differ through nonlinear fertilization and selfing.
- Founder-mean investment trajectories can diverge through sex-specific parental lottery, then influence later density and survival.
- The mathematical transplant may lead to a residual `P80` difference, or it may yield nearly zero. **Either is an admissible result; do not assume or manufacture a sign.**

The key output is `P80_native_shift_minus_equalized` for each fixed historical four-visitor profile, together with the corresponding **fixed-expression contrast**, the difference of native-minus-fixed effects, and unconditional/conditional low-investment allele fixation.

**This test does not identify a unique paternal route** if a residual survives: the equalization fixes TOTAL pollen only, not the maternal recipient-by-recipient vector or father-specific reproductive success. A residual may be due to different maternal pollen allocation, paternal parentage, viability compensation or their interactions. Exact decomposition would require additional explicitly identified interventions and independent validation.

## Scope and guarded reproducibility

- Historical functional mismatches `lambda = 0.25, 0.50, 1.00` (all preserve four visitor types).
- Four original mating rules and resource budgets 6 and 8; **24 synthetic source combinations**.
- The full **165-state** Mendelian/Poisson exact Markov transition from merged #464 and the original `scripts/chapter2_kb_reproduction.py::reproduce_kb`.
- Genotype identity derives from low/hetero/high **class**, explicitly guarding the spurious numeric-allele identity error corrected in merged #466.
- The tests assert equal total delivered pollen at **every one of the 164 nonextinct genetic-census states** for three mismatch conditions under both investment-expression policies, preserve singleton no-outcross cases, and validate stochastic kernels and the complete result grid.
- There are zero newly generated natural populations, randomized visitor histories, independently registered biological tests, genetic mutation-order comparisons, or observations of actual island floral evolution.

The scientific contribution is **discriminating whether functional composition has a durable modeled occupancy effect after removing its aggregate pollen-quantity difference at every source state**. It is not a general theorem that flower–visitor mismatch is beneficial or harmful. A valid biological followup would measure floral and visitor functional traits, quantity and identity of deposited pollen, seed parentage, and population recruitment under common effort in real island populations.

## Execution

```bash
python -m scripts.audit_chapter2_q3q4_statewise_pollen_equalized_20261011 --out /tmp/chapter2_statewise_equalized.json
pytest -q tests/test_chapter2_q3q4_statewise_pollen_equalized_20261011.py
```

No CI claim, numeric residual conclusion or manuscript upgrade is warranted until the final PR head's normal Python matrix and Chapter 2 science gate have passed. The original #411/#442 prospective evidence is unchanged.
