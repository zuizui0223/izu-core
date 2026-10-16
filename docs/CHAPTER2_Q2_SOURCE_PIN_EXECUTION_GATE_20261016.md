# Q2進化順序実験：元Model 3ソースの固定・実行前判定（2026-10-16）


**実行承認の状態更新（2026-10-16 23:27 JST）:** 384経路×200更新の固定設計について利用者本人から明示的な承認を受け、[SHA固定のactivation原本](protocols/chapter2_q2_i_support_order_20261016_activation.json)を`main`に保存済み。これは下記の過去の「未承認／activation未作成」記述より新しい状態記録です。元Model 3の25ソース固定と設計・実行器SHAは保持し、GitHub ActionsのQ2ワークフローは**手動`workflow_dispatch`のみ**。**384経路の本計算／六分類本解析の実行結果は現時点で確認されていません。**

**対象:** merged [PR #577](https://github.com/zuizui0223/izu-core/pull/577) の既存384経路設計。科学的結果は未生成。変更するのは**実行前のソース同一性検査**であり、既存の登録設計、創始者、訪花履歴、遺伝的介入、評価量、Q1〜Q4の原結果は変更しない。

## 発見した検証上の隙間

既存の実行承認処理は、現在のソースから計算したSHA-256一覧に署名相当の対応を求める方式だった。しかし、それだけでは、基準コミット後にModel 3本体や歴史的Q1ソースが変更され、**変更後のソースで新しい一覧と承認ファイルを作った場合**に、最初に計画した実験のままかを判定できない。

## 修正

原実験前の技術専用GitHub Actions証拠（[PR #577](https://github.com/zuizui0223/izu-core/pull/577)の12更新・128初期帳簿検査）に残った**25個のソースSHA-256**を、[凍結レシート](protocols/chapter2_q2_original_model_source_pins_20261016.json)として固定した。内容は21の `scripts/model3_island/*.py`、歴史的Q1／訪花履歴の2つのプログラム、2つの原デザインである。これらは研究設計の基準コミット `8e2dcada6514381bd9304cb6e2ddc2b855a4148f` の同じソースであり、現在のGit blobとの一致を確認済み。

`source_manifest()` を呼ぶたびに25ファイルを期待SHAと比較し、1ファイルでも違えば `ValueError` として停止する。したがって以下すべてが同じ条件で中断する。

- CI内の12更新の技術専用Model3テストと128セルの初期繁殖帳簿確認
- 将来、本人の明示的な実行承認と完全なactivationが揃ってから起動する32シャード×12ケースの原本作成
- 将来の384ケース原本に対する型付きゲノム・親子関係・同一乱数再計算と独立六分類集計

実験固有の設計文書／Q2 runner／保存・検証コードは、これらの古い生物学的ソースとは別に**実行承認レシートでSHA固定**する。原本Model3のSHAを都合のよい変更後の値へ更新して実行することは許容しない。もし新しいModel3本体を試したいなら、**別研究・別プロトコル・別実験ID**が必要。

## 何を実証するか／しないか

この実装は**コードの出所が研究計画と一致するか**を検査する。モデルが現実の島嶼進化を説明したこと、A座の支持変化が順序を変えたこと、遺伝的浮動が唯一の原因だったことを新しく示すものではない。新しい生物学的本解析は0経路。

追加テストでは、原ソースのビット変更、基準コミットの差し替え、必要ファイルの欠落、誤った歴史的ソースの再固定をそれぞれ拒否する。誤りを見逃さない仕組みを確認したあとに、既存384経路の本解析の承認・実行へ進む。

## 再現手順

```bash
pytest -q tests/test_chapter2_q2_i_support_order_20261016.py tests/test_chapter2_q2_i_support_provenance_20261016.py
python -m scripts.chapter2_q2_i_support_order_20261016 --mode technical-smoke --out q2_source_pin_technical_only.json
```

**承認前のSHA付きひな型:** `scripts/prepare_chapter2_q2_activation_template_20261016.py` は、生物進化を1更新も実行せず、元設計SHAと25ソース固定のレシート、Q2実行器まで含めた現在のソース一覧SHAから、384ケースの承認**候補**を生成する。候補は `status=PENDING_AUTHOR_REVIEW_NOT_APPROVED`、`owner_explicit_approval=false`、`approval_is_new_not_reused=false` のまま保存され、`admission()` が明示的に**HOLD**することをCIで検証する。原本とは異なる `q2-384-pending-approval.json` としてActions artifactに保存し、承認済みactivationのフリをさせない。個人による正式承認・手動Actions起動はまだ行われていない。

**実行ゲートの未解除:** 作者承認activation `docs/protocols/chapter2_q2_i_support_order_20261016_activation.json` は存在しない。384経路の200更新を通常CIやPR pushから起動せず、実験結果・CI通過の未確認箇所を成功と表記しない。
