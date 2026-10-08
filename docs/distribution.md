# EnvGeo-Earthquake Distribution Policy

[Japanese version](distribution_Japanese.md)

Decision date: 2026-10-08

## Initial Stable Release

The first stable EnvGeo-Earthquake release will use a **source-only GitHub
Release**. In this context, source-only means a complete, versioned application
archive rather than a Python package published to PyPI.

Most users can use the deployed Streamlit web application without installing
anything. A user who needs a local or reproducible copy can download the GitHub
Release archive and run:

```bash
pip install -r requirements.txt
streamlit run home.py
```

The release archive will include the application, bilingual pages and manuals,
runtime requirements, bundled coastline data and provenance, tests, license,
notices, citation metadata, and release notes.

## Outside the Initial DOI Scope

The initial DOI release will not include:

- publication to PyPI;
- an installable wheel or sdist;
- `pip install envgeo-earthquake`;
- a package-specific launcher or command;
- source-tree restructuring solely for packaging.

These additions are not required to deploy the Streamlit app or obtain a Zenodo
DOI. Avoiding them keeps the first release focused on the verified application
and prevents packaging work from changing stable paths or runtime behavior.

## GitHub Release and Zenodo

The tagged GitHub Release will define the versioned public source archive.
Zenodo will archive that release and issue the version DOI and concept DOI.
The GitHub tag, GitHub Release, Zenodo record, `CITATION.cff`, and bilingual
release notes must identify the same version.

## Future Packaging

Installable packaging may be reconsidered after the DOI release if the project
develops a stable import API, a command-line launcher, or a separately versioned
EnvGeo Core. EnvGeo-Earthquake remains standalone and does not require
EnvGeo-Seawater or a future Core at runtime.
