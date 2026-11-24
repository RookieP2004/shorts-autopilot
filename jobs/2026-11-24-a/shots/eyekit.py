# Shared builder for 2026-11-24-a's animated eye shots: a big glossy 3D eyeball on the night set, an infrared LED, beams,
# a nanoparticle contact lens and an upper eyelid. Exec'd by the shot scripts (they already have every blendkit helper).
import bmesh, math
import bpy

IR_DIM = "#5a0d14"      # infrared drawn as a faint deep red (it is invisible to us)
GREEN = NIGHT["green"]


def eye_set():
    night_set(target=(0, 0, 1.0), rim=NIGHT["rim"], spot_power=9000, spot_height=7, spot_angle=40, grid=True)


def eyeball(loc=(0, 0, 1.0), r=0.5, iris="#2f7f86"):
    x, y, z = loc
    sc = sphere(r, loc, 1, mat("sclera", "#f2ece3", rough=0.22, sss=0.25, coat=0.8), seg=64, name="sclera")
    ir = cylinder(r * 0.44, 0.02, (x, y - r * 0.93, z), (90, 0, 0), mat("iris", iris, rough=0.35, emit=iris, emit_strength=0.0),
                  verts=64, bevel=0.004, name="iris")
    pu = cylinder(r * 0.18, 0.024, (x, y - r * 0.935, z), (90, 0, 0), mat("pupil", "#05070a", rough=0.2), verts=48, bevel=0.003,
                  name="pupil")
    co = sphere(r * 0.5, (x, y - r * 0.80, z), (1, 0.42, 1), glass("#ffffff", 0.01, "cornea"), seg=48, name="cornea")
    # thin red veins: a few tiny tori on the sclera's sides
    return sc, ir, pu, co


def iris_glow(t0, t1, strength=6.0, color=None):
    m = bpy.data.materials["iris"]
    p = m.node_tree.nodes.get("Principled BSDF")
    if color:
        p.inputs["Emission Color"].default_value = (*hexrgb(color), 1) if len(hexrgb(color)) == 3 else hexrgb(color)
    s = p.inputs["Emission Strength"]
    s.default_value = 0.0
    s.keyframe_insert("default_value", frame=int(t0 * FPS) + 1)
    s.default_value = strength
    s.keyframe_insert("default_value", frame=int(t1 * FPS) + 1)


def led(loc=(1.6, -1.2, 1.0), target=(0, -0.4, 1.0)):
    body = cylinder(0.09, 0.22, loc, (0, 0, 0), mat("led_body", "#20252e", rough=0.3, metal=0.6), verts=32, name="led")
    look_at(body, target)
    bulb = sphere(0.085, loc, 1, glow("#7a1018", 3.0, "led_bulb"), seg=24, name="led_bulb")
    return body, bulb


def beam(a, b, color, strength, r=0.035, name="beam"):
    ax, ay, az = a; bx, by, bz = b
    dx, dy, dz = bx - ax, by - ay, bz - az
    L = math.sqrt(dx * dx + dy * dy + dz * dz)
    c = cylinder(r, L, ((ax + bx) / 2, (ay + by) / 2, (az + bz) / 2), (0, 0, 0), glow(color, strength, name + "_m"), verts=16,
                 bevel=0, name=name)
    c.rotation_mode = "QUATERNION"
    import mathutils
    c.rotation_quaternion = mathutils.Vector((dx, dy, dz)).to_track_quat("Z", "Y")
    return c


def contact_lens(loc, r=0.27, name="lens"):
    """A thin glass cap dotted with gold nanoparticles (drawn huge: the real ones are ~45 nm)."""
    x, y, z = loc
    cap = sphere(r, loc, (1, 0.12, 1), mat(name + "_g", "#dff6ff", rough=0.03, transmission=0.95, ior=1.4, coat=1.0), seg=48,
                 name=name)
    gm = glow(NIGHT["gold"], 2.2, name + "_np")
    import random
    rnd = random.Random(3)
    dots = []
    for k in range(42):
        a = rnd.uniform(0, 6.283); rr = r * math.sqrt(rnd.uniform(0, 0.85))
        dx, dz = rr * math.cos(a), rr * math.sin(a)
        dy = -r * 0.12 * math.sqrt(max(0.0, 1 - (rr / r) ** 2)) - 0.004
        d = sphere(0.0065, (x + dx, y + dy, z + dz), 1, gm, seg=8, name=f"{name}_np{k}")
        d.parent = cap
        d.matrix_parent_inverse = cap.matrix_world.inverted()
        dots.append(d)
    return cap, dots


def eyelid(loc=(0, 0, 1.0), r=0.53, name="lid"):
    """Upper eyelid: a dome shell pivoting on the eye's horizontal axis. rot x = -100 (open) -> 0 (closed)."""
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=64, v_segments=32, radius=r)
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.y > 0.0], context="VERTS")   # keep the front half (y<0)
    bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(ob)
    ob.location = loc
    for p in me.polygons:
        p.use_smooth = True
    sol = ob.modifiers.new("solid", "SOLIDIFY"); sol.thickness = 0.03
    assign(ob, mat("skin", "#c98e62", rough=0.45, sss=0.3))
    # lash line: a thin dark torus along the rim
    return ob
