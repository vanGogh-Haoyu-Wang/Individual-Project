# Experimental Plan: Migration and Improvement of AE Peak-Frequency Analysis

> Project-level current status: [[Individual Project/README|Canonical Project Overview]]

## Aim

To migrate an existing MATLAB acoustic-emission (AE) peak-frequency workflow into reproducible Python and Julia prototypes, then test a small improvement that retains the three strongest frequency peaks from each detected AE event rather than only the strongest peak.

## Research Question

Does retaining the top three separated frequency peaks per AE event reveal frequency information that is lost when the analysis uses only one peak frequency?

## Available Data

- Raw AE waveform blocks: 42 MATLAB `.mat` files in `T01`, each containing a `data` signal.
- Processed experiment data: `Tensile-processed.xlsx`, to be exported to CSV where useful for checking specimen, mechanical, and AE-summary information.
- Existing baseline method: `Peak_Freq.m`.

## Phase 1: Reproduce the Existing Method

Both Python and Julia prototypes will:

1. Read selected `.mat` waveform files.
2. Remove the DC offset from each waveform.
3. Apply the existing RMS-based event-selection logic.
4. Extract a short waveform segment for each selected event.
5. Apply FFT to each segment.
6. Record the single strongest frequency peak and plot event time versus peak frequency.

The first result will be compared with the MATLAB workflow in terms of event count, event times, frequency range, and plot structure. The goal is functional agreement, not pixel-identical figures.

## Phase 2: Small Method Improvement

Using exactly the same detected events and FFT settings, the new version will retain the top three frequency peaks for each event, requiring peaks to be separated by at least 20 kHz. It will export an event table containing time, frequency, and magnitude for Top-1, Top-2, and Top-3 peaks, and create a time-frequency plot that shows all retained peaks.

## Evaluation

- Does the baseline Python/Julia output reproduce the overall MATLAB event-time and peak-frequency pattern?
- How many events contain meaningful second or third peaks?
- Are the additional peaks concentrated in particular time periods or frequency ranges?
- Do Python and Julia produce the same result when they use the same input files and parameter values?

## Scope and Interpretation

This experiment will not claim that a particular frequency band proves a specific damage mechanism. The existing labels in `Peak_Freq.m` are composite-material labels and will be treated as a reference example only. The contribution is a transparent, testable AE analysis workflow and a direct comparison between single-peak and multi-peak frequency reporting.

## Deliverables

- One Python prototype and one Julia prototype.
- CSV input/export files and a documented data schema.
- Baseline and Top-3 event tables and figures.
- A short Markdown record of commands, parameters, results, and limitations.
