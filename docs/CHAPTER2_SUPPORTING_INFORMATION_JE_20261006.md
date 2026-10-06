# Supporting Information — How island isolation generates floral change

This Supporting Information accompanies the Journal of Ecology submission
manuscript. It preserves the complete analytical scope around the confirmed
sequence-versus-necessity result without promoting exploratory or numerically
unresolved analyses into the main claim.

## S1. Model structure, reproductive accounting and ecological scope

Plants are finite diploid individuals with three inherited trait axes:
functional matching, pollinator-facing floral investment and autonomous
reproductive assurance. A phenotype is the within-locus allele mean. Visitor
functional types differ in matching optima, breadth and effectiveness. Visitor
communities undergo continuing establishment and disappearance; isolation acts
by reducing successful establishment, not by increasing the per-type
disappearance hazard.

For investment (z) and assurance capacity (a), the ovule budget follows the
implemented allocation function

[
O = O_0 exp(-c_z z^2 - c_a a^2).
]

Functional matching and investment alter pollen export and receipt. Outcross
reproduction contributes both maternal and paternal gametes. Under delayed
selfing, autonomous selfing can use ovules that remain after outcross
fertilization; under prior selfing, selfing occurs before the outcross
opportunity. Inbreeding depression reduces viable selfed offspring. Fixed
assurance means that assurance capacity cannot evolve; it does **not** remove
realized selfing.

The finite-population model samples reproduction, Mendelian inheritance,
mutation, recruitment and survival. A deterministic genotype-density
representation propagates the same declared reproductive and inheritance
structure without finite demographic sampling. The density representation is
not treated as the exact stochastic mean of the finite model.

The isolation coordinate, reproductive updates and trait values are synthetic
model coordinates. They are not kilometres, years, island area, literal flower
colour or a calibrated corolla dimension.

## S2. Confirmatory sequence and necessity design

The discovery cohort used 64 visitor histories and eight nested demographic
repeats. After those outcomes were known, an independent design was frozen
before confirmatory results were generated. The confirmation used 64 new visitor
histories and eight new demographic repeats; discovery history and demographic
seeds were not reused.

The temporal component crossed two reproductive settings, two mutation
probabilities, 64 visitor histories and eight nested demographic repeats.
The preregistered primary cell was delayed selfing, assurance cost 0.5 and
mutation probability 0.01. A temporal event required a founder-relative trait
change to exceed the declared threshold for 20 consecutive updates; events
within five updates were classified as near-simultaneous. The primary threshold
was 0.05, with 0.025 and 0.10 frozen as sensitivity analyses. Near-simultaneous,
investment-first and censored histories counted as not assurance-first for the
primary binary success proportion.

The primary confirmatory success rule required both:
1. assurance-first proportion > 0.50 across the 64 independent visitor histories;
2. lower bound of the 95% visitor-history bootstrap interval > 0.50.

The primary cell passed at all three declared thresholds:

| threshold | assurance first | near-simultaneous | proportion | 95% history-bootstrap |
|---:|---:|---:|---:|---:|
| 0.025 | 48/64 | 16/64 | 0.750 | 0.641–0.845 |
| 0.050 | 51/64 | 13/64 | 0.797 | 0.688–0.891 |
| 0.100 | 59/64 | 5/64 | 0.922 | 0.844–0.984 |

The sequence was not universal. Under prior selfing with positive mutation,
the primary 0.05 threshold yielded 30/64 assurance-first histories and a 95%
bootstrap interval of 0.344–0.594. Other setting-by-mutation cells are retained
in the complete confirmatory result and cannot rescue or overturn the
preregistered primary decision.

The separate necessity component fixed assurance capacity at 0.5 and used the
same new visitor-history design. In the primary delayed/costly positive-mutation
cell, all 64 histories were estimable and near/far occupancy was 1.0. At update
1,000:

- far investment change from founders = -0.306021
  [95% bootstrap -0.318054, -0.294111];
- far-minus-near investment difference = -0.435389
  [-0.453330, -0.417191].

These results establish that **assurance evolution** is not required for the
investment decline under the declared intervention. They do not establish that
selfing itself is absent, that the mediation fraction is zero, or that the
sequence generalizes across reproductive settings.

## S3. Selection conditions, replenishment gradient and reciprocal effects

Fixed-plant assays isolate reproductive return before plant evolution. In the
focal delayed/costly setting at visitor snapshot 400, the marginal reproductive
contribution of floral investment changes from +0.5793 under higher
replenishment to -0.7004 under lower replenishment. The outcross component falls
from +1.6523 to +0.0854, while the viable-selfed component partially offsets
rather than generates the decline. Visitor amount and composition change
together in this contrast.

Analytical rare-mutant conditions and 900 finite-difference checks verify the
local selection calculations. The 13-rate diagnostic, reciprocal-selection
atlas and broad reproductive-parameter grid are exploratory mechanism maps.
They show that attraction and assurance can alter one another's selection
gradients, but reciprocal effects are conditional rather than universal.

The 13-rate finite-population extension holds plant capacity at 48 while varying
only visitor replenishment over 13 values. It contains 13,312 cases, with
2,048 endpoint cases reused from the sustained-isolation experiment. Complete
event and endpoint readouts are retained. Because endpoint behaviour was already
known before the intermediate-rate design was frozen, this extension is treated
as exploratory and cannot substitute for the independent confirmation.

The original fixed-versus-evolving-assurance experiment also showed an
exploratory attenuation of the near-far investment contrast when assurance was
allowed to evolve. This effect is not part of the independently confirmed
headline and remains Supporting Information.

## S4. Finite realization, genetic accessibility and numerical limits

Finite-individual and deterministic genotype-density calculations are kept as
parallel representations. Their differences can reflect multiple processes
including finite demographic sampling, genetic state and pollen self-exclusion;
they are not attributed uniquely to genetic drift.

A same-phenotype genetic counterexample illustrates why phenotype alone does not
identify inherited response. Populations with the same mean phenotype can carry
different genotype distributions and therefore different next-generation
variances.

A restricted one-locus history-switch experiment uses different visitor
histories for 200 updates followed by 800 updates under a common environment.
Without mutation, variation can be lost and late trait change can cease. With
mutation, variants are replenished and further movement can continue while
history-dependent differences remain. This is supplementary evidence about
genetic accessibility, not a claim of irreversible alternative attractors.

The mutation operator is exact at allele birth as the declared reflected jump
process; a heat/diffusion operator is an approximation. Small mutation
probability alone does not guarantee diffusion accuracy. The full
positive-mutation grid comparison failed its declared refinement gate in 31 of
32 endpoint cases, and the later high-resolution long comparison was stopped
after verified update 7. The high-resolution branch is therefore **numerically
unresolved** and is not used as biological evidence.

## S5. Pollen limitation, reproductive assurance and viable output

Supplementation and fixed-trait assays retain pollen-deficit measures and
absolute viable reproductive output as separate quantities. In the delayed/far
fixed-trait comparison at assurance capacity 0.5, increasing investment from
0.25 to 0.75 reduced the fractional viable pollen deficit by 0.0104 but reduced
viable maternal offspring by 15.72 per 48 plants. The prior-selfing comparison
shows the same qualitative mismatch.

This result is not presented as the first demonstration that pollen limitation
can differ from fitness. It is used to show, within the same reproductive
accounting used for the evolutionary model, why a fractional pollen-deficit
metric and absolute viable output can point in different directions.

## S6. Natural-island confrontation and reproducibility

Natural island studies are used as a confrontation layer, not a calibration
layer. The source audit retains examples of shared upstream pollination changes,
downstream branching, buffering, adverse responses, founding chronology,
partner loss and reintroduction. No natural system in the current archive
closes the complete chain from measured starting plant state through visitor
transition to inherited longitudinal change on the same units. That inherited
longitudinal stage remains the principal empirical gap.

No named island or region is assigned to a synthetic model parameter cell.
Cross-sectional floral differences are not treated as observed evolutionary
trajectories, and the model is not used to reconstruct historical causation.

The complete confirmatory design and result are stored in:
- `data/design/chapter2_1005_confirmatory_replication_20261006.json`;
- `data/results/chapter2_1005_confirmatory_replication_20261006.json`.

History-level inputs for the primary estimands are stored in:
- `data/results/chapter2_1005_confirmatory_primary_sequence_history_20261006.csv`;
- `data/results/chapter2_1005_confirmatory_primary_fixed_assurance_history_20261006.csv`.

Artifact identities and SHA-256 hashes are stored in:
`data/results/chapter2_1005_confirmatory_artifact_manifest_20261006.json`.

The Journal of Ecology review package regenerates all three main figures from
committed evidence, extracts the package into a clean directory and redraws the
figures there. This verifies figure reproducibility from frozen summaries and
history-level inputs; it does not rerun the 4,096 confirmatory trajectories.

A DOI-ready raw confirmatory bundle has been prepared. Public DOI deposition is
still external and pending; no public DOI is claimed in the manuscript or this
Supporting Information.
