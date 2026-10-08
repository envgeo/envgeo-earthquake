# EnvGeo-Earthquake Development and Documentation Workflow

[Japanese version](development_workflow_Japanese.md)

Last updated: 2026-10-08

## At the start of a work session

1. Read the root `PROJECT_STATUS.md`.
2. Read the near-term items in `TODO.md` and the newest entries in both work logs.
3. For release, CI, Zenodo, provenance, or shared-core work, also read
   `publication_audit_2026-10-08.md`.
4. Identify the development folder, public Git clone, and target version.
5. Confirm that the task will not modify or create a dependency on Seawater.

## During work

- Prefer small testable changes over a large UI merge or core extraction.
- Follow the Seawater section-comment convention in Python: use a short
  `English / 日本語` heading for each major section and add paired bilingual
  purpose notes where they materially improve comprehension. Apply the rule to
  new or edited sections instead of rewriting unrelated comments in bulk.
- Keep English/Japanese and Simple/Advanced behavior aligned.
- Mock external APIs in automated tests; CI must not depend on live USGS or tile services.
- Before deleting, renaming, or changing release contents, inspect all references.
- Record unavailable environments and unrun checks as unverified; never report
  them as successful.

## Records to update after work

Always update both work-log languages with the date, purpose, changed scope,
unchanged scope, decisions, exact test commands/results, manual checks, and next
action.

Also update when applicable:

- Both `PROJECT_STATUS` files when state, blockers, evidence, or next action changes.
- Both TODO files when priorities or completion changes.
- Both READMEs and manual trees when public behavior changes.
- Both Home histories for a release or user-visible change.
- Both testing guides when tests or skips change.
- Both release checklists when CI, packaging, GitHub, or Zenodo procedure changes.
- `NOTICE.md` and provenance records when external data, tiles, or assets change.

## Minimum work-log template

```markdown
## YYYY-MM-DD — Work title

- Purpose:
- Changes:
- Explicitly unchanged:
- Verification:
  - `command`: N passed, N skipped, N failed
  - Manual checks:
- Decisions and rationale:
- Remaining work / next action:
```
