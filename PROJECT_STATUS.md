# EnvGeo-Earthquake: Current Status and Handoff

[Japanese version](PROJECT_STATUS_Japanese.md)

Last updated: 2026-10-08 (Asia/Tokyo)

Read this file first when resuming work in a new chat or development session.
Chronological evidence belongs in both work-log language files.

## Current objectives

1. Publish EnvGeo-Earthquake as a stable standalone application with no runtime
   dependency on EnvGeo-Seawater.
2. Create a matching GitHub Release and Zenodo archive and obtain a version DOI.
3. Record future EnvGeo Core candidates without extracting a core or adding a
   shared dependency during the current phase.
4. Do not affect EnvGeo-Seawater v1.3.5 or its JOSS work.

## Current assessment

- Development version: `0.3.2` (2026-09-22)
- Status: **publication candidate, not yet ready for a Zenodo release**
- The available test environment now reports `176 passed, 0 skipped`; all 20
  active/test Python files also pass syntax parsing.
- The focused USGS failure-path audit reproduced two unhandled crashes:
  malformed JSON raised `JSONDecodeError`, and a non-list `features` member
  raised `AttributeError`. The shared loader now converts both to readable
  `RuntimeError` messages already handled by all four visualizer pages. Two
  deterministic tests were added. The shared loader is now also covered for
  normal, empty, incomplete, HTTP-error, timeout, and connection-failure
  responses without live service access. Query construction and the shared
  result-limit boundary are also deterministic. Bilingual optional-upload smoke
  paths, all four pages' missing/out-of-range coordinate guards, bilingual
  spatial geometry, plate fallback, page-startup AppTests, repository health,
  marker-size modes, and bilingual Plotly camera guidance are persistent; the
  suite reports `176 passed`.
- This working folder is not a Git repository. The separate public Git clone
  and remote have been identified; machine-specific details are kept in the
  local-only `LOCAL_WORKSPACE` files.
- On 2026-10-08, after explicit user approval, the reviewed public-release
  files were copied into the separate Git clone as a pre-Phase-5 checkpoint.
  Development-only directories, local workspace records, caches, and OS files
  were excluded. The clone remains on `main` based on `86b2d54`, with the
  synchronized changes intentionally uncommitted and unpushed for review in
  GitHub Desktop. Its own read-only test run reports `176 passed`.
- The unused inherited `load_isotope_data()` implementation and its Seawater
  Excel loading/merging logic were removed from the development utility on
  2026-10-08. Before and after the change, the full available suite reported
  `45 passed, 4 skipped`; all 11 active/test Python files parsed successfully.
- The trial Home logo was withdrawn after geographic-accuracy and page-balance
  review. Both Home pages again begin with the application title, and the
  current public scope contains no logo asset. Development candidates remain
  only in the excluded `__logo__/` folder for possible future icon/background
  review.
- Runtime version metadata is centralized in `envgeo_utils.APP_VERSION` and
  `APP_VERSION_DATE`. Both Home pages and all four active visualizer pages read
  the shared definition; a contract test rejects local string redefinitions.
- Bundled 50m/110m coastline CSVs and both Home README views now resolve from
  source-file roots. `test/test_asset_paths.py` changes to a temporary working
  directory and verifies real loading/rendering, so these assets do not depend
  on the process current working directory.
- Bilingual records now identify both bundled coastline CSVs as Natural Earth
  coastline v4.1.0 derivatives and record their SHA-256 hashes. This conclusion
  uses Seawater's retained source-workspace/intermediate-workbook audit plus
  byte identity of both Earthquake copies; original raw-download checksums and
  exact download dates were not retained. Map behavior and data files are unchanged.
- USGS citation text is now centralized in `envgeo_utils.py`: the FDSN-listed
  ANSS Comprehensive Catalog citation and the Bird (2003) / DeMets et al. (2010)
  references named by the USGS plate-service metadata are reused by bilingual
  Home, Simple, and Advanced pages. A contract test prevents local text drift.
- Online map sources and runtime credits are centralized in `envgeo_utils.py`.
  Standard remains Plotly's OpenStreetMap style (no CARTO basemap); satellite,
  bathymetry, and topographic layers now display reviewed USGS/USDA, Esri
  contributor, and linked GSI credits. A network-free contract test protects
  the URLs and attribution. Map selection and tile endpoints are unchanged.
- JMA/NIED responsibility metadata and a dedicated bilingual record now make
  the provider distinction explicit. JMA requires source and processing
  statements under its general website terms; NIED Hi-net prohibits source-data
  redistribution and requires registration/provider acknowledgement, its DOI,
  and result reporting. No JMA/NIED catalog is bundled or persistently stored.
- Bilingual Advanced catalog uploads now accept CSV, TSV, TXT, and `.xlsx`.
  Legacy `.xls` is no longer advertised because its separate reader dependency
  is not installed. Contracts align both controls with `requirements.txt` and
  verify an in-memory XLSX round-trip through `openpyxl`.
- The bilingual validation policy was narrowed to preserve current behavior.
  USGS values are trusted as source data; only crash prevention, readable
  failure handling, and basic user-upload checks are current requirements.
  Elaborate issue codes, duplicate-ID management, and validation dashboards
  are deferred unless a concrete defect justifies them.
- The Advanced-page JMA/NIED upload is classified as an optional retained
  feature, not a core USGS workflow or first-release/DOI gate. Direct bilingual
  checks of a normal CSV, missing required columns, and a broken XLSX all
  completed without an unhandled exception. No runtime code was changed and no
  upload-schema expansion is planned. The manuals now state that the app does
  not intentionally persist uploaded contents beyond the current session.
- All four visualizer pages now coerce their USGS plot coordinates to numeric,
  retain valid longitude ±180° and latitude ±90° boundary points, and exclude
  missing, non-numeric, or out-of-range coordinates before plotting. Eight
  tests execute each page's actual helper. JMA/NIED upload normalization and
  longitude/dateline representation were deliberately left unchanged.
- All four pages' actual longitude-wrapping, map-seam line, and local-km
  helpers now have direct deterministic tests. Both Advanced pages additionally
  test short-path dateline section unwrapping, section distance/offset,
  coincident endpoints, and closed corridor polygons. The 20 new cases required
  no runtime-code change.
- Both Advanced plate loaders now reject a non-list `features` member or a
  non-object feature as a readable layer error instead of crashing. Total
  failure uses the existing schematic lines only for the Japan preset; partial
  microplate failure retains the available USGS main-plate layer and now shows
  an accurate partial-data warning. Thirteen tests use no live network.
- `test/test_app_smoke.py` now runs Streamlit AppTest for bilingual Home and all
  four active visualizer pages as part of ordinary pytest. It protects
  exception-free initial rendering, the shared app title, language-specific
  headings, version display, and paired top/bottom fetch buttons. Interactive
  fetch/filter/download workflows remain separate later coverage.
- `test/test_repository_health.py` now builds a portable release-candidate view
  without deleting excluded local material. Eight tests protect the approved
  top-level structure, `.gitignore` rules, standalone-clone tracked exclusions,
  runtime references, common secret/private-key patterns, machine-specific
  absolute paths, symlinks, and Markdown links.
- Before Phase 5, all four visualizer pages gained a shared per-page marker-size
  mode: `Magnitude-linked` is the default and `Fixed size` is optional. The mode
  applies to the main 2D and 3D views and to both Advanced cross-section views.
  Size sliders now use a direct `0.2–10.0` multiplier with `1.0` as the standard
  size. A separate `Magnitude contrast` slider controls the M7:M4 marker-
  diameter ratio from `1` to `30`, defaulting to `20`.
  Separately, magnitude-linked mode uses an exponential visual curve: at scale
  `1.0`, an M7 marker diameter is approximately twenty times an M4 marker.
  This is a display emphasis, not a physical energy or rupture-area scale.
  Forty deterministic tests protect the bilingual defaults and adjustable ratio,
  both modes, three view profiles, and emphasized scale response.
- All four visualizer pages now show a concise bilingual caption immediately
  before the main 3D chart. It covers drag rotation, the Plotly rotate/pan/zoom/
  reset toolbar, and Shift/Control/Option (Alt)/Command mouse combinations for changing the
  viewpoint or center, with an explicit browser/OS variation note.

## Required publication gates

1. **Completed in the development folder:** inherited Seawater dataset loading
   and unpublished dataset references were removed from active Earthquake code.
   The public clone still awaits a user-directed file copy.
2. **Completed:** four inherited Seawater skip tests were replaced with
   deterministic USGS GeoJSON row/schema/numeric/time contract tests.
3. **Completed at the minimal scope:** USGS malformed-response guards have
   deterministic tests; the optional upload audit found no unhandled failure
   in the three representative cases and therefore added no speculative code.
4. Add network-independent GitHub Actions CI for Python 3.10 and 3.12.
5. **Completed:** bundle Natural Earth provenance and licensing for the coastline CSV files.
6. Add `CITATION.cff`, final release notes, and Zenodo metadata.
7. **Completed in development:** root-anchored ignore rules exclude `old/`,
   `data/`, `__ToDo__/`, `__logo__/`, `images/`, and `.devcontainer/`; generated
   files are covered separately. The local files were retained.
8. Record deployment smoke tests for bilingual Home, Simple, and Advanced
   pages, USGS retrieval, offline maps, uploads, and CSV export.

## Boundaries and shared-core policy

- Current changes belong only in `earthquake_map_v030`.
- Follow the EnvGeo-Seawater section-comment convention: major code sections
  use concise `English / 日本語` headings and bilingual purpose notes where
  useful. Apply it to new or edited sections without unrelated bulk rewrites.
- Do not copy Seawater quality flags, filters, or upload behavior directly into
  Earthquake.
- Core candidates: asset resolution, Streamlit compatibility UI, map modes,
  coastlines, longitude/dateline handling, local-km coordinates, and source
  metadata.
- Earthquake-specific: USGS query/GeoJSON, magnitude/depth/time semantics,
  plate boundaries, earthquake sections, JMA/NIED comparison, and
  preliminary-data warnings.
- See `docs/publication_audit_2026-10-08.md` for the detailed classification.

## Next recommended action

The public scope, Git-clone location, inherited Seawater loader removal,
unpublished-reference audit, and skip-test replacement are complete in the
development folder. Development-only samples and archives are also excluded
without deletion. A trial Home logo was evaluated and removed; no logo asset
is in the current public scope. Runtime version metadata, source-relative asset
loading, and the upload-format/dependency contract are now verified, completing
Phase 1 of the roadmap. The first Phase 2 item, defining Earthquake-specific
minimal validation policy, is also complete. The focused USGS failure audit
fixed only two reproduced malformed-response crashes. The optional JMA/NIED
upload audit required no code change, and Phase 2 is complete at the agreed
minimal scope. The first Phase 3 item is also complete: Natural Earth v4.1.0
provenance, public-domain terms, checksums, retained derivation evidence, and
record limitations are synchronized across the bundled records, NOTICE,
bilingual READMEs, Home source notes, and Advanced source notes. USGS catalog
and plate-boundary citations are also centralized and synchronized. The online
map attribution audit is complete without changing map selection behavior; it
also corrected the documentation-only CARTO mismatch. JMA/NIED use and
redistribution responsibilities are now recorded separately, completing Phase 3.
Phase 4 has begun: deterministic USGS response/failure coverage, query
construction, and the four-page result-limit warning boundary are tested. The
retained optional JMA/NIED comparison now has minimal bilingual smoke tests for
one normal CSV and one missing-required-columns CSV, without schema expansion.
Missing/non-numeric and out-of-range USGS plot coordinates are now tested
across all four pages. Longitude wrapping, dateline handling, local-km
conversion, and section geometry are also tested without a runtime-code change.
Plate-boundary success, total/partial failure, malformed response, and the
Japan-only fallback are now tested. Persistent startup AppTests cover bilingual
Home and all four active visualizer pages. Repository-health checks complete
Phase 4. Next, begin Phase 5 with network-independent GitHub Actions CI for
Python 3.10 and 3.12.
Do not copy files into the public clone without explicit user instruction; the user handles
commit and push in GitHub Desktop.

## Record-update rules

- Every material session: `docs/work_log.md` and `docs/work_log_English.md`
- State/blockers/next action changed: both `PROJECT_STATUS` language files
- Priorities changed: `TODO.md` and `TODO_Japanese.md`
- User workflow changed: both manuals, READMEs, and Home histories
- Release decision: both `docs/release_checklist` language files
- Procedure: both `docs/development_workflow` language files
