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


## Source-locked 512-path numerical results

Dedicated CI source-run [#37896524806](https://github.com/zuizui0223/izu-core/actions/runs/37896524806)
completed successfully on source commit
`9ebd6cb34235824b0e110a324d8774f9a2473f74`.
The [raw two-case JSON archive, artifact 11600821192](https://github.com/zuizui0223/izu-core/actions/runs/37896524806/artifacts/11600821192)
is source locked with SHA256
`29e3c4342b9e588df16e8ba081762728871f792dc1121d70ef5ce087f310708c`.
Permanent compact receipt:
`data/results/model3_k32_outcross_factorial_20261009.json`.
Both biological provenance and the exact 2×2×2 Möbius identities passed CI.

### Eight-generation all-three intervention versus unchanged Model3

| Metric | Budget 8 original | Budget 8 all three | Budget 3 original | Budget 3 all three |
|---|---:|---:|---:|---:|
| Surviving paths out of 512 | 512 | 512 | 505 | 507 |
| Mean assurance high-allele frequency given survival | 0.97861 | **0.99521** | 0.98403 | **0.99646** |
| Mean assurance heterozygote fraction given survival | 0.01898 | **0.00323** | 0.01193 | **0.00173** |
| High-allele complete fixation fraction given survival | 0.63086 | **0.87305** | 0.80000 | **0.94477** |
| Unconditional joint genotype richness | 4.32422 | 4.04102 | 3.11523 | 3.10938 |
| Unconditional ancestral allele types lost | 0.82617 | **1.18750** | 1.39648 | **1.63281** |

**Key distinction:** the combined intervention advances assurance-high
allele fixation and founder-allele-type disappearance, yet in the
resource-stress case retains approximately the same COUNT of occupied
joint diploid genotype classes. Genotype richness and retained allelic
types are not synonyms. The mechanism cannot be interpreted as new
allele generation: mutation and immigration are zero.

### Additivity and its Monte Carlo precision

The following signed numbers are all-three-minus-original factorial
effects, or aggregate pairwise-plus-three-way interaction contrasts.
Each ± is one nested-demographic Monte Carlo standard error, computed
from the COMPLETE per-path paired contrast rather than summing
component SEs. They are NOT independent environment confidence
intervals.

| Factorial response | Budget 8 | Budget 3 |
|---|---:|---:|
| All-three joint genotype richness effect | -0.28320 ± 0.07587 | -0.00586 ± 0.06296 |
| Sum of three individual richness effects | -0.50781 | -0.10547 |
| **Aggregate richness non-additivity** | **+0.22461 ± 0.13270** | **+0.09961 ± 0.11975** |
| All-three occupancy-weighted assurance frequency effect | +0.01660 ± 0.00181 | +0.01616 ± 0.00612 |
| **Aggregate assurance frequency non-additivity** | **-0.00958 ± 0.00315** | -0.00560 ± 0.01217 |
| All-three occupancy-weighted heterozygosity effect | -0.01575 ± 0.00171 | -0.01005 ± 0.00167 |
| Sum of three individual heterozygosity effects | -0.02612 | -0.01899 |
| **Aggregate heterozygosity non-additivity** | **+0.01038 ± 0.00322** | **+0.00894 ± 0.00348** |
| All-three unconditional allele-types-lost effect | +0.36133 ± 0.03432 | +0.23633 ± 0.04093 |
| Aggregate allele-loss non-additivity | -0.08594 ± 0.05807 | -0.05078 ± 0.08541 |

The positive aggregate heterozygosity interaction at BOTH budgets
means three separate heterozygosity-reducing interventions are not
additively interchangeable. Their individual effects sum to a
greater reduction than the actual combined effect. This is
consistent with bounded-frequency saturation and genotype-dependent
feedback, but neither is uniquely isolated as a causal mechanism.

The positive **richness** aggregate non-additivity is LESS
precisely identified: its MC SE is too large to certify a stable
interaction difference in either budget. It would be misleading to
turn a visible numerical nonadditivity into a robust ecological
interaction claim. Similarly, the three-way single coefficient itself
has limited precision, and the design generated multiple candidate
endpoints after the earlier source outcomes were seen.

### Biological and statistical caveats

All eight arms are deliberately altered mating-weight counterfactuals,
not eight independent natural histories. All paths use one archived
near visitor environment 26110601 and artificial founders; random
numbers differ by arm after genotype paths diverge. Total viable
outcross seed intensity and selfed viable seed intensities are
held constant conditional on the SAME arm's CURRENT parent state,
but later parent genotype distributions can change subsequent
fitness and recruitment. Extinction-conditioned allele means are
reported separately from factorial occupancy-weighted products.
The experiment cannot establish natural pollinator fitness, causal
selection, island comparison, or a validated full SDE/SPDE. Keep
PR #420 Draft until newest broad CI and Chapter 2 gate succeed.


## Allelic combinatorial capacity versus actual genotype occupancy

The first source-locked eight-arm experiment showed that at budget3,
the all-three intervention loses **more initial allele types** but has
almost unchanged **joint diploid genotype class richness**. This new
follow-up distinguishes why those apparently conflicting diversity
outcomes can coexist.

For each nonextinct current population with a fixed diploid genotype
grid of 3 unlinked biallelic loci and zero mutation/immigration:

- Count the number of **polymorphic loci** (0..3) that still have BOTH
  initial founder alleles.
- Define a *purely combinatorial upper bound* on the number of possible
  distinct unordered diploid joint genotype types as `P=3^m`,
  where `m` is the number of polymorphic loci. Monomorphic loci allow
  only one diploid allele-pair type. This is an upper bound given
  allele content, **not a prediction that all P types can be formed in
  a single generation under the real source pollen graph**.
- Let `R` be actual occupied joint genotype class richness,
  `1<=R<=min(P,N)` for a living finite population.
  The genotype support coverage is `C=R/P`, which captures
  how many of the mathematically possible classes are actually
  represented. Even coverage C=1 at P=1 can mean a single fixed
  genotype: **high coverage is not high absolute diversity**.
- Compute Shannon effective genotype number
  `exp(-sum p_g log(p_g))` and inverse-Simpson effective number
  `1/sum p_g^2` from actual population genotype frequencies.
  Both are bounded by realized class richness and expose dominance
  of common genotypes despite stable raw class counts.

There is an **exact per-living-population identity**

```text
ln R = ln P + ln(R/P) = ln(3) * m + ln C.
```

The factorial also evaluates occupancy-weighted products of each
log, so the additivity remains algebraically exact without inventing
log genotype richness for extinct populations. For extinction the
occupancy-weighted product is 0, while alive-only population means
are also recorded. Both the source and the seven counterfactual
arms are simulated with their previous, unchanged random
streams; donor export, routing and maternal pairing interventions
are not redefined for this diagnostic.

**Inference caution:** an increase in coverage C after allele loss
does not mean biological compensation or adaptive maintenance by
itself. C's denominator P has fallen by a factor of three whenever
a biallelic founder locus becomes fixed. Diversity number and
evenness need to be examined together to determine whether a
real additional genotype-diversification process exists. The
state-wise identity does not causally distinguish segregation,
recombination, selection and drift.

The existing PR420-only full factorial CI now checks, for all eight
arms and seven Möbius contrasts, both the complete source
provenance and the exact log-genotype-richness decomposition,
as well as occupancy, six ancestral allele types and effective
genotype diversities. No new ecological visitor histories,
mutation, immigration or natural plant observations are used.

**New numerical results are not admitted until the source-commit
CI run succeeds and its raw artifact is inspected.**


## Validated allelic-ceiling versus realized-genotype result

This follow-up successfully ran all eight autonomous old-history
K32 arms with allele combination-capacity and genotype evenness
accounting. The source-bound [GitHub Actions run #37900326737](https://github.com/zuizui0223/izu-core/actions/runs/37900326737),
`model3-k32-full-factorial` job **PASS**, used source SHA
`2164eac18143d34d996a81c4b3a94c8dfedeceae`.
[Executed raw two-budget artifact #11602765416](https://github.com/zuizui0223/izu-core/actions/runs/37900326737/artifacts/11602765416),
SHA256 `1452ea59c4d70723cc4c1aeb74236aee080759b0c2485ef1aafb85b091edeceb`.
Permanent compact result: `data/results/model3_k32_genetic_structure_factorial_20261009.json`.

### Why class richness hides genetic erosion

| Year-8 statistic | Budget8 original | Budget8 all three | Budget3 original | Budget3 all three |
|---|---:|---:|---:|---:|
| Surviving paths | 512 | 512 | 505 | 507 |
| Average loci retaining both founder alleles, alive | 2.174 | 1.813 | 1.667 | 1.410 |
| Average combinatorial upper bound P among survivors | 14.05 | **9.07** | 9.29 | **6.16** |
| Actual multilocus genotype class richness, all paths | 4.324 | 4.041 | 3.115 | 3.109 |
| Fraction of combinatorial genotypes actually occupied, alive | 0.419 | **0.568** | 0.520 | **0.653** |
| Shannon effective genotype count, alive | 2.915 | **2.649** | 2.341 | **2.238** |
| Simpson effective genotype count, alive | 2.435 | **2.213** | 2.048 | **1.936** |

At budget3, the all-three counterfactual reduces the average
**combinatorial upper bound** on available diploid genotype types
by approximately 3.12 classes among surviving populations,
but the realized genotype richness changes by only -0.006 classes
unconditionally. The proportion of potential types actually occupied
rises by ~0.133 among survivors. Consequently, **the apparent
maintenance of raw genotype-class richness does not imply
maintenance of allelic variation or genotype frequency evenness**.

The combinatorial upper bound can fall mechanically when one
locus loses an allele. Coverage C=R/P can then increase even if
R stays flat, simply because the denominator P shrinks. Coverage
increases are therefore NOT in themselves evidence of
compensatory adaptation, recombinational rescue, or restoration
of lost alleles. The unchanged source and altered counterfactuals
all have mutation=0 and immigration=0.

### Pathwise log decomposition and demographic MC precision

The `log genotype richness = log combinatorial upper bound +
log genotype coverage` equation was verified for every living
population and every factorial contrast. For mortality, the
factorial uses occupancy-weighted products, rather than
assigning a log genotype count to extinction.

| All-three-minus-original (occupancy weighted) | Budget8 mean ± MC SE | Budget3 mean ± MC SE |
|---|---:|---:|
| log genotype class richness | -0.06797 ± 0.01839 | +0.00631 ± 0.01965 |
| log combinatorial upper bound | **-0.39696 ± 0.03770** | **-0.27251 ± 0.03851** |
| log realized genotype coverage | **+0.32899 ± 0.02898** | **+0.27881 ± 0.02687** |
| Simpson effective genotype count | **-0.22190 ± 0.03091** | **-0.10287 ± 0.03348** |
| Shannon effective genotype count | -0.26524 ± 0.04035 | -0.09360 ± 0.04011 |

The positive log-coverage component offsets most of the declining
log-upper-bound component, particularly at budget3 where their sum
is close to zero. Separately, the decrease in Shannon/Simpson
effective genotype diversity shows that the relative distribution
across represented classes becomes more concentrated despite
the nearly unchanged raw number of classes.

These are measurements of the fixed-source synthetic Model3
full-factorial trajectories and exact algebraic identities.
They **cannot** identify a unique biological mechanism causing
the occupancy change; selection, finite drift, repeated Mendelian
segregation, mating bias, and extinction may all contribute to
population state distributions. There is still just ONE historical
visitor environment (26110601, near) and no independent island
field measurements or use of future confirmatory visitor histories.
This does not validate a full continuous-time SDE/SPDE.
