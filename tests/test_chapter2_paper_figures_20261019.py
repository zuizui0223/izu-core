"""Source-to-vector figure checks; documentary, not new simulation."""
from __future__ import annotations
import json
from pathlib import Path
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
AUDIT=ROOT/"docs"/"audits"
FIG=ROOT/"figures"/"chapter2_nee"
NS={"s":"http://www.w3.org/2000/svg"}

def load(name):
    r=ET.parse(FIG/name).getroot()
    assert r.tag=="{http://www.w3.org/2000/svg}svg"
    assert r.find("s:title",NS) is not None and r.find("s:desc",NS) is not None
    meta=json.loads(r.find("s:metadata",NS).text)
    return r,meta

def src(name):
    return json.loads((AUDIT/name).read_text(encoding="utf-8"))

def marks(r,kind):
    return [x for x in (r.findall("s:rect",NS)+r.findall("s:circle",NS))
            if x.get("data-kind")==kind]

def same(x,y):
    assert abs(float(x)-float(y))<1e-12

def test_fig02_exploratory_pollen_starts():
    r,m=load("figure_02_baseline_pollen.svg")
    d=src("CHAPTER2_BASELINE_POLLEN_384_AUDIT_20261019.json")
    assert m["source"]=="docs/audits/CHAPTER2_BASELINE_POLLEN_384_AUDIT_20261019.json"
    assert (d["raw_rows"],d["founders"])==(384,12)
    for locus in ("A","I"):
        assert len(marks(r,locus))==4
        for row in d["summaries"]:
            group="strong" if row["baseline"].startswith("strong") else "weak"
            hits=[x for x in marks(r,locus) if float(x.get("data-start"))==row["start_A"]
                  and x.get("data-baseline")==group]
            assert len(hits)==1
            same(hits[0].get("data-value"),row["terminal_decline_minus_control_"+locus])
    assert len(marks(r,"interaction_A"))==2
    for row in d["interactions"]:
        hits=[x for x in marks(r,"interaction_A") if float(x.get("data-start"))==row["start_A"]]
        assert len(hits)==1 and row["n_founders"]==12
        same(hits[0].get("data-value"),row["interaction_A"])
        for key,val in zip(("data-low","data-high"),row["bootstrap_95_A"]):
            same(hits[0].get(key),val)

def test_fig04_registered_counts():
    r,m=load("figure_04_access_survival.svg")
    d=src("CHAPTER2_CONFIRM160_COMPACT_RESULTS_20261019.json")
    assert m["source"]=="docs/audits/CHAPTER2_CONFIRM160_COMPACT_RESULTS_20261019.json"
    assert m["crossings"]==d["crossings"]==25600
    for policy in ("fixed","evolving"):
        hits=[x for x in marks(r,"closure") if x.get("data-policy")==policy]
        assert len(hits)==1
        assert int(hits[0].get("data-count"))==d["arms"][policy+"_B8"]["genetic_first"]
        assert int(hits[0].get("data-denom"))==25600
    assert len(marks(r,"survival"))==4
    for x in marks(r,"survival"):
        assert int(x.get("data-count"))==d["arms"][x.get("data-arm")]["alive"]
        assert int(x.get("data-denom"))==25600
    for slot,name in (("genetic","genetic_loss"),("survival","survival_interaction")):
        ep=next(x for x in d["primary"]["endpoints"] if x["name"]==name)
        same(m[slot]["estimate"],ep["estimate"])
        for a,b in zip(m[slot]["interval"],ep["interval"]):
            same(a,b)
    assert d["actual_restoration_tested"] is False

def test_fig05_duration_and_competing_extinction():
    r,m=load("figure_05_variation_duration.svg")
    d=src("CHAPTER2_VARIATION_CLOCK_RESULTS_20261019.json")
    assert m["source"]=="docs/audits/CHAPTER2_VARIATION_CLOCK_RESULTS_20261019.json"
    assert len(marks(r,"duration"))==2
    for budget in ("B8","B4p5"):
        x=next(x for x in marks(r,"duration") if x.get("data-budget")==budget)
        row=next(x for x in d["contrasts"] if x["budget"]==budget and x["trait"]=="I"
                 and x["endpoint"]=="occupied_polymorphic_duration")
        same(x.get("data-value"),row["estimate"])
        same(x.get("data-low"),row["simultaneous_interval"][0])
        same(x.get("data-high"),row["simultaneous_interval"][1])
    for policy in ("fixed","evolving"):
        row=next(x for x in d["results"] if x["budget"]=="B4p5" and x["trait"]=="I"
                 and x["policy"]==policy)
        assert row["curves"]["extinct"][-1]==m["extinctions_B4p5"][policy]

def test_fig06_cohorts_and_survivor_means():
    r,m=load("figure_06_late_transfer.svg")
    d=src("CHAPTER2_READAPTATION_DESCRIPTIVE_TABLES_20261019.json")
    assert m["source"]=="docs/audits/CHAPTER2_READAPTATION_DESCRIPTIVE_TABLES_20261019.json"
    assert m["cohorts"]==64 and m["futures"]==10240
    assert len(marks(r,"entry"))==4
    for policy in ("fixed","evolving"):
        cohort=[x for x in d["cohort_allele_counts"] if x["key"][2]==policy]
        assert len(cohort)==32
        polym=sum(x["distinct_alleles_M_I_A"][1]>1 for x in cohort)
        t0=next(x for x in d["tables"] if x["policy"]==policy and x["destination"]==0)
        support=next(x for x in t0["support"] if x["epsilon"]==0)["entry_I_supported_cohorts"]
        for metric,count in (("polymI",polym),("supportI",support)):
            hits=[x for x in marks(r,"entry") if x.get("data-policy")==policy and x.get("data-metric")==metric]
            assert len(hits)==1 and int(hits[0].get("data-count"))==count
    assert len(marks(r,"transfer-survival"))==len(marks(r,"performance"))==10
    for row in d["tables"]:
        for kind in ("transfer-survival","performance"):
            hits=[x for x in marks(r,kind) if x.get("data-policy")==row["policy"]
                  and int(x.get("data-destination"))==row["destination"]]
            assert len(hits)==1
            x=hits[0]
            if kind=="transfer-survival":
                assert int(x.get("data-count"))==row["occupied"]
                assert int(x.get("data-denom"))==row["allocated"]==1024
            else:
                same(x.get("data-value"),row["survivor_assay_change"]["mean"])
                assert int(x.get("data-survivors"))==row["survivor_assay_change"]["n"]

def test_figure_links_in_single_manuscript():
    manuscript=(ROOT/"docs"/"CHAPTER2_UNIFIED_NEE_ARTICLE_WORKING_20261017.md").read_text(encoding="utf-8")
    for name in ("figure_02_baseline_pollen.svg","figure_04_access_survival.svg",
                 "figure_05_variation_duration.svg","figure_06_late_transfer.svg"):
        assert "figures/chapter2_nee/"+name in manuscript
