"""Reusable machine sub-assemblies.

Every machine in the catalogue is the same industrial vocabulary rearranged:
a frame on levelling feet, linear rails, a carriage carrying heads and curing,
an energy chain, a bulk-ink station, a console and a signal tower. Building them
once here is what keeps four machines looking like one product family — which is
exactly what a real manufacturer's range looks like.

Conventions: X = machine length, Y = depth, Z = up. Metres.
"""

from __future__ import annotations

import math
from typing import Sequence

import bpy

from . import build


def levelling_feet(kit, col, positions: Sequence[tuple], height: float = 0.09,
                   name: str = "Foot") -> list:
    """Adjustable feet. Machines never sit flush on the floor, and the shadow gap
    underneath is a large part of why a render reads as a real object."""
    out = []
    for i, (x, y) in enumerate(positions):
        stud = build.cylinder(f"{name}Stud{i}", 0.016, height, (x, y, height / 2),
                              mat=kit["steel"], col=col, verts=12)
        pad = build.cylinder(f"{name}Pad{i}", 0.055, 0.022, (x, y, 0.011),
                             mat=kit["anod"], col=col, verts=20)
        nut = build.cylinder(f"{name}Nut{i}", 0.030, 0.018, (x, y, height - 0.02),
                             mat=kit["steel"], col=col, verts=6)
        out += [stud, pad, nut]
    return out


def linear_rail(name: str, length: float, loc, kit, col, axis: str = "X",
                width: float = 0.045, height: float = 0.030) -> list:
    """Profile rail plus its mounting bolts."""
    rot = (0, 0, 0) if axis == "X" else (0, 0, 90)
    rail = build.box(name, (length, width, height), loc, rot,
                     mat=kit["steel"], bevel=0.0025, col=col)
    n = max(2, int(length / 0.28))
    off = (length / n, 0, 0) if axis == "X" else (0, length / n, 0)
    start = (loc[0] - length / 2 + length / n / 2, loc[1], loc[2] + height / 2 - 0.002) \
        if axis == "X" else (loc[0], loc[1] - length / 2 + length / n / 2,
                             loc[2] + height / 2 - 0.002)
    bolts = build.bolt_row(f"{name}Bolts", n, length / n, 0.008, 0.006, start,
                           mat=kit["anod"], col=col,
                           axis=(1, 0, 0) if axis == "X" else (0, 1, 0))
    return [rail, bolts]


def bearing_block(name: str, loc, kit, col, size=(0.16, 0.09, 0.055)) -> list:
    body = build.box(name, size, loc, mat=kit["anod"], bevel=0.003, col=col)
    return [body]


def cable_chain(name: str, length: float, loc, kit, col, axis: str = "X",
                link: float = 0.075, w: float = 0.055, h: float = 0.075) -> list:
    """Energy chain as an array of links with a visible gap between them.
    The gap is the whole point — a solid bar reads as a pipe, not a chain."""
    n = max(2, int(length / link))
    first = (loc[0] - length / 2 + link / 2, loc[1], loc[2]) if axis == "X" \
        else (loc[0], loc[1] - length / 2 + link / 2, loc[2])
    size = (link * 0.82, w, h) if axis == "X" else (w, link * 0.82, h)
    seg = build.box(f"{name}Link", size, first, mat=kit["trim"], bevel=0.003, col=col)
    build.array(seg, n, (link, 0, 0) if axis == "X" else (0, link, 0))
    return [seg]


def vent_grille(name: str, size, loc, kit, col, rot=(0, 0, 0)) -> list:
    """Louvred vent: a recessed frame with slats, not a flat texture."""
    frame = build.box(f"{name}Frame", (size[0], size[1], 0.012), loc, rot,
                      mat=kit["body"], bevel=0.002, col=col)
    n = max(3, int(size[1] / 0.028))
    slat = build.box(f"{name}Slat", (size[0] - 0.02, 0.010, 0.016),
                     (loc[0], loc[1] - size[1] / 2 + 0.02, loc[2] - 0.004), rot,
                     mat=kit["anod"], bevel=0.0012, col=col)
    build.array(slat, n, (0, 0.028, 0))
    return [frame, slat]


def control_console(name: str, loc, kit, col, screen_w: float = 0.34,
                    screen_h: float = 0.23, post_h: float = 0.42,
                    yaw_deg: float = 0.0, tilt_deg: float = 62.0) -> list:
    """Swing-arm touchscreen console. Present on every machine we sell."""
    parts = [
        # Mounting bracket — without it the post looks like it was dropped in.
        build.box(f"{name}Mount", (0.11, 0.09, 0.14),
                  (loc[0], loc[1] + 0.03, loc[2] + 0.05),
                  mat=kit["body"], bevel=0.005, col=col),
        build.cylinder(f"{name}Post", 0.026, post_h,
                       (loc[0], loc[1], loc[2] + post_h / 2),
                       mat=kit["anod"], col=col, verts=20),
        build.cylinder(f"{name}Collar", 0.036, 0.030,
                       (loc[0], loc[1], loc[2] + post_h - 0.05),
                       mat=kit["steel"], col=col, verts=20),
    ]

    hx = loc[0] + math.sin(math.radians(yaw_deg)) * 0.06
    hy = loc[1] - math.cos(math.radians(yaw_deg)) * 0.06
    hz = loc[2] + post_h + 0.05
    # Housing, then a recessed bezel, then the glass proud of it: three parallel
    # planes is what makes a slab read as a screen.
    parts.append(build.box(f"{name}Housing", (screen_w + 0.05, screen_h + 0.06, 0.055),
                           (hx, hy, hz), (tilt_deg, 0, yaw_deg),
                           mat=kit["body"], bevel=0.008, col=col))
    n = build.Vector((0.0, -math.sin(math.radians(tilt_deg)),
                      math.cos(math.radians(tilt_deg))))
    faces = (
        ("Bezel", 0.028, screen_w + 0.018, screen_h + 0.020, 0.006, kit["trim"]),
        ("Glass", 0.034, screen_w, screen_h, 0.004, kit["screen"]),
    )
    for tag, off, w, h, t, mat in faces:
        parts.append(build.box(f"{name}{tag}", (w, h, t),
                               (hx + n.x * off, hy + n.y * off, hz + n.z * off),
                               (tilt_deg, 0, yaw_deg), mat=mat,
                               bevel=0.0015, col=col))
    return parts


def status_beacon(name: str, loc, kit, col, post_h: float = 0.30) -> list:
    """Red / amber / green signal tower."""
    parts = [build.cylinder(f"{name}Post", 0.014, post_h,
                            (loc[0], loc[1], loc[2] + post_h / 2),
                            mat=kit["anod"], col=col, verts=12)]
    for i, key in enumerate(("beacon_g", "beacon_a", "beacon_r")):
        parts.append(build.cylinder(
            f"{name}Lamp{i}", 0.034, 0.045,
            (loc[0], loc[1], loc[2] + post_h + 0.024 + i * 0.048),
            mat=kit[key], col=col, verts=20, bevel=0.002))
    parts.append(build.cylinder(f"{name}Cap", 0.034, 0.012,
                                (loc[0], loc[1], loc[2] + post_h + 0.168),
                                mat=kit["anod"], col=col, verts=20))
    return parts


def estop(name: str, loc, kit, col, rot=(0, 0, 0)) -> list:
    base = build.cylinder(f"{name}Base", 0.032, 0.014, loc, rot,
                          mat=kit["warn"], col=col, verts=20)
    head = build.cylinder(f"{name}Head", 0.026, 0.020,
                          (loc[0], loc[1], loc[2] + 0.016), rot,
                          mat=kit["estop"], col=col, verts=20, bevel=0.004)
    return [base, head]


INK_ORDER = ("ink_c", "ink_m", "ink_y", "ink_k", "ink_w")


def ink_station(name: str, loc, kit, col, channels: int = 6,
                bottle_r: float = 0.048, bottle_h: float = 0.20,
                yaw_deg: float = 0.0) -> list:
    """Bulk-ink rack. The coloured bottles are the single most legible signal in
    the whole render that this machine prints — worth the polygons."""
    pitch = bottle_r * 2 + 0.022
    width = pitch * channels + 0.04
    parts = [
        build.box(f"{name}Rack", (width, 0.16, 0.03),
                  (loc[0], loc[1], loc[2]), (0, 0, yaw_deg),
                  mat=kit["body"], bevel=0.003, col=col),
        build.box(f"{name}Back", (width, 0.02, bottle_h + 0.06),
                  (loc[0], loc[1] + 0.075, loc[2] + bottle_h / 2 + 0.02),
                  (0, 0, yaw_deg), mat=kit["body"], bevel=0.003, col=col),
    ]
    for i in range(channels):
        x = loc[0] - width / 2 + 0.02 + pitch * (i + 0.5)
        mat = kit[INK_ORDER[i % len(INK_ORDER)]]
        parts.append(build.cylinder(
            f"{name}Bottle{i}", bottle_r, bottle_h,
            (x, loc[1], loc[2] + 0.015 + bottle_h / 2),
            mat=mat, col=col, verts=20, bevel=0.004))
        parts.append(build.cylinder(
            f"{name}Cap{i}", bottle_r * 0.45, 0.028,
            (x, loc[1], loc[2] + 0.015 + bottle_h + 0.012),
            mat=kit["trim"], col=col, verts=16))
    return parts


def print_carriage(name: str, loc, kit, col, heads: int = 6,
                   width: float = 0.62, depth: float = 0.40,
                   height: float = 0.30, uv: bool = True) -> list:
    """Head carriage: shell, staggered head bodies underneath, LED-UV lamps either
    side. The lamp glow is the machine's one piece of self-illumination."""
    parts = [build.box(f"{name}Shell", (width, depth, height), loc,
                       mat=kit["body"], bevel=0.006, col=col)]
    parts.append(build.box(f"{name}Lid", (width - 0.03, depth - 0.03, 0.02),
                           (loc[0], loc[1], loc[2] + height / 2 + 0.008),
                           mat=kit["accent"], bevel=0.004, col=col))

    head_w = (width - 0.14) / heads
    for i in range(heads):
        x = loc[0] - width / 2 + 0.07 + head_w * (i + 0.5)
        y = loc[1] + (0.022 if i % 2 else -0.022)      # staggered, as they really are
        parts.append(build.box(f"{name}Head{i}", (head_w * 0.72, 0.10, 0.09),
                               (x, y, loc[2] - height / 2 - 0.03),
                               mat=kit["anod"], bevel=0.003, col=col))
    if uv:
        # Lamps flank the heads along the TRAVEL axis (Y), so ink cures on both
        # the outward and return stroke. Putting them beside the swath instead is
        # the classic tell that whoever modelled it had not looked at one.
        for sign, tag in ((-1, "A"), (1, "B")):
            ly = loc[1] + sign * (depth / 2 + 0.050)
            parts.append(build.box(f"{name}UV{tag}Body", (width - 0.04, 0.078, 0.15),
                                   (loc[0], ly, loc[2] - height / 2 + 0.015),
                                   mat=kit["anod"], bevel=0.004, col=col))
            parts.append(build.box(f"{name}UV{tag}Emit", (width - 0.09, 0.050, 0.006),
                                   (loc[0], ly, loc[2] - height / 2 - 0.062),
                                   mat=kit["uv_lamp"], bevel=0.001, col=col))
    return parts


def skirt_panel(name: str, size, loc, kit, col, rot=(0, 0, 0),
                accent_line: bool = True) -> list:
    """Body panel with a shut line and an optional accent inlay along its top edge.
    The shut line is what separates 'panels' from 'a painted box'."""
    parts = [build.box(name, size, loc, rot, mat=kit["body"], bevel=0.004, col=col)]
    if accent_line:
        parts.append(build.box(f"{name}Accent",
                               (size[0] * 0.985, size[1] + 0.004, 0.012),
                               (loc[0], loc[1], loc[2] + size[2] / 2 - 0.022), rot,
                               mat=kit["accent"], bevel=0.002, col=col))
    return parts
