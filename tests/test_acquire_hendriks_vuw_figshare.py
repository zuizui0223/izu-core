from scripts.acquire_hendriks_vuw_figshare import (
    article_id_from_source,
    build_lock,
    expected_file_id_from_source,
    select_expected_file,
    validate_article_metadata,
)


def source_fixture():
    return {
        "source_id": "hendriks_2019_flower_area_table_b9",
        "title": "The island rule and its application to multiple plant traits",
        "institutional_identifier": "10.26686/wgtn.17136800",
        "institutional_record_page": "https://openaccess.wgtn.ac.nz/articles/thesis/The_island_rule_and_its_application_to_multiple_plant_traits/17136800",
        "institutional_download_url": "https://openaccess.wgtn.ac.nz/ndownloader/files/31690700",
    }


def test_source_routes_resolve_expected_figshare_ids():
    source = source_fixture()
    assert article_id_from_source(source) == 17136800
    assert expected_file_id_from_source(source) == 31690700


def test_article_identity_and_expected_file_are_strict():
    source = source_fixture()
    metadata = {
        "title": source["title"],
        "doi": source["institutional_identifier"],
        "files": [
            {
                "id": 31690700,
                "name": "hendriks_thesis.pdf",
                "download_url": "https://ndownloader.figshare.com/files/31690700",
            }
        ],
    }
    validate_article_metadata(metadata, source)
    selected = select_expected_file(metadata, 31690700)
    assert selected["id"] == 31690700


def test_checksum_lock_does_not_auto_open_provenance_or_eiv():
    source = source_fixture()
    data = b"%PDF-1.7\nsynthetic test bytes only\n"
    import hashlib

    md5 = hashlib.md5(data).hexdigest()  # nosec B324 - integrity test only
    metadata = {"title": source["title"], "doi": source["institutional_identifier"]}
    file_metadata = {
        "id": 31690700,
        "name": "hendriks_thesis.pdf",
        "download_url": "https://ndownloader.figshare.com/files/31690700",
        "supplied_md5": md5,
        "computed_md5": md5,
    }
    lock = build_lock(
        source=source,
        article_id=17136800,
        metadata=metadata,
        file_metadata=file_metadata,
        data=data,
        final_download_url=file_metadata["download_url"],
    )
    assert lock["checksums"]["pdf_magic_valid"] is True
    assert lock["checksums"]["md5"] == md5
    assert lock["provenance_gate_opened"] is False
    assert lock["pair_verification_complete"] is False
    assert lock["eiv_gate_opened"] is False
    assert lock["formal_cross_system_admission_opened"] is False
