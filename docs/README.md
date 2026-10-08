# EnvGeo-Earthquake Docs

[Japanese version](README_Japanese.md)

This folder contains user manuals and public development documentation that are
more detailed than the main README.

## Current Documents

- `../PROJECT_STATUS.md` / `../PROJECT_STATUS_Japanese.md`  
  Start here when resuming work. It records the current release state,
  boundaries, blockers, verified evidence, and next recommended action.

- `development_workflow.md` / `development_workflow_Japanese.md`  
  Maintenance manual describing which logs, manuals, TODO files, and release
  records must be updated after each kind of change.

- `work_log_English.md` / `work_log.md`  
  Chronological work log. New entries must include exact verification evidence
  and any checks that could not be run.

- `publication_audit_2026-10-08.md` / `publication_audit_2026-10-08_Japanese.md`  
  Read-only Seawater/Earthquake comparison, shared-core classification,
  publication blockers, and the minimal GitHub Release / Zenodo plan.

- `publication_roadmap.md` / `publication_roadmap_Japanese.md`  
  Ordered master task list from standalone cleanup through GitHub Release,
  Zenodo DOI, and the later Core review.

- `public_release_scope.md` / `public_release_scope_Japanese.md`  
  The approved include/exclude boundary for the first stable public release.

- `../coastline/LICENSE_OR_SOURCE.md` / `../coastline/LICENSE_OR_SOURCE_Japanese.md`  
  Natural Earth v4.1.0 source, public-domain terms, integrity hashes, retained
  derivation evidence, and provenance limitations for the bundled coastline CSVs.

- `earthquake_validation.md` / `earthquake_validation_Japanese.md`  
  Minimal, behavior-preserving safeguards for USGS retrieval and user uploads;
  speculative catalog-quality features are explicitly deferred.

- `jma_nied_data_responsibilities.md` / `jma_nied_data_responsibilities_Japanese.md`  
  Provider-specific source, processing, acknowledgement, DOI, result-reporting,
  and redistribution responsibilities for optional user-supplied catalogs.

- `testing.md` / `testing_Japanese.md`  
  Notes explaining the current pytest checks and their limits.

- `release_checklist.md` / `release_checklist_Japanese.md`  
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

- begin each new development session with both `PROJECT_STATUS` languages and the latest
  work-log entries;
- add a dated entry to both work-log languages after every material session;
- update both `PROJECT_STATUS` languages when blockers, verified evidence, or the next
  recommended action changes;
- update `README.md` and `README_Japanese.md` when user-facing behavior, page names, data sources, citations, limitations, or the EnvGeo-Seawater relationship changes;
- update both testing guides when tests are added, removed, or their purpose changes;
- update both release checklists when the publication or Git workflow changes.

EnvGeo-Earthquake must remain independently runnable and must not acquire a
runtime dependency on EnvGeo-Seawater during the publication-readiness phase.
Do not edit the Seawater project as a side effect of Earthquake maintenance.

Generated files such as `__pycache__/`, `.pytest_cache/`, and `.DS_Store` should not be copied into GitHub repositories.
