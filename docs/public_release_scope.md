# EnvGeo-Earthquake Public-Release Scope

[Japanese version](public_release_scope_Japanese.md)

Decision date: 2026-10-08

This document defines the intended contents of the first stable public source
release. It is a scope decision, not evidence that every listed file is already
release-ready. Release blockers in the publication roadmap must still be
resolved. EnvGeo-Seawater remains outside this scope and must not become a
runtime dependency.

## Include in the public release

### Application and runtime data

- `home.py`
- `envgeo_utils.py`, after inherited Seawater loading and unpublished-data
  references are removed
- the five active files in `pages/`
- `coastline/world_coastline_coordinates_50m.csv`
- `coastline/world_coastline_coordinates_110m.csv`
- `coastline/LICENSE_OR_SOURCE.md` and
  `coastline/LICENSE_OR_SOURCE_Japanese.md`

### Runtime, tests, and automation

- `requirements.txt`, `requirements-dev.txt`, and `runtime.txt`
- `.gitignore`
- the maintained source files in `test/`
- the future network-independent GitHub Actions workflow
- packaging metadata and a launcher only if installable-package distribution is
  selected later

### Legal, citation, maintenance, and user documentation

- `LICENSE`, `NOTICE.md`, `CONTRIBUTING.md`, and the future `CITATION.cff`
- `README.md`, `README_Japanese.md`, `TODO.md`, and `TODO_Japanese.md`
- `PROJECT_STATUS.md`, `PROJECT_STATUS_Japanese.md`, `AGENTS.md`, and
  `AGENTS_Japanese.md`
- the maintained Markdown documents in `docs/`, including both work logs,
  both manuals, the audit, roadmap, testing guide, workflow, release checklist,
  and this scope decision
- `docs/assets/screenshots/en/*.png` and
  `docs/assets/screenshots/ja/*.png`, because the manuals use them
- `docs/capture_manual_screenshots.mjs`

The work logs and handoff files are included so that a fresh clone and a new
development chat can reconstruct the project's decisions and current state.
They must be reviewed for secrets, private data, and machine-specific paths
before each public release.

## Exclude from the public release

- `old/`: development snapshots, superseded code, and filenames unsuitable for
  a portable source archive
- `data/`: current contents are Seawater sample/scratch spreadsheets and are not
  Earthquake runtime inputs
- `__ToDo__/`: private scratch document
- `__logo__/`, `images/`, and other logo candidates: unused design and
  explanatory assets; no logo image is included in the current public scope
- `.devcontainer/` for the first stable release, unless its disabled XSRF
  setting is corrected and the configuration is explicitly reviewed
- `.DS_Store`, `__pycache__/`, `.pytest_cache/`, bytecode, test caches, coverage
  output, build output, logs, temporary files, editor files, and virtual
  environments
- secrets, tokens, `.streamlit/secrets.toml`, private datasets, unpublished
  filenames, and absolute local filesystem paths
- `LOCAL_WORKSPACE.md` and `LOCAL_WORKSPACE_Japanese.md`, which intentionally
  store machine-specific paths and local Git operating rules

Excluded development material remains untouched in the working folder. This
decision only governs what is copied or tracked for a public release.
The six development-only directories listed above are enforced with
root-anchored `.gitignore` rules. Current active/test Python files contain no
string reference beginning with one of those directory paths.

## Release-content acceptance criteria

Before tagging a release:

1. No included code or documentation may require a file from an excluded
   directory.
2. A repository-health test must enforce the allowed content and reject
   generated files, secrets, absolute local paths, and irrelevant datasets.
3. All local links in included Markdown files must resolve within the release.
4. The application and tests must work from a clean checkout without
   EnvGeo-Seawater.
5. The GitHub source archive must be inspected and match this scope.

## Later changes to this scope

A scope change must be made in both language versions and recorded in both work
logs. Moving a candidate into EnvGeo Core is a separate post-release decision;
it does not silently remove a file or dependency from this standalone release.
