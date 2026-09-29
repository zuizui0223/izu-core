# Campanula biological positive-control protocol

## Partition

These cards are calibration data from the focal lineage. They are not an
independent specialist holdout and will never count as cross-lineage
replication.

The blind card set is frozen in
`data/predictive_meta/campanula_biological_positive_control_blind.csv`. It was
recovered from the pre-existing prediction-photo artifact generated before the
ROI operator was selected. The regional key remains outside the rendering
workflow until the blind review is committed.

## Blind stage-0 review

Each card is reviewed without geography for:

1. an open flower;
2. a focal corolla that is sufficiently visible;
3. visibility of the inner corolla surface; and
4. comparability for the predeclared guide score.

An excluded or unclear card is not score zero.

## Trait score

`campanula_inner_guide_strength_0_3`:

- 0: no visible inner spots or guide;
- 1: few or faint inner spots;
- 2: clear inner guide or repeated spots;
- 3: dense or high-contrast inner guide.

## Minimum biological-positive eligibility

The set can be used as a biological positive control only when all conditions
hold:

- at least three cards pass stage 0;
- at least two distinct guide-score levels are represented;
- after the blind scores are frozen, the key contains both `ardens` and
  `no_bombus` regimes;
- the Oshima/ardens median score exceeds the no-Bombus median score; and
- the result is used only to evaluate an observation operator, never as an
  independent test of the staged theory.

Failure of any condition leaves
`biological_positive_control_status = insufficient` and keeps the broad
specialist holdout locked.

## Provenance

The four card URLs and opaque IDs originate from Actions run `28686916004`,
artifact digest
`sha256:8123dfeb99dca92baf843ec468ab87af5816b5efca751c9decaf73b549f29c9a`.
The blind sheet is committed separately from its regional key.
