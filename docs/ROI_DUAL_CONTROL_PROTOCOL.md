# Dual-control ROI observation protocol

## Why the old gate was insufficient

The manually scored *Ajania pacifica* cards provide a useful known-flat
negative control. An ROI operator fails if it creates a mainland–Oshima or
Oshima–no-Bombus visual-salience contrast larger than the declared tolerance.

Passing only that test is insufficient. An operator that erases the flower and
all biologically relevant variation can also look perfectly flat.

## Two technical controls

Every fixed crop proposal is now tested on the same accepted Ajania cards.

### 1. Flat negative control

The original crops retain the hidden regional key only after descriptor
extraction. Both regime transitions must remain within the existing tolerance.
This tests regional false positives caused by background, light, framing or
composition.

### 2. Paired technical positive control

For each exact crop, a deterministic paired copy is generated with reduced
colour saturation, reduced contrast and mild blur. The representation must
assign lower `visual_salience_v1` to the attenuated copy for most pairs and the
median paired decline must exceed the prespecified threshold.

This tests sensitivity to a known image-level loss of colour and local visual
structure. It is not a biological manipulation and does not validate nectar
guides, pollinator perception or floral phenotype.

## Release gate

The output distinguishes three statuses:

| Status | Meaning |
|---|---|
| flat negative passed | the operator did not manufacture a large regional contrast in the known-flat lineage |
| technical positive passed | the representation still detects a deterministic signal attenuation |
| biological positive passed | an independent source-native or blinded-human floral contrast is recovered in the predeclared direction |

An operator may pass both technical controls and still remains ineligible for
the broad specialist holdout while the biological positive control is missing.
The workflow therefore writes
`eligible_for_broad_specialist_holdout = no` for every current proposal.

## Why the attenuation is not used as evidence

The paired attenuation:

- contributes no evolutionary replication;
- is never joined to a pollinator regime;
- is not entered into the specialist/generalist scenario scorer;
- cannot support the staged Bombus-loss theory; and
- exists only to reject insensitive observation operators.

## Next admissible biological positive control

A future positive-control registry must be fixed before running it and must use
one of the following:

1. a source-native population contrast with an original table/figure locator,
   named localities and a visible trait that can be matched to images; or
2. a blinded human-scored image set with at least two score levels and a
   predeclared expected ordering, kept separate from the final holdout taxa.

Using a holdout lineage to choose the operator would move that lineage into the
calibration partition under the v1 amendment policy.
