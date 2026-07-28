# CT07–Peak_Freq Validation Package

This is the canonical validation and scientific-interpretation package for the
CT07 summary workflow and the Peak_Freq waveform workflow. The two algorithms
remain independent. Their outputs are joined only by the result-layer
`scientific/scientific_analysis.py`.

## Evidence boundary

- CT07: MATLAB oracle plus eight repaired LLM candidates; SMOP is a separate
  deterministic-transpiler baseline.
- Legacy Top-1: MATLAB/Python/Julia full T01 numerical validation.
- Adaptive Top-1/Top-3: MATLAB/Python/Julia full T01–T09 numerical validation.
- Mechanical alignment: data-driven and provisional unless the specimen and
  trigger mapping is independently confirmed.
- Top-3: retained in the main method only if the preregistered descriptive gate
  passes; otherwise it remains an appendix result.
- WFS and R260_2 are separate steel-related cases and are not part of this
  package.

## Current scientific outcome

- All 413 fixed waveform samples were regenerated from raw MAT data; their RMS
  and stored FFT peaks matched the numerical archive.
- All nine presumed waveform-to-CT mappings remain `unresolved`, so no event is
  assigned a mechanical stage.
- Top-3 passed the preregistered descriptive gate and is `retained` as stable
  additional spectral information, not as damage classification.

See the
[Scientific Interpretation Report](results/scientific/Scientific%20Interpretation%20Report.md)
for the evidence and conservative dissertation wording.

## Configure

Edit `validation.toml` if the external waveform/workbook locations or
executable paths differ. Raw MAT and workbook inputs are not copied into this
package; their SHA-256 values are stored under `manifests/`.

No active command depends on the historical temporary or Desktop data paths.

## Run

Fast package verification:

```bash
python3 run_validation.py verify --config validation.toml
```

Rebuild the result-layer scientific outputs from the retained numerical
archives:

```bash
python3 run_validation.py rerun --config validation.toml --stage scientific
```

The complete numerical rerun is also exposed:

```bash
python3 run_validation.py rerun --config validation.toml --stage all
```

The complete rerun requires MATLAB R2026a, Julia 1.12.6 and the Python
environment described under `environment/`. It writes new outputs to a
timestamped staging directory and does not overwrite retained evidence until
the comparison stage passes.

## Scientific review

`results/scientific/waveform_audit_blinded.csv` deliberately hides event class.
Complete the fixed morphology and burst-pattern labels, then run:

```bash
python scientific/scientific_analysis.py unblind --config validation.toml
python scientific/scientific_analysis.py top3 --config validation.toml
```

Pending or predominantly noise-like blind review is treated conservatively:
Top-3 becomes `appendix_only`, never automatically `retained`.
