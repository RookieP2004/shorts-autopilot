"""Generates every pose of this character from ONE base drawing, so poses never drift.
Add a pose = add an entry to POSES (reuse the eye/mouth/arm parts). Run: python make.py"""
import json, os
D = os.path.dirname(os.path.abspath(__file__))
BODY, DARK, INK = "#2dd4bf", "#0f766e", "#0b1020"

def arm(d): return f'<path d="{d}" stroke="{DARK}" stroke-width="26" fill="none" stroke-linecap="round"/>'
ARMS = {
    "normal": arm("M70 300 Q20 330 34 400") + arm("M330 300 Q380 330 366 400"),
    "up":     arm("M70 290 Q10 240 30 170") + arm("M330 290 Q390 240 370 170"),
    "chin":   arm("M70 300 Q20 330 34 400") + arm("M330 300 Q330 380 250 345"),
}
def stroke(d, w=9): return f'<path d="{d}" stroke="{INK}" stroke-width="{w}" fill="none" stroke-linecap="round"/>'
EYES = {
    "open": f'<circle cx="150" cy="215" r="34" fill="#fff"/><circle cx="250" cy="215" r="34" fill="#fff"/><circle cx="156" cy="220" r="16" fill="{INK}"/><circle cx="256" cy="220" r="16" fill="{INK}"/><circle cx="162" cy="213" r="5" fill="#fff"/><circle cx="262" cy="213" r="5" fill="#fff"/>',
    "closed": stroke("M118 218 Q150 236 182 218") + stroke("M218 218 Q250 236 282 218"),
    "happy": stroke("M118 225 Q150 190 182 225", 10) + stroke("M218 225 Q250 190 282 225", 10),
    "wide": f'<circle cx="150" cy="210" r="42" fill="#fff"/><circle cx="250" cy="210" r="42" fill="#fff"/><circle cx="150" cy="210" r="12" fill="{INK}"/><circle cx="250" cy="210" r="12" fill="{INK}"/>',
    "up": f'<circle cx="150" cy="215" r="34" fill="#fff"/><circle cx="250" cy="215" r="34" fill="#fff"/><circle cx="162" cy="200" r="16" fill="{INK}"/><circle cx="262" cy="200" r="16" fill="{INK}"/>',
}
TONGUE = '<path d="M178 336 Q200 326 222 336 Q212 350 200 350 Q188 350 178 336Z" fill="#f43f5e"/>'
MOUTH = {
    "smile": stroke("M160 300 Q200 330 240 300", 10),
    "open": f'<path d="M162 292 Q200 296 238 292 Q232 352 200 352 Q168 352 162 292 Z" fill="{INK}"/>' + TONGUE,
    "big": f'<path d="M150 285 Q200 292 250 285 Q244 370 200 370 Q156 370 150 285 Z" fill="{INK}"/><path d="M172 350 Q200 336 228 350 Q214 368 200 368 Q186 368 172 350Z" fill="#f43f5e"/>',
    "o": f'<ellipse cx="200" cy="320" rx="22" ry="28" fill="{INK}"/>',
    "O": f'<ellipse cx="200" cy="325" rx="30" ry="40" fill="{INK}"/>',
    "hmm": stroke("M172 312 Q200 302 232 316", 10),
    "hmm_talk": f'<ellipse cx="205" cy="315" rx="20" ry="14" fill="{INK}"/>',
}
BROWS = {"none": "", "up": stroke("M118 158 Q150 140 182 155") + stroke("M218 155 Q250 140 282 158"),
         "think": stroke("M120 170 L180 165") + stroke("M220 160 Q250 145 282 158")}

def draw(eyes, mouth, brows="none", arms="normal"):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 520" width="400" height="520">
<ellipse cx="200" cy="505" rx="120" ry="14" fill="#000" fill-opacity="0.25"/>
<line x1="200" y1="70" x2="200" y2="20" stroke="{DARK}" stroke-width="10" stroke-linecap="round"/>
<circle cx="200" cy="18" r="16" fill="#facc15"/>
{ARMS[arms]}
<rect x="140" y="430" width="34" height="70" rx="16" fill="{DARK}"/>
<rect x="226" y="430" width="34" height="70" rx="16" fill="{DARK}"/>
<rect x="60" y="66" width="280" height="380" rx="120" fill="{BODY}" stroke="{DARK}" stroke-width="8"/>
<ellipse cx="150" cy="130" rx="40" ry="22" fill="#fff" fill-opacity="0.25"/>
{BROWS[brows]}{EYES[eyes]}{MOUTH[mouth]}
</svg>'''

POSES = {  # name: (eyes, mouth, brows, arms)   <pose>_talk = open-mouth frame, <pose>_blink = eyes shut
    "idle": ("open", "smile", "none", "normal"), "talk": ("open", "open", "none", "normal"),
    "blink": ("closed", "smile", "none", "normal"),
    "happy": ("happy", "big", "none", "up"), "happy_talk": ("happy", "open", "none", "up"),
    "shocked": ("wide", "O", "up", "normal"), "shocked_talk": ("wide", "o", "up", "normal"),
    "think": ("up", "hmm", "think", "chin"), "think_talk": ("up", "hmm_talk", "think", "chin"),
}
if __name__ == "__main__":
    for name, parts in POSES.items():
        open(os.path.join(D, name + ".svg"), "w").write(draw(*parts))
    print("wrote", ", ".join(POSES))
