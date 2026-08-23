import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent


class PathsTest(unittest.TestCase):
    def test_override_keeps_every_project_path_inside_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            code = (
                "import paths; "
                "print(paths.ROOT); print(paths.CONTENT); print(paths.ARTWORK); "
                "print(paths.ORIGINALS); print(paths.INDESIGN); print(paths.BUILD)"
            )
            result = subprocess.run(
                [sys.executable, "-c", code],
                cwd=HERE,
                text=True,
                capture_output=True,
                env={**os.environ, "REVELATION_ROOT": tmp},
                check=True,
            )
            root = Path(tmp).resolve()
            for line in result.stdout.splitlines():
                Path(line).resolve().relative_to(root)

    def test_default_root_is_repository_root(self):
        sys.path.insert(0, str(HERE))
        import paths

        self.assertEqual(paths.ROOT, HERE.parent.parent)


if __name__ == "__main__":
    unittest.main()
