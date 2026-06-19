# Cross-Language Comparison of Experiments 2 and 3: MATLAB-to-Python versus MATLAB-to-Julia

## 1. Scope and basis of comparison

This report compares the paired Test 02 (MATLAB-to-Python) and Test 03 (MATLAB-to-Julia) outputs produced by Gemini 3.1 Pro High, Claude Sonnet 4.6 High, DeepSeek V4 Pro, and GPT-5.5 XHigh. SMOP is excluded. The comparison uses the submitted scripts, their execution and evaluation records, and the two horizontal reports, `02Prompt_Output_Comparison_Experiment_2.md` and `03Prompt_Output_Comparison_Experiment_3.md`.

“Completeness” is used here in an operational and semantic sense rather than as a code-length measure. A complete translation should:

1. retain all five requested figures and all eight signal assignments;
2. load the supplied workbook without destroying physical column meaning or valid observations;
3. preserve important MATLAB plotting semantics, especially the shared X coordinate of `yyaxis` plots;
4. execute through the full loading-to-plotting path, rather than only after a loader bypass; and
5. provide enough validation and reproducibility evidence to distinguish a plausible picture from a faithful scientific migration.

The experiment is not perfectly controlled. The recorded prompts do not all use the same workbook and worksheet identifiers. Some use `Commercial Tensile Tests.xlsx` / `CT07`, while others use `Tensile-processed.xlsx` / `CT-07`; the supplied fixture is the former. The Julia prompt also explicitly specifies the latter identifiers even when the embedded MATLAB source names the former. Therefore, filename-only failures are separated from code-level defects, and repaired or harness-generated figures are not treated as successful unchanged translations.

## 2. Main conclusion

**The MATLAB-to-Python outputs are more complete overall than the MATLAB-to-Julia outputs for this task.** This conclusion holds in all four within-model pairings, although the size of the advantage varies.

Under the strictest unchanged-fixture criterion, neither language has a fully successful original submission: every unchanged output encounters either an identifier mismatch or a code-level failure. The more informative distinction is how close the submitted logic comes to a valid end-to-end migration after separating prompt-derived identifiers from translation logic:

- In Python, GPT-5.5's existing loader and plotting logic completes and creates five figure objects after only the workbook and worksheet constants are adapted to the supplied fixture. The other three Python outputs fail because their loaders pass mixed text and numbers to Matplotlib.
- In Julia, none of the four original loading-to-plotting paths completes on the supplied workbook. Three lose the physical Excel layout through `XLSX.readtable`; Gemini preserves the physical layout but fails on heterogeneous cells and has no active entry point.
- All four Python outputs use Matplotlib `Axes.twinx()`, whose twin axes share the X axis. All four Julia outputs apply X limits only to the left Plots.jl subplot while the right subplot autoscales independently, so the stress and AE traces do not use the same numeric X transformation.

Thus, Python is not complete in an absolute sense, but it is consistently closer to a complete and semantically correct result. The strongest single Python output is executable after a metadata-only adaptation; the strongest Julia outputs still require a data-loader repair or a harness that bypasses the loader, and the Julia dual-axis plots retain an X-alignment defect.

## 3. Paired model comparison

| Model | Test 02: MATLAB-to-Python | Test 03: MATLAB-to-Julia | More complete paired output |
|---|---|---|---|
| **Gemini 3.1 Pro High** | Correct zero-based column mapping and recognisable five-figure Matplotlib translation. `header=None` retains metadata, so mixed strings and numbers cause Figure 1 to fail, but `main()` is active. | Raw worksheet reading is the best Julia attempt at preserving physical columns, but full-column `Float64.(...)` fails on metadata and `missing`; the only function call is commented out; twin-axis X limits are not shared. | **Python**, because it is at least an active end-to-end script and its plotting coordinate model is closer to MATLAB, despite the blocking loader defect. |
| **Claude Sonnet 4.6 High** | Correct indexing and strong plotting documentation/helpers. `header=0` removes only one row, leaving mechanical metadata that causes Figure 1 to fail; the submitted module also performs I/O at import time. | Strong function boundaries and documentation, but the claim that `XLSX.readtable` mirrors `xlsread` is false for this workbook. It receives nine inferred columns rather than the intended physical layout and also has independent twin-X scaling. | **Python**, because its physical columns remain present and the dominant repair is numeric cleaning, whereas the Julia loader changes the table's column meaning before extraction. |
| **DeepSeek V4 Pro** | Correct zero-based indices and the intended five plots. `header=None` plus NumPy conversion retains mixed objects, and an unguarded maximum is vulnerable to `NaN`; the script is procedural and runs at import. | In addition to nine-column `readtable` inference, it selects eight columns and then incorrectly reuses original positions 9, 10, 12, and 14 on the reduced DataFrame. A global `dropmissing` also conflates the 1,807-row mechanical and 5,850-row AE domains. | **Python**, because the Julia output adds an independent reindexing error and a more destructive data-domain assumption. |
| **GPT-5.5 XHigh** | The best original result: whole-frame numeric coercion, width validation, `np.nanmax`, a reusable dual-axis helper, and an entry-point guard. After changing only the prompt-derived file and sheet constants, it runs and creates all five figures. | The cleanest Julia organization, but `readtable` still returns nine logical columns; `coalesce` handles `missing` but not text; plotting succeeds only when a harness bypasses loading and extraction. | **Python by a clear margin**, because the submitted analysis logic is already operational after identifier adaptation. |

The pairwise pattern is therefore four out of four in favour of Python. This does not imply that every Python script is good, nor that Julia is intrinsically unsuitable. It shows that, under these prompts and with this irregular workbook, the models' learned Python migration patterns are more reliable than their Julia migration patterns.

## 4. Why Python is more complete in this experiment

### 4.1 Language and ecosystem factors

Julia has one apparent advantage: MATLAB and Julia are both 1-based, whereas Python requires a 1-based-to-0-based conversion. In practice, this advantage did not determine the result. All eight outputs selected the intended column positions correctly. The Python prompt made the index conversion explicit, and all four models followed it without an off-by-one error.

The decisive differences appear at library boundaries:

- `pandas.read_excel(..., header=None)` preserves the worksheet's physical columns, even when it does not make them immediately numeric. This makes the failure visible and repairable through coercion and per-signal masks. GPT-5.5 already used `pd.to_numeric(errors="coerce")` and a missing-aware maximum.
- `XLSX.readtable` interprets the worksheet as a logical table. On this fixture it returns nine inferred columns, effectively E:M, rather than preserving the physical A:N positions on which the MATLAB script relies. Three Julia outputs therefore lose the meaning of column numbers before their otherwise correct 1-based extraction code runs.
- Matplotlib's object-oriented `twinx()` is a well-established direct mapping for this use case and shares the X axis. Plots.jl's overlaid `twinx()` pattern is superficially similar but does not automatically reproduce the tested MATLAB `yyaxis` coordinate behaviour when limits are applied only to the left subplot.
- Python's scientific stack is more frequently represented in model training material and has highly conventional recipes for numeric coercion, missing values, plotting, and headless execution. The Julia packages are capable, but their table inference, missing-value types, mutation conventions, and subplot semantics require more package-specific knowledge.

Julia's stricter handling of `Missing` is not itself a defect; failing early can be safer than silently plotting corrupted data. The problem is that the models wrote strict conversions without first establishing what the cells contain. Likewise, Julia syntax is not generally more complex than Python syntax for this script. The lower completeness comes mainly from less reliable package-level semantic mappings and overconfident assumptions about equivalence, not from the core language grammar.

### 4.2 Prompt constraints and biases

The Python prompt identifies the important index-base difference and suggests `pandas` and Matplotlib's `twinx()`. These instructions are specific enough to guide the models toward appropriate primitives without forcing one particular Excel representation.

The Julia prompt is more prescriptive. It requires `XLSX.jl`, `DataFrames.jl`, Plots.jl with GR, and broadcasting syntax. These choices are reasonable in isolation, but they create three biases:

1. Requiring DataFrames encourages `XLSX.readtable` even though the source depends on physical worksheet positions rather than a conventional rectangular table.
2. Requiring broadcasting “for high performance” encourages expressions such as `Float64.(whole_column)`, although no meaningful element-wise computation in the source needs this emphasis. In Gemini's output, this becomes a direct failure on heterogeneous cells.
3. Requiring `twinx()` suggests an API-name equivalence without stating the required coordinate invariant: the left and right plots must use identical X limits and transformations.

Both prompts also focus on visible translation features—library replacement, index syntax, modularity, labels, and limits—while omitting the data and verification contract. The resulting scripts often look idiomatic and well documented while remaining scientifically incomplete. Clean decomposition cannot rescue a loader that has already changed what “column 14” means.

### 4.3 Defects and ambiguities in the MATLAB source and experimental fixture

The original MATLAB script hides several assumptions that `xlsread` previously handled implicitly:

- The worksheet is not one rectangular numeric dataset. The mechanical domain in A:D contains 1,807 finite paired observations beginning at row 4, while the AE domain in E:N contains 5,850 finite paired observations beginning at row 2.
- The source gives no explicit cell range, header schema, row-start rule, missing-value policy, or expected observation counts. `data(:, n)` therefore looks simpler and more uniform than the actual worksheet.
- The source combines signals of different lengths in one numeric matrix and relies on downstream plotting behaviour around nonnumeric or missing cells without documenting it.
- Figure 2 is titled `T09 Commercial Normalised RMS Profile` even though the dataset is CT07. Literal preservation is faithful translation, but the source itself is internally inconsistent.
- The Figure 2 comment calls the RMS layer a scatter plot while the MATLAB command is `plot`, adding another small ambiguity.
- The source creates interactive figures but defines no filenames, output directory, headless behaviour, dependency versions, assertions, or reference arrays/images.

The experiment adds a separate naming inconsistency: the prompt-era `Tensile-processed.xlsx` / `CT-07` identifiers do not match the supplied `Commercial Tensile Tests.xlsx` / `CT07` fixture in some runs. A model cannot infer the later fixture name from a contradictory prompt, so this should not be counted as a pure translation defect. It does, however, demonstrate that the prompt lacks an authoritative input contract.

These source defects affect both languages. Python performs better because its common spreadsheet and plotting patterns happen to tolerate or expose more of the hidden structure, not because the source is intrinsically Python-friendly.

## 5. Recurrent problems across Test 02 and Test 03

### 5.1 Data ingestion is treated as a one-line API substitution

The most important shared failure is the assumption that MATLAB `xlsread` can be replaced directly by `pandas.read_excel` or `XLSX.readtable`. Seven of the eight outputs require a loader repair or cannot reach plotting on the real fixture. Choosing `header=0`, `header=None`, or automatic table inference is not a substitute for inspecting the workbook's physical layout and numeric domains.

### 5.2 The scripts assume one clean, rectangular sampling domain

Most outputs extract all eight variables as if they have the same valid rows. This overlooks the 1,807-point mechanical domain and the 5,850-point AE domain. Global `dropna`/`dropmissing` can discard valid AE observations, while no cleaning leaves text or missing values in plot arrays. Correct migration requires separate pairwise masks for mechanical and AE signals.

### 5.3 Position is checked, but meaning is not validated

All models correctly translate the written column numbers, yet most do not verify that the loaded object still has at least 14 physical columns or that those positions contain the expected signals. The Julia results make this distinction especially clear: correct 1-based syntax is useless after `readtable` has redefined the table shape.

### 5.4 Missing values and numeric conversion are handled incompletely

The Python failures include mixed object arrays and unsafe maxima; the Julia failures include `Float64(::Missing)`, text conversion, or destructive global row removal. Only the GPT-5.5 Python output combines numeric coercion with a missing-aware maximum, and even it does not validate empty/all-NaN signals or expected finite counts.

### 5.5 Plot API resemblance is mistaken for semantic equivalence

The outputs reproduce colours, labels, limits, and the line/scatter distinction well. However, no original answer proves equivalence against trusted MATLAB figures or arrays. In Julia, all four dual-axis implementations leave the right subplot independently scaled on X. Minor-grid behaviour, marker geometry, margins, and axis colouring also vary between libraries. A plausible image is not evidence of coordinate equivalence.

### 5.6 Readability is prioritised over executable correctness

Several outputs contain good docstrings, helpers, type annotations, and parameterisation, but the abstractions sit above an invalid input model. There are also entry-point problems: two Python outputs execute on import, one Julia output calls `main()` unconditionally, and Gemini's Julia output never calls its main function at all.

### 5.7 Reproducibility and output contracts are absent

Across the original submissions, there is no pinned dependency environment, no common direct-run command, no active deterministic image export, and no trusted numerical or visual regression suite. All eight preserve the source's interactive-display orientation. Later repairs and harnesses provide useful evidence, but they do not make the original answers complete.

### 5.8 Source inconsistencies are copied without a declared fidelity policy

All outputs preserve the `T09` title. Some explain that it is probably a source typo; others simply reproduce it. A migration prompt should say whether source anomalies must be preserved, corrected, or preserved with an explicit warning. Without that policy, literal fidelity and domain correctness can be mistaken for each other.

## 6. Implications for prompt revision

The main prompt lesson is to shift from **“translate these visible MATLAB statements”** to **“inspect, translate, and verify an explicit scientific data contract.”** The following changes would address the observed failure modes.

### 6.1 Make the input contract authoritative

State one exact workbook path and worksheet name and require the model to verify that both exist before coding. Resolve any conflict between prose constraints and the embedded source. Specify that physical Excel columns A:N must be preserved and that automatic table inference must not change positional meaning.

### 6.2 Describe or require discovery of the worksheet schema

Either provide the schema directly or require a first inspection phase that reports used range, sheet names, header/unit rows, column types, and separate numeric domains. For this fixture, the prompt should state or require verification of 1,807 mechanical pairs and 5,850 AE pairs, with their different starting rows.

### 6.3 Specify per-domain cleaning rules

Require each signal to be coerced to numeric safely and require pairwise finite masks for `(strain, stress)`, `(t1, stress)`, and each `(time, AE signal)` pair. Explicitly prohibit one global `dropna`/`dropmissing` across all eight signals. Require a finite stress maximum and clear errors for empty or all-missing arrays.

### 6.4 Define semantic plotting invariants

Do not merely request `twinx()`. Require the left and right axes in Figures 2–5 to use exactly the same X limits and numeric transformation, and require this to be asserted in tests. State the intended line versus scatter geometry, marker-size convention, Y limits, titles, labels, and minor-grid behaviour.

### 6.5 Separate correctness from idiomatic style and performance

Ask for correctness and validation before modularity or optimisation. In the Julia prompt, broadcasting should be used only where an actual element-wise operation is required, not as a mandatory performance ornament. Permit raw worksheet/matrix access when physical positions matter, even if DataFrames are used later for labelled organization.

### 6.6 Add an execution and evidence contract

Require a command-line entry point, headless execution, deterministic export of five named figures, and a dependency file (`requirements.txt`/lock file for Python; `Project.toml` and `Manifest.toml` for Julia). Require tests for:

- workbook and worksheet discovery;
- at least 14 preserved physical columns;
- 1,807 mechanical and 5,850 AE finite pairs;
- selected sample values, time ranges, and maximum stress;
- five generated figures with the expected axis topology;
- identical X limits on both sides of every dual-axis figure; and
- nonempty, freshly generated output files.

If exact MATLAB reproduction is claimed, provide trusted MATLAB-exported arrays or checksums and reference figures with tolerances. Without an oracle, the prompt should ask for structural and numerical equivalence rather than “exact plots.”

### 6.7 Declare a source-defect policy

Tell the model to preserve source behaviour by default but list suspected source defects separately. For this case, it should preserve `T09` in a literal translation, flag the CT07/T09 inconsistency, and optionally expose a clearly labelled corrected-title mode. Repairs must be saved separately from the original answer so their provenance remains auditable.

## 7. Suggested language-neutral prompt core

The two experiments would be fairer if they shared the following core and differed only in target-language libraries:

> Inspect the supplied workbook before writing the translation. Confirm the exact file, sheet, used range, physical column positions, header/unit rows, and independent numeric row domains. Preserve physical columns A:N; do not rely on automatic table inference if it changes positional meaning. Convert each requested signal safely, retain the mechanical and AE domains independently, and validate the expected finite counts. Reproduce all five plots. For every dual-axis plot, assert that both axes use identical X limits and transformations. Provide a direct-run, headless script that exports five deterministic files, plus dependency metadata and tests for data counts, selected numeric values, plot structure, and output freshness. Preserve source anomalies but report them explicitly. Do not claim exact MATLAB equivalence unless the supplied MATLAB reference arrays and figures pass the stated tolerances.

Target-specific additions should then be narrow:

- **Python:** use pandas/openpyxl and Matplotlib's object-oriented API; document the 1-based-to-0-based conversion.
- **Julia:** use XLSX.jl and Plots.jl/GR; raw worksheet access is permitted to preserve physical positions; use DataFrames only after the schema is preserved; apply X limits explicitly to both twin subplots; use broadcasting only when semantically required.

## 8. Final assessment

The experiments show a consistent distinction between **surface translation completeness** and **scientific migration completeness**. All four models, in both languages, reproduce the visible structure of the MATLAB script surprisingly well: the column numbers, five figures, signal assignments, labels, limits, colours, and line/scatter choice are largely correct. The failures arise at the hidden boundaries—spreadsheet semantics, unequal sampling domains, missing values, twin-axis coordinates, execution contracts, and validation.

Python has the higher completeness in this comparison because its ecosystem mappings preserve physical columns more readily, Matplotlib's twin axes better match the required shared-X behaviour, and at least one submitted Python design is operational after a prompt-derived identifier correction. Julia's syntactic similarity to MATLAB helps with indexing but creates a false sense of direct equivalence; `readtable`, strict missing-value conversion, and Plots.jl twin-axis behaviour require explicit handling that the prompts did not demand and the models did not reliably infer.

The most important prompt revision is therefore not to add more syntax instructions. It is to make the workbook schema, semantic invariants, validation oracle, and execution evidence part of the task. Under the current prompts, the LLMs are competent first-draft translators in both languages, but Python produces the more complete first draft; neither language's outputs should be treated as validated scientific migrations without workbook-aware testing.
