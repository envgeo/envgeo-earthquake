import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


# -----------------------------------------------------------------------------
# Public-release repository health / 公開版repository health
# -----------------------------------------------------------------------------


EXCLUDED_ROOT_NAMES = {
    ".devcontainer",
    "__ToDo__",
    "__logo__",
    "data",
    "images",
    "old",
}
EXCLUDED_ROOT_FILES = {
    "AGENTS.md",
    "AGENTS_Japanese.md",
    "LOCAL_WORKSPACE.md",
    "LOCAL_WORKSPACE_Japanese.md",
    "PROJECT_STATUS.md",
    "PROJECT_STATUS_Japanese.md",
    "TODO.md",
    "TODO_Japanese.md",
}
EXCLUDED_RELATIVE_PATHS = {
    Path("docs/capture_manual_screenshots.mjs"),
    Path("docs/development_workflow.md"),
    Path("docs/development_workflow_Japanese.md"),
    Path("docs/public_release_scope.md"),
    Path("docs/public_release_scope_Japanese.md"),
    Path("docs/publication_audit_2026-10-08.md"),
    Path("docs/publication_audit_2026-10-08_Japanese.md"),
    Path("docs/publication_roadmap.md"),
    Path("docs/publication_roadmap_Japanese.md"),
    Path("docs/release_checklist.md"),
    Path("docs/release_checklist_Japanese.md"),
    Path("docs/work_log.md"),
    Path("docs/work_log_English.md"),
}
GENERATED_DIRECTORY_NAMES = {
    ".git",
    ".hypothesis",
    ".mypy_cache",
    ".nox",
    ".pytest_cache",
    ".ruff_cache",
    ".tox",
    "__pycache__",
    "build",
    "dist",
    "htmlcov",
}
GENERATED_FILE_NAMES = {".DS_Store", "Thumbs.db", ".coverage"}
PUBLIC_ROOT_FILES = {
    ".gitignore",
    "CONTRIBUTING.md",
    "CITATION.cff",
    "Home.py",
    "home.py",
    "LICENSE",
    "NOTICE.md",
    "README.md",
    "README_Japanese.md",
    "envgeo_utils.py",
    "pyproject.toml",
    "requirements-dev.txt",
    "requirements.txt",
    "runtime.txt",
}
PUBLIC_ROOT_DIRECTORIES = {".github", "coastline", "docs", "pages", "test"}
TEXT_SUFFIXES = {
    "",
    ".gitignore",
    ".json",
    ".md",
    ".mjs",
    ".py",
    ".toml",
    ".txt",
    ".yaml",
    ".yml",
}


def _is_generated(relative_path):
    return (
        any(part in GENERATED_DIRECTORY_NAMES for part in relative_path.parts)
        or relative_path.name in GENERATED_FILE_NAMES
        or relative_path.suffix in {".pyc", ".pyo", ".log", ".tmp", ".temp"}
        or relative_path.name.startswith(".coverage.")
    )


def _is_excluded(relative_path):
    return (
        relative_path.parts[0] in EXCLUDED_ROOT_NAMES
        or relative_path.name in EXCLUDED_ROOT_FILES
        or relative_path in EXCLUDED_RELATIVE_PATHS
        or _is_generated(relative_path)
    )


def _release_candidate_files():
    """Yield intended public files while retaining excluded local material on disk.

    除外するlocal資料をdiskに残したまま、公開候補fileだけを列挙する。
    """
    for path in ROOT.rglob("*"):
        if not path.is_file() and not path.is_symlink():
            continue
        relative_path = path.relative_to(ROOT)
        if not _is_excluded(relative_path):
            yield relative_path


def _tracked_files_if_standalone_clone():
    """Return tracked files only when this project root owns its Git metadata."""
    if not (ROOT / ".git").exists():
        return None
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    return [Path(item.decode("utf-8")) for item in result.stdout.split(b"\0") if item]


def _text_release_files():
    for relative_path in _release_candidate_files():
        if relative_path.suffix.lower() in TEXT_SUFFIXES:
            yield relative_path


def test_release_candidates_use_only_approved_top_level_entries():
    unexpected = []
    for relative_path in _release_candidate_files():
        top_level = relative_path.parts[0]
        if len(relative_path.parts) == 1:
            if top_level not in PUBLIC_ROOT_FILES:
                unexpected.append(relative_path.as_posix())
        elif top_level not in PUBLIC_ROOT_DIRECTORIES:
            unexpected.append(relative_path.as_posix())

    assert unexpected == []


def test_gitignore_covers_private_generated_and_development_material():
    ignore_lines = {
        line.strip()
        for line in (ROOT / ".gitignore").read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }

    for directory in EXCLUDED_ROOT_NAMES:
        assert f"/{directory}/" in ignore_lines
    for filename in EXCLUDED_ROOT_FILES:
        assert f"/{filename}" in ignore_lines or filename in ignore_lines
    for relative_path in EXCLUDED_RELATIVE_PATHS:
        assert f"/{relative_path.as_posix()}" in ignore_lines
    for required_rule in {
        ".DS_Store",
        ".pytest_cache/",
        ".streamlit/secrets.toml",
        "*.log",
        "*.py[cod]",
        "__pycache__/",
        "build/",
        "dist/",
    }:
        assert required_rule in ignore_lines


def test_standalone_clone_tracks_no_excluded_or_generated_files():
    tracked_files = _tracked_files_if_standalone_clone()
    if tracked_files is None:
        return

    rejected = [path.as_posix() for path in tracked_files if _is_excluded(path)]
    assert rejected == []


def test_runtime_python_does_not_reference_excluded_directories():
    runtime_files = [ROOT / "home.py", ROOT / "envgeo_utils.py", *sorted((ROOT / "pages").glob("*.py"))]
    findings = []
    for path in runtime_files:
        text = path.read_text(encoding="utf-8")
        # Provider URLs may legitimately contain segments such as `data/`.
        # 提供元URL内の`data/`などはlocal directory依存ではないため除外する。
        local_reference_text = re.sub(r"https?://[^\s'\")]+", "", text)
        for directory in EXCLUDED_ROOT_NAMES:
            if f"{directory}/" in local_reference_text:
                findings.append((path.relative_to(ROOT).as_posix(), directory))
    assert findings == []


def test_release_text_contains_no_secret_values_or_private_keys():
    secret_patterns = {
        "private key": re.compile("-----BEGIN " + r"(?:RSA |OPENSSH |EC )?PRIVATE KEY-----"),
        "GitHub token": re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})\b"),
        "AWS access key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
        "OpenAI-style key": re.compile(r"\bsk-[A-Za-z0-9]{20,}\b"),
        "credential URL": re.compile(r"https?://[^\s/:]+:[^\s/@]+@"),
        "assigned secret": re.compile(
            r"(?i)\b(?:api[_-]?key|client[_-]?secret|access[_-]?token|auth[_-]?token|password|passwd)"
            r"\s*[:=]\s*['\"][^'\"\r\n]{8,}['\"]"
        ),
    }
    findings = []
    for relative_path in _text_release_files():
        text = (ROOT / relative_path).read_text(encoding="utf-8", errors="replace")
        for label, pattern in secret_patterns.items():
            if pattern.search(text):
                findings.append((relative_path.as_posix(), label))
    assert findings == []


def test_release_text_contains_no_machine_specific_absolute_paths():
    absolute_path_patterns = {
        "macOS user path": re.compile(r"/Users/[A-Za-z0-9._-]+/"),
        "Linux home path": re.compile(r"/home/[A-Za-z0-9._-]+/"),
        "Windows user path": re.compile(r"[A-Za-z]:\\Users\\[^\\\r\n]+\\"),
    }
    findings = []
    for relative_path in _text_release_files():
        text = (ROOT / relative_path).read_text(encoding="utf-8", errors="replace")
        for label, pattern in absolute_path_patterns.items():
            if pattern.search(text):
                findings.append((relative_path.as_posix(), label))
    assert findings == []


def test_release_candidates_contain_no_symlinks():
    symlinks = [
        relative_path.as_posix()
        for relative_path in _release_candidate_files()
        if (ROOT / relative_path).is_symlink()
    ]
    assert symlinks == []


def test_release_markdown_local_links_resolve():
    missing = []
    markdown_link = re.compile(r"!?\[[^]]*\]\(([^)]+)\)")
    for relative_path in _release_candidate_files():
        if relative_path.suffix.lower() != ".md":
            continue
        path = ROOT / relative_path
        text = path.read_text(encoding="utf-8")
        for target in markdown_link.findall(text):
            target = target.strip().split("#", 1)[0]
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            if not (path.parent / target).resolve().exists():
                missing.append((relative_path.as_posix(), target))
    assert missing == []
