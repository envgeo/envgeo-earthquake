# EnvGeo-Earthquake 開発・文書更新手順

[English version](development_workflow.md)

最終更新: 2026-10-08

## 作業開始時

1. ルートの`PROJECT_STATUS_Japanese.md`を読む。
2. `TODO_Japanese.md`の直近項目と日英両方の作業ログ最新記録を読む。
3. 公開、CI、Zenodo、出典、共通化の作業では`publication_audit_2026-10-08_Japanese.md`も読む。
4. 開発フォルダ、公開用Gitクローン、対象バージョンを明記する。
5. Seawater側を変更せず、実行時依存も追加しないことを確認する。

## 作業中

- 大きなUI統合やCore抽出より、テスト可能な小さな変更を優先する。
- PythonではSeawaterのsection comment方式を踏襲し、主要sectionごとに
  `English / 日本語`の短い見出しを置く。理解に必要な場合は目的説明も日英で併記する。
  新規または変更対象sectionから適用し、無関係なcommentの一括書換えは行わない。
- 日英、Simple / Advancedの一方だけが変更されないよう確認する。
- 外部APIの自動テストはモックを基本とし、CIをUSGSや地図タイルの稼働状態に依存させない。
- 削除、改名、公開対象の変更前に、参照先と影響範囲を調べる。
- 環境不足や未実行の確認は、成功とせず未確認と記録する。

## 作業後の更新

日英両方の作業ログに、日付、目的、変更範囲、変更しなかった範囲、判断、
正確なテストコマンドと結果、手動確認、次の作業を記録する。

該当する場合は次も日英同時に更新する。

- 現状、ブロッカー、証拠、次の一手: `PROJECT_STATUS`
- 優先順位と完了状態: TODO
- 公開機能の変更: READMEとユーザーマニュアル
- リリースまたはユーザー影響のある変更: Home更新履歴
- テスト・skipの変更: testingガイド
- CI、配布、GitHub、Zenodo手順: release checklist
- 外部データ、タイル、アセット: `NOTICE.md`と出典記録

## 作業ログの最小テンプレート

```markdown
## YYYY-MM-DD — 作業名

- 目的:
- 変更:
- 変更しなかった範囲:
- 確認:
  - `command`: N passed, N skipped, N failed
  - 手動確認:
- 判断と理由:
- 残件 / 次の一手:
```
