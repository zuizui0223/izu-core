# Central question and repeatability: evidence boundaries

User priority,2026-10-19: explain **what pollinator reduction does to plants**.
Variation among islands is a possible consequence, not the primary explanandum.
First audit repeatability under pollination reduction; new-environment transfer
is a later component of the same question, not a reason to expand the project.
No new biological simulation is authorized or reported by this document.

## Working hypothesis, not a predetermined trait ranking

Pollinator reduction changes the reproductive returns on assurance A and floral
investment I through distinct mechanisms. Investment decline need not require
assurance evolution. Which response occurs first, its realized magnitude and
its reversibility depend on selection, inherited variation and finite population
processes. Test which aspects repeat under identical conditions rather than
declaring A deterministic and I stochastic in advance.

Private benefits do not prove deterministic evolution; nonzero costs, mating
timing and inbreeding depression affect A selection. Shared benefits do not by
themselves prove weak I selection. Include maternal and paternal outcross returns
and viable selfing. A capacity is not the realized selfing fraction, and fixed
A does not mean absence of selfing.

## Corrections to the proposed narrative

| Proposed statement | Supported reading and boundary |
|---|---|
| Investment selection is negative in 128/128 histories | The archived manuscript reports a near-to-far shift toward lower investment in all128 histories. A negative difference of gradients is not a negative absolute gradient or a negative realized change in every trajectory. |
| Price closure makes the next mean deterministic | Exact closure verifies the accounting/conditional calculation. It is not evidence that stochastic offspring means or future trajectories have zero variance. |
| 49% is the prediction ceiling | 1,117/2,304=48.48% is a post-outcome, in-sample majority-label bound under18 specified starting-state groups. It is not a universal or out-of-sample prediction limit. |
| A is more deterministic than I | A comparative hypothesis still requiring matched endpoints, horizons and starting variation; mean shifts or access-event frequencies alone do not establish the ranking. |
| Direction is deterministic; timing and order are random | These are separate aspects to estimate. Broadly shared expected directions can coexist with realized sign reversals; timing can itself have predictable environmental structure. |
| Function repeats across islands but morphology does not | A proposed connection to Chapter1, not a result established by the present model or an identification of natural island assembly. |

Sources checked in the current repository:

- [Four-question audit](CHAPTER2_CENTRAL_FOUR_QUESTION_AUDIT_20261014.md):
  precise 48.48% definition and its claim ceiling.
- [Archived repeatability manuscript](CHAPTER2_MANUSCRIPT_EL_REPEATABILITY_20261003.md):
  relative near/far selection shifts, multivariate Price closure and finite
  realization differences. Use its underlying source artifacts for any new
  quantitative reanalysis; this wording check is not a fresh raw replay.
- [Selection and realization frame](CHAPTER2_SELECTION_REALIZATION_FRAME_20261019.md):
  cost dependence, full reproductive contributions and limits of deterministic
  genotype-density approximations.

## Existing repeatability evidence must be used before adding runs

The [history/demography audit](CHAPTER2_HISTORY_DEMOGRAPHY_REPEATABILITY_AUDIT_20261003.md)
and [its machine-readable result](../data/results/chapter2_history_demography_repeatability_audit_20261003.json)
already analyze128 histories, three starting I states and eight demographic
repeats. Their endpoint is paired far-minus-near terminal-minus-initial I.
The analysis was post hoc, not preregistered. The saved result gives:

| Condition | Single-trajectory structured ICC | Reliability of eight-repeat history mean |
|---|---:|---:|
| Natural | 0.170071 | 0.621123 |
| Capacity192 | 0.370 (rounded in audit) | 0.825 (rounded in audit) |
| Visitor pooled | 0.014 (rounded in audit) | 0.103 (rounded in audit) |

These describe the environmental-history signal in I, not a fraction of evolution
caused by drift or a comparison with A. Uniform signs can arise either because
demographic variation falls or because an environmental-history contrast is
removed. Do not infer the same mechanism from the same categorical sign count.

Next, inspect whether the original stored repeat tensors contain A and I from
the same runs and with comparable definitions. Reuse adequate records before
proposing any new same-condition or capacity simulation. A formal claim about
comparative predictability needs a prospective estimand or clearly labeled
post-outcome analysis; no favorable reanalysis is promoted to confirmation.

Readback completed: the bridge and its capacity comparison fixed expressed A=.5,
so their apparent A invariance cannot be counted as evolved repeatability.
A separate four-setting finite follow-up does store matched evolving A/I
endpoints. The [matched endpoint audit](CHAPTER2_MATCHED_AI_REPEATABILITY_20261019.md)
admits all four original ZIP hashes and finds lower far-endpoint A variance than
I in all12 setting/start summaries. Most unanimous A near/far contrasts are
exactly zero. Independent review reproduced every summary. This supplies a
bounded descriptive attained-state comparison without new simulation; timing
and initial-to-final directions remain unavailable in these endpoint JSONs.

## Priority and completion boundaries

1. Audit existing matched A/I repetitions under pollinator reduction: direction,
   magnitude, order and event time, retaining extinction and non-events.
2. Design only the missing bounded comparison using measured local resources.
   Changing capacity can affect competition and reproduction as well as finite
   sampling; do not label its full effect pure genetic drift.
3. Return to the already scoped new-environment readaptation component after
   resolving what the existing records can answer. Preserve its implemented
   contract and seed-transfer tests. The subsequently authorized GitHub Actions run has now completed all10,240 futures; see the [admitted results](CHAPTER2_READAPTATION_RESULTS_20261019.md).

The proposed new32x32 confirmation in the user's pasted historical summary is
outdated: the authorized160x160 G/S experiment is complete, independently audited
and merged in PR602. Its G/S results do not formally rank A/I repeatability or
test actual readaptation. Lineage-level assembly/selection remains untested and
is not silently added to this local follow-up. The bounded experimental component is complete; manuscript integration and repository verification are separate delivery gates. Universal determinism, permanent irreversibility and natural lineage filtering remain unidentified, rather than silently treated as confirmed.


## Completed baseline-pollen factorial and variation clocks (2026-10-19)

The new [384-path factorial](CHAPTER2_BASELINE_POLLEN_384_RESULTS_20261019.md)
is distinct from Q2's completed 384-path support intervention. All paths survived.
Additional activity decline produced larger A responses after weak than strong
baseline limitation: weak-minus-strong interactions +0.103678 and +0.083550
for nominal initial A=0.3 and 0.5, with descriptive founder-bootstrap 95%
intervals [0.069499,0.137804] and [0.041450,0.128147]. This is exploratory evidence
from 12 founders; the two starts share founders and are not independent replications.
Strong-limitation populations had already increased A, and 22/48 or 10/48
prefixes were A-monomorphic versus 1/48 in each weak stratum. The factorial
identifies a baseline-effectiveness regime/history interaction, not instantaneous
pollen deficit alone or fixation as the sole mediator. Additional I responses
were negative in strong and positive in weak baseline regimes; universal I
decline under every activity reduction is not supported.

The [stored-genome readback](CHAPTER2_VARIATION_CLOCK_RESULTS_20261019.md)
adds no simulations. At B8 with complete survival, evolving assurance shortened
occupied I-polymorphic duration by 2.628 updates; at B4.5 it extended that
duration by 12.684 alongside substantially improved survival. Fixed-policy A
alleles are latent genetic variation despite constant expressed A=0.5.
Most absent I polymorphism in the transferred seed cohorts was already absent
in donors; transfer added two I monomorphisms in evolving-history cohorts.

The current mechanism statement is therefore conditional: baseline pollen
service shapes selection and prior trait change; inherited variation and
persistence shape subsequent realization. Assurance and investment remain
separable, but neither universal temporal order nor a universal assurance-driven
loss of future adaptability follows. Natural island-flora filtering, genetic
mediation and permanent irreversibility remain outside the established evidence.
The [working article](CHAPTER2_UNIFIED_NEE_ARTICLE_WORKING_20261017.md) incorporates
these positive effects, sign changes and limitations without rewriting earlier
registered null results or adding simulations beyond the frozen allocation.
