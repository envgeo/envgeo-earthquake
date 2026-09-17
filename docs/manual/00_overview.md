# Overview

EnvGeo-Earthquake is an interactive explorer for earthquake hypocenter catalogs. Its main data source is the USGS Earthquake Catalog API. You can query by date and time, magnitude, hypocenter depth, and latitude/longitude range.

## Main Capabilities

- Inspect hypocenter distributions on a 2D map.
- Explore depth in a 3D/4D view.
- Color events by magnitude or hypocenter depth.
- Switch among Japan, global, and major seismic-hotspot presets.
- Define an arbitrary A-B section through a subduction zone or other area.
- Count events by depth with a depth profile.
- Review activity through time with a histogram.
- Upload JMA/NIED-style catalog tables and compare them with USGS data.
- Download the current USGS catalog as CSV.

## Page Types

### Simple

`4D Earthquake Simple` retrieves a USGS catalog and displays 3D/4D and 2D hypocenter maps. Use it to build a quick overview of an earthquake distribution.

### Advanced

`4D Earthquake Advanced` adds plate boundaries, an arbitrary cross-section, a depth profile, a time histogram, and JMA/NIED comparison. It is the better choice for research, teaching, and detailed exploration.

## Important Notice

Earthquake records may include preliminary values that are revised later. Use official information from USGS, JMA, local government, and emergency agencies for public-safety decisions.

Plate boundaries are schematic. Do not treat them as official fault traces, hazard zones, or a basis for emergency decisions.

