# Notices and Third-Party Data Terms

EnvGeo-Earthquake application code is released under the MIT License. See
`LICENSE`.

The MIT License applies to the application source code in this repository. It
does not change the terms, attribution requirements, or redistribution rules of
external data, map tiles, catalog services, or user-uploaded datasets used with
the app.

## External Data and Services

The app can access or display data from the following external providers:

- USGS Earthquake Catalog API / ANSS Comprehensive Catalog
- USGS Tectonic Plate Boundaries service
- OpenStreetMap standard raster tiles (CARTO basemaps are not configured)
- USGS National Map imagery tiles
- Esri World Ocean Base tiles
- Geospatial Information Authority of Japan map tiles
- bundled coordinate tables derived from Natural Earth coastline vectors
- user-supplied JMA or NIED catalog tables

For publications, figures, teaching materials, static exports, redistribution,
or derived datasets, check and follow the current terms and attribution guidance
from each provider.

Relevant source and attribution links are maintained in `README.md` and
`README_Japanese.md`.

## Online Map Attribution

- Standard: `© OpenStreetMap contributors`; follow the OpenStreetMap tile
  usage policy and do not bulk-download/prefetch the standard tiles.
- Satellite: `USDA, USGS The National Map: Orthoimagery`.
- Bathymetry: `Sources: Esri, GEBCO, NOAA, National Geographic, DeLorme, HERE,
  Geonames.org, and other contributors`; not for navigation or safety at sea.
- Topographic: `国土地理院`; static publication or redistribution may require
  a separate check of current GSI terms and procedures.

Provider links and the audit date are recorded in both README languages. These
credits do not replace provider-specific terms for a publication or export.

## User-Supplied JMA / NIED Data

No JMA or NIED catalog file is bundled in this repository or release. The
optional comparison reads a user-selected file for the current session only.

JMA website content generally requires source credit and identification of
editing/processing under its stated terms. NIED Hi-net prohibits redistribution
of downloaded data and hypocenter information; publications derived from the
data must follow its acknowledgement, DOI-citation, and result-reporting rules.
Other organizations' data supplied through Hi-net retain their own conditions.

See `docs/jma_nied_data_responsibilities.md`. Upload acceptance or file-format
conversion does not grant publication or redistribution rights.

## Bundled Natural Earth coastline data

The 50m and 110m coordinate CSVs in `coastline/` are derived from Natural
Earth coastline vector data. Natural Earth states that all versions of its map
data are public domain; permission and attribution are not required. The
project nevertheless uses Natural Earth's suggested acknowledgement:

> Made with Natural Earth. Free vector and raster map data @ naturalearthdata.com.

The retained source workspace identifies both resolutions as Natural Earth
coastline v4.1.0. Exact file hashes, representation and derivation evidence,
source links, provenance limitations, and bilingual terms are recorded in
[`coastline/LICENSE_OR_SOURCE.md`](coastline/LICENSE_OR_SOURCE.md) and
[`coastline/LICENSE_OR_SOURCE_Japanese.md`](coastline/LICENSE_OR_SOURCE_Japanese.md).
