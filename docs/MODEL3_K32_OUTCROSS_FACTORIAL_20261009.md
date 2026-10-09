# Model 3 K32 — interaction audit of all eight donor/routing/maternal interventions

## Question and results firewall

The preceding source-locked, one-factor-at-a-time autonomous K32
counterfactuals showed that flattening donor export, visitor routing
or maternal outcross provisioning individually accelerated assurance
high-allele frequency but had **different effects on joint diploid
genotype richness**. A logical next question is whether the THREE
perturbations *interact*, so that the full combination cannot be
predicted by adding three single-factor responses.

This is a new, explicitly exploratory 2×2×2 factorial experiment
on artificial biological mechanisms, **not a natural pollinator
manipulation or preregistered independent experiment**.

The only ecological visitor history is OLD seed 26110601, near;
canonical frozen Model3 K32, mutation0, zero adult survival or
immigration, eight annual generations and fixed, engineered 27-class
joint diploid genotype support. The source arm calls the **unchanged
canonical** reproduction and full Mendelian genetic kernel. None of
the frozen prospective confirmatory visitor histories is used.

## Eight predefined arms

Each binary factor denotes flattening a **single** component of the
currently recomputed original source-ledger outcross matrix.

| Bit | Factor | Intervention |
|---|---|---|
| E=1 | donor export | Equalize positive exported pollen amounts among active donors |
| R=2 | visitor/recipient routing | For each donor, equalize positive fractions of donor export arriving to existing recipient edges |
| M=4 | maternal seed provisioning | Equalize female viable outcross seeds per received pollen among active mothers |

All masks 0..7 are simulated autonomously: original source,
E, R, E+R, M, E+M, R+M, E+R+M. For masks 0,1,2,4, source transition
and one-factor counterfactual exactly reproduce prior implementation
with matched RNG seeds. The combined masks multiply all individually
modified factors BEFORE renormalization and **do not sequentially
renormalize** after each operation.

At every current parent state and in each arm:

- Keep selfed viable-seed intensities exactly equal to canonical
  reproduce() for those current parents.
- Normalize altered positive outcross pair weights to original
  total viable outcross seed intensity, without creating new donor
  or recipient links and without allowing within-individual
  outcross on the diagonal.
- Sample original capped-Poisson source-conditional N and full
  Mendelian offspring genotype multinomial law.
- Recompute the canonical source ledger on each arm's NEW genotype
  population in subsequent years; later demographic rates can
  diverge indirectly through genotype history.

All source and comparator paths share numerical RNG labels
(replication,year), but different genotype composition can change
RNG draws; this is not identical realized offspring coupling.

## Fully observable factorial response estimands

Use six mathematical responses defined unconditionally for all 512
demographic paths: occupancy indicator, joint diploid genotype
richness (zero if extinct), lost types among six initial alleles
(six if extinct), **occupancy-weighted high assurance frequency**,
occupancy-weighted assurance heterozygote fraction and
occupancy-weighted complete-fixation indicator. The last three are
explicit products of occupancy with a defined trait on living
populations; zero after extinction is an occupancy-weighted
*product*, **not a fabricated extinct-population trait mean**.

All arms also report mean surviving assurance high-allele frequency,
heterozygosity and fixation separately. Those conditional means have
arm-specific survivor populations and are not suitable for simple
unconditional factorial effects.

Let f(S) denote each path-specific response under the set of
flattened factors S. The exact Möbius interaction decomposition is

    I(S)=sum_{T subset S} (-1)^(|S|-|T|) f(T).

For all three E,R,M combined:

    f(ERM)-f(empty) =
       I(E)+I(R)+I(M) +
       I(ER)+I(EM)+I(RM)+I(ERM).

These are **counterfactual model interaction contrasts** across
fully specified autonomous path simulations. They are not
regression correlations and not one-step Shapley values. Each
coefficient has nested-demographic Monte Carlo standard error,
computed at its path level. Additionally calculate for EACH path

    total_nonadditivity = [f(ERM)-f(empty)]
      - [f(E)-f(empty)] - [f(R)-f(empty)] - [f(M)-f(empty)]
      = I(ER)+I(EM)+I(RM)+I(ERM).

The demographic Monte Carlo SE of this *aggregate* must be obtained
from the complete path-level contrast, rather than by treating four
correlated interaction terms as independent. A large-looking
interaction is not scientifically resolved if its MC interval overlaps
zero. The joint source visitor environment is still only one
independent ecological history.

## Why this factorial matters

- If genotype richness responds positively to R alone but
  negatively to E alone, their combination may improve or reduce
  diversity, depending on non-additive genotype-dependent feedback.
- Even where individual assurance frequency appears uniformly near
  fixation, the multilocus genotype inventory can diverge across
  combinations.
- Pairwise and three-way interactions can expose why
  **single-factor ablations should not be extrapolated additively**.
- Any interaction is evidence *inside the stated artificial
  reproductive operators*, not causal inference about real pollinator
  species, maternal resource tradeoffs or island history.

## Reproduce and stop line

```bash
pytest -q tests/test_model3_k32_outcross_factorial.py
python -m scripts.run_model3_k32_outcross_factorial --budget 8 --draws 512 --out factorial-budget8.json
python -m scripts.run_model3_k32_outcross_factorial --budget 3 --draws 512 --out factorial-budget3.json
```

The existing .github/workflows/ci.yml has a PR420-only job
model3-k32-full-factorial; confirm both executed JSON results
and mathematical identities before promoting any numerical
contrast to evidence. All reference data remain one OLD ecological
visitor history and nested demographic replicates, not natural
island observations; no SDE/SPDE or INLA acceptance is claimed.
