# Existing tempo cohort: realization accounting tables

Retrospective accounting of the unchanged synthetic cohort. Genetic totals use signed trait units: the arithmetic mean over 4 nested repeats within each profile, then an equal mean over 16 profiles. Early [0,100) contains 100 updates; late [100,400) contains 300; full [0,400) is their sum. No confidence intervals or p-values. Parent sampling is a descriptive lottery realization; these sums do not establish controlled causal mediation. Mutation-zero residual is Mendelian segregation; mutation-active residual combines segregation and mutation.

Genetic table values are displayed with ten significant digits; full precision is retained in JSON. Cost denotes direct assurance cost; mutation is the frozen rate applied to each inherited allele copy. The source expected response is pre-mutation.

## Genetic arm means: I, early [0,100)

| Timing | Cost | Mutation | Schedule | Observed change | Expected response | Parent sampling | Segregation + mutation remainder |
| --- | --- | --- | --- | --- | --- | --- | --- |
| delayed | 0 | 0 | abrupt | 0.03824085124 | 0.04644060994 | -0.01216230329 | 0.003962544578 |
| delayed | 0 | 0 | gradual | 0.154901039 | 0.1487332176 | 0.004876504506 | 0.001291316857 |
| delayed | 0 | 0.01 | abrupt | 0.06369470533 | 0.03191126325 | 0.02430944565 | 0.007473996417 |
| delayed | 0 | 0.01 | gradual | 0.1596925946 | 0.1496508101 | 0.003646901737 | 0.006394882836 |
| delayed | 0.5 | 0 | abrupt | 0.06704072925 | 0.07543201057 | -0.01200662464 | 0.003615343328 |
| delayed | 0.5 | 0 | gradual | 0.1687670208 | 0.1759912907 | -0.01641330038 | 0.009189030481 |
| delayed | 0.5 | 0.01 | abrupt | 0.07901230147 | 0.08156652693 | -0.008362497881 | 0.005808272421 |
| delayed | 0.5 | 0.01 | gradual | 0.1944752026 | 0.1778027068 | 0.009894765496 | 0.006777730291 |
| prior | 0 | 0 | abrupt | -0.06728060452 | -0.08354704354 | 0.01484979543 | 0.001416643587 |
| prior | 0 | 0 | gradual | -0.02655411329 | -0.01582961094 | -0.005385182999 | -0.005339319351 |
| prior | 0 | 0.01 | abrupt | -0.06813602045 | -0.06524798972 | -0.006063817137 | 0.00317578641 |
| prior | 0 | 0.01 | gradual | -0.04655737418 | -0.04438815304 | -0.01041886514 | 0.008249644007 |
| prior | 0.5 | 0 | abrupt | 0.004943622143 | 0.008256234635 | -0.001283324727 | -0.002029287765 |
| prior | 0.5 | 0 | gradual | 0.07081426216 | 0.07949107877 | -0.01201706873 | 0.003340252129 |
| prior | 0.5 | 0.01 | abrupt | -0.01752086439 | -0.0137611267 | -0.007845184002 | 0.004085446311 |
| prior | 0.5 | 0.01 | gradual | 0.06135803646 | 0.06739007141 | 0.003406982084 | -0.00943901704 |

## Genetic arm means: I, late [100,400)

| Timing | Cost | Mutation | Schedule | Observed change | Expected response | Parent sampling | Segregation + mutation remainder |
| --- | --- | --- | --- | --- | --- | --- | --- |
| delayed | 0 | 0 | abrupt | -0.01041092065 | -0.01304563843 | 0.001632805393 | 0.001001912384 |
| delayed | 0 | 0 | gradual | -0.01937178531 | -0.01555215561 | -0.004312512572 | 0.0004928828633 |
| delayed | 0 | 0.01 | abrupt | 0.02307550474 | 0.01542648543 | 0.002973933855 | 0.004675085463 |
| delayed | 0 | 0.01 | gradual | 0.01969994923 | 0.01497271842 | -0.0009126665641 | 0.005639897372 |
| delayed | 0.5 | 0 | abrupt | -0.00534816994 | -0.008249946758 | 0.0005194664286 | 0.00238231039 |
| delayed | 0.5 | 0 | gradual | -0.01181317395 | -0.01269834582 | 0.001309677743 | -0.0004245058706 |
| delayed | 0.5 | 0.01 | abrupt | 0.04162176463 | 0.06027175684 | -0.02482865156 | 0.006178659358 |
| delayed | 0.5 | 0.01 | gradual | 0.05925552883 | 0.04938221202 | 0.01346150936 | -0.00358819255 |
| prior | 0 | 0 | abrupt | -0.005441711174 | -0.003896852707 | -0.001569322029 | 2.446356078e-05 |
| prior | 0 | 0 | gradual | -0.009585569947 | -0.01861804789 | 0.008115806002 | 0.0009166719431 |
| prior | 0 | 0.01 | abrupt | -0.06904182732 | -0.0675996732 | -0.002858041733 | 0.001415887612 |
| prior | 0 | 0.01 | gradual | -0.08121563692 | -0.08402582217 | -0.00156820747 | 0.004378392717 |
| prior | 0.5 | 0 | abrupt | -0.0007133811799 | -0.001227069199 | 0.0006131999914 | -9.951197233e-05 |
| prior | 0.5 | 0 | gradual | -0.01635343752 | -0.0114922541 | -0.001808202727 | -0.003052980698 |
| prior | 0.5 | 0.01 | abrupt | -0.04398054958 | -0.04506240829 | -0.001692862365 | 0.002774721083 |
| prior | 0.5 | 0.01 | gradual | -0.01973658815 | -0.02932946431 | 0.01001960607 | -0.0004267299082 |

## Genetic arm means: I, full [0,400)

| Timing | Cost | Mutation | Schedule | Observed change | Expected response | Parent sampling | Segregation + mutation remainder |
| --- | --- | --- | --- | --- | --- | --- | --- |
| delayed | 0 | 0 | abrupt | 0.02782993058 | 0.03339497151 | -0.01052949789 | 0.004964456963 |
| delayed | 0 | 0 | gradual | 0.1355292537 | 0.133181062 | 0.0005639919344 | 0.00178419972 |
| delayed | 0 | 0.01 | abrupt | 0.08677021007 | 0.04733774868 | 0.02728337951 | 0.01214908188 |
| delayed | 0 | 0.01 | gradual | 0.1793925439 | 0.1646235285 | 0.002734235173 | 0.01203478021 |
| delayed | 0.5 | 0 | abrupt | 0.06169255931 | 0.06718206381 | -0.01148715821 | 0.005997653718 |
| delayed | 0.5 | 0 | gradual | 0.1569538468 | 0.1632929449 | -0.01510362264 | 0.008764524611 |
| delayed | 0.5 | 0.01 | abrupt | 0.1206340661 | 0.1418382838 | -0.03319114945 | 0.01198693178 |
| delayed | 0.5 | 0.01 | gradual | 0.2537307314 | 0.2271849188 | 0.02335627486 | 0.003189537742 |
| prior | 0 | 0 | abrupt | -0.07272231569 | -0.08744389624 | 0.01328047341 | 0.001441107148 |
| prior | 0 | 0 | gradual | -0.03613968323 | -0.03444765883 | 0.002730623003 | -0.004422647408 |
| prior | 0 | 0.01 | abrupt | -0.1371778478 | -0.1328476629 | -0.008921858869 | 0.004591674021 |
| prior | 0 | 0.01 | gradual | -0.1277730111 | -0.1284139752 | -0.01198707261 | 0.01262803672 |
| prior | 0.5 | 0 | abrupt | 0.004230240963 | 0.007029165436 | -0.0006701247353 | -0.002128799737 |
| prior | 0.5 | 0 | gradual | 0.05446082464 | 0.06799882467 | -0.01382527146 | 0.0002872714305 |
| prior | 0.5 | 0.01 | abrupt | -0.06150141397 | -0.058823535 | -0.009538046366 | 0.006860167394 |
| prior | 0.5 | 0.01 | gradual | 0.04162144831 | 0.0380606071 | 0.01342658816 | -0.009865746948 |

## Genetic arm means: A, early [0,100)

| Timing | Cost | Mutation | Schedule | Observed change | Expected response | Parent sampling | Segregation + mutation remainder |
| --- | --- | --- | --- | --- | --- | --- | --- |
| delayed | 0 | 0 | abrupt | 0.2345041487 | 0.2446164983 | 0.003144856101 | -0.01325720568 |
| delayed | 0 | 0 | gradual | 0.1891096741 | 0.2010605086 | -0.01602027299 | 0.004069438473 |
| delayed | 0 | 0.01 | abrupt | 0.2685616276 | 0.2563908208 | 0.01329005905 | -0.00111925223 |
| delayed | 0 | 0.01 | gradual | 0.1922488184 | 0.1998120531 | -0.00709549224 | -0.0004677423839 |
| delayed | 0.5 | 0 | abrupt | 0.1401027491 | 0.1312169767 | 0.007642326084 | 0.001243446357 |
| delayed | 0.5 | 0 | gradual | 0.04458094442 | 0.05807460412 | -0.003610548744 | -0.009883110948 |
| delayed | 0.5 | 0.01 | abrupt | 0.1382767608 | 0.144463451 | -0.006370772383 | 0.0001840821852 |
| delayed | 0.5 | 0.01 | gradual | 0.05785584379 | 0.04834159401 | 0.001371411493 | 0.008142838285 |
| prior | 0 | 0 | abrupt | 0.2554151726 | 0.2483054755 | 0.01406383942 | -0.006954142288 |
| prior | 0 | 0 | gradual | 0.2239604393 | 0.2181535634 | 0.005246013912 | 0.0005608619974 |
| prior | 0 | 0.01 | abrupt | 0.2836095809 | 0.2714595674 | 0.01186149536 | 0.0002885181278 |
| prior | 0 | 0.01 | gradual | 0.3085528256 | 0.2959942688 | 0.01055346261 | 0.002005094183 |
| prior | 0.5 | 0 | abrupt | 0.1339486341 | 0.1501672956 | -0.01833252884 | 0.002113867311 |
| prior | 0.5 | 0 | gradual | 0.09974235591 | 0.09825899624 | 0.02379134393 | -0.02230798427 |
| prior | 0.5 | 0.01 | abrupt | 0.16953155 | 0.1554246051 | 0.01401102139 | 9.592347356e-05 |
| prior | 0.5 | 0.01 | gradual | 0.104845946 | 0.1003858579 | 0.002802549198 | 0.001657538912 |

## Genetic arm means: A, late [100,400)

| Timing | Cost | Mutation | Schedule | Observed change | Expected response | Parent sampling | Segregation + mutation remainder |
| --- | --- | --- | --- | --- | --- | --- | --- |
| delayed | 0 | 0 | abrupt | 0.000828512326 | 0.0005896250495 | -0.0001897577801 | 0.0004286450566 |
| delayed | 0 | 0 | gradual | 0.01158812932 | 0.01200946582 | 0.001991764678 | -0.002413101179 |
| delayed | 0 | 0.01 | abrupt | 0.1034918029 | 0.1142119784 | -0.004169933414 | -0.006550242024 |
| delayed | 0 | 0.01 | gradual | 0.1088813156 | 0.1127590311 | 0.007132760212 | -0.01101047571 |
| delayed | 0.5 | 0 | abrupt | -0.0001191646325 | 0.003281060105 | -0.001333629375 | -0.002066595363 |
| delayed | 0.5 | 0 | gradual | 0.02060196945 | 0.01979331519 | 0.002398834995 | -0.001590180741 |
| delayed | 0.5 | 0.01 | abrupt | 0.005550880905 | 0.0152613412 | -0.006762098925 | -0.002948361367 |
| delayed | 0.5 | 0.01 | gradual | -0.02463769199 | -0.002837368201 | -0.01569042702 | -0.006109896766 |
| prior | 0 | 0 | abrupt | 0.0001393557571 | 0.0001313331595 | 3.639850572e-05 | -2.83759081e-05 |
| prior | 0 | 0 | gradual | 0.0009039001514 | 0.0005639199238 | 0.0005619160084 | -0.0002219357808 |
| prior | 0 | 0.01 | abrupt | 0.1511401029 | 0.1711531232 | 0.003970377934 | -0.02398339831 |
| prior | 0 | 0.01 | gradual | 0.1192197909 | 0.1475901384 | -0.002611427799 | -0.0257589196 |
| prior | 0.5 | 0 | abrupt | 0.001373263624 | 0.00118418907 | 0.0004251184656 | -0.0002360439114 |
| prior | 0.5 | 0 | gradual | 0.01134594233 | 0.01029379106 | 0.001823047946 | -0.0007708966774 |
| prior | 0.5 | 0.01 | abrupt | 0.07341349176 | 0.06029890212 | 0.01205259086 | 0.001061998781 |
| prior | 0.5 | 0.01 | gradual | 0.0415424818 | 0.03694807078 | 0.005667944798 | -0.001073533779 |

## Genetic arm means: A, full [0,400)

| Timing | Cost | Mutation | Schedule | Observed change | Expected response | Parent sampling | Segregation + mutation remainder |
| --- | --- | --- | --- | --- | --- | --- | --- |
| delayed | 0 | 0 | abrupt | 0.235332661 | 0.2452061233 | 0.002955098321 | -0.01282856063 |
| delayed | 0 | 0 | gradual | 0.2006978034 | 0.2130699745 | -0.01402850831 | 0.001656337294 |
| delayed | 0 | 0.01 | abrupt | 0.3720534306 | 0.3706027992 | 0.009120125636 | -0.007669494254 |
| delayed | 0 | 0.01 | gradual | 0.301130134 | 0.3125710841 | 3.726797133e-05 | -0.0114782181 |
| delayed | 0.5 | 0 | abrupt | 0.1399835845 | 0.1344980368 | 0.006308696709 | -0.0008231490066 |
| delayed | 0.5 | 0 | gradual | 0.06518291387 | 0.07786791931 | -0.001211713749 | -0.01147329169 |
| delayed | 0.5 | 0.01 | abrupt | 0.1438276417 | 0.1597247922 | -0.01313287131 | -0.002764279182 |
| delayed | 0.5 | 0.01 | gradual | 0.0332181518 | 0.04550422581 | -0.01431901553 | 0.002032941519 |
| prior | 0 | 0 | abrupt | 0.2555545283 | 0.2484368086 | 0.01410023793 | -0.006982518196 |
| prior | 0 | 0 | gradual | 0.2248643394 | 0.2187174833 | 0.00580792992 | 0.0003389262166 |
| prior | 0 | 0.01 | abrupt | 0.4347496837 | 0.4426126906 | 0.01583187329 | -0.02369488018 |
| prior | 0 | 0.01 | gradual | 0.4277726165 | 0.4435844072 | 0.007942034816 | -0.02375382542 |
| prior | 0.5 | 0 | abrupt | 0.1353218977 | 0.1513514847 | -0.01790741038 | 0.0018778234 |
| prior | 0.5 | 0 | gradual | 0.1110882982 | 0.1085527873 | 0.02561439188 | -0.02307888095 |
| prior | 0.5 | 0.01 | abrupt | 0.2429450418 | 0.2157235073 | 0.02606361226 | 0.001157922254 |
| prior | 0.5 | 0.01 | gradual | 0.1463884278 | 0.1373339287 | 0.008470493995 | 0.0005840051324 |

## Paired abrupt minus gradual: I, early [0,100)

Sixteen paired profile differences, each based on the same four nested repeats per schedule.

| Timing | Cost | Mutation | Observed change | Expected response | Parent sampling | Segregation + mutation remainder |
| --- | --- | --- | --- | --- | --- | --- |
| delayed | 0 | 0 | -0.1166601877 | -0.1022926077 | -0.01703880779 | 0.002671227721 |
| delayed | 0 | 0.01 | -0.09599788932 | -0.1177395468 | 0.02066254392 | 0.001079113581 |
| delayed | 0.5 | 0 | -0.1017262915 | -0.1005592801 | 0.004406675739 | -0.005573687153 |
| delayed | 0.5 | 0.01 | -0.1154629011 | -0.09623617984 | -0.01825726338 | -0.0009694578706 |
| prior | 0 | 0 | -0.04072649123 | -0.0677174326 | 0.02023497843 | 0.006755962938 |
| prior | 0 | 0.01 | -0.02157864627 | -0.02085983668 | 0.004355048008 | -0.005073857598 |
| prior | 0.5 | 0 | -0.06587064002 | -0.07123484413 | 0.01073374401 | -0.005369539894 |
| prior | 0.5 | 0.01 | -0.07887890085 | -0.08115119812 | -0.01125216609 | 0.01352446335 |

## Paired abrupt minus gradual: I, late [100,400)

Sixteen paired profile differences, each based on the same four nested repeats per schedule.

| Timing | Cost | Mutation | Observed change | Expected response | Parent sampling | Segregation + mutation remainder |
| --- | --- | --- | --- | --- | --- | --- |
| delayed | 0 | 0 | 0.008960864663 | 0.002506517177 | 0.005945317965 | 0.0005090295212 |
| delayed | 0 | 0.01 | 0.003375555513 | 0.0004537670033 | 0.003886600419 | -0.0009648119095 |
| delayed | 0.5 | 0 | 0.006465004011 | 0.004448399065 | -0.0007902113145 | 0.002806816261 |
| delayed | 0.5 | 0.01 | -0.01763376419 | 0.01088954483 | -0.03829016092 | 0.009766851907 |
| prior | 0 | 0 | 0.004143858773 | 0.01472119519 | -0.009685128031 | -0.0008922083823 |
| prior | 0 | 0.01 | 0.0121738096 | 0.01642614896 | -0.001289834262 | -0.002962505105 |
| prior | 0.5 | 0 | 0.01564005634 | 0.0102651849 | 0.002421402719 | 0.002953468726 |
| prior | 0.5 | 0.01 | -0.02424396143 | -0.01573294398 | -0.01171246844 | 0.003201450991 |

## Paired abrupt minus gradual: I, full [0,400)

Sixteen paired profile differences, each based on the same four nested repeats per schedule.

| Timing | Cost | Mutation | Observed change | Expected response | Parent sampling | Segregation + mutation remainder |
| --- | --- | --- | --- | --- | --- | --- |
| delayed | 0 | 0 | -0.1076993231 | -0.09978609048 | -0.01109348983 | 0.003180257243 |
| delayed | 0 | 0.01 | -0.09262233381 | -0.1172857798 | 0.02454914434 | 0.0001143016715 |
| delayed | 0.5 | 0 | -0.09526128751 | -0.09611088105 | 0.003616464424 | -0.002766870892 |
| delayed | 0.5 | 0.01 | -0.1330966653 | -0.08534663501 | -0.0565474243 | 0.008797394037 |
| prior | 0 | 0 | -0.03658263246 | -0.05299623741 | 0.0105498504 | 0.005863754556 |
| prior | 0 | 0.01 | -0.009404836669 | -0.004433687711 | 0.003065213746 | -0.008036362703 |
| prior | 0.5 | 0 | -0.05023058368 | -0.06096965923 | 0.01315514673 | -0.002416071168 |
| prior | 0.5 | 0.01 | -0.1031228623 | -0.0968841421 | -0.02296463452 | 0.01672591434 |

## Paired abrupt minus gradual: A, early [0,100)

Sixteen paired profile differences, each based on the same four nested repeats per schedule.

| Timing | Cost | Mutation | Observed change | Expected response | Parent sampling | Segregation + mutation remainder |
| --- | --- | --- | --- | --- | --- | --- |
| delayed | 0 | 0 | 0.04539447457 | 0.04355598964 | 0.01916512909 | -0.01732664416 |
| delayed | 0 | 0.01 | 0.07631280918 | 0.05657876773 | 0.02038555129 | -0.000651509846 |
| delayed | 0.5 | 0 | 0.09552180468 | 0.07314237255 | 0.01125287483 | 0.0111265573 |
| delayed | 0.5 | 0.01 | 0.08042091702 | 0.096121857 | -0.007742183876 | -0.0079587561 |
| prior | 0 | 0 | 0.0314547333 | 0.03015191208 | 0.008817825509 | -0.007515004285 |
| prior | 0 | 0.01 | -0.02494324471 | -0.0245347014 | 0.001308032743 | -0.001716576055 |
| prior | 0.5 | 0 | 0.0342062782 | 0.05190829939 | -0.04212387277 | 0.02442185158 |
| prior | 0.5 | 0.01 | 0.06468560402 | 0.05503874727 | 0.0112084722 | -0.001561615438 |

## Paired abrupt minus gradual: A, late [100,400)

Sixteen paired profile differences, each based on the same four nested repeats per schedule.

| Timing | Cost | Mutation | Observed change | Expected response | Parent sampling | Segregation + mutation remainder |
| --- | --- | --- | --- | --- | --- | --- |
| delayed | 0 | 0 | -0.01075961699 | -0.01141984077 | -0.002181522458 | 0.002841746236 |
| delayed | 0 | 0.01 | -0.005389512634 | 0.001452947301 | -0.01130269363 | 0.004460233691 |
| delayed | 0.5 | 0 | -0.02072113408 | -0.01651225509 | -0.00373246437 | -0.0004764146225 |
| delayed | 0.5 | 0.01 | 0.03018857289 | 0.0180987094 | 0.008928328098 | 0.003161535399 |
| prior | 0 | 0 | -0.0007645443943 | -0.0004325867643 | -0.0005255175026 | 0.0001935598727 |
| prior | 0 | 0.01 | 0.03192031191 | 0.02356298488 | 0.006581805733 | 0.001775521291 |
| prior | 0.5 | 0 | -0.009972678704 | -0.00910960199 | -0.00139792948 | 0.000534852766 |
| prior | 0.5 | 0.01 | 0.03187100996 | 0.02335083133 | 0.006384646066 | 0.00213553256 |

## Paired abrupt minus gradual: A, full [0,400)

Sixteen paired profile differences, each based on the same four nested repeats per schedule.

| Timing | Cost | Mutation | Observed change | Expected response | Parent sampling | Segregation + mutation remainder |
| --- | --- | --- | --- | --- | --- | --- |
| delayed | 0 | 0 | 0.03463485757 | 0.03213614886 | 0.01698360663 | -0.01448489792 |
| delayed | 0 | 0.01 | 0.07092329654 | 0.05803171503 | 0.009082857665 | 0.003808723845 |
| delayed | 0.5 | 0 | 0.0748006706 | 0.05663011746 | 0.007520410458 | 0.01065014268 |
| delayed | 0.5 | 0.01 | 0.1106094899 | 0.1142205664 | 0.001186144221 | -0.004797220701 |
| prior | 0 | 0 | 0.03069018891 | 0.02971932531 | 0.008292308007 | -0.007321444412 |
| prior | 0 | 0.01 | 0.006977067196 | -0.0009717165149 | 0.007889838476 | 5.894523507e-05 |
| prior | 0.5 | 0 | 0.02423359949 | 0.0427986974 | -0.04352180225 | 0.02495670435 |
| prior | 0.5 | 0.01 | 0.09655661398 | 0.0783895786 | 0.01759311826 | 0.000573917122 |

## Full demography: observed census and retained recruitment

All-census totals include founders; post-update totals contain 400 censuses per case. Missing recruit slots count 48 minus actual retained recruits at each update.

| Arm | Cases | All censuses | Post-update censuses | All N<48 | Post N<48 | Minimum N | Cases ever N<48 | Missing recruit slots |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| overall | 1024 | 410624 | 409600 | 23 | 23 | 34 | 13 | 98 |
| delayed; c=0; mu=0; abrupt | 64 | 25664 | 25600 | 0 | 0 | 48 | 0 | 0 |
| delayed; c=0; mu=0; gradual | 64 | 25664 | 25600 | 0 | 0 | 48 | 0 | 0 |
| delayed; c=0; mu=0.01; abrupt | 64 | 25664 | 25600 | 0 | 0 | 48 | 0 | 0 |
| delayed; c=0; mu=0.01; gradual | 64 | 25664 | 25600 | 0 | 0 | 48 | 0 | 0 |
| delayed; c=0.5; mu=0; abrupt | 64 | 25664 | 25600 | 4 | 4 | 37 | 2 | 19 |
| delayed; c=0.5; mu=0; gradual | 64 | 25664 | 25600 | 0 | 0 | 48 | 0 | 0 |
| delayed; c=0.5; mu=0.01; abrupt | 64 | 25664 | 25600 | 9 | 9 | 34 | 3 | 55 |
| delayed; c=0.5; mu=0.01; gradual | 64 | 25664 | 25600 | 0 | 0 | 48 | 0 | 0 |
| prior; c=0; mu=0; abrupt | 64 | 25664 | 25600 | 0 | 0 | 48 | 0 | 0 |
| prior; c=0; mu=0; gradual | 64 | 25664 | 25600 | 0 | 0 | 48 | 0 | 0 |
| prior; c=0; mu=0.01; abrupt | 64 | 25664 | 25600 | 0 | 0 | 48 | 0 | 0 |
| prior; c=0; mu=0.01; gradual | 64 | 25664 | 25600 | 0 | 0 | 48 | 0 | 0 |
| prior; c=0.5; mu=0; abrupt | 64 | 25664 | 25600 | 7 | 7 | 42 | 5 | 17 |
| prior; c=0.5; mu=0; gradual | 64 | 25664 | 25600 | 1 | 1 | 47 | 1 | 1 |
| prior; c=0.5; mu=0.01; abrupt | 64 | 25664 | 25600 | 2 | 2 | 44 | 2 | 6 |
| prior; c=0.5; mu=0.01; gradual | 64 | 25664 | 25600 | 0 | 0 | 48 | 0 | 0 |

## Full demography: seed intensity and retained mating counts

Expected viable seed intensity is distinct from retained recruits. Selfed fraction is the ratio of pooled retained counts; mean case selfed fraction gives cases equal weight. The fraction denominator is retained selfed plus retained outcross recruits. Intensity means/counts use source updates.

| Arm | Min intensity | Mean intensity | Updates intensity<48 | Selfed recruits | Outcross recruits | Total recruits | Pooled self fraction | Mean case self fraction | Defined cases |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| overall | 41.31719221 | 145.6112024 | 7 | 12644952 | 7015750 | 19660702 | 0.6431587234 | 0.643158666 | 1024 |
| delayed; c=0; mu=0; abrupt | 77.04898748 | 147.6860024 | 0 | 881007 | 347793 | 1228800 | 0.716965332 | 0.716965332 | 64 |
| delayed; c=0; mu=0; gradual | 102.0434023 | 161.8539805 | 0 | 624569 | 604231 | 1228800 | 0.5082755534 | 0.5082755534 | 64 |
| delayed; c=0; mu=0.01; abrupt | 69.15817983 | 198.9562223 | 0 | 557930 | 670870 | 1228800 | 0.4540445964 | 0.4540445964 | 64 |
| delayed; c=0; mu=0.01; gradual | 109.4564996 | 205.8544526 | 0 | 364516 | 864284 | 1228800 | 0.2966438802 | 0.2966438802 | 64 |
| delayed; c=0.5; mu=0; abrupt | 44.53007115 | 113.3868135 | 1 | 805909 | 422872 | 1228781 | 0.6558605643 | 0.6558638529 | 64 |
| delayed; c=0.5; mu=0; gradual | 72.80747366 | 131.1154415 | 0 | 533554 | 695246 | 1228800 | 0.4342073568 | 0.4342073568 | 64 |
| delayed; c=0.5; mu=0.01; abrupt | 41.31719221 | 154.5280102 | 6 | 466749 | 761996 | 1228745 | 0.3798583107 | 0.3798615729 | 64 |
| delayed; c=0.5; mu=0.01; gradual | 67.50756827 | 173.1302815 | 0 | 234232 | 994568 | 1228800 | 0.1906184896 | 0.1906184896 | 64 |
| prior; c=0; mu=0; abrupt | 73.44339931 | 135.1568756 | 0 | 1150226 | 78574 | 1228800 | 0.9360563151 | 0.9360563151 | 64 |
| prior; c=0; mu=0; gradual | 105.6553666 | 140.6054015 | 0 | 1047301 | 181499 | 1228800 | 0.8522957357 | 0.8522957357 | 64 |
| prior; c=0; mu=0.01; abrupt | 79.94476659 | 156.2466555 | 0 | 1119996 | 108804 | 1228800 | 0.9114550781 | 0.9114550781 | 64 |
| prior; c=0; mu=0.01; gradual | 100.2882947 | 162.3009188 | 0 | 1081939 | 146861 | 1228800 | 0.8804842122 | 0.8804842122 | 64 |
| prior; c=0.5; mu=0; abrupt | 57.66067061 | 98.27239537 | 0 | 1063852 | 164931 | 1228783 | 0.8657769517 | 0.8657772423 | 64 |
| prior; c=0.5; mu=0; gradual | 69.33924741 | 106.8351047 | 0 | 927372 | 301427 | 1228799 | 0.7546978798 | 0.7546978264 | 64 |
| prior; c=0.5; mu=0.01; abrupt | 50.41117528 | 115.0861369 | 0 | 988720 | 240074 | 1228794 | 0.8046263247 | 0.8046262478 | 64 |
| prior; c=0.5; mu=0.01; gradual | 79.61965672 | 128.7645462 | 0 | 797080 | 431720 | 1228800 | 0.6486653646 | 0.6486653646 | 64 |

## Conditional saved-state recruitment kernels

The conditional one-step law is R ~ Poisson(expected viable seed intensity), next N = min(R,48); it is not multigeneration survival. Minimum, maximum, mean and sum summarize the saved source states. Risk sums are sums of conditional diagnostics, not a probability of loss over a history. Capacity shortfall is directly calculated from the finite Poisson lower tail.

### p_zero

| Arm | Minimum | Maximum | Mean | Sum over source states |
| --- | --- | --- | --- | --- |
| overall | 1.844563314e-110 | 1.138076395e-18 | 4.7898435e-24 | 1.961919898e-18 |
| delayed; c=0; mu=0; abrupt | 1.423740281e-104 | 3.451834007e-34 | 1.106418947e-37 | 2.832432505e-33 |
| delayed; c=0; mu=0; gradual | 2.003154187e-107 | 4.820737322e-45 | 3.398823445e-47 | 8.700988019e-43 |
| delayed; c=0; mu=0.01; abrupt | 1.844563314e-110 | 9.225376986e-31 | 3.803825386e-35 | 9.737792987e-31 |
| delayed; c=0; mu=0.01; gradual | 5.722175248e-110 | 2.908346928e-48 | 1.771321657e-52 | 4.534583442e-48 |
| delayed; c=0.5; mu=0; abrupt | 2.659562477e-86 | 4.579687258e-20 | 1.790081058e-24 | 4.582607509e-20 |
| delayed; c=0.5; mu=0; gradual | 1.583568922e-87 | 2.399473446e-32 | 2.550138058e-34 | 6.528353427e-30 |
| delayed; c=0.5; mu=0.01; abrupt | 1.411832933e-87 | 1.138076395e-18 | 7.484050823e-23 | 1.915917011e-18 |
| delayed; c=0.5; mu=0.01; gradual | 2.941636422e-89 | 4.806573785e-30 | 9.656791999e-34 | 2.472138752e-29 |
| prior; c=0; mu=0; abrupt | 9.806780244e-76 | 1.270389646e-32 | 1.214787165e-36 | 3.109855143e-32 |
| prior; c=0; mu=0; gradual | 3.71387037e-77 | 1.301539388e-46 | 1.557964456e-48 | 3.988389008e-44 |
| prior; c=0; mu=0.01; abrupt | 1.083447374e-82 | 1.907343929e-35 | 1.852201615e-39 | 4.741636134e-35 |
| prior; c=0; mu=0.01; gradual | 1.223095749e-83 | 2.788348365e-44 | 6.290975232e-48 | 1.610489659e-43 |
| prior; c=0.5; mu=0; abrupt | 2.556395182e-73 | 9.084246912e-26 | 5.496624835e-30 | 1.407135958e-25 |
| prior; c=0.5; mu=0; gradual | 4.28934247e-72 | 7.697460523e-31 | 1.604566576e-33 | 4.107690434e-29 |
| prior; c=0.5; mu=0.01; abrupt | 2.200334013e-76 | 1.278511825e-22 | 6.901219676e-27 | 1.766712237e-22 |
| prior; c=0.5; mu=0.01; gradual | 2.314422092e-78 | 2.640112516e-35 | 3.39010512e-39 | 8.678669106e-35 |

### p_below_K

| Arm | Minimum | Maximum | Mean | Sum over source states |
| --- | --- | --- | --- | --- |
| overall | 7.2832521e-57 | 0.8326412317 | 3.432675853e-05 | 14.06024029 |
| delayed; c=0; mu=0; abrupt | 4.264139551e-52 | 0.0001559961039 | 4.133432611e-07 | 0.01058158748 |
| delayed; c=0; mu=0; gradual | 2.129552374e-54 | 8.813110017e-10 | 8.794586324e-12 | 2.251414099e-07 |
| delayed; c=0; mu=0.01; abrupt | 7.2832521e-57 | 0.003066635987 | 2.222874061e-07 | 0.005690557597 |
| delayed; c=0; mu=0.01; gradual | 1.831357357e-56 | 1.361624051e-11 | 1.534419849e-15 | 3.928114814e-11 |
| delayed; c=0.5; mu=0; abrupt | 9.420719885e-38 | 0.6790390825 | 0.0001253272508 | 3.20837762 |
| delayed; c=0.5; mu=0; gradual | 1.089405695e-38 | 0.0008222486868 | 1.215682839e-05 | 0.3112148068 |
| delayed; c=0.5; mu=0.01; abrupt | 9.97655858e-39 | 0.8326412317 | 0.0002546679203 | 6.51949876 |
| delayed; c=0.5; mu=0.01; gradual | 5.08915765e-40 | 0.005358959917 | 3.358514351e-06 | 0.08597796738 |
| prior; c=0; mu=0; abrupt | 7.410774198e-30 | 0.0006465159717 | 1.486411307e-07 | 0.003805212945 |
| prior; c=0; mu=0; gradual | 6.737189183e-31 | 1.187700765e-10 | 1.579343117e-12 | 4.043118379e-08 |
| prior; c=0; mu=0.01; abrupt | 5.131491311e-35 | 4.651252131e-05 | 1.280433096e-08 | 0.0003277908727 |
| prior; c=0; mu=0.01; gradual | 9.904874329e-36 | 2.287555773e-09 | 1.052183652e-12 | 2.69359015e-08 |
| prior; c=0.5; mu=0; abrupt | 4.197362e-28 | 0.08725146608 | 7.094887515e-05 | 1.816291204 |
| prior; c=0.5; mu=0; gradual | 3.186221553e-27 | 0.002880322302 | 2.345191516e-05 | 0.6003690282 |
| prior; c=0.5; mu=0.01; abrupt | 2.484993155e-30 | 0.3481576092 | 5.849797888e-05 | 1.497548259 |
| prior; c=0.5; mu=0.01; gradual | 8.711600443e-32 | 5.343533154e-05 | 2.176583632e-08 | 0.0005572054097 |

### expected_next_N

| Arm | Minimum | Maximum | Mean | Sum over source states |
| --- | --- | --- | --- | --- |
| overall | 40.78448481 | 48 | 47.99983402 | 19660732.01 |
| delayed; c=0; mu=0; abrupt | 47.99963154 | 48 | 47.99999909 | 1228799.977 |
| delayed; c=0; mu=0; gradual | 48 | 48 | 48 | 1228800 |
| delayed; c=0; mu=0.01; abrupt | 47.99163451 | 48 | 47.99999943 | 1228799.985 |
| delayed; c=0; mu=0.01; gradual | 48 | 48 | 48 | 1228800 |
| delayed; c=0.5; mu=0; abrupt | 43.22536705 | 48 | 47.99944585 | 1228785.814 |
| delayed; c=0.5; mu=0; gradual | 47.99791283 | 48 | 47.99996978 | 1228799.226 |
| delayed; c=0.5; mu=0.01; abrupt | 40.78448481 | 48 | 47.99843953 | 1228760.052 |
| delayed; c=0.5; mu=0.01; gradual | 47.98484243 | 48 | 47.99999106 | 1228799.771 |
| prior; c=0; mu=0; abrupt | 47.99837772 | 48 | 47.99999965 | 1228799.991 |
| prior; c=0; mu=0; gradual | 48 | 48 | 48 | 1228800 |
| prior; c=0; mu=0.01; abrupt | 47.99989478 | 48 | 47.99999997 | 1228799.999 |
| prior; c=0; mu=0.01; gradual | 48 | 48 | 48 | 1228800 |
| prior; c=0.5; mu=0; abrupt | 47.67382169 | 48 | 47.99979612 | 1228794.781 |
| prior; c=0.5; mu=0; gradual | 47.99217275 | 48 | 47.99994003 | 1228798.465 |
| prior; c=0.5; mu=0.01; abrupt | 46.23736481 | 48 | 47.99976382 | 1228793.954 |
| prior; c=0.5; mu=0.01; gradual | 47.99987856 | 48 | 47.99999995 | 1228799.999 |

### expected_capacity_shortfall

| Arm | Minimum | Maximum | Mean | Sum over source states |
| --- | --- | --- | --- | --- |
| overall | 8.928120448e-57 | 7.215515194 | 0.0001659825721 | 67.98646153 |
| delayed; c=0; mu=0; abrupt | 5.294108772e-52 | 0.0003684620513 | 9.131961003e-07 | 0.02337782017 |
| delayed; c=0; mu=0; gradual | 2.627174844e-54 | 1.588797299e-09 | 1.573405179e-11 | 4.027917258e-07 |
| delayed; c=0; mu=0.01; abrupt | 8.928120448e-57 | 0.008365490414 | 5.749952218e-07 | 0.01471987768 |
| delayed; c=0; mu=0.01; gradual | 2.247213323e-56 | 2.334178932e-11 | 2.595268577e-15 | 6.643887556e-11 |
| delayed; c=0.5; mu=0; abrupt | 1.232152843e-37 | 4.774632952 | 0.0005541459766 | 14.186137 |
| delayed; c=0.5; mu=0; gradual | 1.418788374e-38 | 0.002087173839 | 3.021563788e-05 | 0.7735203298 |
| delayed; c=0.5; mu=0.01; abrupt | 1.299076132e-38 | 7.215515194 | 0.001560471189 | 39.94806243 |
| delayed; c=0.5; mu=0.01; gradual | 6.589535162e-40 | 0.01515757334 | 8.938880966e-06 | 0.2288353527 |
| prior; c=0; mu=0; abrupt | 1.012307865e-29 | 0.001622275015 | 3.547434803e-07 | 0.009081433095 |
| prior; c=0; mu=0; gradual | 9.141982173e-31 | 2.08692202e-10 | 2.763784936e-12 | 7.075289435e-08 |
| prior; c=0; mu=0.01; abrupt | 6.80218534e-35 | 0.0001052165291 | 2.747834467e-08 | 0.0007034456234 |
| prior; c=0; mu=0.01; gradual | 1.308186576e-35 | 4.17924798e-09 | 1.894014156e-12 | 4.84867624e-08 |
| prior; c=0.5; mu=0; abrupt | 5.802734481e-28 | 0.3261783119 | 0.0002038842952 | 5.219437958 |
| prior; c=0.5; mu=0; gradual | 4.433310819e-27 | 0.007827253267 | 5.997209231e-05 | 1.535285563 |
| prior; c=0.5; mu=0.01; abrupt | 3.38407969e-30 | 1.762635192 | 0.0002361757578 | 6.0460994 |
| prior; c=0.5; mu=0.01; gradual | 1.175726751e-31 | 0.0001214384992 | 4.689042905e-08 | 0.001200394984 |

## Fixed-state zero-pollen seed-intensity bound

S0 = 0.5 sum A_i * 8 exp(-0.5 I_i² - c A_i²). This is an algebraic lower bound on the current native total viable seed intensity. It is not a run zero-pollen future or an observed retained-self count; no universal S0 >= 48 claim is implied.

| Arm | Available | Minimum S0 | Mean S0 | Updates S0<48 |
| --- | --- | --- | --- | --- |
| overall | yes | 31.65557999 | 101.1545885 | 3604 |
| delayed; c=0; mu=0; abrupt | yes | 67.3419028 | 116.0948764 | 0 |
| delayed; c=0; mu=0; gradual | yes | 55.20367904 | 104.3168246 | 0 |
| delayed; c=0; mu=0.01; abrupt | yes | 54.25907999 | 126.0043552 | 0 |
| delayed; c=0; mu=0.01; gradual | yes | 49.45957056 | 109.2143197 | 0 |
| delayed; c=0.5; mu=0; abrupt | yes | 42.39277975 | 81.27682801 | 4 |
| delayed; c=0.5; mu=0; gradual | yes | 41.10845829 | 70.90789385 | 873 |
| delayed; c=0.5; mu=0.01; abrupt | yes | 35.37915883 | 79.43236852 | 354 |
| delayed; c=0.5; mu=0.01; gradual | yes | 31.65557999 | 67.89920942 | 1255 |
| prior; c=0; mu=0; abrupt | yes | 63.3953783 | 126.0357604 | 0 |
| prior; c=0; mu=0; gradual | yes | 63.649427 | 119.3870635 | 0 |
| prior; c=0; mu=0.01; abrupt | yes | 57.75225934 | 142.5116099 | 0 |
| prior; c=0; mu=0.01; gradual | yes | 64.66670645 | 143.4727932 | 0 |
| prior; c=0.5; mu=0; abrupt | yes | 47.61379508 | 83.21096418 | 1 |
| prior; c=0.5; mu=0; gradual | yes | 41.0133814 | 78.46707812 | 442 |
| prior; c=0.5; mu=0.01; abrupt | yes | 38.4895618 | 89.48121578 | 296 |
| prior; c=0.5; mu=0.01; gradual | yes | 32.65226517 | 80.76025549 | 379 |

## Supplementary terminal-I descriptors: original saved categories

These counts are copied from the independent archive checker and crosschecked against its 1,024 case records. They are supplementary terminal descriptors, not new event classes. The original A-only and I-event definitions, onsets and confirmations remain unchanged. Every arm has 64 cases. Threshold denotes the registered 0.05 decrease from each actual founder mean; terminal comparisons use census 400.

| Timing | Cost | Mutation | Schedule | I400 > founder | I400 <= founder-0.05 | Saved I event, I400 > threshold | Saved I event, I400 > founder | Saved A-only, I400 > founder |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| delayed | 0 | 0 | abrupt | 42 | 16 | 0 | 0 | 40 |
| delayed | 0 | 0 | gradual | 59 | 3 | 0 | 0 | 53 |
| delayed | 0 | 0.01 | abrupt | 49 | 13 | 4 | 4 | 45 |
| delayed | 0 | 0.01 | gradual | 56 | 5 | 1 | 0 | 53 |
| delayed | 0.5 | 0 | abrupt | 49 | 9 | 1 | 1 | 41 |
| delayed | 0.5 | 0 | gradual | 59 | 1 | 0 | 0 | 34 |
| delayed | 0.5 | 0.01 | abrupt | 49 | 13 | 4 | 2 | 37 |
| delayed | 0.5 | 0.01 | gradual | 62 | 0 | 0 | 0 | 46 |
| prior | 0 | 0 | abrupt | 18 | 34 | 0 | 0 | 16 |
| prior | 0 | 0 | gradual | 28 | 26 | 2 | 1 | 24 |
| prior | 0 | 0.01 | abrupt | 10 | 49 | 0 | 0 | 10 |
| prior | 0 | 0.01 | gradual | 13 | 45 | 3 | 0 | 11 |
| prior | 0.5 | 0 | abrupt | 41 | 18 | 0 | 0 | 34 |
| prior | 0.5 | 0 | gradual | 48 | 9 | 2 | 1 | 32 |
| prior | 0.5 | 0.01 | abrupt | 24 | 30 | 5 | 1 | 21 |
| prior | 0.5 | 0.01 | gradual | 37 | 16 | 8 | 1 | 27 |

### Copied original saved categories: Full 400 updates

| Timing | Cost | Mutation | Schedule | assurance_first | investment_first | near_simultaneous | assurance_only | investment_only | neither |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| delayed | 0 | 0 | abrupt | 14 | 0 | 1 | 46 | 1 | 2 |
| delayed | 0 | 0 | gradual | 3 | 0 | 0 | 55 | 0 | 6 |
| delayed | 0 | 0.01 | abrupt | 14 | 2 | 0 | 48 | 0 | 0 |
| delayed | 0 | 0.01 | gradual | 4 | 0 | 1 | 56 | 0 | 3 |
| delayed | 0.5 | 0 | abrupt | 9 | 0 | 0 | 47 | 1 | 7 |
| delayed | 0.5 | 0 | gradual | 0 | 0 | 0 | 38 | 1 | 25 |
| delayed | 0.5 | 0.01 | abrupt | 16 | 0 | 1 | 37 | 0 | 10 |
| delayed | 0.5 | 0.01 | gradual | 0 | 0 | 0 | 47 | 0 | 17 |
| prior | 0 | 0 | abrupt | 31 | 1 | 2 | 27 | 0 | 3 |
| prior | 0 | 0 | gradual | 23 | 0 | 5 | 33 | 0 | 3 |
| prior | 0 | 0.01 | abrupt | 44 | 2 | 2 | 16 | 0 | 0 |
| prior | 0 | 0.01 | gradual | 45 | 0 | 2 | 15 | 0 | 2 |
| prior | 0.5 | 0 | abrupt | 8 | 2 | 6 | 39 | 2 | 7 |
| prior | 0.5 | 0 | gradual | 7 | 2 | 0 | 36 | 2 | 17 |
| prior | 0.5 | 0.01 | abrupt | 31 | 1 | 3 | 27 | 0 | 2 |
| prior | 0.5 | 0.01 | gradual | 20 | 2 | 0 | 32 | 1 | 9 |

### Copied original saved categories: By 100 updates

| Timing | Cost | Mutation | Schedule | assurance_first | investment_first | near_simultaneous | assurance_only | investment_only | neither |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| delayed | 0 | 0 | abrupt | 10 | 0 | 1 | 49 | 1 | 3 |
| delayed | 0 | 0 | gradual | 1 | 0 | 0 | 54 | 0 | 9 |
| delayed | 0 | 0.01 | abrupt | 9 | 1 | 0 | 51 | 1 | 2 |
| delayed | 0 | 0.01 | gradual | 2 | 0 | 0 | 51 | 0 | 11 |
| delayed | 0.5 | 0 | abrupt | 8 | 0 | 0 | 45 | 1 | 10 |
| delayed | 0.5 | 0 | gradual | 0 | 0 | 0 | 26 | 0 | 38 |
| delayed | 0.5 | 0.01 | abrupt | 7 | 0 | 1 | 38 | 0 | 18 |
| delayed | 0.5 | 0.01 | gradual | 0 | 0 | 0 | 30 | 0 | 34 |
| prior | 0 | 0 | abrupt | 31 | 1 | 2 | 27 | 0 | 3 |
| prior | 0 | 0 | gradual | 17 | 0 | 5 | 39 | 0 | 3 |
| prior | 0 | 0.01 | abrupt | 25 | 0 | 2 | 34 | 1 | 2 |
| prior | 0 | 0.01 | gradual | 30 | 0 | 2 | 29 | 0 | 3 |
| prior | 0.5 | 0 | abrupt | 7 | 2 | 6 | 40 | 1 | 8 |
| prior | 0.5 | 0 | gradual | 5 | 1 | 0 | 32 | 3 | 23 |
| prior | 0.5 | 0.01 | abrupt | 20 | 0 | 3 | 31 | 1 | 9 |
| prior | 0.5 | 0.01 | gradual | 8 | 1 | 0 | 31 | 1 | 23 |
