"""Exploratory saturated 18-cell lookup control, not an ecological transfer model.

All six original event outcomes and all 256 paired stochastic seed clusters
remain in the denominator. Each founder/context cell's training frequencies
are learned from the *other* four seed folds, with Jeffreys smoothing.
Unknown environments and new founders have no valid lookup prediction.
No original Model 3 biological histories are generated.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import numpy as np
from scripts.audit_chapter2_initial_clock_identifiability_20261013 import admit, EXPECTED_INPUT_GIT_BLOB, CLASSES
from scripts.audit_chapter2_initial_clock_transfer_20261013 import blob_sha
from scripts.audit_chapter2_initial_clock_paired_cv_20261013 import validate_clusters

PAIRED_BLOB='afab849d2f0036d07d28beb1441644f9ca2808cb'
A=(0.01,0.5,1.0,2.0)

def lookup(summary:dict, paired:dict, alpha:float=0.5)->dict:
    if not isinstance(alpha,(float,int)) or not np.isfinite(alpha) or alpha<=0:
        raise ValueError('Positive finite six-class prior pseudocount required')
    cells=admit(summary)
    # Use no t0 features; original six labels themselves are sufficient for
    # a context-specific empirical distribution, but only for KNOWN contexts.
    rows=[{'block':c['block'],'context':c['context'],'counts':np.asarray([c['categories'][k] for k in CLASSES],float)} for c in cells]
    history=validate_clusters(paired,rows)
    keys={(r['block'],r['context']):i for i,r in enumerate(rows)}
    counts=np.zeros((18,6),dtype=float)
    n=0;top=0;ll=0.;bs=0.;
    # Hold all nine source contexts for each seed cluster out in the same fold.
    for fold in range(5):
        counts.fill(0)
        for (block,rep),seq in history.items():
            if rep%5!=fold:
                for ctx,y in enumerate(seq):counts[keys[block,ctx],y]+=1
        if not np.all(counts.sum(axis=1)>0):raise ValueError('Missing training case')
        predicted=(counts+alpha)/(counts.sum(axis=1,keepdims=True)+6*alpha)
        if not np.isfinite(predicted).all() or not np.allclose(predicted.sum(axis=1),1):
            raise ValueError('Invalid empirical probability')
        for (block,rep),seq in history.items():
            if rep%5==fold:
                for ctx,y in enumerate(seq):
                    prob=predicted[keys[block,ctx]]
                    ll-=np.log(prob[y])
                    bs+=1-2*prob[y]+np.dot(prob,prob)
                    top+=int(int(np.argmax(prob))==y)
                    n+=1
    if n!=2304:raise ValueError('Missing original all-start outcome')
    return {'smoothing':alpha,'n':n,'log_loss':float(ll/n),'brier':float(bs/n),
            'argmax_accuracy':float(top/n),'correct':top,
            'model':'18-cell saturated lookup (founder and ecological context are previously known)'}

def run(summary:dict,paired:dict)->dict:
    return {'schema':'chapter2_initial_clock_saturated_lookup_exploratory_v1',
            'status':'ALL256_PAIRED_SEEDS_FIVE_FOLD_LOOKUP_CONTROL_NOT_NOVEL_ECOLOGICAL_TRANSFER',
            'source_original_biological_histories':2304,
            'paired_clusters':256,'source_profiles':18,'frozen_event_categories':list(CLASSES),
            'fold_rule':'replicate % 5; retain all nine context labels per founder-specific seed cluster in same fold',
            'scores':[lookup(summary,paired,x) for x in A],
            'limits':['Saturated lookup is inapplicable to unseen founder/ecological combinations.',
                      'Different parameter dimensions; cannot use lookup comparison to infer genetic-mechanism benefit.',
                      'No model refit uncertainty, no conditional t0 A access-time prediction, no prospective confirmation.',
                      'Original six-category histories stay separate; synthetic stochastic cluster is not ecological independent unit.']}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--compact',type=Path,required=True)
    p.add_argument('--paired',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    a=p.parse_args()
    if a.out.exists():raise ValueError('Refuse output overwrite')
    if blob_sha(a.compact.read_bytes())!=EXPECTED_INPUT_GIT_BLOB:
        raise ValueError('Frozen original ecological source blob differs')
    if blob_sha(a.paired.read_bytes())!=PAIRED_BLOB:
        raise ValueError('Verified original paired 256-cluster readout blob differs')
    obj=run(json.loads(a.compact.read_bytes()),json.loads(a.paired.read_bytes()))
    obj['source']={'original_ecological_compact_blob':EXPECTED_INPUT_GIT_BLOB,
                   'original_verified_paired_blob':PAIRED_BLOB,
                   'new_original_biological_trajectories':0}
    a.out.parent.mkdir(parents=True,exist_ok=True)
    with a.out.open("x", encoding="utf-8", newline="\n") as output:
        output.write(json.dumps(obj,indent=2,allow_nan=False)+'\n')
    print(json.dumps({'status':obj['status'],'scores':obj['scores']},indent=2))
if __name__=='__main__':main()
