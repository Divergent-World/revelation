import assert from "node:assert/strict";
import test from "node:test";

import {
  assertSafeMasterPath,
  masterArchiveName,
  masterEntryPaths,
  officialEditions,
} from "../scripts/lib/master-release.mjs";
import {
  assertPlateStatuses,
  rebuildCommands,
} from "../scripts/verify-master-rebuild.mjs";

test("master archive uses the immutable release version", () => {
  assert.equal(masterArchiveName("v1"), "REVELATION-master-v1.zip");
});

test("master archive uses the singular editable edition name", () => {
  assert.equal(officialEditions["revelation.docx"], "revelation.docx");
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

test("offline rebuild commands stay inside the extracted archive", () => {
  const commands = rebuildCommands("/tmp/extracted/REVELATION-master-v1");
  assert.deepEqual(
    commands.map(({ name }) => name),
    [
      "docx",
      "pandoc-epub",
      "pandoc-pdf",
      "designed-pdf",
      "idml",
      "fixed-epub",
      "reflowable-epub",
    ],
  );
  assert.ok(
    commands.every(
      ({ cwd, args }) =>
        cwd.startsWith("/tmp/extracted/REVELATION-master-v1") &&
        !args.join(" ").includes("http"),
    ),
  );
});

test("offline rebuild requires all ninety tracked survival labels", () => {
  const rows = Array.from({ length: 90 }, (_, index) => {
    const id = index === 0 ? "T1-T01" : `plate-${index}`;
    const status = index === 0 ? "survives" : "lost";
    return `<div class="reg"><span class="k">${id}</span><span class="s ${status}">Label</span></div>`;
  }).join("");
  assert.doesNotThrow(() => assertPlateStatuses(rows));
  assert.throws(
    () => assertPlateStatuses(rows.replace("s survives", "s lost")),
    /T1-T01 survival label/,
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
