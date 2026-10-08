import ast
import math
from pathlib import Path

import pandas as pd
import pytest


ROOT = Path(__file__).resolve().parents[1]
ACTIVE_VISUALIZER_PAGES = [
    ROOT / "pages" / "54_🇺🇸_4D_Earthquake_Simple.py",
    ROOT / "pages" / "55_🇺🇸_4D_Earthquake_Advanced.py",
    ROOT / "pages" / "56_🇯🇵_4D_Earthquake_シンプル版.py",
    ROOT / "pages" / "57_🇯🇵_4D_Earthquake_詳細版.py",
]
ADVANCED_PAGES = [
    ROOT / "pages" / "55_🇺🇸_4D_Earthquake_Advanced.py",
    ROOT / "pages" / "57_🇯🇵_4D_Earthquake_詳細版.py",
]
COMMON_HELPERS = {
    "wrap_longitudes_to_central_meridian",
    "wrap_line_with_breaks",
    "lonlat_to_local_km",
}
ADVANCED_HELPERS = COMMON_HELPERS | {
    "_normalize_longitude_180",
    "_unwrap_longitude_near_reference",
    "_cross_section_unwrapped_longitudes",
    "add_cross_section_coordinates",
    "local_km_to_lonlat",
    "cross_section_corridor_dataframe",
}


# -----------------------------------------------------------------------------
# Page spatial helpers / page空間処理helper
# -----------------------------------------------------------------------------


def _load_page_helpers(page_path, helper_names):
    """Load actual page helpers without running the Streamlit interface.

    Streamlit UIを実行せず、page内の実helperを読み込む。
    """
    source = page_path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(page_path))
    helper_nodes = [
        node
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and node.name in helper_names
    ]
    assert {node.name for node in helper_nodes} == helper_names

    namespace = {"math": math, "pd": pd}
    helper_module = ast.fix_missing_locations(
        ast.Module(body=helper_nodes, type_ignores=[])
    )
    exec(compile(helper_module, str(page_path), "exec"), namespace)
    return namespace


@pytest.mark.parametrize("page_path", ACTIVE_VISUALIZER_PAGES)
def test_bilingual_pages_wrap_longitudes_to_selected_meridian(page_path):
    """Equivalent longitudes must occupy one deterministic 360-degree branch.

    等価な経度を選択中央経線基準の同じ360度branchへ揃える。
    """
    helpers = _load_page_helpers(page_path, COMMON_HELPERS)
    wrap = helpers["wrap_longitudes_to_central_meridian"]

    result = wrap([-181, -180, -179, 179, 180, 181, 540], 0.0)

    assert result.tolist() == pytest.approx(
        [179.0, -180.0, -179.0, 179.0, -180.0, -179.0, -180.0]
    )
    assert wrap([-179.0, 179.0], 180.0).tolist() == pytest.approx(
        [181.0, 179.0]
    )


@pytest.mark.parametrize("page_path", ACTIVE_VISUALIZER_PAGES)
def test_bilingual_pages_break_or_preserve_dateline_lines_by_meridian(page_path):
    """A line breaks on a map seam but remains continuous on a Pacific branch.

    地図の継ぎ目では線を分割し、太平洋中心branchでは連続させる。
    """
    helpers = _load_page_helpers(page_path, COMMON_HELPERS)
    wrap_line = helpers["wrap_line_with_breaks"]

    seam_lon, seam_lat = wrap_line(
        [170.0, 179.0, -179.0, -170.0],
        [0.0, 1.0, 2.0, 3.0],
        0.0,
    )
    assert seam_lon[:2] == pytest.approx([170.0, 179.0])
    assert math.isnan(seam_lon[2])
    assert math.isnan(seam_lat[2])
    assert seam_lon[3:] == pytest.approx([-179.0, -170.0])

    pacific_lon, pacific_lat = wrap_line(
        [170.0, 179.0, -179.0, -170.0],
        [0.0, 1.0, 2.0, 3.0],
        180.0,
    )
    assert pacific_lon == pytest.approx([170.0, 179.0, 181.0, 190.0])
    assert pacific_lat == pytest.approx([0.0, 1.0, 2.0, 3.0])


@pytest.mark.parametrize("page_path", ACTIVE_VISUALIZER_PAGES)
def test_bilingual_pages_convert_dateline_points_to_local_km(page_path):
    """Points on opposite dateline sides must remain locally adjacent.

    日付変更線の両側にある点を近接したlocal km座標へ変換する。
    """
    helpers = _load_page_helpers(page_path, COMMON_HELPERS)
    convert = helpers["lonlat_to_local_km"]

    east_km, north_km = convert(
        [179.0, -179.0],
        [1.0, -1.0],
        center_lon=180.0,
        center_lat=0.0,
        central_meridian=180.0,
    )

    assert east_km.tolist() == pytest.approx([-111.320, 111.320])
    assert north_km.tolist() == pytest.approx([110.574, -110.574])


# -----------------------------------------------------------------------------
# Advanced cross-section geometry / Advanced断面幾何
# -----------------------------------------------------------------------------


@pytest.mark.parametrize("page_path", ADVANCED_PAGES)
def test_bilingual_advanced_sections_choose_short_dateline_path(page_path):
    """A 170E-to-170W section must span 20 degrees, not 340 degrees.

    170Eから170Wの断面を340度でなく20度の短経路にする。
    """
    helpers = _load_page_helpers(page_path, ADVANCED_HELPERS)
    unwrap = helpers["_cross_section_unwrapped_longitudes"]

    assert unwrap(170.0, -170.0) == pytest.approx((170.0, 190.0))
    assert unwrap(-170.0, 170.0) == pytest.approx((-170.0, -190.0))


@pytest.mark.parametrize("page_path", ADVANCED_PAGES)
def test_bilingual_advanced_sections_project_distance_and_offset(page_path):
    """Projection must produce along-section distance and signed offset.

    断面投影が断面方向距離と符号付き横ずれを返すことを確認する。
    """
    helpers = _load_page_helpers(page_path, ADVANCED_HELPERS)
    project = helpers["add_cross_section_coordinates"]
    source = pd.DataFrame(
        {
            "EventID": ["start", "middle", "end", "north-of-middle"],
            "Longitude_degE": [170.0, 180.0, -170.0, 180.0],
            "Latitude_degN": [0.0, 0.0, 0.0, 1.0],
        }
    )

    result, length_km = project(source, 170.0, 0.0, -170.0, 0.0)

    assert length_km == pytest.approx(2226.4)
    assert result["SectionDistance_km"].tolist() == pytest.approx(
        [0.0, 1113.2, 2226.4, 1113.2]
    )
    assert result["SectionOffset_km"].tolist() == pytest.approx(
        [0.0, 0.0, 0.0, 110.574]
    )


@pytest.mark.parametrize("page_path", ADVANCED_PAGES)
def test_bilingual_advanced_sections_handle_degenerate_line(page_path):
    """Coincident endpoints must return an empty section without division by zero.

    始終点が同じ断面はzero divisionせず空結果を返す。
    """
    helpers = _load_page_helpers(page_path, ADVANCED_HELPERS)
    project = helpers["add_cross_section_coordinates"]
    source = pd.DataFrame(
        {"Longitude_degE": [140.0], "Latitude_degN": [35.0]}
    )

    result, length_km = project(source, 140.0, 35.0, 140.0, 35.0)

    assert result.empty
    assert length_km == 0.0


@pytest.mark.parametrize("page_path", ADVANCED_PAGES)
def test_bilingual_advanced_sections_build_closed_dateline_corridor(page_path):
    """The swath polygon must close without a 360-degree seam jump.

    断面帯polygonを360度の継ぎ目jumpなしで閉じる。
    """
    helpers = _load_page_helpers(page_path, ADVANCED_HELPERS)
    corridor = helpers["cross_section_corridor_dataframe"]

    result = corridor(170.0, 0.0, -170.0, 0.0, half_width_km=100.0)

    assert list(result.columns) == ["Longitude_degE", "Latitude_degN"]
    assert len(result) == 5
    assert result.iloc[0].tolist() == pytest.approx(result.iloc[-1].tolist())
    assert result["Longitude_degE"].between(170.0, 190.0).all()
    assert result["Longitude_degE"].diff().dropna().abs().max() < 180.0
    assert result["Latitude_degN"].abs().max() == pytest.approx(
        100.0 / 110.574
    )
