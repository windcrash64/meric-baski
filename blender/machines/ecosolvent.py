"""Maven S-Series — 1.8 m eco-solvent roll printer with print-and-cut.

This is intentionally lighter than the UV machines: a closed benchtop printer
body on a slim wheeled tube stand, with the roll handling exposed beneath it.
"""

from __future__ import annotations

import math

import bpy

from lib import build, parts, shading

SPEC = {
    "key": "eco-solvent",
    "series": "S",
    "print_width": 1.80,
    "overall": (2.90, 0.75, 1.30),
    "heads": 4,
    "channels": 8,
    "heaters": ("pre", "print", "post"),
    "cut_speed_mm_s": 300,
}


def _sheet(name, width, path, mat, col, thickness=0.003, sag=0.0):
    """Thin roll media or basket cloth following a Y/Z section."""
    steps = 14
    verts = []
    for row_i, (y, z) in enumerate(path):
        for i in range(steps + 1):
            x = -width / 2 + width * i / steps
            centre = max(0.0, 1.0 - (2.0 * x / width) ** 2)
            ripple = math.sin(i * math.pi * 0.72 + row_i * 0.55)
            verts.append((x, y + sag * 0.08 * ripple,
                          z - sag * centre * (0.65 + row_i * 0.10)))
    faces = []
    row = steps + 1
    for j in range(len(path) - 1):
        for i in range(steps):
            a = j * row + i
            faces.append((a, a + 1, a + row + 1, a + row))
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.materials.append(mat)
    obj = bpy.data.objects.new(name, me)
    col.objects.link(obj)
    build.solidify(obj, thickness=thickness, offset=0.0)
    build.add_bevel(obj, max(0.001, thickness * 0.5), 2)
    return obj


def _caster(name, loc, kit, col, yaw=0):
    """Twin-fork industrial castor with a visible axle and rubber wheel."""
    x, y, z = loc
    return [
        build.cylinder(f"{name}Swivel", 0.040, 0.030, (x, y, z + 0.105),
                       mat=kit["steel"], col=col, verts=24),
        build.box(f"{name}ForkL", (0.020, 0.028, 0.075),
                  (x - 0.038, y, z + 0.065), (0, yaw, 0),
                  mat=kit["anod"], bevel=0.003, col=col),
        build.box(f"{name}ForkR", (0.020, 0.028, 0.075),
                  (x + 0.038, y, z + 0.065), (0, yaw, 0),
                  mat=kit["anod"], bevel=0.003, col=col),
        build.cylinder(f"{name}Wheel", 0.064, 0.060, (x, y, z + 0.042),
                       rot=(0, 0, yaw), mat=kit["rubber"], col=col,
                       verts=32, axis="Y"),
        build.cylinder(f"{name}Hub", 0.021, 0.066, (x, y, z + 0.042),
                       rot=(0, 0, yaw), mat=kit["chrome"], col=col,
                       verts=20, axis="Y"),
    ]


def assemble(accent: str = shading.MAGENTA, cutter_x: float = 0.56):
    """Build the printer/cutter. Returns (objects, root, spec)."""
    kit = shading.machine_kit(accent)
    col = build.collection("EcoSolvent")
    P = []

    body_w = 2.58
    body_bottom = 0.79
    stand_x = 1.08

    # --- slim tubular stand on castors -------------------------------------
    for x, tag in ((-stand_x, "L"), (stand_x, "R")):
        for y, side in ((-0.25, "F"), (0.25, "B")):
            P.append(build.profile_beam(f"StandLeg{tag}{side}", 0.61, 0.065,
                                        0.065, loc=(x, y, 0.46),
                                        mat=kit["frame"], col=col, axis="Z"))
        P.append(build.profile_beam(f"StandFoot{tag}", 0.64, 0.070, 0.070,
                                    loc=(x, 0, 0.16), mat=kit["frame"],
                                    col=col, axis="Y"))
        P.append(build.box(f"StandCap{tag}", (0.20, 0.58, 0.09),
                           (x, 0, body_bottom - 0.045), mat=kit["body"],
                           bevel=0.009, col=col))
    P.append(build.profile_beam("StandCrossbar", 2.10, 0.065, 0.075,
                                loc=(0, 0.19, 0.39), mat=kit["frame"],
                                col=col, axis="X"))
    P.append(build.profile_beam("StandFrontBrace", 2.10, 0.050, 0.050,
                                loc=(0, -0.22, 0.29), mat=kit["frame"],
                                col=col, axis="X"))
    for i, (x, y, yaw) in enumerate((
        (-stand_x, -0.26, -12), (-stand_x, 0.26, 9),
        (stand_x, -0.26, 15), (stand_x, 0.26, -7),
    )):
        P += _caster(f"Caster{i}", (x, y, 0), kit, col, yaw)

    # --- roll handling and cloth catch basket ------------------------------
    roll_w = 1.86
    P.append(build.cylinder("FeedRollCore", 0.038, roll_w + 0.14,
                            (0, 0.30, 0.52), mat=kit["steel"],
                            col=col, verts=32, axis="X"))
    P.append(build.cylinder("FeedMediaRoll", 0.155, roll_w,
                            (-0.05, 0.30, 0.52), mat=kit["body_light"],
                            col=col, verts=56, axis="X"))
    P.append(build.cylinder("TakeUpCore", 0.045, roll_w + 0.12,
                            (0, -0.32, 0.49), mat=kit["chrome"],
                            col=col, verts=32, axis="X"))
    P.append(build.cylinder("TakeUpMedia", 0.083, roll_w,
                            (0, -0.32, 0.49), mat=kit["body_light"],
                            col=col, verts=48, axis="X"))
    for x, tag in ((-1.04, "L"), (1.04, "R")):
        P.append(build.box(f"RollBracket{tag}", (0.12, 0.22, 0.34),
                           (x, 0.29, 0.49), mat=kit["frame"],
                           bevel=0.006, col=col))
        P.append(build.cylinder(f"RollBearing{tag}", 0.050, 0.032,
                                (x, 0.29, 0.52), mat=kit["anod"],
                                col=col, verts=24, axis="X"))
        P.append(build.box(f"TakeBracket{tag}", (0.10, 0.18, 0.27),
                           (x, -0.32, 0.44), mat=kit["frame"],
                           bevel=0.006, col=col))

    P.append(_sheet("MediaExit", 1.76,
                    [(-0.315, 0.91), (-0.345, 0.78), (-0.34, 0.63),
                     (-0.32, 0.575)], kit["body_light"], col))
    P.append(_sheet("CatchBasket", 1.91,
                    [(-0.40, 0.53), (-0.48, 0.30), (-0.39, 0.18),
                     (-0.10, 0.20)], kit["rubber"], col,
                     thickness=0.005, sag=0.065))
    for y, z, tag in ((-0.40, 0.53, "Front"), (-0.10, 0.20, "Rear")):
        P.append(build.cylinder(f"BasketBar{tag}", 0.023, 2.02,
                                (0, y, z), mat=kit["steel"], col=col,
                                verts=24, axis="X"))
    for y, z, r, tag in ((0.30, 0.52, 0.155, "Feed"),
                         (-0.32, 0.49, 0.083, "Take")):
        for sign, side in ((-1, "L"), (1, "R")):
            P.append(build.cylinder(f"{tag}Collar{side}", r + 0.010, 0.024,
                                    (sign * (roll_w / 2 + 0.014), y, z),
                                    mat=kit["rubber"], col=col, verts=36,
                                    axis="X"))

    # --- closed printer body ------------------------------------------------
    P.append(build.box("MainLowerShell", (body_w, 0.57, 0.29),
                       (0, 0, 0.925), mat=kit["body"],
                       bevel=0.018, segments=3, col=col))
    P.append(build.box("MainRearShell", (body_w - 0.05, 0.18, 0.39),
                       (0, 0.20, 1.08), mat=kit["body"],
                       bevel=0.014, segments=3, col=col))
    P.append(build.box("MainTop", (body_w - 0.10, 0.45, 0.11),
                       (0, 0.02, 1.255), mat=kit["body_light"],
                       bevel=0.024, segments=3, col=col))
    for x, tag in ((-1.285, "Left"), (1.285, "Right")):
        P.append(build.box(f"EndHousing{tag}", (0.14, 0.60, 0.47),
                           (x, 0, 1.03), mat=kit["body_light"],
                           bevel=0.030, segments=3, col=col))

    # Hinged cover, three-layer glazing, and a deep media/cutter opening.
    P.append(build.box("HingedFrontCover", (2.20, 0.085, 0.295),
                       (-0.08, -0.275, 1.105), (-7, 0, 0),
                       mat=kit["body"], bevel=0.016, segments=3, col=col))
    P.append(build.box("WindowBezel", (1.78, 0.024, 0.145),
                       (-0.16, -0.329, 1.125), (-7, 0, 0),
                       mat=kit["trim"], bevel=0.007, col=col))
    P.append(build.box("SafetyWindow", (1.70, 0.014, 0.105),
                       (-0.16, -0.344, 1.128), (-7, 0, 0),
                       mat=kit["glass"], bevel=0.004, col=col))
    P.append(build.box("MediaExitSlot", (2.12, 0.052, 0.090),
                       (-0.07, -0.318, 0.930), mat=kit["trim"],
                       bevel=0.010, col=col))

    # Horizontal shut line and exactly one operator-side accent inlay.
    P.append(build.box("OperatorAccentInlay", (2.17, 0.020, 0.012),
                       (-0.07, -0.349, 0.995), mat=kit["accent"],
                       bevel=0.002, col=col))
    P.append(build.bolt_row("CoverFasteners", 11, 0.19, 0.0065, 0.006,
                            (-1.01, -0.349, 1.245), (90, 0, 0),
                            mat=kit["steel"], col=col, axis=(1, 0, 0)))

    # --- print/cut motion and tri-zone heat --------------------------------
    P += parts.linear_rail("InternalRail", 1.92, (-0.12, -0.305, 1.115),
                           kit, col, axis="X", width=0.032, height=0.025)
    P += parts.print_carriage("PrintCarriage", (-0.34, -0.323, 1.105),
                              kit, col, heads=SPEC["heads"], width=0.34,
                              depth=0.13, height=0.13, uv=False)
    P.append(build.box("CutCarriage", (0.115, 0.105, 0.14),
                       (cutter_x, -0.337, 1.102), mat=kit["anod"],
                       bevel=0.006, col=col))
    P.append(build.cylinder("CutBladeHolder", 0.018, 0.095,
                            (cutter_x, -0.352, 1.00), mat=kit["chrome"],
                            col=col, verts=20))
    P += parts.cable_chain("HeadChain", 1.55, (-0.10, 0.12, 1.185),
                           kit, col, axis="X", link=0.048,
                           w=0.042, h=0.045)
    for i, (y, key, tag) in enumerate((
        (-0.245, "anod", "Pre"), (-0.285, "bed", "Print"),
        (-0.326, "anod", "Post"),
    )):
        P.append(build.box(f"{tag}Heater", (1.92, 0.035, 0.025),
                           (-0.10, y, 0.900 + i * 0.006),
                           mat=kit[key], bevel=0.003, col=col))

    # --- visible cartridge bay and compact control panel -------------------
    P.append(build.box("CartridgeBay", (0.37, 0.065, 0.29),
                       (1.04, -0.327, 1.105), mat=kit["anod"],
                       bevel=0.008, col=col))
    ink_keys = ("ink_c", "ink_m", "ink_y", "ink_k",
                "ink_c", "ink_m", "ink_y", "ink_k")
    for i, key in enumerate(ink_keys):
        x = 0.885 + (i % 4) * 0.080
        z = 1.045 + (i // 4) * 0.120
        P.append(build.box(f"Cartridge{i}", (0.055, 0.045, 0.095),
                           (x, -0.370, z), mat=kit[key],
                           bevel=0.006, col=col))
        P.append(build.box(f"CartridgeGrip{i}", (0.029, 0.012, 0.018),
                           (x, -0.398, z + 0.036), mat=kit["trim"],
                           bevel=0.002, col=col))

    P.append(build.box("ControlPanel", (0.29, 0.075, 0.16),
                       (1.05, -0.335, 1.245), (-8, 0, 0),
                       mat=kit["body"], bevel=0.012, col=col))
    P.append(build.box("ControlScreen", (0.145, 0.015, 0.080),
                       (0.995, -0.381, 1.255), (-8, 0, 0),
                       mat=kit["screen"], bevel=0.004, col=col))
    for i, key in enumerate(("status", "warn", "estop")):
        P.append(build.cylinder(f"PanelButton{i}", 0.016 if i < 2 else 0.021,
                                0.012, (1.095 + i * 0.046, -0.382, 1.245),
                                mat=kit[key], col=col, verts=20, axis="Y"))
    P += parts.vent_grille("ElectronicsVent", (0.28, 0.14),
                           (-1.06, -0.324, 0.855), kit, col,
                           rot=(90, 0, 0))
    P.append(build.box("BrandPlate", (0.35, 0.014, 0.070),
                       (-0.98, -0.349, 1.01), mat=kit["anod"],
                       bevel=0.004, col=col))

    root = build.empty("S1800_Root", col=col)
    build.parent_to(P, root)
    return P, root, SPEC


def camera_shots():
    """Named stills — azimuth, elevation, lens."""
    return {
        "hero": (38, 14, 72),
        "three-quarter": (60, 18, 86),
        "front": (0, 8, 92),
        "detail-cut": (-30, 19, 128),
        "detail-ink": (55, 20, 120),
    }
