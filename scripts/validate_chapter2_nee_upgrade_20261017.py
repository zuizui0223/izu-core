"""Single active NEE *development* route, source evidence and format guards.

This is an editorial scientific-evidence validator. It neither runs original
biology nor declares the NEE restoration core to have been executed. It leaves
the historical EL full-fidelity reproduction selector and raw data untouched.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROUTE = "docs/audits/CHAPTER2_NEE_ACTIVE_PUBLICATION_ROUTE_20261017.json"
OLD = "data/design/chapter2_one_paper_route_20261010.json"
NEE_ABSTRACT_HEAD = "## Abstract — provisional, existing evidence only; NOT for submission"
NEE_INTRO_HEAD = "## Introduction"
NEE_METHODS_HEAD = "## Online Methods"
NEE_RESULTS_HEAD = "## Results — existing source-admitted evidence"
NEE_PENDING_HEAD = "## Planned new decisive Results — PENDING, not observations"
NEE_FIGURES_HEAD = "## Six proposed display items — no unsourced new figures"
SOURCE_CASES = {
    "q1": "data/results/chapter2_assurance_generality_20261006.json",
    "sequence": "data/results/chapter2_1005_confirmatory_replication_20261006.json",
    "q2": "docs/audits/CHAPTER2_Q2_I_SUPPORT_384_ORIGINAL_READOUT_20261016.json",
    "q3": "data/results/directional_access_20261013/READOUT.json",
    "q4": "data/results/chapter2_island_demographic_independent32_20261008.json",
}


class NEEUpgradeMismatch(ValueError):
    pass


def require(v, msg):
    if not v:
        raise NEEUpgradeMismatch(msg)


def count(text):
    return len(text.split())


def split_once(t, start, end):
    require(t.count(start) == 1 and t.count(end) == 1,
            "NEE abstract/body boundary is missing or duplicated")
    return t.split(start, 1)[1].split(end, 1)[0]


def read_json(root, path):
    return json.loads((root / path).read_text(encoding="utf-8"))


def validate(root: Path = ROOT):
    route = read_json(root, ROUTE)
    old = read_json(root, OLD)
    require(route["status"] == "NEE_ARTICLE_CANDIDATE_UNDER_DEVELOPMENT_NO_SUBMISSION",
            "wrong current NEE editorial route")
    require(route["effective_active_paper_count"] == 1 and route["article_type"] == "Article"
            and route["target_journal"] == "Nature Ecology & Evolution",
            "one NEE article is not selected")
    require(route["ready_for_nee_submission"] is False
            and route["no_current_submission"] is True
            and route["no_new_biological_run_from_this_route"] is True,
            "unrun recoverability may not be promoted to submission")
    require(route["active_manuscript"].startswith("docs/CHAPTER2_UNIFIED_NEE_ARTICLE_"),
            "current manuscript is not unified NEE")
    require(route["active_manuscript"] not in
            route["previous_el_surfaces_retained_for_reproduction_not_current_submissions"],
            "NEE and archived EL manuscript cannot be the same active file")
    require(old["research_format"] == "ecology_letters_letter"
            and old["active_manuscript"] in
            route["previous_el_surfaces_retained_for_reproduction_not_current_submissions"],
            "historical EL reproduction route must remain available")
    require("NEE" in route["status"] and "Chapter 3" in route["scope"],
            "historical separate-paper framing was not superseded")
    target = root / route["active_manuscript"]
    manuscript_raw = target.read_bytes()
    text = manuscript_raw.decode("utf-8")
    require(text.startswith("# Predictability and genetic constraints in plant evolution under pollinator limitation"),
            "NEE manuscript wrong title")
    for boundary in (NEE_ABSTRACT_HEAD, NEE_INTRO_HEAD, NEE_RESULTS_HEAD,
                     NEE_PENDING_HEAD, NEE_METHODS_HEAD, NEE_FIGURES_HEAD):
        require(text.count(boundary) == 1, "current NEE manuscript missing boundary " + boundary)
    require(text.index(NEE_ABSTRACT_HEAD) < text.index(NEE_INTRO_HEAD)
            < text.index(NEE_RESULTS_HEAD) < text.index(NEE_PENDING_HEAD)
            < text.index("## Discussion") < text.index(NEE_METHODS_HEAD)
            < text.index(NEE_FIGURES_HEAD), "NEE sections are in the wrong order")
    abstract = split_once(text, NEE_ABSTRACT_HEAD, NEE_INTRO_HEAD)
    main = split_once(text, NEE_INTRO_HEAD, NEE_METHODS_HEAD)
    bounds = route["article_guidelines"]
    require(100 <= count(abstract) <= bounds["abstract_max_words"],
            "NEE Article abstract out of scope")
    require(700 <= count(main) <= bounds[
            "main_text_max_words_excluding_abstract_methods_references_figure_legends"],
            "NEE Article main body out of scope")
    fig = split_once(text, NEE_FIGURES_HEAD, "## Data accessibility")
    figures = re.findall(r"(?m)^(\d+)\.\s+\*\*Figure\s+(\d+)\b", fig)
    require(len(figures) == 6 and len(figures) <= bounds["display_items_max"]
            and [(int(a), int(b)) for a, b in figures] == [(i, i) for i in range(1, 7)],
            "NEE display figure cap or numbering invalid")
    require("NOT EXECUTED" in text and text.count("**NOT EXECUTED.**") >= 4
            and "PENDING" in NEE_PENDING_HEAD and route["ready_for_nee_submission"] is False,
            "missing explicit unobserved main recoverability results")
    for required in (
        "51/64", "30/64", "703 histories",
        "+0.1083984375", "+0.15234375",
        "both were inconclusive",
        "HIGH-I", "LOW-I", "3/32 and 2/32",
        "no I-locus mutation or seed immigration",
        "NOT A SUBMISSION-READY ARTICLE",
        "geological age", "NEE",
    ):
        require(required.lower() in text.lower(), "NEE scientific source boundary missing " + required)
    q1 = read_json(root, SOURCE_CASES["q1"])
    s = read_json(root, SOURCE_CASES["sequence"])
    q2 = read_json(root, SOURCE_CASES["q2"])
    q3 = read_json(root, SOURCE_CASES["q3"])
    q4 = read_json(root, SOURCE_CASES["q4"])
    require(q1["adjudication"]["n_passed"] == 4
            and q1["independent_visitor_histories"] == 64,
            "original registered four-condition model result differs")
    require(s["primary_sequence"]["counts"]["assurance_first"] == 51,
            "original 51/64 primary chronology changed")
    require(q2["registered_inference"]["result"] == "both_inconclusive"
            and all(v["excludes_zero"] is False for v in q2["coprimary"].values()),
            "do not promote the 384-source co-primary results")
    require(q3["cases"] == 2304 and q3["excluded_before_fixation"] == 703,
            "old LOW-I exclusion source does not match")
    require(abs(q4["predeclared_pooled_primary"]["mean"] - .1083984375) < 1e-15,
            "original Q4 pooled interaction differs")
    require(abs(next(x for x in q4["per_setting"]
                     if x["setting"] == "delayed_control")["interaction"]
                - .15234375) < 1e-15,
            "delayed-only stress effect no longer identifiable")
    return {
        "schema": "chapter2_nee_one_paper_evidence_and_format_gate_v1",
        "status": "PASS_EDITORIAL_NEE_DEVELOPMENT_ONLY",
        "journal_target": route["target_journal"],
        "article_type": "Article",
        "effective_active_paper_count": 1,
        "content_sha256": hashlib.sha256(manuscript_raw).hexdigest(),
        "source_abstract_whitespace_words": count(abstract),
        "source_main_whitespace_words_excluding_online_methods": count(main),
        "planned_display_figures": len(figures),
        "old_el_renderer_is_historical_only": True,
        "all_original_registered_results_modified": False,
        "restoration_experiment_executed": False,
        "external_island_prediction_confirmed": False,
        "external_raw_doi_deposited": False,
        "submission_ready": False,
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", type=Path, default=ROOT)
    args = p.parse_args()
    print(json.dumps(validate(args.root), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
