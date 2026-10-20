# Secondary colonisation: bounded exploratory readout (2026-10-20)

## Execution and provenance

- Run: https://github.com/zuizui0223/izu-core/actions/runs/39366132489
- Exact source workflow head at run: 5861aea81c14ae9ab3f2d0da88b4a58cdfd7f7ef
- Frozen experiment design: CHAPTER2_SECONDARY_COLONIZATION_PILOT_20261020.md
- All four crossed founder x visitor source blocks ran to completion. There were
  five pre-declared genetic sources per block, three recipient environments,
  two prescribed distances, and two nested future streams: **240 complete
  biological futures**, each 20 reproductive updates.
- Experiment-specific scientific and numerical invariant tests passed.
- The original complete JSON and checksums were uploaded as the Actions
  artifact named secondary-colonisation-exploratory (retention 90 days).
- These findings were obtained from the workflow-generated source and output,
  NOT from the independent 160x160 registered G/S confirmation; no latter
  result was overwritten or promoted.

## Explicitly descriptive results (NOT inferential)

Endpoint: any allele of the three **selected source loci M/I/A** survives
in the destination at the 20th census. This means ancestry persistence,
NOT necessarily separate colonist-population establishment.
Denominator per row: eight nested futures from only four crossed-source
backgrounds; no IID tests or confidence intervals.

| Source history | Island-like vacant, d=1.5 | Mainland-like vacant, d=1.5 | Mainland-like resident, d=1.5 |
|---|---:|---:|---:|
| Ancestral, t0 | 4/8 | 7/8 | 2/8 |
| Island fixed A, t10 | 5/8 | 7/8 | 2/8 |
| Island evolving A, t10 | 6/8 | 7/8 | 4/8 |
| Island fixed A, t25 | 5/8 | 7/8 | 2/8 |
| Island evolving A, t25 | 6/8 | 8/8 | 4/8 |

The nonzero distance condition imposes a seed arrival and establishment
probability of 0.8*exp(-1.5), applied independently per produced seed.
In the mainland-like resident destination, a colonisation cohort arrived in
6/8 futures for each of the five source histories, but source-locus
ancestry persisted in only 2/8 or 4/8. The total resident recipient
population remained occupied in 8/8 futures for every source history.
Thus overall occupancy is **not a valid substitute** for migrant ancestry
survival. The discrepancy is a model-design demonstrator, not new natural
evidence of counter-colonisation.

At distance zero, source-locus ancestry in mainland-like resident
destinations persisted in 8/8 from ancestral, t10-fixed and t10-evolving
sources, and 7/8 for both t25 histories. In the mainland-like vacant
destination at distance zero, all five histories persisted in 8/8.
Consequently the apparent evolving-A advantage at the far resident
destination is contingent on recipient occupancy and the imposed arrival
kernel; it is not a universal historical treatment effect.

At the island-like vacant recipient at distance zero, both t10 historical
arms retained ancestry in 8/8; at t25 the fixed-A arm retained it in 6/8
versus 8/8 for evolving A. This is exploratory and could reflect source
genetic differences, demographic variation or finite sampling.

## Inference boundaries and falsification

The observed 2/8 vs 4/8 difference must **not** be called significant,
causal mediation by A, demonstrated evolutionary rescue, or a biological
rate of natural island-to-mainland reinvasion. At historical departure the
M, I and A genotype distributions can all differ; no module swap was made.
Historical fixed A still permits selfing; destination A is evolving for all.
Seed creation was performed under a common six-visitor source context and
resident genotypes are artificial. There is no explicit real geography,
repeated immigration, neutral ancestry, standing resident evolutionary
history, or environmental dispersal data.

The full trajectory archive contains source-I bounds, per-census
allele-marker counts and context-specific genetic return diagnostics.
Their descriptive sign and magnitude were not independently extracted
and adjudicated in this summary. Therefore the central **adaptation vs
establishment** contrast and the genetic mediation mechanism are still
unresolved: the pilot directly demonstrates the ability to separate
arrival, trait-locus persistence and recipient occupancy, and suggests
specific contrasts for a future preregistered design.

## Follow-up scientific gate

Before enlarging N, hold source genotypes constant while changing expressed
A and, separately, equalize inherited M/I/A modules to identify direct
assurance versus downstream genetic legacy. Use destination competitor
controls and a neutral lineage marker before calling trait-allele introgression
colonisation success. Report destination fitness in a common assay without
conditioning exclusively on survivors. Include both vacant and occupied
mainland-like recipients, and do not select whichever source history gave
a favourable preliminary difference. A new independent powered cohort and
independent biological replay are required for confirmatory statements.

Operational note: the new Actions workflow was initially run on PR triggers.
The repository-wide scientific gate correctly rejected that trigger policy.
The workflow trigger was subsequently restricted to manual workflow_dispatch;
the above archived exploratory numerical result precedes that CI-policy repair.
This operational correction does not alter the scientific model/seed allocation.
