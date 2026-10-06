# Chapter 2 journal route — 2026-10-06

## Submission conversion status — 2026-10-06

The Journal of Ecology manuscript now exists as
`docs/CHAPTER2_MANUSCRIPT_JOE_20261006.md`. It is approximately 5.7k words
including references and figure captions, uses the confirmed 10/05 result as
the sole paper spine, keeps the prior-selfing failure as a scope boundary, and
uses three main biological figures. The longer active scientific manuscript is
retained as provenance rather than overwritten.

The current Journal of Ecology author guidance was rechecked on 2026-10-06:
Research Articles are typically about 8,000 words; the abstract must not exceed
350 words and uses numbered statements with a final **Synthesis** point. The
JoE manuscript follows that structure.

Remaining publication-delivery blocker: public deposition of the prepared
confirmatory raw-data bundle and insertion of its DOI into Data Availability
and the preservation manifest.

## Decision

**Primary target: Journal of Ecology.**

**Second target: Evolution Letters.**

**Stretch target: Ecology Letters.**

**Evolution / The American Naturalist remain strong fallbacks; Oikos is the conservative route.**

This decision uses the independently confirmed 2026-10-05 process result and
the current active manuscript, not the retired repeatability manuscript.

## Why Journal of Ecology is first

The paper's biological subject is plant ecology: pollinator replenishment,
reproductive assurance, attraction investment, viable reproduction, and the
evolutionary consequences of plant-animal interactions. The paper is theoretical,
but its central contribution is an ecological mechanism rather than a new
general mathematical framework.

The established claim is:

> Under sustained visitor-replenishment limitation, realized reproductive
> assurance change can precede floral-investment decline, but assurance
> evolution is not required for that decline. Isolation can lower the
> reproductive return to attraction directly.

The primary temporal claim is explicitly restricted to delayed selfing,
assurance cost 0.5, and mutation probability 0.01. That bounded scope is a
strength for a mechanism paper, but makes an all-evolutionary-biology
"field-changing" pitch less natural.

Journal of Ecology explicitly publishes influential work where plant ecology is
central, including plant-animal interactions and theoretical ecological research.
Research Articles are typically about 8,000 words. The current active manuscript
is approximately 10.4k words before references, so the required reduction is
substantial but realistic (~20-25%) while retaining the independent confirmation,
mechanistic intervention and scope boundary.

At the 2026-10-06 routing check, the publisher page reports Impact Factor 6.3,
CiteScore 10.1, 14% acceptance rate and a 10-day median first decision.

## Why Evolution Letters moves to second

Evolution Letters is scientifically compatible: it welcomes evolutionary theory,
evolutionary interactions and theoretical studies. But Letters are expected to
be about 5,000 words and must substantially advance the field or be of broad
interest.

The current manuscript would need to lose more than half its main-text length.
That compression would force the paper to choose between the ecological
mechanism, independent confirmation, setting-specific failure, and the
reproductive consequence. The result can be written as an Evolution Letters
paper, but it is not currently the highest-fit or highest-impact route.

Current publisher-reported Impact Factor: 4.3.

If routed there after Journal of Ecology, the title and framing should shift
from island-floral mechanism to the general evolutionary inference:

> **Temporal precedence does not establish causal necessity in multivariate
> evolutionary response.**

## Why Ecology Letters is a stretch, not the default

Ecology Letters seeks very novel, concise ecology of broad general interest and
prioritizes clearly stated hypotheses. Letters are limited to 5,000 words and
six display items. Current publisher metrics list Impact Factor 7.7 and 14%
acceptance.

The paper has a sharp hypothesis and independent confirmation, so submission is
defensible. The risk is editorial: the confirmed temporal order is intentionally
setting-specific, and the natural-island layer is confrontation rather than
causal validation. A broad universal island-syndrome claim would exceed the
evidence.

Therefore Ecology Letters is appropriate only as a deliberate high-desk-risk
attempt; it should not change the frozen claim ceiling.

## Other routes

### Evolution

Evolution welcomes important theoretical investigations and Original Articles
up to 7,500 words. It is a strong fallback if editors regard the paper primarily
as evolutionary process rather than plant ecology.

### The American Naturalist

The American Naturalist is appropriate for conceptual/theoretical work that
changes how broad ecology/evolution questions are viewed. It becomes attractive
if the manuscript is rewritten around the general distinction between temporal
order and causal dependence rather than the island-pollination mechanism.

### Oikos

Oikos remains the conservative mechanism/process route and preserves the lowest
editorial-risk path if the higher targets reject without review.

## Journal of Ecology submission architecture

### Main text

1. **Ecological cause before evolution.** Same-plant-state near/far reproductive
   return decomposition: visitor limitation collapses the outcross return to
   investment and reverses its total marginal contribution in the focal setting.
2. **Evolutionary sequence.** Discovery result followed immediately by the
   prospectively frozen new-history confirmation: 51/64 assurance-first,
   13/64 near-simultaneous, bootstrap 0.6875-0.8906.
3. **Causal necessity.** Fixed assurance=0.5 still gives negative far investment
   change (-0.3060) and far-minus-near investment (-0.4354).
4. **Scope boundary.** Prior-selfing positive mutation gives only 30/64
   assurance-first at the primary threshold. The confirmed sequence is not
   universal.
5. **Reproductive consequence.** Pollen-deficit magnitude and viable reproductive
   output can move differently.

### Supporting Information

Move out of the main narrative:

- 13-rate replenishment surface;
- reciprocal-selection atlas and broad parameter grid;
- finite-versus-deterministic bridge;
- full-mutation common-environment history experiment;
- mutation/PDE diagnostics and unresolved high-resolution branch;
- repeatability-route analyses;
- detailed natural-island confrontation ledger;
- exploratory attenuation of near-far investment divergence when assurance
  evolves.

### Required editorial conversion

- **Completed:** create the journal-specific ~5.7k-word manuscript from the longer scientific source.
- **Completed:** convert the abstract to numbered statements with a final **Synthesis** point.
- **Completed:** retain three core biological figures; the prior-selfing scope boundary is incorporated in Figure 2 rather than requiring a fourth main figure.
- Data Availability must cite the durable history-level CSVs and, once public,
  the DOI-backed confirmatory raw-data deposit.

## Claim language

Use:

> **Temporal precedence is not causal necessity.**

and:

> **Assurance evolution is not required for investment decline under the
> declared delayed-selfing/costly conditions.**

Do not shorten this to "assurance is unnecessary." Fixed assurance=0.5 retains
the capacity for realized selfing; the intervention blocks assurance evolution,
not assurance itself.

## Pre-submission gates

1. Publicly deposit the prepared confirmatory bundle and obtain a DOI.
2. Add the DOI to Data Availability and the preservation manifest.
3. Compress the active manuscript to the Journal of Ecology architecture above.
4. Keep the former Evolution Letters repeatability manuscript retired as a
   standalone submission route.
5. Merge PR #402 after explicit repository-write approval.

Official pages checked 2026-10-06:
- Journal of Ecology aims/scope and author guidance:
  https://besjournals.onlinelibrary.wiley.com/hub/journal/13652745/aims-and-scope/read-full-aims-and-scope
  https://besjournals.onlinelibrary.wiley.com/hub/journal/13652745/author-guidelines
- Ecology Letters:
  https://onlinelibrary.wiley.com/page/journal/14610248/homepage/productinformation.html
- Evolution Letters:
  https://academic.oup.com/evlett/pages/about
  https://academic.oup.com/evlett/pages/author-guidelines
- Evolution:
  https://academic.oup.com/evolut/pages/about
- The American Naturalist:
  https://www.journals.uchicago.edu/journals/an/instruct
