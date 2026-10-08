# EnvGeo-Earthquake 作業記録

[English version](work_log_English.md)

## 運用方針

- 作業の本体は `earthquake_map_v030` で行う。
- 作業フォルダで構文確認、pytest、必要に応じた Streamlit 画面確認を行ってから、Git clone へコピーする。
- README、README_Japanese、Home の更新履歴、docs は、機能変更やUI文言変更に合わせて随時更新する。
- `.DS_Store`、`__pycache__/`、`.pytest_cache/` などの生成物は Git clone へコピーしない。
- EnvGeo-Seawater と将来の共通コア化を意識しつつ、Earthquake 固有処理は無理に共通化しない。

## 2026-10-08 — Phase 5前checkpointを公開Git cloneへ反映

- 目的: Phase 5開始前に、確認済みのEarthquake単独版をcommit可能なcheckpointとして
  公開Git cloneへ揃える。
- userの明示指示に基づき、開発フォルダの公開対象をcloneへ同期した。
- `.git`、`.DS_Store`、cache、`old/`、`data/`、`__ToDo__/`、`__logo__/`、`images/`、
  `.devcontainer/`、local workspace日英記録は除外した。削除同期は行っていない。
- clone上で`PYTHONDONTWRITEBYTECODE=1 pytest -q -p no:cacheprovider`を実行し、
  `176 passed in 2.69s`、skip 0を確認した。`git diff --check`の指摘はREADME類の
  Markdown強制改行用末尾2spaceであり、code errorではない。
- cloneは`main` / `origin/main`のままで、差分は意図的に未commit・未push。
  commit / pushはuserがGitHub Desktopで行う。
- EnvGeo-Seawater、EnvGeo Core、remote、tag、releaseは変更していない。
- 次: GitHub Desktopで差分確認・commit・push後、Phase 5へ進む。

## 2026-10-08 — Plotly 3D視点操作案内の日英追加

- 目的: EnvGeo-Seawaterの簡潔な操作案内を踏襲し、page layoutを広げずPlotlyの
  camera操作を見つけやすくする。
- 日英のSimple / Advanced 4pageすべてで、主要3D震源図の直前にcaptionを追加した。
- ドラッグ回転、右上のPlotly toolbarによる回転・平行移動・拡大縮小・初期視点への復帰、
  `Shift`・`Control`・`Option`（`Alt`）・`Command`とmouse dragの組合せで視点や中心の動かし方を
  変えられることを案内する。
- macOSで`Shift`ではなく`Option`キーが有効だった実機確認を受け、画面案内・manual・
  test・関連記録へ`Option`（`Alt`）を追加した。
- 日本語案内は、可能性だけを示す「変わることがあります」から、操作できることを明示する
  「動かし方を変えることができます」へ改めた。browser・OSによる挙動差の注記は維持した。
- modifier keyの実挙動はbrowser・OSにより異なることを明記し、特定platformの操作を
  一律に保証しない。
- 日英Simple / Advanced manualに同じ案内を追加し、README、Home履歴、testing、TODO、
  audit、引継ぎ記録を同期した。
- `test/test_plotly_camera_guidance.py`に日英4 contractを追加。`Option`を含むmodifier keyの記載と、
  案内が主要3D図より前にあることを保護する。
- 確認: 対象test `4 passed in 0.01s`、最終全suite `176 passed in 2.87s`、skip 0、現行・test
  Python 20fileの構文解析に合格。
- 変更しなかった範囲: 図の計算・camera既定、app version、依存、公開用Git clone、
  EnvGeo-Seawater、EnvGeo Core。

## 2026-10-08 — Phase 5前のmarker size方式・強調倍率追加

- 目的: Phase 5前の表示reviewに対応し、科学機能やdata sourceの範囲は広げず、
  現行のUSGS中心workflowを保ったままmarker sizeの意味と変化をわかりやすくする。
- 現行4 visualizer pageすべてに`マーカーサイズ方式`を追加。先頭・既定は
  `マグニチュード連動`、第2選択肢は`固定サイズ`とし、英語pageも対応表記にした。
- 1つの選択を主要3D震源図、2D分布図、Advancedの断面位置図・断面図に統一適用した。
- 個別のinline計算式を、各pageのEarthquake-local `earthquake_marker_sizes()` helperへ整理した。
  公開安定化中にEnvGeo Coreを先行抽出せずEarthquake単独動作を保つため、小規模重複は意図的に維持した。
- marker倍率の既定をすべて`1.0`にした。最初の`scale ** 1.5`、次の`scale ** 2.0`でも
  効果が弱いと判断されたため、試行で`0.2–20.0`の明確な直接倍率に変更した。
  user確認後は`10.0`が十分とされたため、最終範囲を`0.2–10.0`とした。試行時に早期clipされないよう、3D / 2D /
  断面の上限を180 / 450 / 280 pixelへ広げ、下限で非表示に近い過小化を防ぐ。
- 3D・2D・断面のmagnitude連動profileを強化した。要望の「増幅率」は全体sliderではなく
  magnitude間の大きさ差であると明確化されたため、ほぼ線形の式を
  `reference_size * 20 ** ((M - 4) / 3)`へ変更した。全体倍率`1.0`で、全3 profileの
  M7 marker直径をM4の約20倍とする。これは物理的なenergy・断層面積scaleではなく、
  表示上の強調と明記した。固定方式は一定pixel sizeを使い、欠損・非数値・負のmagnitudeは
  引き続き0として安全に扱う。
- `マグニチュード強調率（M7 / M4 直径比）`を`1–30`、既定`20`で追加し、計算式は
  選択比を使う。固定size時はこのsliderを無効化した。
- `test/test_marker_size_modes.py`に、日英4page×3表示profileを対象と40件の決定論的testを追加。
  magnitudeでの単調増加、M7:M4の既定20:1・調整時5:1、固定方式の一定size、
  全体直接倍率、sliderの存在、日英の連動既定を保護する。
- 最初の対象testで、固定分岐がscalarを返しSeriesとしてclipできない不具合を検出。
  入力indexに合わせたSeriesを返すよう修正し、marker / coordinate 48 testの再実行は合格した。
- 日英Simple / Advanced manual、TODO、Home更新履歴、testing guide、引継ぎを同期した。
  Phase 5は未着手で、次の作業は引き続実network非依存のPython 3.10 / 3.12 GitHub Actions CIである。
- 確認:
  - 編集した4 pageの`python -m py_compile`に合格。
  - 最終増幅強化後の対象`pytest -q test/test_marker_size_modes.py`: `40 passed in 0.67s`。
  - 最終全`pytest -q`: `172 passed in 2.81s`、skip 0。
- 変更しなかった範囲: app version、data取得・filter logic、提供元範囲、依存、公開用Git clone、
  EnvGeo-Seawater、EnvGeo Core。

## 2026-10-08 — Phase 4 repository-health check完了

- 目的: 作業folderの開発資料を削除せず、日英の公開対象方針をportableな自動checkへ変換し、
  Phase 4最後の項目を完了する。
- `test/test_repository_health.py`へ8 checkを追加:
  - 公開候補を許可済みroot file・directoryだけに限定。
  - `.gitignore`が開発専用directory、local workspace記録、secret file、生成物、cache、log、
    build出力を除外。
  - standalone Git cloneで実行する場合、tracked fileに除外・生成pathがない。
  - active runtime Pythonが除外directoryへlocal依存しない。
  - 公開textに一般的な実値token・秘密鍵・credential patternがない。
  - 公開textにuser名を含むmacOS / Linux / Windows絶対pathがない。
  - 公開候補にsymlinkがない。
  - Markdownの全local linkが解決する。
- 最初の対象runで、JMA公式URLの`data/`などをlocal `data/`依存と誤判定するtest側の
  false positiveを確認した。HTTP(S) URLを除いてからlocal runtime参照を調べるように修正し、
  正規の提供元URLを許可しながら依存checkを維持した。
- candidate viewは除外・生成local fileを削除せず判定から除く。testをstandalone公開cloneへ
  copy後はtracked-file branchが自動的に有効になる。
- userのmarker size質問を再確認した。4pageすべてで主要2D・3D marker sizeは既にmagnitudeから
  計算し、Advanced 2pageの断面markerもmagnitude連動である。既存sliderは全体倍率を適用する。
  固定size・magnitude連動の切替はない。日英Simple / Advanced manualへ明記し、機能・runtime
  codeは変更していない。
- roadmap、TODO、testing guide、test note、release checklist、公開監査、日英Home履歴、
  引継ぎを同期した。Phase 4は完了。
- 確認:
  - 対象 `/opt/anaconda3/bin/pytest -q test/test_repository_health.py`:
    `8 passed in 0.10s`。
  - 最終 `/opt/anaconda3/bin/pytest -q`: `132 passed in 2.34s`、skip 0。
  - `ast.parse`: 現行・test Python 18fileに合格。
  - Markdown: 55file、local link/image 108件、欠損0件。
  - 公開用cloneはcleanを維持: `## main...origin/main`。
- 変更しなかった範囲: 除外local file、marker sizeのruntime挙動、依存、app version、
  公開用Git clone、EnvGeo-Seawater、EnvGeo Core抽出。
- 次の1項目: Phase 5としてPython 3.10 / 3.12の実network非依存GitHub Actions CIを追加する。

## 2026-10-08 — 日英page startup AppTestの永続化

- 目的: 毎回手動commandで繰り返していたStreamlit起動確認を通常pytest suiteへ移し、
  Phase 4の次項目を完了する。
- 日英Home / Simple / Advancedの初期AppTest element treeを確認した。6pageすべてが安定した
  共通titleと言語別主要見出しを持ち、4 visualizer pageは既定の上下取得buttonを持つ。
- `test/test_app_smoke.py`へ6件のparameterized caseを追加:
  - 日英Homeが`EnvGeo-Earthquake`と代表的な各言語section見出しを表示し、取得buttonを持たない。
  - 英語Simple / Advancedが共通version付き見出しと、`Fetch / update`、
    `Fetch / update!`を各1個表示する。
  - 日本語Simple / Advancedが共通version付き見出しと、`取得 / 更新`、
    `取得 / 更新！`を各1個表示する。
  - 全pageが60秒以内にStreamlit例外0件で終了する。
- testは`envgeo_utils.APP_VERSION`をimportし、release文字列を重複定義せず表示上の共通version
  contractを確認する。
- 範囲: 実USGS取得を起動しない決定論的な初期描画coverageである。Region / hotspot操作、
  取得・filter、空結果message、download、session state、見た目は後続の自動・手動確認に分ける。
- application runtime code、UI文言、依存、page挙動は変更していない。
- roadmap、TODO・testing方針、testing guide、test note、release checklist、公開監査、
  日英Home履歴、引継ぎを同期した。
- 確認:
  - 対象 `/opt/anaconda3/bin/pytest -q test/test_app_smoke.py`:
    `6 passed in 1.04s`。
  - 最終 `/opt/anaconda3/bin/pytest -q`: `124 passed in 2.42s`、skip 0。
  - `ast.parse`: 現行・test Python 17fileに合格。
  - Markdown: 55file、local link/image 108件、欠損0件。
  - 公開用cloneはcleanを維持: `## main...origin/main`。
- 変更しなかった範囲: application runtime code、USGS・network挙動、UI、依存、app version、
  公開用Git clone、EnvGeo-Seawater、EnvGeo Core抽出。
- 次の1項目: 公開対象、秘密情報、絶対local pathのrepository-health testを追加する。

## 2026-10-08 — plate-boundary fallback経路のtest・安定化

- 目的: 実network通信なしで日英Advancedのplate service正常・失敗・日本限定fallbackを
  確認し、Phase 4の次項目を完了する。
- 日英で重複するplate loaderを監査した。既存実装はservice全面失敗時に、明示的に
  approximateとした日本周辺6模式線を使い、他のregion presetには適用しない設計だった。
- 公開品質上の具体的な不具合を2件再現:
  - HTTP成功でも`features`がlistでない、またはlist内featureがobjectでないresponseは、
    feature変更時に例外となる可能性があった。
  - main plate取得成功・任意microplate失敗時に、日本fallback線を表示中と誤案内した。
- feature変更前に同じ最小の日英guardを追加。不正構造を読めるlayer errorへ変換し、
  既存の安全なfallback経路へ渡す。
- warningを返却sourceで分岐。真の日本fallbackは既存warningを維持し、USGS部分成功では
  取得済みUSGS layerだけを表示すると案内する。正常data、fallback geometry、control、
  map描画は変更していない。
- `test/test_plate_boundary_fallback.py`を追加し、日英Advancedの実helper定義をAST抽出して
  直接実行する13件の実通信なしcaseを確認:
  - main plate・microplate正常取得、layer label、ArcGIS GeoJSON query parameter。
  - 接続全面失敗時は日本だけ明示的な模式dataを使う。
  - 日本以外の全面失敗は空の境界DataFrameを返す。
  - listでない`features`・objectでないfeatureを日本fallbackで安全に処理。
  - microplateだけHTTP 503でも有効なUSGS main-plate dataとsourceを維持。
  - 日英UI codeが部分USGS dataと真のfallbackを区別する。
- roadmap、TODO、testing guide、test note、release checklist、公開監査、日英Home履歴、
  引継ぎを同期した。
- 確認:
  - 対象 `/opt/anaconda3/bin/pytest -q test/test_plate_boundary_fallback.py`:
    `13 passed in 0.47s`。
  - 最終 `/opt/anaconda3/bin/pytest -q`: `118 passed in 2.12s`、skip 0。
  - `ast.parse`: 現行・test Python 16fileに合格。
  - Streamlit `AppTest`: 日英Home / Simple / Advancedの6fileすべて例外0件。
  - Markdown: 55file、local link/image 108件、欠損0件。
  - 公開用cloneはcleanを維持: `## main...origin/main`。
- 変更しなかった範囲: 正常plate data・map geometry、fallback線定義、control、依存、
  app version、公開用Git clone、EnvGeo-Seawater、EnvGeo Core抽出。
- 次の1項目: 日英Homeと現行4 visualizer pageの永続AppTest coverageを追加する。

## 2026-10-08 — 経度・日付変更線・local km・断面幾何test

- 目的: 動作中のruntime codeを変えず、Phase 4の次の空間幾何項目について日英pageの
  現在挙動を記録する。
- 日英Simple / Advanced 4pageの実helperを比較した。経度ラップ、地図継ぎ目line処理、
  正距円筒近似local km変換は同一で、Advanced 2pageの断面unwrapping・投影・断面帯helperも
  同一だった。
- 再現可能な不具合はなかったため、page・utility実装は変更していない。作り直した実装でなく
  実際のpage関数をAST抽出する`test/test_spatial_geometry.py`だけを追加した。
- 4pageを対象とする12 caseを追加:
  - 等価な経度値を選択した360度branchへ揃える。
  - 日付変更線横断lineをGreenwich中心の継ぎ目では`NaN`分割し、太平洋branchでは
    170、179、181、190として連続させる。
  - 中央経線180°に対し179°E・179°Wを約−111.320 km・+111.320 kmの近接local座標へ変換。
- 日英Advancedを対象とする8 caseを追加:
  - 170°E→170°Wと逆向きを20度の短経路にする。
  - 断面方向距離、符号付き横ずれ、赤道上で約2,226.4 kmの断面長を確認。
  - 始終点一致は安全な空断面・長さ0を返す。
  - 5点の断面帯polygonが360度の継ぎ目jumpなしで閉じる。
- roadmap、TODO、testing guide、test note、release checklist、公開監査、日英Home履歴、
  引継ぎを同期した。
- 確認:
  - 対象 `/opt/anaconda3/bin/pytest -q test/test_spatial_geometry.py`:
    `20 passed in 0.77s`。
  - 最終 `/opt/anaconda3/bin/pytest -q`: `105 passed in 2.06s`、skip 0。
  - `ast.parse`: 現行・test Python 15fileに合格。
  - Streamlit `AppTest`: 日英Home / Simple / Advancedの6fileすべて例外0件。
  - Markdown: 55file、local link/image 108件、欠損0件。
  - 公開用cloneはcleanを維持: `## main...origin/main`。
- 変更しなかった範囲: runtime page・utility code、UI、空間計算式、依存、app version、
  公開用Git clone、EnvGeo-Seawater、EnvGeo Core抽出。helperは将来Core候補の記録だけを維持。
- 次の1項目: Advanced pageのplate-boundary network fallbackをtestする。

## 2026-10-08 — 不正USGS描画座標のguard・test

- 目的: 通常のUSGS表示経路を維持したまま、地震座標の欠損・範囲外値の挙動を
  決定論的にし、Phase 4の次項目を完了する。
- 日英Simple / Advanced 4pageの`prepare_plot_dataframe()`を監査した。欠損座標は
  既に除外していたが、GeoJSONの経度・緯度範囲を超える数値も描画対象に残っていた。
- 各pageのEarthquake固有描画準備へ同じ最小guardを追加:
  - 経度、緯度、深さを数値へ変換。
  - 描画必須座標が欠損する行を除外。
  - 経度`[-180, 180]`、緯度`[-90, 90]`の境界を含めて保持。
  - 非数値・範囲外の経度緯度を除外。
- 変更したpage関数へ、Seawater方式を踏襲した日英commentと目的説明を追加した。
- `test/test_page_coordinates.py`を追加。作り直した実装ではなく、4pageそれぞれの実helperを
  ASTで抽出して直接実行する8 caseで、有効な中央・境界行、欠損・非数値、4方向の範囲外、
  marker size、全行不正時の安全な空結果を確認する。
- 範囲: 任意JMA/NIED upload正規化、受付alias・schema、経度ラップ・日付変更線、query、
  UI、依存は変更していない。汎用validation frameworkも追加していない。
- roadmap、TODO、最小validation方針、testing guide、test note、release checklist、
  公開監査、日英Home履歴、引継ぎを同期した。
- 確認:
  - 対象 `/opt/anaconda3/bin/pytest -q test/test_page_coordinates.py`:
    `8 passed in 0.78s`。
  - 最終 `/opt/anaconda3/bin/pytest -q`: `85 passed in 2.45s`、skip 0。
  - `ast.parse`: 現行・test Python 14fileに合格。
  - Streamlit `AppTest`: 日英Home / Simple / Advancedの6fileすべて例外0件。
  - Markdown: 55file、local link/image 108件、欠損0件。
  - 公開用cloneはcleanを維持: `## main...origin/main`。
- 変更しなかった範囲: 有効なUSGS表示結果、任意upload挙動、app version、公開用Git clone、
  EnvGeo-Seawater、EnvGeo Core抽出。
- 次の1項目: page挙動を変えず、経度ラップ、日付変更線、ローカルkm、断面幾何をtestする。

## 2026-10-08 — 任意JMA/NIED uploadの最小smoke test追加

- 目的: 初回releaseにおける任意JMA/NIED比較の位置づけを広げず、維持に必要な最小限の
  回帰coverageを追加してPhase 4の次項目を完了する。
- 日英Advanced page双方で重複するupload helper、`normalize_column_name()`、
  `find_catalog_column()`、`read_uploaded_catalog()`、
  `normalize_external_catalog()`を監査した。
- 各pageをPython ASTで解析し、実際のhelper定義を抽出して直接実行するtestを追加した。
  別に作り直したparserのmockではなく、現在のpage実装そのものを対象としている。
- 各pageに正常CSV 1件を追加。longitude、latitude、depth、magnitude、catalog、place、
  UTC timeの正規化と、warning・errorが出ないことを確認する。
- 各pageに必須列欠損CSV 1件を追加。未処理例外を出さず、空の結果と読めるwarning 1件を
  返すことを確認する。
- roadmap、TODO、testing guide、test note、release checklist、公開監査、日英Home履歴、
  引継ぎを同期した。
- 確認:
  - 対象 `/opt/anaconda3/bin/pytest -q test/test_upload_formats.py`:
    `7 passed in 0.49s`。
  - 最終 `/opt/anaconda3/bin/pytest -q`: `77 passed in 1.58s`、skip 0。
  - `ast.parse`: 現行・test Python 13fileに合格。
  - Streamlit `AppTest`: 日英Home / Simple / Advancedの6fileすべて例外0件。
  - Markdown: 55file、local link/image 108件、欠損0件。
  - 公開用cloneはcleanを維持: `## main...origin/main`。
- 変更しなかった範囲: runtime code、受付alias・schema、upload形式、比較UI、依存、
  app version、公開用Git clone、EnvGeo-Seawater、EnvGeo Core抽出。
- 次の1項目: 現在の表示挙動を維持したまま、地震座標の`NaN`と範囲外値について
  決定論的coverageを追加する。

## 2026-10-08 — USGS query構築・取得上限warningのtest

- 目的: user-facing挙動を変えず、API request contractとwarning境界を決定論的にし、
  Phase 4の第2項目を完了する。
- 4つのvisualizer pageを監査し、全pageが同じ日時、magnitude、depth、緯度、経度、
  並び順、limitを共通loaderへ渡し、`len(df_eq) >= query["limit"]`で既存warningを
  表示していることを確認した。
- `envgeo_utils.py`のUSGS読込み日英sectionへ、Earthquake-local純粋helperを2つ抽出:
  - `build_usgs_earthquake_query_url()`: FDSN query URLを構築。
  - `usgs_result_limit_reached()`: 結果省略可能性warningの境界を判定。
- 4pageを共通limit helper利用へ変更。warning文言、配置、表示時点は変更していない。
  EnvGeo CoreやSeawater依存は追加していない。
- 決定論的testを追加:
  - endpoint、`format=geojson`、`eventtype=earthquake`、ISO日時、`orderby`、整数limit、
    magnitude/depth/座標の任意8 filterを確認。
  - `None`・`NaN`任意filterがURLから除外されることを確認。
  - 取得行数が指定limit未満ではfalse、同数・超過ではtrueとなる境界を確認。
  - 日英Simple / Advancedの4pageすべてが共通条件と`st.caption()` warning経路を維持。
- roadmap、TODO、testing note、release checklist、公開監査、Home履歴、引継ぎを同期。
  query・warning挙動は不変のためmanualは変更していない。
- 確認:
  - 対象 `/opt/anaconda3/bin/pytest -q test/test_envgeo_utils.py`:
    `26 passed in 0.60s`。
  - 最終 `/opt/anaconda3/bin/pytest -q`: `73 passed in 1.43s`、skip 0。
  - `ast.parse`: 現行・test Python 13fileに合格。
  - Streamlit `AppTest`: 日英Home / Simple / Advancedの6fileすべて例外0件。
  - Markdown: 55file、local link/image 108件、欠損0件。
  - 公開用cloneはcleanを維持: `## main...origin/main`。
- 変更しなかった範囲: API parameter semantics、warning文言・時点、UI control、依存、
  app version、公開用Git clone、EnvGeo-Seawater、Core抽出。
- 次の1項目: 任意JMA/NIED比較についてschemaを広げず、正常upload 1件と
  読込み不能または必須列欠損1件だけを自動smoke testする。

## 2026-10-08 — USGS loader失敗coverageの完成

- 目的: 実network通信を行わず、USGSの正常、空、欠損、不正形式、HTTP error、
  timeout、接続失敗を対象とするPhase 4最初のtest項目を完了する。
- 4つの現行visualizer pageが共通利用する`load_usgs_earthquake_data()`を監査した。
  実装は既に`HTTPError`、`URLError`、`TimeoutError`、不正JSON、不正なGeoJSON
  `features`を、全pageがcatchする読める`RuntimeError`へ変換していた。
- runtime code変更は不要で、不足していた回帰証拠だけを追加した:
  - 正常FeatureCollection、空結果、properties/geometry欠損featureのloader test。
  - HTTP 503、DNS/接続失敗、timeoutのtransport test。
  - 既存の不正JSON、listでない`features` testは維持。
- 成功caseでは行数・Event IDと、DataFrame metadataにquery URLが付くことも確認した。
  query parameter全体のcoverageはまだ主張せず、次のroadmap項目として残した。
- roadmap、TODO、testing guide、test note、release checklist、公開監査、Home履歴、
  引継ぎを同期した。app挙動は変わらないためuser manualは変更していない。
- 確認:
  - 対象 `/opt/anaconda3/bin/pytest -q test/test_envgeo_utils.py`:
    `20 passed in 0.61s`。
  - 最終 `/opt/anaconda3/bin/pytest -q`: `67 passed in 1.46s`、skip 0。
  - `ast.parse`: 現行・test Python 13fileに合格。
  - Streamlit `AppTest`: 日英Home / Simple / Advancedの6fileすべて例外0件。
  - Markdown: 55file、local link/image 108件、欠損0件。
  - 公開用cloneはcleanを維持: `## main...origin/main`。
- 変更しなかった範囲: runtime loader/error message、page UI、query control、依存、
  app version、公開用Git clone、EnvGeo-Seawater、Core。
- 次の1項目: USGS query構築と取得件数上限warningをtestする。

## 2026-10-08 — JMA/NIEDの利用・再配布責任の記録

- 目的: 任意比較機能の実装を維持したまま、Phase 3最後の出典・license項目を完了する。
- EnvGeo-Seawaterの再配布監査方針を読取り専用で参照し、「公開されている」「引用できる」
  だけではdataset再配布許可の根拠にしない考え方を採用した。Seawaterは変更していない。
- 2026-10-08に提供元公式資料を再確認:
  - JMA website contentは個別指定がない限り公共データ利用規約第1.0版に従い、
    出典・該当page、編集加工の表示、国作成と誤認させないこと、第三者権利確認を求める。
  - JMA地震月報の利用案内は、統合解析にNIED、大学、研究機関、自治体などの
    観測dataが含まれることを記録している。
  - NIED Hi-netはdownload data・震源情報の再配布を禁止し、提供元・利用登録経由の取得、
    全提供機関の謝辞、DOI `10.17598/NIED.0003`の引用、成果報告を求める。
    Hi-net経由の他機関dataには各提供元規則も適用される。
- `docs/jma_nied_data_responsibilities.md`と日本語版の専用記録を追加した。
  upload受付やCSV/XLSX形式変換は再利用権を付与せず、この記録はproject案内で
  法的助言ではないことを明記した。
- `envgeo_utils.py`の日英sectionへJMA/NIED公式link、NIED引用、確認日を集約した。
- 日英Homeの出典・履歴、README、比較manual、NOTICE、docs index、監査、roadmap、
  TODO、testing、release checklist、引継ぎを同期した。
- 公開判断: JMA/NIED catalogをrepository、package、GitHub Release、予定Zenodo archiveへ
  同梱しない。appはupload元dataを自動取得、認証、権利判定、永続保存しない。
  任意比較は最初release/DOIの必須条件にしない。
- 公式domain参照、NIED DOI、日英Home利用、両責任記録を確認する決定論的contract testを1件追加。
- 確認:
  - 対象 `/opt/anaconda3/bin/pytest -q test/test_basic.py`: `5 passed`。
  - 全体 `/opt/anaconda3/bin/pytest -q`: `61 passed in 1.48s`、skip 0。
  - `ast.parse`: 現行・test Python 13fileに合格。
  - Streamlit `AppTest`: 日英Home / Simple / Advancedの6fileすべて例外0件。
  - Markdown: 55file、local link/image 108件、欠損0件。
  - 公開用cloneはcleanを維持: `## main...origin/main`。
- 変更しなかった範囲: 比較の読込み・schema・UI、upload受付形式、依存、app version、
  公開用Git clone、EnvGeo-Seawater、Core。
- Phase 3の出典・license項目は完了。次の1項目: USGSの正常、空、欠損、不正形式、
  HTTP error、timeout、接続失敗を実通信なしtestで完成させる。

## 2026-10-08 — map挙動を変えないonline地図attribution再確認

- 目的: Phase 3の次項目として、現行の標準、衛星画像、海底地形、GSI背景の
  sourceを提供元案内と照合する。
- EnvGeo-Seawaterの地図実装とoffline operation記録を構成上の参考として読取り専用で
  確認した。Seawaterのsource、data、docsは編集せず、依存も追加していない。
- 文書上の不一致を確認・訂正した。Earthquake active codeは2026-09-20以降
  Plotlyの`open-street-map` styleを使うが、日英Home、README、NOTICEにはCARTO
  basemapとの表記が残っていた。CARTO tileは設定していない。OpenStreetMapの
  copyrightとtile利用方針を示し、一括download・prefetch禁止の注意を追加した。
- `envgeo_utils.py`の日英sectionに、Earthquake-localのmap URL、提供元link、
  実行時credit、確認日を集約した。map選択とtile endpointは変更していない。
- 提供元資料に合わせて実行時creditを更新した:
  - USGS imagery: 従来の曖昧な`USGS`から
    `USDA, USGS The National Map: Orthoimagery`へ更新。
  - Esri World Ocean Base: 現行のEsri Ocean Basemap contributor表記へ更新し、
    日英文書に航海・海上安全判断用でないことを明記。
  - GSI標準tile: `国土地理院`をtile一覧へlinkし、静的出版・再配布では最新条件・
    手続きを再確認することを文書化。
- NOTICE、日英README、Home出典・更新履歴、export/use-note manual、監査、roadmap、
  TODO、testing、release checklist、引継ぎを同期した。
- StandardがOpenStreetMapのままであることと、3つの明示raster layerのURL/credit
  pairを確認する実通信なしtestを1件追加した。
- 確認:
  - 対象 `/opt/anaconda3/bin/pytest -q test/test_offline_map.py`:
    `32 passed in 1.19s`。
  - 全体 `/opt/anaconda3/bin/pytest -q`: `60 passed in 1.75s`、skip 0。
  - `ast.parse`: 現行・test Python 13fileに合格。
  - Streamlit `AppTest`: 日英Home / Simple / Advancedの6fileすべて例外0件。
  - Markdown: 53file、local link/image 102件、欠損0件。
  - active/public文書に`carto.com` linkはなく、残るCARTO文字列は未設定または
    訂正記録だけである。
  - 公開用cloneはcleanを維持: `## main...origin/main`。
- 変更しなかった範囲: map選択・tile endpoint、地震処理、依存、app version、
  公開用Git clone、EnvGeo-Seawater、Core抽出。
- 次の1項目: JMA/NIEDの利用・再配布責任を記録する。

## 2026-10-08 — USGS catalog・plate-boundary引用の共通化

- 目的: Phase 3の第2項目として、日英Home / Simple / Advanced、README、manualで
  USGS catalogとplate-boundaryの引用表記を統一し、将来の表記ずれを防ぐ。
- 2026-10-08に公式・一次情報を再確認:
  - USGS FDSN Event Web ServiceはFDSN Event仕様の実装で、GeoJSON queryと20,000件上限を明記。
  - FDSN USGS data-center recordは、ANSS Comprehensive Catalogの正式引用を
    `U.S. Geological Survey. (2017)...`、DOI `10.5066/F7MS3QZH`として記録。
  - USGS Tectonic Plate Boundaries ArcGIS REST metadataは、USGS Seismicity of the Earth
    Map Series、Bird (2003)、DeMets et al. (2010)を出典として明記し、layer 0を
    Microplates、layer 1をPlatesとしている。
- 実装:
  - `envgeo_utils.py`へ`Earthquake sources and citations / 地震データの出典と引用`
    sectionを追加し、API/service URL、catalog引用、Bird引用、DeMets引用を一元化。
  - 日英Homeと4可視化pageがcatalog引用の共通定義を参照。Simpleにも正式引用と
    FDSN Event Web Service linkを追加。
  - 日英Home・AdvancedがUSGS Map Series URLとBird / DeMets全文引用を共通参照。
    Advancedの既存catalog query、plate取得・fallback・描画処理は変更していない。
  - 日英README、export/notes manual、Home更新履歴、公開監査、roadmap、TODO、
    release checklist、testing guide、test README、PROJECT_STATUSを同期。
  - `test/test_basic.py`へ共通引用contractを1件追加。日英6pageのcatalog引用と、
    該当4pageのMap Series / Bird / DeMets参照を固定した。
- 確認:
  - 対象test `/opt/anaconda3/bin/pytest -q test/test_basic.py`: `4 passed`。
  - 最終全suite `/opt/anaconda3/bin/pytest -q`: `59 passed in 1.56s`、skip 0。
  - `ast.parse`: 現行・test Python 13fileに合格。
  - Streamlit `AppTest`: 日英Home / Simple / Advancedの6fileすべて例外0件。
  - Markdown: 50file、local link/image 100件、欠損0件。
  - active UI code内の3 DOI literalは`envgeo_utils.py`だけにあり、page local重複は0件。
  - 公開用cloneはcleanを維持: `## main...origin/main`。
- 変更しなかった範囲: USGS query parameter・正規化・cache、plate boundary取得・fallback・
  map描画、依存、app version、EnvGeo-Seawater source/data/docs、公開用Git clone。
- 次の1項目: CARTO/OpenStreetMap/USGS imagery/Esri/GSI attributionを再確認する。

## 2026-10-08 — Seawaterの検証記録に基づくNatural Earth海岸線来歴の確定

- 目的: map挙動と海岸線dataを変更せず、Phase 3最初の公開ゲートである同梱海岸線CSVの
  出典、利用条件、派生根拠、fingerprintをEarthquake内へ独立して保存する。
- Seawaterを読取り専用で参照した結果:
  - `docs/geospatial_assets*`と`docs/provenance_inventory*`は、50m・110m CSVを
    Natural Earth coastline v4.1.0由来と記録している。
  - source archiveと座標workbookは2025-01-24に保存され、2026-10-03の監査で現行CSVと
    row数・NaN separatorが一致し、最大絶対数値差は約`1.42e-14`だった。
  - 元raw downloadのchecksum、正確なdownload日、独立conversion scriptは未保持であり、
    過去のraw archiveをbit単位で再構成可能とは表明しない。
  - Seawaterの別directoryにある50m land polygon shapefileは静的map用の別assetであり、
    Earthquakeの2つのcoastline line CSVには含めず、混同しない。
- Earthquakeで追加・同期した内容:
  - `coastline/LICENSE_OR_SOURCE.md`と日本語版に、Natural Earth public-domain条件、v4.1.0、
    保持中間fileとの照合根拠、現行hash、既知の制約、更新時の記録要件を保存。
  - NOTICE、日英README、docs index、manual、Home source/history、日英Advanced source note、
    公開監査、roadmap、TODO、release checklist、PROJECT_STATUSを同期。
  - 50mは61,844 data row / 1,428 separator row、SHA-256
    `c3d7bee4fb696b011fa34bb13bed0c335c5250eeaf37d8739d77d29a27fe385c`。
    110mは5,261 data row / 133 separator row、SHA-256
    `a31df3aeee9dc4195af35a31b0605fdb572c7c7dd7cde17f773c9438f5ec7f3f`。
- 確認:
  - 両CSVは対応するSeawater fileとbyte単位で一致。
  - `/opt/anaconda3/bin/pytest -q`: `58 passed in 1.93s`、skip 0。
  - `ast.parse`: 現行・test Python 13fileに合格。
  - Streamlit `AppTest`: 日英Home / Simple / Advancedの6fileすべて例外0件。
  - Markdown: 50file、local link/image 100件、欠損0件。最初のchecker one-linerは
    `SyntaxError`だったため修正して再実行し、この成功結果だけを合格証拠とした。
  - 公開用cloneはcleanを維持: `## main...origin/main`。
- 変更しなかった範囲: 海岸線CSV本体、map/runtime処理、依存、app version、
  EnvGeo-Seawaterのsource/data/docs、公開用Git clone、EnvGeo Core依存。
  Seawater側の時刻確認ではmacOS管理file `.DS_Store`だけが作業中時刻を示したが、
  今回のtoolで編集しておらず、source/data/docsの変更証拠には含めない。
- 判断: 海岸線asset loader・metadataは将来のCore候補だが、最初のEarthquake DOI releaseまでは
  各appにlocal copyと独立した来歴記録を維持する。
- 次の1項目: USGS catalogとplate-boundaryの引用文を日英で統一する。

## 2026-10-08 — JMA/NIED upload比較を任意機能に分類

- 目的: Advanced pageのJMA/NIED uploadが中核アプリに必要かを判断し、機能を拡張せず
  現行の失敗処理を監査する。
- 必要性の判断:
  - EnvGeo-Earthquakeの中核workflowは公式USGS catalog dataの取得・表示であり、
    JMA/NIED upload比較は必須ではない。
  - 日本周辺の専門的な研究では利用価値があるため、現状挙動維持のため変更せず残す。
  - 最初の安定release・Zenodo DOIのゲートではない任意Advanced機能に分類する。
    新形式、alias、schema、validation subsystem、JMA/NIED自動取得は追加しない。
- 直接監査方法: 外部serviceを動かさず、日英Advanced pageから4つのupload helperを抽出して次を実行。
  - 経度、緯度、深さ、magnitudeを持つ正常CSV: 1正規化row。
  - 必須列がないCSV: 安全な空結果とwarning 1件。
  - 壊れたXLSX byte stream: 安全な空結果と読めるerror 1件。
- 結果: 日英実装とも3caseすべて未処理例外なし。具体的な不具合がないため、
  runtime codeとtest fileは変更しなかった。
- privacy/lifecycle表記: 選択内容は現在のStreamlit sessionで読み、アプリが意図的に
  永続data storeへ書き込まないことを文書化。提供元の利用条件は利用者責任とする。
- 合意した最小範囲で公開ロードマップPhase 2は完了。
- 日英で同期した文書: 検証方針、JMA/NIED manual、README、ロードマップ、TODO、
  project status、公開監査、release checklist、Home更新履歴、作業ログ。
- 文書更新後の確認:
  - 全suite: `58 passed in 2.32s`、skip 0。
  - 構文解析: 現行・testのPython 13ファイルに合格。
  - Streamlit `AppTest`: Home・現行pageの6ファイルすべて例外0件で起動。
  - Markdown: 51ファイル、local link 92件、欠損0件。
  - 公開用cloneはcleanを維持: `## main...origin/main`。
- 範囲: アプリcode、version、依存は変更せず、公開用cloneとEnvGeo-Seawaterも変更していない。
- 次の1項目: map挙動を変えず、同梱海岸線CSVにNatural Earth出典・license記録を追加する。

## 2026-10-08 — USGS失敗経路の焦点監査と2つの最小guard

- 目的: 現状機能維持の方針に従い、現行USGS取得経路を監査し、再現できた
  未処理crashにだけcode変更を行う。
- 変更不要と確認した現行挙動:
  - `HTTPError`、`URLError`、`TimeoutError`は、共通loaderで既に読める`RuntimeError`へ変換される。
  - 現行4可視化pageはすべて`RuntimeError`をcatchし、`st.error`で表示後に安全に停止する。
  - 空FeatureCollectionは既に安定した空DataFrameとなり、各pageの現行no-data messageが表示される。
- 編集前に再現した不足:
  - 不正JSONが未処理の`JSONDecodeError`として伝播する。
  - `features`がmappingのresponseで文字列keyを走査し、
    `AttributeError: 'str' object has no attribute 'get'`になる。
- `envgeo_utils.load_usgs_earthquake_data()`への最小実装:
  - JSON/Unicode decode失敗を`RuntimeError("USGS API returned invalid JSON data.")`へ変換。
  - payloadがdictionaryかつ`features`がlistであることだけを要求し、それ以外は
    読めるunexpected-GeoJSON `RuntimeError`にする。
- `test/test_envgeo_utils.py`に、再現した2 crashにだけ対応する実通信なしの2testを追加。
  通常USGS正規化、plot、query parameter、空結果挙動は変更していない。
- 日英で同期した文書: testing guide/test notes、ロードマップ、TODO、project status、
  公開監査、Home更新履歴、作業ログ。
- 確認:
  - 焦点test: `2 passed, 12 deselected in 0.50s`。
  - 最終全suite: `58 passed in 1.52s`、skip 0。
  - 構文解析: 現行・testのPython 13ファイルに合格。
  - Streamlit `AppTest`: Home・現行pageの6ファイルすべて例外0件で起動。
  - Markdown: 51ファイル、local link 92件、欠損0件。
  - 公開用cloneはcleanを維持: `## main...origin/main`。
- 範囲: アプリversionと依存は変更せず、公開用cloneとEnvGeo-Seawaterも変更していない。
- 次の1項目: 現行JMA/NIED upload失敗経路を監査し、再現できた読込み不能caseのみ変更する。

## 2026-10-08 — validationを必要最小限・現状維持のsafeguardへ絞り込み

- ユーザー方針: Earthquakeの現状機能を維持し、本当に必要な機能だけを追加する。
  本アプリは主に公式USGS catalog dataを取得・表示するため、独立した科学的
  quality等級subsystemは過剰と判断。
- この決定は、直下の作業記録にある広範な段階validation実装計画を更新する。
  直下の記録は時系列履歴として残すが、現在の実装要件ではない。
- 現在の方針:
  - USGS catalog値をsource dataとして信頼し、Earthquake/Seawater独自のquality等級を付けない。
  - 実際に確認した接続、timeout、HTTP、不正response、空結果、plot crash経路に対する
    小さなsafeguardだけを追加する。
  - JMA/NIED uploadのcheckは、表示済み形式、必須列、数値化、読込みerrorに限定する。
  - 重複ID管理、issue code/severity体系、validation dashboard、issue export拡張、
    timezone挙動変更は、具体的な不具合または後日の要件がない限り後回しにする。
  - validation挙動を追加する前に焦点を絞った失敗caseを示し、通常のUSGS表示結果を変えない。
- 日英で更新した継続記録: project作業指示、検証方針、ロードマップ、project status、
  TODO、README、docs index、export/注意マニュアル、公開監査、release checklist、Home更新履歴。
- runtime codeと依存は変更していない。Homeの変更は更新履歴textのみ。
- 方針修正後の確認:
  - `pytest -q`: `56 passed in 1.68s`。
  - 構文解析: 現行・testのPython 13ファイルに合格。
  - Streamlit `AppTest`: Home・現行pageの6ファイルすべて例外0件で起動。
  - Markdown: 51ファイル、local link 92件、欠損0件。
  - 公開用cloneはcleanを維持: `## main...origin/main`。
- 範囲: 公開用cloneとEnvGeo-Seawaterは変更していない。
- 次の1項目: 現行USGS失敗経路を監査し、焦点を絞ったtestで未処理crashを
  確認した場合のみcodeを追加する。

## 2026-10-08 — 地震カタログ検証contractの定義

- 目的: 正規化、filter、図、exportの挙動を変える前に検証基準を定義し、
  Phase 2の最初のロードマップ項目を完了する。
- source確認:
  - 現行のUSGS GeoJSON正規化と、日英Advancedのupload正規化を確認。
  - USGS GeoJSON / FDSN仕様、気象庁震源レコードフォーマット、NIED Hi-net
    data利用案内を公式根拠に使用。
- `docs/earthquake_validation_Japanese.md`と英語版に記録した決定:
  - Seawater式の単一quality等級ではなく、`Error`、`Warning`、`Information`の
    issueを用いる。
  - source rowを保持し、不正値・重複を報告する。黙って書換え、重複除去、
    削除を行わない。
  - 空間利用の経度・緯度は有限数で-180..180 / -90..90、深さ依存の利用は
    USGS query contractの-100..1000 kmとする。負の深さは自動的に不正としない。
  - magnitudeに任意の非負制約を設けず、負のcatalog magnitudeも許容する。
  - USGS epoch millisecondはUTCと解釈する。timezoneのない汎用upload値は
    UTCと黙認せず`timezone_unknown`と報告する。
  - USGS Event IDは空でなく、1 response内でuniqueとするが、重複rowも保持・報告する。
    汎用uploadに架空のsource IDを作らない。
  - USGS `status`と`alert`はsource metadataとして保持し、validityやSeawater
    quality flagに変換しない。
  - 安定issue codeと、2D、3D/断面、時間、magnitude、catalog比較ごとの使用可否を定義。
- 現行実装との差: 今回は目標contractの定義のみ。現行upload正規化はまだ
  timezoneのない値を`utc=True`で解釈し、座標/深さ欠損rowを除外し、
  範囲外値・重複IDの全issueを報告しない。これらは文書のみの今回工程では変更しなかった。
- 同期した文書: 日英README、docs index、export/注意マニュアル、ロードマップ、
  TODO、公開監査、release checklist、project status、Home更新履歴。
- 確認:
  - `pytest -q`: `56 passed in 1.40s`。
  - 構文解析: 現行・testのPython 13ファイルすべてに合格。
  - Streamlit `AppTest`: Home・現行pageの6ファイルすべて例外0件で起動。
  - Markdown link: 51 Markdownファイル、local link 92件、欠損0件。
  - 公開用cloneはcleanを維持: `## main...origin/main`。
- 範囲: runtime挙動・依存は変更せず、公開用cloneとEnvGeo-Seawaterは変更していない。
- 次の1項目: 緯度・経度、震源時刻、深さ、magnitude、Event IDの検証を実装・testする。

## 2026-10-08 — 公開品質監査と継続作業記録の整備

- 目的: EnvGeo-Earthquakeの単独公開とZenodo DOI取得への残件を、
  `envgeo_seawater_v130` を変更せず読取り専用で比較・整理する。
- 監査範囲: コード、データ読込、共通UI、アップロード、フィルタ、
  品質フラグ、出典表示、テスト、CI、配布設定。
- 主な判定:
  - Earthquakeはまだ「公開候補」で、CI、citation metadata、単独化、
    Earthquake固有テスト、海岸線出典の整備後にリリースする。
  - 当面はCoreを抽出せず、Earthquake内の実装とアセットを維持する。
  - Seawaterの品質フラグ、filter、uploadを、地震カタログへそのまま共通化しない。
- 確認:
  - 日英Home / Simple / Advanced、utility、現行testを含む11 Pythonファイルは
    `ast.parse` で構文解析に成功した。
  - 海岸線50m / 110m CSVはSeawaterとEarthquakeでそれぞれSHA-256が一致した。
  - 監査に使用したPython環境にpytestがなく、全テスト実行は未確認。
    既存`.pytest_cache` は古い記録を含むため合格証拠に使用しない。
- 追加した継続記録:
  - ルート `PROJECT_STATUS.md`: 新しいchat/作業セッションの最初に読む現状。
  - `AGENTS.md`: 自動化エージェント用のプロジェクト境界と記録ルール。
  - `docs/development_workflow.md`: 作業ログ、マニュアル、TODO、更新履歴の更新手順。
  - `docs/publication_audit_2026-10-08.md`: 監査詳細、Core分類、ブロッカー、
    公開・Zenodo最小計画。
  - 上記の引継ぎ、監査、維持管理文書を日本語版と英語版の別ファイルに分け、相互リンクを追加した。
- 変更しなかった範囲: `envgeo_seawater_v130`、Earthquakeの実行コード、依存関係、
  データ、バージョン表示。
- 次の一手: 不要なSeawater dataset読込とskipテストをEarthquake側だけで除去し、
  USGS GeoJSON contractテストで置き換える。

## 2026-10-08 — 公開ロードマップ保存と公開対象の確定

- 全作業を1項目ずつ進める日英ロードマップを
  `docs/publication_roadmap*.md`として保存した。
- 第1項目「Earthquakeの公開対象ファイルを確定する」を完了し、
  `docs/public_release_scope*.md`に日英で記録した。
- 現行コード、海岸線、test、日英文書、作業ログを公開対象とした。
- `old/`、`data/`、`__ToDo__/`、`__logo__/`、`images/`、cache・OS生成物は
  公開対象外とした。作業フォルダからは削除していない。
- 作業ログを公開・引継ぎに残すため、`.gitignore`の
  `docs/work_log.md`除外指定を解消した。
- EnvGeo-Seawaterのファイル、Earthquakeの実行コード・データ・依存関係は
  変更していない。
- 次の1項目: 公開用GitHub repositoryまたはローカルGit cloneの場所を確定する。

## 2026-10-08 — 公開Git cloneの確定と読取り専用監査

- 公開用Git cloneとGitHub remoteを確定した。マシン固有パスは、
  `.gitignore`対象の日英`LOCAL_WORKSPACE`ファイルに保存した。
- 運用方針: ユーザーの明示的な指示があるまでcloneを読取り専用とし、
  commitとpushはユーザーがGitHub Desktopで行う。
- `git status --short --branch`、`git remote -v`、`git log -1`、`git branch -vv`、
  `git tag`、`git ls-files`で読取り専用確認を行った。
- cloneはcleanな`main`で、ローカルに記録された`origin/main`と同じ
  `86b2d54`。最終commit日は2026-09-23、tagは`v0.2.3.1`と`v0.2.1`。
  ネットワークfetchは実行していない。
- 54の追跡ファイルのうち、開発フォルダと42がbyte一致、12が異なる。
  clone側のアプリ表示versionは`0.3.2`。
- cloneに書込み、copy、commit、pushは行っていない。Seawaterも変更していない。
- 公開ロードマップの第2項目を完了とした。次の1項目は、開発フォルダの
  アクティブutilityから旧Seawater dataset読込みを除去すること。

## 2026-10-08 — 旧Seawater dataset読込みの除去

- 目的: 公開ロードマップ第3項目として、Earthquakeで未使用の
  Seawater dataset読込みをアクティブutilityから除去する。
- 参照確認: `load_isotope_data()`は現行5ページからは呼び出されず、
  Seawater dataset不在時にskipする4旧testだけが参照していた。
- 変更: `envgeo_utils.py`から`load_isotope_data()`全体と、その内部の
  Seawater Excel読込み、結合、整形処理を除去した。後続section番号も更新した。
- 変更しなかった範囲: Earthquakeの海岸線、USGS、JMA/NIED、画面、依存関係、
  4件のskip test、公開用Git clone、EnvGeo-Seawater。
- 確認:
  - 変更前 `/opt/anaconda3/bin/pytest -q`: `45 passed, 4 skipped`。
  - 変更後 `/opt/anaconda3/bin/pytest -q`: `45 passed, 4 skipped`。
  - `ast.parse`: 現行・testのPython 11ファイルはすべて成功。
  - `rg`: アクティブ`envgeo_utils.py`に`def load_isotope_data`、Seawater dataset path、
    `pd.read_excel(file_...)`は残っていない。
- 判断: 4件の旧skip testは専用の後続項目でEarthquake contract testへ置換するため、
  今回は変更しない。
- 次の1項目: 未公表dataset名・参照のrepository全体監査と残存参照の除去。

## 2026-10-08 — Seawater式の日英section comment方針

- ユーザー方針: コードの主要sectionごとに英語・日本語を併記し、
  EnvGeo-Seawaterの読みやすいコメント形式を踏襲する。
- Seawaterの`envgeo_utils.py`を読取り専用で確認し、`English / 日本語`見出しを
  区切り線で囲む形式をEarthquakeの標準とした。
- 日英の`AGENTS`、`development_workflow`、`PROJECT_STATUS`に方針を保存した。
- `envgeo_utils.py`のsection 0〜9とPandas設定見出しを日英併記に整え、
  必要な目的説明も日英で対応させた。処理ロジックは変更していない。
- 確認:
  - `ast.parse`: 現行・testのPython 11ファイルはすべて成功。
  - `/opt/anaconda3/bin/pytest -q`: `45 passed, 4 skipped`。
- 公開ロードマップの次項目へは進んでいない。公開用Git cloneと
  EnvGeo-Seawaterのファイルは変更していない。

## 2026-10-08 — 未公表dataset参照の監査と除去

- 目的: 公開ロードマップ第4項目として、開発側の現行コード、test、
  公開対象文書に旧未公表dataset名やpathが残っていないか確認する。
- 監査範囲: `old/`、`data/`、cache、ローカル専用メモを除く開発フォルダの
  公開対象。公開用Git cloneは読取り専用で別途確認した。
- 結果: 開発側の現行コードに参照は0件。前項目でloaderと一緒に除去済みだった。
  引継ぎ文書に残っていた具体的な旧ファイル名1件を一般的な記述へ変更した。
- 「機密・非公開データをreleaseに含めない」という安全方針の文言は、実データ参照では
  ないため維持した。
- 公開用cloneの旧utilityには、旧loaderと具体的な未公表参照がまだ残る。
  ユーザー指示がないため、copy・編集・commit・pushは行っていない。
- 確認:
  - 残存検索: 開発側の現行・公開対象で0件。
  - `ast.parse`: 現行・testのPython 11ファイルはすべて成功。
  - `/opt/anaconda3/bin/pytest -q`: `45 passed, 4 skipped`。
  - Markdown local link: 82件中broken 0件。
- 日英のロードマップ、TODO、`PROJECT_STATUS`、監査文書を、開発側で解消済み、
  公開用cloneは反映待ちという状態に更新した。
- 次の1項目: Seawater依存の4件のskip testをEarthquake contract testへ置換する。

## 2026-10-08 — Seawater依存skip testのEarthquake contract test化

- 目的: 公開ロードマップ第5項目として、Seawater datasetがないとskipする
  4テストを、Earthquake単独で常に実行できるcontract testへ置換する。
- 変更: `test/test_envgeo_utils.py`から旧Seawater path、skip helper、isotope loaderの
  4テストを除去した。
- 追加した4契約:
  1. 欠損featureを含め、USGS GeoJSONの1 featureを1行として保持する。
  2. pageとCSV出力が使う列名・列順を固定する。
  3. 数値文字列を数値化し、不正値を欠損にする。
  4. millisecond時刻からUTC、日付、年月日時を一貫して生成する。
- 日英コメントとsection見出しでtestの目的を記述し、`test/README_Japanese.md`を
  追加した。日英のtesting guideとtest READMEを現行契約に更新した。
- 確認:
  - 変更前の全test: `45 passed, 4 skipped`。
  - `/opt/anaconda3/bin/pytest -q test/test_envgeo_utils.py`: `12 passed`。
  - 変更後 `/opt/anaconda3/bin/pytest -q`: `49 passed, 0 skipped`。
  - `ast.parse`: 現行・testのPython 11ファイルはすべて成功。
  - 旧loader test、skip helper、Seawater dataset pathのtest内参照は0件。
- 変更しなかった範囲: 実USGS通信、アプリ実装、公開用Git clone、EnvGeo-Seawater。
- 次の1項目: 開発フォルダから削除せずに、不要なSeawaterサンプルと
  開発archiveを公開対象から除外する。

## 2026-10-08 — 不要サンプルと開発archiveの公開除外

- 目的: 公開ロードマップ第6項目として、Earthquake実行に不要な
  Seawaterサンプル、開発履歴、メモ、未使用素材を公開対象から確実に除外する。
- 確認対象: `old/`、`data/`、`__ToDo__/`、`__logo__/`、`images/`、
  `.devcontainer/`。すべて開発フォルダ内に残し、削除していない。
- 参照監査で、未使用の旧sidebar関数に存在しない`data/`内画像への参照1件を
  発見した。そのSeawater固有の画像表示blockを`envgeo_utils.py`から除去した。
- `.gitignore`に6 directoryのroot固定規則を追加した。`.DS_Store`、cache、
  bytecode、build、log、秘密情報は既存規則で引き続き除外する。
- 確認:
  - root固定ignore規則: 6件すべて存在。
  - 除外対象directory: 6件すべてローカルに維持。
  - 現行・test Python 11ファイルの除外directory文字列参照: 0件。
  - `ast.parse`: Python 11ファイルはすべて成功。
  - `/opt/anaconda3/bin/pytest -q`: `49 passed, 0 skipped`。
  - 公開用cloneで除外directoryから追跡中のファイル: 0件。
- 作業フォルダはGit repositoryでないため、その場での`git check-ignore`は
  `fatal: not a git repository`で実行不可。代わりに規則の存在と公開cloneの追跡対象を検査した。
- 変更しなかった範囲: 公開用Git clone、EnvGeo-Seawater、アプリの表示・地震処理。
- 次の1項目: アプリversion metadataを1か所へ集約する。

## 2026-10-08 — 日英Homeへの公開ロゴ追加

- 目的: EnvGeo-Earthquakeの公開用brandingを、日英のHomeで共通表示する。
- `__logo__/`内のPNG 4点を画像とファイル情報で比較し、当初は`logo_01.png`を採用した。
  同directoryの`ChatGPT Image 2026年5月6日 18_59_26 (3).png`とはbyte単位で同一であることも確認した。
- 採用元は1254×1254 px、RGB PNG、SHA-256
  `d668ed0cb0a720c661732231e7c9173d99611ccd0b49acbcf4b4d9a7ab2166b9`。
- 公開対象の1点だけを`assets/branding/envgeo-earthquake-logo.png`へ複製し、
  複製後のSHA-256一致を確認した。`__logo__/`全体は引き続き公開対象外。
- `home.py`と`pages/00_home_(Japanese).py`に、source fileを基準にした
  カレントdirectory非依存のpath解決と、中央揃え・幅320 pxの表示を追加した。
  変更sectionにはSeawater方針の`English / 日本語`目的commentを追加した。
- 日英のbranding README、ルートREADME、公開対象文書、Home更新履歴、
  release checklist、TODO、PROJECT_STATUSを同期した。
- 公開前の残件: ロゴの作成者・権利とAI支援開発の最終開示文を確定し、
  branding README、`NOTICE.md`、release notesで同期する。
- 確認:
  - `ast.parse`: 現行・test Python 11ファイルはすべて成功。
  - `/opt/anaconda3/bin/pytest -q`: `49 passed, 0 skipped`。
  - Streamlit AppTest: 日英Homeとも例外0件、画像1件。
  - ローカルbrowser表示: 日英Homeともロゴの中央配置とタイトルとの間隔を目視確認。
  - 別途のCLI起動試行は実行環境のport bind権限で`PermissionError`となったため、
    起動成功の証拠には使用していない。
- 変更しなかった範囲: 公開用Git clone、EnvGeo-Seawater、地震データ処理。
- ロードマップの次の1項目は変更せず、アプリversion metadataの1か所への集約。

### 同日訂正 — 不正確な地球図案の撤回

- ユーザー確認により、`logo_01.png`は大陸配置と島・半島の形が不正確であると判断し、
  公開ロゴとしての採用を撤回した。
- 他の地球図候補も図案化された地形であり、地理的正確性を保証できないため不採用とした。
- 大陸・島・半島の輪郭を使わず、地表、山地、都市、地下構造、地震波形、震源を表す
  `ChatGPT Image 2026年5月6日 18_59_25 (2).png`へ差し替えた。
- 公開copyのSHA-256は
  `aa46cc8f90b100ee6c2ad078d43d7ddf117223ccf4cdcd98d5f0f45d28abd064`で、選定元と一致。
- Homeのpathと表示codeは変更せず、画像assetのみを差し替えた。公開用Git cloneと
  EnvGeo-Seawaterは変更していない。
- 差し替え後の確認: 日英HomeのAppTestはそれぞれ例外0件・画像1件、
  pytestは`49 passed, 0 skipped`、Markdownのローカルlink 86件は破損0件。

### 同日最終訂正 — Home上部ロゴの撤去

- ユーザーとのデザイン再検討により、Home最上部の大きな画像はページ全体のバランスに
  合わないと判断し、日英Homeからロゴ表示を撤去した。
- `LOGO_PATH`、中央配置用columns、`st.image()`を日英Homeから削除し、両ページは
  再びアプリ名から開始する構成とした。
- 公開copyの`assets/branding/envgeo-earthquake-logo.png`と日英assetメモを削除し、
  現在の公開対象からロゴassetを外した。
- 元候補は開発専用・公開対象外の`__logo__/`に残っているため、将来、小型iconや
  背景として再検討する場合は復元可能。
- README、公開対象、release checklist、TODO、PROJECT_STATUS、Home更新履歴の
  日英版を現在のロゴなし方針へ同期した。
- 撤去後の確認: 日英HomeのAppTestはそれぞれ例外0件・画像0件、
  Python 11ファイルの構文解析に成功、pytestは`49 passed, 0 skipped`、
  Markdownのローカルlink 84件は破損0件。
- 公開用Git cloneとEnvGeo-Seawaterは変更していない。

## 2026-10-08 — 実行時version metadataの1か所への集約

- 目的: 公開ロードマップPhase 1の次項目として、Home、utility、4つの現行ページに
  重複していた`0.3.2`の実行時定義を1か所へ集約する。
- 唯一の定義元を`envgeo_utils.APP_VERSION = "0.3.2"`と
  `APP_VERSION_DATE = "2026-09-22"`に固定し、後方互換用の`version` aliasは
  `APP_VERSION`を参照する構成を維持した。
- `home.py`、日本語Home、日英Simple / Advancedの合計6画面からローカルな
  `APP_VERSION` / `version`文字列定義を削除し、表示時に
  `envgeo_utils.APP_VERSION`を直接参照するよう変更した。表示値は`0.3.2`のままで変更なし。
- `test/test_basic.py`に、共通version、ISO形式の日付、6画面の共通参照、
  ローカル文字列再定義の不在を確認するcontract testを追加した。
- README、Home更新履歴、test README、testing guide、公開監査、ロードマップ、
  release checklist、TODO、PROJECT_STATUSの日英版を同期した。
- 確認:
  - `/opt/anaconda3/bin/pytest -q test/test_basic.py`: `3 passed, 0 skipped, 0 failed`。
  - `/opt/anaconda3/bin/pytest -q`: `50 passed, 0 skipped, 0 failed`。
  - `ast.parse`: 現行・test Python 11ファイルはすべて成功。
  - 現行Pythonの文字列version定義検索: `envgeo_utils.py`の1件のみ。
  - Streamlit AppTest: 日英Homeと4つの可視化ページの合計6画面で例外0件。
  - Markdownローカルlink: 49ファイルの84件を確認し、破損0件。
  - 公開用cloneの`git status --short --branch`: `## main...origin/main`のみで変更なし。
- 変更しなかった範囲: 表示version値、地震データ処理、公開用Git clone、
  EnvGeo-Seawater、将来のEnvGeo Core依存。
- 判断: ページ専用の新moduleは増やさず、全画面がすでにimportするEarthquake内の
  `envgeo_utils`を単一定義元とすることで、単独配布性を維持する。
- 次の1項目: カレントdirectoryに依存しないasset読込みを確認する。

## 2026-10-08 — current directoryに依存しないasset読込みの確認

- 目的: 公開ロードマップPhase 1の次項目として、Earthquakeの同梱assetが
  processのcurrent directoryに依存せず、単独配布時に安定して読み込めることを確認する。
- 現行・test Pythonを監査し、project内ローカル読込みは、50m / 110m海岸線CSV、
  英語Home内README、日本語Home内READMEの3系統であることを確認した。
  AdvancedページのCSV / Excelはユーザーがuploadするfile objectであり、同梱assetではない。
- `envgeo_utils.py`に`PROJECT_ROOT` / `COASTLINE_DIR`を定義し、同moduleの
  `__file__`から海岸線pathを解決する意図を`English / 日本語`で明記した。
- 英語Homeは`APP_ROOT / "README.md"`、日本語Homeは
  `APP_ROOT / "README_Japanese.md"`を使用する構成に統一した。日本語Homeの
  Markdown内ローカル画像基準も`pages/`ではなくproject rootへ修正した。
- `test/test_asset_paths.py`を追加し、pytestの一時directoryへCWDを変更した状態で、
  両解像度の海岸線をcache clear後に実読込みし、日英HomeがREADME本文を
  描画することを確認する3 testを追加した。
- 最初の別CWD AppTest試行は、CWD変更によりtest processの空文字`sys.path`が
  project rootを指さなくなり、`ModuleNotFoundError: envgeo_utils`で2ページが失敗した。
  これはasset読込み前のtest harnessのimport条件であるため成功証拠に使わず、
  project rootを明示的に`sys.path`に追加してassetだけを別CWDで検証する永続testにした。
- 確認:
  - `/opt/anaconda3/bin/pytest -q test/test_asset_paths.py`: `3 passed, 0 skipped, 0 failed`。
  - `/opt/anaconda3/bin/pytest -q`: `53 passed, 0 skipped, 0 failed`。
  - `ast.parse`: 現行・test Python 12ファイルはすべて成功。
  - 現行・test Pythonの絶対ローカルpath (`/Users/`, `~/`) 検索: 0件。
  - Streamlit AppTest: 通常CWDの日英Homeと4つの可視化ページで例外0件。
  - Markdownローカルlink: 49ファイルの84件を確認し、破損0件。
  - 公開用cloneの`git status --short --branch`: `## main...origin/main`のみで変更なし。
- 変更しなかった範囲: 地震処理、CSV内容、公開用Git clone、EnvGeo-Seawater、
  将来のEnvGeo Core依存。
- 次の1項目: 表示上の`.xls`サポートを外すか、必要依存を追加してtestする。

## 2026-10-08 — 旧`.xls`upload表示の除去と`.xlsx`契約の固定

- 目的: 公開ロードマップPhase 1の最後の項目として、画面が対応を表示する形式と
  実行時依存を一致させる。
- 日英Advancedの`read_uploaded_catalog()`でExcel分岐を`.xlsx`のみに限定し、
  `st.file_uploader()`の受付形式を`csv`, `tsv`, `txt`, `xlsx`に変更した。
- `.xlsx`用の`openpyxl==3.1.5`は維持し、旧binary `.xls`用の`xlrd`は追加していない。
  旧`.xls`はアップロード前に`.xlsx`またはtext形式へ保存し直すよう日英manualに明記した。
- `test/test_upload_formats.py`を追加し、日英画面の受付形式、`.xls`分岐の不在、
  `openpyxl`宣言、`xlrd`非宣言、memory内XLSX workbookの書込み・読込みを固定した。
- 最初の対象testは`2 passed, 1 failed`。XLSX往復で`135.0`が値を保ったまま
  `float64`から`int64`へ推論され、dtype比較だけが失敗した。非整数の座標・深さを
  fixtureに使い、Excel engine契約と無関係なdtype推論に左右されない形へ修正した。
- 日英README、JMA/NIED manual、Home更新履歴、test README、testing guide、
  公開監査、ロードマップ、release checklist、TODO、PROJECT_STATUSを同期した。
- 確認:
  - 修正後 `/opt/anaconda3/bin/pytest -q test/test_upload_formats.py`: `3 passed, 0 skipped, 0 failed`。
  - `/opt/anaconda3/bin/pytest -q`: `56 passed, 0 skipped, 0 failed`。
  - `ast.parse`: 現行・test Python 13ファイルはすべて成功。
  - Streamlit AppTest: 日英Home / Simple / Advancedの6画面で例外0件。
  - 現行pagesの`.xls`受付・分岐検索: 0件。
  - Markdownローカルlink: 49ファイルの84件を確認し、破損0件。
  - 公開用cloneの`git status --short --branch`: `## main...origin/main`のみで変更なし。
- 判断: JMA/NIED比較はCSV / textと現行`.xlsx`で公開要件を満たせるため、
  旧形式のためだけに依存を増やさず、受付形式を実装済み範囲へ絞る。
- 変更しなかった範囲: 現行`.xlsx`、CSV、TSV、TXT対応、必須列処理、
  地震処理、`requirements.txt`、公開用Git clone、EnvGeo-Seawater、EnvGeo Core依存。
- Phase 1の9項目はすべて開発フォルダで完了。次の1項目は、
  Earthquake固有の品質確認基準を定義する。

## 2026-09-22 — Version 0.3.2 consolidation

- Streamlit 1.63で従来のBaseWebセレクタだけではタブ装飾が効かなくなったため、現在のReact/ARIAタブDOM（`data-testid="stTab"`、`data-selected`）にも対応する共通CSSヘルパーを追加した。従来のDOMも残し、Streamlit 1.42との互換性を維持する。
- Home、Japanese Home、英語／日本語のAdvancedページなど、タブを持つすべての現行ページで共通ヘルパーを適用し、選択中タブの青系カード表示を復元した。
- アプリ共通版、Home、英語／日本語Simple・Advanced全ページを0.3.2（2026-09-22）へ更新した。過去版を保管する`old/`以下は変更しない。
- Streamlit 1.63環境でタブ修正後の対象回帰テストを実行し、`14 passed, 4 skipped`を確認した。
- 方針: 50m／110m海岸線CSVと共通ローダーは、将来的に`envgeo-core`（仮）へ集約する候補とする。両アプリでアセット同梱、パス解決、キャッシュ、解像度指定、テストを確認してから移行し、それまでは各アプリ内のCSVを維持する。

## 2026-09-20

- 地図タイルを `carto-positron`（APIキー必須化で警告表示）から `open-street-map` へ変更した。`apply_map_style()` 内の重複していた無条件適用行も同時に削除した。
- 経度・緯度・深さ・塩分のスライダー最小・最大値算出に `.dropna()` を追加し、ギャップ行（NaN）が含まれる場合のクラッシュを防いだ（4箇所）。
- page 55 の `menu_items["About"]` に URL を追加し、page 54 と統一した。
- `--- USGS Earthquake API ---` / `--- USGS 地震カタログ API ---` / `--- Visualization ---` / `--- 可視化設定 ---` の `---` 装飾を英語・日本語・Simple / Advanced の全4ページから削除した（2行表示になるため）。
- page 55・57 の断面図入力（始点/終点の経度・緯度 `st.number_input` ×4、半幅 `st.slider` ×1）で、`value=` とSession Stateの二重指定による Streamlit 1.63 警告を解消した。ウィジェット直前でSession Stateを初期化（未セット時のみ）し、`value=` 引数を削除する方式に統一した。
- page 54 の経度・緯度スライダー（`eq_lon_range_{region}`・`eq_lat_range_{region}`）で同様の Streamlit 1.63 警告を解消した。Region変更時に `apply_region_bounds_to_session()` がSession Stateを上書きするため、ウィジェット直前の初期化＋`value=` 削除を適用した。pages 55・56・57 は既に対応済みであることを確認。

- USGS API検索条件は、`Fetch / update` / `取得 / 更新`を押したときに手動反映されることを赤字で案内するようにした。
- 可視化設定は変更が自動的に反映されることを青字で案内し、EnvGeo-Seawaterと操作説明の意味づけを統一した。
- 英語版・日本語版のSimple / Advanced、計4ページへ同じ案内構成を適用した。
- 英語版・日本語版のAdvanced断面図で、断面始終点と半幅の設定を、断面Plotly図と位置確認マップの間へ移動した。
- 英語版・日本語版のAdvancedで、カラーバースケールの初期値をSession Stateとスライダーの両方に指定していた箇所を修正し、Streamlit 1.63の重複指定警告を解消した。
- 英語版・日本語版の Advanced（page 55・57）で、フォーム上部にも `Fetch / update` / `取得 / 更新` ボタンを追加した（seawater パターンに準拠）。上部ボタンをキャプション直下、下部ボタンをフォーム末尾に配置し、ラベルを上 `Fetch / update` / `取得 / 更新`、下 `Fetch / update!` / `取得 / 更新！` として区別した。両ボタンとも `use_container_width=True` を指定した。
- 英語版・日本語版の Simple（page 54・56）にも同じ上下ボタン構成を適用した。page 54 にはキャプションが未設置だったため、ヘッダー直下に追加した。全4ページで統一。

## 2026-09-18

- Streamlit 1.63 / Python 3.12 / Plotly 5.24.1 環境で互換性確認を開始した。
- Streamlit 1.42では `use_container_width=True`、1.63では `width="stretch"` を自動選択する共通互換ヘルパーを追加した。
- Pandasのcopy-on-write optionは、設定が必要なPandas 3未満でのみ有効化し、Pandas 3の非推奨警告を抑えた。
- 現行の英語・日本語AdvancedページにあるPlotly図へ互換ヘルパーを適用した。履歴保存用の `old/` は変更していない。
- Streamlit 1.42・1.63の両環境で `9 passed, 4 skipped` を確認した。
- Streamlit 1.63環境でHomeと英語・日本語のSimple / Advanced全ページが例外なしで初期表示されることを確認した。

## 2026-09-19

- Python 3.10〜3.12、Streamlit 1.42〜1.63の互換性改善サイクルとして、開発バージョンを0.3.1へ更新した。
- `requirements.txt`のStreamlit指定を`>=1.42.0,<=1.63.0`へ更新した。新規デプロイでは1.63を選択し、既存の1.42環境は回帰確認用として維持する。
- Region変更時の経度・緯度スライダーは、セッション状態を先に初期化し、ウィジェット側の`value`指定を外した。Streamlit 1.63で表示される既定値とSession Stateの二重指定警告を、日英Simple / Advancedの4ページで解消した。
- 読み込み中のSimple / Advanced切り替えでAPI検索フォームの状態が衝突しないよう、日英4ページの検索用ウィジェットキーをページ別に分離した。経緯度の一時状態が無効な場合は、選択中の地域プリセット範囲へ自動復旧するようにした。
- 現時点ではPlotly 5.24を検証基準として維持する。次の段階ではPlotly 5.24上でMapbox系コードをMapLibre APIへ移行し、同じコードをPlotly 6.7、7.1で検証する。
- Python 3.10 / Streamlit 1.63 / Plotly 7の交差環境を確認してから、対応範囲内の全組み合わせを検証済みと表記する。

## 2026-09-16

- README と Home の説明を、EnvGeo-Seawater の研究アプリとしての雰囲気に合わせて整理した。
- EnvGeo-Seawater との関係、将来の EnvGeo 共通コア候補、Earthquake 側に残すべき固有処理を README / README_Japanese に明記した。
- ページ名と説明を現行構成に合わせ、英語版・日本語版の Simple / Advanced ページ名を README に反映した。
- 日本語表現を整理し、`地理分布図` を `2D 震源マップ`、`簡易版` を `基本版`、`発展版` を `詳細版`、`簡易地震可視化アプリ` を `地震カタログ探索アプリ` へ修正した。
- Region 選択UIで、デフォルトが日本周辺の場合にチェックボックスも日本周辺へ同期するようにした。
- hotspot 選択時に selectbox と重複して表示されていた `Selected hotspot` / `選択中の地震多発域` caption を削除した。
- `test/test_envgeo_utils.py` に USGS GeoJSON 正規化テストを追加し、Earthquake に同梱されていない Seawater データセット確認は skip するようにした。
- 作業フォルダで AST 構文確認と `pytest -q` を実行し、`9 passed, 4 skipped` を確認した。
- ローカルGitクローンへは、作業フォルダで確認した必要ファイルだけをコピーする運用とする。
- `.gitignore` を拡張し、`requirements.txt` を実行用依存関係として整理、`requirements-dev.txt` をテスト用に追加した。
- `NOTICE.md` を追加し、MIT License はアプリコードに適用し、外部データ・地図タイル・カタログサービスは各提供元条件に従うことを明確化した。
