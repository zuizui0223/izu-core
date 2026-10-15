"""Q2 renewal standing-support and Price-accounting SI integration checks.

The actual 2304 native histories and 460800 births are pre-existing, preserved
externally, and checked by independent original-array readers. These tests
only inspect committed original scientific receipts and prose; no biology.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SI=ROOT/"docs/CHAPTER2_UNIFIED_EL_SUPPORTING_INFORMATION_20261010.md"
RENEWAL=ROOT/"docs/ECOLOGICAL_INVESTMENT_RENEWAL_RESULTS_20261015.md"
STANDING=ROOT/"docs/CHAPTER2_RENEWAL_STANDING_ACCESS_RESULTS_20261015.md"
NONRESPONSE=ROOT/"docs/CHAPTER2_RENEWAL_NONRESPONSE_ACCOUNTING_RESULTS_20261015.md"
PRICE=ROOT/"docs/CHAPTER2_FAR_ASSURANCE_ORIGINAL_GENOME_PRICE_AUDIT_20261015.md"
READBACK=ROOT/"data/results/ecological_I_renewal_20261015/PUBLIC_READBACK.json"
ROUTE=ROOT/"data/design/chapter2_one_paper_route_20261010.json"


def _section(text,n):
    key=f"## S{n}."
    assert text.count(key)==1, key
    section=text.split(key,1)[1]
    return section.split(f"## S{n+1}.",1)[0]


def _table(doc,marker):
    text=doc.split(marker,1)[1]
    result=[]
    for line in text.splitlines():
        if line.startswith("| main |") or line.startswith("| confirmation |"):
            result.append([p.strip() for p in line.strip().strip("|").split("|")])
        elif result and not line.startswith("|"):
            break
    return result


def test_complete_original_renewal_archive_without_new_simulations():
    d=json.loads(READBACK.read_text(encoding="utf-8"))
    assert d["status"]=="PUBLIC_RAW_DOWNLOAD_ALL6956_MEMBERS_BYTE_IDENTICAL"
    assert (d["members_verified"],d["bytes"])==(6956,681891056)
    assert d["archive_sha256"]=="6977676f2d855e980a6ca8ed9f853abd4a08769f0a150e732ff645dd50f998e1"
    assert d["source_freeze_sha256"]=="97435b5aa1d0072d7ad4b2ea050ab323366d74425e640cfee32cca54be8f97b7"
    assert d["readout_sha256"]=="9251c9a78f3790648bd8041d9ae8bebe244a9dd673c1893776114db86c7c8776"
    assert d["new_biological_updates"]==0
    assert "All2,304 new200-update paths" in RENEWAL.read_text()
    assert "Every simultaneous interval includes0." in RENEWAL.read_text()
    assert "Original source-freeze" not in (ROOT/"scripts/audit_renewal_nonresponse_accounting_20261015.py").read_text()[:400]


def test_s30_standing_reopening_remains_distinct_from_realized_event_and_test():
    txt=SI.read_text(encoding="utf-8")
    x=_section(txt,30)
    s=STANDING.read_text(encoding="utf-8")
    assert "2,304 new histories" in x
    assert "1,246/2,304" in x and "1,138/2,304" in x
    assert "All **18 simultaneous cell intervals include zero**" in x
    assert "1,238" in x and "1,214" in x
    assert "914" in x and "758" in x and "64" in x and "92" in x
    assert "4,868" in x
    assert "968" in x and "278" in x and "170" in x and "888" in x
    assert "not equivalence" in x or "not equivalence" in x.lower()
    assert "Paired event table:968 present in both arms,278 renewal-only,170 original-only,888 neither." in s
    rows=_table(s,"## All18 unpooled cells")
    assert len(rows)==18
    assert sum(int(r[4]) for r in rows)==914
    assert sum(int(r[5]) for r in rows)==92
    assert sum(int(r[6]) for r in rows)==1138
    assert sum(int(r[7]) for r in rows)==1246


def test_s31_original_birth_reconstruction_and_selected_path_classes():
    si=SI.read_text(encoding="utf-8")
    s=_section(si,31)
    source=NONRESPONSE.read_text(encoding="utf-8")
    for v in ("460,800","398,131,200","758","33","420","248","57","24"):
        assert v in s
    assert "not another biological cohort" in s
    assert "conditional response covariances" in s
    assert "causal" in s.lower()
    assert "Native advance calls/new trajectories=0." in source
    for label,count in (("late_reopening",33),("no_support_window",420),
                        ("mean_never_reached",248),("mean_not_sustained",57)):
        rows=[l for l in source.splitlines() if l.startswith(f"| {label} |")]
        assert len(rows)==1
        assert int(rows[0].split("|")[2].strip())==count
    assert sum([33,420,248,57])==758


def test_s32_source_rank_and_anonymous_SI_review_delivery():
    si=SI.read_text(encoding="utf-8")
    assert all(si.count("## S"+str(n)+".")==1 for n in (29,30,31,32))
    assert si.index("## S29.") < si.index("## S30.") < si.index("## S31.") < si.index("## S32.")
    assert "EVIDENCE/Q2_S29_STATIC_FOCAL_W.json" in _section(si,29)
    s=_section(si,32)
    assert "4096 checkpoints" in s and "2048 conditional one-generation Price assays" in s
    assert "50/64" in s
    assert "not the full" in s.lower() or "does not identify the cumulative" in s
    price=PRICE.read_text(encoding="utf-8")
    assert "4,096 audited original genetic checkpoints" in price
    assert "2,048 one-step Price-assay source cells" in price
    for v in ("0.00003439","0.00001711","0.00003391","0.00012697"):
        assert v in price
    deny=("zuizui0223","github.com/","/workspace/","/home/","/root/","issue #436")
    assert not any(token in si.lower() for token in deny)


def test_manuscript_main_ceiling_unmoved_and_f1_evidence_kept():
    route=json.loads(ROUTE.read_text(encoding="utf-8"))
    paper=(ROOT/route["active_manuscript"]).read_text(encoding="utf-8")
    body=paper.split("# Introduction",1)[1].split("# Primary figure assembly and captions",1)[0]
    abstract=paper.split("## Abstract",1)[1].split("## Keywords",1)[0]
    assert len(body.split())==route["journal_fit"]["current_main_text_words"]
    assert len(abstract.split())==route["journal_fit"]["current_abstract_words"]
    assert len(body.split())<=5000 and len(abstract.split())<=150
    assert "S29" in paper
    assert route["status"]=="active_unified_manuscript_not_submitted"
