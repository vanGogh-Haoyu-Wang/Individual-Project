# CT07–Peak_Freq Validation Package

> Project-level scope and defensible claims:
> [Individual Project overview](../README.md)

This is the canonical validation and scientific-interpretation package for the
CT07 summary workflow and the Peak_Freq waveform workflow. The two algorithms
remain independent. Their outputs are joined only by the result-layer
`scientific/scientific_analysis.py`.

## Evidence boundary

- CT07: MATLAB oracle plus eight candidate-derived validation runners, with
  original-generation and fixture-normalized evidence reported separately;
  SMOP is a separate deterministic-transpiler baseline.
- Legacy Top-1: complete T01 only, with 3,098 rows numerically validated across
  MATLAB, Python and Julia.
- Adaptive Top-1/Top-3: complete T01–T09 numerical validation across MATLAB,
  Python and Julia: 377 files, 9,472,125 complete windows, 522,216 selected
  events and 1,566,634 Top-3 rows.
- Mechanical alignment: zero supported and nine unresolved mappings; no event
  is assigned a load, displacement, strain, stress or inferred damage stage.
- Top-3: retained as a secondary descriptive spectral extension under a
  pre-specified follow-on decision rule, not as damage classification or an
  accuracy improvement.
- WFS and R260_2 are separate steel-related cases and are not part of this
  package.

The CT07 prompt-to-result chain is frozen in the
[candidate evidence manifest](results/ct07/llm-validation/evidence/candidate_manifest.json).
It distinguishes original generations, fixture-normalized probes and the
candidate-derived runners used for MATLAB-oracle comparison.

## Current scientific outcome

- All 413 fixed waveform samples were regenerated from raw MAT data; their RMS
  and stored FFT peaks matched the numerical archive.
- All nine presumed waveform-to-CT mappings remain `unresolved`, so no event is
  assigned a mechanical stage.
- The deterministic class-hidden morphology screen is a reproducible signal
  morphology check, not expert review or damage ground truth.
- Top-3 passed the pre-specified follow-on decision rule and is `retained` as
  secondary descriptive spectral information, not as damage classification or
  evidence of improved detection accuracy.

See the
[Scientific Interpretation Report](results/scientific/Scientific%20Interpretation%20Report.md)
for the evidence and conservative dissertation wording.

## Configure

Edit `validation.toml` if the external waveform/workbook locations differ.
The tracked executable values are portable command names. Override a local
installation without editing the file:

```bash
export VALIDATION_PYTHON=/path/to/python
export VALIDATION_JULIA=/path/to/julia
export VALIDATION_MATLAB=/path/to/matlab
```

Raw MAT and workbook inputs are not copied into this package; their SHA-256
values are stored under `manifests/`.

No active command depends on the historical temporary or Desktop data paths.

## Run

Fast package verification:

```bash
python3 run_validation.py verify --config validation.toml
```

Rebuild the result-layer scientific outputs from the retained numerical
archives:

```bash
python3 run_validation.py rerun --config validation.toml --stage scientific
```

Run the complete, non-overwriting rehearsal:

```bash
python3 run_validation.py rehearse \
  --config validation.toml \
  --output rehearsals/<run-id>
```

The rehearsal requires MATLAB R2026a, Julia 1.12.6 and the pinned Python
environment described under `environment/`. It runs CT07, Legacy Top-1 T01,
Adaptive/Top-3 T01–T09 and the complete scientific analysis in that order.
Commands, separate stdout/stderr, timestamps, exit codes, environment
metadata, staged manifests and protected canonical hashes stay below the new
output directory. Existing canonical results and historical generation
evidence are never replaced.

Freeze or verify a staged result tree directly:

```bash
python3 run_validation.py freeze \
  --config rehearsals/<run-id>/effective_validation.toml \
  --results-root rehearsals/<run-id>/results

python3 run_validation.py verify \
  --config rehearsals/<run-id>/effective_validation.toml \
  --results-root rehearsals/<run-id>/results
```

Relocation is tested on the same host with the frozen external inputs still
available. The package does not claim cross-machine or fully offline
reproducibility.

## Final clean rehearsal

The retained final rehearsal is `rehearsals/final-20260729-r2/`. It completed
all 61 recorded commands with exit code 0, reproduced the frozen totals,
generated all 413 morphology figures, kept all nine mappings unresolved, and
passed staged and canonical verification. It reused only the explicitly
identified Legacy T01–T09 MATLAB context and MAT metadata; Adaptive/Top-3
T01–T09 was generated anew.

The preceding `rehearsals/final-20260729/` attempt is retained as failure
evidence. It stopped at the first Julia CT07 runner because the clean project
did not declare two dependencies used by the shared output helper. That
environment-declaration failure was fixed in the Julia project and preflight;
it is not classified as a candidate algorithm failure.

## Scientific morphology screen

The current machine-readable artifacts are:

- `results/scientific/waveform_morphology_screen_class_hidden.csv`;
- `results/scientific/waveform_morphology_screen_class_revealed.csv`;
- `results/scientific/waveform_morphology_screen_method.json`.

The deterministic screen does not use the matched/adaptive-only class while
assigning morphology labels. It is reproducible signal screening rather than
expert review. To rebuild only these derived outputs from retained numerical
evidence, run:

```bash
python scientific/scientific_analysis.py screen --config validation.toml
python scientific/scientific_analysis.py reveal --config validation.toml
python scientific/scientific_analysis.py top3 --config validation.toml
```

The Top-3 decision remains bounded by the pre-specified follow-on decision
rule. Passing it supports only the retained secondary descriptive role.
