# Artifact delivery and remaining scientific qualifications

All 19,968 cases and 80 deterministic replays passed the production audit. The compact completion, original STOP, compute extension, exact source/runtime archive and case receipt index preserve execution provenance. The baseline hash list is now repository-local, so provenance generation does not require the execution workspace ledger.

The main comparison figure was visually reviewed in PNG (the same Matplotlib figure writes SVG/PDF), including labels, zero references, extinction annotation and source/uncertainty footer. Clipped life-history title and crowded S/C/I legend were corrected. Per-condition plots retain trajectories, occupancy bounds and individual-versus-density scatter; they are supplements, not independent tests. Figure files and tables are individually hashed in provenance.json. Raw NPZ arrays remain local; their hashes and deterministic reconstruction code are delivered, not a claim of remote raw-data deposition.

Rebuild from the repository root in the recorded runtime:

1. `python -m scripts.model3_island.audit --design data/design/model3_island_v2.json --results data/results/model3_island_v2 --output data/results/model3_island_v2_audit.json --mode production --replay-per-cell`
2. `python -m scripts.model3_island.summarize --design data/design/model3_island_v2.json --results data/results/model3_island_v2 --output data/results/model3_island_v2_summary --mode production`
3. `python scripts/plot_model3_island_ecology.py`
4. `python -m scripts.build_model3_island_provenance`

The full simulation can be generated from its design and exact source ZIP. Preserve recorded source bytes when raw source hashes are checked. Cross-platform bitwise equivalence is not asserted. The continuation amendment represents a historical execution event; do not reuse it as an unlimited budget reset.

Numerical convergence has not been established, and this is retained as a negative assessment. Four of 70 trajectory rows meet the narrow conditional-mean precision target; 64 do not and two are undefined. No outcome-selected seeds or retuning were added. Effective exposure k is not assigned without an admissible covariance estimate. These are explicit findings/claim boundaries, not passing scientific validation.

Completion of the computational study means implementing and executing the declared tests, preserving their negative/non-evaluable outcomes and reporting what they establish. It does not certify the model as field-calibrated, continuously converged or publication-ready for unrestricted evolutionary magnitudes. Novelty priority remains unproven. The final remote commit and CI still need verification before delivery closes.

The final coverage pass also added and visually inspected floral_return_assays.png (with SVG/PDF): all 16 fixed-state conditions, outcross and total contributions, shared axes and existing 95% intervals. Rebuild with python scripts/plot_model3_island_assays.py before provenance generation.
