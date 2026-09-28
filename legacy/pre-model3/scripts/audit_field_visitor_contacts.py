"""Validate effort and visitor-contact manifests and write descriptive summaries."""

from __future__ import annotations

import argparse
from pathlib import Path

from channel_id.field_legitimate_contact import (
    audit_field_contacts,
    read_effort_manifest,
    read_visit_manifest,
    write_field_contact_audit,
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--effort", type=Path, required=True)
    parser.add_argument("--visits", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    try:
        effort_rows = read_effort_manifest(args.effort)
        visit_rows = read_visit_manifest(args.visits)
        write_field_contact_audit(args.output_dir, audit_field_contacts(effort_rows, visit_rows))
    except (OSError, ValueError) as error:
        raise SystemExit(str(error)) from error


if __name__ == "__main__":
    main()
