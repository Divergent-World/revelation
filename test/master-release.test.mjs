import assert from "node:assert/strict";
import test from "node:test";

import {
  assertSafeMasterPath,
  masterArchiveName,
  masterEntryPaths,
} from "../scripts/lib/master-release.mjs";

test("master archive uses the immutable release version", () => {
  assert.equal(masterArchiveName("v1"), "REVELATION-master-v1.zip");
});

test("master inventory names only the official editions", () => {
  const entries = masterEntryPaths(
    [{ id: "T1-00", originalExtension: ".png" }],
    "v1",
    ["instructions/PANDOC_EXPORTS.md"],
  );
  assert.ok(
    entries.includes("REVELATION-master-v1/editions/REVELATION_web.pdf"),
  );
  assert.ok(
    entries.includes(
      "REVELATION-master-v1/editions/REVELATION_iPad_fixed.epub",
    ),
  );
  assert.ok(
    !entries.some((entry) =>
      /MASTER ORIGINAL|180-page|artwork-v1\.zip/.test(entry),
    ),
  );
});

for (const unsafe of [
  "../escape",
  "/absolute",
  "a/../../b",
  "a\\b",
  "file:test",
  "https://test",
]) {
  test(`rejects unsafe master path ${unsafe}`, () => {
    assert.throws(() => assertSafeMasterPath(unsafe), /safe archive path/);
  });
}
