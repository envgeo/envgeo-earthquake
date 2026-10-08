# Test Notes

[Japanese version](README_Japanese.md)

This folder contains small `pytest` checks for EnvGeo-Earthquake.

In simple terms, each test is an automatic checklist item. For example:

- Can Python import the main utility module?
- Does the utility module expose version information?
- Do all active Home/visualizer pages use the one shared version definition?
- Do bilingual pages reuse the shared USGS catalog and plate-boundary citations?
- Do online map modes retain the reviewed tile URLs and runtime attribution?
- Do bilingual JMA/NIED responsibility records retain the official references and NIED DOI?
- Does each USGS GeoJSON feature remain one earthquake row, even when fields are missing?
- Do USGS results keep the stable columns and column order used by pages and CSV exports?
- Are numeric text values converted safely and invalid values treated as missing?
- Are USGS millisecond timestamps converted consistently into UTC/calendar fields?
- Does GitHub Actions retain the Python 3.10/3.12 matrix, syntax check,
  public-release content check, and network-independent test command?
- Do malformed JSON and a non-list `features` member become readable errors
  handled by the pages instead of uncaught exceptions?
- Do normal, empty, and incomplete responses pass through the shared loader,
  and do HTTP, timeout, and connection failures become page-handled errors?
- Does the query URL preserve every required/optional filter and omit unset
  values, and do all four pages share the tested result-limit boundary?
- Does USGS GeoJSON normalize into the expected EnvGeo-Earthquake columns?
- Does an empty USGS GeoJSON response still return a safe empty table with expected columns?
- Can coastline helper data be loaded for map context?
- Do bundled coastlines and both Home README views still load after changing
  the process working directory?
- Do both Advanced upload controls advertise only CSV, TSV, TXT, and XLSX, and
  can the declared `openpyxl` engine round-trip an XLSX workbook?
- Do the actual bilingual Advanced upload helpers normalize one representative
  CSV and safely return an empty result/warning for missing required columns?
- Do all four pages retain valid geographic-boundary points while excluding
  missing, non-numeric, and out-of-range USGS coordinates before plotting?
- Do all four pages wrap longitude, split/preserve lines at the appropriate map
  seam, and convert dateline-adjacent points to nearby local-km coordinates?
- Do both Advanced pages project a short dateline-crossing section, handle
  coincident endpoints, and build a closed corridor polygon consistently?
- Do both Advanced plate-boundary loaders distinguish normal, total failure,
  malformed response, and partial-layer failure while applying the schematic
  fallback only to the Japan preset?
- Do bilingual Home, Simple, and Advanced pages start without exceptions and
  retain their primary headings and paired fetch buttons?
- Does the release candidate contain only approved content, exclude generated
  and private material, avoid secret values and machine-specific paths, use no
  symlinks, and retain valid Markdown links?

Run tests from the `earthquake_map_v030` directory:

```bash
pytest -q
```

`pytest` may create `.pytest_cache/`, and Python may create `__pycache__/`.
Those files are local generated files and are ignored by `.gitignore`.

## Current Scope

The current tests are intentionally deterministic and make no live USGS
requests. They protect importability, earthquake-catalog normalization,
coastlines/offline maps, and page-state recovery. Browser-level interaction,
map rendering, and real-service end-to-end behavior still require separate
confirmation.

Recorded after the 2026-10-08 CI preparation: `178 passed, 0 skipped` locally.
The GitHub Python 3.10/3.12 jobs remain unverified until the workflow is pushed.
