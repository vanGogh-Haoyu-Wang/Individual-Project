# R260_2 provenance and evidence limits

> Project-level current status:
> [[Individual Project/README|Canonical Project Overview]]

## External input

| Field | Recorded value | Status |
|---|---|---|
| Logical file name | `Copy of current R260_2.xlsx` | confirmed |
| File size | 103,740,621 bytes | confirmed |
| SHA-256 | `2bf80527130a7eab326297a2dc1c17974dbae45cf3840217378169d227f8ea64` | confirmed |
| Data level | Processed hit-level workbook with Msg-173 waveform markers; no raw ADC arrays | confirmed from workbook structure |
| Provider or custodian | `not_available` | not_available |
| Acquisition date | `not_available` | not_available |
| Data licence | `not_available` | not_available |
| Redistribution permission | `not_available`; keep the workbook external | unresolved |
| Original experiment log or data dictionary | `not_available` | not_available |
| Original interactive-analysis session ID | `not_available` | not_available |

The input workbook is not copied into this package. `EXTERNAL_INPUTS.sha256`
freezes its logical file name and digest.

## Material and specimen provenance

- The workbook is labelled `R260_2`, but no surviving metadata independently
  confirms the steel grade, governing material standard, chemical composition,
  rail product form or specimen source. The safe description is **workbook
  labelled R260_2**.
- The relationship between sheets S1–S10 and physical specimens or test runs is
  `unresolved`.
- S1 and S6–S10 do not use the complete shared S2–S5 schema. They are recorded
  as `schema not mapped`, not as zero-hit specimens.

## Field definitions and units

Independent definitions and units are `not_available` for the Mistras-style
fields `COUN`, `ENER`, `DURATION`, `AMP`, `RMS`, `SIG STRNGTH`,
`ABS-ENERGY` and `P-FRQ`, and for workbook configuration values such as load,
frequency and displacement-related fields. In particular:

- P-FRQ values are retained exactly as workbook values and are not labelled kHz.
- Names such as `crack_size_m` in the existing analysis are implementation
  labels, not independent confirmation of the workbook unit.
- No threshold from another rail-steel experiment is transferred to this
  workbook.

## Cycle and formula uncertainty

- S3 configuration records `Cycles to failure = 33,212`.
- The S3 failure row records 33,140 cycles.
- The authoritative value is `unresolved`; neither value is selected as ground
  truth.
- The failure-row AE formula lacks the preceding interval's lower bound. The
  row is retained in the read-only audit but excluded from the nine-interval
  exploratory correlation calculation.
- The workbook is never modified to repair this formula.

## Defensible use

The bounded result is an audit of a processed hit-level workbook. For S3,
3,553 Msg-1 records and 3,553 Msg-173 markers form 3,553 sequential
time/channel pairs. This does not supply raw waveform samples and therefore
does not validate Peak_Freq, DTA/WFS parsing, damage classification or crack
detection. The nine-interval correlations remain exploratory observations.
