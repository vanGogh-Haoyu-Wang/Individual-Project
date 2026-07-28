"""CT07-scoped compatibility surface for one SMOP 0.41 generated script."""

from __future__ import annotations

import builtins
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class _AllRows:
    pass


class _FigureSentinel:
    pass


ALL_ROWS = _AllRows()
figure = _FigureSentinel()
_input_path: Path | None = None
_sheet_name: str | None = None
_figures: list = []
_axes: dict[object, dict[str, object]] = {}
_current_figure = None
_current_side = "left"


class matlabarray:
    def __init__(self, values):
        self.values = np.asarray(values, dtype=float)

    def __call__(self, rows, column):
        if rows is not ALL_ROWS:
            raise NotImplementedError("Only data(arange(), column) is supported.")
        column_index = int(column) - 1
        if not 0 <= column_index < self.values.shape[1]:
            raise IndexError(f"MATLAB column {column} is out of range.")
        return self.values[:, column_index].copy()


def configure(input_path, sheet_name):
    global _input_path, _sheet_name
    _input_path = Path(input_path)
    _sheet_name = str(sheet_name)
    reset_figures()


def reset_figures():
    global _figures, _axes, _current_figure, _current_side
    plt.close("all")
    _figures = []
    _axes = {}
    _current_figure = None
    _current_side = "left"


def figures():
    return list(_figures)


def xlsread(_generated_path, _generated_sheet):
    path = _input_path or Path(_generated_path)
    sheet = _sheet_name or str(_generated_sheet)
    frame = pd.read_excel(path, sheet_name=sheet, header=None)
    numeric = frame.apply(pd.to_numeric, errors="coerce")
    return matlabarray(numeric.to_numpy(float))


def arange(*args):
    if not args:
        return ALL_ROWS
    raise NotImplementedError("Only no-argument arange() is supported.")


def concat(values):
    return tuple(np.asarray(values, dtype=float).reshape(-1).tolist())


def max(values):
    return float(np.nanmax(np.asarray(values, dtype=float)))


def copy(value):
    global _current_figure, _current_side
    if value is not figure:
        return builtins.__import__("copy").copy(value)
    created, left = plt.subplots()
    _figures.append(created)
    _axes[created] = {"left": left, "right": None}
    _current_figure = created
    _current_side = "left"
    return created


def _current_axis():
    if _current_figure is None:
        raise RuntimeError("No current SMOP figure.")
    return _axes[_current_figure][_current_side]


def plot(x, y, style=None):
    return _current_axis().plot(x, y, style or "-")


def scatter(x, y, size=5, *_args):
    color = "red" if "r" in _args else None
    return _current_axis().scatter(x, y, s=size, color=color)


def xlabel(label):
    return _axes[_current_figure]["left"].set_xlabel(label)


def ylabel(label):
    return _current_axis().set_ylabel(label)


def title(label):
    return _axes[_current_figure]["left"].set_title(label)


def xlim(limits):
    return _current_axis().set_xlim(*limits)


def ylim(limits):
    return _current_axis().set_ylim(*limits)


def grid(which):
    axis = _axes[_current_figure]["left"]
    axis.minorticks_on()
    return axis.grid(True, which=which)


def yyaxis(side):
    global _current_side
    if side not in ("left", "right"):
        raise ValueError("yyaxis accepts only 'left' or 'right'.")
    if side == "right" and _axes[_current_figure]["right"] is None:
        _axes[_current_figure]["right"] = _axes[_current_figure]["left"].twinx()
    _current_side = side
    plt.sca(_current_axis())
    return _current_axis()

