---
title: "Auditable Human-in-the-Loop Migration of MATLAB Acoustic-Emission Workflows to Python and Julia"
author: "Haoyu Wang"
programme: "MSc, University of Birmingham"
status: "Draft skeleton"
date: "2026"
---

# Final Report Draft Skeleton

> 使用说明：本骨架以英文最终报告为目标。中文提示用于说明每一节应写什么，正式提交前应删除。所有定量结论均应回到下方列出的 canonical evidence 核验。不要从早期笔记恢复已经被后期证据否定或收窄的表述。

## Working Title

**Recommended title**

> Auditable Human-in-the-Loop Migration of MATLAB Acoustic-Emission Workflows to Python and Julia

**Alternative title**

> From LLM-Generated Drafts to Numerically Validated Scientific Software: Acoustic-Emission Case Studies in Python and Julia

---

# Abstract

> 建议最后写，约250–350词。按 Background → Aim → Methods → Results → Conclusion 五部分压缩。

## Background

- MATLAB scientific workflows can be difficult to reuse in open-source environments.
- Large language models can accelerate code migration, but syntactically plausible output is not necessarily executable or numerically correct.
- Acoustic-emission analysis provides a useful test case because it combines irregular experimental data, signal processing, plotting and domain-specific interpretation.

## Aim

This project evaluates an auditable human-in-the-loop workflow for migrating selected MATLAB acoustic-emission analyses to Python and Julia, with particular emphasis on numerical equivalence, failure provenance, reproducibility and bounded applicability to workflows relevant to railway-steel research.

## Methods

- CT07 spreadsheet/plotting workflow translated through eight observed LLM candidate paths.
- Original generation, fixture-normalised probe and candidate-derived validation runner treated as separate evidence layers.
- SMOP 0.41 evaluated as a deterministic transpiler baseline.
- Legacy Peak_Freq Top-1 reproduced in MATLAB, Python and Julia.
- Adaptive RMS threshold and Top-3 spectral reporting implemented and compared across T01–T09.
- DTA and WFS Julia readers assessed using pinned public fixtures and numerical references.
- A processed workbook labelled R260_2 analysed as a bounded hit-level case.
- Symmetric missing/extra comparisons, numerical tolerances, negative tests, SHA-256 manifests and a final clean-environment rehearsal used for verification.

## Principal Results

- CT07 MATLAB oracle: 1,807 mechanical and 5,850 AE records.
- Eight of eight candidate-derived CT07 runners passed the MATLAB comparison; each produced five valid PNG outputs.
- SMOP raw output was not executable, but two audited recovery paths passed the MATLAB comparison.
- Legacy Top-1: 3,098 rows matched across MATLAB, Python and Julia for complete T01.
- Adaptive/Top-3: 377 files, 9,472,125 complete windows, 522,216 selected events and 1,566,634 Top-3 rows matched across MATLAB, Python and Julia.
- Mechanical alignment: zero supported and nine unresolved waveform-to-workbook mappings.
- DTA: eight hits and eight waveforms matched the public Python fixture; 56/56 Julia tests passed.
- WFS: two channels × 103,424 samples matched the MATLAB reference exactly; 26/26 tests passed.
- Final same-host clean rehearsal: 61/61 commands exited successfully.

## Conclusion

> 建议结论核心：LLM的价值是加速初稿、解释与调试；科学可靠性来自reference、自动测试、人工判断和保守的claim boundary。钢相关案例只证明format/workflow-level applicability，不证明真实钢裂纹检测准确率。

---

# Acknowledgements

> 感谢导师、数据/代码提供者和学校支持。不要在没有确认的情况下推断私人数据的owner或licence。

---

# Declaration of Generative-AI Use

> 根据学校要求调整格式。建议与项目AI-use ledger一致。

Suggested content:

- Generative AI was used for code-generation experiments, debugging assistance, planning and language support.
- Model-generated code was not treated as scientific authority.
- Original generations, later repairs, researcher decisions and automated verification were recorded separately where evidence was available.
- The author remained responsible for research design, execution, numerical verification, interpretation and final claims.
- Unrecoverable model parameters, dates or session identifiers are reported as `not_available`, rather than reconstructed.

Primary evidence:

- `Individual Project/evidence-chain/AI_USE_LEDGER.csv`
- `Individual Project/Session Evidence Index.md`

---

# List of Abbreviations

| Abbreviation | Meaning |
|---|---|
| AE | Acoustic Emission |
| ADC | Analogue-to-Digital Converter |
| DTA | AEWin/Mistras DTA data format |
| FAIR | Findable, Accessible, Interoperable and Reusable |
| FFT | Fast Fourier Transform |
| HITL | Human-in-the-Loop |
| LLM | Large Language Model |
| MAD | Median Absolute Deviation |
| RMS | Root Mean Square |
| SMOP | Small MATLAB and Octave to Python compiler |
| WFS | AEWin/Mistras waveform stream format |

---

# 1. Introduction

## 1.1 Research Background

> 说明MATLAB在科研中的价值和迁移需求；开源、透明性、可重复性；生成式AI带来的机会与风险；AE为何是一个适合研究科学代码迁移的复杂案例。

Suggested opening argument:

> Scientific-code migration is not a purely syntactic task. A translated program may compile, produce plausible figures and still alter the scientific meaning of the input data or numerical algorithm. This risk is particularly important when large language models are used to translate experimental analysis workflows whose assumptions are partly implicit in file layouts, toolbox behaviour and plotting conventions.

## 1.2 Problem Statement

- MATLAB-to-Python/Julia translation can fail at data, algorithm, API and output-contract boundaries.
- Static inspection cannot establish numerical equivalence.
- LLM output can appear polished while mishandling physical worksheet columns, missing values, frame boundaries or peak-selection semantics.
- Steel-related applicability must be demonstrated without overstating the provenance or scientific meaning of limited public fixtures.

## 1.3 Aim

> To develop and evaluate an auditable human-in-the-loop methodology for migrating selected MATLAB acoustic-emission workflows to Python and Julia, and to assess the bounded applicability of this methodology to AE data workflows relevant to railway-steel research.

## 1.4 Objectives

1. Record structured MATLAB-to-Python/Julia generation experiments and distinguish original output from later repair.
2. Establish numerical references for the CT07 and Peak_Freq workflows.
3. Identify and classify translation, environment and verification-harness failures.
4. Validate corrected implementations using symmetric comparisons and explicit tolerances.
5. Evaluate Adaptive thresholding and Top-3 reporting without conflating numerical agreement with physical damage validation.
6. Demonstrate bounded Julia support for tested DTA and WFS fixtures.
7. Audit a processed workbook labelled R260_2 while preserving its provenance limitations.
8. Produce an integrity-verifiable evidence package and AI-use record.

## 1.5 Research Questions

### RQ1

To what extent can Python and Julia reproduce the numerical outputs of the selected MATLAB acoustic-emission workflows?

### RQ2

What failure modes arise in LLM-assisted scientific-code migration, and how does a human-in-the-loop verification workflow detect and correct them?

### RQ3

What additional numerical information is produced by Adaptive RMS thresholding and Top-3 spectral reporting, and what scientific interpretation can the available evidence support?

### RQ4

To what extent can the migration workflow be applied to publicly testable DTA/WFS formats and a processed workbook relevant to railway-steel AE research?

## 1.6 Contributions

- An auditable evidence hierarchy separating generation, normalisation, repair and validation.
- MATLAB-reference numerical validation for CT07 and Peak_Freq cases.
- Empirical failure taxonomy grounded in actual execution logs.
- A deterministic SMOP baseline showing recoverability and limitations.
- Three-language validation of Legacy Top-1 and Adaptive/Top-3 workflows.
- Bounded Julia DTA and WFS readers with symmetric numerical comparisons.
- A conservative R260_2 processed-data audit.
- SHA-256 manifests, AI-use ledger and a complete same-host rehearsal record.

## 1.7 Scope and Explicit Exclusions

Included:

- CT07 and Peak_Freq as core migration cases.
- DTA as the principal controlled steel-related workflow case.
- WFS and R260_2 as secondary bounded cases.
- Adaptive threshold and Top-3 as secondary numerical extensions.

Excluded:

- GUI development.
- Complete Mistras/AEWin replacement.
- Compatibility with all DTA/WFS dialects.
- New rail-steel experiments.
- Crack-classification or damage-detection accuracy claims.
- Automatic mapping of Peak_Freq events to mechanical stages without independent evidence.

## 1.8 Report Structure

> 用一段话简述第2–7章。

---

# 2. Literature Review

## 2.1 Acoustic Emission and Structural Monitoring

- Definition of discrete AE.
- Typical acquisition chain: sensor, pre-amplifier, acquisition system.
- Time-domain and frequency-domain features.
- Influence of material, propagation, coupling and environmental noise.

## 2.2 AE Signal Processing

### 2.2.1 RMS Event Selection

- Moving RMS as an energy-sensitive event-selection measure.
- Fixed-threshold limitations.
- Need to measure or estimate background noise.

### 2.2.2 FFT and Peak Frequency

- Top-1 peak frequency as a compact spectral descriptor.
- Information loss when a waveform contains multiple spectral components.
- Top-N peaks as a descriptive extension.
- Frequency alone is insufficient to establish a damage mechanism.

### 2.2.3 Interpretation and Ground Truth

- Difference between signal clustering and physical damage identification.
- Importance of time/load evolution, independent observations and expert validation.
- Risks of transferring composite-material frequency bands directly to steel.

## 2.3 Scientific-Code Migration

- MATLAB ecosystem and proprietary-toolbox dependency.
- Python and Julia as open-source target environments.
- Syntax translation versus semantic and numerical equivalence.
- Spreadsheet layout, missing values, indexing and library semantics.

## 2.4 LLM-Assisted Code Translation

- Productivity benefits.
- Bugs introduced during translation.
- Hallucinated or inappropriate APIs.
- Plausible code and documentation can hide invalid scientific assumptions.

## 2.5 Human-in-the-Loop and Tool-Mediated Validation

- LLM as translator/middleware rather than final authority.
- Iterative loop: generate → execute → compare → diagnose → repair → verify.
- Researcher as reviewer, evaluator and decision maker.
- Deterministic tools and test oracles as guardrails.

## 2.6 Reproducibility, FAIR and Responsible AI Use

- Provenance of prompts, responses, code, inputs and results.
- Dependency and environment recording.
- SHA-256 manifests.
- Transparency about unavailable session/model parameters.
- Data confidentiality and redistribution limits.

## 2.7 Railway-Steel AE and Mistras/AEWin Workflows

- Rail-steel AE research as an application context.
- DTA and WFS data workflows.
- Difference between workflow applicability and experimental crack-detection validation.
- Public fixture limitations.

## 2.8 Research Gap

> 建议结尾：现有文献分别讨论LLM迁移、AE分析和开源工具，但缺少一个把原始生成、首次失败、人工干预、数值oracle、科学解释边界和可复现证据统一起来的具体案例研究。

---

# 3. Materials, Data and Software Environment

## 3.1 Overview of Research Cases

| Case | Input | Reference | Target | Role |
|---|---|---|---|---|
| CT07 | Commercial Tensile Tests workbook, CT07 sheet | MATLAB R2026a oracle | Python/Julia | Core migration case |
| SMOP | CT07.m and workbook | MATLAB CT07 oracle | Python recovery paths | Deterministic baseline |
| Legacy Top-1 | Complete T01 MAT set | MATLAB exporter | Python/Julia | Core waveform baseline |
| Adaptive/Top-3 | T01–T09, 377 MAT files | MATLAB companion exporter | Python/Julia | Secondary numerical extension |
| DTA | Public 210527-CH1-15.DTA fixture | Public Python NPZ-derived reference | Julia | Principal steel-related workflow case |
| WFS | Public ExampleWFSdata.wfs | MATLAB R2026a export | Julia | Secondary format case |
| R260_2 | Processed workbook | No raw-waveform oracle | Streaming analysis | Exploratory processed-data case |

## 3.2 CT07 Data

- Physical worksheet layout.
- Separate mechanical and AE domains.
- 1,807 mechanical records.
- 5,850 AE records.
- Input names and SHA-256 values.
- Private/external data handling and redistribution status.

## 3.3 Peak_Freq Waveform Archive

- T01–T09 groups.
- 377 MAT files.
- Sampling frequency: 1 MHz.
- First `data` column used as waveform input.
- 200-sample windows.
- Input ordering and frozen inventory.

## 3.4 DTA and WFS Public Fixtures

- Upstream repositories and pinned commits.
- MIT licences.
- Fixture/reference boundaries.
- Unsupported dialects.
- Unknown material provenance of public fixtures.

## 3.5 R260_2 Processed Workbook

- External, read-only workbook.
- Approximate size and hash.
- Processed hit-level records and Msg-173 markers.
- No raw ADC waveform arrays.
- Unconfirmed grade, field units, specimen mapping and licence.

## 3.6 Software and Runtime Environments

- MATLAB R2026a and relevant toolbox functions.
- Python versions and pinned dependencies.
- Julia 1.12.6 and project manifests.
- SMOP 0.41 and NetworkX compatibility patch.
- OS and same-host reproducibility boundary.

## 3.7 LLM Models and Interfaces

> 用“observed run”而不是一般模型能力排名。列出Gemini、Sonnet、DeepSeek、GPT和相应interface/reasoning label。不可确认的date、session或内部参数统一写`not_available`。

## 3.8 Evidence Hierarchy

Define explicitly:

1. `original_generation`;
2. `fixture_normalized_probe`;
3. `candidate_derived_validation_runner`;
4. numerical result and comparator;
5. researcher interpretation and claim boundary.

---

# 4. Methodology

## 4.1 Overall Human-in-the-Loop Workflow

Insert workflow diagram:

- `Individual Project/evidence-chain/workflow-evidence-chain.svg`

Describe:

```text
source workflow
→ structured prompt / deterministic transpiler
→ frozen generation
→ first execution
→ failure classification
→ researcher-supervised repair
→ numerical oracle comparison
→ negative/tamper tests
→ scientific interpretation boundary
→ manifest and rehearsal
```

## 4.2 Prompt Design and Experimental Controls

- Same scientific task and target contract where possible.
- Model/interface differences acknowledged.
- Single observed run per configuration; no general model ranking.
- Fixture-identifier changes separated from model errors.
- Original files frozen or reconstructed explicitly from surviving records.

## 4.3 CT07 MATLAB Oracle

- Execute MATLAB companion runner.
- Preserve physical row numbers.
- Filter mechanical and AE domains independently.
- Export CSV/MAT/metadata.
- Acceptance: zero missing/extra, zero order/row/field mismatch, five valid PNGs.
- Tolerance: `rtol=1e-12`, `atol=1e-12`.

## 4.4 CT07 Candidate Evaluation

For each candidate record:

- model/interface/language;
- original-generation status;
- first environment failure;
- first code-level failure;
- fixture-normalised result;
- repair categories;
- final numerical result.

Important methodological statement:

> The validated runners were candidate-derived audited implementations, not a claim that eight untouched generations executed successfully or required equivalent repair effort.

## 4.5 SMOP Baseline

- Translation smoke test.
- Raw `IndentationError` and runtime-chain failures.
- Script-fixed recovery.
- CT07-scoped runtime-compatible recovery.
- Same MATLAB comparator as CT07 candidates.

## 4.6 Legacy Peak_Freq Top-1

Document the original algorithm:

- deterministic file order;
- first-file mean/extrema;
- one-million-sample zero padding;
- extrema filtering;
- `dsp.MovingRMS(200,1)`/buffer framing;
- fixed RMS threshold 0.1;
- 200-point FFT;
- 20 kHz minimum peak distance;
- Top-1 export.

Explain the framing discovery:

> The first MATLAB frame contains an initial zero followed by the first 199 samples. Reproducing this convention resolved the initial two-row discrepancy.

## 4.7 Adaptive Threshold and Top-3

Adaptive threshold:

```text
threshold = median(window RMS) + 8 × 1.4826 × MAD(window RMS)
```

Algorithm contract:

- centre each file independently;
- complete 200-sample windows;
- 199-sample hop;
- per-file threshold;
- FFT excludes DC and Nyquist;
- up to three peaks;
- accepted peak separation strictly greater than 20 kHz to reproduce MATLAB `findpeaks` behaviour.

## 4.8 Numerical Comparison Method

- Compare both expected and actual record sets.
- Report missing and extra independently.
- Check stable order.
- Compare fields within stated tolerances.
- Verify Top-1 equals Top-3 rank 1.
- Include synthetic tests for zero/no-peak and 20 kHz boundary cases.

## 4.9 Scientific Follow-On Analysis

### 4.9.1 Event Catalogue

- Exact matched key: `file_name + start_sample`.
- 522,216 Adaptive events.
- 16,240 matched Legacy/Adaptive.
- 505,976 Adaptive-only.

### 4.9.2 Deterministic Class-Hidden Morphology Screen

- Fixed 413-event sample.
- Class hidden during morphology assignment.
- Deterministic signal morphology, not expert labels.
- Oversampling of boundary cases prevents prevalence interpretation.

### 4.9.3 Mechanical Alignment

- 81 waveform/workbook combinations.
- Offset search, permutations and file-jackknife stability.
- Pre-specified support criteria.
- Unsupported mappings remain unresolved.

### 4.9.4 Top-3 Decision Rule

- Burst-level representative events.
- Rank-2/Rank-1 and Rank-3/Rank-1 magnitude ratios.
- Availability and cross-band criteria.
- Sensitivity to clustering hop and leave-one-group-out analysis.

## 4.10 DTA Source-Path Experiment

- Same GPT-5.5 XHigh target task.
- Isolated MATLAB-source and Python-source sessions.
- Same public fixture.
- Neither session saw the NPZ oracle or the other source path.
- Freeze candidates before first execution.
- Compare first-run behaviour.
- Final reader based on audited Python parsing route.
- Symmetric comparator and delete/add/reorder tamper tests.

## 4.11 WFS Reader Validation

- MATLAB fixture export.
- Julia Base-only reader.
- Full matrix comparison over all 206,848 voltage values.
- Explicit supported and excluded layout branches.

## 4.12 R260_2 Streaming Audit

- Read XLSX as ZIP/XML without loading or modifying the entire workbook.
- Map S2–S5 shared schema.
- Use S3 as bounded detailed case.
- Preserve formula errors.
- Exclude invalid failure interval from exploratory correlations.
- Do not infer units or steel grade.

## 4.13 Reproducibility and Integrity Verification

- Input, code and result SHA-256 manifests.
- Protected historical-artifact hashes before and after rehearsal.
- Isolated staging outputs.
- Separate failed and successful rehearsal evidence.
- Same-host relocation test.
- No cross-machine/offline claim.

---

# 5. Results

## 5.1 CT07 Original-Generation Failure Patterns

Suggested summary table:

| Candidate | Language | First relevant failure | Main intervention category | Final status |
|---|---|---|---|---|
| Gemini | Python | Mixed strings/floats during plotting | Numeric coercion; independent masks; output contract | Passed |
| Sonnet | Python | Header handling left metadata rows | Numeric coercion; independent masks; CLI/export | Passed |
| DeepSeek | Python | Mixed object arrays | Data cleaning; independent masks; output contract | Passed |
| GPT-5.5 | Python | Original strict-run evidence unavailable; normalised probe made figures but did not export PNGs | Two-domain masks; CLI/headless export | Passed |
| Gemini | Julia | Main call commented; explicit call failed mixed-cell conversion | Entry point; physical matrix; masks; output contract | Passed |
| Sonnet | Julia | Fixture mismatch then nine-column inference | Full worksheet read; restore two AE rows; twin-X fix | Passed |
| DeepSeek | Julia | Nine-column inference and bounds failure | Physical matrix; mixed-cell conversion; masks | Passed |
| GPT-5.5 | Julia | Fixture mismatch then column 10 missing | Physical matrix; masks; callable CLI; twin-X fix | Passed |

## 5.2 CT07 Numerical Validation

Report:

- 8/8 candidate-derived runners passed.
- 1,807 mechanical and 5,850 AE rows each.
- Zero missing/extra, order, matrix-row and field mismatches.
- Five valid PNG files per runner.
- Maximum errors remained within tolerance.

Recommended wording:

> Eight candidate-derived validation runners were numerically validated against the MATLAB CT07 oracle for the tested workbook and worksheet.

## 5.3 SMOP Result

- Raw translation emitted recognisable text but failed compilation.
- Failure chain documented.
- Script-fixed and runtime-compatible paths both passed.
- Do not count SMOP among the eight LLM candidates.

## 5.4 Legacy Top-1 Result

| Measure | MATLAB | Python | Julia |
|---|---:|---:|---:|
| Rows | 3,098 | 3,098 | 3,098 |
| Missing/extra | — | 0/0 | 0/0 |
| Maximum time error | — | 0 s | 0 s |
| Maximum frequency error | — | 0 kHz | 0 kHz |
| Maximum magnitude error | — | 5.684×10⁻¹³ | 5.684×10⁻¹³ |

State clearly: complete T01 only.

## 5.5 Adaptive/Top-3 Result

| Group | Files | Complete windows | Selected events | Top-3 rows |
|---|---:|---:|---:|---:|
| T01 | 42 | 1,055,250 | 78,317 | 234,949 |
| T02 | 43 | 1,080,375 | 57,445 | 172,334 |
| T03 | 42 | 1,055,250 | 52,984 | 158,951 |
| T04 | 47 | 1,180,875 | 57,117 | 171,348 |
| T05 | 41 | 1,030,125 | 73,692 | 221,073 |
| T06 | 42 | 1,055,250 | 68,417 | 205,250 |
| T07 | 44 | 1,105,500 | 55,795 | 167,385 |
| T08 | 38 | 954,750 | 9,943 | 29,828 |
| T09 | 38 | 954,750 | 68,506 | 205,516 |
| **Total** | **377** | **9,472,125** | **522,216** | **1,566,634** |

State:

- All nine groups passed for Python and Julia against MATLAB.
- Frequencies and event times matched exactly.
- Maximum threshold/RMS/magnitude errors remained within tolerance.

## 5.6 Legacy-versus-Adaptive Selection Context

- Legacy logical frames: 11,366,550.
- Legacy selected windows: 16,240.
- Adaptive complete windows: 9,472,125.
- Adaptive selected events: 522,216.
- Adaptive retained 16,240/16,240 Legacy selections.
- Adaptive-only: 505,976.
- `522,216 / 16,240 = 32.16×` is a selected-count ratio, not a common-denominator rate ratio and not an accuracy increase.

## 5.7 Morphology and Mechanical Alignment

Morphology sample:

| Label | Count |
|---|---:|
| Impulsive | 54 |
| Oscillatory | 26 |
| Noise-like | 38 |
| Ambiguous | 295 |
| Total | 413 |

Alignment:

| Status | Groups |
|---|---:|
| Supported | 0 |
| Unresolved | 9 |

Interpretation:

- No event receives a verified mechanical stage.
- Morphology labels are not expert damage labels.

## 5.8 Top-3 Bounded Decision

- Rank-2/Rank-1 and Rank-3/Rank-1 magnitude ratios.
- Cross-band secondary peak prevalence by group.
- Decision stable under tested clustering and leave-one-group-out variants.
- Decision: `retained` as secondary descriptive spectral information.

## 5.9 DTA Results

### 5.9.1 First-Run Source-Path Comparison

- MATLAB-source candidate compiled but failed with an LLM-added `count` shadowing defect.
- Python-source candidate returned 8 hits and 8 waveforms but misclassified 26,732 known/skipped messages as unknown.

### 5.9.2 Final Reader

- 8/8 expected and actual hits.
- 8/8 expected and actual waveforms.
- Zero missing/extra/order/field/length mismatches.
- Recorded numerical errors: 0.
- 56/56 Julia tests passed.

## 5.10 WFS Results

- Two channels in expected order.
- 103,424 samples per channel.
- 206,848 voltage values compared.
- Exact full-matrix equality.
- Missing/extra channels and samples: zero.
- 26/26 tests passed.

## 5.11 R260_2 Results

S3 bounded audit:

- 3,553 Msg-1 hits.
- 3,553 Msg-173 markers.
- 3,553 paired time/channel records.
- Zero missing, extra or order mismatch.
- Activity concentrated late in elapsed time, but elapsed-time bins are not mechanical load stages.
- Nine valid exploratory crack-growth intervals after excluding the initial and invalid failure rows.

Exploratory correlations may be reported with `n=9` and explicit limitations:

- `log10(da/dN)` vs `log10(ΔK)`: `r=0.930`.
- `da/dN` vs AE count/cycle: `r=0.721`.
- `da/dN` vs AE energy/cycle: `r=0.573`.
- `da/dN` vs AE duration/cycle: `r=0.726`.

Do not claim independent prediction or crack-detection accuracy.

## 5.12 Final Rehearsal

First attempt:

- Failed during first Julia CT07 runner.
- Cause: missing declared dependencies in clean Julia project.
- Classified as environment-declaration failure.
- Protected hashes unchanged.

Second attempt:

- 61 commands, zero non-zero exits.
- Reproduced all canonical totals.
- Generated 413 morphology figures.
- Staged and canonical verification passed.
- Same-host relocation path containing spaces passed.

---

# 6. Discussion

## 6.1 Answer to RQ1: Numerical Reproducibility

> 讨论哪些工作流达到了什么级别：CT07、Legacy T01、Adaptive/Top-3 T01–T09。强调范围不同，不把Legacy T01验证泛化到九组。

## 6.2 Answer to RQ2: LLM Failure Modes and HITL Value

Suggested failure taxonomy:

1. Environment and dependency failures.
2. Fixture-identifier mismatch.
3. Physical-column/table-inference errors.
4. Mixed-cell and missing-value handling.
5. Destructive global row removal.
6. Frame-boundary and indexing semantics.
7. Library-API semantic mismatch.
8. Missing entry point/output contract.
9. Silent data loss.
10. Verification-harness failure.

Main argument:

> The greatest risks were not obvious syntax errors, but plausible transformations that changed the input schema, discarded valid records or reproduced an API name without reproducing its numerical semantics.

## 6.3 Python-versus-Julia Observations

- Python outputs were generally closer to executable CT07 results in these observed runs.
- Pandas preserved physical worksheet columns more readily than the chosen Julia table route.
- Matplotlib `twinx()` more directly reproduced shared-X behaviour than the generated Plots.jl patterns.
- Julia’s stricter handling of `Missing` exposed invalid assumptions but required more explicit schema handling.
- These observations apply to the tested tasks and single runs; they are not a universal language or model ranking.

## 6.4 Deterministic Transpiler versus LLM

- SMOP preserved syntax and source order but depended on an obsolete/incomplete runtime.
- LLMs produced more idiomatic ecosystem mappings and documentation.
- Both required execution and human intervention.
- A productive workflow combines probabilistic generation with deterministic verification.

## 6.5 Answer to RQ3: Adaptive and Top-3

- Adaptive is a reproducible numerical superset of Legacy selection on the tested archive.
- More selected windows mean greater sensitivity/coverage, not greater accuracy.
- Mechanical alignment failed to support any of the nine proposed mappings.
- Top-3 adds stable descriptive spectral information but cannot identify damage mechanisms from the present evidence.

## 6.6 Answer to RQ4: Steel-Related Applicability

- DTA is the strongest controlled steel-related workflow example.
- WFS is a single-fixture format extension with unknown material provenance.
- R260_2 is processed hit-level exploration without raw waveform or full provenance.
- Together they support bounded workflow relevance, not experimental steel crack-detection validation.

## 6.7 Reproducibility and Evidence Quality

- Numerical outputs can be checked through manifests and symmetric comparison.
- Final same-host rehearsal is stronger than archived-output integrity alone.
- Cross-machine/offline reproducibility remains unproven because external private inputs were not packaged.
- Failed rehearsal evidence improves auditability rather than weakening the project.

## 6.8 Responsible AI Use

- Report observed sessions only.
- Do not reconstruct unavailable metadata.
- Separate model generation, agent-assisted debugging, researcher decisions and automated verification.
- Researcher retains responsibility for interpretation and claims.

## 6.9 Limitations

Mandatory limitations:

- Single observed generation per CT07 configuration; no statistical model ranking.
- Some original CT07 artifacts reconstructed from historical records rather than preserved byte-exact files.
- CT07 generation dates/session IDs unavailable.
- Legacy three-language validation limited to complete T01.
- Adaptive-only events lack physical ground truth.
- Mechanical mapping unresolved for all nine groups.
- Morphology screen is deterministic, not expert blind review.
- DTA and WFS validation each use one public fixture variant.
- Public DTA/WFS fixture material provenance is not confirmed as steel.
- R260_2 grade, units, specimen mapping and licence are unconfirmed.
- Same-host, not cross-machine, clean reproducibility.
- No formal performance benchmark across Python and Julia.

---

# 7. Conclusions and Future Work

## 7.1 Conclusions

Suggested structure:

1. Restate the aim.
2. Summarise numerical closure of CT07 and Peak_Freq.
3. Summarise LLM/SMOP failure lessons.
4. Summarise bounded steel-related applicability.
5. Emphasise that auditability, not autonomous generation, is the main contribution.

Suggested concluding paragraph:

> The study demonstrates that large language models can accelerate scientific-code migration, but their outputs become trustworthy only within a workflow that preserves provenance, executes the generated code, compares it against a numerical reference and retains researcher control over interpretation. For the tested acoustic-emission cases, corrected Python and Julia implementations reproduced the relevant references within strict tolerances. The DTA, WFS and R260_2 cases extend the workflow to bounded data-format and processed-data contexts relevant to railway-steel research, without constituting experimental validation of steel crack detection.

## 7.2 Future Work

- Obtain independently confirmed specimen and trigger mappings between waveform and mechanical records.
- Conduct expert-labelled waveform review with a documented blinded protocol.
- Validate additional public DTA/WFS dialects.
- Test the packages on a second machine and prepare a redistributable data substitute where licences permit.
- Confirm R260_2 grade, units, specimen mapping, licence and authoritative failure-cycle values.
- Perform controlled Python/Julia runtime and memory benchmarks.
- Evaluate Adaptive-only events against independent physical observations.

---

# References

> 不要让AI生成未核验引用。所有参考文献必须回到原始论文、DOI、出版社或正式项目文档逐条核查。建议从`Individual Project/Background/`中的阅读笔记恢复文献清单，再对原文复核。

Reference groups to include:

1. LLM code translation and bug studies.
2. Human-in-the-loop code migration.
3. LLMs as translators/middleware between specialised tools.
4. Responsible AI in academic writing and higher education.
5. AE feature extraction, RMS and FFT methods.
6. Multi-peak or multi-variant AE spectral analysis.
7. AE machine-learning interpretation and ground-truth limitations.
8. Rail-steel AE monitoring literature.
9. MATLAB, Python, Julia and direct package documentation.
10. MistrasDTA and Mistras AE MATLAB Library repositories with pinned commits.

---

# Appendices

## Appendix A. Standardised Prompts

- CT07 generation prompts.
- DTA frozen prompt and invocation.

## Appendix B. Candidate Evidence Matrix

- Original-generation provenance.
- Fixture-normalisation changes.
- First failure.
- Repair categories.
- Final comparison result.

## Appendix C. SMOP Failure Chain

- Raw output score.
- Syntax normalisation.
- Runtime probe sequence.
- Two recovery paths.

## Appendix D. Peak_Freq Algorithm Definitions

- Legacy framing.
- Adaptive threshold equation.
- Top-3 peak-selection rule.
- Tolerance and output schema.

## Appendix E. Full T01–T09 Numerical Tables

- Per-group window and event counts.
- Maximum numerical errors.
- Legacy/Adaptive framing distinction.

## Appendix F. Scientific Morphology and Alignment Methods

- Sampling design.
- Deterministic rubric.
- Alignment criteria.
- Top-3 decision rule.

## Appendix G. DTA Experiment Evidence

- Frozen source paths.
- First-run captures.
- Candidate-to-final diffs.
- Final 56-test summary.

## Appendix H. WFS Validation

- Supported header/chunk path.
- Full-matrix comparison.
- Excluded dialects.

## Appendix I. R260_2 Data-Quality Audit

- Sheet inventory.
- Formula errors.
- S3 hit summary.
- Exploratory interval table.

## Appendix J. AI-Use Ledger and Session Availability

- Activity categories.
- Confirmed versus unavailable fields.

## Appendix K. Reproducibility Evidence

- Environment versions.
- Manifest structure.
- Failed and successful rehearsal summaries.
- Same-host relocation receipt.

---

# Recommended Figures

| Proposed Figure | Source | Suggested chapter |
|---|---|---|
| Human-in-the-loop workflow/evidence chain | `evidence-chain/workflow-evidence-chain.svg` | Methodology |
| Representative CT07 MATLAB/candidate-derived plots | Select one representative runner from CT07 results | Results |
| Legacy/Adaptive per-group selection comparison | Build from formal framing CSV | Results |
| Mapping score heatmap | `results/scientific/alignment_diagnostics/mapping_score_heatmap.png` | Results/Discussion |
| Curated morphology montage | Not yet available; select a small representative set from 413 archived figures | Results/Discussion |
| Julia/Python DTA waveform comparison | `MistrasDTAJulia/results/waveform_01_julia_vs_python.png` | Steel-related case |
| Eight DTA waveform overview | `MistrasDTAJulia/results/all_8_waveforms.png` | Appendix/Steel-related case |
| R260_2 S3 timing/P-FRQ | `R2602Analysis/results/s3_hit_timing_and_pfrq.png` | Steel-related case |
| R260_2 exploratory crack-growth plot | `R2602Analysis/results/s3_crack_growth_exploratory.png` | Steel-related case/Limitations |

---

# Recommended Tables

1. Research-case and evidence-level matrix.
2. CT07 candidate lineage and first-failure table.
3. CT07 8/8 numerical comparison.
4. SMOP raw versus two recovery paths.
5. Legacy T01 three-language comparison.
6. T01–T09 Legacy/Adaptive framing and selection counts.
7. Adaptive/Top-3 three-language aggregate comparison.
8. Mechanical alignment: 0 supported / 9 unresolved.
9. DTA source-path first-run and final validation.
10. WFS full-matrix validation.
11. R260_2 specimen inventory and S3 exploratory result.
12. Final rehearsal and reproducibility status.

---

# Claim-Safety Checklist

- [ ] Use “candidate-derived validation runner”, not “unmodified LLM output”, for the final CT07 result.
- [ ] Do not describe 8/8 as repeated-trial model reliability.
- [ ] Keep SMOP outside the eight LLM candidates.
- [ ] Restrict Legacy three-language validation to complete T01.
- [ ] State that Legacy and Adaptive have different framing denominators.
- [ ] Describe 32.16× as a selected-window count ratio only.
- [ ] Do not call Adaptive-only events confirmed physical AE damage.
- [ ] Report all nine mechanical mappings as unresolved.
- [ ] Describe morphology work as deterministic class-hidden screening, not expert review.
- [ ] Keep Top-3 secondary and descriptive.
- [ ] Describe DTA/WFS results as single-fixture format/workflow validation.
- [ ] Do not identify public DTA/WFS fixtures as rail steel without provenance.
- [ ] Call R260_2 a processed workbook “labelled R260_2”.
- [ ] Do not attach unconfirmed units to R260_2 fields.
- [ ] Report same-host clean rehearsal; do not claim cross-machine/offline reproducibility.
- [ ] Mark unavailable sessions, dates, model parameters and licences as `not_available`.

---

# Recommended Writing Order

1. Write Chapter 4, Methodology, directly from the formal case records.
2. Write Chapter 5, Results, using only machine-readable summaries and validated totals.
3. Write Chapter 6, Discussion, organised around the four research questions.
4. Write Chapter 3, Materials and Environment.
5. Write Chapter 2, Literature Review, using verified primary sources.
6. Write Chapter 1, Introduction, after the argument is stable.
7. Write Chapter 7 and the Abstract last.
8. Complete figure/table numbering, captions, references and AI-use declaration.

---

# Canonical Evidence Navigation

- Project scope: `Individual Project/README.md`
- Thesis claim/evidence map: `Individual Project/Thesis Evidence Index.md`
- Session registry: `Individual Project/Session Evidence Index.md`
- CT07/Peak_Freq package: `Individual Project/CT07-PeakFreq-Validation/README.md`
- CT07 experiment: `Individual Project/CT07-PeakFreq-Validation/results/ct07/llm-validation/experiment_record.md`
- SMOP record: `Individual Project/CT07-PeakFreq-Validation/results/ct07/smop/运行问题与解决记录.md`
- Adaptive/Top-3 record: `Individual Project/CT07-PeakFreq-Validation/results/peak-frequency/adaptive-three-language/experiment_record.md`
- Scientific interpretation: `Individual Project/CT07-PeakFreq-Validation/results/scientific/Scientific Interpretation Report.md`
- DTA experiment: `Individual Project/MistrasDTAJulia/experiments/experiment_record.md`
- WFS validation: `Individual Project/MistrasWFSJulia/results/final_validation.md`
- R260_2 analysis: `Individual Project/R2602Analysis/results/analysis_report.md`
- AI-use ledger: `Individual Project/evidence-chain/AI_USE_LEDGER.csv`

