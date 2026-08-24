# -*- coding: utf-8 -*-
"""REVELATION — full ebook builder.
Reads the repo's content JSON, emits one HTML document, renders to PDF via Chromium.
"""
import json, os, html, re, sys
from prose import (FOREWORD, LOSSES, METHOD, MOVEMENT_CODAS, PLATE_NOTES,
                   COLOPHON_LEFT, FOREWORD_AUTHOR)
from plate_status import load_statuses
from paths import ARTWORK, BUILD, CONTENT, relative_from_build

HERE = os.path.dirname(os.path.abspath(__file__))
T = json.load(open(CONTENT / "tapestries.json"))
REV = json.load(open(CONTENT / "revelation.web.json"))

SCENES = {s["id"]: s for s in T["scenes"]}
TAPS = T["tapestries"]

# ---- survival status, sourced from the tracked publishing manifest ----
STATUS_BY_ID = load_statuses()

STATUS_LABEL = {"survives": ("Survives", "survives"),
                "fragmentary": ("Fragment", "frag"),
                "missing_or_lost": ("Reconstructed", "lost")}

def status_of(scene):
    raw = STATUS_BY_ID.get(scene["id"])
    return STATUS_LABEL.get(raw, ("Reconstructed", "lost"))

def esc(s): return html.escape(s, quote=False)

# ---------- red-letter rendering ----------
def verse_html(text, ranges):
    if not ranges:
        return esc(text)
    out, cur = [], 0
    for r in sorted(ranges, key=lambda x: x["start"]):
        a, b = max(0, r["start"]), min(len(text), r["end"])
        if a > cur: out.append(esc(text[cur:a]))
        out.append('<span class="wj">%s</span>' % esc(text[a:b]))
        cur = max(cur, b)
    if cur < len(text): out.append(esc(text[cur:]))
    return "".join(out)

MAXW = 165
def anchor_scripture(scene, maxw=None):
    """Verses for a plate's anchor, truncated with a pointer if long."""
    parts, words, truncated = [], 0, False
    for p in scene.get("passages", []):
        for v in p["verses"]:
            w = len(v["text"].split())
            if words + w > (maxw or MAXW) and parts:
                truncated = True
                break
            parts.append('<span class="v">%d</span>%s' % (
                v["verse"], verse_html(v["text"], v.get("wordsOfJesus"))))
            words += w
        if truncated: break
    body = " ".join(parts)
    if truncated:
        body += ' <span class="cont">… %s continues in the complete text.</span>' % esc(
            scene["displayReference"])
    return body

# ---------- page emitters ----------
PAGES = []
def page(cls, inner, rt=None, folio=True, section=None):
    PAGES.append({"cls": cls, "inner": inner, "rt": rt, "folio": folio, "section": section})

def flow(title, blocks, cols=2, rt=None, kicker=None):
    """Emit a flowing section; JS paginates it at render time."""
    src = "".join(blocks)
    PAGES.append({"flow": True, "title": title, "kicker": kicker or "",
                  "cols": cols, "src": src, "rt": rt or title})

def prose_blocks(items):
    out = []
    for kind, text in items:
        t = " ".join(text.split())
        if kind == "h":      continue
        elif kind == "h2":   out.append('<h3>%s</h3>' % esc(t))
        elif kind == "drop": out.append('<p class="drop">%s</p>' % esc(t))
        elif kind == "sig":  out.append('<p class="sig">%s</p>' % esc(t))
        else:                out.append('<p>%s</p>' % esc(t))
    return out

# =====================  COVER  =====================
page("ebookcover nofolio", """
  <img src="plates/ebook_front.jpg" class="fill-cover">
  <div class="ec">
    <h1>REVELATION</h1>
    <div class="ec-sub">AN ILLUMINATED PROPHECY IN SIX MOVEMENTS</div>
    <div class="ec-hair"></div>
    <div class="ec-lede">After the Apocalypse Tapestry of Angers</div>
  </div>
  <div class="ec-author">Ali Rahman</div>""", folio=False)

# =====================  FRONT MATTER  =====================
page("halftitle", """
  <div class="ht"><div class="ht-rule"></div>
    <h1>REVELATION</h1>
    <div class="ht-sub">An Illuminated Prophecy in Six Movements</div>
    <div class="ht-rule"></div></div>""", folio=False)

page("bleed nofolio", """
  <img src="plates/T1-00.jpg" class="fill-contain">
  <div class="frontis-cap">Saint John reading the Apocalypse · Movement I · T1-00</div>""",
     folio=False)

page("titlepage", """
  <div class="tp">
    <div class="tp-drop">DIVERGENT WORLD</div>
    <h1>REVELATION</h1>
    <div class="tp-sub">An Illuminated Prophecy in Six Movements</div>
    <div class="tp-rule"></div>
    <div class="tp-desc">The complete text of the Apocalypse of John, with ninety plates
      reconstructing the lost and surviving registers of the Angers cycle.</div>
    <div class="tp-imprint">Plates and commentary by Ali Rahman</div>
  </div>""", folio=False)

page("copyrightpage", """
  <div class="cp">
    <p><b>REVELATION — An Illuminated Prophecy in Six Movements</b></p>
    <p>Complete edition. First published 2026 by Divergent World.</p>
    <p>Plates &copy; Ali Rahman / Divergent World.</p>
    <p>Scripture quotations are taken from the World English Bible, which is in the public
       domain. “World English Bible” is a trademark of eBible.org. The text is reproduced
       unmodified. Words spoken by Christ are set in red following the ranges marked in the
       official USFM edition.</p>
    <p>The ninety plates in this book were generated with the assistance of generative image
       models between March and August 2026, against a fixed style contract described in the
       Note on Method. Each plate is marked to indicate whether the corresponding
       fourteenth-century compartment survives at Angers, survives only as a fragment, or is
       lost and has been reconstructed.</p>
    <p>This complete edition is distributed without charge. A collector's print edition,
       containing the plates and apparatus without the continuous scripture text, is
       published separately.</p>
    <p class="cp-small">Set in EB Garamond, Cinzel and Space Grotesk.</p>
  </div>""", folio=False)

# contents
toc_rows = []
for tp in TAPS:
    toc_rows.append(
        '<div class="toc-row"><span class="toc-num">%s</span>'
        '<span class="toc-t">%s</span><span class="toc-d">%s</span></div>'
        % (esc(tp["roman"]), esc(tp["title"]), esc(SCENES[tp["leadSceneId"]]["displayReference"].replace("Revelation ", "Rev. "))))
page("contents", """
  <div class="toc">
    <h2>CONTENTS</h2>
    <div class="toc-block">
      <div class="toc-row minor"><span class="toc-num"></span><span class="toc-t">Foreword</span><span class="toc-d">%s</span></div>
      <div class="toc-row minor"><span class="toc-num"></span><span class="toc-t">Note on the Angers Cycle</span><span class="toc-d">Ali Rahman</span></div>
      <div class="toc-row minor"><span class="toc-num"></span><span class="toc-t">Note on Method</span><span class="toc-d">Ali Rahman</span></div>
    </div>
    <div class="toc-lbl">THE SIX MOVEMENTS</div>
    <div class="toc-block">%s</div>
    <div class="toc-lbl">THE TEXT AND THE APPARATUS</div>
    <div class="toc-block">
      <div class="toc-row minor"><span class="toc-num"></span><span class="toc-t">The Revelation to John, complete</span><span class="toc-d">World English Bible</span></div>
      <div class="toc-row minor"><span class="toc-num"></span><span class="toc-t">The Register of Losses</span><span class="toc-d">Ninety compartments</span></div>
      <div class="toc-row minor"><span class="toc-num"></span><span class="toc-t">Colophon</span><span class="toc-d"></span></div>
    </div>
  </div>""" % (esc(FOREWORD_AUTHOR), "".join(toc_rows)), folio=False)

flow("Foreword", prose_blocks(FOREWORD), cols=2, kicker="")
flow("Note on the Angers Cycle", prose_blocks(LOSSES), cols=2, kicker="Ali Rahman")
flow("Note on Method", prose_blocks(METHOD), cols=2, kicker="Ali Rahman")

def divider(kicker, title, sub=""):
    page("divider", """
      <div class="dv"><div class="dv-k">%s</div><h1>%s</h1>
      <div class="dv-rule"></div><div class="dv-s">%s</div></div>"""
         % (esc(kicker), esc(title), esc(sub)), folio=False)

divider("PART ONE", "The Six Movements",
        "Ninety plates, after the Apocalypse Tapestry of Angers")

# =====================  MOVEMENTS  =====================
for tp in TAPS:
    n, roman, mtitle = tp["id"], tp["roman"], tp["title"]
    rt = "Movement %s · %s" % (roman, mtitle)
    lead = SCENES[tp["leadSceneId"]]
    scene_ids = [i for i in tp["sceneIds"] if i != tp["leadSceneId"]]
    scenes = [SCENES[i] for i in scene_ids]
    lab, cls = status_of(lead)

    tally = {"survives": 0, "frag": 0, "lost": 0}
    for s in [lead] + scenes:
        tally[status_of(s)[1]] += 1

    strip = "".join('<span>%s %s</span>' % (esc(s["id"].split("-")[1]), esc(s["title"][:30]))
                    for s in scenes)
    page("mvpage", """
      <div class="mv">
        <div class="plate"><img src="plates/%s.jpg"><div class="vign"></div></div>
        <div class="txt">
          <div class="numeral">MOVEMENT %s</div>
          <h2>%s</h2>
          <div class="rangehair"></div>
          <div class="range">%s &nbsp;·&nbsp; Fifteen compartments</div>
          <div class="arg"><p class="lead">%s</p></div>
          <div class="mv-stat">
            <div><b>%d</b><span>Survive</span></div>
            <div><b>%d</b><span>Fragment</span></div>
            <div><b>%d</b><span>Reconstructed</span></div>
          </div>
          <div class="tocstrip">%s</div>
        </div>
      </div>""" % (lead["id"], roman, esc(mtitle),
                   esc(lead["displayReference"]), esc(tp["summary"]),
                   tally["survives"], tally["frag"], tally["lost"], strip),
         rt=rt, folio=False)

    # the movement's four-part argument, as a flowing section
    blocks = []
    for i, m in enumerate(tp["movements"], 1):
        blocks.append('<h3><span class="mnum">%d</span>%s</h3>' % (i, esc(m["title"])))
        blocks.append('<p%s>%s</p>' % (' class="drop"' if i == 1 else '', esc(m["description"])))
    flow("Movement %s · %s" % (roman, mtitle), blocks, cols=2,
         rt=rt, kicker="The argument of the movement")

    # plates
    for idx, s in enumerate(scenes):
        lab, cls = status_of(s)
        note = PLATE_NOTES.get(s["id"], "")
        chip = '<span class="chip %s">%s</span>' % (cls, lab)
        aid = "%s &nbsp;·&nbsp; Movement %s &nbsp;·&nbsp; %s" % (s["id"], roman, chip)

        if idx % 2 == 0:
            # full-bleed plate, facing text page
            page("bleed", """
              <img src="plates/%s.jpg" class="fill-cover">
              <div class="scrim"></div>
              <div class="cap"><div class="id">Plate %s &nbsp;·&nbsp; %s</div>
                <h3>%s</h3></div>""" % (s["id"], s["id"], esc(s["displayReference"]),
                                        esc(s["title"])), rt=rt)
            page("textpage", """
              <div class="tx">
                <div class="hd"><div class="id">%s</div>
                  <h3>%s</h3>
                  <div class="anchor">%s</div></div>
                <div class="hr"></div>
                <div class="scripture wide">%s</div>
                %s
                <div class="prov">
                  <div class="lbl">Plate data</div>
                  <dl><dt>Compartment</dt><dd>Tapestry %s, %s register, position %d</dd>
                      <dt>Angers state</dt><dd>%s</dd>
                      <dt>Source</dt><dd>%d &times; %d px</dd></dl>
                </div>
              </div>""" % (aid, esc(s["title"]), esc(s["displayReference"]),
                           anchor_scripture(s),
                           ('<div class="note"><div class="lbl">Note on the plate</div><p>%s</p></div>'
                            % esc(note)) if note else "",
                           roman, s["row"], s["position"], lab,
                           s.get("width", 0), s.get("height", 0)), rt=rt)
        else:
            # single page: plate left, scripture right
            page("platepage", """
              <div class="pp-band"><img src="plates/%s.jpg"></div>
              <div class="pp-foot">
                <div class="pp-hd">
                  <div class="id">%s</div>
                  <h3>%s</h3>
                  <div class="anchor">%s</div>
                </div>
                <div class="pp-sc">%s</div>
              </div>
              %s""" % (s["id"], aid, esc(s["title"]), esc(s["displayReference"]),
                       anchor_scripture(s, 120),
                       ('<div class="pp-note"><span>%s</span></div>' % esc(note)) if note else ""),
                 rt=rt)

    ct, cbody = MOVEMENT_CODAS[n]
    page("coda", """
      <div class="cd"><div class="cd-k">MOVEMENT %s CLOSES</div>
        <h2>%s</h2><div class="cd-rule"></div>
        <p>%s</p></div>""" % (roman, esc(ct), esc(" ".join(cbody.split()))),
         rt=rt, folio=False)

# =====================  COMPLETE TEXT  =====================
divider("PART TWO", "The Revelation to John",
        "The complete text · World English Bible · words of Christ in red")

blocks = []
for ch in REV["chapters"]:
    blocks.append('<h3 class="chap"><span>CHAPTER</span>%d</h3>' % ch["chapter"])
    run = []
    for v in ch["verses"]:
        run.append('<span class="v">%d</span>%s' % (v["number"],
                   verse_html(v["text"], v.get("wordsOfJesus"))))
        if len(run) == 4:
            blocks.append('<p class="sc">%s</p>' % " ".join(run)); run = []
    if run: blocks.append('<p class="sc">%s</p>' % " ".join(run))
flow("The Revelation to John", blocks, cols=2, rt="The Revelation to John",
     kicker="World English Bible")

# =====================  APPARATUS  =====================
divider("PART THREE", "The Register of Losses",
        "Ninety compartments · survival status after the 1782 dispersal")

rows = []
for tp in TAPS:
    rows.append('<div class="reg-h">MOVEMENT %s · %s</div>' % (esc(tp["roman"]), esc(tp["title"])))
    for sid in tp["sceneIds"]:
        s = SCENES[sid]; lab, cls = status_of(s)
        rows.append('<div class="reg"><span class="k">%s</span>'
                    '<span class="t">%s</span><span class="a">%s</span>'
                    '<span class="s %s">%s</span></div>'
                    % (esc(s["id"]), esc(s["title"]),
                       esc(s["displayReference"].replace("Revelation ", "")), cls, lab))
flow("The Register of Losses", rows, cols=2, rt="The Register of Losses",
     kicker="Concordance of the ninety compartments")

BACKCOVER = """
  <img src="plates/ebook_back.jpg" class="fill-cover">
  <div class="bc">
    <p class="bc-lead">Ninety compartments were woven at Angers between 1377 and 1382 —
      the whole of Revelation, rendered as a sequence you could walk alongside. Twenty of
      them no longer exist.</p>
    <p>This book rebuilds all ninety, in the original order, against the original anchors,
      and marks on every plate whether what you are looking at survives, survives only in
      fragments, or has been reconstructed.</p>
    <div class="bc-marks">
      <div><b>90</b><span>Compartments</span></div>
      <div><b>6</b><span>Movements</span></div>
      <div><b>22</b><span>Chapters</span></div>
    </div>
    <div class="bc-imprint">Divergent World &nbsp;·&nbsp; Free digital edition</div>
  </div>"""

page("colophon", """
  <div class="colo">
    <div><h2>COLOPHON</h2>%s<div class="mark">&#10016;</div></div>
    <div><h2>THIS EDITION</h2>
      <div class="spec">
        <b>Edition</b>Complete, digital<br>
        <b>Plates</b>90<br>
        <b>Scripture</b>Revelation 1–22, complete<br>
        <b>Verses</b>404<br>
        <b>Text</b>World English Bible<br>
        <b>Trim</b>12 &times; 9 in landscape<br>
        <b>Typefaces</b>EB Garamond · Cinzel · Space Grotesk<br>
        <b>Price</b>Free<br>
        <b>Built</b>August 2026<br>
      </div>
      <div class="spec-note">The collector's print edition — 232 pages, 13 &times; 11 in,
        Mohawk Superfine, section-sewn — carries the plates and the apparatus. The
        continuous scripture text lives in this edition.</div>
    </div>
  </div>""" % "".join('<p>%s</p>' % esc(" ".join(p.split())) for p in COLOPHON_LEFT),
     folio=False)

page("backcover nofolio", BACKCOVER, folio=False)

# =====================  RENDER  =====================
CSS = open(os.path.join(HERE, "theme.css")).read()
PAGINATOR = open(os.path.join(HERE, "paginate.js")).read()

body = []
for p in PAGES:
    if p.get("flow"):
        body.append('<div class="flowsec" data-title="%s" data-kicker="%s" data-cols="%d" data-rt="%s">'
                    '<div class="flow-src">%s</div></div>'
                    % (esc(p["title"]), esc(p["kicker"]), p["cols"], esc(p["rt"]), p["src"]))
    else:
        rt = ('<div class="rt">%s</div>' % esc(p["rt"])) if p.get("rt") else ""
        fol = '<div class="folio"></div>' if p.get("folio") else ""
        body.append('<div class="page %s" %s>%s%s%s</div>'
                    % (p["cls"], 'data-rt="%s"' % esc(p["rt"]) if p.get("rt") else "",
                       rt, p["inner"], fol))

doc = """<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<title>REVELATION — An Illuminated Prophecy in Six Movements</title>
<style>%s</style></head><body>%s
<script>%s</script></body></html>""" % (CSS, "".join(body), PAGINATOR)
doc = doc.replace('src="plates/', 'src="%s/' % relative_from_build(ARTWORK))

BUILD.mkdir(parents=True, exist_ok=True)
out = BUILD / "book.html"
open(out, "w").write(doc)
print("wrote", out, "| fixed pages:", sum(1 for p in PAGES if not p.get("flow")),
      "| flow sections:", sum(1 for p in PAGES if p.get("flow")))
