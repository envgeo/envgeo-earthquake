# テストメモ

[English version](README.md)

このfolderには、EnvGeo-Earthquake用の小さな`pytest`チェックを収録しています。

各testは自動チェックリストの1項目に相当し、主に次を確認します。

- 主utility moduleをimportできるか。
- utility moduleがversion情報を公開しているか。
- 日英Homeと4つの可視化ページが、1つの共通version定義を参照しているか。
- 日英pageが共通USGS catalog・plate-boundary引用を参照しているか。
- online地図modeが監査済みtile URLと実行時attributionを維持しているか。
- 日英JMA/NIED責任記録が公式参照とNIED DOIを維持しているか。
- 欠損列があっても、USGS GeoJSONの1 featureが1地震行として保持されるか。
- pageとCSV出力が依存するUSGS列名・列順が安定しているか。
- 数値文字列が安全に数値化され、不正値が欠損値になるか。
- USGSのmillisecond時刻がUTC・暦列へ一貫して変換されるか。
- 不正JSONと`features`がlistでないresponseが、未処理例外ではなく
  pageが処理する読めるerrorになるか。
- 正常・空・欠損responseが共通loaderを通り、HTTP・timeout・接続失敗が
  page処理済みerrorになるか。
- query URLが必須・任意filterを保持し未指定値を除外するか、日英4pageが
  test済み取得上限境界を共通利用するか。
- 空のUSGS GeoJSONでも、想定列を持つ安全な空表が返るか。
- 地図用の海岸線とオフライン補助が動作するか。
- processのcurrent directoryを変更しても、同梱海岸線と日英Home内READMEが読み込めるか。
- 日英AdvancedのuploadがCSV、TSV、TXT、XLSXだけを受け付け、宣言済みの
  `openpyxl` engineでXLSX workbookを往復できるか。
- 日英Advancedの実upload helperが代表CSVを標準化し、必須列欠損を空結果・warningで
  安全に処理するか。
- 日英4pageが地理的境界上の有効点を保持し、欠損・非数値・範囲外USGS座標を
  描画前に除外するか。
- 日英4pageが経度をラップし、地図の継ぎ目に応じて線を分割・連続化し、
  日付変更線近傍を近接local km座標へ変換するか。
- 日英Advancedが日付変更線をまたぐ短い断面を投影し、始終点一致を安全に処理し、
  閉じた断面帯polygonを一貫して生成するか。
- 日英Advancedのplate-boundary loaderが正常、全面失敗、不正response、部分layer失敗を
  区別し、日本presetだけに模式fallbackを適用するか。
- 日英Home / Simple / Advancedが例外なく起動し、主要見出しと上下取得buttonを維持するか。
- 公開候補が許可対象だけで、生成物・private資料を除外し、secret実値・機械固有path・
  symlink・Markdown link欠損を含まないか。

`earthquake_map_v030`直下で次を実行します。

```bash
pytest -q
```

`pytest`は`.pytest_cache/`を、Pythonは`__pycache__/`を生成する場合があります。
これらはローカル生成物で、`.gitignore`対象です。

## 現在の範囲

現行testは再現可能で、実USGS通信を行いません。import、地震カタログ標準化、
海岸線・オフライン地図、page state復旧を保護します。browser操作、地図描画、
実serviceを使うend-to-end動作は別途確認が必要です。

2026-10-08のrepository-health test追加後の記録: `132 passed, 0 skipped`。
