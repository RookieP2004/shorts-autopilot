# 2026-11-18-dossier: preview of the "case file" pieces (noir desk, blind-stripe light, phone, SIM, papers, envelope, cloche).
import os
from autopilot import devices

A = ASSETS
LOCK = os.path.join(A, "scr_lock.png")
devices.screen({"kind": "lock", "time": "8:14", "date": "Thursday", "notes": [{"app": "Bank", "title": "Rs 49,000 debited",
                "body": "IMPS DR from XXXX 4410"}]}, None, 600, 1336).save(LOCK)
SLIPS = devices.doc_texture("slips", os.path.join(A, "doc_slips.png"), red_rows=(4, 9, 13), title="16 TRANSACTIONS")
FORM = devices.doc_texture("form", os.path.join(A, "doc_form.png"))


def desk(w=1080, h=1920):
    reset(w, h, samples=32, bloom=0.3, exposure=0.1)
    noir_desk((0, 0, 0))


# 1. the phone on the desk, cut by stripes of light (hero, 9:16)
desk()
body, scr = phone((0, 0, 0.042), (-90, 0, 24), w=0.42, screen_image=LOCK)
cam, _ = camera((0.25, -2.0, 1.55), (0, 0, 0), lens=45, fstop=2.2, focus=2.5)
dutch(cam, 4)
still("plate_desk_phone", samples=32)

# 2. papers + a SIM card (9:16)
desk()
doc_sheet(os.path.join(A, "doc_slips.png"), (-0.25, 0.15, 0.003), (0, 0, 12), w=0.9)
doc_sheet(os.path.join(A, "doc_form.png"), (0.45, -0.25, 0.006), (0, 0, -8), w=0.75)
sim_card((-0.1, -0.55, 0.01), (0, 0, -18), w=0.5)
camera((0.2, -2.4, 2.2), (0.05, -0.05, 0), lens=40, fstop=3.0, focus=3.2)
still("plate_desk_docs", samples=32)

# 3. evidence under glass: a SIM in a cloche (9:16)
desk()
cloche((0, 0.2, 0), r=0.55)
sim_card((0, 0.2, 0.3), (60, 0, 15), w=0.42)
cam, _ = camera((0.2, -2.6, 0.9), (0, 0.2, 0.45), lens=50, fstop=2.0, focus=2.8)
still("plate_cloche", samples=32)

# 4. never share: the gold envelope (9:16)
desk()
envelope((0.05, 0.0, 0.02), (0, 0, -14), w=0.8)
camera((0.3, -1.9, 1.5), (0, 0, 0), lens=45, fstop=2.4, focus=2.4)
still("plate_envelope", samples=32)

# 5. the long-video version (16:9): phone, papers and SIM on one desk
desk(1920, 1080)
doc_sheet(os.path.join(A, "doc_slips.png"), (-0.9, 0.3, 0.003), (0, 0, 10), w=0.9)
phone((0.25, -0.05, 0.042), (-90, 0, -18), w=0.42, screen_image=LOCK)
sim_card((0.95, 0.2, 0.01), (0, 0, 20), w=0.45)
cam, _ = camera((0.0, -2.9, 1.7), (0, 0.05, 0), lens=35, fstop=2.8, focus=3.2)
dutch(cam, -3)
still("plate_desk_wide_16x9", 1920, 1080, samples=32)
