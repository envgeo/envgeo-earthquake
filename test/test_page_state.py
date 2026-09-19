from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize(
    ("page_name", "state_key"),
    [
        (
            "54_🇺🇸_4D_Earthquake_Simple.py",
            "eq_en_simple_lon_range_Japan and surrounding area",
        ),
        (
            "55_🇺🇸_4D_Earthquake_Advanced.py",
            "eq_en_advanced_lon_range_Japan and surrounding area",
        ),
        (
            "56_🇯🇵_4D_Earthquake_シンプル版.py",
            "eq_ja_simple_lon_range_日本周辺",
        ),
        (
            "57_🇯🇵_4D_Earthquake_詳細版.py",
            "eq_ja_advanced_lon_range_日本周辺",
        ),
    ],
)
def test_invalid_longitude_state_is_restored(page_name, state_key):
    """Page switching must not retain a longitude span wider than 360 degrees."""
    streamlit_testing = pytest.importorskip("streamlit.testing.v1")
    app = streamlit_testing.AppTest.from_file(str(ROOT / "pages" / page_name))

    app.session_state[state_key] = (-180.0, 360.0)
    app.run(timeout=30)

    assert not app.exception
    assert not app.warning
    assert app.session_state[state_key] == (120.0, 155.0)
