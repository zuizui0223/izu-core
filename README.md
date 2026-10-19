# Izu Core — Model 3 island reproductive economics
> **現行の論文化方針（2026-10-19） — ELを独立のCh3へ分割せず、一つのNEE Article候補へ統合：** [最新の一論文ルート](docs/audits/CHAPTER2_NEE_ACTIVE_PUBLICATION_ROUTE_20261017.json) · [統合NEE作業原稿](docs/CHAPTER2_UNIFIED_NEE_ARTICLE_WORKING_20261017.md)。既存Q1〜Q4に、完了した160×160確認・花粉制限384経路・保存変異解析・限定的再適応を統合する。[現行の成果補足](docs/CHAPTER2_COMPLETED_EVIDENCE_SUPPLEMENT_20261019.md)と[S1〜S33・F1〜F8の配置表](docs/CHAPTER2_HISTORICAL_RESULTS_DISPOSITION_20261019.md)で陰性・未決も追跡する。全回復確率の時計は未検証であり、今回の統合に新規実験を追加しない。旧Ecology Letters原稿・レンダラー・登録結果は再現用の履歴であり、別投稿対象ではない。**NEE投稿準備は未完了。**

> **論文の新規性と証拠の三層（Q1〜Q4）:** [Lepers全文・PR #569を反映した主張の採用／不採用表](docs/CHAPTER2_THREE_TIER_FOUR_QUESTION_NOVELTY_REVIEW_20261016.md)。既知の自殖・花縮小理論との差、新しい遺伝的実現の検証、Q4の独立した存続効果を区別。原稿・原本・登録結果は変更していません。

> **将来の確認実験の検出力ゲート（2026-10-17）：** [Q2・384原本の事後精度監査と新規実験用の事前検出力規則](docs/CHAPTER2_Q2_RETROSPECTIVE_PRECISION_FUTURE_POWER_20261017.md) · [推定可能な効果と計算予算の感度分析（新規実験はHOLD）](docs/CHAPTER2_Q2_FUTURE_POWER_COST_NO_GO_20261017.md)。次の試験は独立した創始者数・訪花履歴数、SESOI、交互作用を含む保守的な分散感度、2主評価量の同時パワー、予算を**新しい結果を見る前**に固定する。Q2の既存主判定`both_inconclusive`は変更しない。

> **中心仮説の採否（2026-10-17）：** [主仮説の最終判定とQ1–Q4の3層対応](docs/CHAPTER2_MAIN_HYPOTHESIS_DECISION_20261017.md)。**「Aの進化がIの低下に先行しても必要条件ではない」**を、限定されたModel 3内で支持済みの論文中心命題として固定。原本384経路のI座保有者数介入については、事前登録した2つの主評価量がともに**未確定**であり、確認済みの効果や遺伝的浮動による単一媒介とは呼ばない。Q1〜Q4の事前登録判定・原本は変更していない。

> **Q2の事前登録384経路本解析（2026-10-16）：** [全六分類・原ゲノム独立再読込結果](docs/CHAPTER2_Q2_I_SUPPORT_384_REGISTERED_RESULT_20261016.md)。元の32シャード×12経路をすべて取得し、7,372,754本のI座子相同染色体・9,999回の二軸bootstrapまで元原本と照合。farでIイベントは24保有20/64対12保有8/64だったが、**進化順序差+0.109375 [−0.125, +0.34375]、Iイベント差+0.1875 [−0.0625, +0.421875]は両方とも多重比較補正区間が0を含み、主判定`both_inconclusive`。** 遺伝的到達可能性の構造的定理と、創始者間で一般化された方向性効果を区別する。新規384経路は[Actions #38918737325](https://github.com/zuizui0223/izu-core/actions/runs/38918737325)で完了。外部DOI原本保存は未完。

> **実装の入口（2026-10-16）：** [現行Model 3のコード範囲・整理方針・実行コマンド](docs/CHAPTER2_ACTIVE_CODE_SURFACE_AND_CLEANUP_20261016.md) · [再現手順](REPRODUCE.md)。生殖・遺伝の凍結済みコードは変更せず、古い解析も削除せずに保存。現在使う数値計算と読み取りツールを明示し、Q4の厳格な再実行検証の限界も記録しています。

> **2026-10-16 統合済み研究・監査の入口：** [8つの発見とS1–S33の証拠序列](docs/CHAPTER2_EIGHT_FINDINGS_INDEX_20261016.md) · [適応度・トレードオフの論文化判断](docs/CHAPTER2_FITNESS_TRADEOFF_EDITORIAL_POSITION_20261016.md) · [コアコードと生態学的因果・循環の監査](docs/MODEL3_REPOSITORY_CODE_ECOLOGY_AUDIT_20261016.md) · [PDE/ODE/SDE/SPDEの成立・失敗範囲](docs/MODEL3_PDE_ODE_SDE_SPDE_FORMAL_AUDIT_20261016.md)。PR #566〜#570でmainに統合済み。単一の現行Letterは未投稿で、全4質問が一つの自然史的因果媒介として証明されたわけではありません。


> **2026-10-16 独立創始者ホールドアウト（PR #569）：** 元の単一創始者でのQ1 4/4設定の正の交互作用は、[新しく引き直した8創始者ゲノム×8訪花者履歴](docs/CHAPTER2_Q1_FRESH_FOUNDER_RESULTS_20261016.md)では**3/4設定でのみ登録基準を通過**。A直接費用ありは +0.04427［95%区間 −0.04406〜+0.13084］で未確定。低送粉側の相対的な花投資温存も2設定で逆符号。全1,088本・陰性対照32ペアは[元のGitHub Actions実行](https://github.com/zuizui0223/izu-core/actions/runs/38853989138)で検証済み。**元のQ1結果を否定したのではなく、創始者・新訪花者背景への一般性の限界を明確化した。** 原軌跡の外部DOI保存は未完了。

> **Start here (navigation audited 2026-10-15):** [Repository map](docs/REPOSITORY_NAVIGATION.md) · [One-paper route and evidence boundary](data/design/chapter2_one_paper_route_20261010.json) · [Reproduction](REPRODUCE.md) · [Historical PR overlap audit](docs/PR_CONSOLIDATION_AUDIT_20261015.md). The one current Chapter 2 manuscript is a **draft, not a submitted paper**. The 2026-10-11 word counts and reviewer-package numbers below are historical snapshots; verify later edits against the active route, source readouts and rebuilt package rather than treating those counts as live.

> **Current merged repository checkpoint (2026-10-15, fixed at `c1b08577`):** [Verified mainline status](docs/REPOSITORY_MERGED_STATE_CHECKPOINT_20261015.md) · [source-ranked paper and SI](docs/CHAPTER2_UNIFIED_EVOLUTION_PERSISTENCE_MANUSCRIPT_20261010.md) · [external data deposit blocker #436](https://github.com/zuizui0223/izu-core/issues/436) · [branch preservation blocker #548](https://github.com/zuizui0223/izu-core/issues/548). At the checkpoint: **one unsubmitted manuscript**, **4,944 main / 147 abstract whitespace-delimited words**, **33 unique SI sections**, **0 open PRs**, **500 branches**, and **no protected branches**. The historical PR audit below contains old open-PR states; use the dated checkpoint for the verified later snapshot. Neither a GitHub reviewer ZIP nor any known raw archive is a complete cross-host DOI deposit.

> **2026-10-11 EL reviewer-preparation snapshot (historical counts):** The **one** current manuscript is [`CHAPTER2_UNIFIED_EVOLUTION_PERSISTENCE_MANUSCRIPT_20261010.md`](docs/CHAPTER2_UNIFIED_EVOLUTION_PERSISTENCE_MANUSCRIPT_20261010.md), with a 142-word abstract and 3,592-word main text. Its reviewer ZIP contains four main figures, **genetic-realization S1 and visitor-tempo S2**, the current Supporting Information and complete tempo tables. **Figure4.svg** retains the original fixed-B48 capacity evidence rank. Use the [current build commands](REPRODUCE.md#current-unified-manuscript-review-package); the historical `build_chapter2_process_review.py` still reproduces the October 6 source draft. DOI-backed raw-data deposition remains incomplete; this package is a reviewer draft, not a submitted manuscript or raw-data deposit.

> **2026-10-11 journal/hypothesis decision (dated snapshot):** Ecology Letters Letter remains the first intended journal for the **single Chapter 2 paper**. The current text passes the route's existing 5,000-word main-text and 150-word abstract limits. Nature Ecology & Evolution or equivalent remains a **conditional research aspiration** requiring new evidence connecting assurance evolution, communal pollen transfer and demographic performance, with generality beyond the present model. See the [high-upside research-question audit](docs/CHAPTER2_HIGH_UPSIDE_QUESTION_AUDIT_20261010.md). Data deposition and the final submission metadata remain outstanding.

> **Active one-paper submission route:** The unified paper retains confirmed 1,000-update floral evolution and a distinct 80-update demographic occupancy experiment as its two principal questions. The separately frozen 400-update visitor-tempo cohort is a **descriptive supplement over 16 synthetic profiles**, with no pooling into the older 64-history studies and no identified persistence benefit at its occupied endpoints. Original manuscript drafts remain source provenance. The route is defined in `data/design/chapter2_one_paper_route_20261010.json`; the [deposit readiness record](docs/CHAPTER2_UNIFIED_DATA_DEPOSIT_READINESS_20261011.md) keeps the original evolutionary, demographic and tempo archives separate.

> **Evolutionary raw archive recovered (2026-10-11):** All **50 original confirmation/generality Actions ZIPs** have now been retrieved and authenticated, including **12,544 original NPZ/JSON case pairs**. The historical archive has been assembled and its private saved copy independently retrieved with an identical checksum. See the [recovery evidence and limits](docs/CHAPTER2_UNIFIED_DATA_DEPOSIT_READINESS_20261011.md#7-evolutionary-raw-archive-recovery-follow-up). Public DOI deposition, the separate 521 demographic ZIPs and tempo archive, and the original discovery replay question retain their distinct requirements.

This repository is the Chapter 2 mechanism paper built around **one ecologically explicit Model 3**.

A [compact Q1–Q4 scientific answer](docs/four_question_resolution_20261011/FOUR_QUESTION_LEDGER.md) now states what is supported, conditional, and still unidentifiable, including the deterministic-versus-finite Model 3 comparison. It does not alter the frozen manuscript or promote pending experiments.

Original 2026-10-06 working title (now source provenance):

> **Reproductive assurance compresses floral-investment divergence under pollinator limitation**

The [2026-10-05 ecological process mainline](docs/CHAPTER2_PROCESS_MAINLINE_20261005.md)
governs the scientific narrative on this branch. The full-mutation
common-environment experiment is complementary genetic/history evidence; it is
not the paper spine.

The previous Ecology Letters Letter remains accessible as source provenance (no longer the active one-paper submission):
[CHAPTER2_MANUSCRIPT_ECOLOGY_LETTERS_20261006.md](docs/CHAPTER2_MANUSCRIPT_ECOLOGY_LETTERS_20261006.md).
The earlier long-form process manuscript is retained as provenance and supporting
material rather than the submission text.

The primary result is prospectively confirmed across **four reproductive settings**.
With assurance fixed at 0.5, low visitor replenishment still produces lower floral
investment. Allowing assurance to evolve then consistently **compresses the near–far
investment contrast**. Post-confirmation decomposition localizes 78–90% of this
attenuation to additional investment decline in the near/high-replenishment arm,
with smaller far-side relief. A corrected rare-mutant analysis shows the local
mechanism: increasing assurance removes substantially more maternal outcross and
paternal pollen-export value where pollination remains effective than where those
returns are already depleted.

The separately confirmed assurance-first temporal sequence remains
setting-specific and is treated as a secondary result, not as evidence that
assurance evolution is required for floral-investment decline.

### Current ecological focus (2026-10-05)

**Why does floral investment decline without assurance evolution, and why does
allowing assurance to evolve compress the phenotypic difference between pollination environments?**

The strongest completed results are:

- at the same plant state, the delayed-setting investment contribution derivative
  shifts from **+0.5793** under near exposure to **-0.7004** under far exposure;
  the outcross component falls from **+1.6523** to **+0.0854**, while the selfed
  component partly offsets rather than drives that decline;
- under maintained isolation, assurance reaches the primary 0.05 change threshold
  first in **51/64** delayed-setting far histories, with 13 near-simultaneous;
- when assurance is fixed at 0.5, far populations still reduce investment by
  **0.3099** in the delayed setting and **0.3316** in the prior setting, so
  assurance evolution is **not required** for investment decline;
- a separate preregistered four-setting campaign confirms that allowing assurance
  to evolve narrows the near–far investment contrast in **4/4 settings**, with
  evolving-minus-fixed interactions from **+0.1007 to +0.2200**;
- in the far fixed-trait assay, higher investment can slightly reduce the
  fractional viable pollen deficit while also reducing viable offspring
  (**-15.72 per 48 plants** in the delayed setting), showing that pollen shortage
  and reproductive return are not interchangeable readouts.

The prior-selfing positive-mutation cell did not show an assurance-first majority.

The ecological synthesis is therefore that **assurance is not necessary for the
initial investment decline, but its evolution compresses the environmental
phenotypic contrast**. Temporal order remains a separate, setting-dependent
quantity. Isolation changes the reproductive economics facing both traits, and
co-evolution can reduce the geographic signature of that selection. Time, distance and trait axes remain uncalibrated synthetic
coordinates.

The additional completed cohorts are distinct from the earlier bridge
design described below; shared near references must not be counted as new runs:

- **Sustained isolation:** 2,048 new far trajectories plus 2,048 existing matched
  near references; 64 visitor histories and eight demographic repeats per setting.
  [Results and temporal-order limits](docs/MODEL3_PERSISTENT_PROCESS_RESULTS_20261005.md).
- **Continuous replenishment:** 13 rates at fixed plant capacity 48; 11,264 new
  trajectories plus 2,048 reused positive-mutation endpoints. All 13,312 cases,
  9,984 event records and 156 endpoint rows are independently verified.
  [Complete results and uncertainty](docs/MODEL3_REPLENISHMENT_EVOLUTION_RESULTS_20261005.md).
  Rates represent established visitor types per update, not visits, kilometres or island area.
- **Fixed plants, changed visitor environment:** 768 verified local assays. At the
  same plant state and capacity0.5, the more-isolated visitor histories produce
  lower investment returns and greater pollen-saturation deficits in the reported
  snapshot comparison. This is a local selection diagnostic, not realized evolution.
  [Results and assumptions](docs/MODEL3_FIXEDPLANT_RETURNS_RESULTS_20261005.md).
- **Evolved-plant pollen assays:** 12,288 verified snapshots. Raw seed compensation
  and deficits after inbreeding depression can differ; pollen limitation is not
  interchangeable with visitor scarcity.
  [Assay results](docs/MODEL3_POLLEN_ASSAY_RESULTS_20261005.md).
- **Fixed versus evolving capacity:** all 8,192 trajectories are complete; 84
  estimates were independently reconstructed and 2,048 zero-mutation pairs are
  identical. Investment declines with capacity fixed at0.5. This does not hold
  realized selfing constant. Both modes lack initial assurance-locus variance.
  [Intervention results](docs/MODEL3_ASSURANCE_INTERVENTION_RESULTS_20261005.md).
- **Trait-by-pollen intervention:** 6,912 completed assays separate fractional
  deficits from absolute viable offspring. [Results](docs/MODEL3_TRAIT_POLLEN_RESULTS_20261005.md).
- **Numerical comparison:** the high-resolution 1,000-update run was stopped at the user
  request after verified period7. The positive-mutation long comparison remains
  computationally unresolved; no automatic restart is planned. Completed local,
  fixed-support and restricted mutation diagnostics retain their stated scope.
  [Stop and alternatives](docs/MODEL3_LONG_COMPARISON_DECISION_20261005.md).

Q1 motivates these independent mechanistic questions. Abstract investment is not
an explicit flower-colour or accessibility phenotype, and no regional Q1 pattern
is used to select parameters. See the [H1–H4 correspondence and claim boundaries](docs/MODEL3_Q1_MECHANISM_MAP_20261005.md)
and the [full closeout requirements](docs/MODEL3_ECOLOGICAL_CLOSEOUT_STATUS_20261005.md).

For the explicit trade-offs, fitness accounting and remaining pathway limits, see
[the pollen-to-evolution explanation](docs/MODEL3_POLLEN_FITNESS_PATHWAYS_20261005.md).

The ecological argument is:

```text
isolation -> continuing visitor arrival/loss -> pollen transfer
                              |
              reproductive contributions and local selection
                              |
                 shared reproduction and inheritance
                        /                    \
         finite individual ABM       deterministic genotype density
         sampled offspring           conditional number propagation
                                             |
                                exact mutation / diffusion approximation
```

[Current result priorities and evidence boundaries](docs/MODEL3_RESULT_PRIORITY_AND_PRESENTATION_20261005.md)
separate the ecological headline, unexpected contrasts and mathematical support.

## What the simulation actually contains

Model 3 is a forward eco-evolutionary simulation, not a statistical fit to named islands.

Each diploid plant state contains three trait axes:

- **access / matching** — which visitor functional types the flower matches best;
- **floral investment** — how strongly the plant invests in the pollinator-facing floral phenotype;
- **reproductive assurance** — the capacity for autonomous reproduction when outcross pollen is limited; this axis can be fixed by intervention or allowed to evolve.

Access and floral investment are inherited in the active trajectories; assurance is inherited only in the treatments that explicitly allow it to evolve.

Each visitor has a functional optimum, breadth and effectiveness. Plant–visitor matching determines finite pollen transfer. Floral investment can increase visitor-mediated return but carries a reproductive allocation cost, so the direction favoured by selection depends on both the plant's starting state and the realized visitor environment.

A full Model 3 reproductive update follows this biological order; the fixed-state assay deliberately stops after the reproductive step before inheritance or population updating:

```text
visitor environment
        ↓
functional matching + pollen export / receipt
        ↓
outcrossing + autonomous selfing
        ↓
viable offspring
        ↓
Mendelian inheritance
        ↓
adult survival + seed arrival + finite recruitment
        ↓
next plant population
```

The same reproductive operator is then viewed at three nested levels:

| layer | what is retained | question |
|---|---|---|
| **fixed-state assay** | reproduction only; no inheritance or population update | Which direction of floral investment is favoured now? |
| **deterministic genotype density** | reproduction + exact Mendelian expectation; no demographic sampling | What inherited change is expected without finite-population sampling? |
| **finite-population ABM** | reproduction + inheritance + explicit individuals, recruitment and extinction | Which expected trajectories are actually realized and persist? |

The prospective isolation bridge changes visitor connectivity rather than assigning synthetic cells to real islands. In the frozen bridge, the primary comparison is a **near** versus **far** visitor-arrival environment, followed by prespecified interventions that diagnose different parts of the mechanism: annual visitor-count matching, pooling independent visitor histories, and increasing plant capacity.

That earlier bridge cohort's **24,576 computational cases** are (not the current mutation/intervention campaign size):

```text
128 independent visitor histories
× 3 starting floral-investment states
× 8 nested demographic repeats
× 8 near/far intervention arms
= 24,576 cases
```

The independent ecological denominator is therefore **128 visitor histories**, not 24,576 cases. Synthetic time, distance and trait coordinates are mechanistic coordinates rather than calibrated natural units.

## Current scientific result

The active process paper separates four biological objects that should not be
collapsed:

1. **current reproductive return** — what additional floral investment yields at
   a fixed plant state;
2. **realized evolutionary order** — which inherited trait reaches a declared
   change threshold first;
3. **causal necessity** — whether evolution of the first-changing trait is
   required for the second response;
4. **reproductive consequence** — whether pollen-deficit metrics track absolute
   viable offspring.

The primary process result is now independently confirmed. In the preregistered
delayed-selfing, assurance-cost 0.5, positive-mutation cell, 64 new visitor histories
again produced **51/64 assurance-first histories** at the primary 0.05
threshold (95% history-bootstrap **0.6875–0.8906**). A separate new-history
fixed-assurance replication retained a negative far investment change
(**−0.3060 [−0.3181, −0.2941]**) and negative far-minus-near effect
(**−0.4354 [−0.4533, −0.4172]**).

The supported synthesis is:

- visitor limitation can lower the marginal reproductive return to attraction
  before plant traits evolve;
- reproductive assurance can reach a realized change threshold before floral
  investment in the confirmed delayed/costly regime;
- **temporal precedence is not causal necessity**: investment still declines
  when assurance capacity cannot evolve;
- assurance evolution can narrow the observed near-far investment contrast even
  when both environments undergo substantial within-population evolution;
- a smaller fractional pollen deficit can coexist with fewer viable offspring;
- the assurance-first sequence is **not universal** across reproductive
  settings: prior selfing with positive mutation gave 30/64 assurance-first
  histories at the same primary threshold;
- the effective ecological sample size is 64 visitor histories; eight
  demographic repeats are nested and are not independent ecological replicates.

The 13-rate extension, mutation/history experiments, finite-versus-deterministic
bridge and unresolved high-resolution positive-mutation numerical comparison are
supporting evidence rather than confirmatory substitutes for this process claim.
Stable latent branch prevalence, calibrated natural rates, named historical
causes and region-to-model-cell assignments remain unidentified.

## Active paper surface

Scientific narrative:

- `docs/CHAPTER2_UNIFIED_EVOLUTION_PERSISTENCE_MANUSCRIPT_20261010.md` — one active Ecology Letters manuscript, including the descriptive tempo supplement.
- `docs/CHAPTER2_UNIFIED_EL_SUPPORTING_INFORMATION_20261010.md` — current Supporting Information, all eight tempo contrasts and their inferential limits.
- `docs/CHAPTER2_MANUSCRIPT_ECOLOGY_LETTERS_20261006.md` — historical evolutionary source manuscript.
- `docs/CHAPTER2_MANUSCRIPT_ACTIVE_20260831.md` — long-form process/provenance manuscript.
- `docs/CHAPTER2_PROCESS_MAINLINE_20261005.md` — current claim spine and parallel-model structure.
- `docs/CHAPTER2_CANONICAL_STORY_20260927.md` — historical bridge narrative.
- `docs/CHAPTER2_MODEL_UNIFICATION_DECISION_20260927.md` — why Model 3 is the only active mechanistic model.
- `docs/CHAPTER2_SUBMISSION_ROUTE_FIREWALL_20260927.md` — current/legacy boundary.
- `docs/MODEL3_Q1_MECHANISM_MAP_20261005.md` — current independent H1–H4 correspondence.
- `docs/CHAPTER1_CHAPTER2_CANONICAL_BRIDGE_20260927.md` — historical Chapter 1 → Chapter 2 handoff.

Model 3 evidence:

- `docs/MODEL3_ISLAND_ECOLOGICAL_RESULTS_20260927.md`
- `docs/MODEL3_ISLAND_NUMERICAL_REVIEW_20260927.md`
- `docs/MODEL3_CH2_BRIDGE_PROSPECTIVE_RESULTS_20260927.md`
- `docs/MODEL3_CH2_BRIDGE_ECOLOGICAL_RESULTS_20260928.md`
- `data/results/model3_ch2_bridge_prospective_frozen_20260927.json`
- `data/results/model3_island_v2_summary/`

Historical bridge-submission control (not the newer process manuscript):

- `data/design/chapter2_unified_model3_lock_20260927.json`
- `data/design/chapter2_oikos_submission_manifest_20260927.json`
- `data/results/chapter2_submission_closure_audit_20260928.json`

Implementation:

- `scripts/model3_island/` — finite-population and deterministic Model 3 implementation.
- `scripts/model3_island_bridge_ops.py` — prospective bridge interventions.
- `scripts/render_chapter2_unified_manuscript.py` — active one-paper renderer and word-limit checks.
- `scripts/build_chapter2_unified_el_submission_bundle.py` — current reviewer ZIP, evidence hashes and separate internal provenance receipt.
- `scripts/render_chapter2_process_manuscript.py` — historical process manuscript renderer.
- `scripts/figure_model3_return_components.py`, `scripts/figure_model3_assurance_compression.py`, `scripts/figure_model3_trait_pollen.py` — main Figures 1–3.
- `scripts/render_chapter2_capacity_companion_evidence_figure.py` — current main Figure 4.
- `scripts/figure_model3_genetic_realization.py` — supplemental Figure S1; the admitted tempo SVG is supplemental Figure S2.
- `scripts/figure_model3_replenishment_evolution.py` — complete replenishment-gradient panels.
- `scripts/generate_chapter2_unified_model3_figures.py` — historical bridge Figures 1–4.
- `scripts/render_chapter2_oikos_generality_overlay.py` — historical snapshot renderer.
- `scripts/render_chapter2_supporting_information.py` — historical bridge Supporting Information.
- `scripts/build_island_ecology_submission_bundle.py` — historical Oikos bundle.
- `scripts/build_island_ecology_review_archive.py` — historical anonymous reviewer archive.

## Natural evidence boundary

Natural systems confront the mechanism by layer rather than being fitted to synthetic parameter cells.

- **A — ecological / selection:** partly observed.
- **B — inherited longitudinal response:** the principal natural-data gap.
- **C — finite / history realization:** partly observed through founding, partner-loss, recovery and persistence systems.

The broader source programme contains **42 research entries / 37 exact geographic labels**. The formal identifiability audit contains **0/25 complete A → B → C contracts**. These counts are evidence-breadth descriptors, not branch-prevalence estimates.

Chapter 3 phenotype values are **not** used to tune, rescue, validate or retroactively prove Chapter 2. Future field work is prospective transport/falsification.

## Reproduction

Fast reviewer checks:

```bash
python -m pip install -e '.[dev]'
pytest -q \
  tests/test_chapter2_model3_submission.py \
  tests/test_chapter2_mechanistic_funnel.py \
  tests/test_chapter2_branch_identifiability_boundary.py \
  tests/test_chapter2_independent_unit_reporting.py \
  tests/test_chapter2_submission_closure_audit.py \
  tests/test_chapter2_unified_model3_figures.py \
  tests/test_model2_legacy_firewall.py
```

Full active regression surface:

```bash
pytest -q
```

Full 24,576-case regeneration is manual-only through `.github/workflows/model3_ch2_bridge_production.yml`. See `REPRODUCE.md`.

## Legacy archive

Historical work remains recoverable but is not part of the current paper or automatic scientific gate:

- `legacy/model2/` — retired Model 2 response geometry, synthetic-`k`, S/C/I and former SI controls.
- `legacy/routes/nee/` — retired NEE route.
- `legacy/routes/ecology-letters/` — retired Ecology Letters analytical route.
- `legacy/submission-history/` — superseded manuscript and submission drafts.
- `legacy/model3-development/` — superseded Model 3 development notes.
- `legacy/pre-model3/` — pre-Model3 top-level scripts and tests.

Git history remains the authoritative provenance for removed current-tree locations. Legacy files must not be cited as current manuscript surfaces.

## Claim ceiling

Do not claim that:

- Model 3 is calibrated to natural kilometres, geological time or evolutionary rates;
- mixed-history fractions estimate natural branch prevalence;
- annual visitor-count matching is a pure field species-richness experiment;
- visitor pooling is literal island number or lifespan;
- the deterministic genotype-density model is a diffusion PDE;
- current Izu associations identify historical *Bombus* causation;
- cross-sectional floral morphology is a measured inherited longitudinal trajectory.
