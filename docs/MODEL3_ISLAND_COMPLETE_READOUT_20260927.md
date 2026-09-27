# Model 3: complete-production evidence readout

Status: preliminary scientific review, not final claims. All 19,968 cases passed state/receipt audit; 80 predeclared deterministic replays passed. Original runtime STOP and compute extension remain part of provenance.

Source summary SHA256: `c744a4890b90be7721d12e376afcc1902fe0600619b278b6cef95c0d24f52a4d`.

Rows: 86 (80 design cells plus six held-out rows). Trajectory precision flags: {'False': 64, 'None': 2, 'True': 4}. Failure of the narrow precision target is not equivalent to a confidence interval including zero; both must be reported.

## First findings requiring numerical-gate qualification

- Early versus late visitor absence produces different terminal investment despite the common final environment: early-gap change -0.1603; late-gap +0.0322; uninterrupted +0.2115. All 256 simulated populations survive in each arm. These are model-conditional, finite-horizon results.
- A 40-year visitor gap without assurance yields zero survivors; fixed or evolving assurance arms retain all populations. This scheduled absence tests reproductive assurance, not the empirical probability of island extinction.
- The density model and individual model can differ in direction following visitor absence. Such a difference is not identified as drift alone.
- Numerical refinement is not universally within tolerance: evolving-assurance coarse/fine individual change differs by about 0.0255, above the declared 0.01 tolerance. Fixed-assurance continuous 7/11-node comparison also needs careful paired and initialization review. Do not promote all magnitudes as converged.
- Initial founding and separation labels with matched states/histories give identical results, as intended. This is a control, not evidence that real oceanic and continental islands are equivalent.
- Shared S/C/I ordering can coexist with poor transported marginal predictions. Component shares remain noisy descriptive cell-mean decompositions with two demographic repeats.

## All condition means and uncertainty

| Cohort / cell | Occupancy | Investment change | 95% cluster CI | Density change | Precision target |
|---|---:|---:|---|---:|---|
| heldout / transport_d0_s3 | 1.000000 | 0.133592 | [0.1154580688476563, 0.15021830240885425] | 0.278655 | False |
| heldout / transport_d0_s5 | 1.000000 | 0.084298 | [0.06707153320312528, 0.10134358723958363] | 0.146787 | False |
| heldout / transport_d0_s7 | 1.000000 | -0.018960 | [-0.0376509602864582, -0.00010864257812489786] | -0.014145 | False |
| heldout / transport_d3_s3 | 1.000000 | -0.021252 | [-0.041768188476562516, -0.0007794189453125295] | -0.175849 | False |
| heldout / transport_d3_s5 | 1.000000 | -0.074935 | [-0.09356852213541651, -0.056361490885416476] | -0.322090 | False |
| heldout / transport_d3_s7 | 1.000000 | -0.134155 | [-0.15176513671874986, -0.1167480468749999] | -0.432325 | False |
| production / assurance_evolving_cost | 1.000000 | -0.187826 | [-0.21028645833333343, -0.16634114583333343] | 0.013259 | False |
| production / assurance_evolving_delayed | 1.000000 | -0.178060 | [-0.20052083333333343, -0.15559895833333343] | 0.013249 | False |
| production / assurance_evolving_discount | 1.000000 | -0.205780 | [-0.22732340494791675, -0.18374379475911468] | -0.151524 | False |
| production / assurance_evolving_prior | 1.000000 | -0.214264 | [-0.23567708333333343, -0.1927795410156251] | -0.252058 | False |
| production / assurance_fixed_disabled | 0.000000 | undefined | None | undefined | None |
| production / assurance_fixed_half | 1.000000 | -0.194661 | [-0.21321614583333343, -0.17610677083333343] | 0.189526 | False |
| production / assurance_fixed_high | 1.000000 | -0.227987 | [-0.24459431966145842, -0.21028645833333343] | -0.023897 | False |
| production / connectivity_p0_v0 | 1.000000 | 0.080270 | [0.06294745724976274, 0.09844343742053029] | 0.165946 | False |
| production / connectivity_p0_v1 | 1.000000 | -0.041859 | [-0.06187382358844358, -0.021763607094396956] | -0.096385 | False |
| production / connectivity_p0_v3 | 1.000000 | -0.131185 | [-0.14639676766878412, -0.11507333693374823] | -0.336942 | False |
| production / connectivity_p1_v0 | 1.000000 | 0.089960 | [0.07287422002044215, 0.10694928386298634] | 0.163634 | False |
| production / connectivity_p1_v1 | 1.000000 | -0.033991 | [-0.05244791531425733, -0.015910817628478017] | -0.103226 | False |
| production / connectivity_p1_v3 | 1.000000 | -0.110691 | [-0.12933913474797826, -0.09035102987692996] | -0.335910 | False |
| production / connectivity_p3_v0 | 1.000000 | 0.097123 | [0.07726124396762016, 0.11708465461630015] | 0.160880 | False |
| production / connectivity_p3_v1 | 1.000000 | -0.023006 | [-0.04259303215880339, -0.003038932606201758] | -0.103321 | False |
| production / connectivity_p3_v3 | 1.000000 | -0.075700 | [-0.09643162132769259, -0.055085661348252685] | -0.332569 | False |
| production / founding_empty | 0.996094 | undefined | None | undefined | None |
| production / founding_matched | 1.000000 | -0.033991 | [-0.05244791531425733, -0.015910817628478017] | -0.103226 | False |
| production / grid_11_continuous | 1.000000 | 0.217188 | [0.20397660187225, 0.22986735908062983] | 0.359499 | False |
| production / grid_11_grid | 1.000000 | 0.215287 | [0.20312133789062506, 0.22759236653645837] | 0.359499 | False |
| production / grid_5_continuous | 1.000000 | 0.240783 | [0.22950404964162593, 0.25206585547625543] | 0.336536 | False |
| production / grid_5_grid | 1.000000 | 0.246297 | [0.23409932454427074, 0.2578536987304687] | 0.336536 | False |
| production / grid_7_continuous | 1.000000 | 0.201308 | [0.1877566947610662, 0.21527221824342802] | 0.359591 | False |
| production / grid_7_grid | 1.000000 | 0.211890 | [0.19810567220052117, 0.22652282714843777] | 0.359591 | False |
| production / grid_evolving_coarse | 1.000000 | 0.191284 | [0.17846679687499992, 0.20484822591145824] | 0.252588 | False |
| production / grid_evolving_fine | 1.000000 | 0.165806 | [0.15048512776692743, 0.18152191162109405] | 0.256257 | False |
| production / life_annual_annual | 1.000000 | -0.243424 | [-0.2615885416666665, -0.22682291666666654] | 0.188032 | False |
| production / life_perennial10_annual | 1.000000 | 0.026392 | [0.010882263183593982, 0.04121246337890649] | 0.101411 | False |
| production / life_perennial10_lifetime | 1.000000 | -0.148255 | [-0.16473534127334327, -0.13186716424060876] | -0.193946 | False |
| production / life_perennial4_annual | 1.000000 | -0.072113 | [-0.08904713948567694, -0.055256856282551885] | 0.148250 | False |
| production / life_perennial4_lifetime | 1.000000 | -0.146899 | [-0.16478708902994776, -0.1295443725585936] | -0.102316 | False |
| production / order_early_gap | 1.000000 | -0.160278 | [-0.17868143717447904, -0.14275288899739572] | 0.163216 | False |
| production / order_early_mismatch | 1.000000 | 0.070087 | [0.05036753336588566, 0.09002400716145861] | 0.262019 | False |
| production / order_late_gap | 1.000000 | 0.032168 | [0.020800679524739893, 0.04375376383463577] | 0.148491 | False |
| production / order_late_mismatch | 1.000000 | 0.094248 | [0.07890991210937531, 0.10913299560546907] | 0.242491 | False |
| production / order_uninterrupted | 1.000000 | 0.211501 | [0.19757720947265656, 0.226143493652344] | 0.359591 | False |
| production / recovery_long_mu0p0 | 1.000000 | -0.257096 | [-0.2750748697916665, -0.23989908854166653] | 0.204019 | False |
| production / recovery_long_mu0p0001 | 1.000000 | -0.252206 | [-0.2694001542247895, -0.23567886209277678] | 0.413333 | False |
| production / recovery_long_mu0p0001_uninterrupted | 1.000000 | 0.209411 | [0.1951639297779764, 0.22502874685008614] | 0.417343 | False |
| production / recovery_long_mu0p0_uninterrupted | 1.000000 | 0.215560 | [0.2013020833333337, 0.23059895833333363] | 0.417319 | False |
| production / recovery_mutation_high | 1.000000 | -0.161204 | [-0.1791645381266944, -0.14383294976210434] | 0.163128 | False |
| production / recovery_mutation_high_uninterrupted | 1.000000 | 0.208049 | [0.19441968703105011, 0.22068031955904682] | 0.359598 | False |
| production / recovery_mutation_low | 1.000000 | -0.159703 | [-0.17780408952495064, -0.1418046938560792] | 0.163207 | False |
| production / recovery_mutation_low_uninterrupted | 1.000000 | 0.201308 | [0.1877566947610662, 0.21527221824342802] | 0.359591 | False |
| production / recovery_resident_immigrants | 1.000000 | -0.159713 | [-0.17827677408854153, -0.1420491536458332] | 0.163179 | False |
| production / recovery_resident_immigrants_uninterrupted | 1.000000 | 0.210699 | [0.19558308919270864, 0.22527486165364613] | 0.359577 | False |
| production / recovery_source_immigrants | 1.000000 | -0.091888 | [-0.11045736952149804, -0.07233492572561885] | 0.169386 | False |
| production / recovery_source_immigrants_uninterrupted | 1.000000 | 0.210799 | [0.19694252790907413, 0.2253569768459949] | 0.357931 | False |
| production / recovery_visitor_only | 1.000000 | -0.160278 | [-0.17868143717447904, -0.14275288899739572] | 0.163216 | False |
| production / recovery_visitor_only_uninterrupted | 1.000000 | 0.211501 | [0.19757720947265656, 0.226143493652344] | 0.359591 | False |
| production / scale_fixed_total_192 | 1.000000 | 0.285071 | [0.27563745691793706, 0.2939151745250777] | 0.359195 | True |
| production / scale_fixed_total_48 | 1.000000 | 0.206313 | [0.19220275594936637, 0.22116299286634883] | 0.358017 | False |
| production / scale_fixed_total_768 | 1.000000 | 0.328814 | [0.3208025285015983, 0.33636514565741205] | 0.359492 | True |
| production / scale_per_capita_192 | 1.000000 | 0.274476 | [0.2663096508973784, 0.28317549971560096] | 0.357919 | True |
| production / scale_per_capita_48 | 1.000000 | 0.206313 | [0.19220275594936637, 0.22116299286634883] | 0.358017 | False |
| production / scale_per_capita_768 | 1.000000 | 0.324403 | [0.3173303878802266, 0.3317490598464329] | 0.357898 | True |
| production / separation_inherited | 1.000000 | -0.033991 | [-0.05244791531425733, -0.015910817628478017] | -0.103226 | False |
| production / separation_matched | 1.000000 | -0.033991 | [-0.05244791531425733, -0.015910817628478017] | -0.103226 | False |
| production / transport_d0_s3 | 1.000000 | 0.150405 | [0.133950907389323, 0.16754699707031256] | 0.288827 | False |
| production / transport_d0_s5 | 1.000000 | 0.100777 | [0.0811836751302086, 0.12065928141276075] | 0.160656 | False |
| production / transport_d0_s7 | 1.000000 | -0.007145 | [-0.02655792236328111, 0.01250681559244802] | 0.001739 | False |
| production / transport_d3_s3 | 1.000000 | -0.005900 | [-0.026338500976562516, 0.015824178059895826] | -0.179260 | False |
| production / transport_d3_s5 | 1.000000 | -0.072375 | [-0.09330159505208316, -0.05095214843749981] | -0.331129 | False |
| production / transport_d3_s7 | 1.000000 | -0.147921 | [-0.16582377115885408, -0.12833190917968737] | -0.433640 | False |

## Fixed-state assays

| Cell | Outcross gradient | Total gradient | Total gradient CI |
|---|---:|---:|---|
| assay_a0p05_m0p5_s0p0_c0p0 | 0.776291 | 0.776291 | [0.7520141153159337, 0.7998248245216382] |
| assay_a0p05_m0p5_s0p0_c0p5 | 0.569745 | 0.569745 | [0.5519573579589212, 0.5869047528276479] |
| assay_a0p05_m0p5_s0p5_c0p0 | 0.776291 | 0.584244 | [0.565902687354128, 0.6020213238069289] |
| assay_a0p05_m0p5_s0p5_c0p5 | 0.569745 | -0.415948 | [-0.43023344190635787, -0.40214428010031994] |
| assay_a0p05_m0p9_s0p0_c0p0 | 0.061054 | 0.061054 | [0.04809850739397498, 0.07519323479215687] |
| assay_a0p05_m0p9_s0p0_c0p5 | 0.043965 | 0.043965 | [0.034581370038716926, 0.05418656843688608] |
| assay_a0p05_m0p9_s0p5_c0p0 | 0.061054 | 0.045814 | [0.03608700802130465, 0.056429820770860166] |
| assay_a0p05_m0p9_s0p5_c0p5 | 0.043965 | -0.836001 | [-0.8434990976743214, -0.8278299668964776] |
| assay_a0p4_m0p5_s0p0_c0p0 | 4.055959 | 4.055959 | [3.968347702473631, 4.137077034140656] |
| assay_a0p4_m0p5_s0p0_c0p5 | 2.904210 | 2.904210 | [2.8433579825125235, 2.960333618552439] |
| assay_a0p4_m0p5_s0p5_c0p0 | 4.055959 | 3.118108 | [3.0484792897896784, 3.1830427884216363] |
| assay_a0p4_m0p5_s0p5_c0p5 | 2.904210 | 1.529701 | [1.4766991201262438, 1.5785380492479133] |
| assay_a0p4_m0p9_s0p0_c0p0 | 0.429490 | 0.429490 | [0.34347552564985345, 0.5231579239073656] |
| assay_a0p4_m0p9_s0p0_c0p5 | 0.306962 | 0.306962 | [0.2452611857098153, 0.3740547889439198] |
| assay_a0p4_m0p9_s0p5_c0p0 | 0.429490 | 0.323301 | [0.2581621645892245, 0.39410805220588424] |
| assay_a0p4_m0p9_s0p5_c0p5 | 0.306962 | -0.624095 | [-0.6739631095602341, -0.5698108700943164] |

## Outstanding before completion

Paired numerical gates and uncertainty; all nine family interpretations; S/C/I and transport uncertainty; effective-exposure admissibility; publication-quality family figures and visual QA; baseline invariants; compact reproducible provenance and final GitHub verification. No further biological tuning or outcome-selected replication.
