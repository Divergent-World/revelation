# InDesign rebuild

The source-controlled `publishing/indesign/*.idml` files are the canonical editable layouts. Open them in Adobe InDesign after extracting the complete master archive; their artwork links resolve within the archive. Save new `.indd` files locally if native InDesign editing is needed.

The supplied `.indd` files are convenience snapshots and are not versioned in Git. Fonts and their licence notices live in `publishing/indesign/Fonts/`.

The generator sources are under `publishing/book-source/`. From the extracted archive root, rebuild and validate the portable IDML files with:

```bash
python3 publishing/book-source/build_idml.py
python3 publishing/book-source/build_cover_idml.py 164
python3 publishing/book-source/validate_idml.py build/REVELATION_13x11.idml --archive-root .
python3 publishing/book-source/validate_idml.py build/REVELATION_cover.idml --archive-root .
```

Outputs appear in `build/`. The interior defaults to lossless PNG links under `artwork/originals/`; set `LINK_SET=jpg` to use the lighter `artwork/book-images/` link set. The cover command preserves the 164-page Blurb spine default; pass a different verified page count when preparing another physical edition.

Prerequisites: Python 3 plus the dependencies documented by the generator, and Adobe InDesign for opening or exporting IDML/INDD.
