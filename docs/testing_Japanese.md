# テスト説明

[English version](testing.md)

この文書では、EnvGeo-Earthquake の現在の pytest 群が何を確認しているか、また今後どこを拡充すべきかを説明します。

## 実行方法

プロジェクトのルートディレクトリで実行します。

初回、または依存関係を更新した後は、開発用 requirements をインストールします。

```bash
pip install -r requirements-dev.txt
```

```bash
pytest -q
```

## GitHub Actions

`.github/workflows/ci.yml`は、同じ決定論的testをPython 3.10と3.12で実行します。
全suiteの前に、現行・test Python fileの構文解析とrepository-health checkを別stepで
実行します。runtime testはmockまたはlocal responseを使用し、実USGS、tile、JMA、NIEDへの
接続を必要としません。

workflowのrepository権限はread-onlyです。local contract testにより、Python matrix、
構文確認、公開内容検査、test commandを保護します。

AppTestは上下2つの取得・更新buttonを順序付きで必須とします。Streamlit 1.63では同じ起動run中に
後段のsidebar cache-clear buttonも現れる場合がありますが、1.51では初期空resultのため到達しない場合が
あります。smoke contractは既知の任意3番目buttonだけを許容し、任意のUI追加は許容しません。

`.pyc` を作らない構文確認を行う場合は、次を使います。

```bash
python -c "import ast, pathlib; files=[pathlib.Path('home.py'), pathlib.Path('envgeo_utils.py'), *pathlib.Path('pages').glob('*.py'), *pathlib.Path('test').glob('*.py')]; [ast.parse(p.read_text(encoding='utf-8'), filename=str(p)) for p in files]; print(f'parsed {len(files)} files')"
```

## 現在のテスト

### `test/test_basic.py`

- `envgeo_utils` を import できること。
- `envgeo_utils.version` が存在すること。
- `APP_VERSION`と`APP_VERSION_DATE`が有効で、日英Homeと4つの可視化ページが
  共通定義を参照し、ローカルなversion文字列を再定義していないこと。
- FDSN記載のUSGS catalog引用とUSGS metadata記載のplate-boundary引用をutilityで
  一元管理し、該当する日英pageが共通定義を参照すること。
- 標準地図が`open-street-map`を維持し、USGS imagery、Esri Ocean、GSIのtile URLと
  実行時attributionが共通定義と一致すること。
- JMA/NIEDの公式参照・NIED DOIが共通定義にあり、日英Homeと専用責任記録が
  それらを維持すること。

### `test/test_envgeo_utils.py`

現在は、主に次を確認しています。

- USGS GeoJSONの1 featureが1行として保持され、欠損featureでも安全に処理されること。
- pageとCSV出力が使用するUSGS列名・列順が安定していること。
- 数値文字列と不正数値が適切に数値・欠損値へ変換されること。
- USGSのmillisecond時刻からUTC、日付、年月日時が一貫して生成されること。
- 不正JSONと`features`がlistでないUSGS responseが、pageで処理可能な
  `RuntimeError`へ変換されること。
- 共通USGS loaderが正常・空・欠損payloadを処理し、HTTP error、timeout、接続失敗を
  pageで処理可能な`RuntimeError`へ変換すること（実通信なし）。
- USGS query URLが必須・任意parameterと日時・limit・orderbyを正しく構築し、未指定・
  NaNの任意値を除外すること。
- 取得行数が指定limit以上のときだけ上限warning条件が成立し、日英4pageが共通判定を使うこと。
- `insert_gap_rows()` が観測グループの切れ目で空白行を挿入すること。
- 深度用・通常用のカラースケールが返ること。
- 海岸線座標が経度・緯度の同じ長さのリストとして読み込めること。
- USGS GeoJSON FeatureCollection が、`Longitude_degE`、`Latitude_degN`、`Depth_km`、`Depth_m`、`Magnitude` などの列を持つ DataFrame に正規化されること。
- 空の USGS GeoJSON payload でも、期待される列を持つ空 DataFrame が返ること。

### `test/test_asset_paths.py`

- project外のcurrent directoryから、50m / 110m海岸線CSVを実際に読み込めること。
- project外のcurrent directoryから、日英Homeが同梱READMEを描画できること。

### `test/test_upload_formats.py`

- 日英Advancedのupload受付形式がCSV、TSV、TXT、XLSXのみであること。
- `requirements.txt`が`openpyxl`を含み、使用しない`xlrd`を含まないこと。
- memory内のXLSX workbookを`openpyxl`で書き込み・読み込みできること。
- 日英Advancedの実際のupload helperが、代表的な正常CSVを標準化できること。
- 必須列が不足するCSVを、日英とも例外ではなく空結果とwarningで処理すること。

### `test/test_page_coordinates.py`

- 日英Simple / Advancedの4pageから実際の`prepare_plot_dataframe()`を抽出して実行すること。
- 経度±180°・緯度±90°の境界上は保持し、欠損・非数値・範囲外座標は描画前に除外すること。
- 全行が不正座標でも例外を出さず、描画対象0行を返すこと。

### `test/test_spatial_geometry.py`

- 日英4pageの実helperで、選択中央経線に対する経度ラップを確認すること。
- 地図の継ぎ目では線を分割し、太平洋中心では日付変更線をまたぐ線を連続させること。
- 日付変更線両側の点を近接したlocal km座標へ変換すること。
- 日英Advancedで170°E→170°Wを20°の短経路として扱い、断面方向距離・横ずれ、
  始終点一致時の安全な空結果、閉じた断面帯polygonを確認すること。

### `test/test_plate_boundary_fallback.py`

- 日英Advancedの実loaderで、main plate・microplateの正常取得とlayer識別を確認すること。
- USGS service全面失敗時は日本queryだけ模式fallbackを使い、他地域には表示しないこと。
- `features`がlistでない場合とfeatureがobjectでない場合を未処理例外にしないこと。
- microplateだけ失敗した場合は取得済みmain plateを維持し、fallbackと誤表示しないこと。

### `test/test_app_smoke.py`

- 日英Homeと日英Simple / Advancedの6pageが初期表示で例外0件となること。
- 全pageが共通`EnvGeo-Earthquake` titleを表示すること。
- Homeは言語別の主要見出し、可視化pageはversion付き見出しを維持すること。
- 可視化4pageが各言語の上部・下部取得buttonを1個ずつ維持すること。

### `test/test_repository_health.py`

- 公開候補が許可されたroot file・directoryだけで構成されること。
- `.gitignore`が開発専用資料、秘密情報file、生成物、cacheを除外すること。
- standalone Git cloneで実行した場合、tracked fileに除外対象・生成物がないこと。
- runtime Pythonが開発専用directoryへlocal依存しないこと。
- 公開候補textに実値形式のtoken・秘密鍵・credential URL・代入済みsecretがないこと。
- user名を含むmacOS / Linux / Windows絶対local path、symlink、Markdown link欠損がないこと。

### `test/test_distribution_policy.py`

- 日英の配布方針文書が相互linkを持ち、初回DOIをsource-only GitHub Releaseとすること。
- Zenodoとの関係と、PyPI・package化を初回DOIの対象外とする決定を維持すること。
- 日英READMEが配布方針へlinkし、local起動commandを維持すること。

4件の追加contractで、日英Plotly camera案内がShift / Control / Option（Alt） / Commandを記載し、
各主要3D図の前にあることを保護する。

2026-10-08の配布方針更新後、利用可能なlocal pytest環境で
`182 passed, 0 skipped`を確認した。日英4pageの固定・連動方式、2D・3D・断面用profile、
M7:M4直径比約20:1と調整case、`0.2–10.0`の全体直接倍率を含み、Seawater datasetや実USGS通信には依存しない。
commit `fe725ee`のGitHub Actions runで、Python 3.10 / 3.12 matrix全体の合格を確認済み。
今回追加した配布方針4 contractは次回push後のCI確認待ちである。

## 現在の限界

まだ次は十分に自動化できていません。

- Streamlit UIのRegion / hotspot / filter / downloadなどの操作。
- USGS API への実ネットワークアクセスを含む end-to-end テスト。
- 2D/3D/4D 図の見た目の自動比較。
- JMA/NIED アップロード表の多様な列名・形式への対応確認。
- Region / hotspot / cross-section UI のブラウザ上の状態確認。

そのため、重要なUI変更後は pytest に加えて手動で Streamlit 画面確認を行います。

## 今後追加したいテスト

- Region 選択ロジックを UI から切り離した純粋関数としてテストする。
- 任意JMA/NIED比較は現状維持とし、実際の不具合がない限り列名・schema testを拡張しない。
- 空間処理はブラウザ上のRegion / hotspot / cross-section操作も手動確認する。
- Seawater と共有できる候補関数は、将来 `envgeo4d` / shared core 側のテストへ移す。
