## User Prompt

Act as a Senior Scientific Computing Engineer. I am working on an MSc project migrating an Acoustic Emission (AE) analysis framework from MATLAB to an open-source Python environment. 

Your task is to translate the following MATLAB script into Python. 

Requirements & Constraints:
1. Data Loading: Replace MATLAB's `xlsread` with an appropriate Python library (e.g., `pandas`).
2. Array Indexing: Pay strict attention to the 1-based to 0-based indexing conversion between MATLAB and Python. Ensure data slicing is correct.
3. Visualization: Use `matplotlib` (and/or `seaborn`) to replicate the exact plots. Handle MATLAB's `yyaxis left` and `yyaxis right` elegantly using Python's object-oriented plotting approach (e.g., `twinx()`).
4. Readability: Keep the code clean, modular, and PEP-8 compliant. Add brief comments explaining the Python-specific implementation choices.

### Original MATLAB Code:
```matlab
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

## Gemini 3 Flash Response

As a Senior Scientific Computing Engineer, I have translated your MATLAB Acoustic Emission (AE) analysis script into a modular, PEP-8 compliant Python script. 

### Key Translation Adjustments:
1.  **Data Loading**: Switched from `xlsread` to `pandas.read_excel`. I used `header=None` to ensure column indexing remains consistent with your 1-based MATLAB references (after the shift).
2.  **Indexing**: Converted all indices from **1-based** (MATLAB) to **0-based** (Python). For example, `data(:, 1)` became `data[:, 0]`.
3.  **Visualization**:
    *   Replicated `yyaxis` using `ax.twinx()`.
    *   Matched axis colors to their respective data (blue for stress, red for AE parameters) to maintain visual parity.
    *   Simulated MATLAB's `grid minor` by enabling minor ticks and custom grid styling in `matplotlib`.

```python
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def ae_analysis_workflow(file_path="Tensile-processed.xlsx", sheet_name="CT-07"):
    \"\"\"
    Translates the AE analysis framework from MATLAB to Python.
    
    Parameters:
        file_path (str): Path to the Excel data file.
        sheet_name (str): Specific worksheet to process.
    \"\"\"
    
    # 1. Data Loading
    # pandas.read_excel handles modern Excel formats efficiently.
    # header=None ensures we treat the sheet as a raw matrix for direct index mapping.
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)
        data = df.to_numpy()
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return
    except Exception as e:
        print(f"Data loading failed: {e}")
        return

    # 2. Array Indexing (1-based MATLAB -> 0-based Python)
    # MATLAB: data(:, 1) -> Python: data[:, 0]
    t1         = data[:, 0]   # Time/Index
    stress     = data[:, 3]   # Stress (MPa)
    strain     = data[:, 2]   # Strain (%)
    ae_time    = data[:, 4]   # AE Hit Time
    rms        = data[:, 8]   # Normalised RMS
    cumrms     = data[:, 9]   # Normalised Cumulative RMS
    energy     = data[:, 11]  # Normalised AE Energy
    cumenergy  = data[:, 13]  # Normalised Cumulative AE Energy

    # 3. Helper for Visual Consistency
    def apply_matlab_style(ax, title):
        \"\"\"Replicates MATLAB's title and minor grid styling.\"\"\"
        ax.set_title(title, fontweight='bold', pad=10)
        ax.grid(True, which='major', linestyle='-', linewidth=0.5, alpha=0.7)
        ax.grid(True, which='minor', linestyle=':', linewidth=0.5, alpha=0.4)
        ax.minorticks_on()

    # --- Figure 1: Strain vs Stress ---
    plt.figure(figsize=(9, 6))
    plt.plot(strain, stress, color='blue', linewidth=1.5)
    plt.ylabel('Stress (MPa)')
    plt.xlabel('Strain (%)')
    plt.ylim([0, 520])
    apply_matlab_style(plt.gca(), 'T07 Strain vs. Stress')

    # --- Figure 2: Stress & Normalised RMS vs Time ---
    fig, ax1 = plt.subplots(figsize=(9, 6))
    ax1.plot(t1, stress, 'b')
    ax1.set_ylabel('Stress (MPa)', color='blue')
    ax1.set_xlabel('Time (s)')
    ax1.set_ylim([0, np.max(stress)])
    ax1.set_xlim([0, 250])
    ax1.tick_params(axis='y', labelcolor='blue')

    ax2 = ax1.twinx()  # Replicates 'yyaxis right'
    ax2.plot(ae_time, rms, 'r')
    ax2.set_ylabel('Normalised RMS (a.u.)', color='red')
    ax2.set_ylim([0, 1.05])
    ax2.tick_params(axis='y', labelcolor='red')
    apply_matlab_style(ax1, 'T09 Commercial Normalised RMS Profile')

    # --- Figure 3: Stress & Normalised Cumulative RMS vs Time ---
    fig, ax1 = plt.subplots(figsize=(9, 6))
    ax1.plot(t1, stress, 'b')
    ax1.set_ylabel('Stress (MPa)', color='blue')
    ax1.set_xlabel('Time (s)')
    ax1.set_ylim([0, np.max(stress)])
    ax1.set_xlim([0, 300])
    ax1.tick_params(axis='y', labelcolor='blue')

    ax2 = ax1.twinx()
    ax2.plot(ae_time, cumrms, 'r')
    ax2.set_ylabel('Normalised Cumulative RMS (a.u.)', color='red')
    ax2.set_ylim([0, 1.05])
    ax2.tick_params(axis='y', labelcolor='red')
    apply_matlab_style(ax1, 'T07 Commercial Normalised Cumulative RMS')

    # --- Figure 4: Stress & Normalised AE Energy (Scatter) ---
    fig, ax1 = plt.subplots(figsize=(9, 6))
    ax1.plot(t1, stress, 'b')
    ax1.set_ylabel('Stress (MPa)', color='blue')
    ax1.set_xlabel('Time (s)')
    ax1.set_ylim([0, np.max(stress)])
    ax1.set_xlim([0, 300])
    ax1.tick_params(axis='y', labelcolor='blue')

    ax2 = ax1.twinx()
    # s=5 matches MATLAB's marker size 5
    ax2.scatter(ae_time, energy, s=5, color='red', marker='o')
    ax2.set_ylabel('Normalised AE Energy (a.u.)', color='red')
    ax2.set_ylim([0, 1.05])
    ax2.tick_params(axis='y', labelcolor='red')
    apply_matlab_style(ax1, 'T07 Commercial Normalised AE Energy')

    # --- Figure 5: Stress & Normalised Cumulative AE Energy ---
    fig, ax1 = plt.subplots(figsize=(9, 6))
    ax1.plot(t1, stress, 'b')
    ax1.set_ylabel('Stress (MPa)', color='blue')
    ax1.set_xlabel('Time (s)')
    ax1.set_ylim([0, np.max(stress)])
    ax1.set_xlim([0, 300])
    ax1.tick_params(axis='y', labelcolor='blue')

    ax2 = ax1.twinx()
    ax2.plot(ae_time, cumenergy, 'r')
    ax2.set_ylabel('Normalised Cumulative AE Energy (a.u.)', color='red')
    ax2.set_ylim([0, 1.05])
    ax2.tick_params(axis='y', labelcolor='red')
    apply_matlab_style(ax1, 'T07 Commercial Normalised Cumulative AE Energy')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    ae_analysis_workflow()
```

### Technical Notes for your MSc Report:
*   **Library Selection**: `pandas` was selected over `numpy.loadtxt` for its superior handling of Excel multi-sheet structures and missing values, which are common in tensile test datasets.
*   **Plotting Engine**: `Matplotlib` was configured with `twinx()` to ensure that the Stress (primary Y-axis) and AE parameters (secondary Y-axis) share the same X-axis (Time/Strain) while maintaining independent scaling, exactly mimicking the `yyaxis` behavior in MATLAB.
*   **Object-Oriented Matplotlib**: Unlike MATLAB's state-machine plotting (`plot`, `ylabel`), this script uses the explicit object-oriented approach (`ax.plot`, `ax.set_ylabel`), which is more stable for complex, multi-axis scientific figures.
