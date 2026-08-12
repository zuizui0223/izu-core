from scripts.verify_hendriks_locked_pdf import (
    contains_numeric,
    contains_taxon,
    table_region,
    verify_appendix_mapping,
    verify_b9,
)


def test_table_region_and_taxon_numeric_matching_are_strict():
    text = '''
    Table B9 Flower area dataset measurements and measurement references
    Abrotanella rosulata 0.067 Abrotanella spathulata 0.38
    Table B10 Next table
    Abrotanella rosulata 999
    '''
    region = table_region(text, "B9", "B10")
    assert contains_taxon(region, "Abrotanella rosulata")
    assert contains_taxon(region, "Abrotanella spathulata")
    assert contains_numeric(region, "0.067")
    assert contains_numeric(region, "0.38")
    assert not contains_numeric(region, "999")


def test_table_region_uses_data_table_not_earlier_toc_copy():
    text = '''
    List of tables
    Table A4 Campbell Island species ................................ 77
    Table A5 Chatham Island species ................................. 78
    Table B9 Flower area dataset .................................... 96
    Table B10 Next dataset .......................................... 98

    Appendix A
    Table A4 Campbell Island species
    Abrotanella rosulata
    Table A5 Chatham Island species
    Brachyglottis huntii

    Appendix B
    Table B9 Flower area dataset measurements and measurement references
    Abrotanella rosulata 0.067 Abrotanella spathulata 0.38
    Table B10 Next dataset
    '''
    a4 = table_region(text, "A4", "A5")
    b9 = table_region(text, "B9", "B10")
    assert contains_taxon(a4, "Abrotanella rosulata")
    assert contains_taxon(b9, "Abrotanella rosulata")
    assert contains_numeric(b9, "0.067")


def test_b9_requires_both_taxa_and_both_values_for_every_row():
    rows = [
        {
            "pair_id": "1",
            "island_species": "Abrotanella rosulata",
            "island_flower_area_cm2": "0.067",
            "mainland_relative": "Abrotanella spathulata",
            "mainland_flower_area_cm2": "0.38",
        }
    ]
    text = "Table B9 Abrotanella rosulata 0.067 Abrotanella spathulata 0.38 Table B10"
    result = verify_b9(text, rows)
    assert result["n_verified"] == 1
    assert result["all_rows_verified"] is False


def test_appendix_mapping_checks_declared_table_not_global_occurrence():
    rows = [
        {
            "pair_id": "1",
            "island_species": "Abrotanella rosulata",
            "island_group": "Campbell",
            "appendix_source_table": "A4",
        }
    ]
    correct = "Table A4 Campbell species Abrotanella rosulata Table A5 other"
    wrong = "Abrotanella rosulata Table A4 Campbell species other Taxon Table A5"
    assert verify_appendix_mapping(correct, rows)["n_verified"] == 1
    assert verify_appendix_mapping(wrong, rows)["n_verified"] == 0
