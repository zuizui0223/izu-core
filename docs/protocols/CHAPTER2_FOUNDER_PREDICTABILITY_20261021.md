# Existing-cohort founder predictability analysis, 2026-10-21

Post-outcome analysis specification, written before calculating the new scores. Earlier aggregate outcomes and repeated-history results are already known; this is not prospective confirmation. No simulation or selected trajectory replay.

Primary outcome: change in mean I from census 0 to 80, evolving assurance, B8 (all 25,600 cells survive). Fixed-assurance B8 is a mandatory companion; endpoint I is a scale/initial-value sensitivity, not a replacement outcome. Report both irrespective of signs. Evolving A and M changes are secondary descriptive comparisons; no latent fixed-A comparison.

Input: original stored-variation artifact 12174875191 from run 39226906489, whose 32 shards have receipts binding source archives, reader code and output bytes. Verify every receipt against tracked source hashes and the producer script. Require exactly one of each 160 x 160 coordinate, all B8 occupancy, consistent initial means across histories/policies, finite values. Retain compact matrices with hashes so analysis reruns without downloading raw trajectories.

For each matrix, leave each cell out. Predict from (a) intercept, (b) its founder's other 159 histories, (c) its history's other 159 founders, (d) additive founder and history effects fitted without that cell. For balanced additive least squares use PRESS with h=1/F+1/H-1/(FH). Report skill=1-SSE(model)/SSE(leave-cell-out intercept), negative values retained. This predicts an unobserved pairing of already sampled sources; it is not prediction from measured initial traits or transfer to new founders. It also is not a causal fraction of variance. No p-values or confirmatory intervals; the cell predictions share training data.

Also report exact descriptive row/column/residual sums of squares, closing to total. Residual is interaction plus stochastic realization and cannot be split. Founder-only skill is the primary headline candidate; joint skill and history-only skill are mandatory context. Zero total variation yields null skill. No selection of the most favourable policy, trait, time or statistic after readout.

Check formulas against direct refits on small matrices; cover constant matrices, pure row/column structure, interaction-only data, permutations and invalid shapes. Check input provenance failures. Keep registered G/S unchanged. State all new numbers as exploratory saved-data reanalysis.
