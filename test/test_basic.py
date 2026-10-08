import sys
import os
import ast
from datetime import date
from pathlib import Path

# Add the parent directory of the current file to sys.path
# 現在のファイル（test_basic.py）の1つ上の階層をシステムパスに追加
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the target module after setting the path
# パスを通した後に、テスト対象のモジュールをインポートします
import envgeo_utils


ROOT = Path(__file__).resolve().parents[1]
VERSION_CONSUMERS = [
    ROOT / "home.py",
    ROOT / "pages" / "00_home_(Japanese).py",
    ROOT / "pages" / "54_🇺🇸_4D_Earthquake_Simple.py",
    ROOT / "pages" / "55_🇺🇸_4D_Earthquake_Advanced.py",
    ROOT / "pages" / "56_🇯🇵_4D_Earthquake_シンプル版.py",
    ROOT / "pages" / "57_🇯🇵_4D_Earthquake_詳細版.py",
]
PLATE_CITATION_CONSUMERS = [
    ROOT / "home.py",
    ROOT / "pages" / "00_home_(Japanese).py",
    ROOT / "pages" / "55_🇺🇸_4D_Earthquake_Advanced.py",
    ROOT / "pages" / "57_🇯🇵_4D_Earthquake_詳細版.py",
]


# -----------------------------------------------------------------------------
# Import and version metadata / importとバージョンmetadata
# -----------------------------------------------------------------------------

def test_import():
    """
    Test if the target module can be imported successfully.
    対象のモジュールが正しくインポートできるかをテスト
    """
    assert envgeo_utils is not None

def test_version():
    """
    Test if the version information exists in the module.
    モジュール内にバージョン情報が存在するかをテスト
    """
    assert envgeo_utils.version == envgeo_utils.APP_VERSION
    assert envgeo_utils.APP_VERSION
    assert date.fromisoformat(envgeo_utils.APP_VERSION_DATE)


def test_active_pages_use_shared_version_metadata():
    """Require all active pages to read the one utility version definition.

    全アクティブページがutilityの単一バージョン定義を参照することを確認する。
    """
    for path in VERSION_CONSUMERS:
        source = path.read_text(encoding="utf-8")
        assert "envgeo_utils.APP_VERSION" in source, path

        tree = ast.parse(source, filename=str(path))
        for node in tree.body:
            if not isinstance(node, (ast.Assign, ast.AnnAssign)):
                continue
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            value = node.value
            names = {target.id for target in targets if isinstance(target, ast.Name)}
            assert not (
                names.intersection({"APP_VERSION", "version"})
                and isinstance(value, ast.Constant)
                and isinstance(value.value, str)
            ), f"duplicated local version metadata: {path}"


# -----------------------------------------------------------------------------
# Source and citation metadata / 出典・引用metadata
# -----------------------------------------------------------------------------

def test_active_pages_use_shared_usgs_citations():
    """Keep bilingual catalog and plate citations synchronized.

    日英画面のカタログ・プレート境界引用を共通定義へ同期する。
    """
    assert envgeo_utils.USGS_CATALOG_CITATION == (
        "U.S. Geological Survey. (2017). Advanced National Seismic System (ANSS) "
        "Comprehensive Catalog. U.S. Geological Survey. "
        "https://doi.org/10.5066/F7MS3QZH"
    )
    assert "10.1029/2001GC000252" in envgeo_utils.BIRD_PLATE_BOUNDARY_CITATION
    assert "10.1111/j.1365-246X.2009.04491.x" in envgeo_utils.DEMETS_PLATE_MOTION_CITATION

    for path in VERSION_CONSUMERS:
        source = path.read_text(encoding="utf-8")
        assert "envgeo_utils.USGS_CATALOG_CITATION" in source, path

    for path in PLATE_CITATION_CONSUMERS:
        source = path.read_text(encoding="utf-8")
        assert "envgeo_utils.USGS_SEISMICITY_MAP_SERIES_URL" in source, path
        assert "envgeo_utils.BIRD_PLATE_BOUNDARY_CITATION" in source, path
        assert "envgeo_utils.DEMETS_PLATE_MOTION_CITATION" in source, path


def test_jma_nied_responsibility_metadata_and_records():
    """Keep optional-upload responsibilities explicit and bilingual.

    任意uploadの利用・再配布責任と日英記録を維持する。
    """
    assert envgeo_utils.JMA_WEBSITE_TERMS_URL.startswith("https://www.jma.go.jp/")
    assert envgeo_utils.JMA_BULLETIN_USAGE_URL.startswith(
        "https://www.data.jma.go.jp/"
    )
    assert envgeo_utils.NIED_HINET_DATA_GUIDANCE_URL.startswith(
        "https://www.hinet.bosai.go.jp/"
    )
    assert "10.17598/NIED.0003" in envgeo_utils.NIED_HINET_CITATION

    for path in VERSION_CONSUMERS[:2]:
        source = path.read_text(encoding="utf-8")
        assert "envgeo_utils.JMA_WEBSITE_TERMS_URL" in source, path
        assert "envgeo_utils.NIED_HINET_DATA_GUIDANCE_URL" in source, path
        assert "envgeo_utils.NIED_HINET_CITATION" in source, path

    records = [
        ROOT / "docs" / "jma_nied_data_responsibilities.md",
        ROOT / "docs" / "jma_nied_data_responsibilities_Japanese.md",
    ]
    for path in records:
        text = path.read_text(encoding="utf-8")
        assert "10.17598/NIED.0003" in text, path
        assert "readme_j.html" in text, path
        assert "hinet.bosai.go.jp" in text, path
