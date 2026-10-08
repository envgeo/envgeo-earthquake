# 同梱海岸線データ: 出典と利用条件

[English version](LICENSE_OR_SOURCE.md)

最終確認: 2026-10-08

## 対象ファイル

- `world_coastline_coordinates_50m.csv`
- `world_coastline_coordinates_110m.csv`

これらはNatural Earth coastline version 4.1.0の1:50 million / 1:110 million vector dataに由来する
座標表です。EnvGeo-Earthquakeの地図・3D plotの表示上の参照線としてだけ同梱します。
地震観測、公式境界、航法、hazard productではありません。

## 元データ

- [Natural Earth 1:50m Physical Vectors](https://www.naturalearthdata.com/downloads/50m-physical-vectors/)
- [Natural Earth 1:110m Physical Vectors](https://www.naturalearthdata.com/downloads/110m-physical-vectors/)
- [Natural Earth Terms of Use](https://www.naturalearthdata.com/about/terms-of-use/)

Natural Earthは、同siteの全versionのraster/vector map dataがpublic domainであるとしています。
利用許可と出典表示は必須ではありません。本projectでは、Natural Earthが提案する
次の表記を使用します。

> Made with Natural Earth. Free vector and raster map data @ naturalearthdata.com.

repository rootのMIT LicenseはEnvGeo-Earthquakeのsource codeに適用します。
これらNatural Earth由来dataのpublic-domain statusを置き換えたり制限したりしません。

## ローカル形式と整合性

元のvector geometryを`Longitude` / `Latitude`列に直列化し、全列空のrowでline segmentを
分離しています。元shapefileのattributeとupstream metadataはCSVに含まれません。

| ファイル | data row | 空separator row | SHA-256 |
|---|---:|---:|---|
| `world_coastline_coordinates_50m.csv` | 61,844 | 1,428 | `c3d7bee4fb696b011fa34bb13bed0c335c5250eeaf37d8739d77d29a27fe385c` |
| `world_coastline_coordinates_110m.csv` | 5,261 | 133 | `a31df3aeee9dc4195af35a31b0605fdb572c7c7dd7cde17f773c9438f5ec7f3f` |

2026-10-08の読取り専用監査で、EnvGeo-Seawater v1.3.5 workspaceの50m / 110m fileと
それぞれbyte単位で一致しました。両アプリは各自のcopyを保持し、互いに実行時依存しません。

## 保持されている派生根拠

読取り専用で参照したEnvGeo-Seawaterの来歴記録には、50m・110mのsource archiveを
Natural Earth coastline version 4.1.0と特定できる、保持中の海岸線source workspaceが
記録されています。archiveと対応する座標workbookは2025-01-24に保存されています。
Seawaterの2026-10-03監査では、両workbookと現行CSVについて、座標、row数、欠損座標による
segment separatorが一致し、最大絶対数値差が約`1.42e-14`であることを確認しています。
Earthquake側のCSVはそのSeawater CSVとbyte単位で一致するため、Earthquake同梱fileも
Natural Earth coastline v4.1.0由来と特定できます。

## 来歴上の制約

元のNatural Earth raw downloadのchecksum、正確なdownload日、独立したconversion scriptは
保持されていません。この記録は、配布artifact、保持中間workbookとの対応、upstream releaseを
特定しますが、過去のraw downloadをbit単位で再構成できるとは表明しません。Natural Earthの
現在のdownload pageに表示されるversionは、この過去のv4.1.0 source workspaceと異なる場合があります。

将来fileを再生成する場合は、upstream archive名、Natural Earth version、download日、
raw download checksum、conversion command/script、output row数、output SHA-256を
この文書に記録してから置き換えます。

## 精度と利用上の制約

Natural Earthはこれらを中・小縮尺の一般化されたmap dataとし、精度または特定用途への
適合性に責任を負わないとしています。同梱座標はmap contextだけに使用し、航法、
法的境界の判断、site scaleの距離測定、災害・hazard判断には使用しないでください。
