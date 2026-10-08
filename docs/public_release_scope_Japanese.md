# EnvGeo-Earthquake 公開対象ファイル範囲

[English version](public_release_scope.md)

決定日: 2026-10-08

この文書は、最初の安定公開版に含めるソースの範囲を定めます。これは公開済みの
証拠ではなく、対象範囲の決定です。公開ロードマップに残るブロッカーは別途解消します。
EnvGeo-Seawaterは対象外とし、実行時依存先にしません。

## 公開版に含めるもの

### アプリと実行時データ

- `home.py`
- 継承したSeawater読込みと未公表データ参照を除去した後の`envgeo_utils.py`
- `pages/`内の現行5ファイル
- `coastline/world_coastline_coordinates_50m.csv`
- `coastline/world_coastline_coordinates_110m.csv`
- `coastline/LICENSE_OR_SOURCE.md`と
  `coastline/LICENSE_OR_SOURCE_Japanese.md`

### 実行環境、テスト、自動化

- `requirements.txt`、`requirements-dev.txt`、`runtime.txt`
- `.gitignore`
- `test/`内の維持対象ソース
- 今後追加する、実ネットワークに依存しないGitHub Actions workflow
- 後でinstall可能package配布を選ぶ場合のみ、package metadataとlauncher

### 法的文書、引用、維持管理、利用者向け文書

- `LICENSE`、`NOTICE.md`、`CONTRIBUTING.md`、今後追加する`CITATION.cff`
- `README.md`、`README_Japanese.md`、`TODO.md`、`TODO_Japanese.md`
- `PROJECT_STATUS.md`、`PROJECT_STATUS_Japanese.md`、`AGENTS.md`、`AGENTS_Japanese.md`
- `docs/`内の維持対象Markdown文書。日英の作業ログ、マニュアル、監査、ロードマップ、
  テスト説明、作業手順、リリースチェック、本決定を含む
- マニュアルが使用する`docs/assets/screenshots/en/*.png`と
  `docs/assets/screenshots/ja/*.png`
- `docs/capture_manual_screenshots.mjs`

新しいcloneやchatでも経緯と現状を再構成できるよう、作業ログと引継ぎ文書も公開対象に
含めます。各公開前に、機密情報、私的データ、マシン固有パスがないか確認します。

## 公開版から除外するもの

- `old/`: 開発履歴スナップショット、旧コード、可搬性の低いファイル名を含む
- `data/`: 現在はSeawaterサンプルと作業用spreadsheetだけで、Earthquakeの実行時入力ではない
- `__ToDo__/`: 非公開の作業メモ
- `__logo__/`、`images/`、その他のロゴ候補: 未使用のデザイン・説明素材。
  現在の公開対象にロゴ画像は含めない
- `.devcontainer/`: XSRF無効化設定を修正し、明示的に再確認するまでは最初の安定版から除外する
- `.DS_Store`、`__pycache__/`、`.pytest_cache/`、bytecode、test cache、coverage出力、build出力、
  log、一時ファイル、editor設定、仮想環境
- 機密情報、token、`.streamlit/secrets.toml`、私的データ、未公表ファイル名、ローカル絶対パス
- マシン固有パスとローカルGit運用ルールを意図的に保存する
  `LOCAL_WORKSPACE.md`と`LOCAL_WORKSPACE_Japanese.md`

除外する開発資料は作業フォルダ内では変更しません。この決定は、公開版へのcopy・追跡対象だけを
定めるものです。
上記の開発専用6 directoryは、root固定の`.gitignore`規則で除外します。
現行・testのPythonファイルに、これらのdirectory pathから始まる文字列参照はありません。

## 公開対象の合格条件

tag作成前に以下を満たします。

1. 公開対象のコードと文書は、除外directory内のファイルを必要としない。
2. repository-health testで許可対象を固定し、生成物、機密情報、絶対パス、不要データを拒否する。
3. 公開対象Markdownのローカルリンクがすべて解決する。
4. クリーンなcloneで、EnvGeo-Seawaterなしにアプリとテストが動作する。
5. GitHubのsource archiveを検査し、この範囲と一致する。

## 後で範囲を変更する場合

日英両版を同時に変更し、日英両方の作業ログに記録します。Core候補の移転は公開後の別決定であり、
この単独公開版からファイルや依存を暗黙に除去しません。
