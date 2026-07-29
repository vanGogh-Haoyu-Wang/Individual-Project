# R260_2 processed-workbook evidence package

> Project-level current status:
> [Individual Project overview](../README.md)

This is a secondary, bounded steel-related case for the thesis body. It audits
a processed hit-level workbook labelled `R260_2`; it is not a raw-waveform or
crack-detection validation.

## Validated boundary

- The external workbook is read-only and frozen by `EXTERNAL_INPUTS.sha256`.
- S3 contains 3,553 Msg-1 records, 3,553 Msg-173 waveform markers and 3,553
  sequential time/channel pairs.
- Missing, extra and order-mismatch counts are zero for this bounded S3 audit.
- The ten equal-duration time bins reconcile to 3,553 records.
- The invalid failure row remains in the source but is excluded from the
  nine-interval exploratory calculation.
- Both S3 PNG outputs are checked for a valid PNG signature and non-zero image
  dimensions.

The workbook has no raw ADC waveform oracle. Material grade, specimen mapping,
field units, data licence and the authoritative S3 failure-cycle count remain
unconfirmed; see [PROVENANCE.md](PROVENANCE.md).

## Reproduce without overwriting historical results

Set `R260_WORKBOOK` to the local path of `Copy of current R260_2.xlsx`, then
choose a new staging directory:

```sh
python3 tools/final_rehearsal.py \
  --workbook "$R260_WORKBOOK" \
  --staging evidence/final-rerun-20260729
```

The runner refuses an existing staging directory and never writes to
`results/`. It records commands, separate stdout/stderr logs, exit codes,
timestamps, Python/uv/NumPy/matplotlib/OS details, protected-result hashes and
the generated-output manifest.

After the runner writes the complete package manifest, verify it independently:

```sh
python3 tools/verify_r260.py \
  --workbook "$R260_WORKBOOK" \
  --results evidence/final-rerun-20260729/outputs \
  --package-root .
```

Success requires exit code 0. `MANIFEST.sha256` covers every regular package
file except itself and transient cache files.

## Evidence roles

- `results/`: preserved historical exploratory outputs.
- `evidence/final-rerun-20260729/`: isolated final rerun and audit logs.
- `PROVENANCE.md`: data, material, unit, cycle and permission limitations.
- `MANIFEST.sha256`: complete package integrity manifest.

Allowed thesis wording:

> The processed workbook labelled R260_2 supports a bounded audit of paired
> hit and waveform-marker records. It contains no raw ADC waveform oracle and
> therefore does not validate Peak_Freq, DTA parsing, damage classification or
> crack detection.

No additional sheet dialects are mapped, no workbook formula is repaired and
the result is not connected to the CT07 or Peak_Freq time axes.
