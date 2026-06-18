# Overview of Initial Prompting Methodology: MATLAB to Julia Migration

## 1. Objectives of Prompt Engineering
The primary goal of the prompting strategy is to ensure a high-fidelity translation of MATLAB scientific code to Julia, adhering to the principle of **functional equivalence** while leveraging Julia’s unique strengths. The strategy focuses on:
- Minimising human intervention during the initial translation phase.
- Capitalizing on Julia’s **1-based indexing** similarity to MATLAB, reducing cognitive load regarding index shifting compared to Python.
- Implementing idiomatic Julia practices (e.g., **Broadcasting**, `DataFrames.jl` usage, and `Plots.jl` composition) rather than literal line-by-line translation.
- Ensuring performance through Julia’s native compilation features (avoiding global scope variables in functions).

## 2. Structured Prompt Design
To ensure consistency across different LLM platforms (ChatGPT, Claude, DeepSeek, Llama), a standardized prompt structure is employed. This structure consists of four key components:

### 2.1 Persona Selection (Role Setting)
- **Role**: Senior Scientific Computing Engineer and Julia Specialist.
- **Rationale**: Setting this persona encourages the model to prioritize performance (avoiding global variables), type stability, and adherence to Julia-specific conventions (e.g., using `begin...end` blocks, proper broadcasting).

### 2.2 Task Context
- The prompt explicitly mentions the context of an **MSc project** and the domain (**Acoustic Emission Analysis**). This helps the model disambiguate domain-specific terms (e.g., "RMS", "Energy") and understand the scientific nature of the data processing.

### 2.3 Hard Constraints
- **Indexing**: Explicit instruction to recognize that Julia uses **1-based indexing**, similar to MATLAB. This prevents the common LLM error of converting to 0-based indexing unnecessarily.
- **Libraries**: Directing the use of `XLSX.jl` and `DataFrames.jl` for robust data handling, and `Plots.jl` (GR backend) for visualization.
- **Plotting**: Requirement to use `twinx()` within `Plots.jl` for dual-axis graphs, ensuring the left and right axes share the same x-axis scale correctly.
- **Performance**: Emphasis on wrapping code in functions to avoid global scope performance penalties.

### 2.4 Modularisation & Documentation
- Requirements for clean, modular code (using `main()` or specific processing functions) and brief explanatory comments for Julia-specific implementation choices (e.g., why `DataFrames` is preferred over raw matrices for mixed-type Excel data).

## 3. Test Case Selection: `CT07.m`
The script `CT07.m` was selected as the initial benchmark because it contains several critical transition points:
- **Excel Data Extraction**: Tests the transition from `xlsread` to `XLSX.jl`/`DataFrames.jl`.
- **Column Slicing**: Tests the model's understanding of 1-based indexing in both Matrix and DataFrame contexts.
- **Dual Y-Axis Figures**: Tests the complexity of recreating MATLAB's `yyaxis` in `Plots.jl`.
- **Multiple Plot Types**: Includes standard line plots, scatter plots, and cumulative metrics.

---
**Status**: This methodology will be applied to all subsequent translation experiments to maintain the validity of the comparison.
![[CT07.m]]![[Commercial Tensile Tests.xlsx]]

---

**Prompt:**

```text
Act as a Senior Scientific Computing Engineer and Julia Specialist. I am working on an MSc project migrating an Acoustic Emission (AE) analysis framework from MATLAB to Julia. 

Your task is to translate the following MATLAB script into idiomatic Julia. 

Requirements & Constraints:

1. Data Loading: Use `XLSX.jl` and `DataFrames.jl` to load the "Tensile-processed.xlsx" file. Ensure you read the specific sheet 'CT-07'.
2. Array Indexing: Note that Julia, like MATLAB, uses 1-based indexing. Ensure the column slicing matches the original MATLAB logic correctly (e.g., MATLAB's `data(:, 1)` should be handled appropriately in the context of a DataFrame or Matrix).
3. Broadcasting: Use Julia's broadcasting dot syntax (e.g., `sin.(x)`) for element-wise operations to ensure high performance.
4. Visualization: Use the `Plots.jl` library (with the GR backend). Replicate the dual-axis plots (`yyaxis left` and `yyaxis right`) using `twinx()`. Ensure titles, labels, and limits match the original script.
5. Readability: Keep the code modular. Wrap the logic in a main function or descriptive sub-functions. Add brief comments explaining the Julia-specific implementation choices.

Here is the original MATLAB code:

data = xlsread("Tensile-processed.xlsx", 'CT-07'); 
% Selection of specific data from the sheet to be used for plotting 
t1 = data(:, 1);
stress = data(:, 4);
strain = data(:, 3); 
time = data(:,5);
rms = data(:, 9);
cumrms = data(:, 10);
energy = data(:, 12);
cumenergy = data(:, 14);

fig1 = figure; % Strain vs Stress plot
plot(strain, stress, 'b')
ylabel('Stress (MPa)');
xlabel('Strain (%)');
ylim([0 520]);
title('T07 Strain vs. Stress');
grid('minor');

fig2 = figure; 
yyaxis left % Stress vs time plot
plot(t1, stress, 'b')
ylabel('Stress (MPa)');
xlabel('Time (s)');
ylim([0 max(stress)]);
xlim([0 250]);

yyaxis right % Normalised RMS scatter plot
plot(time, rms, 'r')
ylim([0 1.05]);
ylabel('Normalised RMS (a.u.)');
title('T09 Commercial Normalised RMS Profile');
grid('minor');

fig3 = figure;
yyaxis left % Stress vs time plot
plot(t1, stress, 'b')
ylabel('Stress (MPa)');
xlabel('Time (s)');
ylim([0 max(stress)]);
xlim([0 300]);

yyaxis right % Normalised cumulative RMS plot
plot(time, cumrms, 'r')
ylim([0 1.05]);
ylabel('Normalised Cumulative RMS (a.u.)');
title('T07 Commercial Normalised Cumulative RMS');
grid('minor');

fig4 = figure;
yyaxis left % Stress vs time plot
plot(t1, stress, 'b')
ylabel('Stress (MPa)');
xlabel('Time (s)');
ylim([0 max(stress)]);
xlim([0 300]);

yyaxis right % Normalised AE energy plot
scatter(time, energy, markersize=5, markerstrokewidth=0, color=:red)
ylabel('Normalised AE Energy (a.u.)');
ylim([0 1.05]);
title('T07 Commercial Normalised AE Energy');
grid('minor');

fig5 = figure;
yyaxis left % Stress vs time plot
plot(t1, stress, 'b')
ylabel('Stress (MPa)');
xlabel('Time (s)');
ylim([0 max(stress)]);
xlim([0 300]);

yyaxis right % Normalised cumulative AE energy plot
plot(time, cumenergy, 'r')
ylabel('Normalised Cumulative AE Energy (a.u.)');
ylim([0 1.05]);
title('T07 Commercial Normalised Cumulative AE Energy');
grid('minor');
```

---

**Judging Criteria (Grading Guide)**

Look for their "flaws" according to the following standards and record them in the comparative document:

1. **Check the indexing logic**: Since both Julia and MATLAB are 1-based, **the correct code should directly use column indices 1, 3, 4, 5, 9, 10, 12, 14**. If the model incorrectly converts it to 0-based (e.g., using `[:, 0]` or `[:, 2]`), **points will be deducted!** This indicates the model's confusion about the basic syntax of Julia.
2. **Regarding the XLSX library and DataFrame usage**: Did you use `XLSX.readtable` or `XLSX.gettable` correctly? A simple `XLSX.readxlsx` only provides a file handle and needs to be converted to a `DataFrame` or `Matrix` for easy slicing. Did you use `DataFrames.jl` correctly for column selection, for example `df[:, :col_name]` or `df[!, :col_name]`? If you manipulate the matrix directly while ignoring potential non-numeric headers in Excel, it may lead to type errors.
3. **Check Broadcast Operations (`.`)**: When Julia handles vectorized operations or plotting data, it's recommended to use `.`. For example, `plot(x, y)` is fine, but if there are mathematical operations in the middle (like normalization), check if it uses Julian-style code like `energy ./ maximum(energy)`.
4. **Check the management of plot objects**: Good code will use the `twinx()` feature of `Plots.jl`. In `Plots.jl`, the standard way to implement dual axes is: 
   ```julia 
   p = plot(t1, stress, ylabel="Stress", color=:blue) plot!(twinx(), time, rms, ylabel="RMS", color=:red) 
   ``` 
   Check if the model confuses the Python `twinx()` object method and the Julia plotting workflow. If it generates pseudo-code that cannot be run, it indicates a lack of understanding of the Julia plotting ecosystem. Pay attention to whether dual axes are created correctly in each `figure`. If the code attempts to use multiple `plot()` calls without sharing the x-axis, or forgets to set the ylabel after `twinx()`, it indicates a lack of understanding of the Julia plotting ecosystem.
5. **Modularity and Performance**: Julia is sensitive to global variables. If the code performs a lot of calculations directly in the top-level scope without being wrapped in a `function`, although it can run, it does not meet the "Senior Engineer" standard, **points will be deducted accordingly**.
