# Simulation-guided public visual-signature protocol

## Why this is a pivot, not a retreat

The Campanula simulation and source-locked channels do not become irrelevant
because independent floral tables are sparse. They provide the **prediction
contract** for a separate, weaker but broader public-information layer.

The question here is not “can a photograph measure flower size?” It cannot,
without scale. The question is whether a staged effective-pollinator-loss model
leaves a repeatable **relative visual signature** among public images when
measured within taxa and compared across the regional proxy regimes.

## Theory-facing signature

The locked contract is
`data/predictive_meta/public_visual_signature_contract.csv`.

For `ardens_replacement_loss` it predicts:

```text
specialist-like taxa
  large Bombus -> ardens:        flat or weak decrease allowed
  ardens -> no effective Bombus: decrease in visual salience

open-generalist negative controls
  large Bombus -> ardens:        flat
  ardens -> no effective Bombus: flat
```

The contract is not a claim that a pixel is a nectar guide. It is the
observable, image-level consequence expected if guide/display complexity loses
selective value only after effective Bombus service has collapsed.

## Public-image observation model

The current first-pass descriptor set is scale-free:

- saturation;
- colourfulness;
- centre-versus-periphery chroma contrast;
- hue entropy; and
- edge density.

Within each taxon the descriptors are robustly standardised and averaged into
`visual_salience_v1`. The raw value is an image descriptor, not a morphology
measurement. A later ROI/segmentation stage must show that the descriptor is
stable in hand-audited flowers before it can be treated as a phenotype proxy.

## Incomplete data are useful, with a limit

The older gate discarded every taxon without mainland, Oshima and a no-Bombus
island. The signature screen instead uses pairwise contrasts separately:

- mainland + Oshima contributes `large_to_ardens`;
- Oshima + no-Bombus contributes `ardens_to_no_bombus`;
- mainland + no-Bombus contributes an endpoint contrast.

At least two images in each relevant bin are required. A taxon contributes at
most one result per transition; images never become independent evolutionary
replicates.

## Mandatory negative-control validation

The existing manually scored *Ajania pacifica* cards revealed an important
failure mode. All accepted cards had visual-signal score 3 across the three
regime bins, but full-frame descriptors manufactured sizable apparent changes.
This means vegetation, rock, light and composition can dominate raw frame
features.

Therefore the public-image pipeline is explicitly exploratory until a
flower-ROI localisation/segmentation step is validated against blinded manual
cards. This is a falsification result for the naive observation model, not a
negative result for the staged Campanula theory.

## Interpretation boundary

A positive ROI-validated signature screen would support a **prediction** of the
staged model across incomplete public-image contrasts. It would not identify a
historical Bombus replacement, estimate visitor effectiveness, estimate
outcrossing, or eliminate unmeasured environmental and colonisation-history
alternatives.
