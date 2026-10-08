# EnvGeo-Earthquake Work Log

[Japanese version](work_log.md)

## Operating policy

- Perform primary work in `earthquake_map_v030`.
- Copy only reviewed and tested changes into the public Git clone.
- Keep READMEs, Home history, manuals, TODOs, and docs aligned with changes.
- Do not copy generated caches or OS files into the public repository.
- Record Core candidates, but do not force Earthquake-specific behavior into a shared layer.

## 2026-10-08 — Synchronized the pre-Phase-5 checkpoint to the public Git clone

- Purpose: place the verified standalone Earthquake state in the public clone
  as a commit-ready checkpoint before Phase 5.
- Following explicit user authorization, synchronized the reviewed public files
  from the development folder into the clone.
- Excluded `.git`, `.DS_Store`, caches, `old/`, `data/`, `__ToDo__/`,
  `__logo__/`, `images/`, `.devcontainer/`, and both local workspace records.
  No delete synchronization was performed.
- Verification in the clone:
  `PYTHONDONTWRITEBYTECODE=1 pytest -q -p no:cacheprovider` reported
  `176 passed in 2.69s`, 0 skipped. `git diff --check` reported only two-space
  Markdown hard line breaks in README documents, not code errors.
- The clone remains on `main` tracking `origin/main`; changes are intentionally
  uncommitted and unpushed for user review and commit through GitHub Desktop.
- Explicitly unchanged: EnvGeo-Seawater, EnvGeo Core, remote, tags, and releases.
- Next action: review, commit, and push in GitHub Desktop, then begin Phase 5.

## 2026-10-08 — Added bilingual Plotly 3D camera guidance

- Purpose: follow the concise EnvGeo-Seawater interaction guidance so users can
  discover Plotly camera controls without expanding the page layout.
- Added a caption immediately before the main 3D hypocenter chart in all four
  English/Japanese Simple and Advanced pages.
- The caption explains drag rotation, the upper-right Plotly toolbar for rotate,
  pan, zoom, and camera reset, and the optional `Shift`, `Control`, `Option`
  (`Alt`), or `Command`
  plus mouse-drag combinations that can move the viewpoint or center.
- Following a macOS device check where `Option`, rather than `Shift`, provided
  the useful gesture, added `Option` (`Alt`) to the UI captions, manuals, test,
  and related records.
- Refined the Japanese wording from a tentative statement that behavior "may
  change" to the direct instruction that users "can change" how the viewpoint
  or center moves; retained the browser/OS variation note.
- It explicitly notes that modifier-key behavior varies by browser and operating
  system rather than promising one platform-specific gesture.
- Expanded the bilingual Simple and Advanced manuals with the same guidance and
  synchronized README, Home history, testing, TODO, audit, and handoff records.
- Added `test/test_plotly_camera_guidance.py` with four bilingual source-order
  contracts ensuring the guidance contains `Option` and the modifier-key list and appears
  before the main 3D chart.
- Verification: targeted test `4 passed in 0.01s`; final full suite
  `176 passed in 2.87s`, 0 skipped; all 20 active/test Python files parse.
- Explicitly unchanged: chart calculation and camera defaults, app version,
  dependencies, public Git clone, EnvGeo-Seawater, and EnvGeo Core.

## 2026-10-08 — Added marker-size mode and emphasized scale before Phase 5

- Purpose: respond to the pre-Phase 5 display review without expanding the
  scientific or data-source scope. Preserve the existing USGS-centered workflow
  while making earthquake marker sizing explicit and easier to see.
- Added `Marker size mode` to all four active visualizer pages. The first and
  default option is `Magnitude-linked`; `Fixed size` is the optional second
  choice. Japanese pages use matching Japanese labels.
- Applied the one selected mode consistently to the main 3D hypocenter view,
  2D distribution map, and both Advanced cross-section location/section views.
- Replaced separate inline formulas with an Earthquake-local
  `earthquake_marker_sizes()` helper in each page. This deliberate small
  duplication keeps Earthquake standalone and avoids premature EnvGeo Core
  extraction during the publication-stabilization phase.
- Set all marker scale defaults to `1.0`. The first two trial responses
  (`scale ** 1.5`, then `scale ** 2.0`) were still judged too subtle. The final
  trial used a transparent direct multiplier over `0.2–20.0`; user review then
  selected `10.0` as a sufficient maximum, so the final range is `0.2–10.0`.
  Expanded the
  3D/2D/section upper bounds to 180/450/280 pixels so this trial is not clipped
  prematurely; lower bounds still prevent invisibility.
- Magnitude-linked profiles were strengthened for 3D, 2D, and cross-section
  rendering; after clarifying that the requested amplification concerned the
  difference between magnitudes rather than the overall slider, replaced the
  nearly linear curve with `reference_size * 20 ** ((M - 4) / 3)`. At overall
  scale `1.0`, this makes the M7 marker diameter approximately twenty times M4
  in all three view profiles. This is explicitly documented as visual emphasis,
  not a physical energy or rupture-area scale. Fixed mode remains constant.
  Added a separate `Magnitude contrast (M7/M4 diameter ratio)` slider from 1 to
  30, default 20; the formula now uses the selected ratio and the control is
  disabled in fixed-size mode.
  Missing/non-numeric/negative magnitude values remain safe and are treated as
  zero for marker sizing.
- Added `test/test_marker_size_modes.py` with 40 deterministic cases across all
  four bilingual pages and all three view profiles. The tests protect monotonic
  magnitude sizing including default 20:1 and adjustable 5:1 M7:M4 diameter
  ratios, constant fixed sizing, direct overall scale response, slider presence,
  and magnitude-linked default labels.
- The first targeted test run found that the fixed branch returned a scalar and
  could not be clipped as a Series. It was corrected to return a Series aligned
  to the input index; the rerun passed all 48 marker/coordinate tests.
- Updated bilingual Simple/Advanced manuals, TODOs, Home history, testing guide,
  and handoff status. Phase 5 remains unstarted; its next item is still the
  network-independent Python 3.10/3.12 GitHub Actions CI.
- Verification:
  - `python -m py_compile` passed for all four edited page files;
  - after the final amplification increase, targeted
    `pytest -q test/test_marker_size_modes.py`: `40 passed in 0.67s`;
  - final full `pytest -q`: `172 passed in 2.81s`, 0 skipped.
- Explicitly unchanged: app version, data acquisition/filter logic, provider
  scope, dependencies, public Git clone, EnvGeo-Seawater, and EnvGeo Core.

## 2026-10-08 — Completed Phase 4 repository-health checks

- Purpose: complete the final Phase 4 item by converting the bilingual public-
  release scope into portable automated checks, without deleting development
  material from the working folder.
- Added `test/test_repository_health.py` with eight checks:
  - release candidates use only approved root files/directories;
  - `.gitignore` covers development-only directories, local workspace records,
    secrets files, generated files, caches, logs, and build output;
  - when the test runs in a standalone Git clone, tracked files contain no
    excluded/generated path;
  - active runtime Python has no local dependency on excluded directories;
  - public text has no common real-value token/private-key/credential patterns;
  - public text has no username-bearing macOS, Linux, or Windows absolute path;
  - release candidates contain no symlinks;
  - every local Markdown link resolves.
- The first targeted run exposed one test false positive: provider URLs such as
  JMA's official `data/` path were mistaken for local `data/` dependencies. The
  check now removes HTTP(S) URLs before inspecting local runtime references;
  this keeps the dependency check while allowing legitimate provider URLs.
- The candidate view deliberately ignores excluded/generated local files rather
  than removing them. The tracked-file branch activates automatically after the
  test is copied into the standalone public clone.
- Rechecked the user's marker-size question. All four pages already calculate
  main 2D and 3D marker sizes from magnitude; both Advanced pages also calculate
  cross-section size from magnitude. Existing sliders apply an overall scale.
  There is no fixed-size/magnitude-linked toggle. Bilingual Simple and Advanced
  manuals now state this explicitly; no feature or runtime code was changed.
- Synchronized roadmap, TODOs, testing guides, test notes, release checklists,
  publication audit, bilingual Home histories, and handoff status. Phase 4 is
  complete.
- Verification:
  - Targeted `/opt/anaconda3/bin/pytest -q test/test_repository_health.py`:
    `8 passed in 0.10s`.
  - Final `/opt/anaconda3/bin/pytest -q`: `132 passed in 2.34s`, 0 skipped.
  - `ast.parse`: all 18 active/test Python files passed.
  - Markdown: 55 files, 108 local links/images, 0 missing.
  - Public clone remained clean: `## main...origin/main`.
- Explicitly unchanged: excluded local files, marker-size runtime behavior,
  dependencies, app version, public Git clone, EnvGeo-Seawater, and EnvGeo Core
  extraction.
- Next single item: begin Phase 5 with network-independent GitHub Actions CI
  for Python 3.10 and 3.12.

## 2026-10-08 — Added persistent bilingual page-startup AppTests

- Purpose: complete the next Phase 4 item by moving the repeated manual
  Streamlit startup command into the ordinary pytest suite.
- Inspected the initial AppTest element tree for bilingual Home, Simple, and
  Advanced pages. All six pages expose a stable common title and language-
  specific primary heading; all four visualizer pages expose the established
  top and bottom fetch buttons.
- Added `test/test_app_smoke.py` with six parameterized cases:
  - English and Japanese Home render `EnvGeo-Earthquake` plus a representative
    language-specific section heading and no fetch button;
  - English Simple/Advanced render their shared-version headings and exactly
    `Fetch / update` plus `Fetch / update!`;
  - Japanese Simple/Advanced render their shared-version headings and exactly
    `取得 / 更新` plus `取得 / 更新！`;
  - every page returns zero Streamlit exceptions within a 60-second limit.
- The test imports `APP_VERSION` from `envgeo_utils`, so it checks the displayed
  shared version contract without duplicating a release string.
- Scope boundary: this is deterministic initial-render coverage and triggers no
  USGS request. Region/hotspot interactions, fetch/filter flows, empty-result
  messages, downloads, session state, and visual appearance remain separate
  later automated/manual coverage.
- No application runtime code, UI text, dependency, or page behavior changed.
- Synchronized roadmap, TODOs/testing policy, testing guides, test notes,
  release checklists, publication audit, bilingual Home histories, and handoff
  status.
- Verification:
  - Targeted `/opt/anaconda3/bin/pytest -q test/test_app_smoke.py`:
    `6 passed in 1.04s`.
  - Final `/opt/anaconda3/bin/pytest -q`: `124 passed in 2.42s`, 0 skipped.
  - `ast.parse`: all 17 active/test Python files passed.
  - Markdown: 55 files, 108 local links/images, 0 missing.
  - Public clone remained clean: `## main...origin/main`.
- Explicitly unchanged: application runtime code, USGS/network behavior, UI,
  dependencies, app version, public Git clone, EnvGeo-Seawater, and EnvGeo Core
  extraction.
- Next single item: add repository-health checks for release contents, secrets,
  and absolute local paths.

## 2026-10-08 — Tested and hardened plate-boundary fallback paths

- Purpose: complete the next Phase 4 item by verifying both Advanced pages'
  plate-service success, failure, and Japan-only fallback behavior without live
  network access.
- Audited the duplicated English/Japanese plate loaders. The existing behavior
  already used six clearly labeled schematic Japan-area lines after total
  service failure and did not apply those lines to other region presets.
- Reproduced two concrete publication-quality defects:
  - an HTTP-success response whose `features` member was not a list, or whose
    list contained a non-object feature, could raise during feature mutation;
  - when the main plate layer succeeded but the optional microplate layer
    failed, the UI incorrectly said that Japan fallback lines were shown.
- Added the same minimal bilingual guard before feature mutation. Malformed
  structures now become readable per-layer errors and enter the existing safe
  fallback path.
- Split the warning branch by returned source. A true Japan fallback retains
  the existing fallback warning; partial USGS success now says that available
  USGS layers are shown. Normal data, fallback geometry, controls, and map
  rendering were not changed.
- Added `test/test_plate_boundary_fallback.py`, which AST-extracts and executes
  the actual helper definitions from both Advanced pages. Thirteen network-free
  cases verify:
  - successful main-plate and microplate requests, layer labels, and ArcGIS
    GeoJSON query parameters;
  - total connection failure uses labeled schematic data for Japan only;
  - a non-Japan total failure returns an empty boundary dataframe;
  - non-list `features` and non-object features use the Japan fallback safely;
  - a microplate-only HTTP 503 retains valid USGS main-plate data and source;
  - bilingual UI code distinguishes partial USGS data from a true fallback.
- Synchronized roadmap, TODOs, testing guides, test notes, release checklists,
  publication audit, bilingual Home histories, and handoff status.
- Verification:
  - Targeted `/opt/anaconda3/bin/pytest -q test/test_plate_boundary_fallback.py`:
    `13 passed in 0.47s`.
  - Final `/opt/anaconda3/bin/pytest -q`: `118 passed in 2.12s`, 0 skipped.
  - `ast.parse`: all 16 active/test Python files passed.
  - Streamlit `AppTest`: zero exceptions across bilingual Home, Simple, and
    Advanced pages (six files).
  - Markdown: 55 files, 108 local links/images, 0 missing.
  - Public clone remained clean: `## main...origin/main`.
- Explicitly unchanged: successful plate data and map geometry, fallback line
  definitions, controls, dependencies, app version, public Git clone,
  EnvGeo-Seawater, and EnvGeo Core extraction.
- Next single item: add persistent AppTest coverage for bilingual Home and all
  four active visualizer pages.

## 2026-10-08 — Tested longitude, dateline, local-km, and section geometry

- Purpose: complete the next Phase 4 spatial-geometry item by recording the
  current bilingual page behavior without changing working runtime code.
- Compared the actual helpers in all four English/Japanese Simple and Advanced
  pages. Their longitude wrapping, map-seam line handling, and equirectangular
  local-km conversions are identical. The two Advanced pages also have
  identical cross-section unwrapping, projection, and corridor helpers.
- No reproducible defect was found, so no page or utility implementation was
  edited. Added only `test/test_spatial_geometry.py`, which AST-extracts the
  actual page functions instead of testing a re-created implementation.
- Added 12 four-page cases that verify:
  - equivalent longitude values occupy the selected 360-degree branch;
  - a dateline-crossing line receives a `NaN` break at the Greenwich-centered
    seam but remains continuous as 170, 179, 181, 190 on a Pacific branch;
  - 179°E and 179°W become adjacent local coordinates of approximately
    −111.320 km and +111.320 km around a 180° central meridian.
- Added eight bilingual Advanced cases that verify:
  - 170°E→170°W and its reverse follow the 20-degree short path;
  - along-section distance, signed cross-section offset, and an approximately
    2,226.4 km equatorial section length;
  - coincident endpoints safely return an empty section and zero length;
  - the five-point corridor polygon closes without a 360-degree seam jump.
- Synchronized roadmap, TODOs, testing guides, test notes, release checklists,
  publication audit, bilingual Home histories, and handoff status.
- Verification:
  - Targeted `/opt/anaconda3/bin/pytest -q test/test_spatial_geometry.py`:
    `20 passed in 0.77s`.
  - Final `/opt/anaconda3/bin/pytest -q`: `105 passed in 2.06s`, 0 skipped.
  - `ast.parse`: all 15 active/test Python files passed.
  - Streamlit `AppTest`: zero exceptions across bilingual Home, Simple, and
    Advanced pages (six files).
  - Markdown: 55 files, 108 local links/images, 0 missing.
  - Public clone remained clean: `## main...origin/main`.
- Explicitly unchanged: runtime page/utility code, UI, spatial formulas,
  dependencies, app version, public Git clone, EnvGeo-Seawater, and EnvGeo Core
  extraction. These helpers remain recorded only as future Core candidates.
- Next single item: test the Advanced-page plate-boundary network fallback.

## 2026-10-08 — Guarded and tested invalid USGS plot coordinates

- Purpose: complete the next Phase 4 item by making missing and out-of-range
  earthquake-coordinate behavior deterministic while preserving every normal
  USGS display path.
- Audited `prepare_plot_dataframe()` in all four English/Japanese Simple and
  Advanced pages. Missing coordinates were already dropped, but numeric values
  beyond GeoJSON longitude/latitude bounds remained eligible for plotting.
- Added the same minimal guard to each page's Earthquake-specific plot
  preparation:
  - coerce longitude, latitude, and depth to numeric values;
  - remove rows missing a required plot coordinate;
  - retain inclusive longitude `[-180, 180]` and latitude `[-90, 90]`;
  - exclude non-numeric and out-of-range longitude/latitude.
- Added bilingual comments and purpose notes to the edited page functions,
  following the established Seawater-style English/Japanese code convention.
- Added `test/test_page_coordinates.py`. It AST-extracts and executes the
  actual helper from each of the four pages rather than testing a re-created
  implementation. Eight cases verify valid center/boundary rows, missing and
  non-numeric values, all four range violations, marker sizes, and a safe empty
  result when every row is invalid.
- Scope boundary: optional JMA/NIED upload normalization, accepted aliases and
  schemas, longitude wrapping/dateline behavior, query parameters, UI, and
  dependencies were not changed. No general validation framework was added.
- Synchronized roadmap, TODOs, minimal-validation policy, testing guides, test
  notes, release checklists, publication audit, bilingual Home histories, and
  handoff status.
- Verification:
  - Targeted `/opt/anaconda3/bin/pytest -q test/test_page_coordinates.py`:
    `8 passed in 0.78s`.
  - Final `/opt/anaconda3/bin/pytest -q`: `85 passed in 2.45s`, 0 skipped.
  - `ast.parse`: all 14 active/test Python files passed.
  - Streamlit `AppTest`: zero exceptions across bilingual Home, Simple, and
    Advanced pages (six files).
  - Markdown: 55 files, 108 local links/images, 0 missing.
  - Public clone remained clean: `## main...origin/main`.
- Explicitly unchanged: valid USGS display results, optional-upload behavior,
  app version, public Git clone, EnvGeo-Seawater, and EnvGeo Core extraction.
- Next single item: test longitude wrapping, dateline handling, local-km
  conversion, and section geometry without changing page behavior.

## 2026-10-08 — Added minimal smoke tests for optional JMA/NIED uploads

- Purpose: complete the next Phase 4 item with the smallest regression coverage
  needed for the retained optional JMA/NIED comparison, without expanding its
  role in the initial release.
- Audited the duplicated upload helpers in both bilingual Advanced pages:
  `normalize_column_name()`, `find_catalog_column()`,
  `read_uploaded_catalog()`, and `normalize_external_catalog()`.
- Added tests that parse each page with Python AST, extract those actual helper
  definitions, and execute them directly. The tests therefore exercise the
  current page implementation rather than a separately re-created parser.
- Added one normal CSV case for each page. It verifies normalized longitude,
  latitude, depth, magnitude, catalog, place, and UTC time, with no warning or
  error.
- Added one missing-required-columns CSV case for each page. It verifies a safe
  empty result and one readable warning, with no uncaught error.
- Synchronized the roadmap, TODOs, testing guides, test notes, release
  checklists, publication audit, bilingual Home histories, and handoff status.
- Verification:
  - Targeted `/opt/anaconda3/bin/pytest -q test/test_upload_formats.py`:
    `7 passed in 0.49s`.
  - Final `/opt/anaconda3/bin/pytest -q`: `77 passed in 1.58s`, 0 skipped.
  - `ast.parse`: all 13 active/test Python files passed.
  - Streamlit `AppTest`: zero exceptions across bilingual Home, Simple, and
    Advanced pages (six files).
  - Markdown: 55 files, 108 local links/images, 0 missing.
  - Public clone remained clean: `## main...origin/main`.
- Explicitly unchanged: runtime code, accepted aliases and schemas, upload
  formats, comparison UI, dependencies, app version, public Git clone,
  EnvGeo-Seawater, and any EnvGeo Core extraction.
- Next single item: add deterministic coverage for `NaN` and out-of-range
  earthquake coordinates while preserving current visible behavior.

## 2026-10-08 — Tested USGS query construction and result-limit warnings

- Purpose: complete the second Phase 4 item by making the API request contract
  and the warning boundary deterministic without changing user-facing behavior.
- Audited all four visualizer pages. Each passed the same date/time, magnitude,
  depth, latitude, longitude, ordering, and limit fields to the shared loader,
  and each displayed its existing warning when `len(df_eq) >= query["limit"]`.
- Extracted two small Earthquake-local pure helpers in the bilingual USGS
  loading section of `envgeo_utils.py`:
  - `build_usgs_earthquake_query_url()` constructs the FDSN query URL;
  - `usgs_result_limit_reached()` owns the truncation-warning boundary.
- Updated all four pages to call the shared limit helper. The warning text,
  placement, and timing remain unchanged. No EnvGeo Core or Seawater dependency
  was introduced.
- Added deterministic tests that verify:
  - endpoint, `format=geojson`, `eventtype=earthquake`, ISO datetimes,
    `orderby`, integer limit, and all eight optional magnitude/depth/coordinate
    filters;
  - `None` and `NaN` optional filters are omitted;
  - the warning condition is false below the requested limit and true at or
    above it;
  - every active bilingual Simple/Advanced page uses the shared condition and
    retains an `st.caption()` warning path.
- Synchronized roadmap, TODOs, testing notes, release checklists, publication
  audit, Home histories, and handoff status. Manuals were unchanged because
  query and warning behavior did not change.
- Verification:
  - Targeted `/opt/anaconda3/bin/pytest -q test/test_envgeo_utils.py`:
    `26 passed in 0.60s`.
  - Final `/opt/anaconda3/bin/pytest -q`: `73 passed in 1.43s`, 0 skipped.
  - `ast.parse`: all 13 active/test Python files passed.
  - Streamlit `AppTest`: zero exceptions across bilingual Home, Simple, and
    Advanced pages (six files).
  - Markdown: 55 files, 108 local links/images, 0 missing.
  - Public clone remained clean: `## main...origin/main`.
- Explicitly unchanged: API parameter semantics, warning text/timing, UI
  controls, dependencies, app version, public Git clone, EnvGeo-Seawater, and
  any Core extraction.
- Next single item: add the minimal automated smoke coverage for the retained
  optional JMA/NIED comparison—one normal upload and one unreadable or
  missing-column case, without expanding schemas.

## 2026-10-08 — Completed deterministic USGS loader failure coverage

- Purpose: complete the first Phase 4 test item for normal, empty, incomplete,
  malformed, HTTP-error, timeout, and connection-failure USGS responses without
  making live network requests.
- Audited the shared `load_usgs_earthquake_data()` path used by all four active
  visualizer pages. It already converted `HTTPError`, `URLError`, `TimeoutError`,
  malformed JSON, and an invalid GeoJSON `features` member into readable
  `RuntimeError` messages caught by every page.
- No runtime code change was needed. Added only missing regression evidence:
  - parameterized loader tests for a normal FeatureCollection, an empty result,
    and a feature with missing properties/geometry;
  - parameterized transport tests for HTTP 503, DNS/connection failure, and
    timeout;
  - retained the existing malformed-JSON and non-list-`features` tests.
- The successful cases also verify that the loader returns the expected row
  count/event ID and attaches its query URL to dataframe metadata. This does not
  yet claim full query-parameter coverage; that remains the next roadmap item.
- Synchronized the roadmap, TODOs, testing guides, test notes, release
  checklists, publication audit, Home histories, and handoff status. User
  manuals were unchanged because application behavior did not change.
- Verification:
  - Targeted `/opt/anaconda3/bin/pytest -q test/test_envgeo_utils.py`:
    `20 passed in 0.61s`.
  - Final `/opt/anaconda3/bin/pytest -q`: `67 passed in 1.46s`, 0 skipped.
  - `ast.parse`: all 13 active/test Python files passed.
  - Streamlit `AppTest`: zero exceptions across bilingual Home, Simple, and
    Advanced pages (six files).
  - Markdown: 55 files, 108 local links/images, 0 missing.
  - Public clone remained clean: `## main...origin/main`.
- Explicitly unchanged: runtime loader/error messages, page UI, query controls,
  dependencies, app version, public Git clone, EnvGeo-Seawater, and Core.
- Next single item: test USGS query construction and the result-limit warning.

## 2026-10-08 — Recorded JMA/NIED use and redistribution responsibilities

- Purpose: complete the last Phase 3 provenance/licensing item while preserving
  the optional comparison exactly as implemented.
- Used EnvGeo-Seawater's redistribution-audit principle as a read-only
  reference: public availability or citation alone is not treated as evidence
  of permission to redistribute a dataset. No Seawater file was changed.
- Rechecked official provider material on 2026-10-08:
  - JMA website terms place content under Public Data License 1.0 unless a
    specific notice applies. They require source/page credit, identification of
    editing or processing, avoidance of false government authorship, and user
    review of third-party rights.
  - JMA's bulletin usage page records that its unified analysis incorporates
    observations from NIED, universities, research institutes, local
    authorities, and other contributors.
  - NIED Hi-net guidance prohibits redistribution of downloaded data and
    hypocenter information, requires use through the provider/registration
    route, acknowledgement of all providers, citation of DOI
    `10.17598/NIED.0003`, and reporting of resulting work. Other providers'
    data distributed through Hi-net remain subject to their rules.
- Added dedicated bilingual records,
  `docs/jma_nied_data_responsibilities.md` and its Japanese counterpart. They
  state that upload acceptance or CSV/XLSX conversion does not grant reuse
  rights and that the record is project guidance rather than legal advice.
- Centralized official JMA/NIED links, the NIED citation, and the review date in
  the Earthquake-local `envgeo_utils.py`, with bilingual section comments.
- Synchronized bilingual Home source notes/histories, READMEs, the comparison
  manuals, NOTICE, docs index, audit, roadmap, TODOs, testing records, release
  checklists, and handoff status.
- Release decision: no JMA/NIED catalog is bundled in the repository, package,
  GitHub Release, or planned Zenodo archive. The app does not automatically
  acquire, authenticate, rights-check, or persist the uploaded source file.
  The optional comparison remains outside the initial release/DOI gate.
- Added one deterministic contract test for official-domain references, the
  NIED DOI, bilingual Home use, and both responsibility records.
- Verification:
  - Targeted `/opt/anaconda3/bin/pytest -q test/test_basic.py`: `5 passed`.
  - Full `/opt/anaconda3/bin/pytest -q`: `61 passed in 1.48s`, 0 skipped.
  - `ast.parse`: all 13 active/test Python files passed.
  - Streamlit `AppTest`: zero exceptions across bilingual Home, Simple, and
    Advanced pages (six files).
  - Markdown: 55 files, 108 local links/images, 0 missing.
  - Public clone remained clean: `## main...origin/main`.
- Explicitly unchanged: comparison parsing/schema/UI, accepted upload formats,
  dependencies, app version, public Git clone, EnvGeo-Seawater, and Core.
- Phase 3 provenance/licensing items are complete. Next single item: complete
  deterministic USGS normal, empty, incomplete, malformed, HTTP-error, timeout,
  and connection-failure coverage.

## 2026-10-08 — Rechecked online-map attribution without changing map behavior

- Purpose: complete the next Phase 3 item by verifying the active Standard,
  Satellite, Bathymetry, and GSI background sources against provider guidance.
- Read EnvGeo-Seawater's map implementation and offline-operation records
  read-only as a structural reference. No Seawater source, data, or document
  was edited, and no dependency was added.
- Found and corrected a documentation mismatch: active Earthquake code has
  used Plotly's `open-street-map` style since 2026-09-20, but bilingual Home,
  README, and NOTICE still called it a CARTO basemap. CARTO tiles are not
  configured. The OpenStreetMap copyright and tile-usage links are now shown,
  including the no-bulk-download/prefetch caution.
- Centralized Earthquake-local map URLs, provider links, runtime credits, and
  the verification date in `envgeo_utils.py`, with bilingual section comments.
  Map selection and tile endpoints were not changed.
- Updated runtime credits from provider material:
  - USGS imagery: `USDA, USGS The National Map: Orthoimagery`, matching the
    service metadata rather than the previous generic `USGS` label.
  - Esri World Ocean Base: current Esri Ocean Basemap contributor wording;
    bilingual documents also state that the background is not for navigation
    or safety at sea.
  - GSI standard tiles: linked `国土地理院` credit; documentation notes that
    static publication/redistribution requires a current terms/procedure check.
- Synchronized NOTICE, bilingual READMEs, Home source notes and histories,
  export/use-note manuals, audit, roadmap, TODOs, testing notes, release
  checklists, and handoff status.
- Added one network-free test that verifies Standard remains OpenStreetMap and
  all three explicit raster layers retain the centralized URL/credit pairs.
- Verification:
  - Targeted `/opt/anaconda3/bin/pytest -q test/test_offline_map.py`:
    `32 passed in 1.19s`.
  - Full `/opt/anaconda3/bin/pytest -q`: `60 passed in 1.75s`, 0 skipped.
  - `ast.parse`: all 13 active/test Python files passed.
  - Streamlit `AppTest`: zero exceptions across bilingual Home, Simple, and
    Advanced pages (six files).
  - Markdown: 53 files, 102 local links/images, 0 missing.
  - Active/public documentation has no `carto.com` link; remaining CARTO text
    only says that CARTO is not configured or records the correction.
  - Public clone remained clean: `## main...origin/main`.
- Explicitly unchanged: map choices and tile endpoints, earthquake processing,
  dependencies, app version, public Git clone, EnvGeo-Seawater, and any Core
  extraction.
- Next single item: record JMA/NIED use and redistribution responsibilities.

## 2026-10-08 — Centralized USGS catalog and plate-boundary citations

- Purpose: complete the second Phase 3 item by aligning USGS catalog and
  plate-boundary citation text across bilingual Home, Simple, Advanced,
  READMEs, and manuals and preventing future page-level drift.
- Authoritative evidence rechecked on 2026-10-08:
  - The USGS FDSN Event Web Service documents its FDSN Event implementation,
    GeoJSON queries, and the 20,000-event service limit.
  - The FDSN USGS data-center record gives the formal ANSS Comprehensive
    Catalog citation beginning `U.S. Geological Survey. (2017)...` and DOI
    `10.5066/F7MS3QZH`.
  - USGS Tectonic Plate Boundaries ArcGIS REST metadata cites the USGS
    Seismicity of the Earth Map Series, Bird (2003), and DeMets et al. (2010),
    and identifies layer 0 as Microplates and layer 1 as Plates.
- Implementation:
  - Added an `Earthquake sources and citations / 地震データの出典と引用`
    section to `envgeo_utils.py`, centralizing API/service URLs and the catalog,
    Bird, and DeMets citation text.
  - Both Home pages and all four visualizer pages now reuse the catalog citation.
    Simple pages also show the formal citation and FDSN Event service link.
  - Both Home and Advanced language pairs reuse the Map Series URL and full
    Bird/DeMets citations. Existing catalog queries, plate retrieval, fallback,
    and rendering logic are unchanged.
  - Synchronized bilingual READMEs, export/notes manuals, Home histories,
    publication audit, roadmap, TODOs, release checklists, testing guides,
    test READMEs, and PROJECT_STATUS files.
  - Added one contract test in `test/test_basic.py` covering the shared catalog
    reference in all six pages and Map Series/Bird/DeMets references in the four
    applicable Home/Advanced pages.
- Verification:
  - Targeted `/opt/anaconda3/bin/pytest -q test/test_basic.py`: `4 passed`.
  - Final `/opt/anaconda3/bin/pytest -q`: `59 passed in 1.56s`, 0 skipped.
  - `ast.parse`: all 13 active/test Python files passed.
  - Streamlit `AppTest`: zero exceptions across the six bilingual Home, Simple,
    and Advanced files.
  - Markdown: 50 files, 100 local links/images, zero missing.
  - The three DOI literals occur only in `envgeo_utils.py` within active UI code;
    no page-local copies remain.
  - Public clone remained clean: `## main...origin/main`.
- Explicitly unchanged: USGS query parameters, normalization and caching;
  plate-boundary retrieval, fallback, and map rendering; dependencies; app
  version; EnvGeo-Seawater source/data/docs; and the public Git clone.
- Next single item: recheck CARTO/OpenStreetMap/USGS imagery/Esri/GSI attribution.

## 2026-10-08 — Established Natural Earth coastline provenance from Seawater evidence

- Purpose: complete the first Phase 3 publication gate by preserving source,
  terms, derivation evidence, and fingerprints for the bundled coastline CSVs
  inside Earthquake without changing map behavior or coastline data.
- Read-only Seawater evidence reviewed:
  - `docs/geospatial_assets*` and `docs/provenance_inventory*` identify both the
    50m and 110m CSVs as derived from Natural Earth coastline v4.1.0.
  - Source archives and coordinate workbooks were saved on 2025-01-24. The
    2026-10-03 audit found matching row counts and NaN separators and a maximum
    absolute numeric difference of approximately `1.42e-14` from the current CSVs.
  - Original raw-download hashes, exact download dates, and a standalone
    conversion script were not retained; bit-for-bit reconstruction of the
    historical raw archives is therefore not claimed.
  - Seawater's separately documented 50m land-polygon shapefile is a different
    static-map asset and is not part of Earthquake's two coastline-line CSVs.
- Earthquake records added and synchronized:
  - Added bilingual `coastline/LICENSE_OR_SOURCE*` records covering Natural
    Earth's public-domain terms, v4.1.0 evidence, retained intermediates,
    current hashes, known limitations, and future replacement requirements.
  - Synchronized NOTICE, bilingual READMEs, docs indexes, manuals, Home source
    and history text, bilingual Advanced source notes, publication audit,
    roadmap, TODOs, release checklists, and PROJECT_STATUS files.
  - 50m: 61,844 data rows / 1,428 separator rows; SHA-256
    `c3d7bee4fb696b011fa34bb13bed0c335c5250eeaf37d8739d77d29a27fe385c`.
    110m: 5,261 data rows / 133 separator rows; SHA-256
    `a31df3aeee9dc4195af35a31b0605fdb572c7c7dd7cde17f773c9438f5ec7f3f`.
- Verification:
  - Both CSVs are byte-identical to their Seawater counterparts.
  - `/opt/anaconda3/bin/pytest -q`: `58 passed in 1.93s`, 0 skipped.
  - `ast.parse`: all 13 active/test Python files passed.
  - Streamlit `AppTest`: zero exceptions across the six bilingual Home, Simple,
    and Advanced files.
  - Markdown: 50 files, 100 local links/images, zero missing. The first checker
    one-liner had a `SyntaxError`; it was corrected and rerun, and only the
    successful result is accepted as evidence.
  - Public clone remained clean: `## main...origin/main`.
- Explicitly unchanged: coastline CSV contents, map/runtime behavior,
  dependencies, app version, EnvGeo-Seawater source/data/docs, the public Git
  clone, and any EnvGeo Core dependency. A timestamp check found only Seawater's
  macOS-managed `.DS_Store` dated during the session; our tools did not edit it,
  and it is excluded from source/data/documentation change claims.
- Decision: asset loading and provenance metadata remain future Core candidates,
  but each app keeps a local copy and independent record until after the first
  Earthquake DOI release.
- Next single item: unify the bilingual USGS catalog and plate-boundary citation text.

## 2026-10-08 — Classified JMA/NIED upload comparison as optional

- Purpose: determine whether the Advanced-page JMA/NIED upload is necessary for
  the core application and audit its current failure handling without expanding
  the feature.
- Necessity decision:
  - The core EnvGeo-Earthquake workflow is retrieval and display of official
    USGS catalog data; JMA/NIED upload comparison is not required for it.
  - The comparison can still help specialized Japan-focused research, so it is
    retained unchanged to preserve current behavior.
  - It is classified as an optional Advanced feature, not a gate for the first
    stable release or Zenodo DOI. No new formats, aliases, schemas, validation
    subsystem, or automatic JMA/NIED retrieval will be added.
- Direct audit method: extracted the four upload helper functions from each
  bilingual Advanced page without running external services, then exercised:
  - a valid CSV with longitude, latitude, depth, and magnitude: 1 normalized row;
  - a CSV missing required columns: safe empty result plus 1 warning;
  - a broken XLSX byte stream: safe empty result plus 1 readable error.
- Result: both English and Japanese implementations passed all three cases with
  no unhandled exception. No runtime code or test file was changed because no
  concrete defect was found.
- Privacy/lifecycle wording: documented that selected contents are read for the
  current Streamlit session and are not intentionally written by the app to a
  persistent application data store. Provider terms remain the user's
  responsibility.
- Phase 2 of the publication roadmap is complete at the agreed minimal scope.
- Documentation synchronized in both languages: validation policy, JMA/NIED
  manual, READMEs, roadmap, TODO, project status, publication audit, release
  checklist, Home history, and work logs.
- Verification after documentation updates:
  - full suite: `58 passed in 2.32s`, 0 skipped;
  - syntax parsing: 13 active/test Python files passed;
  - Streamlit `AppTest`: all 6 Home/active page files opened with 0 exceptions;
  - Markdown: 51 files, 92 local links, 0 missing;
  - public clone remained clean: `## main...origin/main`.
- Scope: application code, version, and dependencies were unchanged; the public
  clone and EnvGeo-Seawater were not modified.
- Next single item: add Natural Earth provenance/license records for the bundled
  coastline CSVs without changing map behavior.

## 2026-10-08 — Focused USGS failure-path audit and two minimal guards

- Purpose: inspect the existing USGS retrieval path under the new
  current-feature-preservation policy and change code only for reproduced
  unhandled crashes.
- Existing behavior confirmed without changes:
  - `HTTPError`, `URLError`, and `TimeoutError` were already converted to
    readable `RuntimeError` messages by the shared loader.
  - All four active visualizer pages already catch `RuntimeError`, show it with
    `st.error`, and stop safely.
  - Empty FeatureCollections already produce the stable empty dataframe, and
    each page displays its existing no-data message.
- Reproduced gaps before editing:
  - malformed JSON escaped as an uncaught `JSONDecodeError`;
  - a response whose `features` member was a mapping iterated string keys and
    failed with `AttributeError: 'str' object has no attribute 'get'`.
- Minimal implementation in `envgeo_utils.load_usgs_earthquake_data()`:
  - convert JSON decoding/Unicode decoding failures to
    `RuntimeError("USGS API returned invalid JSON data.")`;
  - require a dictionary payload with a list-valued `features` member and
    otherwise raise a readable unexpected-GeoJSON `RuntimeError`.
- Added exactly two deterministic, no-network regression tests in
  `test/test_envgeo_utils.py`, one for each reproduced crash. Normal USGS
  normalization, plotting, query parameters, and empty-result behavior were
  not changed.
- Documentation synchronized in both languages: testing guides/test notes,
  roadmap, TODO, project status, publication audit, Home history, and work log.
- Verification:
  - focused tests: `2 passed, 12 deselected in 0.50s`;
  - final full suite: `58 passed in 1.52s`, 0 skipped;
  - syntax parsing: 13 active/test Python files passed;
  - Streamlit `AppTest`: all 6 Home/active page files opened with 0 exceptions;
  - Markdown: 51 files, 92 local links, 0 missing;
  - public clone remained clean: `## main...origin/main`.
- Scope: application version and dependencies did not change; the public clone
  and EnvGeo-Seawater were not modified.
- Next single item: audit existing JMA/NIED upload failure paths and change only
  a reproduced unreadable-input case.

## 2026-10-08 — Narrowed validation to essential, behavior-preserving safeguards

- User direction: preserve the current Earthquake features and add only
  genuinely necessary functionality. The app primarily retrieves and displays
  official USGS catalog data, so a separate scientific grading subsystem would
  be disproportionate.
- This decision supersedes the broader staged-validation implementation plan in
  the entry immediately below. That entry remains as chronological history,
  not as the current implementation requirement.
- Current policy:
  - Trust USGS catalog values as source data and do not assign independent
    Earthquake/Seawater quality grades.
  - Add only small safeguards for demonstrated connection, timeout, HTTP,
    malformed-response, empty-result, or plot-crash paths.
  - Keep JMA/NIED upload checking limited to advertised formats, required
    columns, numeric conversion, and readable file errors.
  - Defer duplicate-ID management, issue-code/severity frameworks, validation
    dashboards, enhanced issue exports, and timezone behavior changes unless a
    concrete defect or later requirement justifies them.
  - Require a focused failing case before adding validation behavior, and keep
    normal USGS display results unchanged.
- Durable records updated in both languages: project instructions, validation
  policy, roadmap, project status, TODO, READMEs, documentation index,
  export/notes manual, publication audit, release checklist, and Home history.
- Runtime code and dependencies were not changed; Home changes are update-log
  text only.
- Verification after the policy revision:
  - `pytest -q`: `56 passed in 1.68s`.
  - Syntax parsing: 13 active/test Python files passed.
  - Streamlit `AppTest`: all 6 Home/active page files opened with zero
    exceptions.
  - Markdown: 51 files, 92 local links, 0 missing.
  - Public clone remained clean: `## main...origin/main`.
- Scope: the public clone and EnvGeo-Seawater were not modified.
- Next single item: audit the current USGS failure paths; add code only if a
  specific unhandled crash is demonstrated by a focused test.

## 2026-10-08 — Defined the Earthquake catalog validation contract

- Purpose: complete the first Phase 2 roadmap item by defining validation
  criteria before changing normalization, filtering, plots, or exports.
- Source review:
  - Checked the active USGS GeoJSON normalization and both bilingual Advanced
    upload normalizers.
  - Used the official USGS GeoJSON/FDSN specifications, JMA hypocenter record
    format, and NIED Hi-net data guidance as the authoritative basis.
- Decisions recorded in `docs/earthquake_validation.md` and its Japanese peer:
  - Use `Error`, `Warning`, and `Information` issues rather than a single
    Seawater-style quality grade.
  - Preserve source rows and report invalid/duplicate values; do not silently
    rewrite, deduplicate, or delete them.
  - Require finite longitude/latitude within -180..180/-90..90 for spatial
    use, and depth within the USGS query contract of -100..1000 km for
    depth-dependent use. Negative depth is not automatically invalid.
  - Do not impose a nonnegative magnitude rule; negative catalog magnitudes
    can be valid.
  - Interpret USGS epoch milliseconds as UTC. Report a timezone-naive generic
    upload as `timezone_unknown` rather than silently labeling it UTC.
  - Require a nonblank, response-unique USGS Event ID while retaining and
    reporting all duplicate rows. Generic uploads do not receive invented IDs.
  - Preserve USGS `status` and `alert` as source metadata, not validity or
    Seawater quality flags.
  - Define stable issue codes and separate eligibility for 2D, 3D/section,
    temporal, magnitude, and comparison views.
- Current implementation gap: this work defines the target contract only. The
  existing upload normalizer still interprets timezone-naive values through
  `utc=True`, drops rows missing coordinate/depth values, and does not yet
  report all out-of-range or duplicate-ID issues. Those behaviors were not
  changed in this documentation-only step.
- Documentation synchronized: bilingual READMEs, documentation indexes,
  export/notes manuals, roadmap, TODO, publication audit, release checklist,
  project status, and Home update history.
- Verification:
  - `pytest -q`: `56 passed in 1.40s`.
  - Syntax parsing: all 13 active/test Python files parsed.
  - Streamlit `AppTest`: all 6 Home/active page files opened with zero
    exceptions.
  - Markdown link check: 51 Markdown files, 92 local links, 0 missing.
  - Public clone remained clean: `## main...origin/main`.
- Scope: no runtime behavior or dependency changed; the public clone and
  EnvGeo-Seawater were not modified.
- Next single item: implement and test validation for coordinates, origin time,
  depth, magnitude, and event IDs.

## 2026-10-08 — Publication audit and durable handoff records

- Purpose: compare Earthquake with Seawater read-only, without changing
  `envgeo_seawater_v130`, and identify the remaining standalone/Zenodo work.
- Scope: code, loading, UI, uploads, filters, quality, provenance, tests, CI,
  and distribution configuration.
- Decisions:
  - Earthquake remains a publication candidate until standalone cleanup, CI,
    citation metadata, domain tests, and coastline provenance are complete.
  - Do not extract a Core during this publication-readiness phase.
  - Do not reuse Seawater quality, filter, or upload semantics directly.
- Verification:
  - All 11 current active/test Python files parsed successfully with `ast.parse`.
  - The 50 m and 110 m coastline CSV hashes match between the two projects.
  - Full pytest was not run because pytest was unavailable in the audit Python.
  - Existing `.pytest_cache` is stale and is not release evidence.
- Records added:
  - Bilingual `PROJECT_STATUS` handoff files.
  - `AGENTS.md` project boundaries for future coding agents.
  - Bilingual development-workflow and publication-audit documents.
  - Separate Japanese and English work logs with reciprocal links.
- Explicitly unchanged: Seawater, Earthquake runtime behavior, dependencies,
  data, and displayed version.
- Next action: remove inherited Seawater loading/skip tests from Earthquake and
  replace them with USGS GeoJSON contract tests.

## 2026-10-08 — Saved roadmap and fixed public-release scope

- Saved the complete ordered task list in both languages as
  `docs/publication_roadmap*.md` so later sessions can proceed one item at a
  time.
- Completed the first item, "Define the intended public-release file scope,"
  and recorded it in both `docs/public_release_scope*.md` files.
- Included current application code, coastlines, tests, bilingual documents,
  and work logs in the intended public source release.
- Excluded `old/`, `data/`, `__ToDo__/`, `__logo__/`, `images/`, caches, and OS
  output. Nothing was deleted from the development folder.
- Removed the `docs/work_log.md` ignore rule so both logs can remain available
  in a future public clone after release-time privacy review.
- Did not change EnvGeo-Seawater or Earthquake runtime code, data, or
  dependencies.
- Next single item: confirm the public GitHub repository or local Git-clone
  location.

## 2026-10-08 — Confirmed and audited the public Git clone read-only

- Confirmed the public Git clone and GitHub remote. Stored machine-specific
  paths in bilingual `LOCAL_WORKSPACE` files covered by `.gitignore`.
- Operating rule: keep the clone read-only until the user explicitly requests
  copying reviewed files; the user performs commits and pushes in GitHub
  Desktop.
- Inspected it read-only with `git status --short --branch`, `git remote -v`,
  `git log -1`, `git branch -vv`, `git tag`, and `git ls-files`.
- The clone was on a clean `main` at `86b2d54`, matching its locally recorded
  `origin/main`. The latest commit date was 2026-09-23; tags were `v0.2.3.1`
  and `v0.2.1`. No network fetch was performed.
- Of 54 tracked files, 42 were byte-identical to the development folder and 12
  differed. The clone displayed application version `0.3.2`.
- Did not write or copy into the clone and did not commit, push, or modify
  Seawater.
- Completed publication-roadmap item 2. The next single item is removing old
  Seawater dataset loading from the active utility in the development folder.

## 2026-10-08 — Removed inherited Seawater dataset loading

- Purpose: complete roadmap item 3 by removing unused Seawater dataset loading
  from the active Earthquake utility.
- Reference check: no active page called `load_isotope_data()`; only four old
  tests that skip when the Seawater files are absent referenced it.
- Change: removed the entire `load_isotope_data()` implementation and its
  Seawater Excel reads, merging, and cleaning logic from `envgeo_utils.py`;
  updated the following section numbers.
- Explicitly unchanged: Earthquake coastline, USGS, JMA/NIED, UI, dependencies,
  four skipped tests, the public Git clone, and EnvGeo-Seawater.
- Verification:
  - Before change, `/opt/anaconda3/bin/pytest -q`: `45 passed, 4 skipped`.
  - After change, `/opt/anaconda3/bin/pytest -q`: `45 passed, 4 skipped`.
  - `ast.parse`: all 11 active/test Python files succeeded.
  - `rg`: no `def load_isotope_data`, Seawater dataset path, or
    `pd.read_excel(file_...)` remains in active `envgeo_utils.py`.
- Decision: retain the four old skipped tests unchanged until their dedicated
  roadmap item replaces them with Earthquake contract tests.
- Next single item: audit the whole repository for unpublished dataset names or
  references and remove any that remain.

## 2026-10-08 — Seawater-style bilingual section-comment policy

- User policy: identify each major code section in both English and Japanese,
  following EnvGeo-Seawater's readable comment structure.
- Inspected Seawater's `envgeo_utils.py` read-only and adopted its separated
  `English / 日本語` heading convention for Earthquake.
- Saved the rule in both `AGENTS`, `development_workflow`, and `PROJECT_STATUS`
  language files.
- Updated sections 0--9 and the Pandas heading in `envgeo_utils.py` with paired
  bilingual headings and purpose notes. No processing logic changed.
- Verification:
  - `ast.parse`: all 11 active/test Python files succeeded.
  - `/opt/anaconda3/bin/pytest -q`: `45 passed, 4 skipped`.
- Did not advance the next publication-roadmap item and did not modify the
  public Git clone or any EnvGeo-Seawater file.

## 2026-10-08 — Audited and removed unpublished-dataset references

- Purpose: complete roadmap item 4 by checking active code, tests, and intended
  public documents for legacy unpublished dataset names or paths.
- Scope: intended public contents in the development folder, excluding `old/`,
  `data/`, caches, and local-only notes. Inspected the public Git clone
  separately and read-only.
- Result: active development code had zero remaining references; the prior
  loader removal had already eliminated them. Replaced one specific legacy
  filename in the handoff document with a generic description.
- Retained general safety statements such as excluding confidential/private
  data because they are policies, not data references.
- The old utility in the public clone still contains the inherited loader and
  specific unpublished references. Per user instruction, did not copy, edit,
  commit, or push in the clone.
- Verification:
  - Residual search: zero matches in current/intended-public development scope.
  - `ast.parse`: all 11 active/test Python files succeeded.
  - `/opt/anaconda3/bin/pytest -q`: `45 passed, 4 skipped`.
  - Markdown local links: 82 checked, zero broken.
- Updated both roadmap, TODO, `PROJECT_STATUS`, and audit languages to show
  completion in development and pending user-directed synchronization to the
  public clone.
- Next single item: replace four Seawater-dependent skipped tests with
  Earthquake contract tests.

## 2026-10-08 — Replaced Seawater skips with Earthquake contract tests

- Purpose: complete roadmap item 5 by replacing four tests that skipped without
  Seawater datasets with contracts that always run in standalone Earthquake.
- Removed the legacy Seawater path, skip helper, and four isotope-loader tests
  from `test/test_envgeo_utils.py`.
- Added four contracts:
  1. Preserve one row per USGS GeoJSON feature, including incomplete features.
  2. Keep the page/CSV column names and order stable.
  3. Coerce numeric strings and convert invalid numeric values to missing.
  4. Derive UTC and calendar fields consistently from millisecond timestamps.
- Documented test intent with bilingual comments/section headings, added
  `test/README_Japanese.md`, and updated both testing guides and the test README.
- Verification:
  - Full suite before replacement: `45 passed, 4 skipped`.
  - `/opt/anaconda3/bin/pytest -q test/test_envgeo_utils.py`: `12 passed`.
  - Full suite after replacement: `49 passed, 0 skipped`.
  - `ast.parse`: all 11 active/test Python files succeeded.
  - Zero test references remain to the inherited loader, skip helper, or
    Seawater dataset path.
- Explicitly unchanged: live USGS access, application implementation, public
  Git clone, and EnvGeo-Seawater.
- Next single item: exclude irrelevant Seawater samples and development
  archives from public contents without deleting them from the development
  folder.

## 2026-10-08 — Excluded irrelevant samples and development archives

- Purpose: complete roadmap item 6 by reliably excluding Seawater samples,
  development history, notes, and unused assets that Earthquake does not need.
- Audited `old/`, `data/`, `__ToDo__/`, `__logo__/`, `images/`, and
  `.devcontainer/`. Retained every directory locally; deleted nothing.
- Found one missing `data/` image reference in an unused inherited sidebar
  function. Removed that Seawater-specific image display block from
  `envgeo_utils.py`.
- Added root-anchored `.gitignore` rules for all six directories. Existing
  rules continue to exclude OS files, caches, bytecode, build/log output, and
  secrets.
- Verification:
  - All six required root-anchored ignore rules are present.
  - All six excluded directories remain available locally.
  - Zero excluded-directory string references in 11 active/test Python files.
  - `ast.parse`: all 11 Python files succeeded.
  - `/opt/anaconda3/bin/pytest -q`: `49 passed, 0 skipped`.
  - Zero files from the excluded directories are tracked in the public clone.
- `git check-ignore` could not run in the development folder because it is not
  a Git repository (`fatal: not a git repository`). Verified the rules and the
  public clone's tracked-file inventory instead.
- Explicitly unchanged: public Git clone, EnvGeo-Seawater, visible application
  behavior, and earthquake processing.
- Next single item: centralize application version metadata.

## 2026-10-08 — Added the public logo to both Home pages

- Purpose: establish one shared public EnvGeo-Earthquake brand image on the
  English and Japanese Home pages.
- Visually and technically compared four PNG candidates in `__logo__/` and
  initially selected `logo_01.png`. It is byte-identical to
  `ChatGPT Image 2026年5月6日 18_59_26 (3).png` in the same directory.
- The selected source is a 1254×1254 RGB PNG with SHA-256
  `d668ed0cb0a720c661732231e7c9173d99611ccd0b49acbcf4b4d9a7ab2166b9`.
- Copied only the selected public asset to
  `assets/branding/envgeo-earthquake-logo.png` and verified the copied hash.
  The full `__logo__/` candidate directory remains excluded from publication.
- Added source-file-relative, current-working-directory-independent asset
  resolution and a centered 320 px display to `home.py` and
  `pages/00_home_(Japanese).py`. The edited sections include the Seawater-style
  `English / Japanese` purpose comment.
- Synchronized bilingual branding READMEs, root READMEs, public-scope records,
  Home histories, release checklists, TODOs, and PROJECT_STATUS files.
- Remaining release decision: confirm the logo creator/rights and final
  AI-assistance disclosure wording, then synchronize the branding READMEs,
  `NOTICE.md`, and release notes.
- Verification:
  - `ast.parse`: all 11 active/test Python files succeeded.
  - `/opt/anaconda3/bin/pytest -q`: `49 passed, 0 skipped`.
  - Streamlit AppTest: zero exceptions and one image on each Home page.
  - Local browser inspection: confirmed centered logo placement and title
    spacing on both Home pages.
  - A separate CLI launch attempt encountered an execution-environment port
    bind `PermissionError`; it is not counted as successful-startup evidence.
- Explicitly unchanged: public Git clone, EnvGeo-Seawater, and earthquake data
  processing.
- The next roadmap item remains unchanged: centralize application version
  metadata.

### Same-day correction — withdrew the inaccurate globe design

- User review identified inaccurate continent placement and island/peninsula
  shapes in `logo_01.png`; it was withdrawn as the public logo.
- The other globe candidate also uses stylized geography whose accuracy cannot
  be guaranteed, so it was not selected.
- Replaced the public asset with
  `ChatGPT Image 2026年5月6日 18_59_25 (2).png`, which depicts a schematic
  surface, mountains, city, subsurface layers, seismic waveform, and hypocenter
  without continent, island, or peninsula outlines.
- The replacement public copy has SHA-256
  `aa46cc8f90b100ee6c2ad078d43d7ddf117223ccf4cdcd98d5f0f45d28abd064`,
  matching the selected source.
- Home paths and rendering code did not change; only the image asset was
  replaced. The public Git clone and EnvGeo-Seawater remain unchanged.
- Post-replacement verification: each bilingual Home AppTest reported zero
  exceptions and one image; pytest reported `49 passed, 0 skipped`; all 86
  local Markdown links resolved.

### Same-day final correction — removed the top-of-page Home logo

- After a further design review with the user, the large image at the top of
  Home was judged inconsistent with the page's overall balance and removed
  from both language versions.
- Removed `LOGO_PATH`, the centering columns, and `st.image()` from both Home
  pages, which now begin with the application title again.
- Removed the public copy at `assets/branding/envgeo-earthquake-logo.png` and
  its bilingual asset notes; the current public scope contains no logo asset.
- Original candidates remain recoverable in the development-only, excluded
  `__logo__/` folder if a small icon or background is considered later.
- Synchronized the bilingual READMEs, public-scope records, release checklists,
  TODOs, PROJECT_STATUS files, and Home histories with the no-logo decision.
- Post-removal verification: each bilingual Home AppTest reported zero
  exceptions and zero images; all 11 Python files parsed; pytest reported
  `49 passed, 0 skipped`; all 84 local Markdown links resolved.
- The public Git clone and EnvGeo-Seawater remain unchanged.

## 2026-10-08 — Centralized runtime version metadata

- Purpose: complete the next Phase 1 roadmap item by replacing duplicated
  runtime `0.3.2` definitions across Home, utility, and four active pages with
  one definition.
- Kept `envgeo_utils.APP_VERSION = "0.3.2"` and
  `APP_VERSION_DATE = "2026-09-22"` as the sole metadata source. The legacy
  `version` compatibility alias continues to reference `APP_VERSION`.
- Removed local `APP_VERSION` / `version` string definitions from `home.py`,
  Japanese Home, and the four English/Japanese Simple/Advanced pages. All six
  displays now read `envgeo_utils.APP_VERSION` directly; the displayed value
  remains `0.3.2`.
- Added a contract in `test/test_basic.py` for the shared value, ISO date,
  shared references in all six pages, and absence of local string
  redefinitions.
- Synchronized bilingual READMEs, Home histories, test READMEs, testing guides,
  publication audits, roadmaps, release checklists, TODOs, and PROJECT_STATUS
  files.
- Verification:
  - `/opt/anaconda3/bin/pytest -q test/test_basic.py`: `3 passed, 0 skipped, 0 failed`.
  - `/opt/anaconda3/bin/pytest -q`: `50 passed, 0 skipped, 0 failed`.
  - `ast.parse`: all 11 active/test Python files succeeded.
  - Active-Python string-definition search: one match, in `envgeo_utils.py` only.
  - Streamlit AppTest: zero exceptions across both Home pages and all four
    active visualizer pages.
  - Markdown local links: 84 checked across 49 files, zero broken.
  - Public-clone `git status --short --branch`: only `## main...origin/main`;
    no changes.
- Explicitly unchanged: displayed version value, earthquake processing, public
  Git clone, EnvGeo-Seawater, and any future EnvGeo Core dependency.
- Decision: use the existing Earthquake-local `envgeo_utils`, already imported
  by every page, rather than adding another module; this preserves standalone
  distribution.
- Next single item: verify current-working-directory-independent asset loading.

## 2026-10-08 — Verified CWD-independent asset loading

- Purpose: complete the next Phase 1 roadmap item by proving that bundled
  Earthquake assets remain loadable independently of the process working
  directory in a standalone distribution.
- Audited active/test Python and identified three local bundled-asset flows:
  50m/110m coastline CSVs, the English Home README, and the Japanese Home
  README. Advanced-page CSV/Excel reads consume user-uploaded file objects and
  are not bundled assets.
- Added `PROJECT_ROOT` / `COASTLINE_DIR` to `envgeo_utils.py`, documenting in
  `English / Japanese` that paths resolve from the module's `__file__`.
- Standardized English Home on `APP_ROOT / "README.md"` and Japanese Home on
  `APP_ROOT / "README_Japanese.md"`. Corrected the Japanese Markdown local-image
  base from `pages/` to the project root.
- Added `test/test_asset_paths.py` with three tests. After changing to a pytest
  temporary directory, they clear the coastline cache and really load both CSV
  resolutions, then render each Home README and verify its content.
- An initial alternate-CWD AppTest attempt failed on both pages with
  `ModuleNotFoundError: envgeo_utils` because changing CWD changed what the
  test process's empty-string `sys.path` entry resolved to. This occurred
  before asset loading and was not counted as success. The durable test adds
  the project root explicitly to isolate and test asset resolution itself.
- Verification:
  - `/opt/anaconda3/bin/pytest -q test/test_asset_paths.py`: `3 passed, 0 skipped, 0 failed`.
  - `/opt/anaconda3/bin/pytest -q`: `53 passed, 0 skipped, 0 failed`.
  - `ast.parse`: all 12 active/test Python files succeeded.
  - Absolute local-path (`/Users/`, `~/`) search in active/test Python: zero.
  - Streamlit AppTest: zero exceptions across both Home pages and all four
    active visualizer pages under the normal project working directory.
  - Markdown local links: 84 checked across 49 files, zero broken.
  - Public-clone `git status --short --branch`: only `## main...origin/main`;
    no changes.
- Explicitly unchanged: earthquake processing, CSV contents, public Git clone,
  EnvGeo-Seawater, and any future EnvGeo Core dependency.
- Next single item: remove advertised `.xls` support or add and test its
  dependency.

## 2026-10-08 — Removed legacy `.xls` advertising and fixed the `.xlsx` contract

- Purpose: complete the final Phase 1 roadmap item by aligning advertised
  upload formats with installed runtime dependencies.
- Limited the Excel branch in both Advanced `read_uploaded_catalog()` copies to
  `.xlsx`, and changed both `st.file_uploader()` controls to accept `csv`,
  `tsv`, `txt`, and `xlsx` only.
- Retained `openpyxl==3.1.5` for `.xlsx`; did not add the separate `xlrd`
  dependency for legacy binary `.xls`. Bilingual manuals now tell users to
  resave old `.xls` files as `.xlsx` or text before upload.
- Added `test/test_upload_formats.py` contracts for bilingual accepted types,
  absence of a `.xls` branch, `openpyxl` declaration, absence of `xlrd`, and an
  in-memory XLSX workbook write/read round-trip.
- The first targeted run reported `2 passed, 1 failed`: Excel preserved the
  value `135.0` while inferring `int64` instead of the fixture's `float64`, so
  only dtype comparison failed. Changed the coordinate/depth fixture to
  non-integer values so the engine contract is not coupled to unrelated dtype
  inference.
- Synchronized bilingual READMEs, JMA/NIED manuals, Home histories, test
  READMEs, testing guides, publication audits, roadmaps, release checklists,
  TODOs, and PROJECT_STATUS files.
- Verification:
  - After correction, `/opt/anaconda3/bin/pytest -q test/test_upload_formats.py`:
    `3 passed, 0 skipped, 0 failed`.
  - `/opt/anaconda3/bin/pytest -q`: `56 passed, 0 skipped, 0 failed`.
  - `ast.parse`: all 13 active/test Python files succeeded.
  - Streamlit AppTest: zero exceptions across bilingual Home, Simple, and
    Advanced pages (six pages total).
  - Active-page `.xls` acceptance/branch search: zero matches.
  - Markdown local links: 84 checked across 49 files, zero broken.
  - Public-clone `git status --short --branch`: only `## main...origin/main`;
    no changes.
- Decision: CSV/text and current `.xlsx` formats satisfy the comparison use
  case; do not enlarge runtime dependencies solely for the legacy format.
- Explicitly unchanged: `.xlsx`, CSV, TSV, and TXT support; required-column
  processing; earthquake processing; `requirements.txt`; public Git clone;
  EnvGeo-Seawater; and any EnvGeo Core dependency.
- All nine Phase 1 items are complete in the development folder. The next
  single item is to define earthquake-specific validation criteria.

## 2026-09-22 — Version 0.3.2 consolidation

- Restored card-style tabs under Streamlit 1.63 while retaining 1.42 selectors.
- Applied the shared tab helper to current Home and active bilingual pages.
- Updated active version labels to 0.3.2; did not modify `old/`.
- Recorded targeted regression evidence of 14 passed and 4 skipped.
- Kept coastline files local until both projects can independently validate a future move.

## 2026-09-20 — Streamlit 1.63 compatibility and UI alignment

- Replaced the problematic default map style with OpenStreetMap and removed a duplicate style call.
- Made filter ranges NaN-safe and resolved Session State/default-value warnings.
- Isolated query-state keys across the four pages.
- Added matching top/bottom Fetch buttons and aligned user guidance across languages.
- Adjusted Advanced cross-section control placement and color-scale state handling.

## 2026-09-19 — Compatibility cycle

- Set development version 0.3.1 and Streamlit range 1.42–1.63 with Plotly 5.24 as baseline.
- Improved region-state restoration and page-specific API widget state.
- Deferred the MapLibre/Plotly 7 migration until a cross-environment test is available.

## 2026-09-18 — Streamlit/Pandas compatibility

- Added old/new Streamlit full-width compatibility and Pandas option guards.
- Verified initial page display in Streamlit 1.42 and 1.63 environments.
- Recorded 9 passed and 4 skipped in the historical test environment.

## 2026-09-16 — Documentation and project-boundary foundation

- Reworked README/Home language around research use and the Seawater relationship.
- Updated page names, Japanese terminology, region state, and hotspot captions.
- Added USGS GeoJSON normalization tests and skipped non-bundled Seawater data checks.
- Recorded 9 passed and 4 skipped in the historical environment.
- Expanded `.gitignore`, split runtime/development requirements, and added `NOTICE.md`.
