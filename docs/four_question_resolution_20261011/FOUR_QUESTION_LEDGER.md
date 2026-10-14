# Four-question resolution: working claim ledger, 2026-10-11

This working synthesis retains frozen prior nulls. The original-mutation numerical comparison is now complete and admitted in all ten contexts, with320 matched ABM histories independently checked. GitHub main25ada7ee (PR483) corrects historical replay claims; later recovered confirmation/generality archives remain distinct from unavailable discovery originals.

## 一頁要約（2026-10-14、既存結果の整理のみ）

**中心質問：** 送粉環境の変化が花への投資（I）と自律繁殖保障（A）の選択をいつ変え、どんな順序・遺伝的軌跡で実現し、集団の存続に結び付くか。

**現時点の答え：** 送粉不足は進化前から花投資の繁殖利得を変える。しかし、選択の方向、観察された順序、有限集団で実現する遺伝的変化、存続上の利得は別々であり、四段階の一続きの因果連鎖はまだ実証されていない。

| 問い | 支持された結果（Model 3内） | 限界 |
| --- | --- | --- |
| **Q1 閾値・利得** | 固定植物状態で投資勾配はnear **+0.5793**、far **−0.7004**。Aの進化を止めてもIは減少し、Aの進化を許すとnear–far差は**4/4設定**で縮小。 | 遺伝的アクセスの閾値はイベント定義に依存し、普遍的な送粉者・地理的閾値ではない。 |
| **Q2 順序** | 遅延自殖・コストありではA先行**51/64**、先行自殖では**30/64**。人為的な発現順序の環境間効果は事前設定の**±0.05**実質的等価域内。 | 「先に観察」と「原因として必要」、人為的順序と自然な遺伝的順序は異なる。 |
| **Q3 実現** | 同じ生殖演算子でも条件付き決定論的軌跡と有限ABMの結果は異なる。低供給・機能一致の2条件で決定論はA先行、ABMのA先行は**3/32、2/32**。 | 確率性・遺伝変異・密度の寄与率は分離していない。 |
| **Q4 存続** | 別の準備状態介入で存続率差**+2.83 / +4.59ポイント**。独立32履歴の別試験では、環境履歴×A進化可否の統合存続交互作用**+10.84ポイント**。 | 介入と試験条件が異なり、前者の準備状態介入では保守的な分布自由区間が0を含む。自然発生したA先行そのものによる集団救済は未同定。 |

**決定論と確率論の要点：** 元のnear/far比較では投資変化が決定論**−0.4510**、有限ABM**−0.1446**。異方向を含む履歴はそれぞれ**0/128、12/128**（判定幅0）。各年の送粉者数を一致させる操作（種の同一性・継続性も変わる）では平均効果が双方で正に反転（**+0.0338、+0.0333**）する一方、異方向の履歴は**16/128、68/128**。植物収容力48→192ではABMの異方向履歴が**12→1**に減る（履歴の分類は反復・判定幅に敏感）。**初期植物状態×送粉者の機能的組成だけでも決定論的な方向分岐は成立し、有限の送粉者履歴・集団過程が実現を変える。** 決定論はABMの厳密な確率平均ではないため、数値差を「浮動の効果量」と呼ばない。

**論文に残す主張：** 「共通の送粉制約は共通の選択問題を作りうるが、初期状態・遺伝的アクセス・送粉者組成・有限過程によって実際の進化経路は一意には決まらず、人口学的帰結も条件付きである」。Q1→Q4の完全な因果媒介、野外の特定島嶼史への外挿、失敗・等価・未確定試験の再分類は行わない。

根拠：[統合原稿](../CHAPTER2_UNIFIED_EVOLUTION_PERSISTENCE_MANUSCRIPT_20261010.md)／[決定論・ABMの前向き比較](../MODEL3_CH2_BRIDGE_PROSPECTIVE_RESULTS_20260927.md)／[決定論モデルの解釈監査](../CHAPTER2_DENSITY_CLOSURE_AUDIT_20261003.md)／[遺伝的実現の数値比較](../atom_comparison_20261011/ATOM_ABM_NUMERICAL_VERDICT_20261011.md)／[独立32履歴の存続試験](../CHAPTER2_ISLAND_DEMOGRAPHIC_PERSISTENCE_20261008.md)。以下に2026-10-11時点の詳細台帳を残す。

## Q1 — Threshold
The independent 6,144-case confirmation identifies a sign-changing order-score band [0.046875, 0.078125] in initial assurance allele half-width, replicated in both founders and all three low-supply contexts. This is a conditional genetic-access boundary, not a universal pollinator-supply threshold. All initial parents have the same expressed assurance, while segregation generates variance. At the registered 0.05 response threshold, standing alleles alone cannot achieve the event when half-width is 0.046875; mutation is necessary. At threshold 0.10 both band endpoints favor investment-first. Threshold sensitivity must accompany the main result.

## Q2 — Sequence
Sequence depends on the estimand. PR472 preserves the historical founder-relative 51/64 assurance-first result, but 22/64 histories become strictly investment-first when measured as isolation-induced far-minus-near divergence. Ties and censoring are not opposite sequences. The hypothesis that assurance selection begins earlier than investment reduction is not established: PR473 offers fixed-state counterexamples, while PR474 introduced a current-checkout replay candidate, whose historical identity remains unverified after PR483. PR473 is now merged source-diagnostic evidence; PR474 is now merged. Neither supplies confirmed all-history selection timing.

PR476 now supplies completed visitor-chronology evidence: abrupt versus gradual functional loss changes assurance/investment crossing probabilities conditionally across eight settings. In the four costly-assurance settings, assurance crossing by100 is higher under abrupt loss by21.875–42.1875 percentage points. Assurance-only remains distinct from assurance-first; one prior/no-cost/mutation setting has fewer assurance-first histories under abrupt loss. No universal sequence or all-history selection-onset mechanism is established.

## Q3 — Realization
Mutation-access histories change realized response. The registered order-score difference is +0.0634765625, with 95% paired interval [0.046875, 0.080078125]. However, only 42/1024 assurance-access-first and 43/1024 investment-access-first preparations achieve both registered responses. Assurance events occur in 636 versus 299 starts; investment events in 52 versus 150. Thus the intervention principally changes which response is realized, as well as sequence. It does not identify a pure order effect among equivalent endpoints.

At preparation end all 1024 starts per arm remain occupied. Conditional end-state mean assurance is 0.5780522362 versus 0.5490180722, and investment 0.4950299740 versus 0.4924639545. These post-result descriptive differences provide possible mediators, not independently established causal decomposition. Conditioning survival analysis on both-event histories would break the randomized all-start comparison.

## Q4 — Persistence
Under common subsequent challenges, assurance-access-first preparation increases terminal occupancy by 2.832 percentage points (simultaneous paired bootstrap interval 0.684–4.980) in the reference-growth-1.05 challenge and 4.590 points (1.855–7.324) at reference growth 1.50. Occupied fractions increase by 5.245 and 1.739 percentage points respectively. These challenges use budgets calibrated on the unevolved main-founder reference; labels are not realized growth rates of evolved populations.

These are preparation-policy effects, not proof that naturally selfing-first evolution itself causes a benefit. Full distribution-free Hoeffding intervals include zero and do not establish equivalence within ±10 percentage points. Viable self/outcross outputs are descriptive and cannot alone identify survival mediators. Earlier frozen inconclusive contrasts remain unchanged.

## Deterministic versus stochastic comparison

The completed atom-plus-cell campaign admits all ten contexts after both65→129 and129→257 comparisons under the original thresholds. All30 archives, full genotype weights, CDFs and decisions were independently verified. The exact initial assurance atom is retained separately from cell-integrated original finite-rate reflected Gaussian birth mutation; reproduction uses midpoint quadrature. Matching and investment have standing variation but do not mutate. This200-update, K48 comparison is not a full three-mutating-locus PDE, heat approximation, SPDE, or stochastic ensemble mean. Prior uniform0/10 and centered4/10 verdicts remain frozen. See [completed numerical and ABM verdict](../atom_comparison_20261011/ATOM_ABM_NUMERICAL_VERDICT_20261011.md).

The matched comparison retains all320 existing ABM starts across the same ten founder/environment contexts. A separate implementation recomputed990 event classifications and40 checkpoint summaries. At primary change0.05, sustained20 censuses with a five-update tie window, density predicts assurance-first in both low-supply0.125/matched contexts, whereas only3/32 and2/32 ABM histories realize that category. Assurance-only is15/32 and7/32 and must not be counted as assurance-first. All32 starts per context remain occupied at200, excluding extinction-based removal as the explanation for the category difference. The source-matched comparison does not separate drift, parent sampling, genetic access or density effects; it does not identify a persistence benefit. At change0.025 those density histories are near-simultaneous, so the response-order statement depends on event magnitude. All three registered sensitivities and all ten contexts are retained in the accompanying table and figure.

## Evidence
- work/resolution_20261011/independent_readout_verification.json: independent all-start arithmetic, 6144 boundary and 3072 preparation records.
- work/resolution_20261011/boundary_readout.json and boundary_access_diagnosis.json.
- work/resolution_20261011/history_readout.json and history_state_diagnosis.json; 6144 future challenges.
- outputs/RESOLUTION_DESIGN_20261011.md and CENTERED_NUMERICAL_DESIGN_20261011.md: immutable predeclared designs.
- PR472 locally replayed with five passing tests; PR473 and PR474 pinned sources passed fourteen and seven local regression tests respectively. PR474 reproduced six original crossing events in one eight-repeat near/far cluster. These checks establish current-checkout diagnostics and agreement with frozen event summaries, not authenticated original annual genomes or additional independent evolutionary cohorts.

The manuscript should retain the four questions and distinguish threshold, observed sequence, achieved genetic response, and persistence-policy effects. An order-centered narrative is possible, but neither a universal selection-onset mechanism nor pure order-mediated persistence benefit is currently established.

PR476 persistence boundary: all64 starts per setting/schedule remain occupied at100 and400. No visitor-tempo persistence benefit, harm or equivalence is identified in this ceiling-limited cohort. See REPO476_READOUT_VERIFICATION_20261011.json; profile-bootstrap recomputation covers128 outcomes, not156 secondary fields per setting.
