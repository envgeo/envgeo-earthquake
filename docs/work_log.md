# EnvGeo-Earthquake 作業記録

## 運用方針

- 作業の本体は `earthquake_map_v030` で行う。
- 作業フォルダで構文確認、pytest、必要に応じた Streamlit 画面確認を行ってから、Git clone へコピーする。
- README、README_Japanese、Home の更新履歴、docs は、機能変更やUI文言変更に合わせて随時更新する。
- `.DS_Store`、`__pycache__/`、`.pytest_cache/` などの生成物は Git clone へコピーしない。
- EnvGeo-Seawater と将来の共通コア化を意識しつつ、Earthquake 固有処理は無理に共通化しない。

## 2026-09-16

- README と Home の説明を、EnvGeo-Seawater の研究アプリとしての雰囲気に合わせて整理した。
- EnvGeo-Seawater との関係、将来の EnvGeo 共通コア候補、Earthquake 側に残すべき固有処理を README / README_Japanese に明記した。
- ページ名と説明を現行構成に合わせ、英語版・日本語版の Simple / Advanced ページ名を README に反映した。
- 日本語表現を整理し、`地理分布図` を `2D 震源マップ`、`簡易版` を `基本版`、`発展版` を `詳細版`、`簡易地震可視化アプリ` を `地震カタログ探索アプリ` へ修正した。
- Region 選択UIで、デフォルトが日本周辺の場合にチェックボックスも日本周辺へ同期するようにした。
- hotspot 選択時に selectbox と重複して表示されていた `Selected hotspot` / `選択中の地震多発域` caption を削除した。
- `test/test_envgeo_utils.py` に USGS GeoJSON 正規化テストを追加し、Earthquake に同梱されていない Seawater データセット確認は skip するようにした。
- 作業フォルダで AST 構文確認と `pytest -q` を実行し、`9 passed, 4 skipped` を確認した。
- Git clone は `/Users/toyoho/Documents/GitHub/envgeo-earthquake`。作業フォルダで確認後に必要ファイルだけコピーする運用とする。
- `.gitignore` を拡張し、`requirements.txt` を実行用依存関係として整理、`requirements-dev.txt` をテスト用に追加した。
- `NOTICE.md` を追加し、MIT License はアプリコードに適用し、外部データ・地図タイル・カタログサービスは各提供元条件に従うことを明確化した。
