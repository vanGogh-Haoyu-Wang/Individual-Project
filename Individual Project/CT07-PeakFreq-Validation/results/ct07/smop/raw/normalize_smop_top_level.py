"""Remove only SMOP 0.41's invalid top-level four-space indentation."""

from __future__ import annotations

import sys
from pathlib import Path


def normalize(source: Path, target: Path) -> None:
    lines = source.read_text(encoding="utf-8").splitlines(keepends=True)
    normalized = [line[4:] if line.startswith("    ") else line for line in lines]
    if normalized == lines:
        raise ValueError("No SMOP top-level indentation was found.")
    target.write_text("".join(normalized), encoding="utf-8")


if __name__ == "__main__":
    normalize(Path(sys.argv[1]), Path(sys.argv[2]))
