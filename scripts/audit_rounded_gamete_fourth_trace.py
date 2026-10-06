from pathlib import Path
import numpy as np,json,hashlib,traceback
from scripts.model3_rounded_gamete_integration import bounded_step
from scripts.run_model3_full_mutation import config,exposure
c=Path.cwd();p=c/'rounded_gamete_ten65/assurance_cost_near_jump.npz'
r=json.loads(p.with_suffix('.json').read_text());assert r['failure_period']==4 and hashlib.sha256(p.read_bytes()).hexdigest()==r['npz_sha256']
with np.load(p) as z:state=(z['core'],tuple(z[f'factor{k}'] for k in range(3)))
try:bounded_step(state,(np.linspace(0,1,65),)*3,exposure(76001,'near').visitors[3],config('assurance_cost',.01),budget=16_000_000)
except Exception:
 text=traceback.format_exc();print(text);(c/'rounded_gamete_fourth_trace.txt').write_text(text,encoding='utf-8')
