# Prompt Output Comparison: Experiment #1 (`CT07.m`)

> [!warning] Unevaluated preliminary assessment
> This historical report is based on generated text and static inspection. The
> outputs had not yet been executed on the frozen fixture or compared with the
> MATLAB oracle. Its rankings are preliminary observations, not a general
> ranking of model families. See
> [[Individual Project/README|Canonical Project Overview]].

## 1. Experiment Metadata
- **Date**: 2026.05.20 to 2026.05.26
- **Source File**: `CT07.m` (Acoustic Emission - Tensile Test Plotting)
- **Target Language**: Python (NumPy, Pandas, Matplotlib)

## 2. Standardised Initial Prompt
The following prompt was used across all platforms:

```text
Act as a Senior Scientific Computing Engineer. I am working on an MSc project migrating an Acoustic Emission (AE) analysis framework from MATLAB to an open-source Python environment. 

Your task is to translate the following MATLAB script into Python. 

Requirements & Constraints:
1. Data Loading: Replace MATLAB's `xlsread` with an appropriate Python library (e.g., `pandas`).
2. Array Indexing: Pay strict attention to the 1-based to 0-based indexing conversion between MATLAB and Python. Ensure data slicing is correct.
3. Visualization: Use `matplotlib` (and/or `seaborn`) to replicate the exact plots. Handle MATLAB's `yyaxis left` and `yyaxis right` elegantly using Python's object-oriented plotting approach (e.g., `twinx()`).
4. Readability: Keep the code clean, modular, and PEP-8 compliant. Add brief comments explaining the Python-specific implementation choices.

Here is the original MATLAB code:
(See Section 3 for source)
```

## 3. Original MATLAB Source Code (`CT07.m`)
```matlab
data = xlsread("Tensile-processed.xlsx", 'CT-07'); 
t1 = data(:, 1);
stress = data(:, 4);
strain = data(:, 3); 
time = data(:,5);
rms = data(:, 9);
cumrms = data(:, 10);
energy = data(:, 12);
cumenergy = data(:, 14);

% ... (Plotting code follows)
```

## 4. Platform Outputs & Analysis
### 4.1 ChatGPT 5.3 
*(Use Codex Cli)*
- **Generated Code**: [[01Test Record from gpt-5.3-codex xhigh]]
- **Strengths**:
    - **High Degree of Modularity**: The implementation utilizes functional encapsulation for data ingestion (`load_ae_data`) and visualization logic (`plot_dual_axis`), significantly enhancing code reusability.
    - **Type Hinting**: The integration of Python type annotations (e.g., `def load_ae_data(file_path: str) -> dict[str, np.ndarray]`) improves code readability and facilitates robust IDE support.
    - **Explicit Index Mapping**: The documentation clearly delineates the column index transformation from MATLAB to Python, simplifying long-term maintenance.
    - **Flexible Visualization Management**: The `plot_dual_axis` function is parameterized (e.g., `right_as_scatter`), allowing for versatile handling of diverse plotting requirements.
    - **Robust Error Handling**: The use of `pd.to_numeric` to convert non-numeric cells to `NaN` effectively replicates MATLAB’s numerical matrix behavior.
- **Weaknesses**:
    - **Header Handling**: The default configuration utilizes `header=None`, failing to account for Excel files with existing headers (requiring manual adjustment to `header=0`).
    - **Documentation Redundancy**: Certain comments, particularly those regarding column index mapping, overlap with the underlying code logic and could be more concise.
- **Functional Verification**:
    - **Indexing**: Correct (implements 0-based indexing via `iloc`).
    - **Plotting**: Correct (utilizes `twinx()` for dual Y-axes with consistent color management).
### 4.2 Google Gemini 3 Flash 
*(Use Gemini Cli)*
- **Generated Code**: [[01Test Record from Gemini 3 flash]]
- **Strengths**:
    - **Effective Encapsulation**: The entire workflow is encapsulated within an `ae_analysis_workflow` function, facilitating streamlined invocation.
    - **Aesthetic Simulation**: The `apply_matlab_style` function accurately replicates MATLAB-style grids and titles, ensuring strong visual consistency.
    - **Error Handling**: Includes basic exception handling for file loading (e.g., `FileNotFoundError`).
- **Weaknesses**:
    - **Inconsistent Indexing Transformation**: While the documentation notes the "MATLAB: `data(:, 1)` → Python: `data[:, 0]`" transition, the implementation utilizes NumPy slicing after `df.to_numpy()`, leading to conceptual confusion between NumPy and Pandas indexing logic.
    - **Ambiguous Header Processing**: The necessity of `header=None` is not explicitly addressed, which may lead to user error.
    - **Incomplete Visualization Management**: Color configuration for the secondary Y-axis is insufficient (only `tick_params` are defined, while the axis line color is omitted).
    - **Variable Naming Conventions**: The use of `ae_time` instead of the original `time` increases cognitive load.
- **Functional Verification**:
    - **Indexing**: Correct (though documentation and implementation logic are misaligned).
    - **Plotting**: Partially Correct (dual Y-axis implementation is technically sound, but color management is incomplete).
### 4.3 Anthropic Claude Sonnet 4.6 
*(In chat mode maybe not good as code mode, Claude code need money)*
- **Generated Code**: [[01Test Record from Sonnet 4.6 Adaptive]]
- **Strengths**:
    - **Comprehensive Documentation**: Provides an exhaustive MATLAB-to-Python mapping table and detailed rationale for each architectural decision.
    - **Explicit Header Handling**: Clearly states the assumption of `header=0` and prompts the user to adjust based on the dataset's actual structure.
    - **Refined Visualization Management**: Utilizes an `apply_minor_grid` function for uniform grid styling; ensures complete color management for the secondary Y-axis (including axis lines and labels).
    - **Performance Optimization**: Pre-calculates `stress_max` to eliminate redundant computations.
    - **Structured Code Organization**: Code is logically partitioned into functional blocks with clear annotations.
- **Weaknesses**:
    - **Insufficient Modularity**: Redundant logic (e.g., dual Y-axis plotting) is not encapsulated, resulting in code duplication.
    - **Hard-coded Parameters**: File paths and worksheet names are hard-coded within the script, hindering reusability.
- **Functional Verification**:
    - **Indexing**: Correct (utilizes 0-based indexing via `iloc`).
    - **Plotting**: Correct (dual Y-axis implementation and color management meet all requirements).
### 4.4 DeepSeek-AI DeepSeek 3.2
*(I didn't find the way to use V3.2 in a free way, so I use v4 flash in Opencode Cli to reduce the reliance of the structure( like using v4 flash in Claude code Cli ))*
- **Generated Code**: [[01Test Record from Deepseek v4 flash (free) max]]
- **Strengths**:
    - **Conciseness**: The code structure is compact and free of extraneous comments.
    - **Correct Header Processing**: Appropriately uses `header=None` for raw data ingestion.
    - **Functional Plotting**: Correct dual Y-axis implementation with consistent color management.
- **Weaknesses**:
    - **Lack of Modularity**: Logic is presented as a continuous script without functional encapsulation, complicating maintenance.
    - **Sparse Documentation**: Lacks explanations for critical steps, such as the indexing transformation logic.
    - **Hard-coded Parameters**: File paths and worksheet names are hard-coded.
    - **Grid Styling Flaws**: `grid(True, which="minor")` is applied directly to `ax_left`, failing to account for potential grid conflicts on the secondary Y-axis.
- **Functional Verification**:
    - **Indexing**: Correct (implements 0-based indexing via `iloc`).
    - **Plotting**: Correct (dual Y-axis implementation is functional, though grid styling is suboptimal).
## 5. Summary Comparison Matrix
| Platform | Indexing Accuracy | Plot Elegance | Library Efficiency | Modularity | Documentation Quality | Error Handling | OOP Compliance |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **ChatGPT 5.3** | Fully Correct | Elegant dual Y-axis implementation with consistent color management and uniform grid styling; supports parameterization (e.g., scatter plot options). | Efficient utilization of Pandas and NumPy; avoids redundant calculations; high reusability through functional encapsulation. | Highly modular; encapsulates data loading and plotting logic into discrete functions. | Detailed documentation featuring type hints, function descriptions, and MATLAB-to-Python index mapping for ease of maintenance. | Includes exception handling for data ingestion (e.g., missing files) and robust conversion of non-numeric cells to `NaN`. | Strictly adheres to OOP principles, utilizing Matplotlib’s object-oriented interface (e.g., `ax.twinx()`) for a clear structure. |
| **Gemini 3 Flash** | Correct (Inconsistent Docs) | Correct dual Y-axis implementation; however, secondary Y-axis color management is incomplete (missing axis line color). | Utilizes Pandas and Matplotlib but fails to fully leverage NumPy vectorization; some logic remains suboptimal. | Moderate modularity; encapsulates the workflow but lacks abstraction for visualization logic. | Thorough documentation explaining key transformations, though some comments contradict the implementation logic. | Includes basic file-loading exception handling; lacks validation for data formatting (e.g., non-numeric cell handling). | Partially follows OOP; uses `ax.twinx()` but fails to fully encapsulate plotting logic within functions or classes. |
| **Claude Sonnet 4.6** | Fully Correct | Elegant dual Y-axis implementation with comprehensive color management (axis lines and labels) and uniform grid styling. | Efficient use of Pandas and Matplotlib; however, fails to encapsulate repetitive logic (e.g., dual Y-axis plotting). | Low modularity; procedural logic with significant code duplication. | Exceptionally detailed; provides a comprehensive mapping table and thorough rationale for transformation decisions. | Insufficient error handling; relies on default Pandas behavior without proactive exception management. | Adheres to OOP via `ax.twinx()`, but the overall structure is script-oriented rather than functional/modular. |
| **DeepSeek 3.2** | Fully Correct | Correct dual Y-axis implementation; grid styling is improperly applied (restricted to the primary axis). | Functional use of Pandas and Matplotlib; compact structure but lacks performance optimization (e.g., redundant calculations). | Negligible modularity; logic is entirely procedural, resulting in poor reusability. | Minimal documentation; lacks explanations for critical logic, such as indexing transformations. | No explicit error handling; relies entirely on default library behaviors. | Basic adherence to OOP via `ax.twinx()`; structure is primarily script-based without encapsulation of repetitive logic. |
## 6. Conclusion
**Top Performer: ChatGPT 5.3 (Codex CLI)**
- **Summary of Advantages**:
    1. **Modular Design**: Achieves high reusability by encapsulating logic into functions (e.g., `load_ae_data` and `plot_dual_axis`), aligning with software engineering best practices.
    2. **Code Quality**: Adheres to production-grade standards through the integration of type hinting, robust error handling, and comprehensive documentation.
    3. **Visualization Management**: The `plot_dual_axis` function provides flexibility for line and scatter plots while maintaining consistent aesthetics and grid styling.
    4. **Indexing Clarity**: Clearly documents the MATLAB-to-Python mapping, facilitating easier maintenance and debugging.

**Runner-up: Claude Sonnet 4.6**
- **Strengths**: Distinguished by exhaustive documentation and meticulous attention to visualization details (e.g., color management and grid styling), making it ideal for scenarios requiring high readability.
- **Weaknesses**: Limited modularity and significant code redundancy hinder its scalability and reusability.

**Recommendations for Improvement**:
- **Gemini 3 Flash**:
    - Enhance secondary Y-axis color management (specifically axis line colors).
    - Increase modularity by abstracting visualization logic into functions.
    - Synchronize documentation with implementation logic to eliminate ambiguity.
- **DeepSeek 3.2**:
    - Implement functional encapsulation and proactive error handling (e.g., file-loading exceptions).
    - Supplement the code with documentation explaining critical transformation steps.
    - Refine grid styling to ensure consistency across dual axes.

**Final Recommendation**:
For scientific computing tasks, **ChatGPT 5.3** provides the most robust output, balancing functional correctness, readability, and maintainability. For projects where extensive documentation and rationale are paramount, the output from **Claude Sonnet 4.6** serves as a valuable secondary reference.

---
# SMOP vs. AI Tools: Output Comparison & Evaluation

## 1. SMOP Output Evaluation (`CT07.m`)

Following the established evaluation methodology, here is the assessment of the SMOP tool's output compared to the original MATLAB script.

### 4.5 SMOP (Small Matlab and Octave to Python compiler)
*(Executed locally via CLI command `smop CT07.m`)*

**Generated Code**: `01Test Record from SMOP.md`

**Strengths**
- **Speed & Automation**: Processes the `.m` file directly from the CLI instantly without needing a carefully engineered prompt or internet access.
- **Logic & Structure Preservation**: Performs a literal 1:1 syntactic mapping of the MATLAB script, maintaining exact variable names, line-by-line structure, and execution flow.

**Weaknesses**
- **Heavy Dependency on Emulation**: Relies entirely on its own `libsmop` wrapper module to emulate MATLAB functions (e.g., `xlsread`, `yyaxis`, `concat`). It completely fails the core requirement to transition to native, open-source Python data science libraries (like `pandas` and `matplotlib`).
- **Non-Pythonic Indexing**: Fails to convert 1-based indexing to 0-based indexing. Instead, it forces Python to behave like MATLAB using `libsmop` arrays (e.g., `data(arange(),1)` instead of standard NumPy slicing like `data[:, 0]`).
- **Poor Modularity and Readability**: The resulting code is essentially "MATLAB written with Python syntax." It is not PEP-8 compliant and entirely misses Python's Object-Oriented Programming (OOP) paradigms for plotting (like `fig, ax = plt.subplots()` and `ax.twinx()`).

**Functional Check**
- **Indexing**: **Incorrect (Non-Standard)** – Retains 1-based indexing and MATLAB array syntax via the `libsmop` compatibility layer rather than adopting native Python 0-based indexing.
- **Plotting**: **Incorrect (Non-Standard)** – Does not utilize `matplotlib` OOP or `twinx()`; improperly relies on MATLAB's `yyaxis` command wrapped through `libsmop`.

---

## 2. Comparison: SMOP vs. AI Tools (GPT-5.3, Gemini 3, Claude 4.6, DeepSeek)

### Summary Comparison Matrix Update

| Platform               | Indexing Accuracy                           | Pandas Usage                         | Drawing Management          | Drawing Colors Matching | Grid Style | Modularity      | Primary Weaknesses & Suggested Remedy                                                                                               |
| :--------------------- | :------------------------------------------ | :----------------------------------- | :-------------------------- | :---------------------- | :--------- | :-------------- | :---------------------------------------------------------------------------------------------------------------------------------- |
| **AI Tools (Average)** | **Correct** (Converted to 0-based)          | High (Native Pandas adoption)        | OOP + `twinx()`             | Mostly Match            | Consistent | High to Highest | Requires prompt engineering; prone to minor detail misses (e.g., NaN handling or secondary axis color).                             |
| **SMOP**               | **Incorrect** (Keeps 1-based via `libsmop`) | **Failed** (Uses emulated `xlsread`) | MATLAB emulation (`yyaxis`) | Match (via emulation)   | Consistent | Low             | Extremely unidiomatic Python; heavily reliant on `libsmop`. Remedy: Only use as a structural reference, not for true modernization. |

### Advantages of AI Tools over SMOP
1. **Native Ecosystem Adoption**: AI tools successfully transition the script to use standard libraries like `pandas` and `matplotlib`, moving the codebase to an idiomatic Python stack. SMOP completely fails this, trapping the code in a MATLAB-emulated ecosystem.
2. **Idiomatic Code & Modernization**: AI intelligently translates array indexing (1-based to 0-based) and uses modern Object-Oriented plotting paradigms, ensuring long-term maintainability for Python developers.
3. **Refactoring & Modularity**: Advanced AI models (especially GPT-5.3 and Claude 4.6) refactor monolithic scripts into modular, reusable functions, significantly improving overall code quality.

### Weaknesses of AI Tools compared to SMOP
1. **Prompt Dependency**: AI output quality heavily relies on the clarity, constraints, and precision of the initial prompt, whereas SMOP provides a deterministic, push-button solution.
2. **Hallucination / Edge Cases**: AI might make assumptions about data formats (e.g., assuming `header=0` for Excel files when none exists) or miss minor styling details, whereas SMOP perfectly and blindly replicates the original logic line-by-line.
3. **Data Security / Offline Capability**: SMOP runs completely locally, making it inherently secure for sensitive projects, whereas most high-end AI tools require sending proprietary codebase snippets to external APIs.

### Conclusion
While **SMOP** is a fast, push-button transliteration tool, its heavy reliance on the `libsmop` compatibility layer defeats the fundamental purpose of modernizing a framework into an open-source Python environment. It outputs "MATLAB code in Python syntax," which creates significant technical debt for future Python maintainers.

**AI Tools** (such as Claude 4.6 and ChatGPT 5.3) are definitively superior for this migration project. Despite requiring careful prompt engineering and minor post-generation tweaks, they successfully convert MATLAB logic into native, idiomatic, and highly maintainable Python code utilizing industry-standard libraries.
