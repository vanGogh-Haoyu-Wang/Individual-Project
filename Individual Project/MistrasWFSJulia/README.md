# MistrasWFSJulia

> Project-level scope and defensible claims:
> [Individual Project overview](../README.md)

Minimal Julia 1.12 reader for the public `ExampleWFSdata.wfs` layout from the
pinned Mistras AE MATLAB Library. The Julia runtime uses Base only.

## Supported scope

The reader implements the branch exercised by the fixture:

- active channel, hardware, gain/filter and timestamp header records;
- WFS sync metadata and FIFO offsets;
- 1,024- or 4,096-sample Int16 data chunks;
- per-channel FIFO alignment;
- MATLAB-reference millivolt scaling and time axes;
- bounded reads and explicit format errors with byte offsets.

Legacy Express/PCI headers, other WFS dialects, streaming partial reads, GUI
and plotting are intentionally excluded until a public fixture can validate
them.

## Usage

```julia
using MistrasWFSJulia

data = read_wfs("test/data/ExampleWFSdata.wfs")
axes = waveform_axes(data, 1)

size(data.voltage_mv)  # (2, 103424)
```

`waveform_axes` accepts the hardware channel number. It returns time in
seconds by default or microseconds with `time_unit=:us`; voltage is in mV.

## Reproduce the evidence

Generate the MATLAB oracle:

```sh
/Applications/MATLAB_R2026a.app/bin/matlab -batch \
  "cd tools; export_matlab_oracle"
```

Run the Julia regression:

```sh
julia --project=. test/runtests.jl
```

The full two-channel Julia voltage matrix is compared with the MATLAB output,
not merely with plotted images or summary statistics.

## Interpretation boundary

This validates one public WFS format fixture. The fixture has no documented
material or experiment provenance, so it is not evidence of steel or rail
crack detection. It complements, but is independent from, analysis of the
processed workbook labelled `R260_2`.
