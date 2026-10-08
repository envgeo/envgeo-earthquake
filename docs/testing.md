# Testing Guide

[Japanese version](testing_Japanese.md)

Run from the project root after installing `requirements-dev.txt`:

```bash
python -m pytest -q test
```

## GitHub Actions

`.github/workflows/ci.yml` runs the same deterministic suite on Python 3.10 and
3.12. Separate steps parse all active/test Python files and run the
repository-health checks before the full suite. Runtime tests use mocked or
local responses and do not require live USGS, tile, JMA, or NIED access.

The workflow uses read-only repository permissions. A local workflow contract
protects the Python matrix, syntax check, release-content check, and test command.

The current suite covers utility import/centralized version, USGS citation metadata,
JMA/NIED responsibility metadata/records, and online-map source/attribution contracts,
current-working-directory-independent bundled assets, coastline and offline
map helpers, upload-format/dependency alignment, XLSX round-trip behavior,
bilingual normal/missing-column comparison-upload smoke paths,
USGS GeoJSON schema/row/numeric/time contracts, loader-level normal/empty/
incomplete payloads, malformed JSON/non-list `features`, HTTP error, timeout,
connection-error conversion, full required/optional query-parameter construction,
result-limit warning boundaries across all four pages, four-page plot-coordinate
handling for missing/non-numeric/out-of-range values and inclusive geographic
boundaries, four-page longitude wrapping/dateline line handling/local-km
conversion, bilingual Advanced section projection/corridor geometry,
network-free bilingual plate-boundary success/failure/malformed/fallback
paths, fixed/magnitude-linked marker sizing, the visual M7:M4 diameter ratio of
approximately 20:1 with an adjustable-ratio case, and direct 0.2–10.0 overall scale response across
all bilingual 2D/3D/cross-section profiles, persistent bilingual
Home/Simple/Advanced startup AppTests, and invalid
page-state recovery. Repository-health tests also enforce release structure,
ignore/tracked-file exclusions, runtime references, common secret/private-key
patterns, machine-specific absolute paths, symlinks, and Markdown links. It contains no
inherited Seawater dataset checks and requires no bundled Seawater files.

Four additional contracts ensure that bilingual Plotly camera guidance names
Shift/Control/Option (Alt)/Command and appears before each main 3D chart.

Recorded after the 2026-10-08 CI preparation: `178 passed, 0 skipped` in the
available local pytest environment. The Python 3.10 / 3.12 GitHub jobs remain
unverified until the workflow is copied, pushed, and completes on GitHub.

Current limitations include interactive browser workflows, live-service end-to-end
behavior, visual regression, varied JMA/NIED input schemas beyond the minimal retained contract, uncommon API failure cases,
and browser-level spatial interactions. CI tests must mock external
services and remain deterministic.

Record the exact Python/Streamlit/Plotly environment, command, and
pass/skip/fail counts in both work logs. A stale `.pytest_cache` is not test
evidence.
