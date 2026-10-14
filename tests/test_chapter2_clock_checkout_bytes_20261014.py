"""Real Git checkout regression; no Model3 transition or pilot is executed."""
from pathlib import Path
import hashlib
import subprocess
import pytest

ROOT=Path(__file__).resolve().parents[1]
PINS={
    'data/design/chapter2_clock_factorial_pilot_input_inventory_20261013.json':'f18eae09e3f569ae7edefe970ea17d93c64b1bd5',
    'data/design/chapter2_clock_factorial_pilot_protocol_20261013.json':'75d49de2781a240c14bdc3f9106212b0dbbda6aa',
    'data/design/chapter2_clock_original_t0_typed_fixture_20261013.json':'4b529cce12bc44e06d43a22b10c325a52bbd967b',
    'data/results/chapter2_clock_t0_reproduction_equivalence_20261013.json':'e1d4e58a8dde547a94b687d6f89d2843c8bfff0c',
    'scripts/model3_island/types.py':'0bc427b3261e7baf1651648ee879b368f9bf935b',
    'scripts/model3_island/reproduction.py':'95314698a3296b6f13b8c053c36f2df0b7b744ca',
    'scripts/model3_island/population.py':'20e90f249f63e9f37e8801d19d9b75cade2fe193',
    'scripts/model3_island/randomness.py':'46f1ee55899e729cdd09d9dbb9332694ef1e2071',
    'scripts/model3_island/history.py':'0c58aee6f73ae133d96d8da4dd6678886ff3061c',
    'data/design/chapter2_clock_factorial_pilot_analysis_contract_20261013.json':'06c343b6e20a08c0575ddbe6ace5ef5fbdeb85ed',
}


def git(cwd,*args):
    return subprocess.run(['git','-C',str(cwd),*args],check=True,capture_output=True).stdout


def blob(raw):return hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()


@pytest.mark.parametrize('autocrlf',['true','false'])
def test_checkout_preserves_all_original_native_and_input_blob_pins(tmp_path,autocrlf):
    repo=tmp_path/'checkout';repo.mkdir()
    git(repo,'init','--quiet')
    git(repo,'config','core.autocrlf','false')
    (repo/'.gitattributes').write_bytes((ROOT/'.gitattributes').read_bytes())
    paths=[*PINS,'scripts/prepare_chapter2_clock_pilot_archive_20261013.py',
           'scripts/verify_chapter2_clock_pilot_raw_20261013.py',
           'scripts/package_chapter2_clock_pilot_shard_20261013.py']
    source={}
    for name in paths:
        raw=git(ROOT,'show','HEAD:'+name)
        if name in PINS:assert blob(raw)==PINS[name], 'Git source anchor already changed'
        source[name]=raw
        p=repo/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
    git(repo,'add','--','.gitattributes',*paths)
    git(repo,'config','core.autocrlf',autocrlf)
    # Forces actual Git worktree conversion, without requiring a commit/identity.
    for name in paths:(repo/name).unlink()
    git(repo,'checkout-index','--force','--all')
    for name in paths:
        current=(repo/name).read_bytes()
        assert current==source[name], f'Unchanged source converted at checkout: {name}'
        if name in PINS:assert blob(current)==PINS[name]
