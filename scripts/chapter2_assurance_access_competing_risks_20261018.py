"""Analysis contract for assurance policy vs genetic access and persistence.

This module never runs biological simulations or alters frozen Model3 source.
Inputs are prospective matched initial founder/visitor histories. Endpoints are
unconditional on post-policy survival and distinguish genetic loss, extinction,
and surviving genetic access. Historical policy effects are not confirmed here.
"""
from __future__ import annotations

from collections import defaultdict
import math

POLICIES = ("fixed", "evolving")
EXPECTED_FIELDS = {"founder_id", "visitor_id", "replicate_id", "policy",
                   "founder_genome_sha256", "visitor_history_sha256",
                   "historical_demographic_seed", "target_I", "censuses"}


def maternal_fault_floor(ovules, expressed_A, depression):
    """No-service viable maternal seed fraction of ideal q=1 ovule output.

    Ovule-weighted, so this is NOT always (1-delta)*mean(A).
    It does not measure pollen export, finite offspring recruitment or survival.
    """
    os = list(ovules)
    aa = list(expressed_A)
    if (not os or len(os) != len(aa)
            or not 0 <= depression <= 1
            or any(not math.isfinite(x) or x < 0 for x in os)
            or any(not math.isfinite(x) or not 0 <= x <= 1 for x in aa)
            or not sum(os) > 0):
        raise ValueError("fault floor needs positive, finite matched source ovules/A")
    return (1-depression)*sum(o*a for o, a in zip(os,aa))/sum(os)


def history_events(record):
    """First HIGH-I support loss while living vs competing source extinction."""
    if not EXPECTED_FIELDS <= set(record) or record["policy"] not in POLICIES:
        raise ValueError("invalid paired historical policy record")
    target = record["target_I"]
    if not isinstance(target,(int,float)) or not math.isfinite(target) or not 0 <= target <= 1:
        raise ValueError("founder I target absent")
    rows = record["censuses"]
    if not isinstance(rows,list) or len(rows) < 2:
        raise ValueError("need every annual census from founding")
    loss = extinction = None
    first_competing = None
    previous_upper = None
    closed = False
    extinct = False
    statuses = []
    for year, row in enumerate(rows):
        if row.get("t") != year or type(row.get("occupied")) is not bool:
            raise ValueError("census missing/nonsequential/nonbinary occupancy")
        alive = row["occupied"]
        upper = row.get("max_I_allele")
        if extinct and alive:
            raise ValueError("demographic rescue violates closed no-immigration source")
        if alive:
            if (not isinstance(upper,(int,float)) or not math.isfinite(upper)
                    or not 0 <= upper <= 1):
                raise ValueError("living state requires finite allele upper support")
            if previous_upper is not None and upper > previous_upper + 1e-12:
                raise ValueError("HIGH-I support rose without I mutation/seed immigration")
            if year == 0 and upper < target-1e-12:
                raise ValueError("founder mean cannot exceed founder allele maximum")
            previous_upper = upper
            now_closed = upper < target-1e-12
            if closed and not now_closed:
                raise ValueError("allele support reopened unexpectedly")
            if now_closed and loss is None:
                loss = year
                if first_competing is None:
                    first_competing = "genetic_loss"
            closed |= now_closed
        else:
            if upper is not None:
                raise ValueError("extinct traits must be undefined, not zero")
            extinct = True
            if extinction is None:
                extinction = year
                if first_competing is None:
                    first_competing = "extinction"
        statuses.append(
            "extinct" if extinct else "alive_closed" if closed else "alive_accessible")
    if rows[0]["occupied"] is not True:
        raise ValueError("original history must be occupied at founding")
    return dict(loss_t=loss, extinction_t=extinction,
                first_competing_event=first_competing, status_by_year=statuses)


def compare_historical_policies(records):
    """Complete paired f x v x replicate histories; no survivor selection.

    A future confirmatory plan must separately provide independent two-axis
    power review. This function returns DESCRIPTIVE contrasts only.
    """
    if not records:
        raise ValueError("no historical records")
    names = defaultdict(dict)
    axes = set()
    horizons = set()
    for record in records:
        event = history_events(record)
        key = (str(record["founder_id"]),str(record["visitor_id"]),
               str(record["replicate_id"]))
        axes.add((key[0],key[1]))
        horizons.add(len(event["status_by_year"]))
        if record["policy"] in names[key]:
            raise ValueError("duplicate historical assignment")
        names[key][record["policy"]] = (record,event)
    if len(horizons) != 1 or any(set(p)!=set(POLICIES) for p in names.values()):
        raise ValueError("paired policies and identical follow-up horizon required")
    founders = {f for f,_ in axes}
    visitors = {v for _,v in axes}
    if axes != {(f,v) for f in founders for v in visitors}:
        raise ValueError("crossed founder x visitor cells incomplete")
    by_cell = defaultdict(set)
    for f,v,r in names:
        by_cell[(f,v)].add(r)
    counts = {len(x) for x in by_cell.values()}
    if len(counts)!=1:
        raise ValueError("unbalanced nested demographic replicates")
    for key, pair in names.items():
        fixed, evolved = (pair[name][0] for name in POLICIES)
        for pinned in ("founder_genome_sha256","visitor_history_sha256",
                       "historical_demographic_seed","target_I"):
            if fixed[pinned] != evolved[pinned]:
                raise ValueError("policies do not share original founder/visitor/seed")
        for val in (fixed["founder_genome_sha256"],fixed["visitor_history_sha256"]):
            if not isinstance(val,str) or not val.strip():
                raise ValueError("missing source identity")
    T = next(iter(horizons))
    histories_per_policy=len(names)
    out=[]
    for t in range(T):
        arms={}
        for policy in POLICIES:
            events=[pair[policy][1] for pair in names.values()]
            at=[x["status_by_year"][t] for x in events]
            c_g=sum(x["first_competing_event"]=="genetic_loss"
                    and x["loss_t"] <= t for x in events)
            c_e=sum(x["first_competing_event"]=="extinction"
                    and x["extinction_t"] <= t for x in events)
            n_alive_access=at.count("alive_accessible")
            n_alive_closed=at.count("alive_closed")
            n_extinct=at.count("extinct")
            if c_g+c_e+n_alive_access!=histories_per_policy:
                raise AssertionError("competing-first-event mass not conserved")
            if n_alive_access+n_alive_closed+n_extinct!=histories_per_policy:
                raise AssertionError("current-state mass not conserved")
            arms[policy]=dict(
                P_alive_and_high_I_access=n_alive_access/histories_per_policy,
                P_alive_but_high_I_closed=n_alive_closed/histories_per_policy,
                P_extinct=n_extinct/histories_per_policy,
                CIF_high_I_genetic_loss=c_g/histories_per_policy,
                CIF_extinction_before_genetic_loss=c_e/histories_per_policy,
                P_alive=(n_alive_access+n_alive_closed)/histories_per_policy,
            )
        out.append(dict(t=t,arms=arms,
                        effects_evolving_minus_fixed={
                           metric:arms["evolving"][metric]-arms["fixed"][metric]
                           for metric in arms["fixed"]}))
    rmst={policy:sum(row["arms"][policy]["P_alive_and_high_I_access"]
                     for row in out) for policy in POLICIES}
    return dict(status="DESCRIPTIVE_FACTORIAL_ENDPOINT_CONTRACT_NOT_POWER_OR_EXECUTION",
                independent_founder_count=len(founders),
                independent_visitor_history_count=len(visitors),
                crossed_founder_visitor_cells=len(axes),
                nested_demographic_repeats_per_cell=next(iter(counts)),
                histories_per_historical_A_policy=histories_per_policy,
                years=T-1, time_series=out,
                restricted_accessible_census_time=rmst,
                restricted_accessible_time_difference_evolving_minus_fixed=(
                    rmst["evolving"]-rmst["fixed"]),
                constraints=[
                    "All originally allocated populations count, including early extinctions.",
                    "Genetic loss is a sufficient closed-I-allele-target condition, not restoration t-star.",
                    "Competing events and current alive/closed/extinct states have different denominators.",
                    "Future restored visitor efficacy and full I/A rare-mutant selection must be assayed separately.",
                    "Independent founder-by-visitor power and preregistration (#585) remain mandatory before biological confirmation.",
                ])
