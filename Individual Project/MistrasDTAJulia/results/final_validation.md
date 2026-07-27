# Final validation

Date: 2026-07-27

## Environment

- Julia: 1.12.6
- Python: 3.14.6
- NumPy: 2.5.1
- Python upstream commit:
  `6c7dfb6f43f812dccff0c9219bd2c5c82bd98e85`
- MATLAB upstream commit:
  `43dd5300844f9f6d9be289a25ead319b47800041`

## End-to-end run

1. Pinned upstream Python regression: `1 passed`.
2. Oracle export: `8 hits`, `8 waveforms`.
3. Oracle checksum verification: all six files `OK`.
4. Frozen Python-source candidate:
   - 8 hits and 8 waveforms;
   - zero field and numerical error;
   - seven known message IDs incorrectly classified as unknown,
     totalling 26,732 messages.
5. Final Julia package:
   - low-level decoding: 10/10 passed;
   - invalid setup and unsupported dialects: 8/8 passed;
   - Python fixture numerical regression: 38/38 passed;
   - total: 56/56 passed.

## Numerical acceptance

```text
missing_in_julia = 0
extra_in_julia = 0
field_mismatches = 0
waveform_length_mismatches = 0
max_hit_time_error_s = 0.0
max_feature_error = 0.0
max_waveform_time_error_s = 0.0
max_waveform_voltage_error_v = 0.0
```

Status: **numerically validated against the Python reference**.

This status applies only to the pinned public Python fixture and tested DTA
variant. It is not evidence of real-steel crack-detection accuracy or general
AEWin/Mistras format compatibility.
