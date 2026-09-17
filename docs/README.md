# EnvGeo-Earthquake Docs

This folder keeps project notes that are more detailed than the public README.

## Current Documents

- `work_log.md`  
  Working log for development decisions, wording changes, UI fixes, and test results.

- `testing_Japanese.md`  
  Japanese notes explaining the current pytest checks and their limits.

- `release_checklist.md`  
  Manual checklist before copying changes to the Git clone, committing, tagging, or publishing.

- `manual_Japanese/`
  Japanese user manual for EnvGeo-Earthquake, including quick start, USGS query settings,
  simple/advanced visualizer usage, JMA/NIED comparison, export, and use notes.

- `manual/`
  English user manual with the same workflow, illustrated with English UI screenshots.

- `assets/screenshots/`
  Japanese and English screenshots used by both manuals.

- `capture_manual_screenshots.mjs`
  Playwright script for regenerating the manual screenshots from a running local app.

## Regenerating Manual Screenshots

Start the app, then run the capture script in an environment with Playwright and Chromium installed:

```bash
streamlit run home.py
APP_URL=http://127.0.0.1:8501 node docs/capture_manual_screenshots.mjs
```

Set `CHROME_PATH` when Playwright should use an existing Chrome executable instead of its bundled Chromium.

## Maintenance Policy

Update these documents together with code and README changes. In particular:

- update `README.md` and `README_Japanese.md` when user-facing behavior, page names, data sources, citations, limitations, or the EnvGeo-Seawater relationship changes;
- update `work_log.md` when a meaningful design decision, UI wording change, test change, or Git/GitHub operation happens;
- update `testing_Japanese.md` when tests are added, removed, or their purpose changes;
- update `release_checklist.md` when the publication or Git workflow changes.

Generated files such as `__pycache__/`, `.pytest_cache/`, and `.DS_Store` should not be copied into GitHub repositories.
