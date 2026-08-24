# REVELATION — Production Bible

**An Illuminated Prophecy in Six Movements**
Plates and commentary by Ali Rahman · Divergent World
Version 1.0 · 14 August 2026

---

## 0. What this document is

The Google Doc is a raw export. This is the spec that turns it into a product: a premium
printed art book, a free or low-cost ebook, and a file set you can hand to a printer or a
publisher without further explanation.

Decisions locked in this pass:

| | |
|---|---|
| **Trim** | 12 × 9 in landscape |
| **Scripture** | Anchor passages beside plates; complete WEB Revelation as a back reading section |
| **Path** | Print-on-demand first, offset later |
| **Sub-resolution plates** | Regenerate on current models |

---

## 1. The thesis

The reason this can be an art book rather than a Bible with pictures is that it is a
**restoration project with its system left visible.**

Ninety registers were woven at Angers between 1377 and 1382. They were cut up, sold, used
as horse blankets and to lag orangery pipes. Roughly seventy survive. You have rebuilt all
ninety — against a fixed style contract, a coordinate system for viewer space, and a LUT
discipline, so that ninety images made across six months read as one hand.

That process is the content. The book should therefore run **two typographic voices that do
not reconcile**:

- **The manuscript voice** — Cinzel inscriptional capitals, EB Garamond scripture,
  rubricated verse numbers, generous vellum ground. This is the illuminated Bible.
- **The apparatus voice** — Space Grotesk, uppercase, tightly tracked, small. Slot IDs,
  survival status, register position, palette codes, source resolution. This is the system.

This is exactly the move Abloh and Zak Group made in *Nike. ICONS* — the book is "equal
parts catalog and conceptual toolbox," and the Swiss binding deliberately "discloses the
production of the book." Your equivalent of the exposed spine is the **status chip** on
every plate: `SURVIVES` / `FRAGMENT` / `RECONSTRUCTED`. It tells the reader, on every page,
how much of what they are looking at is evidence and how much is argument. Nothing else in
the book will do as much work.

**On the reference books.** The two you're remembering are almost certainly
*Virgil Abloh: Figures of Speech* (DelMonico Books, 2022 — 9.5 × 12.75 in, 496 pp,
cloth hardcover, $79.95) and *Virgil Abloh. Nike. ICONS* (Taschen, 2021 — 10 × 11.7 in,
352 pp, 5.1 lb, **Swiss binding with open spine**, $80). The construction and materials you
described point at ICONS. Both sit at $80 — worth noting, because that is the ceiling the
market has already proven for a designer art book at this scale.

---

## 2. The three editions

| | Premium print | Trade print | Ebook |
|---|---|---|---|
| **Format** | 12 × 9 in, section-sewn, exposed spine, cloth, foil | 11 × 8.5 in landscape, casebound | Fixed-layout EPUB 3 + Kindle |
| **Extent** | ~328 pp | ~328 pp | same pagination |
| **Run** | Offset, 500–1500 | POD | — |
| **Price** | $95–140 | $45–60 | Free or $4.99 |
| **Timing** | After the POD edition proves demand | Now | With the trade edition |

The ebook being free is strategically right, not a concession. It is the top of the funnel
for a $120 object and for alirahman.com/apocalypse-tapestry. Give it away properly — well
made, not a flattened PDF.

---

## 3. Physical specification

### 3.1 Premium edition (offset)

```
Trim              304 × 229 mm (12 × 9 in), landscape
Bleed             3 mm all edges
Extent            328 pp + endpapers
Text stock        150 gsm matt coated art, FSC-certified, low blue-white
Plate sections    170 gsm, same shade — optional, for the 39 full-bleed plates
Endpapers         140 gsm uncoated, solid Carmin (your border red)
Binding           Section-sewn, 16 pp signatures, exposed spine with visible
                  head/tail bands — Swiss-bound if budget allows
Case              Cloth over 3 mm greyboard, no jacket
Blocking          Gold foil, front and spine; blind deboss for the frame rule
Printing          4/4 process; consider 5th unit for a spot metallic on the
                  reader panels only
Finishing         Matt machine varnish overall; spot gloss UV on plates only
Head/tail bands   Carmin and gold
Ribbon            One, carmin
```

**On no jacket:** a jacket on an exposed-spine book is a contradiction. Print on the cloth.
It costs less and reads as more confident.

**Weight and freight.** At this trim and extent you are looking at roughly 2.2–2.6 kg.
That is a real number for Kickstarter shipping — budget it before you set a pledge tier,
not after. It is the single most common way art-book campaigns lose their margin.

### 3.2 Trade / POD edition

**Important conflict to resolve.** 12 × 9 in landscape is not a standard print-on-demand
trim. IngramSpark's custom trim options do not reliably cover it, and their hardcover
colour offering is built around portrait sizes. Two workable answers:

1. **IngramSpark at 11 × 8.5 in landscape**, casebound, *premium colour*, white stock.
   Best distribution — it puts you in the Ingram catalogue, which is how bookstores and
   libraries order. Verify the trim against their current spec sheet before you lay out.
2. **Blurb at 13 × 11 in landscape**, ProLine pearl or uncoated. Materially better and
   closer to the premium scale, but weak distribution and higher unit cost.

Recommendation: **IngramSpark 11 × 8.5 landscape for distribution, Blurb 13 × 11 for the
copies you hand to publishers and press.** Two masters, one grid.

Use **premium or ultra-premium colour**, never standard. On standard colour these plates
will go muddy and the golds will turn green. Order a physical proof before you list, and
expect the first one to come back too pale — POD presses under-ink relative to an offset
proof, and the usual fix is a global +8–12% contrast and a slight black-point lift on the
plate files only.

### 3.3 Colour management

Everything you have is sRGB screen output. That has to be dealt with deliberately or the
book will disappoint you in a way that is expensive to fix.

- Convert plates to **CMYK with a profile matched to the stock** —
  `PSO Coated v3` (FOGRA51) for coated offset, `GRACoL 2013` for US.
  POD vendors publish their own; use theirs when supplied.
- **Rendering intent: Perceptual** for these images, not Relative Colorimetric. There is
  a lot of saturated gold and deep shadow, and you want smooth compression, not clipping.
- Your two brand colours are the ones most at risk. **Carmin and Bleu roi both sit outside
  CMYK gamut.** Specify them as **Pantone spot colours** for endpapers, foil and cover, and
  accept the CMYK approximation inside the plates. Do not try to match them in process ink.
- Total ink limit 300% coated, 260% uncoated. Several of these plates have very dense
  shadow areas and will exceed that on conversion.
- **Soft-proof every plate before signing off.** Budget a wet proof of eight
  representative plates on the actual stock. It costs a few hundred dollars and it is the
  difference between a good book and an expensive regret.

---

## 4. Design system

### 4.1 Grid — 12 × 9 in

```
Outer margin      19 mm (0.75 in)
Head              18 mm (0.70 in)
Foot              22 mm (0.85 in)     — deeper foot, holds the folio
Gutter            23 mm (0.90 in)     — landscape books need more; the sewn
                                        spine is stiff and steals inner margin
Baseline          14 pt
Columns           12-column, 4 mm gutters
Plate frame       0.5 pt rule, #9E8F72, on framed plates only
```

Three plate treatments, alternating to control rhythm:

1. **Full-bleed** — image to all four edges, caption reversed out of a bottom scrim.
   Reserved for the 39 spread-capable plates. Never more than two consecutively.
2. **Plate + scripture** — image occupies 7.05 in of the page width, text column 4.95 in.
   The workhorse. Anchor verses, plate data, author's note.
3. **Diptych** — two 16:9 plates side by side with footnotes below. Use to accelerate
   through sequences like the four horsemen or the seven vials.

### 4.2 Typography

| Role | Face | Size / leading |
|---|---|---|
| Movement titles | Cinzel SemiBold | 33 pt / 38 pt, +55 tracking |
| Plate titles | Cinzel SemiBold | 16.5 pt / 20 pt |
| Scripture | EB Garamond Regular | 10.6 pt / 18.7 pt, justified |
| Verse numbers | Space Grotesk Medium | 5.6 pt, superior, Carmin |
| Author's notes | Cormorant Garamond Italic | 10.4 pt / 16.2 pt |
| Apparatus / IDs | Space Grotesk Medium | 6.2 pt, +0.22 em, uppercase |
| Folios | Space Grotesk | 6.4 pt, +0.18 em |

All four are open-licence (SIL OFL), so there is no licensing cost and no barrier to a
publisher picking the files up. If you want to spend money on exactly one upgrade, buy a
licensed text face with a true small-caps and old-style-figure set — Arno Pro, Lyon Text,
or Freight Text — and keep Cinzel and Space Grotesk. That is the only paid font that would
visibly improve the book.

### 4.3 Palette

```
Vellum      #EAE1CE    page ground
Ink         #16120E    warm near-black — never pure black
Ink soft    #3B322A    secondary text
Carmin      #8E2420    rubrication, narrative border system     → Pantone 1805 C
Bleu roi    #1E3566    reader panels, status chips               → Pantone 288 C
Gold        #A8823C    fragment status, accents                  → foil, not ink
Rule        #C3B597    hairlines
```

Never set text in pure black on this ground. The warm near-black is what makes the page
read as vellum rather than as paper.

---

## 5. Book architecture

```
FRONT MATTER                                                         pp. i–xxiv
  Half-title
  Frontispiece — T1-00, full bleed
  Title spread
  Copyright / rights statement
  Contents — the six movements
  Foreword                                     ~1,200 words, commissioned
  Note on the Angers cycle and its losses      ~1,800 words, yours
  Note on method — style contract, LUT system,
     viewer-space coordinates, the reconstruction rule    ~1,500 words, yours

THE SIX MOVEMENTS                                                    pp. 1–260
  For each movement:
    Movement opener        reader panel + argument + survival tally + register list
    15 plates              full-bleed / plate+scripture / diptych, alternating
    Movement coda          one page, the closing image and what it turns on

THE TEXT                                                           pp. 261–300
  The Revelation to John, complete, World English Bible
  Two columns, 9.5/14, plate cross-references in the margin

APPARATUS                                                          pp. 301–326
  The Register of Losses — all 90 slots, status, anchor, plate page
  Concordance of Revelation references to plates
  Notes
  Bibliography
  Acknowledgements

COLOPHON                                                           pp. 327–328
```

**Extent: 328 pp.** A multiple of 16, which is what a sewn book wants. If you overrun,
cut from the back text section, not the plates.

### 5.1 What you still have to write

| Piece | Length | Note |
|---|---|---|
| Foreword | 1,200 w | Commission this. An art historian who works on Angers, or a working artist. An outside voice is what makes it a book rather than a portfolio. |
| Note on the losses | 1,800 w | Yours. The 1782 dispersal, the horse blankets, the orangery pipes, the 1848 recovery. This is the emotional argument for the whole project. |
| Note on method | 1,500 w | Yours. The style contract, the LUT system, the coordinate system. Be specific and technical — do not apologise for the method, document it. |
| Movement arguments | 6 × 250 w | Adapt from your Episode Bible. Already 80% written. |
| Movement codas | 6 × 150 w | New. |
| Plate notes | ~40 × 90 w | Not every plate. Roughly two per movement-third. These are where the book earns re-reading. |

That is around 12,000 words of new writing. It is the real remaining work, and it is the
part that cannot be automated without the book losing the thing that makes it yours.

---

## 6. Asset pipeline — what has to happen to the files

### 6.1 Current state

162 PNGs across `Tapestries/I–VI`, generated March–August 2026 on GPT Image 1.5,
Gemini 3 / Nano Banana Pro, Gemini 3.1 Flash and ChatGPT Images 2.0. Filenames are raw
model exports with version suffixes and ` 1.png` duplicates. **Nothing maps a file to a
slot except the geometry of your Obsidian canvases.**

I have resolved that. Reading each `*.canvas`, the two seven-wide registers sort by
position into exactly the top and bottom rows of each tapestry. That produced a clean
90-slot mapping, delivered as `PLATE_MANIFEST.csv` / `.json`.

### 6.2 Findings

**Resolution is better than the README implied.** Against a 12 × 9 page:

| Grade | Count | Sizes | Capability |
|---|---|---|---|
| Spread-capable | 39 | 5056×3392, 5504×3072 | 16.9–18.3 in at 300 ppi |
| Full-page | 40 | 3840×2160 | 12.8 in at 300 ppi |
| **Sub-resolution** | **11** | 1536×1024, 1024×1536 | **5.1 in — cannot hold a plate** |

**The 11 to regenerate:**

```
T1-00   Saint John reading the Apocalypse              1024×1536
T1-T01  Seven churches of Asia                         1536×1024
T1-T02  Vision of the Seven Candlesticks               1536×1024
T1-B01  First Horseman                                 1536×1024
T1-B03  Third Horseman                                 1536×1024
T2-00   Saint John reading (Second Vision)             1024×1536
T2-T04  Angel empty the incense                        1536×1024
T3-00   Saint John reading (Third Vision)              1024×1536
T4-00   Saint John reading (Fourth Vision)             1024×1536
T5-00   Saint John reading (Fifth Vision)              1024×1536
T6-00   Saint John reading (Sixth Vision)              1024×1536
```

**All six reader panels are in this list.** They are the most ceremonial pages in the book —
each one opens a movement and faces the argument text. They are also the only portrait
images in the set, so they cannot be rescued by running them small. Regenerating the six
readers as a matched set, in one session, on one model, is the highest-value single task
remaining. Do them together or they will not match each other.

**Aspect ratio is split and it will show.** Among the 84 narrative plates: 66 at ~16:9
(1.778 / 1.792) and 18 at ~3:2 (1.491 / 1.499 / 1.5). In a book where every plate sits in
the same frame, a 20% difference in proportion reads as sloppiness even to someone who
cannot name what is wrong. **Standardise on 16:9** — it is the majority, and it is the
ratio that fits a 12 × 9 page. Outpaint the 18 outliers rather than cropping them; you
lose composition either way, but outpainting loses less.

**Two master indexes disagree, and it would have put wrong captions under your plates.**
`INDEX/Master Index.md` in the vault and `MASTER_INDEX_v3.json` in the project diverge
across Movement III. The vault version drops *Measuring the Temple* (whose anchor duplicated
the reader panel's) and adds *Mark of the Beast* at T3-B07, which shifts every slot from
T3-T05 onward by one. The vault version is internally consistent — its Revelation anchors
run in strict order from 11:3 to 13:18 — so **the vault file is canonical and the project
JSON is stale.** I have built the manifest on the vault version. The project copy should be
deleted or replaced so this cannot resurface.

**Text artefacts in at least one plate.** T6-T03, *Christ on the White Horse*, has garbled
pseudo-Latin in the open book at lower left — `IOC SAPIENTU EST QUI MARETINIULECTUM`. At
18 inches across a spread this will be conspicuous and will read as a defect to a reviewer
or an acquisitions editor. Sweep all 90 at full size for legible text before layout; inpaint
or regenerate any that carry it. This is a fast pass and it protects the book's credibility.

### 6.3 The pipeline to build

```
1  Rename       manifest → T{n}-{ROW}{NN}.png, canonical, one file per slot
2  QC           full-size sweep for text artefacts, hands, border bleed
3  Normalise    all narrative plates to 16:9 by outpainting the 18 outliers
4  Regenerate   the 11 sub-resolution plates, readers as one matched set
5  Master       16-bit TIFF, sRGB, archival, untouched
6  Print        CMYK per profile, 300 ppi at placed size, ink limit applied
7  Web/ebook    sRGB JPEG, long edge 2400 px, q88
8  Vector       optional, per the original README plan, for the deck
```

Steps 1 and 5 are worth doing before anything else. Right now a single accidental
file rename in that vault would cost you the ability to reconstruct which image belongs to
which slot, and the canvases are the only thing standing between you and that.

---

## 7. Ebook specification

Two different files. There is no single format that is good on both an iPad and a Kindle.

### 7.1 iPad / Apple Books — fixed-layout EPUB 3

```
Viewport          2732 × 2048 px (landscape, 4:3 — matches iPad Pro natively)
Spread mode       rendition:spread-landscape, rendition:layout pre-paginated
Images            long edge 2400 px, JPEG q88, sRGB
Fonts             embedded, subset — Cinzel, EB Garamond, Space Grotesk
Nav               full EPUB 3 nav doc, one entry per movement and per plate
Accessibility     alt text on every plate — use the title + anchor + status line;
                  this is also what Apple's store surfaces
Target size       under 300 MB
```

Fixed layout is correct here. The whole point is that the typography and the plate sit in
a designed relationship, and reflowable throws that away.

### 7.2 Kindle

Kindle's fixed-layout support is real but narrower, and most of your readers will be on
phones and small tablets where a 12 × 9 landscape spread is unreadable. Ship **two files**:

- **Fixed-layout KPF** via Kindle Create, landscape, for tablets and Kindle apps.
- **Reflowable EPUB** as the fallback: one plate per screen, full width, followed by its
  anchor verses, then the note. Loses the spread but stays readable at 5 inches. This is
  the version most people will actually read.

Do not attempt a single file that serves both. It will be bad at both.

### 7.3 PDF

Also ship a screen PDF — RGB, 150 ppi, hyperlinked contents, under 80 MB. It is what
people will actually pass around, and it is the version that ends up in front of a
publisher. Make it good.

---

## 8. Publishing path

### Now — POD

1. Fix the pipeline (§6.3 steps 1–5). Nothing else can start until the files are canonical.
2. Regenerate the 11. Readers as one matched set.
3. Lay out to the 11 × 8.5 in IngramSpark master.
4. Order a physical proof. Expect it to come back pale; correct and re-proof.
5. Buy your own ISBNs — do not use a free vendor ISBN. It makes you the publisher of
   record, which matters if you later want to license to Taschen or Phaidon.
6. List, and ship the free ebook at the same moment.

### Later — offset

The POD edition's job is to prove demand and to be the physical object you put in front of
people. Once it has, the offset route is:

- **Kickstarter**, which is where premium art books are funded now. Target 500–1500 units.
  Pledge tiers at $95 (book), $150 (book + signed print), $400 (book + original-size
  plate). Model shipping *first*.
- **Printers.** For this spec: Ofset Yapımevi (Istanbul), Die Keure (Belgium),
  Graphius (Belgium), or Artron / Toppan for Asia. All four do museum-catalogue work and
  will quote from this document. Ask for a paper dummy before you commit.
- **Or license it.** With a finished POD edition, a sample, and this spec, you have a real
  submission. DelMonico, Rizzoli, Prestel and Thames & Hudson all publish exactly this
  kind of book. You would trade margin for reach and for a production department that
  knows how to do a Swiss binding properly.

---

## 9. Rights

- **Scripture** — World English Bible, public domain. No permission needed, no royalty.
  Credit it on the copyright page and in the colophon.
- **Plates** — © Ali Rahman / Divergent World. You currently license them CC BY-SA 4.0.
  **Think hard about this before the print edition.** BY-SA lets anyone print and sell
  this book, provided they attribute and share alike. That is a fine choice for the web
  gallery and a difficult one for a $120 object you intend to be the sole source of. A
  common split: **CC BY-NC-SA for the web and the free ebook, all rights reserved for the
  print edition.** You can do this; you are the rights holder and the licences are yours
  to set per-edition. Just do it deliberately.
- **The Angers cycle itself** is long out of copyright. Photographs of it are not —
  if you reproduce any reference photograph, clear it or replace it.
- **AI disclosure.** State the method plainly on the copyright page and in the note on
  method. It is honest, it is increasingly expected, and in this project it is a
  strength — the method *is* the argument. Burying it would be the only version of this
  that reads badly.

---

## 10. Open questions

1. **Who writes the foreword?** Commission early; it has the longest lead time of anything
   in the book.
2. **CC BY-SA on the print edition** — decide before you list.
3. **Tapestry VII.** There is a seventh folder in the vault with a cover image and a
   28 KB document, and nothing else. Is it a planned expansion, an appendix, or dead?
   It should not silently become a loose end at layout.
4. **The historical web preview** — this was unavailable during the original planning
   pass. The current publishing workflow uses archive-local files and does not depend on
   that retired preview environment.

---

## Appendix — files delivered

| File | What it is |
|---|---|
| `REVELATION_sample_spreads.pdf` | Eight designed pages at final trim, using your plates |
| `PLATE_MANIFEST.csv` / `.json` | 90 slots → source file, dimensions, aspect, print grade |
| `_book-build/dims.json` | Dimensions of all 165 images in the vault |
| `spreads.html` | The layout source; the design system as working code |
