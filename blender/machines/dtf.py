"""Maven D-Series — 620 mm DTF printer plus powder shaker / heat tunnel.

The product is modelled as the system buyers actually receive: a compact print
cabinet and a taller wheeled shaker joined by a continuous PET film bridge.
"""

from __future__ import annotations

import bpy

from lib import build, parts, shading

SPEC = {
    "key": "dtf",
    "series": "D",
    "print_width": 0.62,
    "overall": (2.40, 0.80, 1.60),
    "heads": 4,
    "channels": 5,
    "ink": "CMYK + W",
    "shaker_power_w": (2000, 5200),
}


def _film_ribbon(name, width, path, y, mat, col):
    """PET ribbon travelling in X/Z, from printer into the shaker."""
    steps = 12
    verts = []
    for x, z in path:
        for i in range(steps + 1):
            yy = y - width / 2 + width * i / steps
            verts.append((x, yy, z))
    faces = []
    row = steps + 1
    for j in range(len(path) - 1):
        for i in range(steps):
            a = j * row + i
            faces.append((a, a + row, a + row + 1, a + 1))
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.materials.append(mat)
    obj = bpy.data.objects.new(name, me)
    col.objects.link(obj)
    build.solidify(obj, thickness=0.003, offset=0.0)
    build.add_bevel(obj, 0.0015, 2)
    return obj


def _frustum(name, bottom, top, height, loc, mat, col):
    """Closed truncated box for the powder hopper."""
    bx, by = bottom
    tx, ty = top
    z0, z1 = -height / 2, height / 2
    verts = [
        (-bx / 2, -by / 2, z0), (bx / 2, -by / 2, z0),
        (bx / 2, by / 2, z0), (-bx / 2, by / 2, z0),
        (-tx / 2, -ty / 2, z1), (tx / 2, -ty / 2, z1),
        (tx / 2, ty / 2, z1), (-tx / 2, ty / 2, z1),
    ]
    faces = [
        (0, 3, 2, 1), (4, 5, 6, 7),
        (0, 1, 5, 4), (1, 2, 6, 5),
        (2, 3, 7, 6), (3, 0, 4, 7),
    ]
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.materials.append(mat)
    obj = bpy.data.objects.new(name, me)
    obj.location = loc
    col.objects.link(obj)
    build.add_bevel(obj, 0.010, 3)
    return obj


def _caster(name, x, y, kit, col, turn=0):
    """Compact locking castor used under both DTF cabinets."""
    return [
        build.cylinder(f"{name}Swivel", 0.036, 0.026,
                       (x, y, 0.115), mat=kit["steel"], col=col, verts=24),
        build.box(f"{name}ForkL", (0.018, 0.026, 0.068),
                  (x - 0.031, y, 0.073), (0, turn, 0),
                  mat=kit["anod"], bevel=0.003, col=col),
        build.box(f"{name}ForkR", (0.018, 0.026, 0.068),
                  (x + 0.031, y, 0.073), (0, turn, 0),
                  mat=kit["anod"], bevel=0.003, col=col),
        build.cylinder(f"{name}Wheel", 0.055, 0.052,
                       (x, y, 0.045), (0, 0, turn),
                       mat=kit["rubber"], col=col, verts=32, axis="Y"),
        build.cylinder(f"{name}Hub", 0.018, 0.058,
                       (x, y, 0.045), (0, 0, turn),
                       mat=kit["chrome"], col=col, verts=20, axis="Y"),
        build.box(f"{name}Brake", (0.052, 0.030, 0.012),
                  (x + 0.036, y - 0.012, 0.090), (0, turn, -12),
                  mat=kit["warn"], bevel=0.002, col=col),
    ]


def assemble(accent: str = shading.CYAN, carriage_y: float = -0.10):
    """Build the connected DTF system. Returns (objects, root, spec)."""
    kit = shading.machine_kit(accent)
    col = build.collection("DTFSystem")
    P = []

    printer_x = -0.53
    shaker_x = 0.75
    front_y = -0.40

    # --- shared mobile bases ------------------------------------------------
    caster_points = [
        (-1.08, -0.31, -10), (-1.08, 0.31, 8),
        (0.00, -0.31, 12), (0.00, 0.31, -6),
        (0.37, -0.31, -8), (0.37, 0.31, 11),
        (1.13, -0.31, 7), (1.13, 0.31, -12),
    ]
    for i, (x, y, turn) in enumerate(caster_points):
        P += _caster(f"Caster{i}", x, y, kit, col, turn)

    P.append(build.box("PrinterPlinth", (1.36, 0.70, 0.12),
                       (printer_x, 0, 0.18), mat=kit["frame"],
                       bevel=0.012, col=col))
    P.append(build.box("ShakerPlinth", (0.94, 0.70, 0.12),
                       (shaker_x, 0, 0.18), mat=kit["frame"],
                       bevel=0.012, col=col))

    # --- Unit A: printer cabinet -------------------------------------------
    # Closed lower cabinet, front split into two panels and one accent inlay.
    P.append(build.box("PrinterCore", (1.34, 0.72, 0.91),
                       (printer_x, 0, 0.69), mat=kit["body"],
                       bevel=0.020, segments=3, col=col))
    P.append(build.box("PrinterTopShell", (1.30, 0.69, 0.18),
                       (printer_x, 0, 1.16), mat=kit["body_light"],
                       bevel=0.025, segments=3, col=col))
    P.append(build.box("PrinterFrontUpper", (1.25, 0.030, 0.30),
                       (printer_x, front_y + 0.026, 0.91),
                       mat=kit["body"], bevel=0.008, col=col))
    P.append(build.box("PrinterFrontLower", (1.25, 0.028, 0.38),
                       (printer_x, front_y + 0.028, 0.49),
                       mat=kit["body"], bevel=0.008, col=col))
    P.append(build.box("OperatorAccentInlay", (1.20, 0.036, 0.012),
                       (printer_x, front_y + 0.006, 0.705),
                       mat=kit["accent"], bevel=0.002, col=col))
    P.append(build.bolt_row("PrinterPanelFasteners", 6, 0.19, 0.007, 0.006,
                            (-1.02, front_y - 0.014, 0.61), (90, 0, 0),
                            mat=kit["steel"], col=col, axis=(1, 0, 0)))

    # Smoked print window with a fully modelled carriage behind it.
    for tag, size, loc in (
        ("Top", (0.80, 0.028, 0.028), (-0.55, front_y - 0.003, 1.116)),
        ("Bottom", (0.80, 0.028, 0.028), (-0.55, front_y - 0.003, 0.884)),
        ("Left", (0.028, 0.028, 0.21), (-0.936, front_y - 0.003, 1.00)),
        ("Right", (0.028, 0.028, 0.21), (-0.164, front_y - 0.003, 1.00)),
    ):
        P.append(build.box(f"PrintWindowBezel{tag}", size, loc,
                           mat=kit["trim"], bevel=0.006, col=col))
    P.append(build.box("PrintWindowGlass", (0.75, 0.014, 0.215),
                       (-0.55, front_y - 0.020, 1.00), mat=kit["glass"],
                       bevel=0.005, col=col))
    P.append(build.box("InternalPlaten", (0.55, 0.64, 0.055),
                       (-0.49, 0, 0.84), mat=kit["bed"],
                       bevel=0.005, col=col))
    P += parts.linear_rail("InternalYRail", 0.58,
                           (-0.50, carriage_y, 1.04), kit, col,
                           axis="Y", width=0.032, height=0.025)
    P += parts.print_carriage("InternalCarriage",
                              (-0.50, carriage_y, 1.00), kit, col,
                              heads=SPEC["heads"], width=0.26, depth=0.29,
                              height=0.17, uv=False)
    P.append(build.box("CarriageVisibilityPanel", (0.19, 0.035, 0.095),
                       (-0.50, -0.265, 1.01), mat=kit["body_light"],
                       bevel=0.005, col=col))
    P += parts.cable_chain("InternalChain", 0.50,
                           (-0.34, 0.06, 1.13), kit, col,
                           axis="Y", link=0.042, w=0.038, h=0.040)

    # PET feed roll at the back/left; the off-centre roll is visibly part-used.
    P.append(build.cylinder("PETFeedCore", 0.035, 0.70,
                            (-1.06, 0.05, 0.83), mat=kit["steel"],
                            col=col, verts=28, axis="Y"))
    P.append(build.cylinder("PETFeedRoll", 0.135, 0.62,
                            (-1.06, 0.08, 0.83), mat=kit["body_light"],
                            col=col, verts=52, axis="Y"))
    for y, tag in ((-0.30, "Front"), (0.40, "Back")):
        P.append(build.box(f"PETBracket{tag}", (0.18, 0.12, 0.25),
                           (-1.06, y, 0.78), mat=kit["frame"],
                           bevel=0.006, col=col))
        P.append(build.cylinder(f"PETBearing{tag}", 0.045, 0.028,
                                (-1.06, y, 0.83), mat=kit["anod"],
                                col=col, verts=22, axis="Y"))

    # White-ink circulation pot and the adjacent CMYK+W bottle bay.
    P.append(build.box("InkServiceBay", (0.54, 0.055, 0.39),
                       (-0.72, front_y - 0.004, 0.45), mat=kit["anod"],
                       bevel=0.010, col=col))
    P.append(build.cylinder("WhiteCirculationTank", 0.090, 0.25,
                            (-0.92, front_y - 0.058, 0.47),
                            mat=kit["ink_w"], col=col, verts=36))
    P.append(build.cylinder("WhiteTankCap", 0.042, 0.035,
                            (-0.92, front_y - 0.058, 0.615),
                            mat=kit["trim"], col=col, verts=20))
    for i, key in enumerate(("ink_c", "ink_m", "ink_y", "ink_k", "ink_w")):
        x = -0.77 + i * 0.091
        P.append(build.cylinder(f"InkBottle{i}", 0.034, 0.19,
                                (x, front_y - 0.060, 0.45),
                                mat=kit[key], col=col, verts=20))
        P.append(build.cylinder(f"InkCap{i}", 0.016, 0.025,
                                (x, front_y - 0.060, 0.557),
                                mat=kit["trim"], col=col, verts=14))
    P.append(build.tube("WhiteInkLoop", 0.046, 0.035, 0.018,
                        (-0.92, front_y - 0.075, 0.59), (90, 0, 0),
                        verts=28, mat=kit["ink_w"], col=col))

    P.append(build.box("PrinterControl", (0.24, 0.055, 0.18),
                       (-0.03, front_y - 0.005, 1.07),
                       mat=kit["body"], bevel=0.010, col=col))
    P.append(build.box("PrinterScreen", (0.14, 0.012, 0.085),
                       (-0.06, front_y - 0.040, 1.08),
                       mat=kit["screen"], bevel=0.004, col=col))
    for i, key in enumerate(("status", "warn", "estop")):
        P.append(build.cylinder(f"PrinterButton{i}",
                                0.013 if i < 2 else 0.019, 0.010,
                                (0.055 + i * 0.045, front_y - 0.041, 1.07),
                                mat=kit[key], col=col, verts=18, axis="Y"))
    P += parts.vent_grille("PrinterVent", (0.30, 0.14),
                           (-1.03, front_y - 0.006, 0.31),
                           kit, col, rot=(90, 0, 0))

    # --- continuous PET film: feed, platen, bridge, and heat tunnel --------
    P.append(_film_ribbon(
        "PETFilm", SPEC["print_width"],
        [(-1.06, 0.97), (-0.94, 0.89), (-0.70, 0.85),
         (-0.15, 0.84), (0.14, 0.82), (0.29, 0.89),
         (0.55, 0.96), (0.98, 0.92)],
        0.0, kit["body_light"], col))
    # Printed CMYK bands deliberately continue across the bridge.
    band_c = _film_ribbon("FilmBandC", 0.13,
                          [(-0.18, 0.846), (0.14, 0.826),
                           (0.29, 0.896), (0.66, 0.966)],
                          -0.18, kit["ink_c"], col)
    band_m = _film_ribbon("FilmBandM", 0.12,
                          [(-0.18, 0.848), (0.14, 0.828),
                           (0.29, 0.898), (0.66, 0.968)],
                          0.00, kit["ink_m"], col)
    P += [band_c, band_m]
    P.append(build.box("FilmBridgeFrame", (0.18, 0.72, 0.055),
                       (0.23, 0, 0.77), mat=kit["anod"],
                       bevel=0.005, col=col))
    P.append(build.box("BridgePrintedPatch", (0.145, 0.31, 0.008),
                       (0.225, -0.12, 0.872), (0, -18, 0),
                       mat=kit["ink_c"], bevel=0.002, col=col))
    P.append(build.cylinder("BridgeGuide", 0.024, 0.68,
                            (0.27, 0, 0.86), mat=kit["chrome"],
                            col=col, verts=24, axis="Y"))

    # --- Unit B: shaker, powder hopper, oven, and extraction ----------------
    P.append(build.box("ShakerCore", (0.94, 0.72, 1.24),
                       (shaker_x, 0, 0.82), mat=kit["body"],
                       bevel=0.018, segments=3, col=col))
    P.append(build.box("ShakerUpperPanel", (0.88, 0.030, 0.39),
                       (shaker_x, front_y + 0.026, 1.20),
                       mat=kit["body"], bevel=0.009, col=col))
    P.append(build.box("ShakerLowerPanel", (0.88, 0.028, 0.42),
                       (shaker_x, front_y + 0.028, 0.48),
                       mat=kit["body"], bevel=0.009, col=col))
    P.append(build.box("HeatTunnel", (0.78, 0.59, 0.34),
                       (shaker_x, 0.02, 0.94), mat=kit["anod"],
                       bevel=0.012, col=col))
    # Amber luminous chamber is behind the glazing, never used as exterior trim.
    P.append(build.box("AmberOvenGlow", (0.68, 0.020, 0.27),
                       (shaker_x, front_y + 0.018, 0.96),
                       mat=kit["beacon_a"], bevel=0.008, col=col))
    for tag, size, loc in (
        ("Top", (0.74, 0.026, 0.034), (shaker_x, front_y - 0.004, 1.103)),
        ("Bottom", (0.74, 0.026, 0.034), (shaker_x, front_y - 0.004, 0.817)),
        ("Left", (0.034, 0.026, 0.27), (shaker_x - 0.353, front_y - 0.004, 0.96)),
        ("Right", (0.034, 0.026, 0.27), (shaker_x + 0.353, front_y - 0.004, 0.96)),
    ):
        P.append(build.box(f"ShakerWindowBezel{tag}", size, loc,
                           mat=kit["trim"], bevel=0.007, col=col))
    P.append(build.box("ShakerWindow", (0.67, 0.014, 0.25),
                       (shaker_x, front_y - 0.020, 0.96),
                       mat=kit["glass"], bevel=0.006, col=col))
    P.append(build.bolt_row("WindowFasteners", 5, 0.14, 0.007, 0.006,
                            (0.47, front_y - 0.030, 1.13), (90, 0, 0),
                            mat=kit["steel"], col=col, axis=(1, 0, 0)))

    P.append(_frustum("PowderHopper", (0.32, 0.30), (0.62, 0.54), 0.24,
                      (shaker_x - 0.05, 0.02, 1.54),
                      kit["body_light"], col))
    P.append(build.box("HopperLid", (0.65, 0.57, 0.045),
                       (shaker_x - 0.05, 0.02, 1.68),
                       mat=kit["body_light"], bevel=0.012, col=col))
    P.append(build.cylinder("PowderAgitator", 0.085, 0.16,
                            (0.98, 0.02, 1.50), mat=kit["anod"],
                            col=col, verts=32, axis="X"))
    P.append(build.cylinder("AgitatorHub", 0.037, 0.19,
                            (0.98, 0.02, 1.50), mat=kit["chrome"],
                            col=col, verts=20, axis="X"))

    # Short, readable extraction chimney with a rain-cap style hood.
    P.append(build.cylinder("ExtractionDuct", 0.105, 0.30,
                            (1.02, 0.19, 1.57), mat=kit["alu"],
                            col=col, verts=36))
    P.append(build.cylinder("DuctCollar", 0.135, 0.050,
                            (1.02, 0.19, 1.43), mat=kit["anod"],
                            col=col, verts=32))
    P.append(build.box("DuctHood", (0.30, 0.30, 0.075),
                       (1.02, 0.19, 1.75), mat=kit["body_light"],
                       bevel=0.018, segments=3, col=col))
    P += parts.vent_grille("ExtractionVent", (0.35, 0.16),
                           (shaker_x, front_y - 0.005, 0.35),
                           kit, col, rot=(90, 0, 0))
    P += parts.status_beacon("ShakerBeacon", (0.39, 0.29, 1.40),
                             kit, col, post_h=0.12)
    P += parts.estop("ShakerEStop", (1.06, front_y - 0.016, 1.26),
                     kit, col, rot=(90, 0, 0))
    P.append(build.box("ShakerBrandPlate", (0.29, 0.014, 0.072),
                       (0.59, front_y - 0.017, 1.28),
                       mat=kit["anod"], bevel=0.004, col=col))

    root = build.empty("D600_Root", col=col)
    build.parent_to(P, root)
    return P, root, SPEC


def camera_shots():
    """Named stills — azimuth, elevation, lens."""
    return {
        "hero": (38, 15, 70),
        "three-quarter": (58, 20, 82),
        "front": (0, 8, 90),
        "detail-bridge": (-24, 17, 118),
        "detail-shaker": (44, 22, 115),
    }
