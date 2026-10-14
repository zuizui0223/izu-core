"""Exact-source pool for verifier-only portability repair; no generic pooling."""
import ast,base64,hashlib,json,subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OLD_COMMIT='a18d527bdab699d2841adcf4f8663ed41ba0c29b'
OLD_RUNNER_SHA='ce2847eff036b3a74992c18431c4184faa336b68711ad2a3416661e3823eac18'
EXPECTED_BINDINGS={'scripts/future_parent_selection_20261013.py': '45170028aa2e3c79e08eea3e7388da49dc73cbe21625daf05139d5b11da84d5c', 'scripts/initial_assurance_mean_20261013.py': '1af33520ac4524f27ad9eedf148d9564a776b9459b82084fe2f687eec497a5e6', 'scripts/run_initial_assurance_mean_20261013.py': 'b422a6ffd5d6e66e037ecf23cb84dd0b6b288daaf42741da8996cea61d0d7b93', 'scripts/persistence_expression_mechanism_20261012.py': 'da8be50f183732f4bafc0cd3f8e5760514911859a96134a3ba61fdf5e2e32d0d', 'scripts/chapter2_kb_reproduction.py': '79327794763f963f0f3399c8a94cdb94ad019093d306f2ac4c0bb59a92711863', 'scripts/model3_island/types.py': 'a572e1e7f4fded181585871a63582b16f40292bd07b13e8efc9d6b6234eb21c5', 'scripts/model3_island/population.py': 'c959d18816da6666dbfb4e91bd9582c94af5453b25498d033f5747305b05fe0f', 'scripts/model3_island/randomness.py': '63522ae3c5ff8e11f114b5649a989945fa4ba2480fdca0f74857601b0e4b211f', 'scripts/model3_island/history.py': '28d22c7fde81d9be6a604fa9dd4cb6b48d78d388d4db85f798a935cf81415488'}
REGISTRY=ROOT/'data/design/future_parent_source_compatibility_20261013.json'


def sha(raw):return hashlib.sha256(raw).hexdigest()


def generation_digest(source):
    tree=ast.parse(source)
    tree.body=[node for node in tree.body if not isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef)) or node.name not in ('verify','technical_gate')]
    return sha(ast.dump(tree,include_attributes=False).encode())


def validate_active():
    r=json.loads(REGISTRY.read_bytes());old=base64.b64decode(r['old_runner_base64'],validate=True)
    if r['old_commit']!=OLD_COMMIT or sha(old)!=OLD_RUNNER_SHA:raise ValueError('original frozen source identity')
    active=(ROOT/'scripts/run_future_parent_selection_20261013.py').read_text(encoding='utf-8').encode()
    if sha(active)!=r['active_runner_sha256']:raise ValueError('active exact runner source identity')
    if generation_digest(old.decode())!=generation_digest(active.decode()):raise ValueError('biological generation code changed')
    if r['binding_sha256']!=EXPECTED_BINDINGS:raise ValueError('exact original recipe/native binding inventory required')
    for name,h in r['binding_sha256'].items():
        if sha((ROOT/name).read_text(encoding='utf-8').encode())!=h:raise ValueError('generation/native binding changed: '+name)
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    return r,head


def admit_source(header):
    r,head=validate_active();commit=header['execution_commit'];digest=header['runner_sha256']
    if (commit,digest) not in ((OLD_COMMIT,OLD_RUNNER_SHA),(head,r['active_runner_sha256'])):
        raise ValueError('undeclared execution commit/runner source pair')
    return dict(execution_commit=commit,runner_sha256=digest,generation_ast_sha256=generation_digest(base64.b64decode(r['old_runner_base64']).decode()))
