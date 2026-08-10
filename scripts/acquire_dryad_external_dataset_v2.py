#!/usr/bin/env python3
"""Harden the generic Dryad acquisition entrypoint against HTML payloads.

This wrapper preserves the version-aware resolver while replacing the payload
classifier with a bytes-safe implementation.  It exists separately so the
source acquisition contract can be verified before the older entrypoint is
retired.
"""
from __future__ import annotations

import acquire_dryad_external_dataset as legacy


def looks_html(payload: bytes) -> bool:
    prefix = payload[:500].lstrip().lower()
    return prefix.startswith(b"<!doctype html") or prefix.startswith(b"<html")


legacy.looks_html = looks_html

# Re-export the tested acquisition helpers.
id_from_links = legacy.id_from_links
version_sort_key = legacy.version_sort_key
source_filename = legacy.source_filename
zip_info_urls = legacy.zip_info_urls
valid_payload = legacy.valid_payload
main = legacy.main


if __name__ == "__main__":
    main()
