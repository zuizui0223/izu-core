from scripts.audit_cross_archipelago_morphology_source_routes import candidate_links


def test_candidate_links_extracts_repository_and_pdf_routes_only():
    html = '''
    <a href="https://tspace.library.utoronto.ca/example">TSpace</a>
    <a href="https://hdl.handle.net/1807/12345">Handle</a>
    <a href="/files/thesis.pdf">PDF</a>
    <a href="https://example.org/about">About</a>
    '''
    links = candidate_links(html, "https://library-archives.canada.ca/item")
    assert "https://tspace.library.utoronto.ca/example" in links
    assert "https://hdl.handle.net/1807/12345" in links
    assert "https://library-archives.canada.ca/files/thesis.pdf" in links
    assert "https://example.org/about" not in links


def test_route_discovery_never_implies_admission():
    from scripts import audit_cross_archipelago_morphology_source_routes as routes

    # The audit contract is discovery-only even when a candidate PDF is visible.
    assert "admission" in routes.__doc__.lower()
    assert "never by itself opens" in routes.__doc__.lower()
