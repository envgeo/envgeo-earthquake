# テスト説明

この文書では、EnvGeo-Earthquake の現在の pytest 群が何を確認しているか、また今後どこを拡充すべきかを説明します。

## 実行方法

作業フォルダ `earthquake_map_v030` で実行します。

初回、または依存関係を更新した後は、開発用 requirements をインストールします。

```bash
pip install -r requirements-dev.txt
```

```bash
pytest -q
```

`.pyc` を作らない構文確認を行う場合は、次を使います。

```bash
python -c "import ast, pathlib; files=[pathlib.Path('home.py'), pathlib.Path('envgeo_utils.py'), *pathlib.Path('pages').glob('*.py'), *pathlib.Path('test').glob('*.py')]; [ast.parse(p.read_text(encoding='utf-8'), filename=str(p)) for p in files]; print(f'parsed {len(files)} files')"
```

## 現在のテスト

### `test/test_basic.py`

- `envgeo_utils` を import できること。
- `envgeo_utils.version` が存在すること。

### `test/test_envgeo_utils.py`

現在は、主に次を確認しています。

- 継承元 Seawater データセットが存在する環境では、旧来の isotope data loader が動くこと。
- Earthquake 単体配布で Seawater データセットが同梱されていない場合は、その確認を skip すること。
- `insert_gap_rows()` が観測グループの切れ目で空白行を挿入すること。
- 深度用・通常用のカラースケールが返ること。
- 海岸線座標が経度・緯度の同じ長さのリストとして読み込めること。
- USGS GeoJSON FeatureCollection が、`Longitude_degE`、`Latitude_degN`、`Depth_km`、`Depth_m`、`Magnitude` などの列を持つ DataFrame に正規化されること。
- 空の USGS GeoJSON payload でも、期待される列を持つ空 DataFrame が返ること。

## 現在の限界

まだ次は十分に自動化できていません。

- Streamlit UI のブラウザ操作。
- USGS API への実ネットワークアクセスを含む end-to-end テスト。
- 2D/3D/4D 図の見た目の自動比較。
- JMA/NIED アップロード表の多様な列名・形式への対応確認。
- Region / hotspot / cross-section UI のブラウザ上の状態確認。

そのため、重要なUI変更後は pytest に加えて手動で Streamlit 画面確認を行います。

## 今後追加したいテスト

- Region 選択ロジックを UI から切り離した純粋関数としてテストする。
- JMA/NIED 比較表の列名正規化テストを増やす。
- プレート境界フォールバックのデータ構造をテストする。
- 経度ラップ、日付変更線またぎ、ローカル km 座標変換のテストを増やす。
- Seawater と共有できる候補関数は、将来 `envgeo4d` / shared core 側のテストへ移す。
