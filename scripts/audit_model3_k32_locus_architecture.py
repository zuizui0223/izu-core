"""Locus-specific allele loss, multilocus association, and concentration.

This pure finite-genotype diagnostic is called by the K32 eight-arm
factorial study on unchanged original Model3 and deliberately altered
outcross-mating operators. No mutation, immigration, or natural data.

Three biallelic diploid loci in order:
  pollinator_matching / floral_investment / reproductive_assurance.
The (27,3) dosage basis has values {0,.5,1}, not phased gametes.

Pairwise dosage covariance and mutual information describe correlations
between *individual diploid genotypes* within a small finite population.
They are NOT phased gametic linkage disequilibrium, genomic linkage,
proof of linkage disequilibrium selection, or causal effects.
"""
from __future__ import annotations

import numpy as np

LOCI=("pollinator_matching","floral_investment","reproductive_assurance")
PAIRS=((0,1),(0,2),(1,2))
PAIR_NAMES=("matching_investment","matching_assurance","investment_assurance")


def architecture_snapshot(counts, dosage_basis):
    """Loss/fixation and unphased multilocus associations in a living census.

    Extinction has undefined allele frequencies and associations: return
    None; callers may construct occupancy-weighted PRODUCTS separately.
    """
    c=np.asarray(counts)
    b=np.asarray(dosage_basis,float)
    if (c.ndim!=1 or c.dtype.kind not in "iu" or np.any(c<0)
            or b.shape!=(len(c),3)
            or not np.isfinite(b).all()
            or not np.isin(b,[0.,.5,1.]).all()):
        raise ValueError("complete joint diploid genotype census required")
    n=int(c.sum())
    if n==0:
        return None
    probabilities=c/n
    mu=probabilities@b
    centered=b-mu
    covariance=(centered.T*probabilities)@centered
    covariance=.5*(covariance+covariance.T)
    if np.any(np.diag(covariance)<-1e-12):
        raise ArithmeticError("negative allelic dosage variance")
    high_lost=mu<=1e-12
    low_lost=mu>=1.-1e-12
    if np.any(high_lost&low_lost):
        raise ArithmeticError("both alleles cannot disappear from a living locus")
    heterozygosity=probabilities@(b==.5)
    # label each locus with H: high fixed, L: low fixed, P: polymorphic.
    pattern="".join("H" if low_lost[k] else "L" if high_lost[k]
                    else "P" for k in range(3))
    category=np.rint(2*b).astype(int)
    mi=[]
    for k,l in PAIRS:
        joint=np.zeros((3,3),float)
        np.add.at(joint,(category[:,k],category[:,l]),probabilities)
        marginal_k=joint.sum(axis=1)
        marginal_l=joint.sum(axis=0)
        independent=np.outer(marginal_k,marginal_l)
        positive=joint>0
        mutual_info=float(np.sum(joint[positive]*
                         np.log(joint[positive]/independent[positive])))
        if mutual_info < -1e-12:
            raise ArithmeticError("negative mutual information")
        mi.append(max(0.,mutual_info))
    nonzero=probabilities[probabilities>0]
    largest=float(np.max(nonzero))
    largest_class=int(np.argmax(c))
    genotype_label="".join(
        ("L","H","U")[int(x)] for x in category[largest_class]
    )  # L=low homozygote,H=heterozygote,U=high homozygote
    return {
        "high_allele_frequencies":mu.tolist(),
        "high_allele_lost":high_lost.astype(int).tolist(),
        "low_allele_lost":low_lost.astype(int).tolist(),
        "within_locus_heterozygosity":heterozygosity.tolist(),
        "dosage_pairwise_covariance":[float(covariance[k,l]) for k,l in PAIRS],
        "dosage_pairwise_mutual_info_nats":mi,
        "fixed_allele_pattern":pattern,
        "largest_genotype_frequency":largest,
        "largest_genotype_class_index":largest_class,
        "largest_genotype_class_dosage_label":genotype_label,
    }


def architecture_vector(counts,basis):
    """Finite per-population summary vector, 0 only for occupancy-products."""
    r=architecture_snapshot(counts,basis)
    if r is None:
        return np.zeros(3*4+3*2+1,float)
    return np.asarray(
        r["high_allele_frequencies"]+
        r["high_allele_lost"]+
        r["low_allele_lost"]+
        r["within_locus_heterozygosity"]+
        r["dosage_pairwise_covariance"]+
        r["dosage_pairwise_mutual_info_nats"]+
        [r["largest_genotype_frequency"]],float
    )


VECTOR_LABELS=tuple(
    prefix+"_"+locus+suffix
    for prefix,suffix in (
        ("locus","_high_frequency_occ_weighted"),
        ("locus","_high_allele_lost_occ_weighted"),
        ("locus","_low_allele_lost_occ_weighted"),
        ("locus","_heterozygosity_occ_weighted"),
    ) for locus in LOCI
)+tuple(
    "dosage_covariance_"+name+"_occ_weighted" for name in PAIR_NAMES
)+tuple(
    "dosage_mutual_info_"+name+"_occ_weighted" for name in PAIR_NAMES
)+("largest_genotype_frequency_occ_weighted",)

if len(VECTOR_LABELS)!=19:
    raise AssertionError("unexpected three-locus association metric length")


def pattern_frequencies(count_matrix,basis):
    """Conditioned-on-living empirical distribution of 3-locus loss states."""
    counts=np.asarray(count_matrix)
    if counts.ndim!=2 or counts.shape[1]!=len(basis) or counts.dtype.kind not in "iu":
        raise ValueError("integer source path ensemble required")
    patterns={}
    largest={}
    alive=0
    for row in counts:
        s=architecture_snapshot(row,basis)
        if s is None:
            continue
        alive+=1
        p=s["fixed_allele_pattern"]
        patterns[p]=patterns.get(p,0)+1
        label=s["largest_genotype_class_dosage_label"]
        largest[label]=largest.get(label,0)+1
    return {
        "n_living":alive,
        "n_extinct":len(counts)-alive,
        "fixed_allele_pattern_counts":dict(sorted(patterns.items())),
        "dominant_genotype_dosage_label_counts":dict(sorted(largest.items())),
        "pattern_key":"P=both alleles retained,H=high allele fixed (low lost),L=low allele fixed (high lost)",
        "dominant_dosage_key":"Three characters ordered matching/investment/assurance, L=low homozygote,H=heterozygote,U=high homozygote",
    }
