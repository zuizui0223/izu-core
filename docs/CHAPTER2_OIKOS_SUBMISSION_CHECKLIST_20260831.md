# Chapter 2 Oikos submission checklist

Updated: 2026-09-27

## Active route

- Journal: **Oikos**
- Article type: **Research Paper**
- Scientific state: **Unified Model 3 bridge complete**
- Journal-facing story: **controlled branch capacity → isolation-driven coarse response → finite visitor and plant realization → history/context filters → real-island A/B/C confrontation**
- Legacy Model 2: **Supporting Information / provenance only; no active control gate**
- Empirical role: **layer-specific confrontation and falsification boundary, not parameter calibration or full natural validation**
- Izu E3/E4: **future A/C transport/falsification, not a submission gate**
- Fallback: **Journal of Ecology Research Article**

Active scientific contracts:

- `docs/CHAPTER2_CANONICAL_STORY_20260927.md`;
- `docs/CHAPTER2_MECHANISM_MAINLINE_LOCK_20260911.md`;
- `data/design/chapter2_unified_model3_lock_20260927.json`;
- `docs/MODEL3_CH2_BRIDGE_PROSPECTIVE_RESULTS_20260927.md`;
- `docs/CHAPTER1_CHAPTER2_CANONICAL_BRIDGE_20260927.md`.

The scientific gate is closed. The two original Chapter 2 controls that had remained unique to Model 2—dynamic realized-richness matching and finite visitor-environment averaging separated from finite plant-population size—were prospectively evaluated inside Model 3 in a verified **24,576-case** bridge.

No additional simulation, world search, focal field data, NEE Stage-1 work or Chapter 3 result is required to establish the current Chapter 2 scientific claim. Submission readiness still depends on package QA and author-supplied metadata.

## Oikos initial-submission requirements implemented

- blinded main upload: **`MANUSCRIPT.rtf`**;
- separate supporting upload: **`SUPPORTING_INFORMATION.rtf`**;
- separate identity-bearing **`TITLE_PAGE.rtf`**;
- double-anonymous manuscript rendering;
- single-column, double-spaced main text;
- continuous line numbering and page numbering;
- Introduction forced to begin on page two;
- abstract capped at 300 words;
- renderer validates the Unified Model 3 mainline rather than historical three-result/four-act routing;
- dedicated Significance statement;
- Data Availability / data-archiving statement;
- accepted-stage public repository fixed to **Dryad Digital Repository**;
- conflict-of-interest and ethics statement surfaces;
- author confirmation of the prefilled ethics statement remains fail-closed through `ethics_statement_confirmed`;
- reviewer-ready frozen data, code and audit materials in the anonymous review archive.

The active submission manifest is `data/design/chapter2_oikos_submission_manifest_20260927.json`.
The active metadata template is `data/design/island_ecology_submission_metadata_template.json`.

## Scientific claim ceiling retained at submission

### 1. Controlled branch capacity

- under controlled visitor compositions, starting floral state can reverse the reproductive-selection gradient;
- illustrative extreme: start access 0.20 gives left/right gradients `+1.5048 / -0.8720`, and start access 0.80 reverses those signs;
- maximum fixed-count composition effect is `2.3768`;
- deterministic inherited composition effect reaches `0.1891`;
- duplicating identical functional types under fixed total activity changes the operator only by machine precision (`1.78e-15`);
- this establishes branch-generating capacity, **not** universal deterministic branching under natural island assembly.

### 2. Prospective isolation bridge — visitor amount and realized heterogeneity

The frozen 24,576-case bridge uses 128 independent visitor histories, eight demographic repeats, three starting states and four paired near/far interventions.

Natural isolation-driven assembly:

- finite ABM mean far-minus-near inherited-investment effect: **`-0.1446`**;
- deterministic density mean: **`-0.4510`**;
- mixed histories at epsilon 0: **`12/128`** finite ABM versus **`0/128`** density.

Annual response-blind richness matching:

- finite ABM mean reverses to **`+0.0333`**;
- deterministic density mean reverses to **`+0.0338`**;
- finite-ABM mixed histories rise to **`68/128`** at epsilon 0;
- deterministic-density mixed histories are **`16/128`** at epsilon 0, **`1/128`** at 0.01 and **`0/128`** at 0.05.

Supported interpretation:

> **Visitor amount/richness strongly positions the coarse mean response, but does not uniquely determine realized directional heterogeneity.**

Annual thinning also changes visitor identity persistence, so it is not a pure field species-richness causal intervention.

### 3. Finite visitor environment and finite plant population are separate axes

- pooling eight independent visitor histories gives **`0/128`** mixed histories in both finite ABM and deterministic density at all declared deadbands;
- increasing plant capacity from 48 to 192 while retaining the natural visitor history reduces finite-ABM mixed histories from **`12/128 → 1/128`** at epsilon 0;
- the larger plant population closes about **41.5%** of the finite-ABM to deterministic mean gap;
- visitor pooling changes environmental averaging/composition, while plant capacity changes demographic sampling; they are not interchangeable mechanisms.

Therefore the current biological reading is:

> **visitor amount sets the coarse regime; finite visitor composition/history and finite plant demography separately control how much directional heterogeneity is realized.**

### 4. S/C/I is descriptive magnitude structure, not directional branching

- in the pooled-visitor finite ABM, `I=0.542`;
- nevertheless mixed histories are **`0/128`** at every declared deadband.

Thus S/C/I remains a useful historical decomposition but its ranking cannot be used as a proxy for opposite evolutionary directions.

### 5. History, reproductive assurance and connectivity

From the completed 19,968-case Model 3 island campaign:

- common final environment, different histories:
  - early visitor loss `-0.1603`;
  - late loss `+0.0322`;
  - uninterrupted `+0.2115`;
- in the declared severe visitor-absence schedule, zero fixed assurance gives **`0/256`** terminal survivors while assurance-present comparison cells retain endpoints;
- seed connectivity and pollinator connectivity act through different ecological/genetic routes and must not be compressed into a single causal isolation mechanism.

### 6. Chapter 1 bridge

Chapter 1 establishes:

- stronger pollen limitation with isolation;
- recurrent reproductive assurance and accessibility/generalization;
- non-uniform detailed colour/architecture;
- residual display associations not fully absorbed by selfing adjustment.

Chapter 2 explains how those results can coexist without fitting Chapter 1 regions to Model 3 cells:

- controlled functional matching supplies branch capacity;
- isolation-driven visitor amount produces a coarse deterministic response;
- finite visitor histories and finite plant demography determine how much heterogeneous response is realized;
- assurance and ecological history further filter persistence.

The H3/H4 combination is therefore not contradictory: a stressful isolation-associated pollination environment can coexist with traits that buffer its realized reproductive cost.

### 7. Real-island A/B/C confrontation

Natural systems are confronted by model layer, not fitted to synthetic parameter cells.

- **A — ecological/selection:** Izu branching; Ogasawara/Xisha propagation; Hawaii/Puerto Rico–Mona buffering; Dominica counterdirectional falsifier.
- **B — inherited longitudinal response:** principal empirical gap.
- **C — finite/history realization:** Surtsey founding, Tiritiri reintroduction/compensation, New Zealand *Rhabdothamnus* and Mariana bird-loss consequences.

Formal source boundary:

- direct comparable plant response: **21/25**;
- direct partner arrival/replacement: **2/25**;
- complete A → B → C contracts: **0/25**;
- descriptive breadth: **42 research entries / 37 exact geographic labels**, not 42 independent Model 3 fits.

### 8. Legacy Model 2 is Supporting Information only

Retain for reproducibility/provenance:

- exact realized-richness matching on the old service endpoint;
- synthetic-`k` finite-community pooling;
- response-rule factorial;
- historical S/C/I decomposition;
- community-mean asymptotic calculation.

Do not present these as a second biological mechanism or an unresolved control gate. In particular, no natural threshold near `k≈4` is claimed.

## Main figures and Supporting Information

Main figures are generated by `scripts/generate_chapter2_unified_model3_figures.py`:

1. Unified Model 3 nested levels and branch capacity;
2. prospective 24,576-case isolation bridge;
3. chronology / assurance / connectivity realization;
4. real-island A/B/C confrontation.

Supporting Information retains:

- S18A real-island layer projection;
- S18B prospective Model 3 isolation bridge details;
- S19–S22 legacy Model 2 structural controls and asymptotic analyses.

## Author-supplied information still required

After scientific-package QA passes, populate the metadata template with:

- final author order and affiliations;
- corresponding-author email, postal address and ORCID;
- significance prior-work context;
- acknowledgements and funding;
- inclusion/EDI statement;
- conflict-of-interest statement;
- ethics confirmation (`ethics_statement_confirmed=true` after author review);
- explicit submission declarations.

**CRediT / author-contribution roles are not an initial-submission blocker.**

The public repository choice is already fixed to **Dryad Digital Repository**.

## Final build

Run:

`python scripts/audit_chapter2_submission_closure.py --check`

then:

`python scripts/build_island_ecology_submission_bundle.py --metadata data/design/island_ecology_submission_metadata_template.json`

Expected bundle: `dist/chapter2_oikos_submission_bundle.zip`.

Until package QA and author-supplied fields are complete, the builder remains fail-closed by design. Any remaining renderer/package failure is **not** a scientific reason to reopen Model 2, rerun the bridge, search more islands or require field E3/E4.
