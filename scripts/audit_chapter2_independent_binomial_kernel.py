"""Independent ONE-LOCUS diploid ovule-binomial mating/demographic model.

NOT the original Model3 biology, a fit to data, or an independent island.
One annual cohort: each mother tries TWO ovules, with prior/delayed selfing
and pollen-limited fertilization. All viable seeds are independently
Mendelian and a uniform cap-lottery retains <=K. No Poisson recruitment.
The founder genome is constant across demographic histories.

The intentionally constructed analytical sign reversal of individual genetic
W and collective viable-seed output is KNOWN selfing theory, not novel.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
from scipy.stats import beta as beta_distribution

ROOT=Path(__file__).resolve().parents[1]
DESIGN=ROOT/"data/design/chapter2_alternative_binomial_kernel_20261010.json"
STATUS="INDEPENDENT_DIPLOID_BINOMIAL_MODEL_INTERNAL_SIGN_BOUNDARY_TEST"
TIMINGS=("prior","delayed")
POLLEN=(0.8,0.4)
CAPS=(8,48)
MODES=("heritable","frozen_expression")
YEARS=80
REPS=128


def load_contract():
    raw=DESIGN.read_bytes()
    d=json.loads(raw)
    if (d.get("status")!="ALTERNATIVE_KERNEL_INPUT_LOCK_BEFORE_RESULTS"
            or d["constants"]!={"ovules_per_plant":2,
                                 "ovule_maturation":0.9,
                                 "selfed_seed_viability":0.6,
                                 "allee_parameter":1.0}
            or d["grid"]["K"]!=[8,48]
            or d["grid"]["pollen_supply"]!=[.8,.4]
            or d["grid"]["timing"]!=list(TIMINGS)
            or d["grid"]["expression_modes"]!=list(MODES)
            or d["grid"]["n_paths"]!=2048
            or d["grid"]["generations"]!=80
            or d["grid"]["independent_demographic_repeats"]!=128
            or d["grid"]["seed_first"]!=61031001
            or d["grid"]["seed_last"]!=61031128):
        raise ValueError("alternative kernel frozen design mismatch")
    return d,hashlib.sha256(raw).hexdigest()


def effective_pollen(n,q,allee=1.0):
    if (type(n) is not int or n<0 or not 0<=q<=1 or allee<0):
        raise ValueError("invalid density or pollen pressure")
    return 0.0 if n<=1 else float(q*(n-1)/(n-1+allee))


def per_ovule_fates(a,n,q,timing,phi=.9,v=.6,allee=1.):
    if (not 0<=a<=1 or timing not in TIMINGS or not 0<=phi<=1
            or not 0<=v<=1):
        raise ValueError("invalid selfing state")
    qeff=effective_pollen(n,q,allee)
    if timing=="prior":
        ps=phi*a*v
        po=phi*(1-a)*qeff
    else:
        po=phi*qeff
        ps=phi*(1-qeff)*a*v
    pf=1-ps-po
    if min(ps,po,pf)<-1e-12:
        raise AssertionError("overallocated finite maternal ovules")
    return np.array([ps,po,pf],dtype=float)


def analytical_gradient(n,q,timing,phi=.9,v=.6,allee=1.):
    qeff=effective_pollen(n,q,allee)
    # Rare-mutant focal expression: paternal paternity from OTHER mothers is
    # constant with focal a because no pollen discounting is included.
    # W = 0.5 * maternal outcross + 0.5 * paternal outcross + viable self
    if timing=="prior":
        beta=2*phi*(v-.5*qeff)
        gamma=2*phi*(v-qeff)
        father_slope=0.
        mother_slope=-phi*qeff
        self_slope=2*phi*v
    elif timing=="delayed":
        beta=gamma=2*phi*(1-qeff)*v
        father_slope=0.
        mother_slope=0.
        self_slope=2*phi*(1-qeff)*v
    else:
        raise ValueError("invalid timing")
    if not np.isclose(beta,mother_slope+father_slope+self_slope,
                      atol=1e-12,rtol=0):
        raise AssertionError("independent F/P/S derivative accounting false")
    return {
        "n":n,"q":q,"timing":timing,
        "q_effective":qeff,
        "beta_F":mother_slope,"beta_P":father_slope,"beta_S":self_slope,
        "beta_W_local":beta,"gamma_viable_seeds_group":gamma,
        "individual_favored_group_harmed":bool(beta>1e-12 and gamma< -1e-12),
        "aligned_positive":bool(beta>1e-12 and gamma>1e-12),
    }


def _one_update(genotypes,*,K,q,timing,mode,frozen_a,rng,phi,v,allee):
    n=len(genotypes)
    if n==0:return genotypes.copy()
    if len(genotypes.shape)!=2 or genotypes.shape[1]!=2:
        raise ValueError("diploid alleles must have 2 homologs")
    child=[]
    for mother in range(n):
        expressed=(float(genotypes[mother].mean())
                   if mode=="heritable" else frozen_a)
        ps,po,pf=per_ovule_fates(expressed,n,q,timing,phi,v,allee)
        counts=rng.multinomial(2,[ps,po,pf])
        for _ in range(int(counts[0])):
            maternal=rng.integers(0,2,size=2)
            child.append([int(genotypes[mother,maternal[0]]),
                          int(genotypes[mother,maternal[1]])])
        for _ in range(int(counts[1])):
            if n<=1:
                raise AssertionError("outcross with zero possible father")
            # Uniform outcross father (no pollen discounting).
            father=rng.integers(0,n-1)
            if father>=mother:
                father+=1
            mi=int(rng.integers(0,2));fi=int(rng.integers(0,2))
            child.append([int(genotypes[mother,mi]),
                          int(genotypes[father,fi])])
    children=np.array(child,dtype=np.int8).reshape(-1,2)
    if len(children)>K:
        children=children[rng.choice(len(children),size=K,replace=False)]
    return children


def simulate_one(d,seed,K,q,timing,mode):
    if (type(seed) is not int or not 61031001<=seed<=61031128
            or K not in CAPS or q not in POLLEN or timing not in TIMINGS
            or mode not in MODES):
        raise ValueError("only frozen demographic history arms")
    cfg=d["constants"]
    initial=np.asarray(d["grid"]["founder_alleles"],dtype=np.int8)
    if initial.shape!=(8,2) or not np.isin(initial,[0,1]).all():
        raise AssertionError("not the declared source diploid founder panel")
    founder_mean=float(initial.mean())
    # This seed includes q/timing/K to isolate independent comparison cells.
    # Importantly, it is SAME for heritable and frozen_expression modes.
    key=[seed,1 if timing=="prior" else 2,
         1 if q==.8 else 2,1 if K==8 else 2]
    rng=np.random.default_rng(np.random.SeedSequence(key))
    s=initial
    n20=None
    allele_at20=None
    first_extinction=None
    for t in range(1,YEARS+1):
        s=_one_update(
            s,K=K,q=q,timing=timing,mode=mode,frozen_a=founder_mean,rng=rng,
            phi=cfg["ovule_maturation"],
            v=cfg["selfed_seed_viability"],
            allee=cfg["allee_parameter"])
        if len(s)==0 and first_extinction is None:
            first_extinction=t
        if t==20:
            n20=len(s);allele_at20=(float(s.mean()) if len(s) else None)
    return {"seed":seed,"K":K,"q":q,"timing":timing,"expression_mode":mode,
            "N20":n20,"N80":len(s),
            "occupied20":int(n20>0),"occupied80":int(len(s)>0),
            "allele_mean20_given_occupied":allele_at20,
            "allele_mean80_given_occupied":float(s.mean()) if len(s) else None,
            "allele_copies80_unconditional":int(s.sum()) if len(s) else 0,
            "first_extinction":first_extinction}


def exact_paired_interval(positive,negative,n):
    if (type(positive) is not int or type(negative) is not int or
            type(n) is not int or n<1 or min(positive,negative)<0
            or positive+negative>n):
        raise ValueError("invalid paired outcomes")
    # Bonferroni across TWO mutually exclusive discordance proportions.
    def one(k):
        alpha=.025
        lo=0. if k==0 else float(beta_distribution.ppf(alpha/2,k,n-k+1))
        hi=1. if k==n else float(beta_distribution.ppf(1-alpha/2,k+1,n-k))
        return lo,hi
    pl,pu=one(positive)
    nl,nu=one(negative)
    return [pl-nu,pu-nl]


def classify_ci(ci,rope=.05):
    if ci[0]>rope:return "positive"
    if ci[1]<-rope:return "negative"
    if ci[0]>=-rope and ci[1]<=rope:return "practically_equivalent"
    return "inconclusive"


def run_all():
    d,digest=load_contract()
    raw=[]
    for timing in TIMINGS:
        for q in POLLEN:
            for K in CAPS:
                for seed in range(61031001,61031129):
                    for mode in MODES:
                        raw.append(simulate_one(d,seed,K,q,timing,mode))
    if len(raw)!=2048:
        raise AssertionError("incomplete declared alternate model")
    lookup={(x["timing"],x["q"],x["K"],x["seed"],x["expression_mode"]):x
            for x in raw}
    summaries=[]
    for timing in TIMINGS:
        for q in POLLEN:
            for K in CAPS:
                sub={}
                for h in (20,80):
                    a=np.array([
                        lookup[(timing,q,K,s,"heritable")][f"occupied{h}"]
                        for s in range(61031001,61031129)],dtype=int)
                    b=np.array([
                        lookup[(timing,q,K,s,"frozen_expression")][f"occupied{h}"]
                        for s in range(61031001,61031129)],dtype=int)
                    po=int(np.sum((a==1)&(b==0)))
                    ne=int(np.sum((a==0)&(b==1)))
                    ci=exact_paired_interval(po,ne,128)
                    sub[str(h)]={
                        "heritable_occupied":int(a.sum()),
                        "frozen_expression_occupied":int(b.sum()),
                        "heritable_only":po,"frozen_only":ne,
                        "delta":(po-ne)/128,
                        "paired_exact_95":ci,"verdict":classify_ci(ci)}
                genetically_alive=[
                    lookup[(timing,q,K,s,"heritable")]
                    for s in range(61031001,61031129)
                    if lookup[(timing,q,K,s,"heritable")]["occupied80"]]
                summaries.append({
                    "timing":timing,"q":q,"K":K,
                    "N8_beta_gamma":analytical_gradient(8,q,timing),
                    "N48_beta_gamma":analytical_gradient(48,q,timing),
                    "occupancy":sub,
                    "allele_mean80_among_heritable_survivors":(
                        float(np.mean([x["allele_mean80_given_occupied"]
                                      for x in genetically_alive]))
                        if genetically_alive else None),
                    "n_heritable_survivors_allele_summary":len(genetically_alive),
                })
    all_gradients=[analytical_gradient(n,q,timing)
                   for timing in TIMINGS for q in POLLEN
                   for n in range(1,49)]
    return {
        "status":STATUS,
        "design_sha256":digest,
        "model_count":1,"distinct_from_Model3":True,
        "demographic_repeats_per_setting":128,
        "n_independent_natural_island_systems":0,
        "all_2048_paths":raw,
        "all_eight_setting_summaries":summaries,
        "analytic_beta_gamma_at_every_N_q_timing":all_gradients,
        "scope":[
            "This is an independently written ONE-locus diploid ovule-binomial kernel with uniform density cap, not an empirical fit or direct reproduction of Model3 three-locus visitor/pollen model.",
            "Genetically inherited a is selfing propensity; expression-frozen genotype control retains diploid inheritance and genetic drift, but removes genotype/phenotype coupling.",
            "An analytic invasion-vs-group seed-sign reversal is imposed by the frozen v between qeff/2 and qeff at high density; established selfing automatic advantage is known theory, not new discovery.",
            "Extinction hazard also depends on population size, pollen mate limitation, K and first-year genotype heterogeneity; a negative group seed gradient is NOT a guarantee of evolutionary suicide.",
            "All 128 demographic RNG seeds per setting belong to one model, not ecologically independent islands; strict full single-model confirmation is out of scope.",
        ],
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out",type=Path,required=True)
    a=p.parse_args()
    result=run_all()
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+"\n")
    print(json.dumps({
        "status":result["status"],"n_paths":len(result["all_2048_paths"]),
        "summary":result["all_eight_setting_summaries"]
    },sort_keys=True))


if __name__=="__main__":
    main()
