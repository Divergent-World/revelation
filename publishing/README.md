# REVELATION publishing workspace

This directory is the source-controlled publishing half of the project. Together with the canonical content and artwork assembled by the release builder, it supplies the editable sources and instructions included in `REVELATION-master-v1.zip`.

## What Git tracks

- `book-source/`: generators for the print book, IDML, and both EPUB editions.
- `indesign/`: portable IDML, linked-source metadata, cover artwork, fonts, and licence notices.
- `instructions/`: the commands and publishing rules needed after extracting the master archive.
- `reference/`: the Pandoc reference document used to reproduce red-letter DOCX styling.
- `historical-book-build/`: selected planning records from the earlier 180-page build, retained as background only.

## What stays local

Finished PDF, EPUB, DOCX, INDD, and cover-PDF binaries are deliberately ignored to prevent binary revisions from bloating Git history. Stage the exact files named in `editions/README.md` before building the master archive. The release builder packages them; GitHub does not.

The canonical public PDF is `editions/REVELATION_web.pdf`, the 182-page edition. No 180-page PDF belongs in this workspace or the master archive.

## Rebuild map

After extracting the master ZIP, run every publishing command from its top-level `REVELATION-master-v1/` directory:

- `instructions/PANDOC_EXPORTS.md` rebuilds the portable DOCX, Pandoc EPUB, and conventional PDF from `export.md`.
- `book-source/README.md` rebuilds the 182-page designed PDF and both designed EPUB editions.
- `instructions/INDESIGN_BUILD.md` rebuilds and validates the portable interior and cover IDML.
- `instructions/EPUB_BUILD_RULES.md` records the fixed-layout and reflowable EPUB rules.

Generated files always go to `build/`; the packaged official editions remain unchanged under `editions/`. Plate survival labels are sourced from the tracked `historical-book-build/PLATE_MANIFEST.csv`, so a clean extraction does not depend on a generated index.

Maintainers can prove the entire flow against a fresh temporary extraction with:

```bash
npm run assets:release
npm run publishing:verify
```

The verifier requires the external tools below on `PATH`, extracts the ZIP, rebuilds every representative format without network or R2 access, validates the outputs, and removes its temporary directory.
