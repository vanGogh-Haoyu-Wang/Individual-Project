---
status: thesis-evidence-index
last_verified: 2026-07-29
---

# Thesis Evidence Index

Project-level current scope and defensible claims remain in
[[Individual Project/README|Canonical Project Overview]]. This index maps the
current numerical evidence to dissertation claims and records what is still
unavailable. It does not replace case-level manifests or machine summaries.

Path convention:

- **Project-relative** paths are relative to `Individual Project/`.
- **Absolute** paths start at
  `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/`.
- SHA-256 values describe the file bytes verified on 2026-07-29.
- `not_available` means that no supporting artifact was found in the retained
  project evidence. It must not be inferred from a filename, model family or
  later run.
- `not_applicable` means the field does not apply to that activity.

## Seven-Case Thesis Matrix

| Case | Input | Numerical reference | Candidate or implementation | Numerical result | Scientific interpretation level | Planned thesis location | Primary evidence |
|---|---|---|---|---|---|---|---|
| CT07 | `Commercial Tensile Tests.xlsx`, sheet `CT07`; `CT07.m` | MATLAB R2026a oracle | Eight candidate-derived Python/Julia validation runners; original generations and normalized probes remain separate | 1,807 mechanical and 5,850 AE records; 8/8 runners pass with zero missing/extra and five valid PNGs each | Experiment-summary validation only; no raw-waveform or mechanical-stage mapping | Methods and Results | Candidate manifest and CT07 comparison summary |
| SMOP | `CT07.m` and the same CT07 workbook | MATLAB CT07 oracle | SMOP 0.41 raw translation; script-fixed and CT07-scoped runtime-compatible recovery paths | Raw output not executable; 2/2 recovery paths pass the MATLAB comparison | Deterministic-transpiler baseline; evidence of recoverability with intervention | Results and Discussion | SMOP raw score, comparison summary and package manifest |
| Legacy Top-1 | Complete T01 MAT waveform set | MATLAB Legacy Top-1 export | Python and Julia implementations | 3,098 matching rows; zero missing, extra or field mismatches | Validated waveform algorithm for complete T01 only; mechanical mapping unresolved | Results | Legacy T01 comparison summary |
| Adaptive/Top-3 | T01-T09, 377 MAT files | MATLAB adaptive/Top-3 companion exporter | Python and Julia implementations | 9,472,125 complete windows; 522,216 selected events; 1,566,634 Top-3 rows; all groups pass | Numerical agreement only; Top-3 is a secondary descriptive spectral extension; 0/9 mechanical mappings supported | Secondary Results and Discussion | Aggregate comparison, scientific report and alignment summary |
| DTA | Public `210527-CH1-15.DTA` fixture | Public Python fixture oracle | Julia reader developed from isolated MATLAB-source and Python-source candidate paths | 8 hits, 8 waveforms, zero missing/extra, 56/56 Julia tests | Format/workflow-level applicability for one tested DTA variant | Steel-Related Applicability | Complete DTA manifest, experiment evidence and final validation |
| WFS | Public `ExampleWFSdata.wfs` fixture | MATLAB R2026a fixture export | Julia reader | Two channels, 103,424 samples/channel, exact full voltage-matrix equality, 26/26 tests | One-fixture format validation; material and specimen provenance unavailable | Bounded WFS subsection in Steel-Related Applicability | Complete WFS manifest, symmetric comparison and final validation |
| R260_2 | Processed workbook `Copy of current R260_2.xlsx` | No raw-waveform oracle | Streaming ZIP/XML exploratory analysis | S3 contains 3,553 hit/marker pairs with zero missing, extra or ordering mismatches; bounded rerun and full package verification pass | Processed hit-level case only; raw ADC waveform, grade, units and specimen provenance remain unresolved | Bounded R260_2 subsection and Limitations | Complete manifest, provenance, rerun summary and result tables |

## Primary Evidence Files

### CT07

| Role | Project-relative path | Absolute path | SHA-256 |
|---|---|---|---|
| Eight-candidate lineage | `CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidate_manifest.json` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidate_manifest.json` | `8657d7b0e966ecaaeb8451269c142a01930047c24b003a52c97f34b1c6ac93fa` |
| Experiment record | `CT07-PeakFreq-Validation/results/ct07/llm-validation/experiment_record.md` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/results/ct07/llm-validation/experiment_record.md` | `189ea541a2f223751c737c26ed1cdf3cac7ae9fc0a0df33adbc5980b79ac79d2` |
| MATLAB comparison | `CT07-PeakFreq-Validation/results/ct07/llm-validation/comparison_summary.json` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/results/ct07/llm-validation/comparison_summary.json` | `eae63d4e1759f6ae90d3025b68c85c3515b35dbd9b758fbeec28f1a3bba50d85` |

The frozen external CT07 input entries are in
`CT07-PeakFreq-Validation/manifests/inputs.sha256`:

| Input | Absolute path | SHA-256 |
|---|---|---|
| MATLAB source | `/Users/vangogh/Documents/毕设/初始数据&Matlab脚本/CT07.m` | `23b0b5948faa13dd8ffa340b5741bcfb0aaa741ffa400912890fd9ce0416b784` |
| Workbook | `/Users/vangogh/Documents/毕设/初始数据&Matlab脚本/Commercial Tensile Tests.xlsx` | `89033ea6af74f0b99cfe44a1dcda4e59e4fea709d1f4e4c4acba3745edc33b2d` |

### SMOP

| Role | Project-relative path | Absolute path | SHA-256 |
|---|---|---|---|
| Raw score | `CT07-PeakFreq-Validation/results/ct07/smop/smop_raw_score.json` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/results/ct07/smop/smop_raw_score.json` | `a0f7046c7e5ba86e83bd88b77b8f85934123bf91846878c467d924663de7c646` |
| Recovery comparison | `CT07-PeakFreq-Validation/results/ct07/smop/smop_comparison_summary.json` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/results/ct07/smop/smop_comparison_summary.json` | `aa511f6b05b05dbf851aebed3b56aa0c6b27bf8dfe02347b12522c6d7d27d2c7` |
| Environment metadata | `CT07-PeakFreq-Validation/results/ct07/smop/environment_metadata.json` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/results/ct07/smop/environment_metadata.json` | `ddf13a67a29d4486f30a6a1c49e8d04bb7fd8d257334c0fd64e80adeec11748d` |
| SMOP artifact manifest | `CT07-PeakFreq-Validation/results/ct07/smop/manifest.sha256` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/results/ct07/smop/manifest.sha256` | `f2cf4238835149e079cbd6e1344d34ecee1d5af779eb627cd6b594b2c2c294f3` |

### Legacy Top-1

| Role | Project-relative path | Absolute path | SHA-256 |
|---|---|---|---|
| T01 three-language comparison | `CT07-PeakFreq-Validation/results/peak-frequency/legacy-t01-three-language/legacy-regression-current/comparison_summary.json` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/results/peak-frequency/legacy-t01-three-language/legacy-regression-current/comparison_summary.json` | `8a0e2f9d71a48a6f4b248c75fb2ab52b6479a9807fa5ae1379438c2af0259eab` |

The original MATLAB script is externally frozen at:

| Input | Absolute path | SHA-256 |
|---|---|---|
| `Peak_Freq.m` | `/Users/vangogh/Documents/毕设/Haoyu Wang/Peak_Freq.m` | `7c506319d0029990af8d2125af4eb6011011c97333389ac8479b9be885d97a5b` |

The 377 individual MAT files and nine processed workbooks are listed
individually in `CT07-PeakFreq-Validation/manifests/input_inventory.csv` and
`inputs.sha256`; this index does not duplicate 386 per-file rows.

### Adaptive/Top-3 and Scientific Interpretation

| Role | Project-relative path | Absolute path | SHA-256 |
|---|---|---|---|
| Aggregate three-language comparison | `CT07-PeakFreq-Validation/results/peak-frequency/adaptive-three-language/comparison_summary.json` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/results/peak-frequency/adaptive-three-language/comparison_summary.json` | `48e3c9fec1ac7e9fbb1ac49b4c50ef938785b2bf10023b3ca77c0e3d48a9e7ff` |
| Experiment record | `CT07-PeakFreq-Validation/results/peak-frequency/adaptive-three-language/experiment_record.md` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/results/peak-frequency/adaptive-three-language/experiment_record.md` | `e2c258da34407bfbd2e47390fe2175e92f213d4982ab2c1222a8e51ca6ef3cd1` |
| Separate framing table | `CT07-PeakFreq-Validation/results/peak-frequency/legacy-adaptive-framing/t01_t09_comparison_summary.csv` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/results/peak-frequency/legacy-adaptive-framing/t01_t09_comparison_summary.csv` | `48620afc70eb3f0cab3e37963ff9e55f1a11b0ae7fcff274cccd9589a0bbada5` |
| Scientific report | `CT07-PeakFreq-Validation/results/scientific/Scientific Interpretation Report.md` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/results/scientific/Scientific Interpretation Report.md` | `3c6e9589b2695ed766bc28936626bc2c70e9d74001fb0dd1abe9ab4327688e53` |
| Alignment result | `CT07-PeakFreq-Validation/results/scientific/alignment_summary.json` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/results/scientific/alignment_summary.json` | `4d4b1147558277a8d3e41ba2dff92b5f442cf528896d9418b207b2e4772ac7d0` |
| Top-3 bounded decision | `CT07-PeakFreq-Validation/results/scientific/top3_value_summary.json` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/results/scientific/top3_value_summary.json` | `0c1315fb6a52863796c79cf39f4e00116986bf8e5573e381e3ba19755c625ce8` |
| Morphology method | `CT07-PeakFreq-Validation/results/scientific/waveform_morphology_screen_method.json` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/results/scientific/waveform_morphology_screen_method.json` | `6ef6c36eb202c383de15f16d4caf7bbac85d07618932e7ff4a953a2cc286dd8c` |

### Formal CT07/Peak_Freq Package Integrity

| Manifest | Project-relative path | Absolute path | SHA-256 |
|---|---|---|---|
| External inputs | `CT07-PeakFreq-Validation/manifests/inputs.sha256` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/manifests/inputs.sha256` | `b4c3c6c82f70b9443af3b0ec0ac7273a4251a22bbb336c497514b6a1c20e9601` |
| Code | `CT07-PeakFreq-Validation/manifests/code.sha256` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/manifests/code.sha256` | `640b2b177c13e9e60068a8e5706099ec5ca0fe9b2704c5ab57cbdc7f44dfdd8e` |
| Results | `CT07-PeakFreq-Validation/manifests/results.sha256` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/manifests/results.sha256` | `d62aed0282b390903fa482b6b9a9ccca78ce1b79373c37a9b62ee88086117c29` |
| Project summary | `CT07-PeakFreq-Validation/results/validation_summary.json` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/results/validation_summary.json` | `4904f0c9d5199260b7ae9b5e37ae269495ea400524ebad1e60a96b0b6914e61b` |
| Validation matrix | `CT07-PeakFreq-Validation/results/validation_matrix.csv` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/results/validation_matrix.csv` | `1f83a5f063b6d033d77a3f1e08c8375b05137001030bf71fa29273e97ae19b11` |

### Final Clean Rehearsal

The first clean attempt is retained as an
`environment_declaration_failure`: the CT07 Julia project omitted two
dependencies used by its shared output helper. The corrected second attempt
completed all 61 recorded commands with zero nonzero exits. It regenerated
CT07, Legacy Top-1 T01, Adaptive/Top-3 T01-T09 and the complete scientific
analysis, while reusing only the frozen Legacy MATLAB T01-T09 context and MAT
metadata.

| Role | Project-relative path | Absolute path | SHA-256 |
|---|---|---|---|
| First-attempt failure classification | `CT07-PeakFreq-Validation/rehearsals/final-20260729/failure_classification.json` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/rehearsals/final-20260729/failure_classification.json` | `4305eba52b972065d2470c8822e0a81d00e9a5ee77e464cf34372ee2fc809062` |
| Successful rehearsal summary | `CT07-PeakFreq-Validation/rehearsals/final-20260729-r2/rehearsal_summary.json` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/rehearsals/final-20260729-r2/rehearsal_summary.json` | `e9ff3fb9acc19e3c2f2871df2869c319e15a69f04cb0ad7933c9a8c6aeeb9506` |
| Complete command register | `CT07-PeakFreq-Validation/rehearsals/final-20260729-r2/commands.jsonl` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/rehearsals/final-20260729-r2/commands.jsonl` | `f3e0f2aff5a8ae816385876a2530b9aa2990bdcf27f88bea32eaf00480807ea7` |
| Environment record | `CT07-PeakFreq-Validation/rehearsals/final-20260729-r2/environment.json` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/rehearsals/final-20260729-r2/environment.json` | `691725be7865b777fe79d8e1be529ab9174aefee1380722b1d381b12d1cf5f2b` |
| Rehearsal evidence manifest | `CT07-PeakFreq-Validation/rehearsals/final-20260729-r2/manifests/rehearsal_evidence.sha256` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/rehearsals/final-20260729-r2/manifests/rehearsal_evidence.sha256` | `7338870fb170db925d8c29288e398b237b20b328def5622a82f8c2185babd162` |
| Same-host relocation receipt | `CT07-PeakFreq-Validation/rehearsals/final-20260729-r2/relocation_verify_receipt.json` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/CT07-PeakFreq-Validation/rehearsals/final-20260729-r2/relocation_verify_receipt.json` | `c74408b08def357b210d3544518a1c6b82489a1ac91904253b4490ad6861477a` |

This proves a same-host clean-environment rehearsal and relocation check, not
cross-machine or offline reproducibility. The rehearsal is intentionally
ignored by Git because it contains a full large staging result tree; its
manifest and local evidence are retained through dissertation submission.

### DTA

| Role | Project-relative path | Absolute path | SHA-256 |
|---|---|---|---|
| Complete evidence manifest | `MistrasDTAJulia/MANIFEST.sha256` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/MistrasDTAJulia/MANIFEST.sha256` | `ba8602e555a280a08a0752a1e21a81a77a30a75c51ccc4bb234b64d85266f26d` |
| Prompt/session/first-run record | `MistrasDTAJulia/experiments/experiment_evidence.toml` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/MistrasDTAJulia/experiments/experiment_evidence.toml` | `62236cdbfe32d79caa8bccafd5f356171400ee12e3b871c7be9f5e967b5be432` |
| Symmetric comparison | `MistrasDTAJulia/results/comparison_summary.toml` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/MistrasDTAJulia/results/comparison_summary.toml` | `3e24dcebbe9e85dea6e2951ebbbbe9575f95a267181844485c287977bf67d94c` |
| Final validation | `MistrasDTAJulia/results/final_validation.md` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/MistrasDTAJulia/results/final_validation.md` | `9aea60898f30a2c54c613ea49a2f414d7e14570e4e11393ec7558c9483d8ae5f` |

The tested public DTA fixture is:

| Input | Project-relative path | SHA-256 |
|---|---|---|
| `210527-CH1-15.DTA` | `MistrasDTAJulia/test/data/python/210527-CH1-15.DTA` | `ecce2c5134ce46f1d63306c8de9d8e174ff3d03d8d5d3877ee895c745a44c50d` |

### WFS

| Role | Project-relative path | Absolute path | SHA-256 |
|---|---|---|---|
| Complete package manifest | `MistrasWFSJulia/MANIFEST.sha256` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/MistrasWFSJulia/MANIFEST.sha256` | `dda947a7d672eb4a0302ad77742dc176900c49f90529e22021d865dfda4f0146` |
| Upstream/fixture provenance | `MistrasWFSJulia/PROVENANCE.md` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/MistrasWFSJulia/PROVENANCE.md` | `3b69be2c7d80d619c235fbe17bbfe777823b2b05a51736247104de7c3e4264d7` |
| Third-party notice | `MistrasWFSJulia/THIRD_PARTY_NOTICES.md` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/MistrasWFSJulia/THIRD_PARTY_NOTICES.md` | `81b685f8206d763f4cae0b6b727a7235010301cbe98d4836c4deaa43a1aa5393` |
| Fixture/reference manifest | `MistrasWFSJulia/test/reference/reference.sha256` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/MistrasWFSJulia/test/reference/reference.sha256` | `d46b48d78c4391dd76e2c08e4022185af3d1b550b24f405cabc57e2b41c22cd8` |
| Symmetric comparison | `MistrasWFSJulia/results/comparison_summary.toml` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/MistrasWFSJulia/results/comparison_summary.toml` | `20ef2afb94c09ce856bb1e446d9c223dcdec8a67ea0092b02e2b382b75c21673` |
| Final test log | `MistrasWFSJulia/results/final_run.log` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/MistrasWFSJulia/results/final_run.log` | `9f43c7ad3af503686db71aebdd43dcd0b586f7ea92cb165a501c2e2f0f49e231` |
| Environment versions | `MistrasWFSJulia/environment/versions.txt` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/MistrasWFSJulia/environment/versions.txt` | `408b74cd217faf395e154bc461cf86706887dd5f29748a5c2f8eaac34652958f` |
| Final validation | `MistrasWFSJulia/results/final_validation.md` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/MistrasWFSJulia/results/final_validation.md` | `b4d1370f5b260cb61dc6d49fdc8d82880bc424c260d4c8eb97c5e9707813ffb7` |

The tested public WFS fixture is:

| Input | Project-relative path | SHA-256 |
|---|---|---|
| `ExampleWFSdata.wfs` | `MistrasWFSJulia/test/data/ExampleWFSdata.wfs` | `acf7b914900c3d201928e24fd9a3394eb37fbd160cd9e02aae15c41e1be24c43` |

### R260_2

| Role | Project-relative path | Absolute path | SHA-256 |
|---|---|---|---|
| Complete package manifest | `R2602Analysis/MANIFEST.sha256` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/R2602Analysis/MANIFEST.sha256` | `86a821d8e447ecad40a93d37bb41e7bce33a13bf10609cdf1f5d775f244727d5` |
| Provenance and evidence limits | `R2602Analysis/PROVENANCE.md` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/R2602Analysis/PROVENANCE.md` | `55969a85f5ea5bdff67a268855c67b297ad56aebbcd6a934fc732d4cdb6fee2f` |
| Bounded rerun summary | `R2602Analysis/evidence/final-rerun-20260729/rehearsal_summary.json` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/R2602Analysis/evidence/final-rerun-20260729/rehearsal_summary.json` | `8944f7dd9342b15bc31367453b471bbf4fed6bde604432afc6b164ccc4256120` |
| Pre-manifest numerical verification | `R2602Analysis/evidence/final-rerun-20260729/pre_manifest_verification_summary.json` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/R2602Analysis/evidence/final-rerun-20260729/pre_manifest_verification_summary.json` | `101941750da42cd3fb18407efa8f670b10205e677ae2a15fc90d2f50b3d4d051` |
| Machine analysis | `R2602Analysis/results/analysis.json` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/R2602Analysis/results/analysis.json` | `408bea8904c7f0fac40a1955604eb692f4818bf276648fb634ceef78566fdabe` |
| Interpretation report | `R2602Analysis/results/analysis_report.md` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/R2602Analysis/results/analysis_report.md` | `8ccb91149def69ca13bc25f3c21c62c20521934d6c03b79d30f533fd144c176b` |
| Specimen table | `R2602Analysis/results/specimen_summary.tsv` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/R2602Analysis/results/specimen_summary.tsv` | `94d8daa77c85ed2d0f19ed79c73064687fcbca71c30f9de17e045edb7b6336b2` |
| S3 features | `R2602Analysis/results/s3_feature_summary.tsv` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/R2602Analysis/results/s3_feature_summary.tsv` | `de575398844858c83864345c41c8fd8b2483e1e7207e6989a768608f1fc2e063` |
| S3 crack-growth intervals | `R2602Analysis/results/s3_crack_growth.tsv` | `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/R2602Analysis/results/s3_crack_growth.tsv` | `7e38d11f79dbeb0e44b7438ffe1685a8ad9c23d3a648419291385729810c1680` |

The external processed workbook is:

| Input | Absolute path | SHA-256 |
|---|---|---|
| `Copy of current R260_2.xlsx` | `/Users/vangogh/Documents/毕设/Rail Steel/Copy of current R260_2.xlsx` | `2bf80527130a7eab326297a2dc1c17974dbae45cf3840217378169d227f8ea64` |

## Claim-to-Evidence Map

| Claim ID | Thesis-safe claim | Validation level | Primary evidence path | SHA-256 | Thesis location | Claim boundary |
|---|---|---|---|---|---|---|
| CT07-C01 | Eight CT07 candidate-derived runners match the MATLAB oracle for 1,807 mechanical and 5,850 AE records. | Numerical, tested workbook/sheet | `CT07-PeakFreq-Validation/results/ct07/llm-validation/comparison_summary.json` | `eae63d4e1759f6ae90d3025b68c85c3515b35dbd9b758fbeec28f1a3bba50d85` | Results | Does not mean eight original generations ran successfully or received minimal repair. |
| CT07-C02 | The CT07 experiment preserves distinct original-generation, fixture-normalized and candidate-derived validation layers. | Provenance/auditability | `CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidate_manifest.json` | `8657d7b0e966ecaaeb8451269c142a01930047c24b003a52c97f34b1c6ac93fa` | Methods | Reconstructed files are labelled; unavailable sessions are not inferred. |
| SMOP-C01 | SMOP produced recognisable Python text but required intervention; both audited recovery paths match MATLAB. | Deterministic baseline | `CT07-PeakFreq-Validation/results/ct07/smop/smop_comparison_summary.json` | `aa511f6b05b05dbf851aebed3b56aa0c6b27bf8dfe02347b12522c6d7d27d2c7` | Results/Discussion | Not evidence of automatic end-to-end SMOP migration. |
| PEAK-L01 | Legacy Top-1 matches across MATLAB, Python and Julia for complete T01, with 3,098 rows. | Three-language numerical validation | `CT07-PeakFreq-Validation/results/peak-frequency/legacy-t01-three-language/legacy-regression-current/comparison_summary.json` | `8a0e2f9d71a48a6f4b248c75fb2ab52b6479a9807fa5ae1379438c2af0259eab` | Results | Must not be generalized to T01-T09 Legacy three-language validation. |
| PEAK-A01 | Adaptive/Top-3 matches across MATLAB, Python and Julia for T01-T09. | Three-language numerical validation | `CT07-PeakFreq-Validation/results/peak-frequency/adaptive-three-language/comparison_summary.json` | `48e3c9fec1ac7e9fbb1ac49b4c50ef938785b2bf10023b3ca77c0e3d48a9e7ff` | Secondary Results | Numerical agreement is not physical-event or detection-accuracy validation. |
| PEAK-A02 | Legacy and Adaptive use different framing denominators: 11,366,550 logical Legacy frames and 9,472,125 complete Adaptive windows. | Derived statistical summary | `CT07-PeakFreq-Validation/results/peak-frequency/legacy-adaptive-framing/t01_t09_comparison_summary.csv` | `48620afc70eb3f0cab3e37963ff9e55f1a11b0ae7fcff274cccd9589a0bbada5` | Results | The 32.16× value is a selected-window count ratio, not a rate improvement under one denominator. |
| PEAK-A03 | All nine waveform-to-CT mappings are unresolved. | Scientific interpretation | `CT07-PeakFreq-Validation/results/scientific/alignment_summary.json` | `4d4b1147558277a8d3e41ba2dff92b5f442cf528896d9418b207b2e4772ac7d0` | Discussion/Limitations | No load, stress, yield or crack-stage conclusion is released. |
| PEAK-A04 | The waveform check is a deterministic class-hidden morphology screen. | Reproducible morphology screening | `CT07-PeakFreq-Validation/results/scientific/waveform_morphology_screen_method.json` | `6ef6c36eb202c383de15f16d4caf7bbac85d07618932e7ff4a953a2cc286dd8c` | Methods/Discussion | Not expert review and not damage ground truth. |
| PEAK-A05 | Top-3 is retained as a secondary descriptive spectral extension. | Pre-specified follow-on decision | `CT07-PeakFreq-Validation/results/scientific/top3_value_summary.json` | `0c1315fb6a52863796c79cf39f4e00116986bf8e5573e381e3ba19755c625ce8` | Secondary Results/Discussion | Not damage classification, crack-type identification or accuracy improvement. |
| DTA-C01 | The tested DTA variant is read in Julia and matches the public Python fixture for 8 hits and 8 waveforms. | Single-fixture numerical validation | `MistrasDTAJulia/results/comparison_summary.toml` | `3e24dcebbe9e85dea6e2951ebbbbe9575f95a267181844485c287977bf67d94c` | Steel-Related Applicability | Not a three-language oracle, steel-crack experiment or all-DTA claim. |
| WFS-C01 | The tested WFS fixture matches the MATLAB reference exactly over the full two-channel voltage matrix. | Single-fixture numerical validation | `MistrasWFSJulia/results/comparison_summary.toml` | `20ef2afb94c09ce856bb1e446d9c223dcdec8a67ea0092b02e2b382b75c21673` | Steel-Related Applicability | Fixture material/specimen is unknown; no complete WFS compatibility claim. |
| R260-C01 | The processed workbook labelled R260_2 supports bounded hit-level exploratory analysis. | Exploratory processed-data analysis | `R2602Analysis/evidence/final-rerun-20260729/pre_manifest_verification_summary.json` | `101941750da42cd3fb18407efa8f670b10205e677ae2a15fc90d2f50b3d4d051` | Steel-Related Applicability/Limitations | No raw ADC waveform, independent crack-detection validation, confirmed grade or confirmed field units. |

## Project-Level AI-Use Ledger

The canonical machine-readable activity register is:

- Project-relative path:
  `evidence-chain/AI_USE_LEDGER.csv`
- Absolute local-inspection path:
  `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/evidence-chain/AI_USE_LEDGER.csv`
- SHA-256:
  `45327730f6bea3abd770a8536e48b9a041f503f98d1f59f757e4a69364f3cd93`
- Direct link:
  [AI_USE_LEDGER.csv](evidence-chain/AI_USE_LEDGER.csv)

The CSV separates activity status from the availability of model, interface,
reasoning, model-parameter, generation-date and session-ID fields. Every status
column uses only `confirmed`, `not_available`, `unconfirmed` or
`not_applicable`. Prompt/input, response, output artifact and controlling
evidence paths have independent SHA-256 fields. Reconstruction is recorded in
`artifact_origin`, never as an invented status.

| Activity type | Rows | Coverage |
|---|---:|---|
| `model_generation` | 11 | Eight separate CT07 candidates; two separate DTA source sessions; one SMOP `not_applicable` sentinel |
| `agent_assisted_debugging` | 9 | Eight case-level activities plus the final rehearsal harness repair; unavailable model/session attribution remains explicit |
| `researcher_decision` | 3 | CT07 validation contract, Adaptive/Top-3 numerical contract and DTA source-path decision |
| `automated_verification` | 9 | CT07, SMOP, Legacy, Adaptive/Top-3, scientific interpretation, DTA, WFS, R260_2 and the final clean rehearsal are separate rows |

The detailed human-readable session and artifact registry remains
[[Individual Project/Session Evidence Index|Session Evidence Index]]. Neither
index completes an unavailable field from filenames, later outputs or
unretained interaction context.

## Permissions, Licences and Provenance

| Material | Location | Confirmed provenance/licence | Permission or provenance status | Thesis-safe handling |
|---|---|---|---|---|
| CT07 workbook and `CT07.m` | External paths listed above | Input names, paths and SHA-256 confirmed | Owner, dataset licence and redistribution permission: `not_available` | Keep raw inputs external; report hashes and tested sheet; do not redistribute without permission. |
| T01-T09 MAT files, processed workbooks and `Peak_Freq.m` | External paths enumerated by `CT07-PeakFreq-Validation/manifests/input_inventory.csv` | 377 MAT files, nine workbook entries, script path and hashes confirmed | Owner, dataset licence and redistribution permission: `not_available` | Keep raw inputs external; use formal manifests and derived evidence only subject to permission. |
| CT07/Peak_Freq Python dependencies | `CT07-PeakFreq-Validation/environment/requirements.txt` | Exact versions frozen | Consolidated third-party licence notice: `not_available` | Cite software versions; create a licence summary before public redistribution. |
| CT07/Peak_Freq Julia dependencies | Archived `Project.toml` and `Manifest.toml` files | Exact dependency graph frozen | Consolidated third-party licence notice: `not_available` | Cite Julia and direct packages; create a licence summary before public redistribution. |
| MATLAB runtime/toolboxes | `CT07-PeakFreq-Validation/code/peak-frequency/matlab/matlab_environment.txt` | R2026a environment record retained | Proprietary runtime; redistribution is `not_applicable` | Report version/toolbox use; do not distribute MATLAB binaries or licence credentials. |
| SMOP 0.41 | `CT07-PeakFreq-Validation/results/ct07/smop/environment_metadata.json` | PyPI source hash and MIT licence recorded | Complete SMOP licence text is not archived in the formal SMOP result directory | Attribute SMOP/version; preserve or add the upstream MIT text before public redistribution. |
| DTA Python source and fixture | `MistrasDTAJulia/upstream/python/` and `test/data/python/` | d-cogswell/MistrasDTA commit `6c7dfb6f43f812dccff0c9219bd2c5c82bd98e85`; MIT; access date 2026-07-27 | Confirmed in `PROVENANCE.md` and preserved licence | Retain attribution, commit, fixture boundary and licence. |
| DTA MATLAB source | `MistrasDTAJulia/upstream/matlab/` | sayginer/Mistras-AE-MATLAB-Library commit `43dd5300844f9f6d9be289a25ead319b47800041`; MIT | Confirmed in `PROVENANCE.md` and preserved licence | Retain attribution, commit and licence. |
| WFS MATLAB source and fixture | `MistrasWFSJulia/upstream/matlab/` and `test/data/ExampleWFSdata.wfs` | Same sayginer commit; MIT; access date 2026-07-27; complete 23-file package manifest retained | Material, specimen and experiment provenance: `not_available` | Claim only one-fixture format validation; retain MIT notice and package manifest. |
| R260_2 processed workbook | `/Users/vangogh/Documents/毕设/Rail Steel/Copy of current R260_2.xlsx` | Filename, size, workbook schema and SHA-256 confirmed; external-input and complete 34-file package manifests retained | Provider/custodian, acquisition date, data licence, redistribution permission, exact steel grade, field units and specimen provenance: `not_available` | Keep workbook external; treat it as a processed workbook labelled R260_2; no raw-waveform or independent crack-detection claim. |

## Final Figure Register

`thesis_candidate` means that the artifact can support a bounded claim but
still needs final dissertation numbering and captioning. `evidence_archive`
means that the artifact supports auditability and should not be copied in bulk
into the dissertation.

| Figure ID | Artifact | Project-relative or absolute path | Evidence status | Intended use | SHA-256 source |
|---|---|---|---|---|---|
| F01 | Workflow and evidence chain | `evidence-chain/workflow-evidence-chain.svg` | `thesis_candidate` | Methods overview | `881646b4a5f00c77ac3d86cc4fbab17272a7f10bf486d021ec49f54d201b466f` |
| F02 | CT07 five-plot outputs for eight LLM runners | `CT07-PeakFreq-Validation/results/ct07/llm-validation/candidates/` | `evidence_archive`; representative runner/plot not selected | Demonstrate validated plotting contract without ranking models | Individual hashes are in `CT07-PeakFreq-Validation/manifests/results.sha256` (`d62aed0282b390903fa482b6b9a9ccca78ce1b79373c37a9b62ee88086117c29`). |
| F03 | SMOP five-plot outputs for two recovery paths | `CT07-PeakFreq-Validation/results/ct07/smop/validation-candidates/` | `evidence_archive`; representative output not selected | Deterministic baseline recovery evidence | Individual hashes are in the formal results manifest and SMOP manifest. |
| F04 | Peak_Freq mapping-score heatmap | `CT07-PeakFreq-Validation/results/scientific/alignment_diagnostics/mapping_score_heatmap.png` | `thesis_candidate` | Show why mapping remains unresolved | `285a533cfb759e9dd920d179917a9a65897d275900bac3d920656cd27faa1a1c` |
| F05 | Nine activity overlays | `CT07-PeakFreq-Validation/results/scientific/alignment_diagnostics/T01_activity_overlay.png` through `T09_activity_overlay.png` | `evidence_archive` | Mapping diagnostics, not mechanical-stage results | Individual hashes are in the formal results manifest. |
| F06 | 413 waveform morphology plots | `CT07-PeakFreq-Validation/results/scientific/waveform_figures/` | `evidence_archive`; thesis montage not yet available | Support deterministic morphology screen | Individual hashes are in the formal results manifest. |
| F07 | Julia versus Python DTA waveform 1 | `MistrasDTAJulia/results/waveform_01_julia_vs_python.png` | `thesis_candidate` | DTA numerical agreement example | `ff3564f222f2d50fa36ef29189ba8c2985ba1a6d5213a7f17753d1db81fef628` |
| F08 | All eight DTA waveforms | `MistrasDTAJulia/results/all_8_waveforms.png` | `thesis_candidate` | Bounded fixture coverage | `bf8741cf84949e557570480dae7263cec196947f474cea76f0375cb80d7de062` |
| F09 | WFS reader result figure | `not_available` | `not_available` | A validation table currently carries the WFS result | No figure artifact exists in the retained WFS package. |
| F10 | R260_2 S3 hit timing and P-FRQ | `R2602Analysis/results/s3_hit_timing_and_pfrq.png` | `thesis_candidate` | Exploratory hit-level distribution | `27d798d133624ec37aa69b29d4a3451704bb2d1363b76afbe9eadd8f9feae09b` |
| F11 | R260_2 S3 crack-growth exploratory plot | `R2602Analysis/results/s3_crack_growth_exploratory.png` | `thesis_candidate` | Exploratory processed-data illustration | `7f2cce6d6af6d107004d145cc4b4bf3fd9031b6df644c7aeb25dcb3ddf3054e0` |

## Final Table Register

| Table ID | Artifact | Project-relative path | Evidence status | Intended use | SHA-256 |
|---|---|---|---|---|---|
| T01 | Seven-case thesis matrix | This file, `Seven-Case Thesis Matrix` | `thesis_candidate` | Methods/results roadmap | Deferred until final thesis manifest. |
| T02 | CT07 eight-candidate lineage | `CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidate_manifest.csv` | `thesis_candidate` | Condensed model-generation and repair evidence | Contained in formal results manifest. |
| T03 | CT07 numerical comparison | `CT07-PeakFreq-Validation/results/ct07/llm-validation/comparison_summary.json` | `thesis_candidate` | 8/8 result table | `eae63d4e1759f6ae90d3025b68c85c3515b35dbd9b758fbeec28f1a3bba50d85` |
| T04 | SMOP raw/fixed/runtime comparison | `CT07-PeakFreq-Validation/results/ct07/smop/smop_comparison_summary.json` | `thesis_candidate` | Deterministic baseline | `aa511f6b05b05dbf851aebed3b56aa0c6b27bf8dfe02347b12522c6d7d27d2c7` |
| T05 | Legacy T01 comparison | `CT07-PeakFreq-Validation/results/peak-frequency/legacy-t01-three-language/legacy-regression-current/comparison_summary.json` | `thesis_candidate` | 3,098-row validation | `8a0e2f9d71a48a6f4b248c75fb2ab52b6479a9807fa5ae1379438c2af0259eab` |
| T06 | Separate Legacy/Adaptive framing | `CT07-PeakFreq-Validation/results/peak-frequency/legacy-adaptive-framing/t01_t09_comparison_summary.csv` | `thesis_candidate` | Separate denominators and selection counts | `48620afc70eb3f0cab3e37963ff9e55f1a11b0ae7fcff274cccd9589a0bbada5` |
| T07 | Adaptive/Top-3 aggregate comparison | `CT07-PeakFreq-Validation/results/peak-frequency/adaptive-three-language/comparison_summary.json` | `thesis_candidate` | Nine-group validation | `48e3c9fec1ac7e9fbb1ac49b4c50ef938785b2bf10023b3ca77c0e3d48a9e7ff` |
| T08 | Alignment status | `CT07-PeakFreq-Validation/results/scientific/alignment_offsets.csv` and `alignment_summary.json` | `thesis_candidate` | 0 supported / 9 unresolved | Summary: `4d4b1147558277a8d3e41ba2dff92b5f442cf528896d9418b207b2e4772ac7d0` |
| T09 | Top-3 bounded decision | `CT07-PeakFreq-Validation/results/scientific/top3_value_by_group.csv` and `top3_value_summary.json` | `thesis_candidate` | Secondary descriptive value | Summary: `0c1315fb6a52863796c79cf39f4e00116986bf8e5573e381e3ba19755c625ce8` |
| T10 | DTA comparison | `MistrasDTAJulia/results/comparison_summary.toml` | `thesis_candidate` | 8-hit/8-waveform fixture validation | `3e24dcebbe9e85dea6e2951ebbbbe9575f95a267181844485c287977bf67d94c` |
| T11 | WFS validation | `MistrasWFSJulia/results/comparison_summary.toml` | `thesis_candidate` | Two-channel symmetric comparison, exact full matrix and 26/26 tests | `20ef2afb94c09ce856bb1e446d9c223dcdec8a67ea0092b02e2b382b75c21673` |
| T12 | R260_2 specimen inventory | `R2602Analysis/results/specimen_summary.tsv` | `thesis_candidate` | Processed-workbook scope and schema | `94d8daa77c85ed2d0f19ed79c73064687fcbca71c30f9de17e045edb7b6336b2` |
| T13 | R260_2 S3 features | `R2602Analysis/results/s3_feature_summary.tsv` | `thesis_candidate` | Exploratory hit-feature summary | `de575398844858c83864345c41c8fd8b2483e1e7207e6989a768608f1fc2e063` |
| T14 | R260_2 S3 intervals | `R2602Analysis/results/s3_crack_growth.tsv` | `thesis_candidate` with limitations | Exploratory interval analysis | `7e38d11f79dbeb0e44b7438ffe1685a8ad9c23d3a648419291385729810c1680` |

## Workflow Diagram

- Editable source:
  [workflow-evidence-chain.mmd](evidence-chain/workflow-evidence-chain.mmd)
- Thesis-ready vector:
  [workflow-evidence-chain.svg](evidence-chain/workflow-evidence-chain.svg)
- Project-level integrity anchor:
  [THESIS_EVIDENCE_MANIFEST.sha256](evidence-chain/THESIS_EVIDENCE_MANIFEST.sha256)

The thesis manifest uses paths relative to `Individual Project/` and excludes
itself to avoid a self-referential hash.

## Evidence Still Unavailable or Not Yet Frozen

- CT07 generation dates and session IDs for all eight model candidates:
  `not_available`.
- A single retained session record for CT07 runner debugging:
  `not_available`.
- Model/interface/session attribution for the final Legacy, Adaptive/Top-3,
  WFS and R260_2 implementations: `not_available`.
- Formal permission or licence statements for the private CT07, T01-T09 and
  R260_2 datasets: `not_available`.
- Confirmed R260_2 steel grade, field units, specimen series and raw experiment
  provenance: `not_available`.
- A consolidated third-party dependency licence notice for the formal
  CT07/Peak_Freq package: `not_available`.
- A WFS result figure: `not_available`.
- A curated multi-panel morphology figure for the dissertation:
  `not_available`; the 413 source plots remain archived.
- Final thesis figure numbers, captions and manuscript paths:
  `not_available`.

Related notes:

- [[Individual Project/Session Evidence Index|Session Evidence Index]]
- [[Individual Project/Notes/18 Final Validation Milestone Summary|Final Validation Milestone Summary]]
