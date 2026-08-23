# Markdown and DOCX exports

Run these commands from the root of the extracted master archive. They use only paths included in that archive.

The archive's `export.md` points to `artwork/book-images/*.jpg` using relative paths. To rebuild the DOCX with the supplied red-letter styles:

```bash
pandoc --version
mkdir -p build
pandoc export.md \
  --from=markdown+yaml_metadata_block+bracketed_spans+link_attributes \
  --standalone \
  --toc \
  --reference-doc=publishing/reference/red-letter-reference.docx \
  --resource-path=. \
  --output=build/revelations.docx
```

To rebuild a conventional reflowable Pandoc EPUB:

```bash
pandoc export.md \
  --from=markdown+yaml_metadata_block+bracketed_spans+link_attributes \
  --standalone \
  --toc \
  --split-level=2 \
  --resource-path=. \
  --output=build/revelations-pandoc.epub
```

To rebuild a conventional PDF with WeasyPrint:

```bash
pandoc export.md \
  --from=markdown+yaml_metadata_block+bracketed_spans+link_attributes \
  --to=html5 \
  --standalone \
  --toc \
  --resource-path=. \
  --pdf-engine=weasyprint \
  --output=build/revelations-pandoc.pdf
```

Expected outputs:

- `build/revelations.docx` — 90 embedded JPEG plates plus the supplied `Words of Jesus` character style.
- `build/revelations-pandoc.epub` — a conventional reflowable Pandoc EPUB.
- `build/revelations-pandoc.pdf` — a conventional PDF rendered through WeasyPrint.

Verified locally with Pandoc 3.10.1, WeasyPrint 69.0, Python 3.14.7, and Poppler `pdfinfo` 26.05.0. No website, R2 bucket, web server, source vault, or external reference file is required.

Fontconfig may print `No writable cache directories` in a restricted environment. During verification that warning was non-fatal: Pandoc and WeasyPrint completed and the output files validated. Treat it as a failure only if the requested output is absent or the command exits nonzero.
