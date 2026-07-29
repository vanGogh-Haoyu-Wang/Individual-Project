# Prompt Output Comparison: Experiment #3 (MATLAB to Julia)

> [!warning] Pre-oracle original-generation assessment
> This historical report evaluates the original-generation evidence available
> at that stage. It does not replace the final candidate-derived runner
> validation against the MATLAB oracle or support a general ranking of model
> families or target languages. See
> [[Individual Project/README|Canonical Project Overview]].

## 1. Scope and comparison method

This comparison covers the four non-SMOP `03 Test` folders:

| Platform folder | Model recorded in the experiment | Primary translation record |
|---|---|---|
| `Antigravity Cli` | Gemini 3.1 Pro (high) | `03Test Record from Gemini 3.1 Pro (Julia).md` |
| `Claude code cli ccswitch to Deepseek-v4-pro` | DeepSeek V4 Pro (high) | `03Test Record from Deepseek v4 pro high.md` |
| `Claude code Desktop Sonnet 4.6` | Claude Sonnet 4.6 (high) | `03Test Record from Sonnet 4.6 high (Julia).md` |
| `Codex Cli` | GPT-5.5 (xhigh) | `03Test Record from gpt-5.5 xhigh from matlab to julia.md` |

The assessment separates three evidence layers that should not be conflated:

1. **Original translation**: the Julia code initially returned by the model.
2. **Debugged execution**: later repairs, harnesses, environment setup, and generated figures.
3. **Evaluation record**: the later written assessment of the original and repaired paths.

The review used static inspection of the four original translations, the recorded commands and failures, the repair or harness code that remains on disk, PNG metadata, and a visual spot-check of the generated plots. No trusted MATLAB array dump or MATLAB-rendered golden images were supplied, so exact numerical and pixel-level equivalence cannot be claimed.

## 2. Comparability and evidence limits

### 2.1 What is genuinely controlled

The four supplied `Commercial Tensile Tests.xlsx` files are byte-identical. Each has SHA-256:

```text
89033ea6af74f0b99cfe44a1dcda4e59e4fea709d1f4e4c4acba3745edc33b2d
```

The successful test environments also report the same core package versions: Julia 1.12.6, XLSX.jl 0.11.10, DataFrames.jl 1.8.2, Plots.jl 1.41.6, and GR 0.73.26.

### 2.2 What is not fully controlled

| Comparability issue | Evidence and consequence |
|---|---|
| Prompt inconsistency | The Gemini and Sonnet records say `Tensile-processed.xlsx` / `CT-07` in the requirements but show `Commercial Tensile Tests` / `CT07` in the embedded MATLAB line. Their choice of the requirement-era names is therefore one defensible resolution of an internally inconsistent prompt. The DeepSeek and GPT records consistently use `Tensile-processed.xlsx` / `CT-07`; the later fixture name mismatch was not knowable from those prompts. |
| Different post-generation interventions | Gemini received a separate repaired script; Sonnet's workspace script was edited in place; DeepSeek and GPT used external harnesses that bypassed the failed loaders. “Five PNGs exist” therefore does not mean the same thing across platforms. |
| Different verification depth | Gemini has 31 structural PNG assertions; Sonnet has an end-to-end file-count test and a source-text title check; DeepSeek and GPT mainly preserve diagnostic and visual-verification records. |
| Different artifact sizes | Gemini's repaired output is 1200 × 800; the other three sets are 600 × 400. Resolution is an execution choice, not evidence of translation correctness. |
| Missing efficiency data | Wall-clock time, token use, number of tool calls, and human interventions were not recorded under a common protocol. Debugging speed or cost cannot be ranked objectively. |
| Evaluation authorship | The records do not establish that the original translation model independently authored the later `Debug` and `Evaluation` appendices. Those sections can be compared as evaluation artifacts, but not safely treated as direct measures of model self-critique. |

## 3. Executive comparison

| Model | Unchanged code on the supplied workbook | Decisive original defect | What the saved figures actually prove | Evidence-supported characterization |
|---|---|---|---|---|
| **Gemini 3.1 Pro** | Exit 0 but performs no analysis because the only function call is commented out; explicit calls then fail on sheet lookup and `Float64(::Missing)` | No active entry point; whole-column `Float64` conversion cannot handle mixed headers, missing cells, or the two row domains | A separate `Test3_fixed.jl` can process 1,807 mechanical and 5,850 AE rows and render five figures | Good physical-column intent and useful plotting structure, but an end-to-end failure in the original response |
| **DeepSeek V4 Pro** | Fails in `load_tensile_data` after the actual file/sheet is supplied | `readtable` infers nine columns; additionally, the code selects eight columns and then incorrectly reuses the original positions on the reduced DataFrame | The five plotting functions render when an external harness manually supplies corrected arrays | Strong modular surface structure, but the most serious independent indexing/data-domain defects in the loader |
| **Sonnet 4.6** | Initial version fails first on the prompted filename and then on the nine-column `readtable` result | Incorrect claim that default `XLSX.readtable` is equivalent to MATLAB `xlsread` for this worksheet | The edited workspace script runs end to end after explicit range, path, sheet, export, and title changes | Strong documentation and function boundaries; blocking initial loader assumption; successful repaired path is not the unchanged answer |
| **GPT-5.5** | Original direct run fails on the prompted filename; a constants-only copy then fails because `readtable` returns nine columns | Clean abstractions are built on a table-inference model that destroys physical Excel positions | The plotting layer renders after a harness bypasses `load_ct07`, `extract_signals`, and `main` | The most concise and balanced original code organization, but still an end-to-end failure with only component-level plot success |

There is no defensible single overall winner: none of the four unchanged translations completed against the supplied workbook, and the subsequent repair protocols were not equivalent.

## 4. Original code quality comparison

### 4.1 Side-by-side matrix

| Criterion | Gemini 3.1 Pro | DeepSeek V4 Pro | Sonnet 4.6 | GPT-5.5 |
|---|---|---|---|---|
| **MATLAB-to-Julia index-base knowledge** | Correct: retains 1, 3, 4, 5, 9, 10, 12, 14 | Correct index-base statement | Correct index-base statement | Correct index-base statement |
| **Physical Excel column preservation** | Best initial choice: raw worksheet matrix preserves physical positions | Lost through `readtable` inference | Lost through `readtable` inference | Lost through `readtable` inference |
| **Row/type robustness** | Weak: `Float64.(whole_column)` fails on `missing` and metadata | Weak: one `dropmissing` conflates two sampling domains | Partial: handles `missing`/`nothing`, but never receives the intended physical columns | Partial: handles `missing` through `coalesce`, but not text and not lost columns |
| **Independent loader defect** | No active call and no mixed-row filtering | Selects eight columns, then reindexes them as if 14 columns still existed; also discards valid AE-only rows | Automatic-table assumption is blocking | Automatic-table assumption is blocking |
| **Function decomposition** | One main function with a nested shared plotting helper | Loader, twin-axis helper, five figure functions, and guarded `main` | Loader, shared base plot, five typed figure functions, and `main` | Loader, conversion helper, extraction, two plotting abstractions, `make_plots`, and guarded `main` |
| **Entry-point design** | Incomplete: invocation is commented out; CLI arguments are ignored | Standard `PROGRAM_FILE` guard | Initial response calls `main()` unconditionally | Standard `PROGRAM_FILE` guard and keyword-configurable `main` |
| **API generality** | Concrete `String` arguments | Concrete `String` arguments | Concrete vector and `String` types | Uses `AbstractString`, `Integer`, `Real`, and named tuples appropriately |
| **Documentation accuracy** | Clear, but claims about strict conversion/performance do not address mixed cells | Extensive, but commentary overstates broadcasting and misses the reduced-DataFrame error | Most detailed; however, the claim that `readtable` “mirrors `xlsread` semantics exactly” is factually wrong for this workbook | Concise and mostly locally accurate, but leaves the rectangular-table assumption unstated |
| **Plot decomposition** | DRY shared left-axis helper | Reusable `twin_plot!`, but five figure bodies repeat left-axis setup | Reusable left-axis helper; five explicit figure functions | Most compact: one parameterized dual-axis plotting function handles Figures 2–5 |
| **Original reproducibility** | No Project/Manifest and no active run | No Project/Manifest; save block is commented out | Installation instructions but no original Project/Manifest | No Project/Manifest or input-contract validation |

### 4.2 Shared strengths

All four models:

- correctly recognised that MATLAB and Julia are both 1-based;
- used the requested XLSX.jl, DataFrames.jl, Plots.jl, and GR ecosystem;
- retained the intended signal assignments, colours, labels, Y limits, and line/scatter distinction;
- returned or retained separate plot objects and used functions instead of placing all work in global scope;
- used `twinx()` plus mutating `plot!`/`scatter!` calls in a form that renders with the tested Plots.jl version;
- initially preserved the MATLAB source's inconsistent `T09` title in Figure 2, which is translation fidelity rather than a newly introduced model error.

### 4.3 Shared weaknesses

The dominant common failure was not Julia syntax; it was failure to establish the workbook's data contract before designing the loader. `CT07` is not one conventional rectangular table. It contains:

- a mechanical region in A:D with 1,807 numeric rows beginning at row 4; and
- an AE region in E:N with 5,850 numeric rows beginning at row 2.

Three models relied on `XLSX.readtable` automatic inference, which returned E:M as nine logical columns and destroyed the MATLAB code's physical-column semantics. Gemini preserved the raw physical columns but still treated heterogeneous full columns as directly convertible numeric vectors.

All four also applied X limits only to the left subplot. The right subplot created by `twinx()` autoscaled independently. Consequently, Figures 2–5 do not rigorously reproduce MATLAB's shared-X `yyaxis` behaviour; AE events are horizontally transformed relative to the stress curve. This defect remains visible in all four saved artifact sets.

## 5. Model-specific code observations

### 5.1 Gemini 3.1 Pro

Gemini's use of `XLSX.readxlsx(...)[sheet][:]` is the closest initial analogue to MATLAB's physical numeric matrix because it retains worksheet column positions. Its nested `plot_stress_base` also removes the principal plotting duplication. However, the response converts each heterogeneous full column with `Float64.(...)`, so metadata and missing cells cause a blocking error. More fundamentally, the saved program is a no-op because the invocation is commented out. The result is a readable library-like draft, not an executable program.

### 5.2 DeepSeek V4 Pro

DeepSeek provides clear top-level functions, a normal entry-point guard, and a reusable twin-axis helper. Its loader, however, has two separate correctness defects. First, `readtable` returns only nine inferred columns. Second, even on an ideal 14-column table, `df[:, key_cols]` creates an eight-column DataFrame, after which the code incorrectly accesses positions 9, 10, 12, and 14 and mislabels earlier positions. A single `dropmissing` across all eight channels would also truncate the longer AE domain to the shorter mechanical domain. These are semantic defects independent of the later fixture-name mismatch.

### 5.3 Claude Sonnet 4.6

Sonnet has the most extensive explanatory documentation and strong typed function boundaries. Its `to_float` helper is more defensive than Gemini's direct broadcast and GPT's `coalesce`-only conversion. The critical weakness is a confident but false loader claim: default `readtable` does not preserve this worksheet's physical A:O layout. The initial program therefore fails before the otherwise sound plotting functions can be reached. The unconditional `main()` call is convenient for a script but makes the file less safe to include as a module.

### 5.4 GPT-5.5

GPT-5.5 has the strongest balance of concision, parameterization, type generality, and DRY plotting design. `numeric_column`, `extract_signals`, a shared keyword tuple, a single dual-axis helper, a named plot tuple, and a guarded `main` form a coherent small program. Nevertheless, the abstraction boundary is wrong: `readtable` changes the meaning and number of the positions before the carefully written extraction code sees them. The code is therefore maintainable in form but incorrect for the actual data model.

## 6. Debug-process comparison

| Dimension | Gemini 3.1 Pro record | DeepSeek V4 Pro record | Sonnet 4.6 record | GPT-5.5 record |
|---|---|---|---|---|
| **Original preserved?** | Yes; repair is a separate `Test3_fixed.jl` | Yes; harness bypasses the loader without editing the original | Only in the Markdown record; the workspace `.jl` file was edited in place | Yes; original plus a constants-only copy were tested separately |
| **Failure isolation** | Separates no-op run, sheet lookup, mixed-cell conversion, rendering, and layout margins | Separates environment, sheet mismatch, nine-column inference, latent reindex bug, and export | Separates environment, filename, sheet, table inference, export, and title | Separates environment, filename, sheet, nine-column inference, strict direct runs, and harness-only rendering |
| **Workbook investigation** | Raw dimensions, separate numeric masks, row counts, ranges, and maximum stress | Physical ranges and separate 1,807/5,850 domains | Explicit A:O probe from row 4; reports a shared 5,848-row table | Physical A:N inspection and separate 1,807/5,850 domains |
| **Remediation delivered** | Repaired executable script with CLI arguments, validation, separate row masks, headless export, and pinned project | No repaired production script; direct-range harness tests plotting functions | Repaired executable main script with explicit range, headless export, and pinned project | No repaired production script; harness manually builds the signal tuple |
| **Artifact verification** | 31 structural PNG assertions, hashes, run log, row counts, and visual review | PNG type, dimensions, hashes, non-identity, and visual review | End-to-end run, exactly-five/non-empty check, hashes, metadata, visual review, and a source-text title check | PNG metadata and visual review; strict original and constants-only failures are documented |
| **Scientific checks** | Reports 1,807/5,850 rows, time ranges, max stress, and measured twin-X mismatch | Finds the latent reduced-DataFrame bug and the two-domain data-loss problem | Explicitly admits no array-by-array MATLAB comparison; does not preserve the full 5,850-point AE domain | Reports separate ranges and measured left/right X limits; no durable numerical regression test |
| **Main limitation** | Structural tests do not validate array values or X alignment; repair changes Figure 4 marker size to 3 | Diagnosis is strong, but no corrected end-to-end deliverable or automated regression suite remains | Editing the original weakens provenance; row-4 unified loading omits the first two AE rows; title check tests source text, not rendered output | Strong diagnosis but no corrected production script, manifest, or durable automated test harness |

### Debugging conclusions

- **Best preserved repair workflow**: Gemini. The original remains untouched, the repair is explicit, dependencies are pinned, and the executable accepts real paths. This is the cleanest provenance chain among the four.
- **Strongest discovery of a model-specific latent bug**: DeepSeek's evaluation. It identifies the reduced-DataFrame reindexing defect that is independent of the irregular workbook.
- **Only repaired workspace main path demonstrated directly**: Sonnet. This is useful operational evidence, but it is evidence for the edited program, not the original response.
- **Strongest strict separation of original, constants-only, and harness paths**: GPT-5.5. The two direct failures and the component-only success are clearly distinguished.

These statements concern the quality of the recorded workflows, not debugging speed. There is insufficient common timing and intervention data to compare efficiency.

## 7. Evaluation-quality comparison

Legend: **Yes** = explicitly analysed with evidence; **Partial** = acknowledged but not fully tested; **No** = not established in the record.

| Evaluation criterion | Gemini record | DeepSeek record | Sonnet record | GPT-5.5 record |
|---|---:|---:|---:|---:|
| Separates original from repaired/harness output | Yes | Yes | Yes | Yes |
| Distinguishes prompt-era names from later fixture names | Yes | Yes | Yes | Yes |
| Explains physical-column loss from `readtable` | Not applicable to its raw loader | Yes | Yes | Yes |
| Detects mixed headers and separate row domains | Yes | Yes | Partial | Yes |
| Detects an additional model-specific loader bug | No additional defect | Yes | No | No |
| Tests or measures both twin subplot X limits | Yes | Partial/visual | Partial/explicitly unproven | Yes |
| Preserves artifact provenance warnings | Yes | Yes | Yes | Yes |
| Automated artifact checks | Yes, 31 structural checks | No durable suite shown | Partial, count/non-empty plus text grep | No durable suite shown |
| Numerical regression against trusted MATLAB arrays | No | No | No | No |
| Pixel/geometry regression against trusted MATLAB figures | No | No | No | No |

The evaluation records are generally much more rigorous than the Experiment #1 comparison because they explicitly distinguish syntax, component viability, repaired execution, and end-to-end success. Their common remaining weakness is the absence of a trusted scientific oracle. File existence, dimensions, and plausible curves establish that rendering occurred; they do not establish that every extracted value, event time, axis transformation, or marker geometry matches MATLAB.

## 8. Objective conclusions by criterion

| If the priority is... | Evidence-supported result |
|---|---|
| **Correct unchanged execution on the supplied workbook** | None of the four succeeds. |
| **Cleanest original software structure** | GPT-5.5 has the best balance of compactness, parameterization, type generality, and reusable plotting logic, but its loader remains blocking. |
| **Closest initial preservation of physical Excel columns** | Gemini, through raw worksheet-matrix loading; it still fails on heterogeneous rows and has no active entry point. |
| **Most extensive initial documentation** | Sonnet 4.6; documentation volume does not prevent its incorrect `readtable` equivalence claim. |
| **Most severe independent loader defect** | DeepSeek V4 Pro, because the reduced-DataFrame reindexing error would fail even on a conventional 14-column table. |
| **Most reproducible separate repair artifact** | Gemini, due to preserved original, separate fixed script, Project/Manifest, CLI contract, logs, and automated structural checks. |
| **Successful edited end-to-end script** | Sonnet, after repairs; however, its shared row-4 range yields 5,848 AE rows rather than the verified 5,850 and therefore is not proven numerically equivalent to MATLAB. |
| **Most explicit component-vs-end-to-end provenance** | Gemini and GPT are strongest; DeepSeek and Sonnet also state the boundary clearly. |

The central technical lesson is shared across all four models: superficial MATLAB-to-Julia syntax conversion is not the hard part. Correct migration requires an explicit spreadsheet schema, independent handling of the mechanical and AE sampling domains, and tests for plot-coordinate semantics. The models are more alike in missing those requirements than they are different in code style.

## 9. Recommended protocol for a fair Experiment #4

1. Use one byte-identical prompt for all models, with one unambiguous workbook filename and worksheet name.
2. Provide the workbook at generation time and require the model to inspect its sheet names, used range, headers, and numeric row domains before coding.
3. Preserve every original response unchanged; place repairs in separately named files.
4. Supply trusted MATLAB-exported arrays or checksums for all eight signals.
5. Assert the expected 1,807 mechanical rows, 5,850 AE rows, time ranges, maximum stress, selected sample values, and finite-value counts.
6. Assert identical X limits on both subplots for Figures 2–5 and compare marker geometry against a stated tolerance.
7. Require a `Project.toml` and `Manifest.toml`, a direct-run command, an explicit output contract, and one common test suite.
8. Record wall-clock time, tool calls, human interventions, and whether each fix was proposed autonomously; only then compare debugging efficiency.

## 10. Final assessment

The four LLMs all produce recognisably idiomatic Julia and competent plotting abstractions, yet all four unchanged programs fail the actual-workbook test. Their differences are mainly architectural: Gemini preserves raw columns but ignores heterogeneous rows and execution; DeepSeek introduces an additional reindexing error; Sonnet offers the strongest narrative explanation but makes the strongest incorrect loader claim; GPT offers the cleanest compact design but builds it on the same invalid table assumption.

The later debugging records substantially improve the quality of the evidence. Gemini provides the cleanest separate repaired workflow, Sonnet demonstrates a repaired direct-run path, and DeepSeek/GPT provide strong loader and plotting diagnoses through harnesses. None proves exact MATLAB equivalence. The most objective overall conclusion is therefore not a model ranking, but a boundary: **all four are useful first-draft translators, while none of the original outputs is a validated scientific migration without workbook-aware debugging and independent regression tests.**
