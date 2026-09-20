# Simple 4D Visualizer Earthquake

The Simple visualizer retrieves a USGS catalog and shows its distribution in 3D/4D and 2D maps.

![Simple visualizer](../assets/screenshots/en/simple.png)

*Query controls, event count, and the 4D hypocenter map are visible together. Drag and zoom to inspect the plot.*

## Common Uses

- Build a quick overview of an earthquake distribution.
- Examine the relationship between magnitude and depth in 3D.
- Inspect event location, size, and depth on a map.
- Export the current USGS catalog to CSV.

## 4D Hypocenter Map

The horizontal axes use local kilometer coordinates and the vertical axis represents hypocenter depth. This makes the horizontal scale easier to interpret geologically than raw longitude and latitude axes.

- Drag to rotate.
- Scroll to zoom.
- Hover over an event to inspect time, place, magnitude, depth, and other values.
- Adjust `3D Z-axis display scale` to compress or emphasize the apparent depth dimension.

## Visualization Settings

- `Displayed depth range (km)`: depth interval shown in plots.
- `3D marker size scale`: 3D event size.
- `2D marker size scale`: 2D event size.
- `3D Z-axis display scale`: apparent vertical exaggeration.
- `Pacific-centered 3D view (180°)`: centers a global view on the Pacific.
- `Colorbar variable`: color by `Magnitude` or `Hypocenter depth`.

## 2D Map

The 2D view automatically zooms to the retrieved catalog. Available basemaps include Standard, Satellite Imagery, Ocean Bathymetry, and GSI Topographic Map. Marker size follows magnitude and color follows the selected colorbar variable.

## CSV Export

Expand `Retrieved earthquake data (CSV)` to review the table and use `Download CSV`.

