"""Measure the source logo JPEG so the SVG rebuild matches it exactly.

Prints per-colour bounding boxes, the exact brand hex values, and an ASCII map of
the black mask (so the M's outline can be read off as polygon vertices).
"""

from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image

SRC = Path(__file__).resolve().parent.parent / "brand" / "logo-source.jpeg"


def classify(px: np.ndarray) -> np.ndarray:
    """Map RGB -> label: 0 white, 1 black, 2 cyan, 3 magenta, 4 yellow."""
    r, g, b = px[..., 0].astype(int), px[..., 1].astype(int), px[..., 2].astype(int)
    mx, mn = px.max(axis=-1).astype(int), px.min(axis=-1).astype(int)
    sat = mx - mn

    lab = np.zeros(px.shape[:2], dtype=np.uint8)
    lab[(mx < 110) & (sat < 60)] = 1                       # black
    lab[(sat > 70) & (b > 130) & (b > r + 60) & (g > r)] = 2   # cyan
    lab[(sat > 70) & (r > 130) & (r > g + 60) & (b > g)] = 3   # magenta
    lab[(sat > 70) & (r > 150) & (g > 130) & (b < g - 60)] = 4  # yellow
    return lab


def bbox(mask: np.ndarray):
    ys, xs = np.nonzero(mask)
    if len(ys) == 0:
        return None
    return int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())


def components(mask: np.ndarray, min_px: int = 400):
    """4-connected components, largest first."""
    seen = np.zeros_like(mask, dtype=bool)
    out = []
    h, w = mask.shape
    for y0 in range(h):
        for x0 in range(w):
            if not mask[y0, x0] or seen[y0, x0]:
                continue
            q = deque([(y0, x0)])
            seen[y0, x0] = True
            pts = []
            while q:
                y, x = q.popleft()
                pts.append((y, x))
                for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < h and 0 <= nx < w and mask[ny, nx] and not seen[ny, nx]:
                        seen[ny, nx] = True
                        q.append((ny, nx))
            if len(pts) >= min_px:
                arr = np.array(pts)
                out.append({
                    "px": len(pts),
                    "bbox": (int(arr[:, 1].min()), int(arr[:, 0].min()),
                             int(arr[:, 1].max()), int(arr[:, 0].max())),
                    "mask": arr,
                })
    out.sort(key=lambda c: -c["px"])
    return out


def mean_hex(px: np.ndarray, mask: np.ndarray) -> str:
    sel = px[mask]
    if len(sel) == 0:
        return "-"
    # Trim JPEG edge artefacts: keep the most saturated 60% of the region.
    sat = sel.max(axis=1).astype(int) - sel.min(axis=1).astype(int)
    keep = sel[sat >= np.percentile(sat, 40)] if sat.max() > 40 else sel
    m = keep.mean(axis=0).round().astype(int)
    return "#{:02X}{:02X}{:02X}".format(*m)


def ascii_map(mask: np.ndarray, box, cols=76):
    x0, y0, x1, y1 = box
    sub = mask[y0:y1 + 1, x0:x1 + 1]
    h, w = sub.shape
    rows = max(1, round(cols * h / w * 0.5))
    lines = []
    for r in range(rows):
        ya, yb = int(r * h / rows), max(int(r * h / rows) + 1, int((r + 1) * h / rows))
        line = ""
        for c in range(cols):
            xa, xb = int(c * w / cols), max(int(c * w / cols) + 1, int((c + 1) * w / cols))
            cell = sub[ya:yb, xa:xb]
            frac = cell.mean() if cell.size else 0.0
            line += "#" if frac > 0.6 else ("+" if frac > 0.25 else ".")
        lines.append(line)
    return lines


def main():
    img = Image.open(SRC).convert("RGB")
    px = np.asarray(img)
    print(f"source      : {SRC.name}  {img.width}x{img.height}")

    lab = classify(px)
    names = {1: "black", 2: "cyan", 3: "magenta", 4: "yellow"}

    print("\n--- colour regions (whole image) ---")
    for k, name in names.items():
        m = lab == k
        print(f"{name:8s} px={int(m.sum()):7d}  bbox={bbox(m)}  hex={mean_hex(px, m)}")

    print("\n--- black components ---")
    for i, c in enumerate(components(lab == 1)):
        x0, y0, x1, y1 = c["bbox"]
        print(f"  [{i}] px={c['px']:7d} bbox=({x0},{y0})-({x1},{y1}) "
              f"w={x1 - x0 + 1} h={y1 - y0 + 1}")

    print("\n--- colour square components ---")
    for k in (2, 3, 4):
        for i, c in enumerate(components(lab == k, min_px=200)):
            x0, y0, x1, y1 = c["bbox"]
            print(f"  {names[k]:8s}[{i}] px={c['px']:6d} bbox=({x0},{y0})-({x1},{y1}) "
                  f"w={x1 - x0 + 1} h={y1 - y0 + 1}")

    full = bbox(lab > 0)
    print(f"\n--- full logo bbox: {full}  "
          f"w={full[2] - full[0] + 1} h={full[3] - full[1] + 1} "
          f"ratio={(full[2] - full[0] + 1) / (full[3] - full[1] + 1):.4f}")

    print("\n--- ASCII map of black mask (M + dot) ---")
    bb = bbox(lab == 1)
    for line in ascii_map(lab == 1, bb):
        print("   " + line)

    print("\n--- ASCII map of full logo ---")
    for line in ascii_map(lab > 0, full):
        print("   " + line)


if __name__ == "__main__":
    main()
