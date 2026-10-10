# Supplementary mathematical note — what pollen receipt can and cannot identify

**Status:** analytic model-class statements and exact finite counterexamples, added 2026-10-10. This is a bounded supporting note for \`CHAPTER2_MANUSCRIPT_ECOLOGY_LETTERS_20261006.md\`, **not a new prospectively confirmed result**. The full source-operator diagnostics and executable proof development remain separately archived in [PR #452](https://github.com/zuizui0223/izu-core/pull/452); this manuscript note does not import its evolutionary-suicide or natural-island claims.

## Definitions and assumptions

Consider a **closed set of \(n\ge2\) potentially mating plants**. Write \(T_{ij}\ge0\) for effective pollen transfer from pollen donor \(i\) to stigma recipient \(j\), with \(T_{ii}=0\), since selfing is accounted for separately. The \(n\times n\) matrix \(T\) therefore has a zero diagonal. Recipient \(j\)'s pollen receipt is \(r_j=\sum_{i\ne j}T_{ij}\), and the whole-population receipt is \(D=\sum_jr_j\).

Conditioning on a legal transfer matrix, the delayed-selfing portion of the original Model 3 reproductive ledger has expected maternal outcross seeds and viable autonomous-self seeds

\[
F_j=O_j(1-e^{-r_j/(2s)}),\qquad S_j=a_j(1-\delta)(O_j-F_j),
\]

where \(O_j>0\) is its post-allocation ovule budget, \(s>0\) is pollen scale, \(a_j\in[0,1]\) its delayed-assurance fraction, and \(\delta\in[0,1]\) inbreeding depression. The population's expected viable seeds are \(G=\sum_j(F_j+S_j)\).

For \(r_j>0\), the ledger credits donor \(i\) with expected paternal outcross seeds \(P_i=\sum_{j\ne i}(T_{ij}/r_j)F_j\); if \(r_j=0\), that recipient contributes zero. Therefore \(\sum_iP_i=\sum_j F_j\), and \(W_i=\tfrac12F_i+\tfrac12P_i+S_i\) satisfies \(\sum_iW_i=G\).

These formulas describe **Model 3 reproduction downstream of a supplied pollen-transfer matrix**, not a theorem that every nonnegative transfer matrix is reachable under its specified visitor-affinity, breadth, activity and export equations. The paternal credit is a **model accounting rule**, not an assertion that deposited pollen grains reveal real genetic fathers.

## Proposition S1 — total delivered pollen does not identify group viable seeds

Assume homogeneous mothers: \(O_j=O\), \(a_j=a\), and shared \(s,\delta\). Let \(q=a(1-\delta)\in[0,1]\). Because
\[
G=nqO+(1-q)O\sum_{j=1}^n(1-e^{-r_j/(2s)}),
\]
holding only \(D=\sum_jr_j\) fixed yields the **sharp bounds over all nonnegative receipt vectors**
\[
\boxed{nqO+(1-q)O(1-e^{-D/(2s)})\le G
\le nqO+(1-q)On(1-e^{-D/(2ns)})}.
\]

**Proof.** The function \(f(x)=1-e^{-x/(2s)}\) is increasing, strictly concave for \(x\ge0\), and satisfies \(f(0)=0\). Jensen's inequality gives \(\sum_j f(r_j)\le nf(D/n)\), attained by \(r_j=D/n\) for every mother. Moving mass from a smaller receipt to a larger receipt cannot increase a concave sum, so the minimum on the simplex is attained at a vertex \((D,0,\ldots,0)\), where \(\sum_jf(r_j)=f(D)\). Both receipt allocations are realizable by a nonnegative zero-diagonal transfer matrix when at least two candidate donors are present. Multiply by \((1-q)O\) and add \(nqO\). For \(D>0\) and \(q<1\), the bounds differ strictly. \(\square\)

**Consequence.** Equal *population-total* stigma pollen receipt does **not** generally force equal expected seed output. The separate source-model experiment where eight monomorphic maternal genotypes had equal seeds at equal total delivery is a more restrictive symmetric example, not this proposition's negation. Heterogeneous \(O_j,a_j\) introduce additional degrees of freedom.

## Proposition S2 — individual mothers' pollen receipts do not identify fathers for n≥3

Suppose the **entire vector** \((r_1,\ldots,r_n)\) is known, all \(r_j>0\), the candidate mating set is closed and complete, and self-pollen is excluded. Column \(j\) then contains \(n-1\) nonnegative eligible donor transfers whose sum is fixed, leaving \(n-2\) free coordinates in its relative interior. Since each mother's column may vary independently, the compatible transfer-matrix family has dimension

\[
\boxed{\dim\mathcal T(r)=n(n-2)}.
\]

For \(n=2\), the dimension is zero: each mother has exactly one other candidate father, so transfer is mathematically identified **under the stipulated closed two-plant, no-external-donor assumption**. For \(n=3\), there are three degrees of freedom; for \(n=8\), 48. If unobserved candidate fathers or successful pollen from outside the sampled set are admitted, even a two-*sampled*-plant design need not identify fathers.

If maternal outcross seed counts \(F_j\) are also known, then for each focal father \(i\) and \(n\ge3\), the **sharp marginal bounds over this unconstrained matrix class** are

\[
0\le P_i\le\sum_{j\ne i} F_j.
\]

The lower extreme assigns all nonself recipient pollen to other donors; the upper gives all viable outcross descendants of every \(j\ne i\) to father \(i\). These marginal extremes need not be simultaneously possible for all fathers, and the specific Model 3 pollen operator may shrink the feasible set.

**Proof.** A fixed-sum nonnegative \((n-1)\)-vector is an \((n-2)\)-dimensional simplex; multiply over \(n\) independent recipient columns. The maternal-to-paternal seed-credit formula is a convex combination of donor shares for each recipient, establishing the stated individual bounds, and boundary allocations attain them. \(\square\)

## Exact three-plant counterexample

Let rows be fathers and columns mothers:
\[
T_A=\begin{pmatrix}
0&1/2&1/2\\
1/2&0&1/2\\
1/2&1/2&0
\end{pmatrix},\qquad
T_B=\begin{pmatrix}
0&9/10&9/10\\
1/10&0&1/10\\
9/10&1/10&0
\end{pmatrix}.
\]

Both have **identical column sums** \((1,1,1)\), total delivered pollen 3, and zero diagonal, so in homogeneous delayed-selfing mothers they imply the exact same \(F_j,S_j\) and \(G\). Their donor row sums are, respectively, \((1,1,1)\) and \((9/5,1/5,1)\). Expected **paternal shares** therefore differ:
\[
\pi_A=(1/3,1/3,1/3),\quad
\pi_B=(3/5,1/15,1/3),\quad
\|\pi_B-\pi_A\|_1=8/15.
\]
The same maternal and group viable seeds thus coexist with unequal individual \(\tfrac12P_i\) components of genetic reproductive credit.

A separate local-identification argument follows by defining hypothetical, valid smooth families \(T_\pm(x)=T_A\pm x(T_B-T_A)\) in a neighbourhood of \(x=0\). At \(x=0\) they are observationally identical, and for every small \(x\) they preserve all maternal receipts; yet their paternal-return derivatives have **opposite signs**. Consequently, no single reproductive-state snapshot identifies a trait-response/selection gradient **without a specified trait-to-transfer response law**. This \(x\) is a hypothetical transfer coordinate, **not the actual inherited floral-investment locus in Model 3**; its derivative is not the paper's corrected rare-mutant invasion gradient.

## Relation to the model experiment, and inference boundary

The independent post-discovery Model 3 source-operator checks on [PR #452](https://github.com/zuizui0223/izu-core/pull/452) found (i) positive nonfocal viable-seed externalities in 128/128 visitor-present fixed synthetic states (with zero in 64 no-visitor states), (ii) conditional conflicts of **finite individual** versus collective *seed* gradients, and (iii) near-equal group viable seeds after **total recipient pollen delivery** was matched in 36 purposefully designed source states. The homogeneous subset's differences vanished to numerical precision and the mixed-diploid subset retained a mean absolute group-seed difference 0.000904; relative paternal shares could still vary in the mixed group. This is not an independent ecological history cohort and not a long-term population-persistence test.

The **mathematical model-class nonidentifiability** here and the **frozen Model 3 ecological operator** must remain distinct. In nature, single-visit stigma pollen deposition helps estimate functional transfer, but reproductive father identities require genetic parentage or another independently valid donor-tracing method; even that does not by itself reveal heritable selection or long-term persistence.

**Publication firewall:** None of the mathematical lemmas, fixed-state source diagnostics or founder/capacity pilots changes the prospective four-setting claim or its visitor-history-level uncertainty interval in the main paper. The exploratory model interventions are supplementary interpretation, not a fifth preregistered result. A causal claim that attraction-investment evolution depresses occupancy or produces evolutionary suicide is still **unresolved**.


## S3 — Direct versus investment-mediated reproductive-assurance spillover

**Mechanistic follow-up (not the #411 history-level estimand).** In original Model 3, pollen export by individual \(i\) has the source form

\[
e_i = B_p e^{-d a_i}\left[1-\exp(-q\,\overline{u}_i)\right],
\]

where \(a_i\) denotes reproductive assurance, \(d\ge0\) pollen-discount coefficient, \(q\) visitor activity and \(\overline{u}_i\) mean affinity determined by matching, visitors and floral investment \(I_i\). Pollen transfer from father \(i\) to any other mother is proportional to \(e_i\), after holding the visitor assemblage and all other parents constant.

**Proposition S3.** Holding investment, other genotypes, visitor community, background and activity constant, raising focal \(a_i\) does **not** change any other mother \(j\ne i\)'s pollen receipt or maternal outcross seeds \(F_j\) when \(d=0\). When \(d>0\) and some positive focal-to-nonfocal transfer exists, raising focal assurance decreases its exported pollen, reduces each affected other mother's receipt and therefore reduces her outcross fertilization under the source monotonically increasing receipt-to-seed function. This says nothing about the focal mother's own ovule budget or competition among *offspring after recruitment*.

**Proof.** At \(d=0\), \(e_i\) is invariant to \(a_i\), and the source donor–recipient affinity/channel weights depend on \(I_i\), matching and visitor traits, but not assurance. All \(T_{ij}\), \(r_j\) and \(F_j\) for \(j\ne i\) are unchanged. If \(d>0\), \(\partial e_i/\partial a_i=-d e_i<0\), so every affected \(r_j\) declines, and \(\partial F_j/\partial r_j\ge0\), strictly where receptive ovule availability and donor transfer are positive. \(\square\)

An imposed focal investment decrease can produce a **distinct mediated externality**, even when \(d=0\), because it changes affinity, pollen export, and other mothers' pollen receipt. For a controlled fixed resident state, the **ordered finite contrast** is exactly

\[
F_{-i}(a_{\mathrm{high}},I_{\mathrm{low}})-F_{-i}(a_{\mathrm{low}},I_{\mathrm{high}})
=
\underbrace{F_{-i}(a_{\mathrm{high}},I_{\mathrm{high}})-F_{-i}(a_{\mathrm{low}},I_{\mathrm{high}})}_{\text{direct assurance contrast}}
+
\underbrace{F_{-i}(a_{\mathrm{high}},I_{\mathrm{low}})-F_{-i}(a_{\mathrm{high}},I_{\mathrm{high}})}_{\text{imposed investment change}}.
\]

The decomposition is algebraic and **path-order-dependent** in an interacting nonlinear model, not a unique natural direct/indirect causal mediation fraction. The investment reduction is a *chosen counterfactual*, **not** evidence that assurance evolution itself produced that reduction in the original #411 trajectories.

A source-fixed eight-clone fixture (focal starting matching/investment/assurance 0.2/0.35/0.35; fixed four visitor functional optima; \(B=48\); 7 other mothers; assurance 0.25→0.45; focal investment 0.35→0.25) yields the following expected **other mothers' maternal outcross viable-seed changes** from the Model 3 reproduction formula:

| Source setting | Direct assurance change at fixed investment | Imposed investment change at high assurance |
|---|---:|---:|
| Delayed control, no pollen discount | 0 | −0.044772 |
| Prior selfing | 0 | −0.029101 |
| Pollen discount \(d=1\) | −0.030995 | −0.028660 |
| Direct assurance allocation cost | 0 | −0.042112 |

The frozen production-code evaluator is \`scripts/audit_chapter2_assurance_nonfocal_F_source.py\`, with structural checks in \`tests/test_chapter2_assurance_nonfocal_F_source.py\`. Source arithmetic tests must pass on the PR head before treating these fixture values as CI-verified results; no history-level intervention, evolutionary response or future persistence is tested.

**Consequences for the proposed private-insurance/public-advertisement narrative:** It is reasonable to call the direct assurance benefit mostly private under specified reproductive modes. But an unconditional “assurance cannot harm others” claim is false when pollen discount is present, and an assurance-evolution-induced *indirect* external cost requires a demonstrated assurance→investment causal pathway plus the same-state investment→nonfocal pollen-service contrast. The original main four-setting #411 results show assurance evolution changes mean investment, but their arm-mean summaries do not by themselves identify a unique effect on other mothers' outcross seeds in a common genotype/visitor state.

### Prior art and novelty boundary

Do not claim to be first to cast floral display as a public good or to discuss altruistic floral advertising. Relevant precedents include Torices et al. (2018, *Nature Communications*, DOI 10.1038/s41467-018-04378-3), Sun et al. (2021, *Journal of Theoretical Biology*, DOI 10.1016/j.jtbi.2020.110470), and Tachiki et al. (2025, *Journal of Evolutionary Biology*, DOI 10.1093/jeb/voaf015). Cheptou (2004, *Evolution*, DOI 10.1111/j.0014-3820.2004.tb01615.x) already coupled reproductive assurance, pollen-limited Allee effects and possible evolutionary suicide. These papers overlap materially with public/private and kin-context framing.

The possible contribution of our study is narrower: quantitatively **linking evolution of assurance capacity to the value and externalities of a shared effective-pollen-delivery channel within one explicit genetic and finite-demographic architecture**, while enforcing the evidence boundary between current viable-seed externalities and the unresolved long-term persistence effect. This is a proposed research contribution, not a validated novelty claim.
