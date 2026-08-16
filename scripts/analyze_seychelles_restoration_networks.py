#!/usr/bin/env python3
"""Summarize the source-native 64-network Seychelles restoration panel.

The independent treatment unit is the site. Months are repeated observations
within sites. This script therefore reports network-row scale and site-level
means separately and does not treat 64 site-month rows as 64 independent
replicates.
"""
from __future__ import annotations
import argparse, csv, hashlib, json
from collections import Counter, defaultdict
from pathlib import Path

METRICS = (
    "mean_freq_visit", "sum_freq_visit", "mean_visitation_rate",
    "total_visitation_rate", "mean_visits", "total_visits",
    "network_size", "nestedness", "connectance",
)


def read_csv(path: Path):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def f(row, key):
    text=str(row.get(key) or "").strip()
    return float(text) if text else None


def mean(values):
    vals=[v for v in values if v is not None]
    return sum(vals)/len(vals) if vals else None


def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--root",type=Path,default=Path("artifacts/seychelles_restoration_iwdb")); ap.add_argument("--csv",type=Path,default=Path("artifacts/seychelles_restoration_iwdb/empirical_extracted/all_dat.csv")); ap.add_argument("--out",type=Path,default=Path("artifacts/seychelles_restoration_iwdb/analysis/summary.json")); args=ap.parse_args()
    rows=read_csv(args.csv)
    required={"site","Treatment","month",*METRICS}
    if not rows or not required.issubset(rows[0]):
        raise ValueError(f"all_dat schema mismatch; missing {sorted(required-set(rows[0]) if rows else required)}")
    sites=sorted({r["site"] for r in rows}); months=sorted({int(float(r["month"])) for r in rows}); treatments=sorted({r["Treatment"] for r in rows})
    if len(rows)!=64 or len(sites)!=8 or len(months)!=8:
        raise ValueError(f"expected 64 rows / 8 sites / 8 months, got {len(rows)} / {len(sites)} / {len(months)}")
    site_rows=defaultdict(list)
    for r in rows: site_rows[r["site"]].append(r)
    if any(len(v)!=8 for v in site_rows.values()): raise ValueError("each site must contribute exactly 8 monthly rows")
    site_treatment={site: sorted({r["Treatment"] for r in rr}) for site,rr in site_rows.items()}
    if any(len(v)!=1 for v in site_treatment.values()): raise ValueError("treatment changes within site")
    treatment_site_counts=Counter(v[0] for v in site_treatment.values())
    if treatment_site_counts != Counter({"Restored":4,"Unrestored":4}): raise ValueError(f"unexpected treatment-site allocation {treatment_site_counts}")

    site_means={}
    for site,rr in sorted(site_rows.items()):
        site_means[site]={"treatment":site_treatment[site][0],"n_months":len(rr),**{metric:mean(f(r,metric) for r in rr) for metric in METRICS}}
    treatment_means={}
    for tr in ("Restored","Unrestored"):
        members=[v for v in site_means.values() if v["treatment"]==tr]
        treatment_means[tr]={"n_sites":len(members),**{metric:mean(v[metric] for v in members) for metric in METRICS}}
    contrasts={metric:treatment_means["Restored"][metric]-treatment_means["Unrestored"][metric] for metric in METRICS}
    rdata=list(args.root.rglob("Empirical_data.RData"))
    if len(rdata)!=1: raise ValueError(f"expected one Empirical_data.RData, found {len(rdata)}")
    source_bytes=rdata[0].read_bytes()
    report={
        "schema_version":"1.0",
        "source_id":"kaiser_bunbury_et_al_2017_seychelles_restoration_networks",
        "article_doi":"10.1038/nature21071",
        "source_transport":"Kaiser-Bunbury et al. 2017 empirical table extracted from Empirical_data.RData in the configured Zenodo transport fallback when IWDB timed out",
        "source_empirical_object":{"object":"all_dat","rdata_bytes":len(source_bytes),"rdata_sha256":hashlib.sha256(source_bytes).hexdigest()},
        "scale":{"network_rows":len(rows),"sites":len(sites),"months":len(months),"site_months_per_site":{site:len(rr) for site,rr in sorted(site_rows.items())},"treatment_sites":dict(treatment_site_counts)},
        "sites":site_means,
        "treatment_site_level_means":treatment_means,
        "restored_minus_unrestored_site_mean":contrasts,
        "source_contract_context":{"reported_observation_hours":1525,"reported_unique_links":581,"reported_pollinator_visits":12235,"reading":"These study-scale values come from the source contract/article and are not reverse-engineered from all_dat when the table does not encode the required raw identity/effort fields."},
        "analysis_unit_boundary":"The 64 rows are site x month repeated observations. Site is the treatment-level independent unit (4 restored, 4 unrestored); months are not independent restoration replicates.",
        "claim_boundary":"This is a source-native network/visitation restoration panel from one Mahe experiment. Descriptive restored-minus-unrestored contrasts do not establish direct plant reproductive dependency, historical floral evolution, or an additional independent archipelago."
    }
    args.out.parent.mkdir(parents=True,exist_ok=True); args.out.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8"); print(json.dumps(report,indent=2,ensure_ascii=False))

if __name__=="__main__": main()
