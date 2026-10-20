# Secondary colonisation after island adaptation — exploratory Model3 pilot

Status: frozen design for a bounded exploratory experiment, NOT a
confirmatory study, field observation, or natural reverse-migration claim.
Date: 2026-10-20. This experiment is an extension of IZU-CORE reproductive
assurance and genetic accessibility, not a new independent natural-island result.

## Central question

Does a plant population's history of pollination limitation, through evolved
reproductive assurance and inherited floral/genetic states, modify its chance
to arrive, leave descendants, and respond evolutionarily in a different
environment? Secondary island-to-mainland dispersal is a motivating hypothesis;
the actual treatment labels are artificial environmental analogues.

The primary endpoint is secondary colonisation and inherited trait-locus
lineage survival, NOT pollinator restoration or recovery of ancestral I.

## Frozen source cohorts

Use unchanged native finite Model3: scripts/model3_island/types.py,
reproduction.py, population.py, randomness.py and history.py.
Its three selected loci are M (matching), I (investment) and A (assurance).
Fixed A expression at 0.5 still permits selfing.

Founder RNG seeds: 202610201, 202610202.
Visitor RNG seeds: 202610211, 202610212.
Cross the two founder seeds with the two visitor seeds: four
independent crossed-source blocks, NOT 16 independent islands.
Draw 48 original diploids with standing M, I and A variation.
Six visitor types are present through year 5 and one through year 25.
The five donor states per source block are:

| Source | Historical census | Expressed assurance during history |
|---|---:|---|
| Ancestral | 0 | no historical evolution |
| Island fixed A | 10 | 0.5 |
| Island evolving A | 10 | inherited genotype-dependent |
| Island fixed A | 25 | 0.5 |
| Island evolving A | 25 | inherited genotype-dependent |

The paired historical policies share founder and visitor backgrounds but
their stochastic reproductive draws need not be eventwise coupled.

Historical and destination parameters: K=48, ovule budget B=8,
survival=0, investment cost=0.5, assurance cost=0.5,
inbreeding depression=0.5, delayed selfing, mutation rate=0,
no seed immigration and no new visitor arrivals.

## Common-source seed production, arrival, and destination

Each donor produces native sexually generated offspring under the SAME
six-visitor source pollen environment. Cap its sampled viable seed production
at 8 diploids. This is a controlled genetic-history comparison and NOT a
simulation of source-habitat-specific propagule production. Extinct and
seedless donors remain in the all-start denominator.

For every produced seed, arrival plus establishment is sampled with

    p = 0.8 * exp(-d)

where dimensionless distance d is either 0 or 1.5, held identical across
source histories. This is an imposed reach opportunity, NOT measured
island-to-mainland distance.

Three destinations are each crossed with both distances:

1. island_like_vacant: one functional visitor, no resident plants.
2. mainland_like_vacant: six visitors, no resident plants.
3. mainland_like_resident: same six visitors, 40 pre-established synthetic
   reference genotypes and up to 8 available settlement slots.

In every destination, expressed A becomes genotype-dependent (evolving) and
the descendants carry unmodified inherited A alleles. Future simulations
have 20 annual reproductive updates, two seeded repeats per
source/destination/distance, no immigration, no mutation and no further
visitor turnover.

Total maximum allocation: 2 founder x 2 visitor x 5 sources x 3 sites x
2 distances x 2 future repeats = 240 futures, with 4,800 future updates.
All future streams are nested within the four crossed-source histories;
no independent-population inference is made from N=240.

## Measurements and claim boundaries

Report complete denominators including historical extinction, donor seed
production, settled seed number, subsequent habitat total occupancy and
the persistence of source-locus ancestry. In a vacant destination,
source-allele persistence indicates descendants remain. In an already
occupied mainland-like destination, it can instead mean introgression into
resident genotypes: it does NOT prove a self-sustaining separate migrant
population. An occupied recipient can coexist with total disappearance of
migrant alleles.

The tracked source IDs refer to three SELECTED loci, not neutral markers
or full-genome ancestry. Record their count at each census, source-I
polymorphism, first absence of their support, and mean I and A for
ancestry-bearing individuals. Original high-I support is a necessary
bound under no mutation/immigration, not proof of phenotype restoration.

Also assay the source-allele carriers at entry and last census against
47 fixed reference competitors, using the existing common-context
genetic-return assay. Its change is descriptive and conditioned on the
remaining carriers. It is not a standalone causal estimate of adaptation,
especially after introgression in the resident destination.

Primary contrasts are historical source policy and elapsed island history
at matched destination and arrival opportunity, with founder x visitor
blocks retained. No p-value, CI, biological SESOI, mediation fraction,
permanent irreversibility, or empirically calibrated colonisation
probability is claimed from this exploratory allocation.

A simple genetic-ratchet interpretation would be weakened if a cohort lacks
ancestral I alleles but attains equal or better destination performance,
or if the destination never favours higher I. If donor histories have
comparable settlement and ancestry survival, no demographic difference
has been demonstrated. If total mainland occupancy persists but source
alleles disappear, the recipient remains occupied without migrant lineage
persistence.

## Execution and provenance

Producer: scripts/secondary_colonization_pilot_20261020.py
Tests: tests/test_secondary_colonization_pilot_20261020.py
Pilot Actions: .github/workflows/secondary-colonization-pilot.yml

Command from repo root:

    python -m scripts.secondary_colonization_pilot_20261020 --exploratory-pilot --output results/secondary_colonization_exploratory.json

The output path must be new; the script refuses overwrite, includes the
source, protocol and native operator SHA256 values, and records every
allocated path and per-census ancestry readout. The Actions workflow
retains an output checksum. The 160x160 historical confirmation and
10,240 conditional transfer experiment remain distinct and unchanged.
