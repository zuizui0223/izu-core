from channel_id.candidate_registry import Candidate, audit_candidates


def candidate(name, group, ready, grade="A", matched_set="pair1", status="ready"):
    return Candidate(
        lineage=name,
        group=group,
        growth_form="herb",
        flowering_season="summer",
        mainland_coverage="mainland",
        island_coverage="islands",
        trait_channel="corolla length",
        evidence_grade=grade,
        quantitative_ready=ready,
        specialization_source="source" if group != "uncertain" else "",
        trait_source="trait source" if grade in {"A", "B"} else "",
        matched_set=matched_set,
        status=status,
        next_action="extract",
    )


def test_gate_opens_with_two_complete_ready_pairs():
    rows = (
        candidate("s1", "specialist", True, matched_set="p1"),
        candidate("g1", "generalist", True, matched_set="p1"),
        candidate("s2", "specialist", True, matched_set="p2"),
        candidate("g2", "generalist", True, matched_set="p2"),
    )
    result = audit_candidates(rows)
    assert result["analysis_gate"]["open"] is True
    assert result["complete_matched_sets"] == ["p1", "p2"]


def test_unresolved_candidates_do_not_open_gate():
    rows = (
        candidate("s1", "specialist", False, grade="B", matched_set="p1", status="candidate"),
        candidate("u1", "uncertain", False, grade="B", matched_set="p1", status="candidate"),
    )
    result = audit_candidates(rows)
    assert result["analysis_gate"]["open"] is False
    assert result["unresolved_group"] == ["u1"]
