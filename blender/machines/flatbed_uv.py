"""Maven F-Series — 2500 x 1300 mm industrial UV LED flatbed.

Proportions follow the real class of machine this sits in (Mimaki JFX200-2513 is
4400 x 2450 x 1250 mm over a 2500 x 1300 bed), so the model reads at the right
scale next to a person or a 3 m sheet.

Nothing here is a copy of any manufacturer's industrial design — the silhouette
is our own, built from the generic vocabulary every flatbed shares.
"""

from __future__ import annotations

import math

from lib import build, parts, shading

SPEC = {
    "key": "flatbed-uv",
    "series": "F",
    "print_x": 2.50,
    "print_y": 1.30,
    "overall": (4.40, 2.45, 1.25),
    "table_h": 0.90,
    "channels": 6,
    "heads": 6,
}


def assemble(accent: str = shading.CYAN, gantry_x: float = -0.42):
    """Build the machine. Returns (objects, root, spec)."""
    kit = shading.machine_kit(accent)
    col = build.collection("FlatbedUV")
    P = []

    LX, LY, LZ = SPEC["overall"]
    TH = SPEC["table_h"]
    half_x, half_y = LX / 2, LY / 2

    # --- bed ----------------------------------------------------------------
    bed_x, bed_y = 3.05, 1.62
    P.append(build.box("BedPlate", (bed_x, bed_y, 0.055), (0, 0, TH - 0.0275),
                       mat=kit["alu"], bevel=0.004, col=col))
    # The vacuum field is a recessed, darker panel inside a bright machined
    # surround. Without that tonal step the whole bed renders as one grey sheet.
    vac_x, vac_y = SPEC["print_x"] + 0.07, SPEC["print_y"] + 0.07
    P.append(build.box("VacuumField", (vac_x, vac_y, 0.020), (0, 0, TH - 0.013),
                       mat=kit["bed"], bevel=0.002, col=col))
    # Two vacuum zones, divided on the X axis — matches the class's 2-zone table.
    P.append(build.box("ZoneSplit", (0.016, vac_y, 0.022), (0, 0, TH - 0.011),
                       mat=kit["alu"], bevel=0.0015, col=col))
    for i, (sx, sy, ox, oy) in enumerate([
        (vac_x + 0.05, 0.025, 0, vac_y / 2 + 0.012),
        (vac_x + 0.05, 0.025, 0, -vac_y / 2 - 0.012),
        (0.025, vac_y + 0.05, vac_x / 2 + 0.012, 0),
        (0.025, vac_y + 0.05, -vac_x / 2 - 0.012, 0),
    ]):
        P.append(build.box(f"BedTrim{i}", (sx, sy, 0.026), (ox, oy, TH - 0.010),
                           mat=kit["anod"], bevel=0.002, col=col))
    # Registration pins along the origin corner.
    for i, (px, py) in enumerate([(-SPEC["print_x"] / 2 + 0.04, -SPEC["print_y"] / 2 + 0.04),
                                  (-SPEC["print_x"] / 2 + 0.04, 0.0),
                                  (-SPEC["print_x"] / 2 + 0.04, SPEC["print_y"] / 2 - 0.04),
                                  (0.0, -SPEC["print_y"] / 2 + 0.04)]):
        P.append(build.cylinder(f"RegPin{i}", 0.009, 0.026, (px, py, TH + 0.012),
                                mat=kit["steel"], col=col, verts=14))

    # Zoned-vacuum valve levers on the operator edge (2 zones, as the class has).
    for i, zx in enumerate((-0.62, 0.62)):
        P.append(build.box(f"ZoneValve{i}", (0.09, 0.05, 0.05),
                           (zx, -bed_y / 2 - 0.03, TH - 0.06),
                           mat=kit["anod"], bevel=0.004, col=col))
        P.append(build.box(f"ZoneLever{i}", (0.015, 0.10, 0.015),
                           (zx, -bed_y / 2 - 0.075, TH - 0.045), (18, 0, 0),
                           mat=kit["accent"], bevel=0.002, col=col))

    # --- frame --------------------------------------------------------------
    for sign in (-1, 1):
        P.append(build.box(f"FrameRail{'PY' if sign > 0 else 'NY'}",
                           (LX - 0.30, 0.16, 0.22), (0, sign * 0.86, TH - 0.20),
                           mat=kit["frame"], bevel=0.005, col=col))
        P.append(build.box(f"FrameLower{'PY' if sign > 0 else 'NY'}",
                           (LX - 0.50, 0.10, 0.12), (0, sign * 0.80, 0.24),
                           mat=kit["frame"], bevel=0.004, col=col))
    for sign in (-1, 1):
        P.append(build.box(f"FrameCross{'PX' if sign > 0 else 'NX'}",
                           (0.14, 1.78, 0.20), (sign * (half_x - 0.55), 0, TH - 0.21),
                           mat=kit["frame"], bevel=0.005, col=col))

    leg_xs = (-half_x + 0.42, 0.0, half_x - 0.42)
    for i, lx in enumerate(leg_xs):
        for sign in (-1, 1):
            P.append(build.box(f"Leg{i}{'P' if sign > 0 else 'N'}",
                               (0.13, 0.13, TH - 0.40),
                               (lx, sign * 0.86, 0.09 + (TH - 0.40) / 2),
                               mat=kit["frame"], bevel=0.005, col=col))

    P += parts.levelling_feet(kit, col,
                              [(lx, sign * 0.86) for lx in leg_xs for sign in (-1, 1)])

    # --- body panels --------------------------------------------------------
    # The body is a closed volume, split by a horizontal shut line into an upper
    # and a lower panel. Leaving it open shows the empty frame interior, which is
    # the single fastest way to make a render read as a model rather than a machine.
    body_top = TH - 0.015          # panels stop just under the bed lip
    upper_h, lower_h, shut = 0.24, 0.30, 0.010
    upper_z = body_top - upper_h / 2
    lower_z = body_top - upper_h - shut - lower_h / 2
    panel_x = LX - 0.30
    side_y = 0.955

    for sign, tag in ((-1, "Front"), (1, "Back")):
        P.append(build.box(f"SkirtUpper{tag}", (panel_x, 0.030, upper_h),
                           (0, sign * side_y, upper_z),
                           mat=kit["body"], bevel=0.004, col=col))
        P.append(build.box(f"SkirtLower{tag}", (panel_x - 0.02, 0.026, lower_h),
                           (0, sign * side_y, lower_z),
                           mat=kit["body"], bevel=0.004, col=col))
    # One accent inlay, operator side only — a stripe on every face is a toy.
    P.append(build.box("SkirtAccent", (panel_x * 0.995, 0.034, 0.010),
                       (0, -side_y, body_top - upper_h - shut / 2),
                       mat=kit["accent"], bevel=0.002, col=col))

    for sign, tag in ((-1, "Left"), (1, "Right")):
        ex = sign * (half_x - 0.14)
        P.append(build.box(f"EndUpper{tag}", (0.030, side_y * 2, upper_h),
                           (ex, 0, upper_z), mat=kit["body"], bevel=0.004, col=col))
        P.append(build.box(f"EndLower{tag}", (0.026, side_y * 2 - 0.02, lower_h),
                           (ex, 0, lower_z), mat=kit["body"], bevel=0.004, col=col))
        # Deck plate closing the top between the bed and the machine end.
        deck_w = (half_x - 0.14) - bed_x / 2
        P.append(build.box(f"Deck{tag}", (deck_w, side_y * 2 - 0.02, 0.030),
                           (sign * (bed_x / 2 + deck_w / 2), 0, body_top),
                           mat=kit["body"], bevel=0.004, col=col))

    P += parts.vent_grille("VentL", (0.42, 0.18), (-1.42, -side_y - 0.012, lower_z),
                           kit, col, rot=(90, 0, 0))
    P += parts.vent_grille("VentR", (0.42, 0.18), (1.42, -side_y - 0.012, lower_z),
                           kit, col, rot=(90, 0, 0))

    # --- motion system ------------------------------------------------------
    for sign, tag in ((-1, "N"), (1, "P")):
        P += parts.linear_rail(f"RailX{tag}", LX - 0.46,
                               (0, sign * 0.86, TH + 0.055), kit, col, axis="X")

    gx = gantry_x
    for sign, tag in ((-1, "N"), (1, "P")):
        P.append(build.box(f"GantryEnd{tag}", (0.34, 0.26, 0.40),
                           (gx, sign * 0.86, TH + 0.26),
                           mat=kit["body"], bevel=0.006, col=col))
        P += parts.bearing_block(f"GantryBearing{tag}", (gx, sign * 0.86, TH + 0.085),
                                 kit, col, size=(0.26, 0.13, 0.06))

    beam_len = 1.86
    P.append(build.profile_beam("GantryBeam", beam_len, 0.26, 0.30,
                                loc=(gx, 0, TH + 0.34), mat=kit["alu"],
                                col=col, axis="Y"))
    # Fascia and carriage go on the +X face: that is the side the hero camera
    # sees, and on a real machine the head faces the finished area.
    P.append(build.box("GantryFascia", (0.030, beam_len - 0.04, 0.12),
                       (gx + 0.145, 0, TH + 0.40), mat=kit["accent"],
                       bevel=0.004, col=col))
    P += parts.linear_rail("RailY", beam_len - 0.10, (gx + 0.15, 0, TH + 0.22),
                           kit, col, axis="Y", width=0.038, height=0.026)

    # Carriage parked off centre on the beam so the machine reads as "in use".
    cy = 0.24
    P += parts.print_carriage("Carriage", (gx + 0.26, cy, TH + 0.245), kit, col,
                              heads=SPEC["heads"], width=0.42, depth=0.30,
                              height=0.28)

    # Energy chains: one along the bed for the gantry, one behind the beam.
    P += parts.cable_chain("ChainX", LX - 0.70, (0, 1.02, TH - 0.06), kit, col,
                           axis="X")
    P += parts.cable_chain("ChainY", beam_len - 0.30, (gx - 0.20, 0, TH + 0.46),
                           kit, col, axis="Y", link=0.06, w=0.045, h=0.055)

    # --- ink, control, safety ----------------------------------------------
    # Ink rack sits on the right-hand deck, back edge, clear of the operator side.
    deck_cx = bed_x / 2 + ((half_x - 0.14) - bed_x / 2) / 2
    P += parts.ink_station("Ink", (deck_cx, 0.34, body_top + 0.015), kit, col,
                           channels=SPEC["channels"], bottle_r=0.042,
                           bottle_h=0.17)

    # Console on its own post at the front-right corner, where an operator stands.
    P += parts.control_console("Console", (half_x - 0.42, -side_y - 0.07, lower_z),
                               kit, col, yaw_deg=-22, post_h=0.46,
                               screen_w=0.28, screen_h=0.19)
    P += parts.status_beacon("Beacon", (gx, 0.86, TH + 0.46), kit, col,
                             post_h=0.22)
    P += parts.estop("EStopL", (-half_x + 0.60, -side_y - 0.016, upper_z), kit, col,
                     rot=(90, 0, 0))
    P += parts.estop("EStopR", (half_x - 0.95, -side_y - 0.016, upper_z), kit, col,
                     rot=(90, 0, 0))

    # Vacuum pump, parked under the frame — machines are never a single box.
    P.append(build.box("VacPump", (0.52, 0.40, 0.34), (-1.30, 0.30, 0.30),
                       mat=kit["frame"], bevel=0.006, col=col))
    P.append(build.cylinder("VacMotor", 0.13, 0.30, (-1.30, 0.30, 0.56),
                            mat=kit["anod"], col=col, verts=24, axis="X"))

    # Brand plate on the front skirt, upper panel.
    P.append(build.box("BrandPlate", (0.46, 0.012, 0.085),
                       (-1.48, -side_y - 0.019, upper_z), mat=kit["anod"],
                       bevel=0.003, col=col))

    root = build.empty("F2513_Root", col=col)
    build.parent_to(P, root)
    return P, root, SPEC


def camera_shots():
    """Named hero angles for the stills gallery — azimuth, elevation, lens."""
    return {
        "hero": (38, 14, 70),
        "three-quarter": (58, 20, 85),
        "front": (0, 8, 85),
        "detail-carriage": (-46, 26, 135),
        "detail-ink": (96, 18, 120),
    }
