from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs/ISLAND_ECOLOGY_JECOLOGY_SUBMISSION_DRAFT_V2_20260824.md"
DEFAULT_OUTPUT = ROOT / "dist/ISLAND_ECOLOGY_JECOLOGY_SUBMISSION_DRAFT_V3_20260826.md"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise ValueError(f"{label}: expected exactly one source block, found {count}")
    return text.replace(old, new, 1)


def build_text(source_text: str) -> str:
    text = source_text

    text = replace_once(
        text,
        "3. Mixed-sign branching occurred in 0.4167 of matched runs in both original and independent blocks, but disappeared when initial functional-position heterogeneity was removed. Local support changed 105/288 paired lineage response signs. Network context rescued reproductive sign in 16/96 eligible declines and attenuated 85/96, but worsened 11/96. Autonomous assurance attenuated 207/216 declines while producing no sign rescues in the independent block and none across a broadened 525-contrast envelope.",
        "3. Mixed-sign branching occurred in 0.4167 of matched runs in both original and independent blocks, but disappeared when initial functional-position heterogeneity was removed. At the frozen v12 endpoint, downstream transforms preserved response sign, so sign(Δ reproduction) = sign(Δ service) = sign(Δ functional opportunity). Local support changed 105/288 paired lineage response signs. Network context rescued reproductive sign in 16/96 eligible declines and attenuated 85/96, but worsened 11/96. Autonomous assurance attenuated 207/216 declines while producing no sign rescues in the independent block and none across a broadened 525-contrast envelope.",
        "abstract_h2",
    )

    text = replace_once(
        text,
        "5. **Synthesis.** Island-associated biotic simplification is better viewed as a common perturbation acting on different ecological starting states than as a force imposing one universal plant trajectory. Aggregate island syndromes can coexist with lineage-level branching because colonization and persistence shape which states arrive, whereas functional starting state, local interaction context and reproductive filters shape how established lineages respond.",
        "5. **Synthesis.** Island-associated biotic simplification is better viewed as a common perturbation acting on different ecological starting states than as a force imposing one universal plant trajectory. Aggregate island syndromes can coexist with lineage-level branching because colonization and persistence shape which states arrive, whereas functional starting state, local interaction context and downstream reproductive assurance shape how established lineages respond.",
        "abstract_synthesis",
    )

    text = replace_once(
        text,
        "This motivates a different island-ecology question from asking whether plants become more selfing, less specialized or morphologically simplified on average: **why does a common island-associated change in pollinator function produce different downstream responses among established plant lineages?** We considered three conditional layers within the post-establishment response itself. First, lineages occupy different positions in plant–pollinator functional space before the environment changes. Second, local interaction context determines how changed global opportunity is redistributed. Third, reproductive filters such as autonomous assurance change how service loss propagates into reproduction. The resulting ecological logic is summarized in Fig. 1.",
        "The unresolved problem is therefore not whether island floras show recurrent syndromes, but why **the same island-associated change in pollinator function can send already-established lineages in different directions**. Existing comparative work documents assembly bias and heterogeneous island evolution; it does not by itself identify the post-establishment response architecture that turns one perturbation into divergent lineage trajectories. We considered three conditional layers within that response. First, lineages occupy different positions in plant–pollinator functional space before the environment changes. Second, local interaction context determines how changed global opportunity is redistributed. Third, autonomous reproductive assurance changes how service loss propagates into reproduction. The resulting ecological logic is summarized in Fig. 1.",
        "intro_gap",
    )

    h2_methods_old = "The strongest boundary was tested once in an independent frozen block using seed 90260825, four replicates per saturation, 24 lineages, 120 steps and saturation values 1, 2 and 3. The decision rule and stop rule were specified before execution. The result was classified as `replicated_minimal_generator` only if the independent full residual block contained branching, initial functional-position heterogeneity OFF eliminated both branching and within-run branching balance, and at least one other single residual ablation retained branching. The first workflow attempt failed before scientific execution because of an import-path error; only that path was repaired, and the first successfully executed scientific result was retained. No further seed search was performed."
    h2_methods_new = h2_methods_old + "\n\nTo determine where response sign entered the frozen v12 endpoint, we also unpacked the model algebraically without changing any simulation. For lineage `i` in environment `g`, weighted functional opportunity was `O_i^g`, service was `S_i^g = 1 - exp(-sigma O_i^g)` with `sigma > 0`, and reproduction could be written `R_i^g = B_i + d(1 - B_i)S_i^g`. Within a matched mainland–island contrast, `d` and `B_i` were fixed and `d(1 - B_i) > 0`. Consequently, `sign(Delta R_i) = sign(Delta S_i) = sign(Delta O_i)`. This decomposition tests whether downstream transforms can create a sign reversal; it does not assign the synthetic functional coordinate to a named empirical trait."
    text = replace_once(text, h2_methods_old, h2_methods_new, "methods_h2_sign")

    h2_results_old = "The independent block reproduced the same boundary (Fig. 2; Table S1). Full-model mixed-sign frequency was 0.4167 with mean within-run balance 0.2917. Removing initial functional-position heterogeneity again reduced both quantities to zero and changed 44 paired lineage signs, whereas removing trait-adjustment heterogeneity or assurance-ceiling heterogeneity retained mixed-sign frequency 0.4167. Across two independently seeded frozen blocks, pre-existing lineage functional position was the only tested residual factor whose removal eliminated within-run response-sign branching. H2 was supported within the declared model."
    h2_results_new = h2_results_old + "\n\nThe analytical endpoint decomposition located the sign difference upstream of the service and reproduction transforms. Because both transforms were monotonic under the frozen v12 conditions, `sign(Delta reproduction) = sign(Delta service) = sign(Delta functional opportunity)`. Thus mixed-sign reproductive branching could not be manufactured downstream from a same-sign opportunity contrast; it had to be present already in lineage-specific functional-opportunity change."
    text = replace_once(text, h2_results_old, h2_results_new, "results_h2_sign")

    h2_disc_old = "The strongest mechanistic result is the replicated loss of branching when initial functional-position heterogeneity is removed. Response direction is therefore relational within the model: the effect of a changed pollinator environment depends not only on the perturbation but also on where a lineage already lies relative to functional opportunity."
    h2_disc_new = h2_disc_old + " The analytical decomposition makes that interpretation more precise: under the frozen v12 endpoint, the sign of the reproductive response is inherited from the sign of the functional-opportunity change because the downstream service and reproduction mappings are monotonic. The key state dependence therefore enters before those downstream filters, not as an artefact of them."
    text = replace_once(text, h2_disc_old, h2_disc_new, "discussion_h2_sign")

    text = replace_once(
        text,
        "Island-associated pollinator simplification is better viewed as a common perturbation acting on different ecological starting states than as a force imposing one universal post-establishment plant trajectory. In the frozen ABM, pre-existing lineage functional position is the replicated minimal generator of within-environment response branching. Local interaction context reallocates branch identity and can rescue or worsen propagation, whereas autonomous assurance mainly attenuates reproductive decline magnitude.",
        "Island-associated pollinator simplification is better viewed as a common perturbation acting on different ecological starting states than as a force imposing one universal post-establishment plant trajectory. In the frozen ABM, pre-existing lineage functional position is the replicated minimal generator of within-environment response branching, and the frozen endpoint algebra shows that response sign is inherited from lineage-specific functional-opportunity change rather than created by downstream transforms. Local interaction context reallocates branch identity and can rescue or worsen propagation, whereas autonomous assurance mainly attenuates reproductive decline magnitude.",
        "conclusion_h2",
    )

    return text


def build_manuscript(output: Path = DEFAULT_OUTPUT) -> Path:
    source_text = SOURCE.read_text(encoding="utf-8")
    rendered = build_text(source_text)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(rendered, encoding="utf-8")
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    path = build_manuscript(args.output)
    print(path)


if __name__ == "__main__":
    main()
