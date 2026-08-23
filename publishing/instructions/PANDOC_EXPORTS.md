# Markdown and DOCX exports

Run these commands from the root of the extracted master archive. They use only paths included in that archive.

The archive's `export.md` points to `artwork/book-images/*.jpg` using relative paths. To rebuild the DOCX with the supplied red-letter styles:

```bash
pandoc export.md \
  --from=gfm+raw_html \
  --reference-doc=publishing/reference/red-letter-reference.docx \
  --resource-path=. \
  --output=editions/revelations.docx
```

Prerequisite: Pandoc. No website, R2 bucket, localhost server, or external reference file is required.
