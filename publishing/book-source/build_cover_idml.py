# -*- coding: utf-8 -*-
"""REVELATION — Blurb ImageWrap cover as an editable InDesign document."""
import json, os, sys
from idml_lib import Doc

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = "/Users/alirahman/Desktop/test/revelations/book/indesign"

PAGES  = int(sys.argv[1]) if len(sys.argv) > 1 else 164
TRIM_W, TRIM_H = 900.0, 765.0          # 12.5 x 10.625 in
WRAP   = 35.748                        # 0.4965 in, measured from Blurb's own template
PER_PG = 0.006763 * 72                 # spine growth per page, from Blurb's 152pp = 1.028 in
SPINE  = round(PAGES * PER_PG, 3)
W = TRIM_W * 2 + SPINE + WRAP * 2
H = TRIM_H + WRAP * 2
print("cover for %d pages: %.3f x %.3f in  (spine %.3f in)" % (PAGES, W/72, H/72, SPINE/72))

doc = Doc(W, H, 0.0, 0, 0, 0, 0, facing=False)
for n, c, m, y, k in [
    ("Gold",      31.0, 45.5, 91.0,  9.0),
    ("GoldLight", 21.6, 28.6, 64.3,  0.0),
    ("GoldDim",   38.0, 48.0, 86.0, 22.0),
    ("Cream",      8.6, 10.2, 23.1,  0.0),
    ("Sand",      18.0, 22.0, 42.0,  8.0),
    ("Night",     69.4, 67.5, 67.5, 84.3)]:
    doc.color(n, c, m, y, k)
doc.font("EB Garamond", [("Regular","EBGaramond-Regular"),("Italic","EBGaramond-Italic"),
                         ("SemiBold","EBGaramond-SemiBold")])
doc.font("Cinzel", [("Regular","Cinzel-Regular"),("SemiBold","Cinzel-SemiBold")])
doc.font("Space Grotesk", [("Medium","SpaceGrotesk-Medium"),("Regular","SpaceGrotesk-Regular")])
CIN, EBG, SG = "Cinzel", "EB Garamond", "Space Grotesk"
JC, JR = "CenterAlign", "RightAlign"
P = doc.pstyle
P("CovTitle",  font=CIN, FontStyle="SemiBold", PointSize=78, leading=82, Tracking=145,
  Justification=JC, FillColor="Color/Gold")
P("CovSub",    font=CIN, FontStyle="Regular", PointSize=12, leading=18, Tracking=440,
  Justification=JC, SpaceBefore=24, FillColor="Color/GoldLight")
P("CovLede",   font=EBG, FontStyle="Italic", PointSize=14.5, leading=20, Justification=JC,
  SpaceBefore=26, FillColor="Color/Sand")
P("CovAuthor", font=SG, FontStyle="Medium", PointSize=9, leading=14, Tracking=400,
  Capitalization="AllCaps", Justification=JC, FillColor="Color/GoldLight")
P("Spine",     font=CIN, FontStyle="Regular", PointSize=13.5, leading=18, Tracking=300,
  Justification=JC, FillColor="Color/Gold")
P("BackLead",  font=EBG, FontStyle="Regular", PointSize=16, leading=25.6, SpaceAfter=16,
  FillColor="Color/Cream")
P("BackBody",  font=EBG, FontStyle="Regular", PointSize=13.5, leading=23, SpaceAfter=16,
  FillColor="Color/Sand")
P("MarkN",     font=CIN, FontStyle="SemiBold", PointSize=20, leading=22, FillColor="Color/Gold")
P("MarkL",     font=SG, FontStyle="Medium", PointSize=7, leading=11, Tracking=240,
  Capitalization="AllCaps", SpaceBefore=4, FillColor="Color/Sand")
P("Imprint",   font=SG, FontStyle="Medium", PointSize=7.5, leading=12, Tracking=340,
  Capitalization="AllCaps", FillColor="Color/GoldDim")
P("IsbnLbl",   font=SG, FontStyle="Regular", PointSize=6, leading=10, Tracking=200,
  Capitalization="AllCaps", Justification=JC, FillColor="Color/GoldDim")

p = doc.add_page()
p.rect(0, 0, W, H, fill="Color/Night")
dims = json.load(open(os.path.join(HERE, "indesign", "coverbg_dims.json")))
p.image(0, 0, W, H, BASE + "/cover_bg.jpg", dims[0], dims[1], fit="cover")

BACK_X  = WRAP
SPINE_X = WRAP + TRIM_W
FRONT_X = WRAP + TRIM_W + SPINE
PY_ = WRAP

def frame(x, inset, extra=0):
    p.rect(x + inset, PY_ + inset, TRIM_W - 2*inset, TRIM_H - 2*inset,
           fill="Swatch/None", stroke="Color/GoldDim", sw=1.1 if not extra else 0.5)
for x in (BACK_X, FRONT_X):
    frame(x, 46); frame(x, 54, 1)

# ---- front ----
st = (doc.story().para("CovTitle", "REVELATION")
      .para("CovSub", "AN ILLUMINATED PROPHECY IN SIX MOVEMENTS"))
p.text(FRONT_X, PY_ + 236, TRIM_W, 150, st.id)
p.rect(FRONT_X + (TRIM_W - 168)/2, PY_ + 424, 168, 0.8, fill="Color/GoldDim")
st = doc.story().para("CovLede", "After the Apocalypse Tapestry of Angers")
p.text(FRONT_X, PY_ + 440, TRIM_W, 30, st.id)
st = doc.story().para("CovAuthor", "Ali Rahman")
p.text(FRONT_X, PY_ + TRIM_H - 118, TRIM_W, 20, st.id)

# ---- spine ---- (rotated 90° counter-clockwise)
sid = doc.story().para("Spine", "REVELATION  ·  RAHMAN").id
sx, sy = SPINE_X + SPINE/2.0, PY_ + TRIM_H - 96
doc.spreads[0].items.append(
    '<TextFrame Self="%s" ParentStory="%s" PreviousTextFrame="n" NextTextFrame="n" '
    'ContentType="TextType" ItemTransform="0 -1 1 0 %s %s" '
    'AppliedObjectStyle="ObjectStyle/$ID/[Normal Text Frame]" ItemLayer="ua" Visible="true" '
    'Name="$ID/" FillColor="Swatch/None" StrokeColor="Swatch/None" StrokeWeight="0">%s'
    '<TextFramePreference TextColumnCount="1" TextColumnGutter="0" VerticalJustification="CenterAlign" '
    'FirstBaselineOffset="AscentOffset"><Properties><InsetSpacing type="list">'
    '<ListItem type="unit">0</ListItem><ListItem type="unit">0</ListItem>'
    '<ListItem type="unit">0</ListItem><ListItem type="unit">0</ListItem>'
    '</InsetSpacing></Properties></TextFramePreference></TextFrame>'
    % (doc.uid("tf"), sid,
       ("%.3f" % (sx - SPINE/2.0 - H/2.0 + H/2.0)), ("%.3f" % (sy - H/2.0)),
       __import__("idml_lib").rect_path(420, SPINE)))
for dy in (60, TRIM_H - 180):
    p.rect(SPINE_X + SPINE/2.0 - 0.25, PY_ + dy, 0.5, 120, fill="Color/GoldDim")

# ---- back ----
st = (doc.story()
      .para("BackLead", "Ninety compartments were woven at Angers between 1377 and 1382 — "
                        "the whole of Revelation, rendered as a sequence you could walk "
                        "alongside. Twenty of them no longer exist.")
      .para("BackBody", "This book rebuilds all ninety, in the original order, against the "
                        "original anchors, and marks on every plate whether what you are "
                        "looking at survives, survives only in fragments, or has been "
                        "reconstructed. The complete text of the Revelation to John is set "
                        "alongside, with the words of Christ in red."))
p.text(BACK_X + 104, PY_ + 170, TRIM_W - 234, 300, st.id)
p.rect(BACK_X + 104, PY_ + TRIM_H - 200, TRIM_W - 234, 0.5, fill="Color/GoldDim")
for i, (num, lbl) in enumerate([("90","Compartments"),("6","Movements"),("22","Chapters")]):
    st = doc.story().para("MarkN", num).para("MarkL", lbl)
    p.text(BACK_X + 104 + i*104, PY_ + TRIM_H - 182, 100, 48, st.id)
st = doc.story().para("Imprint", "Divergent World")
p.text(BACK_X + 104, PY_ + TRIM_H - 118, 260, 16, st.id)
p.rect(BACK_X + TRIM_W - 272, PY_ + TRIM_H - 172, 142, 72,
       fill="Swatch/None", stroke="Color/GoldDim", sw=0.6)
st = doc.story().para("IsbnLbl", "ISBN")
p.text(BACK_X + TRIM_W - 272, PY_ + TRIM_H - 142, 142, 14, st.id)

out = os.path.join(HERE, "indesign", "REVELATION_cover.idml")
doc.write(out)
print("wrote", out, os.path.getsize(out)//1024, "KB")
