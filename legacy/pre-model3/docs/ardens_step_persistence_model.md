# Ardens step-persistence candidate

## Biological question

The original continuous `ardens_bridge_loss` candidate treats flower length as
responding to present candidate pollinator service. That is not the same as the
alternative biological story:

1. a large initial floral-size reduction occurs at an Oshima-like *Bombus
   ardens* bridge stage; and
2. this smaller flower is retained through downstream small-bee-dominated
   islands, while outcrossing, autonomous reproduction, and perhaps guide state
   can change later.

This module makes that second story a separate, falsifiable candidate.

## Declared scaffold

`data/ardens_step_persistence_stages.csv` is locked before scoring:

| stage | islands |
|---|---|
| mainland reference | Honshu |
| bridge flower step | Oshima and every downstream island |
| post-bridge reproductive stage | Toshima, Niijima, Kozushima, Miyake, Hachijo |

The scaffold is based on the working biological hypothesis and retained source
context. It is **not** an occupation history, colonization route, dated
transition, or causal observation.

## Equations

The model permits a bridge effect and an additional downstream effect for
assurance and outcrossing. Its crucial strict prediction is the flower equation:

```text
flower length = intercept - bridge flower step + environment residual
```

There is deliberately no downstream small-bee term and no ordinal island-order
term in flower length. Thus, after the Oshima-like transition, the expected
flower length is identical across downstream islands at identical environment.
Observed downstream decline is handled only by the declared residual scale; if
that is inadequate, this strict-persistence candidate should lose to a model
that predicts continued change.

## What a result would mean

A high compatibility score would mean only that the retained source summaries
are compatible with this proposed step pattern under the declared priors and
residuals. It would not prove that *B. ardens* was the causal agent, that small
bees had no effect, or that the stages occurred in this historical order.

The six-candidate SMC screen keeps the prior five-candidate register intact and
adds this candidate explicitly. Results must be reported as a new comparison,
not substituted into old five-candidate wording.
