# Model 3: independent scientific recheck of the settings

Date: 2026-09-25. Scope: independent island ecology; Q1 is inspiration only. This is a source-level review, not an outcome review. The running frozen campaign is preserved. No campaign outcome arrays were read, no frozen code was changed, and no new simulations were run. Numerical statements below are algebraic consequences of settings, not campaign results.

## Judgment

The model can answer a bounded question about inherited response from standing variation under a prescribed visitor process. It cannot yet establish that a direction is robust to defensible alternative settings. Mendelian inheritance establishes that changes can be evolutionary; it does not validate the ecological selection surface. No fatal arithmetic defect was identified in this review. Several interpretations would nevertheless be definition errors, and several ecological conclusions require a separately frozen robustness campaign.

Evidence inspected: `scripts/model3_evolution.py`, `scripts/model3_reproduction.py`, the implementation plan, natural-history timescale note, and fitness primary-source note. Source references are those files as inspected on this date; the original campaign hash remains authoritative.

## Priority findings

### 1. Founder support determines what evolution can reach

Access alleles begin in [.2,.4] or [.6,.8], investment alleles in [.4,.6]. With no mutation or immigration and an additive allelic mean, every descendant stays inside its realized founder allele range. The two access populations can never have a common mean: their separation is at least .2, and slightly greater for finite sampled founders. Apparent late stability may be fixation or a boundary, not an optimum. The plan already correctly restricts convergence to distance reduction; interpreting persistent separation as multiple ecological attractors would be a fatal definition error.

Investment can move by only about .1 in either direction. Its chosen cost, exp(-.5 b²), falls from .9231 to .8353 across the entire accessible interval, while the affinity multiplier .1+b rises from .5 to .7. This is an imposed cost-benefit comparison; its net selective sign still depends on pollen limitation and siring. A directional result from this one interval/cost is not evidence that the direction persists beyond it.

The uniform visitor pool also has finite boundaries. Mean Gaussian matching is proportional to erf((1-x)/.2)+erf(x/.2), maximal at .5. It is approximately .348483 at .3/.7 and .354347 at .5: a 1.68% central matching advantage exists before ecological filtering. This is not a proof of the fitness gradient, but rules out calling any central tendency wholly emergent from island turnover. The main review records the independent matching calculation.

### 2. Visitor absence and reproductive assurance are strong built-in regimes

The visitor count follows K(t+1)=Binomial(K(t),1-p)+Bernoulli(a). Its stationary zero-count probability is the convergent product over j>=0 of [1-a(1-p)^j]: about .001447 for a=.3,p=.05 and .503785 for a=.1,p=.15. These are properties of the exogenous stationary process, not finite-horizon campaign frequencies; founders produce an initial transient.

An annual plant population with selfing=0 goes extinct in its first visitor-free reproductive year, regardless of floral access. A perennial can survive a gap. At selfing=.5 and depression=.5, however, visitor-free annual expected viable offspring per adult are 2 exp(-.5 b²), or 1.671–1.846 within founder investment support. Thus the assurance arm has above-replacement expected recruitment even without visitors before density thinning and stochastic loss. It also mechanically favors lower investment in that limit. Selfing is fixed, not an evolving mating-system response.

This is a legitimate, deliberately favorable delayed-assurance scenario. It is insufficient to establish general island selection on attraction. Separate sensitivity to assurance strength, depression and a pollen-discounting/competing-selfing case is needed before that claim. Total ecosystem simulation is unnecessary.

### 3. Annual/perennial contrasts include a nonlinear effort change

Let c=1-survival. Both ovules and pollen budget scale by c. For a held-fixed population, visitor community and phenotype state, recipient pollen dose scales by c and outcross offspring are proportional to c[1-exp(-c P)], where P is the annual-baseline episode dose. At low dose this scales as c²; at saturation it scales as c. At survival=.75, low-dose annual outcross output is approximately 1/16 of the annual baseline. Multiplying by expected adult persistence 4 leaves approximately 1/4 of lifetime output, not equality. This is a limiting calculation, not a prediction for evolving populations with changing density.

Equal maximum lifetime ovule/pollen effort is correctly declared, but does not equalize lifetime realized reproduction or isolate demographic buffering. Comparing equal replacement-time checkpoints does not remove this difference. Any claim that longevity alone causes a result is invalid. A bounded follow-up should separately vary survival and annual effort, with the original joint treatment retained as its own scenario.

### 4. Neutral and survivor comparisons have specific meanings

`neutralize` preserves current-state selfed and outcross totals, then makes parental identity exchangeable within each class. It correctly removes differential reproductive contribution at that step. It does not preserve the selected trajectory's subsequent totals: the neutral population develops different traits, densities and pollen receipt. Its interpretation is an intervention removing parent-identity selection in an ecology-dependent demographic system, not a matched census drift process.

Paired-survivor trait comparisons condition on survival in both interventions. This is a valid descriptive estimand, but may exclude precisely the environments/founders in which selection changes persistence. A nonzero conditional contrast need not describe all founded populations; neutral surviving populations can also be filtered indirectly by trait-dependent population persistence. Report both marginal extinction frequencies, paired-survivor counts, and unconditional joint frequencies of survival with each directional category. Never impute an extinct population's trait. If mechanism attribution remains essential, a separate fixed-demography one-step comparison can distinguish reproductive selection from survival filtering.

### 5. Mating, density and resource assumptions deserve small targeted checks

All adults are compatible; transfer mixes individuals globally, diagonal deposition is lost, and autonomous self pollen is separately unlimited. There are no distances, flowering mismatches, incompatibility alleles, pollen carryover sequences or juvenile delays. These are scoped assumptions, not automatically fatal omissions. However, the mechanism can depend on them: decreasing plant density raises pollen loss to a background fixed at capacity, reducing compatible transfer and potentially creating demographic feedback. Increasing capacity from 48 to 192 also increases this background, so that sensitivity scales population and background together; it is not a test of the background-loss assumption.

[Sargent & Otto (2006), original full text](https://www.zoology.ubc.ca/~otto/Reprints/SargentOtto2006.pdf) explicitly treats conspecific abundance, visitor attraction and flower constancy, and shows why their choice can alter specialization predictions. Its functional-group treatment and fixed pollinator preferences also show that one-way pollinator ecology is a legitimate theoretical scope. It does not calibrate this model's all-to-all transfer or background value. This paper was reopened for this review; other source claims are bounded by the access statements in the existing fitness note.

### 6. Four hundred seasons test a stationary forcing model

The visitor process has a stationary distribution but starts away from it. Plant feedback, changing climate, succession and shifting mainland source pools are absent. The two within-year episodes have identical ecology. This is adequate for conditional local-response theory, not a historical island reconstruction or evidence that the direction survives environmental change. A single preregistered source-pool shift or bounded temporal autocorrelation perturbation would test transferability more directly than simply running longer. Missing feedback only becomes fatal when claiming coevolution, community assembly caused by floral evolution, or long-run ecosystem equilibrium.

## Bounded falsifiable next gate

Keep the current run, original endpoints and all unfavorable outcomes. Before viewing any new robustness outcomes, freeze a small separate experiment with explicit predictions and an unresolved category. Do not search parameter combinations until the desired direction appears.

1. **Reachability and geometry:** compare the original supports to overlapping supports with matched initial means; separately replace the uniform visitor pool by a declared symmetric central or bimodal pool. Ask whether a claimed direction reverses or disappears. Do not add mutation merely to guarantee convergence.
2. **Fitness surface:** evaluate one-step expected parent contribution over the accessible trait ranges at fixed resident states; vary the investment cost coefficient (for example .25,.5,1) and pollen saturation scale (for example .5,1,2). Treat this as a scenario grid, not empirical uncertainty. No-cost attraction is only a diagnostic endpoint. Relate any later population direction to these preregistered local predictions.
3. **Mechanism separation:** use a small survival-by-effort factorial, a richness-matched turnover comparison, and an alternative background-loss level. Separate visitor gaps from composition matching. Include one delayed-selfing sensitivity crossing replacement and one discounting treatment if assurance underlies the ecological claim.
4. **Estimands:** preserve conditional survivor effects alongside extinction and unconditional survival-plus-direction frequencies. Predeclare what degree of sign/qualitative disagreement counts as failure of robustness. Wide uncertainty or insufficient surviving pairs means unresolved, not support.

A manageable response-surface/one-step screen can precede a limited factorial of full trajectories. Select its grid and escalation rules before outcomes, preserving every screen result. Robustness does not mean all settings agree: reversals that follow the declared mechanisms delimit the claim. The defensible endpoint is a conditional regime map, not a universal island floral direction.
