# Project Status Review

## Current Position

The project has moved beyond a purely prompt-comparison exercise. It now has one genuinely validated AE analysis case study: the legacy MATLAB peak-frequency workflow has been executed, reproduced, and compared against Python and Julia. The broader MSc objective, however, is larger than this one workflow, so the project is partially complete rather than finished.

## Completed Work

- Read and documented literature on AI-assisted code migration, reproducibility, scientific use of LLMs, AE interpretation, composite monitoring, and steel-structure considerations.
- Installed and tested a local scientific-code migration environment, including SMOP, Python environments, and Julia environments.
- Designed and recorded structured prompts for three MATLAB translation experiments.
- Compared multiple LLM and SMOP outputs for the CT07 spreadsheet/plotting task in Python and Julia.
- Identified the critical workbook issue: mechanical and AE variables have different valid row domains, so automatic table inference or global missing-value removal can invalidate the scientific data.
- Demonstrated that LLM outputs are useful first drafts but require workbook-aware debugging and independent tests before being treated as scientific migrations.
- Built Python and Julia AE peak-frequency prototypes that read MAT, CSV, and XLSX inputs and export CSV/PNG/JSON outputs.
- Implemented adaptive RMS event selection and Top-1/Top-3 frequency reporting.
- Installed a runnable MATLAB DSP System Toolbox environment and executed the original `Peak_Freq.m` workflow on the complete T01 set.
- Validated the T01 legacy MATLAB output against Python and Julia row by row: 3,098 rows, identical event indices/times/frequencies, and only normal floating-point magnitude differences.
- Compared legacy MATLAB and adaptive Python selection on T02, T03, and T04. In every group, adaptive selection retained all legacy windows and added additional lower-amplitude candidate windows while preserving the dominant frequency band below 200 kHz.
- Kept run records, test evidence, MATLAB validation material, and English technical notes.

## What Is Not Yet Complete

- No steel-structure dataset has been analysed. The current verified AE data are composite tensile-test data, so frequency-based composite damage labels must not be claimed for steel.
- The physical meaning of adaptive-only events has not been validated. They may be genuine weak AE events, but may also include fixture, machine, electrical, or sensor noise.
- Adaptive event times have not yet been aligned with the tensile load/displacement record, specimen behaviour, or independent inspection evidence.
- The Top-3 extension has been implemented and exported, but its scientific value has not yet been evaluated systematically across datasets.
- No final choice has been made for the dissertation's main "new algorithm" contribution. The current adaptive threshold is a strong candidate, but it needs a validation criterion and perhaps one focused extension rather than several unrelated methods.
- Python/Julia performance, memory use, and maintainability have not been compared systematically.
- The full UoB-NDT MATLAB codebase has not been migrated; the verified work covers the selected CT07-style translation exercises and the `Peak_Freq.m` workflow.
- The final dissertation outputs remain to be written: methods, results, discussion, limitations, reproducibility package, and an AI-use/translation-risk reflection.

## Most Important Next Work

1. Confirm the intended material and dataset scope with the supervisor: steel data, composite data, or a clearly justified transfer study.
2. Validate adaptive-only events against tensile load/displacement and inspect a representative sample of raw waveforms/spectra.
3. Turn the adaptive method into one focused research question with measurable success criteria, such as legacy-event retention, false-positive control, stability across files, and agreement with mechanical stages.
4. Analyse whether Top-2/Top-3 peaks add useful information beyond Top-1, or explicitly reduce the scope and keep adaptive event selection as the sole improvement.
5. Prepare a clean, reproducible final code/data contract and write the dissertation around the evidence already obtained.

## Honest Summary

The code-migration and baseline-validation part is strong for one AE workflow. The scientific-algorithm part has begun and produced a promising result, but it is not complete until the adaptive-only detections are connected to physical experimental evidence and the material scope is agreed with the supervisor.
