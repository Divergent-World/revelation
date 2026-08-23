# -*- coding: utf-8 -*-
"""REVELATION — 13 x 11 in collector's edition, emitted as an InDesign IDML package."""
import json, os
from idml_lib import Doc
import build as B          # reuse content helpers (status_of, scenes, etc.)
from prose import (FOREWORD, LOSSES, METHOD, MOVEMENT_CODAS, PLATE_NOTES,
                   COLOPHON_LEFT, AUTHOR)

HERE = os.path.dirname(os.path.abspath(__file__))
# LINK_SET=png  -> lossless originals, native resolution, 300 dpi tagged  (default)
# LINK_SET=jpg  -> 3975 px JPEG q92, ~180 MB total, faster to work with
_BASE = "/Users/alirahman/Desktop/test/revelations/book/indesign"
LINK_SET = os.environ.get("LINK_SET", "png")
if LINK_SET == "png":
    LINKS, LINK_EXT, _DIMS = _BASE + "/Links_png", ".png", "linkdims_png.json"
else:
    LINKS, LINK_EXT, _DIMS = _BASE + "/Links", ".jpg", "linkdims.json"
T = B.T; REV = B.REV; SCENES = B.SCENES; TAPS = B.TAPS
DIMS = json.load(open(os.path.join(HERE, "indesign", _DIMS)))
SECT = json.load(open(os.path.join(HERE, "sections.json")))
_ext = os.path.join(HERE, "indesign", "extent.txt")
EXTENT = int(open(_ext).read().strip()) if os.path.exists(_ext) else 0

# ---------------------------------------------------------------- geometry
# Blurb Large Landscape (marketed 13 x 11): actual trim 12.5 x 10.625 in = 900 x 765 pt.
# Blurb's uploader expects an exported page of 12.625 x 10.875 in, which is the trim plus
# 0.125 in bleed on the top, bottom and OUTSIDE edge, and nothing at the gutter.
W, H = 900.0, 765.0
BLEED_DOC = (9.0, 9.0, 0.0, 9.0)      # top, bottom, inside, outside
BLEED = 13.5                          # how far artwork is drawn past trim; excess is clipped
MT, MB, MI, MO = 50.0, 62.0, 64.0, 54.0
CW = W - MI - MO                      # 782 content width
GUT = 31.0
doc = Doc(W, H, BLEED_DOC, MT, MB, MI, MO)

def cx(p):   return MI if p.recto else MO
def cr(p):   return W - (MO if p.recto else MI)

# ---------------------------------------------------------------- colours
# Swatches measured from the ebook PDF's own hex values through a real RGB->CMYK
# transform, so the print edition matches the PDF rather than approximating it.
# Exception: InkSoft and Faint carry small text (5.5-10 pt). Their true conversions are
# four-colour darks, which go fuzzy at that size if the press drifts even slightly, so
# they are kept K-dominant with just enough warmth to read as brown rather than grey.
for n, c, m, y, k in [
    ("Vellum",     7.1,  9.0, 18.8,  0.0),   # #EAE1CE — the page ground
    ("Cream",      8.6, 10.2, 23.1,  0.0),   # #E6DCC4
    ("Rule",      23.9, 24.7, 42.7,  0.0),   # #C3B597
    ("GoldLight", 21.6, 28.6, 64.3,  0.0),   # #C9AE72
    ("Gold",      31.0, 45.5, 91.0,  9.0),   # #A8823C
    ("Rubric",    27.1, 96.1, 96.9, 27.8),   # #8E2420
    ("WJ",        25.1, 99.6, 80.0, 21.6),   # #9B1C31 — words of Christ
    ("Lapis",     98.8, 87.8, 32.2, 21.2),   # #1E3566
    ("Dark",      67.5, 67.5, 68.2, 81.6),   # #171210 — part dividers
    ("Night",     69.4, 67.5, 67.5, 84.3),   # #0E0A08 — frontispiece, full-bleed grounds
    ("Band",      70.2, 67.1, 67.5, 85.5),   # #0A0705 — caption band
    ("InkSoft",    0.0,  6.0, 12.0, 76.0),   # small text: warm, but K-dominant
    ("Faint",      0.0,  5.0, 14.0, 52.0)]:  # running heads at 6 pt
    doc.color(n, c, m, y, k)

doc.font("EB Garamond", [("Regular", "EBGaramond-Regular"), ("Italic", "EBGaramond-Italic"),
                         ("SemiBold", "EBGaramond-SemiBold")])
doc.font("Cinzel", [("Regular", "Cinzel-Regular"), ("SemiBold", "Cinzel-SemiBold")])
doc.font("Space Grotesk", [("Medium", "SpaceGrotesk-Medium"), ("Regular", "SpaceGrotesk-Regular")])
doc.font("Cormorant Garamond", [("Italic", "CormorantGaramond-Italic")])

EBG, CIN, SG, CG = "EB Garamond", "Cinzel", "Space Grotesk", "Cormorant Garamond"
JC, JL, JR, JF = "CenterAlign", "LeftAlign", "RightAlign", "LeftJustified"

def P(name, **kw): doc.pstyle(name, **kw)

# prose
P("Body", font=EBG, FontStyle="Regular", PointSize=10.5, leading=17.8, Justification=JF,
  SpaceAfter=9.4, FillColor="Color/Black", Hyphenation="true")
P("BodyDrop", font=EBG, FontStyle="Regular", PointSize=10.5, leading=17.8, Justification=JF,
  SpaceAfter=9.4, FillColor="Color/Black", Hyphenation="true",
  DropCapCharacters=1, DropCapLines=3, DropCapStyle="CharacterStyle/DropCapRed")
P("H3", font=CIN, FontStyle="SemiBold", PointSize=10.5, leading=14, Tracking=70,
  SpaceBefore=15, SpaceAfter=7, FillColor="Color/Black")
P("Sig", font=SG, FontStyle="Medium", PointSize=6.4, leading=11, Tracking=220,
  Capitalization="AllCaps", SpaceBefore=14, FillColor="Color/InkSoft")
P("SecHead", font=CIN, FontStyle="SemiBold", PointSize=21, leading=25, Tracking=90,
  FillColor="Color/Black")
P("SecKick", font=SG, FontStyle="Medium", PointSize=6.2, leading=10, Tracking=240,
  Capitalization="AllCaps", SpaceBefore=6, FillColor="Color/Gold")
# scripture section
P("ChapKick", font=SG, FontStyle="Medium", PointSize=5.8, leading=9, Tracking=260,
  Capitalization="AllCaps", SpaceBefore=19, FillColor="Color/InkSoft")
P("Chap", font=CIN, FontStyle="SemiBold", PointSize=13.5, leading=16, Tracking=100,
  SpaceAfter=8, FillColor="Color/Rubric")
P("Sc", font=EBG, FontStyle="Regular", PointSize=10.0, leading=16.6, Justification=JF,
  SpaceAfter=7.2, FillColor="Color/Black", Hyphenation="true")
# register
P("RegH", font=SG, FontStyle="Medium", PointSize=6.0, leading=10, Tracking=240,
  Capitalization="AllCaps", SpaceBefore=16, SpaceAfter=6, FillColor="Color/Gold")
P("RegRow", font=EBG, FontStyle="Regular", PointSize=8.6, leading=12.4, SpaceAfter=2.4,
  FillColor="Color/Black",
  tabs=[(46, "LeftAlign", ""), (296, "LeftAlign", ""), (388.5, "RightAlign", "")])
# front matter
P("HalfT", font=CIN, FontStyle="SemiBold", PointSize=30, leading=36, Tracking=340,
  Justification=JC, FillColor="Color/Black")
P("HalfS", font=EBG, FontStyle="Italic", PointSize=11.5, leading=16, Justification=JC,
  SpaceBefore=10, FillColor="Color/InkSoft")
P("TitDrop", font=CIN, FontStyle="Regular", PointSize=9.5, leading=14, Tracking=400,
  Justification=JC, SpaceAfter=26, FillColor="Color/Rubric")
P("TitMain", font=CIN, FontStyle="SemiBold", PointSize=48, leading=50, Tracking=100,
  Justification=JC, FillColor="Color/Black")
P("TitSub", font=EBG, FontStyle="Italic", PointSize=15, leading=20, Justification=JC,
  SpaceBefore=20, SpaceAfter=26, FillColor="Color/InkSoft")
P("TitDesc", font=EBG, FontStyle="Regular", PointSize=10.8, leading=18, Justification=JC,
  FillColor="Color/InkSoft")
P("TitImp", font=SG, FontStyle="Medium", PointSize=6.8, leading=11, Tracking=300,
  Capitalization="AllCaps", Justification=JC, SpaceBefore=24, FillColor="Color/InkSoft")
P("Copy", font=EBG, FontStyle="Regular", PointSize=8.5, leading=13.5, SpaceAfter=9,
  FillColor="Color/InkSoft")
P("CopySm", font=SG, FontStyle="Regular", PointSize=5.9, leading=10, Tracking=160,
  Capitalization="AllCaps", SpaceBefore=16, FillColor="Color/InkSoft")
P("TocH", font=CIN, FontStyle="SemiBold", PointSize=14.5, leading=20, Tracking=280,
  Justification=JC, SpaceAfter=32, FillColor="Color/Black")
P("TocLbl", font=SG, FontStyle="Medium", PointSize=5.8, leading=10, Tracking=260,
  Capitalization="AllCaps", SpaceBefore=22, SpaceAfter=9, FillColor="Color/Gold")
P("TocRow", font=EBG, FontStyle="Regular", PointSize=12.5, leading=19, SpaceAfter=5,
  FillColor="Color/Black", tabs=[(46, "LeftAlign", ""), (560, "RightAlign", " .")])
P("TocRowMin", font=EBG, FontStyle="Regular", PointSize=11, leading=17, SpaceAfter=4,
  FillColor="Color/InkSoft", tabs=[(46, "LeftAlign", ""), (560, "RightAlign", " .")])
# divider
P("DivK", font=SG, FontStyle="Medium", PointSize=6.4, leading=11, Tracking=420,
  Capitalization="AllCaps", Justification=JC, FillColor="Color/Gold")
P("DivT", font=CIN, FontStyle="SemiBold", PointSize=40, leading=46, Tracking=90,
  Justification=JC, SpaceBefore=18, FillColor="Color/GoldLight")
P("DivS", font=EBG, FontStyle="Italic", PointSize=11.5, leading=17, Justification=JC,
  SpaceBefore=26, FillColor="Color/Gold")
# movement opener
P("MvNum", font=CIN, FontStyle="Regular", PointSize=14, leading=18, Tracking=500,
  FillColor="Color/Rubric")
P("MvTitle", font=CIN, FontStyle="SemiBold", PointSize=34, leading=39, Tracking=50,
  SpaceBefore=14, FillColor="Color/Black")
P("MvRange", font=SG, FontStyle="Medium", PointSize=7, leading=12, Tracking=240,
  Capitalization="AllCaps", SpaceBefore=20, FillColor="Color/InkSoft")
P("MvArg", font=EBG, FontStyle="Regular", PointSize=11.8, leading=20.2, Justification=JF,
  SpaceBefore=22, FillColor="Color/Black", DropCapCharacters=1, DropCapLines=3,
  DropCapStyle="CharacterStyle/DropCapRed")
P("MvStatN", font=CIN, FontStyle="SemiBold", PointSize=17, leading=19, FillColor="Color/Rubric")
P("MvStatL", font=SG, FontStyle="Medium", PointSize=5.8, leading=9, Tracking=200,
  Capitalization="AllCaps", SpaceBefore=3, FillColor="Color/InkSoft")
P("MvStrip", font=SG, FontStyle="Regular", PointSize=5.9, leading=10.5, Tracking=100,
  Capitalization="AllCaps", FillColor="Color/Faint")
# plates
P("PlateId", font=SG, FontStyle="Medium", PointSize=6.2, leading=11, Tracking=210,
  Capitalization="AllCaps", FillColor="Color/InkSoft")
P("PlateTitle", font=CIN, FontStyle="SemiBold", PointSize=17, leading=21, Tracking=45,
  SpaceBefore=7, FillColor="Color/Black")
P("PlateAnchor", font=SG, FontStyle="Medium", PointSize=6.6, leading=11, Tracking=190,
  Capitalization="AllCaps", SpaceBefore=6, FillColor="Color/Rubric")
P("PlateSc", font=EBG, FontStyle="Regular", PointSize=10.6, leading=18.2, Justification=JF,
  SpaceBefore=16, FillColor="Color/Black", Hyphenation="true")
P("PlateScSm", font=EBG, FontStyle="Regular", PointSize=9.6, leading=15.6, Justification=JF,
  FillColor="Color/Black", Hyphenation="true")
P("NoteLbl", font=SG, FontStyle="Medium", PointSize=5.9, leading=10, Tracking=220,
  Capitalization="AllCaps", SpaceBefore=18, SpaceAfter=5, FillColor="Color/Gold")
P("NoteBody", font=CG, FontStyle="Italic", PointSize=10.8, leading=16.6,
  FillColor="Color/InkSoft")
P("ProvLbl", font=SG, FontStyle="Medium", PointSize=5.9, leading=10, Tracking=220,
  Capitalization="AllCaps", SpaceAfter=6, FillColor="Color/InkSoft")
P("ProvRow", font=SG, FontStyle="Regular", PointSize=6.2, leading=11.4, Tracking=110,
  Capitalization="AllCaps", FillColor="Color/InkSoft",
  tabs=[(104, "LeftAlign", "")])
P("BleedId", font=SG, FontStyle="Medium", PointSize=6.2, leading=11, Tracking=260,
  Capitalization="AllCaps", FillColor="Color/Cream")
P("BleedTitle", font=CIN, FontStyle="Regular", PointSize=22, leading=26, Tracking=50,
  SpaceBefore=7, FillColor="Color/Cream")
# coda
P("CodaK", font=SG, FontStyle="Medium", PointSize=6, leading=11, Tracking=340,
  Capitalization="AllCaps", Justification=JC, FillColor="Color/Gold")
P("CodaT", font=CIN, FontStyle="SemiBold", PointSize=18, leading=23, Tracking=50,
  Justification=JC, SpaceBefore=14, SpaceAfter=22, FillColor="Color/Black")
P("CodaB", font=EBG, FontStyle="Italic", PointSize=12.2, leading=21, Justification=JC,
  FillColor="Color/InkSoft")
# colophon
P("ColH", font=CIN, FontStyle="SemiBold", PointSize=13, leading=18, Tracking=180,
  SpaceAfter=18, FillColor="Color/Black")
P("ColB", font=EBG, FontStyle="Regular", PointSize=9.8, leading=16.5, SpaceAfter=11,
  FillColor="Color/InkSoft")
P("SpecRow", font=SG, FontStyle="Regular", PointSize=6.6, leading=15, Tracking=120,
  Capitalization="AllCaps", FillColor="Color/InkSoft",
  tabs=[(112, "LeftAlign", "")])
P("Mark", font=CIN, FontStyle="Regular", PointSize=9, leading=14, Tracking=400,
  SpaceBefore=26, FillColor="Color/Rubric")
# running elements
P("RunHead", font=SG, FontStyle="Regular", PointSize=6.1, leading=9, Tracking=240,
  Capitalization="AllCaps", FillColor="Color/Faint")
P("RunHeadR", font=SG, FontStyle="Regular", PointSize=6.1, leading=9, Tracking=240,
  Capitalization="AllCaps", Justification=JR, FillColor="Color/Faint")
P("RunHeadLight", font=SG, FontStyle="Regular", PointSize=6.1, leading=9, Tracking=240,
  Capitalization="AllCaps", FillColor="Color/Cream")
P("RunHeadLightR", font=SG, FontStyle="Regular", PointSize=6.1, leading=9, Tracking=240,
  Capitalization="AllCaps", Justification=JR, FillColor="Color/Cream")
P("Folio", font=SG, FontStyle="Regular", PointSize=6.4, leading=9, Tracking=180,
  FillColor="Color/InkSoft")
P("FolioR", font=SG, FontStyle="Regular", PointSize=6.4, leading=9, Tracking=180,
  Justification=JR, FillColor="Color/InkSoft")
P("FrontisCap", font=SG, FontStyle="Regular", PointSize=5.9, leading=10, Tracking=260,
  Capitalization="AllCaps", Justification=JC, FillColor="Color/InkSoft")
P("FrontisCapLight", font=SG, FontStyle="Regular", PointSize=5.9, leading=10, Tracking=260,
  Capitalization="AllCaps", Justification=JC, FillColor="Color/Cream")

doc.cstyle("DropCapRed", font=CIN, FontStyle="SemiBold", FillColor="Color/Rubric")
doc.cstyle("WJ", FillColor="Color/WJ")
doc.cstyle("VNum", font=SG, FontStyle="Medium", PointSize=5.6, FillColor="Color/Rubric",
           Position="Superscript")
doc.cstyle("Cont", font=EBG, FontStyle="Italic", FillColor="Color/InkSoft")
doc.cstyle("Chip", font=SG, FontStyle="Medium", PointSize=5.6, FillColor="Color/Lapis")

# ---------------------------------------------------------------- helpers
def verse_runs(text, ranges):
    if not ranges: return [(None, text)]
    out, cur = [], 0
    for r in sorted(ranges, key=lambda x: x["start"]):
        a, b = max(0, r["start"]), min(len(text), r["end"])
        if a > cur: out.append((None, text[cur:a]))
        out.append(("WJ", text[a:b])); cur = max(cur, b)
    if cur < len(text): out.append((None, text[cur:]))
    return out

def anchor_runs(scene, maxw=165):
    runs, words, trunc = [], 0, False
    for p in scene.get("passages", []):
        for v in p["verses"]:
            n = len(v["text"].split())
            if words + n > maxw and runs: trunc = True; break
            runs.append(("VNum", str(v["verse"]) + " "))
            runs.extend(verse_runs(v["text"], v.get("wordsOfJesus")))
            runs.append((None, " "))
            words += n
        if trunc: break
    if trunc:
        runs.append(("Cont", "… %s continues in the complete text." % scene["displayReference"]))
    return runs

def rule(p, x, y, w, color="Color/Rule", weight=0.5):
    p.rect(x, y, w, weight, fill=color)

def vrule(p, x, y, h, color="Color/Rule", weight=0.4):
    p.rect(x, y, weight, h, fill=color)

def running(p, txt, light=False):
    if not txt: return
    base = "RunHeadLight" if light else ("RunHeadR" if p.recto else "RunHead")
    if light and p.recto: base = "RunHeadLightR"
    st = doc.story().para(base, txt)
    p.text(cx(p), MT - 26, CW, 14, st.id)

def folio(p):
    st = doc.story().para("FolioR" if p.recto else "Folio", str(p.n))
    p.text(cx(p), H - MB + 22, CW, 14, st.id)

def newpage(rt=None, fol=True, bg="Color/Vellum"):
    """Every page starts with its ground. InDesign pages are white unless you draw one."""
    p = doc.add_page()
    if bg:
        p.rect(-BLEED, -BLEED, W + 2 * BLEED, H + 2 * BLEED, fill=bg)
    if rt: running(p, rt)
    if fol: folio(p)
    return p

def ensure_recto():
    """Insert a blank verso so the next page falls on a right-hand page."""
    if doc.page_count % 2 == 1:
        b = doc.add_page()
        b.rect(-BLEED, -BLEED, W + 2 * BLEED, H + 2 * BLEED, fill="Color/Vellum")

def flow_section(key, title, kicker, paras, rt, extra=1):
    """Threaded 2-column frames across the measured number of pages (+slack)."""
    st = doc.story()
    for pstyle, runs in paras:
        st.para(pstyle, runs)
    n = SECT.get(key, 1) + extra
    frames = []
    for i in range(n):
        p = newpage(rt=rt)
        if i == 0:
            hd = doc.story().para("SecHead", title)
            if kicker: hd.para("SecKick", kicker)
            p.text(cx(p), MT, CW, 96, hd.id)
            rule(p, cx(p), MT + 104, CW)
            y, h = MT + 118, H - MB - (MT + 118)
        else:
            y, h = MT, H - MB - MT
        frames.append((p, y, h))
    ids = [doc.uid("tf") for _ in frames]
    for i, (p, y, h) in enumerate(frames):
        p.text(cx(p), y, CW, h, st.id, cols=2, gutter=GUT,
               prev=ids[i - 1] if i else "n",
               nxt=ids[i + 1] if i < len(frames) - 1 else "n",
               name=ids[i])

def chip_line(scene, roman):
    lab, _ = B.status_of(scene)
    return "%s  ·  Movement %s  ·  %s" % (scene["id"], roman, lab)

# ================================================================ FRONT MATTER
p = newpage(fol=False)
rule(p, W / 2 - 50, 292, 100)
st = doc.story().para("HalfT", "REVELATION").para("HalfS", "An Illuminated Prophecy in Six Movements")
p.text(cx(p), 308, CW, 90, st.id)
rule(p, W / 2 - 50, 392, 100)

p = newpage(fol=False, bg="Color/Night")                 # frontispiece
d = DIMS["T1-00"]
p.image(MO, MT, W - MO - MI, H - MT - MB - 30, LINKS + "/T1-00" + LINK_EXT, d[0], d[1], fit="contain")
st = doc.story().para("FrontisCapLight", "Saint John reading the Apocalypse · Movement I · T1-00")
p.text(cx(p), H - MB + 6, CW, 16, st.id)

p = newpage(fol=False)                                   # title
st = (doc.story().para("TitDrop", "DIVERGENT WORLD").para("TitMain", "REVELATION")
      .para("TitSub", "An Illuminated Prophecy in Six Movements")
      .para("TitDesc", "The complete text of the Apocalypse of John, with ninety plates "
                       "reconstructing the lost and surviving registers of the Angers cycle.")
      .para("TitImp", "Plates and commentary by Ali Rahman"))
p.text(cx(p) + 60, 180, CW - 120, 460, st.id)

p = newpage(fol=False)                                   # copyright
st = doc.story()
st.para("Copy", [("Chip", "REVELATION — An Illuminated Prophecy in Six Movements")])
for t in ["Collector's edition. First published 2026 by Divergent World.",
          "Plates © Ali Rahman / Divergent World.",
          "Scripture quotations are taken from the World English Bible, which is in the public "
          "domain. “World English Bible” is a trademark of eBible.org. The text is reproduced "
          "unmodified. Words spoken by Christ are set in red following the ranges marked in the "
          "official USFM edition.",
          "The ninety plates in this book were generated with the assistance of generative image "
          "models between March and August 2026, against a fixed style contract described in the "
          "Note on Method. Each plate is marked to indicate whether the corresponding "
          "fourteenth-century compartment survives at Angers, survives only as a fragment, or is "
          "lost and has been reconstructed.",
          "A complete digital edition, containing the full continuous text of Revelation, is "
          "distributed without charge."]:
    st.para("Copy", t)
st.para("CopySm", "Set in EB Garamond, Cinzel and Space Grotesk")
p.text(cx(p), H - MB - 300, 430, 300, st.id)

p = newpage(fol=False)                                   # contents
st = doc.story().para("TocH", "CONTENTS")
st.para("TocLbl", "—")
for t, d_ in [("Foreword", AUTHOR), ("Note on the Angers Cycle", AUTHOR),
              ("Note on Method", AUTHOR)]:
    st.para("TocRowMin", "\t%s\t%s" % (t, d_))
st.para("TocLbl", "THE SIX MOVEMENTS")
for tp in TAPS:
    st.para("TocRow", "%s\t%s\t%s" % (tp["roman"], tp["title"],
            SCENES[tp["leadSceneId"]]["displayReference"].replace("Revelation ", "Rev. ")))
st.para("TocLbl", "THE APPARATUS")
for t, d_ in [("The Register of Losses", "Ninety compartments"), ("Colophon", "")]:
    st.para("TocRowMin", "\t%s\t%s" % (t, d_))
p.text(cx(p) + 100, MT + 40, CW - 200, H - MT - MB - 60, st.id)

def dropcap(text):
    """Split the first character into its own run carrying the DropCapRed character style.
    Relying on the paragraph style's DropCapStyle is not enough — InDesign takes the
    drop cap's appearance from the character formatting actually on that character."""
    t = text.lstrip()
    return [("DropCapRed", t[:1]), (None, t[1:])]

def prose_paras(items):
    out = []
    for kind, text in items:
        t = " ".join(text.split())
        if kind == "h":      continue
        elif kind == "h2":   out.append(("H3", t))
        elif kind == "drop": out.append(("BodyDrop", dropcap(t)))
        elif kind == "sig":  out.append(("Sig", t))
        else:                out.append(("Body", t))
    return out

flow_section("foreword", "Foreword", AUTHOR, prose_paras(FOREWORD), "Foreword")
flow_section("losses", "Note on the Angers Cycle", AUTHOR, prose_paras(LOSSES),
             "Note on the Angers Cycle")
flow_section("method", "Note on Method", AUTHOR, prose_paras(METHOD), "Note on Method")

# ================================================================ DIVIDER
def divider(kicker, title, sub):
    ensure_recto()
    p = doc.add_page()
    p.rect(-BLEED, -BLEED, W + 2 * BLEED, H + 2 * BLEED, fill="Color/Dark")
    st = (doc.story().para("DivK", kicker).para("DivT", title).para("DivS", sub))
    p.text(cx(p), 240, CW, 300, st.id)
    return p

divider("PART ONE", "The Six Movements",
        "Ninety plates, after the Apocalypse Tapestry of Angers")

# ================================================================ MOVEMENTS
for tp in TAPS:
    roman, mtitle = tp["roman"], tp["title"]
    rt = "Movement %s · %s" % (roman, mtitle)
    lead = SCENES[tp["leadSceneId"]]
    scenes = [SCENES[i] for i in tp["sceneIds"] if i != tp["leadSceneId"]]
    tally = {"survives": 0, "frag": 0, "lost": 0}
    for s in [lead] + scenes:
        tally[B.status_of(s)[1]] += 1

    # --- opener -------------------------------------------------------
    ensure_recto()
    p = newpage(fol=False)
    IW = 360.0
    d = DIMS[lead["id"]]
    # reader panel shown whole on a night ground rather than cropped to the strip
    p.rect(-BLEED, -BLEED, IW + BLEED, H + 2 * BLEED, fill="Color/Night")
    p.image(0, 40, IW, H - 80, LINKS + "/%s%s" % (lead["id"], LINK_EXT),
            d[0], d[1], fit="contain")
    tx = IW + 46
    tw = W - MO - tx
    st = (doc.story().para("MvNum", "MOVEMENT %s" % roman).para("MvTitle", mtitle))
    p.text(tx, MT + 46, tw, 130, st.id)
    rule(p, tx, MT + 196, 90, color="Color/Rubric", weight=0.6)
    st = doc.story().para("MvRange", "%s  ·  Fifteen compartments" % lead["displayReference"])
    p.text(tx, MT + 208, tw, 16, st.id)
    st = doc.story().para("MvArg", dropcap(" ".join(tp["summary"].split())))
    p.text(tx, MT + 236, tw - 20, 190, st.id)
    rule(p, tx, H - MB - 176, tw - 20)
    for i, (num, lbl) in enumerate([(tally["survives"], "Survive"), (tally["frag"], "Fragment"),
                                    (tally["lost"], "Reconstructed")]):
        st = doc.story().para("MvStatN", str(num) if num else "—").para("MvStatL", lbl)
        p.text(tx + i * 96, H - MB - 164, 92, 44, st.id)
    rule(p, tx, H - MB - 96, tw - 20)
    st = doc.story().para("MvStrip", "   ·   ".join(
        "%s %s" % (s["id"].split("-")[1], s["title"]) for s in scenes))
    p.text(tx, H - MB - 86, tw - 20, 76, st.id)
    folio(p)

    # --- argument -----------------------------------------------------
    paras = []
    for i, m in enumerate(tp["movements"], 1):
        paras.append(("H3", "%d.  %s" % (i, m["title"])))
        d = " ".join(m["description"].split())
        paras.append(("BodyDrop", dropcap(d)) if i == 1 else ("Body", d))
    flow_section("arg%d" % tp["id"], "Movement %s · %s" % (roman, mtitle),
                 "The argument of the movement", paras, rt, extra=0)

    # --- plates -------------------------------------------------------
    for idx, s in enumerate(scenes):
        d = DIMS[s["id"]]
        note = PLATE_NOTES.get(s["id"], "")
        # full-bleed only where the plate has the pixels to survive it
        if idx % 2 == 0 and d[0] >= 5000:
            # full-bleed plate
            # whole plate, centred on a night page, caption beneath
            p = newpage(fol=False, bg="Color/Night")
            bx, bw = (0.0, W + 9.0) if p.recto else (-9.0, W + 9.0)
            ih = bw * d[1] / d[0]
            p.image(bx, (H - ih) / 2.0 - 26, bw, ih,
                    LINKS + "/%s%s" % (s["id"], LINK_EXT), d[0], d[1], fit="contain")
            st = (doc.story().para("BleedId", "Plate %s  ·  %s  ·  %s"
                                   % (s["id"], s["displayReference"], B.status_of(s)[0]))
                  .para("BleedTitle", s["title"]))
            p.text(cx(p), (H + ih) / 2.0 + 4, CW, 84, st.id)
            running(p, rt, light=True)
            # facing text page
            p = newpage(rt=rt)
            st = (doc.story().para("PlateId", chip_line(s, roman))
                  .para("PlateTitle", s["title"])
                  .para("PlateAnchor", s["displayReference"])
                  .para("PlateSc", anchor_runs(s)))
            if note:
                st.para("NoteLbl", "Note on the plate").para("NoteBody", note)
            p.text(cx(p) + 108, MT + 74, CW - 216, H - MT - MB - 190, st.id)
            rule(p, cx(p) + 108, H - MB - 96, CW - 216)
            st = doc.story().para("ProvLbl", "Plate data")
            for k, v in [("Compartment", "Tapestry %s, %s register, position %d"
                          % (roman, s["row"], s["position"])),
                         ("Angers state", B.status_of(s)[0]),
                         ("Source", "%d × %d px" % (s.get("width", 0), s.get("height", 0)))]:
                st.para("ProvRow", "%s\t%s" % (k, v))
            p.text(cx(p) + 108, H - MB - 84, CW - 216, 76, st.id)
        else:
            # 16:9 band + footer
            p = newpage(fol=False)
            bx, bw = (0.0, W + 9.0) if p.recto else (-9.0, W + 9.0)
            # whole plate, never cropped; the band is capped so the footer always fits
            bh = min(bw * d[1] / d[0], 496.0)
            p.rect(bx, -9.0, bw, bh + 9.0, fill="Color/Night")
            p.image(bx, -9.0, bw, bh + 9.0,
                    LINKS + "/%s%s" % (s["id"], LINK_EXT), d[0], d[1], fit="contain")
            fy = bh + 30
            st = (doc.story().para("PlateId", chip_line(s, roman))
                  .para("PlateTitle", s["title"])
                  .para("PlateAnchor", s["displayReference"]))
            p.text(cx(p), fy, 250, 150, st.id)
            vrule(p, cx(p) + 282, fy, H - MB - fy - 6)
            st = doc.story().para("PlateScSm", anchor_runs(s, 95))
            p.text(cx(p) + 306, fy, CW - 306, H - MB - fy - 6, st.id, cols=2, gutter=26)
            running(p, rt)
            folio(p)

    # --- coda ---------------------------------------------------------
    ct, cbody = MOVEMENT_CODAS[tp["id"]]
    p = newpage(fol=False)
    st = (doc.story().para("CodaK", "MOVEMENT %s CLOSES" % roman).para("CodaT", ct)
          .para("CodaB", " ".join(cbody.split())))
    p.text(cx(p) + 150, 250, CW - 300, 340, st.id)
    running(p, rt)

# ================================================================ THE TEXT
divider("PART TWO", "The Revelation to John",
        "The complete text · World English Bible · words of Christ in red")

sc = []
for ch in REV["chapters"]:
    sc.append(("ChapKick", "Chapter"))
    sc.append(("Chap", str(ch["chapter"])))
    run = []
    for v in ch["verses"]:
        run.append(("VNum", str(v["number"]) + " "))
        run.extend(verse_runs(v["text"], v.get("wordsOfJesus")))
        run.append((None, " "))
        if sum(1 for r in run if r[0] == "VNum") == 4:
            sc.append(("Sc", run)); run = []
    if run: sc.append(("Sc", run))
flow_section("text", "The Revelation to John", "World English Bible",
             sc, "The Revelation to John", extra=1)

# ================================================================ APPARATUS
divider("PART THREE", "The Register of Losses",
        "Ninety compartments · survival status after the 1782 dispersal")

rows = []
for tp in TAPS:
    rows.append(("RegH", "MOVEMENT %s · %s" % (tp["roman"], tp["title"])))
    for sid in tp["sceneIds"]:
        s = SCENES[sid]; lab, _ = B.status_of(s)
        rows.append(("RegRow", "%s\t%s\t%s\t%s"
                     % (s["id"], s["title"],
                        s["displayReference"].replace("Revelation ", ""), lab)))
flow_section("register", "The Register of Losses",
             "Concordance of the ninety compartments", rows, "The Register of Losses", extra=0)

# ================================================================ COLOPHON
ensure_recto()
p = newpage(fol=False)
st = doc.story().para("ColH", "COLOPHON")
for t in COLOPHON_LEFT[:3]:
    st.para("ColB", " ".join(t.split()))
st.para("Mark", "✠")
p.text(cx(p), 160, 350, 460, st.id)
st = doc.story().para("ColH", "THIS EDITION")
for k, v in [("Edition", "Collector's, first"), ("Plates", "90"),
             ("Trim", "13 × 11 in landscape"), ("Extent", "%d pages" % EXTENT),
             ("Stock", "Mohawk Superfine Eggshell"), ("Binding", "Section sewn, case bound"),
             ("Typefaces", "EB Garamond · Cinzel · Space Grotesk"),
             ("Scripture", "World English Bible"), ("Printed", "2026")]:
    st.para("SpecRow", "%s\t%s" % (k, v))
st.para("ColB", "")
st.para("NoteBody", "The complete continuous text of the Revelation to John is published "
                    "in the free digital edition.")
p.text(cx(p) + 440, 160, 340, 460, st.id)

# even up the book
while doc.page_count % 4 != 0:
    b = doc.add_page()
    b.rect(-BLEED, -BLEED, W + 2 * BLEED, H + 2 * BLEED, fill="Color/Vellum")

out = os.path.join(HERE, "indesign", "REVELATION_13x11.idml")
print("link set:", LINK_SET, "->", LINKS)
import json as _j
_j.dump({"placements": doc.placements,
         "stories": {st.id: st.paras for st in doc.stories},
         "styles": {n: kw for n, kw in doc.pstyles},
         "cstyles": {n: kw for n, kw in doc.cstyles}},
        open(os.path.join(HERE, "indesign", "layout.json"), "w"))
parts = doc.write(out)
print("pages:", doc.page_count, "| spreads:", len(doc.spreads),
      "| stories:", len(doc.stories), "| parts:", len(parts))
open(_ext, "w").write(str(doc.page_count))
print("wrote", out, os.path.getsize(out) // 1024, "KB")
