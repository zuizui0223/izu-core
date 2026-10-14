# Q3 published delivery review

**PASS — the publication condition in the final document review is now closed.**

The reviewer independently queried GitHub's read-only release and tag APIs after publication. Release [q3-conditional-futures-20261014](https://github.com/zuizui0223/izu-core/releases/tag/q3-conditional-futures-20261014), ID `412344508`, is non-draft, non-prerelease, published at `2026-10-14T04:56:25Z`. Both the release target and resolved tag point to the scientific execution commit `d92ac4324b6e1c8924dcc8e5f30e0750088a3acf`.

All three assets are in uploaded state. Their live GitHub server sizes and digests match the previously verified scientific archive and the locally hashed receipts:

| Asset | Asset ID | Bytes | SHA256 |
| --- | ---: | ---: | --- |
| `Q3_CONDITIONAL_FUTURES_20261014.zip` | 639243280 | 410326692 | `8a2462910025b4a386e789583578cb1380349097393916dac4e50d01c9637b7e` |
| `PUBLICATION_RECEIPT.json` | 639243287 | 529 | `3d508d6d97a7a9e5230a225d80c17f7cc940c010d0acefb5fcfa4e52a87786ff` |
| `EXTERNAL_READBACK.json` | 639243282 | 910 | `f0962abe3a5ca66e36d81de1e7111c970bd29960f93f44f55d76a41f866b0d21` |

The publication receipt `data/results/q3_conditional_futures_20261014/GITHUB_PUBLICATION.json` agrees with those live identities and records the coordinator's byte comparisons of the two small downloaded receipt assets. The reviewer verified the live API identities and local receipt hashes directly, without duplicating asset downloads.

GitHub reports `immutable: false`, accurately retained in the publication receipt. This is a published, hash-bound preservation release, not a platform-locked immutable release. Future retrieval should check the recorded hashes and asset identities.

This closes the release-delivery condition only; the scientific claim ceilings in the actual-results and final-document reviews remain unchanged. No native update, replay, new seed, binary download, or GitHub write was performed for this review.
