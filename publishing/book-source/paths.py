import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = Path(os.environ.get("REVELATION_ROOT", HERE.parent.parent)).resolve()
CONTENT = ROOT / "content"
ARTWORK = ROOT / "artwork" / "book-images"
ORIGINALS = ROOT / "artwork" / "originals"
PUBLISHING = ROOT / "publishing"
INDESIGN = PUBLISHING / "indesign"
BUILD = ROOT / "build"


def relative_from_build(path):
    return Path(os.path.relpath(Path(path), BUILD)).as_posix()
