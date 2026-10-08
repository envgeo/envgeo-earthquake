# EnvGeo-Earthquake Publication and Shared-Core Audit

[Japanese version](publication_audit_2026-10-08_Japanese.md)

Audit date: 2026-10-08 (Asia/Tokyo)  
Scope: read-only comparison of `earthquake_map_v030` and `../envgeo_seawater_v130`

## Purpose and conclusion

The goals are to make Earthquake independently runnable, testable, deployable,
and archivable with a Zenodo DOI; identify future Core candidates without
extracting them now; and avoid any effect on Seawater v1.3.5/JOSS work.

Earthquake already has its main features, bilingual manuals, an MIT license,
and basic tests. It remains a publication candidate because standalone cleanup,
CI/distribution metadata, domain-specific tests, and coastline provenance are
not yet complete.

## Classification

### Future EnvGeo Core candidates

- Streamlit compatibility helpers, tab UI, and asset resolution
- Map backgrounds, connectivity checks, offline fallback, coastlines, graticules
- Longitude/dateline handling and region-preset data structures
- Local-km conversion and generic 3D layout
- Source/citation/license metadata and safe export naming

### EnvGeo-Seawater specific

- Seawater isotope/hydrographic Excel integration, d-excess, salinity, temperature
- Seawater physical-range quality flags
- GSW, Cartopy, GEBCO, bathymetric interpolation
- Cruise/station/transect filters, overlap detection, and Seawater upload integration

### EnvGeo-Earthquake specific

- USGS FDSN Event API, GeoJSON normalization, and the 20,000-event limit
- Earthquake time, magnitude, hypocenter depth, and ordering semantics
- Hotspots, plate boundaries, earthquake sections, depth/time histograms
- JMA/NIED catalog comparison and preliminary/revisable-data warnings

### Similar names that should not be shared yet

- Data loaders: bundled seawater files and a live earthquake API have different responsibilities.
- Filters: post-load observations versus API query conditions.
- Quality: seawater physical bounds versus catalog review/status semantics.
- Uploads: generic observation tables versus JMA/NIED catalog schemas and terms.
- Cross-sections: geometry may later be shared, but water-column interpolation and hypocenter distributions remain separate layers.
- Bilingual page duplication: an internal Earthquake maintenance problem, not a Core responsibility.

## Main publication blockers

- Resolved in the development folder on 2026-10-08: active
  `envgeo_utils.py` no longer contains the inherited Seawater loader or
  unpublished dataset references. The separate public clone awaits a
  user-directed copy.
- Resolved in the development folder on 2026-10-08: the four inherited
  Seawater skips were replaced with deterministic USGS GeoJSON contract tests;
  the full available suite reported `49 passed, 0 skipped`.
- No CI, `CITATION.cff`, package/release metadata, or distribution-content proof.
- Resolved in the development folder on 2026-10-08: bilingual Advanced upload
  controls accept CSV, TSV, TXT, and `.xlsx` only. Legacy `.xls` is no longer
  advertised; `openpyxl` remains declared and an in-memory XLSX round-trip is
  tested. No unused `xlrd` dependency was added.
- The bilingual validation policy was narrowed to current-feature preservation.
  USGS catalog values are trusted; publication work is limited to demonstrated
  crash/error paths and basic upload safety. Duplicate-ID management, issue
  codes, dashboards, and independent catalog grading are not current blockers.
- Resolved in the development folder on 2026-10-08: malformed USGS JSON and a
  non-list GeoJSON `features` member now become readable `RuntimeError` messages
  handled by all four pages. Two deterministic tests cover only these reproduced
  crashes. Loader-level normal, empty, incomplete, HTTP-error, timeout, and
  connection-failure cases are now also deterministic; the full suite reports
  `67 passed, 0 skipped` without live service access. Required/optional query
  construction and the four-page result-limit boundary were subsequently
  centralized and tested, bringing the suite to `73 passed`.
- Reviewed on 2026-10-08: JMA/NIED upload comparison is optional and not a
  first-release/DOI gate. Bilingual direct checks of a normal CSV, missing
  columns, and a broken XLSX all returned safely. The feature remains unchanged
  for compatibility, with no schema expansion; session-only handling is now
  documented. The actual bilingual page helpers now have persistent smoke tests
  for one representative CSV and one missing-required-columns CSV; the full
  suite then reported `77 passed`.
- Resolved in the development folder on 2026-10-08: all four visualizer pages
  now retain valid longitude ±180° and latitude ±90° boundary points while
  excluding missing, non-numeric, and out-of-range USGS coordinates before
  plotting. Eight direct page-helper tests bring the full suite to `85 passed`.
  Optional-upload normalization and dateline behavior were not changed.
- Verified in the development folder on 2026-10-08: 20 direct-helper tests now
  cover longitude wrapping, map-seam breaks, Pacific-centered continuity,
  dateline-adjacent local-km coordinates, short-path cross-section projection,
  signed section offsets, coincident endpoints, and closed corridor polygons
  in every applicable bilingual page. No runtime code change was required; the
  full suite now reports `105 passed`.
- Resolved in the development folder on 2026-10-08: malformed plate-service
  GeoJSON now enters the existing per-layer error/fallback path instead of
  raising during feature mutation. Japan-only total failure shows the explicit
  schematic fallback; non-Japan failure remains empty; partial microplate
  failure retains the valid USGS main-plate data and displays an accurate
  partial-layer warning. Thirteen network-free bilingual tests bring the full
  suite to `118 passed`.
- Completed in the development folder on 2026-10-08: persistent Streamlit
  AppTests now start bilingual Home and all four active visualizer pages during
  ordinary pytest. Six cases protect exception-free initial rendering, common
  title, bilingual primary headings, shared version display, and paired fetch
  buttons. No runtime code changed; the full suite reports `124 passed`.
- Completed in the development folder on 2026-10-08: eight portable repository-
  health tests now enforce the release allowlist/exclusions, ignore rules,
  standalone-clone tracked files, runtime references, common secret/private-key
  patterns, machine-specific absolute paths, symlinks, and Markdown links. The
  working folder keeps excluded local material, and the public clone remains
  untouched. The full suite reports `132 passed`.
- Completed before Phase 5 in the development folder on 2026-10-08: all four
  bilingual visualizer pages now default to magnitude-linked marker sizing and
  offer a fixed-size option. Main 2D/3D and Advanced cross-section markers use
  the selected mode, a visual M7:M4 diameter ratio of approximately 20:1, and
  an adjustable 1:1–30:1 contrast control, and a separate direct overall scale
  up to ten times. Forty deterministic
  tests brought the full suite to `172 passed`; the public clone remained untouched.
- Completed before Phase 5 in the development folder on 2026-10-08: all four
  visualizer pages now place concise bilingual Plotly camera guidance before
  the main 3D chart. It covers drag, rotate/pan/zoom/reset,
  Shift/Control/Option (Alt)/Command, and browser/OS variation. Option was
  confirmed on macOS. Four contracts bring the full suite to `176 passed`;
  the public clone remains untouched.
- Resolved in the development folder on 2026-10-08: a bilingual responsibility
  record now distinguishes JMA's source/processing/third-party-rights terms from
  NIED Hi-net's registration, no-redistribution, provider acknowledgement, DOI
  citation, and result-reporting requirements. No provider catalog is bundled;
  a deterministic metadata/record contract brings the suite to `61 passed`.
- Reviewed on 2026-10-08: active code uses Plotly's OpenStreetMap standard
  style, not a CARTO basemap. USGS imagery, Esri World Ocean Base, and GSI
  credits were aligned with provider sources and centralized locally. Static
  export cautions and a network-free attribution contract were added; tile
  selection and endpoints were not changed.
- Resolved in the development folder on 2026-10-08: bilingual bundled records
  identify both byte-identical coastline CSVs as Natural Earth coastline v4.1.0
  derivatives, preserve output hashes and retained intermediate-workbook evidence,
  and disclose that original raw-download hashes and exact dates were not retained.
- Resolved in the development folder on 2026-10-08: the FDSN-listed ANSS
  Comprehensive Catalog citation and the Bird (2003) / DeMets et al. (2010)
  citations named by USGS plate-service metadata are centralized in the local
  utility and reused by all applicable bilingual pages. A deterministic contract
  test prevents page-level citation drift.
- Resolved in the development folder on 2026-10-08: runtime version metadata
  is defined once in `envgeo_utils.py`; both Home pages and all four active
  visualizer pages reference it. A contract test prevents local string
  redefinitions, and the full suite reported `50 passed, 0 skipped`.
- Resolved for public tracking in the development folder on 2026-10-08:
  root-anchored ignore rules exclude development archives, local data/assets,
  caches, and OS files. The source material remains available locally.
- Resolved in the development folder on 2026-10-08: bundled coastline CSVs and
  both Home README views resolve from source-file locations. Tests load them
  after changing outside the project working directory; the full suite reports
  `53 passed, 0 skipped`.

## Minimal publication plan

1. Establish an Earthquake-only public Git repository and explicit release scope.
2. Replace inherited Seawater loading/tests with Earthquake contract tests.
3. Preserve source, retrieval time, query URL, and app-version metadata.
4. Add focused API/geometry/AppTest coverage and Python 3.10/3.12 CI; test the
   optional upload only if it remains enabled in the release.
5. Add `CITATION.cff`, release metadata, provenance, and content checks.
6. Complete the Streamlit deployment smoke test.
7. Enable the GitHub repository in Zenodo, then archive a CI-passing tagged release.
8. Add the issued DOI to README, citation metadata, and the release record.

## Evidence recorded

- The 50 m coastline files are byte-identical across the projects, as are the
  110 m files.
- `apply_common_layout`, `get_custom_colorscale`, and `insert_gap_rows` were
  AST-identical. Identical source alone does not justify extraction now.
- English/Japanese Simple and Advanced pages share about 87% of distinct lines.
- All 11 current active/test Python files parsed successfully with `ast.parse`.
- Full pytest was not run because pytest was unavailable in the audit Python.
