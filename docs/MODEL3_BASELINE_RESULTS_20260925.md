# Verified baseline: preliminary scientific results

The independent island-ecology baseline completed28,672cases in160artifacts.
All cases passed validation and160sampled cases (one per artifact) replayed
exactly. Design57c0e52f87cb1b7d6db003f8acd93a6b2ec2670e6c23d724083893101c5f5324.
The verification receipt and172,032checkpoint rows are in
`data/results/model3_evolution_20260925/verification.json` and
`data/results/model3_evolution_summary_20260925/`. Nested checkpoints are not
independent replicates. These results do not finish the broader model audit.

## Baseline island response at100 reproductive years

Primary capacity48; full-island condition combines community and activity
changes. Each cell has256independent seed blocks. Selfing0.5, depression0.5.
All selected and neutral populations in the following four cells survived.

|Adult survival|Initial access|Mean investment change|Selected-minus-neutral investment|Monte Carlo SE of contrast|
|---:|---:|---:|---:|---:|
|0|0.3|-0.021535|-0.022015|0.004449|
|0|0.7|-0.022924|-0.015641|0.004358|
|0.75|0.3|-0.018001|-0.015146|0.003320|
|0.75|0.7|-0.022638|-0.017701|0.003318|

These are inherited changes in the model's abstract investment trait, not
measured flower size, color or an empirical regional syndrome. They show a
conditional mean shift, not an identical response in every population. The
Monte Carlo errors are simulation precision, not uncertainty about nature or
a multiplicity-adjusted significance claim.

Access does not show uniform convergence. Among256pairs of low/high starts in
the selected annual island condition,111reduced their distance by more than0.02,
39changed within0.02, and106increased their distance by more than0.02. The mean
distance change was-0.005972. Corresponding perennial counts were94/72/90,
with mean distance change-0.001318. Disjoint founder supports prohibit a common
optimum; these are distance changes, not convergence to one floral phenotype.

## Persistence is a primary result, not missing trait data

Without selfing, all256replicates in each selected full-island cell (two starts
and two life histories) were extinct by100years. Neutral counterparts were
also extinct. Trait differences in these cells are undefined, not zero. The
community-only island intervention also had no survivors in these cells.

For annual obligate outcrossers, mainland selected survivors were117/256 and
155/256 at starts0.3/0.7; reducing activity alone gave50/256 and49/256. Thus
even the baseline mainland is not guaranteed persistence. Perennial baseline
allocation further reduces annual pollen and ovule effort together; its
contrast cannot be called a pure longevity effect.

## Interpretation and next checks

Under this frozen model, delayed selfing permits persistence during missing
visitor opportunities and changes the reproductive benefit of floral investment.
The archived settings audit already identified the built-in visitor-free
replacement advantage at selfing0.5/depression0.5, so persistence here is not
independent validation of those settings. The separately frozen assurance and
effort campaign tests whether stronger depression, weaker assurance or changed
allocation removes or reverses these outcomes. It is still running at the time
of this report. The matched individual/distribution comparison is also running.

Retain the uniform source-pool geometry, finite founder support, no mutation,
fixed depression and density-regulation qualifications. Q1 is inspiration only;
no four-region fit or actual island reconstruction is claimed. Full results,
all controls, temporal comparisons, capacity sensitivity and figures remain to
be synthesized after supplementary verification. Do not label the scientific
goal complete from this preliminary report.
