# Stage-A Izu comparative-taxon evidence map

## Purpose

This is the first practical step toward the `izu core` issue. It does **not**
claim that the Izu Islands already form a replicated natural experiment of
sequential Bombus loss, and it does not start a meta-analysis.

Its purpose is narrower: identify which plant lineages could eventually provide
independent mainland--Izu contrasts under the same field measurement framework.

## Four gates before a taxon is an independent comparative replicate

A candidate must have all of the following documented separately:

1. **Taxonomic scope:** an accepted scientific name and project-relevant
   circumscription;
2. **Mainland reference:** a traceable mainland population or valid comparison,
   not just a broad national range statement;
3. **Izu replication:** at least two verified Izu-island populations or another
   predeclared repeated island design;
4. **Shared channels:** feasible linked inner-corolla imaging, flower geometry,
   time-bounded observation effort, and visit-bout handling measures.

Only then can it enter a multi-lineage field pilot. A later hierarchical
synthesis additionally requires comparable effect sizes, site replication,
direct interaction evidence, and a design for lineage/phylogenetic and shared
island dependence.

## Current result

The current map intentionally returns only one ready mainland--Izu core:
`Campanula microdonta`. This does not mean it is the only suitable Izu plant; it
means it is the only one presently backed by the locked known-data scope and
existing field protocol.

`Lilium platyphyllum` is retained as an Izu-only auxiliary lead. It may support
within-archipelago comparisons but cannot be counted as a mainland--Izu
replicate. The other initial coastal-flora names are discovery leads only: no
claim of focal-island occurrence, independent replication, or pollination
function is made until their source records are audited.

## Run

```bash
python scripts/build_izu_comparative_taxon_screen.py \
  --screen data/izu_comparative_taxon_screen.csv \
  --output-dir izu_comparative_taxon_screen
```

The generated report shows why a taxon is stopped and what exact source or field
check would move it forward.

## Discovery protocol for a candidate taxon

For each proposed addition, do not begin with a model. First add primary or
source-traceable records for:

- accepted name and synonym handling;
- one mainland reference population;
- at least two independently verified Izu island populations;
- flower accessibility and phenology at those sites;
- any existing pollination/visitor literature;
- legal, conservation, and collection constraints.

Then change the row status only for the relevant gate. A field pilot is justified
only after the four-gate screen passes; a meta-analysis remains explicitly out
of scope until several independent lineages pass.
