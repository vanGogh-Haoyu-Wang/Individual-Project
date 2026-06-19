# Julia Acoustic Emission Plot Run Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Run `Test3 by Gemini 3.1pro high.jl` against the absolute-path workbook and produce five verified PNG plots plus a complete troubleshooting record.

**Architecture:** Preserve the original script as evidence. Inspect the workbook schema, reproduce the unmodified behavior, then create one minimally corrected Julia runner inside the output directory that loads only numeric data rows and saves all five plots headlessly with GR.

**Tech Stack:** Julia 1.12.6, XLSX.jl, DataFrames.jl, Plots.jl/GR, PNG validation utilities.

---

### Task 1: Inspect inputs and runtime

**Files:**
- Read: `Test3 by Gemini 3.1pro high.jl`
- Read: `Commercial Tensile Tests.xlsx`
- Create: `outputs/03Test Outputs/workbook-inspection.txt`

- [ ] Inspect workbook sheet names, used ranges, headers, and the eight required data columns.
- [ ] Locate the real Julia binary and determine whether the required Julia packages already exist.
- [ ] Record exact findings in `workbook-inspection.txt`.

### Task 2: Reproduce original behavior

**Files:**
- Read: `Test3 by Gemini 3.1pro high.jl`
- Create: `outputs/03Test Outputs/01-original-run.log`

- [ ] Run the original file with the absolute workbook path supplied as an argument.
- [ ] Capture stdout, stderr, exit status, and output image count.
- [ ] Confirm the failure or no-output behavior is repeatable before editing anything.

### Task 3: Implement the minimal corrected runner

**Files:**
- Create: `outputs/03Test Outputs/Test3_fixed.jl`
- Create: `outputs/03Test Outputs/Project.toml` only if no usable existing package environment is available.

- [ ] Add explicit command-line input/output arguments and an actual function call.
- [ ] Select the real workbook sheet and numeric data rows while keeping original 1-based column mappings.
- [ ] Preserve the five requested graph definitions and save each plot with `savefig`.
- [ ] Set GR to a headless workstation mode so GUI display is unnecessary.

### Task 4: Run and verify five outputs

**Files:**
- Create: `outputs/03Test Outputs/02-fixed-run.log`
- Create: `outputs/03Test Outputs/figure_1_strain_stress.png`
- Create: `outputs/03Test Outputs/figure_2_rms.png`
- Create: `outputs/03Test Outputs/figure_3_cumulative_rms.png`
- Create: `outputs/03Test Outputs/figure_4_ae_energy.png`
- Create: `outputs/03Test Outputs/figure_5_cumulative_ae_energy.png`

- [ ] Run the corrected script against the absolute workbook path.
- [ ] Require a zero exit status and exactly five non-empty PNG files.
- [ ] Validate PNG dimensions and decode every image.
- [ ] Visually inspect all five plots for nonblank data, titles, axes, and dual-axis series.

### Task 5: Produce the troubleshooting record

**Files:**
- Create: `outputs/03Test Outputs/运行问题与解决记录.md`

- [ ] Document every encountered issue with symptom, evidence, root cause, minimal fix, and verification result.
- [ ] Include exact commands, runtime/package versions, workbook facts, and the final five-file manifest.
- [ ] Cross-check that every artifact named in the record exists in the output directory.

