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
    for name in ("figure_01_framework.svg", "figure_02_independent_decline.svg",
                 "figure_03_assurance_interaction.svg", "figure_04_predictability.svg",
                 "figure_05_persistence_options.svg", "figure_06_transfer.svg"):
        assert "figures/chapter2_nee_five_results/"+name in manuscript
        assert (ROOT/"figures/chapter2_nee_five_results"/name).exists()
    results=manuscript.split("## Results — existing source-admitted evidence",1)[1].split("## Planned new decisive",1)[0]
    assert [line.split(' — ')[0] for line in results.splitlines() if line.startswith('### ')] == [f'### R{i}' for i in range(1,6)]



def test_figure_01_q1_fixed_and_fresh_founder_results():
    r, meta = load("figure_01_q1_mechanism.svg")
    original = json.loads((ROOT / "data/results/chapter2_assurance_generality_20261006.json").read_text(encoding="utf-8"))
    receipt = json.loads((ROOT / "docs/CHAPTER2_TWO_PROPOSITION_EVIDENCE_RECEIPT_20261016.json").read_text(encoding="utf-8"))
    assert len(marks(r, "fixed_I")) == len(marks(r, "fresh_D")) == 4
    for row in original["settings"]:
        hits = [x for x in marks(r, "fixed_I") if x.get("data-setting") == row["setting"]]
        assert len(hits) == 1
        q = row["fixed_far_change_from_founders"]
        same(hits[0].get("data-value"), q["mean"])
        same(hits[0].get("data-low"), q["bootstrap95"][0])
        same(hits[0].get("data-high"), q["bootstrap95"][1])
    for row in receipt["fresh_founder_q1"]["settings"]:
        hits = [x for x in marks(r, "fresh_D") if x.get("data-setting") == row["setting"]]
        assert len(hits) == 1
        same(hits[0].get("data-value"), row["original_D"])
        assert float(hits[0].get("data-low")) <= row["original_D"] <= float(hits[0].get("data-high"))
    assert meta["status"] == "ORIGINAL_ALL_4_SUPPORTED__FRESH_3_OF_4"
    assert receipt["fresh_founder_q1"]["global_support"].startswith("A genetic-capacity evolution not necessary")


def test_figure_03_order_q2_and_source_separated_finite_realization():
    r, meta = load("figure_03_order_repeatability.svg")
    assert meta["interpretation"].startswith("No retrospective Q1-Q4")
    assert meta["denominators"] == {"seq": 64, "bridge": 128, "access": 2304, "first_exclusions": 1238}
    sequence = json.loads((ROOT / "data/results/chapter2_1005_confirmatory_replication_20261006.json").read_text(encoding="utf-8"))
    q2 = src("CHAPTER2_Q2_I_SUPPORT_384_ORIGINAL_READOUT_20261016.json")
    bridge = json.loads((ROOT / "data/results/model3_ch2_bridge_prospective_frozen_20260927.json").read_text(encoding="utf-8"))
    access = json.loads((ROOT / "data/results/directional_access_20261013/READOUT.json").read_text(encoding="utf-8"))
    assert len(marks(r, "chronology")) == 2
    count = {
        "assurance_cost": sequence["primary_sequence"]["counts"]["assurance_first"],
        "prior_selfing": next(x for x in sequence["threshold_sensitivity"]
                              if x["setting"] == "prior_selfing" and x["mutation_rate"] == .01
                              and x["threshold"] == .05)["counts"]["assurance_first"]
    }
    assert count == {"assurance_cost": 51, "prior_selfing": 30}
    for bar in marks(r, "chronology"):
        assert int(bar.get("data-count")) == count[bar.get("data-setting")]
        assert int(bar.get("data-denom")) == 64
    assert q2["registered_inference"]["result"] == "both_inconclusive"
    assert len(marks(r, "q2")) == 2
    for bar in marks(r, "q2"):
        row = q2["coprimary"][bar.get("data-endpoint")]
        same(bar.get("data-value"), row["estimate"])
        same(bar.get("data-low"), row["simultaneous_familywise_CI"][0])
        same(bar.get("data-high"), row["simultaneous_familywise_CI"][1])
        assert row["simultaneous_familywise_CI"][0] <= 0 <= row["simultaneous_familywise_CI"][1]
    assert len(marks(r, "q3_response")) == 4
    for bar in marks(r, "q3_response"):
        row = next(x for x in bridge["reports"] if x["intervention"] == bar.get("data-intervention")
                   and x["model"] == bar.get("data-model"))
        same(bar.get("data-mean"), row["mean"])
        assert int(bar.get("data-mixed")) == row["mixed_counts"][0]
        assert int(bar.get("data-denom")) == bridge["provenance"]["histories_verified"] == 128
    assert len(marks(r, "q3_access")) == 3
    groups = {
        "before-fixation": access["excluded_before_fixation"],
        "at-fixation": access["excluded_at_fixation"],
        "not-excluded": access["cases"] - access["ever_excluded"]
    }
    assert sum(groups.values()) == access["cases"] == 2304
    for bar in marks(r, "q3_access"):
        assert int(bar.get("data-count")) == groups[bar.get("data-category")]
        assert int(bar.get("data-denom")) == access["cases"]
    assert len(marks(r, "q3_selected")) == 2
    selected = {"favorable-but-lost": 315, "other-first-exclusions": 923}
    for bar in marks(r, "q3_selected"):
        assert int(bar.get("data-count")) == selected[bar.get("data-category")]
        assert int(bar.get("data-denom")) == access["ever_excluded"] == 1238


def test_original_four_question_contract_and_figure_03_synthesis():
    original = (ROOT / "docs/CHAPTER2_UNIFIED_EVOLUTION_PERSISTENCE_MANUSCRIPT_20261010.md").read_text(encoding="utf8")
    active = (ROOT / "docs/CHAPTER2_UNIFIED_NEE_ARTICLE_WORKING_20261017.md").read_text(encoding="utf8")
    assert "CHAPTER2_FIVE_RESULTS_EXTENDED_EVIDENCE_20261021.md" in active
    active += (ROOT / "docs/CHAPTER2_FIVE_RESULTS_EXTENDED_EVIDENCE_20261021.md").read_text(encoding="utf8")
    crosswalk = (ROOT / "docs/CHAPTER2_Q1_Q4_ORIGINAL_FOUR_PARTS_AUDIT_20261019.md").read_text(encoding="utf8")
    assert all(("## Q" + str(i) + " —") in original for i in range(1, 5))
    assert all(("### Q" + str(i) + " —") in active for i in range(1, 5))
    assert "density is not the abm" in active.lower()
    assert "−0.4510" in active and "−0.1446" in active
    assert "+2.83 and +4.59" in active
    assert "selection → sequence → finite realization → persistence" in crosswalk
    assert "entire mediation chain" in crosswalk


def test_q4_original_vs_new_cohorts_are_separate():
    original = json.loads((ROOT / "data/results/chapter2_island_demographic_independent32_20261008.json").read_text(encoding="utf-8"))
    latest = src("CHAPTER2_CONFIRM160_COMPACT_RESULTS_20261019.json")
    manuscript = (ROOT / "docs/CHAPTER2_UNIFIED_NEE_ARTICLE_WORKING_20261017.md").read_text(encoding="utf8")
    assert "CHAPTER2_FIVE_RESULTS_EXTENDED_EVIDENCE_20261021.md" in manuscript
    manuscript += (ROOT / "docs/CHAPTER2_FIVE_RESULTS_EXTENDED_EVIDENCE_20261021.md").read_text(encoding="utf8")
    assert original["independent_histories"] == 32
    assert original["predeclared_pooled_primary"]["pass"] is True
    same(original["predeclared_pooled_primary"]["mean"], .1083984375)
    assert original["predeclared_pooled_primary"]["bootstrap95"][0] > 0
    prior = next(x for x in original["per_setting"] if x["setting"] == "prior_selfing")
    assert prior["bootstrap95"][0] < 0 < prior["bootstrap95"][1]
    assert latest["independent_axes"] == [160, 160] and latest["crossings"] == 25600
    newest = next(x for x in latest["primary"]["endpoints"] if x["name"] == "survival_interaction")
    same(newest["estimate"], .9270703125)
    assert newest["interval"][0] > 0
    assert "### Q4 — Persistence" in manuscript
    assert "+0.1083984375" in manuscript
    assert "+2.83 and +4.59" in manuscript
    assert "policy-by-budget interaction" in manuscript
    # The two studies are separate experiments and the Q4 result is not a genetic mediation estimate.
    assert "not" in manuscript.split("### Q4 — Persistence", 1)[1].split("### Confirmed policy effects", 1)[0].lower()


def test_main_figure_03_sequence_and_realization_sources():
    """All four Q2/Q3 panels use separate, original, admitted cohorts."""
    r, m = load("figure_03_sequence_realization.svg")
    sequence = json.loads((ROOT/"data/results/chapter2_1005_confirmatory_replication_20261006.json").read_text(encoding="utf8"))
    assigned = json.loads((ROOT/"results/chapter2/order_expression_full_cohort_20261009.json").read_text(encoding="utf8"))
    carrier = src("CHAPTER2_Q2_I_SUPPORT_384_ORIGINAL_READOUT_20261016.json")
    atom = (ROOT/"docs/atom_comparison_20261011/ATOM_ABM_NUMERICAL_VERDICT_20261011.md").read_text(encoding="utf8")
    access = json.loads((ROOT/"data/results/directional_access_20261013/READOUT.json").read_text(encoding="utf8"))
    high = src("CHAPTER2_NEE_HIGH_I_SUPPORT_SOURCE_READOUT_20261017.json")
    assert m["scientific_status"] == "SOURCE_BACKED_FOUR_COHORT_DESCRIPTIVE_FIGURE_NO_POOLING"
    assert len(marks(r,"A-first")) == 2
    expected = {"assurance_cost": sequence["primary_sequence"]["counts"]["assurance_first"],
                "prior_selfing": next(x for x in sequence["threshold_sensitivity"]
                    if x["setting"]=="prior_selfing" and x["threshold"]==.05 and
                    x["mutation_rate"]==.01)["counts"]["assurance_first"]}
    for x in marks(r,"A-first"):
        assert int(x.get("data-count")) == expected[x.get("data-setting")]
        assert int(x.get("data-denom")) == 64
    assert len(marks(r,"assigned-order")) == 1
    a = marks(r,"assigned-order")[0]
    d = assigned["main_order_history_DID"]
    assert d["decision"] == "equivalent_within_predeclared_ROPE"
    same(a.get("data-value"), d["pooled_mean"])
    same(a.get("data-low"), d["history_bootstrap95"][0])
    same(a.get("data-high"), d["history_bootstrap95"][1])
    assert -.05 < d["history_bootstrap95"][0] < d["history_bootstrap95"][1] < .05
    assert len(marks(r,"carrier-Q2")) == 2
    assert carrier["registered_inference"]["result"]=="both_inconclusive"
    for x in marks(r,"carrier-Q2"):
        target=carrier["coprimary"][x.get("data-endpoint")]
        same(x.get("data-value"),target["estimate"])
        same(x.get("data-low"),target["simultaneous_familywise_CI"][0])
        same(x.get("data-high"),target["simultaneous_familywise_CI"][1])
        assert target["simultaneous_familywise_CI"][0] < 0 < target["simultaneous_familywise_CI"][1]
    assert len(marks(r,"finite-Q3")) == 6
    for block in ("Main","Confirmation"):
        line=next(x for x in atom.splitlines() if x.startswith("| "+block+" | 0.125 | matched"))
        col=[v.strip() for v in line.split("|")[1:-1]]
        assert col[3]=="A first"
        assert sum(map(int,col[4:]))==32
        cats={"A-first":int(col[4]),"A-only":int(col[5]),
              "other":sum(map(int,col[6:]))}
        for cat,count in cats.items():
            row=[x for x in marks(r,"finite-Q3") if x.get("data-founder")==block and
                 x.get("data-category")==cat]
            assert len(row)==1 and int(row[0].get("data-count"))==count
            assert int(row[0].get("data-denom"))==32
    assert len(marks(r,"access-Q3"))==3
    groups={"before":access["excluded_before_fixation"],
            "at":access["excluded_at_fixation"],
            "never":access["cases"]-access["ever_excluded"]}
    assert sum(groups.values())==2304
    for x in marks(r,"access-Q3"):
        assert int(x.get("data-count"))==groups[x.get("data-class")]
        assert int(x.get("data-denom"))==2304
    assert m["high_ever"]==high["overall"]["high_I_founder_mean_excluded"]==1455
    # No independent-genetic-loss mediator or natural extinction inference is made.


def test_figure_04_three_state_panel_preserves_registered_contrasts_and_denominators():
    """Read-only post-outcome graphic is an exact all-start partition, not a third registered test."""
    r, m = load("figure_04_access_survival.svg")
    original = src("CHAPTER2_CONFIRM160_COMPACT_RESULTS_20261019.json")
    assert m["source"] == "docs/audits/CHAPTER2_CONFIRM160_COMPACT_RESULTS_20261019.json"
    extra = m["descriptive_three_state"]
    assert extra["status"] == "POST_OUTCOME_DESCRIPTIVE_NOT_REGISTERED_NO_NEW_INTERVAL"
    assert extra["all_start_denominator"] == original["crossings"] == 25600
    assert len(marks(r, "three_state")) == 12
    expected = {}
    for budget in ("B8", "B4p5"):
        for policy in ("fixed", "evolving"):
            arm = original["arms"][policy + "_" + budget]
            expected[budget, policy] = {
                "alive_accessible": arm["alive_accessible"],
                "alive_closed": arm["alive"] - arm["alive_accessible"],
                "extinct": original["crossings"] - arm["alive"],
            }
    for (budget, policy), states in expected.items():
        found = [x for x in marks(r, "three_state")
                 if x.get("data-budget") == budget and x.get("data-policy") == policy]
        assert len(found) == 3
        row = {}
        for item in found:
            key = item.get("data-state")
            assert key in states and key not in row
            row[key] = int(item.get("data-count"))
            assert int(item.get("data-denom")) == 25600
        assert row == states and sum(row.values()) == 25600
        # The plotted bars must be exactly adjacent and scaled to their actual counts;
        # hiding a tiny cell must not alter its denominator.
        by_state = {x.get("data-state"): x for x in found}
        order = ("alive_accessible", "alive_closed", "extinct")
        start = 282.0
        for key in order:
            item = by_state[key]
            same(float(item.get("x")), start)
            same(float(item.get("width")), 945 * states[key] / 25600)
            start += float(item.get("width"))
        same(start, 282 + 945)
        assert len({x.get("y") for x in found}) == 1
    from scripts.audit_chapter2_three_state_publication_20261019 import derive
    derived = derive(original)
    same(extra["delta_B8_pp"], derived["budgets"]["B8"]["evolving_minus_fixed_accessible_alive_pp"])
    same(extra["delta_B4p5_pp"], derived["budgets"]["B4p5"]["evolving_minus_fixed_accessible_alive_pp"])
    same(extra["difference_of_descriptive_differences_pp"],
         derived["descriptive_budget_interaction_pp"])
    title = r.find("s:title", NS).text
    desc = r.find("s:desc", NS).text
    assert "three possible final population states" in title
    assert "not a third preregistered test" in desc
    assert original["primary"]["joint_positive"] is True
    assert original["actual_restoration_tested"] is False


def test_five_result_prediction_marks_preserve_existing_scores():
    r=ET.parse(ROOT/"figures/chapter2_nee_five_results/figure_04_predictability.svg").getroot()
    metadata=json.loads(r.find("s:metadata",NS).text)
    original=src("CHAPTER2_FOUNDER_PREDICTABILITY_20261021.json")["results"]
    for trait in ("I","M"):
        same(metadata["history_skills"][trait],original[f"evolving_{trait}_change"]["loo_skill"]["history"])
    endpoint=src("CHAPTER2_MATCHED_AI_REPEATABILITY_20261019.json")["settings"]
    for row in metadata["endpoint_counts"]:
        assert row["value"]==endpoint[row["setting"]]["central"][row["trait"]]["far_identical_endpoint_contexts"]
