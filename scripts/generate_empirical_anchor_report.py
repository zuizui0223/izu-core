"""Render a transparent empirical-to-simulation anchor report.

The command reads population spot summaries, one P_ST--F_ST summary, one
selfed/outcrossed fitness summary, and pollinator guild availability records.
It reports observed inputs separately from declared service-gradient assumptions.
It does not fit a mechanism to field data.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from channel_id.empirical_gradient_anchor import (
    EmpiricalGradientAssumptions,
    load_empirical_anchor_bundle,
    render_empirical_anchor_report,
    write_empirical_anchor_templates,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input-dir",
        type=Path,
        help="Directory containing the four empirical-anchor CSV files.",
    )
    parser.add_argument(
        "--write-templates",
        type=Path,
        default=None,
        help="Write blank CSV templates and README to this directory, then exit.",
    )
    parser.add_argument("--focal-guild", default=None)
    parser.add_argument("--service-low", type=float, default=0.25)
    parser.add_argument("--service-high", type=float, default=0.75)
    parser.add_argument("--trait-contrast-min", type=float, default=0.0)
    parser.add_argument("--trait-contrast-max", type=float, default=1.0)
    parser.add_argument("--establishment-multiplier", type=float, default=1.0)
    parser.add_argument("--output", type=Path, default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.write_templates is not None:
        if args.input_dir is not None or args.focal_guild is not None:
            raise SystemExit("--write-templates cannot be combined with empirical input options")
        for path in write_empirical_anchor_templates(args.write_templates):
            print(path)
        return
    if args.input_dir is None or args.focal_guild is None:
        raise SystemExit("--input-dir and --focal-guild are required unless --write-templates is used")
    try:
        bundle = load_empirical_anchor_bundle(args.input_dir)
        assumptions = EmpiricalGradientAssumptions(
            focal_guild=args.focal_guild,
            trait_contrast_min=args.trait_contrast_min,
            trait_contrast_max=args.trait_contrast_max,
            pollinator_service_low=args.service_low,
            pollinator_service_high=args.service_high,
            establishment_multiplier=args.establishment_multiplier,
        )
        rendered = render_empirical_anchor_report(bundle, assumptions)
    except (OSError, ValueError) as error:
        raise SystemExit(str(error)) from error
    if args.output is None:
        print(rendered, end="")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")


if __name__ == "__main__":
    main()
