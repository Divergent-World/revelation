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

    def test_idml_uri_is_relative_and_portable(self):
        sys.path.insert(0, str(HERE))
        from idml_lib import link_uri

        self.assertEqual(
            link_uri(Path("../artwork/originals/T1-00.png")),
            "file:../artwork/originals/T1-00.png",
        )
        with self.assertRaises(ValueError):
            link_uri(Path("/absolute/T1-00.png"))

    def test_plate_statuses_come_from_tracked_manifest(self):
        sys.path.insert(0, str(HERE))
        from plate_status import load_statuses

        statuses = load_statuses()
        self.assertEqual(len(statuses), 90)
        self.assertEqual(statuses["T1-T01"], "survives")
        self.assertEqual(statuses["T1-00"], "missing_or_lost")


if __name__ == "__main__":
    unittest.main()
