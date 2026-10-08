# EnvGeo-Earthquake TODO（日本語版）

英語版: [TODO.md](TODO.md)

原則として、この日本語版と英語版の内容を対応させます。ユーザー向けUI、README、マニュアル、テスト説明、リリースノート、および主要な開発方針は、日本語・英語の両方で維持します。

## 現在の基本方針

- 現状の機能と挙動を維持し、安定動作、正確な文書、test、配布、releaseに本当に必要な変更だけを追加する。
- 日常的な編集は開発用作業フォルダで行う。
- レビューとテストを終えた変更だけをGitクローンへコピーしてcommitする。
- ユーザー向けの挙動、文言、データソース、テスト、操作手順を変更した場合は、README、README_Japanese、Homeの更新履歴、`docs/`も更新する。
- 可能な限り、対応する英語・日本語文書を同時に更新する。開発途中で一方を先に更新する必要がある場合は、未翻訳項目をフォローアップとして記録し、次の公開リリースまでに同期する。
- UIの雰囲気と操作の流れはEnvGeo-Seawaterに近づける一方、地震固有の処理はEarthquake側に維持する。
- 移行期間中は、検証済みのStreamlit 1.42環境と、Streamlit 1.63 / Plotly 5比較環境の両方で互換性を確認する。

## 直近の作業

- [ ] `PROJECT_STATUS.md` と `docs/publication_audit_2026-10-08.md` に記録した
  単独公開ゲートを、EnvGeo-Seawaterを変更・依存先化せず完了する。
  - [x] Earthquakeのアクティブutilityから、継承したSeawater dataset読込みと
    未公表dataset参照を除去または隔離する。開発フォルダで完了し、
    公開用cloneへの反映はユーザー指示待ち。
  - [x] Seawater dataset不在時にskipする4テストをEarthquake contractテストへ置き換える。
  - [x] 実行時のversion metadataを`envgeo_utils.py`に集約し、日英Homeと4つの現行可視化ページで共通参照を強制する。
  - [x] project外のcurrent directoryから、同梱海岸線と日英Home内READMEの読込みを確認する。
  - [x] 日英Advancedのuploadから旧`.xls`を外し、CSV、TSV、TXT、`.xlsx`対応を維持・testする。
  - [x] 現状挙動を維持し、推測的なvalidation機能を後回しにする日英の最小検証方針を定義する。
  - [x] 現行USGS失敗経路を監査し、再現した不正JSONと不正`features`のcrashを、既存pageが処理する`RuntimeError`経路へ変換する。
  - [x] 任意JMA/NIED uploadを監査。正常CSV、必須列欠損、壊れたXLSXは日英とも安全に処理される。拡張せず維持し、最初release/DOIのゲートにしない。
  - [ ] 実ネットワーク非依存のPython 3.10/3.12 GitHub Actions CIを追加する。
  - [x] 同梱海岸線CSVへNatural Earth v4.1.0の派生根拠、出力hash、raw download記録上の
    制約を含む出典・ライセンス情報を追加する。
  - [x] USGS/ANSS catalogとUSGS plate-boundaryの引用文を共通定義へ集約し、
    日英Home、Simple、Advanced、README、manualで同期する。
  - [x] online地図の出典表示を再確認する。標準地図がCARTOではなくOpenStreetMapで
    あることを確認し、USGS imagery、Esri Ocean、GSIの実行時creditと日英案内を
    提供元資料に合わせる。
  - [x] JMAとNIEDの責任を分けて記録する。JMAの出典・加工表示・第三者権利確認と、
    NIEDの再配布禁止、提供機関謝辞、DOI引用、利用登録、成果報告を明記する。
  - [x] 現行pageのerror処理を変えず、USGS loaderの正常、空、欠損、不正JSON/GeoJSON、
    HTTP error、timeout、接続失敗を実通信なしtestで完成させる。
  - [x] USGS query構築と、日英4 visualizer pageが使う取得上限境界を純粋helperへ
    切り出してtestする。warning文言・表示時点は変更しない。
  - [x] 日英Advancedの実際のupload helperを、正常CSV 1件と必須列欠損CSV 1件で
    smoke testする。alias・schemaは変更しない。
  - [x] 日英4pageの実際の描画準備helperをtestし、境界上の座標は保持したまま、
    USGS GeoJSONの欠損・非数値・範囲外座標を描画前に除外する。
  - [x] 日英Advancedのplate-boundary loaderを、実通信なしで2layer正常取得、全面・部分失敗、
    不正GeoJSON、日本限定fallback、正確な部分data warningについてtestする。
  - [x] 日英Homeと現行4 visualizer pageについて、主要見出しと上下取得buttonを含む
    永続startup AppTestを追加する。
  - [x] 公開allowlist・除外、秘密情報・秘密鍵pattern、機械固有絶対path、symlink、
    runtime参照、Markdown linkのportable repository-health testを追加する。
  - [x] Phase 5前に、日英の固定・マグニチュード連動のmarker size切替を追加する。
    既定はマグニチュード連動とし、M7:M4直径比を調整可能にする。主要2D・3D・Advanced断面表示に
    標準の最大10倍の全体直接倍率を適用して、決定論的testを追加する。
  - [x] EnvGeo-Seawaterの文言を踏襲し、日英4 visualizer pageの主要3D図直前に、
    Shift / Control / Option（Alt） / Command・browser・OS差を含む簡潔なPlotly 3D camera操作案内を追加する。
  - [ ] `CITATION.cff`、リリースmetadata、公開対象検査を追加する。
  - [x] `old/`、cache、OS生成物、作業用文書、不要データを公開リリースから除外する。開発専用directoryはroot固定のignore規則で除外し、ファイル自体は開発フォルダに維持する。
  - [ ] tag作成前に日英Home / Simple / Advancedの公開環境スモークを実施・記録する。
- [ ] Plotly 5.24を検証済み基準として、Python 3.10-3.12 / Streamlit 1.42-1.63互換の0.3.2について残りの画面確認を完了し、その後に公開を判断する。
- [ ] 別途設計レビュー後、50m／110m海岸線CSVとキャッシュ読込を`envgeo-core`へ集約する。SeawaterとEarthquakeの両方で読込・画面確認が独立して合格するまで、各アプリ内のCSVを維持する。
  - [x] `requirements.txt`でStreamlit 1.42-1.63を許容し、新規デプロイでは1.63が選択される設定へ更新する。
  - [x] Streamlit 1.63の Session State / `value=` 二重指定警告を断面図入力（page 55・57）で解消: ウィジェット直前でSession Stateを初期化し、`value=` 引数を削除。
  - [x] Advancedページ（page 55・57）にフォーム上部の取得ボタンを追加（seawaterパターンに準拠）: キャプション直下に上部ボタン（ラベルに `!` なし）、フォーム末尾に下部ボタン（ラベルに `!` / `！` あり）、両ボタンとも `use_container_width=True`。
  - [x] Simpleページ（page 54・56）にも同じ上下ボタン構成を適用。page 54 にはキャプションが未設置だったためヘッダー直下に追加。全4ページ統一。
- [ ] MapboxトレースをPlotly 5.24で利用できるMapLibre APIへ移行し、同じ実装をPlotly 6.7および7.1でも確認する。
- [ ] 対応バージョン範囲全体を検証済みとする前に、Python 3.10 / Streamlit 1.63 / Plotly 7の交差環境テストを追加する。
- [ ] 大規模リファクタリングの前に、2026-09-17の外部レビューで確認した低リスク修正を反映する。
  - [x] NaNに安全なフィルタ範囲: スライダー最小・最大値算出に `.dropna()` を追加（4箇所）。
  - [x] 重複した地図スタイル呼び出し: 無条件の `carto-positron` 行を削除し、`open-street-map` へ切り替え。
  - [x] Advancedページで欠けているAbout URL: page 55 に追加し page 54 と統一。
  - [ ] NaNに安全な統計（`np.mean` → `np.nanmean`）: `envgeo4d` 統合時に対応。
  - [ ] 空データ判定のbool化: `envgeo4d` 統合時に対応。
  - [ ] 未使用変数（`Transect_list`）: `envgeo4d` 統合時に対応。
- [ ] API障害、不正なGeoJSON、フィルタ範囲、科学・空間処理ヘルパーについて、Earthquake固有のテストを拡充する。
- [ ] UI変更後にStreamlitを起動し、Region / hotspot選択の挙動を画面で確認する。
- [ ] 日本語・英語ページの文言をブラウザ上で確認する。
- [ ] Simple / Advancedページ用の短いスクリーンショット・手動QAチェックリストを追加する。
- [ ] Region選択の状態管理を、テスト可能なヘルパー関数へ移すことを検討する。
- [x] 経度ラップ、日付変更線の連続・継ぎ目、ローカルkm座標、日英Advancedの
  断面図ジオメトリのテストを拡充する。
- [x] JMA/NIED比較uploadの説明と受付列を見直し、現行alias/形式は変更せず任意機能に分類する。
- [x] `old/`、`data/`、`__logo__/`、画像素材を公開GitHubリポジトリへ含めるか判断する。`docs/public_release_scope_Japanese.md`に基づき除外し、マニュアル用screenshotだけを含める。

## ドキュメント・テスト方針

採用日: 2026-09-19

JOSS対応を想定した外部レビューから有益な部分を、EnvGeo-Earthquakeに合う形で採用する。大規模なUI統合とは分け、段階的に進める。

ドキュメント方針:

- ドキュメントサイト生成ツールを導入する前に、既存の英語・日本語Markdownマニュアルを完成させる。インストール、クイックスタート、USGS検索、Simple / Advancedワークフロー、JMA/NIED比較データ、書き出し、制約、トラブルシューティング、テスト、コントリビューション、サポートを対象とする。
- 将来のGitHub PagesドキュメントサイトにはMkDocsを第一候補とし、EnvGeo-Seawaterおよび共通`envgeo4d`コアと、構成・デザインを共有できる形を目指す。
- APIリファレンスは、USGSデータ正規化、海域・地域プリセット、経度・日付変更線処理、ローカル座標変換、断面図ジオメトリ、データソース情報など、安定した再利用可能ヘルパーだけを対象にする。

テスト方針:

- 科学・空間処理の主な確認には純粋関数のpytestを使用し、UIワークフローには永続的な`streamlit.testing.v1.AppTest`テストを追加する。
- AppTestは日英Homeと日本語・英語のSimple / Advancedの起動確認を開始済み。今後は
  Region / hotspot操作、フィルタ適用、抽出結果0件、メッセージ、ダウンロード、session stateを確認する。
- 自動テストではUSGS応答をモックする。CIで実サービスへ依存せず、正常、空、不正形式、タイムアウト、レート制限、その他のAPI障害を確認する。
- JMA/NIEDアップロードについて、想定内・想定外の列名、不正ファイル、座標欠損、NaN、日付変更線付近のデータをテストする。
- Plotly/WebGL描画、地図タイル、選択ツール、3Dカメラ、最終スクリーンショットの見た目は、短い手動視覚QAチェックリストで確認する。
- 代表的なAppTest群が安定した後にGitHub Actionsへ組み込む。可能な範囲でSeawaterと同じPython / Streamlit互換方針を使用し、Earthquake固有のネットワークテストは常に再現可能な形にする。

JOSS・共通コアに関する注意:

- ドキュメントとAppTestは、パッケージ化、CI、コントリビューション・サポート案内、公開リリース履歴、研究利用実績、AI支援開発の開示を含む、より広いリリース品質向上の一部として扱う。
- ヘルパー関数を`envgeo4d`へ移す場合は、対応する単体テストとAPI文書も一緒に移す。Earthquake固有のページワークフローテストはEnvGeo-Earthquake側に残す。

## 共通コア候補

現在の方針では、英語・日本語、Simple / Advancedの4ページは当面分離したまま維持する。ページUI全体を一度に統合せず、十分に理解できている純粋関数だけを小さな単位で抽出し、対象を絞ったテストを追加して、抽出ごとに4ページすべてを確認する。

- [ ] 地図背景の選択と出典表示。
- [ ] Region preset処理。
- [ ] 海岸線データ読込。
- [ ] 経度ラップと日付変更線処理。
- [ ] ローカルkm座標への変換。
- [ ] 断面図ジオメトリのヘルパー。
- [ ] データソース・引用情報の表示。
