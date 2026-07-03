"""Assign a pollination functional group (the meta-analysis moderator) to each
Izu gradient-spanning candidate species.

Groups (predicted response to bumblebee loss):
  specialist_bee   zygomorphic/tubular, long-tongued-/bumblebee-dependent  -> PREDICT reduction + selfing
  generalist_open  small radial, accessible to many small insects          -> PREDICT weak / no trend (negative control)
  large_flower     large flowers, non-bumblebee vectors (hawkmoth/bird)     -> counter-direction (may enlarge)
  nonbee_special   fly/gnat/beetle/deceptive systems                        -> off-hypothesis
  abiotic_ambig    wind/water or strongly selfing/ambiguous                 -> excluded from primary test

Assignment is by family with genus-level overrides, each carrying a confidence.
It is a transparent first pass to be refined against pollination literature;
`basis` and `confidence` are recorded so low-confidence calls can be revisited.
"""

from __future__ import annotations

import csv
import pathlib
from collections import Counter

HERE = pathlib.Path(__file__).parent
CANDS = HERE / "izu_entomophilous_candidates.csv"
OUT = HERE / "functional_group_classification.csv"

FAMILY_GROUP = {
    # specialist long-tongued / bumblebee bee flowers (zygomorphic or tubular)
    "Campanulaceae": ("specialist_bee", "high"),
    "Lamiaceae": ("specialist_bee", "high"),
    "Fabaceae": ("specialist_bee", "high"),
    "Caprifoliaceae": ("specialist_bee", "medium"),   # Weigela/Lonicera tubular
    "Apocynaceae": ("specialist_bee", "medium"),
    "Violaceae": ("specialist_bee", "medium"),          # spurred, bee; note high cleistogamy
    # generalist open, small radial flowers
    "Apiaceae": ("generalist_open", "high"),
    "Araliaceae": ("generalist_open", "high"),
    "Rosaceae": ("generalist_open", "high"),
    "Hydrangeaceae": ("generalist_open", "high"),
    "Oleaceae": ("generalist_open", "medium"),
    "Elaeagnaceae": ("generalist_open", "medium"),
    "Aquifoliaceae": ("generalist_open", "high"),
    "Celastraceae": ("generalist_open", "high"),
    "Pittosporaceae": ("generalist_open", "medium"),
    "Rutaceae": ("generalist_open", "medium"),
    "Rubiaceae": ("generalist_open", "low"),            # Paederia tubular -> uncertain
    "Crassulaceae": ("generalist_open", "medium"),
    "Primulaceae": ("generalist_open", "low"),
    "Berberidaceae": ("generalist_open", "medium"),
    "Ranunculaceae": ("generalist_open", "medium"),
    "Stachyuraceae": ("generalist_open", "low"),
    "Saxifragaceae": ("generalist_open", "medium"),
    "Rhamnaceae": ("generalist_open", "medium"),
    "Sapindaceae": ("generalist_open", "low"),
    "Cornaceae": ("generalist_open", "medium"),
    "Aizoaceae": ("generalist_open", "low"),
    "Oxalidaceae": ("generalist_open", "low"),
    "Pentaphylacaceae": ("generalist_open", "low"),     # Eurya
    "Garryaceae": ("generalist_open", "low"),           # Aucuba (dioecious, small)
    "Daphniphyllaceae": ("generalist_open", "low"),
    # large flowers, non-bumblebee vectors
    "Liliaceae": ("large_flower", "high"),
    "Ericaceae": ("large_flower", "medium"),
    "Theaceae": ("large_flower", "medium"),             # Camellia often bird-pollinated
    "Colchicaceae": ("large_flower", "medium"),
    "Convolvulaceae": ("large_flower", "medium"),
    "Asphodelaceae": ("large_flower", "medium"),        # Hemerocallis
    "Amaryllidaceae": ("large_flower", "medium"),
    "Iridaceae": ("large_flower", "medium"),
    "Styracaceae": ("large_flower", "low"),
    # fly/gnat/beetle/deceptive
    "Araceae": ("nonbee_special", "high"),              # Arisaema fungus-gnat
    "Aristolochiaceae": ("nonbee_special", "high"),
    "Saururaceae": ("nonbee_special", "low"),
    "Piperaceae": ("nonbee_special", "low"),
    # abiotic / ambiguous / strongly selfing
    "Vitaceae": ("abiotic_ambig", "medium"),
    "Euphorbiaceae": ("abiotic_ambig", "medium"),
    "Lauraceae": ("abiotic_ambig", "low"),
    "Commelinaceae": ("abiotic_ambig", "low"),
    "Dioscoreaceae": ("abiotic_ambig", "medium"),
    "Smilacaceae": ("abiotic_ambig", "low"),
    "Cucurbitaceae": ("generalist_open", "low"),
    "Asteraceae": ("generalist_open", "high"),          # composite heads, generalist (see genus overrides)
    "Asparagaceae": ("generalist_open", "low"),
    "Caryophyllaceae": ("generalist_open", "low"),      # but Dianthus -> specialist (override)
    "Viburnaceae": ("generalist_open", "high"),         # Viburnum flat cymes (incl. endemic Shima-gamazumi)
    "Lardizabalaceae": ("generalist_open", "low"),
    "Boraginaceae": ("generalist_open", "medium"),
    "Papaveraceae": ("generalist_open", "medium"),
    "Onagraceae": ("generalist_open", "low"),
    "Clethraceae": ("generalist_open", "low"),
    "Phytolaccaceae": ("generalist_open", "low"),
    "Phyllanthaceae": ("abiotic_ambig", "low"),
    "Schisandraceae": ("nonbee_special", "low"),        # beetle
    "Trochodendraceae": ("generalist_open", "low"),
    "Solanaceae": ("specialist_bee", "medium"),         # buzz pollination
    "Orobanchaceae": ("specialist_bee", "high"),        # zygomorphic
    "Gentianaceae": ("specialist_bee", "medium"),       # tubular
    "Orchidaceae": ("nonbee_special", "medium"),        # specialized/deceptive
}

GENUS_OVERRIDE = {
    "Artemisia": ("abiotic_ambig", "high", "wind-pollinated Asteraceae"),
    "Cirsium": ("specialist_bee", "medium", "thistle: bumblebee/butterfly"),
    "Camellia": ("large_flower", "high", "winter bird (Zosterops) pollination"),
    "Trachelospermum": ("specialist_bee", "medium", "salverform, long-tongued"),
    "Vitex": ("specialist_bee", "medium", "zygomorphic Lamiaceae"),
    "Clerodendrum": ("specialist_bee", "medium", "long-tubed, butterfly/large bee"),
    "Paederia": ("specialist_bee", "low", "long tube; not open-generalist"),
    "Ipomoea": ("large_flower", "medium", "funnelform, large"),
    "Calystegia": ("large_flower", "medium", "funnelform, large"),
    "Hemerocallis": ("large_flower", "high", "large tepals"),
    "Lilium": ("large_flower", "high", "large; hawkmoth/large-bee, incl. Sakuyuri lineage"),
    "Rhododendron": ("large_flower", "high", "large corolla; counter-direction case"),
    "Dianthus": ("specialist_bee", "high", "long-tubed; butterfly/long-tongue (Izu candidate D. japonicus)"),
    "Sigesbeckia": ("generalist_open", "medium", "small composite, generalist"),
}


def classify(name: str, family: str):
    genus = name.split()[0]
    if genus in GENUS_OVERRIDE:
        g, c, why = GENUS_OVERRIDE[genus]
        return g, c, f"genus:{genus} ({why})"
    if family in FAMILY_GROUP:
        g, c = FAMILY_GROUP[family]
        return g, c, f"family:{family}"
    return "review", "none", f"unmapped family:{family}"


def main() -> None:
    rows = list(csv.DictReader(CANDS.open(encoding="utf-8")))
    out_rows = []
    for r in rows:
        g, c, basis = classify(r["name"], r["family"])
        out_rows.append({
            "speciesKey": r["speciesKey"], "name": r["name"], "family": r["family"],
            "n_islands": r["n_islands"], "total_occ": r["total_occ"],
            "functional_group": g, "confidence": c, "basis": basis,
        })
    with OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(out_rows[0].keys()))
        w.writeheader()
        w.writerows(out_rows)

    grp = Counter(r["functional_group"] for r in out_rows)
    conf = Counter(r["confidence"] for r in out_rows)
    print(f"classified {len(out_rows)} species -> {OUT.name}")
    print("by functional group:")
    for k, v in grp.most_common():
        print(f"  {k:18s} {v}")
    print("by confidence:", dict(conf.most_common()))
    # the core moderator contrast
    spec = grp["specialist_bee"]
    gen = grp["generalist_open"]
    print(f"\nprimary moderator contrast: specialist_bee={spec} vs generalist_open={gen}")


if __name__ == "__main__":
    main()
