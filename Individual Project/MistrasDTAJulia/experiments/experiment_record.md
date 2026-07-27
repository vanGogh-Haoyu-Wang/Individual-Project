# GPT-5.5 DTA-to-Julia source-path experiment

## Research question

> Under the same target interface and Python DTA oracle, does MATLAB or Python
> source code provide the same LLM with a more reliable starting point for a
> Julia DTA reader?

This is a two-source LLM-generation experiment with a Python numerical oracle.
It is not a MATLAB/Python/Julia same-file equivalence claim.

## Fixed method

- Date: 2026-07-27
- Model: `gpt-5.5`
- Reasoning effort: `xhigh`
- Prompt: `TASK.md`
- Prompt SHA-256:
  `70c8dcbd741c0ecdbbf9d1b4e3625843260e4060c97bb68e79b19893dc73fd81`
- Python source commit:
  `6c7dfb6f43f812dccff0c9219bd2c5c82bd98e85`
- MATLAB source commit:
  `43dd5300844f9f6d9be289a25ead319b47800041`
- Target fixture: `210527-CH1-15.DTA`
- Numerical oracle: pinned `210527-CH1-15.npz`, excluding absolute
  `TIMESTAMP` exactly as in the upstream Python test

Two parts ran in separate temporary directories with read-only sandboxes . Each saw the same task and fixture, but only its assigned source. Neither session could see the
other candidate or the final implementation. Candidates were saved and hashed before execution.

## Frozen candidates

| Path | Session | SHA-256 |
|---|---|---|
| MATLAB source | `019fa582-f69b-7061-878e-afb14d409ac4` | `268988d6a80836f839676b70d24cb500b13bde15cd39d089bebe895136bfd6ec` |
| Python source | `019fa58b-67a9-7f83-9bd1-34b4e6336a87` | `fa0bbe3c33d3752406ae719d0adc745a4d5a51a820a4612a8d576920522dddf1` |

The `.txt` raw response and `.jl` candidate for each path are byte-identical.
The original candidates were never edited.

## First-run comparison

| Criterion | MATLAB-source candidate | Python-source candidate |
|---|---|---|
| Compiles | Yes | Yes |
| Reads fixture | No | Yes |
| Hits/waveforms | No result | 8 / 8 |
| Oracle field mismatches | Not measurable | 0 |
| Maximum numeric error | Not measurable | 0 |
| Silent-alignment risk | High | Lower |
| First defect | Local `count` shadows `count(...)`, causing `MethodError` during setup parsing | Seven known message IDs reported as unknown; 26,732 messages misclassified |

### MATLAB-source failure classification

The first blocking error is LLM-added Julia code: the candidate binds an
integer named `count` and later attempts to call `count(...)`. The candidate
also inferred setup records heuristically from bytes because the supplied
MATLAB source does not describe the dynamic Python-fixture dialect. It was not
used as the final implementation base.

### Python-source result classification

The Python-source candidate reproduced all tested hit fields and waveform
values with zero observed numeric error. Its first remaining defect was
classification rather than numeric decoding: messages handled as known but
unused by the final scope were counted as unknown.

It also required human correction to meet the complete safety contract:

- use the specified typed public fields instead of aliases and
  `Dict{String,Any}`;
- report a dedicated `DTAFormatError` with byte offsets;
- reject empty, truncated, unknown-CHID, missing-setup, and unsupported-dialect
  inputs deterministically;
- distinguish known skipped messages from unknown messages;
- lock the core to the pinned Python CHID layout so the MATLAB fixture cannot
  be silently interpreted as equivalent;
- return the required named tuple from `waveform_axes`;
- keep only `:us` and `:s`, avoiding speculative units and API aliases.

The final module follows the Python-source parsing route but is a separate
human-verified implementation. The two generated candidates remain experimental
evidence, not maintained production alternatives.

## Final verification

The final Julia reader passes:

- bounded frame and endian tests;
- invalid setup, missing setup, unknown CHID, and unsupported dialect tests;
- the full public Python fixture regression;
- hit-only mode;
- trigger-delay-adjusted waveform-axis checks.

`results/comparison_summary.toml` is the machine-readable result. At the
verified run it reports:

- `missing_in_julia = 0`
- `extra_in_julia = 0`
- `field_mismatches = 0`
- `waveform_length_mismatches = 0`
- all recorded maximum absolute errors equal to `0.0`

## Claim boundary

> A Julia reader was produced for the tested AEWin/Mistras DTA variant and
> numerically validated against a public Python reference fixture. The
> MATLAB- and Python-source translation paths were compared under a fixed
> LLM-assisted workflow. This demonstrates format-level applicability to an
> AE data workflow relevant to railway steel research, rather than
> experimental validation of crack detection in steel.

The fixture has no confirmed rail-steel provenance. WFS, other DTA dialects,
real steel experiments, crack-detection accuracy, and full Mistras
compatibility remain out of scope.
