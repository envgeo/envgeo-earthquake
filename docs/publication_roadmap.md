# EnvGeo-Earthquake Publication Roadmap

[Japanese version](publication_roadmap_Japanese.md)

Last updated: 2026-10-08

Complete items in order. Check an item only after its evidence is recorded in
both work-log languages. Do not modify or add a dependency on EnvGeo-Seawater.

## Phase 1 — Standalone Earthquake application

- [x] Define the intended public-release file scope.
- [x] Confirm the public GitHub repository or clone location.
- [x] Remove inherited Seawater dataset loading from active utilities.
- [x] Remove unpublished dataset references.
- [x] Replace four Seawater-dependent skip tests.
- [x] Exclude irrelevant Seawater samples and development archives.
- [x] Centralize application version metadata.
- [x] Verify current-working-directory-independent asset loading.
- [x] Remove advertised `.xls` support or add and test its dependency.

## Phase 2 — Minimal robustness and reproducibility

- [x] Define a minimal validation policy that preserves current behavior.
- [x] Audit current USGS failure handling and add only guards needed to prevent
  page crashes for connection, timeout, HTTP, malformed JSON, and empty data.
- [x] Verify the existing JMA/NIED upload required-column and unreadable-file
  handling; change it only where a concrete failure is demonstrated.
- [x] Document session-only upload handling.
- [x] Preserve the existing result-limit and revisable-USGS-record notices.
- Deferred unless separately justified: duplicate-ID management, issue-code
  frameworks, validation dashboards, and expanded export metadata.

## Phase 3 — Provenance and licensing

- [x] Add Natural Earth provenance/license records for coastline CSVs.
- [x] Unify USGS catalog and plate-boundary citation text.
- [x] Recheck CARTO/OSM/USGS/Esri/GSI attribution.
- [x] Record JMA/NIED use and redistribution responsibilities.
- [x] Synchronize NOTICE, bilingual READMEs, and Home source notes for the
  completed coastline-provenance item; keep this synchronized as later sources are audited.

## Phase 4 — Earthquake-specific tests

- [x] Expand normal, empty, incomplete, malformed, HTTP-error, timeout, and connection tests for USGS data.
- [x] Test query construction and result-limit warnings.
- [x] If the optional comparison remains enabled for release, smoke-test one
  normal upload and one unreadable/missing-column case; do not expand schemas.
- [x] Test NaN and out-of-range coordinates in the actual plot-preparation
  helper used by all four bilingual visualizer pages.
- [x] Test longitude wrapping, dateline handling, local-km conversion, and
  section geometry by executing the actual bilingual page helpers.
- [x] Test plate-boundary success, total/partial failure, malformed GeoJSON,
  and the Japan-only schematic fallback in both Advanced pages.
- [x] Add persistent startup AppTest coverage for bilingual Home and all four
  active visualizer pages, including headings and fetch-button contracts.
- [x] Add repository-health checks for allowed release contents, ignore rules,
  tracked-file exclusions, runtime references, secrets/private keys, absolute
  local paths, symlinks, and Markdown local links.

## Phase 5 — CI and distribution

- [ ] Add Python 3.10 and 3.12 GitHub Actions CI.
- [ ] Run pytest, syntax, and release-content checks without live network access.
- [ ] Decide source-only versus installable package distribution.
- [ ] If packaged, add `pyproject.toml`, launcher, package-data rules, wheel proof, and isolated install test.
- [ ] Verify Streamlit Community Cloud configuration.
- [ ] Review the development container's disabled XSRF setting.

## Phase 6 — Complete bilingual documentation

- [ ] Verify clean-environment installation instructions.
- [ ] Synchronize quick start, USGS limits, upload schemas, validation, exports, offline behavior, and troubleshooting.
- [ ] Decide and record the AI-assistance disclosure policy.
- [ ] Check bilingual content parity and links.

## Phase 7 — Public deployment smoke test

- [ ] Verify bilingual Home, Simple, and Advanced pages.
- [ ] Verify USGS retrieval, empty results, limits, presets, and hotspots.
- [ ] Verify 2D/3D, sections, histograms, plate boundaries, and offline coastlines.
- [ ] If enabled in the release, verify the optional JMA/NIED upload once; also
  verify the core USGS CSV export.
- [ ] Check desktop and small-screen presentation.
- [ ] Record all results in both work logs.

## Phase 8 — GitHub Release

- [ ] Select the stable version and synchronize every version field.
- [ ] Add and validate `CITATION.cff` and bilingual release notes.
- [ ] Verify repository description, topics, license, and exact release contents.
- [ ] Select a clean CI-passing commit, tag it, create the Release, and inspect the archive.

## Phase 9 — Zenodo DOI

- [ ] Enable the GitHub repository in Zenodo before creating the Release.
- [ ] Verify author, ORCID, affiliation, license, keywords, version, and files.
- [ ] Publish the record and save version/concept DOIs.
- [ ] Add DOI links to bilingual READMEs, citation metadata, and release records.
- [ ] Verify reciprocal links among the app, GitHub Release, and Zenodo.

## Phase 10 — Future EnvGeo Core review

- [ ] Begin only after the Earthquake DOI release and separately from Seawater JOSS work.
- [ ] Add contract tests before evaluating asset, map, coastline, longitude,
  local-km, and source-metadata extraction.
- [ ] Design dependency/versioning and rollback plans that preserve both apps independently.
