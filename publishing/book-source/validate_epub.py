import zipfile
import xml.etree.ElementTree as ET
import argparse
from pathlib import Path, PurePosixPath


def _local_name(tag):
    return tag.rsplit("}", 1)[-1]


def _safe_member(opf_path, href):
    value = PurePosixPath(href)
    if (
        not href
        or href.startswith("/")
        or "\\" in href
        or ":" in href
        or "?" in href
        or "#" in href
        or any(part in ("", ".", "..") for part in value.parts)
    ):
        raise ValueError("manifest href is not a safe EPUB path: %s" % href)
    return (PurePosixPath(opf_path).parent / value).as_posix()


def validate_epub(path, edition):
    if edition not in ("fixed", "reflowable"):
        raise ValueError("edition must be fixed or reflowable")

    path = Path(path)
    with zipfile.ZipFile(path) as archive:
        infos = archive.infolist()
        if (
            not infos
            or infos[0].filename != "mimetype"
            or infos[0].compress_type != zipfile.ZIP_STORED
        ):
            raise ValueError("mimetype must be first and stored")
        if archive.read("mimetype") != b"application/epub+zip":
            raise ValueError("mimetype content is invalid")

        names = set(archive.namelist())
        try:
            container = ET.fromstring(archive.read("META-INF/container.xml"))
        except (KeyError, ET.ParseError) as error:
            raise ValueError("container.xml is missing or invalid") from error

        rootfile = next(
            (
                element.get("full-path")
                for element in container.iter()
                if _local_name(element.tag) == "rootfile"
            ),
            None,
        )
        if not rootfile or rootfile not in names:
            raise ValueError("container rootfile is missing")

        parsed = {}
        for name in sorted(names):
            if name.endswith((".xhtml", ".opf")):
                try:
                    parsed[name] = ET.fromstring(archive.read(name))
                except ET.ParseError as error:
                    raise ValueError("EPUB XML is invalid: %s" % name) from error

        opf = parsed[rootfile]
        manifest = {}
        for element in opf.iter():
            if _local_name(element.tag) != "item":
                continue
            item_id = element.get("id")
            href = element.get("href")
            if not item_id or not href:
                raise ValueError("manifest item requires id and href")
            target = _safe_member(rootfile, href)
            if target not in names:
                raise ValueError("manifest target is missing: %s" % target)
            manifest[item_id] = target

        spine_items = [
            element
            for element in opf.iter()
            if _local_name(element.tag) == "itemref"
        ]
        for itemref in spine_items:
            idref = itemref.get("idref")
            if idref not in manifest:
                raise ValueError("spine idref is missing from manifest: %s" % idref)
            if edition == "fixed":
                properties = set((itemref.get("properties") or "").split())
                if not properties.intersection(
                    {
                        "rendition:page-spread-center",
                        "rendition:page-spread-left",
                        "rendition:page-spread-right",
                    }
                ):
                    raise ValueError("fixed spine item requires page-spread properties")

        if edition == "reflowable":
            has_red_letters = any(
                "wj" in (element.get("class") or "").split()
                for name, tree in parsed.items()
                if name.endswith(".xhtml")
                for element in tree.iter()
            )
            if not has_red_letters:
                raise ValueError('reflowable EPUB requires class="wj" spans')

    return path


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    parser.add_argument("edition", choices=("fixed", "reflowable"))
    arguments = parser.parse_args()
    validated = validate_epub(arguments.path, arguments.edition)
    print("validated", validated)
