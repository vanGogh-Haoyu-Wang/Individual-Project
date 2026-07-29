---
status: historical-milestone
milestone_date: 2026-07-29
---

# Final Validation Milestone Summary

> [!note] Historical evidence-closure milestone
> This note records the evidence-closure milestone reached on 2026-07-29. It is
> not the current project status. Current scope, validation status and
> defensible claims are maintained in
> [[Individual Project/README|Canonical Project Overview]].

## 中文执行摘要

截至 2026 年 7 月 29 日，本项目的核心数值证据已经形成闭环：CT07 的八个
candidate-derived validation runners 均通过 MATLAB oracle 比较；Legacy
Top-1 在完整 T01 上完成 MATLAB/Python/Julia 验证；Adaptive threshold 和
Top-3 在 T01–T09 的 377 个文件上完成三语言验证；DTA Julia reader 则针对
公开 Python fixture 完成受限格式验证及 provenance 封闭。九组 Peak_Freq
waveform 与 CT workbook 的时间映射仍全部 unresolved，因此不能得出载荷、
应力、屈服或裂纹阶段结论。Top-3 只保留为次要、描述性的附加频谱信息。核心
研究在论文写作前不再需要扩展新算法，剩余工作是清理历史表述、执行一次干净的
验证复演并将证据整合进论文。

## Milestone reached

The project now has bounded, auditable numerical evidence for its three
research objects:

| Research object | Evidence closure | Validated scope | Scientific boundary |
|---|---|---|---|
| CT07 | Closed | MATLAB oracle with 1,807 mechanical and 5,850 AE records; eight candidate-derived Python/Julia validation runners passed | Experiment-level mechanical and AE summaries only |
| Peak_Freq Legacy Top-1 | Closed | Complete T01 MATLAB/Python/Julia comparison; 3,098 matching rows | No validated mechanical-stage mapping |
| Peak_Freq Adaptive/Top-3 | Closed numerically | T01–T09; 377 files, 9,472,125 complete windows, 522,216 selected events and 1,566,634 Top-3 rows | Adaptive-only events are not damage truth; Top-3 is a secondary descriptive spectral extension |
| DTA Julia reader | Closed for the tested fixture | Public Python fixture; 8 hits, 8 waveforms and 56/56 Julia tests | Format/workflow-level applicability for one tested DTA variant |

SMOP remains a separate deterministic-transpiler baseline. Its two audited
recovery paths passed the CT07 MATLAB-oracle comparison, but SMOP is not
included in the eight LLM candidates.

## Auditability and evidence lineage

### CT07

Each of the eight LLM cases is separated into three evidence levels:

1. `original_generation`;
2. `fixture_normalized_probe`;
3. `candidate_derived_validation_runner`.

Prompt, response, source, normalized probe and final-runner hashes are recorded
in the candidate manifest. Artifacts recovered from historical records are
labelled `reconstructed_from_record`; they are not presented as surviving
byte-exact raw files. The final runners' numerical success is reported
separately from the quality and first-run behaviour of the original
generations.

### Peak_Freq

Legacy and Adaptive framing are kept distinct:

- Legacy T01–T09 MATLAB context: 11,366,550 logical frames and 16,240 selected
  windows;
- Legacy three-language validation: complete T01 only, with 3,098 rows;
- Adaptive/Top-3 three-language validation: T01–T09, with 9,472,125 complete
  windows, 522,216 selected events and 1,566,634 Top-3 rows.

The retained waveform sample contains 413 events. Recalculation reproduces the
stored RMS and FFT results with zero recorded mismatches. The review is a
**deterministic class-hidden morphology screen**: it is neither expert blinded
assessment nor damage ground truth.

All nine waveform-to-CT mappings are `unresolved` (`0` supported, `9`
unresolved). No aligned mechanical-stage result is therefore released. CT07
and Peak_Freq remain separate analyses connected only by a future mapping if
independent evidence becomes available.

Top-3 satisfied the **pre-specified follow-on decision rule** and is retained
only as secondary descriptive spectral information. This does not establish
damage classes, crack mechanisms or improved detection accuracy.

### DTA

The DTA evidence package freezes the recoverable prompt and invocation,
isolated MATLAB-source and Python-source sessions, raw responses, first-run
captures, candidate-to-final diffs, final reader, tests, comparison results,
reports and waveform figures under one SHA-256 manifest. The final Julia
reader was validated against the public Python fixture only. The MATLAB-source
candidate remains an informative failed translation path rather than a second
numerical oracle.

## Thesis-ready claims

- An auditable human-in-the-loop workflow identified translation failures and
  numerically validated corrected MATLAB-to-Python/Julia implementations.
- Eight candidate-derived CT07 runners match the MATLAB oracle for the tested
  workbook and sheet.
- Legacy Top-1 matches across MATLAB, Python and Julia for complete T01.
- Adaptive threshold and Top-3 match across MATLAB, Python and Julia for the
  tested T01–T09 waveform archive.
- A Julia reader supports the tested public AEWin/Mistras DTA variant and
  matches its Python reference fixture.
- The DTA case demonstrates bounded **format/workflow-level applicability** to
  an AE workflow relevant to railway-steel research.

## Claims prohibited by the evidence

- No experimental validation of crack detection in steel.
- No damage-classification or crack-type accuracy claim.
- No validated CT07-to-T01–T09 specimen or mechanical-time mapping.
- No load, stress, yield or crack-growth stage conclusion from Peak_Freq.
- No claim that adaptive-only selections are confirmed physical damage events.
- No claim of complete DTA or WFS compatibility.
- No claim that one LLM family is generally superior based on these single
  observed generations.

## Remaining before dissertation drafting

At this milestone, the remaining work is evidence presentation rather than
algorithm development:

1. finish marking stale notes and presentation statements as historical;
2. run one clean validation rehearsal, or limit the reproducibility claim to
   integrity-verified archived results if a full rehearsal is impractical;
3. integrate the validated methods, failure evidence, numerical comparisons,
   scientific limitations and steel-applicability boundary into the
   dissertation.

WFS and R260_2 remain optional appendix cases. They do not block the core
dissertation argument.

## Canonical evidence

- [[Individual Project/README|Canonical Project Overview]]
- [CT07–Peak_Freq validation package](../CT07-PeakFreq-Validation/README.md)
- [CT07 candidate evidence manifest](../CT07-PeakFreq-Validation/results/ct07/llm-validation/evidence/candidate_manifest.json)
- [SMOP comparison summary](../CT07-PeakFreq-Validation/results/ct07/smop/smop_comparison_summary.json)
- [Legacy T01 comparison](../CT07-PeakFreq-Validation/results/peak-frequency/legacy-t01-three-language/legacy-regression-current/comparison_summary.json)
- [Adaptive/Top-3 aggregate comparison](../CT07-PeakFreq-Validation/results/peak-frequency/adaptive-three-language/comparison_summary.json)
- [Scientific interpretation report](<../CT07-PeakFreq-Validation/results/scientific/Scientific Interpretation Report.md>)
- [DTA evidence manifest](../MistrasDTAJulia/MANIFEST.sha256)
- [DTA final validation](../MistrasDTAJulia/results/final_validation.md)

