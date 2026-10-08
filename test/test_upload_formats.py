import ast
from io import BytesIO
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

import pandas as pd
import pytest


ROOT = Path(__file__).resolve().parents[1]
ADVANCED_PAGES = [
    ROOT / "pages" / "55_🇺🇸_4D_Earthquake_Advanced.py",
    ROOT / "pages" / "57_🇯🇵_4D_Earthquake_詳細版.py",
]
SUPPORTED_UPLOAD_FORMATS = ["csv", "tsv", "txt", "xlsx"]
UPLOAD_HELPER_NAMES = {
    "normalize_column_name",
    "find_catalog_column",
    "read_uploaded_catalog",
    "normalize_external_catalog",
}


# -----------------------------------------------------------------------------
# Catalog upload formats / カタログupload形式
# -----------------------------------------------------------------------------


def _file_uploader_types(tree):
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if not isinstance(node.func, ast.Attribute) or node.func.attr != "file_uploader":
            continue
        for keyword in node.keywords:
            if keyword.arg == "type":
                return ast.literal_eval(keyword.value)
    raise AssertionError("st.file_uploader(..., type=...) was not found")


def _load_page_upload_helpers(page_path):
    """Load only the upload helper definitions, without running the Streamlit page."""
    source = page_path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(page_path))
    helper_nodes = [
        node
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and node.name in UPLOAD_HELPER_NAMES
    ]
    assert {node.name for node in helper_nodes} == UPLOAD_HELPER_NAMES

    st_stub = SimpleNamespace(error=mock.Mock(), warning=mock.Mock())
    namespace = {"pd": pd, "st": st_stub}
    helper_module = ast.fix_missing_locations(
        ast.Module(body=helper_nodes, type_ignores=[])
    )
    exec(compile(helper_module, str(page_path), "exec"), namespace)
    return namespace, st_stub


class UploadedBytesIO(BytesIO):
    """Small in-memory stand-in for Streamlit's uploaded file."""

    def __init__(self, data, name):
        super().__init__(data)
        self.name = name


def test_bilingual_advanced_pages_advertise_supported_upload_formats_only():
    """Keep both upload controls aligned with declared runtime dependencies.

    日英のupload受付形式を宣言済み実行時依存と一致させる。
    """
    for page_path in ADVANCED_PAGES:
        tree = ast.parse(page_path.read_text(encoding="utf-8"), filename=str(page_path))
        assert _file_uploader_types(tree) == SUPPORTED_UPLOAD_FORMATS

        string_constants = {
            node.value
            for node in ast.walk(tree)
            if isinstance(node, ast.Constant) and isinstance(node.value, str)
        }
        assert ".xlsx" in string_constants
        assert ".xls" not in string_constants


def test_runtime_dependencies_match_excel_upload_policy():
    """Require the XLSX engine and avoid an unused legacy XLS dependency.

    XLSX engineを必須とし、使用しない旧XLS依存を追加しない。
    """
    requirement_lines = {
        line.strip().lower()
        for line in (ROOT / "requirements.txt").read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }
    assert any(line.startswith("openpyxl") for line in requirement_lines)
    assert not any(line.startswith("xlrd") for line in requirement_lines)


def test_xlsx_round_trip_uses_declared_runtime_engine():
    """Write and read a small XLSX workbook entirely in memory.

    小さなXLSX workbookをmemory内で書き込み・読み込みする。
    """
    expected = pd.DataFrame(
        {
            "Longitude_degE": [135.25],
            "Latitude_degN": [35.5],
            "Depth_km": [10.75],
            "Magnitude": [4.5],
        }
    )
    workbook = BytesIO()
    expected.to_excel(workbook, index=False, engine="openpyxl")
    workbook.seek(0)

    actual = pd.read_excel(workbook, engine="openpyxl")

    pd.testing.assert_frame_equal(actual, expected)


@pytest.mark.parametrize("page_path", ADVANCED_PAGES)
def test_bilingual_upload_helpers_smoke_normal_csv(page_path):
    """A representative catalog must read and normalize in both languages.

    代表catalogを日英両実装で読込み・標準化できることを確認する。
    """
    namespace, st_stub = _load_page_upload_helpers(page_path)
    upload = UploadedBytesIO(
        (
            b"Origin Time,Longitude,Latitude,Depth,Mag,Region\n"
            b"2026-01-02T03:04:05Z,139.7,35.6,12.3,4.8,Test Region\n"
        ),
        "catalog.csv",
    )

    raw = namespace["read_uploaded_catalog"](upload)
    normalized = namespace["normalize_external_catalog"](raw, "JMA test")

    assert len(normalized) == 1
    row = normalized.iloc[0]
    assert row["Longitude_degE"] == 139.7
    assert row["Latitude_degN"] == 35.6
    assert row["Depth_km"] == 12.3
    assert row["Magnitude"] == 4.8
    assert row["Catalog"] == "JMA test"
    assert row["Place"] == "Test Region"
    assert str(row["Time_UTC"]) == "2026-01-02 03:04:05+00:00"
    st_stub.error.assert_not_called()
    st_stub.warning.assert_not_called()


@pytest.mark.parametrize("page_path", ADVANCED_PAGES)
def test_bilingual_upload_helpers_smoke_missing_required_columns(page_path):
    """Missing required columns must produce a safe empty result and warning.

    必須列欠損は安全な空結果とwarningにする。
    """
    namespace, st_stub = _load_page_upload_helpers(page_path)
    upload = UploadedBytesIO(
        b"Origin Time,Longitude,Region\n2026-01-02T03:04:05Z,139.7,Test Region\n",
        "missing-columns.csv",
    )

    raw = namespace["read_uploaded_catalog"](upload)
    normalized = namespace["normalize_external_catalog"](raw, "JMA test")

    assert normalized.empty
    st_stub.error.assert_not_called()
    st_stub.warning.assert_called_once()
