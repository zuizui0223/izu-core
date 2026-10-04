# Full Model 3 grid continuation after the declared fidelity failure

The completed 5/7/9-node campaign is retained unchanged at e1ec4099.
Its positive-mutation refinement failed. This follow-up addresses numerical
resolution, not biological parameter fitting or rescue of an effect direction.

Run all 32 positive-mutation density cases on 13 uniformly spaced allele nodes:
two assurance settings x four original histories x near/far x jump/heat_fv.
Keep all 1,000 periods, the same projected five-node founders, mutation rate
0.01, width 0.05, and all other biology unchanged. Thirteen nodes include all
five founder support points exactly; 9 and 13 grids are not nested with each
other, so compare their fixed common initial distributions explicitly.

Report signed terminal differences per trait, maximum terminal discrepancy,
and full-trajectory maximum for 9-to-13 in every case. Keep the 0.01 terminal
criterion; no selective removal of histories or changing rates. Passing is a
finite refinement diagnostic, not a rigorous continuum error bound. If it fails,
retain unresolved status and assess computational feasibility of further
refinement before declaring continuum fidelity. The original negative result
remains part of the record.

A timing-only 13-node benchmark used 753,571 genotype states and approximately
1.11 seconds per initial step. No biological outcome was used to select cases.
At most two workers with BLAS/OpenMP limited to one thread. Capture a separate
source snapshot, verify archived members on resume, and preserve all outputs.
No ABM rerun is required because this continuation changes only density grid
resolution. The full goal remains active while the continuum comparison is
unresolved.
