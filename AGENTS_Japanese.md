# EnvGeo-Earthquake プロジェクト作業指示

[English version](AGENTS.md)

作業前に、ローカルに存在する場合は日英の`LOCAL_WORKSPACE`を最初に読む。
続けて、日英の`PROJECT_STATUS`、TODO、`development_workflow`、作業ログの
最新記録を読む。公開、配布、CI、Zenodo、出典、共通化に関係する場合は
日英の`publication_audit_2026-10-08`も読む。

## プロジェクトの境界

- 現状のアプリ挙動と機能を維持する。安定動作、正確な文書、test、配布、
  releaseに本当に必要な変更だけを追加し、推測的なvalidationや機能は追加しない。
- 挙動を追加する前に、防ぐ具体的な失敗または解消する公開blockerを示し、
  testで確認できる最小変更を優先する。
- Earthquakeは単独で実行・テスト・配布・保存可能に保つ。
- ユーザーが別途明示しない限り`../envgeo_seawater_v130`を変更しない。
- 現在の公開準備中はSeawaterや将来のCoreへの実行時依存を追加しない。
- Core候補は候補のまま記録し、両アプリの独立した回帰証拠が揃うまで移動しない。
- USGS、地震カタログ、マグニチュード/深さ/時間、プレート境界、JMA/NIED比較はEarthquake固有とする。
- USGS `Status`/`Alert`とSeawater物理範囲の品質フラグを同一視しない。

## 記録と証拠

- EnvGeo-Seawaterのコードコメント形式を踏襲し、主要sectionごとに
  `English / 日本語`の簡潔な見出しを置く。必要な場合は目的説明も日英対応で
  併記する。新規・実質変更sectionから適用し、無関係な一括翻訳は行わない。
- 実質的な作業ごとに日英両方の作業ログへ追記する。
- 現状、ブロッカー、確認済み証拠、次の一手が変わったら日英の`PROJECT_STATUS`を更新する。
- 優先順位や完了状態の変更は日英TODOへ反映する。
- ユーザー向け変更は日英README、マニュアル、Home履歴へ反映する。
- 正確な実行コマンド、環境、pass/skip/fail数、手動確認を記録し、未実行は成功としない。
- 生成物、cache、認証情報、非公開データ、開発専用archiveを公開物に含めない。
