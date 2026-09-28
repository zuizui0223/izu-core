# Production v2 runtime stop — 2026-09-27

The frozen campaign stopped with `runtime_budget`, not a scientific stopping criterion. Terminal receipt: completed/executed 15,565 of 19,968; incomplete. Original production PID 320540 and closeout watcher PID 321932 are absent. Watcher correctly rejected incomplete production; no production audit or scientific summary is claimed.

Manifest hash: 0dcf6190c27f5fc9c50b07a270826932691f8c21886ff4b148c6fe299bf3135e.

Receipt-only inspection (no biological outcome arrays opened): completed-case elapsed seconds sum 34151.52799999458; interrupted case grid_evolving_fine-production-h72103-d29 recorded 9462.485000000335 seconds. Largest completed case elapsed time was 2059.609 seconds, next largest 18.187 seconds. These times include host delays; they are not CPU costs.

Windows System / Microsoft-Windows-Kernel-Power events show Modern Standby entry at 2026-09-27 02:11:19 JST (506), exit at 05:41:07 JST (507). Earlier entry at 01:36:59 and transition events at 01:37:02 also occurred. This establishes host standby during execution; it does not establish an exact amount of recoverable CPU budget. The runner uses time.monotonic elapsed time, not process CPU time, with a 43,200-second limit. Original limit, terminal STOP, case receipts, interruption, and source archive must remain immutable.

Next action: prepare an explicit outcome-blind computational-budget amendment and validated continuation mechanism. Preserve all scientific cells, seeds, horizons, operators, numerical/precision thresholds, and original receipts. Do not silently edit the old manifest or relabel old receipts. Resume only missing cases after identity validation; do not count interrupted computation as a completed case. Full-case audit and 80 replays remain required. The goal remains active and incomplete.

Compute amendment implemented: data/design/model3_island_v2_compute_extension.json fixes one additional 43,200-second attempt for exactly 4,403 missing cases. All scientific parameters and frozen source hashes remain unchanged. The independent runner scripts/model3_island_continue.py verifies existing input/receipt/array identities before executing missing cases, preserves original STOP/interruption records under continuations/compute-extension-20260927-v1, and tags new receipts with the amendment. Six tests pass, including end-to-end preservation and missing-only execution. This is an explicitly amended campaign, not completion within the original budget.
