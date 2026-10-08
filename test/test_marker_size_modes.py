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
# Marker size modes / マーカーサイズ方式
# -----------------------------------------------------------------------------


def _load_marker_size_helper(page_path):
    """Load the page helper without starting the Streamlit interface.

    Streamlit UIを起動せず、page内の実helperを読み込む。
    """
    tree = ast.parse(page_path.read_text(encoding="utf-8"), filename=str(page_path))
    matches = [
        node
        for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name == "earthquake_marker_sizes"
    ]
    assert len(matches) == 1

    namespace = {"pd": pd}
    module = ast.fix_missing_locations(ast.Module(body=matches, type_ignores=[]))
    exec(compile(module, str(page_path), "exec"), namespace)
    return namespace["earthquake_marker_sizes"]


@pytest.mark.parametrize("page_path", ACTIVE_VISUALIZER_PAGES)
@pytest.mark.parametrize("view", ["3d", "2d", "section"])
def test_magnitude_mode_increases_marker_size(page_path, view):
    """Magnitude-linked mode must make larger earthquakes visibly larger.

    マグニチュード連動では、大きな地震ほどマーカーを大きくする。
    """
    marker_sizes = _load_marker_size_helper(page_path)
    sizes = marker_sizes(pd.Series([0.0, 2.0, 4.0, 6.0]), "magnitude", 1.0, view)

    assert sizes.is_monotonic_increasing
    assert sizes.nunique() == 4

    reference_sizes = marker_sizes(pd.Series([4.0, 7.0]), "magnitude", 1.0, view)
    assert reference_sizes.iloc[1] / reference_sizes.iloc[0] == pytest.approx(20.0)

    adjusted_sizes = marker_sizes(pd.Series([4.0, 7.0]), "magnitude", 1.0, view, 5.0)
    assert adjusted_sizes.iloc[1] / adjusted_sizes.iloc[0] == pytest.approx(5.0)


@pytest.mark.parametrize("page_path", ACTIVE_VISUALIZER_PAGES)
@pytest.mark.parametrize("view", ["3d", "2d", "section"])
def test_fixed_mode_uses_one_size(page_path, view):
    """Fixed mode must ignore magnitude while retaining the selected scale.

    固定サイズでは、倍率を保ったままマグニチュード差を反映しない。
    """
    marker_sizes = _load_marker_size_helper(page_path)
    sizes = marker_sizes(pd.Series([0.0, 2.0, 4.0, 6.0]), "fixed", 1.0, view)

    assert sizes.nunique() == 1


@pytest.mark.parametrize("page_path", ACTIVE_VISUALIZER_PAGES)
@pytest.mark.parametrize("view", ["3d", "2d", "section"])
def test_scale_value_is_a_direct_multiplier_up_to_twenty(page_path, view):
    """The UI scale value must directly match the visible multiplier.

    UI倍率の数値を、最大20倍まで表示倍率と直接一致させる。
    """
    marker_sizes = _load_marker_size_helper(page_path)
    standard = marker_sizes(pd.Series([2.0]), "fixed", 1.0, view).iloc[0]
    enlarged = marker_sizes(pd.Series([2.0]), "fixed", 20.0, view).iloc[0]

    assert enlarged / standard == pytest.approx(20.0)


@pytest.mark.parametrize("page_path", ACTIVE_VISUALIZER_PAGES)
def test_page_defaults_to_magnitude_linked_mode(page_path):
    """The first radio option must remain magnitude-linked in both languages.

    日英ともradioの先頭をマグニチュード連動に保つ。
    """
    source = page_path.read_text(encoding="utf-8")

    assert 'index=0' in source
    assert (
        '["Magnitude-linked", "Fixed size"]' in source
        or '["マグニチュード連動", "固定サイズ"]' in source
    )
    expected_scale_sliders = 3 if ("Advanced" in page_path.name or "詳細" in page_path.name) else 2
    overall_help = (
        "Direct overall multiplier"
        if "Earthquake_" in page_path.name and "🇺🇸" in page_path.name
        else "全体の直接倍率"
    )
    assert source.count(overall_help) == expected_scale_sliders
    assert source.count("max_value=30.0") == 1
    assert source.count('key="eq_magnitude_size_ratio"') == 1
    assert source.count('disabled=(marker_size_mode == "fixed")') == 1
