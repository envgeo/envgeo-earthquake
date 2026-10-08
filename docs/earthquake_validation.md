# EnvGeo-Earthquake Minimal Validation Policy

[Japanese version](earthquake_validation_Japanese.md)

Status: revised on 2026-10-08 to prioritize preservation of current behavior.

## Principle

EnvGeo-Earthquake primarily retrieves and displays records from the official
USGS Earthquake Catalog API. The app does not need a separate scientific
quality-grading system for those records. Publication work must preserve the
current features and add only checks needed to prevent crashes, misleading
output, or unusable uploads.

USGS `status`, `alert`, magnitude, depth, origin time, and event ID remain
source values. They are not converted into EnvGeo-Seawater quality flags.

## Minimum checks for USGS data

Only the following safeguards are required:

1. Handle connection failures, timeouts, HTTP errors, and malformed JSON
   without crashing the Streamlit page.
2. Confirm that the response contains a `features` list before normalization.
3. Convert the coordinates and properties already used by the current plots;
   exclude missing, non-numeric, or GeoJSON-out-of-range longitude/latitude
   before plotting so such records cannot crash or distort a plot.
4. Preserve the existing empty-result and 20,000-event-limit notices.
5. Preserve the notice that USGS records are preliminary and may be revised.

The app trusts values supplied by the USGS service within this workflow. A new
severity framework, duplicate Event ID manager, per-record issue-code system,
or independent scientific review of USGS values is not a current publication
requirement.

## Optional JMA/NIED-style uploads

This existing Advanced-page comparison is optional. It is useful for some
Japan-focused research workflows, but it is not part of the core USGS display
workflow and is not a gate for the first stable release or Zenodo DOI. It is
retained to preserve current behavior, without expanding its scope.

The existing basic checks are sufficient:

- Accept only the advertised CSV, TSV, TXT, and XLSX formats.
- Require the current longitude, latitude, depth, and magnitude columns using
  the accepted English or Japanese aliases.
- Convert the required values to numeric form and show a clear error when the
  file cannot be read or the required columns are missing.
- Keep optional time and place fields optional.
- Do not add a new catalog-quality score or silently claim that an uploaded
  file has been scientifically validated.

The app reads the selected file for the current Streamlit session and does not
intentionally write it to a persistent application data store. The user remains
responsible for the source file and provider terms.

## Deferred unless a concrete defect requires them

- duplicate Event ID reporting;
- `updated` versus origin-time consistency checks;
- a multi-level validation severity and stable issue-code framework;
- per-view validation dashboards and issue-count exports;
- stricter bounds beyond what is required to keep the current plots safe;
- changing timezone interpretation or normalization behavior without a
  separately reviewed requirement and regression tests.

These ideas may be reconsidered later, but they are not gates for the first
stable Earthquake release or Zenodo DOI.

## Implementation rule

Before adding any validation code, demonstrate the concrete failure it prevents
with a focused test. Prefer a small guard in the existing workflow over a new
validation subsystem. Do not change normal USGS display results unless a
verified defect requires it.

## Authoritative references

- [USGS GeoJSON Summary Format](https://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php)
- [USGS FDSN Event Web Service](https://earthquake.usgs.gov/fdsnws/event/1/)
- [JMA Hypocenter Record Format](https://www.data.jma.go.jp/eqev/data/bulletin/data/format/hypfmt_e.html)
- [NIED Hi-net data guidance](https://www.hinet.bosai.go.jp/about_data/?LANG=en)
