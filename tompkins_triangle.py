#!/usr/bin/env python3
"""
Tompkins Triangle CLI
---------------------
Generate and save a Tompkins Triangle T_k as a PNG.

Usage examples:
  python tompkins_triangle.py --k 4 --n 10 --highlight 2
  python tompkins_triangle.py --k 5 --n 12
  python tompkins_triangle.py --k 5 --n 12 --highlight-multi 0:red,1:blue,2:green
"""

import argparse
import math
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch

# ---------- Core construction ----------

def build_tompkins_triangle(k: int, n_max: int):
    """
    Construct T_k up to row n_max (inclusive).
    c = k-2
    T_k(0,0) = c
    For n >= 1: T_k(n,0) = 1, T_k(n,n) = c
    Interior:   T_k(n,r) = T_k(n-1,r-1) + T_k(n-1,r)
    Returns list of rows (row n has length n+1).
    """
    assert k >= 3 and n_max >= 0
    c = k - 2
    T = [[c]]  # row 0
    for n in range(1, n_max + 1):
        row = [1] + [0]*(n-1) + [c]
        for r in range(1, n):
            row[r] = T[n-1][r-1] + T[n-1][r]
        T.append(row)
    return T, c

# ---------- Rendering ----------

def render_triangle_png(T, k: int, c: int, highlight_j, out_path: Path, highlight_multi=None):
    """
    Render T as a PNG with readable typography and optional highlighted diagonals.
    highlight_j = 0 highlights the right edge (constant c), 1 highlights next inwards, etc.
    highlight_multi = dict of {j: color} for multi-diagonal highlighting.
    """
    n_max = len(T) - 1

    # Layout & typography tuned for readability
    cell = 1.0            # base spacing
    yscale = 1.0          # vertical spacing multiplier
    pad_cells = 0.9       # margin around triangle
    base_fs = 28          # base font size; scale down with n
    fs = max(10, int(base_fs - 1.1 * n_max))

    fig_w = 0.9 * (n_max + 4)   # scale canvas with size
    fig_h = 0.9 * (n_max + 4)
    fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=180)
    ax.set_facecolor('white')
    ax.axis('off')

    # Draw nodes
    for n, row in enumerate(T):
        for r, val in enumerate(row):
            x = (r - n/2.0) * cell
            y = -(n * yscale) * cell

            # subtle rounded background to improve contrast
            box = FancyBboxPatch(
                (x - 0.38, y - 0.38), 0.76, 0.76,
                boxstyle="round,pad=0.02,rounding_size=0.05",
                linewidth=0.6, edgecolor=(0,0,0,0.15), facecolor=(0,0,0,0.03)
            )
            ax.add_patch(box)
            ax.text(x, y, str(val), ha='center', va='center', fontsize=fs)

            # highlight chosen descending diagonal j (cells with r = n - j)
            # Single diagonal (legacy)
            if (highlight_j is not None) and (n >= highlight_j) and (r == n - highlight_j):
                circ = Circle((x, y), 0.46, fill=False, linewidth=2.2, alpha=0.75)
                ax.add_patch(circ)
            # Multiple diagonals with color
            if highlight_multi:
                for j, color in highlight_multi.items():
                    if (n >= j) and (r == n - j):
                        circ = Circle((x, y), 0.46, fill=False, linewidth=2.2, alpha=0.85, edgecolor=color)
                        ax.add_patch(circ)

    # Bounds & title
    xmin = - (n_max/2.0) * cell - pad_cells
    xmax =   (n_max/2.0) * cell + pad_cells
    ymin = - (n_max * yscale) * cell - pad_cells
    ymax = pad_cells
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)

    ax.set_title(f"Tompkins Triangle  T_{k}  (c={c}), rows 0..{n_max}", fontsize=fs+2, pad=20)

    # comfortable space above/below
    plt.subplots_adjust(top=0.88, bottom=0.12)
    fig.savefig(out_path, bbox_inches="tight")
    plt.close(fig)

def parse_highlight_multi(arg: str):
    """
    Parse a highlight-multi CLI string into a {j: color} dict.
    Example arg: "0:red,1:blue,2:#00ff00"
    """
    result = {}
    if not arg:
        return result
    for part in arg.split(','):
        if ':' not in part:
            continue
        jstr, color = part.split(':', 1)
        try:
            j = int(jstr)
            result[j] = color
        except ValueError:
            continue
    return result

# ---------- CLI ----------

def main():
    ap = argparse.ArgumentParser(description="Generate a Tompkins Triangle PNG.")
    ap.add_argument("--k", type=int, required=True, help="Polygon side count (k>=3). Example: 4 for squares.")
    ap.add_argument("--n", type=int, required=True, help="Max row index n_max (rows 0..n).")
    ap.add_argument("--highlight", type=int, default=None,
                    help="Descending diagonal index j to highlight (j=0 is right edge constant c).")
    ap.add_argument("--highlight-multi", type=str, default=None,
                    help="Comma-separated list of diagonal:color, e.g. 0:red,1:blue,2:#00ff00")
    ap.add_argument("--out", type=Path, default=None,
                    help="Output PNG path. If omitted, an auto name is used.")
    args = ap.parse_args()

    T, c = build_tompkins_triangle(args.k, args.n)

    highlight_multi = parse_highlight_multi(args.highlight_multi) if args.highlight_multi else None

    # auto filename
    if args.out is None:
        fname = f"tompkins_T{args.k}_n{args.n}"
        if args.highlight is not None:
            fname += f"_j{args.highlight}"
        if highlight_multi:
            fname += "_multi"
        fname += ".png"
        out_path = Path(fname)
    else:
        out_path = args.out

    render_triangle_png(
        T, k=args.k, c=c,
        highlight_j=args.highlight,
        out_path=out_path,
        highlight_multi=highlight_multi
    )
    print(f"Saved: {out_path.resolve()}")

if __name__ == "__main__":
    main()
