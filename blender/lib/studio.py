"""Studio rig, render settings and export for the Maven machine visuals.

One rig serves both outputs so the web viewer and the gallery stills agree:
  * `setup_studio()`  — soft key/fill/rim + gradient environment + sweep floor
  * `render_stills()` — hero angles and a turntable for the sliding gallery
  * `export_glb()`    — the same model, web-weight, for the in-page 3D viewer

Rendering is deliberately device-switchable: this box is shared with gaming, and
a Cycles job on the GPU while a game is running is not acceptable.
"""

from __future__ import annotations

import math
import os
from contextlib import contextmanager
from pathlib import Path
from typing import Sequence

import bpy
from mathutils import Vector

from . import shading


# --- world & lights ---------------------------------------------------------

def _world_gradient(top: str = "#2A2F35", bottom: str = "#0B0D0F",
                    strength: float = 0.55) -> None:
    world = bpy.data.worlds.new("Studio") if not bpy.data.worlds else bpy.data.worlds[0]
    bpy.context.scene.world = world
    world.use_nodes = True
    nt = world.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)

    out = nt.nodes.new("ShaderNodeOutputWorld")
    out.location = (400, 0)
    bg = nt.nodes.new("ShaderNodeBackground")
    bg.location = (200, 0)
    bg.inputs["Strength"].default_value = strength
    nt.links.new(bg.outputs["Background"], out.inputs["Surface"])

    tex = nt.nodes.new("ShaderNodeTexCoord")
    tex.location = (-600, 0)
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    sep.location = (-400, 0)
    nt.links.new(tex.outputs["Generated"], sep.inputs["Vector"])
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.location = (-200, 0)
    ramp.color_ramp.elements[0].position = 0.35
    ramp.color_ramp.elements[0].color = shading.srgb(bottom)
    ramp.color_ramp.elements[1].position = 0.72
    ramp.color_ramp.elements[1].color = shading.srgb(top)
    nt.links.new(sep.outputs["Z"], ramp.inputs["Fac"])
    nt.links.new(ramp.outputs["Color"], bg.inputs["Color"])


def _area(name: str, loc, rot_deg, size, energy: float, col=None,
          shape: str = "RECTANGLE", size_y: float | None = None):
    light = bpy.data.lights.new(name, "AREA")
    light.shape = shape
    light.size = size
    if size_y is not None:
        light.size_y = size_y
    light.energy = energy
    light.use_shadow = True
    obj = bpy.data.objects.new(name, light)
    obj.location = loc
    obj.rotation_euler = [math.radians(a) for a in rot_deg]
    (col or bpy.context.scene.collection).objects.link(obj)
    return obj


# Two grounds, because the site uses both: catalogue cards sit on white, the
# hero and the 3D viewer sit on ink. Rendering a dark machine on a dark sweep for
# a white card produces a grey smudge, so the look is chosen per shot.
LOOKS = {
    "dark":  {"top": "#2A2F35", "bottom": "#0B0D0F", "strength": 0.55,
              "floor": "#14171A", "floor_rough": 0.42, "gain": 1.0},
    "light": {"top": "#F2F4F6", "bottom": "#C4C9CE", "strength": 1.35,
              "floor": "#E4E7EA", "floor_rough": 0.48, "gain": 0.65},
}


def setup_studio(machine_width: float = 3.0, machine_height: float = 1.6,
                 sweep: bool = True, look: str = "light") -> dict:
    """Three-light product rig scaled to the subject, plus an infinite sweep floor.

    Key is large and close (soft, wrapping terminator), fill is a wide low-power
    bounce on the opposite side, and a narrow high rim separates the machine from
    the background. Sizes scale with the machine so a 4 m flatbed and a 1 m DTF
    unit both get the same *relative* softness."""
    s = max(machine_width, 1.0)
    cfg = LOOKS[look]
    g = cfg["gain"]
    _world_gradient(cfg["top"], cfg["bottom"], cfg["strength"])

    lights = {
        "key": _area("KeyLight", (-s * 1.15, -s * 1.05, machine_height * 2.1),
                     (52, 0, -42), size=s * 1.5, size_y=s * 1.1, energy=520 * s * g),
        "fill": _area("FillLight", (s * 1.6, -s * 0.9, machine_height * 1.25),
                      (72, 0, 58), size=s * 2.2, size_y=s * 1.4, energy=130 * s * g),
        "rim": _area("RimLight", (s * 0.55, s * 1.5, machine_height * 2.3),
                     (118, 0, 22), size=s * 0.5, size_y=s * 1.6, energy=900 * s * g),
        "top": _area("TopSoft", (0, 0, machine_height * 3.0), (0, 0, 0),
                     size=s * 2.6, size_y=s * 2.0, energy=170 * s * g),
    }

    if sweep:
        # A big rounded-corner sweep: flat under the machine, curving up behind.
        floor = _sweep_floor(radius=s * 1.6, extent=s * 6.0,
                             hex_color=cfg["floor"], roughness=cfg["floor_rough"])
    else:
        # No sweep means a transparent background — but a machine with no contact
        # shadow reads as clip art pasted onto the page. A shadow catcher keeps
        # the shadow and nothing else.
        floor = _shadow_catcher(extent=s * 8.0)
    return {"lights": lights, "floor": floor, "look": look}


def _shadow_catcher(extent: float):
    import bmesh
    bm = bmesh.new()
    bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=extent)
    me = bpy.data.meshes.new("ShadowCatcher")
    bm.to_mesh(me)
    bm.free()
    obj = bpy.data.objects.new("ShadowCatcher", me)
    bpy.context.scene.collection.objects.link(obj)
    # Cycles honours is_shadow_catcher; EEVEE gained it in 4.2. Setting it is
    # harmless on builds that ignore it.
    if hasattr(obj, "is_shadow_catcher"):
        obj.is_shadow_catcher = True
    return obj


def _sweep_floor(radius: float, extent: float, hex_color: str = "#14171A",
                 roughness: float = 0.42):
    import bmesh
    bm = bmesh.new()
    steps = 24
    profile = [(-extent, 0.0)]
    for i in range(steps + 1):
        a = math.pi / 2 * i / steps
        profile.append((radius * (1 - math.sin(a)) + 0.0, radius * (1 - math.cos(a))))
    profile.append((radius, extent))
    verts_a, verts_b = [], []
    for y, z in profile:
        verts_a.append(bm.verts.new((-extent, y, z)))
        verts_b.append(bm.verts.new((extent, y, z)))
    for i in range(len(profile) - 1):
        bm.faces.new((verts_a[i], verts_a[i + 1], verts_b[i + 1], verts_b[i]))
    me = bpy.data.meshes.new("Sweep")
    bm.to_mesh(me)
    bm.free()
    obj = bpy.data.objects.new("Sweep", me)
    bpy.context.scene.collection.objects.link(obj)

    mat, nt, bsdf = shading._new("SweepFloor")
    if nt is not None:
        shading.put(bsdf, "base_color", shading.srgb(hex_color))
        shading.put(bsdf, "roughness", roughness)
        shading.put(bsdf, "metallic", 0.0)
        shading._roughness_breakup(nt, bsdf, roughness, 0.10, 1.4)
    obj.data.materials.append(mat)
    obj.data.shade_smooth()
    return obj


# --- camera -----------------------------------------------------------------

def add_camera(target: Vector, distance: float, azimuth_deg: float = 38.0,
               elevation_deg: float = 14.0, lens: float = 85.0,
               name: str = "Cam", dof_fstop: float | None = 6.3):
    cam_data = bpy.data.cameras.new(name)
    cam_data.lens = lens
    cam_data.sensor_width = 36.0
    cam = bpy.data.objects.new(name, cam_data)
    bpy.context.scene.collection.objects.link(cam)

    az, el = math.radians(azimuth_deg), math.radians(elevation_deg)
    cam.location = target + Vector((
        math.sin(az) * math.cos(el) * distance,
        -math.cos(az) * math.cos(el) * distance,
        math.sin(el) * distance,
    ))
    # Aim: track-to via direct rotation so nothing depends on constraint eval order.
    d = (target - cam.location)
    cam.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()

    if dof_fstop:
        cam_data.dof.use_dof = True
        cam_data.dof.focus_distance = d.length
        cam_data.dof.aperture_fstop = dof_fstop
    bpy.context.scene.camera = cam
    return cam


def frame_subject(cam, objs, margin: float = 1.12) -> None:
    """Dolly the camera back until the subject fits, keeping the angle."""
    from .build import bounds
    lo, hi = bounds(objs)
    centre = (lo + hi) / 2
    radius = (hi - lo).length / 2
    fov = 2 * math.atan(cam.data.sensor_width / (2 * cam.data.lens))
    dist = radius / math.tan(fov / 2) * margin
    direction = (cam.location - centre).normalized()
    cam.location = centre + direction * dist
    cam.rotation_euler = (centre - cam.location).to_track_quat("-Z", "Y").to_euler()
    if cam.data.dof.use_dof:
        cam.data.dof.focus_distance = (centre - cam.location).length


# --- render -----------------------------------------------------------------

def _resolve_engine(engine: str) -> str:
    """Set the render engine across Blender versions and add-on states.

    Two traps here. EEVEE's enum id changed twice across 4.x ('BLENDER_EEVEE' ->
    'BLENDER_EEVEE_NEXT' -> back again in 4.2+). And the static RNA enum only
    lists built-ins: under `--factory-startup` Cycles is not registered yet, so
    introspecting `enum_items` reports CYCLES as unavailable when it is one
    addon_enable away. Enable, then try to assign, and let the assignment be the
    test rather than a pre-flight check.
    """
    scn = bpy.context.scene
    candidates = [engine]
    if "EEVEE" in engine.upper():
        candidates += ["BLENDER_EEVEE", "BLENDER_EEVEE_NEXT"]

    if engine == "CYCLES" and "cycles" not in bpy.context.preferences.addons:
        try:
            bpy.ops.preferences.addon_enable(module="cycles")
        except RuntimeError as exc:
            raise ValueError(f"Cycles is not available in this build: {exc}") from exc

    for cand in candidates:
        try:
            scn.render.engine = cand
            return cand
        except TypeError:
            continue
    raise ValueError(f"render engine {engine!r} could not be enabled")


def configure_render(engine: str = "CYCLES", samples: int = 256,
                     width: int = 2000, height: int = 1400,
                     device: str = "CPU", transparent: bool = False,
                     look: str = "AgX - Medium High Contrast") -> None:
    scn = bpy.context.scene
    scn.render.engine = _resolve_engine(engine)
    engine = scn.render.engine
    scn.render.resolution_x = width
    scn.render.resolution_y = height
    scn.render.resolution_percentage = 100
    scn.render.film_transparent = transparent
    scn.render.image_settings.file_format = "PNG"
    scn.render.image_settings.color_mode = "RGBA" if transparent else "RGB"
    scn.render.image_settings.compression = 20

    if engine == "CYCLES":
        cyc = scn.cycles
        cyc.samples = samples
        cyc.use_adaptive_sampling = True
        cyc.adaptive_threshold = 0.01
        cyc.use_denoising = True
        cyc.max_bounces = 8
        cyc.diffuse_bounces = 3
        cyc.glossy_bounces = 6
        cyc.transmission_bounces = 8
        cyc.transparent_max_bounces = 8
        cyc.caustics_reflective = False
        cyc.caustics_refractive = False
        cyc.device = "GPU" if device.upper() == "GPU" else "CPU"
        if device.upper() == "GPU":
            _enable_gpu()

    try:
        scn.view_settings.view_transform = "AgX"
        scn.view_settings.look = look
    except TypeError:
        scn.view_settings.view_transform = "Filmic"


def _enable_gpu() -> None:
    prefs = bpy.context.preferences.addons.get("cycles")
    if not prefs:
        return
    cp = prefs.preferences
    for backend in ("OPTIX", "CUDA"):
        try:
            cp.compute_device_type = backend
            break
        except TypeError:
            continue
    cp.get_devices()
    for dev in cp.devices:
        dev.use = dev.type != "CPU"


def render_to(path: str | Path) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    bpy.context.scene.render.filepath = str(path.with_suffix(""))
    bpy.ops.render.render(write_still=True)
    return path


def render_turntable(cam, target: Vector, frames: int, out_dir: str | Path,
                     stem: str, elevation_deg: float = 14.0,
                     start_deg: float = 38.0) -> list[Path]:
    """Orbit stills for the product gallery. The web viewer gets a real glTF; this
    is the no-JS fallback and the social/OG imagery."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    radius = (cam.location - target).length
    el = math.radians(elevation_deg)
    written = []
    for i in range(frames):
        az = math.radians(start_deg + 360.0 * i / frames)
        cam.location = target + Vector((
            math.sin(az) * math.cos(el) * radius,
            -math.cos(az) * math.cos(el) * radius,
            math.sin(el) * radius,
        ))
        cam.rotation_euler = (target - cam.location).to_track_quat("-Z", "Y").to_euler()
        written.append(render_to(out_dir / f"{stem}-{i:02d}.png"))
    return written


# --- export -----------------------------------------------------------------

#: Sockets whose value comes from a procedural node chain that glTF cannot carry.
_FLATTEN = ("Roughness", "Metallic", "Normal", "Specular IOR Level")


@contextmanager
def _flattened_materials(objs: Sequence[bpy.types.Object]):
    """Drop procedural inputs for the duration of an export.

    The materials drive roughness from a noise chain, which is what makes a
    Cycles frame read as a machined surface rather than a CAD screenshot. glTF
    has no such node graph, and the exporter will not bake one: a socket that is
    LINKED exports as its factor default, so every metal in the GLB arrived at
    roughness 1.0 — fully rough metal catches no highlight, and the whole machine
    rendered as a black silhouette in <model-viewer>.

    Unlinking restores the scalar the chain was varying around, because `put()`
    writes it to the socket before the link is made and linking does not erase
    it. The detail lost is sub-millimetre noise nobody can see in a 570 px
    viewport; the highlight regained is the entire read of the material.
    """
    saved = []
    seen = set()
    for obj in objs:
        for slot in getattr(obj, "material_slots", []):
            mat = slot.material
            if mat is None or mat.name in seen or not mat.use_nodes:
                continue
            seen.add(mat.name)
            for node in mat.node_tree.nodes:
                if node.type != "BSDF_PRINCIPLED":
                    continue
                for name in _FLATTEN:
                    socket = node.inputs.get(name)
                    if socket is None:
                        continue
                    for link in list(socket.links):
                        saved.append((mat.node_tree, link.from_socket, socket))
                        mat.node_tree.links.remove(link)
    try:
        yield len(saved)
    finally:
        for tree, from_socket, to_socket in saved:
            tree.links.new(from_socket, to_socket)


def export_glb(objs: Sequence[bpy.types.Object], path: str | Path,
               draco: bool = True, draco_level: int = 6) -> Path:
    """Web-weight GLB of the machine only — no lights, no floor, no camera."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    bpy.ops.object.select_all(action="DESELECT")
    for o in objs:
        if o.name in bpy.context.view_layer.objects:
            o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0] if objs else None

    kwargs = dict(
        filepath=str(path),
        export_format="GLB",
        use_selection=True,
        export_apply=True,
        export_yup=True,
        export_cameras=False,
        export_lights=False,
        export_extras=False,
        export_materials="EXPORT",
    )
    if draco:
        kwargs.update(
            export_draco_mesh_compression_enable=True,
            export_draco_mesh_compression_level=draco_level,
            export_draco_position_quantization=14,
            export_draco_normal_quantization=10,
            export_draco_texcoord_quantization=12,
        )
    with _flattened_materials(objs) as dropped:
        if dropped:
            print(f"[export] flattened {dropped} procedural material inputs")
        try:
            bpy.ops.export_scene.gltf(**kwargs)
        except TypeError as exc:
            # Option set drifts between Blender releases; drop the unknown key and retry.
            bad = str(exc).split("'")[1] if "'" in str(exc) else None
            if bad and bad in kwargs:
                kwargs.pop(bad)
                bpy.ops.export_scene.gltf(**kwargs)
            else:
                raise
    return path


def report(objs: Sequence[bpy.types.Object]) -> dict:
    dg = bpy.context.evaluated_depsgraph_get()
    tris = verts = 0
    for o in objs:
        if o.type != "MESH":
            continue
        me = o.evaluated_get(dg).to_mesh()
        verts += len(me.vertices)
        tris += sum(max(0, len(p.vertices) - 2) for p in me.polygons)
        o.evaluated_get(dg).to_mesh_clear()
    from .build import bounds
    lo, hi = bounds(objs)
    return {
        "objects": len(objs),
        "verts": verts,
        "tris": tris,
        "size_m": tuple(round(v, 3) for v in (hi - lo)),
    }
