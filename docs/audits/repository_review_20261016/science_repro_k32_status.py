from pathlib import Path
import json, sys, importlib
from unittest.mock import patch
root=Path(__file__).resolve().parents[2]
repo=root/'work/repository_review_20261016'
sys.path.insert(0,str(repo))
cases=[('fixed_frequency_heterozygosity','run_fixed_frequency','INSUFFICIENT_SHARED_ALIVE_SOURCE_PARENT_PATHS'),('heterozygosity_reproductive_channels','run_channels','NOT_ENOUGH_SURVIVORS'),('self_transmission_curvature','run_self_curvature','INSUFFICIENT_SOURCE_YEAR8_PARENT_SURVIVORS')]
for suffix,runner,status in cases:
    module=importlib.import_module('scripts.audit_model3_k32_'+suffix)
    output=Path(__file__).with_name('repro_k32_'+suffix+'.json')
    with patch.object(module,runner,return_value={'status':status}),patch.object(sys,'argv',['audit','--out',str(output)]):
        try: module.main()
        except KeyError as e: print(suffix, 'KeyError', str(e), 'written status',json.loads(output.read_text())['status'])
        else: raise AssertionError('Expected current failure did not reproduce')
