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
