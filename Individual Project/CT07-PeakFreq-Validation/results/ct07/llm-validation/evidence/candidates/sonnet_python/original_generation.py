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
