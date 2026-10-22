"""Build a source-hashed CURRENT Chapter 2 author-review packet (no biology).

This deliberately supersedes the *review-export route* of historical EL/JE ZIPs,
not their preserved contents, and is NOT a journal submission or DOI deposit.
"""
from __future__ import annotations

import argparse
from hashlib import sha256
import io
import json
from pathlib import Path
import re
import zipfile

ROOT = Path(__file__).resolve().parents[1]
TITLE = "Reproductive assurance differentially affects floral genetic accessibility and persistence under pollinator limitation"
MAIN = "docs/CHAPTER2_NEE_SUPPORTED_RESULTS_ARTICLE_EXTRACT_20261019.md"
SUPPLEMENT = "docs/CHAPTER2_COMPLETED_EVIDENCE_SUPPLEMENT_20261019.md"
FOLDER = "figures/chapter2_nee"
FIGURES = tuple(f"{FOLDER}/figure_{n:02d}_{suffix}.svg" for n, suffix in [
    (1, "q1_mechanism"), (2, "baseline_pollen"),
    (3, "sequence_realization"), (4, "access_survival"),
    (5, "variation_duration"), (6, "late_transfer"),
])
EXTRA = (
    "docs/CHAPTER2_PAPER_CLOSURE_20261020.md",
    "docs/CHAPTER2_CLOSEST_PRIOR_ART_PRIMARY_AUDIT_20261020.md",
    "docs/CHAPTER2_CONCLUSION_CODE_REVIEW_20261020.md",
    "docs/CHAPTER2_HITCHHIKING_SECONDARY_EXPANSION_REVIEW_20261020.md",
    "docs/CHAPTER2_CONFIRM160_RESULTS_20261019.md",
    "docs/CHAPTER2_READAPTATION_RESULTS_20261019.md",
    "docs/audits/CHAPTER2_CONFIRM160_COMPACT_RESULTS_20261019.json",
    f"{FOLDER}/README.md",
)
ALL = (MAIN, SUPPLEMENT, *FIGURES, *EXTRA)
ABSTRACT_MAX = 200
BODY_MAX = 3500
EXPECTED_STATUS = "AUTHOR_REVIEW_ONLY_NOT_SUBMISSION_READY"


def words(s: str) -> int:
    return len(s.split())


def check_manuscript(raw: bytes) -> dict:
    t = raw.decode("utf-8")
    if not t.startswith("# " + TITLE + "\n"):
        raise ValueError("current completed-evidence manuscript title mismatch")
    headings = ("## Abstract\n", "## Introduction\n", "## Results\n",
                "## Discussion\n", "## Online Methods", "## Figure legends",
                "## Data availability\n", "## References")
    starts = [t.find(k) for k in headings]
    if any(p < 0 or t.count(k) != 1 for p, k in zip(starts, headings)):
        raise ValueError("missing or duplicated completed-only manuscript boundary")
    if starts != sorted(starts):
        raise ValueError("manuscript sections out of order")
    if "## Planned new decisive Results" in t or "## Planned new" in t:
        raise ValueError("historic unexecuted results entered current export")
    abstract = t[starts[0] + len(headings[0]):starts[1]]
    main = t[starts[1] + len(headings[1]):starts[4]]
    a_words, m_words = words(abstract), words(main)
    if not 100 <= a_words <= ABSTRACT_MAX or not 2500 <= m_words <= BODY_MAX:
        raise ValueError(f"author-review word bounds: abstract {a_words}, main {m_words}")
    legends = t[starts[5]:starts[6]]
    nums = [int(n) for n in re.findall(r"(?m)^\d+\.\s+\*\*Figure\s+(\d+)\b", legends)]
    if nums != list(range(1, 7)):
        raise ValueError(f"expected exactly six current Figure legends, got {nums}")
    for key in ("8.33", "92.71", "25,600", "fixed A", "secondary colonization"):
        if key.lower() not in t.lower():
            raise ValueError("required evidence/interpretation missing: " + key)
    return dict(abstract_whitespace_words=a_words,
                main_whitespace_words_including_headings=m_words,
                main_figure_count=6)


def check_results(raw: bytes) -> dict:
    d = json.loads(raw)
    try:
        cases = d["crossings"]
        arms = d["arms"]
        e = {x["name"]: x for x in d["primary"]["endpoints"]}
        genetic, demographic = e["genetic_loss"], e["survival_interaction"]
        if (cases != 25600 or d["independent_axes"] != [160, 160]
                or arms["fixed_B8"]["alive"] != cases
                or arms["evolving_B8"]["alive"] != cases
                or arms["fixed_B4p5"]["alive"] != 1385
                or arms["evolving_B4p5"]["alive"] != 25118
                or abs(genetic["estimate"] - 0.08328125) > 1e-10
                or abs(demographic["estimate"] - 0.9270703125) > 1e-10
                or not d["primary"]["joint_positive"]
                or d["primary"]["both_exceed_margin"]
                or d.get("actual_restoration_tested") is not False):
            raise ValueError("frozen registered scientific result does not match")
    except (KeyError, TypeError) as exc:
        raise ValueError("incomplete registered scientific readout") from exc
    return dict(crossed_cells=cases, independent_axes=[160, 160],
                G_high_I_support_loss_difference_pp=genetic["estimate"] * 100,
                G_adjusted_97p5_pp=[v * 100 for v in genetic["interval"]],
                S_policy_by_budget_survival_interaction_pp=demographic["estimate"] * 100,
                S_adjusted_97p5_pp=[v * 100 for v in demographic["interval"]],
                B8_every_population_occupied=True,
                B4p5_survival_fixed=1385,
                B4p5_survival_evolving=25118,
                registered_effects_do_not_identify_mediation=True)


def collect(root: Path, source_commit: str = "UNKNOWN") -> tuple[dict, dict]:
    root = Path(root)
    members = {}
    for name in ALL:
        p = root / name
        if not p.is_file():
            raise ValueError("missing source-bound author-review member " + name)
        raw = p.read_bytes()
        if not raw:
            raise ValueError("empty author-review member " + name)
        members[name] = raw
    for path in FIGURES:
        s = members[path].decode("utf-8")
        if "<svg" not in s or "</svg>" not in s or "<metadata" not in s:
            raise ValueError("invalid source-marked SVG: " + path)
    counts = check_manuscript(members[MAIN])
    inference = check_results(members["docs/audits/CHAPTER2_CONFIRM160_COMPACT_RESULTS_20261019.json"])
    manifest = dict(schema="izu_core_chapter2_current_author_review_v1",
                    status=EXPECTED_STATUS,
                    source_commit=source_commit,
                    source_master=MAIN, secondary_source=SUPPLEMENT,
                    figures=list(FIGURES),
                    manuscript_counts=counts,
                    registered_evidence_check=inference,
                    source_files={
                        name: {"sha256": sha256(raw).hexdigest(), "bytes": len(raw)}
                        for name, raw in sorted(members.items())
                    },
                    excluded=["unexecuted recovery-window plans", "new simulations",
                              "historical 2026-10-10 EL/JE review ZIPs",
                              "journal submission assertions", "DOI assertions"],
                    cautions=[
                        "Author-review source bundle, not submitted or anonymously formatted.",
                        "SVGs remain source-checked DRAFT artwork, not journal-approved.",
                        "Relative research links in markdown require the full GitHub source tree.",
                        "Late transfer and secondary colonization do not identify adaptation.",
                        "No biological simulations, new significance tests or new inferential units."
                    ])
    return members, manifest


def assemble(root: Path, source_commit: str = "UNKNOWN") -> bytes:
    members, manifest = collect(root, source_commit)
    readme = (
        "# CURRENT Chapter 2 — author review only\n\n"
        "Main manuscript: " + MAIN + "\n"
        "Completed-evidence supplement: " + SUPPLEMENT + "\n\n"
        "This ZIP is NOT the historical EL/JE package, not anonymous submission "
        "material, not final figure artwork and not a DOI deposit.\n\n"
        "The paper's supported question: reproductive assurance changes "
        "the retention of founder-target-compatible floral investment alleles "
        "and population persistence differently under the sampled model conditions.\n"
        "A hypothetical island-to-mainland secondary migration is a FUTURE "
        "generality question, not an experimentally established natural result.\n"
        "Use MANIFEST.json to check exact bytes and science-status boundaries.\n"
    )
    members["README_AUTHOR_REVIEW.md"] = readme.encode("utf-8")
    members["MANIFEST.json"] = (json.dumps(
        manifest, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for name, content in sorted(members.items()):
            info = zipfile.ZipInfo(name, date_time=(2020, 10, 20, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (0o644 & 0xFFFF) << 16
            z.writestr(info, content, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    return buf.getvalue()


def publish(root: Path, out: Path, source_commit: str = "UNKNOWN") -> dict:
    out = Path(out)
    checksum = out.with_suffix(out.suffix + ".sha256")
    if out.exists() or checksum.exists() or out.resolve() == (Path(root) / MAIN).resolve():
        raise ValueError("refusing to overwrite publication evidence or review packet")
    output = assemble(root, source_commit=source_commit)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(output)
    digest = sha256(output).hexdigest()
    checksum.write_text(digest + "  " + out.name + "\n", encoding="utf-8")
    return dict(status=EXPECTED_STATUS, path=str(out), sha256=digest,
                bytes=len(output), sidecar=str(checksum))


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", type=Path, default=ROOT)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--source-commit", default="UNKNOWN")
    args = p.parse_args()
    print(json.dumps(publish(args.root, args.out, args.source_commit), indent=2))


if __name__ == "__main__":
    main()
