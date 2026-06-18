# Overview of Initial Prompting Methodology

## 1. Objectives of Prompt Engineering
The primary goal of the prompting strategy is to ensure a high-fidelity translation of MATLAB scientific code to Python, adhering to the principle of **functional equivalence**. The strategy focuses on:
- Minimising human intervention during the initial translation phase.
- Ensuring correct handling of 1-based to 0-based indexing.
- Implementing idiomatic Python (e.g., NumPy vectorisation) rather than literal line-by-line translation.

## 2. Structured Prompt Design
To ensure consistency across different LLM platforms (ChatGPT, Claude, DeepSeek, Llama), a standardized prompt structure is employed. This structure consists of four key components:

### 2.1 Persona Selection (Role Setting)
- **Role**: Senior Scientific Computing Engineer.
- **Rationale**: Setting this persona encourages the model to prioritise performance (NumPy), type safety, and adherence to scientific coding standards (PEP-8).

### 2.2 Task Context
- The prompt explicitly mentions the context of an **MSc project** and the domain (**Acoustic Emission Analysis**). This helps the model disambiguate domain-specific terms (e.g., "RMS", "Energy").

### 2.3 Hard Constraints
- **Indexing**: Explicit instruction to handle the MATLAB 1-based indexing shift.
- **Libraries**: Directing the use of `pandas` for data loading and `matplotlib` for visualization.
- **Plotting**: Requirement to use object-oriented plotting (`twinx()`) for dual-axis graphs.

### 2.4 Modularisation & Documentation
- Requirements for clean, modular code and brief explanatory comments for implementation choices.

## 3. Test Case Selection: `CT07.m`
The script `CT07.m` was selected as the initial benchmark because it contains several critical transition points:
- **Excel Data Extraction**: Tests the transition from `xlsread` to `pandas`.
- **Column Slicing**: Tests the model's awareness of 0-based indexing.
- **Dual Y-Axis Figures**: Tests the complexity of recreating MATLAB's `yyaxis` in Matplotlib.
- **Multiple Plot Types**: Includes standard line plots and scatter plots.

---
**Status**: This methodology will be applied to all subsequent translation experiments to maintain the validity of the comparison.
![[CT07.m]]![[Commercial Tensile Tests.xlsx]]

---
 Prompt：
```text
Act as a Senior Scientific Computing Engineer. I am working on an MSc project migrating an Acoustic Emission (AE) analysis framework from MATLAB to an open-source Python environment. 

Your task is to translate the following MATLAB script into Python. 

Requirements & Constraints:

1. Data Loading: Replace MATLAB's `xlsread` with an appropriate Python library (e.g., `pandas`).
2. Array Indexing: Pay strict attention to the 1-based to 0-based indexing conversion between MATLAB and Python. Ensure data slicing is correct.
3. Visualization: Use `matplotlib` (and/or `seaborn`) to replicate the exact plots. Handle MATLAB's `yyaxis left` and `yyaxis right` elegantly using Python's object-oriented plotting approach (e.g., `twinx()`).
4. Readability: Keep the code clean, modular, and PEP-8 compliant. Add brief comments explaining the Python-specific implementation choices.

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
scatter(time, energy, 5, 'filled', 'r')
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
1. **Indexing Accuracy**: 
* **Core Indicator**: MATLAB is 1-based, Python is 0-based. 
* **Correct Examples**: `data(:, 1)` (1st column) should be converted to `data.iloc[:, 0]` or `data_arr[:, 0]`.*
* **Incorrect Example**: Still using `data.iloc[:, 1]` (this will incorrectly get the 2nd column). 
2. **Pandas Data Loading Best Practices**: 
* **Core Indicator**: Did you handle the Excel header? 
* **Correct Approach**: Use `header=None` or explicitly skip the header to prevent reading column names (strings) as data, which can cause errors in `pd.to_numeric` or misaligned data. 
* **Incorrect Approach**: Directly reading without handling the header, leading to the first row of data being shifted or having incorrect types. 
3. **Proficiency in Plotting APIs**: 
* **Core Indicators**: Whether an object-oriented (OO) interface is used? Is the dual Y-axis (`yyaxis`) correctly bound to the same X-axis using `twinx()`? 
* **Correct Example**: ```python fig, ax1 = plt.subplots() ax2 = ax1.twinx() ax1.plot(...) ax2.plot(...) ``` 
* **Incorrect Practices**: Mixing global state machines with `plt.plot`, or failing to correctly associate the X-axis range after `twinx()`, causing misalignment in dual-axis plots.
4. **Modularity & Readability**: 
* **Core indicators**: Is the repetitive dual-axis plotting logic encapsulated as a function? Does it follow PEP-8?