# MistrasDTAJulia

Minimal Julia 1.12 reader for the tested AEWin/Mistras DTA variant. The
runtime uses Julia Base only.

## Supported scope

The reader implements the format path exercised by the pinned Python
`MistrasDTA` fixture:

- Msg-42 dynamic hit fields, gain, sample rate, and trigger delay;
- Msg-1 hit time, channel, and features;
- Msg-173 Int16 waveform samples and voltage scaling;
- bounded little-endian frame parsing and explicit format errors.

It intentionally does not support WFS, GUI/plotting, MAT/HDF5 export, absolute
wall-clock timestamps, or automatic DTA-dialect guessing. The included MATLAB
example uses a different feature layout and is rejected explicitly.

## Usage

```julia
using MistrasDTAJulia

data = read_dta("test/data/python/210527-CH1-15.DTA")
axes = waveform_axes(data.waveforms[1])

length(data.hits)       # 8
length(data.waveforms)  # 8
```

`waveform_axes` returns a named tuple containing a trigger-delay-adjusted time
axis and the waveform voltage. Time units are `:us` by default or `:s`.

To read hit records without decoding waveform payloads:

```julia
hits_only = read_dta(path; read_waveforms=false)
```

## Reproduce the evidence

The Python oracle requires NumPy. Run it with the existing project Python
environment or another isolated environment containing NumPy:

```sh
python tools/export_python_oracle.py
shasum -a 256 -c test/reference/reference.sha256
```

Run the Julia validation:

```sh
julia --project=. -e 'using Pkg; Pkg.test()'
```

The test run writes `results/comparison_summary.toml`. The verified reference
result is:

- 8 hits and 8 waveforms;
- zero missing or extra records;
- zero field or waveform-length mismatches;
- zero observed hit, feature, waveform-time, and waveform-voltage error.

## Interpretation boundary

This project demonstrates a Julia implementation for one publicly testable
AEWin/Mistras DTA variant and format-level applicability to an AE workflow
relevant to railway-steel research. The public fixture is not identified as
rail steel. This work does not validate crack detection in steel, reproduce
the 2012 rail experiment, or establish support for every AEWin/Mistras format
version.

See `experiments/experiment_record.md` for the isolated GPT-5.5
MATLAB-source versus Python-source generation experiment.
