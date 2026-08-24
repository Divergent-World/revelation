# -*- coding: utf-8 -*-
"""Reflowable EPUB 3 — real text, generated from the content JSON rather than from a
paginated layout. This is the edition that works on a phone or a Kindle."""
import os, re, zipfile, html
import build as B
from prose import (FOREWORD, LOSSES, METHOD, MOVEMENT_CODAS, PLATE_NOTES,
                   COLOPHON_LEFT, AUTHOR)
from paths import ARTWORK, BUILD, INDESIGN
from validate_epub import validate_epub

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = BUILD / "REVELATION_reflowable.epub"
BUILD.mkdir(parents=True, exist_ok=True)
T, REV, SCENES, TAPS = B.T, B.REV, B.SCENES, B.TAPS
esc = B.esc

CSS = """
@font-face{font-family:"EBG";src:url(fonts/EBGaramond-Regular.ttf);font-weight:400;font-style:normal}
@font-face{font-family:"EBG";src:url(fonts/EBGaramond-Italic.ttf);font-weight:400;font-style:italic}
@font-face{font-family:"EBG";src:url(fonts/EBGaramond-SemiBold.ttf);font-weight:600;font-style:normal}
@font-face{font-family:"CZ";src:url(fonts/Cinzel-SemiBold.ttf);font-weight:600}
@font-face{font-family:"SG";src:url(fonts/SpaceGrotesk-Medium.ttf);font-weight:500}
html{background:#EAE1CE}
body{font-family:"EBG",Georgia,serif;color:#16120E;background:#EAE1CE;
     margin:0;padding:1.1em 1.2em 2em;line-height:1.62;text-align:left;
     -webkit-text-size-adjust:100%;text-size-adjust:100%}
h1{font-family:"CZ",Georgia,serif;font-weight:600;font-size:1.55em;line-height:1.22;
   letter-spacing:.05em;margin:0 0 .5em;color:#16120E;page-break-after:avoid}
h2{font-family:"CZ",Georgia,serif;font-weight:600;font-size:1.18em;letter-spacing:.05em;
   margin:1.6em 0 .5em;page-break-after:avoid}
h3{font-family:"CZ",Georgia,serif;font-weight:600;font-size:1em;letter-spacing:.06em;
   margin:1.4em 0 .4em;page-break-after:avoid}
p{margin:0 0 .85em;orphans:2;widows:2}
.kick{font-family:"SG",sans-serif;font-size:.62em;letter-spacing:.24em;text-transform:uppercase;
  color:#6E6155;margin:0 0 .5em}
.rule{border:0;border-top:1px solid #C3B597;margin:1.5em 0}
figure{margin:1.4em 0;padding:0;page-break-inside:avoid}
figure img{width:100%;height:auto;display:block;border:1px solid #C3B597}
figcaption{margin-top:.5em;font-size:.82em;color:#3B322A}
figcaption .id{font-family:"SG",sans-serif;font-size:.68em;letter-spacing:.2em;
  text-transform:uppercase;color:#6E6155;display:block;margin-bottom:.25em}
figcaption .t{font-family:"CZ",Georgia,serif;font-size:1.12em;letter-spacing:.04em;color:#16120E}
figcaption .a{font-family:"SG",sans-serif;font-size:.68em;letter-spacing:.16em;
  text-transform:uppercase;color:#8E2420;display:block;margin-top:.2em}
.status{font-family:"SG",sans-serif;font-size:.62em;letter-spacing:.16em;text-transform:uppercase;
  border:1px solid currentColor;padding:.1em .4em;white-space:nowrap}
.s-survives{color:#1E3566}.s-frag{color:#A8823C}.s-lost{color:#8E2420}
.scripture{margin:.7em 0 0}
.v{font-family:"SG",sans-serif;font-size:.6em;color:#8E2420;vertical-align:super;
   margin-right:.15em;font-weight:500}
.wj{color:#9B1C31}
.note{margin:.9em 0 0;padding-top:.6em;border-top:1px solid #C3B597}
.note .lbl{font-family:"SG",sans-serif;font-size:.62em;letter-spacing:.2em;text-transform:uppercase;
  color:#A8823C;display:block;margin-bottom:.3em}
.note p{font-style:italic;color:#3B322A;font-size:.94em;margin:0}
.drop::first-letter{font-family:"CZ",Georgia,serif;font-size:2.6em;line-height:.9;float:left;
  padding:.06em .1em 0 0;color:#8E2420}
.sig{font-family:"SG",sans-serif;font-size:.66em;letter-spacing:.2em;text-transform:uppercase;
  color:#3B322A;margin-top:1.4em}
.cover,.backcover{margin:0;padding:0}
.cover img,.backcover img{width:100%;height:auto;display:block;border:0}
.reg{margin:0;padding:0;list-style:none}
.reg li{padding:.35em 0;border-bottom:1px solid #D8CCB4;font-size:.88em}
.reg .k{font-family:"SG",sans-serif;font-size:.72em;letter-spacing:.1em;color:#3B322A;
  display:inline-block;min-width:5.2em}
.chapnum{font-family:"CZ",Georgia,serif;font-size:1.5em;color:#8E2420;letter-spacing:.08em}
.spec{font-family:"SG",sans-serif;font-size:.72em;letter-spacing:.08em;line-height:2;
  text-transform:uppercase;color:#3B322A}
"""

def doc(title, body, cls=""):
    return ('<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE html>\n'
            '<html xmlns="http://www.w3.org/1999/xhtml" '
            'xmlns:epub="http://www.idpf.org/2007/ops" lang="en">\n'
            '<head><meta charset="utf-8"/><title>%s</title>'
            '<link rel="stylesheet" type="text/css" href="style.css"/></head>\n'
            '<body%s>%s</body></html>'
            % (esc(title), (' class="%s"' % cls) if cls else "", body))

def verse_html(text, ranges):
    return B.verse_html(text, ranges)

def status_span(sc):
    lab, cls = B.status_of(sc)
    return '<span class="status s-%s">%s</span>' % (cls, lab)

def anchor_full(sc):
    out = []
    for p in sc.get("passages", []):
        for v in p["verses"]:
            out.append('<span class="v">%d</span>%s' % (v["verse"],
                       verse_html(v["text"], v.get("wordsOfJesus"))))
    return " ".join(out)

def prose_html(items, drop_first=True):
    out, first = [], True
    for kind, text in items:
        t = " ".join(text.split())
        if kind == "h":      continue
        elif kind == "h2":   out.append("<h2>%s</h2>" % esc(t)); first = True
        elif kind == "sig":  out.append('<p class="sig">%s</p>' % esc(t))
        elif kind == "drop": out.append('<p class="drop">%s</p>' % esc(t)); first = False
        else:                out.append("<p>%s</p>" % esc(t))
    return "".join(out)

files, spine, nav = [], [], []
def add(name, title, body, cls="", in_nav=True):
    files.append((name, doc(title, body, cls)))
    spine.append(name)
    if in_nav: nav.append((name, title))

# ---- cover, title, copyright ----
add("cover.xhtml", "Cover",
    '<div class="cover"><img src="plates/ebook_front.jpg" alt="Revelation"/></div>',
    cls="cover")
add("title.xhtml", "Title",
    '<p class="kick">Divergent World</p><h1>Revelation</h1>'
    '<p><i>An Illuminated Prophecy in Six Movements</i></p><hr class="rule"/>'
    '<p>The complete text of the Apocalypse of John, with ninety plates reconstructing the '
    'lost and surviving registers of the Angers cycle.</p>'
    '<p class="sig">Plates and commentary by %s</p>' % esc(AUTHOR), in_nav=False)
add("copyright.xhtml", "Copyright",
    "".join("<p>%s</p>" % esc(t) for t in [
      "Complete digital edition. First published 2026 by Divergent World.",
      "Plates © Ali Rahman / Divergent World.",
      "Scripture quotations are taken from the World English Bible, which is in the public "
      "domain. “World English Bible” is a trademark of eBible.org. The text is reproduced "
      "unmodified. Words spoken by Christ are set in red following the ranges marked in the "
      "official USFM edition.",
      "The ninety plates were generated with the assistance of generative image models "
      "between March and August 2026, against the fixed style contract described in the Note "
      "on Method. Each plate is marked to show whether the corresponding fourteenth-century "
      "compartment survives at Angers, survives only as a fragment, or is lost and has been "
      "reconstructed."]), in_nav=False)

add("foreword.xhtml", "Foreword",
    '<p class="kick">%s</p><h1>Foreword</h1>%s' % (esc(AUTHOR), prose_html(FOREWORD)))
add("losses.xhtml", "Note on the Angers Cycle",
    '<p class="kick">%s</p><h1>Note on the Angers Cycle</h1>%s' % (esc(AUTHOR), prose_html(LOSSES)))
add("method.xhtml", "Note on Method",
    '<p class="kick">%s</p><h1>Note on Method</h1>%s' % (esc(AUTHOR), prose_html(METHOD)))

# ---- movements ----
for tp in TAPS:
    roman, mtitle = tp["roman"], tp["title"]
    lead = SCENES[tp["leadSceneId"]]
    scenes = [SCENES[i] for i in tp["sceneIds"] if i != tp["leadSceneId"]]
    b = ['<p class="kick">Movement %s</p><h1>%s</h1>' % (esc(roman), esc(mtitle))]
    b.append('<figure><img src="plates/%s.jpg" alt="%s"/><figcaption>'
             '<span class="id">%s &#183; %s &#183; </span>'
             '<span class="t">%s</span></figcaption></figure>'
             % (lead["id"], esc(lead["alt"]), esc(lead["id"]),
                esc(lead["displayReference"]), esc(lead["title"])))
    b.append('<p class="drop">%s</p>' % esc(" ".join(tp["summary"].split())))
    for i, m in enumerate(tp["movements"], 1):
        b.append("<h3>%d. %s</h3><p>%s</p>"
                 % (i, esc(m["title"]), esc(" ".join(m["description"].split()))))
    b.append('<hr class="rule"/>')
    for sc in scenes:
        note = PLATE_NOTES.get(sc["id"], "")
        b.append('<figure><img src="plates/%s.jpg" alt="%s"/><figcaption>'
                 '<span class="id">%s &#183; Movement %s &#183; </span>%s'
                 '<span class="t">%s</span><span class="a">%s</span></figcaption></figure>'
                 % (sc["id"], esc(sc["alt"]), esc(sc["id"]), esc(roman), status_span(sc),
                    esc(sc["title"]), esc(sc["displayReference"])))
        b.append('<div class="scripture">%s</div>' % anchor_full(sc))
        if note:
            b.append('<div class="note"><span class="lbl">Note on the plate</span>'
                     '<p>%s</p></div>' % esc(note))
    ct, cbody = MOVEMENT_CODAS[tp["id"]]
    b.append('<hr class="rule"/><h2>%s</h2><p><i>%s</i></p>'
             % (esc(ct), esc(" ".join(cbody.split()))))
    add("movement-%d.xhtml" % tp["id"], "Movement %s — %s" % (roman, mtitle), "".join(b))

# ---- the complete text ----
for ch in REV["chapters"]:
    b = ['<p class="kick">The Revelation to John</p>'
         '<h1><span class="chapnum">Chapter %d</span></h1>' % ch["chapter"]]
    run = []
    for v in ch["verses"]:
        run.append('<span class="v">%d</span>%s' % (v["number"],
                   verse_html(v["text"], v.get("wordsOfJesus"))))
        if len(run) == 5:
            b.append("<p>%s</p>" % " ".join(run)); run = []
    if run: b.append("<p>%s</p>" % " ".join(run))
    add("rev-%02d.xhtml" % ch["chapter"], "Revelation %d" % ch["chapter"], "".join(b),
        in_nav=(ch["chapter"] == 1))

# ---- apparatus ----
rows = []
for tp in TAPS:
    rows.append("<h2>Movement %s &#183; %s</h2><ul class=\"reg\">" % (esc(tp["roman"]), esc(tp["title"])))
    for sid in tp["sceneIds"]:
        sc = SCENES[sid]
        rows.append('<li><span class="k">%s</span> %s &#160;&#183;&#160; %s &#160;%s</li>'
                    % (esc(sc["id"]), esc(sc["title"]),
                       esc(sc["displayReference"].replace("Revelation ", "")), status_span(sc)))
    rows.append("</ul>")
add("register.xhtml", "The Register of Losses",
    '<p class="kick">Concordance of the ninety compartments</p>'
    '<h1>The Register of Losses</h1>%s' % "".join(rows))

add("colophon.xhtml", "Colophon",
    "<h1>Colophon</h1>" + "".join("<p>%s</p>" % esc(" ".join(t.split())) for t in COLOPHON_LEFT) +
    '<hr class="rule"/><div class="spec">Edition — complete, digital<br/>Plates — 90<br/>'
    'Scripture — Revelation 1–22, complete<br/>Verses — 404<br/>'
    'Text — World English Bible<br/>Price — free</div>')
add("backcover.xhtml", "Back Cover",
    '<div class="backcover"><img src="plates/ebook_back.jpg" alt=""/></div>',
    cls="backcover", in_nav=False)

# ---- package ----
FONTS = INDESIGN / "Fonts"
FF = ["EBGaramond-Regular.ttf","EBGaramond-Italic.ttf","EBGaramond-SemiBold.ttf",
      "Cinzel-SemiBold.ttf","SpaceGrotesk-Medium.ttf"]
items = ['<item id="css" href="style.css" media-type="text/css"/>']
zf = zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED)
zi = zipfile.ZipInfo("mimetype"); zi.compress_type = zipfile.ZIP_STORED
zf.writestr(zi, "application/epub+zip")
zf.writestr("META-INF/container.xml",
    '<?xml version="1.0" encoding="UTF-8"?>\n<container version="1.0" '
    'xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles>'
    '<rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>'
    '</rootfiles></container>')
zf.writestr("OEBPS/style.css", CSS)
for f in FF:
    src = FONTS / f
    if src.exists():
        zf.write(src, "OEBPS/fonts/" + f)
        items.append('<item id="f%s" href="fonts/%s" media-type="font/ttf"/>'
                     % (re.sub(r"\W","",f), f))
used = set()
for _, body in files: used.update(re.findall(r'src="plates/([^"]+)"', body))
for f in sorted(used):
    zf.write(ARTWORK / f, "OEBPS/plates/" + f)
    items.append('<item id="i%s" href="plates/%s" media-type="image/jpeg"%s/>'
                 % (re.sub(r"\W","",f), f,
                    ' properties="cover-image"' if f == "ebook_front.jpg" else ''))
for name, body in files:
    zf.writestr("OEBPS/" + name, body)
    items.append('<item id="x%s" href="%s" media-type="application/xhtml+xml"/>'
                 % (re.sub(r"\W","",name), name))
navlist = "".join('<li><a href="%s">%s</a></li>' % (n, esc(t)) for n, t in nav)
zf.writestr("OEBPS/nav.xhtml",
    '<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE html>\n'
    '<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" '
    'lang="en"><head><meta charset="utf-8"/><title>Contents</title></head><body>'
    '<nav epub:type="toc" id="toc"><h1>Contents</h1><ol>%s</ol></nav>'
    '<nav epub:type="landmarks" hidden="hidden"><ol>'
    '<li><a epub:type="cover" href="cover.xhtml">Cover</a></li>'
    '<li><a epub:type="bodymatter" href="movement-1.xhtml">Begin Reading</a></li>'
    '</ol></nav></body></html>' % navlist)
items.append('<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>')
zf.writestr("OEBPS/content.opf",
    '<?xml version="1.0" encoding="utf-8"?>\n'
    '<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="bookid">\n'
    '<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">'
    '<dc:identifier id="bookid">urn:uuid:revelation-dw-2026-reflow</dc:identifier>'
    '<dc:title>Revelation — An Illuminated Prophecy in Six Movements</dc:title>'
    '<dc:creator>Ali Rahman</dc:creator><dc:language>en</dc:language>'
    '<dc:publisher>Divergent World</dc:publisher>'
    '<dc:rights>Plates and text (c) Ali Rahman / Divergent World. Scripture: World English '
    'Bible, public domain.</dc:rights>'
    '<meta property="dcterms:modified">2026-08-23T00:00:00Z</meta>'
    '<meta name="cover" content="iebookfrontjpg"/></metadata>\n'
    '<manifest>%s</manifest>\n<spine>%s</spine></package>'
    % ("".join(items),
       "".join('<itemref idref="x%s"/>' % re.sub(r"\W","",n) for n, _ in files)))
zf.close()
validate_epub(OUT, "reflowable")
print("wrote", OUT, round(OUT.stat().st_size/1e6,1), "MB |",
      len(files), "documents |", len(nav), "nav entries")
