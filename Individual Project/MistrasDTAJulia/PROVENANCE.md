# Frozen-evidence provenance

Upstream access date: 2026-07-27

Evidence closure date: 2026-07-29

## Python source

Repository: https://github.com/d-cogswell/MistrasDTA  
Commit: `6c7dfb6f43f812dccff0c9219bd2c5c82bd98e85`

| File | SHA-256 |
|---|---|
| `upstream/python/LICENSE` | `9ce1b3646592e4611e7cc1ef44078cc1ea74b7ef60ed8e382a96b4bb1b3337c3` |
| `upstream/python/MistrasDTA.py` | `233a394e8b70c7aa90dfb388ad4ab16c52731c3ba33a8b6ada58d7e5cf85c0f6` |
| `upstream/python/test_MistrasDTA.py` | `ec5c955c44bf42d70d8d8c5ed9a924c53e1d988211ca08c922b314610f55cf89` |
| `upstream/python/conftest.py` | `a6fcfdb0faa1fb54d82811f293c8f937bb0e6f08e49f41ea03df3646cb8ea74e` |
| `test/data/python/210527-CH1-15.DTA` | `ecce2c5134ce46f1d63306c8de9d8e174ff3d03d8d5d3877ee895c745a44c50d` |
| `test/reference/210527-CH1-15.npz` | `cb1f27375b0a8e6eb0bfa9dc9ad8788aa4797d61c87b09cfb127e2af65b933ae` |

## MATLAB source

Repository: https://github.com/sayginer/Mistras-AE-MATLAB-Library  
Commit: `43dd5300844f9f6d9be289a25ead319b47800041`

| File | SHA-256 |
|---|---|
| `upstream/matlab/LICENSE` | `23e443a08ef475eee1afc40c4c93249d362226263324944e7da94a09b4e4db2b` |
| `upstream/matlab/AE_readHits_noPara.m` | `5e963e3e8e5cb6d3035cc6e72a45e49c826ea49ffb7179921b0cde3501fd4957` |
| `upstream/matlab/AE_listWaveforms.m` | `812ea9b350e006941467011b5c0212d768eca9109b70489d33cd180ab4098891` |
| `upstream/matlab/AE_plotWaveformByIndex.m` | `dc56130383ab0e26627400fedcb702a8149289daf09e5736ca990d54b7df506c` |
| `test/data/matlab/ExampleDTAfile.DTA` | `e5621d9f867bc51cebde2e49072c2ac24bebd8c64725ae18859bc962e480670e` |

## LLM experiment

| File | SHA-256 |
|---|---|
| `experiments/frozen_prompt.md` | `70c8dcbd741c0ecdbbf9d1b4e3625843260e4060c97bb68e79b19893dc73fd81` |
| `experiments/invocation_prompt.txt` | `d1dc99fe5e3b6bbed9e0c4265e22bd0e920e7ca0738cadbb6391cb63d78edcf3` |
| `experiments/matlab_source_raw_response.txt` | `268988d6a80836f839676b70d24cb500b13bde15cd39d089bebe895136bfd6ec` |
| `experiments/matlab_source_candidate.jl` | `268988d6a80836f839676b70d24cb500b13bde15cd39d089bebe895136bfd6ec` |
| `experiments/python_source_raw_response.txt` | `fa0bbe3c33d3752406ae719d0adc745a4d5a51a820a4612a8d576920522dddf1` |
| `experiments/python_source_candidate.jl` | `fa0bbe3c33d3752406ae719d0adc745a4d5a51a820a4612a8d576920522dddf1` |
| `src/MistrasDTAJulia.jl` | `f7b6f4ace21386782c57c97b7fc59a1af37d3b84722f8a2c3583a96ed5c6fbc4` |

The frozen task was recovered byte-for-byte from Git commit
`824374e98f7791ff46bd4447724da95e70fe2d66`, blob
`7388fde51c43d5ebf9a61ef3b738a079aa9d0f11`. The pre-closure simplified
`TASK.md` had SHA-256
`3b041b95a64b4eb43942e68f896099134c8a2cad4d97a8af5cdd6ca8057e37d3`;
it is retained only as `experiments/task_summary.md` and is not the frozen
generation prompt. The invocation prompt has no trailing newline.

The `.txt` raw response and `.jl` candidate for each source path are
byte-identical. Both candidates were saved and hashed before their first
execution.

## Session and first-run evidence

The two candidate sessions were ephemeral, so their direct rollout files do
not exist. The CLI headers, isolated file inventories, freeze-before-run
sequence and first-run tool results were recovered from parent Codex rollout
`019fa0fb-8468-7f30-8c6e-0b827f0e13e1`, SHA-256
`60116cc1731310cdfbe36ea5fa881fcc87c7b21c574e2ed5d49dbd263d38386a`.
Only the bounded first-run combined outputs are copied into this package; the
unrelated parent transcript is not.

The MATLAB-source first run exited `1`; the Python-source first run exited
`0`. The tool history preserved a combined output stream, not independently
recoverable stdout and stderr. The exact session and capture fields are in
`experiments/experiment_evidence.toml`.

The later Python oracle scorer is separate from the first run. Its initial
harness failure and corrected result are preserved verbatim as
`experiments/python_source_scorer_initial_failure_combined.txt` and
`experiments/python_source_scorer_fixed_run_combined.txt`. The soft-scope
`UndefVarError` is classified as a verification-harness failure, not a model
failure.

## Candidate-to-final lineage

The frozen diagnostic diffs are:

| Diff | SHA-256 | Added | Deleted |
|---|---|---:|---:|
| `experiments/diffs/matlab_source_candidate_to_final.diff` | `89c1b03b335abf0c43ed2e5cbe8052a66d82c107fdb2086dc3807f361061aca9` | 261 | 301 |
| `experiments/diffs/python_source_candidate_to_final.diff` | `333d2c7304ba6a23b36000e32dd727bd52b03d0f1f2265da0ca7bb53d6d7bad3` | 267 | 411 |

The MATLAB-source candidate remained a failed comparison artifact. The final
reader adopted the Python-source parsing route but is a substantial audited
human-in-the-loop reconstruction, not a minimal repair.

## Checksum manifests

Generated dependency-free oracle files have their own checksum manifest at
`test/reference/reference.sha256`. `MANIFEST.sha256` covers the complete
bounded DTA evidence package, excluding itself and ignored transient files.
