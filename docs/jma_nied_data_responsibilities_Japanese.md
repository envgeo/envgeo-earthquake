# JMA / NIED uploadデータの利用者責任

[English version](jma_nied_data_responsibilities.md)

最終確認: 2026-10-08

## 対象

この記録は、詳細版で利用者が用意したfileを比較する任意機能を対象とします。
EnvGeo-EarthquakeはJMA/NIED catalogを自動取得せず、repositoryやrelease archiveへ
同梱せず、upload fileを現在のStreamlit sessionを超えて意図的に保存しません。

アプリがfileを受け付けることは、そのfileの利用、加工、出版、再配布を許可するものでは
ありません。正確な取得元と条件の確認は利用者の責任です。CSVやXLSXへの形式変換によって、
権利・義務は変わりません。

## 気象庁（JMA）

気象庁は、個別の権利表示がないwebsite contentについて、原則として公共データ利用規約
第1.0版に従って利用できると案内しています。利用者は次を行います。

- 気象庁を出典として、該当page URLを記載する。
- contentを編集・加工した場合、その事実を記載する。
- 加工情報を気象庁または国が作成したものと誤認させない。
- 第三者の権利や、個別sourceに別条件がないか確認する。

地震月報catalogの利用案内では、統合解析にNIED、大学、研究機関、自治体などの
観測dataが含まれることが説明されています。選択したcatalogに提供機関の謝辞が
指定されている場合は、その表示を維持してください。

公式参照:

- [気象庁website利用規約](https://www.jma.go.jp/jma/kishou/info/coment.html)
- [地震月報（カタログ編）](https://www.data.jma.go.jp/eqev/data/bulletin/index.html)
- [地震月報catalogの利用にあたって](https://www.data.jma.go.jp/eqev/data/bulletin/readme_j.html)

## 防災科研Hi-net（NIED）

NIED Hi-netの案内は、JMA websiteの一般条件より厳格です。Hi-net siteからdownloadした
data・震源情報の再配布を禁止し、dataを用いた独自成果は所定条件の下で公表できると
案内しています。利用者は次を行います。

- 他者から無断copyを受け取らず、提供元から取得・利用登録する。
- 成果の論文・報告で、使用した全提供機関を明記する。
- Hi-net dataを用いた成果ではNIED Hi-net DOIを引用する。
- JMA、大学など他機関提供dataは各機関の規則に従い、必要なら事前許可を得る。
- 論文、報告、教育、consultingなどの成果を、案内に従ってNIED Data Management
  Centerへ報告する。

NIED Hi-net推奨reference:

> National Research Institute for Earth Science and Disaster Resilience (2019), NIED Hi-net, National Research Institute for Earth Science and Disaster Resilience, https://doi.org/10.17598/NIED.0003

公式参照:

- [Hi-net dataの利用方法](https://www.hinet.bosai.go.jp/about_data/?LANG=ja)
- [Hi-net再配布Q&A](https://www.hinet.bosai.go.jp/faq/?LANG=ja)

## EnvGeo-Earthquakeの公開判断

- JMA/NIED catalog fileをsource repository、GitHub Release、package、Zenodo archiveへ
  同梱しない。
- 比較機能は任意で、release/DOI取得の必須条件にしない。
- アプリは提供元認証、利用許可確認、権利の自動判定を行わない。
- upload値は現在sessionで可視化・集計できるが、それをsource data再公開の許可と扱わない。
- 公開図、派生表、教材、論文では、必要な出典、加工表示、謝辞、引用、成果報告を維持する。

これはprojectのcompliance記録であり、法的助言ではありません。出版・再配布前に、
正確なdatasetに対する提供元の最新条件を再確認してください。
