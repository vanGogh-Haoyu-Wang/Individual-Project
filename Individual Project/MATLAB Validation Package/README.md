# MATLAB Legacy Validation Package

> **Superseded package notice:** This directory is retained as historical
> validation material. Use the
> [CT07–Peak_Freq validation package](../CT07-PeakFreq-Validation/README.md)
> for current numerical evidence and the
> [Individual Project overview](../README.md) for project-level scope.

## Purpose

This package supports the requested reference comparison between the existing
MATLAB method in `Peak_Freq.m` and the Python/Julia work. It does not modify
the original script or raw data.

The local Mac has MATLAB R2026a but no DSP System Toolbox license. Run the
following steps on a MATLAB machine where all three checks succeed:

```matlab
license('test', 'DSP_System_Toolbox')
exist('dsp.MovingRMS', 'class')
exist('buffer', 'file')
```

The expected values are `1`, `8`, and `2` respectively.

## Inputs

Use the full raw-data directory:

```text
/Users/vangogh/Desktop/毕设/Haoyu Wang/T01
```

The directory contains 42 MAT waveform files. The first file must be
`20221018_140051.mat`, because `Peak_Freq.m` uses the first file's mean,
maximum, and minimum as the global reference values. The export companion
sorts filenames to make that order explicit.

## Run the original script unchanged

1. Open MATLAB on the licensed machine.
2. Change to the directory containing the original script:

   ```matlab
   cd('/Users/vangogh/Desktop/毕设/Haoyu Wang')
   ```

3. Run the original script:

   ```matlab
   Peak_Freq
   ```

4. In the file picker, select every `.mat` file in `T01`, beginning with
   `20221018_140051.mat`. Do not select the Excel workbook.
5. Keep the generated figures open or capture screenshots. This is the visual
   check that the unmodified original script runs in that environment.

## Export reference rows

Copy the `ae-peak-frequency/matlab` folder to the licensed machine, then run:

```matlab
addpath('/path/to/ae-peak-frequency/matlab')
run_legacy_peak_freq_export( ...
    '/Users/vangogh/Desktop/毕设/Haoyu Wang/T01', ...
    '/path/to/legacy-matlab-all-files-output', ...
    '/Users/vangogh/Desktop/毕设/Haoyu Wang/Peak_Freq.m')
```

This repeats the computational lines from `Peak_Freq.m`, but replaces only the
interactive file picker with deterministic sorted files and adds saved output.
It writes:

- `legacy_top1_events.csv`: one row per legacy-selected event, with
  `event_index`, `time_s`, `peak_frequency_khz`, and `peak_magnitude`.
- `legacy_run_metadata.json`: input ordering, thresholds, and row counts.
- `legacy_peak_freq_export.mat`: the same export table plus intermediate
  legacy arrays needed for audit.

Bring that output folder back into this project before running the numerical
comparison. Do not overwrite the existing Python or Julia output folders.

## Important interpretation

The previous `0`-event result is correct only for the single first waveform.
It does not predict the 42-file result: later files contain retained samples
well above the `0.1` threshold. Therefore the all-file MATLAB export is needed
before making any claim about legacy versus adaptive event counts.

## Completed Reference Run

On 2026-07-14, the unmodified `Peak_Freq.m` completed on the full 42-file
input set after DSP System Toolbox became runnable. The export companion
produced 3,098 Top-1 legacy rows. Matched Python and Julia legacy-mode exports
had the same 3,098 event indices, times, and peak frequencies; each maximum
peak-magnitude difference from MATLAB was `5.684341886080801e-13`.

The formal row comparison is retained in:

```text
/Users/vangogh/Documents/temp/ae-peak-frequency/outputs/legacy-row-comparison
```
