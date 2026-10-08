import sys
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import envgeo_utils


# -----------------------------------------------------------------------------
# Persistent bilingual page startup smoke / 日英page起動の永続smoke
# -----------------------------------------------------------------------------


PAGE_CASES = [
    pytest.param(
        ROOT / "Home.py",
        "Start",
        None,
        id="home-english",
    ),
    pytest.param(
        ROOT / "pages" / "00_home_(Japanese).py",
        "データソースと参考情報",
        None,
        id="home-japanese",
    ),
    pytest.param(
        ROOT / "pages" / "54_🇺🇸_4D_Earthquake_Simple.py",
        f"4D Visualizer Earthquake Simple ({envgeo_utils.APP_VERSION})",
        [":red[Fetch / update]", ":red[Fetch / update!]"],
        id="simple-english",
    ),
    pytest.param(
        ROOT / "pages" / "55_🇺🇸_4D_Earthquake_Advanced.py",
        f"4D Visualizer Earthquake Advanced ({envgeo_utils.APP_VERSION})",
        [":red[Fetch / update]", ":red[Fetch / update!]"],
        id="advanced-english",
    ),
    pytest.param(
        ROOT / "pages" / "56_🇯🇵_4D_Earthquake_シンプル版.py",
        f"4D Visualizer Earthquake 簡易版（{envgeo_utils.APP_VERSION}）",
        [":red[取得 / 更新]", ":red[取得 / 更新！]"],
        id="simple-japanese",
    ),
    pytest.param(
        ROOT / "pages" / "57_🇯🇵_4D_Earthquake_詳細版.py",
        f"4D Visualizer Earthquake 詳細版（{envgeo_utils.APP_VERSION}）",
        [":red[取得 / 更新]", ":red[取得 / 更新！]"],
        id="advanced-japanese",
    ),
]


@pytest.mark.parametrize(
    ("page_path", "expected_heading", "expected_buttons"), PAGE_CASES
)
def test_bilingual_pages_start_without_exceptions(
    page_path, expected_heading, expected_buttons
):
    """Each public page must render its initial state without external requests.

    各公開pageが外部取得なしの初期状態を例外なく描画する。
    """
    app = AppTest.from_file(str(page_path)).run(timeout=60)

    assert list(app.exception) == []
    assert [title.value for title in app.title] == ["EnvGeo-Earthquake"]

    visible_headings = [item.value for item in app.header]
    assert expected_heading in visible_headings

    button_labels = [button.label for button in app.button]
    if expected_buttons is None:
        assert button_labels == []
    else:
        assert button_labels == expected_buttons
