# AE Peak-Frequency Implementation Plan

> Project-level current status: [[Individual Project/README|Canonical Project Overview]]

## Confirmed Scope

This work will migrate the existing `Peak_Freq.m` workflow into Python first, then Julia. The baseline records one strongest FFT frequency peak for each selected AE event. The improvement records up to three separated frequency peaks for the same events.

## Work Order

1. Create an isolated prototype folder; leave `Peak_Freq.m`, `T01/*.mat`, and the original Excel workbook unchanged.
2. Create one shared parameter file: 1 MHz sampling rate, 200-sample window, 0.1 RMS threshold, 20 kHz peak separation, and three retained peaks.
3. In Python, test reading `.mat` waveform data, `.csv`, and `.xlsx` summary data.
4. In Python, test and implement DC-offset removal, RMS event selection, FFT, and one strongest peak per event.
5. Add the Top-3 output using the same events and FFT settings.
6. Export baseline and Top-3 event tables as CSV, plus two time-frequency figures.
7. Run one real `.mat` file and record event count, output files, parameter values, and limitations.
8. Only after Python runs successfully, repeat the same input/output contract in Julia.

## Required Outputs

- `baseline_events.csv` and `top3_events.csv` with columns: `event_id`, `file_name`, `event_time_s`, `peak_rank`, `frequency_khz`, `magnitude`.
- `baseline_peak_frequency.png` and `top3_peak_frequency.png`.
- A Markdown run record stating exactly which files and parameters were used.

## Interpretation Boundary

Top-3 reporting may retain frequency information that Top-1 reporting omits. It does not, by itself, prove a particular material damage mechanism.
