# -*- coding: utf-8 -*-
"""Estimate whether any single-frame story will overset in InDesign.

Renders each placed story in Chromium at the frame's exact width, with the same font,
size, leading, tracking and spacing as the IDML paragraph style, then compares the
composed height to the frame height. InDesign's composer differs slightly from a browser's,
so a small tolerance is applied; anything over is reported.
"""
import json, os, html, sys
from playwright.sync_api import sync_playwright
import pathlib

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, "indesign", "layout.json")))
STY, CST = D["styles"], D["cstyles"]
STORIES = D["stories"]

WEIGHT = {"Regular": "400", "Italic": "400", "Medium": "500",
          "SemiBold": "600", "Bold": "700"}

def css_for(name, kw):
    f = kw.get("font", "EB Garamond")
    fs = kw.get("FontStyle", "Regular")
    out = ['font-family:"%s",serif' % f,
           'font-weight:%s' % WEIGHT.get(fs, "400"),
           'font-style:%s' % ("italic" if "Italic" in fs else "normal"),
           'font-size:%spt' % kw.get("PointSize", 12),
           'line-height:%spt' % kw.get("leading", float(kw.get("PointSize", 12)) * 1.2),
           'margin-top:%spt' % kw.get("SpaceBefore", 0),
           'margin-bottom:%spt' % kw.get("SpaceAfter", 0)]
    if kw.get("Tracking"): out.append("letter-spacing:%fem" % (float(kw["Tracking"]) / 1000.0))
    j = kw.get("Justification", "LeftAlign")
    out.append("text-align:%s" % {"CenterAlign": "center", "RightAlign": "right",
                                  "LeftJustified": "justify"}.get(j, "left"))
    if kw.get("Capitalization") == "AllCaps": out.append("text-transform:uppercase")
    if kw.get("Hyphenation") == "true": out.append("hyphens:auto")
    if kw.get("DropCapLines"): out.append("--drop:1")
    return ";".join(out)

rules = []
for n, kw in STY.items():
    rules.append(".%s{%s}" % (n, css_for(n, kw)))
    if kw.get("DropCapLines"):
        rules.append('.%s::first-letter{font-family:"Cinzel",serif;font-size:%spt;'
                     'line-height:.84;float:left;padding:2pt 5pt 0 0}'
                     % (n, float(kw.get("PointSize", 11)) * 2.55))
for n, kw in CST.items():
    rules.append(".c-%s{%s}" % (n, css_for(n, kw).replace("margin-top:0pt;", "")
                                .replace("margin-bottom:0pt;", "")))

blocks, meta = [], []
for pl in D["placements"]:
    if pl["threaded"]:
        continue
    paras = STORIES.get(pl["story"], [])
    inner = []
    for pstyle, runs in paras:
        spans = "".join(
            ('<span class="c-%s">%s</span>' % (cs, html.escape(t)) if cs else html.escape(t))
            for cs, t in runs)
        inner.append('<p class="%s">%s</p>' % (pstyle, spans or "&nbsp;"))
    colw = (pl["w"] - pl["gutter"] * (pl["cols"] - 1)) / pl["cols"]
    style = "width:%fpt" % pl["w"]
    if pl["cols"] > 1:
        style += ";column-count:%d;column-gap:%fpt" % (pl["cols"], pl["gutter"])
    blocks.append('<div class="box" style="%s">%s</div>' % (style, "".join(inner)))
    meta.append({"frame": pl["frame"], "story": pl["story"], "h": pl["h"],
                 "w": pl["w"], "cols": pl["cols"],
                 "style": paras[0][0] if paras else "?",
                 "text": (paras[0][1][0][1][:60] if paras and paras[0][1] else "")})

doc = ("""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#fff}
.box{margin:0 0 40pt 0}
.box p:first-child{margin-top:0}
%s
</style></head><body>%s</body></html>""" % ("\n".join(rules), "".join(blocks)))
open(os.path.join(HERE, "overset.html"), "w").write(doc)

with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page(viewport={"width": 1400, "height": 1000})
    pg.goto(pathlib.Path(os.path.join(HERE, "overset.html")).as_uri(), wait_until="load")
    pg.wait_for_timeout(1500)
    heights = pg.evaluate(
        "Array.from(document.querySelectorAll('.box')).map(b=>b.getBoundingClientRect().height*72/96)")
    b.close()

TOL = 1.06          # InDesign composes a little tighter than Chromium
bad = []
for m, hpx in zip(meta, heights):
    if hpx > m["h"] * TOL:
        m["measured"] = round(hpx, 1)
        m["over"] = round(hpx - m["h"], 1)
        bad.append(m)

print("checked %d single-frame stories" % len(meta))
if not bad:
    print("PASSED — no frame is predicted to overset")
    sys.exit(0)
bad.sort(key=lambda m: -m["over"])
print("\n%d frames predicted to overset:\n" % len(bad))
for m in bad[:30]:
    print("  %-8s %-14s frame %6.1fpt  needs %6.1fpt  (+%5.1f)  %s"
          % (m["frame"], m["style"], m["h"], m["measured"], m["over"], m["text"][:44]))
