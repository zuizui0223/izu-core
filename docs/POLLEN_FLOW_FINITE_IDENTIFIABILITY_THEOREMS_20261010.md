# Finite pollen-flow identifiability: a mathematical boundary, not an island empirical result

**2026-10-10 · PR #452 · mathematical statement, exact rational witness, deterministic tests.** This note takes priority over starting more artificial ecological sweeps or treating missing natural field data as measured zeros. It does **not** claim mathematical novelty without a formal literature comparison, or establish evolutionary suicide, island adaptation, empirical paternity, or a specific Model3 visitor trajectory.

## Variables and assumptions

For \(n\ge2\) tagged potential reproductive adults, let \(T_{ij}\) be the **nonnegative effective pollen transferred from father \(i\) to mother \(j\)**. The outcross transfer matrix has \(T_{ii}=0\); autonomous selfing is handled separately. Define recipient pollen receipt \(r_j=\sum_{i\neq j}T_{ij}\), total delivery \(D=\sum_j r_j\), and source delayed-selfing maternal outcross seed expectation

\[
F_j=O_j\left(1-\exp[-r_j/(2s)]\right),\qquad
S_j=a_j(1-\delta)(O_j-F_j).
\]

Here \(O_j>0\) is ovule budget after costs, \(a_j\in[0,1]\) autonomous assurance fraction, \(\delta\in[0,1]\) constant inbreeding depression and \(s>0\) pollen scale. (This is the algebra of the source Model3 delayed-selfing reproductive kernel *downstream of a given transfer ledger*; the original Model3 ecological rule also constrains which \(T\) matrices can arise.)

For \(r_j>0\), let outcross paternal viable-seed success be

\[
P_i=\sum_{j\ne i}\frac{T_{ij}}{r_j}F_j.
\]

Thus \(\sum_iP_i=\sum_j F_j\) and the source finite reproductive ledger is \(W_i=\tfrac12 F_i+\tfrac12P_i+S_i\); in particular \(\sum_i W_i=\sum_j(F_j+S_j)\).

### Result 1: identical **total** delivery does not identify group viable seed output

Suppose all mothers have the same \(O,a,\delta\), let \(A=a(1-\delta)\), and fix only \(D=\sum_j r_j\). Then

\[
nAO + (1-A)O\left(1-e^{-D/(2s)}\right)
\ \le\ \sum_j(F_j+S_j)\ \le\
nAO+(1-A)On\left(1-e^{-D/(2sn)}\right).
\]

The lower bound is attained if all delivery is concentrated on one recipient (a feasible nonnegative outcross ledger for \(n\ge2\)); the upper bound when each mother receives \(D/n\). The proof is the strict concavity of \(1-e^{-x/(2s)}\), Jensen's inequality and the fact that shifting receipt to a more unequal vector cannot increase the sum of a concave function. For \(D>0\) and \(1-A>0\), the interval has positive width. **Merely recording the sum of pollen grains reaching the study population cannot identify the total seed response.**

Note the distinction from the previous **cloned-parent, exact-source intervention**, where equal maternal receipt arises by symmetry. That special case is consistent with, and *does not imply*, the general assertion that equal \(D\) always fixes seeds.

### Result 2: even the full vector of maternal pollen receipts does not identify fathers once n≥3

Fix every \(r_j>0\). Each column \(j\) is a simplex of \(n-1\) nonnegative donor entries summing to \(r_j\), hence has interior dimension \(n-2\). The set of all legal matrices has dimension

\[
\boxed{\dim \mathcal T(r) = n(n-2),\quad n\ge2.}
\]

For \(n=2\), donor identity is identified automatically because each mother has only one potential outcross father; \(T_{12}=r_2\), \(T_{21}=r_1\). For \(n=3\), **three free continuous transport coordinates** already remain despite *perfectly observed pollen arrival to every mother*. Moreover, if each \(F_j\) is known and no genotype/parentage constraints further narrow the donor set, the **sharp donor-specific expected paternal bounds** are, for \(n\ge3\),

\[
0\ \le P_i\ \le\ \sum_{j\ne i}F_j.
\]

Both endpoints are attainable on the boundary: another donor can cover every non-self recipient when \(n\ge3\), or focal father \(i\) can supply all outcross offspring of each mother \(j\ne i\). The marginal bounds are not jointly attainable by every donor at once, and the original Model3 visitor-affinity kernel may narrow them further.

### Result 3: explicit exact counterexample at three adults

Rows are fathers and columns are mothers. Both matrices have all diagonal entries zero, each recipient receives exactly one unit, and **total delivered pollen is exactly three in both**:

\[
T_A=\begin{pmatrix}
0&1/2&1/2\\1/2&0&1/2\\1/2&1/2&0
\end{pmatrix},\qquad
T_B=\begin{pmatrix}
0&9/10&9/10\\1/10&0&1/10\\9/10&1/10&0
\end{pmatrix}.
\]

The column sums are \((1,1,1)\) in both cases, so every mother's \(F_j,S_j\), the entire group viable seed production, and total outcross mating success are **exactly the same**. Yet paternal donor pollen transfer row sums change from \((1,1,1)\) to \((9/5,1/5,1)\); with equal mothers, paternal shares change from \((1/3,1/3,1/3)\) to \((3/5,1/15,1/3)\), **L1 distance \(8/15\)**. Consequently the individual \(W_i\) can differ despite the same population output.

This is a **mathematically valid nonnegative outcross source-ledger counterexample**, **not** an assertion that both matrices are reachable at the exact same genotype/visitor settings in Model3's fixed pollen-transfer formula. Reachability is a *separate, stronger* mechanical question; the source Model3 36-fixture numerical F/P/S study provides evidence of narrower, concrete heterogeneity within its own operator.

### Result 4: a reproductive state alone does not identify an investment-response gradient

Consider two possible local transport response functions \(T_{\pm}(x)=T_A\pm x(T_B-T_A)\), for \(-1\le x\le1\), around \(x=0\). Both are nonnegative and column-preserving at every x; at \(x=0\), they have exactly the **same** transfer matrix, total seed, female success, paternal share and \(W\).

However donor one's male success changes in opposite directions. For identical mothers \(F_1=f\), \(S_1=s_0\), and \(W_1=f+s_0\) at \(x=0\),

\[
\left.\frac{\partial \log W_1}{\partial x}\right|_{0}
=\pm \frac{(2/5)f}{f+s_0}.
\]

Thus a single snapshot of seed success, pollen delivery and even paternity cannot distinguish opposite local genotype/trait-payoff gradients **without specifying how the trait changes transport**. This is a formal *model-class* identification limit. The hypothetical \(x\) is **not shown to be Model3's actual floral-investment locus**; do not label this expression as an observed evolutionary β. In Model3, β must instead be calculated from its explicitly frozen genotype-dependent reproductive operator (already done in the preceding source audit).

## Numerical and symbolic reproducibility

The **transfer entries and conservation identities are exact rational arithmetic** using Python standard library \`fractions.Fraction\`. Only Model3's exponential ovule-to-outcross conversion uses floating point. Code: \`scripts/prove_pollen_flow_identifiability.py\`; tests: \`tests/test_pollen_flow_identifiability_theorems.py\`.

~~~bash
python -m scripts.prove_pollen_flow_identifiability --out /tmp/pollen_identification_certificate.json
pytest -q tests/test_pollen_flow_identifiability_theorems.py
~~~

The mathematical certificate reports both transfer matrices, exact row and column sums, donor shares, source-shaped \(F/P/S/W\) expectations, dimensional thresholds, sharp paternal bounds, the concavity/total-receipt seed interval and the two opposing *hypothetical* local response derivatives.

## Decision for the project

- A stronger scientific question is **which observation level removes which nonidentifiability**, rather than whether moving pollen makes seed production change.
- \`total delivered pollen\` cannot resolve recipient saturation; \`receipt by mother\` resolves maternal seed output under the source reproductive formula but leaves father identity unidentified for \(n\ge3\).
- **Genetic parentage evidence** or a well-supported mechanistic donor-transfer operator is necessary to narrow paternal shares. To infer heritable selection, an additional trait-to-transport response law and time-indexed genotype outcomes are required.
- These mathematical results are conditional statements with sharp assumptions and a concrete proof. They are not an empirical result, nor by themselves proof of novelty against existing pollen-flow or parentage identifiability literature.

**Scope firewall:** The legacy prospective Izu parentage extension has been staged separately, but the present task prioritizes this math certificate and its source tests. No sites are admitted, no field data synthesized, and no journal-level claims about natural selection or evolutionary suicide are authorized by this proof.
