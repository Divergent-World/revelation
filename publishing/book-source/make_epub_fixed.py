# -*- coding: utf-8 -*-
"""Fixed-layout EPUB 3 whose pages are rendered images.

The book's design depends on justification, hyphenation, multi-column boxes, tracking and
::first-letter drop caps. No two reading engines agree on those, so a live-text fixed
layout drifts and clips. Rendering each page guarantees the EPUB is pixel-identical to the
PDF. The reflowable edition is where the live text lives.
"""
import os, re, sys, zipfile, html
from playwright.sync_api import sync_playwright
from PIL import Image
from paths import BUILD

PAGES = BUILD / "epub_pages"
if len(sys.argv) > 1:
    PAGES = (BUILD.parent / sys.argv[1]).resolve()
OUT = BUILD / "REVELATION_iPad_fixed.epub"
BUILD.mkdir(parents=True, exist_ok=True)

files = sorted(f for f in os.listdir(PAGES) if f.endswith(".jpg"))
W, H = Image.open(PAGES / files[0]).size
print("%d pages at %d x %d" % (len(files), W, H))

# landmark titles, read from the live DOM (cheap: no screenshots)
with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page(viewport={"width": 1200, "height": 900})
    pg.goto((BUILD / "book.html").as_uri(),
            wait_until="load", timeout=240000)
    pg.wait_for_function("document.documentElement.getAttribute('data-ready')==='1'",
                         timeout=240000)
    marks = pg.evaluate("""() => {
        const out = [];
        document.querySelectorAll('.page').forEach((p, i) => {
            const n = i + 1;
            if (p.classList.contains('ebookcover')) out.push([n, 'Cover']);
            const mv = p.querySelector('.numeral');
            if (mv) {
                const t = p.querySelector('.mv h2');
                out.push([n, mv.textContent.trim() + ' — ' + (t ? t.textContent.trim() : '')]);
            }
            const dv = p.querySelector('.dv h1');
            if (dv) out.push([n, dv.textContent.trim()]);
            const sh = p.querySelector('.sechd h2');
            if (sh) out.push([n, sh.textContent.trim()]);
            if (p.classList.contains('colophon')) out.push([n, 'Colophon']);
        });
        return out;
    }""")
    b.close()
seen, landmarks = set(), []
for n, t in marks:
    if t and t not in seen:
        seen.add(t); landmarks.append((n, t))
print("nav entries:", len(landmarks))

def page_xhtml(i):
    return ('<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE html>\n'
            '<html xmlns="http://www.w3.org/1999/xhtml" '
            'xmlns:epub="http://www.idpf.org/2007/ops" lang="en">\n'
            '<head><meta charset="utf-8"/><title>Page %d</title>\n'
            '<meta name="viewport" content="width=%d, height=%d"/>\n'
            '<link rel="stylesheet" type="text/css" href="style.css"/></head>\n'
            '<body><div class="p"><img src="pages/p%03d.jpg" alt="Page %d"/></div></body>'
            '</html>' % (i, W, H, i, i))

CSS = ("@page{margin:0}\n"
       "html,body{margin:0;padding:0;width:%dpx;height:%dpx;background:#EAE1CE}\n"
       ".p{margin:0;padding:0;width:%dpx;height:%dpx}\n"
       ".p img{width:%dpx;height:%dpx;display:block;margin:0;padding:0}\n" % (W, H, W, H, W, H))

items, spine = [], []
zf = zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED)
zi = zipfile.ZipInfo("mimetype"); zi.compress_type = zipfile.ZIP_STORED
zf.writestr(zi, "application/epub+zip")
zf.writestr("META-INF/container.xml",
    '<?xml version="1.0" encoding="UTF-8"?>\n<container version="1.0" '
    'xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles>'
    '<rootfile full-path="OEBPS/content.opf" '
    'media-type="application/oebps-package+xml"/></rootfiles></container>')
zf.writestr("OEBPS/style.css", CSS)
items.append('<item id="css" href="style.css" media-type="text/css"/>')

for i, f in enumerate(files, 1):
    zf.write(PAGES / f, "OEBPS/pages/" + f)
    items.append('<item id="img%03d" href="pages/%s" media-type="image/jpeg"%s/>'
                 % (i, f, ' properties="cover-image"' if i == 1 else ''))
    name = "page-%03d.xhtml" % i
    zf.writestr("OEBPS/" + name, page_xhtml(i))
    items.append('<item id="p%03d" href="%s" media-type="application/xhtml+xml"/>' % (i, name))
    spread = "center" if i == 1 else ("right" if i % 2 == 1 else "left")
    spine.append('<itemref idref="p%03d" properties="rendition:page-spread-%s"/>' % (i, spread))

nav = "".join('<li><a href="page-%03d.xhtml">%s</a></li>' % (n, html.escape(t))
              for n, t in landmarks)
zf.writestr("OEBPS/nav.xhtml",
    '<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE html>\n'
    '<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" '
    'lang="en"><head><meta charset="utf-8"/><title>Contents</title></head><body>'
    '<nav epub:type="toc" id="toc"><h1>Contents</h1><ol>%s</ol></nav>'
    '<nav epub:type="landmarks" hidden="hidden"><ol>'
    '<li><a epub:type="cover" href="page-001.xhtml">Cover</a></li>'
    '<li><a epub:type="bodymatter" href="page-010.xhtml">Begin Reading</a></li>'
    '</ol></nav></body></html>' % nav)
items.append('<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>')

zf.writestr("OEBPS/content.opf",
    '<?xml version="1.0" encoding="utf-8"?>\n'
    '<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="bookid" '
    'prefix="rendition: http://www.idpf.org/vocab/rendition/#">\n'
    '<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">'
    '<dc:identifier id="bookid">urn:uuid:revelation-dw-2026-fixed</dc:identifier>'
    '<dc:title>Revelation — An Illuminated Prophecy in Six Movements</dc:title>'
    '<dc:creator>Ali Rahman</dc:creator><dc:language>en</dc:language>'
    '<dc:publisher>Divergent World</dc:publisher>'
    '<dc:rights>Plates and text (c) Ali Rahman / Divergent World. Scripture: World English '
    'Bible, public domain.</dc:rights>'
    '<meta property="dcterms:modified">2026-08-23T00:00:00Z</meta>'
    '<meta property="rendition:layout">pre-paginated</meta>'
    '<meta property="rendition:orientation">landscape</meta>'
    '<meta property="rendition:spread">both</meta>'
    '<meta name="cover" content="img001"/></metadata>\n'
    '<manifest>%s</manifest>\n<spine>%s</spine></package>'
    % ("".join(items), "".join(spine)))
zf.close()
print("wrote", OUT, round(OUT.stat().st_size/1e6, 1), "MB")
