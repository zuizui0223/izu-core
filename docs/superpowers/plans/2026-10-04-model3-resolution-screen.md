# Resolution screening before additional full-grid computation

The user requests estimating necessary resolution before launching additional
full-grid campaigns. Therefore the prepared 17-node full run is pending and
must not launch automatically after 13 nodes. Keep the already active 13-node
run. This instruction supersedes an automatic 17-node next step.

Before examining this screen's outputs, fix candidate allele counts
9,13,17,25,33,49,65,97,129, with original mutation probability .01 and width .05.
Use only the one-dimensional mutation operators; never allocate the full
three-locus state space for this screen.

For each operator separately, compare numerical evolution of cosine modes
1 through 8 at 1,200,1000 birth events with its exact reflecting continuum
eigenvalues. Report modes 16 and 32 separately wherever resolvable, without
silently changing the primary eight-mode criterion. Exact eigenvalues are
1-u+u exp(-(m*pi*sigma)^2/2) for jump and exp(-u*(m*pi*sigma)^2/2)
for heat. Thus numerical error is not confused with jump-vs-heat biological
approximation discrepancy.

Screen candidates by maximum absolute eight-mode expectation error < .01
across starting nodes and the three horizons, and central one-birth variance
relative error < .01. These are proposed engineering diagnostics fixed before
this screen, not a theorem or substitute for the existing whole-model terminal
trait tolerance .01. Include boundary starting nodes in the mode check. The
central variance reference u*sigma^2 neglects only negligible boundary tails.
Mutation-only repeated births exclude selection, inheritance, mating and
ecological feedback. Neither pass nor fail alone decides full ecological
trajectory precision. The screening thresholds are not inherited ecological
acceptance criteria or new statistical tests.

Calculate full-grid state counts and a transparent memory lower bound from
genotype alleles, one gamete-pair float matrix, the child lookup and one state
vector. Real peak memory is larger (Python mappings, sparse matrices, visitors,
mutation copies and checkpoints). Use the screen to choose feasible numerical
work, not to assert that a specific count guarantees trajectory convergence.
Archive source hashes, all candidate outcomes and the analytical reference.
