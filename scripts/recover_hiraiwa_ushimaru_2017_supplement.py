#!/usr/bin/env python3
"""Recover source-native Hiraiwa-Ushimaru (2017) supplementary bytes.

This is an acquisition/audit utility. It never imputes proboscis length and never
uses downstream reproductive outcomes. The target is Table S2 in the source-native
supplementary material for doi:10.1098/rspb.2016.2218.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path
from typing import Any

TARGET_FILE = "rspb20162218supp1.pdf"
PMCID = "PMC5247496"
DOI = "10.1098/rspb.2016.2218"
FIGSHARE_ARTICLE_ID = 4479803

DIRECT_CANDIDATES = [
    "https://pmc.ncbi.nlm.nih.gov/articles/PMC5247496/bin/rspb20162218supp1.pdf",
    "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5247496/bin/rspb20162218supp1.pdf",
    "https://royalsocietypublishing.org/doi/suppl/10.1098/rspb.2016.2218/suppl_file/rspb20162218supp1.pdf",
    "https://royalsocietypublishing.org/action/downloadSupplement?doi=10.1098%2Frspb.2016.2218&file=rspb20162218supp1.pdf",
]

API_CANDIDATES = [
    f"https://api.figshare.com/v2/articles/{FIGSHARE_ARTICLE_ID}",
    f"https://www.ebi.ac.uk/europepmc/webservices/rest/{PMCID}/fullTextXML",
    f"https://www.ebi.ac.uk/europepmc/webservices/rest/{PMCID}/supplementaryFiles",
]


def request(url: str, *, timeout: int = 90) -> tuple[bytes, dict[str, str], str]:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "izu-core-source-audit/1.0 (+https://github.com/zuizui0223/izu-core)",
            "Accept": "application/pdf, application/zip, application/json, application/xml, text/xml, */*;q=0.5",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as response:
        payload = response.read()
        headers = {str(k).lower(): str(v) for k, v in response.headers.items()}
        final_url = str(response.geturl())
    return payload, headers, final_url


def sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def is_pdf(payload: bytes) -> bool:
    return payload.startswith(b"%PDF")


def is_zip(payload: bytes) -> bool:
    return zipfile.is_zipfile(io.BytesIO(payload))


def save_pdf(payload: bytes, outdir: Path, source: dict[str, Any]) -> Path:
    path = outdir / TARGET_FILE
    path.write_bytes(payload)
    source["pdf_sha256"] = sha256(payload)
    source["pdf_size_bytes"] = len(payload)
    return path


def extract_pdf_text(pdf_path: Path, outdir: Path) -> dict[str, Any]:
    from pypdf import PdfReader

    reader = PdfReader(str(pdf_path))
    pages: list[str] = []
    for page_no, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        pages.append(f"\n\n===== PAGE {page_no} =====\n{text}")
    full_text = "".join(pages)
    (outdir / "supplementary_material_text.txt").write_text(full_text, encoding="utf-8")

    matches = [m.start() for m in re.finditer(r"Table\s+S2\b", full_text, flags=re.IGNORECASE)]
    window = ""
    if matches:
        start = max(0, matches[0] - 1500)
        next_s3 = re.search(r"Table\s+S3\b", full_text[matches[0] + 1 :], flags=re.IGNORECASE)
        if next_s3:
            end = matches[0] + 1 + next_s3.start()
        else:
            end = min(len(full_text), matches[0] + 90000)
        window = full_text[start:end]
    (outdir / "table_s2_text_window.txt").write_text(window, encoding="utf-8")
    return {
        "n_pdf_pages": len(reader.pages),
        "extracted_text_characters": len(full_text),
        "table_s2_heading_hits": len(matches),
        "table_s2_window_characters": len(window),
    }


def try_direct(outdir: Path, audit: list[dict[str, Any]]) -> tuple[Path | None, dict[str, Any] | None]:
    for url in DIRECT_CANDIDATES:
        row: dict[str, Any] = {"route": "direct_pdf", "url": url}
        try:
            payload, headers, final_url = request(url)
            row.update(
                {
                    "status": "fetched",
                    "final_url": final_url,
                    "content_type": headers.get("content-type", ""),
                    "size_bytes": len(payload),
                    "sha256": sha256(payload),
                    "is_pdf": is_pdf(payload),
                }
            )
            if is_pdf(payload):
                row["status"] = "accepted_pdf"
                audit.append(row)
                return save_pdf(payload, outdir, row), row
            row["prefix_preview"] = payload[:200].decode("utf-8", errors="replace")
        except Exception as exc:  # acquisition audit must record provider failures
            row.update({"status": "failed", "error": f"{type(exc).__name__}: {exc}"})
        audit.append(row)
    return None, None


def try_figshare(outdir: Path, audit: list[dict[str, Any]]) -> tuple[Path | None, dict[str, Any] | None]:
    url = f"https://api.figshare.com/v2/articles/{FIGSHARE_ARTICLE_ID}"
    row: dict[str, Any] = {"route": "figshare_api", "url": url}
    try:
        payload, headers, final_url = request(url)
        metadata = json.loads(payload.decode("utf-8"))
        (outdir / "figshare_article_metadata.json").write_text(
            json.dumps(metadata, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        row.update(
            {
                "status": "metadata_fetched",
                "final_url": final_url,
                "article_id": metadata.get("id"),
                "version": metadata.get("version"),
                "title": metadata.get("title"),
                "n_files": len(metadata.get("files") or []),
            }
        )
        audit.append(row)
        files = metadata.get("files") or []
        ranked = sorted(
            files,
            key=lambda item: (
                0 if str(item.get("name", "")).lower() == TARGET_FILE.lower() else 1,
                0 if str(item.get("name", "")).lower().endswith(".pdf") else 1,
            ),
        )
        for item in ranked:
            download_url = str(item.get("download_url") or "")
            if not download_url:
                continue
            frow: dict[str, Any] = {
                "route": "figshare_file",
                "file_id": item.get("id"),
                "file_name": item.get("name"),
                "url": download_url,
            }
            try:
                fpayload, fheaders, ffinal = request(download_url)
                frow.update(
                    {
                        "status": "fetched",
                        "final_url": ffinal,
                        "content_type": fheaders.get("content-type", ""),
                        "size_bytes": len(fpayload),
                        "sha256": sha256(fpayload),
                        "is_pdf": is_pdf(fpayload),
                    }
                )
                if is_pdf(fpayload) and (
                    str(item.get("name", "")).lower() == TARGET_FILE.lower()
                    or "supplement" in str(item.get("name", "")).lower()
                    or len(fpayload) > 1_000_000
                ):
                    frow["status"] = "accepted_pdf"
                    audit.append(frow)
                    return save_pdf(fpayload, outdir, frow), frow
            except Exception as exc:
                frow.update({"status": "failed", "error": f"{type(exc).__name__}: {exc}"})
            audit.append(frow)
    except Exception as exc:
        row.update({"status": "failed", "error": f"{type(exc).__name__}: {exc}"})
        audit.append(row)
    return None, None


def try_europe_pmc(outdir: Path, audit: list[dict[str, Any]]) -> tuple[Path | None, dict[str, Any] | None]:
    # First try the supplementaryFiles endpoint, which may return a zip archive.
    supp_url = f"https://www.ebi.ac.uk/europepmc/webservices/rest/{PMCID}/supplementaryFiles"
    row: dict[str, Any] = {"route": "europe_pmc_supplementary", "url": supp_url}
    try:
        payload, headers, final_url = request(supp_url)
        row.update(
            {
                "status": "fetched",
                "final_url": final_url,
                "content_type": headers.get("content-type", ""),
                "size_bytes": len(payload),
                "sha256": sha256(payload),
                "is_pdf": is_pdf(payload),
                "is_zip": is_zip(payload),
            }
        )
        if is_pdf(payload):
            row["status"] = "accepted_pdf"
            audit.append(row)
            return save_pdf(payload, outdir, row), row
        if is_zip(payload):
            zip_path = outdir / "europe_pmc_supplementary_files.zip"
            zip_path.write_bytes(payload)
            with zipfile.ZipFile(io.BytesIO(payload)) as archive:
                names = archive.namelist()
                row["archive_members"] = names
                targets = [name for name in names if name.lower().endswith(TARGET_FILE.lower())]
                if not targets:
                    targets = [name for name in names if name.lower().endswith(".pdf")]
                for name in targets:
                    candidate = archive.read(name)
                    if is_pdf(candidate):
                        row["status"] = "accepted_pdf_from_zip"
                        row["accepted_member"] = name
                        audit.append(row)
                        return save_pdf(candidate, outdir, row), row
        row["prefix_preview"] = payload[:200].decode("utf-8", errors="replace")
    except Exception as exc:
        row.update({"status": "failed", "error": f"{type(exc).__name__}: {exc}"})
    audit.append(row)

    xml_url = f"https://www.ebi.ac.uk/europepmc/webservices/rest/{PMCID}/fullTextXML"
    xrow: dict[str, Any] = {"route": "europe_pmc_xml", "url": xml_url}
    try:
        payload, headers, final_url = request(xml_url)
        text = payload.decode("utf-8", errors="replace")
        (outdir / "europe_pmc_fulltext.xml").write_text(text, encoding="utf-8")
        hrefs = sorted(set(re.findall(r'(?:xlink:href|href)=[\"\']([^\"\']+)[\"\']', text)))
        relevant = [href for href in hrefs if "rspb20162218supp1" in href.lower()]
        xrow.update(
            {
                "status": "fetched",
                "final_url": final_url,
                "content_type": headers.get("content-type", ""),
                "size_bytes": len(payload),
                "sha256": sha256(payload),
                "relevant_hrefs": relevant,
            }
        )
        for href in relevant:
            candidates = []
            if href.startswith("http"):
                candidates.append(href)
            else:
                candidates.extend(
                    [
                        urllib.parse.urljoin("https://pmc.ncbi.nlm.nih.gov/articles/PMC5247496/bin/", href),
                        urllib.parse.urljoin("https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5247496/bin/", href),
                    ]
                )
            for candidate_url in candidates:
                hrow: dict[str, Any] = {"route": "europe_pmc_xml_href", "url": candidate_url}
                try:
                    hpayload, hheaders, hfinal = request(candidate_url)
                    hrow.update(
                        {
                            "status": "fetched",
                            "final_url": hfinal,
                            "content_type": hheaders.get("content-type", ""),
                            "size_bytes": len(hpayload),
                            "sha256": sha256(hpayload),
                            "is_pdf": is_pdf(hpayload),
                        }
                    )
                    if is_pdf(hpayload):
                        hrow["status"] = "accepted_pdf"
                        audit.extend([xrow, hrow])
                        return save_pdf(hpayload, outdir, hrow), hrow
                except Exception as exc:
                    hrow.update({"status": "failed", "error": f"{type(exc).__name__}: {exc}"})
                audit.append(hrow)
    except Exception as exc:
        xrow.update({"status": "failed", "error": f"{type(exc).__name__}: {exc}"})
    audit.append(xrow)
    return None, None


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    outdir = args.output_dir
    outdir.mkdir(parents=True, exist_ok=True)

    audit: list[dict[str, Any]] = []
    pdf_path: Path | None = None
    accepted_source: dict[str, Any] | None = None

    # Use independent lawful public routes. A failed route is recorded, not treated as evidence.
    for recovery in (try_figshare, try_direct, try_europe_pmc):
        pdf_path, accepted_source = recovery(outdir, audit)
        if pdf_path is not None:
            break

    extraction: dict[str, Any] = {}
    if pdf_path is not None:
        extraction = extract_pdf_text(pdf_path, outdir)

    status = "source_pdf_recovered" if pdf_path is not None else "blocked_no_source_pdf_recovered"
    result = {
        "contract": "hiraiwa_ushimaru_2017_source_proboscis_recovery_v1",
        "article_doi": DOI,
        "pmcid": PMCID,
        "target_file": TARGET_FILE,
        "target_table": "Table S2 species x site mean proboscis length in mm",
        "status": status,
        "accepted_source": accepted_source,
        "extraction": extraction,
        "n_routes_attempted": len(audit),
        "audit": audit,
        "claim_boundary": (
            "Acquisition only. No trait midpoint, family proxy, fuzzy taxon match, downstream reproductive outcome, "
            "or inferred proboscis value is used. A recovered PDF opens source-row extraction but does not itself "
            "validate the 211-versus-209 taxon mapping or an empirical signed-position estimand."
        ),
    }
    (outdir / "recovery_audit.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    lines = [
        "# Hiraiwa-Ushimaru 2017 proboscis source recovery",
        "",
        f"Status: **{status}**",
        f"Target: `{TARGET_FILE}` / Table S2.",
        "",
    ]
    if accepted_source:
        lines += [
            f"Accepted route: `{accepted_source.get('route')}`",
            f"SHA256: `{accepted_source.get('pdf_sha256') or accepted_source.get('sha256')}`",
            f"PDF bytes: `{accepted_source.get('pdf_size_bytes') or accepted_source.get('size_bytes')}`",
            f"Table S2 heading hits after text extraction: `{extraction.get('table_s2_heading_hits', 0)}`",
            "",
        ]
    lines += ["## Route audit", ""]
    for row in audit:
        lines.append(f"- `{row.get('route')}` — `{row.get('status')}` — {row.get('url', '')}")
    (outdir / "recovery_summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(json.dumps({"status": status, "accepted_source": accepted_source, "extraction": extraction}, indent=2))


if __name__ == "__main__":
    main()
