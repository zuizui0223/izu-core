# Microdonta identifiability core retained in izu-core

## Decision

Only the reusable causal-identification layer is retained from `microdonta`.
The old nectar-guide assumptions, historical Campanula acceptance targets, legacy
ABM families and synthetic worked examples are **not** imported as evidence.

The retained architecture is:

```text
observed response / interaction pattern
    -> declared evidence gate
    -> W = F * E identifiability boundary
    -> admissible competing explanations
    -> value of the next discriminating observation
```

This sits below the current `izu-core` evidence workflow.  It cannot promote a
source merely because a model can reproduce its pattern.

## 1. Exact channel boundary

`channel_id/channel_identifiability.py` implements four conditional results.

### N1: net-only non-identifiability

For positive factors,

```text
W(z) = F(z) E(z)
```

and any positive trait-dependent multiplier `a(z)`, the two different changes

```text
(F, E) -> (aF, E)
(F, E) -> (F, aE)
```

produce exactly the same `W_after = aFE`.

Therefore floral response geometry, persistence geometry, or another quantity
that is only a function of net performance cannot by itself identify which
channel changed.

### N2: W plus one factor

Inside the positive domain,

```text
E = W / F
F = W / E
```

so direct W plus one direct factor identifies the other factor on the same trait
and census scale.

### N3/N4: proxy calibration boundary

For `X_i(z) = q_i(z) F_i(z)`:

```text
q_0(z) = q_1(z)
    -> X_1/X_0 identifies relative F change

q_0(z), q_1(z) unconstrained
    -> the same observed W and X can imply different latent F/E changes
```

This is the formal reason that FDQ, visitor counts, visitation, network degree or
trait matching must not be relabelled as direct effective reproductive service
without a stable/calibrated mapping.

Structural zeroes and extinction are outside the positive-division theorem and
must be modelled separately.

## 2. Current Izu evidence projection

`channel_id/evidence_projection.py` records where the exact theorem can and cannot
currently be invoked.

| evidence layer | status | current permitted use |
|---|---|---|
| abstract positive W=F*E model | exact | N1-N4 mathematical statements |
| historical Campanula three-channel record | not applicable | compare response shapes / constrain alternatives |
| Hiraiwa-Ushimaru FDQ -> matching | not applicable | observational functional-environment link |
| Issue #91 linked field chain | requires factorisation extension | direct effective-service/dependency constraints after real data collection |
| external morphology response shapes | not applicable | recurrence of morphology response direction |

The historical Campanula record remains exactly the adopted three-channel state:

- floral size: continuous erosion;
- multilocus outcrossing: continuous erosion;
- autonomous reproductive capacity: second-transition step;
- nectar-guide change: excluded.

None of those response shapes alone identifies historical Bombus-loss causation
or local-versus-establishment channel attribution.

## 3. Admissible explanations rather than forced model selection

`channel_id/causal_admissibility.py` summarises a caller-supplied admissible
region after biological and observation-compatibility gates have already been
applied.

It reports:

- per-mechanism admissible fraction;
- joint switch-space degeneracy;
- causal resolvability;
- mass over surviving declared explanations;
- causal replaceability cost;
- expected resolvability gain per cost for a predeclared next observation.

These are **grammar-relative structural diagnostics**.  They are not empirical
posterior cause probabilities unless a separate inferential model justifies that
interpretation.

## 4. Immediate use in the current programme

The useful application is not to reopen old guide simulations.  It is to make the
existing claim boundary executable:

```text
historical response shapes
    != historical causal channel

FDQ / visitation / matching
    != calibrated local reproductive factor

linked SVD + treatment data
    -> stronger direct mechanism constraints
    != lifetime F-versus-E identification unless the required W/E mapping is added
```

For future Issue #91 pilot decisions, candidate extra measurements can be ranked
by how much they reduce the declared explanation degeneracy per unit field cost.
The ranking must use prespecified candidate outcomes and should not substitute for
the existing raw-data admission, linkage, independence, and measurement-error
gates.
