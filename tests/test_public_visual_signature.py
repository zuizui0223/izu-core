from channel_id.public_visual_signature import add_within_taxon_salience, summarize_group_signatures, transition_contrasts


def row(taxon: str, group: str, regime: str, image_id: str, values: tuple[float, float, float, float, float]):
    return {
        "taxon": taxon,
        "analysis_group": group,
        "pollinator_regime": regime,
        "image_id": image_id,
        "feature_status": "ok",
        "mean_saturation": values[0],
        "colourfulness": values[1],
        "radial_chroma_contrast": values[2],
        "hue_entropy": values[3],
        "edge_density": values[4],
    }


def test_taxon_can_contribute_to_second_transition_without_mainland_images():
    data = [
        row("Specialist", "specialist", "ardens", "a1", (2, 2, 2, 2, 2)),
        row("Specialist", "specialist", "ardens", "a2", (2.1, 2.1, 2.1, 2.1, 2.1)),
        row("Specialist", "specialist", "no_bombus", "n1", (1, 1, 1, 1, 1)),
        row("Specialist", "specialist", "no_bombus", "n2", (1.1, 1.1, 1.1, 1.1, 1.1)),
    ]
    contrasts = transition_contrasts(add_within_taxon_salience(data), min_images_per_regime=2, bootstrap_draws=20)
    assert len(contrasts) == 1
    assert contrasts[0]["transition"] == "ardens_to_no_bombus"
    assert contrasts[0]["point_direction"] == "decrease"


def test_images_do_not_become_independent_taxa_in_group_summary():
    data = []
    for taxon in ("A", "B"):
        for index in range(3):
            data.append(row(taxon, "generalist", "ardens", f"{taxon}a{index}", (1, 1, 1, 1, 1)))
            data.append(row(taxon, "generalist", "no_bombus", f"{taxon}n{index}", (1, 1, 1, 1, 1)))
    contrasts = transition_contrasts(add_within_taxon_salience(data), min_images_per_regime=2, bootstrap_draws=20)
    summary = summarize_group_signatures(contrasts)
    second = next(row for row in summary if row["transition"] == "ardens_to_no_bombus")
    assert second["taxa_contributing"] == 2
    assert second["taxa_flat"] == 2


def test_within_taxon_normalisation_does_not_compare_raw_colours_between_taxa():
    data = [
        row("Low", "generalist", "ardens", "l1", (0.1, 0.1, 0.1, 0.1, 0.1)),
        row("Low", "generalist", "no_bombus", "l2", (0.2, 0.2, 0.2, 0.2, 0.2)),
        row("High", "generalist", "ardens", "h1", (10, 10, 10, 10, 10)),
        row("High", "generalist", "no_bombus", "h2", (11, 11, 11, 11, 11)),
    ]
    enriched = add_within_taxon_salience(data)
    low = [item for item in enriched if item["taxon"] == "Low"]
    high = [item for item in enriched if item["taxon"] == "High"]
    assert abs(low[0]["visual_salience_v1"] - high[0]["visual_salience_v1"]) < 1e-12
