# EnvGeo-Earthquake 公開ロードマップ

[English version](publication_roadmap.md)

最終更新: 2026-10-08

上から順番に、1項目ずつ進めます。日英両方の作業ログに証拠を残した後だけ
完了とします。EnvGeo-Seawaterは変更せず、実行時依存も追加しません。

## Phase 1 — Earthquake単独化

- [x] Earthquakeの公開対象ファイルを確定する。
- [x] 公開用GitHubリポジトリ／Gitクローンの場所を確定する。
- [x] `envgeo_utils.py`から旧Seawaterデータ読込を除去する。
- [x] 未公表データ参照を除去する。
- [x] Seawaterがないとskipする4テストを置き換える。
- [x] 不要なSeawaterサンプルと開発archiveを公開対象から外す。
- [x] アプリバージョン定義を1か所へ集約する。
- [x] カレントディレクトリに依存しないアセット読込を確認する。
- [x] `.xls`表示を外すか、必要依存を追加・テストする。

## Phase 2 — 最小限の安定性・再現性

- [x] 現状挙動を維持する最小検証方針を定義する。
- [x] 現行のUSGS失敗処理を監査し、接続、timeout、HTTP、不正JSON、空dataで
  page crashを防ぐために必要なguardだけを追加する。
- [x] 現行JMA/NIED uploadの必須列・読込み不能file処理を確認し、
  具体的な失敗を確認した場合のみ変更する。
- [x] uploadがsession-onlyであることを明記する。
- [x] 現行の取得件数上限とUSGS recordが改訂され得る注意を維持する。
- 別途の必要性が示されない限り後回し: 重複ID管理、issue code体系、
  validation dashboard、export metadata拡張。

## Phase 3 — 出典・ライセンス

- [x] 海岸線CSVのNatural Earth出典・ライセンスを追加する。
- [x] USGSカタログとプレート境界の引用文を統一する。
- [x] CARTO/OSM/USGS/Esri/GSIの出典表示を再確認する。
- [x] JMA/NIEDの利用・再配布責任を記録する。
- [x] 完了した海岸線来歴項目についてNOTICE、日英README、Homeの出典を同期する。
  後続の出典監査でも同期状態を維持する。

## Phase 4 — Earthquake固有テスト

- [x] USGSの正常、空、欠損、不正JSON、HTTPエラー、timeout、接続失敗をテストする。
- [x] query構築と20,000件上限警告をテストする。
- [x] 任意比較機能をreleaseに残す場合、正常upload 1件と読込み不能/必須列欠損1件だけをsmoke testし、schemaを拡張しない。
- [x] 日英4 visualizer pageの実際の描画準備helperで、NaNと範囲外座標をテストする。
- [x] 日英pageの実helperを実行し、経度ラップ、日付変更線、ローカルkm、断面幾何をテストする。
- [x] 日英Advancedでプレート境界の正常取得、全面・部分失敗、不正GeoJSON、
  日本限定模式fallbackをテストする。
- [x] 日英Homeと現行4 visualizer pageについて、見出し・取得buttonを含む永続startup AppTestを追加する。
- [x] 許可された公開対象、ignore規則、tracked file除外、runtime参照、秘密情報・秘密鍵、
  絶対local path、symlink、Markdown local linkのrepository-health testを追加する。

## Phase 5 — CI・配布

- [ ] Python 3.10 / 3.12 GitHub Actions CIを追加する。
- [ ] 実ネットワークなしでpytest、構文、公開物検査を実行する。
- [ ] ソース配布のみか、インストール可能なpackageにするか決める。
- [ ] package化する場合は`pyproject.toml`、launcher、package data、wheel検査、隔離installを追加する。
- [ ] Streamlit Community Cloud設定を確認する。
- [ ] devcontainerのXSRF無効化設定を見直す。

## Phase 6 — 日英ドキュメント完成

- [ ] クリーン環境で導入手順を確認する。
- [ ] Quick Start、USGS上限、upload形式、品質確認、出力、offline、トラブル対応を日英同期する。
- [ ] AI支援開発の開示方針を決める。
- [ ] 日英の内容対応とリンクを確認する。

## Phase 7 — 公開環境スモーク

- [ ] 日英Home / Simple / Advancedを確認する。
- [ ] USGS取得、空結果、上限、preset、hotspotを確認する。
- [ ] 2D/3D、断面、頻度、プレート境界、offline海岸線を確認する。
- [ ] releaseで有効にする場合は任意JMA/NIED uploadを1回確認し、中核のUSGS CSV出力も確認する。
- [ ] PCと小画面表示を確認する。
- [ ] 全結果を日英作業ログへ記録する。

## Phase 8 — GitHub Release

- [ ] 安定版versionを決め、全表示を同期する。
- [ ] `CITATION.cff`と日英release notesを追加・検証する。
- [ ] repository説明、topics、license、公開物を確認する。
- [ ] CI合格commitをtagし、GitHub Releaseとarchiveを確認する。

## Phase 9 — Zenodo DOI

- [ ] GitHub Release作成前にZenodoでrepositoryを有効化する。
- [ ] author、ORCID、affiliation、license、keywords、version、filesを確認する。
- [ ] recordを公開し、version DOIとconcept DOIを記録する。
- [ ] DOIを日英README、citation metadata、release recordへ反映する。
- [ ] アプリ、GitHub Release、Zenodoの相互リンクを確認する。

## Phase 10 — 将来のEnvGeo Core検討

- [ ] Earthquake DOI公開後、Seawater JOSS作業と分けて開始する。
- [ ] contractテスト追加後に、アセット、地図、海岸線、経度、ローカルkm、出典metadataを評価する。
- [ ] 両アプリの独立性を保つ依存、versioning、rollback計画を作る。
