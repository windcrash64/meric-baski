"""Generate the Maven brand SVG set from one parametric construction.

The mark was reverse-engineered from the client's bitmap (see analyze_logo.py /
vectorize_logo.py). It sits on a square module grid:

    module      = 1 unit
    mark height = 3 modules
    diagonal    = 4 across : 7 down
    stem width  = 1 module
    dot         = 1 x 1 module, bottom-right of the M
    CMYK cluster= three 1 x 1 modules on a 2x3 sub-grid, one module clear of the M

Every file is emitted from these constants, so the lockups can never drift apart.
The wordmark uses `currentColor` so a single file works on light and dark.
"""

from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "brand"

# --- construction -----------------------------------------------------------
S = 4 / 7          # diagonal run per unit of drop
H = 3.0            # mark height, modules
STEM = 1.0         # stem width
W = 4.84375        # black mark width (dot's right edge)
T = 1.125          # horizontal thickness of a diagonal
ARM = 1.0          # height of the top-right arm
GAP = 1.0          # clear space between mark and CMYK cluster

CX = W / 2                       # the inner apex sits on the mark's centre line
L2_TOP = 1.4375                  # inner edge of the left diagonal at y=0
L1_TOP = L2_TOP - T              # outer edge of the left diagonal at y=0
R1_TOP = W - L2_TOP              # inner edge of the right diagonal at y=0
R2_TOP = R1_TOP + T              # outer edge of the right diagonal at y=0

Y_APEX = (CX - L2_TOP) / S       # where the two inner edges meet
Y_NOTCH = (STEM - L1_TOP) / S    # where the outer edge leaves the stem

CYAN, MAGENTA, YELLOW = "#0081D2", "#E30161", "#FFE305"
INK = "#0A0A0A"

TOTAL_W = W + GAP + 2.0          # mark + gap + 2-column CMYK cluster


def n(v: float) -> str:
    s = f"{v:.4f}".rstrip("0").rstrip(".")
    return s if s not in ("", "-0") else "0"


def mark_path() -> str:
    """The 'M.' glyph: outer contour with the stem notch cut out, plus the dot."""
    p = [
        (0, 0),
        (L2_TOP, 0),
        (CX, Y_APEX),
        (R1_TOP, 0),
        (W, 0),
        (W, ARM),
        (R2_TOP - ARM * S, ARM),
        (R2_TOP - H * S, H),
        (L1_TOP + H * S, H),
        (STEM, Y_NOTCH),
        (STEM, H),
        (0, H),
    ]
    d = "M" + "L".join(f"{n(x)} {n(y)}" for x, y in p) + "Z"
    d += f"M{n(W - 1)} {n(H - 1)}L{n(W)} {n(H - 1)}L{n(W)} {n(H)}L{n(W - 1)} {n(H)}Z"
    return d


def squares(x0: float = None) -> str:
    """The CMYK pixel cluster: cyan top-left, magenta mid-right, yellow bottom-left."""
    x0 = W + GAP if x0 is None else x0
    return "\n".join([
        f'  <rect fill="{CYAN}" x="{n(x0)}" y="0" width="1" height="1"/>',
        f'  <rect fill="{MAGENTA}" x="{n(x0 + 1)}" y="1" width="1" height="1"/>',
        f'  <rect fill="{YELLOW}" x="{n(x0)}" y="2" width="1" height="1"/>',
    ])


def svg(body: str, vw: float, vh: float, title: str, extra: str = "") -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {n(vw)} {n(vh)}"'
        f' role="img" aria-label="{title}"{extra}>\n'
        f"  <title>{title}</title>\n{body}\n</svg>\n"
    )


def write(name: str, content: str) -> None:
    (OUT / name).write_text(content, encoding="utf-8")
    print(f"  {name:28s} {len(content):5d} B")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    print("construction:")
    print(f"  apex y      = {Y_APEX:.4f}")
    print(f"  notch y     = {Y_NOTCH:.4f}")
    print(f"  arm inner x = {R2_TOP - ARM * S:.4f}")
    print(f"  baseline x  = {R2_TOP - H * S:.4f} .. {L1_TOP + H * S:.4f}")
    print(f"  total box   = {TOTAL_W:.5f} x {H}")
    print("files:")

    d = mark_path()

    # 1. Primary lockup — inherits colour, so one file serves light and dark.
    write("maven-logo.svg", svg(
        f'  <path fill="currentColor" d="{d}"/>\n{squares()}',
        TOTAL_W, H, "Maven"))

    # 2. Wordmark only, no CMYK cluster.
    write("maven-wordmark.svg", svg(
        f'  <path fill="currentColor" d="{d}"/>', W, H, "Maven"))

    # 3. Single-colour lockup for embroidery / fax / one-colour print.
    write("maven-logo-mono.svg", svg(
        f'  <path fill="currentColor" d="{d}"/>\n'
        f'  <rect fill="currentColor" x="{n(W + GAP)}" y="0" width="1" height="1"/>\n'
        f'  <rect fill="currentColor" x="{n(W + GAP + 1)}" y="1" width="1" height="1"/>\n'
        f'  <rect fill="currentColor" x="{n(W + GAP)}" y="2" width="1" height="1"/>',
        TOTAL_W, H, "Maven"))

    # 4 & 5. Square tile lockup — the mark fitted to width with a CMYK rule beneath,
    # right-aligned to the mark. Used for the avatar badge and the favicon; the only
    # difference is the corner radius, so they can never drift apart.
    def tile(side: float, pad: float, rule_h: float, gap: float, radius: float) -> str:
        inner = side - pad * 2
        k = inner / W                                  # fit the mark to the width
        mark_h = H * k
        block_h = mark_h + gap + rule_h
        top = (side - block_h) / 2
        rule_w = inner / 3
        ry = top + mark_h + gap
        return (
            f'  <rect width="{n(side)}" height="{n(side)}" rx="{n(radius)}" fill="{INK}"/>\n'
            f'  <g transform="translate({n(pad)} {n(top)}) scale({n(k)})">\n'
            f'    <path fill="#FFFFFF" d="{d}"/>\n'
            f'  </g>\n'
            f'  <rect fill="{CYAN}" x="{n(pad)}" y="{n(ry)}" '
            f'width="{n(rule_w)}" height="{n(rule_h)}"/>\n'
            f'  <rect fill="{MAGENTA}" x="{n(pad + rule_w)}" y="{n(ry)}" '
            f'width="{n(rule_w)}" height="{n(rule_h)}"/>\n'
            f'  <rect fill="{YELLOW}" x="{n(pad + rule_w * 2)}" y="{n(ry)}" '
            f'width="{n(rule_w)}" height="{n(rule_h)}"/>'
        )

    write("maven-badge.svg", svg(tile(96, 14, 7, 9, 0), 96, 96, "Maven"))
    # Tighter margins than the badge: a favicon is read at 16 px, so the mark has
    # to take as much of the tile as the rounded corners allow.
    write("favicon.svg", svg(tile(32, 3, 3, 2.5, 6), 32, 32, "Maven"))

    print("\ncolours:")
    for k, v in (("ink", INK), ("cyan", CYAN), ("magenta", MAGENTA), ("yellow", YELLOW)):
        print(f"  {k:8s} {v}")


if __name__ == "__main__":
    main()
