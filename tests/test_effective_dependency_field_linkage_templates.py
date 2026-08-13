import csv
from pathlib import Path

from scripts.audit_effective_pollinator_dependency import FRUIT_COLUMNS


ROOT = Path(__file__).resolve().parents[1]
FRUIT_TEMPLATE = ROOT / "templates/field_mature_fruit_template.csv"
PARENTAGE_TEMPLATE = ROOT / "templates/field_seed_parentage_template.csv"
TREATMENT_TEMPLATE = ROOT / "templates/field_pollination_treatment_template.csv"
SVD_RECOUNT_TEMPLATE = ROOT / "templates/field_svd_recount_calibration_template.csv"


def header(path: Path) -> list[str]:
    with path.open(encoding="utf-8", newline="") as handle:
        return next(csv.reader(handle))


def test_mature_fruit_template_matches_cli_contract_and_treatment_link():
    fruit_header = header(FRUIT_TEMPLATE)
    assert tuple(fruit_header) == FRUIT_COLUMNS
    treatment_header = header(TREATMENT_TEMPLATE)
    assert "fruit_id" in treatment_header
    assert "fruit_id" in fruit_header


def test_parentage_template_preserves_unresolved_state_without_selfing_inference():
    parentage_header = header(PARENTAGE_TEMPLATE)
    required = {
        "parentage_id",
        "fruit_id",
        "seed_id",
        "maternal_id",
        "paternal_id",
        "parentage_status",
        "posterior_probability",
        "genotype_qc_status",
    }
    assert required.issubset(parentage_header)
    # Missing paternal identity remains representable as unresolved parentage;
    # the schema contains no derived selfing flag that could turn missingness into selfing.
    assert "selfed" not in parentage_header
    assert "selfing" not in parentage_header


def test_svd_recount_calibration_links_to_raw_svd_without_embedding_derived_reliability():
    recount_header = header(SVD_RECOUNT_TEMPLATE)
    required = {
        "calibration_id",
        "svd_id",
        "recount_id",
        "counter_id",
        "blinded_to_original",
        "total_pollen_grains",
        "conspecific_pollen_grains",
        "heterospecific_pollen_grains",
        "unclassified_pollen_grains",
    }
    assert required.issubset(recount_header)
    assert "reliability" not in recount_header
    assert "repeatability" not in recount_header
