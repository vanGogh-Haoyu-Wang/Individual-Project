# T02, T03 and T04: Legacy MATLAB vs Adaptive AE Peak-Frequency Comparison

> [!note] Historical comparison stage
> This note records the T02-T04 evidence available on 2026-07-15. Later
> full-dataset numerical and scientific status is maintained in
> [[Individual Project/README|Canonical Project Overview]].

> Project-level current status: [[Individual Project/README|Canonical Project Overview]]

## Purpose

This note compares the existing legacy `Peak_Freq.m` workflow with the adaptive Python AE workflow on the complete T02, T03 and T04 datasets. The aim is not to claim that the adaptive method is automatically better. The aim is to measure exactly how its event selection and peak-frequency output differ from the validated old MATLAB baseline.

## Methods Compared

### Legacy MATLAB workflow

For each dataset, files were sorted by name. The first file supplied the mean and the upper/lower extrema reference. Each waveform was mean-centred using that first-file mean, padded with one million zeros, and then filtered so that only samples at or beyond the first-file extrema remained. MATLAB `dsp.MovingRMS(200,1)` and `buffer(...,200,1)` were used. Frames with RMS above the fixed threshold `0.1` were selected. A 200-sample FFT then supplied one peak frequency per selected frame.

### Adaptive workflow

Each waveform was mean-centred independently and was not subjected to the extrema-only filter. It was divided into 200-sample windows with one-sample overlap. Its RMS threshold was calculated separately for each file as:

```text
median(RMS) + 8 × 1.4826 × MAD(RMS)
```

The same 1 MHz sampling frequency, 200-sample FFT window, Top-1 peak selection, and 20 kHz peak-separation rule were used. This means that the main change is event selection, not spectral resolution.

### Window matching rule

The legacy MATLAB implementation uses an initial zero in the first `buffer` frame, whereas the adaptive implementation starts at the first raw sample. Both use the same 199-sample hop. For comparison, matching used the same logical frame number in the same source file, with the known one-sample offset accounted for. Each dataset had 30,150 legacy RMS frames per MAT file.

## Overall Result

| Dataset | MAT files | Candidate frames | Legacy events | Adaptive events | Adaptive-only events | Legacy windows also adaptive |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| T02 | 43 | 1,296,450 | 2,405 (0.186%) | 57,445 (4.431%) | 55,040 | 100.0% |
| T03 | 42 | 1,266,300 | 1,141 (0.090%) | 52,984 (4.184%) | 51,843 | 100.0% |
| T04 | 47 | 1,417,050 | 1,472 (0.104%) | 57,117 (4.031%) | 55,645 | 100.0% |

Across all three datasets, **the adaptive method retained every legacy event and added many lower-amplitude candidate events**. The extra detections are substantial, so the adaptive method should be described as a sensitivity-oriented extension of the old method, not as a small numerical variation.

## T02

### Data and event-selection result

- Input waveforms: **43** MAT files.
- Legacy MATLAB frames: **1,296,450** (30,150 frames per file).
- Legacy selected events: **2,405** (0.186% of all frames), found in **27/43** files.
- Adaptive selected events: **57,445** (4.431% of all frames), found in **43/43** files.
- Additional events selected only by the adaptive method: **55,040**.
- Window agreement: **every one of the 2,405 legacy windows was also selected by the adaptive method**. Thus the legacy event set is a strict subset of the adaptive event set for T02.

### Threshold behaviour

The adaptive RMS thresholds were calculated independently for each file using `median + 8 × 1.4826 × MAD`.

| Adaptive threshold statistic | Value |
| --- | ---: |
| Minimum | 0.000966726 |
| Median | 0.001042549 |
| Maximum | 0.015124061 |

The legacy method used the fixed value `0.1`, but its RMS signal had first been changed by the extrema-only filter. Therefore the numerical values `0.1` and the adaptive thresholds are **not directly comparable**. The meaningful comparison is their selection behaviour: the fixed legacy rule suppresses many windows and misses events in 16 complete files, while the adaptive rule finds events in every file.

### Peak-frequency comparison

| Statistic | Legacy MATLAB Top-1 | Adaptive Python Top-1 |
| --- | ---: | ---: |
| Minimum frequency (kHz) | 60 | 60 |
| 25th percentile (kHz) | 165 | 165 |
| Median (kHz) | 170 | 165 |
| 75th percentile (kHz) | 175 | 175 |
| Maximum frequency (kHz) | 465 | 495 |
| Events below 200 kHz | 2,183 (90.77%) | 52,602 (91.57%) |

The central frequency pattern is stable: both methods concentrate strongly below 200 kHz, and the interquartile ranges are 165–175 kHz (legacy) and 165–175 kHz (adaptive). The adaptive method mainly makes the time-frequency record denser; it does not replace the dominant frequency band with a different one.

### Interpretation and conclusion

For T02, the adaptive method is **more sensitive** than the legacy method while retaining all legacy detections. The extra events arise because the adaptive workflow keeps the mean-centred waveform and sets a threshold from the local background level of each file. In contrast, the legacy workflow keeps only values at or beyond extrema derived from the first file, adds padding, and then applies one fixed threshold to the whole group. This makes the legacy method conservative and dependent on the first file's amplitude scale.

This is evidence of broader detection coverage, not yet proof that every additional adaptive event is physically meaningful AE. The additional events could include low-amplitude AE activity, but they could also include machine/electrical noise. A later validation must align event times with the tensile load/displacement record and inspect representative waveforms before assigning physical damage labels.

## T03

### Data and event-selection result

- Input waveforms: **42** MAT files.
- Legacy MATLAB frames: **1,266,300** (30,150 frames per file).
- Legacy selected events: **1,141** (0.090% of all frames), found in **27/42** files.
- Adaptive selected events: **52,984** (4.184% of all frames), found in **42/42** files.
- Additional events selected only by the adaptive method: **51,843**.
- Window agreement: **every one of the 1,141 legacy windows was also selected by the adaptive method**. Thus the legacy event set is a strict subset of the adaptive event set for T03.

### Threshold behaviour

The adaptive RMS thresholds were calculated independently for each file using `median + 8 × 1.4826 × MAD`.

| Adaptive threshold statistic | Value |
| --- | ---: |
| Minimum | 0.000953992 |
| Median | 0.001033292 |
| Maximum | 0.004999455 |

The legacy method used the fixed value `0.1`, but its RMS signal had first been changed by the extrema-only filter. Therefore the numerical values `0.1` and the adaptive thresholds are **not directly comparable**. The meaningful comparison is their selection behaviour: the fixed legacy rule suppresses many windows and misses events in 15 complete files, while the adaptive rule finds events in every file.

### Peak-frequency comparison

| Statistic | Legacy MATLAB Top-1 | Adaptive Python Top-1 |
| --- | ---: | ---: |
| Minimum frequency (kHz) | 105 | 70 |
| 25th percentile (kHz) | 165 | 165 |
| Median (kHz) | 165 | 165 |
| 75th percentile (kHz) | 170 | 170 |
| Maximum frequency (kHz) | 450 | 495 |
| Events below 200 kHz | 1,069 (93.69%) | 48,260 (91.08%) |

The central frequency pattern is stable: both methods concentrate strongly below 200 kHz, and the interquartile ranges are 165–170 kHz (legacy) and 165–170 kHz (adaptive). The adaptive method mainly makes the time-frequency record denser; it does not replace the dominant frequency band with a different one.

### Interpretation and conclusion

For T03, the adaptive method is **more sensitive** than the legacy method while retaining all legacy detections. The extra events arise because the adaptive workflow keeps the mean-centred waveform and sets a threshold from the local background level of each file. In contrast, the legacy workflow keeps only values at or beyond extrema derived from the first file, adds padding, and then applies one fixed threshold to the whole group. This makes the legacy method conservative and dependent on the first file's amplitude scale.

This is evidence of broader detection coverage, not yet proof that every additional adaptive event is physically meaningful AE. The additional events could include low-amplitude AE activity, but they could also include machine/electrical noise. A later validation must align event times with the tensile load/displacement record and inspect representative waveforms before assigning physical damage labels.

## T04

### Data and event-selection result

- Input waveforms: **47** MAT files.
- Legacy MATLAB frames: **1,417,050** (30,150 frames per file).
- Legacy selected events: **1,472** (0.104% of all frames), found in **32/47** files.
- Adaptive selected events: **57,117** (4.031% of all frames), found in **47/47** files.
- Additional events selected only by the adaptive method: **55,645**.
- Window agreement: **every one of the 1,472 legacy windows was also selected by the adaptive method**. Thus the legacy event set is a strict subset of the adaptive event set for T04.

### Threshold behaviour

The adaptive RMS thresholds were calculated independently for each file using `median + 8 × 1.4826 × MAD`.

| Adaptive threshold statistic | Value |
| --- | ---: |
| Minimum | 0.000966592 |
| Median | 0.001035451 |
| Maximum | 0.015830343 |

The legacy method used the fixed value `0.1`, but its RMS signal had first been changed by the extrema-only filter. Therefore the numerical values `0.1` and the adaptive thresholds are **not directly comparable**. The meaningful comparison is their selection behaviour: the fixed legacy rule suppresses many windows and misses events in 15 complete files, while the adaptive rule finds events in every file.

### Peak-frequency comparison

| Statistic | Legacy MATLAB Top-1 | Adaptive Python Top-1 |
| --- | ---: | ---: |
| Minimum frequency (kHz) | 65 | 65 |
| 25th percentile (kHz) | 165 | 165 |
| Median (kHz) | 165 | 165 |
| 75th percentile (kHz) | 170 | 170 |
| Maximum frequency (kHz) | 485 | 495 |
| Events below 200 kHz | 1,318 (89.54%) | 50,935 (89.18%) |

The central frequency pattern is stable: both methods concentrate strongly below 200 kHz, and the interquartile ranges are 165–170 kHz (legacy) and 165–170 kHz (adaptive). The adaptive method mainly makes the time-frequency record denser; it does not replace the dominant frequency band with a different one.

### Interpretation and conclusion

For T04, the adaptive method is **more sensitive** than the legacy method while retaining all legacy detections. The extra events arise because the adaptive workflow keeps the mean-centred waveform and sets a threshold from the local background level of each file. In contrast, the legacy workflow keeps only values at or beyond extrema derived from the first file, adds padding, and then applies one fixed threshold to the whole group. This makes the legacy method conservative and dependent on the first file's amplitude scale.

This is evidence of broader detection coverage, not yet proof that every additional adaptive event is physically meaningful AE. The additional events could include low-amplitude AE activity, but they could also include machine/electrical noise. A later validation must align event times with the tensile load/displacement record and inspect representative waveforms before assigning physical damage labels.

## Cross-Dataset Conclusion

1. The comparison is technically trustworthy because the legacy MATLAB workflow had already been validated row by row against its Python and Julia reproductions on T01, and the same validated MATLAB exporter was used here.
2. T02, T03 and T04 show the same selection relationship: legacy events are fully contained within the adaptive event set.
3. The dominant Top-1 peak-frequency band remains below 200 kHz in every dataset. Therefore the adaptive method changes detection density much more than it changes the central frequency character of the selected events.
4. The legacy method is highly dependent on one global amplitude reference and its fixed threshold; it produced no events in several full waveform files in every group. The adaptive method adjusts to the noise scale of each file and produced events in every file.
5. The adaptive method is promising as a transferable AE event-selection improvement, but it should not yet be described as a validated damage-classification algorithm. The next scientific check is to compare the adaptive-only events with tensile load/displacement, specimen behaviour, and representative waveform/spectrum quality.

## Practical Next Step

For a supervisor discussion, the defensible statement is:

> The existing MATLAB peak-frequency method has been reproduced and used as a baseline. On T02–T04, an adaptive per-file RMS threshold preserved all legacy-selected windows while detecting additional low-amplitude windows in every file. The dominant peak-frequency band remained stable. The next stage is physical validation of the additional detections against the tensile-test record, rather than assuming that more detections automatically mean more damage.

## Output Locations

- Legacy MATLAB outputs: `/Users/vangogh/Documents/temp/ae-peak-frequency/outputs/t02-matlab-legacy`, `t03-matlab-legacy`, and `t04-matlab-legacy`.
- Adaptive Python outputs: `/Users/vangogh/Documents/temp/ae-peak-frequency/outputs/t02-python-adaptive`, `t03-python-adaptive`, and `t04-python-adaptive`.

## Final Status Addendum (2026-07-29)

Adaptive/Top-3 was subsequently validated across T01-T09 in
MATLAB/Python/Julia using 9,472,125 Adaptive complete windows, 522,216
selected events and 1,566,634 Top-3 rows. The deterministic class-hidden
morphology screen was completed, but it is not expert blind review or damage
ground truth. The attempted waveform-to-workbook mapping supported `0` of
the `9` groups, so no load, stress, yield or crack-stage interpretation is
made. Top-3 remains secondary descriptive spectral information.
