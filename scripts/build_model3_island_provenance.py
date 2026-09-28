import json,csv
from pathlib import Path
from hashlib import sha256
from scripts.model3_island.design import digest,source_hashes,compile_design
root=Path('data/results/model3_island_v2');out=Path('data/results/model3_island_v2_summary');design=json.loads(Path('data/design/model3_island_v2.json').read_text())
assert source_hashes()==design['source_hashes']
baseline=json.loads(Path('data/design/model3_island_frozen_baseline_hashes.json').read_text())
assert all(sha256(Path(p).read_bytes()).hexdigest()==h for p,h in baseline.items())
cases=[c for c in compile_design(design) if c['cohort']!='pilot']; rows=[]
for c in cases:
 p=root/c['case_id']/'receipt.json';raw=p.read_bytes();r=json.loads(raw)
 assert r['status']=='complete' and r['case_hash']==digest(c) and r['manifest_hash']==digest(design)
 rows.append({'case_id':c['case_id'],'receipt_sha256':sha256(raw).hexdigest(),'arrays_sha256':r['arrays_sha256'],'case_hash':r['case_hash'],'compute_amendment':r.get('compute_amendment','original')})
assert len(rows)==19968
with (out/'case_receipts.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
artifacts={p.name:sha256(p.read_bytes()).hexdigest() for p in sorted(out.iterdir()) if p.is_file() and p.name!='provenance.json'}
receipt={'manifest_hash':digest(design),'cases':len(rows),'original_cases':sum(r['compute_amendment']=='original' for r in rows),'amended_cases':sum(r['compute_amendment']!='original' for r in rows),'frozen_baseline_files_unchanged':baseline,'audit':json.loads(Path('data/results/model3_island_v2_audit.json').read_text()),'artifacts':artifacts,'raw_arrays_location':str(root),'raw_arrays_remotely_deposited':False,'scope':'Receipt identities rechecked; full array/state validation is evidenced by the completed all-case audit. Artifact hashes include locally generated per-condition figures.'}
(out/'provenance.json').write_text(json.dumps(receipt,indent=2),encoding='utf-8')
print(json.dumps({k:receipt[k] for k in ['cases','original_cases','amended_cases']}))
