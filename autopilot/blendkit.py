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
    if isinstance(rgb, str):
        rgb = hexrgb(rgb)
    bg.inputs[0].default_value = (*rgb[:3], 1)
    bg.inputs[1].default_value = strength
    return w


HDRI_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "third_party", "lemo", "core", "assets",
                        "polyhaven")
HDRIS = {"lounge": "lythwood_lounge_2k.hdr", "studio": "photo_studio_loft_hall_2k.hdr"}   # Poly Haven, CC0


def world_hdri(name="studio", strength=0.35, rotate=0.0, tint=None, backdrop=(0.6, 0.6, 0.62)):
    """Image-based light from a real room (Poly Haven CC0, fetched with scripts/fetch_instruments.sh): softer, more "real"
    reflections and fill than flat world light. Keep it low (0.2-0.5) and let the set's own key light lead. The room
    itself is never seen: camera rays see `backdrop` (a colour; None shows the room). Falls back to world_color."""
    path = os.path.join(HDRI_DIR, HDRIS.get(name, name))
    if not os.path.exists(path):
        return world_color(tint or (0.8, 0.8, 0.82), strength)
    w = bpy.data.worlds.get("World") or bpy.data.worlds.new("World")
    bpy.context.scene.world = w
    w.use_nodes = True
    nt = w.node_tree
    bg = nt.nodes.get("Background")
    env = nt.nodes.new("ShaderNodeTexEnvironment")
    env.image = bpy.data.images.load(path, check_existing=True)
    mp = nt.nodes.new("ShaderNodeMapping")
    tc = nt.nodes.new("ShaderNodeTexCoord")
    mp.inputs["Rotation"].default_value[2] = math.radians(rotate)
    nt.links.new(tc.outputs["Generated"], mp.inputs["Vector"])
    nt.links.new(mp.outputs["Vector"], env.inputs["Vector"])
    if tint:
        mix = nt.nodes.new("ShaderNodeMix")
        mix.data_type = "RGBA"
        mix.blend_type = "MULTIPLY"
        mix.inputs[0].default_value = 1.0
        mix.inputs[7].default_value = (*(hexrgb(tint) if isinstance(tint, str) else tint)[:3], 1)
        nt.links.new(env.outputs["Color"], mix.inputs[6])
        nt.links.new(mix.outputs[2], bg.inputs[0])
    else:
        nt.links.new(env.outputs["Color"], bg.inputs[0])
    bg.inputs[1].default_value = strength
    if backdrop is not None:                      # light from the room, but the camera sees a plain backdrop
        out = nt.nodes.get("World Output")
        flat = nt.nodes.new("ShaderNodeBackground")
        flat.inputs[0].default_value = (*(hexrgb(backdrop) if isinstance(backdrop, str) else backdrop)[:3], 1)
        flat.inputs[1].default_value = 1.0
        lp = nt.nodes.new("ShaderNodeLightPath")
        mx = nt.nodes.new("ShaderNodeMixShader")
        nt.links.new(lp.outputs["Is Camera Ray"], mx.inputs[0])
        nt.links.new(bg.outputs[0], mx.inputs[1])
        nt.links.new(flat.outputs[0], mx.inputs[2])
        nt.links.new(mx.outputs[0], out.inputs["Surface"])
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


# ------------------------------------------------------------------ stills and cut-outs (the cheap path)
ASSET_DIR = os.environ.get("BK_ASSETS", "")


def _save_camera(path, w, h):
    """Camera data next to a plate, so characters can be placed by floor position (autopilot.stage)."""
    import json
    sc = bpy.context.scene
    cam = sc.camera
    if cam is None:
        return
    bpy.context.view_layer.update()
    M = [list(r) for r in cam.matrix_world]
    json.dump({"matrix_world": M, "lens": cam.data.lens, "sensor": cam.data.sensor_width, "fit": cam.data.sensor_fit,
               "w": w, "h": h}, open(path, "w"))


def still(name, w=1080, h=1920, samples=32, transparent=False, crop=False, pad=12, frame=1, only=None):
    """Render the current scene once to <assets>/<name>.png. transparent+crop = a prop cut-out (sprite)
    that the 2D compositor animates. only=[objects] renders just those (transparent, same camera): a foreground
    layer (counter, table) that sits in front of the 2D characters. Plates also save <name>.json camera data.
    Use reset() before building each new still."""
    sc = bpy.context.scene
    hidden = []
    if only is not None:
        keep = set()
        for o in only:
            keep.add(o)
            keep.update(o.children_recursive)
        for o in sc.objects:
            if o.type in ("MESH", "FONT", "CURVE", "EMPTY") and o not in keep and not o.hide_render:
                o.hide_render = True
                hidden.append(o)
        transparent = True
    if os.environ.get("BK_SKIP_EXISTING") and os.path.exists(os.path.join(ASSET_DIR or ".", name + ".png")):
        print("kept", name)
        return os.path.join(ASSET_DIR or ".", name + ".png")
    if os.environ.get("BK_PREVIEW"):                     # quick look: half size, fewer samples
        w, h, samples = w // 2, h // 2, max(8, samples // 3)
    sc.render.resolution_x, sc.render.resolution_y = w, h
    sc.cycles.samples = samples
    sc.render.film_transparent = transparent
    sc.render.image_settings.color_mode = "RGBA" if transparent else "RGB"
    sc.render.use_motion_blur = False
    sc.frame_set(frame)
    out = os.path.join(ASSET_DIR or ".", name + ".png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    sc.render.filepath = out
    bpy.ops.render.render(write_still=True)
    for o in hidden:
        o.hide_render = False
    if not crop:
        _save_camera(out[:-4] + ".json", w, h)
    if crop and transparent:
        from PIL import Image as _I
        im = _I.open(out)
        box = im.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox()
        if box:
            x0, y0, x1, y1 = box
            im.crop((max(0, x0 - pad), max(0, y0 - pad), min(im.width, x1 + pad), min(im.height, y1 + pad))).save(out)
    print("still", out)
    return out


def sprite_camera(obj_center=(0, 0, 0.3), dist=3.0, height=1.2, lens=60, azimuth=-20):
    """A camera framing one prop for a cut-out (3/4 view from the front-left by default)."""
    a = math.radians(azimuth)
    cx, cy, cz = obj_center
    loc = (cx + dist * math.sin(a), cy - dist * math.cos(a), cz + height)
    return camera(loc, obj_center, lens=lens, fstop=0)


# ------------------------------------------------------------------ nicer materials and props (v3)
def wood(color="#a8743f", dark="#7a4e2a", name=None, scale=6.0, rough=0.5):
    """Procedural wood: stretched noise between two browns, light clear coat."""
    m = bpy.data.materials.new(name or f"wood_{color}")
    m.use_nodes = True
    nt = m.node_tree
    p = nt.nodes.get("Principled BSDF")
    p.inputs["Roughness"].default_value = rough
    p.inputs["Coat Weight"].default_value = 0.25
    tc = nt.nodes.new("ShaderNodeTexCoord")
    mp = nt.nodes.new("ShaderNodeMapping")
    mp.inputs["Scale"].default_value = (1.0, scale, scale)
    nz = nt.nodes.new("ShaderNodeTexNoise")
    nz.inputs["Scale"].default_value = 3.0
    nz.inputs["Detail"].default_value = 8.0
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].color = (*hexrgb(dark), 1)
    ramp.color_ramp.elements[1].color = (*hexrgb(color), 1)
    nt.links.new(tc.outputs["Object"], mp.inputs["Vector"])
    nt.links.new(mp.outputs["Vector"], nz.inputs["Vector"])
    nt.links.new(nz.outputs["Fac"], ramp.inputs["Fac"])
    nt.links.new(ramp.outputs["Color"], p.inputs["Base Color"])
    return m


def apple_mat(red="#b3121b", yellow="#e0a32a", name="apple_v3"):
    """Red apple skin blushing to yellow, with a soft wax sheen."""
    m = bpy.data.materials.get(name)
    if m:
        return m
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    p = nt.nodes.get("Principled BSDF")
    p.inputs["Roughness"].default_value = 0.32
    p.inputs["Coat Weight"].default_value = 0.35
    p.inputs["Subsurface Weight"].default_value = 0.08
    nz = nt.nodes.new("ShaderNodeTexNoise")
    nz.inputs["Scale"].default_value = 1.4
    nz.inputs["Detail"].default_value = 2.0
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].position = 0.55
    ramp.color_ramp.elements[0].color = (*hexrgb(red), 1)
    ramp.color_ramp.elements[1].position = 0.95
    ramp.color_ramp.elements[1].color = (*hexrgb(yellow), 1)
    nt.links.new(nz.outputs["Fac"], ramp.inputs["Fac"])
    nt.links.new(ramp.outputs["Color"], p.inputs["Base Color"])
    return m


def lathe(profile, segments=40, loc=(0, 0, 0), material=None, subdiv=1, name="lathe"):
    """Revolve a profile [(radius, z), ...] (bottom to top) around Z: smooth round objects (apples, vases, bowls)."""
    import bmesh
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    rings = []
    for r, z in profile:
        ring = []
        for k in range(segments):
            a = 2 * math.pi * k / segments
            ring.append(bm.verts.new((r * math.cos(a), r * math.sin(a), z)))
        rings.append(ring)
    for i in range(len(rings) - 1):
        for k in range(segments):
            k2 = (k + 1) % segments
            bm.faces.new((rings[i][k], rings[i][k2], rings[i + 1][k2], rings[i + 1][k]))
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-5)
    bm.to_mesh(me)
    bm.free()
    o = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(o)
    o.location = loc
    for poly in me.polygons:
        poly.use_smooth = True
    if subdiv:
        m = o.modifiers.new("subd", "SUBSURF")
        m.levels = m.render_levels = subdiv
    if material is not None:
        assign(o, material)
    return o


APPLE_PROFILE = [(0.0, 0.04), (0.18, 0.02), (0.42, 0.06), (0.7, 0.2), (0.9, 0.42), (0.95, 0.6), (0.86, 0.8),
                 (0.66, 0.95), (0.42, 1.0), (0.22, 0.95), (0.08, 0.86), (0.0, 0.84)]


def apple2(loc=(0, 0, 0), r=0.08, name="apple", red="#b3121b"):
    """A smooth, natural apple (lathe profile with a dimpled top), stem and leaf. loc = bottom."""
    x, y, z = loc
    prof = [(a * r, b * r * 1.9) for a, b in APPLE_PROFILE]
    body = lathe(prof, 36, (x, y, z), apple_mat(red, name=f"apple_{red}"), 1, name)
    stem = cylinder(r * 0.06, r * 0.5, (0, 0, r * 1.9 * 0.95), (8, 0, 0), clay("#4a3220", "stem"), verts=10, bevel=0)
    stem.parent = body
    leaf = sphere(r * 0.45, (r * 0.28, 0, r * 1.9 * 0.98), (0.6, 0.24, 0.05), plastic("#4c9a3f", 0.4, "leaf"))
    leaf.rotation_euler = (0, math.radians(-28), math.radians(25))
    leaf.parent = body
    return body


# ------------------------------------------------------------------ night set (v4: dark-files, scams, money traps, reveals)
NIGHT = {"bg": "#04070e", "floor": "#0a1322", "spot": "#fff4e2", "rim": "#3fa9ff", "rim_red": "#ff3b4a",
         "green": "#35e08a", "red": "#ff3b4a", "gold": "#f4c04e", "blue": "#4aa3ff"}


def spot_light(loc, target=(0, 0, 0), power=2500, angle=38, blend=0.25, radius=0.08, color="#fff4e2", name="spot"):
    """A hard theatre spot: small radius = crisp shadows, `angle` = cone width in degrees."""
    d = bpy.data.lights.new(name, "SPOT")
    d.energy = power
    d.spot_size = math.radians(angle)
    d.spot_blend = blend
    d.shadow_soft_size = radius
    d.color = _col(color)
    o = bpy.data.objects.new(name, d)
    bpy.context.scene.collection.objects.link(o)
    o.location = loc
    look_at(o, target)
    return o


def night_set(target=(0, 0, 0), rim="#3fa9ff", spot_power=16000, spot_height=9.0, spot_angle=36, floor_color=None,
              floor_rough=0.42, grid=True, grid_color="#1d3b66", grid_step=1.0, grid_extent=14, fill=0.04, back_wall=None, wall_glow=0.35):
    """The second house mood: near-black navy surroundings, ONE hard spotlight from above on `target`, a coloured rim light
    from behind, a slightly glossy floor that catches both, optional faint floor grid. Pair with camera(..., fstop=2.0, roll=4)
    for the shallow-focus, Dutch-tilted hero shots. back_wall = an image (e.g. a glowing chart) on a huge plane far behind."""
    tx, ty, tz = target
    world_color(NIGHT["bg"], fill)
    floor(color=floor_color or NIGHT["floor"], rough=floor_rough, size=80, curve=False)
    spot_light((tx, ty - 1.0, tz + spot_height), (tx, ty, tz), spot_power, spot_angle, color=NIGHT["spot"], name="night_spot")
    area_light((tx + 3.0, ty + 5.0, tz + 5.5), (tx, ty, tz + 0.8), 700, 1.5, rim, "night_rim")
    area_light((tx - 5.0, ty + 4.0, tz + 5.0), (tx, ty, tz + 0.8), 260, 1.5, "#7a5cff", "night_rim2")
    if grid:
        gm = glow(grid_color, 1.6, "night_grid")
        n = int(grid_extent / grid_step)
        for i in range(-n, n + 1):
            plane(grid_extent * 2, 0.012, (tx, ty + i * grid_step, 0.002), material=gm, name=f"gx{i}")
            plane(0.012, grid_extent * 2, (tx + i * grid_step, ty, 0.002), material=gm, name=f"gy{i}")
    if back_wall:
        from PIL import Image as _I
        iw, ih = _I.open(back_wall).size
        wall = plane(30, 30 * ih / iw, (tx, ty + 16, 8), rot=(90, 0, 0), name="night_wall")
        m = mat("night_wall_mat", "#000000", rough=1.0)
        nt = m.node_tree
        tex = nt.nodes.new("ShaderNodeTexImage")
        tex.image = bpy.data.images.load(back_wall)
        em = nt.nodes.new("ShaderNodeEmission")
        em.inputs["Strength"].default_value = wall_glow
        nt.links.new(tex.outputs["Color"], em.inputs["Color"])
        out = [n_ for n_ in nt.nodes if n_.type == "OUTPUT_MATERIAL"][0]
        nt.links.new(em.outputs["Emission"], out.inputs["Surface"])
        assign(wall, m)


def dutch(cam, deg):
    """Tilt a camera made by camera() around its viewing axis (a Dutch angle) while it keeps tracking its target."""
    tr = [c for c in cam.constraints if c.type == "TRACK_TO"]
    if tr:
        bpy.context.view_layer.update()
        mw = cam.matrix_world.copy()
        cam.constraints.remove(tr[0])
        cam.matrix_world = mw
    cam.rotation_mode = "XYZ"
    q = cam.rotation_euler.to_quaternion() @ mathutils.Quaternion((0, 0, 1), math.radians(deg))
    cam.rotation_euler = q.to_euler()
    bpy.context.view_layer.update()
    return cam


def _person_mesh(h=0.34, name="crowd_person"):
    """One low-poly faceless figure (capsule body + head), feet at z=0, `h` metres tall."""
    import bmesh
    bm = bmesh.new()
    r = h * 0.17
    bmesh.ops.create_uvsphere(bm, u_segments=10, v_segments=6, radius=h * 0.12,
                              matrix=mathutils.Matrix.Translation((0, 0, h * 0.87)))
    ret = bmesh.ops.create_cone(bm, cap_ends=True, segments=10, radius1=r, radius2=r * 0.82, depth=h * 0.68,
                                matrix=mathutils.Matrix.Translation((0, 0, h * 0.36)))
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    for p in me.polygons:
        p.use_smooth = True
    return me


def crowd(area=(-4, 4, -3, 3), n=4000, h=0.3, colors=("#c9d2e3",), color_of=None, glow_of=None, seed=7, jitter=0.35,
          rough=0.35, name="crowd"):
    """A carpet of `n` tiny figures standing on the floor inside area=(x0, x1, y0, y1): a big number made visible.
    color_of(i, x, y, u, v) -> hex picks each figure's colour (u, v = 0..1 across the area), e.g. halves blue/yellow,
    survivors green; glow_of(i, x, y, u, v) -> True makes that figure emissive (survivors that light up).
    Figures are linked duplicates of one mesh (fast; 5-10k is fine). Returns the list of objects."""
    import random
    rnd = random.Random(seed)
    x0, x1, y0, y1 = area
    aspect = (x1 - x0) / max(0.01, y1 - y0)
    cols = max(1, int(round(math.sqrt(n * aspect))))
    rows = max(1, int(math.ceil(n / cols)))
    me = _person_mesh(h, name + "_mesh")
    me.materials.append(mat(name + "_base", colors[0], rough=rough))
    mats = {}

    def m_for(c, g):
        k = (c, g)
        if k not in mats:
            mats[k] = (glow(c, 3.0, f"{name}_g_{c}") if g else mat(f"{name}_{c}", c, rough=rough))
        return mats[k]
    coll = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(coll)
    objs = []
    dx, dy = (x1 - x0) / cols, (y1 - y0) / rows
    i = 0
    for r in range(rows):
        for c in range(cols):
            if i >= n:
                break
            u, v = (c + 0.5) / cols, (r + 0.5) / rows
            x = x0 + u * (x1 - x0) + (rnd.random() - 0.5) * dx * jitter
            y = y0 + v * (y1 - y0) + (rnd.random() - 0.5) * dy * jitter
            col = color_of(i, x, y, u, v) if color_of else colors[i % len(colors)]
            g = bool(glow_of and glow_of(i, x, y, u, v))
            o = bpy.data.objects.new(f"{name}_{i}", me)
            o.data = me
            o.location = (x, y, 0)
            o.rotation_euler = (0, 0, rnd.uniform(-0.6, 0.6))
            sc = 0.9 + rnd.random() * 0.2
            o.scale = (sc, sc, sc)
            coll.objects.link(o)
            objs.append((o, m_for(col, g)))
            i += 1
    # per-object materials: link the material to the OBJECT slot so one shared mesh can carry many colours
    for o, m in objs:
        o.material_slots[0].link = "OBJECT"
        o.material_slots[0].material = m
    return [o for o, _ in objs]


def glossy_black(name="gloss_black"):
    return mat(name, "#05070b", rough=0.08, metal=0.0)


def phone(loc=(0, 0, 0), rot=(0, 0, 0), w=0.8, frame="#2a2f3a", screen_image=None, name="phone"):
    """A glossy hero phone (generic, no brand): bevelled metal frame, black glass front, camera bump on the back.
    screen_image = a PNG from autopilot.devices (shown emissive); None = black glass, for a live screen composited later
    (phone_sprite() saves where the screen sits). Height = 2.1 x w. Returns (body, screen)."""
    h, t = w * 2.1, w * 0.1
    body = box((w, t, h), loc, rot, material=mat(name + "_frame", frame, rough=0.22, metal=1.0), bevel=w * 0.11, name=name)
    sw, sh = w * 0.9, h * 0.955
    scr = plane(sw, sh, (0, -t / 2 - 0.002, 0), rot=(90, 0, 0), name=name + "_screen")
    if screen_image:
        m = mat(name + "_scr", "#000000", rough=0.05)
        nt = m.node_tree
        tex = nt.nodes.new("ShaderNodeTexImage")
        tex.image = bpy.data.images.load(screen_image)
        em = nt.nodes.new("ShaderNodeEmission")
        em.inputs["Strength"].default_value = 1.4
        mix = nt.nodes.new("ShaderNodeAddShader")
        bsdf = [n_ for n_ in nt.nodes if n_.type == "BSDF_PRINCIPLED"][0]
        nt.links.new(tex.outputs["Color"], em.inputs["Color"])
        nt.links.new(em.outputs["Emission"], mix.inputs[0])
        nt.links.new(bsdf.outputs["BSDF"], mix.inputs[1])
        out = [n_ for n_ in nt.nodes if n_.type == "OUTPUT_MATERIAL"][0]
        nt.links.new(mix.outputs["Shader"], out.inputs["Surface"])
        assign(scr, m)
    else:
        assign(scr, glossy_black(name + "_glass"))
    scr.parent = body
    cam_bump = box((w * 0.34, t * 0.4, w * 0.34), (-w * 0.24, t * 0.6, h * 0.36), material=glossy_black(name + "_bump"),
                   bevel=w * 0.06, name=name + "_bump")
    cam_bump.parent = body
    for i, (cx, cz) in enumerate(((-w * 0.31, h * 0.42), (-w * 0.17, h * 0.3))):
        lens = cylinder(w * 0.055, t * 0.3, (cx, t * 0.8, cz), (90, 0, 0), material=glass("#0a0c12"), name=f"{name}_lens{i}")
        lens.parent = body
    return body, scr


def screen_corners(scr):
    """Screen-pixel corners (TL, TR, BR, BL) of a phone screen plane in the current camera view."""
    from bpy_extras.object_utils import world_to_camera_view
    sc = bpy.context.scene
    bpy.context.view_layer.update()
    W, H = sc.render.resolution_x, sc.render.resolution_y
    vs = [scr.matrix_world @ v.co for v in scr.data.vertices]
    pts = []
    for v in vs:
        p = world_to_camera_view(sc, sc.camera, v)
        pts.append((p.x * W, (1 - p.y) * H))
    cx = sum(p[0] for p in pts) / 4
    cy = sum(p[1] for p in pts) / 4
    tl = min((p for p in pts if p[1] < cy), key=lambda p: p[0])
    tr = max((p for p in pts if p[1] < cy), key=lambda p: p[0])
    br = max((p for p in pts if p[1] >= cy), key=lambda p: p[0])
    bl = min((p for p in pts if p[1] >= cy), key=lambda p: p[0])
    return [tl, tr, br, bl]


def phone_sprite(name, scr, w=1080, h=1920, samples=48, pad=12):
    """Render a phone cut-out and save <name>.json with the screen quad (in the cropped sprite's pixels), so the
    compositor can draw any live screen UI (autopilot.devices) into it: the `phone` layer."""
    import json
    sc = bpy.context.scene
    if os.environ.get("BK_PREVIEW"):
        w, h = w // 2, h // 2
    sc.render.resolution_x, sc.render.resolution_y = w, h
    corners = screen_corners(scr)
    out = still(name, w, h, samples=samples, transparent=True, crop=False)
    from PIL import Image as _I
    im = _I.open(out)
    box_ = im.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox()
    x0, y0, x1, y1 = box_
    x0, y0 = max(0, x0 - pad), max(0, y0 - pad)
    im.crop((x0, y0, min(im.width, x1 + pad), min(im.height, y1 + pad))).save(out)
    json.dump({"screen": [[round(px - x0, 2), round(py - y0, 2)] for px, py in corners]}, open(out[:-4] + ".json", "w"))
    return out


def coin(loc=(0, 0, 0), rot=(90, 0, 0), r=0.5, symbol="₹", name="coin"):
    """A thick gold coin with a raised rim and an embossed symbol on both faces (fictional, no real design)."""
    t = r * 0.16
    gold = metal(NIGHT["gold"], 0.22, name + "_gold")
    c = cylinder(r, t, loc, rot, material=gold, verts=96, bevel=r * 0.05, name=name)
    for side in (1, -1):
        rim = torus(r * 0.9, r * 0.05, (0, 0, side * t / 2), material=gold, name=f"{name}_rim{side}")
        rim.parent = c
        s = text3d(symbol, size=r * 1.0, loc=(0, -r * 0.05, side * t / 2), rot=(0, 0 if side > 0 else 180, 0),
                   material=gold, font="body", extrude=r * 0.03, name=f"{name}_sym{side}")
        s.parent = c
    return c


# ------------------------------------------------------------------ noir desk (v5: "case file" documentary look)
NOIR = {"bg": "#0b1018", "desk": "#2a2f38", "wall": "#141a24", "sun": "#ffb46b", "cream": "#efe6d2", "gold": "#d9a441",
        "red": "#e2484d", "green": "#3ecf8e"}


def blinds(target=(0, 0, 0), from_dir=(-1.0, -0.6, 0.9), dist=7.0, power=9000, color="#ffb46b", slats=48, gap=0.13, angle=26,
           size=6.0, name="blinds"):
    """Warm light through venetian blinds: a hard spot with a row of slats in front of it, so crisp stripes of light fall
    across the desk / floor / wall (the noir 'case file' look). from_dir = direction the light comes FROM (towards the window)."""
    tx, ty, tz = target
    v = mathutils.Vector(from_dir).normalized()
    loc = mathutils.Vector((tx, ty, tz)) + v * dist
    sp = spot_light(tuple(loc), target, power, angle, blend=0.05, radius=0.02, color=color, name=name + "_sun")
    blk = mat(name + "_slat", "#000000", rough=1.0)
    rig = bpy.data.objects.new(name + "_rig", None)
    bpy.context.scene.collection.objects.link(rig)
    rig.location = tuple(mathutils.Vector((tx, ty, tz)) + v * (dist * 0.8))
    look_at(rig, target)
    h = gap * slats
    for i in range(slats):
        s = box((size, 0.02, gap * 0.55), (0, (i - slats / 2) * gap, 0), (90, 0, 0), material=blk, bevel=0.0, name=f"{name}_s{i}")
        s.parent = rig
        s.visible_camera = False
        s.visible_glossy = False
    return sp


def noir_desk(target=(0, 0, 0), desk="#3a4250", wall=True, sun=NOIR["sun"], sun_power=7000, fill=0.35, rough=0.42,
              from_dir=(-1.0, -0.5, 0.85), slats=60, gap=0.12):
    """The case-file set: a dark desk top (z = 0) that fills the frame, a dark wall behind, and warm blind-stripes of light
    across both. Put props (phone_sprite props, sim_card, doc_sheet, envelope, cloche) on it; frame with a 35-50 mm lens
    looking down 25-45 degrees; fstop 2-3 for the soft background."""
    world_color("#1c2433", fill)
    floor(color=desk, rough=rough, size=40, curve=False)
    if wall:
        w = plane(40, 12, (target[0], target[1] + 6.0, 6.0), rot=(90, 0, 0), name="noir_wall")
        assign(w, mat("noir_wall_mat", NOIR["wall"], rough=0.8))
    blinds(target, from_dir, 8.0, sun_power, sun, slats, gap, 30, 12.0)
    area_light((target[0] + 4, target[1] - 5, 4), target, 260, 8.0, "#7f9cc8", "noir_fill")
    area_light((target[0] - 1, target[1] - 3, 3), target, 120, 3.0, "#ffd9b0", "noir_bounce")


def sim_card(loc=(0, 0, 0), rot=(0, 0, 0), w=0.85, color=NOIR["cream"], name="sim"):
    """A big fictional SIM card: cream plastic with a clipped corner and a gold contact chip."""
    import bmesh
    h, t = w * 0.66, w * 0.02
    bm = bmesh.new()
    c = w * 0.16
    pts = [(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2 - c), (w / 2 - c, h / 2), (-w / 2, h / 2)]
    vs = [bm.verts.new((x, y, 0)) for x, y in pts]
    bm.faces.new(vs)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    o = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(o)
    o.location, o.rotation_euler = loc, tuple(math.radians(a) for a in rot)
    so = o.modifiers.new("solid", "SOLIDIFY")
    so.thickness = t
    so.offset = 1.0
    bv = o.modifiers.new("bevel", "BEVEL")
    bv.width = t * 0.4
    bv.segments = 2
    assign(o, mat(name + "_plastic", color, rough=0.5))
    chip = box((w * 0.28, w * 0.22, t * 0.4), (-w * 0.18, 0, t + t * 0.1), material=metal(NOIR["gold"], 0.25, name + "_chip"),
               bevel=w * 0.02, name=name + "_chip")
    chip.parent = o
    for i in (-1, 1):
        ln = box((w * 0.28, 0.006, 0.003), (-w * 0.18, i * w * 0.05, t * 1.35), material=mat(name + "_cut", "#8a6a2a"), bevel=0,
                 name=f"{name}_cut{i}")
        ln.parent = o
    return o


def doc_sheet(image, loc=(0, 0, 0), rot=(0, 0, 0), w=1.0, curl=0.06, name="doc"):
    """A sheet of paper lying on the desk (image = a texture from autopilot.devices.doc_texture), with a slight curl."""
    from PIL import Image as _I
    iw, ih = _I.open(image).size
    h = w * ih / iw
    bpy.ops.mesh.primitive_grid_add(x_subdivisions=24, y_subdivisions=24, size=1, location=loc)
    o = bpy.context.active_object
    o.name = name
    o.scale = (w, h, 1)
    for v in o.data.vertices:
        u = v.co.x + 0.5
        v.co.z = curl * (u - 0.5) ** 2 * 2 / max(w, 0.01)
    bpy.ops.object.transform_apply(scale=True)
    o.rotation_euler = tuple(math.radians(a) for a in rot)
    assign(o, paper(image))
    return o


def envelope(loc=(0, 0, 0), rot=(0, 0, 0), w=0.9, color=NOIR["gold"], lock=True, name="env"):
    """A gold envelope (metallic paper) with an embossed padlock: 'private / never share' moments."""
    h = w * 0.62
    body = box((w, h, 0.02), loc, rot, material=mat(name + "_m", color, rough=0.32, metal=0.65), bevel=0.01, name=name)
    import bmesh
    bm = bmesh.new()
    a, b, c = bm.verts.new((-w / 2, h / 2, 0.012)), bm.verts.new((w / 2, h / 2, 0.012)), bm.verts.new((0, -h * 0.02, 0.012))
    bm.faces.new((a, b, c))
    me = bpy.data.meshes.new(name + "_flap")
    bm.to_mesh(me)
    bm.free()
    flap = bpy.data.objects.new(name + "_flap", me)
    bpy.context.scene.collection.objects.link(flap)
    flap.parent = body
    assign(flap, mat(name + "_flapm", color, rough=0.25, metal=0.75))
    if lock:
        lk = box((w * 0.12, w * 0.1, 0.02), (0, -h * 0.05, 0.03), material=metal("#f1d48a", 0.2, name + "_lock"), bevel=0.01, name=name + "_lock")
        lk.parent = body
        sh = torus(w * 0.04, w * 0.012, (0, -h * 0.05 + w * 0.06, 0.03), (0, 0, 0), material=metal("#f1d48a", 0.2, name + "_lock2"),
                   name=name + "_shackle")
        sh.parent = body
    return body


def cloche(loc=(0, 0, 0), r=0.7, base="#16181e", name="cloche"):
    """A glass dome on a dark round plinth: put the 'evidence' under it (a SIM, a key, a coin)."""
    x, y, z = loc
    plinth = cylinder(r * 1.15, r * 0.5, (x, y, z + r * 0.25), material=mat(name + "_base", base, rough=0.3, metal=0.4),
                      verts=96, bevel=0.02, name=name + "_plinth")
    dome = sphere(r, (x, y, z + r * 0.5), material=glass("#ffffff", 0.0, name + "_glass"), seg=64, name=name + "_dome")
    import bmesh
    bm = bmesh.new()
    bm.from_mesh(dome.data)
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.z < -0.001], context="VERTS")
    bm.to_mesh(dome.data)
    bm.free()
    knob = sphere(r * 0.08, (x, y, z + r * 1.55), material=metal("#c9b27a", 0.2, name + "_knob"), name=name + "_knob")
    return plinth, dome, knob
