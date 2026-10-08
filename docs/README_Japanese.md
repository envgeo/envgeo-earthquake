# EnvGeo-Earthquake ドキュメント

[English version](README.md)

このフォルダには、ユーザーマニュアルと公開用開発文書を収録しています。

## 主な文書

- `../PROJECT_STATUS.md` / `../PROJECT_STATUS_Japanese.md`: 新しい作業で最初に読む現状と引継ぎ。
- `development_workflow.md` / `development_workflow_Japanese.md`: 記録・マニュアル・TODO・公開文書の更新手順。
- `work_log_English.md` / `work_log.md`: 日英の時系列作業ログ。
- `publication_audit_2026-10-08.md` / `publication_audit_2026-10-08_Japanese.md`: 公開監査、Core分類、Zenodo計画。
- `publication_roadmap.md` / `publication_roadmap_Japanese.md`: 単独化からGitHub Release、Zenodo DOI、将来のCore検討までの全作業リスト。
- `public_release_scope.md` / `public_release_scope_Japanese.md`: 最初の安定公開版に含めるもの・除外するものの確定範囲。
- `../coastline/LICENSE_OR_SOURCE.md` / `../coastline/LICENSE_OR_SOURCE_Japanese.md`: 同梱海岸線CSVのNatural Earth v4.1.0出典、public-domain条件、整合性hash、保持された派生根拠、来歴上の制約。
- `earthquake_validation.md` / `earthquake_validation_Japanese.md`: USGS取得と利用者uploadに対する、現状挙動を維持する最小safeguard。推測的なcatalog quality機能は後回し。
- `jma_nied_data_responsibilities.md` / `jma_nied_data_responsibilities_Japanese.md`: 任意の利用者提供catalogに対する、提供元別の出典、加工表示、謝辞、DOI、成果報告、再配布責任。
- `testing.md` / `testing_Japanese.md`: 現行テストと制約。
- `release_checklist.md` / `release_checklist_Japanese.md`: コミット、tag、公開、Zenodo前の確認。
- `manual/` / `manual_Japanese/`: 日英ユーザーマニュアル。

## 維持管理方針

- 新しい作業は日英の`PROJECT_STATUS`と最新作業ログから始める。
- 実質的な作業後は日英両方の作業ログを更新する。
- ユーザー向けの振る舞い、ページ名、出典、引用、制約の変更は日英READMEとマニュアルに反映する。
- テストの追加・削除・目的変更は日英testingガイドに反映する。
- 公開・Git・Zenodo手順の変更は日英release checklistに反映する。
- Earthquakeは単独実行を維持し、公開準備中はSeawaterへの実行時依存を追加しない。
- cache、`.DS_Store`、認証情報、作業用archiveを公開Gitへ含めない。
