"""Local investment selection in a fixed monomorphic resident at capacity.

The mutant changes; resident donor mass and recipient competition stay fixed.
Fitness is .5 maternal outcross + .5 paternal outcross + viable selfed seed.
This is not the derivative of whole-population seed production.
"""
import numpy as np


def investment_invasion_terms(resident, visitors, config):
    """Return analytic log-invasion gradient, allowing a batch (..., 3)."""
    z = np.asarray(resident, dtype=float)
    if z.shape[-1:] != (3,) or not np.isfinite(z).all() or ((z < 0) | (z > 1)).any():
        raise ValueError("resident traits must be finite and in [0,1]")
    x, i, a = np.moveaxis(z, -1, 0)
    u = .1 + i
    ov = config.ovule_budget * np.exp(-config.investment_cost*i*i-config.assurance_cost*a*a)
    q = np.zeros_like(i)
    dq = np.zeros_like(i)
    export_elasticity = np.zeros_like(i)
    if len(visitors.ids) and config.activity > 0:
        g = np.exp(-((x[...,None]-visitors.optima)/visitors.breadths)**2)
        gs = g.sum(axis=-1,keepdims=True)
        channels = np.divide(g,gs,out=np.zeros_like(g),where=gs>0)
        activity = config.activity
        if config.activity_mode == "count_scaled":
            activity *= len(visitors.ids)/config.reference_visitor_count
        rate = activity*g.mean(axis=-1)
        export_scale = config.pollen_budget*np.exp(-config.pollen_discount*a)
        removed = export_scale*(-np.expm1(-rate*u))
        removed_prime = export_scale*rate*np.exp(-rate*u)
        match = u[...,None]*g/(u[...,None]*g+config.background_ratio)
        receipt = removed*np.sum(channels*visitors.effectiveness*match,axis=-1)
        q = -np.expm1(-receipt/(2*config.pollen_scale))
        # Only mutant recipient affinity changes: resident pollen and denominator fixed.
        dq = np.exp(-receipt/(2*config.pollen_scale))*receipt/(u*2*config.pollen_scale)
        export_elasticity = np.divide(removed_prime,removed,out=np.zeros_like(i),where=removed>0)
    prior = config.assurance_timing == "prior"
    available = ov*(1-a) if prior else ov
    female = available*q
    selfed = (ov*a if prior else a*(ov-female))*(1-config.depression)
    fitness = female+selfed  # paternal equals female at mutant=resident
    if (fitness<=0).any() or not np.isfinite(fitness).all():
        raise ArithmeticError("nonpositive invasion fitness")
    female_benefit = available*dq
    self_benefit = np.zeros_like(i) if prior else -a*(1-config.depression)*female_benefit
    paternal_benefit = female*export_elasticity
    benefit = (.5*female_benefit+.5*paternal_benefit+self_benefit)/fitness
    # Mutant ovule costs affect its female/selfed production, not resident mothers.
    cost = 2*config.investment_cost*i*(.5*female+selfed)/fitness
    return dict(gradient=benefit-cost,benefit=benefit,cost=cost,fitness=fitness,
                outcross_fraction=q, female=female, selfed=selfed, ovules=ov)


def syndrome_thresholds(resident, visitors, config):
    """Local interior rare-mutant conditions; not an equilibrium or G-beta result.

    At fixed resident state, q does not depend on ovule cost coefficients.
    Hence beta_i < 0 iff c_i > c_i_star, and beta_a > 0 iff c_a < c_a_star.
    Thresholds may be negative; do not clip them to biologically valid costs.
    Trait-boundary cases require one-sided feasible directions instead.
    """
    z = np.asarray(resident, dtype=float)
    terms = investment_invasion_terms(z, visitors, config)
    i, a = z[..., 1], z[..., 2]
    if ((i <= 0) | (i >= 1) | (a <= 0) | (a >= 1)).any():
        raise ValueError('joint thresholds require interior investment and assurance')
    q = terms['outcross_fraction']
    v = 1-config.depression
    prior = config.assurance_timing == 'prior'
    f = (1-a)*q if prior else q
    l = np.ones_like(q) if prior else 1-q
    s = a*v*l
    maternal_weight = .5*f+s
    if (maternal_weight <= 0).any():
        raise ArithmeticError('zero marginal ovule contribution')
    a_benefit = v*l - (.5*q if prior else 0) - .5*config.pollen_discount*f
    a_cost_slope = 2*a*maternal_weight
    a_gradient = (a_benefit-config.assurance_cost*a_cost_slope)/(f+s)
    i_cost_slope = 2*i*maternal_weight/(f+s)
    i_threshold = terms['benefit']/i_cost_slope
    a_threshold = a_benefit/a_cost_slope
    return dict(investment_gradient=terms['gradient'], assurance_gradient=a_gradient,
                investment_cost_threshold=i_threshold, assurance_cost_threshold=a_threshold,
                local_syndrome_direction=(terms['gradient']<0)&(a_gradient>0))
