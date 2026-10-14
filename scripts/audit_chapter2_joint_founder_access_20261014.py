#!/usr/bin/env python3
"""Exact design-only joint A/I founder carrier retention; no Model3 imports/runs.

The artificial source is NOT mainland genotype evidence. A carrier means a
symmetric heterozygote at one trait, not a sustained evolutionary response.
"""
from __future__ import annotations

import json
from fractions import Fraction
from math import comb
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "data/design/chapter2_colonisation_genetic_access_draft_20261014.json"


def choose(n: int, r: int) -> int:
    return comb(n, r) if 0 <= r <= n else 0


def joint_access_exact(total: int, A: int, I: int, intersection: int, founders: int) -> dict:
    """Exact outcomes of without-replacement carrier sampling, not Model3 events."""
    if any(type(v) is not int for v in (total, A, I, intersection, founders)):
        raise ValueError("Founding counts must be integers")
    if not (total > 0 and 0 <= A <= total and 0 <= I <= total and
            max(0, A + I - total) <= intersection <= min(A, I) and
            1 <= founders <= total):
        raise ValueError("Impossible source carrier margins/overlap or founder count")
    neither = total - A - I + intersection
    den = comb(total, founders)
    no_A = Fraction(choose(total - A, founders), den)
    no_I = Fraction(choose(total - I, founders), den)
    neither_access = Fraction(choose(neither, founders), den)
    A_only = no_I - neither_access
    I_only = no_A - neither_access
    both_access = 1 - no_A - no_I + neither_access
    one_axis = A_only + I_only
    if min(A_only, I_only, both_access, neither_access) < 0 or (
            A_only + I_only + both_access + neither_access != 1):
        raise AssertionError("Invalid joint hypergeometric partition")
    pa = Fraction(A, total)
    pi = Fraction(I, total)
    fpc = Fraction(total-founders, founders*(total-1)) if total > 1 else Fraction(0)
    return {
        "N": total, "A_source_carriers": A, "I_source_carriers": I,
        "source_overlap_carriers": intersection, "founders": founders,
        "p_A_retained_I_lost": A_only,
        "p_I_retained_A_lost": I_only,
        "p_both_retained": both_access,
        "p_both_lost": neither_access,
        "p_only_one_axis_retained": one_axis,
        "expected_A_carrier_fraction": pa,
        "expected_I_carrier_fraction": pi,
        "variance_founder_A_carrier_fraction": pa*(1-pa)*fpc,
        "variance_founder_I_carrier_fraction": pi*(1-pi)*fpc,
        "covariance_founder_carrier_fractions":
            (Fraction(intersection,total)-pa*pi)*fpc,
    }


def carrier_count_distribution(total: int, A: int, founders: int) -> list[Fraction]:
    if not (total > 0 and 0 <= A <= total and 1 <= founders <= total):
        raise ValueError("Invalid carrier count distribution parameters")
    den = comb(total, founders)
    result = [Fraction(choose(A,k)*choose(total-A,founders-k),den)
              for k in range(founders+1)]
    if sum(result) != 1:
        raise AssertionError("Hypergeometric probabilities fail to close")
    return result


def audit_design(d: dict) -> dict:
    approval = d.get("approval", {})
    if (d.get("status") != "DESIGN_CANDIDATE_NO_EXECUTION_NO_CONFIRMATION" or
            approval.get("author_approval_for_new_biology") is not False or
            approval.get("new_biological_histories") != 0):
        raise ValueError("No new biology or confirmation authorised by this design")
    source = d["illustrative_mainland_source"]
    N = source["adults"]
    A = source["A_heterozygote_adults"]
    if ((N,A,source["A_neutral_homozygote_adults"]) != (48,12,36) or
            source["real_observed_mainland_data"] is not False):
        raise ValueError("Requires frozen hypothetical A source, not field data")
    if d["candidate_founder_samples"] != [2,8,24,48]:
        raise ValueError("Founder counts outside design scope")

    # NEW illustrative I margin, NOT measured from original Model3.
    I = 12
    overlaps = (0,3,6,12)
    rows=[]
    for overlap in overlaps:
        for n in d["candidate_founder_samples"]:
            data=joint_access_exact(N,A,I,overlap,n)
            rows.append({k: str(v) if isinstance(v,Fraction) else v
                         for k,v in data.items()})

    carrier_moments=[]
    for n in d["candidate_founder_samples"]:
        p=carrier_count_distribution(N,A,n)
        e_k=sum(Fraction(k)*v for k,v in enumerate(p))
        e_kk=sum(Fraction(k*k)*v for k,v in enumerate(p))
        v_q=(e_kk-e_k*e_k)/(n*n)
        formula=Fraction(1,4)*Fraction(3,4)*Fraction(N-n,n*(N-1))
        if e_k/n != Fraction(1,4) or v_q != formula:
            raise AssertionError("Independent hypergeometric carrier moments mismatch")
        carrier_moments.append({
            "founders":n,"p_no_A_carrier":str(p[0]),
            "p_exactly_one_A_carrier":str(p[1]),
            "expected_fraction_A_carriers":str(e_k/n),
            "variance_fraction_A_carriers":str(v_q),
        })
    return {
        "status":"MATHEMATICAL_HYPOTHESIS_GENERATOR_NO_BIOLOGICAL_HISTORY",
        "new_biological_histories":0,"source_total":N,
        "hypothetical_A_carriers":A,"hypothetical_I_carriers":I,
        "source_co_carrier_overlaps":list(overlaps),
        "joint_access_rows":rows,
        "marginal_A_founder_distribution_moments":carrier_moments,
        "limitations":[
            "I-carrier prevalence and overlap hypothetical, not old Model3",
            "carrier=standing symmetric heterozygote, not observed response",
            "no mutation/recombination/selection/demography/survival simulated",
            "retaining a carrier does not guarantee an evolutionary event",
            "not natural island founder inference or causal mediation",
        ],
    }


def main() -> None:
    d=json.loads(SPEC.read_text(encoding="utf-8"))
    print(json.dumps(audit_design(d),indent=2,sort_keys=True))


if __name__=="__main__":
    main()
