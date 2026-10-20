# Secondary colonisation: persistence versus realised reproductive return (2026-10-20)

**Evidence status: newly extracted descriptive readout of the *same* 240 archived exploratory trajectories, not an additional biological experiment, independent replication or confirmatory claim.**

## Source and independent arithmetic

- Repository PR: [#611](https://github.com/zuizui0223/izu-core/pull/611); source experiment workflow [39366132489](https://github.com/zuizui0223/izu-core/actions/runs/39366132489), source commit \`5861aea81c14ae9ab3f2d0da88b4a58cdfd7f7ef\`.
- Archived \`EXPLORATORY.json\` SHA-256: \`44664beef561ff30a0bddd0a9bd06950302b60c90477aa2ccb0698bb9542c223\`. The archived checksums for \`EXPLORATORY.json\` and \`READOUT.json\` were independently verified against the downloaded Actions artifact.
- New pure readback: \`scripts/summarize_secondary_colonization_fitness_20261020.py\`. It rejects any changed source bytes, duplicate/missing allocation, mismatched source-locus persistence or incorrect genetic-return subtraction. All 240 original futures pass, yielding 30 descriptive cells. The source and its original 4 × 5 historical donor cohort allocation are unchanged.
- No new random seeds, biological updates, confidence intervals, biological SESOI, or p-values are introduced.
- **Independent units:** four original crossed founder-by-visitor blocks (2 founder seeds × 2 visitor seeds). Each table row includes **eight *nested* future paths**, two per block. Neither 8 nor 240 is an independently replicated geographic system.

## Important newly extracted distinction

For a **distant mainland-like recipient with 40 pre-existing synthetic plants** (\`mainland_like_resident\`, dimensionless distance \`d=1.5\`), all five origin-history groups have six out of eight paths with at least one seed settled, but all eight recipient communities remain occupied because residents were already present.

| Source genetic history | Selected source-locus allele remains at census 20 | Changed common-context genetic return among lineages with entry and terminal assays |
|---|---:|---:|
| Ancestral, t0 | 2 / 8 | +1, −1 (2 paired) |
| Island history, A fixed, t10 | 2 / 8 | +1, −1 (2 paired) |
| Island history, A evolving, t10 | 4 / 8 | +3, −1 (4 paired) |
| Island history, A fixed, t25 | 2 / 8 | +2, −0 (2 paired) |
| Island history, A evolving, t25 | 4 / 8 | +1, −3 (4 paired) |

Here \`+\` / \`−\` are arithmetic signs of **terminal minus entry** reproductive genetic return, each assayed against 47 fixed reference genotypes in the same destination. A near-zero numerical tolerance of \`1e-12\` is used only to avoid classifying floating-point roundoff as a biological change; it is **not** a practical-effect threshold or proof of adaptation. The return metric is defined for **surviving source-locus carriers only**.

For the t25 pair, evolving-A ancestry survives more often (4/8 vs 2/8), but three of its four surviving futures show negative assay change. This is **not** evidence that assurance evolution inhibits adaptation: inherited M/I/A states all differ and the survivor-conditioned assays have changing genetic composition.

The persistence difference is concentrated in two of four crossed-source blocks: in founder × visitor order (0,0), (0,1), (1,0), (1,1), t25 fixed counts are \`[0,1,0,1]\` and t25 evolving counts are \`[1,2,0,1]\`, each out of two nested streams. **At d=0 in the same resident recipient, both t25 histories retain selected source alleles in 7/8 paths.** The proposed advantage is therefore not a demonstrated general or statistically resolved effect.

## What this resolves and what it does not

The original model already distinguished **recipient occupancy** from **selected M/I/A source-allele persistence**. This new readback additionally establishes that selected-locus persistence and a positive, *survivor-conditioned* genetic-return change are different outcomes in the archived futures. It does not independently test neutral ancestry, biological immigration from a real island to a mainland, or ecological genetic adaptation.

The accompanying read-only [pedigree audit](CHAPTER2_SECONDARY_COLONIZATION_PEDIGREE_AUDIT_20261020.md) can distinguish genealogical descendants from retained selected loci using original native parentage. Its **full original-archive replay result is not included here**, so no unverified pedigree count is promoted to evidence.

## Appropriate next experiment, without changing the archived pilot

1. **Freeze the denominator at original arrival opportunities.** Separate seeds produced at origin, dispersal/reach, first settlement, source-selected-locus persistence, genealogical contribution and local reproduction; resident-only occupancy is not colonisation.
2. **Hold migrant genomes and propagule number fixed** while altering expressed A and recipient visitor regime. This isolates immediate assay differences from inherited histories; then use predeclared genetic-module swaps (A vs I/M), recognising that the model has only three selected loci.
3. **Compare independent new source histories** at the level of crossed founder × visitor blocks. Treat the candidate advantage as exploratory until supported by an independently frozen allocation. Do not automatically count repeated futures from one source as independent population origins.
4. **Do not interpret return increases as adaptation by themselves.** Define a common destination-relative fitness endpoint including all initially allocated migrants (loss/extinction as competing outcomes), compared with the recipient reference genotype in that same ecological environment.

### Reproduction command

Use the **unmodified** downloaded \`EXPLORATORY.json\` from workflow run 39366132489:

\`\`\`bash
python -m scripts.summarize_secondary_colonization_fitness_20261020 \
  --original /path/to/EXPLORATORY.json \
  --out /new/path/SECONDARY_FITNESS_READOUT.json
\`\`\`

The script checks the archived SHA-256 before writing; it never overwrites an output file.
