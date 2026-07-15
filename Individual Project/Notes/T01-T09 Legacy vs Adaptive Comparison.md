# T01-T09 Legacy vs Adaptive Comparison

**Date:** 2026-07-15  
**Purpose:** Independent repeat validation of the Legacy MATLAB-style AE peak-frequency workflow against the Adaptive Python workflow across every available T01-T09 raw-waveform group.

## Scope and Reproducibility

- Input: 377 MAT waveform files in T01-T09.
- Outputs: one Legacy export and one Adaptive export per group, stored in `ae-peak-frequency/outputs/t01-t09-revalidation/`.
- The original `Peak_Freq.m` was not edited. A companion MATLAB exporter reproduces its computational path and writes machine-readable CSV/MAT/JSON outputs.
- The comparison uses the same method as the earlier T02-T04 note, extended to all nine groups.

## Methods Compared

### Legacy MATLAB-style workflow

1. Sort MAT files by filename; use the mean and extreme values of the first file for the complete group.
2. Subtract that mean, append the original 1,000,000-sample zero padding, and retain only samples at or beyond the first-file extrema.
3. Compute a 200-sample moving RMS and select 200-sample frames with one-sample overlap (199-sample hop) above the fixed threshold 0.1.
4. Calculate a 200-point FFT for each selected window; retain the strongest detected peak with a 20 kHz minimum peak distance.

### Adaptive Python workflow

1. Process each MAT file independently and subtract its own mean.
2. Keep the raw centred waveform, without the first-file-extrema filter or appended padding.
3. Use the same 200-sample window and one-sample overlap (199-sample hop), but set the RMS threshold per file as `median + 8 x 1.4826 x MAD`.
4. Use the same FFT length, frequency range, Top-1 peak output, and 20 kHz minimum peak distance.

The raw threshold numbers are not directly comparable: Legacy RMS is calculated after an extreme-value filter and zero padding, while Adaptive RMS is calculated on the original centred waveform.

## Results Summary

| Group | Files | Candidate windows | Legacy selected (active files) | Adaptive Top-1 (active files) | Adaptive-only | Legacy rate | Adaptive rate | Adaptive/Legacy | Legacy windows also adaptive |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| T01 | 42 | 1,266,300 | 3,098 (38/42) | 78,317 (42/42) | 75,219 | 0.245% | 6.185% | 25.3x | 3,098/3,098 |
| T02 | 43 | 1,296,450 | 2,405 (27/43) | 57,445 (43/43) | 55,040 | 0.186% | 4.431% | 23.9x | 2,405/2,405 |
| T03 | 42 | 1,266,300 | 1,141 (27/42) | 52,984 (42/42) | 51,843 | 0.090% | 4.184% | 46.4x | 1,141/1,141 |
| T04 | 47 | 1,417,050 | 1,472 (32/47) | 57,117 (47/47) | 55,645 | 0.104% | 4.031% | 38.8x | 1,472/1,472 |
| T05 | 41 | 1,236,150 | 1,608 (33/41) | 73,692 (41/41) | 72,084 | 0.130% | 5.961% | 45.8x | 1,608/1,608 |
| T06 | 42 | 1,266,300 | 1,775 (35/42) | 68,417 (42/42) | 66,642 | 0.140% | 5.403% | 38.5x | 1,775/1,775 |
| T07 | 44 | 1,326,600 | 961 (29/44) | 55,795 (44/44) | 54,834 | 0.072% | 4.206% | 58.1x | 961/961 |
| T08 | 38 | 1,145,700 | 103 (17/38) | 9,943 (38/38) | 9,840 | 0.009% | 0.868% | 96.5x | 103/103 |
| T09 | 38 | 1,145,700 | 3,677 (24/38) | 68,506 (38/38) | 64,829 | 0.321% | 5.979% | 18.6x | 3,677/3,677 |

## Per-group Frequency Results

Frequency values below are Top-1 peak frequencies in kHz. IQR gives the middle 50% of results.

| Group | Legacy median (IQR) | Adaptive median (IQR) | Adaptive threshold range | Result |
|---|---:|---:|---:|---|
| T01 | 160.0 (160.0-180.0) | 160.0 (160.0-175.0) | 0.000934-0.032475 | All Legacy-selected windows were also selected by Adaptive. |
| T02 | 170.0 (165.0-175.0) | 165.0 (165.0-175.0) | 0.000967-0.015124 | All Legacy-selected windows were also selected by Adaptive. |
| T03 | 165.0 (165.0-170.0) | 165.0 (165.0-170.0) | 0.000954-0.004999 | All Legacy-selected windows were also selected by Adaptive. |
| T04 | 165.0 (165.0-170.0) | 165.0 (165.0-170.0) | 0.000967-0.015830 | All Legacy-selected windows were also selected by Adaptive. |
| T05 | 160.0 (160.0-175.0) | 160.0 (160.0-175.0) | 0.000930-0.004829 | All Legacy-selected windows were also selected by Adaptive. |
| T06 | 160.0 (160.0-165.0) | 160.0 (160.0-165.0) | 0.000938-0.018822 | All Legacy-selected windows were also selected by Adaptive. |
| T07 | 165.0 (165.0-175.0) | 165.0 (165.0-175.0) | 0.000958-0.005191 | All Legacy-selected windows were also selected by Adaptive. |
| T08 | 160.0 (160.0-165.0) | 160.0 (160.0-175.0) | 0.000935-0.000997 | All Legacy-selected windows were also selected by Adaptive. |
| T09 | 165.0 (165.0-170.0) | 165.0 (165.0-170.0) | 0.000971-0.017127 | All Legacy-selected windows were also selected by Adaptive. 1 Legacy-selected window had no valid FFT peak. |

## Interpretation

1. **The repeated result is consistent across all nine groups.** Adaptive selected 522,216 Top-1 windows from 11,366,550 candidates (4.594%), compared with 16,240 Legacy-selected windows (0.143%). Adaptive therefore returned 32.2 times as many candidate events.
2. **Adaptive retained the Legacy selections.** 16,240 of 16,240 Legacy-selected windows mapped exactly to an Adaptive selected window; 0 were absent. This is an event-selection containment result, not proof that every added Adaptive window is real AE.
3. **The difference is caused by selection logic, not by using a different FFT.** Both methods use the same 200-sample FFT, Top-1 peak representation, and 20 kHz spacing. The major change is the gate before the FFT: a fixed, group-level and strongly filtered Legacy gate versus a per-file, robust and unfiltered Adaptive gate.
4. **Adaptive frequencies are not expected to be numerically identical to Legacy frequencies.** Adaptive includes many lower-amplitude windows that Legacy discarded, so its median and IQR describe a broader population. The appropriate next comparison is matched-window frequency agreement, followed by waveform and mechanical-data checks.
5. **T09 exposed one Legacy robustness limitation.** 1 of 16,240 Legacy-selected windows had no valid local FFT peak. The original `Peak_Freq.m` assumes that every selected window yields a peak and would form unequal output vectors here. The companion exporter recorded this case and excluded it only from the frequency table; the selected window remains counted. This is not evidence of a bad raw file.

## Conclusion

The T01-T09 repeat validation supports the earlier T02-T04 conclusion: the Adaptive workflow is a reproducible superset of the Legacy selection on these nine datasets, while producing substantially more candidate windows. That is a useful algorithmic improvement because it removes dependence on one fixed threshold and one first-file extreme-value setting. It is not yet a claim that the extra Adaptive windows are all genuine AE events or that the method is better for a particular material. Those claims require checking representative raw waveforms and aligning event times with tensile load/displacement or other experiment labels.

## Next Validation Step

For each group, sample matched Legacy/Adaptive windows and Adaptive-only windows from low, middle, and high test activity. Plot their raw waveform, RMS, and FFT, then align them with the mechanical record once the correct specimen/time mapping is confirmed. This will test whether the added Adaptive detections are physical AE, background noise, or repeated windows from the same burst.
