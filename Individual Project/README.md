---
status: canonical
last_verified: 2026-07-29
evidence_commit: pending
---

# Individual Project: Canonical Scope and Validation Status

> This README is the sole current project-level statement of scope, validation status and defensible claims. Dated notes and experiment records remain historical evidence and must be interpreted through this overview.

## 中文摘要

本项目研究如何以可审计的 human-in-the-loop 流程，将 MATLAB 声发射分析工作流迁移到开源 Python 和 Julia 实现，并通过 reference output、对称 missing/extra 比较及失败—修复记录验证迁移结果。核心研究对象是 CT07 和 Peak_Freq；DTA、WFS 与 R260_2 构成三个彼此独立、边界受限的钢相关案例。CT07、Legacy Top-1、Adaptive/Top-3、公开 DTA/WFS fixture 及 R260_2 processed workbook 均已有相应证据，但钢相关结论只达到 **format/workflow-level applicability** 或 processed-data exploration，不构成真实钢裂纹检测、损伤分类准确率或全格式兼容性验证。当前剩余工作是论文整合与最终呈现，不再扩展新算法或文件 dialect。

## Dissertation argument

> This project evaluates an auditable human-in-the-loop workflow for migrating MATLAB acoustic-emission analyses to open-source Python and Julia implementations. Numerical references and symmetric comparison are used to identify translation failures and validate corrected implementations. A bounded DTA reader case demonstrates format/workflow-level applicability to an AE data workflow relevant to railway-steel research; it does not validate crack detection in steel.

## Final project hierarchy

| Level | Content | Dissertation role |
|---|---|---|
| Core migration cases | CT07 and Peak_Freq | Main methods and results |
| Controlled steel-related case | DTA | Format/workflow-level applicability |
| Secondary bounded steel-related cases | WFS and R260_2 | Single-fixture validation and processed-data exploration in the thesis body |
| Secondary extensions | Adaptive threshold and Top-3 | Secondary numerical results |
| Explicitly excluded | GUI, complete Mistras replacement, real rail-steel experiments, crack classification, all-format compatibility | Not implemented or claimed as outcomes |

Milestone record: [[Individual Project/Notes/18 Final Validation Milestone Summary|Final Validation Milestone Summary]] is a dated evidence-closure snapshot; this README remains the sole current project-level status.

Writing indexes: [[Thesis Evidence Index]] and [[Session Evidence Index]].
Their project-level integrity anchor is the
[thesis evidence manifest](evidence-chain/THESIS_EVIDENCE_MANIFEST.sha256).

## Research objects and defensible claims

### CT07: LLM-assisted MATLAB to Python/Julia migration

CT07 is an experiment-level mechanical and AE-summary workflow. The MATLAB oracle contains 1,807 mechanical records and 5,850 AE records. Eight **candidate-derived validation runners** were numerically checked against that oracle; SMOP is reported separately as a deterministic-transpiler baseline. Numerical validation of the corrected runners and assessment of the original LLM generations are distinct evidence layers.

The eight prompt, response, original-generation, fixture-normalized and final
runner artifacts are now frozen in the
[candidate evidence manifest](CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidate_manifest.json).
Reconstructed artifacts are labelled explicitly and are not presented as
surviving byte-exact raw files.

Defensible wording:

> Eight candidate-derived validation runners were numerically validated against the MATLAB CT07 oracle.

This does not mean that eight unmodified generations ran successfully, that every generation received only a minimal repair, or that a single observed run establishes the general reliability of a model family.

### Peak_Freq: three-language numerical validation

Peak_Freq is a raw-waveform event-selection and FFT workflow. Its validated levels are:

- **Legacy Top-1:** full T01 MATLAB/Python/Julia validation with 3,098 matching rows.
- **Adaptive Top-1/Top-3:** full T01-T09 MATLAB/Python/Julia validation across 377 files, 9,472,125 candidate windows, 522,216 selected events and 1,566,634 Top-3 rows.

CT07 and Peak_Freq remain separate algorithms. All nine presumed waveform-to-CT mappings are `unresolved`; therefore, no event is assigned a verified load, displacement, stress, yield or crack-growth stage. Top-3 is retained only as descriptive additional spectral information. The waveform review is a **deterministic class-hidden morphology screen**, not expert review and not damage ground truth.

### DTA: bounded steel-related workflow applicability

The DTA case compares MATLAB-source and Python-source LLM translation paths. The final Julia reader has one numerical oracle: the pinned public Python fixture, which contains 8 hits and 8 waveforms. Only the DTA variant exercised by that fixture is supported. Technical validation and prompt-to-result provenance closure are complete for this bounded case; the frozen evidence set is covered by the [DTA evidence manifest](MistrasDTAJulia/MANIFEST.sha256).

Defensible wording:

> A Julia reader was produced for the tested public AEWin/Mistras DTA variant and numerically validated against a Python reference fixture.

The fixture is not identified as rail steel or R260 data. This result is not a MATLAB/Python/Julia three-language numerical oracle, an experimental validation of steel crack detection, or evidence of compatibility with every DTA or WFS version.

## Project-level validation matrix

| workflow | research_role | source_and_target | numerical_reference | dataset_scope | numerical_status | scientific_status | allowed_claim | canonical_evidence |
|---|---|---|---|---|---|---|---|---|
| CT07 | Core LLM-assisted migration case | MATLAB → Python/Julia | MATLAB oracle | CT07 workbook sheet; 1,807 mechanical and 5,850 AE records | Eight candidate-derived runners passed; prompt-to-runner lineage frozen; SMOP reported separately | Mechanical/AE summary only; no raw-waveform mapping | Candidate-derived runners were numerically validated against MATLAB | [Validation package](CT07-PeakFreq-Validation/README.md); [candidate manifest](CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidate_manifest.json); [comparison summary](CT07-PeakFreq-Validation/results/ct07/llm-validation/comparison_summary.json); [experiment record](CT07-PeakFreq-Validation/results/ct07/llm-validation/experiment_record.md); [SMOP summary](CT07-PeakFreq-Validation/results/ct07/smop/smop_comparison_summary.json) |
| Legacy Top-1 | Core waveform migration baseline | MATLAB → Python/Julia | MATLAB | Complete T01; 3,098 rows | Three-language numerical validation passed | Waveform workflow validated; mechanical stage unresolved | Legacy Top-1 is numerically validated across three languages for T01 | [legacy summary](CT07-PeakFreq-Validation/results/peak-frequency/legacy-t01-three-language/legacy-regression-current/comparison_summary.json) |
| Adaptive threshold | Secondary event-selection extension | MATLAB → Python/Julia | MATLAB adaptive reference | T01-T09; 377 files and 522,216 selected events | Three-language numerical validation passed | Additional detections are sensitivity/coverage, not damage truth | Adaptive selection is numerically consistent across three languages for T01-T09 | [aggregate summary](CT07-PeakFreq-Validation/results/peak-frequency/adaptive-three-language/comparison_summary.json); [experiment record](CT07-PeakFreq-Validation/results/peak-frequency/adaptive-three-language/experiment_record.md) |
| Top-3 | Secondary spectral extension | MATLAB → Python/Julia | MATLAB Top-3 reference | T01-T09; 1,566,634 peak rows | Three-language numerical validation passed | Descriptive additional spectral information only | Top-3 supplies stable additional numerical peak information under the tested workflow | [aggregate summary](CT07-PeakFreq-Validation/results/peak-frequency/adaptive-three-language/comparison_summary.json); [scientific report](<CT07-PeakFreq-Validation/results/scientific/Scientific Interpretation Report.md>) |
| DTA | Steel-related format/workflow case | MATLAB/Python source paths → Julia | Public Python fixture | One tested DTA variant; 8 hits and 8 waveforms | Julia fixture validation and evidence closure passed | Format/workflow applicability only | The tested DTA variant was read in Julia and checked against the Python fixture | [DTA README](MistrasDTAJulia/README.md); [evidence manifest](MistrasDTAJulia/MANIFEST.sha256); [final validation](MistrasDTAJulia/results/final_validation.md); [experiment record](MistrasDTAJulia/experiments/experiment_record.md) |
| WFS | Secondary bounded steel-related case | MATLAB → Julia | MATLAB fixture export | One public WFS fixture; 2 channels × 103,424 samples | Exact full-matrix agreement; symmetric missing/extra 0; Julia 26/26 | Single-fixture format/workflow applicability; material and specimen provenance unknown | The tested public WFS fixture is supported by the bounded Julia reader | [WFS README](MistrasWFSJulia/README.md); [manifest](MistrasWFSJulia/MANIFEST.sha256); [comparison](MistrasWFSJulia/results/comparison_summary.toml) |
| R260_2 | Secondary bounded steel-related case | Processed workbook analysis | No raw-waveform oracle | Processed AE-hit workbook labelled R260_2; S3 has 3,553 paired markers | Bounded rerun and package verification passed | Processed hit-level exploration only; grade, units and specimen provenance remain unresolved | A processed workbook labelled R260_2 was explored without reconstructing raw waveforms | [R260_2 README](R2602Analysis/README.md); [manifest](R2602Analysis/MANIFEST.sha256); [provenance](R2602Analysis/PROVENANCE.md) |

## Claims that this project does not make

- No experimental validation of crack detection in steel.
- No damage-classification accuracy claim.
- No validated CT07-to-T01-T09 specimen or mechanical-time mapping.
- No claim of complete DTA or WFS format compatibility.
- No general ranking of LLM model families from single observed runs.
- No claim that adaptive-only detections are confirmed physical AE damage events.

## Evidence hierarchy and update rules

1. This README is the only project-level source for current scope, validation status and defensible claims.
2. Case READMEs and machine-readable summaries provide case-level technical evidence.
3. Notes, Background, Diary and Tools history preserve dated development and experiment evidence; they are not current project status.

When evidence or scope changes:

1. update this README first;
2. update the relevant case README or machine summary second;
3. append to dated logs rather than rewriting their historical state;
4. update `last_verified` and `evidence_commit` here.

## Reproducibility status

A final same-host clean-environment rehearsal completed CT07, Legacy Top-1
T01, Adaptive/Top-3 T01-T09, the scientific analysis, freeze and verify in 61
recorded commands with no nonzero exit. Staged results reproduced the canonical
totals, all 413 morphology figures, and the 0-supported/9-unresolved alignment
status. A copy of the package also passed `verify` from a same-host path
containing spaces. Frozen external inputs remained at their original
locations, so this is not a claim of cross-machine or offline reproducibility.

The first clean attempt is retained separately as an
`environment_declaration_failure`; it stopped before completing CT07 because
the clean Julia project omitted dependencies used by the output helper. The
second rehearsal and both failure/success records are indexed in
[[Thesis Evidence Index]].

## Remaining work before dissertation submission

- integrate the indexed methods, failure evidence, numerical comparisons and limitations into the dissertation;
- assign final manuscript figure/table numbers and captions;
- retain DTA, WFS and R260_2 as separate bounded cases and preserve their stated limitations.
