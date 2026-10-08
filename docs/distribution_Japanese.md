# EnvGeo-Earthquake 配布方針

[English version](distribution.md)

決定日: 2026-10-08

## 初回安定版

EnvGeo-Earthquakeの初回安定版は、**GitHub Releaseによるsource-only配布**とします。
ここでいうsource-onlyは、PyPIで配布するPython packageではなく、アプリ一式を含む
version付きの正式archiveを意味します。

通常の利用者は、公開中のStreamlit Webアプリをinstallなしで利用できます。
local実行や再現可能な保存が必要な場合は、GitHub Releaseのarchiveをdownloadして
次を実行します。

```bash
pip install -r requirements.txt
streamlit run home.py
```

release archiveには、アプリ、日英page・manual、runtime依存、同梱海岸線dataと出典、
test、license、notice、citation metadata、release notesを含めます。

## 初回DOIの対象外

初回DOI releaseでは、次を行いません。

- PyPIへの公開
- install可能なwheelまたはsdistの作成
- `pip install envgeo-earthquake`への対応
- package専用launcher・commandの追加
- package化だけを目的としたsource tree再編

これらはStreamlitアプリの公開やZenodo DOI取得に必要ありません。初回公開を検証済みの
アプリに集中させ、package化による安定path・runtime挙動の変更を避けます。

## GitHub ReleaseとZenodo

tag付きGitHub Releaseをversion付き公開source archiveとし、Zenodoがそのreleaseを保存して
version DOIとconcept DOIを発行します。GitHub tag、GitHub Release、Zenodo record、
`CITATION.cff`、日英release notesは同一versionに揃えます。

## 将来のpackage化

安定したimport API、command-line launcher、または独立versionのEnvGeo Coreが必要になった場合、
DOI公開後にinstall可能packageを再検討できます。EnvGeo-Earthquakeは単独動作を維持し、
EnvGeo-Seawaterや将来のCoreをruntimeに必要としません。
