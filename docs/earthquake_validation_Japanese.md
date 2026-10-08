# EnvGeo-Earthquake 最小検証方針

[English version](earthquake_validation.md)

状態: 現状機能の維持を優先するため、2026-10-08に内容を絞り込み。

## 原則

EnvGeo-Earthquakeの主な役割は、公式のUSGS Earthquake Catalog APIから
recordを取得して表示することです。USGS recordに対する独自の科学的品質等級は
必要としません。公開整備では現状機能を維持し、crash、誤解を招く表示、
読込み不能なuploadを防ぐために本当に必要なcheckだけを追加します。

USGSの`status`、`alert`、magnitude、深さ、震源時刻、Event IDはsource値のまま扱い、
EnvGeo-Seawaterのquality flagに変換しません。

## USGS dataの最小check

1. 接続失敗、timeout、HTTP error、不正JSONでStreamlit pageをcrashさせない。
2. 正規化前にresponseに`features` listがあることを確認する。
3. 現行の図が使うcoordinateとpropertyを変換し、欠損・非数値・GeoJSON範囲外の
   経度緯度を描画前に除外して、対象plotのcrashや歪みを防ぐ。
4. 現行の空結果と20,000 event上限の案内を維持する。
5. USGS recordは速報値を含み、改訂され得るという注意を維持する。

このworkflowではUSGS serviceが供給する値を信頼します。新しいseverity体系、
重複Event ID管理、recordごとのissue code、USGS値の独自科学審査は、
現時点の公開要件にしません。

## 任意のJMA/NIED系upload

この既存のAdvanced比較は任意機能です。日本周辺の一部研究workflowでは有用ですが、
USGS表示の中核機能ではなく、最初の安定releaseまたはZenodo DOIのゲートにしません。
現状挙動を維持するため残し、機能範囲は拡張しません。

現行の基本checkで十分です。

- 表示済みのCSV、TSV、TXT、XLSXのみを受け付ける。
- 日英の許容aliasを用い、現行の経度、緯度、深さ、magnitude列を必須とする。
- 必須値を数値化し、fileが読めない場合や必須列がない場合は明確なerrorを出す。
- 時刻と地名は任意のままとする。
- 新しいcatalog quality scoreを追加せず、upload fileが科学的に検証済みとも表現しない。

アプリは選択fileを現在のStreamlit sessionで読み、意図的に永続的なアプリdata storeへ
書き込みません。source fileと提供元の利用条件は利用者が管理します。

## 明確な不具合がない限り後回しにする項目

- 重複Event IDの報告
- `updated`と震源時刻の整合check
- 多段階severityと安定issue codeの体系
- 図ごとのvalidation dashboardとissue件数export
- 現行plotの安全性に必要な範囲を超える厳格なbounds check
- 別途の要件・回帰testなしでのtimezone解釈や正規化挙動の変更

これらは将来再検討できますが、最初の安定公開・Zenodo DOIのゲートにしません。

## 実装ルール

validation codeを追加する前に、何の具体的な失敗を防ぐかを小さなtestで示します。
新しいvalidation subsystemよりも、現行workflowへの小さなguardを優先します。
確認された不具合がない限り、通常のUSGS表示結果を変えません。

## 公式参照先

- [USGS GeoJSON Summary Format](https://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php)
- [USGS FDSN Event Web Service](https://earthquake.usgs.gov/fdsnws/event/1/)
- [JMA 震源レコードフォーマット](https://www.data.jma.go.jp/eqev/data/bulletin/data/format/hypfmt_j.html)
- [NIED Hi-net データ利用案内](https://www.hinet.bosai.go.jp/about_data/?LANG=ja)
