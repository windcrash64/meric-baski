"""Build, preview, render and export one machine.

  blender --background --factory-startup --python blender/build_machine.py -- \
      --machine flatbed_uv --preview
  ... --render --engine CYCLES --device GPU --samples 300 --shots hero,front
  ... --export

Renders default to EEVEE on CPU: this box is shared with gaming, and the
5 GB VRAM cap applies whenever a game is running.
"""

from __future__ import annotations

import argparse
import importlib
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import bpy  # noqa: E402
from mathutils import Vector  # noqa: E402

from lib import build, studio  # noqa: E402

OUT_RENDER = HERE.parent / "assets" / "renders"
OUT_MODEL = HERE.parent / "public" / "models"


def parse_args() -> argparse.Namespace:
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    p = argparse.ArgumentParser()
    p.add_argument("--machine", required=True)
    p.add_argument("--preview", action="store_true", help="one fast EEVEE hero frame")
    p.add_argument("--render", action="store_true")
    p.add_argument("--export", action="store_true", help="write the web GLB")
    p.add_argument("--turntable", type=int, default=0, help="orbit frame count")
    p.add_argument("--shots", default="hero")
    p.add_argument("--engine", default="BLENDER_EEVEE")
    p.add_argument("--device", default="CPU", choices=["CPU", "GPU"])
    p.add_argument("--samples", type=int, default=192)
    p.add_argument("--look", default="light", choices=sorted(studio.LOOKS))
    p.add_argument("--cutout", action="store_true",
                   help="transparent background, no sweep — sits directly on the page")
    p.add_argument("--width", type=int, default=1800)
    p.add_argument("--height", type=int, default=1200)
    p.add_argument("--no-draco", action="store_true")
    return p.parse_args(argv)


def main() -> None:
    args = parse_args()
    build.reset_scene()

    mod = importlib.import_module(f"machines.{args.machine}")
    objs, root, spec = mod.assemble()
    info = studio.report(objs)
    print(f"[{spec['key']}] objects={info['objects']} verts={info['verts']} "
          f"tris={info['tris']} size={info['size_m']} m")

    lo, hi = build.bounds(objs)
    centre = Vector(((lo.x + hi.x) / 2, (lo.y + hi.y) / 2, (lo.z + hi.z) / 2))

    if args.export:
        glb = OUT_MODEL / f"{spec['key']}.glb"
        studio.export_glb(objs, glb, draco=not args.no_draco)
        kb = glb.stat().st_size / 1024
        print(f"[export] {glb.name} {kb:.0f} KB")
        if kb > 3000:
            print(f"[warn] {glb.name} is {kb:.0f} KB — over the 3 MB web budget")

    if not (args.preview or args.render or args.turntable):
        return

    # A cutout drops the sweep so the machine can sit directly on the page's own
    # ground. On a white section a rendered grey sweep reads as a photo pasted
    # into a box, which is exactly what a product page must not look like.
    studio.setup_studio(machine_width=max(info["size_m"][0], 1.0),
                        machine_height=info["size_m"][2], look=args.look,
                        sweep=not args.cutout)

    shots = mod.camera_shots()
    wanted = ["hero"] if args.preview else [s for s in args.shots.split(",") if s]
    engine = "BLENDER_EEVEE" if args.preview else args.engine
    samples = 48 if args.preview else args.samples
    w, h = (1100, 740) if args.preview else (args.width, args.height)

    # Shadow catchers are a Cycles feature — EEVEE renders the catcher plane as
    # an ordinary opaque surface, which fills the frame instead of leaving it
    # transparent. A cutout therefore always goes through Cycles.
    if args.cutout:
        engine = "CYCLES"
        samples = max(samples, 96)

    studio.configure_render(engine=engine, samples=samples, width=w, height=h,
                            device=args.device, transparent=args.cutout)

    out_dir = OUT_RENDER / spec["key"]
    if args.cutout:
        out_dir = out_dir / "cutout"
    for shot in wanted:
        if shot not in shots:
            print(f"[warn] no such shot {shot!r}; have {sorted(shots)}")
            continue
        az, el, lens = shots[shot]
        cam = studio.add_camera(centre, distance=info["size_m"][0] * 1.6,
                                azimuth_deg=az, elevation_deg=el, lens=lens)
        studio.frame_subject(cam, objs, margin=1.10)
        path = studio.render_to(out_dir / f"{spec['key']}-{shot}.png")
        print(f"[render] {path}")

    if args.turntable:
        az, el, lens = shots["hero"]
        cam = studio.add_camera(centre, distance=info["size_m"][0] * 1.6,
                                azimuth_deg=az, elevation_deg=el, lens=lens)
        studio.frame_subject(cam, objs, margin=1.16)
        written = studio.render_turntable(cam, centre, args.turntable,
                                          out_dir / "turntable", spec["key"],
                                          elevation_deg=el, start_deg=az)
        print(f"[turntable] {len(written)} frames -> {out_dir / 'turntable'}")


if __name__ == "__main__":
    main()
