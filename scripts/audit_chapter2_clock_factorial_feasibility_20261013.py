"""Read-only archived t0-genotype factorial-geometry audit.

No Model3 reproduction/advance, synthetic ecological history or simulated
phenotypic response is permitted here. Inputs are the *original* GitHub Actions
provider shard 0 with two founders and 128 stored histories per founder.
"""
from __future__ import annotations
import argparse
import hashlib
import io
import json
from pathlib import Path
import zipfile

import numpy as np

SOURCE_SHARD0_SHA256 = "5b850eaad6104f572f56df2a37da00fbc8473503a827703c82f6870a87e9a881"
FOUNDER_BLOCKS = ("main", "confirmation")
A_HALF_WIDTHS = (0.046875, 0.078125)
I_ALLELE_SCALE = (0.5, 1.0)
A_FOUNDER_CENTER = 0.5
RESPONSE_THRESHOLD = 0.05
EXPECTED_FOUNDER_IDS = 48


def original_state(shard: zipfile.ZipFile, block: str) -> tuple[np.ndarray, dict]:
    name = f"{block}_c0_r0.npz"
    with np.load(io.BytesIO(shard.read(name)), allow_pickle=False) as d:
        if set(("alleles", "ids", "offsets", "metadata")) - set(d.files):
            raise ValueError("source archive lacks required founding-state fields")
        data = d["alleles"]
        offsets = d["offsets"]
        n = int(offsets[1] - offsets[0])
        if n != EXPECTED_FOUNDER_IDS or int(offsets[0]) != 0:
            raise ValueError("original first-census admission failed")
        initial = np.asarray(data[:n], dtype=np.float64)
        ids = np.asarray(d["ids"][:n])
        metadata = json.loads(str(d["metadata"].item()))
        if initial.shape != (n, 3, 2) or len(set(map(int, ids))) != n:
            raise ValueError("original founding genotype dimensions and identifiers")
        if not np.isfinite(initial).all() or initial.min() < 0 or initial.max() > 1:
            raise ValueError("invalid original allele bounds")
        if not np.array_equal(initial[:, 2, :], np.tile([0.4375, 0.5625], (n, 1))):
            raise ValueError("source A locus not the frozen 0.0625-width heterozygote")
        task = metadata.get("task", {})
        if task.get("block") != block or task.get("replicate") != 0 or task.get("context") != 0:
            raise ValueError("unexpected original task labels")
        config = metadata.get("config", {})
        if (config.get("capacity"), config.get("mutation_rate"), config.get("mutation_sd")) != (48, 0.01, 0.05):
            raise ValueError("original model configuration mismatch")
        return initial, {"source_case": name, "source_task": task, "original_config_sha256": hashlib.sha256(json.dumps(config, sort_keys=True, separators=(",", ":")).encode()).hexdigest()}


def transform(initial: np.ndarray, width: float, i_scale: float) -> tuple[np.ndarray, dict]:
    """Transform only A and I allele values, preserving means and genetic M."""
    initial = np.asarray(initial)
    if initial.shape != (48, 3, 2) or (width not in A_HALF_WIDTHS) or (i_scale not in I_ALLELE_SCALE):
        raise ValueError("unregistered initial transform")
    old = initial[:, 1, :]
    mean = float(old.mean())
    new = initial.copy()
    new[:, 1, :] = mean + i_scale * (old - mean)
    new[:, 2, :] = np.array([A_FOUNDER_CENTER - width, A_FOUNDER_CENTER + width])
    if not np.array_equal(new[:, 0, :], initial[:, 0, :]):
        raise ValueError("matching alleles changed")
    if not np.isclose(new[:, 1, :].mean(), mean, rtol=0, atol=1e-14):
        raise ValueError("I founding mean changed")
    if not np.array_equal(new[:, 2, :], np.tile([.5 - width, .5 + width], (48, 1))):
        raise ValueError("A founding heterozygosity changed")
    if new.min() < 0 or new.max() > 1 or not np.isfinite(new).all():
        raise ValueError("transformed alleles violate bounded source scale")
    i_copy_var = float(new[:, 1, :].var() / 2)
    original_var = float(initial[:, 1, :].var() / 2)
    if not np.isclose(i_copy_var, original_var * i_scale * i_scale, atol=1e-15, rtol=0):
        raise ValueError("I genetic-variance factor violated")
    if not (float(new[:, 1, :].min()) <= mean - RESPONSE_THRESHOLD):
        raise ValueError("I locus structurally cannot attain registered decline")
    return new, {
        "A_width":width,
        "A_founding_allele_values": [float(.5-width), float(.5+width)],
        "A_founding_expressed_variance": float(new[:, 2, :].mean(axis=1).var()),
        "A_expected_F1_segregation_variance_no_mutation": float(width*width/2),
        "A_can_reach_threshold_without_mutation": bool(width >= RESPONSE_THRESHOLD),
        "I_scale":i_scale,
        "I_allele_copy_mean": float(new[:, 1, :].mean()),
        "I_allelic_variance_proxy":i_copy_var,
        "I_expressed_variance":float(new[:, 1, :].mean(axis=1).var()),
        "I_original_variance_proxy":original_var,
        "I_variance_relative_to_source":float(i_copy_var/original_var),
        "I_possible_decline_support":float(mean - new[:, 1, :].min()),
        "I_can_reach_decline_without_mutation":True,
        "no_clipping": True,
    }


def audit(shard0: Path) -> dict:
    raw=shard0.read_bytes()
    sha=hashlib.sha256(raw).hexdigest()
    if sha!=SOURCE_SHARD0_SHA256:
        raise ValueError("original source-shard SHA256 mismatch; do not substitute regenerated genomes")
    records=[]
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        if len(z.namelist())!=259 or len(z.namelist())!=len(set(z.namelist())):
            raise ValueError("original shard member inventory mismatch")
        for block in FOUNDER_BLOCKS:
            initial,source=original_state(z,block)
            for width in A_HALF_WIDTHS:
                for scale in I_ALLELE_SCALE:
                    transformed,summary=transform(initial,width,scale)
                    # Explicitly ensure no original array was overwritten.
                    if float(initial[:,2,:].mean())!=0.5 or float(initial[:,1,:].mean())!=summary["I_allele_copy_mean"]:
                        raise ValueError("original founder mutated during examination")
                    records.append({"block":block,**source,**summary,
                                    "transformed_alleles_sha256":hashlib.sha256(transformed.tobytes(order="C")).hexdigest()})
    assert len(records)==8
    return {
        "schema":"chapter2_clock_factorial_genotype_feasibility_v1",
        "status":"EIGHT_COUNTERFACTUAL_T0_GENOTYPE_CONFIGURATIONS_VERIFIED_NO_TRAJECTORIES",
        "original_source_shard0_sha256":SOURCE_SHARD0_SHA256,
        "original_source_shard0_bytes":len(raw),
        "founder_blocks":list(FOUNDER_BLOCKS),
        "A_half_widths":list(A_HALF_WIDTHS),
        "I_allele_multipliers":list(I_ALLELE_SCALE),
        "original_annual_genomes_replayed":False,
        "new_biological_histories":0,
        "factorial_t0_genotype_records":records,
        "limitations":[
            "Synthetic founding-genotype transformation only, no realised genetic evolution or first-passage time.",
            "I allele scaling also rescales genetic covariances with other loci; it does not isolate a marginal quantitative-genetic variance effect.",
            "A width changes both initial allelic spread and structural threshold accessibility under no A mutation.",
            "Exact original Model3 reproductive and inheritance source must be bound and tested before biological execution.",
            "Only original context-zero founding state used; previously source-admitted context identity does not substitute for a fresh new-producer gate."
        ],
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--original-shard0",type=Path,required=True)
    p.add_argument("--out",type=Path,required=True)
    a=p.parse_args()
    result=audit(a.original_shard0)
    a.out.parent.mkdir(parents=True,exist_ok=True)
    with a.out.open("x",encoding="utf8",newline="\n") as stream:
        json.dump(result,stream,indent=2,ensure_ascii=False,allow_nan=False)
        stream.write("\n")
    print(json.dumps({"status":result["status"],"configurations":len(result["factorial_t0_genotype_records"]),"sha":result["original_source_shard0_sha256"]}))

if __name__=="__main__": main()
