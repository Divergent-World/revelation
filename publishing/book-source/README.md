# book/ — REVELATION book build target

Generates the complete ebook (PDF) from the repo's content JSON. One source, one command.

## Run

```bash
pip install playwright --break-system-packages && playwright install chromium
python3 build.py     # content JSON -> book.html
python3 render.py    # book.html -> REVELATION_complete_edition.pdf
```

## Inputs

| File | Source |
|---|---|
| `tapestries.json`, `revelation.web.json` | copied from `content/` — symlink or copy at build time |
| `plates/T*.jpg` | 90 plates. Currently 1500px previews. **For print, regenerate from the `print/` derivative track** (see BOOK_BUILD_PLAN §3) |

## Editing

| To change | Edit |
|---|---|
| Foreword, notes, plate notes, codas | `prose.py` — plain strings, no markup needed |
| Typography, grid, colour, page treatments | `theme.css` |
| Page order, plate pacing, what goes where | `build.py` |
| How flowing text paginates | `paginate.js` |

Plate pacing is in `build.py`: even-indexed plates get a full-bleed page plus a facing
text page; odd-indexed plates get a single page with a 16:9 band and a footer. Change the
`if idx % 2 == 0` rule to change the rhythm of the whole book.

## Notes

- Survival status is joined **by title**, not by slot id, because the vault's
  `Master Index.md` is shifted one position against `content/scene-metadata.json` for 29
  slots. `content/` is canonical. See BOOK_BUILD_PLAN §0.
- Red-letter words of Christ come from `wordsOfJesus` character ranges in the content JSON.
- `plates/` is derived output. Do not commit it.
