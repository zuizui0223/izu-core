# Q3: a minimal pair of controlled distribution-policy contrasts

Status: construction feasibility verified; future effects unknown; no biological execution authorised by this document. This refines the candidate family in the pre-extraction protocol after the event-condition analysis. It does not amend that frozen readout or turn this exploratory design into confirmation of its already known results.

## Why these three policies

The original q=1 restoration has only {v-w,v+w} as its support. A partial restoration adds the interior v. Equal support *width* alone therefore does not imply an equal support *set*. To obtain one exact-support contrast and one matched-variance range contrast while preserving interior mass in every arm, use:

| Policy | Half-width w | Heterozygous fraction q | Heterozygotes at N=48 | Allele variance V=q*w^2 |
|---|---:|---:|---:|---:|
| A | 1/16 | 1/2 | 24 | 1/512 |
| B (shared reference) | 1/16 | 1/4 | 12 | 1/1024 |
| C | 1/8 | 1/16 | 3 | 1/1024 |

Each selected individual receives [v-w,v+w]; every other individual keeps [v,v]. Each individual has expressed I=v at intervention. M/A, IDs, birth years, origin labels and historical mutation flags remain unchanged. Artificial genotype edits must be logged as interventions, not relabelled as natural mutation or ancestry.

A versus B fixes the exact support set {v-1/16,v,v+1/16} and changes variance and the carrier configuration. C versus B fixes allele variance at 1/1024 and widens the support while changing allele frequencies, heterozygosity and the carrier configuration. Both are effects of specified genotype-distribution policies, not unique causal effects of abstract variance or support. Refixation, later expressed variance and selection are downstream outcomes of these assignments, not separately controlled components.

Three policies are minimal for these **two nondegenerate contrasts sharing a reference**: two distinct policies cannot simultaneously differ in variance at equal support and differ in support at equal variance. This is not a universal minimum for every possible improvement on the prior experiment. No interaction is estimated. A fourth cell w=1/8,q=1/8,V=1/512 (six carriers) would permit the corresponding policy interaction contrast, but that is an additional scientific question and cost. A fresh native reference is unnecessary for the two direct policy comparisons; historical PR #514 values remain context rather than a newly randomised control.

## Feasibility evidence and allocation boundary

`scripts/q3_distribution_triangle_20261014.py` constructed all three assignments at each of the 61 frozen trigger states, without annual updates or random draws. Every state has N=48 and v in {0.375,0.5,0.625}; all endpoints lie within the archived PlantState allele domain [0,1]. Construction checks exact variances, three-point support, individual expression and unchanged other fields. The receipt `data/results/q3_distribution_triangle_20261014.json` records 183 constructions, raw-source hashes, explicit witness indices and resulting allele-array hashes.

Those deterministic first-index subsets prove existence only. They are not the future allocation policy. A later execution contract should average over independently randomised carrier subsets as part of each policy, using a stream separate from biological dynamics and nested prefixes of one permutation for the 24/12/3 sets. Nesting supplies coupling; it does not remove carrier-allocation effects or their potential association with fixed M/A values. The contract must explicitly choose allocation-averaged versus allocation-conditional estimands; the proposed choice is allocation-averaged.

## Remaining execution gate

Before running any new future, freeze the common 61-state admission, original non-trigger policy-zero slots, both direct contrasts, exact event/terminal/survival estimands and their conditioning, allocation law and independent streams, endpoint family and multiplicity, operational margins and precision-based sample size, source/runtime hashes, raw genotype/parentage storage, independent replay/readback, resource ceilings, stopping and technical-failure handling. Present concrete cost and obtain execution approval. The old 7,808-path approval is exhausted and cannot cover these policies.

In particular, do not choose N to make confirmation exceed 0.01, select states after observing their future response, treat technical failures as scientific nulls, or interpret policy contrasts as natural-history explanations. Time and active variation-maintenance interventions remain separate questions if required after these comparisons. The raw reader's conditional geometry remains valid for the old width; it is not an outcome prediction for C.

Feasibility reproduction (fresh output filename required):

```text
python scripts/q3_distribution_triangle_20261014.py --archive work/Q3_CONDITIONAL_FUTURES_20261014.zip --preflight data/designs/restoration_futures_preflight_20261014.json --out work/q3-triangle-feasibility-fresh.json
```
