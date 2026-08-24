# REVELATION — Build Plan

How the 90 plates and the complete text of Revelation become a finished ebook and a
collector's-edition print book. What software, what it costs, what order.

Version 1.0 · 14 August 2026 · supersedes §3.2 and §6.2 of the Production Bible

---

## 0. Correction first

**I got the master index backwards last turn, and you should know before you act on it.**

I told you the vault's `INDEX/Master Index.md` was canonical and the project's
`MASTER_INDEX_v3.json` was stale. That was the wrong way round. I reasoned from the fact
that the vault version's Revelation anchors run in unbroken order, which looked like the
corrected file. It isn't.

The images settle it. `T3-T07` is assigned the same source file in both my manifest and
your repo. The vault index calls it *Saint Michael and the dragon*. Your repo calls it
*Woman and the dragon*. **The plate shows a crowned woman clothed with the sun, holding a
child, on a cloud, above a seven-headed dragon.** That is Revelation 12:1–6. Your repo is
right.

The scope is larger than Movement III: **29 of the 90 slots disagree**, in Movements I, II
and III, and in each case the vault file is shifted one position late.

| | |
|---|---|
| **Canonical** | `content/scene-metadata.json` + `content/source-map.json` in the repo |
| **Stale — do not use** | `Apocalypse Tapestry/INDEX/Master Index.md` |
| **Also stale** | `MASTER_INDEX_v3.json` in the Claude project (same content as the repo, but a second copy) |
| **My `PLATE_MANIFEST.csv`** | File→slot mapping is correct. **Title and anchor columns are wrong for 29 rows.** Use the repo's. |

Nothing shipped is broken — your site and your `export.md` both read from the repo, so
they have been correct all along. The vault file is the odd one out. Rename it
`Master Index (SUPERSEDED).md` so this cannot happen again.

---

## 1. The short answer on software

**Not Canva. Not Google Docs. Not InDesign. Your repo.**

You already built the thing that makes this book possible, and you built it correctly:

- `content/tapestries.json` — the manifest, 90 scenes with movement structure
- `content/scene-metadata.json` — titles and anchors
- `content/source-map.json` — slot → vault file, with SHA-256 checksums
- `content/revelation.web.json` — all 22 chapters, verse-per-line, **with words-of-Jesus
  ranges derived from official USFM `\wj` markers**
- `scripts/build-release.mjs` — checksum-verified derivative pipeline

That last point is worth dwelling on. You have red-letter data at verse-range precision,
tied to a public-domain text, tied to a checksummed image set. **No page-layout program can
consume that.** In Canva or InDesign you would be hand-placing 90 images and 404 verses,
and every correction — a regenerated plate, a retitled scene — would be manual, in two
places, forever.

In the repo it is a data change and a rebuild.

### Why each alternative fails

| Tool | Why not |
|---|---|
| **Canva** | Not a book tool. No text flow across pages, no master pages, no facing-page spreads, no reliable CMYK or PDF/X, and it degrades badly past ~100 pages with large images. There is no EPUB export at all. You would rebuild by hand and still have no ebook. |
| **Google Docs** | Will open your Pandoc DOCX and let you edit the words — genuinely useful for *drafting the foreword and notes*. But it cannot typeset an art book. No bleed, no facing pages, no image control, no colour management. Its PDF export is not printable at this level. |
| **Adobe InDesign** | Actually capable, and the right answer if you were hand-designing 328 unique pages. $23/mo, steep curve. Its real advantage is that publishers want INDD. Its real cost is that it breaks the link to your JSON — you'd be maintaining the book and the site as two separate products. **Keep this in reserve for a publisher handoff, not for v1.** |
| **Pandoc alone** (your current `docs/book-export.md`) | Correct for the *reading* ebook and already working. But Pandoc's DOCX and default EPUB have no design system — no grid, no plate treatment, no apparatus. It gets you a good book of the text. It cannot get you a $250 object. |

### What to build instead

One new build target in the repo — `npm run book:build` — that reads the same content JSON
and emits **three artefacts from one source**:

```
content/*.json  ─┐
book/*.md       ─┼─▶  book/build.mjs  ─┬─▶  print/REVELATION-print.pdf   (PDF/X, bleed, crops)
book/theme.css  ─┘                     ├─▶  ebook/REVELATION.epub        (fixed-layout EPUB 3)
                                       └─▶  ebook/REVELATION-reflow.epub (Kindle fallback)
```

The renderer is Chromium via Playwright — **which you already have in the repo** as a
Playwright dev dependency for your e2e tests. The `spreads.html` I sent you is the working
prototype of the print profile: it produced a real 12 × 9 in PDF with your plates, correct
trim, embedded fonts. Scaling it from 8 pages to 328 is a loop, not a redesign.

**Where you edit what:**

| You want to change | You edit |
|---|---|
| Foreword, notes on method, plate notes, codas | `book/front-matter/*.md`, `book/notes/*.md` — plain Markdown |
| Which plate is in which slot | `content/source-map.json` |
| A title or anchor | `content/scene-metadata.json` |
| Typography, grid, colour, plate treatments | `book/theme.css` |
| Page order, section structure | `book/structure.json` |

All of it plain text, all of it in git, all of it reversible. You never open a layout app.

---

## 2. The two products are genuinely different

You said the print version should differ from the ebook. Here is the split, and it is
forced by a hard constraint I found (§4).

| | **Ebook** | **Collector's print edition** |
|---|---|---|
| Complete WEB Revelation, all 22 chapters | ✅ Yes — this is its job | ❌ No |
| 90 plates | ✅ All | ✅ All |
| Anchor verses beside each plate | ✅ | ✅ |
| Red-letter words of Jesus | ✅ | ✅ in anchors only |
| Foreword, notes on method, plate notes | ✅ | ✅ expanded |
| Register of Losses, concordance | ✅ | ✅ |
| Extent | ~410 screens | **232 pages** |
| Price | Free | $200–300 |

The ebook carries the whole Bible text. The print edition carries the *art* — plates,
anchors, apparatus, and your writing — and points to the free ebook for the complete text.
This is a stronger book, not a compromised one. A 328-page art book where 40 pages are
solid two-column scripture is a book with a dead zone in the back.

---

## 3. The blocker in your current pipeline

`scripts/build-release.mjs` line 60:

```js
sharp(input).resize({ width: Math.min(1920, metadata.width) …}).jpeg({ quality: 88 })
  .toFile(book);
```

Your **"book-safe" JPEGs are capped at 1920 px**. That is 6.4 inches at 300 ppi. It is a
web derivative wearing the word "book." If you build the print edition off
`dist/releases/v1/book/images/`, every plate in the collector's edition maxes out at
6.4 inches on a 13-inch page.

**Fix:** add a fourth derivative track. Roughly twenty lines in the same loop:

```js
mkdir(path.join(releaseRoot, "print"), { recursive: true }),
…
sharp(input)
  .resize({ width: Math.min(5600, metadata.width), withoutEnlargement: true })
  .withMetadata({ density: 300 })
  .jpeg({ quality: 95, mozjpeg: true, chromaSubsampling: "4:4:4" })
  .toFile(printOut),
```

No chroma subsampling and q95 — the 88/4:2:0 you use for web will show as colour fringing
on gold edges at print size. Keep `originals/` as the archival master; `print/` is the
placement copy.

Also: `print/` must be gitignored and must **not** go to R2 with a public URL. Your web
assets are CC BY-SA. The print masters are the thing you are selling.

---

## 4. The constraint that shapes the print edition

**Blurb caps premium papers at 240 pages.** Verified on their current specs:

| Paper | Max pages |
|---|---|
| Standard 80# Semi-Matte, 118 gsm | 440 |
| Premium Lustre / Matte, 148 gsm | 240 |
| Mohawk Superfine Eggshell uncoated, 148 gsm | 240 |
| Mohawk proPhoto Pearl, 190 gsm | 240 |
| Layflat | 110 |

A 328-page book on Blurb must run on 118 gsm standard stock. On a $250 art book that paper
is disqualifying — it is thin, it shows through, and it will not hold these shadows.

Three ways out, in order of preference:

**A. Trim to 232 pages and use Mohawk.** Drop the complete-text section to the ebook.
This is the recommendation. 232 pp on Mohawk Superfine Eggshell at 13 × 11 in landscape is
a genuinely beautiful object, and uncoated eggshell suits a manuscript book far better than
a gloss photo paper.

**B. Two volumes in a slipcase.** Volume I: Movements I–III. Volume II: Movements IV–VI.
~150 pp each, both on Mohawk, complete text included in Volume II's back matter. This is
the most collectible version and the easiest to justify at $300. It roughly doubles unit
cost and the slipcase has to be sourced separately — Blurb does not make one.

**C. Go straight to offset.** Removes every constraint, needs 500+ units and $15–25k up
front. This is the Kickstarter path from the Production Bible. Right eventually, wrong now.

Take A for the first edition. It is one decision — move the scripture section to the ebook
— and everything else falls into place.

---

## 5. Where to print, and what it costs

### The collector's edition — Blurb

13 × 11 in landscape, ImageWrap or Linen hardcover, Mohawk Superfine Eggshell, 232 pp.

Blurb publishes prices through a calculator rather than a rate card, so **run
blurb.com/pricing against the real page count before you commit**. Based on their
structure — base price plus per-page, with a premium-paper uplift — expect **$115–165 unit
cost** at this size, extent and stock. That supports a $250–300 retail price with a real
margin, and it is exactly the price band *Figures of Speech* and *Nike. ICONS* proved at $80
for a mass-produced offset book. You are selling a short-run object; the premium is
defensible.

Order **one proof before anything else.** Expect it to come back flatter and paler than
your screen. The standard correction is +8–12% contrast and a slight black-point lift on
the plate files only — never on the type. Budget two proof rounds and about three weeks.

### The trade edition — IngramSpark

11 × 8.5 in landscape casebound, premium colour, ~232 pp, retail $55–70. This is the one
that gets an ISBN into the Ingram catalogue so bookstores and libraries can order it. Much
lower unit cost, noticeably lower quality. Its job is reach, not beauty.

Buy your own ISBNs — one per format, so three or four. Do not take a free vendor ISBN; it
makes the vendor the publisher of record, which will complicate any later licensing deal.

### The ebook — free

EPUB 3 fixed-layout on Apple Books, reflowable EPUB on Kindle, plus a screen PDF from your
own site. Zero marginal cost. It is the funnel for the $250 object and for
alirahman.com/apocalypse-tapestry.

### Indicative first-edition economics

| | |
|---|---|
| Proofs (2 rounds, both editions) | $300–450 |
| ISBNs (block of 10) | ~$300 |
| Foreword commission | $500–2,000 |
| Fonts (optional text-face licence) | $0–400 |
| **Setup total** | **~$1,100–3,150** |
| Collector's unit cost | $115–165 |
| Collector's retail | $250–300 |
| **Margin per collector's copy** | **~$90–170** |

Break-even lands somewhere around 20–30 collector's copies. That is a reachable number
from your own audience before you ever run a campaign.

---

## 6. The writing you still owe

The build is mechanical. This is not, and it is the part that decides whether the book is
any good.

| Piece | Words | Where it lives |
|---|---|---|
| Foreword | 1,200 | `book/front-matter/foreword.md` — **commission now**, longest lead time |
| Note on the Angers cycle and its losses | 1,800 | `book/front-matter/losses.md` |
| Note on method | 1,500 | `book/front-matter/method.md` |
| Movement arguments (6) | 1,500 | already in `tapestries.json` — adapt, don't rewrite |
| Movement codas (6) | 900 | `book/movements/*.coda.md` |
| Plate notes (~40) | 3,600 | `book/notes/T{n}-{slot}.md` |
| Colophon, rights, acknowledgements | 600 | `book/back-matter/` |

~11,000 words of new writing. Draft it in Google Docs if that is comfortable — that is
what Docs is *good* at — and paste into the Markdown files. The build picks them up.

**On the foreword:** commission an art historian who works on Angers or on medieval
textiles, or a working artist. An outside voice is the difference between a book and a
portfolio, and it is the first thing an acquisitions editor looks for.

---

## 7. Build order

**Phase 1 — unblock (this week)**

1. Rename the vault's `Master Index.md` to `(SUPERSEDED)`. Delete the stale copy from the
   Claude project. One canonical source: the repo.
2. Add the `print/` derivative track to `build-release.mjs` (§3).
3. Regenerate the 11 sub-resolution plates. **The six reader panels in one session, on one
   model** — they open the six movements and face each other across the book; if they don't
   match, nothing else will save them.
4. Sweep all 90 at full size for legible text artefacts. T6-T03 has garbled pseudo-Latin
   in the open book at lower left. At 13 inches that reads as a defect.
5. Normalise the 18 off-ratio plates to 16:9 by outpainting.

**Phase 2 — the book target (next)**

6. `book/` directory, `structure.json`, `theme.css` seeded from `spreads.html`.
7. `book:build` print profile → full 232-page PDF.
8. `book:build` ebook profiles → fixed-layout and reflowable EPUB.
9. Wire into `npm run build` so the site, the book and the ebook stay in lockstep.

**Phase 3 — proof and ship**

10. Blurb proof. Correct. Second proof.
11. ISBNs, metadata, listings.
12. Ship the free ebook and the collector's edition the same day.

**Phase 4 — offset**

13. Kickstarter, or a submission package to DelMonico / Rizzoli / Prestel / Thames & Hudson.

---

## 8. What I need from you

1. **Confirm Option A** — trim the print edition to 232 pp and move the complete scripture
   text to the ebook only. Everything in Phase 2 depends on it.
2. **Confirm I should build the `book/` target in the repo** rather than hand you an
   InDesign route. If yes I'll write it against your existing content JSON and open it as a
   branch you can review.
3. **The CC BY-SA question from the Production Bible is still open**, and it matters more
   now that there is a $250 edition. BY-SA permits anyone to print and sell this book. Web
   and ebook under BY-NC-SA, print edition all-rights-reserved, is the usual split.
4. **Tapestry VII** — the seventh vault folder with a cover image and a 28 KB document.
   Expansion, appendix, or dead? It should not surface as a loose end mid-layout.
