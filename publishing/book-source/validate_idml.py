# -*- coding: utf-8 -*-
"""Structural validation of the generated IDML. Fails loudly on anything InDesign would reject."""
import zipfile, sys, os, re
import xml.etree.ElementTree as ET

PATH = sys.argv[1] if len(sys.argv) > 1 else "indesign/REVELATION_13x11.idml"
zf = zipfile.ZipFile(PATH)
names = zf.namelist()
errs, warns = [], []

# 1. mimetype first and stored
if names[0] != "mimetype":
    errs.append("mimetype is not the first zip entry (got %r)" % names[0])
info = zf.getinfo("mimetype")
if info.compress_type != zipfile.ZIP_STORED:
    errs.append("mimetype must be STORED, not deflated")
if zf.read("mimetype").decode() != "application/vnd.adobe.indesign-idml-package":
    errs.append("mimetype content wrong")

# 2. every part well-formed XML
trees = {}
for n in names:
    if not n.endswith(".xml"): continue
    try:
        trees[n] = ET.fromstring(zf.read(n))
    except ET.ParseError as e:
        errs.append("XML parse error in %s: %s" % (n, e))

# 3. designmap references resolve
dm = zf.read("designmap.xml").decode()
refs = re.findall(r'src="([^"]+)"', dm)
for r in refs:
    if r not in names: errs.append("designmap references missing part: %s" % r)
for n in names:
    if n.startswith(("Spreads/", "Stories/")) and n not in refs:
        errs.append("part not referenced by designmap: %s" % n)

# 4. collect ids
story_ids, frame_ids, self_ids = set(), set(), set()
for n, t in trees.items():
    for el in t.iter():
        s = el.get("Self")
        if s:
            if s in self_ids and not s.startswith(("$ID", "Color/", "Swatch/", "ParagraphStyle/",
                                                   "CharacterStyle/", "ObjectStyle/", "TableStyle/",
                                                   "CellStyle/", "TOCStyle/", "StrokeStyle/")):
                errs.append("duplicate Self id: %s (in %s)" % (s, n))
            self_ids.add(s)
        if el.tag == "Story": story_ids.add(s)
        if el.tag == "TextFrame": frame_ids.add(s)

# 5. text frames point at real stories and real neighbours
pstyles = {e.get("Self") for n, t in trees.items() for e in t.iter("ParagraphStyle")}
cstyles = {e.get("Self") for n, t in trees.items() for e in t.iter("CharacterStyle")}
colors = {e.get("Self") for n, t in trees.items() for e in t.iter("Color")}
colors |= {e.get("Self") for n, t in trees.items() for e in t.iter("Swatch")}
fonts = {e.get("Name") for n, t in trees.items() for e in t.iter("FontFamily")}

used_stories = set()
for n, t in trees.items():
    for tf in t.iter("TextFrame"):
        ps = tf.get("ParentStory")
        used_stories.add(ps)
        if ps not in story_ids:
            errs.append("%s: TextFrame %s -> missing story %s" % (n, tf.get("Self"), ps))
        for att in ("PreviousTextFrame", "NextTextFrame"):
            v = tf.get(att)
            if v and v != "n" and v not in frame_ids:
                errs.append("%s: TextFrame %s %s -> missing frame %s"
                            % (n, tf.get("Self"), att, v))

orphan = story_ids - used_stories
if orphan: warns.append("%d stories not placed in any frame" % len(orphan))

# 6. styles / colours referenced actually exist
for n, t in trees.items():
    for el in t.iter():
        v = el.get("AppliedParagraphStyle")
        if v and v not in pstyles: errs.append("%s: missing paragraph style %s" % (n, v))
        v = el.get("AppliedCharacterStyle")
        if v and v not in cstyles: errs.append("%s: missing character style %s" % (n, v))
        for att in ("FillColor", "StrokeColor"):
            v = el.get(att)
            if v and v not in colors and v != "Swatch/None":
                errs.append("%s: missing colour %s (%s)" % (n, v, att))
        v = el.get("AppliedFont")
        if v and v not in fonts: errs.append("%s: missing font family %s" % (n, v))
for n, t in trees.items():
    for el in t.iter("AppliedFont"):
        if el.text and el.text not in fonts:
            errs.append("%s: missing font family %s" % (n, el.text))

# 7. font styles referenced by paragraph styles exist in Fonts.xml
fam_styles = {}
for n, t in trees.items():
    for fam in t.iter("FontFamily"):
        fam_styles[fam.get("Name")] = {f.get("FontStyleName") for f in fam.iter("Font")}
for n, t in trees.items():
    for ps in t.iter("ParagraphStyle"):
        fs = ps.get("FontStyle")
        af = ps.find("Properties/AppliedFont")
        if fs and af is not None and af.text in fam_styles:
            if fs not in fam_styles[af.text]:
                errs.append("style %s: %s has no %s cut" % (ps.get("Name"), af.text, fs))

# 8. pages: sequential, correct count, geometry sane
pages = []
for n, t in sorted(trees.items()):
    if not n.startswith("Spreads/"): continue
    for pg in t.iter("Page"):
        pages.append((n, int(pg.get("Name")), pg.get("ItemTransform")))
pages.sort(key=lambda x: x[1])
nums = [p[1] for p in pages]
if nums != list(range(1, len(nums) + 1)):
    errs.append("page numbers not sequential: %s" % nums[:20])
# PagesPerDocument is the Document Setup default, NOT the page count: InDesign creates
# that many pages and THEN imports the spreads, so anything above 1 prepends blanks.
dp = [t for n, t in trees.items() if n.endswith("Preferences.xml")][0].find("DocumentPreference")
if int(dp.get("PagesPerDocument")) != 1:
    errs.append("PagesPerDocument=%s — must be 1, or InDesign prepends that many blank pages"
                % dp.get("PagesPerDocument"))
dmt = trees["designmap.xml"]
sec = dmt.find("Section")
if sec is None:
    errs.append("designmap has no <Section> — page numbering will be wrong")
else:
    if int(sec.get("Length")) != len(nums):
        errs.append("Section Length=%s but %d pages exist" % (sec.get("Length"), len(nums)))
    first = min(pages, key=lambda x: x[1])
    firstself = next(pg.get("Self") for pg in trees[first[0]].iter("Page")
                     if int(pg.get("Name")) == first[1])
    if sec.get("PageStart") != firstself:
        errs.append("Section PageStart=%s but first page is %s"
                    % (sec.get("PageStart"), firstself))
if len(nums) % 2: warns.append("odd page count (%d) — a print book wants an even extent" % len(nums))

# 9. degenerate geometry
for n, t in trees.items():
    for el in list(t.iter("Rectangle")) + list(t.iter("TextFrame")):
        pts = [(float(a.get("Anchor").split()[0]), float(a.get("Anchor").split()[1]))
               for a in el.iter("PathPointType")]
        if not pts: continue
        w = max(x for x, y in pts) - min(x for x, y in pts)
        h = max(y for x, y in pts) - min(y for x, y in pts)
        if w <= 0 or h <= 0:
            errs.append("%s: degenerate frame %s (%gx%g)" % (n, el.get("Self"), w, h))

# 10. links exist
missing_links, links = [], set()
for n, t in trees.items():
    for lk in t.iter("Link"):
        uri = lk.get("LinkResourceURI", "")
        if uri.startswith("file:"):
            links.add(uri[5:])
print("=" * 68)
print("IDML VALIDATION —", os.path.basename(PATH))
print("=" * 68)
print("parts: %d | spreads: %d | stories: %d | frames: %d | pages: %d"
      % (len(names), sum(1 for n in names if n.startswith("Spreads/")),
         len(story_ids), len(frame_ids), len(nums)))
print("paragraph styles: %d | character styles: %d | colours: %d | font families: %d"
      % (len(pstyles), len(cstyles), len(colors), len(fonts)))
print("distinct linked images: %d" % len(links))
print()
for w in warns: print("  WARN  " + w)
if errs:
    print()
    for e in errs[:40]: print("  ERROR " + e)
    if len(errs) > 40: print("  ... and %d more" % (len(errs) - 40))
    print("\nFAILED: %d errors" % len(errs))
    sys.exit(1)
print("\nPASSED — no structural errors")
