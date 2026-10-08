# Bundled Coastline Data: Source and Terms

[Japanese version](LICENSE_OR_SOURCE_Japanese.md)

Last verified: 2026-10-08

## Files covered

- `world_coastline_coordinates_50m.csv`
- `world_coastline_coordinates_110m.csv`

These files are derived coordinate tables for Natural Earth coastline vector
data version 4.1.0 at 1:50 million and 1:110 million scales. They are bundled only as visual
reference lines for EnvGeo-Earthquake maps and 3D plots; they are not earthquake
observations, official boundaries, navigation data, or hazard products.

## Upstream source

- [Natural Earth 1:50m Physical Vectors](https://www.naturalearthdata.com/downloads/50m-physical-vectors/)
- [Natural Earth 1:110m Physical Vectors](https://www.naturalearthdata.com/downloads/110m-physical-vectors/)
- [Natural Earth Terms of Use](https://www.naturalearthdata.com/about/terms-of-use/)

Natural Earth states that all versions of its raster and vector map data are in
the public domain. Permission and attribution are not required. This project
nevertheless uses the acknowledgement suggested by Natural Earth:

> Made with Natural Earth. Free vector and raster map data @ naturalearthdata.com.

The MIT License in the repository root applies to the EnvGeo-Earthquake source
code. It does not replace or restrict the public-domain status of these derived
Natural Earth data files.

## Local representation and integrity

The original vector geometry was serialized as `Longitude` and `Latitude`
columns. Fully blank rows separate line segments. Original shapefile attributes
and upstream metadata are not contained in the CSVs.

| File | Data rows | Blank separator rows | SHA-256 |
|---|---:|---:|---|
| `world_coastline_coordinates_50m.csv` | 61,844 | 1,428 | `c3d7bee4fb696b011fa34bb13bed0c335c5250eeaf37d8739d77d29a27fe385c` |
| `world_coastline_coordinates_110m.csv` | 5,261 | 133 | `a31df3aeee9dc4195af35a31b0605fdb572c7c7dd7cde17f773c9438f5ec7f3f` |

The corresponding 50m and 110m files in the read-only
EnvGeo-Seawater v1.3.5 workspace were byte-identical during the 2026-10-08
audit. Each application keeps its own copy and has no runtime dependency on the
other.

## Retained derivation evidence

The read-only EnvGeo-Seawater provenance record documents a retained coastline
source workspace whose 50m and 110m source archives identify Natural Earth
coastline version 4.1.0. The archives and corresponding coordinate workbooks
were saved on 2025-01-24. Seawater's 2026-10-03 audit found that both retained
workbooks match the current CSV coordinates, row counts, and missing-coordinate
segment separators; the maximum absolute numeric difference was approximately
`1.42e-14`. Because the Earthquake copies are byte-identical to those audited
Seawater CSVs, this evidence also identifies the bundled Earthquake files as
derived from Natural Earth coastline v4.1.0.

## Provenance limitation

The original Natural Earth raw-download checksums, exact download dates, and a
standalone conversion script were not retained. This record therefore identifies
the distributed artifacts, retained intermediate-workbook relationship, and
upstream release, but does not claim bit-for-bit reconstruction of the original
raw downloads. The currently published Natural Earth download-page version
labels need not match this historical v4.1.0 source workspace.

If the files are regenerated, record the upstream archive filename, Natural
Earth version, download date, raw-download checksum, conversion command/script,
output row counts, and output SHA-256 hashes here before replacing them.

## Accuracy and use limitation

Natural Earth describes these as generalized small-/medium-scale map data and
disclaims responsibility for accuracy or fitness for a particular use. Use the
bundled coordinates only for map context. Do not use them for navigation,
legal-boundary decisions, site-scale distance measurements, or disaster and
hazard decisions.
