from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data/design/chapter2_oikos_submission_manifest_20260831.json"
REVIEW = ROOT / "data/results/chapter2_systematic_source_strengthening_wave11_audit_20260905.json"

ABSTRACT_SOURCE = (
    "We then confronted this vocabulary with a source-audited 25-entry island literature inventory and increased "
    "mechanistic resolution in Izu using source floral state, pollinator composition, raw matching and null-corrected matching."
)
RESULT_SOURCE = (
    "Existing studies were outcome-rich but process-poor: responses were directly measured in 21/25 entries, but partner "
    "arrival/replacement in only 2/25, and no entry supplied the full outcome-independent contract."
)
METHOD_SOURCE = (
    "The source-audited comparative universe contains 13 strict external state challenges and 12 additional analytical or "
    "model-development entries; these 25 research entries are not independent archipelagos."
)


def _replace_exact_once(text: str, old: str, new: str, label: str) -> str:
    if text.count(old) != 1:
        raise ValueError(f"{label} changed; expected exactly one source occurrence")
    return text.replace(old, new, 1)


def _counts() -> tuple[int, int, int, int]:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    review = json.loads(REVIEW.read_text(encoding="utf-8"))

    breadth = manifest["world_breadth_extension"]
    formal_entries = breadth["formal_identifiability_research_entries"]
    descriptive_entries = breadth["combined_descriptive_research_entries_before_cross_layer_deduplication"]
    exact_labels = breadth["combined_exact_overlap_labels_before_higher_level_archipelago_deduplication"]
    search_targets = review["effective_search_targets"]

    if formal_entries != 25:
        raise ValueError(f"formal identifiability denominator changed: expected 25, got {formal_entries}")
    if descriptive_entries != 39 or exact_labels != 34:
        raise ValueError(
            f"manuscript-facing breadth changed: expected 39 entries / 34 labels, got {descriptive_entries}/{exact_labels}"
        )
    completion = review["source_work_state_after_wave11"]
    if search_targets != 111:
        raise ValueError(f"systematic search frame changed: expected 111, got {search_targets}")
    if completion["targets_requiring_additional_source_work"] != 0:
        raise ValueError("systematic source review is not complete; refuse submission overlay")
    if not completion["source_review_complete_under_current_protocol"]:
        raise ValueError("systematic source review completion flag is false")
    if not completion["reopen_if_new_source_found"]:
        raise ValueError("terminal source states must remain reopenable")
    if review["wave11"]["global_confrontation_candidates_after_review"] != 0:
        raise ValueError("wave 11 unexpectedly created confrontation candidates")
    if review["full_contract_result"]["systematic_extension_creates_full_contract"]:
        raise ValueError("systematic review unexpectedly created a full external contract")

    claims = manifest["claim_ceiling"]
    if claims["formal_external_prediction"] != "not_evaluable" or claims["external_full_contracts"] != "0_of_25":
        raise ValueError("formal prediction/full-contract boundary changed")

    return search_targets, descriptive_entries, exact_labels, formal_entries


def apply_systematic_review_overlay(text: str) -> str:
    search_targets, descriptive_entries, exact_labels, formal_entries = _counts()

    abstract = (
        f"We then screened a systematic {search_targets}-target island frame, retained {descriptive_entries} source-backed "
        f"research entries for global confrontation, audited mechanism identifiability in a frozen {formal_entries}-entry subset, "
        "and increased resolution in Izu using source floral state, pollinator composition, raw matching and null-corrected matching."
    )
    results = (
        f"The systematic search was review-complete, but the frozen {formal_entries}-entry audit remained outcome-rich and process-poor: "
        "responses were directly measured in 21/25 entries, partner arrival/replacement in 2/25, and none supplied the full "
        "outcome-independent contract."
    )
    methods = (
        f"The world layer separates three denominators. A systematic search frame contains {search_targets} named geographic targets, "
        "each with a documented review state under a reopenable terminal-gap rule; this is a search frame, not a census of all islands "
        f"or {search_targets} independent tests. The admitted descriptive confrontation contains {descriptive_entries} source-backed "
        f"research entries across {exact_labels} exact geographic labels. A frozen {formal_entries}-entry subset—13 strict external state "
        "challenges plus 12 additional analytical or model-development entries—supplies the direct-measurement audit used for formal "
        "identifiability. Terminal source gaps are literature states, not biological absences."
    )

    text = _replace_exact_once(text, ABSTRACT_SOURCE, abstract, "Abstract world denominator sentence")
    text = _replace_exact_once(text, RESULT_SOURCE, results, "Abstract/Results identifiability sentence")
    text = _replace_exact_once(text, METHOD_SOURCE, methods, "Methods world denominator sentence")

    lower = text.lower()
    required = (
        f"systematic {search_targets}-target island frame",
        f"{descriptive_entries} source-backed research entries",
        f"frozen {formal_entries}-entry subset",
        f"{exact_labels} exact geographic labels",
        "terminal source gaps are literature states, not biological absences",
        "not a census of all islands",
    )
    missing = [token for token in required if token not in lower]
    if missing:
        raise ValueError(f"systematic-review submission wording disappeared: {missing}")

    return text
