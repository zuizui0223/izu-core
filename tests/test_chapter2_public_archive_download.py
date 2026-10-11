import hashlib
import io
import json
from pathlib import Path
import textwrap
import urllib.request

import pytest


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/chapter2-public-archive.yml"


@pytest.mark.parametrize("valid_digest", [True, False], ids=["matching-digest", "wrong-digest"])
def test_workflow_authenticates_api_only_and_verifies_redirected_bytes(
    tmp_path, monkeypatch, valid_digest
):
    # Exercise the workflow's actual Python and urllib's real redirect handler;
    # replace only network transport with deterministic artifact bytes.
    workflow = WORKFLOW.read_text(encoding="utf-8")
    inline = workflow.split("python - <<'PY'\n", 1)[1].split("\n          PY", 1)[0]
    code = compile(textwrap.dedent(inline), str(WORKFLOW), "exec")
    payload = b"original artifact bytes\n"
    digest = hashlib.sha256(payload).hexdigest() if valid_digest else "0" * 64
    manifest_path = tmp_path / "data/design/chapter2_public_archive_manifest_20261006.json"
    manifest_path.parent.mkdir(parents=True)
    manifest_path.write_text(
        json.dumps({"campaigns": {"confirmation": {"artifacts": [
            {"id": 123, "name": "original-shard", "digest": "sha256:" + digest}
        ]}}}),
        encoding="utf-8",
    )
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("REPO", "example/repository")
    monkeypatch.setenv("GH_TOKEN", "test-token")
    requests = []

    def download_after_redirect(request):
        redirected = urllib.request.HTTPRedirectHandler().redirect_request(
            request, None, 302, "Found", {},
            "https://artifact-storage.invalid/original.zip",
        )
        requests.append((request, redirected))
        return io.BytesIO(payload)

    monkeypatch.setattr(urllib.request, "urlopen", download_after_redirect)
    if valid_digest:
        exec(code, {})
    else:
        with pytest.raises(SystemExit, match="digest mismatch original-shard"):
            exec(code, {})

    assert len(requests) == 1
    initial, redirected = requests[0]
    assert initial.full_url == "https://api.github.com/repos/example/repository/actions/artifacts/123/zip"
    assert dict(initial.header_items())["Authorization"] == "Bearer test-token"
    assert redirected.get_header("Authorization") is None
    assert (tmp_path / "public-archive-artifacts/confirmation/original-shard.zip").read_bytes() == payload
