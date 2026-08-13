# Candidate lineage registry

`data/candidate_lineages.csv` is the pre-analysis evidence map for the Izu specialist-generalist test.

A row may enter quantitative negative-control analysis only when:

1. the specialist/generalist assignment is resolved from an explicit source;
2. the trait comparison has mainland and island values with uncertainty and sample size in the original source;
3. the row is evidence grade `A`;
4. `quantitative_ready=true` and `status=ready`;
5. a specialist and a generalist form a predeclared matched set.

Grades:

- `A`: mean/effect, uncertainty and sample size can be extracted from an original source;
- `B`: directional, binary or incompletely reported comparison;
- `C`: photo, description or other hypothesis-generating evidence;
- `U`: unresolved.

The analysis gate remains closed until at least four quantitative-ready lineages form at least two complete specialist-generalist matched sets. This is a minimal software gate, not a claim that four lineages provide publication-grade power.

Candidate names in the registry are leads, not accepted biological classifications. Rows labelled `uncertain` or lacking a source must not be silently promoted.

Run:

```bash
python scripts/audit_candidate_registry.py data/candidate_lineages.csv \
  --output results/candidate-registry-audit.json
```
