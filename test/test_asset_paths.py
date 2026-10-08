import sys
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import envgeo_utils


# -----------------------------------------------------------------------------
# CWD-independent bundled assets / CWDに依存しない同梱asset
# -----------------------------------------------------------------------------


def test_coastline_loading_is_independent_of_current_working_directory(
    tmp_path,
    monkeypatch,
):
    """Load both bundled coastline resolutions after moving outside the project.

    project外へcurrent directoryを移動しても、両解像度の同梱海岸線を読み込む。
    """
    monkeypatch.chdir(tmp_path)
    envgeo_utils.load_coastline_data.clear()

    for resolution in ("50m", "110m"):
        longitude, latitude = envgeo_utils.load_coastline_data(
            envgeo_utils.data_source_GLOBAL,
            resolution=resolution,
        )
        assert longitude
        assert len(longitude) == len(latitude)


@pytest.mark.parametrize(
    ("page_path", "readme_marker"),
    [
        (ROOT / "home.py", "Current development version"),
        (ROOT / "pages" / "00_home_(Japanese).py", "現在の開発バージョン"),
    ],
)
def test_home_readme_loading_is_independent_of_current_working_directory(
    tmp_path,
    monkeypatch,
    page_path,
    readme_marker,
):
    """Render each bundled README from a working directory outside the project.

    project外のcurrent directoryから、日英Homeの同梱READMEを描画する。
    """
    monkeypatch.chdir(tmp_path)

    app = AppTest.from_file(str(page_path)).run(timeout=60)

    assert len(app.exception) == 0
    assert any(readme_marker in element.value for element in app.markdown)
