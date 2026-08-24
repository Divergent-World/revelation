# Self-Contained Publishing Export Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and publish one portable `REVELATION-master-v1.zip` containing the official editions, canonical content, artwork, instructions, book generators, and editable InDesign sources, with every project path resolving inside the extracted archive.

**Architecture:** Consolidate tracked publishing sources under `publishing/` while keeping finished editions and INDD binaries locally staged but Git-ignored. Extend the pure Markdown renderer and release builder with an explicit bundle mode that writes relative artwork paths, then validate the ZIP after extraction in an arbitrary temporary directory. Keep the existing Next.js static `/export.md` route and v1 artwork objects for compatibility while making the master ZIP, Blurb preview, and GitHub source the three primary homepage actions.

**Tech Stack:** Next.js 16.3 static export, React 19, TypeScript 5.9, Node.js 22 test runner and standard library, Python 3 standard library plus Pillow and Playwright, Pandoc, WeasyPrint, Poppler `pdfinfo`, Adobe IDML/INDD, ZIP, Cloudflare R2 through the existing AWS S3 SDK.

**Spec:** `docs/superpowers/specs/2026-08-22-self-contained-publishing-export-design.md`

## Global Constraints

- The only public finished PDF is the 182-page `REVELATION_web.pdf` staged from `New Info/versions/`.
- Never commit, upload, or package either 180-page PDF.
- `/book/` remains ignored.
- Finished PDF, EPUB, DOCX, and INDD binaries remain Git-ignored but are required local inputs for the master release.
- IDML is the canonical reproducible InDesign source; INDD is a convenience artifact in the ZIP.
- The master ZIP must rebuild without R2, the website, the source vault, localhost, or machine-specific absolute paths.
- `export.md` remains scripture content only; build instructions live under `publishing/instructions/`.
- Always ship two purpose-built EPUBs: fixed-layout page images and live-text reflowable.
- Do not vendor Adobe InDesign, Pandoc, Chromium, Python, or other general-purpose runtimes.
- Preserve existing immutable `releases/v1/...` object keys and backward-compatible standalone URLs.
- Follow Next.js 16 static-export rules: the request-independent `GET` route remains statically generated during `next build`.
- Use only existing dependencies and platform standard libraries unless a failing requirement proves a new dependency necessary.

---

## File structure after implementation

### Tracked repository files

```text
publishing/
├── .gitignore
├── README.md
├── editions/README.md
├── instructions/
│   ├── PANDOC_EXPORTS.md
│   ├── EPUB_BUILD_RULES.md
│   └── INDESIGN_BUILD.md
├── reference/red-letter-reference.docx
├── book-source/
│   ├── paths.py
│   ├── test_paths.py
│   ├── validate_epub.py
│   ├── test_validate_epub.py
│   └── existing generator sources
├── indesign/
│   ├── README.md
│   ├── REVELATION_13x11.idml
│   ├── REVELATION_cover.idml
│   ├── cover_bg.jpg
│   ├── coverbg_dims.json
│   ├── linkdims.json
│   ├── linkdims_png.json
│   ├── Fonts/*.ttf
│   └── Fonts/OFL-*.txt
└── historical-book-build/
    ├── README.md
    ├── BOOK_BUILD_PLAN.md
    ├── REVELATION_Production_Bible.md
    ├── PLATE_MANIFEST.csv
    ├── dims.json
    └── spreads.html

scripts/lib/master-release.mjs
test/master-release.test.mjs
scripts/validate-master-release.mjs
```

### Local ignored inputs

```text
publishing/editions/REVELATION_web.pdf
publishing/editions/REVELATION_iPad_fixed_web.epub
publishing/editions/REVELATION_reflowable.epub
publishing/editions/revelations.docx
publishing/indesign/REVELATION_13x11.indd
publishing/indesign/REVELATION_cover.indd
publishing/indesign/REVELATION_cover.pdf
```

### Generated release output

```text
dist/releases/v1/REVELATION-master-v1.zip
```

---

### Task 1: Consolidate the publishing workspace and enforce Git boundaries

**Files:**
- Modify: `.gitignore`
- Create: `test/publishing-layout.test.mjs`
- Create: `publishing/.gitignore`
- Create: `publishing/README.md`
- Create: `publishing/editions/README.md`
- Move: `EPUB_INSTRUCTIONS.md` to `publishing/instructions/EPUB_BUILD_RULES.md`
- Copy: `public/red-letter-reference.docx` to `publishing/reference/red-letter-reference.docx`, retaining the public compatibility copy
- Copy tracked source: `New Info/REVELATION_book_source/*` to `publishing/book-source/`
- Copy tracked source: selected `New Info/REVELATION_InDesign/*` to `publishing/indesign/`
- Copy tracked history: selected `New Info/_book-build/*` to `publishing/historical-book-build/`
- Copy ignored inputs: `New Info/versions/*` and the INDD/cover PDF files to their staging paths

**Interfaces:**
- Consumes: the user-supplied `New Info` directory and the approved source/binary boundary.
- Produces: the stable repository paths consumed by every later task, plus local ignored artifacts required by Task 5.

- [ ] **Step 1: Write the failing publishing-layout test**

Create `test/publishing-layout.test.mjs`:

```js
import assert from "node:assert/strict";
import { access, readFile } from "node:fs/promises";
import test from "node:test";

const required = [
  "publishing/README.md",
  "publishing/instructions/PANDOC_EXPORTS.md",
  "publishing/instructions/EPUB_BUILD_RULES.md",
  "publishing/instructions/INDESIGN_BUILD.md",
  "publishing/reference/red-letter-reference.docx",
  "public/red-letter-reference.docx",
  "publishing/book-source/build.py",
  "publishing/book-source/make_epub_fixed.py",
  "publishing/book-source/make_epub_reflow.py",
  "publishing/indesign/REVELATION_13x11.idml",
  "publishing/indesign/REVELATION_cover.idml",
  "publishing/historical-book-build/README.md",
];

test("publishing source layout contains every tracked rebuild input", async () => {
  await Promise.all(required.map((file) => access(file)));
});

test("historical publishing notes declare canonical and excluded inputs", async () => {
  const history = await readFile("publishing/historical-book-build/README.md", "utf8");
  assert.match(history, /historical/i);
  assert.match(history, /content\/\*\.json.*canonical/i);
  assert.match(history, /180-page PDFs.*excluded/i);
});

test("public and publishing red-letter references remain byte-identical", async () => {
  const [publicReference, publishingReference] = await Promise.all([
    readFile("public/red-letter-reference.docx"),
    readFile("publishing/reference/red-letter-reference.docx"),
  ]);
  assert.deepEqual(publicReference, publishingReference);
});
```

- [ ] **Step 2: Run the focused test and confirm it fails**

Run:

```bash
rtk node --disable-warning=MODULE_TYPELESS_PACKAGE_JSON --test test/publishing-layout.test.mjs
```

Expected: FAIL because `publishing/` does not exist.

- [ ] **Step 3: Create the tracked directory structure and copy source-only material**

Use mechanical copies for the existing source files, then edit the copied READMEs with `apply_patch`:

```bash
rtk mkdir -p publishing/book-source publishing/indesign/Fonts publishing/historical-book-build publishing/instructions publishing/reference publishing/editions
rtk cp -R "/Users/alirahman/Desktop/test/new info/REVELATION_book_source/." publishing/book-source/
rtk cp "/Users/alirahman/Desktop/test/new info/REVELATION_InDesign/REVELATION_13x11.idml" publishing/indesign/
rtk cp "/Users/alirahman/Desktop/test/new info/REVELATION_InDesign/REVELATION_cover.idml" publishing/indesign/
rtk cp "/Users/alirahman/Desktop/test/new info/REVELATION_InDesign/cover_bg.jpg" publishing/indesign/
rtk cp "/Users/alirahman/Desktop/test/new info/REVELATION_InDesign/coverbg_dims.json" publishing/indesign/
rtk cp "/Users/alirahman/Desktop/test/new info/book/indesign/linkdims.json" publishing/indesign/
rtk cp "/Users/alirahman/Desktop/test/new info/book/indesign/linkdims_png.json" publishing/indesign/
rtk cp -R "/Users/alirahman/Desktop/test/new info/REVELATION_InDesign/Fonts/." publishing/indesign/Fonts/
rtk cp "/Users/alirahman/Desktop/test/new info/_book-build/BOOK_BUILD_PLAN.md" publishing/historical-book-build/
rtk cp "/Users/alirahman/Desktop/test/new info/_book-build/REVELATION_Production_Bible.md" publishing/historical-book-build/
rtk cp "/Users/alirahman/Desktop/test/new info/_book-build/PLATE_MANIFEST.csv" publishing/historical-book-build/
rtk cp "/Users/alirahman/Desktop/test/new info/_book-build/dims.json" publishing/historical-book-build/
rtk cp "/Users/alirahman/Desktop/test/new info/_book-build/spreads.html" publishing/historical-book-build/
rtk mv EPUB_INSTRUCTIONS.md publishing/instructions/EPUB_BUILD_RULES.md
rtk cp public/red-letter-reference.docx publishing/reference/red-letter-reference.docx
```

Do not copy `_book-build/*.pdf`, `_book-build/plates/`, `_book-build/preview/`, `book/_to_delete/`, or either 180-page PDF.

- [ ] **Step 4: Stage the ignored finished editions and INDD files locally**

```bash
rtk cp "/Users/alirahman/Desktop/test/new info/versions/REVELATION_web.pdf" publishing/editions/
rtk cp "/Users/alirahman/Desktop/test/new info/versions/REVELATION_iPad_fixed_web.epub" publishing/editions/
rtk cp "/Users/alirahman/Desktop/test/new info/versions/REVELATION_reflowable.epub" publishing/editions/
rtk cp "/Users/alirahman/Desktop/test/new info/versions/revelations.docx" publishing/editions/
rtk cp "/Users/alirahman/Desktop/test/new info/REVELATION_InDesign/REVELATION_13x11.indd" publishing/indesign/
rtk cp "/Users/alirahman/Desktop/test/new info/REVELATION_InDesign/REVELATION_cover.indd" publishing/indesign/
rtk cp "/Users/alirahman/Desktop/test/new info/REVELATION_InDesign/REVELATION_cover.pdf" publishing/indesign/
```

Use `rtk pdfinfo publishing/editions/REVELATION_web.pdf` and require `Pages: 182` before proceeding.

- [ ] **Step 5: Add narrow ignore rules and publishing READMEs**

Keep the approved root entry:

```gitignore
/book/
```

Create `publishing/.gitignore`:

```gitignore
editions/*
!editions/README.md
indesign/*.indd
indesign/*.pdf
book-source/book.html
book-source/epub_pages/
book-source/*.pdf
book-source/*.epub
book-source/__pycache__/
```

Create `publishing/editions/README.md` with the seven exact local staging filenames from this task. Create `publishing/README.md` explaining tracked sources versus ignored release inputs. Create `publishing/historical-book-build/README.md` with the canonicality warning required by the test.

Create initial `PANDOC_EXPORTS.md` and `INDESIGN_BUILD.md` with the approved relative archive paths and prerequisites. Copy the EPUB rules verbatim except for replacing the opening “Paste into project instructions” sentence with “Standing rules for rebuilding the two EPUB editions in the master archive.”

- [ ] **Step 6: Add the font licence notices**

Download the exact SIL Open Font License notices from the Google Fonts upstream distribution:

```bash
rtk curl -L https://raw.githubusercontent.com/google/fonts/main/ofl/cinzel/OFL.txt -o publishing/indesign/Fonts/OFL-Cinzel.txt
rtk curl -L https://raw.githubusercontent.com/google/fonts/main/ofl/cormorantgaramond/OFL.txt -o publishing/indesign/Fonts/OFL-Cormorant-Garamond.txt
rtk curl -L https://raw.githubusercontent.com/google/fonts/main/ofl/ebgaramond/OFL.txt -o publishing/indesign/Fonts/OFL-EB-Garamond.txt
rtk curl -L https://raw.githubusercontent.com/google/fonts/main/ofl/spacegrotesk/OFL.txt -o publishing/indesign/Fonts/OFL-Space-Grotesk.txt
```

The resulting paths are:

```text
publishing/indesign/Fonts/OFL-Cinzel.txt
publishing/indesign/Fonts/OFL-Cormorant-Garamond.txt
publishing/indesign/Fonts/OFL-EB-Garamond.txt
publishing/indesign/Fonts/OFL-Space-Grotesk.txt
```

Do not infer or rewrite licence wording. Verify each font family name with `rtk fc-scan publishing/indesign/Fonts/*.ttf` before assigning its notice.

- [ ] **Step 7: Verify layout, ignores, and absence of prohibited PDFs**

Run:

```bash
rtk node --disable-warning=MODULE_TYPELESS_PACKAGE_JSON --test test/publishing-layout.test.mjs
rtk git check-ignore -v book/build.py publishing/editions/REVELATION_web.pdf publishing/indesign/REVELATION_13x11.indd
rtk proxy find publishing/historical-book-build -type f -iname '*.pdf'
rtk git status --short
```

Expected: tests PASS; all three binary paths are ignored; the historical PDF search prints nothing; tracked publishing sources appear as untracked files ready to add.

- [ ] **Step 8: Commit the publishing source boundary**

```bash
rtk git add .gitignore publishing test/publishing-layout.test.mjs
rtk git commit -m "feat: consolidate publishing source workspace"
```

Before committing, use `rtk git diff --cached --name-only` to confirm that no `.indd`, finished edition, generated PDF, or 180-page PDF is staged.

---

### Task 2: Add safe relative-image mode to the Markdown renderer

**Files:**
- Modify: `lib/markdown-book.ts`
- Modify: `app/export.md/route.ts`
- Modify: `test/markdown-book.test.mjs`

**Interfaces:**
- Consumes: canonical `ScriptureChapter[]`, `Scene[]`, and either a web origin or bundle-relative image root.
- Produces: `MarkdownImageSource` and `renderMarkdownBook()` output used by the static route and Task 5's master builder.

- [ ] **Step 1: Replace test inputs with an explicit image-source union and add bundle assertions**

Update the test helper:

```js
const render = (overrides = {}) => renderMarkdownBook({
  chapters,
  scenes,
  imageSource: { kind: "web", assetBaseUrl: "https://assets.example.test" },
  ...overrides,
});
```

Add:

```js
test("renders bundle images as safe relative paths", () => {
  const markdown = render({
    imageSource: { kind: "bundle", imageRoot: "artwork/book-images" },
  });
  const images = [...markdown.matchAll(/^!\[[^\n]+\]\(([^)]+)\)/gm)].map((match) => match[1]);
  assert.equal(images.length, 90);
  assert.equal(images[0], "artwork/book-images/T1-00.jpg");
  assert.ok(images.every((image) => !image.includes("://") && !image.startsWith("/")));
});

for (const imageRoot of ["../outside", "/absolute", "file:artwork", "https://assets.test", "artwork\\book-images", "artwork/book-images?x=1", "artwork/book-images#x"]) {
  test(`rejects unsafe bundle image root ${imageRoot}`, () => {
    assert.throws(
      () => render({ imageSource: { kind: "bundle", imageRoot } }),
      /safe relative image root/,
    );
  });
}
```

Update existing web-origin rejection tests to pass `imageSource.kind = "web"`.

- [ ] **Step 2: Run the Markdown tests and confirm they fail**

```bash
rtk node --disable-warning=MODULE_TYPELESS_PACKAGE_JSON --test test/markdown-book.test.mjs
```

Expected: FAIL because `renderMarkdownBook()` still requires `assetBaseUrl`.

- [ ] **Step 3: Implement the discriminated image-source interface**

In `lib/markdown-book.ts`, define:

```ts
export type MarkdownImageSource =
  | { kind: "web"; assetBaseUrl: string }
  | { kind: "bundle"; imageRoot: string };

export type MarkdownBookInput = {
  chapters: ScriptureChapter[];
  scenes: Scene[];
  imageSource: MarkdownImageSource;
};
```

Add a bundle validator with no new dependency:

```ts
function cleanRelativeImageRoot(value: string) {
  const segments = value.split("/");
  if (
    !value || value.startsWith("/") || value.endsWith("/") ||
    value.includes("\\") || value.includes(":") || value.includes("?") || value.includes("#") ||
    segments.some((segment) => !segment || segment === "." || segment === ".." || !/^[A-Za-z0-9._-]+$/.test(segment))
  ) {
    throw new Error(`Book bundle requires a safe relative image root: ${value}`);
  }
  return segments.join("/");
}

function imageReference(source: MarkdownImageSource, sceneId: string) {
  if (source.kind === "web") {
    return new URL(`releases/v1/book/images/${sceneId}.jpg`, `${cleanOrigin(source.assetBaseUrl)}/`).href;
  }
  return `${cleanRelativeImageRoot(source.imageRoot)}/${sceneId}.jpg`;
}
```

Use `imageReference(imageSource, scene.id)` in the scene loop while preserving every existing content validation.

- [ ] **Step 4: Keep the Next.js 16 route statically exportable**

Update `app/export.md/route.ts` to call:

```ts
renderMarkdownBook({
  chapters,
  scenes,
  imageSource: {
    kind: "web",
    assetBaseUrl: process.env.NEXT_PUBLIC_ASSET_BASE_URL ?? "http://127.0.0.1:3101",
  },
});
```

Do not read the incoming `Request`; the request-independent `GET` must remain compatible with `output: "export"`.

- [ ] **Step 5: Run focused and full tests**

```bash
rtk node --disable-warning=MODULE_TYPELESS_PACKAGE_JSON --test test/markdown-book.test.mjs
rtk npm test
```

Expected: all tests PASS, including 22 chapters, 404 verses, 90 images, 90 unique scenes, and 91 red-letter ranges.

- [ ] **Step 6: Commit portable Markdown rendering**

```bash
rtk git add lib/markdown-book.ts app/export.md/route.ts test/markdown-book.test.mjs
rtk git commit -m "feat: render self-contained Markdown exports"
```

---

### Task 3: Make the designed-book source archive-relative

**Files:**
- Create: `publishing/book-source/paths.py`
- Create: `publishing/book-source/test_paths.py`
- Modify: `publishing/book-source/build.py`
- Modify: `publishing/book-source/render.py`
- Modify: `publishing/book-source/render_pages.py`
- Modify: `publishing/book-source/make_epub_fixed.py`
- Modify: `publishing/book-source/make_epub_reflow.py`
- Modify: `publishing/book-source/measure.py`
- Modify: `publishing/book-source/check_overset.py`
- Modify: `publishing/book-source/README.md`

**Interfaces:**
- Consumes: `REVELATION_ROOT` only as an optional development override; defaults to the archive/repository root derived from the source location.
- Produces: `ROOT`, `CONTENT`, `ARTWORK`, `ORIGINALS`, `PUBLISHING`, `INDESIGN`, and `BUILD` `pathlib.Path` constants used by all Python builders.

- [ ] **Step 1: Write failing path-contract tests**

Create `publishing/book-source/test_paths.py`:

```python
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent

class PathsTest(unittest.TestCase):
    def test_override_keeps_every_project_path_inside_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            code = (
                "import paths; "
                "print(paths.ROOT); print(paths.CONTENT); print(paths.ARTWORK); "
                "print(paths.ORIGINALS); print(paths.INDESIGN); print(paths.BUILD)"
            )
            result = subprocess.run(
                [sys.executable, "-c", code], cwd=HERE, text=True, capture_output=True,
                env={**os.environ, "REVELATION_ROOT": tmp}, check=True,
            )
            root = Path(tmp).resolve()
            for line in result.stdout.splitlines():
                Path(line).resolve().relative_to(root)

    def test_default_root_is_repository_root(self):
        sys.path.insert(0, str(HERE))
        import paths
        self.assertEqual(paths.ROOT, HERE.parent.parent)

if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the test and confirm it fails**

```bash
rtk python3 publishing/book-source/test_paths.py
```

Expected: FAIL with `ModuleNotFoundError: No module named 'paths'`.

- [ ] **Step 3: Add the shared path module**

Create `publishing/book-source/paths.py`:

```python
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = Path(os.environ.get("REVELATION_ROOT", HERE.parent.parent)).resolve()
CONTENT = ROOT / "content"
ARTWORK = ROOT / "artwork" / "book-images"
ORIGINALS = ROOT / "artwork" / "originals"
PUBLISHING = ROOT / "publishing"
INDESIGN = PUBLISHING / "indesign"
BUILD = ROOT / "build"

def relative_from_build(path):
    return Path(os.path.relpath(Path(path), BUILD)).as_posix()
```

- [ ] **Step 4: Replace copied content, plate, font, and output assumptions**

Make these exact path changes across the book scripts:

```python
from paths import ARTWORK, BUILD, CONTENT, INDESIGN, relative_from_build

T = json.load(open(CONTENT / "tapestries.json"))
REV = json.load(open(CONTENT / "revelation.web.json"))
BUILD.mkdir(parents=True, exist_ok=True)
```

Generate `build/book.html`, reference plate images through `relative_from_build(ARTWORK / filename)`, and reference `theme.css` and `paginate.js` through paths relative to `build/`. Write the designed PDF to `build/REVELATION_web.pdf`, rendered EPUB pages to `build/epub_pages/`, and both rebuilt EPUBs to `build/`.

Replace local `plates/...` reads in `make_epub_reflow.py` with `ARTWORK / filename`, and replace `indesign/Fonts` with `INDESIGN / "Fonts"`.

Keep `REVELATION_ROOT` optional. No instructions may require it when running inside the extracted archive.

- [ ] **Step 5: Update designed-book instructions with exact root-relative commands**

Document:

```bash
python3 publishing/book-source/build.py
python3 publishing/book-source/render.py
python3 publishing/book-source/render_pages.py 2048
python3 publishing/book-source/make_epub_fixed.py build/epub_pages
python3 publishing/book-source/make_epub_reflow.py
```

State that outputs appear in `build/`, and list Python/Playwright/Pillow prerequisites.

- [ ] **Step 6: Run unit and static path checks**

```bash
rtk python3 publishing/book-source/test_paths.py
rtk rg -n "/Users/alirahman|Desktop/test|localhost|127\.0\.0\.1" publishing/book-source -g '*.py' -g '*.js' -g '*.md'
```

Expected: path tests PASS; the prohibited-path search prints nothing.

- [ ] **Step 7: Run the lightweight HTML build against archive-shaped inputs**

Create a temporary archive root containing symlinks or copies of `content/`, staged `artwork/book-images/`, and `publishing/`, then run:

```bash
rtk env REVELATION_ROOT=/private/tmp/revelation-portable-check python3 publishing/book-source/build.py
rtk test -s /private/tmp/revelation-portable-check/build/book.html
```

Expected: `book.html` exists and every referenced local image resolves inside the temporary root.

- [ ] **Step 8: Commit portable designed-book paths**

```bash
rtk git add publishing/book-source
rtk git commit -m "feat: make book builders archive-relative"
```

---

### Task 4: Make IDML and both EPUB workflows portable and validated

**Files:**
- Modify: `publishing/book-source/build_idml.py`
- Modify: `publishing/book-source/build_cover_idml.py`
- Modify: `publishing/book-source/idml_lib.py`
- Modify: `publishing/book-source/validate_idml.py`
- Modify: `publishing/book-source/render_pages.py`
- Modify: `publishing/book-source/make_epub_fixed.py`
- Modify: `publishing/book-source/make_epub_reflow.py`
- Create: `publishing/book-source/validate_epub.py`
- Create: `publishing/book-source/test_validate_epub.py`
- Modify: `publishing/instructions/EPUB_BUILD_RULES.md`
- Modify: `publishing/instructions/INDESIGN_BUILD.md`

**Interfaces:**
- Consumes: Task 3's archive-root path constants and local artwork/font trees.
- Produces: archive-local IDML links, CLI-selectable fixed EPUB page size, and `validate_epub(path, edition)` for both EPUB types.

- [ ] **Step 1: Write failing IDML-link and EPUB-validator tests**

Extend `test_paths.py` with a URI assertion:

```python
def test_idml_uri_is_relative_and_portable(self):
    sys.path.insert(0, str(HERE))
    from idml_lib import link_uri
    self.assertEqual(link_uri(Path("../artwork/originals/T1-00.png")),
                     "file:../artwork/originals/T1-00.png")
    with self.assertRaises(ValueError):
        link_uri(Path("/Users/alirahman/T1-00.png"))
```

Create `test_validate_epub.py` with a minimal valid EPUB fixture and corrupt variants:

```python
import tempfile
import unittest
import zipfile
from pathlib import Path
from validate_epub import validate_epub

class ValidateEpubTest(unittest.TestCase):
    def make_epub(self, root):
        path = Path(root) / "valid.epub"
        with zipfile.ZipFile(path, "w") as zf:
            info = zipfile.ZipInfo("mimetype")
            info.compress_type = zipfile.ZIP_STORED
            zf.writestr(info, "application/epub+zip")
            zf.writestr("META-INF/container.xml", """<?xml version="1.0"?><container xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles><rootfile full-path="OEBPS/content.opf"/></rootfiles></container>""")
            zf.writestr("OEBPS/chapter.xhtml", """<html xmlns="http://www.w3.org/1999/xhtml"><body><span class="wj">Jesus</span></body></html>""")
            zf.writestr("OEBPS/content.opf", """<package xmlns="http://www.idpf.org/2007/opf"><manifest><item id="c" href="chapter.xhtml" media-type="application/xhtml+xml"/></manifest><spine><itemref idref="c"/></spine></package>""")
        return path

    def test_valid_reflowable_epub(self):
        with tempfile.TemporaryDirectory() as tmp:
            validate_epub(self.make_epub(tmp), "reflowable")

if __name__ == "__main__":
    unittest.main()
```

Add corrupt cases for compressed/non-first `mimetype`, missing manifest targets, unresolved spine `idref`, missing fixed spread properties, and missing reflowable `class="wj"`.

- [ ] **Step 2: Run the tests and confirm they fail**

```bash
rtk python3 publishing/book-source/test_paths.py
rtk python3 publishing/book-source/test_validate_epub.py
```

Expected: FAIL because `link_uri()` and `validate_epub()` do not exist.

- [ ] **Step 3: Centralize safe IDML file URIs**

In `idml_lib.py` add:

```python
def link_uri(path):
    value = Path(path)
    if value.is_absolute() or ".." not in value.parts:
        raise ValueError("IDML image link must be a relative path into the archive")
    return "file:" + value.as_posix()
```

Import `Path`, call `link_uri(link_path)` from `Page.image()`, and pass relative paths from the output IDML directory to `artwork/originals` or the lightweight JPEG link set.

Update `validate_idml.py` to resolve each `file:` URI against the containing IDML directory and require the resolved target to remain under the archive root when `--archive-root PATH` is supplied. Without that option, validate URI safety and IDML structure but defer target existence until the bundle has staged its artwork.

- [ ] **Step 4: Replace hard-coded InDesign bases and outputs**

Use Task 3 paths:

```python
from paths import BUILD, INDESIGN, ORIGINALS

LINKS = ORIGINALS
OUTPUT = BUILD / "REVELATION_13x11.idml"
```

For the cover, read `INDESIGN / "cover_bg.jpg"` and write `BUILD / "REVELATION_cover.idml"`. Preserve the 164-page default and existing Blurb geometry.

Regenerate the tracked source IDMLs once with their output directory set to `publishing/indesign/`, so the shipped files use `file:../../artwork/originals/...` rather than desktop paths.

- [ ] **Step 5: Implement the EPUB validator using only the standard library**

In `validate_epub.py`, implement:

```python
def validate_epub(path, edition):
    with zipfile.ZipFile(path) as zf:
        infos = zf.infolist()
        if not infos or infos[0].filename != "mimetype" or infos[0].compress_type != zipfile.ZIP_STORED:
            raise ValueError("mimetype must be first and stored")
        # Parse container.xml, OPF, and every XHTML with ElementTree.
        # Require every manifest href and spine idref to resolve.
        # Require fixed spread properties or reflowable class=\"wj\" according to edition.
```

Use `xml.etree.ElementTree`, `pathlib.PurePosixPath`, and `zipfile`; do not add an EPUB library.

- [ ] **Step 6: Implement the EPUB build-rule deltas**

Make `render_pages.py` accept a width argument, defaulting to `2048`, and choose JPEG quality from the page's classes: `76` for plate/cover pages and `88` for type-led pages. Make `make_epub_fixed.py` accept an optional pages directory argument exactly as documented.

Keep the fixed EPUB spine rule: page 1 center, subsequent odd pages right, even pages left. Keep DOM-derived navigation. Keep the reflowable source rooted in canonical JSON and `prose.py`, with embedded fonts, full scripture anchors, and actual `.wj` spans.

Call `validate_epub()` after each builder closes its ZIP.

- [ ] **Step 7: Run portable IDML and EPUB tests**

```bash
rtk python3 publishing/book-source/test_paths.py
rtk python3 publishing/book-source/test_validate_epub.py
rtk python3 publishing/book-source/validate_idml.py publishing/indesign/REVELATION_13x11.idml
rtk rg -n "/Users/alirahman|Desktop/test" publishing/indesign publishing/book-source -g '*.idml' -g '*.py' -g '*.md'
```

Expected: tests and structural/URI IDML validation PASS; prohibited-path search prints nothing. Task 6 repeats validation with `--archive-root` after extracting the artwork-bearing master ZIP.

- [ ] **Step 8: Commit portable publishing builders**

```bash
rtk git add publishing/book-source publishing/indesign publishing/instructions
rtk git commit -m "feat: make InDesign and EPUB builds portable"
```

Confirm ignored INDD/PDF files remain unstaged.

---

### Task 5: Build the master archive from validated release and publishing inputs

**Files:**
- Create: `scripts/lib/master-release.mjs`
- Create: `test/master-release.test.mjs`
- Modify: `scripts/build-release.mjs`
- Modify: `package.json`

**Interfaces:**
- Consumes: `content/*.json`, the existing `dist/releases/v1` artwork derivatives, tracked `publishing/` source, and ignored local finished artifacts.
- Produces: `masterArchiveName(version)`, `masterEntryPaths(sources, version, publishingFiles)`, `assertSafeMasterPath(path)`, `stageMasterRelease(options)`, and `dist/releases/v1/REVELATION-master-v1.zip`.

- [ ] **Step 1: Write failing pure master-release tests**

Create `test/master-release.test.mjs`:

```js
import assert from "node:assert/strict";
import test from "node:test";
import {
  assertSafeMasterPath,
  masterArchiveName,
  masterEntryPaths,
} from "../scripts/lib/master-release.mjs";

test("master archive uses the immutable release version", () => {
  assert.equal(masterArchiveName("v1"), "REVELATION-master-v1.zip");
});

test("master inventory names only the official editions", () => {
  const entries = masterEntryPaths(
    [{ id: "T1-00", originalExtension: ".png" }],
    "v1",
    ["instructions/PANDOC_EXPORTS.md"],
  );
  assert.ok(entries.includes("REVELATION-master-v1/editions/REVELATION_web.pdf"));
  assert.ok(entries.includes("REVELATION-master-v1/editions/REVELATION_iPad_fixed.epub"));
  assert.ok(!entries.some((entry) => /MASTER ORIGINAL|180-page|artwork-v1\.zip/.test(entry)));
});

for (const unsafe of ["../escape", "/absolute", "a/../../b", "a\\b", "file:test", "https://test"]){
  test(`rejects unsafe master path ${unsafe}`, () => {
    assert.throws(() => assertSafeMasterPath(unsafe), /safe archive path/);
  });
}
```

- [ ] **Step 2: Run the focused test and confirm it fails**

```bash
rtk node --disable-warning=MODULE_TYPELESS_PACKAGE_JSON --test test/master-release.test.mjs
```

Expected: FAIL because `scripts/lib/master-release.mjs` does not exist.

- [ ] **Step 3: Implement pure naming and inventory helpers**

Create `scripts/lib/master-release.mjs` with these exports:

```js
export const officialEditions = Object.freeze({
  "REVELATION_web.pdf": "REVELATION_web.pdf",
  "REVELATION_iPad_fixed.epub": "REVELATION_iPad_fixed_web.epub",
  "REVELATION_reflowable.epub": "REVELATION_reflowable.epub",
  "revelations.docx": "revelations.docx",
});

export function masterArchiveName(version) {
  return `REVELATION-master-${version}.zip`;
}

export function assertSafeMasterPath(value) {
  const parts = value.split("/");
  if (!value || value.startsWith("/") || value.includes("\\") || value.includes(":") || parts.some((part) => !part || part === "." || part === "..")) {
    throw new Error(`Master entry is not a safe archive path: ${value}`);
  }
  return value;
}
```

`masterEntryPaths(sources, version, publishingFiles)` returns the deterministic root metadata, content JSON, all expected artwork renditions, four official editions, and the caller-supplied sorted publishing source paths. `stageMasterRelease()` discovers publishing files with the documented filters, sorts them, and passes them into this pure helper.

- [ ] **Step 4: Implement staging and deterministic ZIP creation**

`stageMasterRelease()` must:

1. Create a temporary stage under `dist/releases/v1/.master-stage/REVELATION-master-v1/`.
2. Copy canonical content JSON.
3. Map `originals/` to `artwork/originals/`, `book/images/` to `artwork/book-images/`, and both web derivative directories to `artwork/web/`.
4. Copy tracked publishing source plus ignored local INDD, cover PDF, and official editions.
5. Normalize `REVELATION_iPad_fixed_web.epub` to `REVELATION_iPad_fixed.epub` inside the archive.
6. Render bundle-mode `export.md` with `imageRoot: "artwork/book-images"`.
7. Write the root README and `manifest.json`.
8. Hash every payload file in sorted POSIX-path order and write `SHA256SUMS.txt`.
9. Call the system `zip` command from the stage parent, with the master root as the only input.
10. Remove only `.master-stage` after successful ZIP creation.

Do not copy `publishing/.gitignore`, `.DS_Store`, `__pycache__`, generated book outputs, wrapper ZIPs, or Git-ignored editions other than the exact allowlist.

- [ ] **Step 5: Integrate master staging with the existing release build**

After the current 90 originals, 180 WebP derivatives, 90 JPEGs, manifest, checksums, and artwork ZIP are complete, call:

```js
await stageMasterRelease({
  root,
  releaseRoot,
  publishingRoot: path.join(root, "publishing"),
  version: "v1",
  sources,
  manifest,
  chapters,
  scenes: manifest.scenes,
});
```

Load `chapters` from `content/revelation.web.json`. Fail with the exact missing staging filename when any official edition or INDD input is absent.

- [ ] **Step 6: Add the package script and run focused tests**

Add:

```json
"publishing:validate": "node scripts/validate-master-release.mjs"
```

Do not add a second archive builder script; `npm run assets:release` remains the one release build command.

Run:

```bash
rtk node --disable-warning=MODULE_TYPELESS_PACKAGE_JSON --test test/master-release.test.mjs test/release-lib.test.mjs
rtk npm test
```

Expected: all tests PASS.

- [ ] **Step 7: Build the real release and inspect the master ZIP**

```bash
rtk npm run assets:release
rtk unzip -Z1 dist/releases/v1/REVELATION-master-v1.zip | rtk head -n 80
rtk unzip -tq dist/releases/v1/REVELATION-master-v1.zip
```

Expected: release build succeeds; ZIP has one `REVELATION-master-v1/` root; integrity check reports no errors.

- [ ] **Step 8: Commit master archive generation**

```bash
rtk git add scripts/build-release.mjs scripts/lib/master-release.mjs test/master-release.test.mjs package.json
rtk git commit -m "feat: build the self-contained master archive"
```

Do not stage `dist/`.

---

### Task 6: Validate archive portability and R2 metadata

**Files:**
- Create: `scripts/validate-master-release.mjs`
- Modify: `scripts/validate-release.mjs`
- Modify: `scripts/lib/release.mjs`
- Modify: `test/release-lib.test.mjs`
- Modify: `package.json`

**Interfaces:**
- Consumes: the archive and deterministic inventory from Task 5.
- Produces: `validateMasterInventory()`, expanded MIME/disposition rules, and `npm run publishing:validate` offline portability verification.

- [ ] **Step 1: Write failing release metadata and master inventory tests**

Add to `test/release-lib.test.mjs`:

```js
test("contentTypeFor covers publishing formats", () => {
  assert.equal(contentTypeFor("edition.pdf"), "application/pdf");
  assert.equal(contentTypeFor("edition.epub"), "application/epub+zip");
  assert.equal(contentTypeFor("edition.docx"), "application/vnd.openxmlformats-officedocument.wordprocessingml.document");
  assert.equal(contentTypeFor("source.idml"), "application/vnd.adobe.indesign-idml-package");
  assert.equal(contentTypeFor("source.indd"), "application/x-indesign");
  assert.equal(contentTypeFor("font.ttf"), "font/ttf");
  assert.equal(contentTypeFor("instructions.md"), "text/markdown; charset=utf-8");
});

test("publishing binaries and the master archive download as attachments", () => {
  assert.equal(contentDispositionFor("releases/v1/editions/REVELATION_web.pdf"), 'attachment; filename="REVELATION_web.pdf"');
  assert.equal(contentDispositionFor("releases/v1/REVELATION-master-v1.zip"), 'attachment; filename="REVELATION-master-v1.zip"');
});
```

- [ ] **Step 2: Run the tests and confirm they fail**

```bash
rtk node --disable-warning=MODULE_TYPELESS_PACKAGE_JSON --test test/release-lib.test.mjs
```

Expected: FAIL because the publishing MIME types and attachment paths are absent.

- [ ] **Step 3: Extend release metadata without changing immutable upload behavior**

Add MIME types for `.csv`, `.docx`, `.epub`, `.html`, `.idml`, `.indd`, `.js`, `.md`, `.pdf`, `.py`, `.ttf`, and `.woff2`. Mark originals, master ZIP, finished editions, and publishing binaries as attachments. Keep web artwork and source text inline-capable.

Do not change `HeadObject`, SHA-256 comparison, `IfNoneMatch: "*"`, or immutable cache headers in `upload-r2.mjs`.

- [ ] **Step 4: Implement extracted-archive validation**

`scripts/validate-master-release.mjs` must:

1. Create a new directory with `mkdtemp(path.join(tmpdir(), "revelation-master-"))`.
2. Extract the ZIP with `unzip -q`.
3. Discover and sort the extracted publishing paths, then compare the exact inventory to `masterEntryPaths(sources, "v1", publishingFiles)`.
4. Recompute and compare every checksum.
5. Run `pdfinfo` and require exactly 182 pages for `editions/REVELATION_web.pdf`.
6. Reject every other PDF with 180 pages and every filename containing `MASTER ORIGINAL`.
7. Scan `.md`, `.py`, `.js`, `.css`, `.html`, `.json`, `.csv`, and extracted IDML XML for `/Users/alirahman`, `Desktop/test`, localhost, required HTTP artwork, and escaping `file:` links.
8. Parse `export.md`, require 90 unique relative `artwork/book-images/*.jpg` paths, and verify each target exists.
9. Run the Python IDML and EPUB validators against extracted sources and finished EPUBs.
10. Remove the temporary extraction directory in `finally` using `rm(temp, { recursive: true, force: true })` only after confirming it is under `tmpdir()`.

- [ ] **Step 5: Update the existing release inventory validator**

Preserve all existing validation for 90 originals, 180 WebP derivatives, 90 book JPEGs, canonical manifests, and deterministic derivative checks. Extend the expected release tree with the master ZIP, and invoke the new validator after the artwork checks.

Do not hash or inspect the 1.4 GB artwork wrapper twice; its existing ZIP-entry verification remains sufficient.

- [ ] **Step 6: Run validation and tests**

```bash
rtk npm test
rtk npm run assets:validate
rtk npm run publishing:validate
```

Expected: all tests PASS; the current release and extracted master archive both validate.

- [ ] **Step 7: Commit validation and R2 metadata**

```bash
rtk git add scripts/validate-master-release.mjs scripts/validate-release.mjs scripts/lib/release.mjs test/release-lib.test.mjs package.json
rtk git commit -m "feat: validate portable publishing releases"
```

---

### Task 7: Replace fragmented homepage downloads with master, Blurb, and GitHub actions

**Files:**
- Modify: `lib/content.ts`
- Modify: `app/page.tsx`
- Modify: `app/page.module.css`
- Modify: `e2e/exhibition.spec.ts`
- Modify: `README.md`
- Modify: `docs/book-export.md`

**Interfaces:**
- Consumes: immutable R2 asset base and Task 5's master filename.
- Produces: `masterArchiveUrl`, an accessible Blurb iframe/link, and the three approved public actions.

- [ ] **Step 1: Write failing homepage behavior tests**

In `e2e/exhibition.spec.ts`, replace the fragmented archive expectations with:

```ts
test("offers the master archive, Blurb edition, and source", async ({ page }) => {
  await page.goto("/");
  const master = page.getByRole("link", { name: "Download the master archive" });
  await expect(master).toHaveAttribute("href", /releases\/v1\/REVELATION-master-v1\.zip$/);
  await expect(page.getByTitle("Preview Revelation on Blurb")).toHaveAttribute(
    "src",
    "https://www.blurb.com/bookshare/app/index.html?bookId=12978394",
  );
  await expect(page.getByRole("link", { name: "View the source on GitHub" })).toHaveAttribute(
    "href",
    "https://github.com/Divergent-World/revelations",
  );
});
```

Keep a separate assertion that `/export.md` still returns 200 for backward compatibility.

- [ ] **Step 2: Run the focused browser test and confirm it fails**

```bash
rtk npx playwright test e2e/exhibition.spec.ts --grep "offers the master archive"
```

Expected: FAIL because the master link and Blurb iframe are absent.

- [ ] **Step 3: Add stable public URLs**

In `lib/content.ts` add:

```ts
export const masterArchiveUrl = assetUrl(`releases/${contentVersion}/REVELATION-master-${contentVersion}.zip`);
export const blurbPreviewUrl = "https://www.blurb.com/bookshare/app/index.html?bookId=12978394";
```

Keep `archiveUrl` exported for backward compatibility even when the homepage stops rendering it.

- [ ] **Step 4: Implement the archive section and responsive preview**

Render these controls in order:

```tsx
<a className="button button-primary" href={masterArchiveUrl}>Download the master archive</a>
<a className="button" href={blurbPreviewUrl}>Preview / buy the print edition</a>
<a className="button" href="https://github.com/Divergent-World/revelations">View the source on GitHub</a>
```

Add the supplied embed with an accessible title and lazy loading:

```tsx
<iframe
  className={styles.blurbPreview}
  title="Preview Revelation on Blurb"
  src={blurbPreviewUrl}
  loading="lazy"
  allowFullScreen
/>
```

Use CSS `width: 100%`, `border: 0`, a bounded `aspect-ratio`, and a minimum height that remains usable on mobile. Do not add client state or a new package.

- [ ] **Step 5: Consolidate public documentation**

Update `README.md` and `docs/book-export.md` so the master archive is the default workflow. Preserve the standalone `/export.md` guide as a compatibility note. Use the root-relative Pandoc commands from `publishing/instructions/PANDOC_EXPORTS.md`; remove the requirement to run `npm run dev:local` for the master archive.

- [ ] **Step 6: Run static build and browser tests**

```bash
rtk npm run build
rtk npx playwright test e2e/exhibition.spec.ts
```

Expected: Next.js 16 statically generates `/export.md`; homepage tests PASS; the iframe and three actions are present.

- [ ] **Step 7: Commit the public master-download experience**

```bash
rtk git add lib/content.ts app/page.tsx app/page.module.css e2e/exhibition.spec.ts README.md docs/book-export.md
rtk git commit -m "feat: publish the master art-book archive"
```

---

### Task 8: Prove offline rebuildability from the final ZIP

**Files:**
- Create: `scripts/verify-master-rebuild.mjs`
- Modify: `package.json`
- Modify: `publishing/README.md`
- Modify: `publishing/instructions/PANDOC_EXPORTS.md`
- Modify: `publishing/instructions/EPUB_BUILD_RULES.md`
- Modify: `publishing/instructions/INDESIGN_BUILD.md`

**Interfaces:**
- Consumes: the final master ZIP and installed external build tools.
- Produces: `npm run publishing:verify`, which proves representative DOCX, PDF, EPUB, and IDML rebuilds from a fresh extraction.

- [ ] **Step 1: Write the rebuild verifier contract as a failing smoke test**

Add a test in `test/master-release.test.mjs` that imports `rebuildCommands()` from `scripts/verify-master-rebuild.mjs` and asserts the commands operate only inside the extraction root:

```js
test("offline rebuild commands stay inside the extracted archive", () => {
  const commands = rebuildCommands("/tmp/extracted/REVELATION-master-v1");
  assert.deepEqual(commands.map(({ name }) => name), ["docx", "pandoc-epub", "pandoc-pdf", "designed-pdf", "idml", "fixed-epub", "reflowable-epub"]);
  assert.ok(commands.every(({ cwd, args }) => cwd.startsWith("/tmp/extracted/REVELATION-master-v1") && !args.join(" ").includes("http")));
});
```

- [ ] **Step 2: Run the focused test and confirm it fails**

```bash
rtk node --disable-warning=MODULE_TYPELESS_PACKAGE_JSON --test test/master-release.test.mjs
```

Expected: FAIL because `verify-master-rebuild.mjs` does not exist.

- [ ] **Step 3: Implement the command manifest and verifier**

Export `rebuildCommands(root)` and, when invoked directly:

1. Extract the ZIP to `mkdtemp()`.
2. Require `pandoc`, `weasyprint`, `python3`, and `pdfinfo`; report one exact missing command if unavailable.
3. Run the root-relative DOCX, Pandoc EPUB, and Pandoc PDF commands.
4. Run the IDML generator and validator.
5. Run both designed EPUB builders and validators.
6. Run the designed PDF builder and require 182 pages.
7. Inspect the rebuilt DOCX ZIP for 90 `word/media/*.jpg` entries and the `Words of Jesus` style.
8. Reject any output path outside the extraction root.
9. Clean the verified temporary directory in `finally` after checking its parent is `tmpdir()`.

Add:

```json
"publishing:verify": "node scripts/verify-master-rebuild.mjs"
```

- [ ] **Step 4: Run the complete verification matrix**

```bash
rtk npm test
rtk npm run content:validate
rtk npm run assets:release
rtk npm run assets:validate
rtk npm run publishing:validate
rtk npm run publishing:verify
rtk npm run build
rtk npm run test:e2e
```

Expected:

- Unit and content tests pass.
- Release generation and both validators pass.
- Fresh extraction rebuilds DOCX with 90 images and red letters.
- Portable Pandoc EPUB/PDF build without network resources.
- Designed PDF has 182 pages.
- Fixed and reflowable EPUB validation passes.
- IDML validation passes with archive-local links.
- Next.js static build and end-to-end tests pass.

- [ ] **Step 5: Perform visual spot checks**

Render representative pages from the official and rebuilt PDFs with Poppler: cover, first scripture spread, a full-bleed plate, a band plate, Revelation text, Register of Losses, and back cover. Inspect for cropped images, missing fonts, clipped text, broken backgrounds, or changed proportions.

Open the rebuilt DOCX in a renderer and inspect at least one words-of-Jesus passage and three differently proportioned plates. Open both EPUBs in an EPUB reader and inspect navigation, cover, fixed spreads, live text, and red-letter spans.

- [ ] **Step 6: Finish instructions with observed commands and outputs**

Update all three instruction files with the exact commands that passed, expected output filenames under `build/`, prerequisite versions observed locally, and troubleshooting limited to real failures encountered during verification.

- [ ] **Step 7: Commit the offline rebuild proof**

```bash
rtk git add scripts/verify-master-rebuild.mjs test/master-release.test.mjs package.json publishing/README.md publishing/instructions
rtk git commit -m "test: prove master archive rebuildability"
```

- [ ] **Step 8: Final repository audit**

```bash
rtk git status --short
rtk git log --oneline -8
rtk git ls-files | rtk rg '\.(indd|pdf|epub)$'
rtk git check-ignore -v publishing/editions/REVELATION_web.pdf publishing/indesign/REVELATION_13x11.indd book/build.py
```

Expected: only pre-existing unrelated user changes remain; no INDD or finished edition is tracked; required binaries are ignored; the implementation consists of focused commits matching Tasks 1-8.

---

## Spec coverage map

- Git/source/binary boundary: Task 1.
- Historical `_book-build` preservation and warnings: Task 1.
- Relative `export.md` and red-letter DOCX: Tasks 2, 5, 6, and 8.
- Portable designed-book paths: Task 3.
- Portable IDML/INDD source and link validation: Tasks 1, 4, and 8.
- Two EPUB rules and structural validation: Tasks 4 and 8.
- Master ZIP inventory, checksums, and wrapper exclusion: Tasks 5 and 6.
- R2 immutability, MIME types, and attachment disposition: Task 6.
- Only the 182-page PDF and no 180-page PDF: Tasks 1, 5, 6, and 8.
- Master/Blurb/GitHub homepage actions: Task 7.
- External prerequisites and no network/source-vault dependency: Tasks 3, 4, 6, and 8.
- Fresh-directory offline rebuild and visual verification: Task 8.
