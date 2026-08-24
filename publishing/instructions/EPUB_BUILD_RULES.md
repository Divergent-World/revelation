# EPUB build rules — REVELATION

Standing rules for rebuilding the two EPUB editions in the master archive.

---

## Always build two EPUBs. Never one.

**Do not attempt a fixed-layout EPUB with live text.** It cannot match the PDF and it will
look broken. This book's design depends on justified text, automatic hyphenation,
multi-column boxes, letter-spacing on 51 CSS rules, `::first-letter` drop caps, and
`overflow:hidden` page boxes. No two reading engines agree on any of those. One word
hyphenating differently reflows a column, and the hidden overflow then clips it mid-line.
This was tried and it failed; do not retry it.

| Edition | What it is | For |
|---|---|---|
| `REVELATION_iPad_fixed.epub` | Every page rendered as a JPEG | Apple Books, tablets |
| `REVELATION_reflowable.epub` | Real text generated from the content JSON | Phones, Kindle |

---

## Fixed-layout edition — page images

From the extracted archive root, build with:

```bash
python3 publishing/book-source/build.py
python3 publishing/book-source/render_pages.py 2048
python3 publishing/book-source/make_epub_fixed.py build/epub_pages
python3 publishing/book-source/validate_epub.py build/REVELATION_iPad_fixed.epub fixed
```

- Render each `.page` element from `book.html` **after the paginator has run** — wait for
  `document.documentElement.getAttribute('data-ready') === '1'`.
- 2048 px wide (≈170 ppi across a 12 in page) for the archive master.
  1560 px if the file has to clear a 30 MB limit.
- JPEG, progressive, optimized. Quality by page type: **~76 for plate pages, ~88 for pages
  that are mostly type** — text needs the quality, photographs do not.
- One XHTML per page containing only `<img>`, with
  `<meta name="viewport" content="width=W, height=H"/>` matching the image pixel size.
- OPF metadata: `rendition:layout` = `pre-paginated`, `rendition:orientation` = `landscape`,
  `rendition:spread` = `both`.
- Spine: page 1 `rendition:page-spread-center`, then odd = `right`, even = `left`.
- Page 1's image carries `properties="cover-image"`.
- Nav is built by reading the live DOM for movement openers, part dividers and section
  headings — not hand-maintained.

## Reflowable edition — real text

From the extracted archive root, build with:

```bash
python3 publishing/book-source/make_epub_reflow.py
python3 publishing/book-source/validate_epub.py build/REVELATION_reflowable.epub reflowable
```

- Generate from `content/*.json` and `prose.py` directly. **Never** from the paginated DOM.
- One XHTML per section: cover, title, copyright, foreword, the two notes, one per movement,
  one per Revelation chapter, register, colophon, back cover.
- Embed EB Garamond (regular/italic/semibold), Cinzel SemiBold, Space Grotesk Medium.
- Keep the red letters: `wordsOfJesus` character ranges become `<span class="wj">`.
- Verse numbers are `<span class="v">`, superscript, rubric red.
- Plates are `<figure>` at `width:100%` with the caption carrying slot id, title, anchor and
  the SURVIVES / FRAGMENT / RECONSTRUCTED chip.
- Set `-webkit-text-size-adjust:100%` and `text-size-adjust:100%`.
- Full anchor scripture, not the truncated print version.

## Both editions

- `mimetype` must be the **first** zip entry and **stored uncompressed**.
- EPUB 3, `nav.xhtml` with `epub:type="toc"` plus a hidden `landmarks` nav.
- Declare a `cover-image` and a `<meta name="cover">`.
- Include `dcterms:modified`, rights naming the WEB scripture as public domain.

## Validate before shipping

1. `mimetype` first and stored.
2. Every `.xhtml` and `.opf` parses as XML.
3. Every manifest `href` resolves to a file in the archive.
4. Every spine `idref` resolves to a manifest `id`.
5. Fixed edition: spread properties present on all itemrefs.
6. Reflowable: `class="wj"` spans actually present in the chapter files.

The complete commands above passed with Python 3.14.7, Playwright for Python 1.62.0, Pillow 12.3.0, and Playwright Chromium. The verified outputs were `build/REVELATION_iPad_fixed.epub` (182 page images, 20 navigation entries, 30.1 MB at 1560 px) and `build/REVELATION_reflowable.epub` (37 documents, 13 navigation entries, 41.2 MB).

If Python cannot import `playwright` or `PIL`, create and activate a virtual environment and run:

```bash
python3 -m pip install playwright Pillow
python3 -m playwright install chromium
```

If Chromium reports `TargetClosedError` inside a restricted execution sandbox, run the build in a normal terminal or grant that environment permission to launch the local browser.

## Size limits

Chat upload caps at 30 MB and the device bridge at 20 MB per file. The full-resolution
fixed EPUB can exceed either limit — deliver the 1560 px version and note that the master
can be rebuilt locally with the supplied scripts.
