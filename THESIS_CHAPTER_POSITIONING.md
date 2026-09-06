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

## World confrontation closes breadth before the Izu depth axis

Chapter 2 now distinguishes breadth from depth explicitly. The original 25-entry identifiability audit remains frozen, while later geography-first review used an independent island master and an outcome-independent stopping rule. The large-island expansion stopped only after two consecutive preselected tranches added no new response, process or falsification state, and a separate small-island supplement was then completed. The world programme therefore reaches Izu **after** breadth has stopped materially changing the mechanism vocabulary, not because the analysis simply began in Japan.

The world result is also specific about what is missing. New systems repeatedly add present-day visitor communities, breeding systems and plant outcomes, whereas direct historical partner loss/arrival linked to a matched plant state remains rare. Small islands improve access to chronology—Surtsey provides a dated founding sequence and Tiritiri Matangi a documented pollinator reintroduction—but even these do not close a matched source-state → transition → realized-community → plant-response contract.

That bottleneck determines the focal-system criterion. After breadth saturates, the depth system should maximize **measurement continuity across the missing chain**, not geographic convenience, representativeness or agreement with the simulation.

## Why Izu is the focal depth axis

Izu is selected as a **continuity system**, not as a convenient local case and not as a globally ranked positive example. The rationale is frozen in `data/design/chapter2_izu_focal_system_rationale_20260906.json`.

The same regional island series supports six unusually complementary layers:

1. **Historical focal-lineage response.** *Campanula microdonta* has source-locked island-series information on flower size, multilocus outcrossing and autonomous reproductive capacity. The channels are not identical: size/outcrossing show ordered erosion, whereas autonomous capacity shows a sharp Oshima-to-Toshima transition. Population-genetic history remains an explicit competing explanation rather than being erased.
2. **Repeated contemporary interaction structure.** The Hiraiwa–Ushimaru programme contains three mainland sites, one Oshima bridge-state site and four post-Oshima island sites, each sampled across repeated seasons.
3. **Numeric pollinator functional traits.** Source-native proboscis values are safely recovered for 202/209 current named pollinator taxa, allowing functional structure to be analysed without family/guild midpoint substitution.
4. **Present functional propagation.** Contemporary FDQ → corrected matching is leave-one-island sign robust, whereas matching → pollen is weaker and downstream plant responses branch. The system therefore contains both a strong upstream signal and internal counterexamples to a deterministic cascade.
5. **An independent within-lineage phenotype endpoint.** Chapter 3 (`zuizui0223/shimahotarubukuro`) already contains a direct five-island *C. microdonta* phenotype dataset. Its current result is a large coordinated size/investment trajectory plus selected departures from common allometric scaling. That result belongs to Chapter 3 and is not imported as Chapter 2 validation; its value here is that the downstream phenotype is independently measurable in the same focal lineage.
6. **A prospective missing-link design.** Visitor effort, visitor identity/contact, single-visit pollen deposition, autonomous/outcross treatments and mature fruit/seed can be linked in the same tagged populations under an already specified field schema.

This combination makes Izu scientifically useful for **identifiability**, not merely accessible. It carries the argument from historical reproductive response through present community structure toward a directly measured phenotype while preserving alternative historical explanations and the possibility of negative results.

The last point matters for selection bias. Izu is retained even though the frozen signed-position predictor does not explain null-corrected matching and the Oshima-source sensitivity is unsupported. The focal system is therefore not chosen because every analysis agrees with the synthetic mechanism. It is chosen because conflicting layers can be resolved within one linked system.

## Relationship to Chapter 3

The Chapter 2 → Chapter 3 handoff is therefore not “theory followed by a convenient case study.” It is a change in inferential scale:

```text
Chapter 2
world breadth saturates
    -> conditional response geometry
    -> transition-measurement bottleneck
    -> Izu selected by measurement continuity
    -> contemporary functional structure resolved, history still open
        ↓
Chapter 3
same focal lineage, direct phenotype
    -> quantify what coordinated and residual divergence is actually realized
    -> add effectiveness/dependency only as new empirical measurements, not retroactive validation
```

The current Chapter 3 phenotype layer already establishes, in its own repository, pronounced five-island *C. microdonta* divergence with a strong coordinated size/investment component and selected residual departures in access, reproductive-interface and visual-investment channels. Chapter 2 does **not** use those values to tune or validate its model. Instead, Chapter 2 explains why such a multichannel phenotype should not be expected to follow one universal direction and specifies which interaction measurements are still needed to connect the phenotype to mechanism.

No Chapter 3 phenotype is used as Chapter 2 model validation, *Bombus*-causation proof, pollinator-selection proof or external-prediction success.

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

- Chapter 1 identified *Bombus* loss or another pollinator as the cause of the northern/tropical difference;
- the northern-midlatitude and tropical Chapter 1 vectors have been assigned to particular Chapter 2 parameter regimes;
- pollinator occurrence equals visitor effectiveness;
- floral form identifies effective-pollinator dependency;
- starting functional position alone determines a lineage response;
- one functional decline must yield one floral response direction;
- `41/96`, `16/48`, filtering transition rates or synthetic thresholds estimate natural prevalence;
- additive design-space coefficients are causal ecological effect sizes;
- the external systems validate one universal response mechanism;
- Izu is focal because it is geographically close, logistically easy or representative of all islands;
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
WHICH measurements prevent that mechanism from being identified in world data?
WHY is Izu the appropriate continuity system for the depth transition?
        ↓
Chapter 3
WHAT mixture of shared phenotypic coordination and residual divergence
is actually realized within the focal Izu lineage?
```

The Chapter 2 contribution is:

> **to define a conditional post-establishment response geometry, show that its response vocabulary and measurement bottleneck persist through geography-first world expansion to an outcome-independent saturation point, and then select Izu on measurement-continuity grounds to resolve the contemporary functional half of the chain while handing the directly measured focal phenotype and remaining transition-linked causal bridge to Chapter 3.**
