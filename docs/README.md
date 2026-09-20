# EnvGeo-Earthquake Docs

This folder contains user manuals and public development documentation that are
more detailed than the main README.

## Current Documents

- `testing_Japanese.md`  
  Japanese notes explaining the current pytest checks and their limits.

- `release_checklist.md`  
  General checklist before committing, tagging, or publishing a release.

- `manual_Japanese/`
  Japanese user manual for EnvGeo-Earthquake, including quick start, USGS query settings,
  simple/advanced visualizer usage, JMA/NIED comparison, export, and use notes.

- `manual/`
  English user manual with the same workflow, illustrated with English UI screenshots.

- `assets/screenshots/`
  Japanese and English screenshots used by both manuals.

## Maintenance Policy

Update these documents together with code and README changes. In particular:

- update `README.md` and `README_Japanese.md` when user-facing behavior, page names, data sources, citations, limitations, or the EnvGeo-Seawater relationship changes;
- update `testing_Japanese.md` when tests are added, removed, or their purpose changes;
- update `release_checklist.md` when the publication or Git workflow changes.

Generated files such as `__pycache__/`, `.pytest_cache/`, and `.DS_Store` should not be copied into GitHub repositories.
