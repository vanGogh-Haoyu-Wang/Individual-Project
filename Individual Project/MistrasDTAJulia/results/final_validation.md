# Final validation

Date: 2026-07-29

## Environment

- Julia: 1.12.6
- Python: 3.14.6
- NumPy: 2.5.1
- pytest: 9.1.1
- Python upstream commit:
  `6c7dfb6f43f812dccff0c9219bd2c5c82bd98e85`
- MATLAB upstream commit:
  `43dd5300844f9f6d9be289a25ead319b47800041`

## Evidence closure

- Frozen task SHA-256:
  `70c8dcbd741c0ecdbbf9d1b4e3625843260e4060c97bb68e79b19893dc73fd81`
- CLI invocation SHA-256:
  `d1dc99fe5e3b6bbed9e0c4265e22bd0e920e7ca0738cadbb6391cb63d78edcf3`
- MATLAB raw response and candidate are byte-identical.
- Python raw response and candidate are byte-identical.
- Both first-run combined outputs and exit codes were recovered from the
  original parent rollout.
- Candidate-to-final diffs and intervention categories are frozen.
- `MANIFEST.sha256` covers the complete bounded evidence set and passes its
  checksum and path-set checks.

## End-to-end run

1. Pinned upstream Python regression: `1 passed`.
2. Frozen oracle checksum verification: all six files `OK`.
3. Frozen MATLAB-source candidate:
   - compilation succeeded;
   - first fixture read exited `1` with the preserved `MethodError`;
   - no hit or waveform result was returned.
4. Frozen Python-source candidate:
   - first fixture read exited `0`;
   - 8 hits and 8 waveforms were returned;
   - seven known message IDs were incorrectly classified as unknown,
     totalling 26,732 messages.
5. Final Julia package:
   - low-level decoding: 10/10 passed;
   - invalid setup and unsupported dialects: 8/8 passed;
   - Python fixture numerical regression: 38/38 passed;
   - total: 56/56 passed.
6. Comparator tamper checks:
   - one deleted hit and waveform were reported as missing;
   - one added hit and waveform were reported as extra;
   - reordered records were rejected with zero missing/extra but failed order
     checks.
7. Waveform figures:
   - `waveform_01_julia_vs_python.png`: valid 3300 × 1740 PNG;
   - `all_8_waveforms.png`: valid 3600 × 3000 PNG.

## Numerical acceptance

```text
hits expected/actual/missing/extra = 8 / 8 / 0 / 0
waveforms expected/actual/missing/extra = 8 / 8 / 0 / 0
missing_in_julia = 0
extra_in_julia = 0
hit_order_matches = true
waveform_order_matches = true
field_mismatches = 0
waveform_length_mismatches = 0
max_hit_time_error_s = 0.0
max_feature_error = 0.0
max_waveform_time_error_s = 0.0
max_waveform_voltage_error_v = 0.0
```

All hit features and waveform metadata have zero recorded mismatch. Raw-count
arrays match exactly. All recorded per-field maximum absolute errors are
`0.0`.

Status: **numerically validated against the Python reference**.

This status applies only to the pinned public Python fixture and tested DTA
variant. MATLAB and Python were isolated LLM source paths; MATLAB is not a
second numerical oracle for this fixture. The result is format/workflow-level
applicability evidence, not real-steel crack-detection validation or general
AEWin/Mistras format compatibility.
