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

Prerequisites: Pandoc, plus WeasyPrint for the PDF command. No website, R2 bucket, web server, or external reference file is required.
