from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs/ISLAND_ECOLOGY_RESEARCH_ARTICLE_SUPPORTING_INFORMATION_20260827.md"
DEFAULT_OUTPUT = ROOT / "dist/SUPPORTING_INFORMATION.md"

OLD_HEADER = """# Supporting Information — Response geometry under community reorganization

**Status:** active manuscript companion  
**Updated:** 2026-08-28
**Main manuscript:** `docs/ISLAND_ECOLOGY_RESEARCH_ARTICLE_ACTIVE_DRAFT_V2_20260827.md`

This Supporting Information is part of the active manuscript surface. It exposes the complete model rules required to reproduce the response-geometry, local-context and assurance analyses. The numerical values below are synthetic design and sensitivity choices unless explicitly identified as literature-motivated directions; they are not empirical estimates of one island system.

The appendices follow the active funnel: S1–S11 define and diagnose the synthetic response space, S12 records the claim boundary, S13 reports the world-comparison identifiability gate, S14 gives the exact interaction-kernel derivation, and S15 separates the roles of simulation, comparative research entries, Izu and the Chapter 3 handoff.
"""

NEW_HEADER = """# Supporting Information — Response geometry under community reorganization

This Supporting Information exposes the complete model rules required to reproduce the response-geometry, local-context, assurance and relational-robustness analyses. Numerical values are synthetic design or sensitivity quantities unless explicitly identified as published empirical measurements; they are not estimates of natural prevalence or calibrated island thresholds.

Appendices S1–S14 preserve the original frozen model, source-readiness and interaction-kernel analyses. Appendix S15 separates the roles of simulation, comparative evidence and Izu. Appendix S16 records the prespecified relational-robustness audit. Appendix S17 records the geography-first world-saturation audit without reopening the frozen formal denominator. Appendix S18 reports contemporary Izu functional-chain sensitivities that distinguish a robust FDQ-to-matching association from weaker downstream matching-to-pollen propagation.
"""

OLD_NONADD = """For the baseline `21 × 96` matrix, the shares were `2.18%`, `80.17%` and `17.64%`, respectively. The observed and additive-fitted response signs differed in `271/2016 = 13.44%` of cells. The same decomposition was applied separately to every `21 × 24` joint-design matrix. Median additive-sign mismatch was `13.59%` for all-positive, `18.06%` for mixed and `11.61%` for all-negative points.

Because there is one simulated value per starting-position × realization cell, the non-additive remainder combines state-by-realization contingency with cell-level simulation variation. It is not a pure empirical interaction variance estimate.
"""

NEW_NONADD = """For the historical baseline `21 × 96` matrix, the shares were `2.18%`, `80.17%` and `17.64%`, respectively. The observed and additive-fitted response signs differed in `271/2016 = 13.44%` of cells. The same decomposition was applied separately to every `21 × 24` joint-design matrix.

Each pollinator-community trajectory is generated once per realization and shared across all 21 starting positions. Conditional on that trajectory, `endpoint_on_trajectory` contains no additional random draw and every response-matrix cell is deterministic. The non-additive remainder is therefore the exact starting-position × community-realization non-additive component of the fixed matrix, not a mixture with within-cell simulation noise. The numerical shares remain finite-ensemble synthetic diagnostics rather than population variance parameters. A later prespecified six-seed audit places the baseline community share at the upper end of a `69.34–80.17%` sensitivity range while preserving the component ordering; see Appendix S16.
"""

OLD_S13_CH3 = "Chapter 3 phenotype was excluded from the predictor ledger and Chapter 2 validation decision."
NEW_S13_CH3 = "Prospective focal phenotype data were excluded from the predictor ledger and the present validation decision."

OLD_S15 = """# Appendix S15. Evidence roles and mechanistic-resolution funnel

| Layer | Supported role | Explicit exclusion |
|---|---|---|
| Synthetic model | Defines possible response geometries and a model-conditional proximal explanation | Natural prevalence, empirical thresholds, ultimate history and external predictive accuracy |
| Comparative universe | Establishes empirical response diversity and audits source-native joint measurement | Meta-analysis, independent-archipelago denominator, validation coverage and outcome-derived regime assignment |
| Izu focal system | Separates raw source-state/community-composition structure from null-corrected beyond-composition sorting | Outcome-independent global selection, synthetic-threshold validation, precise island-centre causation and floral evolution |
| Chapter 3 | Receives the remaining plant-linked effectiveness/dependency/phenotype measurement problem | Retrospective validation, Bombus-causation proof, pollinator-selection proof and external prediction success |

The Izu raw-matching slope was `0.5669` (95% CI `0.2977–0.8361`), whereas the same frozen predictor had slope `0.0333` (95% CI `−0.2680–0.3346`) for null-corrected matching. Thirteen of 120 exact assignments of observed island centre shifts produced raw slopes at least as large as the observed assignment, and a source-position-only model described raw response at least as well as the full centre-shift projection. These attacks locate the current signal at source state plus background community composition and do not support additional non-random partner sorting.

The remaining prospective contract is:

`source state + community assembly + realized partner sorting + partner effectiveness + reproductive dependency/outcome`.

Chapter 2 identifies that contract; it does not claim that Chapter 3 has already satisfied it.
"""

NEW_S15 = """# Appendix S15. Evidence roles and mechanistic-resolution funnel

| Layer | Supported role | Explicit exclusion |
|---|---|---|
| Synthetic model | Defines possible response geometries and a model-conditional proximal explanation | Natural prevalence, empirical thresholds, ultimate history and external predictive accuracy |
| Comparative universe | Establishes empirical response diversity and audits source-native joint measurement | Meta-analysis, independent-archipelago denominator, validation coverage and outcome-derived regime assignment |
| Izu focal system | Separates historical source-state/community-composition inference from contemporary functional realization | Outcome-independent global selection, synthetic-threshold validation, precise island-centre causation and floral evolution |
| Prospective measurement | Tests the remaining plant-linked effectiveness/dependency contract | Retrospective validation or outcome-derived predictor reconstruction |

The historical Izu raw-matching slope was `0.5669` (95% CI `0.2977–0.8361`), whereas the same frozen predictor had slope `0.0333` (95% CI `−0.2680–0.3346`) for null-corrected matching. Thirteen of 120 exact assignments of observed island centre shifts produced raw slopes at least as large as the observed assignment, and a source-position-only model described raw response at least as well as the full centre-shift projection. A prespecified Oshima-source bridge was unsupported. These attacks locate the historical signed-position signal at source state plus background community composition and do not support additional non-random partner sorting.

The remaining prospective contract is:

`source state + partner loss/arrival + realized community + partner effectiveness + reproductive dependency/outcome`.
"""

APPENDIX_S16 = """

# Appendix S16. Prespecified relational-robustness audit

A structural audit was frozen on 2026-08-31 before execution and retained the historical baseline rather than selecting a new seed or horizon after inspection. It varied model horizon `steps in {30, 60, 120, 240}`, trait adjustment `{0, 0.01, 0.03, 0.06}`, the historical seed plus five prespecified sensitivity seeds, and one equal-initial-richness scenario with 9 mainland-like and 9 island-like pollinator types. All other baseline mainland-like/island-like differences were retained in the equal-richness sensitivity.

Across horizons, mixed-sign realization counts were `65, 48, 41, 43` of 96 for 30, 60, 120 and 240 steps, respectively. Community realization remained the largest sum-of-squares component at every horizon (`71.00–81.57%`), while the starting-position additive component ranged `0.59–4.26%` and non-additivity `17.64–28.41%`.

Across the six prespecified seeds, community realization ranged `69.34–80.17%`, starting position `2.17–3.14%` and state × community non-additivity `17.64–27.91%`. The historical seed produced the largest community share in this sensitivity ensemble but was not replaced. Community realization was the largest component for every seed.

At trait adjustment zero, `64/96` realizations remained mixed-sign. The starting-position additive component was `0.18%`, community realization `67.32%` and state × community non-additivity `32.50%`. Thus trait adjustment is not required for state-dependent mixed geometry; it changes how state dependence is partitioned between additive and non-additive terms.

With initial pollinator richness equalized at 9 versus 9, `53/96` realizations were mixed, 31 all-positive and 12 all-negative. Community realization remained the largest component (`74.04%`). This result establishes only that reduced initial pollinator richness is not necessary for mixed response geometry; loss, arrival, dispersion, generalist fraction and replacement differences remain.

The same audit summarized direct-measurement availability across the frozen 25-entry source ledger: response outcome `21/25`, community functional shift `13/25`, local filtering `9/25`, richness/FD change `8/25`, source functional state `5/25`, partner loss `5/25`, reproductive assurance `5/25`, and partner arrival/replacement `2/25`. These are research-entry availability counts before geographic de-duplication, not independent-archipelago frequencies. Their role is to identify an outcome-rich/process-poor measurement bottleneck; the full joint contract remains `0/25` and formal external prediction remains `not_evaluable`.
"""

APPENDIX_S17 = """

# Appendix S17. Geography-first saturation and final world synthesis

The frozen 25-entry identifiability audit was not expanded after outcomes were inspected. A separate geography-first audit was instead used to test whether the response/process vocabulary or the measurement bottleneck changed when the search frame no longer began from the literature-built target list.

The independent starting artifact contained `4,663` candidate island polygons at least 20 km2. Raw polygons were grouped into archipelago or biogeographically coherent system units before literature review so that multiple nested islands did not automatically create independent replication. Search rows remained descriptive/saturation evidence and were never silently promoted into the formal prediction denominator.

In the first 20 omitted systems, direct plant response was recoverable in `10/20`, breeding or assurance information in `9/20`, realized-community/process contrast in `7/20`, and local filtering in `2/20`. Direct historical partner loss was `0/20`, direct partner arrival/replacement was `0/20`, and full matched contracts were `0/20`. Continued breadth therefore added contemporary states more readily than historical transition coordinates.

The stopping rule required two consecutive eligible geography-first tranches with no new response state, process state, falsification role, direct historical partner loss/arrival measurement or full contract. The counter was reset when a later Gulf of California tranche added a historical/ploidy alternative mechanism in *Pachycereus pringlei*. The following two eligible tranches added no new state and no full contract, satisfying the declared `2/2` large-island saturation rule.

A mandatory <20 km2 supplement then reviewed eight preselected small-island systems. Tiritiri Matangi supplied a documented pollinator reintroduction linked to a direct functional pollination experiment, while Surtsey supplied a bounded empty-island founding/colonization chronology. Across the eight systems, direct historical partner loss was `0/8`, direct arrival/reintroduction `1/8`, and full contracts `0/8`.

The final world synthesis therefore retained only distinct mechanistic roles rather than every searched island: Surtsey for dated founding chronology, Tiritiri Matangi for documented reintroduction plus functional testing, and Gulf of California *Pachycereus* for a historical/ploidy alternative and failure of a simple current-pollinator-abundance explanation. The separate descriptive breadth is `42 research entries across 37 exact geographic labels`; the formal identifiability denominator remains `25 research entries across 21 exact labels`, full contracts remain `0/25`, and formal external prediction remains `not_evaluable`.
"""

APPENDIX_S18 = """

# Appendix S18. Contemporary Izu functional-chain sensitivity

## S18.1 FDQ to corrected trait matching

A transparent source-native sensitivity model used `TM_z ~ FDQ + FEve + site fixed effects + season fixed effects`. The FDQ coefficient was `+1.8346` across all eight source sites, `+1.5414` across the three mainland sites, `+1.9426` across the five Izu islands, and `+2.0590` within Niijima, Kozu, Miyake and Hachijo alone. The five-island leave-one-island range was `+1.4320 to +2.2257`; the post-Oshima four-island range was `+1.4561 to +2.3325`. Every coefficient in both island omission sets remained positive.

The archived pollinator table contained zero recorded *Bombus* species × site × season rows in the four-island post-Oshima subset. This is a sampled-network statement, not proof of biological absence. The result shows that continuous contemporary pollinator functional structure contains explanatory variation within the sampled post-Oshima networks and should not be reduced to a binary sampled-*Bombus* label.

## S18.2 Corrected trait matching to pollen receipt

Pollen observations were first aggregated to plant × site × season means because `TM_z` is shared within site × season. The fixed-effect coefficient of `TM_z` was `+0.0295` across all eight sites, `+0.0468` on the mainland, `+0.0353` across Izu5 and `+0.0342` across post-Oshima4.

Site × season clustered CR1 uncertainty was broad: the Izu5 coefficient was `+0.0353` with 95% t interval `−0.0314 to +0.1019`; the post4 coefficient was `+0.0342` with interval `−0.0510 to +0.1194`. All four geographic-subset intervals included zero. The downstream association is therefore positive in point estimate but not estimated as a precise geographically stable coefficient.

Omission diagnostics localize the fragility to network state rather than one plant taxon. In both Izu5 and post4, all nine estimable leave-one-plant models remained positive; one *Oxalis corniculata* var. *trichocaulon* omission was non-estimable because the fixed-effect design became singular. Leaving out Hachijo or season 3 reversed the island-only coefficient. For Izu5, all `24/24` estimable leave-one-site-season coefficients remained positive. For post4, `18/19` remained positive; the single reversal occurred when `Hachijo × season 3` was omitted.

## S18.3 Cross-channel response branching

Eight source-defined Oshima-to-post plant targets had all three contrasts available. Corrected trait matching was lower post-Oshima in `8/8`. Floral-tube response split into `3 shorter / 4 longer / 1 unchanged`, and pollen receipt split into `4 lower / 4 higher`. Only `2/8` targets showed the complete `matching lower + tube shorter + pollen lower` combination.

These eight plants share island environments and are not eight independent boundary experiments. Their supported role is response-branching evidence: a common decline in corrected matching does not imply one downstream morphology or pollen direction.

The contemporary evidence therefore has a hierarchy. `FDQ -> corrected matching` is the robust upstream association; `matching -> pollen` is positive on average but cluster-uncertain and network-state sensitive; morphology and pollen responses branch further downstream. None of these associations identifies historical *Bombus* loss, historical selection, causal mediation or a completed visitor-effectiveness/dependency chain.
"""


def render_supporting_information(source: Path = SOURCE) -> str:
    text = source.read_text(encoding="utf-8")
    for old, new, label in (
        (OLD_HEADER, NEW_HEADER, "header"),
        (OLD_NONADD, NEW_NONADD, "nonadditivity interpretation"),
        (OLD_S13_CH3, NEW_S13_CH3, "prospective-data boundary"),
        (OLD_S15, NEW_S15, "evidence-role appendix"),
    ):
        if old not in text:
            raise ValueError(f"supporting-information {label} changed; refuse silent rendering")
        text = text.replace(old, new, 1)
    text = text.rstrip() + APPENDIX_S16 + APPENDIX_S17 + APPENDIX_S18 + "\n"
    lower = text.lower()
    if "cell-level simulation variation" in lower:
        raise ValueError("superseded within-cell-noise wording survived supporting-information render")
    if "chapter 3" in lower:
        raise ValueError("dissertation-specific Chapter 3 wording survived supporting-information render")
    required = (
        "69.34–80.17%",
        "64/96",
        "53/96",
        "partner arrival/replacement `2/25`",
        "# Appendix S17. Geography-first saturation and final world synthesis",
        "4,663",
        "42 research entries across 37 exact geographic labels",
        "# Appendix S18. Contemporary Izu functional-chain sensitivity",
        "+1.9426",
        "+2.0590",
        "+0.0353",
        "3 shorter / 4 longer / 1 unchanged",
    )
    for token in required:
        if token not in text:
            raise ValueError(f"required supporting-information token missing: {token}")
    return text


def render_to_path(output: Path = DEFAULT_OUTPUT) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_supporting_information(), encoding="utf-8")
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    print(render_to_path(args.output))


if __name__ == "__main__":
    main()
