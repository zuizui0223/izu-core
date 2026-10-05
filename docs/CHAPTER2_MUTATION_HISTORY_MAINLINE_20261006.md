# Chapter 2 mutation-history mainline — 2026-10-06

## Decision

The paper is now organized around the completed full-mutation common-environment
experiment rather than around the five-question maintained-isolation process
decomposition.

The ecological question is:

> **After pollinator environments become identical, what does it mean when evolved
> floral differences persist?**

The central distinction is not whether history can leave a residual difference.
That is already known in evolutionary biology. The contribution is that the same
phenotypic memory can correspond to different evolutionary states.

> **Evolutionary memory is not equivalent to evolutionary arrest.**

In Model 3, past visitor-isolation histories are imposed for 200 reproductive
updates and then both arms receive exactly the same visitor environment for the
next 800 updates. All three plant traits can evolve. Mutation is crossed at
0 versus 0.01 per transmitted allele, and the two declared reproductive settings
are retained as separate model conditions.

## Primary result

At update 1000, after 800 updates of identical current visitor exposure, the
far-history minus near-history contrasts remain nonzero for investment and
reproductive assurance.

| Reproductive setting | Mutation | Investment difference | Assurance difference |
|---|---:|---:|---:|
| delayed selfing, assurance cost 0.5 | 0 | -0.140408 | +0.034050 |
| delayed selfing, assurance cost 0.5 | 0.01 | -0.130106 | +0.055755 |
| prior selfing, assurance cost 0 | 0 | -0.030532 | +0.003515 |
| prior selfing, assurance cost 0 | 0.01 | -0.016545 | +0.001444 |

The corresponding descriptive history-cluster bootstrap intervals are reported
in `MODEL3_FULL_MUTATION_RESULTS_20261004.md` and remain the source of truth.

Terminal access-position intervals include zero in all four groups, so the
history effect is trait-specific rather than a uniform three-trait syndrome.

## Why this is not merely "history matters"

The zero- and positive-mutation populations can show persistent history
contrasts while occupying different dynamical states.

### No mutation: memory with genetic arrest

Occupied zero-mutation populations retain one investment allele and their
mean investment change over the final 100 updates is zero. Under these model
conditions, historical divergence can persist because alternative alleles have
been lost and no new variation is introduced.

### Positive mutation: memory during continuing evolution

With mutation, multiple investment alleles remain or are replenished:
approximately 6.63/6.44 near/far alleles in the delayed setting and
5.43/5.38 in the prior setting. The positive-mutation populations are still
changing over the final 100 updates. Therefore a residual history contrast at
the same endpoint does **not** imply evolutionary arrest or an alternative
stable state.

This is the paper's main conceptual result:

> **A persistent phenotypic difference after ecological equalization is not a
> diagnostic of a trapped evolutionary state. History can remain visible while
> evolution continues.**

## What mutation does and does not establish

Mutation replenishes variation and permits continued movement beyond the
founder support, but the present experiment does not establish that mutation
eliminates historical memory on a longer horizon. Nor does it establish that
mutation significantly changes the magnitude of the history contrast relative
to zero mutation.

The full positive-mutation deterministic/PDE comparison is numerically
unresolved. The 9-to-13 grid gate fails in 31/32 positive-mutation cases, and
the high-resolution 1000-update comparison was stopped after verified update 7.
This numerical branch remains closed unresolved and is not needed for the
finite-ABM ecological claim.

Accordingly, the paper must not claim:

- irreversible evolution;
- alternative stable attractors;
- a universal recovery time;
- mutation-independent memory;
- an ABM-minus-converged-continuum finite-population effect;
- a field-calibrated island restoration trajectory.

## Novelty boundary

"Pollinator restoration need not restore the ancestral phenotype" is not a
standalone novelty claim. Existing work already addresses historical
contingency, genetic variation loss after pollinator removal, and theoretical
failure of reversal after pollinator restoration.

The narrower contribution is:

1. three inherited plant traits are allowed to evolve jointly under an explicit
   plant-pollinator reproductive process;
2. the ecological environment is exactly equalized after a controlled history;
3. mutation is manipulated directly, rather than assuming that standing
   variation is permanently absent;
4. the endpoint history contrast is interpreted together with allele
   availability and ongoing trait change;
5. this separates **memory**, **arrest**, and **continued recovery** as different
   biological states that can look similar in a cross-sectional endpoint.

The closest empirical motivation is Busch et al. (2022), where pollinator loss
increased selfing and reduced genomic variation. The present model asks the next
question: after the environment is restored, does a remaining trait difference
mean the population is genetically trapped? The answer in this model is no.

## Paper-level causal chain

```text
different visitor-isolation histories
              ↓
different reproductive selection and inherited states
              ↓
      ecological environments equalized
              ↓
      do trait differences disappear?
              |
       yes / no endpoint
              ↓
if no: inspect genetic state and ongoing change
        /                         \
no mutation                     mutation
allelic support collapses       variation is replenished
late change = 0                 late change continues
        \                         /
         persistent endpoint difference
                      ↓
    memory does not identify arrest
```

## Role of the maintained-isolation process experiments

The 2026-10-05 process decomposition is retained as mechanism support, not as
the paper spine.

It answers why the historical divergence is biologically plausible:

- isolation changes visitor replenishment and outcross returns;
- investment selection can become less favourable;
- reproductive assurance can change earlier than investment;
- investment decline does not require assurance evolution;
- lower pollen deficit need not mean greater viable offspring.

These results move to the mechanistic explanation section after the main
common-environment result. They no longer define five co-equal paper questions.

## Result hierarchy

### Main Figure 1 — history creation and environmental equalization

Show the 200-update near/far history phase followed by 800 updates of the exact
same visitor snapshots. Plot investment and assurance trajectories for the four
setting × mutation groups with history-level summaries.

### Main Figure 2 — memory is trait-specific and setting-dependent

Show terminal far-minus-near contrasts for access, investment and assurance.
Access remains compatible with zero while investment and assurance retain
history in the focal delayed/costly setting.

### Main Figure 3 — the same memory can mean arrest or continued recovery

Pair endpoint differences with genetic-state diagnostics:

- zero mutation: one retained investment allele, final-100-update change zero;
- positive mutation: multiple alleles, continuing final-100-update change.

This is the conceptual centre of the paper.

### Main Figure 4 — why history was generated

Use only the strongest maintained-isolation mechanism results:

- fixed-plant return contrast;
- fixed versus evolving assurance intervention;
- pollen-deficit versus viable-offspring contrast.

Do not let replenishment gradients or five-question process architecture
overtake the common-environment result.

### Supporting Information

Move the following to SI or bounded mathematical support:

- full 13-rate process surface;
- local selection inequalities and 900-cell verification;
- reciprocal-selection parameter grid;
- finite versus deterministic bridge;
- one-locus mutation diagnostic;
- failed positive-mutation grid/PDE convergence campaign;
- natural-island confrontation ledger;
- all stopped high-resolution numerical receipts.

## Manuscript claim

Preferred one-sentence claim:

> **Past pollinator isolation can remain visible after current pollinator
> environments are equalized, but the persistence of a floral difference does
> not reveal whether evolution has stopped: without mutation the model can be
> genetically arrested, whereas with mutational replenishment comparable
> historical memory persists while evolution continues.**

Short title candidate:

> **Evolutionary memory after pollinator isolation does not imply evolutionary arrest**

More island-forward title candidate:

> **Island pollinator history can outlast the environment without halting floral evolution**

## Empirical prediction

The main falsifiable prediction is not simply that restored populations remain
different. It is:

> Among populations with similar present pollinator environments and similar
> residual floral divergence, recovery dynamics should differ according to
> available genetic variation. Populations with depleted adaptive variation
> should show little short-term inherited movement, whereas populations with
> replenished or retained variation can continue moving despite an equally
> persistent historical phenotype gap.

This prediction requires longitudinal or resurrection/common-garden genetic
data; current natural-island evidence does not test it directly.

## Routing decision

This file is the controlling scientific narrative for the branch
`codex/model3-full-mutation-closeout-20261004`.

`CHAPTER2_PROCESS_MAINLINE_20261005.md` becomes mechanism-support provenance.
`MODEL3_FULL_MUTATION_RESULTS_20261004.md` remains the primary numerical
source. No numerical result is changed by this routing decision.
