"""Probe iNaturalist: per-island research-grade photo availability for Tier-C."""
import json, urllib.request, urllib.parse, time

islands = {
    "Oshima":    (34.7385, 139.4024, 8),
    "Toshima":   (34.5230, 139.2800, 5),
    "Niijima":   (34.3813, 139.2654, 6),
    "Kozushima": (34.2142, 139.1523, 6),
    "Miyake":    (34.0854, 139.5213, 8),
    "Hachijo":   (33.1025, 139.8077, 8),
}
# specialist / generalist / large-flower candidates that span the gradient
species = [
    ("Campanula microdonta", "specialist"),
    ("Weigela coraeensis", "specialist"),
    ("Clerodendrum trichotomum", "specialist"),
    ("Hydrangea macrophylla", "generalist"),
    ("Ligustrum ovalifolium", "generalist"),
    ("Farfugium japonicum", "generalist"),
    ("Lilium maculatum", "large_flower"),
    ("Rhododendron kaempferi", "large_flower"),
]

def count(sp, lat, lng, radius):
    params = {
        "taxon_name": sp, "lat": lat, "lng": lng, "radius": radius,
        "quality_grade": "research", "photos": "true", "per_page": 0,
    }
    url = "https://api.inaturalist.org/v1/observations?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "izu-meta-analysis-probe"})
    try:
        with urllib.request.urlopen(req, timeout=40) as r:
            return json.load(r).get("total_results", 0)
    except Exception as e:
        return f"err:{e}"

print(f"{'species':26s} {'grp':12s} " + " ".join(f"{k[:5]:>5s}" for k in islands) + "   TOT nISL")
for sp, grp in species:
    counts = {}
    for isl, (lat, lng, rad) in islands.items():
        counts[isl] = count(sp, lat, lng, rad)
        time.sleep(0.7)
    nums = [c if isinstance(c, int) else 0 for c in counts.values()]
    tot = sum(nums)
    nisl = sum(1 for c in nums if c > 0)
    print(f"{sp:26s} {grp:12s} " + " ".join(f"{counts[k]!s:>5s}" for k in islands) + f"   {tot:>4d} {nisl:>3d}")
