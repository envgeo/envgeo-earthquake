# EnvGeo-Earthquake TODO

## Current Policy

- Keep the working folder as the source of edits:
  `/Users/toyoho/Documents/study/704-Python/Webアプリ_main134_20230513/Streamlit_EnvGeo2/earthquake_map_v030`
- Copy to the Git clone only after checks:
  `/Users/toyoho/Documents/GitHub/envgeo-earthquake`
- Update README, README_Japanese, Home update history, and `docs/` whenever user-facing behavior, wording, data sources, testing, or workflow changes.
- Keep the app close to EnvGeo-Seawater in tone and workflow, while leaving earthquake-specific logic in the Earthquake layer.

## Near-Term Tasks

- [ ] Run Streamlit and visually confirm Region / hotspot selection behavior after UI changes.
- [ ] Confirm Japanese and English page wording in the browser.
- [ ] Add a small screenshot/manual QA checklist for Simple and Advanced pages.
- [ ] Consider moving Region selection state handling into testable helper functions.
- [ ] Expand tests for longitude wrapping, local km coordinates, and cross-section geometry.
- [ ] Review JMA/NIED comparison upload wording and accepted column names.
- [ ] Decide whether `old/`, `data/`, `__logo__/`, and image assets should be included in the public GitHub repository.

## Shared-Core Candidates

- [ ] Map background selection and attribution notes.
- [ ] Region preset handling.
- [ ] Coastline loading.
- [ ] Longitude wrapping and dateline handling.
- [ ] Local kilometer-coordinate conversion.
- [ ] Cross-section geometry helpers.
- [ ] Source/citation metadata display.
