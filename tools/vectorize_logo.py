"""Trace the source logo bitmap into an exact SVG.

The mark is entirely polygonal, so we follow the pixel boundary (marching-squares
style), simplify with Ramer-Douglas-Peucker, then snap the result onto the 89 px
module grid the mark was designed on. Output is a crisp, hand-editable path.
"""

from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "brand" / "logo-source.jpeg"
OUT = ROOT / "brand" / "logo-traced.svg"

# Measured from analyze_logo.py
UNIT = 89.0
ORIGIN = (373.0, 395.0)


def classify(px: np.ndarray) -> np.ndarray:
    r, g, b = px[..., 0].astype(int), px[..., 1].astype(int), px[..., 2].astype(int)
    mx, mn = px.max(axis=-1).astype(int), px.min(axis=-1).astype(int)
    sat = mx - mn
    lab = np.zeros(px.shape[:2], dtype=np.uint8)
    lab[(mx < 110) & (sat < 60)] = 1
    lab[(sat > 70) & (b > 130) & (b > r + 60) & (g > r)] = 2
    lab[(sat > 70) & (r > 130) & (r > g + 60) & (b > g)] = 3
    lab[(sat > 70) & (r > 150) & (g > 130) & (b < g - 60)] = 4
    return lab


def trace_boundary(mask: np.ndarray):
    """Follow the outline of every filled region, returning corner-point loops.

    Walks the *edges between pixels* (crack following) so the result is exact:
    every vertex lands on an integer pixel corner.
    """
    h, w = mask.shape
    padded = np.zeros((h + 2, w + 2), dtype=bool)
    padded[1:-1, 1:-1] = mask

    # Collect boundary edges as directed segments, keeping the filled area on the left.
    edges = {}
    for y in range(h + 1):
        for x in range(w + 1):
            inside = padded[y + 1, x + 1] if (y < h + 1 and x < w + 1) else False
            up = padded[y, x + 1] if y >= 0 else False
            left = padded[y + 1, x] if x >= 0 else False
            if inside != up:  # horizontal edge at y between (x,y)-(x+1,y)
                a, b = ((x, y), (x + 1, y)) if inside else ((x + 1, y), (x, y))
                edges.setdefault(a, []).append(b)
            if inside != left:  # vertical edge at x between (x,y)-(x,y+1)
                a, b = ((x, y + 1), (x, y)) if inside else ((x, y), (x, y + 1))
                edges.setdefault(a, []).append(b)

    loops = []
    while edges:
        start = next(iter(edges))
        loop = [start]
        cur = start
        while True:
            nxts = edges.get(cur)
            if not nxts:
                break
            nxt = nxts.pop()
            if not nxts:
                del edges[cur]
            cur = nxt
            if cur == start:
                break
            loop.append(cur)
        if len(loop) > 3:
            loops.append(loop)
    return loops


def rdp(points, eps):
    """Ramer-Douglas-Peucker on a closed loop."""
    if len(points) < 3:
        return points
    pts = np.array(points, dtype=float)

    def _rdp(lo, hi):
        if hi <= lo + 1:
            return [lo]
        a, b = pts[lo], pts[hi]
        ab = b - a
        n = np.hypot(*ab)
        seg = pts[lo:hi + 1]
        rel = seg - a
        if n < 1e-9:
            d = np.hypot(rel[:, 0], rel[:, 1])
        else:
            # 2-D cross product (numpy 2.x dropped the 2-vector form of np.cross)
            d = np.abs(ab[0] * rel[:, 1] - ab[1] * rel[:, 0]) / n
        i = int(np.argmax(d))
        if d[i] <= eps:
            return [lo]
        return _rdp(lo, lo + i) + _rdp(lo + i, hi)

    # Anchor on the extreme point so the loop split is stable.
    k = int(np.argmin(pts[:, 0] * 100000 + pts[:, 1]))
    pts = np.roll(pts, -k, axis=0)
    pts = np.vstack([pts, pts[0]])
    idx = _rdp(0, len(pts) - 1)
    return [tuple(pts[i]) for i in idx]


def to_grid(p):
    """Express a pixel coordinate in module units, snapped to 1/32 of a module."""
    x = (p[0] - ORIGIN[0]) / UNIT
    y = (p[1] - ORIGIN[1]) / UNIT
    return (round(x * 32) / 32, round(y * 32) / 32)


def fmt(v: float) -> str:
    s = f"{v:.4f}".rstrip("0").rstrip(".")
    return s if s not in ("", "-0") else "0"


def path_d(loops):
    parts = []
    for loop in loops:
        pts = [to_grid(p) for p in loop]
        # Drop consecutive duplicates created by snapping.
        clean = [pts[0]]
        for p in pts[1:]:
            if p != clean[-1]:
                clean.append(p)
        if len(clean) > 1 and clean[0] == clean[-1]:
            clean.pop()
        d = f"M{fmt(clean[0][0])} {fmt(clean[0][1])}"
        for p in clean[1:]:
            d += f"L{fmt(p[0])} {fmt(p[1])}"
        parts.append(d + "Z")
    return " ".join(parts)


def main():
    px = np.asarray(Image.open(SRC).convert("RGB"))
    lab = classify(px)

    black_d = path_d([rdp(l, 2.0) for l in trace_boundary(lab == 1)])

    squares = []
    for k, name in ((2, "cyan"), (3, "magenta"), (4, "yellow")):
        ys, xs = np.nonzero(lab == k)
        x0, y0 = to_grid((xs.min(), ys.min()))
        x1, y1 = to_grid((xs.max() + 1, ys.max() + 1))
        squares.append((name, x0, y0, x1 - x0, y1 - y0))

    ys, xs = np.nonzero(lab > 0)
    vb_w = (xs.max() + 1 - ORIGIN[0]) / UNIT
    vb_h = (ys.max() + 1 - ORIGIN[1]) / UNIT

    print(f"viewBox 0 0 {vb_w:.4f} {vb_h:.4f}")
    print("black path:")
    print(" ", black_d)
    print("squares (name x y w h in module units):")
    for s in squares:
        print("  ", s[0], [round(v, 4) for v in s[1:]])

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {fmt(round(vb_w, 4))} {fmt(round(vb_h, 4))}">',
        f'  <path fill="#000" d="{black_d}"/>',
    ]
    colors = {"cyan": "#0081D2", "magenta": "#E30161", "yellow": "#FFE305"}
    for name, x, y, w, h in squares:
        svg.append(f'  <rect fill="{colors[name]}" x="{fmt(x)}" y="{fmt(y)}" '
                   f'width="{fmt(w)}" height="{fmt(h)}"/>')
    svg.append("</svg>")
    OUT.write_text("\n".join(svg), encoding="utf-8")
    print(f"\nwrote {OUT}")


if __name__ == "__main__":
    main()
