# Post-outcome assurance-locus genomic contribution to selected-source persistence, age20 transplant

**2026-10-10. Completed synthetic mechanism diagnostic, NOT independent prospective confirmation.**

## Aim and source validity

The previous t20 whole-genome intervention used **only 50 original shared-survivor visitor-history sources** selected from an exposed 64-history Model3 cohort (selected prehistory alive 58/64, genotype-neutralized prehistory alive 52/64, BOTH alive 50/64). The t20 source mean genotype differed in all three traits; selected minus neutral mean was **matching −.013845, investment −.012492, assurance +.082666**. Under original selected future parentage and K8/N0=8/B48, selected source produced 36/50 surviving trajectories versus neutral source 15/50; future K48 produced 49/50 versus 41/50.

The new counterfactual tests **whether selection-history differences on the assurance locus can account for most of that source-genome contrast** without changing the original t20 history population eligibility, future Model3 implementation, or ecologies. This is explicitly a **post-outcome** mechanism probe: these original 64 visitor seeds were already exposed, not freshly generated for confirmation.

## Exact intervention

For every one of the original 50 both-surviving histories, the runner regenerates the **same already source-verified eight-whole-individual genotype draws** from both previously selected and previously genotype-neutral source t20 populations, with donor ancestry/allele-origin/mutation flags retained. Each individual receives one of four artificial diploid genotype compositions:

1. **Neutral all**: all three entire diploid loci from the neutralized t20 source draw.
2. **Selected assurance only**: both homologs, origins and flags of the assurance locus from selected t20 donors; entire matching/investment diploid loci retained from neutral source.
3. **Selected other two loci**: matching and investment whole loci from selected source; assurance locus retained from neutral source.
4. **Selected all**: all three complete diploid loci from selected donors.

Crosses of two source histories can create new **across-locus genomic associations and pedigrees** that never occurred naturally. This is an intervention on genomic origin, **not a direct physiological change of mean selfing, or a natural hybrid-crossing experiment**. It preserves entire two-copy genotypes within each locus and exact ancestry array provenance; no alleles are invented or randomly sampled locus by locus. All starts have N0=8, pollen background B48; future K8 and K48 are crossed and original source-selected parentage is used for 60 later updates under the identical exposed visitor history.

**All 400 outputs are required to reproduce the previous full-three-locus original outcome controls bit-for-bit at the aggregated occupancy level:** K8 neutral all 15/50 and selected all 36/50, K48 neutral all 41/50 and selected all 49/50. The runner fails if these controls disagree with the original verified experiment; both did pass.

## Execution/provenance

- Source runner `scripts/audit_chapter2_t20_assurance_locus_hybrid.py`, experiment contract `data/design/chapter2_t20_assurance_locus_hybrid_replay_20261010.json`; focused test `tests/test_chapter2_t20_assurance_locus_hybrid.py` and permanent compact-source regression `tests/test_chapter2_t20_assurance_hybrid_receipt.py`.
- Execution commit **`49dca0b2a810e03ecd04a4d09c15af8d18a791be`**, [CI #38018139649](https://github.com/zuizui0223/izu-core/actions/runs/38018139649), focused source tests and full 400-future execution/upload **PASS**. Raw [artifact #11656913704](https://github.com/zuizui0223/izu-core/actions/runs/38018139649/artifacts/11656913704). Original JSON SHA256 **`339d73f4522ee20bfb62b6796845e983a6169ca99c819975e388ca89a34d8106`**; ZIP SHA256 **`99f8eb22f9b562fe9f4dbf494b08f357732dedd92a576619ed5c080b0666896a`**; original design SHA256 **`91d8147d569840f9a32386a11ecfe1b3eb43236baf28888097d16e430bd60f53`**.
- Complete-source compact receipt `data/results/chapter2_t20_assurance_locus_hybrid_receipt_20261010.json` preserves all 8 cell counts, all 10 paired secondary source comparisons, zero new visitor histories, original cohort eligibility, two-order decomposition and interval limitations.
- No original source Model3 biology is edited. The visitor histories, original t20 genotype distributions, complete original whole-genome primary results and their fail/uncertainty boundaries remain separate and immutable.

## Actual survival results

All values show model populations occupied at update80 out of the SAME 50 eligible t20 source histories. Original inheritance operates for all future descendants.

| Genomic origin at t20 | Future K=8 | Future K=48 |
|---|---:|---:|
| **All neutral source loci** | **15/50** | **41/50** |
| **Only assurance locus selected-source** | **32/50** | **48/50** |
| **Only matching + investment loci selected-source** | **18/50** | **43/50** |
| **All selected source loci** | **36/50** | **49/50** |

At K8, among identical genomic-transplant source histories, adding the selected-history assurance locus to the **neutral matching/investment background** changes survival from 15 to 32 (+17/50 = **+34pp**). Adding selected matching/investment while assurance remains neutral changes 15→18 (+3/50 = +6pp). Under a selected matching/investment background, changing assurance from neutral to selected changes 18→36 (+18/50=+36pp). These two assurance contrasts are each nonzero under *unadjusted*, conservative single-contrast 95% CIs ([+5.53,+56.94]pp and [+7.29,+58.87]pp), BUT cannot be promoted independently because 10 overlapping contrasts were examined on the same outcome-selected source histories.

At K48, the analogous assurance-only counterfactual is **41→48** (+14pp) and other-two-loci-only is 41→43 (+4pp), with wide uncertainty overlapping zero.

## Balanced two-order decomposition (descriptive, not causal shares of real extinction)

Let `Y_00` denote neutral for assurance and other loci; `Y_10` selected assurance only, `Y_01` selected other loci only, and `Y_11` all selected. Define

```
A = 0.5*[(Y10-Y00) + (Y11-Y01)]
O = 0.5*[(Y01-Y00) + (Y11-Y10)]
I = Y11-Y10-Y01+Y00
```

Then **A+O=Y11−Y00**, and interaction I is **already allocated** in the two-order means; adding I to the sum again would double-count. These are factorial contrasts over artificial locus mosaics and within a source-survivor-selected cohort, not causal partitions of natural gene-based extinction risk.

| Recipient K | Assurance-locus two-order A | Other-two-locus two-order O | Whole genome source Y11-Y00 | Interaction I |
|---|---:|---:|---:|---:|
| **K8** | **+.35** | +.07 | +.42 | +.02 |
| **K48** | **+.13** | +.03 | +.16 | −.02 |

The location of the signal is mechanistically more informative than a statement that genomic drift matters: **in this finite source model under the stated fixed costs, delayed histories and viable-self stress, the selected-history assurance genotype is the larger correlate of later persistence**.

### Conservative multiple-comparison adjudication

The ten paired comparison intervals were originally computed as separate conservative 95% intervals, not a family-wide set. A second clearly **post-outcome** Bonferroni exact sensitivity allocates 5% error across **all ten comparisons and both positive-only/negative-only discordance events**. Among K8, assurance-only effect +34pp then has approximate family-wise95 [−4.04,+63.06]pp; assurance under a selected other-loci background +36pp has [−2.41,+64.91]pp. The full selected-versus-neutral 3-locus G contrast +42pp remains positive relative to zero, family-wise95 [+3.87,+69.04]pp, but **does not clear the predeclared +5pp meaningful-effect threshold**. At K48, assurance-only family-wise95 is roughly [−12.30,+36.53]pp. **Zero of the ten family-wide intervals has a lower limit above +5pp.** No inferential finding about the assurance locus alone is independently confirmed.

## Scientific conclusions and disallowed interpretations

**Supported as a synthetic counterfactual observation:** with identical donor eligibility, original source visitor history and later demographic processes, swapping a whole assurance locus from an earlier selected source can change later occupancy, with a larger **descriptive** response than swapping the other two loci, particularly under K8 regulation. All original full-G transfer controls reproduce exactly.

**Not identified:** a fixed fraction of extinction causally mediated by assurance, selection-gradient-to-persistence universal agreement, conditional vs unconditional from-time0 evolutionary benefit, or independent effects of allele mean versus heterozygosity/source ancestry. The mosaic is a novel combined genetic arrangement from two counterfactual source genealogies; it is not ordinary Mendelian crossing. One source genome draw per paired visitor history and 50/64 source survivor conditioning remain material uncertainty.

**Research decision:** The next test—if done—must be a distinct, pre-outcome-defined whole-locus randomized genomic-origin swap with **new unexposed model visitor future environments, multiple donor resampling repeats, and sham matched-source controls**, preferably with power evaluated before generating trajectories. The previous beta/seed/growth and this source t20 mosaic do NOT demonstrate the central evolutionary-suicide hypothesis. Preserve all no-effect and inconclusive comparisons alongside positive model-internal mechanism candidates. Keep #452 Draft; do not merge it with #411's independently supported floral-investment manuscript or #451's separate capacity companion.
