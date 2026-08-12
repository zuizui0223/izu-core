from scripts.audit_cross_archipelago_morphology_source_routes import (
    candidate_links,
    repository_search_urls,
    route_urls,
)


def test_candidate_links_extracts_repository_and_pdf_routes_only():
    html = '''
    <a href="https://tspace.library.utoronto.ca/example">TSpace</a>
    <a href="https://hdl.handle.net/1807/12345">Handle</a>
    <a href="https://openaccess.wgtn.ac.nz/ndownloader/files/31690700">VUW download</a>
    <a href="/files/thesis.pdf">PDF</a>
    <a href="https://example.org/about">About</a>
    '''
    links = candidate_links(html, "https://library-archives.canada.ca/item")
    assert "https://tspace.library.utoronto.ca/example" in links
    assert "https://hdl.handle.net/1807/12345" in links
    assert "https://openaccess.wgtn.ac.nz/ndownloader/files/31690700" in links
    assert "https://library-archives.canada.ca/files/thesis.pdf" in links
    assert "https://example.org/about" not in links


def test_hendriks_route_generation_queries_title_and_author():
    source = {
        "source_id": "hendriks_2019_flower_area",
        "title": "The island rule and its application to multiple plant traits",
        "author": "Annemieke Lona Hedi Hendriks",
        "known_routes": [
            {
                "url": "https://openaccess.wgtn.ac.nz/articles/thesis/The_island_rule_and_its_application_to_multiple_plant_traits/17136800"
            }
        ],
        "institutional_repository": {"base_url": "https://openaccess.wgtn.ac.nz/"},
    }
    searches = repository_search_urls(source)
    assert len(searches) == 3
    assert all(url.startswith("https://openaccess.wgtn.ac.nz/search?q=") for url in searches)
    urls = route_urls(source)
    assert urls[0].startswith("https://openaccess.wgtn.ac.nz/articles/thesis/")
    assert "https://openaccess.wgtn.ac.nz/" in urls
    assert any("island+rule" in url.lower() for url in urls)
    assert any("annemieke" in url.lower() for url in urls)


def test_hetherington_route_generation_queries_both_utoronto_frontends():
    source = {
        "source_id": "hetherington_rauth_johnson_2020_136_pairs",
        "thesis_title": "The Comparative Evolution of the Floral Traits of Island Angiosperms",
        "thesis_author": "Molly Christina Hetherington-Rauth",
        "known_routes": [{"url": "https://library-archives.canada.ca/example"}],
    }
    searches = repository_search_urls(source)
    assert len(searches) == 6
    assert any(url.startswith("https://utoronto.scholaris.ca/search?query=") for url in searches)
    assert any(url.startswith("https://tspace.library.utoronto.ca/simple-search?query=") for url in searches)
    urls = route_urls(source)
    assert urls[0] == "https://library-archives.canada.ca/example"
    assert any("comparative+evolution" in url.lower() for url in urls)
    assert any("molly+christina" in url.lower() for url in urls)


def test_route_discovery_never_implies_admission():
    from scripts import audit_cross_archipelago_morphology_source_routes as routes

    # The audit contract is discovery-only even when a candidate PDF is visible.
    assert "admission" in routes.__doc__.lower()
    assert "never by itself opens" in routes.__doc__.lower()
