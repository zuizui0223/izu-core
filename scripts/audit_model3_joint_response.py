"""Frozen multivariate G-beta response audit for Model 3.

The exact one-generation response is obtained from the genotype-density
operator and is identical to the multivariate Price covariance response under
mutation=0, immigration=0 and survival=0.

A local Lande-style approximation is then formed as

    Delta z_L = G beta,

for z=(investment, assurance), retaining the observed off-diagonal G_ia.
A diagonalized-G control measures the information lost by discarding trait
covariance.

Design:
data/design/model3_joint_syndrome_response_20261004.json
"""
from __future__ import annotations

from dataclasses import replace
import json
from pathlib import Path

import numpy as np

from scripts.audit_model3_joint_syndrome_vector import invasion_gradient
from scripts.model3_island.density import density_step, make_grid, project_state
from scripts.model3_island.run import founders_from_spec
from scripts.model3_island.types import Config, PlantState, VisitorState

ROOT=Path(__file__).resolve().parents[1]
BRIDGE=ROOT/"data/design/model3_ch2_bridge_20260927.json"
JOINT=ROOT/"data/design/model3_joint_syndrome_rare_mutant_20261004.json"
DESIGN=ROOT/"data/design/model3_joint_syndrome_response_20261004.json"


def _empty():
    return PlantState(
        alleles=np.empty((0,3,2),float),
        allele_origin=np.empty((0,3,2),np.int64),
        mutation_flags=np.empty((0,3,2),bool),
        ids=np.empty(0,np.int64),
        birth_years=np.empty(0,np.int64),
    )


def _visitor(optima, config):
    optima=np.asarray(optima,float)
    n=len(optima)
    return VisitorState(
        ids=np.arange(1000,1000+n,dtype=np.int64),
        optima=optima,
        breadths=np.full(n,config.visitor_breadth),
        effectiveness=np.full(n,config.visitor_effectiveness),
    )


def _settings(base, joint):
    return {
        name:replace(
            base,
            assurance_mode="evolving",
            assurance_timing=patch["assurance_timing"],
            pollen_discount=float(patch["pollen_discount"]),
            assurance_cost=float(patch["assurance_cost"]),
        )
        for name,patch in joint["settings"].items()
    }


def _weighted_mean_cov(values, counts):
    p=counts/counts.sum()
    mean=p@values
    centered=values-mean
    cov=(centered.T*p)@centered
    return mean,cov


def _cosine(a,b):
    na=float(np.linalg.norm(a)); nb=float(np.linalg.norm(b))
    if na==0 or nb==0:
        return 1.0 if na==nb==0 else 0.0
    return float(a@b/(na*nb))


def run_audit():
    bridge=json.loads(BRIDGE.read_text())
    joint=json.loads(JOINT.read_text())
    design=json.loads(DESIGN.read_text())
    base=Config.from_dict(bridge["base_config"])
    settings=_settings(base,joint)
    h=float(joint["invasion_fitness"]["finite_difference_step"])
    grid=make_grid(tuple(design["grid_axes"]))
    trait_all=grid.genotypes.mean(axis=2)
    ia=trait_all[:,1:3]

    rows=[]
    for state in design["founder_states"]:
        means=[float(design["access"]),float(state["investment"]),float(state["assurance"])]
        founders=founders_from_spec(
            {
                "count":int(design["founder_count"]),
                "draw_count":int(design["founder_count"]),
                "means":means,
                "sd":float(design["founder_sd"]),
                "birth_year":0,
            },
            bridge["founder_seed"],
        )
        _,counts=project_state(founders,grid)
        current,G=_weighted_mean_cov(ia,counts)
        sd=np.sqrt(np.diag(G))

        for setting_name,config in settings.items():
            if config.mutation_rate!=0 or config.survival!=0 or config.seed_arrival.supply!=0:
                raise ValueError("Price identity boundary changed")
            for community,optima in design["communities"].items():
                visitors=_visitor(optima,config)
                next_counts,_=density_step(
                    counts,grid,visitors,_empty(),config,immigration_mode="source"
                )
                nxt=next_counts@ia/next_counts.sum()
                exact=nxt-current

                resident=(float(design["access"]),float(current[0]),float(current[1]))
                beta=np.array([
                    invasion_gradient(resident,visitors,config,trait_index=1,step=h),
                    invasion_gradient(resident,visitors,config,trait_index=2,step=h),
                ])
                lande=G@beta
                Gdiag=np.diag(np.diag(G))
                lande_diag=Gdiag@beta

                sign_match=bool(np.all(
                    (np.sign(lande)==np.sign(exact))
                    | (np.abs(exact)<1e-14)
                ))
                cos=_cosine(exact,lande)
                cos_diag=_cosine(exact,lande_diag)
                standardized=np.divide(
                    exact,sd,out=np.zeros_like(exact),where=sd>0
                )
                rows.append({
                    "founder_state":dict(state),
                    "setting":setting_name,
                    "community":community,
                    "current_mean":current.tolist(),
                    "G":G.tolist(),
                    "G_ia":float(G[0,1]),
                    "beta":beta.tolist(),
                    "exact_price_response":exact.tolist(),
                    "standardized_exact_response":standardized.tolist(),
                    "lande_full_G":lande.tolist(),
                    "lande_diagonal_G":lande_diag.tolist(),
                    "cosine_full_G":cos,
                    "cosine_diagonal_G":cos_diag,
                    "component_sign_match_full_G":sign_match,
                    "full_G_improves_cosine":bool(cos>cos_diag+1e-12),
                })

    gate=design["gates"]
    passed=[
        r for r in rows
        if r["cosine_full_G"]>=float(gate["cosine_similarity"])
        and r["component_sign_match_full_G"]
    ]
    nonzero_offdiag=[r for r in rows if abs(r["G_ia"])>1e-12]
    return {
        "status":"complete_frozen_multivariate_G_beta_audit",
        "cells":len(rows),
        "local_fidelity_pass_cells":len(passed),
        "local_fidelity_fraction":len(passed)/len(rows),
        "nonzero_offdiagonal_cells":len(nonzero_offdiag),
        "full_G_improves_cosine_cells":sum(r["full_G_improves_cosine"] for r in rows),
        "mean_cosine_full_G":float(np.mean([r["cosine_full_G"] for r in rows])),
        "mean_cosine_diagonal_G":float(np.mean([r["cosine_diagonal_G"] for r in rows])),
        "rows":rows,
        "claim_boundary":[
            "exact Price response is the one-generation identity; G beta is only a local approximation",
            "beta is rare-mutant invasion selection at the current mean phenotype",
            "G includes the observed investment-assurance covariance and is never assumed diagonal",
            "fixed delta; no purging feedback",
        ],
    }


if __name__=="__main__":
    print(json.dumps(run_audit(),indent=2,sort_keys=True))
