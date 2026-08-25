# Self-Contained Publishing Export Design

## Goal

Publish one downloadable `REVELATION-master-v1.zip` that contains every project input needed to rebuild the official digital editions and editable publishing sources without contacting R2, running the website, reading the source vault, or resolving paths outside the extracted archive.

The website will present three clear actions: download the master archive, preview or buy the print edition through Blurb, and view or clone the GitHub source.

## Product boundaries

The master archive is the free, complete project payload. It includes finished editions, canonical content, artwork, publishing source, instructions, and validation metadata.

The only public finished PDF is the 182-page `REVELATION_web.pdf` from `New Info/versions/`. The following files are historical inputs and must not be committed, uploaded, or included in the master archive:

- `(MASTER ORIGINAL) REVELATION_complete_edition.pdf`, 180 pages.
- `_book-build/REVELATION_web.pdf`, 180 pages.
- Any other duplicate or superseded PDF under the ignored `book/` working tree.

The Blurb book-share URL remains the preview and purchase surface for the print edition:

`https://www.blurb.com/bookshare/app/index.html?bookId=12978394`

No custom payment gateway is part of this work. Blurb already supplies preview, cart, and fullscreen behavior.

## Repository organization

The existing root `/book/` directory remains ignored. It is a 1.7 GB working tree containing generated files, duplicate binaries, obsolete archives, and linked artwork.

Commit-worthy publishing material moves into a new tracked `publishing/` tree:

```text
publishing/
├── README.md
├── instructions/
│   ├── PANDOC_EXPORTS.md
│   ├── EPUB_BUILD_RULES.md
│   └── INDESIGN_BUILD.md
├── reference/
│   └── red-letter-reference.docx
├── book-source/
├── indesign/
├── historical-book-build/
└── editions/
```

The paths have these roles:

- `publishing/book-source/` is the maintained Python, JavaScript, CSS, HTML, JSON, and prose source currently in `New Info/REVELATION_book_source/`.
- `publishing/indesign/` contains tracked IDML sources, cover inputs, font files, font licence files, dimension metadata, and its README.
- `publishing/historical-book-build/` preserves useful planning and layout evidence from `_book-build/`, clearly marked non-canonical and historical.
- `publishing/instructions/` holds runnable build guidance. The new root `EPUB_INSTRUCTIONS.md` moves to `publishing/instructions/EPUB_BUILD_RULES.md`.
- `publishing/reference/red-letter-reference.docx` replaces the separately exposed file under `public/` as the canonical Pandoc reference document. The static site may copy it into its build output for backward compatibility.
- `publishing/editions/` is the local staging location for finished deliverables. Its binary contents are Git-ignored.

The following publishing files remain locally available but are ignored by Git:

- `publishing/editions/*.pdf`
- `publishing/editions/*.epub`
- `publishing/editions/*.docx`
- `publishing/indesign/*.indd`
- Generated PDFs and page renders under `publishing/indesign/` or `publishing/book-source/`

The following InDesign assets are tracked because they are reproducible source or required inputs:

- Interior and cover `.idml` files.
- Cover background artwork and dimension metadata.
- Font files and their SIL Open Font License notices.
- Generator scripts and validation tools.

The `.indd` files ship in the master archive for convenience but never enter Git history. IDML is the canonical reproducible InDesign source. Recreating an INDD means opening the included IDML in Adobe InDesign and saving it as INDD.

## Historical `_book-build` material

`_book-build` contains valuable design history but also decisions that the newer Master Context supersedes, including older trim, extent, and canonical-index conclusions. It must not be presented as the active build source.

The tracked historical directory includes:

- `BOOK_BUILD_PLAN.md`
- `REVELATION_Production_Bible.md`
- `PLATE_MANIFEST.csv`
- `dims.json`
- `spreads.html`

Its README states that `content/*.json` in the repository is canonical and that the current book source and Master Context override conflicting historical statements.

The directory excludes:

- Both 180-page PDFs.
- `REVELATION_sample_spreads.pdf`.
- `plates/` and `preview/` derivatives.
- `.DS_Store` and other generated files.

## Master archive layout

The release builder creates this user-facing archive:

```text
REVELATION-master-v1/
├── README.md
├── export.md
├── manifest.json
├── SHA256SUMS.txt
├── content/
│   ├── tapestries.json
│   ├── revelation.web.json
│   ├── scene-metadata.json
│   └── source-map.json
├── artwork/
│   ├── originals/
│   ├── book-images/
│   └── web/
│       ├── 640/
│       └── 1920/
├── editions/
│   ├── REVELATION_web.pdf
│   ├── REVELATION_iPad_fixed.epub
│   ├── REVELATION_reflowable.epub
│   └── revelation.docx
├── publishing/
│   ├── instructions/
│   ├── reference/
│   ├── book-source/
│   ├── indesign/
│   └── historical-book-build/
└── build/
```

`build/` is the documented destination for regenerated outputs. The archive may preserve the empty directory with a short README.

The fixed-layout EPUB is normalized to `REVELATION_iPad_fixed.epub`, matching the EPUB build rules, even when the incoming staging file is named `REVELATION_iPad_fixed_web.epub`.

The archive does not contain the older `revelation-artwork-v1.zip` or itself. Wrapper ZIPs are excluded to prevent recursive archives and a second 1.4 GB copy of the originals.

## Portable path contract

Every rebuild input must resolve from the extracted archive root. Rebuildable files must contain none of the following:

- `/Users/alirahman/...` or another machine-specific absolute path.
- `http://127.0.0.1`, `localhost`, or a requirement to run the website.
- An R2, Cloudflare, or other network URL for required artwork.
- `file:` references that point outside the extracted archive.
- `../` traversal that escapes the archive root.

The release copy of `export.md` uses relative POSIX image references such as:

```markdown
![Description](artwork/book-images/T1-00.jpg){width=4.83in height=7.25in}
```

The website's legacy standalone `/export.md` route may continue using absolute R2 URLs. The pure Markdown renderer therefore supports two explicit output modes:

- Web mode: clean HTTP or HTTPS asset origin plus canonical release keys.
- Bundle mode: a safe relative image root, fixed to `artwork/book-images` by the release builder.

Bundle mode rejects absolute filesystem paths, URL schemes, query strings, fragments, encoded traversal, and parent-directory traversal.

Book generators resolve canonical JSON, artwork, fonts, cover inputs, and outputs relative to the archive root. A narrowly scoped environment override may support repository development, but the extracted archive works with no path configuration.

The InDesign generators emit portable link URIs targeting artwork within the archive. Shipped IDML must not preserve the current absolute links into `/Users/alirahman/Desktop/test/Revelation/book/indesign/Links_png`.

## `export.md` and Pandoc workflow

`export.md` remains the complete illuminated scripture document: 22 chapters, 404 verses, 90 artworks, proportional figure dimensions, and red-letter character spans.

Build instructions do not appear in the scripture body. Instead, the root README links to `publishing/instructions/PANDOC_EXPORTS.md` and `publishing/instructions/EPUB_BUILD_RULES.md`.

From the extracted archive root, the DOCX command is:

```bash
pandoc export.md \
  --from=markdown+yaml_metadata_block+bracketed_spans+link_attributes \
  --standalone \
  --toc \
  --resource-path=. \
  --reference-doc=publishing/reference/red-letter-reference.docx \
  -o build/revelation.docx
```

Equivalent EPUB and PDF commands use the same relative resources. PDF generation through Pandoc uses the documented WeasyPrint HTML path so red lettering and proportional image guards survive.

The finished `editions/revelation.docx` is included for immediate use. The command demonstrates that a new editable DOCX can be created with all 90 JPEGs and the `Words of Jesus` character style using only archive contents.

## Designed book and EPUB workflow

The `publishing/book-source/` workflow is distinct from the portable Pandoc conversion. It rebuilds the designed 182-page PDF and the two purpose-built EPUB editions.

The EPUB rules are standing requirements:

- Always build both a fixed-layout and a reflowable EPUB.
- The fixed-layout EPUB renders each fully paginated page as a JPEG and never attempts live text.
- The reflowable EPUB is generated from canonical content JSON and `prose.py`, never from the paginated DOM.
- Both EPUBs satisfy EPUB 3 packaging, navigation, cover, metadata, XML, manifest, spine, and red-letter validation rules.
- The full archive carries the master-quality fixed EPUB. Instructions may document the smaller 1560 px derivative for constrained upload channels, but it is not the canonical archive edition.

The designed-book scripts consume:

- `content/*.json` from the archive root.
- Local artwork under `artwork/`.
- Local fonts and cover inputs under `publishing/indesign/`.
- Prose and layout code under `publishing/book-source/`.

Generated files go to `build/` rather than modifying shipped finished editions.

## InDesign workflow

The archive contains the editable interior and cover sources, current convenience INDD files, required fonts, cover background, artwork, dimension metadata, and generator code.

The canonical workflow is:

1. Install the included open-licence fonts.
2. Validate or regenerate the interior IDML from archive-local content and artwork.
3. Regenerate the 164-page Blurb cover IDML with the included cover generator.
4. Open IDML in Adobe InDesign and save as INDD.
5. Export using PDF/X-4:2010, document bleed settings, pages rather than spreads, and no printer marks.

Adobe InDesign itself is an external prerequisite and is not redistributed. The archive is self-contained with respect to project data and source assets, not proprietary runtimes.

## R2 release and immutability

`dist/releases/v1/` remains the local mirror used by `scripts/upload-r2.mjs`. The release builder adds the official editions, publishing payload, and `REVELATION-master-v1.zip` to the existing artwork and derivative tree.

The R2 uploader continues using immutable object keys. Existing v1 objects may be skipped when their stored SHA-256 matches. A key with different content remains a hard failure. A later edition change requires a new release version rather than overwriting the v1 master archive.

The master archive is the homepage's primary download. Existing artwork-only and standalone export URLs may remain addressable for backward compatibility, but they are no longer primary actions.

Content types and attachment headers cover PDF, EPUB, DOCX, Markdown, IDML, INDD, fonts, source files, and ZIP archives.

## Homepage presentation

The archive section presents:

1. `Download the master archive` - the primary R2 ZIP.
2. `Preview / buy the print edition` - the Blurb book-share experience.
3. `View the source on GitHub` - the repository.

The Blurb experience may be embedded responsively on the homepage or linked from a dedicated preview panel. The initial implementation uses the existing Blurb service rather than introducing checkout code.

## External prerequisites

The master archive includes all project-specific inputs, scripts, references, and assets. It does not vendor general-purpose or proprietary runtimes. Instructions name exact prerequisites for each workflow:

- Pandoc for DOCX and portable EPUB conversion.
- WeasyPrint for the Pandoc PDF path.
- Python and declared Python packages for the designed book and EPUB tools.
- Playwright and Chromium for pagination, PDF rendering, and fixed EPUB page rendering.
- Ghostscript where cover outlining is required.
- Adobe InDesign for INDD editing and final print PDF export.

No workflow silently downloads project content or artwork.

## Validation

The release is valid only when all of these checks pass:

### Inventory and integrity

- The master ZIP has one `REVELATION-master-v1/` root.
- Required paths and exact official edition names are present.
- The official PDF has exactly 182 pages.
- The archive contains no 180-page PDF.
- SHA-256 metadata covers every shipped file other than `SHA256SUMS.txt` itself.
- All 90 canonical artwork IDs appear exactly once in each required artwork rendition set.

### Portability

- Extract the ZIP into a newly created arbitrary temporary directory.
- Scan rebuild inputs for machine-specific paths, localhost, required R2 URLs, and escaping traversal.
- Confirm every relative image in `export.md` resolves inside the archive.
- Confirm every IDML link resolves inside the archive.

### Rebuilds

- Pandoc rebuilds `build/revelation.docx` with 90 embedded JPEGs and the red-letter character style.
- Pandoc rebuilds a portable EPUB and PDF without network access.
- The designed-book workflow regenerates a 182-page PDF.
- The fixed-layout EPUB has page images, required spread properties, valid XML, and resolvable manifest and spine entries.
- The reflowable EPUB has valid XML, resolvable manifest and spine entries, embedded fonts, and actual `class="wj"` spans.
- The IDML structural validator passes and all links are archive-local.

### Application and release

- Existing content, unit, and release tests pass.
- The Next.js static build succeeds.
- The homepage exposes the master, Blurb, and GitHub actions with accessible names and focus behavior.
- The R2 upload inventory includes the master archive with the correct content type and attachment disposition.

## Non-goals

- Reintroducing either 180-page PDF.
- Committing finished editions or INDD binaries to Git.
- Bundling Adobe InDesign, Pandoc, Chromium, Python, or other third-party runtimes.
- Building a custom payment gateway while Blurb supplies the purchase flow.
- Making the historical `_book-build` documents canonical.
- Producing one hybrid EPUB that attempts both fixed layout and live text.
- Guaranteeing byte-identical generated DOCX, EPUB, PDF, or INDD files across different tool versions; validation guarantees required content, structure, paths, and page counts instead.
