from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "dist/SUPPORTING_INFORMATION.md"

APPENDIX_S1 = """

# Appendix S1. Geography-first saturation and final world synthesis

The frozen 25-entry identifiability audit was not expanded after outcomes were inspected. A separate geography-first audit was instead used to test whether the response/process vocabulary or the measurement bottleneck changed when the search frame no longer began from the literature-built target list.

The independent starting artifact contained `4,663` candidate island polygons at least 20 km2. Raw polygons were grouped into archipelago or biogeographically coherent system units before literature review so that multiple nested islands did not automatically create independent replication. Search rows remained descriptive/saturation evidence and were never silently promoted into the formal prediction denominator.

In the first 20 omitted systems, direct plant response was recoverable in `10/20`, breeding or assurance information in `9/20`, realized-community/process contrast in `7/20`, and local filtering in `2/20`. Direct historical partner loss was `0/20`, direct partner arrival/replacement was `0/20`, and full matched contracts were `0/20`. Continued breadth therefore added contemporary states more readily than historical transition coordinates.

The stopping rule required two consecutive eligible geography-first tranches with no new response state, process state, falsification role, direct historical partner loss/arrival measurement or full contract. The counter was reset when a later Gulf of California tranche added a historical/ploidy alternative mechanism in *Pachycereus pringlei*. The following two eligible tranches added no new state and no full contract, satisfying the declared `2/2` large-island saturation rule.

A mandatory <20 km2 supplement then reviewed eight preselected small-island systems. Tiritiri Matangi supplied a documented pollinator reintroduction linked to a direct functional pollination experiment, while Surtsey supplied a bounded empty-island founding/colonization chronology. Across the eight systems, direct historical partner loss was `0/8`, direct arrival/reintroduction `1/8`, and full contracts `0/8`.

The final world synthesis therefore retained only distinct mechanistic roles rather than every searched island: Surtsey for dated founding chronology, Tiritiri Matangi for documented reintroduction plus functional testing, and Gulf of California *Pachycereus* for a historical/ploidy alternative and failure of a simple current-pollinator-abundance explanation. The separate descriptive breadth is `42 research entries across 37 exact geographic labels`; the formal identifiability denominator remains `25 research entries across 21 exact labels`, full contracts remain `0/25`, and formal external prediction remains `not_evaluable`.
"""

APPENDIX_S2 = """

# Appendix S2. Contemporary Izu functional-chain sensitivity

## S2.1 FDQ to corrected trait matching

A transparent source-native sensitivity model used `TM_z ~ FDQ + FEve + site fixed effects + season fixed effects`. The FDQ coefficient was `+1.8346` across all eight source sites, `+1.5414` across the three mainland sites, `+1.9426` across the five Izu islands, and `+2.0590` within Niijima, Kozu, Miyake and Hachijo alone. The five-island leave-one-island range was `+1.4320 to +2.2257`; the post-Oshima four-island range was `+1.4561 to +2.3325`. Every coefficient in both island omission sets remained positive.

The archived pollinator table contained zero recorded *Bombus* species × site × season rows in the four-island post-Oshima subset. This is a sampled-network statement, not proof of biological absence. The result shows that continuous contemporary pollinator functional structure contains explanatory variation within the sampled post-Oshima networks and should not be reduced to a binary sampled-*Bombus* label.

## S2.2 Corrected trait matching to pollen receipt

Pollen observations were first aggregated to plant × site × season means because `TM_z` is shared within site × season. The fixed-effect coefficient of `TM_z` was `+0.0295` across all eight sites, `+0.0468` on the mainland, `+0.0353` across Izu5 and `+0.0342` across post-Oshima4.

Site × season clustered CR1 uncertainty was broad: the Izu5 coefficient was `+0.0353` with 95% t interval `−0.0314 to +0.1019`; the post4 coefficient was `+0.0342` with interval `−0.0510 to +0.1194`. All four geographic-subset intervals included zero. The downstream association is therefore positive in point estimate but not estimated as a precise geographically stable coefficient.

Omission diagnostics localize the fragility to network state rather than one plant taxon. In both Izu5 and post4, all nine estimable leave-one-plant models remained positive; one *Oxalis corniculata* var. *trichocaulon* omission was non-estimable because the fixed-effect design became singular. Leaving out Hachijo or season 3 reversed the island-only coefficient. For Izu5, all `24/24` estimable leave-one-site-season coefficients remained positive. For post4, `18/19` remained positive; the single reversal occurred when `Hachijo × season 3` was omitted.

## S2.3 Cross-channel response branching

Eight source-defined Oshima-to-post plant targets had all three contrasts available. Corrected trait matching was lower post-Oshima in `8/8`. Floral-tube response split into `3 shorter / 4 longer / 1 unchanged`, and pollen receipt split into `4 lower / 4 higher`. Only `2/8` targets showed the complete `matching lower + tube shorter + pollen lower` combination.

These eight plants share island environments and are not eight independent boundary experiments. Their supported role is response-branching evidence: a common decline in corrected matching does not imply one downstream morphology or pollen direction.

The contemporary evidence therefore has a hierarchy. `FDQ -> corrected matching` is the robust upstream association; `matching -> pollen` is positive on average but cluster-uncertain and network-state sensitive; morphology and pollen responses branch further downstream. None of these associations identifies historical *Bombus* loss, historical selection, causal mediation or a completed visitor-effectiveness/dependency chain.
"""



APPENDIX_S3 = """

# Appendix S3. Unified Model 3 projection onto real-island evidence

The current manuscript no longer assigns natural island systems to synthetic `k`, S/C/I regimes or response-geometry classes. Instead, source-locked systems are evaluated against three nested Model 3 layers:

- **A — ecological/selection:** starting plant state × visitor functional composition/access/effectiveness and immediate reproductive return;
- **B — deterministic inheritance:** inherited longitudinal response under a measured visitor regime, with demographic sampling conceptually separated;
- **C — finite/history realization:** assurance, chronology, connectivity, founding, recovery and demographic persistence.

The existing propagation matrix contains 14 biological system layers across 12 geographic clusters. Their descriptive states are: same-direction propagation 1, downstream branching 2, buffered/resilient 3, counterdirectional 1, adjacent links only 4 and unresolved missing link 3. These counts are not prevalence estimates because the rows are heterogeneous and not independent geographic replicates.

Izu is the clearest current branching example. Corrected matching is lower in all eight shared Oshima-to-post targets, whereas pollen response is `4 lower / 4 higher` and tube response is `3 shorter / 4 longer / 1 unchanged`. Ogasawara *Psychotria homalosperma* provides a stronger same-direction A-layer chain from morph-specific access through directional pollen flow to reproductive asymmetry. Xisha *Cordia subcordata* is a near-complete A-to-reproduction example but has asymmetric measurement across the two islands. Hawaii lobelioids and Puerto Rico–Mona *Guaiacum* provide buffering examples, whereas the frozen Dominica *Heliconia* signed-position prediction is retained as a counterdirectional falsifier.

For the C layer, Surtsey supplies dated empty-start founding chronology, Tiritiri Matangi supplies documented pollinator reintroduction with compensatory function, and New Zealand *Rhabdothamnus* and Mariana bird-loss systems link direct partner loss to reproductive or recruitment consequences.

The principal natural-data gap is B. The current archive does not contain a clean longitudinal system with measured starting genetic/common-garden trait state, measured visitor regime, inherited trait/genotype change through time and enough demographic information to distinguish expected selection from finite-population realization.

The broader `42 research entries across 37 exact geographic labels` remains a breadth and falsification layer, not 42 Model 3 fits. The formal source audit remains `21/25` direct comparable plant responses, `2/25` direct partner arrival/replacement measurements and `0/25` complete A -> B -> C contracts.

This re-projection is descriptive and source-locked. It does not calibrate Model 3, estimate branch prevalence, identify historical *Bombus* causation or turn cross-sectional morphology into an inherited evolutionary trajectory.
"""


APPENDIX_S4 = """

# Appendix S4. Prospective Model 3 isolation bridge

The bridge design and interpretation rules were frozen before production outcomes were inspected. Production completed successfully in GitHub Actions workflow run `36311030639` with `24,576` verified cases, `128` independent visitor histories and `16` deterministic execution shards. The frozen compact result is `data/results/model3_ch2_bridge_prospective_frozen_20260927.json`.

The endpoint is the paired far-minus-near difference in terminal-minus-initial inherited floral investment. All three predeclared deadbands (`0`, `0.01`, `0.05`) are retained.

## S4.1 Natural isolation-driven assembly

The finite ABM mean far-minus-near effect is `-0.1446` (95% history-cluster bootstrap interval `-0.1588 to -0.1306`), whereas the conditional deterministic genotype-density closure is `-0.4510` (`-0.4716 to -0.4301`). The density closure is not the stochastic mean of the finite ABM, so their magnitude gap is not interpreted as a finite-population attenuation coefficient. Finite-ABM mixed-history counts are `12/128`, `8/128` and `1/128` across the three deadbands; deterministic density is `0/128` at all three.

## S4.2 Annual response-blind realized-richness matching

Annual thinning makes near and far visitor counts identical before reproduction. The mean effect reverses from negative to positive: finite ABM `+0.0333` (`0.0245 to 0.0425`) and deterministic density `+0.0338` (`0.0236 to 0.0444`). Finite-ABM mixed histories become `68/128`, `59/128` and `18/128`; deterministic density gives `16/128`, `1/128` and `0/128`.

This intervention also changes visitor identity persistence and therefore is not a pure natural species-richness manipulation.

## S4.3 Finite visitor-environment sampling

Pooling eight independent visitor histories with count-scaled activity normalization eliminates mixed history-level branches in both finite ABM and deterministic density at all three deadbands. Finite-ABM mean effect is `-0.2259`; deterministic-density mean effect is `-0.5560`.

Pooling changes environmental averaging and functional composition under a nonlinear reproductive operator. It is not an island-count or lifespan manipulation.

## S4.4 Finite plant demography

Increasing plant capacity from `48` to `192` while retaining the natural visitor history reduces finite-ABM mixed histories from `12` to `1` at deadband 0, from `8` to `1` at 0.01 and from `1` to `0` at 0.05. The mean effect moves from `-0.1446` to `-0.2716`, numerically closing approximately `41.5%` of the trait-effect gap to the deterministic density closure. This 41.5% is descriptive only and is not interpreted as convergence to a stochastic expectation or as a finite-size attenuation coefficient.

Thus visitor-environment realization and finite plant demography are separable manipulated axes that modify observed directional heterogeneity; these finite-repeat labels do not identify stable latent branch prevalence. The density closure is used as a comparator, not as the finite model's expected trajectory.

## S4.5 S/C/I is not directional branching

The visitor-pooled finite ABM has a descriptive interaction share `I = 0.542` while showing `0/128` mixed-sign histories. S/C/I therefore summarizes magnitude structure and cannot be used as a proxy for directional evolutionary branching.

These are synthetic model-conditional results. Mixed fractions are descriptive history labels, not natural prevalence; model time, distance and trait coordinates are not calibrated field quantities.
"""


def render_supporting_information() -> str:
    """Render the current Model 3 / natural-confrontation Supporting Information."""
    header = """# Supporting Information — Model 3 pollination-to-evolution pathway

This Supporting Information contains only material supporting the active Model 3 paper and its source-audited natural confrontation. Retired Model 2, synthetic-k, S/C/I, Gaussian-limit and response-rule analyses are legacy provenance and are excluded.

"""
    text = header + APPENDIX_S1 + APPENDIX_S2 + APPENDIX_S3 + APPENDIX_S4 + "\n"
    lower = text.lower()
    required = (
        "# appendix s1. geography-first saturation and final world synthesis",
        "4,663",
        "42 research entries across 37 exact geographic labels",
        "# appendix s2. contemporary izu functional-chain sensitivity",
        "+1.9426",
        "+0.0353",
        "3 shorter / 4 longer / 1 unchanged",
        "# appendix s3. unified model 3 projection onto real-island evidence",
        "same-direction propagation 1",
        "`0/25` complete a -> b -> c contracts",
        "# appendix s4. prospective model 3 isolation bridge",
        "24,576",
        "68/128",
        "pooling eight independent visitor histories",
        "41.5%",
        "descriptive only",
    )
    for token in required:
        if token.lower() not in lower:
            raise ValueError(f"required current-SI token missing: {token}")
    forbidden = (
        "appendix s19",
        "finite-community system-size audit",
        "gaussian mean-field limit",
        "regime-dependent response hierarchy under active plant adjustment",
        "synthetic-k finite-community pooling",
        "prespecified relational-robustness audit",
    )
    for token in forbidden:
        if token in lower:
            raise ValueError(f"legacy material leaked into current SI: {token}")
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
