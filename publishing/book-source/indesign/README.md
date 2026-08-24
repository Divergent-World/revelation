# REVELATION — InDesign package

Blurb **Large Landscape**, generated from the same `content/*.json` as the site and the ebook.

```
REVELATION_13x11.idml        the interior, 164 pp — open this
REVELATION_cover.idml        the cover, editable in InDesign
REVELATION_cover.pdf         the same cover, text outlined, upload-ready
REVELATION_cover_300dpi.png  the same cover as flat 300 ppi artwork
cover_bg.jpg                 the cover's background artwork (the IDML links to it)
Links_png/                   90 plates, your original PNGs, untouched pixels
Links/                       the same 90 as 3975 px JPEG, if you want a lighter file
Fonts/                       8 static cuts — install these BEFORE opening the document
```

## Digital editions

There are now two EPUBs, and the split is deliberate. A fixed-layout EPUB with live text
cannot match the PDF: the design depends on justification, hyphenation, multi-column boxes,
letter-spacing, `::first-letter` drop caps and clipped page boxes, and no two reading
engines agree on any of them. `REVELATION_iPad_fixed.epub` therefore ships each page as a
2048 × 1536 image — identical to the PDF, for Apple Books and tablets.
`REVELATION_reflowable.epub` carries the live text, generated from the content JSON, with
embedded fonts and the red-letter markup intact — for phones and Kindle.

## This build (v5)

**The complete scripture is now in the print edition.** All 22 chapters, 404 verses, words
of Christ in red, threaded across 12 pages as PART TWO between the movements and the
Register of Losses. Extent went 152 → **164 pages**.

**Which changes the spine.** Blurb derives spine width from the extent — 0.006763 in per
page. At 164 pages that is **1.109 in**, and the cover is now **27.102 × 11.618 in**. Both
the cover IDML and the cover PDF are drawn at that size. Regenerate the Blurb cover template
at 164 pages to confirm before you upload.

**The cover is editable now.** `REVELATION_cover.idml` is a real InDesign document — live
text frames for the title, subtitle, spine, back-cover copy and the three count marks, the
artwork linked rather than flattened, 12 paragraph styles. Use it when you want to change
wording. Use `REVELATION_cover.pdf` when you just want to upload.

**Drop caps are actually red this time.** The two previous attempts both went through the
paragraph style — first as an attribute, then correctly as an object property — and InDesign
ignored both. The reliable answer is that the drop cap takes its appearance from the
character formatting on the character itself, so the generator now splits the first letter
into its own character run with `DropCapRed` applied directly. 15 paragraphs, verified in
the story XML.

**Plates are no longer cropped.** Everything is contain-fit, so the whole image renders as
it does in the web PDF. Full-page plates sit centred on a night ground with the caption
beneath; band plates cap at 496 pt so the footer always has room. Nothing overset.

## Blurb preflight — what was failing and what fixed it

Three separate things, all now resolved.

**1. Interior page size.** Preflight wanted `12.625 × 10.875 in` and got `12.500 × 10.625`.
That difference decodes exactly: **0.125 in of bleed on the top, bottom and outside edge,
and none at the gutter.** The trim was right; the bleed was wrong and uniform. The document
now carries non-uniform bleed — top 9 pt, bottom 9 pt, inside 0, outside 9 pt — which
exports to precisely 12.625 × 10.875.

> **When you export:** File → Export → Adobe PDF (Print). Under **Marks and Bleeds**, tick
> **Use Document Bleed Settings** and leave every printer mark off. Export **Pages**, not
> spreads. Preset **PDF/X-4:2010**. If you don't tick Use Document Bleed Settings you get
> 12.5 × 10.625 again and preflight fails the same way.

**2. Cover size.** Preflight wanted `27.021 × 11.618 in` and got `25.750 × 13.250`. My
earlier reading of your cover template was wrong. The real geometry decodes as:

| | |
|---|---|
| Wrap | 0.4965 in per side (35.75 pt) |
| Panels | 12.5 in each (900 pt) |
| **Spine** | **1.028 in (74.02 pt)** — derived from 152 pages on your chosen paper |
| Total | 27.021 × 11.618 in = 1945.512 × 836.496 pt |

The cover is redrawn at exactly that. **The spine is the number tied to your extent** — if
the page count changes, Blurb recalculates it and this cover no longer fits. Tell me the new
count and I'll redraw.

**3. Non-embedded fonts in the cover.** Chromium's PDF writer referenced EB Garamond and
Cinzel without fully embedding them. Rather than fight it, **all cover text is now converted
to outlines** — `pdffonts` reports zero fonts in the file, so there is nothing left to embed
or substitute. It stays fully vector and sharp. The interior never had this problem because
InDesign embeds properly on export.

While fixing the outlining I found the gradients were being flattened away by the same pass,
so the cover's darkening is now baked into the artwork itself rather than layered as
transparency. Same look, nothing for a PDF processor to misinterpret.

## Also fixed in this build

**Drop caps really are red now.** `DropCapStyle` is an *object reference*, not an attribute
— it has to sit inside `<Properties>` as `<DropCapStyle type="object">`. I had written it as
an attribute, which InDesign silently ignores, which is why they stayed black. Both
`BodyDrop` and `MvArg` now carry it properly and pick up the `DropCapRed` character style.

**The beige was wrong, and so were most of the swatches.** You were right to check. The
ebook PDF's vellum is `#EAE1CE`; my swatch was `C5 M6 Y18 K0`, which renders back as
`#F2F0D1` — noticeably lighter and greener. Every swatch has now been measured by pushing
the PDF's own hex value through a real RGB→CMYK transform:

| Swatch | PDF hex | was | now |
|---|---|---|---|
| Vellum | #EAE1CE | C5 M6 Y18 K0 | **C7.1 M9 Y18.8 K0** |
| Rubric | #8E2420 | C15 M96 Y88 K8 | **C27.1 M96.1 Y96.9 K27.8** |
| Gold | #A8823C | C25 M40 Y92 K4 | **C31 M45.5 Y91 K9** |
| Rule | #C3B597 | C14 M16 Y30 K0 | **C23.9 M24.7 Y42.7 K0** |
| WJ (words of Christ) | #9B1C31 | C8 M96 Y78 K2 | **C25.1 M99.6 Y80 K21.6** |
| Night | #0E0A08 | C74 M68 Y66 K82 | **C69.4 M67.5 Y67.5 K84.3** |

Two deliberate exceptions: `InkSoft` and `Faint` carry text at 5.5–10 pt, and their true
conversions are four-colour darks that go fuzzy at that size if the press drifts. They are
kept K-dominant with a little warmth — `C0 M6 Y12 K76` and `C0 M5 Y14 K52` — so small type
stays crisp. Everything else matches the PDF.

## What changed in the previous build

**The trim was wrong.** Blurb markets this format as 13 × 11 in; the actual trim is
**12.5 × 10.625 in — 900 × 765 pt**. Confirmed two ways: Blurb's dimensions page lists Large
Landscape as 12.50 × 10.63, and the `revelation Pages.indd` you made with Book Creator
carries `900 × 765` in its document record.

**Two links were broken, not a handful.** `T1-T07.png` and `T4-B01.png` were truncated —
written without their closing `IEND` chunk when the conversion job timed out mid-file. Both
are regenerated and all 90 now verify as complete PNGs.

**The page grounds were missing entirely.** In the PDF the beige comes from a CSS page
background. An InDesign page has no background — it is white unless you draw a rectangle on
it. I never drew one, which is why the beige vanished and why the frontispiece sat on white
instead of near-black. Every page now carries a full-bleed ground rectangle: **124 vellum,
26 night** (frontispiece and the full-bleed plates), **2 dark** (the part dividers).

**Drop caps are red.** InDesign does not colour a drop cap from the paragraph — it takes it
from a nominated character style. There is now a `DropCapRed` character style in Cinzel and
Rubric, applied by `BodyDrop` and `MvArg`.

**The front matter is yours.** The foreword was written as though someone else were
introducing your work, with a placeholder for a commissioned author. It is now first person
throughout and signed by you, and the note on method is rewritten from your own project
files — the style contract, the six colour grades and their progression from centred light
to eternal light, the viewer-space rule, the character canon, and the seven-count constraint
with its 4-against-3 arrangement. The colophon credits you for design, writing, generation
and typesetting.

## Open it in this order

1. **Install the fonts first.** Select all 8 in `Fonts/`, right-click → Open → Install. If
   you open the document without them InDesign substitutes and everything recomposes.
2. Open `REVELATION_13x11.idml`, then immediately **File → Save As** → `.indd`.
3. Window → Links: all 90 linked, none missing. They point at `Links_png/` by absolute
   path, so don't move that folder.

## Interior specification

| | |
|---|---|
| Trim | 12.5 × 10.625 in — 900 × 765 pt, facing pages |
| Bleed | top 9 · bottom 9 · inside 0 · outside 9 pt — exports to 12.625 × 10.875 in |
| Margins | top 50 · bottom 62 · inside 64 · outside 54 pt |
| Extent | 164 pages |
| Plates | 90, original PNGs, 279–413 ppi on the page |
| Paragraph styles | 61 · Character styles 6 · Swatches 16, matched to the ebook PDF |

Everything is styled. Change `Body` and every prose page recomposes. The only local
formatting is the red-letter words of Christ (`WJ`) and the verse numbers (`VNum`).

## The cover

`REVELATION_cover.pdf` is drawn at **1945.512 × 836.496 pt (27.021 × 11.618 in)** — the size
Blurb's preflight asked for. Upload it directly to the PDF uploader as the cover file; it
does not need to go through InDesign at all. `REVELATION_cover_300dpi.png` is the same
artwork flattened, if you'd rather place a raster into the Book Creator cover template.

All text in the PDF is outlined, so there are no fonts to embed and nothing to substitute.
The darkening is baked into the artwork rather than layered as transparency, so no PDF
processor can flatten it away.

**The spine is 1.109 in and that number belongs to 164 pages on your paper.** Change the
extent or the stock and Blurb recalculates it; this cover will no longer fit. Tell me the new
page count and I'll redraw it.

The artwork uses T3-T07, *Woman and the dragon*, darkened across the back panel and lifted
on the front. Text is live vector in the PDF, so it stays sharp. The ISBN box on the back is
an empty placeholder — drop your barcode into it.

## Before you export

**1. Preflight for overset.** Nothing is predicted to overset, but InDesign's composer is
not identical to the one I measured with.

**2. Replace the eleven low-resolution plates.** Still the March–April generations at
1536 px, landing between 119 and 178 ppi on a 12.5 in page:

```
T1-00  T1-T01  T1-T02  T1-B01  T1-B03  T2-00  T2-T04
T3-00  T4-00   T5-00   T6-00
```

All six reader panels are among them and they are the largest images in the book. Drop
replacements into `Links_png/` under the same names and InDesign relinks automatically.
Every other placement is 279–413 ppi.

**3. Think about the beige.** A flat vellum tint across 124 pages is a lot of ink. On
uncoated stock it can mottle, and any variation between signatures will show as banding
across a book that is mostly one flat colour. The professional alternative is to print on
a naturally cream stock — Mohawk Superfine comes in Softwhite and a warmer shade — and set
the page ground to white. You'd get the same warmth with none of the risk and slightly
lower cost. If you want that, delete the `Vellum` grounds; they are all on the same layer
and selectable in one pass with Edit → Select All then filtering by fill.

**4. Extent.** 152 pages, a multiple of 4, comfortably under Blurb's 240-page cap for
Mohawk and proPhoto Pearl.

## If you rebuild this yourself

```bash
python3 measure.py         # re-measures how prose flows at the current trim
python3 build_idml.py      # content JSON + prose.py -> IDML
python3 validate_idml.py   # structural check
python3 check_overset.py   # predicts text overset
```

Two things that will bite you. `DocumentPreference/@PagesPerDocument` must be **1** — it is
the Document Setup default and InDesign creates that many pages *before* importing the
spreads. And the designmap needs a `<Section>` whose `PageStart` is the first page's `Self`
id. Both are checked by `validate_idml.py`.

Editing in InDesign and regenerating are mutually exclusive. Once you start laying out by
hand, work in the `.indd` and retire the generator for that edition.
