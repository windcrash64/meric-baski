"""Mesh construction helpers for the machine models.

Real machines are sheet metal and extrusion: flat faces, tight radii, visible
panel gaps and fasteners. These helpers make that cheap to express, and — more
importantly — make it impossible to forget the bevel. An unbevelled edge catches
no highlight, and a machine with no edge highlights reads as CG instantly.

All units are metres, matching the real machine dimensions.
"""

from __future__ import annotations

import math
from typing import Iterable, Sequence

import bmesh
import bpy
from mathutils import Vector

V3 = Sequence[float]


# --- scene plumbing ---------------------------------------------------------

def reset_scene() -> None:
    bpy.ops.wm.read_factory_settings(use_empty=True)


def collection(name: str) -> bpy.types.Collection:
    col = bpy.data.collections.get(name)
    if col is None:
        col = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(col)
    return col


def _link(obj: bpy.types.Object, col: bpy.types.Collection | None) -> None:
    (col or bpy.context.scene.collection).objects.link(obj)


def empty(name: str, loc: V3 = (0, 0, 0), col=None) -> bpy.types.Object:
    obj = bpy.data.objects.new(name, None)
    obj.empty_display_size = 0.25
    obj.location = loc
    _link(obj, col)
    return obj


def _mesh_obj(name: str, bm: bmesh.types.BMesh, loc: V3, rot: V3, col) -> bpy.types.Object:
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    obj = bpy.data.objects.new(name, me)
    obj.location = loc
    obj.rotation_euler = [math.radians(a) for a in rot]
    _link(obj, col)
    return obj


# --- primitives -------------------------------------------------------------

def box(name: str, size: V3, loc: V3 = (0, 0, 0), rot: V3 = (0, 0, 0),
        mat=None, bevel: float = 0.004, segments: int = 2, col=None,
        anchor: str = "center") -> bpy.types.Object:
    """Axis-aligned box. `anchor` shifts the origin: 'center', 'bottom', 'min'."""
    sx, sy, sz = size
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=Vector((sx, sy, sz)), verts=bm.verts)
    if anchor == "bottom":
        bmesh.ops.translate(bm, vec=Vector((0, 0, sz / 2)), verts=bm.verts)
    elif anchor == "min":
        bmesh.ops.translate(bm, vec=Vector((sx / 2, sy / 2, sz / 2)), verts=bm.verts)
    obj = _mesh_obj(name, bm, loc, rot, col)
    if mat:
        set_material(obj, mat)
    if bevel:
        add_bevel(obj, bevel, segments)
    return obj


def cylinder(name: str, radius: float, depth: float, loc: V3 = (0, 0, 0),
             rot: V3 = (0, 0, 0), verts: int = 32, mat=None,
             bevel: float = 0.0015, col=None, axis: str = "Z") -> bpy.types.Object:
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=verts,
                          radius1=radius, radius2=radius, depth=depth)
    obj = _mesh_obj(name, bm, loc, rot, col)
    if axis == "X":
        obj.rotation_euler[1] += math.radians(90)
    elif axis == "Y":
        obj.rotation_euler[0] += math.radians(90)
    if mat:
        set_material(obj, mat)
    if bevel:
        add_bevel(obj, bevel, 2)
    shade_auto(obj)
    return obj


def tube(name: str, r_out: float, r_in: float, depth: float, loc: V3 = (0, 0, 0),
         rot: V3 = (0, 0, 0), verts: int = 32, mat=None, col=None) -> bpy.types.Object:
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=False, segments=verts,
                          radius1=r_out, radius2=r_out, depth=depth)
    bmesh.ops.create_cone(bm, cap_ends=False, segments=verts,
                          radius1=r_in, radius2=r_in, depth=depth)
    bmesh.ops.bridge_loops(bm, edges=[e for e in bm.edges if len(e.link_faces) == 1])
    obj = _mesh_obj(name, bm, loc, rot, col)
    if mat:
        set_material(obj, mat)
    add_bevel(obj, 0.001, 2)
    shade_auto(obj)
    return obj


def plane(name: str, size: V3, loc: V3 = (0, 0, 0), rot: V3 = (0, 0, 0),
          mat=None, col=None) -> bpy.types.Object:
    bm = bmesh.new()
    bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=0.5)
    bmesh.ops.scale(bm, vec=Vector((size[0], size[1], 1.0)), verts=bm.verts)
    obj = _mesh_obj(name, bm, loc, rot, col)
    if mat:
        set_material(obj, mat)
    return obj


def profile_beam(name: str, length: float, w: float, h: float, wall: float = 0.006,
                 loc: V3 = (0, 0, 0), rot: V3 = (0, 0, 0), mat=None,
                 col=None, axis: str = "X") -> bpy.types.Object:
    """Hollow extruded profile — the honest way to build a gantry beam.
    The visible wall thickness at the ends is what sells it as extrusion."""
    bm = bmesh.new()
    outer = bmesh.ops.create_cube(bm, size=1.0)["verts"]
    bmesh.ops.scale(bm, vec=Vector((w, h, length)), verts=outer)
    inner = bmesh.ops.create_cube(bm, size=1.0)["verts"]
    bmesh.ops.scale(bm, vec=Vector((w - wall * 2, h - wall * 2, length + 0.002)),
                    verts=inner)
    bmesh.ops.reverse_faces(bm, faces=[f for f in bm.faces
                                       if all(v in inner for v in f.verts)])
    obj = _mesh_obj(name, bm, loc, rot, col)
    if axis == "X":
        obj.rotation_euler[1] += math.radians(90)
    elif axis == "Y":
        obj.rotation_euler[0] += math.radians(90)
    if mat:
        set_material(obj, mat)
    add_bevel(obj, 0.0018, 2)
    return obj


# --- modifiers & shading ----------------------------------------------------

def add_bevel(obj: bpy.types.Object, width: float = 0.004, segments: int = 2,
              angle_deg: float = 32.0) -> None:
    m = obj.modifiers.new("Bevel", "BEVEL")
    m.width = width
    m.segments = segments
    m.limit_method = "ANGLE"
    m.angle_limit = math.radians(angle_deg)
    m.miter_outer = "MITER_ARC"
    m.harden_normals = True
    obj.data.shade_smooth()
    shade_auto(obj, angle_deg)


def shade_auto(obj: bpy.types.Object, angle_deg: float = 32.0) -> None:
    """Smooth-by-angle. Blender 4.1 removed mesh auto-smooth in favour of a
    modifier, so try the operator and fall back to the legacy attribute."""
    obj.data.shade_smooth()
    try:
        prev = bpy.context.view_layer.objects.active
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.shade_auto_smooth(angle=math.radians(angle_deg))
        bpy.context.view_layer.objects.active = prev
    except (AttributeError, RuntimeError):
        if hasattr(obj.data, "use_auto_smooth"):
            obj.data.use_auto_smooth = True
            obj.data.auto_smooth_angle = math.radians(angle_deg)


def array(obj: bpy.types.Object, count: int, offset: V3,
          name: str = "Array") -> bpy.types.Modifier:
    m = obj.modifiers.new(name, "ARRAY")
    m.count = count
    m.use_relative_offset = False
    m.use_constant_offset = True
    m.constant_offset_displace = offset
    return m


def mirror(obj: bpy.types.Object, axis: str = "X",
           mirror_object: bpy.types.Object | None = None) -> bpy.types.Modifier:
    m = obj.modifiers.new("Mirror", "MIRROR")
    m.use_axis = ("XYZ".index(axis) == 0, "XYZ".index(axis) == 1, "XYZ".index(axis) == 2)
    if mirror_object:
        m.mirror_object = mirror_object
    return m


def boolean(obj: bpy.types.Object, cutter: bpy.types.Object,
            op: str = "DIFFERENCE") -> bpy.types.Modifier:
    m = obj.modifiers.new("Bool", "BOOLEAN")
    m.operation = op
    m.object = cutter
    m.solver = "EXACT"
    cutter.hide_render = True
    cutter.hide_viewport = True
    return m


def solidify(obj: bpy.types.Object, thickness: float = 0.002,
             offset: float = -1.0) -> bpy.types.Modifier:
    m = obj.modifiers.new("Solidify", "SOLIDIFY")
    m.thickness = thickness
    m.offset = offset
    return m


# --- materials --------------------------------------------------------------

def set_material(obj: bpy.types.Object, mat) -> None:
    obj.data.materials.clear()
    obj.data.materials.append(mat)


def assign_faces(obj: bpy.types.Object, mats: Iterable, picker) -> None:
    """Multi-material assignment: `picker(face_center, face_normal) -> slot index."""
    mats = list(mats)
    obj.data.materials.clear()
    for m in mats:
        obj.data.materials.append(m)
    me = obj.data
    for poly in me.polygons:
        poly.material_index = max(0, min(len(mats) - 1,
                                         picker(poly.center, poly.normal)))


# --- composition ------------------------------------------------------------

def parent_to(children: Iterable[bpy.types.Object], root: bpy.types.Object) -> None:
    for c in children:
        if c is not root and c.parent is None:
            c.parent = root
            c.matrix_parent_inverse = root.matrix_world.inverted()


def bounds(objs: Iterable[bpy.types.Object]):
    """World-space bounding box of a set of objects."""
    lo = Vector((1e9, 1e9, 1e9))
    hi = Vector((-1e9, -1e9, -1e9))
    dg = bpy.context.evaluated_depsgraph_get()
    for o in objs:
        if o.type != "MESH":
            continue
        ev = o.evaluated_get(dg)
        for corner in ev.bound_box:
            p = ev.matrix_world @ Vector(corner)
            lo = Vector((min(lo[i], p[i]) for i in range(3)))
            hi = Vector((max(hi[i], p[i]) for i in range(3)))
    return lo, hi


def bolt_row(name: str, count: int, spacing: float, radius: float, height: float,
             loc: V3, rot: V3 = (0, 0, 0), mat=None, col=None,
             axis: V3 = (1, 0, 0)) -> bpy.types.Object:
    """A run of hex fasteners. Nothing says 'machine' faster than visible bolts."""
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=6,
                          radius1=radius, radius2=radius * 0.96, depth=height)
    obj = _mesh_obj(name, bm, loc, rot, col)
    if mat:
        set_material(obj, mat)
    add_bevel(obj, radius * 0.12, 2)
    if count > 1:
        array(obj, count, (axis[0] * spacing, axis[1] * spacing, axis[2] * spacing))
    return obj
