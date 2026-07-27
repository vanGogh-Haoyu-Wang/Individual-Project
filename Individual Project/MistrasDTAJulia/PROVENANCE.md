# Frozen-input provenance

Access date: 2026-07-27

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
| `experiments/TASK.md` | `70c8dcbd741c0ecdbbf9d1b4e3625843260e4060c97bb68e79b19893dc73fd81` |
| `experiments/matlab_source_raw_response.txt` | `268988d6a80836f839676b70d24cb500b13bde15cd39d089bebe895136bfd6ec` |
| `experiments/python_source_raw_response.txt` | `fa0bbe3c33d3752406ae719d0adc745a4d5a51a820a4612a8d576920522dddf1` |

The corresponding `.jl` candidate is byte-identical to each raw response.
Generated dependency-free oracle files have their own checksum manifest at
`test/reference/reference.sha256`.
