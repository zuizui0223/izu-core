# Pollen limitation, inbreeding depression and the next robustness gate

User request: explicitly include pollen limitation and inbreeding depression, and recheck whether directional evolution is justified by the settings. This extends the independent island-ecology question; Q1 remains inspiration only.

## Existing versus new capability

The frozen individual campaign already has outcross fertilization O*(1-exp(-P/scale)), delayed autonomous selfing of remaining ovules, and a fixed0.5 loss of selfed offspring. It does not vary depression, evolve selfing, model recessive genetic load, or demonstrate purging. Its current outcomes cannot establish robustness to those choices.

New `scripts/model3_pollen_limitation.py` explicitly reports resource-matched counterfactuals before density regulation:

- Ideal supplemented outcross offspring Ysupp=sum(O), with baseline outcross viability1.
- Outcross shortfall before selfing: Lout=1-Yout/Ysupp.
- Raw selfed offspring, viable selfed offspring, and their difference (inbreeding loss).
- Total viable-seed shortfall: Lviable=1-(Yout+Yself_viable)/Ysupp.

For constant selfing a and depression delta, Lviable=Lout*[1-a*(1-delta)]. These are model indices. The second combines insufficient outcross fertilization with assurance and offspring loss; do not mislabel it a pure measure of pollen receipt. Zero ovules gives undefined indices, not zero limitation. Ideal supplementation is not an implemented field-treatment model; resource redistribution, supplementation costs and offspring density dependence are held out of this ceiling.

At zero visitors, annual viable offspring per parent equal8*exp(-.5*b^2)*a*(1-delta). With b=.5 and a=.5, the replacement boundary is delta=1-1/[4*exp(-.125)] approximately0.7167. The baseline delta=.5 is above replacement; delta=.9 is below. For a=.1, even delta=0 is below replacement at that investment. These are consequences of the declared budgets, not simulated findings or calibrated demographic thresholds. Stochastic survival is not equivalent to the sign of the expected growth rate.

## Implementation verification

Five counterfactual tests check complete visitor absence, complete depression, no-selfing invariance to depression, resource-matched increasing pollen, and zero-ovule undefinedness.

`scripts/model3_meanfield.py` supplies a separate finite-allele Mendelian distribution update and a variable depression parameter. Seven tests verify inheritance probabilities and moments, zero-pollen extinction, delayed assurance, activity invariance to duplicated visitor types, complete depression, and approach of a finite individual transfer calculation to the density limit. Independent review found no mathematical blocker. These are operator checks, not a completed long-term PDE comparison or a completed robustness campaign.

Comparator admission: initialize genotype frequencies from declared ordered-allele probabilities, then collapse to unordered diploid states. Uniform mass on unordered states is NOT uniform independent allele draws. Declare finite-grid approximation and check resolution; initial-density and discretization differences must not be interpreted as demographic stochasticity. The current primary campaign uses continuous sampled founder alleles and is not automatically identical to the finite-grid comparator.

## Required next execution gate

Preserve the running baseline and all its outcomes. Before new full-trajectory outcomes, freeze a separate parameterized campaign crossing weak/strong assurance with depression below/above the replacement boundary, and distinct pollen availability. Include the no-selfing control (depression then must be irrelevant), report ideal supplementation deficit, expected viable offspring, actual recruitment and extinction separately. Reproduction parameters must feed the inherited offspring ledger, not merely a plotted after-the-fact penalty.

The independent settings audit also requires separating survival from annual effort and checking accessible trait support/source geometry and fitness cost. A source-level one-step fitness-surface screen can map these before a bounded trajectory experiment. Freeze the screen grid and escalation rules prospectively; a desired sign must never choose the settings.

No claim of fully sufficient evolutionary settings, biological genetic-load evolution, empirical island calibration, or final model completion is licensed by these additions. Audit: `MODEL3_EVOLUTION_SCIENTIFIC_RECHECK_20260925.md`.
