# T01-T09 Legacy vs Adaptive Comparison

> [!warning] Superseded comparison stage
> This note preserves the 2026-07-15 comparison and has been corrected to use
> separate Legacy and Adaptive framing denominators. Current validation scope
> and scientific interpretation are maintained in
> [[Individual Project/README|Canonical Project Overview]].

> Project-level current status: [[Individual Project/README|Canonical Project Overview]]

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

| Group | Files | Legacy logical frames | Adaptive complete windows | Legacy selected (active files) | Adaptive selected (active files) | Adaptive-only | Legacy rate | Adaptive rate | Selected-count ratio | Legacy windows also adaptive |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| T01 | 42 | 1,266,300 | 1,055,250 | 3,098 (38/42) | 78,317 (42/42) | 75,219 | 0.245% | 7.422% | 25.3x | 3,098/3,098 |
| T02 | 43 | 1,296,450 | 1,080,375 | 2,405 (27/43) | 57,445 (43/43) | 55,040 | 0.186% | 5.317% | 23.9x | 2,405/2,405 |
| T03 | 42 | 1,266,300 | 1,055,250 | 1,141 (27/42) | 52,984 (42/42) | 51,843 | 0.090% | 5.021% | 46.4x | 1,141/1,141 |
| T04 | 47 | 1,417,050 | 1,180,875 | 1,472 (32/47) | 57,117 (47/47) | 55,645 | 0.104% | 4.837% | 38.8x | 1,472/1,472 |
| T05 | 41 | 1,236,150 | 1,030,125 | 1,608 (33/41) | 73,692 (41/41) | 72,084 | 0.130% | 7.154% | 45.8x | 1,608/1,608 |
| T06 | 42 | 1,266,300 | 1,055,250 | 1,775 (35/42) | 68,417 (42/42) | 66,642 | 0.140% | 6.483% | 38.5x | 1,775/1,775 |
| T07 | 44 | 1,326,600 | 1,105,500 | 961 (29/44) | 55,795 (44/44) | 54,834 | 0.072% | 5.047% | 58.1x | 961/961 |
| T08 | 38 | 1,145,700 | 954,750 | 103 (17/38) | 9,943 (38/38) | 9,840 | 0.009% | 1.041% | 96.5x | 103/103 |
| T09 | 38 | 1,145,700 | 954,750 | 3,677 (24/38) | 68,506 (38/38) | 64,829 | 0.321% | 7.175% | 18.6x | 3,677/3,677 |
| **Total** | **377** | **11,366,550** | **9,472,125** | **16,240** | **522,216** | **505,976** | **0.143%** | **5.513%** | **32.16x** | **16,240/16,240** |

Legacy and Adaptive use different framing domains. Legacy has 30,150 logical
frames per file after its padding/buffering convention; Adaptive has 25,125
complete raw-waveform windows per file. Consequently, `32.16x` is the ratio
of selected-window counts, not a rate ratio computed from one shared
denominator.

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

1. **The repeated result is consistent across all nine groups.** Adaptive selected 522,216 events from 9,472,125 complete windows (5.513%). Legacy selected 16,240 windows from 11,366,550 logical frames (0.143%). Adaptive therefore returned 32.16 times as many selected windows, but the two rates have different denominators.
2. **Adaptive retained the Legacy selections.** 16,240 of 16,240 Legacy-selected windows mapped exactly to an Adaptive selected window; 0 were absent. This is an event-selection containment result, not proof that every added Adaptive window is real AE.
3. **The difference is caused by selection logic, not by using a different FFT.** Both methods use the same 200-sample FFT, Top-1 peak representation, and 20 kHz spacing. The major change is the gate before the FFT: a fixed, group-level and strongly filtered Legacy gate versus a per-file, robust and unfiltered Adaptive gate.
4. **Adaptive frequencies are not expected to be numerically identical to Legacy frequencies.** Adaptive includes many lower-amplitude windows that Legacy discarded, so its median and IQR describe a broader population. The later formal analysis completed a deterministic class-hidden morphology screen, but that screen is neither expert blind review nor physical damage ground truth.
5. **T09 exposed one Legacy robustness limitation.** 1 of 16,240 Legacy-selected windows had no valid local FFT peak. The original `Peak_Freq.m` assumes that every selected window yields a peak and would form unequal output vectors here. The companion exporter recorded this case and excluded it only from the frequency table; the selected window remains counted. This is not evidence of a bad raw file.

## Conclusion

The T01-T09 repeat comparison supports the earlier T02-T04 observation: the Adaptive workflow is a reproducible superset of the Legacy selection on these nine datasets while producing substantially more selected windows. The later MATLAB/Python/Julia validation establishes numerical agreement for Adaptive/Top-3 over T01-T09; Legacy three-language validation remains limited to the complete T01 dataset. This does not establish that adaptive-only windows are genuine AE damage events or that either workflow is superior for a material mechanism.

## Final Follow-on Status (2026-07-29)

The planned waveform follow-on was completed as a deterministic class-hidden
morphology screen. The subsequent T01-T09 waveform-to-workbook alignment
analysis supported none of the nine candidate mappings: `0` groups were
supported and `9` remained unresolved. No load, stress, yield or crack-stage
conclusion is therefore made. Top-3 is retained only as secondary,
descriptive additional spectral information.
