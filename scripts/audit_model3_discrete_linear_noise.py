"""Discrete-generation finite-genotype CLT / linear-noise error screen.

This compares the *exact* conditional finite-offspring distribution of a
floral-investment mean against a normal fluctuation approximation, at fixed
numbers of recruited offspring N. It is NOT a time-continuous Ito SDE and
does not replace the three-locus Mendelian state in Model 3.

For a finite support law q of child diploid genotypes, conditional on N=n>0
the N offspring are independent draws from q under the restricted Model3
recruitment rule. This makes a transparent, auditable one-step CLT diagnostic.
A distinct test of rarity/extinction is required before using any Gaussian
surrogate in full stochastic dynamics.
"""
from __future__ import annotations

from dataclasses import replace
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
from scipy.stats import norm

from scripts.audit_model3_stochastic_bridge import (
    parent_pair_probabilities, offspring_genotype_distribution,
)
from scripts.model3_island.density import make_grid
from scripts.model3_island.reproduction import reproduce
from scripts.model3_island.types import Config, PlantState, VisitorState

# A conservative general Berry--Esseen constant for independent finite-variance
# draws. This bounds the Kolmogorov distance of the standardized sample mean.
BERRY_ESSEEN_C = 0.56
OBSERVED_N = (8, 16, 32, 64, 128)


def restricted_reference_support() -> tuple[np.ndarray, np.ndarray]:
    """Source Model3 mating mechanism on a fixed two-allele/three-locus support.

    These four synthetic diploid founders and two visitors are an *engineering
    assay*, not observed island plants or independent ecological histories.
    No numerical projection or modification of biological mating rules occurs.
    """
    raw = json.loads(Path("data/design/model3_ch2_bridge_20260927.json").read_text())
    base=Config.from_dict(raw["base_config"])
    config=replace(
        base, capacity=8, survival=0., mutation_rate=0.,
        ovule_budget=4., assurance_mode="evolving",
        seed_arrival=replace(base.seed_arrival,supply=0.),
    )
    genotype_alleles=np.array([
        [[.25,.75],[.25,.25],[.75,.75]],
        [[.75,.75],[.25,.75],[.25,.25]],
        [[.25,.25],[.75,.75],[.25,.75]],
        [[.25,.75],[.75,.25],[.25,.75]],
    ],dtype=float)
    state=PlantState(
        genotype_alleles,np.zeros((4,3,2),dtype=np.int64),
        np.zeros((4,3,2),dtype=bool),np.arange(4,dtype=np.int64),
        np.zeros(4,dtype=np.int64),
    )
    visitors=VisitorState(
        np.array([1,2],dtype=np.int64),
        np.array([.25,.75]),np.array([.2,.2]),np.array([.8,.8]),
    )
    grid=make_grid(([.25,.75],)*3)
    w,_=parent_pair_probabilities(state,reproduce(state,visitors,config),config)
    child_genotype_prob=offspring_genotype_distribution(state,w,grid)
    investment=grid.genotypes.mean(axis=2)[:,1]
    values=np.array([.25,.50,.75])
    p=np.array([child_genotype_prob[np.isclose(investment,z,atol=1e-12)].sum()
                for z in values])
    if not np.isclose(p.sum(),1,atol=1e-12) or (p<=0).any():
        raise AssertionError("fixed offspring investment support is not nondegenerate")
    return values,p


def finite_offspring_mean_clt(values:np.ndarray, probabilities:np.ndarray,
                             sizes=OBSERVED_N) -> dict:
    """Exact n-convolution versus Gaussian CLT with certified upper bound.

    This implementation intentionally supports exactly the three equally
    spaced offspring-investment phenotypes [0.25, 0.5, 0.75], so the
    convolution has exact bins. It never rounds continuous allele values.
    """
    values=np.asarray(values,dtype=float)
    p=np.asarray(probabilities,dtype=float)
    sizes=tuple(sizes)
    if (values.shape!=(3,) or not np.allclose(values,[.25,.5,.75],
                                             rtol=0,atol=1e-12)
            or p.shape!=(3,) or (p<0).any()
            or not np.isfinite(p).all()
            or not np.isclose(p.sum(),1,atol=1e-12,rtol=0)
            or not sizes or any(type(n) is not int or n<1 for n in sizes)
            or len(set(sizes))!=len(sizes)):
        raise ValueError("nondegenerate three-value child law and positive distinct N required")
    mu=float(p @ values)
    variance=float(p @ ((values-mu)**2))
    if variance<=1e-15:
        raise ValueError("constant child phenotype has no CLT variance")
    rho=float(p @ (np.abs(values-mu)**3))
    scale=rho / variance**1.5
    exact_sum_pmf=np.array([1.])
    previous=0
    rows=[]
    for n in sorted(sizes):
        for _ in range(n-previous):
            exact_sum_pmf=np.convolve(exact_sum_pmf,p)
        previous=n
        exact_sum_pmf=np.maximum(exact_sum_pmf,0)
        exact_sum_pmf=exact_sum_pmf/exact_sum_pmf.sum()
        # Child phenotype Y=0.25+0.25*Z where Z in {0,1,2}
        attainable_means=.25+.25*np.arange(2*n+1)/n
        normal_cdf=norm.cdf(
            (attainable_means-mu)/np.sqrt(variance/n)
        )
        exact_right=np.cumsum(exact_sum_pmf)
        exact_left=exact_right-exact_sum_pmf
        kolmogorov=float(max(
            np.max(np.abs(exact_right-normal_cdf)),
            np.max(np.abs(exact_left-normal_cdf)),
        ))
        bound=float(min(1.,BERRY_ESSEEN_C*scale/np.sqrt(n)))
        if kolmogorov>bound+1e-11:
            raise AssertionError("discrete exact/normal CDF violates Berry-Esseen bound")
        rows.append({
            "N":n,
            "mean":mu,
            "sample_mean_variance":variance/n,
            "normal_approximation_sample_mean_sd":np.sqrt(variance/n),
            "exact_gaussian_kolmogorov_distance":kolmogorov,
            "berry_esseen_bound":bound,
            "standardized_third_absolute_moment":scale,
            "finite_diploid_frequency_zeros_represented_by_gaussian":False,
        })
    return {
        "status":"EXACT_DISCRETE_GENERATION_CLT_DIAGNOSTIC",
        "n_independent_visitor_histories":0,
        "source":"canonical_Model3_mating_kernel_with_engineering_fixed_diploid_support",
        "child_investment_support":values.tolist(),
        "child_investment_probabilities":p.tolist(),
        "child_trait_mean":mu,
        "child_trait_variance":variance,
        "berry_esseen_conservative_constant":BERRY_ESSEEN_C,
        "rows":rows,
        "conditional_offspring_census_fixed_not_new_plant_capacity":True,
        "temporal_SDE_or_SPDE_validated":False,
        "rare_allele_loss_or_whole_population_extinction_validated":False,
        "model3_source_modified":False,
        "geographic_INLA_performed":False,
    }


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out",type=Path,required=True)
    args=parser.parse_args()
    vals,p=restricted_reference_support()
    result=finite_offspring_mean_clt(vals,p)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(result,sort_keys=True,indent=2,
                                   allow_nan=False)+"\n",encoding="utf-8")
    print(json.dumps({
        "status":result["status"],
        "probabilities":result["child_investment_probabilities"],
        "kolmogorov_by_N":{r["N"]:r["exact_gaussian_kolmogorov_distance"]
                            for r in result["rows"]},
        "berry_esseen_bounds":{r["N"]:r["berry_esseen_bound"]
                                for r in result["rows"]},
    }))


if __name__=="__main__":
    main()
