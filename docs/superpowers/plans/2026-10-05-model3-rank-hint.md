# Rank-start optimization under unchanged residual acceptance

The captured high-grid contraction and all4 completed second-step channels
accepted rank128. Test initial rank128 instead of8/16/32/64/128, preserving
seed997, block width,16million cap and direct residual1e-14. This changes
only numerical search cost. Clamp the hint to admissible rank and still
measure residual; never assume success. On captured input require saved
q/core exactly equal to prior accepted rank128 projection, then measure
runtime. This is not a guarantee that later states need rank128.
