# Chapter 2 manuscript-value promotion review

Updated: 2026-09-05

## Decision

The systematic source-review phase is complete under the current 111-target protocol, with the active source-work queue at **0**. The next task is therefore not another indiscriminate literature-search wave. It is to decide which source-resolved candidates materially improve the manuscript rather than merely increasing its example count.

A manuscript-value review was run across **29 source-resolved or explicitly bounded candidates** accumulated during the systematic programme.

The review uses five filters:

1. source directness;
2. clean geographic increment relative to the current evidence layers;
3. marginal process information;
4. falsification/mechanistic value;
5. redundancy risk.

The full Chapter 2 contract remains a separate requirement. No reviewed candidate passes the source-state → community-transition → local-realization → plant-response contract.

Machine-readable surfaces:

- `data/design/chapter2_manuscript_value_promotion_review_20260905.csv`
- `scripts/audit_chapter2_manuscript_value_promotion_review.py`
- `data/results/chapter2_manuscript_value_promotion_review_audit_20260905.json`

## Review result

- reviewed candidates: **29**
- `promote_next_integration`: **3**
- `retain_si_only`: **22**
- `hold_overlap`: **3**
- `do_not_promote`: **1**
- full Chapter 2 contracts: **0**

The three candidates selected for the next integration step are:

### 1. Crete

Primary anchor: `10.1006/bijl.1996.0119`.

The key value is not simply another island breeding-system example. *Cyclamen creticum* is self-compatible but unable to set seed without pollinators, and the study quantifies inbreeding depression.

That makes Crete a strong **negative control against collapsing self-compatibility into autonomous reproductive assurance**. It sharpens a distinction already important in the paper's mechanism vocabulary: compatibility state and realized assurance are not interchangeable.

Decision: `promote_next_integration`.

### 2. Trinidad and Tobago

Primary anchor: `10.2307/1938966`.

The study followed early-successional hummingbird-pollinated plants for 13 months across Trinidad and Tobago and explicitly asked how the lower hummingbird diversity on the smaller island affected plant pollination biology.

This is unusually close to the Chapter 2 relational framing because the relevant contrast is not simply `island vs mainland`; it is a **plant response evaluated under differing realized pollinator communities across two islands**.

Decision: `promote_next_integration`.

### 3. Iceland

Primary anchor: `10.1657/1523-0430(2006)38[305:BSEITA]2.0.CO;2`.

North-Iceland *Campanula uniflora* was tested with outcrossed, actively selfed, passively selfed and control flowers. The Icelandic population showed pre-anthesis cleistogamy and predominant inbreeding, interpreted as reproductive assurance under severe arctic constraints.

This adds a distinct **Arctic assurance state** and, importantly, a strong abiotic context in which pollinator scarcity and climate are coupled. It therefore broadens response-state coverage while guarding against a pollinator-only interpretation.

Decision: `promote_next_integration`.

## High-value cases deliberately held

Three cases have high falsification value but are not yet safe for count-changing admission.

### Solomon Islands

Direct bat pollination plus hand-selfing evidence is strong, but geographic de-duplication against the unresolved Pacific multi-system morphology layer is not yet clean.

Decision: `hold_overlap`.

### Palau

The targeted field study is particularly useful because it weakens a simple lost-pollinator narrative: multiple current visitors were observed and the report concluded that simple pollinator-loss limitation was unlikely.

That is high falsification value. However, the source is an authoritative conservation research report rather than a journal article, and Pacific de-duplication remains unresolved.

Decision: `hold_overlap`.

### Cook Islands

The fig-wasp mutualism persisted despite loss of other mutualists, with habitat loss providing a stronger alternative explanation. This is potentially an excellent counterexample to a universal mutualist-collapse narrative, but the Pacific overlap state remains unresolved.

Decision: `hold_overlap`.

## Why most candidates are not promoted

The systematic search recovered many valid direct sources. That does not mean all of them improve the paper.

Most non-promoted candidates fall into one of four groups:

1. **network redundancy** — another interaction network without a linked plant response or transition (for example Sardinia, Sicily, parts of the Aegean/Maltese evidence);
2. **breeding-system redundancy** — strong hand-pollination or exclusion studies whose mechanistic role is already represented by stronger or more discriminating cases;
3. **non-insect natural-history breadth** — valuable direct pollen-vector evidence but no plant reproductive response, where the active breadth layer already includes bird/gecko examples;
4. **geographic or source-boundary holds** — direct subtarget evidence that should not be generalized to a broader archipelago, or multi-system Pacific evidence whose exact de-duplication is unresolved.

This is intentional. The manuscript should not convert exhaustive searching into exhaustive example accumulation.

## Active manuscript boundary

This review itself does **not** change the current active manuscript-facing breadth:

- **39 source-backed research entries**
- **34 exact geographic labels**

It also does not change:

- frozen identifiability audit: **25 research entries**;
- frozen full contracts: **0/25**;
- formal external prediction: **`not_evaluable`**;
- frozen measurement fractions.

The three selected cases are recommendations for the next integration step, not silently counted additions in this review commit.

## Next step

Integrate exactly the three selected exact-group entries — Crete, Trinidad and Tobago, and Iceland — into the post-freeze breadth layer, update the breadth audit/manifest/documentation, and preserve the frozen 25-entry identifiability denominator.

The expected descriptive counts after that dedicated integration step are:

- post-freeze breadth entries: **17**;
- post-freeze exact geographic groups: **16**;
- combined descriptive research entries before cross-layer de-duplication: **42**;
- combined exact labels before higher-level de-duplication: **37**.

Those future counts must not be interpreted as independent archipelagos or as a reopened formal prediction dataset.
