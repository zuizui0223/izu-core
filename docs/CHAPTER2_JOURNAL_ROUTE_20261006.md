# Chapter 2 journal route — 2026-10-06

## Decision

**Primary target: Ecology Letters.**

**Backup target: Journal of Ecology.**

**The American Naturalist / Evolution remain theory-oriented alternatives.**

This routing replaces the earlier same-day Journal of Ecology-first decision
because a new outcome-independent promotion gate has now been completed. The
four-setting generality campaign was frozen before execution and explicitly
specified: all four reproductive settings had to show both a negative
fixed-assurance near–far investment contrast and a positive
evolving-minus-fixed attenuation interaction, with visitor-history bootstrap
intervals excluding zero. All four passed.

## What changed the route

The earlier manuscript had a strong but narrow result:

> in one delayed-selfing/costly setting, assurance often changes before floral
> investment, yet assurance evolution is not required for investment decline.

That temporal-order result remains useful but setting-specific. Prior selfing
does not reproduce the same assurance-first majority at the primary threshold.

The new four-setting campaign establishes a broader result:

> **Under sustained visitor-replenishment limitation, floral-investment
> divergence persists when assurance evolution is blocked, whereas allowing
> assurance to evolve consistently attenuates that divergence.**

This held in all four pre-existing reproductive settings:

| Setting | Fixed far−near investment | Evolving−fixed attenuation |
|---|---:|---:|
| Delayed control | −0.4413 [−0.4564, −0.4262] | +0.1605 [+0.1418, +0.1789] |
| Prior selfing | −0.3018 [−0.3172, −0.2866] | +0.2200 [+0.2025, +0.2383] |
| Pollen discount | −0.3305 [−0.3461, −0.3151] | +0.1915 [+0.1762, +0.2069] |
| Assurance cost | −0.4337 [−0.4501, −0.4171] | +0.1007 [+0.0842, +0.1177] |

All fixed/evolving × near/far arms had terminal occupancy 1.0, all 64 visitor
histories were eligible in every setting, and the independent zero-mutation
structural identity audit passed all 128 matched trace pairs.

Design: `data/design/chapter2_assurance_generality_20261006.json`.
Result: `data/results/chapter2_assurance_generality_20261006.json`.

## Why Ecology Letters is now first

The paper can now be centered on a general ecological/evolutionary inference
rather than on the order observed in a single reproductive cell:

1. ecological isolation changes the marginal return to floral attraction;
2. investment reduction still occurs when assurance capacity cannot evolve;
3. allowing assurance to evolve does not intensify that divergence — it
   consistently compresses it across four reproductive implementations, mainly
   by driving additional investment decline in the high-replenishment arm;
4. therefore a reduced-attraction phenotype need not be a downstream
   consequence of evolving reproductive assurance, even though assurance can
   precede it in some trajectories.

The conceptual reversal is the point: a mechanism commonly treated as a route
toward reduced attraction is, in this explicit system, not required for the
reduction and can oppose the magnitude of geographic divergence.

This is broader than the setting-specific temporal-order result and was tested
prospectively rather than selected after inspecting all four outcomes.

## What Ecology Letters must *not* be sold

The new result does not justify claiming that:

- selfing itself is absent or unnecessary;
- the attenuation interaction is a mediation fraction;
- every selfing mechanism in nature behaves this way;
- flower size, colour or a named island system is quantitatively calibrated by
  the abstract investment trait;
- the delayed/costly assurance-first temporal sequence is universal;
- natural island populations have already validated the model causally.

The claim is **cross-setting within one explicit pollination–reproduction model
class**, not empirical universality across plant lineages.

## Ecology Letters manuscript spine

The main text should be compressed around one question:

> **Is reproductive assurance required for floral-investment loss under
> pollinator limitation, and why does its evolution compress rather than amplify
> the difference between pollination environments?**

### Result 1 — upstream ecological cause

At matched plant state, low visitor replenishment collapses the outcross return
to investment. Use the corrected fixed-resident rare-mutant accounting and the
fixed-plant return decomposition. Do not use the retired whole-population
derivative as an evolutionary gradient.

### Result 2 — causal non-necessity

The original matched fixed/evolving intervention and the independent
new-history confirmation show that investment still declines when assurance
capacity is fixed.

### Result 3 — preregistered generality

Make the four-setting intervention the center of the paper. Main Figure 2 now
shows fixed-assurance non-necessity, evolving-minus-fixed attenuation, matched
near/far arm localization, and the corrected rare-mutant component mechanism.
The trajectory decomposition localizes 78–90% of attenuation to additional
near-side investment decline.

### Result 4 — temporal order as a mechanistic example, not the headline

The delayed/costly assurance-first 51/64 replication demonstrates why temporal
precedence is not causal necessity. The failed generalization to prior selfing
is useful because it prevents the paper from turning the sequence into a law.

### Result 5 — reproductive consequence

Retain the pollen-deficit versus viable-offspring mismatch as a concise
consequence of why fractional pollen limitation cannot substitute for total
reproductive return.

Move the 13-rate surface, broad reciprocal-selection atlas, deterministic/PDE
diagnostics, full-mutation history work and most natural-system source auditing
to Supporting Information.

## Journal of Ecology backup

Journal of Ecology remains the strongest backup if Ecology Letters regards the
cross-setting evidence as insufficiently external to one model class. The same
results fit a plant-ecology mechanism paper without changing any numerical or
causal claim. The backup framing should emphasize plant–pollinator
replenishment, reproductive assurance and attraction allocation rather than the
causal-inference reversal.

## Why not Nature Ecology & Evolution from this result alone

The four-setting test adds genuine internal generality but no independent
empirical transport across natural systems. A Nature Ecology & Evolution pitch
would require a stronger external biological arm, not more reframing of the
same model.

## Claim language

Preferred headline:

> **Reproductive assurance is not required for pollinator-limitation-driven
> investment reduction and can compress its geographic divergence.**

More precise manuscript sentence:

> **Across four prospectively tested reproductive settings, sustained
> visitor-replenishment limitation reduced floral investment even when
> assurance capacity was fixed, while allowing assurance to evolve consistently
> reduced the near–far investment contrast.**

Keep the temporal result separate:

> **In the delayed-selfing, assurance-cost setting, assurance often changed
> first, but this ordering did not generalize across reproductive settings.**

## Pre-submission gates

1. **DONE — evidence lock.** Four-setting design, 8,448-case result, source
   receipts, artifact digests and result-level regression tests are preserved.
2. **DONE — main visual.** Main Figure 2 now integrates non-necessity,
   attenuation, near-side localization and the corrected local-selection
   mechanism.
3. **DONE — EL manuscript surface.** The submission-focused manuscript is
   `CHAPTER2_MANUSCRIPT_ECOLOGY_LETTERS_20261006.md`; main text is ~3.2k
   words, with four figures.
4. **DONE — novelty/claim boundary.** The manuscript does not sell
   selfing-first as novel or universal, and separates the confirmed four-setting
   result from the setting-specific temporal sequence.
5. **PENDING EXTERNAL DEPENDENCY — public archive.** Deposit the
   confirmatory/generalization raw bundles in a permanent public repository and
   add DOI(s) to Data Accessibility before submission.

This journal decision follows the preregistered promotion rule; it does not
raise the scientific claim ceiling beyond the evidence above.
