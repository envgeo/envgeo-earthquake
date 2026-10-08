# EnvGeo-Earthquake

EnvGeo-Earthquake is an interactive platform for exploring earthquake
hypocenter catalogs in research and education.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/python-3.10--3.12-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Current development version:** 0.3.2 (2026-09-22)

The single runtime version source is `envgeo_utils.APP_VERSION` with
`envgeo_utils.APP_VERSION_DATE`; active Home and visualizer pages read it
directly instead of redefining version strings.

Bundled coastline CSVs and the Home README views are resolved from source-file
locations rather than the process working directory.

This application adapts the spatial 3D/4D visualization workflow of
**EnvGeo-Seawater** (https://envgeo.h.kyoto-u.ac.jp/sw_jpn/) to earthquake
catalog data. EnvGeo-Seawater was developed for interactive visualization of
oceanographic and marine geochemical datasets; EnvGeo-Earthquake applies the
same exploratory, source-aware approach to hypocenter catalogs.

The app is intended to support **exploratory data analysis**, teaching, and
reproducible research workflows. It is not an official earthquake alert,
tsunami warning, hazard assessment, or disaster-response system.

Illustrated user manuals: [English](docs/manual/README.md) | [Japanese](docs/manual_Japanese/README.md)

The minimal, behavior-preserving catalog validation policy is documented in
[English](docs/earthquake_validation.md) and
[Japanese](docs/earthquake_validation_Japanese.md). It limits new checks to
crash prevention, readable errors, and safe handling of user uploads.

---

## Overview

EnvGeo-Earthquake fetches earthquake hypocenter data from the USGS Earthquake
Catalog API and visualizes the results through EnvGeo-style 2D, 3D, 4D, and
section-based workflows:

- 2D/3D maps with magnitude-linked (default) or fixed marker sizing
- 3D/4D hypocenter plots with depth, magnitude, and colorbar controls
- user-defined A-B cross-sections with a section-location map
- depth-frequency profiles
- time-series histograms
- optional Japan-focused comparison with uploaded JMA/NIED catalog tables in the Advanced page
- plate-boundary overlays from USGS where available

The project is also used as a testbed for identifying which parts of the
EnvGeo-Seawater workflow can become shared geoscience utilities, such as data
normalization, source-aware metadata handling, map presets, local coordinate
conversion, 3D/4D layout helpers, and cross-section tools.



---

## Main Pages

The Streamlit app uses `home.py` for the overview, data-source, manual,
update-log, and README tabs. The `pages/` directory contains English and
Japanese versions of the earthquake visualization workflows:

- `pages/54_🇺🇸_4D_Earthquake_Simple.py`
  English focused USGS hypocenter visualizer.

- `pages/55_🇺🇸_4D_Earthquake_Advanced.py`
  English advanced earthquake visualizer with plate boundaries, 2D/3D maps,
  cross-section, depth profile, time histogram, and JMA/NIED comparison tools.

- `pages/56_🇯🇵_4D_Earthquake_シンプル版.py`
  Japanese focused USGS hypocenter visualizer.

- `pages/57_🇯🇵_4D_Earthquake_詳細版.py`
  Japanese advanced earthquake visualizer with plate boundaries, 2D/3D maps,
  cross-section, depth profile, time histogram, and JMA/NIED comparison tools.


---

## Key Features

- USGS Earthquake Catalog API access using GeoJSON
- filters for UTC date/time, magnitude, hypocenter depth, latitude, longitude,
  order, and maximum event count
- main-screen region selection for Japan and surrounding area or global view
- magnitude-linked (default) or fixed marker sizing, with direct scale controls
  up to 10 times for 2D, 3D, and Advanced cross-section views; linked mode has
  an adjustable visual M7:M4 marker-diameter ratio from 1:1 to 30:1 (default 20:1)
- colorbar variable selection between magnitude and hypocenter depth
- EnvGeo-style 3D/4D view using local kilometer coordinates so horizontal
  scale is more physically meaningful than raw degree axes
- concise in-app Plotly guidance for drag rotation, pan/zoom/reset tools, and
  Shift/Control/Option (Alt)/Command plus mouse camera operation
- depth-axis scaling up to 1,000 km
- plate-boundary overlays from the USGS Tectonic Plate Boundaries service
- user-defined cross-section and depth-profile tools
- map showing the selected A-B cross-section line and section width
- time-series histogram of earthquake occurrence
- CSV export of the selected USGS catalog records
- warning when the selected query reaches the 20,000-event API limit
- concise source and data-use notes in the app
- PC recommendation for 3D display and 2D recommendation for smartphones/tablets

---

## Relationship to EnvGeo-Seawater

EnvGeo-Earthquake is intentionally kept close to EnvGeo-Seawater in structure,
terminology, and visual workflow. The two applications currently remain
separate, but future refactoring should treat the following as candidates for a
shared EnvGeo core:

- standardized geoscience column names and unit conventions
- source and citation metadata displayed alongside data products
- map background, regional preset, and coastline helper functions
- longitude wrapping and local kilometer-coordinate conversion
- reusable 3D/4D layout helpers
- cross-section geometry and depth-profile workflows
- user-upload validation and comparison-table normalization

Generic input-safety helpers may later become Core candidates, but scientific
review of USGS catalog values is not a current Earthquake or Core requirement.

Earthquake-specific logic, such as USGS catalog queries, JMA/NIED comparison
details, hypocenter terminology, and seismic-source limitations, should remain
in the earthquake layer unless the same pattern is needed by other EnvGeo
applications.

EnvGeo-Earthquake remains independently runnable and does not require
EnvGeo-Seawater or a future shared core at runtime.

---

## Data Sources and Attribution

### USGS Earthquake Catalog API

Primary earthquake hypocenter data are accessed from:

- USGS Earthquake Catalog API / FDSN Event Web Service  
  https://earthquake.usgs.gov/fdsnws/event/1/

The app uses the `query` method with:

- `format=geojson`
- `eventtype=earthquake`
- `starttime`
- `endtime`
- `minmagnitude`, `maxmagnitude`
- `mindepth`, `maxdepth`
- `minlatitude`, `maxlatitude`
- `minlongitude`, `maxlongitude`
- `orderby`
- `limit`

The USGS API documentation states that the service implements the FDSN Event
Web Service and supports query parameters for time, geographic bounds,
magnitude, depth, order, and a result limit. The service limit is 20,000 events;
the app therefore warns the user when a query reaches the selected limit.

Recommended catalog citation:

> U.S. Geological Survey. (2017). Advanced National Seismic System (ANSS)
> Comprehensive Catalog. U.S. Geological Survey.
> https://doi.org/10.5066/F7MS3QZH

The same catalog citation is defined once in `envgeo_utils.py` and reused by
both Home pages and all four active visualizer pages to prevent bilingual drift.

Additional USGS links:

- ANSS / USGS FDSN data-center record  
  https://www.fdsn.org/datacenters/detail/USGS/
- USGS Earthquake Hazards Program  
  https://www.usgs.gov/programs/earthquake-hazards
- USGS Search Earthquake Catalog  
  https://earthquake.usgs.gov/earthquakes/search/
- USGS Latest Earthquakes  
  https://www.usgs.gov/tools/latest-earthquakes

### USGS data credit and preliminary-data note

USGS-authored or USGS-produced data and information are generally considered to
be in the U.S. public domain, and USGS requests proper credit when its products,
publications, or websites are used. However, earthquake catalog systems can
include information contributed by multiple networks or agencies, and some
non-USGS materials on USGS websites may have separate copyright restrictions.
For publication or redistribution, cite the USGS/ANSS catalog and also follow
any contributor-specific acknowledgement required by the specific catalog or
table being used.

- USGS Copyrights and Credits  
  https://www.usgs.gov/information-policies-and-instructions/copyrights-and-credits

Earthquake information can be preliminary and may be revised. This app therefore
states that earthquake data may be updated and that official agencies should be
used for emergency response and public-safety decisions.

- USGS Earthquake Notification Service disclaimer, included here as a related
  USGS note about preliminary earthquake information  
  https://earthquake.usgs.gov/ens/help_disclaimer

### Plate-boundary data

Plate-boundary overlays are loaded from:

- USGS Tectonic Plate Boundaries ArcGIS REST service  
  https://earthquake.usgs.gov/arcgis/rest/services/eq/map_plateboundaries/MapServer

The app uses:

- `Plates (1)`
- optional `Microplates (0)`

The USGS plate-boundary service metadata lists the following sources:

- USGS Seismicity of the Earth Map Series, as cited in the USGS service metadata  
  https://earthquake.usgs.gov/earthquakes/byregion/
- Bird, P. (2003). An updated digital model of plate boundaries.
  *Geochemistry, Geophysics, Geosystems*, 4(3), 52 pp.  
  https://doi.org/10.1029/2001GC000252
- DeMets, C., Gordon, R. G., & Argus, D. F. (2010). Geologically current
  plate motions. *Geophysical Journal International*, 181, 1-80.  
  https://doi.org/10.1111/j.1365-246X.2009.04491.x

Plate-boundary locations are approximate and are used as educational/research
context lines. They should not be used as official fault traces, hazard-zone
boundaries, or disaster-response information.

If the USGS plate-boundary service cannot be reached, the app can show a small
Japan-area fallback set of approximate schematic lines for trenches and troughs.
Those fallback lines are visual guides only and are not a formal dataset.

### JMA and NIED comparison data

This is an optional Advanced-page feature and is not required for the main USGS
visualization workflow or the first stable release/DOI.

The app does **not** automatically scrape JMA or NIED services. Instead, it
provides a comparison interface where the user can upload a catalog table
obtained and checked by the user.

Supported upload formats are CSV, TSV, TXT, and modern Excel `.xlsx` files.
The legacy binary Excel `.xls` format is intentionally not advertised because
its separate reader dependency is not part of the runtime environment.

Relevant official references:

- JMA Earthquake Information issued by Japan Meteorological Agency  
  https://www.data.jma.go.jp/eqev/data/en/guide/earthinfo.html
- JMA Seismological Bulletin of Japan  
  https://www.data.jma.go.jp/eqev/data/bulletin/index_e.html
- JMA Hypocenter file format  
  https://www.data.jma.go.jp/eqev/data/bulletin/data/format/fmthyp_e.html
- NIED Hi-net data guidance  
  https://www.hinet.bosai.go.jp/about_data/?LANG=en
- JMA website terms of use  
  https://www.jma.go.jp/jma/en/copyright.html
- NIED Hi-net redistribution FAQ  
  https://www.hinet.bosai.go.jp/faq/?LANG=en

NIED Hi-net guidance describes the automatic hypocenter catalog as a quick
report and advises users to refer to official JMA earthquake information. It
also notes that the JMA unified catalog is available through the Hi-net website
for registered users and recommends using the final JMA Seismological Bulletin
where appropriate.

JMA website content generally requires source credit and a statement when it
has been edited or processed; users must also check third-party rights and any
source-specific notice. NIED Hi-net prohibits redistribution of downloaded
data and hypocenter information. Results derived from Hi-net data may be
published only under its stated conditions, including provider acknowledgement,
the NIED Hi-net DOI, and reporting results to NIED. Data contributed through
Hi-net by JMA, universities, or other organizations remain subject to each
provider's rules.

NIED Hi-net reference:

> National Research Institute for Earth Science and Disaster Resilience (2019), NIED Hi-net, National Research Institute for Earth Science and Disaster Resilience, https://doi.org/10.17598/NIED.0003

The full bilingual responsibility record is in
[`docs/jma_nied_data_responsibilities.md`](docs/jma_nied_data_responsibilities.md).
Users must not use the comparison upload as a mechanism to republish source data.

Uploaded contents are read for the current Streamlit session and are not
intentionally written to a persistent application data store by this app.
No JMA/NIED catalog file is bundled in the repository or planned release archive.

### Base maps and display layers

The app uses several map background styles through Plotly Mapbox layers. The
following attribution review was performed on 2026-10-08:

- Standard map: Plotly's built-in OpenStreetMap standard raster style. The
  interactive layer displays `© OpenStreetMap contributors`. CARTO basemaps
  are not configured. Follow the OpenStreetMap copyright/license and tile
  usage policy; do not bulk-download or prefetch these tiles for offline use.  
  https://www.openstreetmap.org/copyright  
  https://operations.osmfoundation.org/policies/tiles/
- Satellite map: USGS National Map imagery tiles. Runtime credit:
  `USDA, USGS The National Map: Orthoimagery`. The service metadata notes that
  the imagery includes USDA NAIP and may include other source imagery.  
  https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer
- Bathymetry map: Esri World Ocean Base tiles. Runtime credit:
  `Sources: Esri, GEBCO, NOAA, National Geographic, DeLorme, HERE,
  Geonames.org, and other contributors`. This background is not for navigation
  or safety at sea. Recheck Esri guidance for publication or static exports.  
  https://services.arcgisonline.com/arcgis/rest/services/Ocean/World_Ocean_Base/MapServer  
  https://support.esri.com/en-us/knowledge-base/what-is-the-correct-way-to-cite-an-arcgis-online-basema-000012040
- Contour/topographic map: Geospatial Information Authority of Japan (GSI)
  standard tiles. Runtime credit: `国土地理院`. Real-time display is used here;
  recheck the current GSI terms and any required procedure for static
  publication or redistribution.  
  https://maps.gsi.go.jp/development/ichiran.html  
  https://maps.gsi.go.jp/help/termsofuse.html



### Source certainty audit

The following status was checked against official or provider pages on
2026-05-04.

- USGS FDSN Event Web Service/API parameters, GeoJSON output,
  `eventtype=earthquake`, depth/magnitude/location/time filters, and the
  20,000-event service limit are documented by USGS.
- The ANSS Comprehensive Catalog citation and DOI
  `10.5066/F7MS3QZH` are listed by the FDSN USGS data-center record.
- The plate-boundary overlay is an official USGS ArcGIS REST
  service with `Plates (1)` and `Microplates (0)` layers. Its own metadata cites
  Bird (2003), DeMets et al. (2010), and the USGS Seismicity of the Earth Map
  Series.
- JMA and NIED links are official provider pages. The app does
  not scrape them; it only accepts user-uploaded comparison tables.
- For papers, figures, printed handouts, or static
  exports, re-check each tile provider's current terms and required attribution.
- Coastline data used for plotting were derived from Natural Earth public-domain
  coastline v4.1.0. See the bilingual [source and terms record](coastline/LICENSE_OR_SOURCE.md)
  for file hashes, retained intermediate-workbook evidence, and the limitations
  of the historical raw-download record.

---

## Installation

This project is designed for Python 3.10 to 3.12.

```bash
pip install -r requirements.txt
```

For local testing, install the development requirements:

```bash
pip install -r requirements-dev.txt
```

## Distribution

The first stable release will be distributed as a complete source archive
through GitHub Release and archived by Zenodo. It will not be published to PyPI
or reorganized as an installable wheel for the initial DOI release. See the
[distribution policy](docs/distribution.md) for the scope and rationale.

---

## Quick Start

```bash
streamlit run home.py
```

Then open the local URL shown in the terminal, usually:

```text
http://localhost:8501
```

Recommended workflow:

1. Open `4D Visualizer Earthquake Advanced`.
2. Select `Japan and surrounding area` or `Global`.
3. Set the sidebar filters for time, magnitude, depth, and geographic bounds.
4. Fetch/update the USGS query.
5. Review the 2D map first.
6. Use the 3D/4D map on a PC for depth structure.
7. Use cross-section and depth-profile tools for subduction-zone or regional
   seismicity analysis.
8. Use the time histogram to examine temporal clustering.
9. Use the JMA/NIED comparison tools in the Advanced page with manually uploaded
   catalog data when comparing Japan-area catalogs.

---

## API Usage

The USGS data loader is implemented in `envgeo_utils.py`.

```python
from datetime import datetime, timezone

import envgeo_utils

df = envgeo_utils.load_usgs_earthquake_data(
    starttime=datetime(2026, 1, 1, tzinfo=timezone.utc),
    endtime=datetime(2026, 1, 31, tzinfo=timezone.utc),
    minmagnitude=4.5,
    mindepth=0,
    maxdepth=700,
    minlatitude=20,
    maxlatitude=50,
    minlongitude=120,
    maxlongitude=155,
    limit=2000,
    orderby="time",
)
```

Returned columns include:

- `EventID`
- `DateTime_UTC`
- `Time_UTC`
- `Longitude_degE`
- `Latitude_degN`
- `Depth_km`
- `Magnitude`
- `MagnitudeType`
- `Place`
- `URL`

The generated USGS query URL is stored in:

```python
df.attrs["query_url"]
```

---

## Directory Structure

- `home.py`  
  Main Streamlit entry point for EnvGeo-Earthquake.

- `envgeo_utils.py`  
  Shared low-level utilities, including USGS API loading, GeoJSON normalization,
  mapping styles, coastline loading, and cache clearing.

- `pages/54_🇺🇸_4D_Earthquake_Simple.py`  
  English focused earthquake visualizer.

- `pages/55_🇺🇸_4D_Earthquake_Advanced.py`  
  English advanced earthquake visualizer, including JMA/NIED comparison tools.

- `pages/56_🇯🇵_4D_Earthquake_シンプル版.py`  
  Japanese focused earthquake visualizer.

- `pages/57_🇯🇵_4D_Earthquake_詳細版.py`  
  Japanese advanced earthquake visualizer, including JMA/NIED comparison tools.

- `coastline/`  
  Local 50m and 110m Natural Earth-derived coastline coordinate CSV files for
  reference overlays, with bilingual source/terms records.

- `test/`  
  Deterministic tests for utility imports, USGS GeoJSON contracts, coastlines,
  offline maps, and page-state recovery.

- `requirements.txt`  
  Runtime dependencies for the Streamlit app.

- `requirements-dev.txt`  
  Runtime dependencies plus local test tools.

- `docs/`  
  Bilingual user manuals, screenshots, validation notes, provider-responsibility
  records, and testing documentation.

---

## Documentation Notes

The public documentation covers application use, data sources, limitations,
validation behavior, and testing. Internal handoff records and local development
logs are intentionally excluded from the public repository.

---

## Reproducibility and Caching

USGS earthquake queries are made through explicit URL parameters and the query
URL is displayed in the app. Downloaded results can be exported as CSV.

Streamlit caching is used to reduce repeated API access. Cached USGS earthquake
queries use a time-to-live of 1 hour, and plate-boundary queries use a
time-to-live of 24 hours. The sidebar includes a cache-clear/reload button.

Because earthquake catalogs can be revised, exact reproduced results may change
when USGS updates event parameters or when a query is rerun at a later date.

---

## Limitations

- This app is not an official alert or disaster-response product.
- USGS event data may be preliminary and may be revised.
- The USGS FDSN event service has a 20,000-event query limit.
- Large global queries can be slow in the browser because many points are drawn
  interactively.
- Plotly 3D interaction is best on a PC; 2D maps are recommended for
  smartphones and tablets.
- Plate boundaries are approximate context lines.
- JMA/NIED comparison depends on user-uploaded data and user-side compliance
  with provider terms.
- Local coastline reference files are used only for visualization context.

---

## Related Official Tools

- USGS Latest Earthquakes  
  https://www.usgs.gov/tools/latest-earthquakes
- USGS Search Earthquake Catalog  
  https://earthquake.usgs.gov/earthquakes/search/
- JMA earthquake information  
  https://www.data.jma.go.jp/eqev/data/en/guide/earthinfo.html
- JMA Seismological Bulletin of Japan  
  https://www.data.jma.go.jp/eqev/data/bulletin/index_e.html
- NIED Hi-net  
  https://www.hinet.bosai.go.jp/?LANG=en

---

## Development Reference

The USGS earthquake API implementation was informed by the official USGS
documentation and by the following introductory article:

- ssfuno, "PyGMTとUSGSのAPIを使って地震の分布を描いてみる"  
  https://zenn.dev/ssfuno/articles/56e2577ee794f3

The official USGS documentation and provider pages listed above should be used
as the primary references for data access, terms, and citations.

---

## Citation

If you use this application in teaching material, presentations, or research
workflows, please cite both the app and the original data providers.

Suggested app citation:

> Ishimura, T. (2026). EnvGeo-Earthquake: An interactive earthquake
> hypocenter exploration app based on EnvGeo-Seawater. Kyoto University.

Required or recommended data citations should include:

> U.S. Geological Survey. (2017). Advanced National Seismic System (ANSS)
> Comprehensive Catalog. U.S. Geological Survey.
> https://doi.org/10.5066/F7MS3QZH

When plate boundaries are shown, also cite:

> Bird, P. (2003). An updated digital model of plate boundaries.
> *Geochemistry, Geophysics, Geosystems*, 4(3), 52 pp.
> https://doi.org/10.1029/2001GC000252

> DeMets, C., Gordon, R. G., & Argus, D. F. (2010). Geologically current
> plate motions. *Geophysical Journal International*, 181, 1-80.
> https://doi.org/10.1111/j.1365-246X.2009.04491.x

For Japan-area catalog comparison, cite and acknowledge JMA/NIED according to
the provider guidance for the specific dataset used.

---

## License

The application code is released under the MIT License. Data accessed from
external services remain subject to the terms, policies, and attribution
guidance of their original providers.

See `NOTICE.md` for the separation between application-code licensing and
external data/provider terms.
