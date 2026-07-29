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
- Codex CLI: `0.140.0`
- Frozen task: `frozen_prompt.md`
- Prompt SHA-256:
  `70c8dcbd741c0ecdbbf9d1b4e3625843260e4060c97bb68e79b19893dc73fd81`
- CLI invocation: `invocation_prompt.txt`
- Invocation SHA-256:
  `d1dc99fe5e3b6bbed9e0c4265e22bd0e920e7ca0738cadbb6391cb63d78edcf3`
- Python source commit:
  `6c7dfb6f43f812dccff0c9219bd2c5c82bd98e85`
- MATLAB source commit:
  `43dd5300844f9f6d9be289a25ead319b47800041`
- Target fixture: `210527-CH1-15.DTA`
- Numerical oracle: pinned `210527-CH1-15.npz`, excluding absolute
  `TIMESTAMP` exactly as in the upstream Python test

The recoverable user prompt surface consists of the frozen task file and CLI
invocation. Platform-internal system instructions are not claimed as archived.
The pre-closure simplified `TASK.md` is retained as `task_summary.md`; it is
not the generation prompt.

## Isolated source sessions

Two ephemeral Codex sessions ran in separate temporary directories with
read-only sandboxes and ignored user/project rules and configuration:

| Source path | Session | Visible implementation files |
|---|---|---|
| MATLAB | `019fa582-f69b-7061-878e-afb14d409ac4` | `AE_readHits_noPara.m`, `AE_listWaveforms.m`, `AE_plotWaveformByIndex.m` |
| Python | `019fa58b-67a9-7f83-9bd1-34b4e6336a87` | `MistrasDTA.py` |

Both sessions saw the same frozen task and public DTA fixture. Neither saw the
NPZ oracle, the other source path, the other candidate or the final reader.
The exact visible-file inventories and session settings are frozen in
`experiment_evidence.toml`. Generation-time OS information is not available;
the requested target was Julia 1.12 and the first executions used Julia
1.12.6.

## Frozen candidates

| Path | Session | SHA-256 |
|---|---|---|
| MATLAB source | `019fa582-f69b-7061-878e-afb14d409ac4` | `268988d6a80836f839676b70d24cb500b13bde15cd39d089bebe895136bfd6ec` |
| Python source | `019fa58b-67a9-7f83-9bd1-34b4e6336a87` | `fa0bbe3c33d3752406ae719d0adc745a4d5a51a820a4612a8d576920522dddf1` |

The `.txt` raw response and `.jl` candidate for each path are byte-identical.
The original candidates were never edited. Rollout chronology confirms that
each response was copied and hashed before its first execution.

## First-run evidence

The original tool history preserved combined process output and exit status,
but not separable stdout and stderr. Therefore:

- `matlab_source_first_run_combined.txt` is the verbatim combined output from
  the MATLAB candidate's first execution (`exit 1`);
- `python_source_first_run_combined.txt` is the verbatim combined output from
  the Python candidate's first execution (`exit 0`);
- the two `*_first_run_summary.md` files are later narrative summaries, not
  raw process logs;
- `stream_separation = not_available` is recorded rather than reconstructed.

## First-run comparison

| Criterion | MATLAB-source candidate | Python-source candidate |
|---|---|---|
| Compiles | Yes | Yes |
| Reads fixture | No | Yes |
| Hits/waveforms | No result | 8 / 8 |
| Oracle comparison in first-run process | Not performed | Not performed |
| Silent-alignment risk | High | Lower |
| First defect | Local `count` shadows `count(...)`, causing `MethodError` during setup parsing | Seven known message IDs reported as unknown; 26,732 messages misclassified |

The Python first-run process printed only the hit count, waveform count and
unknown-message dictionary. It did not load the NPZ-derived oracle and is not
the source of the later zero-mismatch result.

## Subsequent Python candidate scorer evidence

The separate scorer first exited 1 because of a Julia soft-scope
`UndefVarError` in the verification harness. Its verbatim combined output is
preserved in `python_source_scorer_initial_failure_combined.txt`. After the
harness was corrected, the second scorer exited 0 and reported:

- 8 hits and 8 waveforms;
- `field_mismatches = 0`;
- zero hit-time, feature, waveform-time and waveform-voltage maximum errors;
- seven known-but-unused IDs still classified as unknown.

That successful scorer output is preserved verbatim in
`python_source_scorer_fixed_run_combined.txt`. The scorer failure is classified
as `verification_harness_failure`, not a candidate failure. No equivalent
oracle score was produced for the blocked MATLAB-source candidate.

### MATLAB-source failure classification

The first blocking error is LLM-added Julia code: the candidate binds an
integer named `count` and later attempts to call `count(...)`. The candidate
also inferred setup records heuristically from bytes because the supplied
MATLAB source does not describe the dynamic Python-fixture dialect. It was not
used as the final implementation base.

### Python-source result classification

The subsequent corrected scorer showed that the Python-source candidate
reproduced all tested hit fields and waveform values with zero observed
numeric error. Its first-run process itself established only the 8/8 record
counts and the remaining classification defect: messages handled as known but
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

The final module follows the Python-source parsing route but is a separate,
substantial human-in-the-loop, human-verified implementation. It is not a
minimal patch of the candidate. The two generated candidates remain
experimental evidence, not maintained production alternatives.

## Candidate-to-final intervention

The frozen unified diffs are diagnostic evidence:

| Comparison | Insertions | Deletions | Lineage meaning |
|---|---:|---:|---|
| MATLAB candidate → final | 261 | 301 | Not selected and not repaired |
| Python candidate → final | 267 | 411 | Parsing route selected; substantial audited reconstruction |

Intervention categories were the typed public contract, byte-offset errors,
frame/setup/dialect checks, known-versus-unknown message classification,
waveform metadata and axes contracts, explicit rejection of the MATLAB
fixture dialect, and negative/oracle tests.

The scorer captures and classification are machine-indexed in
`experiment_evidence.toml`.

## Final verification

The final Julia reader passes:

- bounded frame and endian tests;
- invalid setup, missing setup, unknown CHID, and unsupported dialect tests;
- the full public Python fixture regression;
- hit-only mode;
- trigger-delay-adjusted waveform-axis checks.

`results/comparison_summary.toml` is the machine-readable result. Its
comparison now calculates both sides before any common-prefix field
comparison, reports hit and waveform order explicitly, and includes
delete/add/reorder tamper regressions. At the verified run it reports:

- `missing_in_julia = 0`
- `extra_in_julia = 0`
- hit and waveform order both match
- `field_mismatches = 0`
- `waveform_length_mismatches = 0`
- all per-field maximum absolute errors are within the fixed tolerances

The full prompt, responses, candidates, captures, diffs, source, tests,
results and figures are covered by `../MANIFEST.sha256`.

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
