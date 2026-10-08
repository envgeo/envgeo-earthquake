import ast
import io
import json
from pathlib import Path
from types import SimpleNamespace
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, urlencode, urlparse
from urllib.request import Request

import pandas as pd
import pytest


ROOT = Path(__file__).resolve().parents[1]
ADVANCED_PAGES = [
    ROOT / "pages" / "55_🇺🇸_4D_Earthquake_Advanced.py",
    ROOT / "pages" / "57_🇯🇵_4D_Earthquake_詳細版.py",
]
PLATE_HELPERS = {
    "fallback_japan_plate_boundary_features",
    "fetch_usgs_plate_boundary_features",
    "iter_line_coordinates",
    "coordinate_in_query_window",
    "plate_features_to_dataframe",
    "load_plate_boundary_dataframe",
}
JAPAN_REGION_LABEL = "Japan and surrounding area"
USGS_SOURCE_LABEL = "USGS Tectonic Plate Boundaries"
FALLBACK_SOURCE_LABEL = "Approximate Japan plate-boundary fallback"
PLATE_SERVICE = "https://example.invalid/MapServer"
JAPAN_QUERY = {
    "region_preset": JAPAN_REGION_LABEL,
    "lon_min": 120.0,
    "lon_max": 155.0,
    "lat_min": 20.0,
    "lat_max": 50.0,
}
NON_JAPAN_QUERY = {
    "region_preset": "Global",
    "lon_min": -180.0,
    "lon_max": 180.0,
    "lat_min": -90.0,
    "lat_max": 90.0,
}


# -----------------------------------------------------------------------------
# Plate-boundary retrieval fallback / プレート境界取得fallback
# -----------------------------------------------------------------------------


class _StreamlitCacheStub:
    @staticmethod
    def cache_data(**kwargs):
        return lambda function: function


def _load_plate_helpers(page_path):
    """Load actual Advanced-page helpers without running the Streamlit UI.

    Streamlit UIを実行せず、Advanced page内の実helperを読み込む。
    """
    source = page_path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(page_path))
    helper_nodes = [
        node
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and node.name in PLATE_HELPERS
    ]
    assert {node.name for node in helper_nodes} == PLATE_HELPERS

    namespace = {
        "HTTPError": HTTPError,
        "JAPAN_REGION_LABEL": JAPAN_REGION_LABEL,
        "PLATE_LAYER_IDS": {1: "Plates", 0: "Microplates"},
        "Request": Request,
        "TimeoutError": TimeoutError,
        "URLError": URLError,
        "USGS_PLATE_BOUNDARY_SERVICE": PLATE_SERVICE,
        "json": json,
        "pd": pd,
        "st": _StreamlitCacheStub(),
        "urlencode": urlencode,
        "urlopen": None,
    }
    helper_module = ast.fix_missing_locations(
        ast.Module(body=helper_nodes, type_ignores=[])
    )
    exec(compile(helper_module, str(page_path), "exec"), namespace)
    return namespace


def _feature(name="Test boundary", label="Convergent Boundary"):
    return {
        "type": "Feature",
        "properties": {"NAME": name, "LABEL": label},
        "geometry": {
            "type": "LineString",
            "coordinates": [[140.0, 35.0], [141.0, 36.0]],
        },
    }


def _json_response(payload):
    return io.BytesIO(json.dumps(payload).encode("utf-8"))


@pytest.mark.parametrize("page_path", ADVANCED_PAGES)
def test_bilingual_advanced_fetches_plate_and_microplate_layers(page_path):
    """Successful requests must retain layer identity and query parameters.

    正常取得時にlayer識別とquery parameterを維持する。
    """
    namespace = _load_plate_helpers(page_path)
    requested_urls = []

    def fake_urlopen(request, timeout):
        requested_urls.append(request.full_url)
        return _json_response({"type": "FeatureCollection", "features": [_feature()]})

    namespace["urlopen"] = fake_urlopen
    features, errors = namespace["fetch_usgs_plate_boundary_features"](True)

    assert errors == []
    assert [item["properties"]["Layer"] for item in features] == [
        "Plates",
        "Microplates",
    ]
    assert [urlparse(url).path for url in requested_urls] == [
        "/MapServer/1/query",
        "/MapServer/0/query",
    ]
    for url in requested_urls:
        params = parse_qs(urlparse(url).query)
        assert params["f"] == ["geojson"]
        assert params["outSR"] == ["4326"]
        assert params["returnGeometry"] == ["true"]


@pytest.mark.parametrize("page_path", ADVANCED_PAGES)
def test_bilingual_advanced_uses_japan_fallback_after_connection_failure(page_path):
    """A total service failure must produce labeled Japan schematic lines.

    service全面失敗時に日本周辺の明示された模式線へ切り替える。
    """
    namespace = _load_plate_helpers(page_path)

    def fail_urlopen(request, timeout):
        raise URLError("offline")

    namespace["urlopen"] = fail_urlopen
    result, source, errors = namespace["load_plate_boundary_dataframe"](
        JAPAN_QUERY, False
    )

    assert source == FALLBACK_SOURCE_LABEL
    assert errors and errors[0].startswith("Plates:")
    assert not result.empty
    assert set(result["Label"].dropna()) == {"Approximate"}
    assert set(result["Layer"].dropna()) == {"Approximate Japan"}
    assert "Japan Trench (approx.)" in set(result["Name"].dropna())


@pytest.mark.parametrize("page_path", ADVANCED_PAGES)
def test_bilingual_advanced_does_not_apply_japan_fallback_elsewhere(page_path):
    """Japan-only schematic data must not appear for a non-Japan query.

    日本専用模式線を日本以外のqueryへ表示しない。
    """
    namespace = _load_plate_helpers(page_path)

    def fail_urlopen(request, timeout):
        raise TimeoutError("timed out")

    namespace["urlopen"] = fail_urlopen
    result, source, errors = namespace["load_plate_boundary_dataframe"](
        NON_JAPAN_QUERY, False
    )

    assert result.empty
    assert source == USGS_SOURCE_LABEL
    assert errors and errors[0].startswith("Plates:")


@pytest.mark.parametrize(
    "payload",
    [
        {"type": "FeatureCollection", "features": {"unexpected": True}},
        {"type": "FeatureCollection", "features": ["not-a-feature"]},
    ],
)
@pytest.mark.parametrize("page_path", ADVANCED_PAGES)
def test_bilingual_advanced_falls_back_for_malformed_geojson(page_path, payload):
    """Malformed successful responses must use the same safe fallback path.

    HTTP成功でも不正GeoJSONなら同じ安全なfallback経路を使う。
    """
    namespace = _load_plate_helpers(page_path)
    namespace["urlopen"] = lambda request, timeout: _json_response(payload)

    result, source, errors = namespace["load_plate_boundary_dataframe"](
        JAPAN_QUERY, False
    )

    assert source == FALLBACK_SOURCE_LABEL
    assert errors
    assert not result.empty
    assert set(result["Label"].dropna()) == {"Approximate"}


@pytest.mark.parametrize("page_path", ADVANCED_PAGES)
def test_bilingual_advanced_keeps_available_usgs_layer_after_partial_failure(page_path):
    """A microplate failure must not replace a valid main-plate response.

    microplate失敗時も取得済みmain plateをfallbackで置き換えない。
    """
    namespace = _load_plate_helpers(page_path)

    def partial_urlopen(request, timeout):
        if "/1/query" in request.full_url:
            return _json_response(
                {"type": "FeatureCollection", "features": [_feature()]}
            )
        raise HTTPError(request.full_url, 503, "Service Unavailable", None, None)

    namespace["urlopen"] = partial_urlopen
    result, source, errors = namespace["load_plate_boundary_dataframe"](
        JAPAN_QUERY, True
    )

    assert source == USGS_SOURCE_LABEL
    assert errors and errors[0].startswith("Microplates:")
    assert not result.empty
    assert set(result["Layer"].dropna()) == {"Plates"}
    assert "Approximate" not in set(result["Label"].dropna())


def test_bilingual_advanced_pages_distinguish_partial_failure_warning():
    """Partial USGS data and Japan fallback must not share a misleading warning.

    一部USGS dataと日本fallbackを誤解させる同一warningにしない。
    """
    english = ADVANCED_PAGES[0].read_text(encoding="utf-8")
    japanese = ADVANCED_PAGES[1].read_text(encoding="utf-8")

    for source in (english, japanese):
        assert 'plate_source == "Approximate Japan plate-boundary fallback"' in source
    assert "available USGS layers are shown" in english
    assert "取得済みlayerだけを表示しています" in japanese
