import assert from "node:assert/strict";
import test from "node:test";

import { contentDispositionFor, contentTypeFor, expectedReleaseFiles, releasePaths, validateReleaseInventory } from "../scripts/lib/release.mjs";

test("releasePaths uses stable scene IDs and preserves original extension", () => {
  assert.deepEqual(releasePaths("T2-B07", ".PNG"), {
    original: "releases/v1/originals/T2-B07.png",
    preview: "releases/v1/web/640/T2-B07.webp",
    reader: "releases/v1/web/1920/T2-B07.webp",
    book: "releases/v1/book/images/T2-B07.jpg",
  });
});

test("contentTypeFor covers published release formats", () => {
  assert.equal(contentTypeFor("scene.webp"), "image/webp");
  assert.equal(contentTypeFor("scene.jpg"), "image/jpeg");
  assert.equal(contentTypeFor("manifest.json"), "application/json; charset=utf-8");
  assert.equal(contentTypeFor("artwork.zip"), "application/zip");
  assert.equal(contentTypeFor("edition.pdf"), "application/pdf");
  assert.equal(contentTypeFor("edition.epub"), "application/epub+zip");
  assert.equal(
    contentTypeFor("edition.docx"),
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
  );
  assert.equal(
    contentTypeFor("source.idml"),
    "application/vnd.adobe.indesign-idml-package",
  );
  assert.equal(contentTypeFor("source.indd"), "application/x-indesign");
  assert.equal(contentTypeFor("font.ttf"), "font/ttf");
  assert.equal(contentTypeFor("instructions.md"), "text/markdown; charset=utf-8");
});

test("contentDispositionFor forces cross-origin originals and archives to download", () => {
  assert.equal(contentDispositionFor("releases/v1/originals/T1-T01.png"), 'attachment; filename="T1-T01.png"');
  assert.equal(contentDispositionFor("releases/v1/revelations-artwork-v1.zip"), 'attachment; filename="revelations-artwork-v1.zip"');
  assert.equal(contentDispositionFor("releases/v1/web/640/T1-T01.webp"), undefined);
});

test("publishing binaries and the master archive download as attachments", () => {
  assert.equal(
    contentDispositionFor("releases/v1/editions/REVELATION_web.pdf"),
    'attachment; filename="REVELATION_web.pdf"',
  );
  assert.equal(
    contentDispositionFor("releases/v1/REVELATION-master-v1.zip"),
    'attachment; filename="REVELATION-master-v1.zip"',
  );
});

test("expectedReleaseFiles produces exact stable filenames", () => {
  const files = expectedReleaseFiles([{ id: "T1-T01", originalExtension: ".png" }]);
  assert.deepEqual(files, {
    originals: ["T1-T01.png"],
    previews: ["T1-T01.webp"],
    readers: ["T1-T01.webp"],
    books: ["T1-T01.jpg"],
  });
});

test("validateReleaseInventory requires 90 originals, two derivative sets, and archive metadata", () => {
  const valid = {
    originals: 90,
    previews: 90,
    readers: 90,
    books: 90,
    zipFiles: 95,
    archiveOriginals: 90,
  };
  assert.doesNotThrow(() => validateReleaseInventory(valid));
  assert.throws(
    () => validateReleaseInventory({ ...valid, archiveOriginals: 89 }),
    /archive originals: expected 90, received 89/,
  );
});
