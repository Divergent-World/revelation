# REVELATION designed-book builders

These scripts read canonical content, artwork, fonts, and publishing sources from the root of the repository or extracted master archive. No copied JSON, local web server, R2 bucket, or machine-specific path is required.

## Build commands

Run from the archive root:

```bash
python3 publishing/book-source/build.py
python3 publishing/book-source/render.py
python3 publishing/book-source/render_pages.py 2048
python3 publishing/book-source/make_epub_fixed.py build/epub_pages
python3 publishing/book-source/make_epub_reflow.py
```

Outputs appear under `build/`:

- `book.html`
- `REVELATION_web.pdf`
- `epub_pages/*.jpg`
- `REVELATION_iPad_fixed.epub`
- `REVELATION_reflowable.epub`

The scripts derive the archive root from their own location. `REVELATION_ROOT` is an optional development/testing override; normal archive use does not need it.

## Prerequisites

- Python 3
- Playwright for Python with Chromium installed
- Pillow

Install the Python packages in your preferred virtual environment, then install Playwright's Chromium browser. The builders intentionally do not vendor these general-purpose runtimes.

## Source map

- Canonical JSON: `content/`
- Designed-book JPEGs: `artwork/book-images/`
- Original artwork: `artwork/originals/`
- Fonts and IDML: `publishing/indesign/`
- Editorial prose and layout logic: this directory

Plate pacing is controlled by `build.py`; typography and page treatments are in `theme.css`; flowing pagination is in `paginate.js`. Red-letter words of Christ come from the canonical `wordsOfJesus` ranges.
