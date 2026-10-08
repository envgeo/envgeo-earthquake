# Release Checklist

[Japanese version](release_checklist_Japanese.md)

Use this checklist before committing, tagging, or publishing a release.

## Documentation And Metadata

- [ ] Read `PROJECT_STATUS.md` and confirm that every publication gate is complete.
- [ ] Review the newest `docs/work_log.md` entry and confirm that all claimed checks have exact evidence.
- [ ] Confirm `docs/publication_audit_2026-10-08.md` blockers are resolved or explicitly superseded by a newer dated audit.
- [ ] Confirm the app, active pages, READMEs, and citation metadata match
  `envgeo_utils.APP_VERSION` and `envgeo_utils.APP_VERSION_DATE`.
- [ ] Update `README.md` and `README_Japanese.md` when user-facing behavior, page names, sources, limitations, or EnvGeo-Seawater relationship changes.
- [ ] Update `docs/testing_Japanese.md` when tests change.
- [ ] Update Home update history when the change should be visible in the app.
- [ ] Update `requirements.txt`, `requirements-dev.txt`, `.gitignore`, `LICENSE`, or `NOTICE.md` when dependencies, ignored artifacts, or licensing notes change.

## Checks

- [ ] Run pytest:

```bash
pytest -q
```

- [ ] Run syntax check without creating `.pyc` files:

```bash
python -c "import ast, pathlib; files=[pathlib.Path('home.py'), pathlib.Path('envgeo_utils.py'), *pathlib.Path('pages').glob('*.py'), *pathlib.Path('test').glob('*.py')]; [ast.parse(p.read_text(encoding='utf-8'), filename=str(p)) for p in files]; print(f'parsed {len(files)} files')"
```

- [ ] Confirm `test/test_asset_paths.py` passes from a temporary working
  directory for both coastline resolutions and both Home README views.
- [ ] Confirm both bundled coastline hashes still match
  `coastline/LICENSE_OR_SOURCE.md`, and keep its Natural Earth v4.1.0
  derivation evidence and provenance limitations in the release archive.
- [ ] Confirm `test/test_basic.py` enforces the shared USGS catalog and
  plate-boundary citations across all applicable bilingual pages.
- [ ] Confirm `test/test_offline_map.py` keeps Standard on OpenStreetMap and
  verifies the reviewed USGS imagery, Esri Ocean, and GSI runtime credits
  without making live tile requests.
- [ ] If the optional comparison is enabled in the release, confirm both
  Advanced upload controls accept only CSV, TSV, TXT, and XLSX, and
  `test/test_upload_formats.py` passes its normal and missing-column bilingual
  smoke cases.
- [ ] Review `docs/earthquake_validation.md`; confirm every added guard prevents
  a demonstrated failure and that normal USGS display behavior remains unchanged.
- [ ] Confirm `test/test_envgeo_utils.py` passes its network-free USGS loader
  cases for normal, empty, incomplete, malformed, HTTP-error, timeout, and
  connection-failure responses.
- [ ] Confirm USGS query construction includes required/selected parameters,
  omits unset optional values, and all four pages use the tested shared
  result-limit boundary.
- [ ] Confirm `test/test_page_coordinates.py` keeps longitude ±180° and
  latitude ±90° boundary points and excludes missing, non-numeric, and
  out-of-range USGS coordinates in all four pages.
- [ ] Confirm `test/test_spatial_geometry.py` passes four-page longitude,
  dateline, and local-km cases plus both Advanced section-geometry cases.
- [ ] Confirm `test/test_plate_boundary_fallback.py` passes normal, total and
  partial failure, malformed-response, and Japan-only fallback cases without
  live USGS plate-service access.
- [ ] Confirm `test/test_app_smoke.py` passes for bilingual Home and all four
  active visualizer pages with expected headings and paired fetch buttons.
- [ ] Confirm `test/test_repository_health.py` passes in the standalone public
  clone so tracked-file exclusions are checked in addition to release candidates.
- [ ] Confirm no JMA/NIED source catalog is bundled, and review
  `docs/jma_nied_data_responsibilities.md` for source, processing,
  acknowledgement, DOI, result-reporting, and redistribution obligations.

- [ ] For UI changes, run Streamlit locally and check the affected page manually.

## Files To Exclude

Do not commit:

- `.DS_Store`
- `__pycache__/`
- `.pytest_cache/`
- local secrets
- local development notes
- scratch or archive folders unless intentionally publishing them
- `old/` and `__ToDo__/` development archives
- irrelevant Seawater sample files or temporary coastline workbooks
- logo candidates and unused image assets

## Before Commit

- [ ] Check `git status --short`.
- [ ] Check `git diff --stat`.
- [ ] Make sure generated files are not staged.
- [ ] Commit with a short summary and a description of user-facing/documentation/test changes.
