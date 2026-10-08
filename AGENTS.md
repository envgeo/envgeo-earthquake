# EnvGeo-Earthquake project instructions

[Japanese version](AGENTS_Japanese.md)

Before changing this project, read these files in order:

0. `LOCAL_WORKSPACE.md` and `LOCAL_WORKSPACE_Japanese.md`, if present locally
1. `PROJECT_STATUS.md` and `PROJECT_STATUS_Japanese.md`
2. `TODO_Japanese.md` (and keep `TODO.md` aligned)
3. both language versions of `docs/development_workflow`
4. the newest entries in both language versions of `docs/work_log`
5. both language versions of `docs/publication_audit_2026-10-08` when working on release, packaging,
   CI, Zenodo, shared-core candidates, uploads, quality checks, or provenance

Project boundaries:

- Preserve current application behavior and features. Add only changes that
  are necessary for stable operation, accurate documentation, testing,
  deployment, or release; do not introduce speculative validation or features.
- Before adding behavior, identify the concrete failure or publication blocker
  it resolves and prefer the smallest tested change.
- EnvGeo-Earthquake must remain independently runnable, testable, deployable,
  and archivable.
- Do not edit `../envgeo_seawater_v130` as part of Earthquake work unless the
  user explicitly requests a separate Seawater change.
- Do not add a runtime dependency on EnvGeo-Seawater or a future EnvGeo Core
  during the current publication-readiness phase.
- Treat shared-core items as candidates only. Keep local implementations and
  assets until both applications have independent regression evidence.
- Keep earthquake-domain behavior in Earthquake: USGS queries, earthquake
  catalog normalization, magnitude/depth/time semantics, plate boundaries,
  and JMA/NIED comparison.
- Do not describe USGS `Status`/`Alert` or earthquake-catalog validation as the
  same quality system as Seawater physical-range quality flags.

Documentation and evidence:

- Follow the EnvGeo-Seawater code-comment style: give every major section a
  concise `English / 日本語` heading and, when needed, a paired bilingual
  purpose note. Apply this to newly added or materially edited sections; do not
  perform unrelated mass comment rewrites.
- Add dated entries to both work-log language files for every material session.
- Update both `PROJECT_STATUS` language files whenever the current state, blockers, verified
  evidence, or next recommended action changes.
- Update both TODO languages when priorities or completion states change.
- Update both user manuals, both READMEs, and the in-app update history when a
  user-facing workflow changes.
- Record exact commands, environments, pass/skip/fail counts, and manual checks.
  Never convert an unrun check into a success statement.
- Keep generated files, caches, credentials, private data, and development-only
  archives out of public release contents.
