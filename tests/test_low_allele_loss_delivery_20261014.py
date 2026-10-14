import json
from pathlib import Path
import pytest
import scripts.build_chapter2_unified_el_submission_bundle as builder

def test_low_loss_delivery_preserves_expected_frequency_and_scope():
    members, derivations = builder.low_allele_loss_materials()
    result=json.loads(members['EVIDENCE/LOW_ALLELE_LOSS_READOUT.json'])
    assert result['cases']==2304 and result['eligible_loss']==1238
    assert result['direction_counts']=={'favouring_needed':315,'opposing_needed':923,'screened_near_zero':0}
    assert result['new_biological_histories']==result['reproduction_advances']==0
    assert len(members)==6 and len(derivations)==6
    assert 'not pure drift' in members['EVIDENCE/LOW_ALLELE_LOSS_SCOPE.md'].decode()

def test_low_loss_delivery_rejects_changed_receipt(tmp_path,monkeypatch):
    root=Path(builder.ROOT)
    receipt=root/'data/results/low_allele_loss_20261014/PUBLIC_READBACK.json'
    dest=tmp_path/receipt.relative_to(root)
    dest.parent.mkdir(parents=True)
    value=json.loads(receipt.read_text())
    value['payloads']=19
    dest.write_text(json.dumps(value))
    monkeypatch.setattr(builder,'ROOT',tmp_path)
    with pytest.raises(ValueError,match='low-allele-loss'):
        builder.low_allele_loss_materials()
