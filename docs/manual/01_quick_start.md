# Quick Start

## Run Locally

From the `earthquake_map_v030` directory, run the app in an environment where its dependencies are installed.

```bash
streamlit run home.py
```

Open the local URL shown in the terminal, normally `http://localhost:8501`.

## Choose a Page

Use the Streamlit sidebar to select a page.

![Page navigation and Simple visualizer](../assets/screenshots/en/simple.png)

*Simple visualizer at startup. Set catalog filters on the left and review the event count and plots on the right.*

- Quick exploration in English: `4D Earthquake Simple`
- Detailed analysis in English: `4D Earthquake Advanced`
- Japanese interface: `4D Earthquake シンプル版` or `4D Earthquake 詳細版`

## Basic Workflow

1. Choose a display region.
2. Set the date/time, magnitude, depth, latitude/longitude, ordering, and maximum event count in `USGS Earthquake API`.
3. Confirm that the event count and visualizations update.
4. Adjust depth range, marker sizes, vertical scale, and color variable in `Visualization`.
5. Switch among 3D/4D, 2D, section, time, comparison, and data views as needed.

## Region Selection

- `Japan and surrounding area`: Japan, trenches, and nearby seismicity.
- `Global`: worldwide large-earthquake patterns and plate boundaries.
- `Additional seismic hotspot presets`: quickly select Indonesia, New Zealand, Chile, the Aleutians, Kamchatka, the Himalaya, the Philippines, and other regions.

A preset initializes the longitude and latitude sliders for that region.

## Recommended Devices

Use a desktop computer for the 3D/4D view. On phones and tablets, the 2D map and data table are easier to operate.

