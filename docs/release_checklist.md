# Release Checklist

Use this checklist before committing, tagging, or publishing a release.

## Documentation And Metadata

- [ ] Update `README.md` and `README_Japanese.md` when user-facing behavior, page names, sources, limitations, or EnvGeo-Seawater relationship changes.
- [ ] Update `docs/testing_Japanese.md` when tests change.
- [ ] Update Home update history when the change should be visible in the app.
- [ ] Update `requirements.txt`, `requirements-dev.txt`, `.gitignore`, `LICENSE`, or `NOTICE.md` when dependencies, ignored artifacts, or licensing notes change.

## Checks

- [ ] Run pytest:

```bash
pytest -q
```

- [ ] Run syntax check without creating `.pyc` files:

```bash
python -c "import ast, pathlib; files=[pathlib.Path('home.py'), pathlib.Path('envgeo_utils.py'), *pathlib.Path('pages').glob('*.py'), *pathlib.Path('test').glob('*.py')]; [ast.parse(p.read_text(encoding='utf-8'), filename=str(p)) for p in files]; print(f'parsed {len(files)} files')"
```

- [ ] For UI changes, run Streamlit locally and check the affected page manually.

## Files To Exclude

Do not commit:

- `.DS_Store`
- `__pycache__/`
- `.pytest_cache/`
- local secrets
- local development notes
- scratch or archive folders unless intentionally publishing them

## Before Commit

- [ ] Check `git status --short`.
- [ ] Check `git diff --stat`.
- [ ] Make sure generated files are not staged.
- [ ] Commit with a short summary and a description of user-facing/documentation/test changes.
