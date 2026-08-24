# REVELATION — Master Context

**Drop this whole file into a new conversation to pick the project up cold.**

Ali Rahman / Divergent World · last updated 23 August 2026

---

## 1. What this is

A reconstruction of the **Apocalypse Tapestry of Angers** as a modern illuminated book.

Ninety compartments were woven at Angers between 1377 and 1382 — the entire Book of
Revelation as a continuous visual narrative, six tapestries, roughly 140 metres. Roughly
seventy survive, many damaged; about twenty were destroyed during the Revolution (cut up
for horse blankets, orangery pipe lagging, rags). The *sequence* has not been experiencable
since the eighteenth century.

Ali has rebuilt all ninety plates with generative models against a fixed system, in the
original order, against the original Revelation anchors. Every plate is marked
**SURVIVES / FRAGMENT / RECONSTRUCTED** so the reader always knows how much is evidence and
how much is argument. That honesty is the intellectual spine of the project.

Three products:

| | |
|---|---|
| **Web** | alirahman.com — Next.js static site, already built |
| **Digital edition** | Free. Complete: 90 plates + all 404 verses. PDF + two EPUBs (see §4) |
| **Collector's print edition** | Blurb Large Landscape hardcover, 164 pp, target $250–300 |

---

## 2. Where everything lives

```
~/Desktop/test/revelations/                 the Next.js repo — CANONICAL DATA
  content/tapestries.json                   90 scenes, movements, resolved passages
  content/scene-metadata.json               titles + anchors      ← canonical
  content/source-map.json                   slot -> vault file + SHA-256
  content/revelation.web.json               22 chapters, wordsOfJesus char ranges
  book/                                     the book generator (see §6)
    prose.py  build_idml.py  build_cover_idml.py  idml_lib.py
    validate_idml.py  check_overset.py  measure.py
    build.py  render.py  render_pages.py  theme.css  paginate.js
    make_epub_fixed.py  make_epub_reflow.py
    indesign/
      REVELATION_13x11.idml                 interior, 164 pp
      REVELATION_cover.idml                 cover, editable
      REVELATION_cover.pdf                  cover, outlined, upload-ready
      Links_png/                            90 original PNGs, 300 dpi tagged, 1.5 GB
      Links/                                same 90 as 3975 px JPEG, 178 MB
      Fonts/                                8 static cuts — install before opening

~/Desktop/Obsidian/Ali's Vault/Apocalypse Tapestry/    the art archive
  Tapestries/I..VI/                         ~162 source PNGs, 20–29 MB each
  INDEX/Master Index.md                     ⚠ SUPERSEDED — see §3
  _book-build/                              earlier deliverables, plate previews
```

---

## 3. Data integrity — read this before touching captions

**`content/scene-metadata.json` in the repo is canonical.** The vault's
`INDEX/Master Index.md` disagrees with it on **29 of the 90 slots**, across Movements I–III,
and is shifted one position late from T3-T05 onward.

This was settled by looking at the picture: `T3-T07` shows a crowned woman on a cloud with a
child and a seven-headed dragon — Revelation 12:1–6, *Woman and the dragon*, which is what
the repo says. The vault file calls it *Saint Michael*. The repo wins.

Anything that joins by slot id against the vault index will produce wrong captions. The
generator therefore joins **survival status by title, not by slot**, which is immune to the
shift. Statuses themselves are from published accounts of the cycle and are **still
unverified against the Musée de la Tapisserie's conservation records** — the one open
research task.

---

## 4. The hard-won production knowledge

Everything below cost real debugging. None of it is guessable.

### Blurb Large Landscape geometry

| | |
|---|---|
| Marketed as | 13 × 11 in |
| **Actual trim** | **12.5 × 10.625 in = 900 × 765 pt** |
| **Required exported page** | **12.625 × 10.875 in** |
| Which means bleed of | 0.125 in top, 0.125 in bottom, **0 at the gutter**, 0.125 in outside |
| Wrap on the cover | 0.4965 in per side (35.748 pt) |
| **Spine** | **pages × 0.006763 in** — 152 pp = 1.028 in, 164 pp = 1.109 in |
| Cover page | 2 × 900 pt + spine + 2 × 35.748 pt wide; 765 + 2 × 35.748 pt tall |
| Premium paper cap | 240 pages (Mohawk Superfine, proPhoto Pearl). Standard stock goes to 440 |

The spine constant was derived from Blurb's own preflight expectation at 152 pages and is
linear. **Any change in extent changes the cover size.** Regenerate both.

**Export settings that actually matter:** File → Export → Adobe PDF (Print), preset
**PDF/X-4:2010**, Marks and Bleeds → tick **Use Document Bleed Settings**, all printer marks
off, export **Pages** not spreads. Without that tick the page comes out at trim and preflight
rejects it.

### IDML gotchas

These four cost the most time:

1. **`DocumentPreference/@PagesPerDocument` must be `1`.** It is the Document Setup default,
   not the page count. InDesign creates that many pages *and then* imports the spreads — set
   it to 164 and you get 164 blank pages in front of the book.

2. **The designmap needs a `<Section>` element** whose `PageStart` is the first page's `Self`
   id and whose `Length` is the real page count, or numbering is wrong.

3. **Object-typed properties belong in `<Properties>`, never as attributes.** Written as an
   attribute they are silently ignored. This is why drop caps stayed black through two
   attempted fixes.

4. **Drop cap colour comes from the character, not the paragraph style.** Even a correct
   `<DropCapStyle type="object">` was not enough. The reliable fix is to split the first
   character into its own `CharacterStyleRange` with the red character style applied
   directly. That is what the generator does now.

Also: an InDesign page has **no background**. It is white unless you draw a rectangle. The
beige vanished from the first IDML build for exactly this reason.

### Colour

Swatches were measured by pushing the ebook PDF's own hex values through a real RGB→CMYK
transform, not eyeballed:

| | hex | CMYK |
|---|---|---|
| Vellum (page ground) | #EAE1CE | 7.1 / 9 / 18.8 / 0 |
| Rubric | #8E2420 | 27.1 / 96.1 / 96.9 / 27.8 |
| WJ (words of Christ) | #9B1C31 | 25.1 / 99.6 / 80 / 21.6 |
| Gold | #A8823C | 31 / 45.5 / 91 / 9 |
| Rule | #C3B597 | 23.9 / 24.7 / 42.7 / 0 |
| Night | #0E0A08 | 69.4 / 67.5 / 67.5 / 84.3 |

**Exception:** `InkSoft` and `Faint` carry 5.5–10 pt text. Their true conversions are
four-colour darks that go fuzzy at that size if the press drifts, so they are kept
K-dominant — `0/6/12/76` and `0/5/14/52`.

### Images

- **Link resolution ≠ placed resolution.** A 3840 × 2160 plate is 12.8 × 7.2 in at 300 dpi;
  bleeding it across a 10.625 in page scales it up 1.56× to **192 ppi**. Full-bleed is
  therefore assigned by pixel count, and everything is now **contain-fit** so no plate is
  cropped — matching the web PDF.
- Links point at **original PNGs**, byte-identical to the vault, with only a `pHYs` chunk
  injected declaring 300 dpi. Without that InDesign assumes 72 dpi and places them 4× too big.
- Two PNGs (`T1-T07`, `T4-B01`) were once truncated mid-write and showed as broken links.
  If links break again, check for a missing `IEND` chunk first.

### EPUB — why there are two

A **fixed-layout EPUB with live text will not match the PDF**, and it is worth knowing why
before anyone tries again. This design leans on justified text, automatic hyphenation,
multi-column boxes, letter-spacing on 51 rules, `::first-letter` drop caps and
`overflow:hidden` page boxes. No two reading engines agree on any of those. A line that
breaks one word differently reflows a column, and `overflow:hidden` then clips it — which
reads as "glitchy".

So the fixed edition renders each page to an image at 2048 × 1536 (about 170 ppi across a
12 in page) and ships those. Fidelity is guaranteed. The live text lives in the reflowable
edition instead, generated from the content JSON rather than from a paginated layout, which
is the edition that actually works on a phone.

### Cover PDF

Chromium's PDF writer references fonts without fully embedding them, which Blurb rejects.
**All cover text is converted to outlines** with `gs -dNoOutputFonts`. That pass also
flattens CSS alpha gradients, so the cover's darkening is **baked into the artwork in PIL**
rather than layered as transparency.

---

## 5. Design system

| Role | Face | Notes |
|---|---|---|
| Display, movement titles, drop caps | **Cinzel** SemiBold | inscriptional Roman caps |
| Scripture and prose | **EB Garamond** | |
| Author's notes | **Cormorant Garamond** Italic | |
| Apparatus — slot ids, status chips, folios | **Space Grotesk** Medium | tightly tracked, uppercase |

All four are SIL OFL. Static cuts were instanced from the variable originals with fontTools
and live in `book/indesign/Fonts/`.

The two families deliberately do not reconcile: one belongs to the manuscript, the other to
the system that rebuilt it. That tension is the book's visual argument, and it is borrowed
from Abloh/Zak Group's *Nike. ICONS*, where the binding discloses the book's own production.

**Interior grid** (900 × 765 pt): margins top 50 · bottom 62 · inside 64 · outside 54 pt;
content width 782 pt; two-column gutter 31 pt. 61 paragraph styles, 6 character styles.
Nothing is locally formatted except the words of Christ (`WJ`) and verse numbers (`VNum`).

**Structure:** half-title · frontispiece · title · copyright · contents · foreword · note on
the Angers cycle · note on method · PART ONE, the six movements (opener + four-part argument
+ 14 plates + coda each) · PART TWO, the complete Revelation · PART THREE, the Register of
Losses · colophon.

---

## 6. The build

Everything generates from `content/*.json` plus `prose.py`. Nothing is hand-placed.

```bash
cd ~/Desktop/test/revelations/book

python3 measure.py                 # re-measure how prose flows at the current trim
python3 build_idml.py              # -> indesign/REVELATION_13x11.idml
python3 build_cover_idml.py 164    # -> indesign/REVELATION_cover.idml (pass the page count)
python3 validate_idml.py           # structural check — run this every time
python3 check_overset.py           # predicts text overset before InDesign sees it

python3 build.py && python3 render.py   # -> REVELATION_complete_edition.pdf
python3 render_pages.py                 # -> epub_pages/*.jpg  (one image per page)
python3 make_epub_fixed.py              # -> REVELATION_iPad_fixed.epub
python3 make_epub_reflow.py             # -> REVELATION_reflowable.epub
cd cover && python3 make_bg.py 164 && python3 rc.py   # cover artwork at a given extent
```

`LINK_SET=jpg python3 build_idml.py` swaps the 1.5 GB PNG links for the 178 MB JPEGs.

**Where to edit what:** prose lives in `prose.py` as plain strings. Typography, colour and
grid live in `build_idml.py`'s style block. Page order and plate pacing live in the body of
`build_idml.py`. Text flow across pages is `paginate.js`.

**Editing in InDesign and regenerating are mutually exclusive.** Once hand layout starts,
work in the `.indd` and retire the generator for that edition.

---

## 7. Current state

- **Interior IDML** — 164 pp, includes the complete scripture with red words of Christ,
  contain-fit plates, red drop caps, matched swatches. Validates clean, no predicted overset.
- **Cover** — editable IDML *and* outlined upload-ready PDF, both at 27.102 × 11.618 in for
  164 pages.
- **Digital edition** — 182-page PDF plus **two** EPUBs, all with front and back covers and
  all 404 verses:
  - `REVELATION_iPad_fixed.epub` (55 MB) — fixed layout, pages as 2048 × 1536 images.
    Pixel-identical to the PDF. For Apple Books and tablets.
  - `REVELATION_reflowable.epub` (27 MB) — real text, 37 documents, embedded fonts,
    red-letter intact, plates full-width. For phones and Kindle.
- **A 152-page version has been ordered from Blurb** and is in transit. It does **not**
  contain the scripture section; the 164-page build supersedes it.

---

## 8. Open items

1. **Regenerate 11 plates.** Still the March–April generations at 1536 px, landing at
   119–178 ppi. All six reader panels are among them and they are the largest images in the
   book. Drop replacements into `Links_png/` under the same names and InDesign relinks.
   Everything else sits at 279–413 ppi.

   ```
   T1-00  T1-T01  T1-T02  T1-B01  T1-B03  T2-00  T2-T04
   T3-00  T4-00   T5-00   T6-00
   ```

2. **Verify survival statuses** against the Musée de la Tapisserie's records. This is the
   book's central claim and it is currently sourced from published summaries.

3. **Decide the licence for the print edition.** Artwork is currently CC BY-SA 4.0, which
   permits anyone to print and sell this book. The usual split is BY-NC-SA for web and the
   free ebook, all rights reserved for print.

4. **Commission or finalise a foreword.** Currently first person by Ali, which works. An
   outside voice — an Angers scholar, a working artist — is what an acquisitions editor
   looks for.

5. **Think about the beige on press.** A flat vellum tint across 124 pages is a lot of ink
   and can mottle or band on uncoated stock. The alternative is printing on naturally cream
   stock with the ground left white.

6. **Buy ISBNs** — one per format, own them rather than taking a vendor's.

7. **Tapestry VII.** A seventh vault folder exists with a cover image and a 28 KB document.
   Expansion, appendix, or dead? Unresolved.

---

## 9. Business

| | |
|---|---|
| Collector's, Blurb, 164 pp, Mohawk Superfine | est. $115–165 unit → retail $250–300 |
| Trade, IngramSpark 11 × 8.5 casebound | retail $55–70 |
| Digital | free — the funnel for both |

Break-even is roughly 20–30 collector's copies. Setup (proofs, ISBNs, foreword) runs
$1,100–3,150. Offset via Kickstarter is the eventual path once the POD edition proves demand;
500–1500 units unlocks Swiss binding, foil and real paper choices. *Figures of Speech* and
*Nike. ICONS* both sit at $80 for mass-produced offset, which is the ceiling the market has
proven for a designer art book — a short-run object at $250 is a different and defensible
proposition.

---

## 10. How to brief a new conversation

> I'm building REVELATION, an illuminated art book reconstructing the Apocalypse Tapestry of
> Angers — 90 plates plus the complete text of Revelation. The repo is at
> `~/Desktop/test/revelations`, the art archive is in my Obsidian vault under
> `Apocalypse Tapestry`. The book generates from `content/*.json` via the scripts in `book/`.
> Attached is the master context. [this file]
>
> Today I want to: ______

Connect both folders at the start. The generator needs the repo; the plate archive needs
the vault.
