# Adaptive Top-3 three-language validation record

## Scope and frozen algorithm

The manually written MATLAB exporter is the oracle. Each MAT file is centred
independently, divided into complete 200-sample windows with a 199-sample hop,
and selected with `median(RMS) + 8 * 1.4826 * MAD`. FFT peaks use MATLAB
`findpeaks`, exclude DC and Nyquist, retain up to three ranks and apply a
20 kHz minimum separation.

## First comparison and repair

The first-file comparison exposed one semantic difference: MATLAB
`MinPeakDistance=20` rejects another peak exactly 20 kHz from an already chosen
peak, while the initial Python and Julia translations accepted the equality
boundary. Only the peak-selection functions were changed. Both languages now
require a separation strictly greater than 20 kHz, and synthetic regression
tests preserve this behaviour.

## Final result

T01–T09 contain 377 MAT files and 9,472,125 candidate windows. MATLAB selected
522,216 events, producing 522,216 Top-1 rows and 1,566,634 Top-3 rows. No
selected event in this public batch lacked a valid peak; the zero/no-peak path
is instead covered by synthetic tests.

All nine groups passed for Python and Julia:

- identical file order and candidate-window counts;
- zero missing and extra rows in thresholds, selected events, Top-1 and Top-3;
- zero threshold, event-field, peak-field and no-peak-status mismatches;
- exact event times and frequency bins;
- Top-1 equals Top-3 rank 1 in each language.

At `rtol=1e-12, atol=1e-12`, maximum absolute errors versus MATLAB were:

| Field | Python | Julia |
|---|---:|---:|
| threshold | 1.4200012693477149e-14 | 1.4900190456468287e-14 |
| RMS | 8.881784197001252e-15 | 7.105427357601002e-15 |
| event time (s) | 0 | 0 |
| frequency (kHz) | 0 | 0 |
| magnitude | 3.637978807091713e-12 | 3.637978807091713e-12 |

The magnitude error remains within the stated combined relative/absolute
tolerance. These extra adaptive detections demonstrate three-language numerical
agreement only; they are not evidence of physical damage or improved detection
accuracy.

The current legacy regression also remains closed: MATLAB, Python and Julia
each produce 3,098 Top-1 rows with zero missing, extra or field mismatches.
