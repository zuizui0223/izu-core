# ROI dual-control result — 2026-07-10

## Provenance

- workflow run: `29086553464`
- artifact: `roi-observation-calibration`
- artifact digest: `sha256:1a28f2a659859ab8258c54819a1cce90b749fea5695feda7436538b624f845ef`
- manually accepted flat-control cards: 10 *Ajania pacifica* images
- all 10 images were recovered

The source numerical table is
`data/predictive_meta/roi_dual_control_result_20260710.csv`.

## Result

All four representations detected the deterministic technical attenuation in
all ten pairs. The median attenuated-minus-original salience difference ranged
from -1.330 to -1.410, and the paired direction was negative in every case.
The operators are therefore not simply insensitive.

Only `full_frame` remained within the predeclared 0.25 tolerance for both known-flat
regional contrasts. The three attempted flower-directed crops failed the flat
control:

| proposal | max absolute flat-control contrast | flat control | technical sensitivity |
|---|---:|---|---|
| full_frame | 0.099 | pass | pass |
| centre_65 | 0.308 | fail | pass |
| max_chroma_65 | 0.465 | fail | pass |
| max_chroma_edge_65 | 0.430 | fail | pass |

The automatic centre/chroma crops therefore amplified image-composition or
plant-state differences enough to create a false regional signal in a lineage
whose accepted cards all received the same blinded human score.

## Decision

No operator is released to the broad specialist holdout.

Although `full_frame` passed both technical controls on this strictly screened
subset, it is not a validated flower ROI and remains vulnerable to habitat,
background and framing. The biological positive-control status is still
`missing`, so every row retains
`eligible_for_broad_specialist_holdout = no`.

This result rejects the current simple crop proposals. It does not reject the
staged pollinator-loss prediction. The next admissible step is to register an
independent biological positive-control set before trying a new observation
operator.
