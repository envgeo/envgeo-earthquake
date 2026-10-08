from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
PAGES = [
    (ROOT / "pages" / "54_🇺🇸_4D_Earthquake_Simple.py", "3D camera controls", "Command"),
    (ROOT / "pages" / "55_🇺🇸_4D_Earthquake_Advanced.py", "3D camera controls", "Command"),
    (ROOT / "pages" / "56_🇯🇵_4D_Earthquake_シンプル版.py", "3D視点操作", "Commandキー"),
    (ROOT / "pages" / "57_🇯🇵_4D_Earthquake_詳細版.py", "3D視点操作", "Commandキー"),
]


# -----------------------------------------------------------------------------
# Plotly camera guidance / Plotly 3D視点操作案内
# -----------------------------------------------------------------------------


@pytest.mark.parametrize("page_path,heading,modifier", PAGES)
def test_camera_guidance_precedes_main_3d_chart(page_path, heading, modifier):
    """Each bilingual page must explain 3D mouse/modifier-key operation.

    日英4pageで、3D図のマウス・modifier key操作を図の直前に案内する。
    """
    source = page_path.read_text(encoding="utf-8")
    guidance_index = source.index(heading)
    chart_index = source.index('key="earthquake_4d_hypocenter_map"')

    assert guidance_index < chart_index
    guidance = source[guidance_index:chart_index]
    assert modifier in guidance
    assert "Shift" in guidance
    assert "Control" in guidance
    assert "Option" in guidance
    assert "Alt" in guidance
    assert "Plotly" in guidance
    if heading == "3D視点操作":
        assert "視点や中心の動かし方を変えることができます" in guidance
        assert "変わることがあります" not in guidance
