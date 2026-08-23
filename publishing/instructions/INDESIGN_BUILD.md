# InDesign rebuild

The source-controlled `publishing/indesign/*.idml` files are the canonical editable layouts. Open them in Adobe InDesign after extracting the complete master archive; their artwork links resolve within the archive. Save new `.indd` files locally if native InDesign editing is needed.

The supplied `.indd` files are convenience snapshots and are not versioned in Git. Fonts and their licence notices live in `publishing/indesign/Fonts/`.

The generator sources are under `publishing/book-source/`. Run book commands from that directory so its archive-relative path resolver can find canonical content, artwork, and InDesign output paths. Exact generation and validation commands are documented here as those portable scripts are introduced.

Prerequisites: Python 3 plus the dependencies documented by the generator, and Adobe InDesign for opening or exporting IDML/INDD.
