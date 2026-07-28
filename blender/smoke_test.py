"""Exercise every helper in lib/ against the installed Blender before we depend on it.

Run:  blender --background --factory-startup --python blender/smoke_test.py
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import bpy  # noqa: E402
from mathutils import Vector  # noqa: E402

from lib import build, shading, studio  # noqa: E402

OUT = HERE.parent / "docs" / "_smoke"


def main() -> None:
    print(f"blender {bpy.app.version_string}")
    build.reset_scene()
    col = build.collection("Test")
    kit = shading.machine_kit()
    print(f"materials: {len(kit)} -> {sorted(kit)}")

    parts = [
        build.box("Body", (1.2, 0.8, 0.6), (0, 0, 0), mat=kit["body"],
                  col=col, anchor="bottom"),
        build.box("Accent", (1.24, 0.06, 0.05), (0, -0.42, 0.52), mat=kit["accent"],
                  col=col),
        build.cylinder("Roller", 0.06, 1.1, (0, 0, 0.72), mat=kit["steel"],
                       col=col, axis="X"),
        build.tube("Ring", 0.10, 0.07, 0.04, (0.5, 0, 0.75), mat=kit["chrome"],
                   col=col),
        build.profile_beam("Beam", 1.4, 0.10, 0.14, loc=(0, 0.3, 0.95),
                           mat=kit["alu"], col=col, axis="X"),
        build.bolt_row("Bolts", 5, 0.2, 0.012, 0.008, (-0.4, -0.41, 0.3),
                       rot=(90, 0, 0), mat=kit["anod"], col=col),
        build.plane("Screen", (0.30, 0.20), (0.62, -0.30, 0.75), rot=(70, 0, 20),
                    mat=kit["screen"], col=col),
    ]
    vent = build.box("Vent", (0.4, 0.02, 0.3), (-0.3, 0.41, 0.35),
                     mat=kit["vent"], col=col)
    parts.append(vent)

    root = build.empty("MachineRoot", col=col)
    build.parent_to(parts, root)

    rig = studio.setup_studio(machine_width=1.4, machine_height=1.0)
    print(f"lights: {sorted(rig['lights'])}  sweep={rig['floor'] is not None}")

    lo, hi = build.bounds(parts)
    centre = (lo + hi) / 2
    cam = studio.add_camera(centre, distance=4.0, azimuth_deg=38, elevation_deg=15)
    studio.frame_subject(cam, parts)

    info = studio.report(parts)
    print(f"report: {info}")

    # Fast EEVEE preview only — a Cycles job would fight the GPU with the game.
    studio.configure_render(engine="BLENDER_EEVEE_NEXT", width=900, height=620,
                            device="CPU")
    OUT.mkdir(parents=True, exist_ok=True)
    studio.render_to(OUT / "smoke.png")
    print(f"rendered -> {OUT / 'smoke.png'}")

    glb = studio.export_glb(parts, OUT / "smoke.glb")
    print(f"glb {glb.stat().st_size / 1024:.1f} KB -> {glb}")
    print("SMOKE_OK")


if __name__ == "__main__":
    main()
