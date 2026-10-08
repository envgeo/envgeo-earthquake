# EnvGeo-Earthquake 公開・共通コア監査

[English version](publication_audit_2026-10-08.md)

監査日: 2026-10-08（Asia/Tokyo）  
対象: `earthquake_map_v030` と `../envgeo_seawater_v130` の読取り専用比較

## 目的

- EnvGeo-Earthquakeを単独で実行・テスト・公開・Zenodo保存可能にする。
- 将来のEnvGeo Core候補を特定するが、現時点では抽出しない。
- EnvGeo-Seawater v1.3.5 / JOSS作業に影響を与えない。

## 結論

Earthquakeは主要機能、日英マニュアル、MIT License、基本テストを持つ。
ただし、単独化の残件、CIと配布metadataの欠如、Earthquake固有テストの不足、
海岸線出典の不足があり、現在はまだ公開候補である。

## 分類

### 将来のEnvGeo Core候補

- Streamlit互換ヘルパー、タブUI、アセット解決
- 地図背景、通信確認、オフライン縮退、海岸線、経緯線
- 経度正規化、日付変更線、地域プリセット構造
- ローカルkm座標変換と汎用3Dレイアウト
- 出典・引用・ライセンスmetadataと安全な出力ファイル名

### EnvGeo-Seawater固有

- 海水同位体・水理Excel統合、d-excess、塩分、水温
- Seawaterの物理範囲と品質フラグ
- GSW、Cartopy、GEBCO、海底地形補間
- 航海・観測点・測線filter、重複候補判定、Seawater upload統合

### EnvGeo-Earthquake固有

- USGS FDSN Event API、GeoJSON正規化、20,000件上限
- 地震の時刻、マグニチュード、震源深さ、並び順
- ホットスポット、プレート境界、地震断面、深度・時間頻度
- JMA/NIEDカタログ比較と速報値・改訂可能性の注意

### 現時点で共通化しないもの

- `load_*_data`: 同梱海水データとライブ地震APIで責務が異なる。
- filter: Seawaterは取得後データ、EarthquakeはAPI検索条件。
- quality flag: 海水物理範囲と地震カタログ審査状態は別定義。
- upload: 汎用観測表とJMA/NIEDカタログで列・単位・利用条件が異なる。
- cross-section: 幾何は候補だが、海底・水柱補間と震源分布は別層。
- 日英ページ重複: Earthquake内の保守性問題で、Coreの責務ではない。

## 主な公開ブロッカー

- 2026-10-08に開発フォルダで解消: アクティブ`envgeo_utils.py`から
  継承したSeawater loaderと未公表dataset参照を除去した。別の公開用cloneは
  ユーザー指示による反映待ち。
- 2026-10-08に開発フォルダで解消: Seawater依存の4件のskipを、実通信非依存の
  USGS GeoJSON contract testへ置換し、利用可能な全testは`49 passed, 0 skipped`。
- CI、`CITATION.cff`、配布metadata、配布物検査がない。
- 2026-10-08に開発フォルダで解消: 日英AdvancedのuploadをCSV、TSV、TXT、
  `.xlsx`に限定し、旧`.xls`の表示を除去した。`openpyxl`の宣言を維持し、
  memory内XLSX往復testを追加。不要な`xlrd`依存は追加していない。
- 日英検証方針を現状機能の維持に絞り込んだ。USGS catalog値は信頼し、
  公開整備は実際に確認したcrash/error経路とuploadの基本safetyに限定する。
  重複ID管理、issue code、dashboard、独自catalog等級は現在のblockerにしない。
- 2026-10-08に開発フォルダで解消: 不正USGS JSONとGeoJSON `features`がlistでない
  responseを、4画面が処理する読める`RuntimeError`へ変換。再現できたこ2 crashのみを
  実通信なしtestで確認した。loaderの正常、空、欠損、HTTP error、timeout、接続失敗も
  決定論的に確認した。後続で必須・任意query構築と4pageの取得上限境界も共通化・testし、
  実service非依存の全suiteは`73 passed, 0 skipped`。
- 2026-10-08に確認: JMA/NIED upload比較は任意機能で、最初release/DOIのゲートにしない。
  日英の正常CSV、必須列欠損、壊れたXLSXはすべて安全に終了した。互換性のため
  機能は変更せず、schema拡張も行わない。session-onlyの扱いを文書化した。日英pageの
  実helperに正常CSV 1件・必須列欠損CSV 1件の永続smoke testを追加し、全suiteは`77 passed`。
- 2026-10-08に開発フォルダで解消: 日英4 visualizer pageが経度±180°・緯度±90°の
  有効な境界点を保持し、欠損・非数値・範囲外USGS座標を描画前に除外するようにした。
  各pageの実helperを直接実行する8 testを追加し、全suiteは`85 passed`。
  任意upload正規化と日付変更線挙動は変更していない。
- 2026-10-08に開発フォルダで確認: 日英の該当pageすべてについて、経度ラップ、地図継ぎ目の
  分割、太平洋中心の連続性、日付変更線近傍local km、断面短経路、符号付き横ずれ、
  始終点一致、閉じた断面帯polygonを実helper 20 testで確認した。runtime code変更は不要で、
  全suiteは`105 passed`。
- 2026-10-08に開発フォルダで解消: plate serviceの不正GeoJSONをfeature変更時の例外にせず、
  既存のlayer error・fallback経路へ渡す。日本presetの全面失敗だけ明示的な模式fallbackを使い、
  日本以外は空のまま、microplate部分失敗は有効なUSGS main-plate dataを維持して正確な
  部分layer warningを表示する。日英13件の実通信なしtestで全suiteは`118 passed`。
- 2026-10-08に開発フォルダで完了: 日英Homeと現行4 visualizer pageの永続Streamlit AppTestを
  通常pytestへ組み込んだ。初期表示の例外0件、共通title、日英主要見出し、共通version表示、
  上下取得buttonを6 caseで保護する。runtime code変更はなく、全suiteは`124 passed`。
- 2026-10-08に開発フォルダで完了: portableなrepository-health test 8件で、公開allowlist・
  除外、ignore規則、standalone cloneのtracked file、runtime参照、一般的なsecret・秘密鍵pattern、
  機械固有絶対path、symlink、Markdown linkを保護する。作業folderの除外local資料は維持し、
  公開cloneは未変更。全suiteは`132 passed`。
- 2026-10-08にPhase 5前の追加調整として、日英4 visualizer pageを
  magnitude連動marker size既定とし、固定sizeも選択可能にした。主要2D・3Dと
  Advanced断面markerに同じ方式、M7:M4直径比1:1–30:1の調整、最大10倍の全体直接倍率を適用。
  40件の決定論的testにより
  全suiteは`172 passed`となった。公開cloneは未変更。
- 2026-10-08にPhase 5前の追加調整として、日英4 visualizer pageの主要3D図前に
  Plotly camera操作案内を追加。drag、回転・平行移動・zoom・reset、modifier key、
  browser・OS差を含み、macOS実機確認に基づいてOption（Alt）も明記した。
  4 contractにより全suiteは`176 passed`。公開cloneは未変更。
- 2026-10-08に開発フォルダで解消: JMAの出典・加工表示・第三者権利条件と、
  NIED Hi-netの利用登録、再配布禁止、提供機関謝辞、DOI引用、成果報告要件を分けた
  日英責任記録を追加。提供元catalogは同梱せず、metadata/記録contractを含む全suiteは
  `61 passed`。
- 2026-10-08に確認: active codeの標準地図はCARTO basemapではなくPlotlyの
  OpenStreetMap標準style。USGS imagery、Esri World Ocean Base、GSIのcreditを
  提供元資料に合わせ、Earthquake内へ集約した。tile選択・endpointは変更せず、
  静的出力の注意と実通信なしattribution contractを追加した。
- 2026-10-08に開発フォルダで解消: byte一致する両海岸線CSVをNatural Earth coastline
  v4.1.0由来と特定する日英の同梱記録を追加し、出力hashと保持中間workbookの根拠を保存した。
  元raw downloadのhashと正確な日付が未保持である制約も明記した。
- 2026-10-08に開発フォルダで解消: FDSN記載のANSS Comprehensive Catalog引用と、
  USGS plate service metadataが示すBird (2003) / DeMets et al. (2010)引用をlocal utilityへ
  集約し、該当する日英pageで共通参照した。決定論的contract testでpage間の表記ずれを防ぐ。
- 2026-10-08に開発フォルダで解消: 実行時のversion metadataを
  `envgeo_utils.py`1か所に定義し、日英Homeと4つの可視化ページが参照する。
  ローカル文字列の再定義をcontract testで防止し、全testは`50 passed, 0 skipped`。
- 2026-10-08に開発フォルダの公開追跡方針で解消: root固定のignore規則で
  開発archive、ローカルdata/assets、cache、OS生成物を除外した。元資料はローカルに維持する。
- 2026-10-08に開発フォルダで解消: 同梱海岸線CSVと日英Home内READMEを
  source file基準で解決する。project外へcurrent directoryを変更した後の実読込みを
  testし、全testは`53 passed, 0 skipped`。

## 最小公開計画

1. Earthquakeだけの公開用Gitリポジトリと公開対象を固定。
2. Seawater読込みとskipテストをEarthquake contractテストで置換。
3. 出典、取得時刻、query URL、アプリversionの保存方針を固定。
4. 焦点を絞ったAPI・幾何・AppTestとPython 3.10/3.12 CIを追加。任意uploadはreleaseで有効にする場合のみtestする。
5. `CITATION.cff`、リリースmetadata、公開対象検査を追加。
6. Streamlit公開環境で手動スモークを実施。
7. ZenodoでGitHubリポジトリを有効化後、CI合格commitをtag/Releaseして保存。
8. 発行DOIをREADME、citation metadata、リリース記録に反映。

## 監査証拠

- 50mと110m海岸線CSVは両プロジェクトでそれぞれ同一。
- `apply_common_layout`、`get_custom_colorscale`、`insert_gap_rows`はAST上同一だが、それだけで抽出しない。
- 日英Simple / Advancedページは異なる行集合の約87%を共有。
- 現行のアクティブ/テストPython 11ファイルは構文解析に成功。
- 監査Pythonにpytestがなく、全pytestは未実行。
