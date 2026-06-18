# User:

Act as a Senior Scientific Computing Engineer. I am working on an MSc project migrating an Acoustic Emission (AE) analysis framework from MATLAB to an open-source Python environment. Your task is to translate the following MATLAB script into Python. Requirements & Constraints:

1. Data Loading: Replace MATLAB's `xlsread` with an appropriate Python library (e.g., `pandas`).
2. Array Indexing: Pay strict attention to the 1-based to 0-based indexing conversion between MATLAB and Python. Ensure data slicing is correct.
3. Visualization: Use `matplotlib` (and/or `seaborn`) to replicate the exact plots. Handle MATLAB's `yyaxis left` and `yyaxis right` elegantly using Python's object-oriented plotting approach (e.g., `twinx()`).
4. Readability: Keep the code clean, modular, and PEP-8 compliant. Add brief comments explaining the Python-specific implementation choices. Here is the original MATLAB code:

```matlab
data = xlsread("Commercial Tensile Tests", 'CT07'); 
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
# Assisstant:
This is a pure Python/scientific translation task — no document skill needed. Let me write the translation directly.Here's a full breakdown of every translation decision made:

## MATLAB → Python Translation Notes

### 1. Data Loading

|MATLAB|Python|
|---|---|
|`xlsread("file", 'sheet')`|`pd.read_excel("file.xlsx", sheet_name="CT07", header=0)`|

`xlsread` silently discards text rows and returns only numeric data. The `header=0` in pandas mirrors this by treating row 1 as column names. **If your sheet has no header row at all**, change it to `header=None`.

### 2. Column Indexing (Critical)

MATLAB is **1-based**; Python `.iloc` is **0-based**. Every column index is decremented by 1:

|Variable|MATLAB col|`.iloc` index|
|---|---|---|
|`t1`|1|`0`|
|`strain`|3|`2`|
|`stress`|4|`3`|
|`time`|5|`4`|
|`rms`|9|`8`|
|`cumrms`|10|`9`|
|`energy`|12|`11`|
|`cumenergy`|14|`13`|

### 3. Dual Y-Axis (`yyaxis` → `twinx`)

```python
# MATLAB               │  Python
# yyaxis left          │  ax_left  = plt.subplots()[1]  (the primary axes)
# yyaxis right         │  ax_right = ax_left.twinx()
```

The left and right axis spines, ticks, and labels are coloured blue/red respectively to preserve MATLAB's visual convention.

### 4. Minor Grid

`grid('minor')` is replicated with:

```python
ax.minorticks_on()
ax.grid(which="major", ...)
ax.grid(which="minor", ...)
```

Applied only to the **left** axis — the `twinx()` right axes is transparent by default, so the grid shows through both datasets correctly.

### 5. Scatter Plot

|MATLAB|Python|
|---|---|
|`scatter(time, energy, 5, 'filled', 'r')`|`ax.scatter(time, energy, s=5, color="red", marker="o", alpha=0.7)`|

The 5th MATLAB argument is marker area in pt² — directly maps to `s=5`. Matplotlib scatter markers are solid-filled by default, so no extra keyword is needed. `alpha=0.7` is added to handle overplotting common in dense AE datasets.

### 6. One Preserved Quirk

The original MATLAB code labels **Fig 2** as `'T09 Commercial...'` while loading sheet `CT07`. This looks like a copy-paste error in the original — it's preserved here exactly as written, with a comment flagging it.
### 7. python code
```python
"""
ae_analysis.py
==============
Python translation of the MATLAB Acoustic Emission (AE) analysis script.

Key translation decisions:
  - xlsread()        →  pandas.read_excel()  (preserves dtypes, handles headers)
  - MATLAB 1-based   →  Python 0-based column indexing via .iloc
  - yyaxis left/right →  matplotlib twinx() with colour-coded spines/ticks
  - grid('minor')    →  ax.minorticks_on() + ax.grid(which='both')
  - scatter(…,5,…)   →  ax.scatter(…, s=5) where s is marker area in pt²

Dependencies:  pandas, openpyxl, matplotlib
Install via:   pip install pandas openpyxl matplotlib
"""

import pandas as pd
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------------
# 1. Data Loading
# ---------------------------------------------------------------------------
# MATLAB's xlsread() silently skips text rows and returns numeric data only.
# pandas read_excel() keeps the full sheet.
#   • header=0  →  treat the first row as column names  (most common case)
#   • header=None →  use if the sheet has NO header row (all rows are data)
# Adjust the file extension to match your actual file (.xlsx / .xls).
EXCEL_FILE = "Commercial Tensile Tests.xlsx"
SHEET_NAME = "CT07"

df = pd.read_excel(EXCEL_FILE, sheet_name=SHEET_NAME, header=0)


# ---------------------------------------------------------------------------
# 2. Column Extraction  (MATLAB 1-based → Python 0-based via .iloc)
# ---------------------------------------------------------------------------
#  MATLAB col  │  .iloc index  │  Variable    │  Description
#  ──────────────────────────────────────────────────────────
#      1        │      0        │  t1          │  Mechanical time axis
#      3        │      2        │  strain      │  Strain (%)
#      4        │      3        │  stress      │  Stress (MPa)
#      5        │      4        │  time        │  AE time axis
#      9        │      8        │  rms         │  Normalised RMS
#     10        │      9        │  cumrms      │  Normalised Cumulative RMS
#     12        │     11        │  energy      │  Normalised AE Energy
#     14        │     13        │  cumenergy   │  Normalised Cumulative AE Energy
t1        = df.iloc[:, 0]
strain    = df.iloc[:, 2]
stress    = df.iloc[:, 3]
time      = df.iloc[:, 4]
rms       = df.iloc[:, 8]
cumrms    = df.iloc[:, 9]
energy    = df.iloc[:, 11]
cumenergy = df.iloc[:, 13]


# ---------------------------------------------------------------------------
# 3. Reusable Helper Functions
# ---------------------------------------------------------------------------

def apply_minor_grid(ax: plt.Axes) -> None:
    """
    Replicate MATLAB's grid('minor'): enable both major and minor grid lines.
    Applied to the *primary* (left) axis only; the twinx right axis is
    transparent by default, so the same grid is visible behind both datasets.
    """
    ax.minorticks_on()
    ax.grid(which="major", linestyle="-",  linewidth=0.6, alpha=0.7, zorder=0)
    ax.grid(which="minor", linestyle=":",  linewidth=0.4, alpha=0.5, zorder=0)


def plot_stress_left(
    ax: plt.Axes,
    t1_data: pd.Series,
    stress_data: pd.Series,
    xlim: float,
) -> None:
    """
    Draw the stress-vs-time curve on the left y-axis (blue).

    Colours the spine, label, and ticks blue to mirror MATLAB's
    yyaxis left visual convention.

    Parameters
    ----------
    ax          : primary (left) matplotlib Axes
    t1_data     : mechanical time series
    stress_data : stress series (MPa)
    xlim        : upper x-axis limit (seconds)
    """
    ax.plot(t1_data, stress_data, color="blue", linewidth=1.2)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Stress (MPa)", color="blue")
    ax.set_ylim(0, stress_data.max())
    ax.set_xlim(0, xlim)
    # Colour axis elements blue to match MATLAB's yyaxis left behaviour
    ax.tick_params(axis="y", colors="blue")
    ax.spines["left"].set_color("blue")


def style_right_axis(ax: plt.Axes, ylabel: str, color: str = "red") -> None:
    """
    Apply shared styling to the right y-axis created by twinx().

    All normalised AE quantities share the [0, 1.05] y-range.
    Colours the spine, label, and ticks red to mirror MATLAB's
    yyaxis right visual convention.

    Parameters
    ----------
    ax     : secondary (right) matplotlib Axes from twinx()
    ylabel : y-axis label string
    color  : axis / label colour (default 'red')
    """
    ax.set_ylabel(ylabel, color=color)
    ax.set_ylim(0, 1.05)
    ax.tick_params(axis="y", colors=color)
    ax.spines["right"].set_color(color)


# ---------------------------------------------------------------------------
# 4. Figure 1 – Strain vs Stress
# ---------------------------------------------------------------------------
fig1, ax1 = plt.subplots(figsize=(7, 5))

ax1.plot(strain, stress, color="blue", linewidth=1.2)
ax1.set_xlabel("Strain (%)")
ax1.set_ylabel("Stress (MPa)")
ax1.set_ylim(0, 520)
ax1.set_title("T07 Strain vs. Stress")
apply_minor_grid(ax1)

fig1.tight_layout()


# ---------------------------------------------------------------------------
# 5. Figure 2 – Stress (left) + Normalised RMS (right) vs Time
#
#    NOTE: The title 'T09' in the original MATLAB script appears to be a
#    copy-paste inconsistency (the sheet is CT07). Preserved here as-is.
# ---------------------------------------------------------------------------
fig2, ax2l = plt.subplots(figsize=(8, 5))
plot_stress_left(ax2l, t1, stress, xlim=250)

# twinx() creates a new Axes sharing the same x-axis → yyaxis right equivalent
ax2r = ax2l.twinx()
ax2r.plot(time, rms, color="red", linewidth=1.0)
style_right_axis(ax2r, ylabel="Normalised RMS (a.u.)")

ax2l.set_title("T09 Commercial Normalised RMS Profile")
apply_minor_grid(ax2l)

fig2.tight_layout()


# ---------------------------------------------------------------------------
# 6. Figure 3 – Stress (left) + Normalised Cumulative RMS (right) vs Time
# ---------------------------------------------------------------------------
fig3, ax3l = plt.subplots(figsize=(8, 5))
plot_stress_left(ax3l, t1, stress, xlim=300)

ax3r = ax3l.twinx()
ax3r.plot(time, cumrms, color="red", linewidth=1.0)
style_right_axis(ax3r, ylabel="Normalised Cumulative RMS (a.u.)")

ax3l.set_title("T07 Commercial Normalised Cumulative RMS")
apply_minor_grid(ax3l)

fig3.tight_layout()


# ---------------------------------------------------------------------------
# 7. Figure 4 – Stress (left) + Normalised AE Energy scatter (right) vs Time
#
#    MATLAB: scatter(time, energy, 5, 'filled', 'r')
#    Python:  ax.scatter(time, energy, s=5, color='red')
#      • s=5  → marker area in points² (matches MATLAB's size argument)
#      • matplotlib scatter markers are filled by default (no extra kwarg needed)
#      • alpha=0.7 improves readability for dense AE datasets
# ---------------------------------------------------------------------------
fig4, ax4l = plt.subplots(figsize=(8, 5))
plot_stress_left(ax4l, t1, stress, xlim=300)

ax4r = ax4l.twinx()
ax4r.scatter(
    time, energy,
    s=5,
    color="red",
    marker="o",
    alpha=0.7,
)
style_right_axis(ax4r, ylabel="Normalised AE Energy (a.u.)")

ax4l.set_title("T07 Commercial Normalised AE Energy")
apply_minor_grid(ax4l)

fig4.tight_layout()


# ---------------------------------------------------------------------------
# 8. Figure 5 – Stress (left) + Normalised Cumulative AE Energy (right) vs Time
# ---------------------------------------------------------------------------
fig5, ax5l = plt.subplots(figsize=(8, 5))
plot_stress_left(ax5l, t1, stress, xlim=300)

ax5r = ax5l.twinx()
ax5r.plot(time, cumenergy, color="red", linewidth=1.0)
style_right_axis(ax5r, ylabel="Normalised Cumulative AE Energy (a.u.)")

ax5l.set_title("T07 Commercial Normalised Cumulative AE Energy")
apply_minor_grid(ax5l)

fig5.tight_layout()


# ---------------------------------------------------------------------------
# 9. Render all figures
# ---------------------------------------------------------------------------
# Call plt.show() once at the end; matplotlib renders all open figures together.
# In a Jupyter notebook, individual figures appear inline automatically and
# this call can be omitted.
plt.show()
```
---
# Debug


---
# Results
Figure 1  
  
Figure 2  
  
Figure 3  
  
Figure 4  
  
Figure 5  

  
---
# Evaluation:

  
---
# Summary