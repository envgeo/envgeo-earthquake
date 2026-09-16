# Test Notes

This folder contains small `pytest` checks for EnvGeo-Earthquake.

In simple terms, each test is an automatic checklist item. For example:

- Can Python import the main utility module?
- Does the utility module expose version information?
- Do inherited Seawater helper functions still behave when their optional data files are available?
- Does the Earthquake app skip inherited Seawater dataset checks when those files are not bundled?
- Does USGS GeoJSON normalize into the expected EnvGeo-style earthquake columns?
- Does an empty USGS GeoJSON response still return a safe empty table with expected columns?
- Can coastline helper data be loaded for map context?

Run tests from the `earthquake_map_v030` directory:

```bash
pytest -q
```

`pytest` may create `.pytest_cache/`, and Python may create `__pycache__/`.
Those files are local generated files and are ignored by `.gitignore`.

## Current Scope

The current tests are intentionally small. They protect importability, inherited utility behavior, and USGS catalog normalization. Browser-level Streamlit behavior, map rendering, and real API access still require manual confirmation.
