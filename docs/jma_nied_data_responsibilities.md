# JMA / NIED Uploaded-Data Responsibilities

[Japanese version](jma_nied_data_responsibilities_Japanese.md)

Last verified: 2026-10-08

## Scope

This record applies to the optional Advanced-page comparison of a file supplied
by the user. EnvGeo-Earthquake does not automatically retrieve JMA or NIED
catalogs, bundle them in the repository or release archive, or intentionally
save an uploaded file beyond the current Streamlit session.

The application accepting a file does not establish permission to use,
transform, publish, or redistribute it. The user remains responsible for the
exact source and terms. Converting a file to CSV or XLSX does not change those
rights or obligations.

## JMA

JMA states that website content may generally be used under the Public Data
License 1.0 unless a specific notice says otherwise. Users must:

- cite the JMA source and relevant page URL;
- state when the content has been edited or processed;
- avoid presenting edited information as if JMA or the Government of Japan
  created it; and
- check and clear any third-party rights or source-specific terms.

The Seismological Bulletin catalog usage page explains that the unified
analysis includes observations supplied by NIED, universities, research
institutes, local authorities, and other contributors. Preserve the relevant
provider acknowledgement when the selected catalog requires it.

Official references:

- [JMA website terms of use](https://www.jma.go.jp/jma/en/copyright.html)
- [Seismological Bulletin of Japan](https://www.data.jma.go.jp/eqev/data/bulletin/index_e.html)
- [Bulletin catalog usage notes](https://www.data.jma.go.jp/eqev/data/bulletin/readme_j.html)

## NIED Hi-net

NIED Hi-net guidance is more restrictive than the general JMA website terms.
It states that data and hypocenter information downloaded from the Hi-net site
must not be redistributed. Users may publish their own results derived from the
data, subject to the stated conditions. Users must:

- obtain or register for data through the provider rather than receiving an
  unauthorized copy from another person;
- identify all contributing organizations in resulting publications or reports;
- cite the NIED Hi-net DOI for work using Hi-net data;
- follow separate rules, and obtain prior permission where required, for data
  contributed by JMA, universities, or other organizations; and
- report resulting publications, reports, educational use, consulting, or
  other outcomes to the NIED Data Management Center as requested.

Recommended NIED Hi-net reference:

> National Research Institute for Earth Science and Disaster Resilience (2019), NIED Hi-net, National Research Institute for Earth Science and Disaster Resilience, https://doi.org/10.17598/NIED.0003

Official references:

- [How to use the Hi-net data](https://www.hinet.bosai.go.jp/about_data/?LANG=en)
- [Hi-net FAQ on redistribution](https://www.hinet.bosai.go.jp/faq/?LANG=en)

## EnvGeo-Earthquake Release Decision

- No JMA or NIED catalog file is part of the source repository, GitHub Release,
  package, or planned Zenodo archive.
- The comparison remains optional and is not a release/DOI gate.
- The app performs no provider authentication, permission check, or automated
  rights determination.
- Uploaded values may be visualized and summarized in the current session, but
  users must not treat that processing as permission to republish source data.
- Public figures, derived tables, teaching materials, and publications must
  preserve the required source, processing statement, acknowledgements,
  citations, and result-reporting obligations.

This is a project compliance record, not legal advice. Recheck the provider's
current terms for the exact dataset before publication or redistribution.
