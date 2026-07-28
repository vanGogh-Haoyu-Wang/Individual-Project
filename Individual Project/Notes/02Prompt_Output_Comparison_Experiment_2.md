# Prompt Output Comparison: Experiment #2 (MATLAB to Python)

> [!warning] Pre-oracle experiment record
> This report evaluates original-generation evidence available at that stage.
> It does not replace the final MATLAB-oracle validation or support a general
> ranking of model families. See [[Individual Project/README|Canonical Project Overview]].

## 1. Experiment Metadata and Scope

This report compares four observed MATLAB-to-Python translation runs for the same Acoustic Emission (AE) plotting task. It follows the horizontal-comparison structure used in [[01Prompt_Output_Comparison_Experiment_1]], while adding separate comparisons of the debugging process and the recorded evaluation evidence.

| ID | Model and setting | Interface | Primary 02 Test record | Submitted Python answer |
|---|---|---|---|---|
| **G** | Gemini 3.1 Pro High | Antigravity CLI | `Tools history/Antigravity Cli/02Test Record from Gemini 3.1 Pro (Python).md` | `Tools history/Antigravity Cli/Test2 by Gemini 3.1pro high.py` |
| **S** | Claude Sonnet 4.6 High | Claude Code Desktop | `Tools history/Claude code Desktop Sonnet 4.6/02Test Record from Sonnet 4.6 high (Python).md` | Original answer recorded in the 02 Test record; the working `.py` file was subsequently repaired for testing |
| **D** | DeepSeek v4 Pro XHigh | Claude Code CLI via ccswitch | `Tools history/Claude code cli ccswitch to Deepseek-v4-pro/02Test Record from Deepseek v4 pro xhigh.md` | `Tools history/Claude code cli ccswitch to Deepseek-v4-pro/Test 2 by DSv4pxh ae_analysis.py` |
| **C** | GPT-5.5 XHigh | Codex CLI | `Tools history/Codex Cli/02Test Record from gpt-5.5 xhigh from matlab to python.md` | `Tools history/Codex Cli/Test 2 by gpt-5.5 max.py` |

**Assessment date:** 19 June 2026

**Target stack:** Python, pandas, NumPy where used, openpyxl, and Matplotlib

**Actual fixture:** `Commercial Tensile Tests.xlsx`, worksheet `CT07`
**Excluded material:** the 01 Test, the 03 Test, and SMOP are outside this comparison.

### 1.1 Unit of comparison

The unit assessed here is one recorded **model + interface + prompt + execution environment** run. The observations do not establish the general capability of a model family. There was one recorded answer per configuration, the interfaces and dependency environments differed, and no repeated-trial variance was measured.

### 1.2 Prompt and fixture comparability

The four prompts contained the same column selections and five plotting operations, but their input identifiers were not identical:

| Runs | Workbook in prompt | Worksheet in prompt | Match to tested fixture? |
|---|---|---|---|
| Gemini, Sonnet, DeepSeek | `Commercial Tensile Tests` | `CT07` | Yes, after using the `.xlsx` filename present in each folder |
| GPT-5.5 | `Tensile-processed.xlsx` | `CT-07` | No; the tested fixture was `Commercial Tensile Tests.xlsx`, sheet `CT07` |

The GPT-5.5 script therefore required two input-identifier changes before it could be tested against the supplied fixture. Those changes did not alter its data-cleaning or plotting logic, but they mean its result is not an unchanged-fixture run. Conversely, the other three scripts had the correct fixture identifiers but required code-level data-ingestion repairs.

### 1.3 Worksheet structure relevant to all four runs

The worksheet is not one uniform rectangular numeric table. It combines two domains:

- 1,807 finite paired mechanical observations in the relevant time, strain, and stress columns;
- 5,850 finite paired AE observations in the relevant time, RMS, cumulative RMS, energy, and cumulative-energy columns;
- headings, units, blanks, and trailing missing cells in different physical rows for the two domains;
- a maximum finite stress of approximately `505.214799 MPa`.

This layout is the central execution challenge. `header=None` preserves physical row and column positions, but it does not reproduce MATLAB `xlsread`'s numeric-matrix behaviour. Likewise, `header=0` consumes only the first worksheet row and does not remove the later mechanical labels and units.

### 1.4 Evidence rules

The following evidence hierarchy is used throughout the report:

1. strict execution of the submitted answer against the available fixture;
2. captured exit status, traceback, workbook inspection, and numerical checks;
3. automated tests and artifact validation;
4. visual inspection of Python figures.

Environment-provisioning failures are recorded separately from translation defects. Results from repaired scripts demonstrate that a proposed plotting design can work after repair; they do not prove that the submitted answer ran successfully. Manually saved figures are also distinguished from script-generated artifacts.

No MATLAB-rendered reference figures or reference arrays were supplied. Consequently, this report can assess code mapping, execution, plotted data assignments, axes, labels, limits, and internal visual consistency, but it cannot claim pixel-level MATLAB equivalence.

No weighted aggregate score or overall model ranking is used. Such a score would require subjective weights and would conceal the prompt mismatch described above.

---

## 2. Code Quality Comparison

### 2.1 Observable structural features in the submitted answers

| Feature | Gemini 3.1 Pro | Sonnet 4.6 High | DeepSeek v4 Pro | GPT-5.5 |
|---|---|---|---|---|
| Correct 1-based to 0-based mapping for all eight columns | **Yes** | **Yes** | **Yes** | **Yes** |
| Numeric coercion in submitted answer | No | No | No | **Yes:** `apply(pd.to_numeric, errors="coerce")` |
| Missing-data-aware stress maximum | No: `Series.max()` after unclean loading | No: `Series.max()` after unclean loading | No: NumPy `.max()` can return `NaN` | **Yes:** `np.nanmax(stress)` |
| Minimum-column validation | No | No | No | **Yes:** rejects fewer than 14 columns |
| Defined functions | 1 (`main`) | 3 plotting/style helpers | 0 | 5, including loader and `main` |
| Entry-point guard | Yes | No; work occurs at import time | No; work occurs at import time | Yes |
| Shared helper for all four dual-axis panels | No | Partial: shared axis styling, repeated orchestration | No | **Yes:** parameterised line/scatter helper |
| Explicit exception handling | `FileNotFoundError` only | No | No | No catch; loader raises normal I/O errors and an explicit shape error |
| Type hints/docstrings | Minimal | Extensive | Minimal | Extensive |
| Automatic image export in submitted answer | No | No | No | No |

Function count is reported only as structural evidence; more functions are not automatically better. The relevant distinction is whether repeated behaviour is centralised and whether importing the module triggers I/O and plotting.

### 2.2 Criterion-level comparison

| Criterion | Gemini 3.1 Pro | Sonnet 4.6 High | DeepSeek v4 Pro | GPT-5.5 |
|---|---|---|---|---|
| **Indexing correctness** | All eight `.iloc` positions are correct. | All eight `.iloc` positions are correct. | All eight NumPy positions are correct. | All eight `.iloc` positions are correct. |
| **Workbook ingestion** | `header=None` retains mixed text and numbers; Figure 1 fails. | `header=0` leaves two mechanical metadata rows; Figure 1 fails. | `header=None` plus `.values` creates mixed object arrays; Figure 1 fails, and trailing `NaN` would later invalidate `stress.max()`. | Coerces all cells to numeric and preserves nonnumeric cells as `NaN`; suitable for this worksheet after input identifiers are adapted. |
| **Matplotlib mapping** | Correct use of `subplots`, four `twinx()` axes, line/scatter distinction, limits, labels, and grids. | Correct OO API and `twinx()`; helper functions also colour spines, labels, and ticks. Adds `alpha=0.7` to Figure 4 beyond the source. | Correct OO API, `twinx()`, signals, limits, and Figure 4 scatter. Minor grids may not appear because minor ticks are not enabled. | Correct OO API, one parameterised dual-axis helper, source line/scatter distinction, limits, and minor grids. Axis labels are not colour-coded, which was not an explicit prompt requirement. |
| **Modularity** | One `main()` contains loading and five mostly repeated plotting blocks. | Reuses grid and axis-style helpers, but repeats the Figure 2-5 construction and executes at import. | Entirely procedural module-level code with four repeated dual-axis blocks. | Separates loading, grid styling, the single-axis panel, dual-axis panels, and orchestration. |
| **Validation and robustness** | Handles only a missing workbook; no sheet, shape, numeric-count, or finite-value checks. | No input validation in the submitted answer. | No input validation; conversion to NumPy removes pandas' labelled context without resolving mixed types. | Validates width and uses numeric coercion and `np.nanmax`; still does not validate expected finite counts, time ranges, or an empty/all-`NaN` stress signal. |
| **Reusability** | Relative hard-coded input, but protected by an entry-point guard. | Original answer uses a configurable `Path` constant, but import has side effects and helpers do not cover full orchestration. | Relative hard-coded input and import-time side effects. | Loader accepts path and sheet arguments and common plotting logic is parameterised; top-level constants remain relative. |
| **Reproducibility** | Lists packages informally; no pinned environment. | Lists packages informally; no pinned environment in the answer. | Provides `pip install` and a usage command; no pinned environment. | Imports are explicit, but the answer contains no environment file or pinned versions. A pinned local environment was created during debugging. |
| **Submitted-answer result on the available fixture** | Exit 1 during Figure 1; no completed five-figure run. | Exit 1 during Figure 1; no completed five-figure run. | Exit 1 during Figure 1; no completed five-figure run. | Cannot run unchanged because the prompt-specified identifiers do not exist; after changing only those two constants, exit 0 and five figure objects are created. |

### 2.3 Common code-level result

All four answers correctly performed the explicit MATLAB-to-Python column-index conversion and chose the requested native Python libraries. All four also used Matplotlib's object-oriented axes interface and `twinx()` rather than emulating MATLAB `yyaxis`.

The decisive difference is data ingestion. Gemini, Sonnet, and DeepSeek assumed that choosing a header mode was enough to obtain plot-ready numeric series. GPT-5.5 performed numeric coercion before extraction, retained the worksheet's physical layout, and used a missing-data-aware maximum. This is why its existing logic survived the actual worksheet after the external identifiers were adapted.

The source MATLAB script creates interactive figures and does not save files. Therefore, the absence of `savefig()` in all four submitted answers is an output-contract limitation for automated evaluation, not by itself a translation error.

The Figure 2 title `T09 Commercial Normalised RMS Profile` is inconsistent with the `CT07` data, but it is present in the supplied MATLAB source. Preserving it is literal translation behaviour and is not counted as a model defect. Any repaired output that changes it to `CT07` should be labelled as a deliberate provenance correction.

---

## 3. Debug Process Comparison

### 3.1 Execution timeline

| Stage | Gemini 3.1 Pro | Sonnet 4.6 High | DeepSeek v4 Pro | GPT-5.5 |
|---|---|---|---|---|
| **Initial environment blocker** | Matplotlib missing. | Matplotlib missing. | Matplotlib missing; first installation also blocked by sandbox networking; Matplotlib cache path was unwritable. | NumPy and the remaining scientific stack missing from the selected interpreters; first package installation was blocked by networking. |
| **Environment resolution** | Matplotlib supplied through an additional package path. | Matplotlib 3.11.0 and dependencies installed under the test output directory and exposed through `PYTHONPATH`. | Matplotlib 3.11.0 installed in a temporary target; `MPLCONFIGDIR` and `MPLBACKEND=Agg` set. | Project-local `.venv` created with pinned NumPy, pandas, Matplotlib, and openpyxl versions; local Matplotlib cache used. |
| **Strict code-level result** | Exit 1 at the first `plot`: mixed strings and floats. | Exit 1 at the first `plot`: mixed strings and numbers. | Exit 1 at the first `plot`: mixed strings and floats. | After fixture-identifier adaptation, exit 0 in both headless and interactive checks. |
| **Root cause identified** | `header=None` does not remove headings/units or reconcile independent row domains. | `header=0` removes only one row; two mechanical metadata rows remain. | `header=None` plus NumPy conversion retains metadata; unequal row domains also make an unguarded NumPy maximum unsafe. | The generated ingestion logic already handles mixed data; the blocking mismatch was the workbook/sheet identifiers inherited from its different prompt. |
| **Repair scope used for demonstrable figures** | Separate repaired script: numeric coercion per signal, pairwise masks, arguments, headless mode, and export. | Working script updated: numeric coercion for the three mechanical columns, deterministic export, and headless handling. | Separate repaired script: skips upper rows, coerces fields, separates domains, adds CLI, headless mode, export, and changes the Figure 2 title. | Only the workbook and sheet constants were adapted; PNGs were then saved manually from the interactive windows. |
| **Finite records evidenced** | Mechanical 1,807; AE 5,850. | Mechanical 1,807; AE data retained from the 5,850-row post-header frame; the repair leaves AE columns untouched. | Mechanical 1,807; AE 5,848 in the repaired run. | Arrays have 5,851 physical positions; finite mechanical values 1,807 and finite AE values 5,850. |
| **Original-answer preservation** | Original hash checked before and after the repaired run. | The record preserves the original response and discloses later edits, but the working `.py` file is the repaired version. | Original answer retained separately from `ae_analysis_fixed.py`. | The record discloses the two constant changes; the current `.py` reflects those adapted constants. |

Environment setup is not ranked by the number of obstacles because the interfaces did not start from the same runtime or permissions. The relevant comparison is whether each record separated environment failures from code failures and whether the final evidence can be attributed to the correct program.

### 3.2 Repair fidelity and data preservation

The Gemini and Sonnet repairs retain the two physical domains without globally deleting rows that contain valid AE data. The GPT-5.5 loader achieves the same effect through whole-frame numeric coercion: nonnumeric mechanical cells become `NaN`, while the 5,850 finite AE values remain available.

The DeepSeek repair reports 5,848 AE rows because it first skips upper worksheet rows and then cleans the AE domain. Compared with the independently observed 5,850 finite AE values, this procedure discards two valid early AE observations. This is an inference supported by the cross-record finite-count evidence, and it means that the DeepSeek repaired data path is not numerically equivalent to the better-preserving repairs even though its five figures are visually coherent.

### 3.3 Verification mechanisms

| Verification mechanism | Gemini 3.1 Pro record | Sonnet 4.6 High record | DeepSeek v4 Pro record | GPT-5.5 record |
|---|---:|---:|---:|---:|
| Captured original traceback | Yes | Yes | Yes | Not applicable after identifier adaptation; earlier dependency and identifier failures documented |
| Separate or explicitly identified repair | Yes | Yes | Yes | Yes: two constants identified |
| Subprocess exit-status assertion | Yes | Yes | Yes | Execution status recorded, but no retained automated integration test |
| Output generated in an empty temporary directory | No | No | **Yes** in the integration test | No |
| Exact expected filename set | Yes | Yes | Count in temporary test; named files checked in formal run | No automatic export contract |
| Regeneration timestamp check | **Yes** | No | No | No |
| Original-script hash before and after test | **Yes** | No | Original kept separate, but no hash assertion | No |
| File-size threshold | Yes, `>20 KB` | Yes, `>10 KB` | Yes, `>10 KB` | Sizes/dimensions reported for manually saved files |
| Image decode check | Yes | Yes in an additional Pillow check | Yes in formal verification | Manually saved PNGs inspected |
| Resolution check | Yes | Dimensions reported | Dimensions reported | All five reported as `640 × 480` |
| Non-blank/tonal-content check | **Yes** | No | Visual inspection only | Visual inspection only |
| Figure/axes object-count check | No | No | No | **Yes:** five figures with axes counts `[1, 2, 2, 2, 2]` |

The Gemini verification has the broadest recorded artifact-provenance checks: it proves that the original file remained unchanged, that five files were freshly regenerated, and that the images decode, meet minimum resolution, and contain tonal variation. The DeepSeek integration test offers the clearest protection against stale output because it uses a temporary output directory, although its assertions cover only exit status, file count, and size. The Sonnet test checks exact names, exit status, warnings, and sizes, with a separate decode check, but does not assert freshness or original-file identity. The GPT-5.5 record verifies the in-memory figure topology and actual execution, but its PNGs were saved manually and are not evidence of an automatic export path.

These statements compare the recorded checks, not the inherent debugging ability of the four model families.

---

## 4. Evaluation Quality Comparison

### 4.1 Evidence coverage in the four records

| Evaluation property | Gemini 3.1 Pro | Sonnet 4.6 High | DeepSeek v4 Pro | GPT-5.5 |
|---|---|---|---|---|
| Separates environment issues from code defects | Yes | Yes | Yes | Yes |
| States whether the submitted answer ran unchanged | Yes: it did not | Yes: it did not | Yes: it did not | Yes: identifiers were changed before the logic was tested |
| Separates original and repaired image provenance | Explicitly | Explicitly | Explicitly | Explicitly distinguishes manually saved images |
| Verifies all eight column offsets | Yes | Yes | Yes, with a mapping table | Yes |
| Reports worksheet shape or finite counts | Shape, both domain counts, and max stress | DataFrame shape and affected columns; domain structure described | Both repaired-domain counts | Physical lengths, finite counts, and figure/axes counts |
| Evaluates output images | Five repaired images, with automated and visual checks | Five repaired images, with automated and visual checks | Five repaired images, with automated and visual checks | Five manually saved images, visually inspected |
| States absence of MATLAB reference evidence | Yes | Evaluation is limited to repaired Python output | Provenance limitation stated | Explicitly rejects pixel-equivalence claims |
| Identifies the inherited `T09` title correctly | Yes, source issue | Yes, source issue | Yes; repaired title identified as a deliberate change | Yes, source issue |

### 4.2 Strengths and limits of the recorded evaluations

**Gemini record.** Its evaluation is strongly tied to strict-run evidence and repeatedly prevents the repaired PNGs from being mistaken for original-answer output. It also records the most extensive artifact integrity checks. Its central conclusion—correct index/plot mapping but blocking ingestion—is supported by the traceback and workbook inspection.

**Sonnet record.** Its evaluation identifies precisely why `header=0` is insufficient and why global row deletion would damage the AE domain. The repair is narrowly targeted to the three mechanical series. The evaluation is transparent that the working Python file was changed, but preservation evidence is weaker than Gemini's hash-based boundary.

**DeepSeek record.** Its evaluation documents the full chain from dependency and sandbox issues to the mixed-data failure and the second-order `NaN` maximum risk. The temporary-directory integration test is good isolation practice. However, the repaired 5,848-row AE result is lower than the independently established 5,850 finite observations, and the evaluation does not treat that two-point loss as a repair-fidelity limitation.

**GPT-5.5 record.** Its evaluation provides the clearest direct numerical account of physical array length versus finite counts and verifies the five-figure axes structure. It correctly limits the PNG claim to manual saving. Its main comparability constraint is external to the generated logic: the prompt used different input identifiers, so the successful run followed an identifier adaptation rather than an unchanged submission.

### 4.3 Why evaluation quality is a separate dimension

A detailed evaluation can document a weak submitted answer accurately, while a robust submitted answer may have a less extensive artifact-testing record. For example, the Gemini answer fails end to end but has the broadest file-provenance verification; the GPT-5.5 plotting logic runs after identifier adaptation but has no automatic PNG export test. It would therefore be incorrect to use the quality of the later evaluation record as a substitute for the quality of the original translation.

---

## 5. Shared Patterns and Distinctive Differences

### 5.1 Shared patterns

All four observed answers:

1. convert the eight MATLAB column positions correctly;
2. replace `xlsread` with `pandas.read_excel`;
3. use Matplotlib's object-oriented interface and four `twinx()` calls or their parameterised equivalent;
4. reproduce the requested five panel definitions, including the line/scatter distinction;
5. preserve the source's `T09` Figure 2 title;
6. depend on fixed physical column positions;
7. provide no dependency lock file or fully reproducible environment in the submitted answer;
8. end with interactive display rather than automatic file export.

### 5.2 Distinctive differences

| Dimension | Observed difference |
|---|---|
| **Data robustness** | GPT-5.5 is the only submitted answer with numeric coercion before plotting and a missing-data-aware stress maximum. |
| **Full dual-axis reuse** | GPT-5.5 uses one parameterised helper for all four dual-axis panels; Sonnet centralises styling only; Gemini and DeepSeek repeat the blocks. |
| **Import safety** | Gemini and GPT-5.5 use entry-point guards; Sonnet and DeepSeek perform workbook I/O and plotting on import. |
| **Plot styling detail** | Sonnet explicitly colours spines, ticks, and labels; Gemini colours labels/ticks; DeepSeek and GPT-5.5 retain the requested series colours without full axis colour styling. |
| **Minor-grid implementation** | Gemini, Sonnet, and GPT-5.5 enable minor ticks before requesting minor grids. DeepSeek requests minor grids without enabling minor ticks. |
| **Strict original execution** | Gemini, Sonnet, and DeepSeek reach the actual workbook but fail during Figure 1. GPT-5.5 cannot locate the actual fixture unchanged, but completes after two identifier substitutions. |
| **Repair fidelity** | Gemini, Sonnet, and GPT-5.5 evidence 5,850 finite AE observations; the DeepSeek repair retains 5,848. |
| **Artifact evidence** | Gemini has the widest freshness/integrity checks; DeepSeek has the cleanest temporary-output isolation; Sonnet has deterministic script export after repair; GPT-5.5 has manual PNGs plus in-memory axes verification. |

---

## 6. Dimension-Specific Conclusions

| Dimension | Evidence-based conclusion |
|---|---|
| **Column-index translation** | No observed difference: all four answers map every requested column correctly. |
| **Submitted data-ingestion design** | GPT-5.5 provides the only design that handles the worksheet's mixed metadata and missing cells without a code-level ingestion repair. This conclusion is conditional on adapting its mismatched input identifiers. |
| **Unchanged execution against the available fixture** | None of the four submissions passes completely unchanged: three fail on mixed data, while GPT-5.5 points to a workbook and sheet that are absent from the fixture. |
| **Plotting intent** | All four provide technically recognisable Matplotlib equivalents. Repaired runs demonstrate that each mapping can generate the five intended Python figures when supplied with clean numeric series. This does not establish exact MATLAB visual equivalence. |
| **Modularity and reuse** | GPT-5.5 centralises the complete repeated dual-axis workflow. Sonnet partially centralises styling. Gemini and DeepSeek retain repeated figure construction. |
| **Debug repair scope** | GPT-5.5 needs only fixture-identifier adaptation because its submitted loader is already tolerant. Sonnet makes the narrowest code-level data repair among the three ingestion failures. Gemini and DeepSeek introduce separate, broader execution wrappers. |
| **Debug evidence rigor** | Gemini records the widest artifact freshness and original-preservation checks. DeepSeek uniquely tests in a temporary output directory. These are different strengths rather than a basis for a combined rank. |
| **Evaluation transparency** | All four records explicitly distinguish environment problems, original code, repaired code, and image provenance. The principal remaining inconsistency is that DeepSeek's repaired two-point AE loss is not highlighted in its own evaluation. |

There is no overall winner declared. A composite result would depend on whether the evaluator values unchanged fixture execution, tolerance of prompt/fixture mismatch, source-code modularity, minimal repair, or artifact provenance most heavily. Those weights were not specified before the experiment.

---

## 7. Recommendations for Future Experiments

1. **Freeze one canonical prompt.** Use identical workbook and worksheet identifiers in every run and store a hash of the prompt text.
2. **Freeze one fixture.** Record the workbook hash, sheet names, dimensions, expected finite counts (`1,807` mechanical and `5,850` AE), and finite maximum stress before testing.
3. **Preserve every original answer immutably.** Hash it before execution and write all repairs to separate files.
4. **Use one controlled environment.** Run all submissions with the same Python and pinned package versions, backend, cache location, working directory, and timeout.
5. **Test without editing input constants.** Supply fixture paths through a neutral wrapper or copy the fixture to each prompt-specified name; report wrapper intervention explicitly.
6. **Standardise the strict-run harness.** Capture exit code, traceback, warnings, figure count, axes count, selected column positions, finite counts, maxima, and plotted artist types.
7. **Prevent stale-artifact credit.** Generate outputs in a new temporary directory and require exact names, fresh timestamps, successful decoding, minimum resolution, and non-blank content.
8. **Add MATLAB numerical references.** Export the eight source arrays and axes limits from MATLAB and compare values directly. Use image comparison only as a secondary styling check.
9. **Separate literal fidelity from scientific correction.** Score preservation of the source `T09` title separately from an optional correction to `T07` or `CT07`.
10. **Repeat each configuration.** Multiple independent runs are required before making claims about model-level reliability.
11. **Pre-register any scoring rubric.** If a future report requires an overall score, define criterion weights and pass thresholds before viewing the outputs.

## 8. Final Summary

The four observed runs share correct index conversion, appropriate Python libraries, and a valid high-level `twinx()` plotting strategy. Their main difference is not the visible MATLAB syntax translation but whether the generated data loader understands the actual worksheet's mixed metadata and unequal signal domains.

Gemini 3.1 Pro, Sonnet 4.6 High, and DeepSeek v4 Pro all fail at Figure 1 because their submitted loaders pass mixed text and numeric values to Matplotlib. GPT-5.5 includes numeric coercion, column-width validation, missing-data-aware limits, and a reusable plotting function; after its prompt-derived workbook and sheet identifiers are adapted to the available fixture, the existing analysis logic completes and creates five figures.

The debugging and evaluation records add a second, independent comparison. Gemini provides the broadest recorded artifact freshness and original-file checks; Sonnet applies a focused mechanical-column repair; DeepSeek uses a clean temporary-output integration test but its repair retains two fewer AE observations; GPT-5.5 verifies finite counts and in-memory figure topology but relies on manual PNG saving. These differences are reported by dimension rather than collapsed into a subjective overall ranking.
