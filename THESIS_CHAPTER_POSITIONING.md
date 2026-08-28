# Thesis positioning — Chapter 2

## Role in the dissertation

This repository is the **Chapter 2 / conditional-response mechanism** component of the dissertation.

The dissertation-level question is:

> **How does geographic isolation alter plant reproduction through changes in ecological interactions, why can those changes produce different outcomes across islands and lineages, and what phenotype structure is ultimately realized?**

The three empirical levels are intentionally separated:

- [`zuizui0223/island`](https://github.com/zuizui0223/island) — **Chapter 1:** asks **when and where** isolation-associated floral/reproductive filtering is detectable and where multivariate response vectors differ.
- `izu-core` — **Chapter 2:** asks **how** post-establishment interaction change propagates and supplies a model-conditional **proximal why** for divergent responses under a common broad perturbation.
- [`zuizui0223/shimahotarubukuro`](https://github.com/zuizui0223/shimahotarubukuro) — **Chapter 3:** asks how the focal Izu lineage's phenotype is structured: how much divergence follows a shared size/investment trajectory and what departures remain beyond common allometric scaling.

## Canonical Chapter 2 question

Chapter 2 is not a search for one universal island syndrome or one universal minimal mechanism.

Its central question is:

> **Why need not a common island-like reorganization of pollinator interactions produce one post-establishment plant response?**

The current answer is a **conditional response geometry**:

```text
partner loss / arrival balance
        ↓
possible response regime
        ×
plant starting functional state
        ×
realized pollinator community
        ↓
matching / effective-service consequence
        ↓
local availability / interaction filtering
        ↓
realized response branch
        ↓
autonomous assurance
        ↓
response magnitude, without sign rescue in the tested envelope
```

The crucial distinction is that starting functional position organizes the **mean response geometry**, while realized community state dominates much of the **cell-level variation**. Starting position is therefore not promoted as a universal generator acting independently of community realization.

## Chapter 1 handoff

The canonical Chapter 1 when/where result establishes that:

1. isolation-associated floral/reproductive filtering is confirmatorily detectable in **northern mid-latitude** island floras;
2. it is also confirmatorily detectable in **tropical** island floras;
3. both signals persist within **native non-endemic** assemblages;
4. the northern-midlatitude and tropical isolation-response vectors differ at the multivariate level;
5. northern high-latitude and southern-extratropical contexts remain data-limited at the confirmatory tier.

Chapter 1 therefore ends with a problem rather than a mechanism:

> **Why is isolation-associated filtering detectable in more than one biogeographic context while the resulting multivariate response vectors differ?**

Chapter 2 does not assign those particular regional vectors to synthetic model regimes. Instead, it demonstrates a mechanistic class in which a broad interaction perturbation need not map to one downstream response.

## Scope: the third layer of the island syndrome

The conceptual decomposition is:

1. **Colonization / assembly filtering** — which lineages arrive, establish and persist.
2. **In-situ evolutionary change** — how established island lineages change after colonization.
3. **Post-establishment interaction response** — how established lineages respond when pollinator functional composition and realized interactions change.

The active Chapter 2 simulation directly addresses the third layer.

A useful bookkeeping identity is

\[
W(z)=F(z)E(z),
\]

where `W(z)` is the observed island pattern, `F(z)` is local reproductive contribution under a focal interaction state, and `E(z)` is establishment / reachability conditional on viable reproduction. Chapter 1 primarily observes differences in `W`; Chapter 2 diagnoses post-establishment processes inside `F`. Assembly, colonization, regional species pools, persistence and evolutionary history inside or upstream of `E` remain outside the direct test.

## HOW, proximal WHY and ultimate WHY

- **HOW:** how partner turnover propagates through matching, service, local filtering and reproduction.
- **Proximal WHY:** why the same broad perturbation can yield different branches because regime, starting state and realized community differ and combine non-additively.
- **Ultimate WHY:** why the island acquired its biota, starting states or interaction architecture in the first place; this remains outside the Chapter 2 test.

| Level | Question | Current Chapter 2 answer | Claim ceiling |
|---|---|---|---|
| **HOW** | Through what response architecture does pollinator reorganization propagate? | Partner turnover changes functional matching and service; local availability / interaction filtering can change branch identity; autonomous assurance changes downstream magnitude without sign rescue in the declared envelope. | Directly represented within the declared synthetic model. |
| **Proximal WHY** | Why can the same broad perturbation yield opposite responses? | Response regime changes with partner loss/arrival balance and other matching dimensions; starting state organizes the mean sign geometry; realized community is the largest cell-level component; state and community combine non-additively; local filtering reallocates branches asymmetrically. | Diagnostic explanation within the frozen synthetic design, not a field-estimated causal effect. |
| **Ultimate WHY** | Why did an island acquire its biota, lineage starting states or interaction architecture? | Not tested. | Assembly, colonization, persistence and evolutionary history remain upstream explanations. |

## Frozen evidence supporting the story

### 1. Conditional response geometry

Across 96 matched pollinator-community realizations:

- 41 were mixed-sign across starting positions;
- 42 were all-positive;
- 13 were all-negative.

The mean response is approximately U-shaped, with sign transitions around `0.30–0.35` and `0.65–0.70` on the synthetic starting-position axis.

Across the fixed 48-point, 10-parameter joint design:

- 16 points had mixed mean geometry;
- 22 were all-positive;
- 10 were all-negative.

Mixed geometry is therefore nontrivial but not universal. The coexistence of mixed and one-direction regimes is part of the result, not a failure to obtain one preferred pattern.

### 2. Regime movement is associated most strongly with partner turnover balance

The fixed additive diagnostic explains `R² = 0.611` of variation in the negative fraction of the starting-position grid, with leave-one-point-out RMSE `0.329`.

The largest sign-stable full-range associations are:

- partner-loss multiplier: `+0.634`;
- partner-arrival multiplier: `−0.626`.

Within the declared design, stronger loss and weaker arrival accompany a larger negative portion of the response surface. These are design-space associations, not natural causal effect sizes.

### 3. Starting state is not the whole explanation

For the baseline `21 × 96` response matrix, total sum of squares partitions as:

- starting-position main effect: `2.18%`;
- community-realization main effect: `80.17%`;
- non-additive starting-position-by-community remainder: `17.64%`.

Observed sign differs from the fitted additive sign in `271/2016 = 13.44%` of cells.

Thus starting position organizes the mean U-shaped boundary, but the biologically relevant unit is a lineage **relative to the particular community that is realized**, not starting position or island status alone.

### 4. Local filtering allocates branches asymmetrically

Across the fixed local-filtering design, 737 lineage contrasts change sign at least once. Filtering is bidirectional, but positive baselines cross to non-positive more readily than negative baselines cross to non-negative at every non-zero declared strength.

For example, at filtering strength `0.40`:

- negative → non-negative: `42/268 = 15.67%`;
- positive → non-positive: `337/596 = 56.54%`.

The model therefore treats local filtering as a **bidirectional but directionally asymmetric branch allocator**, not as beneficial support.

### 5. Reproductive assurance attenuates magnitude rather than rescuing sign

Among 580 eligible baseline declines, assurance multipliers from `0.5×` through `4×` produce **zero sign rescues** while leaving upstream effective service unchanged. Magnitude improvement is widespread, but sign does not cross the non-negative boundary in the declared envelope.

The defensible interpretation is:

> **assurance is a downstream magnitude filter, not a second sign-changing branch in the current model.**

## Broad comparative universe and the role of Izu

Chapter 2 has examined a broader empirical universe than the 13 systems retained in the strict frozen manuscript challenge set. The canonical ledger is `docs/COMPARATIVE_ISLAND_SYSTEM_UNIVERSE_20260827.md`.

The roles are asymmetric:

```text
broad comparative universe
    -> response-state breadth, counterexamples, source gates and falsification
        -> 13 strict external challenges
            -> Izu as the focal mechanistic-resolution system
```

The external systems are **comparative grounding and boundary examples**, not validation coverage of a universal mechanism. Failed or blocked cases remain part of the scientific evidence trail.

Izu is used for depth because the same island series can connect historical reproductive evidence, contemporary interaction networks, pollinator functional traits, source-native signed-position analyses and prospective direct effectiveness/dependency measurements. This is a transparent programme rationale, not an outcome-independent global ranking. The raw-versus-null-corrected contrast localizes the current matching signal to source state plus background community composition rather than additional non-random sorting. Chapter 3 remains a downstream measurement handoff and is excluded from Chapter 2 selection and validation.

## Relationship to Chapter 3

The Chapter 2 → Chapter 3 handoff is therefore a measurement contract:

```text
Chapter 2
defines possible response geometry, confronts it with empirical diversity,
identifies the state-community-context-outcome measurement bottleneck,
and separates composition-level from beyond-composition matching in Izu
        ↓
Chapter 3
advances to higher-resolution focal phenotype, effectiveness and dependency
measurement in the same island series
```

No Chapter 3 phenotype is used as Chapter 2 model validation, Bombus-causation proof, pollinator-selection proof or external prediction success.

## Falsification logic

A convincing empirical mechanism should eventually show that:

- the proposed functional/dependency state changes at the relevant boundary;
- matched nondependent or alternative systems do not reproduce the same result merely because they share geography;
- climate, area, history and observation structure do not explain the pattern equally well;
- visitor identity is separated from effective pollen transfer;
- effective service is separated from reproductive dependency;
- occupancy or lineage replacement is not mislabeled as within-lineage adaptation;
- null and counterdirectional results remain null rather than triggering post-hoc mechanism rescue.

## Claim boundary

Chapter 2 must not imply that:

- Chapter 1 identified Bombus loss or another pollinator as the cause of the northern/tropical difference;
- the northern-midlatitude and tropical Chapter 1 vectors have been assigned to particular Chapter 2 parameter regimes;
- pollinator occurrence equals visitor effectiveness;
- floral form identifies effective-pollinator dependency;
- starting functional position alone determines a lineage response;
- one functional decline must yield one floral response direction;
- `41/96`, `16/48`, filtering transition rates or synthetic thresholds estimate natural prevalence;
- additive design-space coefficients are causal ecological effect sizes;
- the 13 strict systems validate one universal response mechanism;
- Chapter 3 phenotypic divergence identifies the historical mechanism; or
- the current model explains why regional biotas, starting states or interaction architectures formed.

## Dissertation sequence

```text
Chapter 1
WHEN / WHERE is island-associated filtering detectable?
WHERE do multivariate response vectors differ?
        ↓
Chapter 2
HOW can interaction reorganization propagate differently?
WHY can a common broad perturbation yield different response branches?
        ↓
Chapter 3
WHAT mixture of shared phenotypic coordination and residual divergence
is actually realized within one focal Izu lineage?
```

The Chapter 2 contribution is:

> **to define a conditional post-establishment response geometry, confront its response vocabulary with empirical island diversity, expose the joint-measurement bottleneck that prevents formal external identification, and use Izu resolution to separate source-state/community-composition structure from unsupported beyond-composition sorting—while leaving ultimate history and the remaining causal test unresolved.**
