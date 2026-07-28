"""PBR material library for the Maven machine renders.

Everything here exists to kill the two things that make CG machines look fake:
perfectly uniform surfaces and perfectly sharp edges. Every material carries a
procedural roughness break-up, and `build.py` bevels every hard edge.

Blender renames Principled BSDF sockets between releases (4.0 moved Specular ->
'Specular IOR Level', Emission -> 'Emission Color', Clearcoat -> 'Coat Weight'),
so sockets are always resolved by trying a list of names rather than assuming.
"""

from __future__ import annotations

import bpy

# --- socket-name compatibility ---------------------------------------------

_ALIASES = {
    "specular": ("Specular IOR Level", "Specular"),
    "emission_color": ("Emission Color", "Emission"),
    "emission_strength": ("Emission Strength",),
    "coat": ("Coat Weight", "Clearcoat"),
    "coat_roughness": ("Coat Roughness", "Clearcoat Roughness"),
    "transmission": ("Transmission Weight", "Transmission"),
    "sheen": ("Sheen Weight", "Sheen"),
    "base_color": ("Base Color",),
    "metallic": ("Metallic",),
    "roughness": ("Roughness",),
    "ior": ("IOR",),
    "alpha": ("Alpha",),
    "normal": ("Normal",),
    "anisotropic": ("Anisotropic",),
}


def sock(node, key: str):
    """Resolve a Principled input across Blender versions. Returns None if absent."""
    for name in _ALIASES.get(key, (key,)):
        if name in node.inputs:
            return node.inputs[name]
    return None


def put(node, key: str, value) -> None:
    s = sock(node, key)
    if s is not None:
        s.default_value = value


# --- helpers ----------------------------------------------------------------

def srgb(hex_str: str, alpha: float = 1.0):
    """'#RRGGBB' -> linear RGBA, because Blender node values are scene-linear."""
    h = hex_str.lstrip("#")
    out = []
    for i in (0, 2, 4):
        c = int(h[i:i + 2], 16) / 255.0
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return (*out, alpha)


def _new(name: str):
    mat = bpy.data.materials.get(name)
    if mat:
        return mat, None, None
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    out.location = (600, 0)
    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.location = (240, 0)
    nt.links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
    return mat, nt, bsdf


def _texcoord(nt, x=-1400):
    tc = nt.nodes.new("ShaderNodeTexCoord")
    tc.location = (x, 0)
    return tc


def _stretched_coords(nt, stretch, x: float, y: float):
    """Object coords, optionally squashed on one axis so noise becomes streaks.

    Object coordinates are in metres here, so a 'Scale' of N means features of
    1/N metres — get this wrong and a 1.4 m beam ends up covered in 30 cm clouds.
    """
    tc = _texcoord(nt, x)
    tc.location = (x, y)
    if stretch is None:
        return tc.outputs["Object"]
    mapping = nt.nodes.new("ShaderNodeMapping")
    mapping.location = (x + 190, y)
    mapping.inputs["Scale"].default_value = stretch
    nt.links.new(tc.outputs["Object"], mapping.inputs["Vector"])
    return mapping.outputs["Vector"]


def _roughness_breakup(nt, bsdf, base: float, amount: float, scale: float,
                       detail: float = 6.0, y: float = -320.0, stretch=None):
    """Large-scale roughness variation. This single node chain is the difference
    between 'a render' and 'a photograph of a painted panel'."""
    coords = _stretched_coords(nt, stretch, -1600, y)
    noise = nt.nodes.new("ShaderNodeTexNoise")
    noise.location = (-1180, y)
    noise.inputs["Scale"].default_value = scale
    noise.inputs["Detail"].default_value = detail
    noise.inputs["Roughness"].default_value = 0.55
    nt.links.new(coords, noise.inputs["Vector"])

    ramp = nt.nodes.new("ShaderNodeMapRange")
    ramp.location = (-960, y)
    ramp.inputs["From Min"].default_value = 0.30
    ramp.inputs["From Max"].default_value = 0.70
    ramp.inputs["To Min"].default_value = max(0.0, base - amount)
    ramp.inputs["To Max"].default_value = min(1.0, base + amount)
    ramp.clamp = True
    nt.links.new(noise.outputs["Fac"], ramp.inputs["Value"])
    nt.links.new(ramp.outputs["Result"], sock(bsdf, "roughness"))
    return noise


def _bump(nt, bsdf, strength: float, scale: float, detail: float = 12.0,
          y: float = -760.0, distance: float = 0.0006, stretch=None):
    """Fine surface texture (orange peel on paint, brush lines on metal)."""
    coords = _stretched_coords(nt, stretch, -1600, y)
    noise = nt.nodes.new("ShaderNodeTexNoise")
    noise.location = (-1180, y)
    noise.inputs["Scale"].default_value = scale
    noise.inputs["Detail"].default_value = detail
    noise.inputs["Roughness"].default_value = 0.6
    nt.links.new(coords, noise.inputs["Vector"])

    bump = nt.nodes.new("ShaderNodeBump")
    bump.location = (-960, y)
    bump.inputs["Strength"].default_value = strength
    bump.inputs["Distance"].default_value = distance
    nt.links.new(noise.outputs["Fac"], bump.inputs["Height"])
    nt.links.new(bump.outputs["Normal"], sock(bsdf, "normal"))
    return bump


# --- the library ------------------------------------------------------------

def painted_metal(name: str, hex_color: str, roughness: float = 0.34,
                  coat: float = 0.28, metallic: float = 0.0):
    """Powder-coated sheet steel — the main body panels."""
    mat, nt, bsdf = _new(name)
    if nt is None:
        return mat
    put(bsdf, "base_color", srgb(hex_color))
    put(bsdf, "metallic", metallic)
    put(bsdf, "roughness", roughness)
    put(bsdf, "coat", coat)
    put(bsdf, "coat_roughness", 0.18)
    _roughness_breakup(nt, bsdf, roughness, 0.055, 7.0)   # ~14 cm spray variation
    _bump(nt, bsdf, 0.10, 260.0)                          # ~4 mm orange peel
    return mat


# Long parts are modelled along local Z, so squashing Z turns isotropic noise
# into brush lines running down the extrusion.
_BRUSH = (1.0, 1.0, 0.04)


def brushed_aluminium(name: str = "AluBrushed", hex_color: str = "#B9BCBF",
                      roughness: float = 0.30):
    """Extruded aluminium profile — gantry beams, rails, frames."""
    mat, nt, bsdf = _new(name)
    if nt is None:
        return mat
    put(bsdf, "base_color", srgb(hex_color))
    put(bsdf, "metallic", 1.0)
    put(bsdf, "roughness", roughness)
    put(bsdf, "anisotropic", 0.65)
    _roughness_breakup(nt, bsdf, roughness, 0.05, 90.0, stretch=_BRUSH)
    _bump(nt, bsdf, 0.25, 420.0, detail=8.0, distance=0.00012, stretch=_BRUSH)
    return mat


def anodised_black(name: str = "AnodBlack", roughness: float = 0.40):
    mat, nt, bsdf = _new(name)
    if nt is None:
        return mat
    put(bsdf, "base_color", srgb("#1B1D1F"))
    put(bsdf, "metallic", 1.0)
    put(bsdf, "roughness", roughness)
    _roughness_breakup(nt, bsdf, roughness, 0.05, 60.0)
    _bump(nt, bsdf, 0.14, 380.0, distance=0.00015)
    return mat


def steel_machined(name: str = "SteelMachined"):
    """Bright turned/ground steel — shafts, screws, linear rails."""
    mat, nt, bsdf = _new(name)
    if nt is None:
        return mat
    put(bsdf, "base_color", srgb("#C6C9CD"))
    put(bsdf, "metallic", 1.0)
    put(bsdf, "roughness", 0.16)
    _roughness_breakup(nt, bsdf, 0.16, 0.045, 140.0, stretch=_BRUSH)
    _bump(nt, bsdf, 0.12, 600.0, distance=0.0001, stretch=_BRUSH)
    return mat


def chrome(name: str = "Chrome"):
    mat, nt, bsdf = _new(name)
    if nt is None:
        return mat
    put(bsdf, "base_color", srgb("#E8EAEC"))
    put(bsdf, "metallic", 1.0)
    put(bsdf, "roughness", 0.055)
    return mat


def rubber(name: str = "Rubber", hex_color: str = "#141517", roughness: float = 0.72):
    mat, nt, bsdf = _new(name)
    if nt is None:
        return mat
    put(bsdf, "base_color", srgb(hex_color))
    put(bsdf, "metallic", 0.0)
    put(bsdf, "roughness", roughness)
    _roughness_breakup(nt, bsdf, roughness, 0.06, 24.0)
    _bump(nt, bsdf, 0.35, 1400.0, distance=0.0004)
    return mat


def plastic_textured(name: str, hex_color: str, roughness: float = 0.55):
    """Injection-moulded covers and trim — subtle pebble grain."""
    mat, nt, bsdf = _new(name)
    if nt is None:
        return mat
    put(bsdf, "base_color", srgb(hex_color))
    put(bsdf, "metallic", 0.0)
    put(bsdf, "roughness", roughness)
    put(bsdf, "coat", 0.10)
    _roughness_breakup(nt, bsdf, roughness, 0.07, 9.0)
    _bump(nt, bsdf, 0.30, 1100.0, distance=0.0003)
    return mat


def acrylic(name: str = "AcrylicSmoke", hex_color: str = "#20262B",
            alpha: float = 0.42):
    """Smoked safety glazing over the print area."""
    mat, nt, bsdf = _new(name)
    if nt is None:
        return mat
    put(bsdf, "base_color", srgb(hex_color))
    put(bsdf, "metallic", 0.0)
    put(bsdf, "roughness", 0.06)
    put(bsdf, "ior", 1.49)
    put(bsdf, "transmission", 0.92)
    put(bsdf, "alpha", alpha)
    mat.blend_method = "BLEND" if hasattr(mat, "blend_method") else mat.blend_method
    return mat


def emissive(name: str, hex_color: str, strength: float = 6.0):
    """LED-UV lamp glow, status strips, screen backlight."""
    mat, nt, bsdf = _new(name)
    if nt is None:
        return mat
    put(bsdf, "base_color", srgb(hex_color))
    put(bsdf, "roughness", 0.4)
    put(bsdf, "emission_color", srgb(hex_color))
    put(bsdf, "emission_strength", strength)
    return mat


def screen(name: str = "ScreenUI", hex_color: str = "#0E1418"):
    mat, nt, bsdf = _new(name)
    if nt is None:
        return mat
    put(bsdf, "base_color", srgb(hex_color))
    put(bsdf, "roughness", 0.10)
    put(bsdf, "emission_color", srgb("#1E6C9B"))
    put(bsdf, "emission_strength", 1.6)
    put(bsdf, "coat", 0.5)
    put(bsdf, "coat_roughness", 0.05)
    return mat


def vacuum_table(name: str = "VacuumTable", hex_color: str = "#63686D",
                 pitch: float = 45.0):
    """Anodised bed plate with the vacuum hole grid as bump only.

    A 2.5 x 1.3 m bed carries tens of thousands of holes; as geometry that is a
    dead weight in the GLB and invisible past 2 m. As a bump it reads correctly
    from every distance the site will ever show.
    """
    mat, nt, bsdf = _new(name)
    if nt is None:
        return mat
    put(bsdf, "base_color", srgb(hex_color))
    put(bsdf, "metallic", 0.9)
    put(bsdf, "roughness", 0.44)

    tc = _texcoord(nt, -1400)
    wave = nt.nodes.new("ShaderNodeTexChecker")
    wave.location = (-1180, 240)
    wave.inputs["Scale"].default_value = pitch
    nt.links.new(tc.outputs["Object"], wave.inputs["Vector"])

    bump = nt.nodes.new("ShaderNodeBump")
    bump.location = (-960, 240)
    bump.inputs["Strength"].default_value = 0.55
    bump.inputs["Distance"].default_value = 0.0025
    nt.links.new(wave.outputs["Fac"], bump.inputs["Height"])
    nt.links.new(bump.outputs["Normal"], sock(bsdf, "normal"))
    _roughness_breakup(nt, bsdf, 0.44, 0.06, 6.0)
    return mat


def perforated_steel(name: str = "PerfSteel", hex_color: str = "#2A2D30",
                     scale: float = 420.0):
    """Ventilation panel — real holes are expensive, an alpha-cut grid is not."""
    mat, nt, bsdf = _new(name)
    if nt is None:
        return mat
    put(bsdf, "base_color", srgb(hex_color))
    put(bsdf, "metallic", 0.85)
    put(bsdf, "roughness", 0.45)

    tc = _texcoord(nt, -1400)
    brick = nt.nodes.new("ShaderNodeTexBrick")
    brick.location = (-1180, 200)
    brick.inputs["Scale"].default_value = scale
    brick.inputs["Mortar Size"].default_value = 0.28
    brick.inputs["Brick Width"].default_value = 1.0
    brick.inputs["Row Height"].default_value = 1.0
    nt.links.new(tc.outputs["Object"], brick.inputs["Vector"])
    nt.links.new(brick.outputs["Fac"], sock(bsdf, "alpha"))
    return mat


# --- brand + machine palette ------------------------------------------------

INK = "#131518"          # near-black body panels
GRAPHITE = "#4A4F55"     # secondary structure
SILVER = "#B9BCBF"
WARN_YELLOW = "#FFE305"  # brand yellow, doubles as machine safety yellow
CYAN = "#0081D2"
MAGENTA = "#E30161"


def machine_kit(accent_hex: str = CYAN) -> dict:
    """One call returns every material a machine needs, sharing node graphs so the
    GLB stays small and the renders stay consistent between machines."""
    return {
        "body": painted_metal("BodyInk", INK, roughness=0.36, coat=0.30),
        # Light body panels are a matte warm grey, not a glossy near-white:
        # at #D8DBDE with a clearcoat they read as moulded white plastic on the
        # dark hero ground, which is exactly what a machine cover is not.
        "body_light": painted_metal("BodyLight", "#B4B7BA", roughness=0.52, coat=0.10),
        "accent": painted_metal("Accent", accent_hex, roughness=0.28, coat=0.45),
        "frame": painted_metal("FrameGraphite", GRAPHITE, roughness=0.45, coat=0.12),
        "alu": brushed_aluminium(),
        "anod": anodised_black(),
        "steel": steel_machined(),
        "chrome": chrome(),
        "rubber": rubber(),
        "trim": plastic_textured("TrimPlastic", "#26292C", roughness=0.58),
        "glass": acrylic(),
        "uv_lamp": emissive("UVLamp", "#7A5CFF", strength=14.0),
        "status": emissive("StatusLed", "#39D98A", strength=8.0),
        "warn": painted_metal("WarnYellow", WARN_YELLOW, roughness=0.42, coat=0.15),
        "screen": screen(),
        "vent": perforated_steel(),
        "bed": vacuum_table(),
        "ink_c": emissive("InkCyan", CYAN, strength=0.0),
        "ink_m": emissive("InkMagenta", MAGENTA, strength=0.0),
        "ink_y": emissive("InkYellow", WARN_YELLOW, strength=0.0),
        "ink_k": painted_metal("InkBlack", "#101214", roughness=0.30),
        "ink_w": painted_metal("InkWhite", "#EDEFF1", roughness=0.30),
        "beacon_r": emissive("BeaconRed", "#E01B2E", strength=4.0),
        "beacon_a": emissive("BeaconAmber", "#F2A61B", strength=3.0),
        "beacon_g": emissive("BeaconGreen", "#2FBF71", strength=4.0),
        "estop": painted_metal("EStopRed", "#C81027", roughness=0.42, coat=0.2),
    }
