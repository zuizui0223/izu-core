import importlib.util
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "parse_canary_balearic_plos_derived.py"
SPEC = importlib.util.spec_from_file_location(
    "canary_balearic_plos_derived", MODULE_PATH
)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_parse_visitor_rows_carries_specificity_zone_and_species_context():
    lines = [
        "Specificity Zone sp.cod Month L Functional richness Rank abundance Evenness",
        "Generalized CB las.sp 1 (January) 3 3 3.00 0.314",
        "las.sp 2 (February) 7 5 2.57 0.362",
        "CM api.mel 1 (April) 3 2 3.67 0.207",
    ]
    rows = MODULE.parse_derived_lines(
        lines,
        source_logical_id="s003",
        resolved_domain="flower_visitor",
    )
    assert len(rows) == 3
    assert rows[1]["specificity"] == "Generalized"
    assert rows[1]["zone"] == "CB"
    assert rows[1]["month_label"] == "February"
    assert rows[2]["zone"] == "CM"
    assert rows[2]["classification_metric"] == "L"
    assert rows[2]["geological_origin"] == "continental_island_system"


def test_parse_selectiveness_rows_supports_missing_evenness():
    lines = [
        "Specificity Zone sp.cod Month d-prime Functional richness Rank abundance Evenness",
        "Selective SB par.tib 2 0.98 4 1.20 -",
        "par.tib 3 0.67 5 1.20 0.229",
    ]
    rows = MODULE.parse_derived_lines(
        lines,
        source_logical_id="s004",
        resolved_domain="plant",
    )
    assert rows[0]["classification_metric"] == "d_prime"
    assert rows[0]["partner_abundance_evenness"] is None
    assert rows[1]["partner_abundance_evenness"] == pytest.approx(0.229)


def test_row_parser_rejects_unexpected_month_or_column_count():
    with pytest.raises(ValueError, match="unexpected relative month"):
        MODULE.parse_derived_lines(
            ["Generalized CB las.sp 5 3 3 3.00 0.314"],
            source_logical_id="s003",
            resolved_domain="flower_visitor",
        )
    with pytest.raises(ValueError, match="expected four derived values"):
        MODULE.parse_derived_lines(
            ["Generalized CB las.sp 1 3 3 3.00"],
            source_logical_id="s003",
            resolved_domain="flower_visitor",
        )


def test_validate_rows_preserves_four_community_two_domain_structure():
    rows = []
    for domain in ("flower_visitor", "plant"):
        for zone in sorted(MODULE.ZONES):
            for specificity in sorted(MODULE.SPECIFICITY_CLASSES):
                rows.append(
                    {
                        "resolved_domain": domain,
                        "zone": zone,
                        "specificity": specificity,
                        "species_code": f"{zone.casefold()}x.ab",
                        "classification_metric": (
                            "L"
                            if specificity in {"Generalized", "Specialized"}
                            else "d_prime"
                        ),
                    }
                )
    result = MODULE.validate_rows(rows)
    assert result["n_rows"] == 32
    assert result["domains"] == ["flower_visitor", "plant"]
    assert set(result["zones"]) == MODULE.ZONES
    assert set(result["specificity_classes"]) == MODULE.SPECIFICITY_CLASSES


def test_zone_context_does_not_create_independent_origin_replicates():
    assert MODULE.ZONE_CONTEXT["SB"]["island"] == "Mallorca"
    assert MODULE.ZONE_CONTEXT["CM"]["island"] == "Mallorca"
    assert MODULE.ZONE_CONTEXT["CB"]["island"] == "Lanzarote"
    assert MODULE.ZONE_CONTEXT["LC"]["island"] == "Lanzarote"
