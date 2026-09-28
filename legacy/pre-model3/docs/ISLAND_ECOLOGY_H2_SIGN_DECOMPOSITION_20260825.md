# Analytical sign decomposition for H2

Updated: 2026-08-25

## Purpose

This note makes explicit why the v12 branch-generator result is an upstream
functional-opportunity result rather than an artefact of the downstream service or
reproduction transforms. It is an algebraic unpacking of the already-frozen v12
endpoint equations. It introduces no new simulation, parameter value, empirical
mapping, response-state definition, or scientific hypothesis.

The corresponding implementation is
`scripts/run_constraint_mechanism_abm_v12_residual_trait_causes.py`.

## 1. Endpoint quantities

For lineage `i` in environment `g` (mainland-like `M` or island-like `I`), define
its final weighted functional opportunity as the row sum

```text
O_i^g = sum_j w_ij^g
```

where the weights are generated from the plant–pollinator matching architecture.
In v12 the row weights already contain the realized endpoint matching scores and
the declared partner normalization.

The fixed saturation transform is

```text
S_i^g = 1 - exp(-sigma * O_i^g),     sigma > 0.
```

`S_i^g` is therefore strictly increasing in `O_i^g`.

The v12 reproduction transform is

```text
R_i^g = 1 - (1 - d * S_i^g) * (1 - B_i),
```

with

```text
d = 0.65
B_i = (1 - d) * a_i
a_i = assurance_ceiling_i * 0.08.
```

Within a matched mainland–island contrast for one lineage, `d` and `B_i` are
unchanged. v12 freezes assurance responsiveness at zero, so no dynamic assurance
update can create a between-environment sign difference in this endpoint
calculation.

Expanding the reproduction equation gives

```text
R_i^g = B_i + d * (1 - B_i) * S_i^g.
```

Hence

```text
Delta R_i
= R_i^I - R_i^M
= d * (1 - B_i) * (S_i^I - S_i^M).
```

Because `d > 0` and the declared assurance range guarantees `B_i < 1`, the
coefficient `d * (1 - B_i)` is strictly positive. Therefore

```text
sign(Delta R_i) = sign(Delta S_i).
```

Likewise, because `S(O) = 1 - exp(-sigma O)` is strictly increasing for
`sigma > 0`,

```text
sign(Delta S_i) = sign(Delta O_i).
```

Combining the two gives the exact v12 endpoint identity

```text
sign(Delta R_i)
= sign(Delta S_i)
= sign(Delta O_i).
```

## 2. Interpretation of H2

This identity narrows the mechanism interpretation.

The downstream saturation transform cannot manufacture a reproductive sign
reversal from an opportunity contrast, and the fixed reproduction transform
cannot reverse that sign either. Mixed-sign reproductive branching in v12 must
therefore already be present as mixed-sign lineage differences in the upstream
functional-opportunity contrast `Delta O_i`.

The residual ablation then identifies which tested lineage heterogeneity is
required for that within-run opportunity/reproduction branching:

- full residual model: mixed-sign run fraction `0.4167`;
- initial functional-position heterogeneity OFF: `0`;
- trait-adjustment heterogeneity OFF: `0.4167`;
- assurance-ceiling heterogeneity OFF: `0.4167`.

The independent frozen block reproduces the same qualitative boundary.
Consequently, the strongest statement is:

> Within the declared residual ABM, pre-existing lineage functional-position
> heterogeneity is the only tested residual factor whose removal eliminates
> same-environment mixed-sign opportunity/reproductive branching; the downstream
> service and reproduction transforms preserve, rather than create, the sign of
> the upstream opportunity contrast.

## 3. What this does not prove

The sign decomposition does **not** show that arbitrary heterogeneity in an
arbitrary floral trait must generate branching. It also does not establish that
one named empirical trait is the real-world coordinate represented by the
synthetic matching axis.

Initial position affects the endpoint opportunity through the declared matching
architecture and may also affect the trajectory followed under trait adjustment.
The ablation identifies necessity within the tested residual model family; it is
not a theorem that every conceivable ecological model requires initial-position
heterogeneity.

The external 13-system challenge remains a response-state challenge. It does not
convert this algebraic/model-internal result into empirical identification of the
same mechanism in every island system.

## 4. Relation to falsification

This analytical decomposition does not alter the frozen falsification rules.

- H2 would still be contradicted within the declared gate if mixed-sign branching
  survived initial functional-position heterogeneity OFF.
- Network-context worsening still rejects universal protection.
- Autonomous assurance still lacks robust sign rescue.
- The Dominica signed-position projection remains failed and unretuned.

Thus the derivation strengthens transparency about the mechanism path without
making the empirical claim stronger than the frozen evidence.
