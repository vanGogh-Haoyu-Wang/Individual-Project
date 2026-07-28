# CT07–Peak_Freq scientific interpretation

## Outcome

The completed analysis separates numerical equivalence from physical
interpretation.

- The event catalogue contains 522,216 adaptive windows.
- 16,240 are exact `file_name + start_sample` matches to a Legacy-selected
  window; 505,976 are adaptive-only.
- Two events have one valid peak, ten have two, and 522,204 have three.
- The 2-hop burst view reduces the event windows to 258,993 representatives.
- Every retained waveform sample reproduces its stored RMS and FFT peak
  magnitudes within the numerical tolerance.

These facts describe the output population. They do not identify damage.

## Waveform audit

The fixed sample contains 413 events:

- 108 preregistered group/class/RMS-quantile samples;
- 12 events with fewer than three valid peaks;
- the one Legacy-selected event without a valid local FFT peak;
- 292 file-boundary events.

The blind audit uses only waveform shape, RMS/threshold ratio and burst
membership. It does not use the matched/adaptive-only class. The deterministic
rubric labelled 54 samples impulsive, 26 oscillatory, 38 noise-like and 295
ambiguous; none met the clipping definition after quantisation was correctly
distinguished from clipping. The plots were also visually spot-checked across
the fixed classes.

The audit is a reproducible morphology screen, not expert damage labelling.
Because boundary and edge cases are deliberately over-sampled, its percentages
must not be presented as prevalence estimates for the 522,216-event population.

## Mechanical time alignment

The `CT-07` mechanical and AE-summary columns reproduce the CT07 MATLAB oracle:

- 1,807 mechanical rows;
- 5,850 AE rows;
- all shared values within `rtol=1e-12, atol=1e-12`.

This establishes the workbook bridge only. It does not establish which raw
waveform group belongs to that specimen.

For each of the 81 waveform/CT combinations, the analysis searched offsets at
0.5, 1 and 2 second resolution, ran 1,000 circular-shift permutations and used
file-jackknife bootstrap offsets. The globally optimal one-to-one assignment
was not the identity mapping. T01, T02, T04, T05, T07 and T09 each scored a
different CT group above their same-number candidate; the remaining diagonal
pairs also failed at least one preregistered gate. All nine mappings are
therefore `unresolved`.

Consequences:

- no event is assigned a definitive load, displacement, strain or stress stage;
- `aligned_events.csv.gz` and stage summaries intentionally contain no
  physically assigned events;
- offsets in `alignment_offsets.csv` are diagnostics, not calibrated clocks;
- supervisor confirmation or an independent trigger marker is required before
  mechanical-stage interpretation.

## Top-3 scope decision

At the 2-hop burst level:

- median Rank-2/Rank-1 magnitude ratios range from 0.390 to 0.588;
- median Rank-3/Rank-1 ratios range from 0.242 to 0.399;
- cross-band secondary peaks occur in 0.819 to 0.959 of representatives,
  depending on group;
- the availability, magnitude and cross-band criteria pass in all nine groups;
- the pass/fail conclusion is unchanged for 1-hop, 2-hop and 5-hop clustering
  and leave-one-group-out analysis;
- the blind morphology screen is not dominated by noise-like or clipped cases.

The preregistered decision is therefore `retained`: Top-3 may remain in the main
method as stable additional spectral information. It must not be described as
crack-type identification, improved detection accuracy, or physical damage
validation.

## Conservative dissertation wording

> Adaptive thresholding and ranked spectral peaks were numerically consistent
> across MATLAB, Python and Julia for the tested T01–T09 waveform collection.
> A deterministic waveform audit and file-level sensitivity analysis supported
> retaining Top-3 as additional descriptive spectral information. However, a
> nine-by-nine data-driven alignment did not uniquely support the presumed
> T01–T09 to CT-01–CT-09 mapping. The added adaptive detections therefore
> cannot yet be assigned to mechanical loading stages or interpreted as
> confirmed damage events.

