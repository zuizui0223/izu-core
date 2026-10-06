# Chapter 2 public archive preparation — 2026-10-06

## Current state

The scientific branch has been merged to main. The remaining Ecology Letters
pre-submission dependency is a permanent public archive with DOI.

This route preserves the exact GitHub Actions ZIP bytes underlying both
prospective campaigns rather than only the summarized JSON committed to git.

- independent confirmation: 4,096 trajectories, 16 shard artifacts + 1 result artifact;
- four-setting assurance generality: 8,448 trajectories, 32 shard artifacts + 1 result artifact;
- total tracked GitHub Actions artifacts: 50;
- every artifact has an API-reported SHA-256 digest recorded in
  `data/design/chapter2_public_archive_manifest_20261006.json`.

The manifest also records frozen design SHA-256 values, workflow run IDs,
committed result files, derived attenuation/gradient diagnostics and the active
Ecology Letters manuscript.

## Automated bundle

`.github/workflows/chapter2-public-archive.yml` downloads the original artifact
ZIP bytes from the two frozen workflow runs, verifies every SHA-256 against the
manifest, and builds:

`outputs/chapter2_public_archive/chapter2_public_archive_20261006.zip`

The builder stores the original artifact ZIPs without recompressing their
contents. The receipt records source main SHA, artifact count, raw byte total and
final bundle SHA-256.

## Claim boundary

This workflow prepares a deposition-ready scientific data bundle. It does not
mint a DOI, publish to a third-party repository, or invent creator/license
metadata. DOI assignment and repository-specific metadata remain an external
deposition action.
