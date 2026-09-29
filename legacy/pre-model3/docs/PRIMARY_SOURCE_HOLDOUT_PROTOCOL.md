# Primary-source holdout protocol

## Why this protocol exists

The prediction-locked synthesis has reached a hard evidence boundary:

- source-locked *Campanula microdonta* supplies calibration;
- public photographs can currently supply only balanced **generalist negative
  controls**;
- no specialist public-photo positive comparison passes the predeclared
  two-eligible-cards-per-regime gate.

The next specialist evidence must therefore be extracted from original papers.
A title, abstract, occurrence record, or a picture is not an effect size.

## Two registries, two roles

### 1. `primary_source_native_evidence.csv`

This registry preserves what an original source actually reports, including
qualitative results that cannot yet enter the prediction scorer. It records:

- the source-native comparison units;
- a trait and the reported direction, if the source explicitly states one;
- whether the observation is numeric, qualitative-only, or not extracted;
- whether exact localities can be mapped to the declared pollinator regimes;
- why a row is not yet scoreable.

For example, the verified publisher abstract for *Ligustrum ovalifolium* reports
shorter Izu corolla tubes and stamens, with stronger shortening on Hachijo. The
registry stores these as qualitative, source-native observations. It does **not**
turn them into a numeric Izu effect, a Bombus-history estimate, or a second-step
transition until the source table and locality definitions are transcribed.

### 2. Common prediction-meta holdout schema

Only `ready_for_holdout` rows are compiled into the common observation schema
used by `scripts/run_predictive_meta_analysis.py`. A row reaches that status only
when it has all of the following:

1. an original table or figure locator;
2. a numeric trait value and unit;
3. sample size and a variance measure;
4. a named population/island locality;
5. an explicit mapping from that locality to one declared regime; and
6. a within-lineage comparison that survives the comparator audit.

The compiler refuses to emit a row with a missing variance, missing regime, or
unmapped source geography.

## Recovery order

The live queue is `data/predictive_meta/primary_source_extraction_queue.csv`.

1. **Weigela coraeensis (2010)** — highest priority because it is the direct
   specialist-like mainland/island floral-differentiation candidate. Recover the
   original table, its locality units, n, and dispersion before assigning any
   direction.
2. **Ligustrum ovalifolium (2014)** — already contributes verified qualitative
   source-native evidence. Recover population tables and locality labels to ask
   whether its mainland–Izu and Hachijo comparisons map to the locked scaffold.
3. **Lilium auratum (2018)** — extract only after checking whether the
   insular/mainland variety comparison is taxonomically interpretable for this
   holdout question.
4. **Clerodendrum (2012)** — contextual only. It is an interspecific contrast,
   so it remains excluded from the within-lineage prediction meta-analysis.

## Reproducible compiler

```bash
python paper/compile_primary_source_holdout.py \
  --registry data/predictive_meta/primary_source_native_evidence.csv \
  --out artifacts/primary_source_holdout/primary_numeric_holdout_observations.csv \
  --summary-out artifacts/primary_source_holdout/primary_source_holdout.summary.json
```

The corresponding GitHub Action uploads both outputs as
`primary-source-holdout-registry`. An empty numeric output is an honest result:
it means no original-table row has yet met the strict entry gate, not that the
registry contains no biological evidence.

## Non-negotiable boundaries

- Do not infer a trait direction from an article title.
- Do not convert a qualitative abstract claim into a numeric effect size.
- Do not map “Izu Islands” to a Bombus regime without its named localities.
- Do not use an interspecific comparison as a within-species island replicate.
- Do not treat a pollinator-fauna difference as pollinator effectiveness.
