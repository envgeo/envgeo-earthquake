import ast
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


# -----------------------------------------------------------------------------
# Plottable earthquake coordinates / 描画可能な地震座標
# -----------------------------------------------------------------------------


def _load_prepare_plot_dataframe(page_path):
    """Load the page's actual helper without running the Streamlit interface.

    Streamlit UIを実行せず、page内の実helperを読み込む。
    """
    source = page_path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(page_path))
    matches = [
        node
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and node.name == "prepare_plot_dataframe"
    ]
    assert len(matches) == 1

    namespace = {"pd": pd}
    helper_module = ast.fix_missing_locations(
        ast.Module(body=matches, type_ignores=[])
    )
    exec(compile(helper_module, str(page_path), "exec"), namespace)
    return namespace["prepare_plot_dataframe"]


@pytest.mark.parametrize("page_path", ACTIVE_VISUALIZER_PAGES)
def test_bilingual_pages_exclude_missing_and_out_of_range_coordinates(page_path):
    """All four pages must keep boundary points and reject invalid coordinates.

    4pageすべてで境界上の点を保持し、欠損・範囲外座標を除外する。
    """
    prepare_plot_dataframe = _load_prepare_plot_dataframe(page_path)
    source = pd.DataFrame(
        {
            "EventID": [
                "center",
                "southwest-boundary",
                "northeast-boundary",
                "missing-longitude",
                "missing-latitude",
                "east-out-of-range",
                "west-out-of-range",
                "north-out-of-range",
                "south-out-of-range",
                "non-numeric-longitude",
            ],
            "Longitude_degE": [
                139.7,
                -180.0,
                180.0,
                float("nan"),
                140.0,
                180.1,
                -180.1,
                140.0,
                140.0,
                "invalid",
            ],
            "Latitude_degN": [
                35.6,
                -90.0,
                90.0,
                35.0,
                float("nan"),
                35.0,
                35.0,
                90.1,
                -90.1,
                35.0,
            ],
            "Depth_km": [10.0] * 10,
            "Magnitude": [4.0] * 10,
        }
    )

    result = prepare_plot_dataframe(source)

    assert result["EventID"].tolist() == [
        "center",
        "southwest-boundary",
        "northeast-boundary",
    ]
    assert result[["Longitude_degE", "Latitude_degN"]].notna().all().all()
    assert result["Longitude_degE"].between(-180.0, 180.0).all()
    assert result["Latitude_degN"].between(-90.0, 90.0).all()
    assert (result["MarkerSize"] == 25.0).all()
    assert (result["MagnitudeMarkerSize"] == 14.0).all()


@pytest.mark.parametrize("page_path", ACTIVE_VISUALIZER_PAGES)
def test_bilingual_pages_return_empty_for_only_invalid_coordinates(page_path):
    """An entirely invalid response must safely produce no plottable rows.

    全行が不正座標でも例外にせず、描画対象0行を返す。
    """
    prepare_plot_dataframe = _load_prepare_plot_dataframe(page_path)
    source = pd.DataFrame(
        {
            "Longitude_degE": [float("nan"), 181.0],
            "Latitude_degN": [35.0, 91.0],
            "Depth_km": [10.0, 20.0],
            "Magnitude": [4.0, 5.0],
        }
    )

    result = prepare_plot_dataframe(source)

    assert result.empty
    assert "MarkerSize" not in result.columns
    assert "MagnitudeMarkerSize" not in result.columns
