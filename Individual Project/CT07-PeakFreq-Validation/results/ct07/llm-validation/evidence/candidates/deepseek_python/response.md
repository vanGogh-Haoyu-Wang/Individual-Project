```python
"""
Acoustic Emission (AE) Analysis — MATLAB-to-Python Migration
============================================================
Original MATLAB script: plots stress–strain, normalised RMS, cumulative RMS,
AE energy, and cumulative AE energy for a commercial tensile test dataset.

Python implementation notes:
  - pandas replaces xlsread for Excel I/O
  - matplotlib OOP API + twinx() replaces yyaxis left/right
  - All indexing is 0-based (MATLAB columns 1,3,4,5,9,10,12,14 → Python 0,2,3,4,8,9,11,13)
"""

import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# 1. Data loading
# ---------------------------------------------------------------------------
# MATLAB: data = xlsread("Commercial Tensile Tests", 'CT07');
# Python: use pandas.read_excel; returns a DataFrame (2-D labelled array)
FILE_PATH = "Commercial Tensile Tests.xlsx"          # adjust extension as needed
SHEET    = "CT07"

df = pd.read_excel(FILE_PATH, sheet_name=SHEET, header=None)

# Convert to numpy array for parity with the original script.
# If the file has a header row, set header=0 and use column names instead.
data = df.values

# ---------------------------------------------------------------------------
# 2. Column selection  (MATLAB 1-based → Python 0-based)
# ---------------------------------------------------------------------------
# t1 = data(:, 1)   → col 0
# stress = data(:,4) → col 3
# strain = data(:,3) → col 2
# time = data(:,5)   → col 4
# rms = data(:,9)    → col 8
# cumrms = data(:,10)→ col 9
# energy = data(:,12)→ col 11
# cumenergy = data(:,14)→ col 13
t1        = data[:, 0]
strain    = data[:, 2]
stress    = data[:, 3]
time      = data[:, 4]
rms       = data[:, 8]
cumrms    = data[:, 9]
energy    = data[:, 11]
cumenergy = data[:, 13]

# ---------------------------------------------------------------------------
# 3. Plotting
# ---------------------------------------------------------------------------
# Global style: match MATLAB's default minor-grid look
plt.rcParams["axes.grid"]       = True
plt.rcParams["axes.grid.which"] = "both"
plt.rcParams["grid.alpha"]      = 0.4

# --- Figure 1: Strain vs. Stress -------------------------------------------
fig1, ax1 = plt.subplots()
ax1.plot(strain, stress, "b")
ax1.set_ylabel("Stress (MPa)")
ax1.set_xlabel("Strain (%)")
ax1.set_ylim(0, 520)
ax1.set_title("T07 Strain vs. Stress")
ax1.grid(which="minor", alpha=0.3)          # minor grid, as in MATLAB

# --- Figure 2: Stress + Normalised RMS (scatter) ----------------------------
fig2, ax2_left = plt.subplots()

# Left y-axis — Stress vs t1
ax2_left.plot(t1, stress, "b")
ax2_left.set_ylabel("Stress (MPa)")
ax2_left.set_xlabel("Time (s)")
ax2_left.set_ylim(0, stress.max())
ax2_left.set_xlim(0, 250)

# Right y-axis — Normalised RMS scatter
ax2_right = ax2_left.twinx()                # replaces MATLAB yyaxis right
ax2_right.plot(time, rms, "r")
ax2_right.set_ylabel("Normalised RMS (a.u.)")
ax2_right.set_ylim(0, 1.05)

ax2_left.set_title("T09 Commercial Normalised RMS Profile")
ax2_left.grid(which="minor", alpha=0.3)

# --- Figure 3: Stress + Normalised Cumulative RMS --------------------------
fig3, ax3_left = plt.subplots()

ax3_left.plot(t1, stress, "b")
ax3_left.set_ylabel("Stress (MPa)")
ax3_left.set_xlabel("Time (s)")
ax3_left.set_ylim(0, stress.max())
ax3_left.set_xlim(0, 300)

ax3_right = ax3_left.twinx()
ax3_right.plot(time, cumrms, "r")
ax3_right.set_ylabel("Normalised Cumulative RMS (a.u.)")
ax3_right.set_ylim(0, 1.05)

ax3_left.set_title("T07 Commercial Normalised Cumulative RMS")
ax3_left.grid(which="minor", alpha=0.3)

# --- Figure 4: Stress + Normalised AE Energy (scatter) ---------------------
fig4, ax4_left = plt.subplots()

ax4_left.plot(t1, stress, "b")
ax4_left.set_ylabel("Stress (MPa)")
ax4_left.set_xlabel("Time (s)")
ax4_left.set_ylim(0, stress.max())
ax4_left.set_xlim(0, 300)

ax4_right = ax4_left.twinx()
# MATLAB: scatter(time, energy, 5, 'filled', 'r')
ax4_right.scatter(time, energy, s=5, c="r", edgecolors="none")
ax4_right.set_ylabel("Normalised AE Energy (a.u.)")
ax4_right.set_ylim(0, 1.05)

ax4_left.set_title("T07 Commercial Normalised AE Energy")
ax4_left.grid(which="minor", alpha=0.3)

# --- Figure 5: Stress + Normalised Cumulative AE Energy --------------------
fig5, ax5_left = plt.subplots()

ax5_left.plot(t1, stress, "b")
ax5_left.set_ylabel("Stress (MPa)")
ax5_left.set_xlabel("Time (s)")
ax5_left.set_ylim(0, stress.max())
ax5_left.set_xlim(0, 300)

ax5_right = ax5_left.twinx()
ax5_right.plot(time, cumenergy, "r")
ax5_right.set_ylabel("Normalised Cumulative AE Energy (a.u.)")
ax5_right.set_ylim(0, 1.05)

ax5_left.set_title("T07 Commercial Normalised Cumulative AE Energy")
ax5_left.grid(which="minor", alpha=0.3)

# ---------------------------------------------------------------------------
# 4. Display all figures
# ---------------------------------------------------------------------------
plt.show()
```

File created at: `/Users/vangogh/Documents/Obsidian/brainmse/Individual Project/Tools history/Claude code cli ccswitch to Deepseek-v4-pro/ae_analysis.py`

---

## Assistant (continued):

The translation is complete at `ae_analysis.py`. Here's a summary of the key MATLAB → Python mappings and design decisions:

---

## MATLAB → Python Mapping Table

| MATLAB | Python (this translation) | Rationale |
|---|---|---|
| `xlsread(file, sheet)` | `pd.read_excel()` → `.values` | pandas for robust Excel I/O; numpy array for parity |
| `data(:, 1)` | `data[:, 0]` | MATLAB 1-based → Python 0-based: subtract 1 |
| `yyaxis left` … `yyaxis right` | `ax.twinx()` | Object-oriented matplotlib dual-axis pattern |
| `grid('minor')` | `ax.grid(which="minor")` | Explicit minor-grid toggle in matplotlib |
| `ylim([0 max(stress)])` | `ax.set_ylim(0, stress.max())` | `.max()` is numpy's array maximum method |
| `scatter(…, 5, 'filled', 'r')` | `ax.scatter(…, s=5, c="r", edgecolors="none")` | `s` = marker size in points²; `edgecolors="none"` = filled |
| `figure` | `plt.subplots()` | OOP approach returns (fig, ax) tuple |

## Python-Specific Design Choices

1. **`pd.read_excel` with `header=None`** — treats the Excel sheet as raw numeric data with no header row, matching MATLAB's `xlsread` behaviour. If the file has headers, switch to `header=0` and use column-name access.

2. **0-based indexing** — every MATLAB column index *n* becomes *n−1* in Python. This is the single most common source of bugs in MATLAB→Python migrations, so each column assignment is explicitly commented with its mapping.

3. **`twinx()` pattern** — for each dual-axis figure (Figs 2–5), a left `Axes` is created with `plt.subplots()`, then a right twin is spawned via `.twinx()`. This mirrors MATLAB's `yyaxis left`/`yyaxis right` semantics exactly: both axes share the same x-axis but have independent y-scales.

4. **`plt.rcParams` for grid** — matplotlib's default grid is major-only. Setting `axes.grid.which = "both"` and adding `ax.grid(which="minor")` replicates MATLAB's `grid('minor')` appearance.

5. **Scatter `edgecolors="none"`** — MATLAB's `'filled'` marker option removes edge strokes. In matplotlib this is achieved with `edgecolors="none"` (not `edgecolor` — the plural form is intentional for the scatter API).

## Dependencies

```bash
pip install pandas matplotlib openpyxl
```

## Usage

```bash
python ae_analysis.py
```

Make sure `Commercial Tensile Tests.xlsx` is in the working directory, or update `FILE_PATH` in the script.

---
