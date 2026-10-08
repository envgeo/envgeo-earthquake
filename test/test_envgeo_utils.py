import io
import json
import sys
from datetime import datetime
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, urlparse

import pandas as pd
import pytest
from pandas.api.types import is_numeric_dtype

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import envgeo_utils


USGS_EXPECTED_COLUMNS = [
    "EventID",
    "DateTime_UTC",
    "Time_UTC",
    "Updated_UTC",
    "Longitude_degE",
    "Latitude_degN",
    "Depth_km",
    "Depth_m",
    "Magnitude",
    "MagnitudeType",
    "Place",
    "Tsunami",
    "Alert",
    "Status",
    "URL",
    "DetailURL",
    "Dataset",
    "reference",
    "Year",
    "Month",
    "Day",
    "Hour",
    "Date",
    "lat",
    "lon",
]

ACTIVE_VISUALIZER_PAGES = [
    ROOT / "pages" / "54_🇺🇸_4D_Earthquake_Simple.py",
    ROOT / "pages" / "55_🇺🇸_4D_Earthquake_Advanced.py",
    ROOT / "pages" / "56_🇯🇵_4D_Earthquake_シンプル版.py",
    ROOT / "pages" / "57_🇯🇵_4D_Earthquake_詳細版.py",
]


# -----------------------------------------------------------------------------
# USGS GeoJSON contract tests / USGS GeoJSON契約テスト
# -----------------------------------------------------------------------------


def test_build_usgs_query_url_includes_required_and_optional_parameters():
    """Keep the complete API parameter mapping stable and inspectable."""
    query_url = envgeo_utils.build_usgs_earthquake_query_url(
        datetime(2026, 1, 2, 3, 4, 5),
        datetime(2026, 1, 3, 6, 7, 8),
        minmagnitude=1.2,
        maxmagnitude=8.4,
        mindepth=-5.0,
        maxdepth=700.0,
        minlatitude=20.0,
        maxlatitude=50.0,
        minlongitude=120.0,
        maxlongitude=155.0,
        limit=3210,
        orderby="magnitude",
    )

    parsed = urlparse(query_url)
    params = parse_qs(parsed.query)

    assert f"{parsed.scheme}://{parsed.netloc}{parsed.path}" == (
        envgeo_utils.USGS_EARTHQUAKE_QUERY_URL
    )
    assert params == {
        "format": ["geojson"],
        "eventtype": ["earthquake"],
        "starttime": ["2026-01-02T03:04:05"],
        "endtime": ["2026-01-03T06:07:08"],
        "orderby": ["magnitude"],
        "limit": ["3210"],
        "minmagnitude": ["1.2"],
        "maxmagnitude": ["8.4"],
        "mindepth": ["-5.0"],
        "maxdepth": ["700.0"],
        "minlatitude": ["20.0"],
        "maxlatitude": ["50.0"],
        "minlongitude": ["120.0"],
        "maxlongitude": ["155.0"],
    }


def test_build_usgs_query_url_omits_unset_optional_parameters():
    query_url = envgeo_utils.build_usgs_earthquake_query_url(
        "2026-04-01",
        "2026-04-02",
        minmagnitude=None,
        maxmagnitude=float("nan"),
    )
    params = parse_qs(urlparse(query_url).query)

    assert "minmagnitude" not in params
    assert "maxmagnitude" not in params
    assert params["format"] == ["geojson"]
    assert params["eventtype"] == ["earthquake"]
    assert params["limit"] == ["2000"]
    assert params["orderby"] == ["time"]


@pytest.mark.parametrize(
    ("result_count", "requested_limit", "expected"),
    [(1999, 2000, False), (2000, 2000, True), (2001, 2000, True)],
)
def test_usgs_result_limit_reached_boundary(result_count, requested_limit, expected):
    assert envgeo_utils.usgs_result_limit_reached(result_count, requested_limit) is expected


def test_all_visualizer_pages_use_shared_result_limit_warning_condition():
    for path in ACTIVE_VISUALIZER_PAGES:
        source = path.read_text(encoding="utf-8")
        assert "envgeo_utils.usgs_result_limit_reached(" in source, path
        assert "st.caption(" in source, path
        assert "len(df_eq) >= query[\"limit\"]" not in source, path


# One GeoJSON feature must produce one row, including incomplete features.
# 欠損featureを含め、GeoJSONの1 featureを1行として保持する。
def test_usgs_contract_preserves_one_row_per_feature():
    payload = {
        "features": [
            {
                "id": "complete-event",
                "properties": {"time": 1_700_000_000_000, "mag": 4.2},
                "geometry": {"coordinates": [140.0, 35.0, 10.0]},
            },
            {"id": "incomplete-event", "properties": None, "geometry": None},
        ]
    }

    df = envgeo_utils.usgs_geojson_to_dataframe(payload)

    assert len(df) == 2
    assert df["EventID"].tolist() == ["complete-event", "incomplete-event"]
    assert pd.isna(df.loc[1, "Longitude_degE"])
    assert pd.isna(df.loc[1, "Magnitude"])


# Column names and order are a stable interface for pages and CSV exports.
# 列名と列順はpageとCSV出力が依存する安定interfaceとする。
def test_usgs_contract_has_stable_column_order():
    df = envgeo_utils.usgs_geojson_to_dataframe({"features": []})

    assert list(df.columns) == USGS_EXPECTED_COLUMNS


# Numeric strings are coerced to numbers and invalid values become missing.
# 数値文字列は数値化し、不正値は欠損値とする。
def test_usgs_contract_coerces_numeric_fields():
    payload = {
        "features": [
            {
                "id": "numeric-contract",
                "properties": {
                    "time": "1700000000000",
                    "updated": "1700000010000",
                    "mag": "not-a-number",
                    "tsunami": "1",
                },
                "geometry": {"coordinates": ["142.5", "38.1", "34.2"]},
            }
        ]
    }

    df = envgeo_utils.usgs_geojson_to_dataframe(payload)

    for column in (
        "Longitude_degE",
        "Latitude_degN",
        "Depth_km",
        "Depth_m",
        "Magnitude",
        "Tsunami",
    ):
        assert is_numeric_dtype(df[column]), f"{column} is not numeric"
    assert df.loc[0, "Depth_m"] == 34_200.0
    assert df.loc[0, "Tsunami"] == 1
    assert pd.isna(df.loc[0, "Magnitude"])


# Millisecond timestamps must produce UTC and calendar fields consistently.
# millisecond時刻からUTCと暦列を一貫して生成する。
def test_usgs_contract_derives_utc_calendar_fields():
    payload = {
        "features": [
            {
                "id": "time-contract",
                "properties": {
                    "time": 1_700_000_000_000,
                    "updated": 1_700_000_010_000,
                },
                "geometry": {"coordinates": [142.5, 38.1, 34.2]},
            }
        ]
    }

    row = envgeo_utils.usgs_geojson_to_dataframe(payload).iloc[0]

    assert row["DateTime_UTC"] == "2023-11-14 22:13:20 UTC"
    assert row["Date"] == "2023-11-14"
    assert (row["Year"], row["Month"], row["Day"], row["Hour"]) == (
        2023,
        11,
        14,
        22,
    )


# Malformed API JSON must become the RuntimeError handled by every page.
# 不正なAPI JSONは、全pageが処理するRuntimeErrorへ変換する。
def test_load_usgs_data_reports_invalid_json(monkeypatch):
    monkeypatch.setattr(
        envgeo_utils,
        "urlopen",
        lambda request, timeout: io.BytesIO(b"{not-json"),
    )
    envgeo_utils.load_usgs_earthquake_data.clear()

    with pytest.raises(RuntimeError, match="invalid JSON"):
        envgeo_utils.load_usgs_earthquake_data("2026-01-01", "2026-01-02")


# A non-list features member must produce a readable error instead of AttributeError.
# featuresがlistでないresponseは、AttributeErrorではなく読めるerrorにする。
def test_load_usgs_data_rejects_unexpected_geojson(monkeypatch):
    monkeypatch.setattr(
        envgeo_utils,
        "urlopen",
        lambda request, timeout: io.BytesIO(b'{"features": {"unexpected": true}}'),
    )
    envgeo_utils.load_usgs_earthquake_data.clear()

    with pytest.raises(RuntimeError, match="unexpected GeoJSON"):
        envgeo_utils.load_usgs_earthquake_data("2026-01-03", "2026-01-04")


# Successful, empty, and incomplete API payloads must pass through the same
# network-facing loader used by all four pages.
# 正常・空・欠損payloadを、4page共通のnetwork-facing loaderで確認する。
@pytest.mark.parametrize(
    ("payload", "expected_rows", "expected_event_id"),
    [
        (
            {
                "type": "FeatureCollection",
                "features": [
                    {
                        "id": "normal-loader-event",
                        "properties": {"time": 1_700_000_000_000, "mag": 4.8},
                        "geometry": {"coordinates": [139.7, 35.6, 12.3]},
                    }
                ],
            },
            1,
            "normal-loader-event",
        ),
        ({"type": "FeatureCollection", "features": []}, 0, None),
        (
            {
                "type": "FeatureCollection",
                "features": [
                    {"id": "incomplete-loader-event", "properties": None, "geometry": None}
                ],
            },
            1,
            "incomplete-loader-event",
        ),
    ],
)
def test_load_usgs_data_handles_valid_payload_variants(
    monkeypatch, payload, expected_rows, expected_event_id
):
    encoded = json.dumps(payload).encode("utf-8")
    monkeypatch.setattr(
        envgeo_utils,
        "urlopen",
        lambda request, timeout: io.BytesIO(encoded),
    )
    envgeo_utils.load_usgs_earthquake_data.clear()

    df = envgeo_utils.load_usgs_earthquake_data("2026-02-01", "2026-02-02")

    assert len(df) == expected_rows
    assert df.attrs["query_url"].startswith(envgeo_utils.USGS_EARTHQUAKE_QUERY_URL)
    if expected_event_id is not None:
        assert df.loc[0, "EventID"] == expected_event_id


# Transport failures must become the RuntimeError already handled by every page.
# 通信失敗は全pageが処理済みのRuntimeErrorへ変換する。
@pytest.mark.parametrize(
    ("transport_error", "message"),
    [
        (
            HTTPError(
                envgeo_utils.USGS_EARTHQUAKE_QUERY_URL,
                503,
                "Service Unavailable",
                hdrs=None,
                fp=None,
            ),
            r"USGS API error \(503\): Service Unavailable",
        ),
        (URLError("temporary DNS failure"), "USGS API connection error"),
        (TimeoutError("timed out"), "USGS API request timed out"),
    ],
)
def test_load_usgs_data_converts_transport_failures(
    monkeypatch, transport_error, message
):
    def raise_transport_error(request, timeout):
        raise transport_error

    monkeypatch.setattr(envgeo_utils, "urlopen", raise_transport_error)
    envgeo_utils.load_usgs_earthquake_data.clear()

    with pytest.raises(RuntimeError, match=message):
        envgeo_utils.load_usgs_earthquake_data("2026-03-01", "2026-03-02")


# Verifies that a blank separator row is inserted when observation groups change.
# 観測グループが切り替わる位置で、区切り用の空白行が挿入されることを確認する。
def test_insert_gap_rows_inserts_blank_row_between_groups():
    df = pd.DataFrame(
        {
            "Latitude_degN": [35.0, 35.0, 36.0],
            "Longitude_degE": [135.0, 135.0, 136.0],
            "Year": [2020, 2020, 2020],
            "Month": [1, 1, 2],
            "reference": ["A", "A", "B"],
            "d18O": [0.1, 0.2, 0.3],
        }
    )

    out = envgeo_utils.insert_gap_rows(df)

    assert len(out) == len(df) + 1
    gap_rows = out[out.isna().all(axis=1)]
    assert len(gap_rows) == 1


# Verifies that inserting gap rows does not disturb the original order of non-empty observations.
# 空白行を挿入しても、元の観測データの順序が維持されていることを確認する。
def test_insert_gap_rows_preserves_non_gap_row_order():
    df = pd.DataFrame(
        {
            "Latitude_degN": [35.0, 35.0, 36.0],
            "Longitude_degE": [135.0, 135.0, 136.0],
            "Year": [2020, 2020, 2020],
            "Month": [1, 1, 2],
            "reference": ["A", "A", "B"],
            "d18O": [0.1, 0.2, 0.3],
        }
    )

    out = envgeo_utils.insert_gap_rows(df)
    non_gap = out[out["d18O"].notna()].reset_index(drop=True)

    pd.testing.assert_series_equal(non_gap["d18O"], df["d18O"], check_names=False)
    pd.testing.assert_series_equal(non_gap["reference"], df["reference"], check_names=False)


# Verifies that depth-related variables use the dedicated depth colorscale.
# 深度に関する変数に対して、専用の深度カラースケールが返されることを確認する。
def test_get_custom_colorscale_returns_depth_scale_for_depth():
    scale = envgeo_utils.get_custom_colorscale("Depth_m")
    assert isinstance(scale, list)
    assert scale[0][1] == "red"
    assert scale[-1][1] == "darkblue"


# Verifies that non-depth variables use the standard colorscale.
# 深度以外の変数に対して、標準カラースケールが返されることを確認する。
def test_get_custom_colorscale_returns_standard_scale_for_non_depth():
    scale = envgeo_utils.get_custom_colorscale("d18O")
    assert isinstance(scale, list)
    assert "darkblue" in scale
    assert "red" in scale


# Verifies that coastline loading returns valid longitude and latitude lists of equal length.
# 海岸線データ読み込み結果として、有効な経度・緯度リストが同じ長さで返ることを確認する。
def test_load_coastline_data_returns_same_length_coordinate_lists():
    lon, lat = envgeo_utils.load_coastline_data(envgeo_utils.data_source_GLOBAL)
    assert isinstance(lon, list)
    assert isinstance(lat, list)
    assert len(lon) > 0
    assert len(lon) == len(lat)


def test_load_coastline_data_supports_110m_csv():
    lon_50m, lat_50m = envgeo_utils.load_coastline_data(
        envgeo_utils.data_source_GLOBAL,
        resolution="50m",
    )
    lon_110m, lat_110m = envgeo_utils.load_coastline_data(
        envgeo_utils.data_source_GLOBAL,
        resolution="110m",
    )

    assert len(lon_110m) == len(lat_110m)
    assert 0 < len(lon_110m) < len(lon_50m)


def test_usgs_geojson_to_dataframe_normalizes_core_columns():
    payload = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "id": "us-test",
                "properties": {
                    "time": 1_700_000_000_000,
                    "updated": 1_700_000_010_000,
                    "mag": 5.6,
                    "magType": "mww",
                    "place": "Test Region",
                    "tsunami": 0,
                    "alert": "green",
                    "status": "reviewed",
                    "url": "https://example.test/event",
                    "detail": "https://example.test/detail",
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [142.5, 38.1, 34.2],
                },
            }
        ],
    }

    df = envgeo_utils.usgs_geojson_to_dataframe(payload)

    assert len(df) == 1
    row = df.iloc[0]
    assert row["EventID"] == "us-test"
    assert row["Longitude_degE"] == 142.5
    assert row["Latitude_degN"] == 38.1
    assert row["Depth_km"] == 34.2
    assert row["Depth_m"] == 34200.0
    assert row["Magnitude"] == 5.6
    assert row["Dataset"] == "USGS Earthquake Catalog"
    assert row["reference"] == "USGS Earthquake Catalog API"


def test_usgs_geojson_to_dataframe_empty_payload_has_expected_columns():
    df = envgeo_utils.usgs_geojson_to_dataframe({"features": []})

    assert df.empty
    assert {"EventID", "Longitude_degE", "Latitude_degN", "Depth_km", "Magnitude"}.issubset(df.columns)
