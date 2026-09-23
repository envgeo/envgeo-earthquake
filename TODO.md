# EnvGeo-Earthquake TODO

Japanese version: [TODO_Japanese.md](TODO_Japanese.md)

Keep this English file and the Japanese version aligned. As a general project
policy, maintain user-facing UI text, README files, manuals, testing guides,
release notes, and major development policies in both English and Japanese.

## Current Policy

- Keep the development workspace as the source of edits.
- Copy only reviewed and tested changes to the Git clone before committing.
- Update README, README_Japanese, Home update history, and `docs/` whenever user-facing behavior, wording, data sources, testing, or workflow changes.
- Update the corresponding English and Japanese documents together whenever
  practical. If one language must temporarily lead during active development,
  record the missing translation as a follow-up and synchronize it before the
  next public release.
- Keep the app close to EnvGeo-Seawater in tone and workflow, while leaving earthquake-specific logic in the Earthquake layer.
- Maintain compatibility checks in both the verified Streamlit 1.42 environment and the Streamlit 1.63 / Plotly 5 comparison environment during migration.

## Near-Term Tasks

- [ ] Complete the remaining visual checks for the 0.3.2 Python 3.10-3.12 / Streamlit 1.42-1.63 compatibility cycle with Plotly 5.24 as the verified baseline, then decide on a public release.
  - [x] Update `requirements.txt` to allow Streamlit 1.42-1.63; a fresh deployment resolves to 1.63.
  - [x] Resolve Streamlit 1.63 dual Session State / `value=` warning in cross-section inputs (pages 55, 57): initialize session state before widgets and remove `value=` arguments.
  - [x] Add top Fetch/Update button to Advanced pages (55, 57) following the seawater pattern: top button after caption (label without `!`), bottom button at form end (label with `!`), both `use_container_width=True`.
  - [x] Apply the same top/bottom button pattern to Simple pages (54, 56). Added missing caption to page 54. All four pages now consistent.
- [ ] Migrate Mapbox traces to the MapLibre APIs available in Plotly 5.24, then test the same implementation with Plotly 6.7 and 7.1.
- [ ] After a separate design review, move the shared 50m/110m coastline CSV
  assets and cached loader into `envgeo-core`. Retain local copies until both
  Seawater and Earthquake independently pass loader and visual checks.
- [ ] Add a Python 3.10 / Streamlit 1.63 / Plotly 7 cross-environment test before claiming the full supported-version matrix is verified.
- [ ] Apply the verified low-risk fixes from the 2026-09-17 external review before larger refactoring.
  - [x] NaN-safe filter bounds: add `.dropna()` to slider min/max calculations (4 locations).
  - [x] Duplicate map-style calls: remove unconditional `carto-positron` line; switch to `open-street-map`.
  - [x] Missing Advanced-page About URL: added to page 55 to match page 54.
  - [ ] NaN-safe statistics (`np.mean` → `np.nanmean`): deferred to `envgeo4d` integration.
  - [ ] Boolean empty-data checks: deferred to `envgeo4d` integration.
  - [ ] Unused variable (`Transect_list`): deferred to `envgeo4d` integration.
- [ ] Expand Earthquake-specific tests for API failures, malformed GeoJSON, filter bounds, and scientific/spatial helper behavior.
- [ ] Run Streamlit and visually confirm Region / hotspot selection behavior after UI changes.
- [ ] Confirm Japanese and English page wording in the browser.
- [ ] Add a small screenshot/manual QA checklist for Simple and Advanced pages.
- [ ] Consider moving Region selection state handling into testable helper functions.
- [ ] Expand tests for longitude wrapping, local km coordinates, and cross-section geometry.
- [ ] Review JMA/NIED comparison upload wording and accepted column names.
- [ ] Decide whether `old/`, `data/`, `__logo__/`, and image assets should be included in the public GitHub repository.

## Documentation and Test Strategy

Date adopted: 2026-09-19

Adopt the useful parts of the JOSS-oriented documentation and testing review in
a way that fits EnvGeo-Earthquake. Keep this work incremental and separate from
large UI merges.

Documentation policy:
- Complete the existing English/Japanese Markdown manuals before introducing a
  documentation-site generator. Cover installation, quick start, USGS query
  behavior, Simple and Advanced workflows, JMA/NIED comparison data, exports,
  limitations, troubleshooting, testing, contribution, and support.
- Use MkDocs as the leading candidate for a future GitHub Pages documentation
  site, with a structure and visual style that can later be shared with
  EnvGeo-Seawater and the common `envgeo4d` core.
- Add API reference pages only for stable reusable helpers, such as USGS
  normalization, region presets, longitude/dateline handling, local-coordinate
  conversion, cross-section geometry, and source metadata.

Testing policy:
- Keep pure-function pytest tests as the primary check for scientific and
  spatial logic, and add persistent `streamlit.testing.v1.AppTest` tests for UI
  workflows.
- Start AppTest coverage with Home plus the English/Japanese Simple and Advanced
  pages. Confirm startup, region and hotspot controls, filter/application flow,
  empty results, messages, downloads, and session state.
- Mock USGS responses in automated tests. Cover successful, empty, malformed,
  timeout, rate-limit, and other API-failure responses without depending on the
  live service during CI.
- Add upload tests for expected and unexpected JMA/NIED column names, invalid
  files, missing coordinates, NaN values, and dateline-adjacent records.
- Keep Plotly/WebGL rendering, map tiles, selection tools, 3D camera behavior,
  and final screenshot appearance in a concise manual visual QA checklist.
- Add GitHub Actions after a representative AppTest set is stable. Use the same
  verified Python/Streamlit compatibility policy as Seawater where practical,
  while keeping Earthquake-specific network tests deterministic.

JOSS/shared-core note:
- Treat documentation and AppTest as part of the broader release-quality work,
  alongside packaging, CI, contribution/support guidance, public release
  history, research-use evidence, and AI-assistance disclosure.
- When helpers move into `envgeo4d`, move their unit tests and API documentation
  with them; retain page-specific workflow tests in EnvGeo-Earthquake.

## Shared-Core Candidates

Current policy: keep the four English/Japanese and Simple/Advanced pages separate
for now. Do not merge their page-level UI in one large change. Extract only
well-understood pure helpers in small steps, add focused tests, and confirm all
four pages after each extraction.

- [ ] Map background selection and attribution notes.
- [ ] Region preset handling.
- [ ] Coastline loading.
- [ ] Longitude wrapping and dateline handling.
- [ ] Local kilometer-coordinate conversion.
- [ ] Cross-section geometry helpers.
- [ ] Source/citation metadata display.
