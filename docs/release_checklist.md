# Release / Git Copy Checklist

Use this checklist before copying changes from the working folder to the Git clone or before committing.

## Working Folder

- [ ] Work in `/Users/toyoho/Documents/study/704-Python/Webアプリ_main134_20230513/Streamlit_EnvGeo2/earthquake_map_v030`.
- [ ] Update `README.md` and `README_Japanese.md` when user-facing behavior, page names, sources, limitations, or EnvGeo-Seawater relationship changes.
- [ ] Update `docs/work_log.md` for meaningful changes.
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

## Copy To Git Clone

Git clone path:

```text
/Users/toyoho/Documents/GitHub/envgeo-earthquake
```

Copy only source/docs/test files. Do not copy:

- `.DS_Store`
- `__pycache__/`
- `.pytest_cache/`
- local secrets
- old local scratch folders unless intentionally publishing them

## Before Commit

- [ ] Check `git status --short`.
- [ ] Check `git diff --stat`.
- [ ] Make sure generated files are not staged.
- [ ] Commit with a short summary and a description of user-facing/documentation/test changes.
