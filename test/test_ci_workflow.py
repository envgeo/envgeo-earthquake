from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "ci.yml"


# -----------------------------------------------------------------------------
# GitHub Actions CI contract / GitHub Actions CI契約
# -----------------------------------------------------------------------------


def test_ci_covers_supported_python_versions_and_read_only_permissions():
    """CI must cover the advertised Python range with minimal permissions.

    CIが対応Python範囲を最小権限で確認することを保護する。
    """
    source = WORKFLOW.read_text(encoding="utf-8")

    assert 'python-version: ["3.10", "3.12"]' in source
    assert "permissions:\n  contents: read" in source
    assert "actions/checkout@v4" in source
    assert "actions/setup-python@v5" in source


def test_ci_runs_syntax_release_content_and_network_independent_tests():
    """CI must retain every release gate without invoking a live service.

    実serviceを呼ばず、構文・公開内容・全testをCIで維持する。
    """
    source = WORKFLOW.read_text(encoding="utf-8")

    assert "Check Python syntax" in source
    assert "test/test_repository_health.py" in source
    assert "Run network-independent test suite" in source
    assert "python -m pytest -q -p no:cacheprovider test" in source
