import assert from "node:assert/strict";
import { access, readFile } from "node:fs/promises";
import test from "node:test";

const required = [
  "publishing/README.md",
  "publishing/instructions/PANDOC_EXPORTS.md",
  "publishing/instructions/EPUB_BUILD_RULES.md",
  "publishing/instructions/INDESIGN_BUILD.md",
  "publishing/reference/red-letter-reference.docx",
  "public/red-letter-reference.docx",
  "publishing/book-source/build.py",
  "publishing/book-source/make_epub_fixed.py",
  "publishing/book-source/make_epub_reflow.py",
  "publishing/indesign/REVELATION_13x11.idml",
  "publishing/indesign/REVELATION_cover.idml",
  "publishing/historical-book-build/README.md",
];

test("publishing source layout contains every tracked rebuild input", async () => {
  await Promise.all(required.map((file) => access(file)));
});

test("historical publishing notes declare canonical and excluded inputs", async () => {
  const history = await readFile(
    "publishing/historical-book-build/README.md",
    "utf8",
  );
  assert.match(history, /historical/i);
  assert.match(history, /content\/\*\.json.*canonical/i);
  assert.match(history, /180-page PDFs.*excluded/i);
});

test("public and publishing red-letter references remain byte-identical", async () => {
  const [publicReference, publishingReference] = await Promise.all([
    readFile("public/red-letter-reference.docx"),
    readFile("publishing/reference/red-letter-reference.docx"),
  ]);
  assert.deepEqual(publicReference, publishingReference);
});
