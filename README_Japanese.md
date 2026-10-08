# EnvGeo-Earthquake

EnvGeo-Earthquake は、研究・教育向けに地震の震源カタログを探索するための
インタラクティブ可視化プラットフォームです。

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/python-3.10--3.12-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**現在の開発バージョン:** 0.3.2（2026-09-22）

実行時のバージョン情報は`envgeo_utils.APP_VERSION`と
`envgeo_utils.APP_VERSION_DATE`の1か所で定義し、日英Homeと可視化ページは
個別に文字列を再定義せず直接参照します。

同梱の海岸線CSVとHome内READMEは、processのcurrent directoryではなく
source fileの位置を基準に読み込みます。

このアプリケーションは、**EnvGeo-Seawater**
(https://envgeo.h.kyoto-u.ac.jp/sw_jpn/) の空間 3D/4D 可視化ワークフローを、
地震カタログデータに応用したものです。EnvGeo-Seawater は、海洋学・海洋地球化学
データのインタラクティブな可視化を目的として開発されました。EnvGeo-Earthquake は、
その探索的で、出典を明示する研究用ワークフローを震源カタログに展開しています。

本アプリは、**探索的データ解析**、授業、再現可能な研究ワークフローの支援を目的としています。
公式の地震速報、津波警報、ハザード評価、防災対応システムではありません。

画面キャプチャ付きユーザーマニュアル: [日本語](docs/manual_Japanese/README.md) | [English](docs/manual/README.md)

Earthquakeの現状挙動を維持する最小カタログ検証方針は
[日本語](docs/earthquake_validation_Japanese.md) / [English](docs/earthquake_validation.md)
に記録しています。新しいcheckは、crash防止、明確なerror、利用者uploadの
安全な読込みに必要な範囲に限定します。

---

## 概要

EnvGeo-Earthquake は、USGS Earthquake Catalog API から震源データを取得し、
EnvGeo 形式の 2D、3D、4D、断面表示ワークフローで可視化します。

- マグニチュード連動（既定）または固定サイズの 2D / 3D マップ
- 深さ、マグニチュード、カラーバー制御を備えた 3D/4D 震源プロット
- 任意の A-B 断面図と断面位置マップ
- 深度頻度プロファイル
- 時系列ヒストグラム
- Advanced ページ内での、アップロードした JMA/NIED カタログ表との日本周辺向け比較
- 利用可能な場合の USGS プレート境界オーバーレイ

また、本プロジェクトは EnvGeo-Seawater のワークフローのうち、どの部分を地球科学データに
共通する機能として整理できるかを検討するための実例でもあります。候補には、データ正規化、
出典メタデータ、地図プリセット、ローカル km 座標変換、3D/4D レイアウト、断面図処理などが含まれます。

---

## 主要ページ

Streamlit アプリでは、`home.py` が概要、データ出典、使い方、更新履歴、README のタブを担当します。
`pages/` ディレクトリには、英語版と日本語版の地震可視化ワークフローが含まれます。

- `pages/54_🇺🇸_4D_Earthquake_Simple.py`  
  英語版の基本的な USGS 震源可視化ページです。

- `pages/55_🇺🇸_4D_Earthquake_Advanced.py`  
  英語版の詳細ページです。プレート境界、2D/3D マップ、断面図、深度プロファイル、時系列ヒストグラム、
  JMA/NIED 比較機能を含む詳細版の地震カタログ探索ページです。

- `pages/56_🇯🇵_4D_Earthquake_シンプル版.py`  
  日本語版の基本的な USGS 震源可視化ページです。

- `pages/57_🇯🇵_4D_Earthquake_詳細版.py`  
  日本語版の詳細ページです。プレート境界、2D/3D マップ、断面図、深度プロファイル、時系列ヒストグラム、
  JMA/NIED 比較機能を含みます。

---

## 主な機能

- GeoJSON を用いた USGS Earthquake Catalog API へのアクセス
- UTC 日時、マグニチュード、震源深さ、緯度、経度、並び順、最大イベント数によるフィルタ
- メイン画面での「日本周辺」または「全球」表示の選択
- 2D・3D・Advanced断面表示でのマグニチュード連動（既定）または固定マーカーサイズと、
  最大10倍の全体直接倍率調整。連動方式はM7:M4のmarker直径比を1:1–30:1で調整可能（既定20:1）
- カラーバー変数として、マグニチュードまたは震源深さを選択可能
- 経緯度の生値ではなくローカルな km 座標を用いた EnvGeo 形式の 3D/4D 表示
- drag回転、平行移動・zoom・reset、Shift / Control / Option（Alt） / Commandとmouseによる
  camera操作を案内する簡潔なPlotly説明
- 最大 1,000 km までの深度軸スケーリング
- USGS Tectonic Plate Boundaries service からのプレート境界オーバーレイ
- 任意断面図と深度プロファイル機能
- 選択した A-B 断面線と断面幅を表示するマップ
- 地震発生数の時系列ヒストグラム
- 選択した USGS カタログ記録の CSV 出力
- 選択クエリが 20,000 イベントの API 上限に達した場合の警告
- アプリ内での簡潔な出典・利用上の注意表示
- 3D 表示は PC 推奨、スマートフォン・タブレットでは 2D 表示推奨

---

## EnvGeo-Seawater との関係

EnvGeo-Earthquake は、構成、用語、可視化ワークフローを EnvGeo-Seawater に近い形で維持しています。
現在は別アプリとして扱いますが、今後の整理では、次の要素を EnvGeo 共通コア候補として検討します。

- 地球科学データの標準列名と単位の扱い
- データソース、引用、出典メタデータの表示
- 地図背景、地域プリセット、海岸線ヘルパー
- 経度ラップとローカル km 座標変換
- 3D/4D 図の共通レイアウト
- 断面図と深度プロファイルの幾何処理
- ユーザーアップロードデータの検証と比較表の正規化

汎用的なinput safety helperは将来のCore候補にできますが、USGS catalog値の
独自科学審査は現時点のEarthquakeまたはCoreの要件にしません。

一方で、USGS カタログ取得、JMA/NIED 比較、震源用語、地震データ固有の注意事項は、
他の EnvGeo アプリでも同じ構造が必要になるまでは Earthquake 側に残します。

EnvGeo-Earthquakeは単独で実行可能であり、EnvGeo-Seawaterまたは将来の
共通コアを実行時に必要としません。

---

## データソースと出典表示

### USGS Earthquake Catalog API

主要な震源データは以下から取得します。

- USGS Earthquake Catalog API / FDSN Event Web Service  
  https://earthquake.usgs.gov/fdsnws/event/1/

本アプリでは `query` メソッドを用い、主に以下のパラメータを使用します。

- `format=geojson`
- `eventtype=earthquake`
- `starttime`
- `endtime`
- `minmagnitude`, `maxmagnitude`
- `mindepth`, `maxdepth`
- `minlatitude`, `maxlatitude`
- `minlongitude`, `maxlongitude`
- `orderby`
- `limit`

USGS API ドキュメントでは、このサービスが FDSN Event Web Service を実装しており、
時刻、地理範囲、マグニチュード、深さ、並び順、結果数上限などのクエリパラメータを
サポートしていることが説明されています。サービスの上限は 20,000 イベントであるため、
本アプリではクエリが選択上限に達した場合に警告を表示します。

推奨カタログ引用:

> U.S. Geological Survey. (2017). Advanced National Seismic System (ANSS)
> Comprehensive Catalog. U.S. Geological Survey.
> https://doi.org/10.5066/F7MS3QZH

同じcatalog引用文を`envgeo_utils.py`の1か所で定義し、日英Homeと4つの現行可視化pageが
参照することで、言語版・画面間の表記ずれを防ぎます。

追加の USGS 関連リンク:

- ANSS / USGS FDSN data-center record  
  https://www.fdsn.org/datacenters/detail/USGS/
- USGS Earthquake Hazards Program  
  https://www.usgs.gov/programs/earthquake-hazards
- USGS Search Earthquake Catalog  
  https://earthquake.usgs.gov/earthquakes/search/
- USGS Latest Earthquakes  
  https://www.usgs.gov/tools/latest-earthquakes

### USGS データのクレジットと速報値に関する注意

USGS が作成したデータや情報は、一般に米国のパブリックドメインとみなされます。
一方で、USGS はそのプロダクト、出版物、Web サイトを利用する際に適切なクレジットを
表示することを求めています。また、地震カタログには複数の観測網や機関から提供された
情報が含まれる場合があり、USGS Web サイト上の非 USGS 資料には別の著作権制限が
適用されることがあります。出版や再配布の際には、USGS/ANSS カタログを引用するとともに、
利用するカタログや表に対して各提供元が求める謝辞・利用条件にも従ってください。

- USGS Copyrights and Credits  
  https://www.usgs.gov/information-policies-and-instructions/copyrights-and-credits

地震情報は速報的であり、後から修正される場合があります。そのため本アプリでは、
地震データが更新・修正される可能性があること、緊急対応や公共安全上の判断には
公式機関の情報を利用すべきであることを明示しています。

- USGS Earthquake Notification Service disclaimer  
  https://earthquake.usgs.gov/ens/help_disclaimer

### プレート境界データ

プレート境界オーバーレイは以下から読み込みます。

- USGS Tectonic Plate Boundaries ArcGIS REST service  
  https://earthquake.usgs.gov/arcgis/rest/services/eq/map_plateboundaries/MapServer

本アプリでは以下を使用します。

- `Plates (1)`
- 任意で `Microplates (0)`

USGS のプレート境界サービスのメタデータには、以下の出典が示されています。

- USGS Seismicity of the Earth Map Series  
  https://earthquake.usgs.gov/earthquakes/byregion/
- Bird, P. (2003). An updated digital model of plate boundaries.
  *Geochemistry, Geophysics, Geosystems*, 4(3), 52 pp.  
  https://doi.org/10.1029/2001GC000252
- DeMets, C., Gordon, R. G., & Argus, D. F. (2010). Geologically current
  plate motions. *Geophysical Journal International*, 181, 1-80.  
  https://doi.org/10.1111/j.1365-246X.2009.04491.x

プレート境界の位置は概略であり、教育・研究用の文脈表示として使用します。
公式な断層線、ハザードゾーン境界、防災対応情報として使用しないでください。

USGS プレート境界サービスに接続できない場合、本アプリは日本周辺の海溝・トラフを示す
小規模な概略フォールバック線を表示できます。これらは視覚的なガイドであり、
正式なデータセットではありません。

### JMA および NIED 比較データ

これはAdvanced pageの任意機能で、主要なUSGS可視化workflowや最初の安定
release/DOIには必要ありません。

本アプリは JMA や NIED のサービスを自動的にスクレイピングしません。
代わりに、利用者が取得・確認したカタログ表をアップロードして比較できる
インターフェースを提供します。

対応形式はCSV、TSV、TXT、新しいExcel形式の`.xlsx`です。古いbinary Excel形式の
`.xls`は別のreader依存が必要で、現在の実行環境に含めないため対応形式として表示しません。

関連する公式情報:

- JMA Earthquake Information issued by Japan Meteorological Agency  
  https://www.data.jma.go.jp/eqev/data/en/guide/earthinfo.html
- JMA Seismological Bulletin of Japan  
  https://www.data.jma.go.jp/eqev/data/bulletin/index_e.html
- JMA Hypocenter file format  
  https://www.data.jma.go.jp/eqev/data/bulletin/data/format/fmthyp_e.html
- NIED Hi-net data guidance  
  https://www.hinet.bosai.go.jp/about_data/?LANG=en
- 気象庁website利用規約  
  https://www.jma.go.jp/jma/kishou/info/coment.html
- NIED Hi-net再配布Q&A  
  https://www.hinet.bosai.go.jp/faq/?LANG=ja

NIED Hi-net のガイダンスでは、自動震源カタログは速報的な報告であり、
公式な地震情報については気象庁情報を参照するよう案内されています。
また、JMA 一元化カタログは登録ユーザー向けに Hi-net Web サイトから利用可能であり、
必要に応じて最終版の JMA Seismological Bulletin を使用することが推奨されています。

JMA website contentは、原則として出典と、編集・加工した場合の表示が必要です。
第三者の権利や個別sourceの条件も利用者が確認します。NIED Hi-netはdownloadしたdata・
震源情報の再配布を禁止しています。Hi-net dataによる成果の公表では、提供機関の謝辞、
NIED Hi-net DOIの引用、NIEDへの成果報告が必要です。Hi-netを通じて提供されるJMA、大学、
その他機関のdataには、それぞれの提供元規則も適用されます。

NIED Hi-net reference:

> National Research Institute for Earth Science and Disaster Resilience (2019), NIED Hi-net, National Research Institute for Earth Science and Disaster Resilience, https://doi.org/10.17598/NIED.0003

詳細は日英の責任記録
[`docs/jma_nied_data_responsibilities_Japanese.md`](docs/jma_nied_data_responsibilities_Japanese.md)
に整理しています。比較uploadをsource dataの再公開手段として使用しないでください。

upload内容は現在のStreamlit sessionで読み、本アプリが意図的に永続的な
アプリdata storeへ書き込むことはありません。
JMA/NIED catalog fileはrepositoryや予定release archiveへ同梱しません。

### ベースマップと表示レイヤー

本アプリでは、Plotly Mapboxレイヤーを通じて複数の地図背景を使用します。
以下の出典表示は2026-10-08に再確認しました。

- 標準地図: Plotly組込みのOpenStreetMap標準raster styleです。インタラクティブ
  レイヤーが`© OpenStreetMap contributors`を表示します。CARTO basemapは設定して
  いません。OpenStreetMapの著作権・licenseとtile利用方針に従い、offline利用のための
  一括downloadやprefetchは行わないでください。  
  https://www.openstreetmap.org/copyright  
  https://operations.osmfoundation.org/policies/tiles/
- 衛星画像: USGS National Map imagery tiles。表示creditは
  `USDA, USGS The National Map: Orthoimagery`です。service metadataではUSDA NAIPを
  主なsourceとし、他のsource imageryを含む場合があると説明されています。  
  https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer
- 海底地形図: Esri World Ocean Base tiles。表示creditは
  `Sources: Esri, GEBCO, NOAA, National Geographic, DeLorme, HERE,
  Geonames.org, and other contributors`です。航海・海上安全判断には使用しないで
  ください。出版・静的出力ではEsriの最新案内を再確認してください。  
  https://services.arcgisonline.com/arcgis/rest/services/Ocean/World_Ocean_Base/MapServer  
  https://support.esri.com/en-us/knowledge-base/what-is-the-correct-way-to-cite-an-arcgis-online-basema-000012040
- 等高線・地形図: 国土地理院の標準tile。表示creditは`国土地理院`です。本アプリは
  realtime表示として利用します。静的な出版・再配布では最新の利用条件と必要手続きを
  再確認してください。  
  https://maps.gsi.go.jp/development/ichiran.html  
  https://maps.gsi.go.jp/help/termsofuse.html

### 出典確認状況

以下の状態は、2026-05-04 に公式または提供元ページに基づいて確認したものです。

- USGS FDSN Event Web Service/API パラメータ、GeoJSON 出力、
  `eventtype=earthquake`、深さ・マグニチュード・位置・時刻フィルタ、
  20,000 イベントのサービス上限は USGS により文書化されています。
- ANSS Comprehensive Catalog の引用情報と DOI `10.5066/F7MS3QZH` は
  FDSN の USGS data-center record に記載されています。
- プレート境界オーバーレイは、`Plates (1)` および `Microplates (0)` レイヤーを持つ
  USGS の公式 ArcGIS REST service です。メタデータでは Bird (2003)、DeMets et al. (2010)、
  USGS Seismicity of the Earth Map Series が引用されています。
- JMA と NIED のリンクは公式提供元ページです。本アプリはこれらをスクレイピングせず、
  利用者がアップロードした比較表のみを受け付けます。
- 論文、図、印刷教材、静的出力で使う場合は、
  各タイル提供元の最新の利用条件と必要な attribution を再確認してください。
- プロットに使用する海岸線データはNatural Earthのpublic-domain coastline v4.1.0に由来します。
  file hash、保持中間workbookとの照合根拠、過去のraw download記録上の制約を含む
  日英の[出典・利用条件記録](coastline/LICENSE_OR_SOURCE_Japanese.md)を参照してください。

---

## インストール

このプロジェクトは Python 3.10 から 3.12 を想定しています。

```bash
pip install -r requirements.txt
```

ローカルでテストを実行する場合は、開発用 requirements もインストールします。

```bash
pip install -r requirements-dev.txt
```

## 配布方式

初回安定版は、アプリ一式をGitHub Releaseのsource archiveとして配布し、Zenodoへ保存します。
初回DOI releaseではPyPI公開やinstall可能wheelへの再編を行いません。範囲と理由は
[配布方針](docs/distribution_Japanese.md)に記録しています。

---

## Quick Start

```bash
streamlit run home.py
```

その後、ターミナルに表示されるローカル URL を開きます。通常は以下です。

```text
http://localhost:8501
```

推奨ワークフロー:

1. `4D Visualizer Earthquake Advanced` を開きます。
2. `Japan and surrounding area` または `Global` を選択します。
3. サイドバーで、時刻、マグニチュード、深さ、地理範囲のフィルタを設定します。
4. USGS クエリを取得または更新します。
5. まず 2D マップで概観を確認します。
6. 深さ構造を確認する場合は、PC で 3D/4D マップを使用します。
7. 沈み込み帯や地域地震活動を解析する場合は、断面図と深度プロファイルを使用します。
8. 時系列ヒストグラムで時系列の地震発生頻度を確認します。
9. 日本周辺カタログを比較する場合は、手動で取得したカタログデータを Advanced ページ内の JMA/NIED 比較機能にアップロードします。

---

## API 使用例

USGS データローダーは `envgeo_utils.py` に実装されています。

```python
from datetime import datetime, timezone

import envgeo_utils

df = envgeo_utils.load_usgs_earthquake_data(
    starttime=datetime(2026, 1, 1, tzinfo=timezone.utc),
    endtime=datetime(2026, 1, 31, tzinfo=timezone.utc),
    minmagnitude=4.5,
    mindepth=0,
    maxdepth=700,
    minlatitude=20,
    maxlatitude=50,
    minlongitude=120,
    maxlongitude=155,
    limit=2000,
    orderby="time",
)
```

返される主な列:

- `EventID`
- `DateTime_UTC`
- `Time_UTC`
- `Longitude_degE`
- `Latitude_degN`
- `Depth_km`
- `Magnitude`
- `MagnitudeType`
- `Place`
- `URL`

生成された USGS クエリ URL は以下に保存されます。

```python
df.attrs["query_url"]
```

---

## ディレクトリ構成

- `home.py`  
  EnvGeo-Earthquake の Streamlit メインエントリーポイントです。

- `envgeo_utils.py`  
  USGS API 読み込み、GeoJSON 正規化、地図スタイル、海岸線読み込み、
  キャッシュ削除などを含む低レベル共通ユーティリティです。

- `pages/54_🇺🇸_4D_Earthquake_Simple.py`  
  英語版の基本的な地震可視化ページです。

- `pages/55_🇺🇸_4D_Earthquake_Advanced.py`  
  英語版の JMA/NIED 比較機能を含む詳細版の地震カタログ探索ページです。

- `pages/56_🇯🇵_4D_Earthquake_シンプル版.py`  
  日本語版の基本的な地震可視化ページです。

- `pages/57_🇯🇵_4D_Earthquake_詳細版.py`  
  日本語版の JMA/NIED 比較機能を含む詳細版の地震カタログ探索ページです。

- `coastline/`  
  参照overlay用のNatural Earth由来50m・110mローカル海岸線座標CSVと、
  日英の出典・利用条件記録です。

- `test/`  
  utility import、USGS GeoJSON契約、海岸線、オフライン地図、page state復旧の
  再現可能なtestです。

- `requirements.txt`  
  Streamlit アプリ実行用の依存関係です。

- `requirements-dev.txt`  
  実行用依存関係に加え、ローカルテスト用ツールを含みます。

- `docs/`  
  日英ユーザーマニュアル、画面画像、検証方針、提供元別の利用責任、
  テスト説明を収録しています。

---

## 文書について

公開文書には、アプリの利用方法、データ出典、制約、検証方法、テスト方法を収録します。
引継ぎ記録やローカル開発用の詳細な作業ログは、公開repositoryには含めません。

---

## 再現性とキャッシュ

USGS 地震クエリは明示的な URL パラメータを通じて実行され、クエリ URL はアプリ内に表示されます。
取得結果は CSV としてエクスポートできます。

Streamlit のキャッシュを用いて、API への重複アクセスを減らしています。
USGS 地震クエリのキャッシュは 1 時間、プレート境界クエリのキャッシュは 24 時間です。
サイドバーにはキャッシュ削除・再読み込みボタンがあります。

地震カタログは修正される場合があるため、USGS がイベントパラメータを更新した場合や、
後日クエリを再実行した場合には、完全に同じ結果が再現されないことがあります。

---

## 制約

- このアプリは公式の警報・防災対応プロダクトではありません。
- USGS イベントデータは速報的であり、後から修正される場合があります。
- USGS FDSN event service には 20,000 イベントのクエリ上限があります。
- 大規模な全球クエリは、多数の点をブラウザがインタラクティブに描画するため遅くなる場合があります。
- Plotly 3D の操作は PC に適しています。スマートフォンやタブレットでは 2D マップを推奨します。
- プレート境界は概略的なコンテキスト線です。
- JMA/NIED 比較は、利用者がアップロードしたデータと、利用者側での提供元条件遵守に依存します。
- ローカル海岸線参照ファイルは、可視化コンテキストとしてのみ使用します。

---

## 関連する公式ツール

- USGS Latest Earthquakes  
  https://www.usgs.gov/tools/latest-earthquakes
- USGS Search Earthquake Catalog  
  https://earthquake.usgs.gov/earthquakes/search/
- JMA earthquake information  
  https://www.data.jma.go.jp/eqev/data/en/guide/earthinfo.html
- JMA Seismological Bulletin of Japan  
  https://www.data.jma.go.jp/eqev/data/bulletin/index_e.html
- NIED Hi-net  
  https://www.hinet.bosai.go.jp/?LANG=en

---

## 開発参考資料

USGS 地震 API の実装は、公式 USGS ドキュメントと以下の入門記事を参考にしています。

- ssfuno, "PyGMTとUSGSのAPIを使って地震の分布を描いてみる"  
  https://zenn.dev/ssfuno/articles/56e2577ee794f3

データアクセス、利用条件、引用については、上記の公式 USGS ドキュメントおよび提供元ページを
一次的な参照先として使用してください。

---

## Citation

授業資料、発表、研究ワークフローで本アプリを使用する場合は、アプリ本体と元データ提供者の
両方を引用してください。

推奨アプリ引用:

> Ishimura, T. (2026). EnvGeo-Earthquake: An interactive earthquake
> hypocenter exploration app based on EnvGeo-Seawater. Kyoto University.

必須または推奨されるデータ引用には、以下を含めてください。

> U.S. Geological Survey. (2017). Advanced National Seismic System (ANSS)
> Comprehensive Catalog. U.S. Geological Survey.
> https://doi.org/10.5066/F7MS3QZH

プレート境界を表示する場合は、以下も引用してください。

> Bird, P. (2003). An updated digital model of plate boundaries.
> *Geochemistry, Geophysics, Geosystems*, 4(3), 52 pp.
> https://doi.org/10.1029/2001GC000252

> DeMets, C., Gordon, R. G., & Argus, D. F. (2010). Geologically current
> plate motions. *Geophysical Journal International*, 181, 1-80.
> https://doi.org/10.1111/j.1365-246X.2009.04491.x

日本周辺カタログ比較を行う場合は、使用した具体的なデータセットに応じて、
JMA/NIED の提供元ガイダンスに従い、引用・謝辞を記載してください。

---

## License

アプリケーションコードは MIT License のもとで公開されています。
外部サービスから取得するデータは、それぞれの元提供者の利用条件、ポリシー、
attribution guidance に従います。

アプリケーションコードのライセンスと、外部データ・提供元条件の切り分けについては
`NOTICE.md` も参照してください。
