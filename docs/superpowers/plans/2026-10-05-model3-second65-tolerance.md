# Second65-step strict tolerance comparison

After130 candidate tests, use identical saved first65 near/jump state and
second visitor snapshot. Fast streamed solver uses rank hint128 but same
seed997, residual acceptance and16million allocation cap. Tighten local
relative tolerance from1e-8 to1e-10. This checks one step, not full-path error.
Compare full joint state to prior verified second65 output with QR distance:
normalized L1 upper bound<=1e-5. Retain exact marginal reference thresholds
relativeL1<=1e-5 and mean trait gap<=1e-6. Preserve failure without retuning.
No high-grid production admission or ecological conclusions from this gate.
