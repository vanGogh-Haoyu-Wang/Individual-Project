# Fixed candidate-generation task

Act as a senior scientific-computing engineer translating an existing
AEWin/Mistras DTA reader into Julia 1.12.

Read every implementation file under `source/`. Produce one self-contained
Julia module named `MistrasDTAJulia` and output only the raw Julia source,
without Markdown fences or explanation. Do not run or modify files.

Required public interface:

```julia
read_dta(path; read_waveforms=true) -> DTAData
waveform_axes(waveform; time_unit=:us) -> (time, voltage)
```

Required data:

- `DTAData`: hits, waveforms, unknown message counts.
- `HitRecord`: relative time in seconds, UInt8 channel, feature dictionary.
- `WaveformRecord`: relative time, channel, sample rate, trigger delay,
  raw Int16 samples, and scaled voltage.

Required supported dialect:

- Fixture: `test/210527-CH1-15.DTA`.
- Little-endian UInt16 frame length.
- Message IDs 40–49 carry an additional ID byte.
- Msg-42 supplies the dynamic CHID list, channel gain, sample rate, and
  trigger delay.
- Msg-1 supplies hit relative time, channel, and dynamic features.
- Msg-173 supplies SUBID, relative time, channel, ALB, and Int16 waveform.
- Implement RMS, signal-strength, absolute-energy, and voltage scaling from
  the supplied source.

Safety contract:

- Use Julia Base only.
- Check every declared length before reading.
- Errors for truncated frames, invalid setup records, unknown CHIDs, missing
  channel setup, or unsupported waveform layout must include the byte offset.
- Unknown top-level messages must be skipped without losing frame alignment
  and counted by ID.
- `read_waveforms=false` must preserve identical hits while skipping waveform
  decoding.

Out of scope: WFS, GUI, plotting, MAT/HDF5 export, package registration,
automatic support for other DTA dialects, and absolute wall-clock timestamps.
