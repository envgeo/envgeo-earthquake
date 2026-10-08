from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]


# -----------------------------------------------------------------------------
# Source-only distribution policy / source-only配布方針
# -----------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("policy_path", "paired_name"),
    [
        (ROOT / "docs" / "distribution.md", "distribution_Japanese.md"),
        (ROOT / "docs" / "distribution_Japanese.md", "distribution.md"),
    ],
)
def test_distribution_policy_records_release_and_zenodo_scope(
    policy_path, paired_name
):
    """Both languages must preserve the initial source-only release decision.

    日英両方で初回source-only release決定を維持する。
    """
    source = policy_path.read_text(encoding="utf-8")

    assert paired_name in source
    assert "source-only" in source
    assert "GitHub Release" in source
    assert "Zenodo" in source
    assert "PyPI" in source
    assert "pip install envgeo-earthquake" in source


@pytest.mark.parametrize(
    ("readme_path", "policy_name"),
    [
        (ROOT / "README.md", "docs/distribution.md"),
        (ROOT / "README_Japanese.md", "docs/distribution_Japanese.md"),
    ],
)
def test_readmes_link_distribution_policy_and_local_start(readme_path, policy_name):
    """Public READMEs must link the policy and retain the local start command.

    公開READMEが配布方針とlocal起動commandを維持する。
    """
    source = readme_path.read_text(encoding="utf-8")

    assert policy_name in source
    assert "streamlit run home.py" in source
