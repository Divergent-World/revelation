# Rebuild the illuminated book from the master archive

## Default workflow

Download `REVELATION-master-v1.zip` from the homepage and extract it. The archive already contains the official finished editions under `editions/`, including the 182-page PDF, fixed-layout and reflowable EPUBs, and DOCX.

It also contains everything project-specific needed to rebuild them: `export.md`, all 90 book JPEGs, canonical JSON, the red-letter reference DOCX, fonts, publishing scripts, portable IDML/INDD source, and detailed instructions. General-purpose tools such as Pandoc, WeasyPrint, Python, Playwright/Chromium, Pillow, and Adobe InDesign remain external prerequisites where relevant.

Run commands from the extracted `REVELATION-master-v1/` root. No site, R2 bucket, local asset server, or separate reference download is required.

## Pandoc exports

Install Pandoc and create the output directory:

```bash
brew install pandoc
mkdir -p build
```

### Microsoft Word / Google Docs

```bash
pandoc export.md \
  --from=markdown+yaml_metadata_block+bracketed_spans+link_attributes \
  --standalone \
  --toc \
  --reference-doc=publishing/reference/red-letter-reference.docx \
  --resource-path=. \
  --output=build/revelations.docx
```

The 90 relative images are embedded, and the `Words of Jesus` character style preserves crimson text in Word and Google Docs.

### Conventional reflowable EPUB

```bash
pandoc export.md \
  --from=markdown+yaml_metadata_block+bracketed_spans+link_attributes \
  --standalone \
  --toc \
  --split-level=2 \
  --resource-path=. \
  --output=build/revelations-pandoc.epub
```

The finished fixed-layout and purpose-built reflowable EPUBs in `editions/` follow stricter rules than this conventional Pandoc export. Rebuild those with `publishing/instructions/EPUB_BUILD_RULES.md`.

### Conventional PDF

```bash
brew install weasyprint
pandoc export.md \
  --from=markdown+yaml_metadata_block+bracketed_spans+link_attributes \
  --to=html5 \
  --standalone \
  --toc \
  --resource-path=. \
  --pdf-engine=weasyprint \
  --output=build/revelations-pandoc.pdf
```

For the designed 182-page book and editable InDesign layouts, follow `publishing/book-source/README.md` and `publishing/instructions/INDESIGN_BUILD.md` inside the archive.

## Standalone compatibility export

`/export.md` remains available for lightweight use. That route intentionally contains web artwork URLs, so conversions require those published URLs to remain reachable. The master archive is the reproducible offline workflow.
