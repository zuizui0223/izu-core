# K32 late parent-state matching direction: locus reassignment controls

## What is actually tested

A source-locked 8×8 crossover identified that around 82–85% of the
two-order early-to-late change of Model3 matching high-allele expected
reproductive direction was attributable to the evolved **parent
genotype/census state**, not the year-specific visitor snapshot.
That parent-state term is composite and is NOT the isolated influence
of increased reproductive assurance. The year8 original matching
expected allele shift was positive under the late visitor snapshot,
but near zero or slightly negative under the original year1 visitor
condition in budget8.

We now test a deliberately synthetic *one-locus genetic reassignment*,
holding all other genetic loci, parent identities and census fixed.
Original Model3 reproduce(), pollen mating weights and Mendelian
transmission are **unchanged biological source functions**; edited
parent genotypes are external hypothetical inputs, never output
by the frozen source transition.

## Parent source and visitor controls

Use original source parent counts at the START of reproduction year8:
K32, mutation0, adult survival0, seed immigration0, Chapter2
prior_selfing, engineered four-founder/27-genotype diploid initial
support. Evolve the source using ONLY archived near visitor history
26110601 for source years1–7 and the same 512 nested demographic
random-number streams as the earlier factorial/8×8 source studies.
Source populations extinct by year8 parent start are **excluded**,
not assigned a fictitious allele frequency or genotype.

For each surviving original parent population, compare two archived
visitor snapshots from THE SAME old history: year1 and year8. For
every hypothetically edited parent state, use the SAME edited
genotypes in both visitor comparisons, so visitor differences do
not reflect a second reassignment RNG draw.

## Two explicit artificial genotype controls, one locus at a time

We use each of the three source diploid loci (pollinator matching,
floral investment, reproductive assurance), separately. No source
Model3 allele values outside 0.25 and 0.75 are created.

**1. Full-diplotype shuffle, preserved locus marginals.** Shuffle
the complete two-allele genotype of exactly one locus among current
individuals. Maintain the parent census, all three locus-specific
diploid genotype frequency marginals, and every other individual's
two unedited loci exactly. Reassignment changes **the association
of loci within parents**, not the frequency or heterozygosity
marginal of any locus. It can affect source reproduction, however,
because mating success and investment/assurance depend on traits
combined within individuals. For a completely fixed locus, shuffle
does nothing, and this is checked rather than replacing a lost allele.

**2. Founder diplotype-distribution reset plus random assignment.**
Set the changed locus's homozygote/heterozygote genotype counts to
the fixed artificial founder's empirical per-locus genotype
distribution, scaled to the current parent census with
Hamilton largest-remainder allocation, then randomly assign
the pairs among existing individuals. The initial founder assurance
high-allele frequency is exactly 0.5, versus near fixation at
the original late source parents. This operation changes allele
frequency, heterozygosity and genotype associations **together**,
and may *reintroduce alleles that the source path already lost*.
Such reintroduction is explicitly not a possible event in the
original mutation=0/immigration=0 process: this is a counterfactual
input, not biological restoration, recurrent mutation or a
demonstrated evolutionary mechanism.

Use four deterministic independent reassignment permutations per
original demographic path and genetic-locus variant. Average
over reassignment replicates INSIDE each path, then estimate
nested demographic-path Monte Carlo SE across original source
replicate identities. These do not represent independent visitor
environments, islands or genetic experiments in nature.

## Report and limits

For six specific controls (shuffle/reset each of three loci),
report across the retained original source year8 parental paths:

- Expected original source matching/investment/assurance next-allele
  direction under original year1 visitors and year8 visitors.
- The same three expected directions for the synthetic edited
  parent under each visitor condition, original source rule unchanged.
- Edited minus original one-step expected direction under both
  visitor snapshots, and interaction with visitor replacement.
- Exact per-locus parent high-allele-frequency marginal changes:
  zero for all shuffled controls; only the single selected locus
  may change under a founder diplotype reset.
- For each locus, founder-reset minus full-diplotype-shuffle
  contrast: an **order/baseline-dependent** sensitivity which is
  NOT the isolated effect of an allele's marginal frequency mean.

**Important limits:** This cannot identify the fraction of the
8×8 source-parent-state contribution "caused by reassurance",
or the effect of a specific pollinator selection trait in
nature. Parent genetic edits alter several joint source mating
features, and genotype reassignment breaks existing interlocus
associations. The founder reset's forced allele revival violates
the source's no-mutation evolutionary state space, though every
hypothetically edited genotype is from the pre-existing
27-class representation.

The per-locus shuffles control existing allele marginals
but may also shift mating patterns, so their contrast is a
sensitivity to genetic association rather than a unique
causal selection component. Neither genetic rearrangement
reproduces a historical genotype evolution path. They
are one-step comparisons only, not autonomous eight-year
population trajectories and not experimental evidence
of viable plant gene editing.

## Executable and acceptance criteria

    pytest -q tests/test_model3_k32_locus_reassignment.py
    python -m scripts.audit_model3_k32_locus_reassignment --budget 8 --draws 512 --permutations 4 --out locus-reassignment-budget8.json
    python -m scripts.audit_model3_k32_locus_reassignment --budget 3 --draws 512 --permutations 4 --out locus-reassignment-budget3.json

PR420's existing core CI has a source-locked dedicated
model3-k32-locus-reassignment job verifying all six controls,
original-source biology and zero-marginal-change shuffle
invariants. **No numerical conclusions are accepted before
the source CI and the archived raw JSON have been checked.**


## Validated original source run: locus reassignment

The source-locked `model3-k32-locus-reassignment` job
**PASSED** in [GitHub Actions 37918381568](https://github.com/zuizui0223/izu-core/actions/runs/37918381568),
using source commit `a01425b31cecdc608d6805c03d9da5d6eaa295a7`.
Both budget8 and budget3 source simulations, the original
source reproduction regression tests, and the strict one-locus
marginal preservation guards passed. The
[full two-budget raw result artifact 11610733074](https://github.com/zuizui0223/izu-core/actions/runs/37918381568/artifacts/11610733074)
has SHA256
`c366c7b478209f46df346007f6cedeaea4a7ba669f2afc49915d2f66dba5e9c6`.
Permanent compact source-lock:
`data/results/model3_k32_locus_reassignment_20261009.json`.

### Matching locus direction at the original late parent state

Every row is the expected NEXT matching-high allele-frequency
shift under the original Model3 reproduction rule. Artificially
edited parent genotypes are evaluated with the exact same late
visitor snapshot as the unchanged source; this does not
simulate a new eight-year evolutionary trajectory.

| Parent input | Budget8 matching direction | Budget3 matching direction |
|---|---:|---:|
| **Unchanged late source parents** | **+0.005533** | **+0.006607** |
| Shuffle assurance complete diploid genotypes among individuals (allele/diplotype marginal preserved) | +0.002689 | +0.004159 |
| **Reset assurance to founder diploid-genotype distribution (assurance p≈0.5)** | **-0.005896** | **-0.001742** |
| Shuffle investment complete diploid genotypes among individuals (all marginals preserved) | -0.000183 | +0.000989 |
| Reset investment to founder genotype distribution (investment p≈0.5) | -0.001065 | +0.000233 |
| Shuffle matching complete diploid genotypes among individuals (all marginals preserved) | -0.003461 | -0.001492 |
| Reset matching to founder genotype distribution (matching p≈0.5) | -0.002341 | -0.001591 |

Late original source populations had 512 budget8 and
506 budget3 surviving parental states at the start of year8.
There were four independently randomized genetic-diplotype
assignments INSIDE each original source demographic path
and per artificial genetic control. The same edited parents
were evaluated under BOTH archived year1 and year8 visitor
snapshots. The original source only evolved through
canonical years1–7.

**Compared with the unchanged original source**, assurance
diplotype shuffling under late visitors reduced the matching-high
expected reproductive shift by **-0.002844 (MC SE 0.000422)**
budget8, and **-0.002448 (SE 0.000881)** budget3.
These effects do not change the allele frequency OR
heterozygote frequency marginal of ANY of the three loci.
They are therefore a within-model sensitivity to the
alignment of assurance diplotypes with matching/investment
genotypes in the same individual.

Replacing the assurance diplotype distribution with
the founder distribution additionally changed mean assurance
high allele frequency by **-0.4664 budget8** and
**-0.4816 budget3**, to its founder value near 0.5.
It made the matching allele direction negative under
late visitors: -0.005896 and -0.001742.
The reset-minus-assurance-shuffle difference in matching
direction was **-0.008585 ±0.000661 MC SE** (budget8)
and **-0.005901 ±0.000797** (budget3). This isolates a
declared *genetic-distribution reset contrast after
randomization*, but does NOT separately identify the
effect of mean assurance high-allele frequency from
heterozygosity and altered individual-level genotype
pairing. Reset can reintroduce long-lost alleles by
artificial editing, a source-evolution impossibility
with mutation=immigration=0.

### Matching and investment genetic background matter too

Exact within-locus marginal-preserving shuffles of
**matching** genotypes produced expected late direction
-0.003461 budget8 and -0.001492 budget3.
**Investment** shuffles produced -0.000183 budget8
and +0.000989 budget3, both below the original.
The response is not specific to the assurance locus;
joint individual genotype composition and interacting
trait-dependent mating weights must be considered.

**What this does and does not explain:**
The assurance-high-diplotype distribution AND its pairing
with other encoded traits matter for late matching-high
reproductive direction in the old-source synthetic Model3.
However, the interventions include artificial reassignment,
genotype-association disruption and potentially resurrected
founder alleles. They do NOT establish that assured selfing
alone caused the historical direction reversal, that
natural recombination produces these edits, or that
individual pollinators impose the measured allele
directions in field populations. Original source biological
code is not modified, there is just one archived visitor
environment, and none of the frozen prospective
confirmatory visitor histories was accessed.
