"""Maven R-Series — 3.2 m industrial UV roll-to-roll / hybrid printer.

The silhouette follows the 3.2 m DOCAN-class machines from the catalogue
research, compressed to a five-metre website-friendly chassis while keeping the
full media width.  X is print width, -Y is the operator side, and Z is up.
"""

from __future__ import annotations

import bpy

from lib import build, parts, shading

SPEC = {
    "key": "roll-uv",
    "series": "R",
    "print_width": 3.20,
    "overall": (5.00, 1.40, 1.60),
    "roll_capacity_t": (1, 2),
    "channels": 7,
    "heads": 12,
    "power_kw": 15,
}


def _media_web(name, width, path, mat, col):
    """A gently faceted sheet following a Y/Z path across the full roll width."""
    x_steps = 16
    verts = []
    for y, z in path:
        for i in range(x_steps + 1):
            x = -width / 2 + width * i / x_steps
            verts.append((x, y, z))
    faces = []
    row = x_steps + 1
    for j in range(len(path) - 1):
        for i in range(x_steps):
            a = j * row + i
            faces.append((a, a + 1, a + 1 + row, a + row))
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.materials.append(mat)
    obj = bpy.data.objects.new(name, me)
    col.objects.link(obj)
    build.solidify(obj, thickness=0.004, offset=0.0)
    build.add_bevel(obj, 0.002, 2)
    return obj


def _roll_station(name, x, y, z, length, roll_r, kit, col):
    out = [
        build.cylinder(f"{name}Core", 0.052, length + 0.22, (x, y, z),
                       mat=kit["steel"], col=col, verts=32, axis="X"),
        build.cylinder(f"{name}Media", roll_r, length, (x, y, z),
                       mat=kit["body_light"], col=col, verts=64, axis="X"),
    ]
    for sign, tag in ((-1, "L"), (1, "R")):
        bx = x + sign * (length / 2 + 0.10)
        out += [
            build.box(f"{name}Bracket{tag}", (0.16, 0.20, 0.34),
                      (bx, y, z - 0.10), mat=kit["frame"],
                      bevel=0.008, col=col),
            build.cylinder(f"{name}Bearing{tag}", 0.072, 0.026,
                           (bx - sign * 0.084, y, z), mat=kit["anod"],
                           col=col, verts=24, axis="X"),
            build.cylinder(f"{name}Hub{tag}", 0.035, 0.045,
                           (bx - sign * 0.10, y, z), mat=kit["chrome"],
                           col=col, verts=20, axis="X"),
        ]
    return out


def assemble(accent: str = shading.CYAN, carriage_x: float = 0.48):
    """Build the roll printer. Returns (objects, root, spec)."""
    kit = shading.machine_kit(accent)
    col = build.collection("RollUV")
    P = []

    LX, LY, LZ = SPEC["overall"]
    half_x = LX / 2
    deck_z = 0.91
    media_w = SPEC["print_width"]

    # --- floor frame and closed lower cabinet ------------------------------
    rail_x = 4.56
    for y, tag in ((-0.50, "Front"), (0.50, "Back")):
        P.append(build.profile_beam(f"LowerRail{tag}", rail_x, 0.12, 0.12,
                                    loc=(0, y, 0.20), mat=kit["frame"],
                                    col=col, axis="X"))
        P.append(build.profile_beam(f"UpperRail{tag}", rail_x, 0.13, 0.14,
                                    loc=(0, y, 0.76), mat=kit["frame"],
                                    col=col, axis="X"))
    for x, tag in ((-2.16, "L"), (-0.78, "ML"), (0.78, "MR"), (2.16, "R")):
        for y, side in ((-0.50, "F"), (0.50, "B")):
            P.append(build.box(f"Leg{tag}{side}", (0.13, 0.13, 0.58),
                               (x, y, 0.49), mat=kit["frame"],
                               bevel=0.006, col=col))
    P += parts.levelling_feet(
        kit, col,
        [(x, y) for x in (-2.16, -0.78, 0.78, 2.16) for y in (-0.50, 0.50)],
        height=0.10, name="Level")

    # Closed panels eliminate the empty-frame view.  The front is split by one
    # long shut line; only this operator face carries an accent inlay.
    panel_x = 4.42
    upper_h, lower_h, shut = 0.24, 0.34, 0.012
    upper_z, lower_z = 0.72, 0.42
    for y, tag in ((-0.555, "Front"), (0.555, "Back")):
        P.append(build.box(f"CabUpper{tag}", (panel_x, 0.035, upper_h),
                           (0, y, upper_z), mat=kit["body"],
                           bevel=0.005, col=col))
        P.append(build.box(f"CabLower{tag}", (panel_x, 0.032, lower_h),
                           (0, y, lower_z), mat=kit["body"],
                           bevel=0.005, col=col))
    P.append(build.box("OperatorAccentInlay", (panel_x - 0.10, 0.040, 0.012),
                       (0, -0.558, 0.585), mat=kit["accent"],
                       bevel=0.002, col=col))
    for x, tag in ((-2.225, "Left"), (2.225, "Right")):
        P.append(build.box(f"CabEnd{tag}", (0.040, 1.08, 0.60),
                           (x, 0, 0.56), mat=kit["body"],
                           bevel=0.006, col=col))
        P.append(build.box(f"EndCap{tag}", (0.18, 1.17, 0.24),
                           (x, 0, 0.84), mat=kit["body_light"],
                           bevel=0.025, segments=3, col=col))
    P.append(build.box("CabinetTop", (4.46, 1.10, 0.045), (0, 0, 0.865),
                       mat=kit["body"], bevel=0.005, col=col))

    P += parts.vent_grille("PowerVent", (0.52, 0.20),
                           (-1.45, -0.576, lower_z), kit, col,
                           rot=(90, 0, 0))
    P += parts.vent_grille("LampVent", (0.52, 0.20),
                           (1.45, -0.576, lower_z), kit, col,
                           rot=(90, 0, 0))
    P.append(build.bolt_row("FrontFasteners", 16, 0.265, 0.009, 0.008,
                            (-1.99, -0.580, 0.77), (90, 0, 0),
                            mat=kit["steel"], col=col, axis=(1, 0, 0)))

    # --- platen, rolls, tension control, and the hero media web ------------
    P.append(build.box("HeatedPlaten", (3.50, 0.54, 0.10), (0, -0.02, deck_z),
                       mat=kit["bed"], bevel=0.006, col=col))
    P.append(build.box("PlatenFrontHeater", (3.42, 0.10, 0.055),
                       (0, -0.33, deck_z - 0.015), mat=kit["anod"],
                       bevel=0.004, col=col))
    P.append(build.box("PlatenRearHeater", (3.42, 0.10, 0.055),
                       (0, 0.31, deck_z - 0.015), mat=kit["anod"],
                       bevel=0.004, col=col))

    # A heavy, partially used feed roll and a deliberately smaller take-up roll
    # make the material path directional rather than symmetrical.
    P += _roll_station("Unwind", 0, 0.49, 0.56, media_w + 0.08, 0.225,
                       kit, col)
    P += _roll_station("TakeUp", 0, -0.52, 0.50, media_w + 0.08, 0.145,
                       kit, col)
    for y, z, r, tag in ((0.49, 0.56, 0.225, "Feed"),
                         (-0.52, 0.50, 0.145, "Take")):
        for sign, side in ((-1, "L"), (1, "R")):
            P.append(build.cylinder(f"{tag}RollCollar{side}", r + 0.012, 0.025,
                                    (sign * (media_w / 2 + 0.052), y, z),
                                    mat=kit["rubber"], col=col, verts=40,
                                    axis="X"))
    for y, z, name, r in (
        (0.27, 0.73, "RearTension", 0.038),
        (0.12, 0.81, "RearDancer", 0.052),
        (-0.35, 0.76, "FrontDancer", 0.047),
        (-0.47, 0.65, "FrontTension", 0.034),
    ):
        P.append(build.cylinder(name, r, media_w + 0.12, (0, y, z),
                                mat=kit["chrome"], col=col, verts=32, axis="X"))
        for sign, tag in ((-1, "L"), (1, "R")):
            P.append(build.box(f"{name}Arm{tag}", (0.055, 0.16, 0.20),
                               (sign * 1.72, y, z - 0.05),
                               (18 if sign < 0 else -18, 0, 0),
                               mat=kit["frame"], bevel=0.005, col=col))

    P.append(_media_web(
        "BannerWeb", media_w,
        [(0.49, 0.77), (0.34, 0.76), (0.20, 0.82), (0.10, 0.91),
         (-0.20, 0.965), (-0.34, 0.79), (-0.46, 0.67), (-0.52, 0.64)],
        kit["body_light"], col))
    # A printed swatch riding on the pale web reinforces that this is media,
    # without adding a second family accent stripe to the machine body.
    swatch_c = _media_web(
        "PrintedSwatchC", 0.72,
        [(-0.18, 0.969), (-0.25, 0.91), (-0.34, 0.795),
         (-0.46, 0.672), (-0.50, 0.652)],
        kit["accent"], col)
    swatch_c.location.x = -0.84
    P.append(swatch_c)
    swatch_m = _media_web(
        "PrintedSwatchM", 0.50,
        [(-0.19, 0.971), (-0.26, 0.90), (-0.34, 0.797),
         (-0.46, 0.674), (-0.50, 0.654)],
        kit["ink_m"], col)
    swatch_m.location.x = 0.16
    P.append(swatch_m)
    swatch_y = _media_web(
        "PrintedSwatchY", 0.42,
        [(-0.20, 0.973), (-0.27, 0.89), (-0.35, 0.799),
         (-0.46, 0.676), (-0.50, 0.656)],
        kit["ink_y"], col)
    swatch_y.location.x = 0.90
    P.append(swatch_y)

    # --- full-width gantry and print system --------------------------------
    column_x = 1.88
    for x, tag in ((-column_x, "L"), (column_x, "R")):
        P.append(build.box(f"GantryColumn{tag}", (0.30, 0.46, 0.66),
                           (x, 0.02, 1.14), mat=kit["body"],
                           bevel=0.010, col=col))
        P += parts.bearing_block(f"GantryFoot{tag}", (x, 0.02, 0.885),
                                 kit, col, size=(0.28, 0.34, 0.08))
    P.append(build.profile_beam("GantryBeam", 3.86, 0.24, 0.30,
                                loc=(0, 0.04, 1.36), mat=kit["alu"],
                                col=col, axis="X"))
    P.append(build.box("GantryFascia", (3.72, 0.035, 0.14),
                       (0, -0.105, 1.41), mat=kit["body"],
                       bevel=0.004, col=col))
    P += parts.linear_rail("CarriageRail", 3.48, (0, -0.128, 1.27),
                           kit, col, axis="X", width=0.042, height=0.030)
    P += parts.print_carriage("Carriage", (carriage_x, -0.20, 1.19),
                              kit, col, heads=SPEC["heads"], width=0.70,
                              depth=0.25, height=0.27, uv=True)
    P += parts.cable_chain("EnergyChain", 3.08, (0.12, 0.17, 1.49),
                           kit, col, axis="X", link=0.055, w=0.060, h=0.068)

    # --- ink, control, and service detail ----------------------------------
    P += parts.ink_station("BulkInk", (-1.70, 0.13, 0.90), kit, col,
                           channels=SPEC["channels"], bottle_r=0.043,
                           bottle_h=0.23)
    P += parts.control_console("Console", (2.27, -0.58, 0.68), kit, col,
                               screen_w=0.31, screen_h=0.21, post_h=0.43,
                               yaw_deg=-18)
    P += parts.status_beacon("Beacon", (2.00, 0.36, 1.43), kit, col,
                             post_h=0.16)
    P += parts.estop("EStop", (1.74, -0.578, 0.72), kit, col,
                     rot=(90, 0, 0))
    P.append(build.box("DriveMotor", (0.30, 0.28, 0.29),
                       (-2.05, -0.18, 0.30), mat=kit["frame"],
                       bevel=0.010, col=col))
    P.append(build.cylinder("DriveMotorFan", 0.095, 0.035,
                            (-2.05, -0.335, 0.30), mat=kit["vent"],
                            col=col, verts=32, axis="Y"))
    P.append(build.box("BrandPlate", (0.46, 0.018, 0.09),
                       (-1.67, -0.582, 0.71), mat=kit["anod"],
                       bevel=0.004, col=col))

    root = build.empty("R3200_Root", col=col)
    build.parent_to(P, root)
    return P, root, SPEC


def camera_shots():
    """Named stills — azimuth, elevation, lens."""
    return {
        "hero": (36, 13, 72),
        "three-quarter": (58, 18, 82),
        "front": (0, 7, 88),
        "detail-web": (-25, 18, 118),
        "detail-carriage": (42, 22, 130),
    }
