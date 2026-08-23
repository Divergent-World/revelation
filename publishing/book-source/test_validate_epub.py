import tempfile
import unittest
import zipfile
from pathlib import Path

from validate_epub import validate_epub


class ValidateEpubTest(unittest.TestCase):
    def make_epub(
        self,
        root,
        *,
        first=True,
        stored=True,
        manifest_href="chapter.xhtml",
        spine_idref="c",
        spread="rendition:page-spread-center",
        words_of_jesus=True,
    ):
        path = Path(root) / "fixture.epub"
        mimetype = zipfile.ZipInfo("mimetype")
        mimetype.compress_type = (
            zipfile.ZIP_STORED if stored else zipfile.ZIP_DEFLATED
        )
        chapter = (
            '<html xmlns="http://www.w3.org/1999/xhtml"><body>'
            + ('<span class="wj">Jesus</span>' if words_of_jesus else "Jesus")
            + "</body></html>"
        )
        opf = (
            '<package xmlns="http://www.idpf.org/2007/opf">'
            '<manifest><item id="c" href="%s" media-type="application/xhtml+xml"/>'
            '</manifest><spine><itemref idref="%s" properties="%s"/></spine>'
            "</package>"
        ) % (manifest_href, spine_idref, spread)
        with zipfile.ZipFile(path, "w") as archive:
            if not first:
                archive.writestr("before.txt", "wrong order")
            archive.writestr(mimetype, "application/epub+zip")
            archive.writestr(
                "META-INF/container.xml",
                '<?xml version="1.0"?><container '
                'xmlns="urn:oasis:names:tc:opendocument:xmlns:container">'
                '<rootfiles><rootfile full-path="OEBPS/content.opf"/>'
                "</rootfiles></container>",
            )
            archive.writestr("OEBPS/chapter.xhtml", chapter)
            archive.writestr("OEBPS/content.opf", opf)
        return path

    def test_valid_reflowable_epub(self):
        with tempfile.TemporaryDirectory() as tmp:
            validate_epub(self.make_epub(tmp), "reflowable")

    def test_valid_fixed_epub(self):
        with tempfile.TemporaryDirectory() as tmp:
            validate_epub(self.make_epub(tmp, words_of_jesus=False), "fixed")

    def test_rejects_mimetype_that_is_not_first_or_stored(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError, "mimetype must be first and stored"):
                validate_epub(self.make_epub(tmp, first=False), "reflowable")
            with self.assertRaisesRegex(ValueError, "mimetype must be first and stored"):
                validate_epub(self.make_epub(tmp, stored=False), "reflowable")

    def test_rejects_missing_manifest_target(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError, "manifest target is missing"):
                validate_epub(
                    self.make_epub(tmp, manifest_href="missing.xhtml"),
                    "reflowable",
                )

    def test_rejects_unresolved_spine_idref(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError, "spine idref is missing"):
                validate_epub(
                    self.make_epub(tmp, spine_idref="missing"),
                    "reflowable",
                )

    def test_rejects_fixed_spine_without_spread_properties(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError, "fixed spine item requires"):
                validate_epub(
                    self.make_epub(tmp, spread="", words_of_jesus=False),
                    "fixed",
                )

    def test_rejects_reflowable_without_red_letter_spans(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError, 'class="wj"'):
                validate_epub(
                    self.make_epub(tmp, words_of_jesus=False),
                    "reflowable",
                )


if __name__ == "__main__":
    unittest.main()
