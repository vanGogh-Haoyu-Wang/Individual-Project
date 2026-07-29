# AE Peak-Frequency Development Log

> [!note] Historical development log
> Entries describe the state at their recorded dates. Current validated scope
> and conclusions are maintained in [[Individual Project/README|Canonical Project Overview]].

## 2026-07-14 - Scope Decision

### Confirmed objective

The project will first migrate the existing MATLAB `Peak_Freq.m` workflow into Python. Julia implementation will begin only after the Python prototype has been tested on real input data.

The analysis has two modes:

1. **Legacy mode** preserves the fixed RMS threshold and single-peak reporting logic from the MATLAB script as closely as possible.
2. **Adaptive mode** will select events using a threshold calculated from each waveform's background RMS, then compare single-peak and Top-3 peak reporting on the same selected events.

The Top-3 result is interpreted only as additional frequency information. It is not treated as proof of a specific material damage mechanism.

## 2026-07-14 - Input Data Findings

### Raw waveform files

- Directory inspected: `T01`.
- Raw input: 42 MATLAB v5 `.mat` files.
- First inspected file: `20221018_140051.mat`.
- The file contains a `data` array; the migration will use its first column, matching `Peak_Freq.m`.
- The first waveform contains 5,000,000 samples.
- Observed raw range: minimum `0.43122955`, maximum `0.48783312`, mean `0.45901688`.

### Summary data

- `Tensile-processed.xlsx` contains mechanical and AE-summary sheets, including `CT-01` through `CT-09`.
- Python input support is required for `.mat`, `.csv`, and `.xlsx` files. The raw waveform workflow itself depends on `.mat`; CSV/XLSX are used for summary inspection and later comparison.

## 2026-07-14 - Python Input Layer

### Implementation

A standalone Python prototype was created under `/Users/vangogh/Documents/temp/ae-peak-frequency/python`. It leaves the original MATLAB script, raw `.mat` files, and workbook unchanged.

The input layer implements:

- `load_waveform(path)`: loads the first column of the MATLAB `data` variable.
- `load_summary(path)`: reads `.csv` or `.xlsx` summary data without deleting physical rows.

### Tests

Four automated tests passed:

1. Read the first column from a valid `.mat` file.
2. Reject a `.mat` file without a `data` variable.
3. Read a CSV summary.
4. Read an Excel summary without treating the first physical row as a header.

## 2026-07-14 - Legacy Threshold Check

### Observation

The MATLAB script uses a fixed event-selection condition `RMS > 0.1` after removing the mean and retaining only extrema.

On `20221018_140051.mat`:

- Maximum moving RMS after reproducing the legacy extrema filtering: `0.0028306463`.
- Maximum moving RMS after only mean removal: `0.0061821661`.
- Number of windows above the legacy threshold `0.1`: `0` in both cases.

### Decision

The literal legacy threshold cannot produce an event for this input file. It will be retained as an auditable **Legacy mode** result, not silently changed. An **Adaptive mode** will be implemented and evaluated separately, with its threshold calculation recorded in the output metadata.

## 2026-07-14 - Adaptive Event Selection

### Threshold definition

The adaptive threshold is defined as:

```text
adaptive threshold = median(window RMS) + 8 × 1.4826 × MAD(window RMS)
```

`MAD` is the median absolute deviation. It is used instead of a normal standard deviation because a small number of high-energy AE events should not strongly inflate the background-noise estimate.

### Real-data check

For `20221018_140051.mat`, using 200-sample windows with one-sample overlap:

- Number of RMS windows: `25,125`.
- Median RMS: `0.00064925031`.
- Robust RMS noise scale: `0.000035892874`.
- Adaptive threshold with multiplier 8: `0.00093639331`.
- Candidate windows above this threshold: `125`.

The multiplier is configurable and is not presented as a universal physical constant. Its value and the selected-event count will be included in every run record.

### Automated test status

Seven Python tests pass:

- Four input tests for `.mat`, `.csv`, and `.xlsx` reading.
- Three event-selection tests for the legacy extrema filter, robust adaptive threshold, and 200-sample event extraction.

### Test correction

One early test incorrectly expected a threshold of zero for a synthetic waveform. The event itself changes the full-signal mean used for DC-offset removal, so the correct threshold is small but positive. Diagnostic output confirmed that the detector selected exactly one intended event window. The test was corrected to check the scientifically relevant behaviour: one event is selected and the threshold is positive but small.

## 2026-07-14 - FFT and Python Prototype Run

### FFT verification

Three FFT tests pass before real data is used:

1. A 100 kHz synthetic sine wave is reported near 100 kHz.
2. A synthetic mixture at 100, 200, and 300 kHz is returned in descending magnitude order when Top-3 reporting is requested.
3. A zero waveform returns no false frequency peak.

### Real-data adaptive run

Input file:

```text
20221018_140051.mat
```

Configuration:

- Sampling rate: `1,000,000 Hz`.
- Window length: `200 samples`.
- Window overlap: `1 sample`.
- Adaptive multiplier: `8`.
- Minimum frequency separation: `20 kHz`.

Results:

- Adaptive threshold: `0.0009363933078584744`.
- Selected event windows: `125`.
- Top-1 CSV rows: `125`.
- Top-3 CSV rows: `375`.
- Top-1 observed peak-frequency range: `90–295 kHz`.

The prototype created `baseline_events.csv`, `top3_events.csv`, `baseline_peak_frequency.png`, `top3_peak_frequency.png`, and `run_metadata.json` in its separate output folder.

### Visual inspection

Both output plots were inspected. The Top-1 figure contains one point per selected event. The Top-3 figure contains three points per selected event and visibly retains additional frequency information. Neither figure is used to claim a material damage classification.

### Environment observation

Matplotlib initially attempted to create its cache under the user home directory, which is not writable in the current execution sandbox. It automatically used a temporary cache and still generated valid plots. Future direct-run commands will set `MPLCONFIGDIR` to a writable project-local cache directory so the run is warning-free and reproducible.

## 2026-07-14 - Legacy Audit and Command-Line Prototype

### Command-line interface

The Python prototype now has a direct command-line entry point. It accepts one or more `.mat` waveform paths and an output directory. The command writes Top-1 and Top-3 CSV/PNG outputs plus a JSON metadata file.

### Legacy audit result

The metadata now records the literal legacy-mode result separately from the adaptive result. For `20221018_140051.mat`:

- Legacy RMS threshold: `0.1`.
- Legacy selected event count: `0`.
- Adaptive selected event count: `125`.

This preserves the original method's non-working result as evidence rather than hiding it.

### Reproducibility update

Matplotlib now uses a writable cache directory beside the project outputs. The second direct command-line run completed without the earlier home-directory permission warning. A first-time font-cache message is expected and does not change the analysis result.

### Automated test status

Twelve Python tests pass:

- Input reading.
- Legacy and adaptive event selection.
- FFT Top-1 and Top-3 ranking.
- CSV/PNG/JSON output generation.
- Direct command-line execution.

## 2026-07-14 - Summary-File Integration

### CSV and Excel row-preservation decision

CSV and Excel summary files now both preserve their physical first rows. This is deliberate because the supplied experimental sheets contain labels and units in physical rows that must not disappear silently during import.

During implementation, CSV initially used the library default that treated the first physical row as column names. That removed one row from the metadata. The reader was corrected to use `header=None` for CSV and Excel alike.

### Excel-sheet selection decision

The command-line prototype now accepts:

```text
--summary <path-to-csv-or-xlsx>
--summary-sheet <worksheet-name>
```

If no Excel sheet is named, the first sheet is read. If a sheet name is provided, that exact sheet is read. This avoids the incorrect assumption that `sheet_name=None` means the first sheet; in pandas it means all sheets and returns a dictionary.

### Real summary integration check

The prototype was run with:

```text
Raw waveform: 20221018_140051.mat
Summary workbook: Tensile-processed.xlsx
Summary worksheet: CT-07
```

The metadata correctly records the selected worksheet as `CT-07`, with `6,027` rows and `31` columns. The waveform result remains:

- Legacy event count: `0`.
- Adaptive event count: `125`.
- Adaptive threshold: `0.0009363933078584744`.

### Automated test status

Fifteen Python tests pass. They cover raw MAT loading, CSV/XLSX physical-row preservation, explicit Excel sheet selection, legacy and adaptive event selection, FFT peak ranking, generated outputs, and direct command-line execution.

## 2026-07-14 - Julia Prototype

### Julia environment

Julia `1.12.6` was used with a standalone project environment containing `MAT`, `CSV`, `DataFrames`, `XLSX`, `FFTW`, `JSON3`, and `Plots`.

The first `Pkg.test()` attempt was blocked because the sandbox did not permit Julia to write its own environment-usage lock file. Running the same project with local Julia write permission resolved this environment-only issue. The project also required a package `name` and `uuid` before `Pkg.test()` could run.

### Core implementation and tests

The Julia module implements the same core contract as Python:

- `.mat` waveform loading from the first `data` column.
- Legacy extrema filter and fixed threshold.
- Adaptive RMS threshold using `median + 8 × 1.4826 × MAD`.
- 200-sample event windows with one-sample overlap.
- FFT Top-1 and Top-3 peak ranking with 20 kHz separation.
- CSV Top-1/Top-3 tables, two PNG figures, and JSON run metadata.

Julia core tests pass:

- MAT waveform input: `1/1`.
- Adaptive event selection: `3/3`.
- Top-3 FFT ranking: `1/1`.

### Excel physical-layout correction

An initial Julia implementation used `XLSX.readtable`, which automatically inferred a reduced table and changed `CT-07` from the physical `6027 × 31` worksheet into `1810 × 4`. This was rejected because it violates the same physical-row/column contract used in Python.

The reader was changed to `XLSX.readxlsx` plus `XLSX.getdata` on the requested worksheet. This preserves the real worksheet layout.

### Python/Julia real-data alignment

Both implementations were run on:

```text
Raw waveform: 20221018_140051.mat
Summary workbook: Tensile-processed.xlsx
Summary worksheet: CT-07
```

Both now report:

- Summary layout: `6027 × 31`.
- Legacy event count: `0`.
- Adaptive event count: `125`.
- Top-1 rows: `125`.
- Top-3 rows: `375`.
- Adaptive threshold: Python `0.0009363933078584744`; Julia `0.0009363933078584757` (normal floating-point difference only).

The Julia output folder contains the same five artifact names as Python: `baseline_events.csv`, `top3_events.csv`, `baseline_peak_frequency.png`, `top3_peak_frequency.png`, and `run_metadata.json`.

### Final Julia verification

Julia also has an automated CSV summary test confirming that the first physical row is preserved rather than silently converted to column names.

Direct comparison of the Python and Julia Top-3 CSV files confirms:

- Same column order.
- Same row count: `375`.
- Event times, peak ranks, frequencies, and magnitudes agree within `1e-12` absolute/relative tolerance.
- Largest observed magnitude difference: `1.1102230246251565e-16`, which is normal floating-point rounding.

This establishes cross-language numerical agreement for the tested waveform file and configuration. It does not establish equivalence with the original MATLAB output until the MATLAB script itself is run on the same file set and its output is retained for comparison.

## 2026-07-14 - MATLAB Legacy Validation

### MATLAB availability and scope

MATLAB R2026a is installed at:

```text
/Applications/MATLAB_R2026a.app/bin/matlab
```

The original script was preserved unchanged at:

```text
/Users/vangogh/Desktop/毕设/Haoyu Wang/Peak_Freq.m
```

For headless validation, a separate wrapper was created at:

```text
/Users/vangogh/Documents/temp/ae-peak-frequency/matlab/run_legacy_peak_freq_fixed_input.m
```

The wrapper changes only the interactive file-selection step: it receives a known input file, writes a new report, and does not create the original figures when there are no events. It preserves the original mean subtraction, one-million-zero padding, extrema-only filter, 200-sample setting, and fixed `0.1` event threshold.

### Toolbox boundary

The original script calls `dsp.MovingRMS`, which requires DSP System Toolbox. That toolbox is not installed in this MATLAB environment, so the original script cannot complete literally here. The attempted direct call correctly raised MATLAB's missing-toolbox error; this is an environment dependency, not a data or prototype error.

The wrapper therefore performs a mathematically exact threshold check that does not replace or approximate the unavailable DSP function: for every possible window, RMS is at most the maximum absolute input sample. If that upper bound is below the threshold, no RMS implementation can produce an event.

### Result on the shared reference waveform

Input:

```text
/Users/vangogh/Desktop/毕设/Haoyu Wang/T01/20221018_140051.mat
```

MATLAB produced:

- Mean of first waveform: `0.45901687983319478`.
- Upper extreme after mean subtraction: `0.0288162451668052`.
- Lower extreme after mean subtraction: `-0.027787329833194707`.
- Maximum possible RMS after the original extrema-only filter: `0.0288162451668052`.
- Literal legacy threshold: `0.1`.
- Guaranteed legacy event count: `0`.

The report is retained at:

```text
/Users/vangogh/Documents/temp/ae-peak-frequency/outputs/matlab-legacy-first-file/legacy_peak_freq_report.json
```

### Decision

The Python and Julia implementations are aligned with MATLAB on the important baseline conclusion: this input cannot pass the existing script's fixed event threshold. The adaptive pipeline is not an arbitrary replacement for a working legacy baseline; it is the necessary next experiment because the legacy baseline selects no events for this waveform.

Before claiming exact MATLAB numerical equivalence for MovingRMS values or peak-frequency rows, DSP System Toolbox must be available and the original script must be run on the same data with its outputs retained. That is a future validation task, not a reason to discard the already verified Python/Julia adaptive results.

## 2026-07-14 - MATLAB Multi-File Correction and Portable Validation Package

### License investigation

The local MATLAB environment was queried directly. It is MATLAB R2026a Update 3 with license number `40472096`. The checks returned:

```text
license('test', 'DSP_System_Toolbox') = 0
exist('dsp.MovingRMS', 'class') = 0
```

This confirms that the limitation is a missing DSP System Toolbox license, not merely an absent folder on disk. The local machine therefore cannot legally execute the unmodified `Peak_Freq.m` computational path or provide an exact MATLAB row-level reference.

### Correction to the single-file conclusion

The earlier MATLAB/Python/Julia legacy audit used only `20221018_140051.mat` and correctly found zero events for that one waveform. That result must not be generalized to the whole `T01` experiment.

`Peak_Freq.m` uses multi-file selection. An audit of all 42 MAT files using its first-file mean and extrema filter found later files with retained sample amplitudes up to `10.919285506833196`, far above the fixed `0.1` threshold. Thus the complete multi-file MATLAB run can plausibly contain legacy events and needs an actual DSP-enabled execution.

### Prepared validation package

Two files were added without modifying the original MATLAB script or raw data:

- `ae-peak-frequency/matlab/run_legacy_peak_freq_export.m`
- `ae-peak-frequency/matlab/README.md`

The export companion requires an existing `Peak_Freq.m` path and checks for `dsp.MovingRMS`, `buffer`, and `findpeaks`. It mirrors the original computational statements while replacing only GUI file selection with deterministic alphabetical MAT-file ordering. It exports a stable one-row-per-event table:

```text
event_index, time_s, peak_frequency_khz, peak_magnitude
```

It also writes JSON metadata and a MATLAB MAT archive. The README gives the exact workflow for a licensed machine: first run `Peak_Freq.m` unchanged as a visual check, then run the exporter, bring the output folder back, and perform the numerical comparison.

### Current decision

Do not claim a full MATLAB/Python/Julia row comparison yet. The only missing artifact is the all-42-file output from a MATLAB environment licensed for DSP System Toolbox. The validation package is ready for that environment; after its output returns, the next work is to produce a row-by-row comparison report against matched Python and Julia legacy-mode outputs.

### Package verification

The Python project test suite now has 16 passing tests, including a static contract test for the MATLAB exporter. MATLAB R2026a also parsed the exporter with `checkcode`; it reported only one expected `AGROW` performance warning for the intentionally preserved dynamic structure-array accumulation from the original script. No MATLAB syntax error was reported.

## 2026-07-14 - Completed MATLAB / Python / Julia Legacy Comparison

### DSP runtime became available

After the DSP System Toolbox installation was updated, MATLAB reported:

```text
exist('dsp.MovingRMS', 'class') = 8
exist('buffer', 'file') = 2
exist('findpeaks', 'file') = 2
```

Although `license('test', 'DSP_System_Toolbox')` still returned `0`, direct execution of `dsp.MovingRMS(200, +1)` succeeded. The runnable function and the installed toolbox were therefore treated as the authoritative runtime evidence.

### The unmodified original script ran successfully

`/Users/vangogh/Desktop/毕设/Haoyu Wang/Peak_Freq.m` was executed without edits against all 42 waveform files in `T01`.

The test harness replaced only the GUI file-picker response with the deterministic alphabetical file list and hid figures because the run was headless. It did not alter the original script. MATLAB printed all expected phases:

```text
Loading Data
Formatting Data
Permforming DFT
Finding Peaks
Plotting
```

The script completed in `11.985973` seconds.

### Retained MATLAB reference output

The companion exporter, which mirrors the original calculations and adds only deterministic input selection plus output files, produced:

```text
Input MAT files: 42
Legacy-selected events: 3,098
Top-1 output rows: 3,098
```

Output location:

```text
/Users/vangogh/Documents/temp/ae-peak-frequency/outputs/matlab-legacy-all-files
```

The reference columns are:

```text
event_index, time_s, peak_frequency_khz, peak_magnitude
```

### Important MATLAB framing discovery

The first Python legacy implementation initially disagreed with MATLAB by two total rows because it assumed windows began at the first sample. A direct MATLAB experiment with the known sequence `1:400` showed that:

```matlab
dsp.MovingRMS(200, 1)
```

uses the same initial-overlap convention as:

```matlab
buffer(x, 200, 1)
```

Its first frame is `[0, 1, 2, ..., 199]`, not `[1, 2, ..., 200]`. The original script also discards the final padded buffer column. Python and Julia were changed to reproduce this exact convention before the final comparison.

### Final row-by-row result

Python and Julia both ran the same 42-file legacy mode and wrote the same output contract as MATLAB. The formal comparison is stored in:

```text
/Users/vangogh/Documents/temp/ae-peak-frequency/outputs/legacy-row-comparison
```

Results:

| Check | MATLAB vs Python | MATLAB vs Julia |
| --- | ---: | ---: |
| Rows | 3,098 vs 3,098 | 3,098 vs 3,098 |
| Event indices | Identical | Identical |
| Maximum time error | 0 s | 0 s |
| Maximum frequency error | 0 kHz | 0 kHz |
| Maximum magnitude error | `5.684341886080801e-13` | `5.684341886080801e-13` |
| Pass at `rtol=1e-12`, `atol=1e-12` | Yes | Yes |

The magnitude difference is normal double-precision rounding, not a behavioral discrepancy. This completes the requested old-MATLAB-to-Python/Julia row-level validation for the complete T01 input set.

### Final verification

- Python: 19 tests passed.
- Julia: all five test groups passed, including the MATLAB buffer-framing test.
- MATLAB: the original unmodified script completed successfully and the retained export contains 3,098 rows.

## 2026-07-15 - T02, T03 and T04 Legacy vs Adaptive Comparison

The validated MATLAB legacy workflow and the adaptive Python workflow were run on the complete T02 (43 MAT files), T03 (42 MAT files), and T04 (47 MAT files) groups. A complete English report is stored separately as `2026-07-15 T02-T04 Legacy vs Adaptive Comparison.md`.

The central result is consistent across all three datasets: every legacy-selected window was also selected by the adaptive workflow. The adaptive workflow additionally selected 55,040 windows in T02, 51,843 in T03, and 55,645 in T04. The legacy method selected events in only 27/43 T02 files, 27/42 T03 files, and 32/47 T04 files; the adaptive method selected events in every file.

Both methods retained the same dominant Top-1 frequency region below 200 kHz. The interpretation is therefore that adaptive selection substantially increases detection density without changing the central spectral character of the detections. This demonstrates increased sensitivity and transferability, but does not by itself prove that every adaptive-only event is physical AE rather than noise. The next validation should align adaptive-only detections with tensile load/displacement and representative waveform inspection.

## 2026-07-15 - Relationship Between CT07.m and Peak_Freq.m

`CT07.m` and `Peak_Freq.m` are complementary analysis layers, not duplicate algorithms and not scripts that should be merged line by line.

- `CT07.m` reads the processed `CT-07` Excel sheet and plots experiment-scale mechanical and AE-summary quantities: stress versus strain/time, normalised RMS, cumulative RMS, AE energy, and cumulative AE energy.
- `Peak_Freq.m` reads raw MAT waveform blocks, selects short high-RMS windows, calculates FFTs, and reports the dominant frequency of each selected waveform event.

The correct future integration is a third analysis step: retain `Peak_Freq` event frequency/time information, align it to a confirmed mechanical test timebase, then overlay or join it with stress, strain, RMS, and energy from the processed workbook. This is necessary to test whether adaptive-only events occur during mechanically meaningful stages.

The scripts must not yet be joined automatically because their time coordinates are not proven to be the same. `Peak_Freq.m` constructs a frame-index time after concatenating files and inserting artificial zero gaps; it does not use the workbook's experiment clock. In addition, every T01–T04 workbook contains a `CT-07` sheet, so the sheet name alone does not establish which raw Txx file group corresponds to the CT07 processed trace. A specimen/group mapping and trigger/start-time alignment must be confirmed before any physical time-series conclusion is made.

## 2026-07-29 - Final Numerical Closure and Scientific Interpretation Status

The final evidence separates three Peak_Freq result scopes:

1. **Legacy MATLAB T01-T09 context:** 377 MAT files produced 11,366,550
   Legacy logical frames, 16,240 selected windows and 16,239 valid Top-1
   rows. These nine-group Legacy totals are descriptive MATLAB context, not a
   nine-group three-language validation.
2. **Legacy Top-1 numerical validation:** the complete T01 dataset produced
   3,098 rows that matched across MATLAB, Python and Julia within
   `rtol=1e-12`, `atol=1e-12`.
3. **Adaptive/Top-3 numerical validation:** the complete T01-T09 dataset
   comprised 377 files and 9,472,125 Adaptive complete windows. MATLAB,
   Python and Julia matched for 522,216 selected events and 1,566,634 Top-3
   rows.

The Legacy and Adaptive framing totals are not interchangeable. The Adaptive
selection rate is `522,216 / 9,472,125 = 5.513%`; the Legacy rate is
`16,240 / 11,366,550 = 0.143%`. The ratio `522,216 / 16,240 = 32.16x`
describes selected-window counts, not rates calculated from one shared
denominator.

The scientific follow-on does not raise the validation level:

- a deterministic class-hidden morphology screen was completed for 413
  fixed samples; it is not expert human blind review and does not provide
  damage ground truth;
- the T01-T09 waveform-to-workbook alignment returned `0` supported and `9`
  unresolved groups, so no load, stress, yield or crack-stage result is
  reported;
- Top-3 is retained only as secondary descriptive spectral information under
  a pre-specified follow-on decision rule; no formal preregistration is
  claimed;
- adaptive-only events are not treated as confirmed physical AE damage
  events, and no damage-classification or accuracy-improvement claim is made.

Current project-level scope and defensible claims are maintained in
[[Individual Project/README|Canonical Project Overview]].
