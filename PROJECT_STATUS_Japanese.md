# EnvGeo-Earthquake: 現状と引継ぎ

[English version](PROJECT_STATUS.md)

最終更新: 2026-10-08（Asia/Tokyo）

新しいchatや開発作業では、最初にこのファイルを読みます。時系列の証拠は
日英両方の作業ログに残します。

## 現在の目標

1. EnvGeo-Earthquakeを、EnvGeo-Seawaterに実行時依存しない安定した単独アプリとして公開する。
2. GitHub ReleaseとZenodoアーカイブを一致させ、バージョンDOIを取得する。
3. 将来のEnvGeo Core候補を記録するが、現在はCore抽出や共通依存追加を行わない。
4. EnvGeo-Seawater v1.3.5とJOSS作業に影響を与えない。

## 現在の判定

- 開発バージョン: `0.3.2`（2026-09-22）
- ステータス: **公開候補だが、まだZenodoリリース可ではない**
- 利用可能なtest環境で`176 passed, 0 skipped`を確認済み。
  現行・testのPython 20fileもすべて構文解析に成功した。
- USGS失敗経路の焦点監査で、不正JSONが`JSONDecodeError`、`features`がlistでない
  responseが`AttributeError`になる2つの未処理crashを再現した。共通loaderで両方を
  4画面が既に処理する読める`RuntimeError`へ変換し、実通信なしtestを追加。
  共通loaderは正常、空、欠損、HTTP error、timeout、接続失敗も実serviceなしで確認した。
  query構築と共通取得上限境界も決定論的にtestした。日英任意upload smoke経路、
  4pageの欠損・範囲外座標guard、日英空間幾何、plate fallback、page startup AppTest、
  repository health、marker size方式、日英Plotly視点操作案内も永続化し、
  全suiteは`176 passed`となった。
- この作業フォルダはGitリポジトリではない。別の公開用Git cloneとremoteは確定済みで、
  マシン固有情報は公開対象外の`LOCAL_WORKSPACE`日英ファイルに保存した。
- 2026-10-08、userの明示指示後、review済み公開対象fileをPhase 5前checkpointとして
  別のGit cloneへ反映した。開発専用directory、local workspace記録、cache、OS生成物は
  除外した。cloneは`86b2d54`を基点とする`main`のままで、同期差分はGitHub Desktopでの
  review用に意図的に未commit・未pushである。clone自身の読取り中心testは`176 passed`。
- 2026-10-08に、未使用の`load_isotope_data()`とその内部のSeawater Excel読込み・結合処理を
  開発用utilityから除去した。変更前後とも全testは`45 passed, 4 skipped`、現行・testの
  Python 11ファイルはすべて構文解析に成功した。
- 試行したHome上部ロゴは、地球図の正確性とページバランスの再検討後に撤去した。
  日英Homeは再びアプリ名から開始し、現在の公開対象にロゴassetは含まない。
  候補は将来の小型icon・背景検討用に、公開対象外の`__logo__/`だけに残す。
- 実行時のversion metadataは`envgeo_utils.APP_VERSION`と`APP_VERSION_DATE`に
  集約済み。日英Homeと4つの現行可視化ページが共通定義を参照し、
  contract testがローカル文字列の再定義を検出する。
- 同梱の50m / 110m海岸線CSVと日英Home内READMEはsource file rootから解決する。
  `test/test_asset_paths.py`は一時current directoryへ移動し、実際の読込み・描画を
  確認するため、processのcurrent directoryに依存しない。
- 日英の記録で、両海岸線CSVをNatural Earth coastline v4.1.0由来と特定し、
  SHA-256を記録した。この判断はSeawaterが保持するsource workspace・中間workbookの
  監査と、Earthquake側2fileのbyte一致に基づく。元raw downloadのchecksumと正確な
  download日は未保持。map挙動とdata fileは変更していない。
- USGS引用文を`envgeo_utils.py`へ集約した。FDSN記載のANSS Comprehensive Catalog引用と、
  USGS plate service metadataが示すBird (2003) / DeMets et al. (2010)を、日英Home、
  Simple、Advancedが共通参照する。contract testでlocal textのずれを防ぐ。
- online地図のsourceと実行時creditを`envgeo_utils.py`へ集約した。標準地図は
  PlotlyのOpenStreetMap styleのままでCARTO basemapは使用しない。衛星、海底地形、
  地形図は監査済みのUSGS/USDA、Esri contributors、link付きGSI creditを表示し、
  実通信なしcontract testでURLとattributionを固定した。地図選択とtile endpointは変更なし。
- JMA/NIED責任metadataと専用の日英記録を追加し、提供元の違いを明確化した。JMAは
  一般website条件の下で出典・加工表示が必要。NIED Hi-netはsource data再配布を禁止し、
  利用登録・提供機関謝辞・DOI引用・成果報告を求める。JMA/NIED catalogは同梱・永続保存しない。
- 日英AdvancedのカタログuploadはCSV、TSV、TXT、`.xlsx`を受け付ける。
  別のreader依存が未導入の旧`.xls`は表示しない。contract testで両画面と
  `requirements.txt`の一致、`openpyxl`によるmemory内XLSX往復を確認する。
- 日英検証方針を、現状挙動を維持する最小内容へ絞り込んだ。USGS値は
  source dataとして信頼し、crash防止、明確な失敗処理、利用者uploadの基本checkのみを
  現在の要件とする。複雑なissue code、重複ID管理、validation dashboardは、
  具体的な不具合が示されない限り後回しにする。
- Advanced pageのJMA/NIED uploadは、中核USGS workflowまたは最初release/DOIのゲートではない
  「任意の現状維持機能」に分類した。正常CSV、必須列欠損、壊れたXLSXを日英実装で
  直接確認し、未処理例外なし。runtime codeは変更せず、schema拡張も行わない。
  マニュアルに、アプリがupload内容を現在のsessionを超えて意図的に永続保存しないことを明記した。
- 日英4 visualizer pageは、USGS描画座標を数値化し、経度±180°・緯度±90°の有効な
  境界点を保持したまま、欠損・非数値・範囲外座標を描画前に除外する。各pageの実helperを
  8 testで直接確認した。JMA/NIED upload正規化と経度・日付変更線表現は今回変更していない。
- 日英4pageの実際の経度ラップ、地図継ぎ目line、local km helperを直接testした。
  日英Advancedでは、日付変更線をまたぐ断面の短経路、断面距離・横ずれ、始終点一致、
  閉じた断面帯polygonも確認した。20件の追加testにruntime code変更は不要だった。
- 日英Advancedのplate loaderは、`features`がlistでない場合やfeatureがobjectでない場合を
  未処理例外でなく読めるlayer errorにする。全面失敗時は日本presetだけ既存模式線を使い、
  microplateだけ失敗した場合は取得済みUSGS main-plateを維持して正確な部分data warningを
  表示する。13 testは実networkを使わない。
- `test/test_app_smoke.py`を通常pytestへ組み込み、日英Homeと現行4 visualizer pageを
  Streamlit AppTestで確認する。初期表示の例外0件、共通app title、言語別見出し、version表示、
  上下取得buttonを保護する。実取得・filter・download操作は後続coverageとして分ける。
- `test/test_repository_health.py`は、除外local資料を削除せずportableな公開候補viewを作る。
  許可root構成、`.gitignore`、standalone cloneのtracked除外、runtime参照、一般的なsecret・
  秘密鍵pattern、機械固有絶対path、symlink、Markdown linkを8 testで保護する。
- Phase 5の前に、日英4 visualizer pageへmarker size方式を追加した。既定は
  `マグニチュード連動`、任意で`固定サイズ`に切り替えられ、主要2D・3Dと
  Advanced断面表示へ同じ選択を適用する。全体倍率は`1.0`を標準に`0.2–10.0`の直接倍率とする。
  別の`マグニチュード強調率`でM7:M4のmarker直径比を`1–30`、既定`20`で調整できる。magnitude連動は
  指数的な表示強調を使い、倍率`1.0`でM7のmarker直径をM4の約20倍とする。これは
  energyや断層面積の物理scaleではない。日英既定、2方式、3表示profile、20倍応答を40 testで保護する。
- 日英4 visualizer pageの主要3D図直前に、drag回転、Plotly toolbarの回転・平行移動・
  zoom・reset、Shift / Control / Option（Alt） / Commandとmouseの組合せによる視点・中心操作と
  browser・OS差の簡潔な案内を追加した。

## 公開前の必須ゲート

1. **開発フォルダで完了:** Seawater dataset読込みと未公表dataset参照を
   Earthquakeのアクティブコードから除去した。公開用cloneはユーザー指示による反映待ち。
2. **完了:** Seawater不在時にskipしていた4テストを、実通信非依存の
   USGS GeoJSONの行数・schema・数値・時刻contract testへ置き換えた。
3. **最小範囲で完了:** USGS不正response guardは実通信なしtestで確認。任意uploadの3代表caseに未処理失敗がなく、推測的なcodeは追加しなかった。
4. Python 3.10 / 3.12のネットワーク非依存CIを追加する。
5. **完了:** 海岸線CSVのNatural Earth出典・ライセンスを同梱する。
6. `CITATION.cff`、確定リリースノート、Zenodo metadataを追加する。
7. **開発側で完了:** root固定のignore規則で`old/`、`data/`、`__ToDo__/`、
   `__logo__/`、`images/`、`.devcontainer/`を除外し、生成物は別規則で除外した。
   ローカルファイル自体は削除していない。
8. 日英各ページ、USGS取得、オフライン地図、upload、CSV出力の手動スモークを記録する。

## 境界と共通化方針

- 当面の変更先は`earthquake_map_v030`のみ。
- EnvGeo-Seawaterのsection comment方式を踏襲し、主要コードsectionは簡潔な
  `English / 日本語`見出しと、必要な日英目的説明を持つ。新規・変更箇所から適用し、
  無関係な一括書換えは行わない。
- Seawaterの品質フラグ、filter、uploadをそのままEarthquakeへコピーしない。
- Core候補: アセット解決、Streamlit互換UI、地図モード、海岸線、経度/日付変更線、ローカルkm座標、出典metadata。
- Earthquake固有: USGS query/GeoJSON、マグニチュード・深さ・時間、プレート境界、地震断面、JMA/NIED比較、速報値の注意。
- 詳細は`docs/publication_audit_2026-10-08_Japanese.md`を参照。

## 次の推奨作業

公開スコープ、Git cloneの場所、旧Seawater dataset読込みの除去、未公表参照の
監査、skip testの置換は開発フォルダで完了しました。次は、開発フォルダから
削除せずに、不要なSeawaterサンプルと開発archiveも公開対象から除外しました。
試行したHomeロゴは評価後に撤去し、現在の公開対象にロゴassetはありません。
実行時version metadataの集約、source相対のasset読込み、upload形式と依存の
整合も完了し、ロードマップPhase 1が完了しました。Phase 2の最初の項目である
現状維持を優先する最小検証方針の定義も完了しました。焦点を絞ったUSGS失敗監査で、
再現できた不正responseの2 crash経路のみ修正済みです。任意JMA/NIED uploadの監査は
code変更不要で、合意した最小範囲でPhase 2は完了しました。Phase 3の最初の項目も完了し、
Natural Earth v4.1.0の来歴、public-domain条件、checksum、保持された派生根拠、記録上の制約を、
同梱記録、NOTICE、日英README、Home・Advancedの出典表示で同期しました。USGS catalogと
plate-boundaryの引用文も共通化・同期済みです。online地図attribution監査もmap選択挙動を
変えず完了し、文書だけに残っていたCARTO表記も訂正しました。JMA/NIEDの利用・再配布責任も
別々に記録し、Phase 3は完了です。Phase 4では、実通信なしUSGS response・失敗、query構築、
4pageの取得上限warning境界をtest済みです。任意JMA/NIED比較もschemaを広げず、日英で
正常CSV 1件と必須列欠損CSV 1件の永続smoke testを追加しました。地震座標のNaN・非数値・
範囲外値も日英4pageでtest・guard済みです。経度ラップ、日付変更線、ローカルkm、
断面幾何もruntime codeを変えずtest済みです。プレート境界の正常、全面・部分失敗、
不正response、日本限定fallbackもtest済みです。日英Homeと現行4 visualizer pageの
永続startup AppTestも追加済みです。repository-health testも完了し、Phase 4は完了です。
次はPhase 5として、Python 3.10 / 3.12の実network非依存GitHub Actions CIを追加します。
ユーザーの明示的な指示なしに公開用cloneへcopyしません。commitとpushはユーザーが
GitHub Desktopで行います。

## 記録の更新ルール

- 毎回の実質的作業: `docs/work_log.md` と `docs/work_log_English.md`
- 現状・ブロッカー・次の一手: 日英の`PROJECT_STATUS`
- 優先順位: `TODO.md` / `TODO_Japanese.md`
- ユーザー操作: 日英マニュアル、README、Home履歴
- 公開判定: 日英の`docs/release_checklist`
- 作業手順: 日英の`docs/development_workflow`
