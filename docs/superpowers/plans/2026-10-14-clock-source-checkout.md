# Clock source checkout Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Preserve the PR503 original source/input byte anchors under Windows and Unix Git checkout.

**Architecture:** Add narrowly scoped LF checkout attributes and test real Git index-to-worktree conversion. No biological code, source pins, conditions or statistical decisions change.

**Tech Stack:** Git, Python, pytest.

**Spec:** PR496–503 source-identity contracts and the P2 checkout finding from the pinned183a386f source review.

1. Add a regression using exact Git source bytes in an isolated Git fixture, with core.autocrlf true and false. Confirm the Windows-style checkout fails before correction.
2. Apply LF checkout rules only to pinned clock JSON/scripts and the five original native biological modules. Re-run without relaxing original hashes.
3. Verify protected tracked file blobs remain unchanged and run relevant non-biological producer/reader/packaging tests. Do not execute registered scientific paths. Keep cross-BLAS numerical STOP as a separate limitation.
4. Obtain independent review, publish a corrective branch/PR against the PR503 route, and verify exact-source CI. Preserve the alternate PR498/499 route as separate provenance.
