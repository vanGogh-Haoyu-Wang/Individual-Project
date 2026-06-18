# User Prompt

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
# Assistance Response
The user wants me to translate MATLAB code to Python. Let me create a clean, well-structured Python script.

Check frontend design skill for any relevant patterns

Done

Now let me write the Python translation directly — this is a pure code task, no skill needed.

Created a file, read a file

Created a file, read a file

Here's a breakdown of every translation decision made:

---
```python
"""
ae_analysis.py
==============
Python translation of the MATLAB Acoustic Emission (AE) analysis script.
Reads tensile-test data from an Excel workbook and produces five figures
that replicate the original MATLAB plots.

Dependencies
------------
    pip install pandas openpyxl matplotlib

Usage
-----
    python ae_analysis.py
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd


# ---------------------------------------------------------------------------
# 1. Data loading
# ---------------------------------------------------------------------------
# MATLAB : data = xlsread("Tensile-processed.xlsx", 'CT-07')
# Python  : pd.read_excel returns a DataFrame; header=0 assumes the first row
#           is a header row — set header=None if the sheet has no header and
#           adjust column indices accordingly.

EXCEL_FILE = "Tensile-processed.xlsx"
SHEET_NAME = "CT-07"

df = pd.read_excel(EXCEL_FILE, sheet_name=SHEET_NAME, header=0, engine="openpyxl")

# ---------------------------------------------------------------------------
# 2. Column extraction
# ---------------------------------------------------------------------------
# MATLAB uses 1-based column indices; Python DataFrames use 0-based iloc.
#
#   MATLAB col 1  → Python iloc[:, 0]   → t1       (time axis for stress plot)
#   MATLAB col 3  → Python iloc[:, 2]   → strain
#   MATLAB col 4  → Python iloc[:, 3]   → stress
#   MATLAB col 5  → Python iloc[:, 4]   → time     (AE time axis)
#   MATLAB col 9  → Python iloc[:, 8]   → rms
#   MATLAB col 10 → Python iloc[:, 9]   → cumrms
#   MATLAB col 12 → Python iloc[:, 11]  → energy
#   MATLAB col 14 → Python iloc[:, 13]  → cumenergy

t1       = df.iloc[:, 0]   # time axis shared with stress (col 1)
strain   = df.iloc[:, 2]   # strain             (col 3)
stress   = df.iloc[:, 3]   # stress / MPa       (col 4)
time     = df.iloc[:, 4]   # AE event time      (col 5)
rms      = df.iloc[:, 8]   # normalised RMS     (col 9)
cumrms   = df.iloc[:, 9]   # cumulative RMS     (col 10)
energy   = df.iloc[:, 11]  # normalised energy  (col 12)
cumenergy = df.iloc[:, 13] # cumulative energy  (col 14)

stress_max = stress.max()  # computed once; used in ylim across several figures


# ---------------------------------------------------------------------------
# Helper: apply minor grid to both axes of a figure
# ---------------------------------------------------------------------------

def apply_minor_grid(ax):
    """Enable MATLAB-style minor grid on a given Axes object."""
    ax.minorticks_on()
    ax.grid(which="major", linestyle="-",  linewidth=0.6, alpha=0.7)
    ax.grid(which="minor", linestyle=":",  linewidth=0.4, alpha=0.5)


# ---------------------------------------------------------------------------
# Figure 1 – Strain vs Stress
# ---------------------------------------------------------------------------
# MATLAB: plot(strain, stress, 'b') on a single-axis figure.

fig1, ax1 = plt.subplots(figsize=(7, 5))

ax1.plot(strain, stress, color="blue", linewidth=1.2)
ax1.set_xlabel("Strain (%)")
ax1.set_ylabel("Stress (MPa)")
ax1.set_ylim(0, 520)
ax1.set_title("T07 Strain vs. Stress")
apply_minor_grid(ax1)

fig1.tight_layout()


# ---------------------------------------------------------------------------
# Figure 2 – Stress (left) + Normalised RMS (right) vs Time
# ---------------------------------------------------------------------------
# MATLAB: yyaxis left / yyaxis right → Python: ax.twinx() to share the x-axis
# while maintaining independent y-axes with their own colours and tick labels.

fig2, ax2l = plt.subplots(figsize=(8, 5))
ax2r = ax2l.twinx()  # right-hand y-axis sharing the same x-axis

# Left axis – stress
ax2l.plot(t1, stress, color="blue", linewidth=1.2, label="Stress")
ax2l.set_xlabel("Time (s)")
ax2l.set_ylabel("Stress (MPa)", color="blue")
ax2l.set_ylim(0, stress_max)
ax2l.set_xlim(0, 250)
ax2l.tick_params(axis="y", labelcolor="blue")

# Right axis – normalised RMS
ax2r.plot(time, rms, color="red", linewidth=1.0, label="Norm. RMS")
ax2r.set_ylabel("Normalised RMS (a.u.)", color="red")
ax2r.set_ylim(0, 1.05)
ax2r.tick_params(axis="y", labelcolor="red")

ax2l.set_title("T09 Commercial Normalised RMS Profile")

# Apply minor grid only to the primary (left) axes to avoid double grid artefacts
apply_minor_grid(ax2l)

fig2.tight_layout()


# ---------------------------------------------------------------------------
# Figure 3 – Stress (left) + Normalised Cumulative RMS (right) vs Time
# ---------------------------------------------------------------------------

fig3, ax3l = plt.subplots(figsize=(8, 5))
ax3r = ax3l.twinx()

ax3l.plot(t1, stress, color="blue", linewidth=1.2)
ax3l.set_xlabel("Time (s)")
ax3l.set_ylabel("Stress (MPa)", color="blue")
ax3l.set_ylim(0, stress_max)
ax3l.set_xlim(0, 300)
ax3l.tick_params(axis="y", labelcolor="blue")

ax3r.plot(time, cumrms, color="red", linewidth=1.0)
ax3r.set_ylabel("Normalised Cumulative RMS (a.u.)", color="red")
ax3r.set_ylim(0, 1.05)
ax3r.tick_params(axis="y", labelcolor="red")

ax3l.set_title("T07 Commercial Normalised Cumulative RMS")
apply_minor_grid(ax3l)

fig3.tight_layout()


# ---------------------------------------------------------------------------
# Figure 4 – Stress (left) + Normalised AE Energy scatter (right) vs Time
# ---------------------------------------------------------------------------
# MATLAB: scatter(time, energy, 5, 'filled', 'r')
# Python : ax.scatter with s=5 (marker area in points²), marker='o' (filled by default)

fig4, ax4l = plt.subplots(figsize=(8, 5))
ax4r = ax4l.twinx()

ax4l.plot(t1, stress, color="blue", linewidth=1.2)
ax4l.set_xlabel("Time (s)")
ax4l.set_ylabel("Stress (MPa)", color="blue")
ax4l.set_ylim(0, stress_max)
ax4l.set_xlim(0, 300)
ax4l.tick_params(axis="y", labelcolor="blue")

# s=5 replicates the MATLAB marker size; zorder ensures dots render above the grid
ax4r.scatter(time, energy, s=5, color="red", marker="o", zorder=3, label="AE Energy")
ax4r.set_ylabel("Normalised AE Energy (a.u.)", color="red")
ax4r.set_ylim(0, 1.05)
ax4r.tick_params(axis="y", labelcolor="red")

ax4l.set_title("T07 Commercial Normalised AE Energy")
apply_minor_grid(ax4l)

fig4.tight_layout()


# ---------------------------------------------------------------------------
# Figure 5 – Stress (left) + Normalised Cumulative AE Energy (right) vs Time
# ---------------------------------------------------------------------------

fig5, ax5l = plt.subplots(figsize=(8, 5))
ax5r = ax5l.twinx()

ax5l.plot(t1, stress, color="blue", linewidth=1.2)
ax5l.set_xlabel("Time (s)")
ax5l.set_ylabel("Stress (MPa)", color="blue")
ax5l.set_ylim(0, stress_max)
ax5l.set_xlim(0, 300)
ax5l.tick_params(axis="y", labelcolor="blue")

ax5r.plot(time, cumenergy, color="red", linewidth=1.0)
ax5r.set_ylabel("Normalised Cumulative AE Energy (a.u.)", color="red")
ax5r.set_ylim(0, 1.05)
ax5r.tick_params(axis="y", labelcolor="red")

ax5l.set_title("T07 Commercial Normalised Cumulative AE Energy")
apply_minor_grid(ax5l)

fig5.tight_layout()


# ---------------------------------------------------------------------------
# Render all figures
# ---------------------------------------------------------------------------
# plt.show() renders every figure created above in a single call.
# For non-interactive / batch use, replace with fig1.savefig("fig1.png"), etc.

plt.show()
```
#### Key MATLAB → Python mappings

|Concern|MATLAB|Python|
|---|---|---|
|**Data loading**|`xlsread(file, sheet)`|`pd.read_excel(..., engine="openpyxl")` — returns a DataFrame; requires `openpyxl` for `.xlsx`|
|**Column indexing**|1-based: `data(:, 4)`|0-based: `df.iloc[:, 3]` — every index is shifted by −1|
|**Dual y-axes**|`yyaxis left` / `yyaxis right`|`ax_left, ax_right = plt.subplots(); ax_right = ax_left.twinx()` — the OO approach gives full independent control of each axis|
|**Axis colour pairing**|MATLAB auto-colours both axis spines|Explicit `ax.tick_params(axis="y", labelcolor=...)` + coloured `ylabel` strings replicate this|
|**Scatter plot**|`scatter(x, y, 5, 'filled', 'r')`|`ax.scatter(x, y, s=5, color="red", marker="o")` — `s` is marker area in points², `marker="o"` is filled by default|
|**Minor grid**|`grid('minor')`|`ax.minorticks_on()` + `ax.grid(which="minor", ...)` — wrapped in a reusable `apply_minor_grid()` helper to keep things DRY|
|**`max(stress)`**|Evaluated inline in `ylim`|Computed once as `stress_max` before the plotting block and reused across all figures|

#### One note on `fig2`'s title

The MATLAB source says `'T09 Commercial ...'` for `fig2` but `'T07 ...'` for all others — the translation preserves that exactly as written, in case it's intentional in your dataset.
