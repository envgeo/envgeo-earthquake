# EnvGeo-Earthquake リリースチェックリスト

[English version](release_checklist.md)

## 文書とmetadata

- [ ] 日英の`PROJECT_STATUS`で公開ゲートが全て完了している。
- [ ] 日英の最新作業ログに正確な確認証拠がある。
- [ ] 2026-10-08公開監査のブロッカーが解消済み、または新しい日付の監査で更新済み。
- [ ] アプリ、全アクティブページ、README、`CITATION.cff`のバージョンが一致。
- [ ] 日英README、マニュアル、Home更新履歴、testingガイドが同期。
- [ ] 出典、ライセンス、外部サービスの注意が最新。

## 自動確認

- [ ] `python -m pytest -q test`が公開対象環境で合格。
- [ ] Python 3.10 / 3.12 GitHub Actions CIが合格。
- [ ] 全アクティブPythonファイルの構文確認に合格。
- [ ] `test/test_asset_paths.py`で、一時current directoryから両解像度の海岸線と日英Home内READMEの読込みに合格。
- [ ] 同梱両海岸線のhashが`coastline/LICENSE_OR_SOURCE_Japanese.md`と一致することを確認し、
  Natural Earth v4.1.0の派生根拠と来歴上の制約をrelease archiveへ維持。
- [ ] `test/test_basic.py`が、該当する全日英pageで共通USGS catalog・plate-boundary引用を
  使用するcontractを確認。
- [ ] `test/test_offline_map.py`が標準地図のOpenStreetMap利用と、USGS imagery、
  Esri Ocean、GSIの監査済み実行時creditを実tile通信なしで確認。
- [ ] 任意比較をreleaseで有効にする場合、日英AdvancedのuploadがCSV、TSV、TXT、XLSXのみを受け付け、`test/test_upload_formats.py`に合格。
  正常CSVと必須列欠損CSVの日英smoke caseも確認する。
- [ ] `docs/earthquake_validation_Japanese.md`を確認し、追加した各guardが実際の失敗を防ぎ、通常のUSGS表示挙動を変えていない。
- [ ] `test/test_envgeo_utils.py`が正常、空、欠損、不正形式、HTTP error、timeout、
  接続失敗のUSGS loader caseに実通信なしで合格。
- [ ] USGS query構築が必須・選択parameterを含み、未指定任意値を除外し、日英4pageが
  test済み共通取得上限境界を使うことを確認。
- [ ] `test/test_page_coordinates.py`で、日英4pageが経度±180°・緯度±90°の境界点を
  保持し、欠損・非数値・範囲外USGS座標を除外することを確認。
- [ ] `test/test_spatial_geometry.py`で、日英4pageの経度・日付変更線・local kmと、
  日英Advancedの断面幾何caseに合格することを確認。
- [ ] `test/test_plate_boundary_fallback.py`で、実USGS plate serviceを使わず、正常、
  全面・部分失敗、不正response、日本限定fallback caseに合格することを確認。
- [ ] `test/test_app_smoke.py`で、日英Homeと現行4 visualizer pageが想定見出し・
  上下取得buttonを維持して例外なく起動することを確認。
- [ ] standalone公開cloneで`test/test_repository_health.py`に合格し、公開候補に加えて
  tracked fileの除外も確認。
- [ ] JMA/NIED source catalogが同梱されていないことを確認し、
  `docs/jma_nied_data_responsibilities_Japanese.md`で出典、加工表示、謝辞、DOI、
  成果報告、再配布責任を確認。
- [ ] CIテストはUSGSや地図タイルの実通信に依存しない。
- [ ] 公開物のファイル一覧とインポート/起動確認に合格。

## 手動スモーク

- [ ] 日英Home / Simple / Advancedが例外なしで開く。
- [ ] USGS取得、空結果、上限警告、CSV出力を確認。
- [ ] 2D/3D、断面、時間頻度、プレート境界の主要表示を確認。
- [ ] オンライン地図とオフライン海岸線を確認。
- [ ] 任意JMA/NIED比較をreleaseで有効にする場合のみ、uploadの正常系とerror表示を1回ずつ確認。

## 公開対象外

- [ ] `.DS_Store`、`__pycache__/`、`.pytest_cache/`、秘密情報、ログ、一時ファイルがない。
- [ ] `old/`、`__ToDo__/`、作業用DOCX、不要ロゴ、不要Seawaterサンプルがない。
- [ ] 絶対ローカルパス、token、非公開データがない。

## GitHub Release / Zenodo

- [ ] クリーンな公開commitとCI結果を確認。
- [ ] ZenodoでGitHubリポジトリをRelease作成前に有効化。
- [ ] 対象commitにバージョンtagを付けGitHub Releaseを作成。
- [ ] Zenodo recordのtitle、author、ORCID、affiliation、license、version、ファイルを確認。
- [ ] 発行されたversion DOIとconcept DOIを記録し、READMEとcitation metadataへ反映。
