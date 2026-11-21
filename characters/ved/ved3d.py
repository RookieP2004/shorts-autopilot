"""3D Ved: the same flat-vector Ved built as a layered paper standee in a real 3D scene (2D characters in a 3D world).

Each pose is split into three depth layers (body, head, forearms in front). Every layer is cut along its own
silhouette, printed on card with a thin cream paper edge, and stood a few centimetres apart, so the camera can orbit
and light him like an object while he stays exactly the character the audience knows.

    python characters/ved/ved3d.py --pose explain --angles -32,0,28 --out /tmp/ved3d
    python characters/ved/ved3d.py --pose explain --orbit 2.0 --out /tmp/ved3d_orbit     # frames for a short orbit
"""
import argparse
import io
import math
import os
import sys

import numpy as np
import cv2
import cairosvg
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
import make                                        # noqa: E402
import bpy                                         # noqa: E402
import bmesh                                       # noqa: E402
from autopilot import blendkit as bk              # noqa: E402

HEIGHT_M = 1.75                       # Ved's height in the 3D world
LAYERS = (("body", 0.0), ("head", -0.022), ("front", -0.044))   # depth toward the camera (m)
TEX_W = 1200


def layer_png(pose, layer, path):
    svg = make.figure(**make.POSES[pose], layer=layer, shadow=False)
    png = cairosvg.svg2png(bytestring=svg.encode(), output_width=TEX_W)
    im = Image.open(io.BytesIO(png)).convert("RGBA")
    a = np.asarray(im)[..., 3]
    if a.max() < 10:
        return None, None
    # bleed colour 3 px past the edge so the cut never shows a white fringe
    arr = np.asarray(im).copy()
    rgb = arr[..., :3].astype(np.float32)
    m = (a > 0).astype(np.float32)
    for _ in range(3):
        blur = cv2.blur(rgb * m[..., None], (3, 3))
        bm = cv2.blur(m, (3, 3))
        fill = (m == 0) & (bm > 0)
        rgb[fill] = blur[fill] / bm[fill][..., None]
        m = np.maximum(m, (bm > 0).astype(np.float32))
    arr[..., :3] = rgb.clip(0, 255).astype(np.uint8)
    arr[..., 3] = 255
    Image.fromarray(arr, "RGBA").save(path)
    return path, a


def contours(alpha):
    mask = (alpha > 110).astype(np.uint8) * 255
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    cs, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    out = []
    for c in cs:
        if cv2.contourArea(c) < 400:
            continue
        c = cv2.approxPolyDP(c, 1.2, True)[:, 0, :]
        out.append(c)
    return out


def standee(name, tex, alpha, depth, thick=0.008):
    h_px, w_px = alpha.shape
    s = HEIGHT_M / h_px * (1500 / 1500)
    face_mat = bk.mat(f"{name}_print", "#ffffff", rough=0.6, image=tex)
    nt = face_mat.node_tree                     # a little self-light keeps the flat colours true to the 2D Ved
    p, t = nt.nodes["Principled BSDF"], [n for n in nt.nodes if n.type == "TEX_IMAGE"][0]
    nt.links.new(t.outputs["Color"], p.inputs["Emission Color"])
    p.inputs["Emission Strength"].default_value = 0.22
    edge_mat = bk.mat(f"{name}_edge", "#efe3c8", rough=0.8)
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new()
    edges = []
    for c in contours(alpha):
        vs = [bm.verts.new(((x - w_px / 2) * s, depth, (h_px - y) * s - 0.022)) for x, y in c[::-1]]
        edges += [bm.edges.new((vs[i], vs[(i + 1) % len(vs)])) for i in range(len(vs))]
    bmesh.ops.triangle_fill(bm, use_beauty=True, use_dissolve=False, edges=edges, normal=(0, -1, 0))
    for f in bm.faces:
        if f.normal.y > 0:                      # print faces the camera (-Y)
            f.normal_flip()
        for lp in f.loops:
            x, _, z = lp.vert.co
            lp[uv].uv = (x / s / w_px + 0.5, (z + 0.022) / s / h_px)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(ob)
    ob.data.materials.append(face_mat)
    ob.data.materials.append(edge_mat)
    sol = ob.modifiers.new("card", "SOLIDIFY")
    sol.thickness = thick
    sol.offset = 1.0
    sol.material_offset_rim = 1
    bev = ob.modifiers.new("soft", "BEVEL")
    bev.width = 0.0012
    bev.segments = 2
    return ob


def build(pose, tmp):
    os.makedirs(tmp, exist_ok=True)
    obs = []
    for layer, depth in LAYERS:
        tex, alpha = layer_png(pose, layer, os.path.join(tmp, f"{pose}_{layer}.png"))
        if tex:
            obs.append(standee(f"ved_{layer}", tex, alpha, depth))
    # a small base so he stands like a figure on a table-top world
    base = bk.cylinder(r=0.34, depth=0.03, loc=(0, -0.02, 0.015), material=bk.mat("base", "#1d2a33", rough=0.4, coat=0.4))
    ring = bk.torus(r=0.34, thick=0.012, loc=(0, -0.02, 0.03), material=bk.metal("#d4a64a", rough=0.3))
    return obs + [base, ring]


def scene(w, h, samples, dur=1.0):
    bk.reset(w=w, h=h, samples=samples, dur=dur, motion_blur=False, bloom=0.12)
    bk.world_hdri("studio", strength=0.32, backdrop=(0.93, 0.89, 0.8))
    sc = bpy.context.scene
    sc.view_settings.view_transform = "Standard"         # keep the brand colours (AgX greys them)
    sc.view_settings.look = "None"
    sc.view_settings.exposure = -0.75
    bk.floor("#d8c7a2", rough=0.7)
    bk.area_light((-2.2, -2.6, 3.0), (0, 0, 1.0), power=300, size=2.5, color="#ffe6c8")      # warm key
    bk.area_light((2.0, 1.4, 2.2), (0, 0, 1.2), power=480, size=1.2, color="#bfe6ff")         # cool rim (v9 rim colour)
    bk.area_light((1.8, -3.0, 1.2), (0, 0, 0.9), power=90, size=3.0, color="#fff4e6")        # fill


def cam_at(azimuth_deg, dist=3.3, height=1.15, target=(0, 0, 0.92), lens=50):
    a = math.radians(azimuth_deg)
    loc = (dist * math.sin(a), -dist * math.cos(a), height)
    return bk.camera(loc=loc, target=target, lens=lens, fstop=4.0, focus=dist, name=f"cam{int(azimuth_deg)}")[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pose", default="explain")
    ap.add_argument("--angles", default="-30,0,30")
    ap.add_argument("--orbit", type=float, default=0.0, help="seconds of a -35..35 degree orbit (frames)")
    ap.add_argument("--size", default="720x1280")
    ap.add_argument("--samples", type=int, default=40)
    ap.add_argument("--out", default="/tmp/ved3d")
    a = ap.parse_args()
    w, h = map(int, a.size.split("x"))
    os.makedirs(a.out, exist_ok=True)
    scene(w, h, a.samples, dur=a.orbit or 1.0)
    build(a.pose, os.path.join(a.out, "tex"))
    sc = bpy.context.scene
    if a.orbit:
        cam = cam_at(-35)
        n = sc.frame_end
        for f in range(1, n + 1):
            az = -35 + 70 * (0.5 - 0.5 * math.cos(math.pi * (f - 1) / max(1, n - 1)))
            r = math.radians(az)
            cam.location = (3.3 * math.sin(r), -3.3 * math.cos(r), 1.15)
            cam.keyframe_insert("location", frame=f)          # the camera tracks Ved's chest (constraint)
        bk.render(a.out)
        return
    for az in [float(x) for x in a.angles.split(",")]:
        cam = cam_at(az)
        sc.camera = cam
        sc.render.filepath = os.path.join(a.out, f"{a.pose}_{int(az):+d}.png")
        bk._compositor()
        bpy.ops.render.render(write_still=True)


if __name__ == "__main__":
    main()
