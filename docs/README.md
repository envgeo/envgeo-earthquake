# EnvGeo-Earthquake Docs

This folder keeps project notes that are more detailed than the public README.

## Current Documents

- `work_log.md`  
  Working log for development decisions, wording changes, UI fixes, and test results.

- `testing_Japanese.md`  
  Japanese notes explaining the current pytest checks and their limits.

- `release_checklist.md`  
  Manual checklist before copying changes to the Git clone, committing, tagging, or publishing.

## Maintenance Policy

Update these documents together with code and README changes. In particular:

- update `README.md` and `README_Japanese.md` when user-facing behavior, page names, data sources, citations, limitations, or the EnvGeo-Seawater relationship changes;
- update `work_log.md` when a meaningful design decision, UI wording change, test change, or Git/GitHub operation happens;
- update `testing_Japanese.md` when tests are added, removed, or their purpose changes;
- update `release_checklist.md` when the publication or Git workflow changes.

Generated files such as `__pycache__/`, `.pytest_cache/`, and `.DS_Store` should not be copied into GitHub repositories.
