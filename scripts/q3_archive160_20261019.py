"""Source-local archive packaging and safe restoration; no biology or credentials."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import zipfile


def pack(root, output):
    root=Path(root); output=Path(output)
    if (root/'RUN.lock').exists(): raise ValueError('active worker cannot be packed')
    files=[root/'RUN.json']+sorted((root/'states').glob('*.npz'))
    manifest={str(p.relative_to(root).as_posix()):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    with zipfile.ZipFile(output,'x',compression=zipfile.ZIP_STORED) as z:
        for p in files:z.write(p,p.relative_to(root).as_posix())
        z.writestr('ARCHIVE_MANIFEST.json',json.dumps(manifest,sort_keys=True))
    return dict(file=output.name,bytes=output.stat().st_size,sha256=hashlib.sha256(output.read_bytes()).hexdigest())


def restore(archive,root):
    root=Path(root)
    if root.exists(): raise ValueError('restore requires absent root')
    with zipfile.ZipFile(archive) as z:
        names=z.namelist()
        manifest=json.loads(z.read('ARCHIVE_MANIFEST.json'))
        if len(names)!=len(set(names)) or set(names)!=set(manifest)|{'ARCHIVE_MANIFEST.json'}:
            raise ValueError('archive inventory mismatch')
        for name,sha in manifest.items():
            p=PurePosixPath(name)
            if ('\\' in name or p.is_absolute() or '..' in p.parts or
                not (name=='RUN.json' or len(p.parts)==2 and p.parts[0]=='states' and p.suffix=='.npz')):
                raise ValueError('unsafe archive member')
            if hashlib.sha256(z.read(name)).hexdigest()!=sha:
                raise ValueError('archive checksum mismatch')
        root.mkdir(parents=True); (root/'states').mkdir()
        for name in manifest:(root/name).write_bytes(z.read(name))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('action',choices=('pack','restore'));p.add_argument('--root',type=Path,required=True)
    p.add_argument('--archive',type=Path,required=True)
    a=p.parse_args()
    if a.action=='pack':print(json.dumps(pack(a.root,a.archive),sort_keys=True))
    else:restore(a.archive,a.root)
