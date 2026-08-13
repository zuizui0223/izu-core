#!/usr/bin/env python3
"""Bytes-safe entrypoint for public Oxford Academic supplementary data.

This wrapper preserves the source-discovery and provenance logic of the original
acquirer while replacing its HTML payload classifier with a bytes-safe
implementation. A blocked publisher response remains an acquisition state, not a
biological result.
"""
from __future__ import annotations

from typing import Mapping

import acquire_oup_supplementary_data as legacy


def looks_html(payload: bytes, headers: Mapping[str, str]) -> bool:
    if legacy.content_type(headers) in {"text/html", "application/xhtml+xml"}:
        return True
    prefix = payload[:500].lstrip().lower()
    return prefix.startswith(b"<!doctype html") or prefix.startswith(b"<html")


legacy.looks_html = looks_html

# Re-export tested helpers and the source-acquisition entrypoint.
parse_links = legacy.parse_links
is_candidate_link = legacy.is_candidate_link
content_disposition_filename = legacy.content_disposition_filename
safe_filename = legacy.safe_filename
valid_data_payload = legacy.valid_data_payload
main = legacy.main


if __name__ == "__main__":
    main()
