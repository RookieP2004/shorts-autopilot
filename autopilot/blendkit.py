"""blendkit: build cinematic 3D shots in Blender (bpy) from short Python scripts.

A shot script is plain Python that starts with `from autopilot.blendkit import *` and uses these helpers.
It is run in its own process by `python -m autopilot.blendrun <script> <out_dir> <dur> <fps> <w> <h>`,
which defines DUR (seconds), FPS, FRAMES and renders PNG frames (with alpha when `transparent=True`).

Look: soft studio light, smooth plastic / clay / metal / paper materials, shallow depth of field, gentle
camera moves, AgX colour with a little bloom: a clean "Zack D Films" style, not photoreal.

Coordinates: metres, Z is up. Time: helpers take seconds and convert to frames.
"""
import math
import os

import bpy
import mathutils

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = {"display": os.path.join(ROOT, "fonts", "Anton-Regular.ttf"),
         "body": os.path.join(ROOT, "fonts", "Poppins-ExtraBold.ttf"),
         "serif": os.path.join(ROOT, "fonts", "DMSerifDisplay-Regular.ttf")}
FPS = 30
_STATE = {}


# ------------------------------------------------------------------ scene
def reset(w=540, h=960, fps=30, dur=5.0, samples=10, transparent=False, motion_blur=True, bloom=0.25, exposure=0.0,
          look="AgX - Medium High Contrast"):
    """Start an empty scene. Cycles on CPU, denoised; vertical frame by default."""
    global FPS
    FPS = fps
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = samples
    sc.cycles.use_adaptive_sampling = True
    sc.cycles.adaptive_threshold = 0.05
    sc.cycles.use_denoising = True
    try:
        sc.cycles.denoiser = "OPENIMAGEDENOISE"
    except Exception:
        pass
    sc.cycles.max_bounces = 4
    sc.cycles.diffuse_bounces = 1
    sc.cycles.glossy_bounces = 1
    sc.cycles.transmission_bounces = 2
    sc.cycles.transparent_max_bounces = 4
    sc.cycles.adaptive_threshold = 0.08
    sc.render.use_persistent_data = True
    sc.cycles.caustics_reflective = False
    sc.cycles.caustics_refractive = False
    sc.render.resolution_x, sc.render.resolution_y = w, h
    sc.render.resolution_percentage = 100
    sc.render.fps = fps
    sc.frame_start = 1
    sc.frame_end = max(1, int(round(dur * fps)))
    sc.render.film_transparent = transparent
    sc.render.use_motion_blur = motion_blur
    sc.render.motion_blur_shutter = 0.5
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGBA" if transparent else "RGB"
    try:
        sc.view_settings.view_transform = "AgX"
        sc.view_settings.look = look
    except Exception:
        pass
    sc.view_settings.exposure = exposure
    sc.render.threads_mode = "AUTO"
    world_color((0.03, 0.035, 0.045), 1.0)
    _STATE.update(bloom=bloom)
    return sc


def world_color(rgb, strength=1.0):
    """Flat world light (also the background unless transparent)."""
    w = bpy.data.worlds.get("World") or bpy.data.worlds.new("World")
    bpy.context.scene.world = w
    w.use_nodes = True
    bg = w.node_tree.nodes.get("Background")
    bg.inputs[0].default_value = (*rgb, 1)
    bg.inputs[1].default_value = strength
    return w


def frames(seconds):
    return max(1, int(round(seconds * FPS)) + 1)


def hexrgb(h):
    h = h.lstrip("#")
    lin = lambda c: (c / 12.92) if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    return tuple(lin(int(h[i:i + 2], 16) / 255) for i in (0, 2, 4))


def _col(c):
    return hexrgb(c) if isinstance(c, str) else tuple(c)


# ------------------------------------------------------------------ materials
def mat(name, color="#cccccc", rough=0.45, metal=0.0, emit=None, emit_strength=0.0, sss=0.0, transmission=0.0,
        ior=1.45, alpha=1.0, coat=0.0, image=None, noise_bump=0.0):
    """Principled material. image = path to a texture (UV mapped)."""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    p = nt.nodes.get("Principled BSDF")
    p.inputs["Base Color"].default_value = (*_col(color), 1)
    p.inputs["Roughness"].default_value = rough
    p.inputs["Metallic"].default_value = metal
    if sss:
        p.inputs["Subsurface Weight"].default_value = sss
        p.inputs["Subsurface Radius"].default_value = (0.9, 0.35, 0.2)
        p.inputs["Subsurface Scale"].default_value = 0.05
    if transmission:
        p.inputs["Transmission Weight"].default_value = transmission
        p.inputs["IOR"].default_value = ior
    if coat:
        p.inputs["Coat Weight"].default_value = coat
    if emit:
        p.inputs["Emission Color"].default_value = (*_col(emit), 1)
        p.inputs["Emission Strength"].default_value = emit_strength
    if alpha < 1:
        p.inputs["Alpha"].default_value = alpha
    if image:
        tex = nt.nodes.new("ShaderNodeTexImage")
        tex.image = bpy.data.images.load(image)
        tex.interpolation = "Cubic"
        nt.links.new(tex.outputs["Color"], p.inputs["Base Color"])
        if image.lower().endswith(".png"):
            nt.links.new(tex.outputs["Alpha"], p.inputs["Alpha"])
    if noise_bump:
        n = nt.nodes.new("ShaderNodeTexNoise")
        n.inputs["Scale"].default_value = 60
        b = nt.nodes.new("ShaderNodeBump")
        b.inputs["Strength"].default_value = noise_bump
        nt.links.new(n.outputs["Fac"], b.inputs["Height"])
        nt.links.new(b.outputs["Normal"], p.inputs["Normal"])
    return m


def plastic(color, rough=0.35, name=None):
    return mat(name or f"plastic_{color}", color, rough=rough, coat=0.3)


def clay(color, name=None):
    return mat(name or f"clay_{color}", color, rough=0.75, sss=0.05)


def metal(color="#d9a441", rough=0.25, name=None):
    return mat(name or f"metal_{color}", color, rough=rough, metal=1.0)


def glass(color="#ffffff", rough=0.02, name=None):
    return mat(name or "glass", color, rough=rough, transmission=1.0, ior=1.45)


def glow(color, strength=6.0, name=None):
    return mat(name or f"glow_{color}", color, rough=0.5, emit=color, emit_strength=strength)


def organic(color="#c85a5a", name=None):
    """Wet, fleshy, slightly translucent: organs, cells, fruit."""
    return mat(name or f"organic_{color}", color, rough=0.28, sss=0.35, coat=0.6, noise_bump=0.15)


def paper(image, rough=0.6, name=None):
    return mat(name or f"paper_{os.path.basename(image)}", "#ffffff", rough=rough, image=image)


def assign(obj, m):
    if obj.data and hasattr(obj.data, "materials"):
        obj.data.materials.clear()
        obj.data.materials.append(m)
    for c in obj.children:
        assign(c, m)
    return obj


# ------------------------------------------------------------------ objects
def _finish(obj, name, loc, rot, scale, material, smooth, bevel):
    if name:
        obj.name = name
    obj.location = loc
    obj.rotation_euler = [math.radians(a) for a in rot]
    obj.scale = scale if isinstance(scale, (tuple, list)) else (scale,) * 3
    if bevel:
        mod = obj.modifiers.new("bevel", "BEVEL")
        mod.width = bevel
        mod.segments = 3
        mod.limit_method = "ANGLE"
    if smooth and obj.type == "MESH":
        for p in obj.data.polygons:
            p.use_smooth = True
        if bevel:
            try:
                obj.data.set_sharp_from_angle(angle=math.radians(40))
            except Exception:
                pass
    if material is not None:
        assign(obj, material)
    return obj


def box(size=(1, 1, 1), loc=(0, 0, 0), rot=(0, 0, 0), material=None, bevel=0.03, name=None):
    bpy.ops.mesh.primitive_cube_add(size=1)
    o = bpy.context.object
    o.scale = size
    bpy.ops.object.transform_apply(scale=True)
    return _finish(o, name, loc, rot, 1, material, True, bevel)


def sphere(r=0.5, loc=(0, 0, 0), scale=1, material=None, seg=48, name=None):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, segments=seg, ring_count=seg // 2)
    return _finish(bpy.context.object, name, loc, (0, 0, 0), scale, material, True, 0)


def cylinder(r=0.5, depth=1, loc=(0, 0, 0), rot=(0, 0, 0), material=None, verts=48, bevel=0.01, name=None):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=depth, vertices=verts)
    return _finish(bpy.context.object, name, loc, rot, 1, material, True, bevel)


def torus(r=0.5, thick=0.12, loc=(0, 0, 0), rot=(0, 0, 0), material=None, name=None):
    bpy.ops.mesh.primitive_torus_add(major_radius=r, minor_radius=thick, major_segments=64, minor_segments=24)
    return _finish(bpy.context.object, name, loc, rot, 1, material, True, 0)


def cone(r=0.5, depth=1, loc=(0, 0, 0), rot=(0, 0, 0), material=None, name=None):
    bpy.ops.mesh.primitive_cone_add(radius1=r, depth=depth, vertices=48)
    return _finish(bpy.context.object, name, loc, rot, 1, material, True, 0)


def plane(w=10, d=10, loc=(0, 0, 0), rot=(0, 0, 0), material=None, name=None):
    bpy.ops.mesh.primitive_plane_add(size=1)
    o = bpy.context.object
    o.scale = (w, d, 1)
    bpy.ops.object.transform_apply(scale=True)
    return _finish(o, name, loc, rot, 1, material, False, 0)


def floor(color="#1b2229", rough=0.55, size=60, z=0.0, curve=True):
    """A seamless studio floor that bends up into a back wall (cyclorama)."""
    if not curve:
        return plane(size, size, (0, 0, z), material=mat("floor", color, rough=rough), name="floor")
    bpy.ops.mesh.primitive_plane_add(size=1)
    o = bpy.context.object
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.object.mode_set(mode="OBJECT")
    me = o.data
    import bmesh
    bm = bmesh.new()
    n = 24
    verts = []
    for i in range(n + 1):
        t = i / n
        if t < 0.6:
            y, zz = -size / 2 + t / 0.6 * size * 0.6, 0
        else:
            a = (t - 0.6) / 0.4 * math.pi / 2
            rr = size * 0.25
            y, zz = size * 0.1 + math.sin(a) * rr, rr - math.cos(a) * rr
        verts.append((bm.verts.new((-size / 2, y, zz + z)), bm.verts.new((size / 2, y, zz + z))))
    for i in range(n):
        bm.faces.new((verts[i][0], verts[i][1], verts[i + 1][1], verts[i + 1][0]))
    bm.to_mesh(me)
    bm.free()
    for p in me.polygons:
        p.use_smooth = True
    o.name = "floor"
    assign(o, mat("floor", color, rough=rough))
    return o


def text3d(body, size=1.0, loc=(0, 0, 0), rot=(90, 0, 0), material=None, font="display", extrude=0.06,
           bevel=0.01, align="CENTER", name=None):
    """3D text standing up, facing -Y (towards a camera on -Y) by default."""
    bpy.ops.object.text_add()
    o = bpy.context.object
    o.data.body = body
    o.data.size = size
    o.data.extrude = extrude
    o.data.bevel_depth = bevel
    o.data.align_x = align
    o.data.align_y = "CENTER"
    f = FONTS.get(font, font)
    if os.path.exists(f):
        o.data.font = bpy.data.fonts.load(f)
    return _finish(o, name, loc, rot, 1, material, False, 0)


def empty(loc=(0, 0, 0), name="target"):
    o = bpy.data.objects.new(name, None)
    bpy.context.scene.collection.objects.link(o)
    o.location = loc
    return o


def group(objs, name="group", loc=(0, 0, 0)):
    """Parent objects to an empty so they move together."""
    e = empty(loc, name)
    for o in objs:
        o.parent = e
        o.location = (o.location[0] - loc[0], o.location[1] - loc[1], o.location[2] - loc[2])
    return e


# ------------------------------------------------------------------ light and camera
def area_light(loc, target=(0, 0, 0), power=400, size=2.0, color="#ffffff", name=None):
    d = bpy.data.lights.new(name or "area", "AREA")
    d.energy = power
    d.size = size
    d.color = _col(color)
    o = bpy.data.objects.new(name or "area", d)
    bpy.context.scene.collection.objects.link(o)
    o.location = loc
    look_at(o, target)
    return o


def studio(target=(0, 0, 1), key="#ffe2c2", rim="#8fd3ff", fill="#9fb4c8", scale=1.0):
    """Three-point light: warm key from upper-left front, cool rim from behind, soft fill."""
    tx, ty, tz = target
    area_light((tx - 4 * scale, ty - 4 * scale, tz + 4 * scale), target, 900 * scale ** 2, 3 * scale, key, "key")
    area_light((tx + 4 * scale, ty + 5 * scale, tz + 3 * scale), target, 700 * scale ** 2, 2 * scale, rim, "rim")
    area_light((tx + 5 * scale, ty - 3 * scale, tz + 1 * scale), target, 150 * scale ** 2, 5 * scale, fill, "fill")


def look_at(obj, target):
    t = target.location if hasattr(target, "location") else mathutils.Vector(target)
    d = t - obj.location
    obj.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()


def camera(loc=(0, -8, 2), target=(0, 0, 1), lens=50, fstop=2.8, focus=None, name="cam"):
    """Camera that always looks at `target` (an empty you can animate). focus = object or distance for DOF."""
    c = bpy.data.cameras.new(name)
    c.lens = lens
    o = bpy.data.objects.new(name, c)
    bpy.context.scene.collection.objects.link(o)
    bpy.context.scene.camera = o
    o.location = loc
    tgt = target if hasattr(target, "location") else empty(target, "cam_target")
    tr = o.constraints.new("TRACK_TO")
    tr.target = tgt
    tr.track_axis = "TRACK_NEGATIVE_Z"
    tr.up_axis = "UP_Y"
    if fstop:
        c.dof.use_dof = True
        c.dof.aperture_fstop = fstop
        if focus is None:
            c.dof.focus_object = tgt
        elif hasattr(focus, "location"):
            c.dof.focus_object = focus
        else:
            c.dof.focus_distance = focus
    o["target"] = tgt.name
    return o, tgt


# ------------------------------------------------------------------ animation
def key(obj, t, loc=None, rot=None, scale=None, ease="EASE_IN_OUT", **props):
    """Keyframe at time t (s). rot in degrees. Extra props: any obj attribute, e.g. hide_render=True."""
    f = int(round(t * FPS)) + 1
    if loc is not None:
        obj.location = loc
        obj.keyframe_insert("location", frame=f)
    if rot is not None:
        obj.rotation_euler = [math.radians(a) for a in rot]
        obj.keyframe_insert("rotation_euler", frame=f)
    if scale is not None:
        obj.scale = scale if isinstance(scale, (tuple, list)) else (scale,) * 3
        obj.keyframe_insert("scale", frame=f)
    for k, v in props.items():
        setattr(obj, k, v)
        obj.keyframe_insert(k, frame=f)
    _ease(obj, ease)
    return obj


def _ease(obj, ease):
    ad = obj.animation_data
    if not ad or not ad.action:
        return
    try:
        curves = ad.action.fcurves
    except AttributeError:   # Blender 5 layered actions
        curves = [fc for layer in ad.action.layers for strip in layer.strips
                  for bag in strip.channelbags for fc in bag.fcurves]
    for fc in curves:
        for kp in fc.keyframe_points:
            kp.interpolation = "BEZIER" if ease != "LINEAR" else "LINEAR"
            if ease != "LINEAR":
                kp.easing = "AUTO"


def pop_in(obj, t, dur=0.35, overshoot=1.12):
    """Scale from 0 with a small overshoot."""
    s = tuple(obj.scale)
    key(obj, t, scale=(0.001, 0.001, 0.001))
    key(obj, t + dur * 0.7, scale=tuple(v * overshoot for v in s))
    key(obj, t + dur, scale=s)
    return obj


def show_at(obj, t):
    """Hidden before t, visible from t."""
    key(obj, 0, hide_render=True, ease="LINEAR")
    key(obj, t, hide_render=False, ease="LINEAR")
    for c in obj.children:
        show_at(c, t)


def spin(obj, deg_per_s, axis=2):
    """Constant rotation for the whole shot."""
    sc = bpy.context.scene
    r0 = list(obj.rotation_euler)
    obj.keyframe_insert("rotation_euler", frame=sc.frame_start)
    r1 = list(r0)
    r1[axis] += math.radians(deg_per_s * (sc.frame_end - sc.frame_start) / FPS)
    obj.rotation_euler = r1
    obj.keyframe_insert("rotation_euler", frame=sc.frame_end)
    _ease(obj, "LINEAR")


# ------------------------------------------------------------------ physics
def rigid(obj, active=True, mass=1.0, friction=0.6, bounce=0.1, shape="CONVEX_HULL"):
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.rigidbody.object_add()
    rb = obj.rigid_body
    rb.type = "ACTIVE" if active else "PASSIVE"
    rb.mass = mass
    rb.friction = friction
    rb.restitution = bounce
    rb.collision_shape = shape
    obj.select_set(False)
    return obj


def bake_physics():
    sc = bpy.context.scene
    if sc.rigidbody_world:
        sc.rigidbody_world.point_cache.frame_start = sc.frame_start
        sc.rigidbody_world.point_cache.frame_end = sc.frame_end
        bpy.ops.ptcache.bake_all(bake=True)


# ------------------------------------------------------------------ compositing
def _compositor():
    """Glare (bloom) + soft vignette in the compositor."""
    sc = bpy.context.scene
    bloom = _STATE.get("bloom", 0.25)
    if bloom <= 0:
        return
    try:
        sc.use_nodes = True
        nt = sc.node_tree
        rl = nt.nodes.get("Render Layers") or nt.nodes.new("CompositorNodeRLayers")
        comp = nt.nodes.get("Composite") or nt.nodes.new("CompositorNodeComposite")
        g = nt.nodes.new("CompositorNodeGlare")
        g.glare_type = "BLOOM" if hasattr(g, "glare_type") else g.glare_type
        try:
            g.threshold = 0.8
            g.mix = -1 + bloom * 2
        except Exception:
            pass
        nt.links.new(rl.outputs["Image"], g.inputs["Image"])
        nt.links.new(g.outputs["Image"], comp.inputs["Image"])
    except Exception as e:  # compositor API changes between Blender versions: bloom is optional
        print("blendkit: bloom skipped:", e)


def render(out_dir, every=1):
    """Render all frames (or every n-th) to out_dir/0001.png ..."""
    sc = bpy.context.scene
    _compositor()
    os.makedirs(out_dir, exist_ok=True)
    only = os.environ.get("BK_FRAMES")          # preview: render just these frame numbers, e.g. "1,60,120"
    todo = [int(x) for x in only.split(",")] if only else range(sc.frame_start, sc.frame_end + 1, every)
    for f in todo:
        sc.frame_set(f)
        sc.render.filepath = os.path.join(out_dir, f"{f:04d}.png")
        bpy.ops.render.render(write_still=True)


# ------------------------------------------------------------------ reusable props
TEX = os.path.join(ROOT, "assets", "tex")


def apple(loc=(0, 0, 0), r=0.16, color="#b3141c", name="apple"):
    """A glossy apple with stem and leaf, sitting on loc (loc = bottom)."""
    x, y, z = loc
    body = sphere(r, (x, y, z + r * 0.88), (1, 1, 0.88), organic(color, "apple_skin"), name=name)
    stem = cylinder(r * 0.06, r * 0.45, (x, y, z + r * 1.85), (12, 0, 0), clay("#4a3220", "stem"), verts=12, bevel=0)
    leaf = sphere(r * 0.5, (x + r * 0.25, y, z + r * 1.78), (0.55, 0.22, 0.05), plastic("#3f8a3a", 0.4, "leaf"))
    leaf.rotation_euler = (0, math.radians(-25), math.radians(20))
    stem.parent = body
    leaf.parent = body
    stem.location = (0, 0, r * 0.97 / 0.88)
    leaf.location = (r * 0.25 / 1, 0, r * 0.9 / 0.88)
    return body


def banknote(image=None, loc=(0, 0, 0), rot=(0, 0, 0), w=0.62, name="note", bend=0.0):
    """A banknote (thin double-sided card) with a texture from assets/tex."""
    image = image or os.path.join(TEX, "note_1.png")
    from PIL import Image as _I
    iw, ih = _I.open(image).size
    h = w * ih / iw
    bpy.ops.mesh.primitive_plane_add(size=1)
    o = bpy.context.object
    o.scale = (w, h, 1)
    bpy.ops.object.transform_apply(scale=True)
    if bend:
        bpy.ops.object.mode_set(mode="EDIT")
        bpy.ops.mesh.subdivide(number_cuts=16)
        bpy.ops.object.mode_set(mode="OBJECT")
        m = o.modifiers.new("bend", "SIMPLE_DEFORM")
        m.deform_method = "BEND"
        m.angle = math.radians(bend)
        m.deform_axis = "Y"
    sol = o.modifiers.new("thick", "SOLIDIFY")
    sol.thickness = 0.002
    return _finish(o, name, loc, rot, 1, paper(image, 0.55, f"paper_{os.path.basename(image)}"), False, 0)


def price_tag(front, back=None, loc=(0, 0, 0), w=0.5, name="tag"):
    """A card tag; `back` image shows when it flips 180 degrees around Z."""
    from PIL import Image as _I
    iw, ih = _I.open(front).size
    h = w * ih / iw
    f = plane(w, h, (0, -0.002, 0), (90, 0, 0), paper(front, 0.5, "tag_front"), name=name + "_front")
    parts = [f]
    if back:
        b = plane(w, h, (0, 0.002, 0), (90, 0, 180), paper(back, 0.5, "tag_back"), name=name + "_back")
        parts.append(b)
    return _tag_group(parts, name, loc)


def _tag_group(parts, name, loc):
    e = empty(loc, name)
    for p in parts:
        p.parent = e
    return e


def printer(loc=(0, 0, 0), scale=1.0, name="printer"):
    """A chunky money printer. Returns (root, slot_world_position). Bills come out of the slot towards -Y."""
    s = scale
    body_m = mat("printer_body", "#2c343c", rough=0.32, metal=0.6, coat=0.4)
    trim_m = metal("#c9a24a", 0.3, "printer_trim")
    dark = mat("printer_slot", "#07090b", rough=0.6)
    parts = [
        box((1.7 * s, 1.1 * s, 1.0 * s), (0, 0, 0.5 * s), material=body_m, bevel=0.06 * s),
        box((1.5 * s, 0.9 * s, 0.35 * s), (0, 0.05 * s, 1.17 * s), material=body_m, bevel=0.05 * s),
        box((1.2 * s, 0.06 * s, 0.09 * s), (0, -0.56 * s, 0.72 * s), material=dark, bevel=0.01 * s),
        box((1.74 * s, 1.14 * s, 0.05 * s), (0, 0, 0.98 * s), material=trim_m, bevel=0.01 * s),
        cylinder(0.05 * s, 1.15 * s, (0, -0.58 * s, 0.79 * s), (0, 90, 0), metal("#9aa3ab", 0.25, "roller"), verts=24),
        cylinder(0.05 * s, 1.15 * s, (0, -0.58 * s, 0.65 * s), (0, 90, 0), metal("#9aa3ab", 0.25, "roller"), verts=24),
        sphere(0.05 * s, (0.6 * s, -0.56 * s, 1.17 * s), 1, glow("#3dff8a", 12, "led")),
        box((0.5 * s, 0.03 * s, 0.18 * s), (-0.35 * s, -0.47 * s, 1.17 * s), material=glow("#6fc3c0", 2.5, "screen"), bevel=0.01 * s),
    ]
    root = _tag_group(parts, name, loc)
    slot = (loc[0], loc[1] - 0.6 * s, loc[2] + 0.72 * s)
    return root, slot
