# MistrasDTAJulia

> Project-level scope and defensible claims:
> [Individual Project overview](../README.md)

Minimal Julia 1.12 reader for the tested AEWin/Mistras DTA variant. The
runtime uses Julia Base only.

## Supported scope

The reader implements the format path exercised by the pinned Python
`MistrasDTA` fixture:

- Msg-42 dynamic hit fields, gain, sample rate, and trigger delay;
- Msg-1 hit time, channel, and features;
- Msg-173 Int16 waveform samples and voltage scaling;
- bounded little-endian frame parsing and explicit format errors.

It intentionally does not support WFS, a GUI or plotting inside the reader,
MAT/HDF5 export, absolute wall-clock timestamps, or automatic DTA-dialect
guessing. The included MATLAB example uses a different feature layout and is
rejected explicitly.

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

Verify the frozen Python fixture and oracle without regenerating them:

```sh
shasum -a 256 -c test/reference/reference.sha256
```

With an environment containing NumPy and pytest, the pinned upstream
regression can also be run directly:

```sh
python -m pytest -q upstream/python/test_MistrasDTA.py \
  --dtaDir=test/data/python --refDir=test/reference
```

Run the Julia validation and then verify the complete evidence package:

```sh
julia --project=. -e 'using Pkg; Pkg.test()'
shasum -a 256 -c MANIFEST.sha256
```

`tools/export_python_oracle.py` is retained to document how the plain oracle
was produced. It is not part of routine verification because the oracle is
frozen.

Generate the optional waveform figures without adding a Julia dependency:

```sh
uv run tools/plot_waveforms.py
```

This writes `results/waveform_01_julia_vs_python.png` and
`results/all_8_waveforms.png`. The script calls the Julia reader, compares its
arrays with the frozen Python oracle, and stops before plotting if they differ.

The test run writes `results/comparison_summary.toml`. It calculates
missing/extra counts separately for hits and waveforms, checks both record
orders, and reports per-field mismatches and maximum absolute errors. The
verified reference result is:

- 8 hits and 8 waveforms;
- zero missing or extra records;
- identical hit and waveform order;
- zero field or waveform-length mismatches;
- all numerical fields within the fixed tolerances.

The 56-test Julia suite includes deliberate delete, add and reorder mutations
that must be rejected by the comparator.

## Interpretation boundary

This project demonstrates a Julia implementation for one publicly testable
AEWin/Mistras DTA variant and format-level applicability to an AE workflow
relevant to railway-steel research. The public fixture is not identified as
rail steel. This work does not validate crack detection in steel, reproduce
the 2012 rail experiment, or establish support for every AEWin/Mistras format
version.

See `experiments/experiment_record.md` for the isolated GPT-5.5
MATLAB-source versus Python-source generation experiment, and
`MANIFEST.sha256` for the frozen artifact set.
