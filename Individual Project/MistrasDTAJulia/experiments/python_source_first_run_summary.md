# Python-source first-run summary

> [!warning] Reconstructed narrative
> This is a post-run summary, not a raw stdout/stderr capture. The verbatim
> combined tool output is preserved in `python_source_first_run_combined.txt`;
> separate stdout and stderr streams are not available.

MODEL: gpt-5.5
REASONING EFFORT: xhigh
SESSION: 019fa58b-67a9-7f83-9bd1-34b4e6336a87
PROMPT SHA-256: 70c8dcbd741c0ecdbbf9d1b4e3625843260e4060c97bb68e79b19893dc73fd81
CANDIDATE SHA-256: fa0bbe3c33d3752406ae719d0adc745a4d5a51a820a4612a8d576920522dddf1

COMMAND (exact parent invocation):
'/Users/vangogh/.julia/juliaup/julia-1.12.6+0.aarch64.apple.darwin14/Julia-1.12.app/Contents/Resources/julia/bin/julia' -e 'include("experiments/python_source_candidate.jl"); using .MistrasDTAJulia; data=read_dta("test/data/python/210527-CH1-15.DTA"); println("hits=", length(data.hits)); println("waveforms=", length(data.waveforms)); println("unknown=", data.unknown_message_counts)'

RESULT:
hits=8
waveforms=8
unknown=Dict{UInt8, Int64}(0x31 => 1, 0x0b => 1, 0x2c => 2,
0x26 => 1, 0x6b => 1, 0x02 => 26721, 0x74 => 5)

This first process did not load the NPZ-derived oracle or calculate field or
numeric mismatches.

FIRST DEFECT:
The core records were returned, but seven known-unimplemented message IDs
were incorrectly reported as unknown, totalling 26,732 messages.

SUBSEQUENT SCORER/HARNESS EVIDENCE:
The first scorer process (`call_NLOfOdDXADdC6BWQpB7mA9BT`) exited 1 because
of a Julia soft-scope error in the verification harness. After that harness
was corrected, `call_1stt8Cyyxb5zFS0qVIxfOU3v` exited 0 and produced the
following oracle comparison. These values are not part of the candidate's
first-run process capture.

hits=8
waveforms=8
field_mismatches=0
max_hit_time_error_s=0.0
max_feature_error=0.0
max_waveform_time_error_s=0.0
max_waveform_voltage_error_v=0.0
unknown_message_entries=7
unknown_message_total=26732
