import { createHash } from "node:crypto";
import {
  copyFile,
  mkdir,
  readdir,
  readFile,
  rm,
  writeFile,
} from "node:fs/promises";
import path from "node:path";
import { spawn } from "node:child_process";

export const officialEditions = Object.freeze({
  "REVELATION_web.pdf": "REVELATION_web.pdf",
  "REVELATION_iPad_fixed.epub": "REVELATION_iPad_fixed_web.epub",
  "REVELATION_reflowable.epub": "REVELATION_reflowable.epub",
  "revelation.docx": "revelation.docx",
});

const contentFiles = Object.freeze([
  "revelation.web.json",
  "scene-metadata.json",
  "source-map.json",
  "tapestries.json",
]);

const publishingBinaryFiles = Object.freeze([
  "indesign/REVELATION_13x11.indd",
  "indesign/REVELATION_cover.indd",
  "indesign/REVELATION_cover.pdf",
]);

export function masterArchiveName(version) {
  return `REVELATION-master-${version}.zip`;
}

export function assertSafeMasterPath(value) {
  const parts = value.split("/");
  if (
    !value ||
    value.startsWith("/") ||
    value.includes("\\") ||
    value.includes(":") ||
    parts.some((part) => !part || part === "." || part === "..")
  ) {
    throw new Error(`Master entry is not a safe archive path: ${value}`);
  }
  return value;
}

export function masterEntryPaths(sources, version, publishingFiles) {
  const archiveRoot = `REVELATION-master-${version}`;
  assertSafeMasterPath(archiveRoot);
  const entries = [
    "README.md",
    "manifest.json",
    "SHA256SUMS.txt",
    "export.md",
    ...contentFiles.map((file) => `content/${file}`),
    "artwork/book-images/ebook_front.jpg",
    "artwork/book-images/ebook_back.jpg",
    ...Object.keys(officialEditions).map((file) => `editions/${file}`),
    ...sources.flatMap(({ id, originalExtension }) => [
      `artwork/originals/${id}${originalExtension}`,
      `artwork/book-images/${id}.jpg`,
      `artwork/web/640/${id}.webp`,
      `artwork/web/1920/${id}.webp`,
    ]),
    ...publishingFiles.map((file) => `publishing/${file}`),
  ].map((file) => `${archiveRoot}/${file}`);
  return [...new Set(entries.map(assertSafeMasterPath))].sort();
}

async function filesBelow(directory, prefix = "") {
  const entries = await readdir(directory, { withFileTypes: true });
  const files = [];
  for (const entry of entries.sort((a, b) => a.name.localeCompare(b.name))) {
    const relative = prefix ? `${prefix}/${entry.name}` : entry.name;
    if (entry.isDirectory()) {
      files.push(...(await filesBelow(path.join(directory, entry.name), relative)));
    } else if (entry.isFile()) {
      files.push(relative);
    }
  }
  return files;
}

function includePublishingSource(relative) {
  const parts = relative.split("/");
  const basename = parts.at(-1);
  if (
    basename === ".gitignore" ||
    basename === ".DS_Store" ||
    parts.includes("__pycache__") ||
    basename.endsWith(".pyc")
  ) {
    return false;
  }
  if (parts[0] === "editions" && relative !== "editions/README.md") return false;
  if (parts[0] === "indesign" && /\.(?:indd|pdf)$/i.test(relative)) return false;
  if (
    parts[0] === "book-source" &&
    (basename === "book.html" ||
      parts.includes("epub_pages") ||
      /\.(?:pdf|epub)$/i.test(relative))
  ) {
    return false;
  }
  return true;
}

export async function discoverPublishingFiles(publishingRoot) {
  const sourceFiles = (await filesBelow(publishingRoot)).filter(
    includePublishingSource,
  );
  return [...new Set([...sourceFiles, ...publishingBinaryFiles])].sort();
}

async function copy(source, destination) {
  await mkdir(path.dirname(destination), { recursive: true });
  await copyFile(source, destination);
}

async function run(command, args, cwd) {
  await new Promise((resolve, reject) => {
    const child = spawn(command, args, { cwd, stdio: "inherit" });
    child.on("error", reject);
    child.on("exit", (code) =>
      code === 0
        ? resolve()
        : reject(new Error(`${command} exited ${code}`)),
    );
  });
}

function sha256(buffer) {
  return createHash("sha256").update(buffer).digest("hex");
}

export async function stageMasterRelease({
  root,
  releaseRoot,
  publishingRoot,
  version,
  sources,
  manifest,
  chapters,
  scenes,
}) {
  const archiveName = masterArchiveName(version);
  const archiveRootName = `REVELATION-master-${version}`;
  const stageBase = path.join(releaseRoot, ".master-stage");
  const stageRoot = path.join(stageBase, archiveRootName);
  const archivePath = path.join(releaseRoot, archiveName);
  await rm(stageBase, { recursive: true, force: true });
  await rm(archivePath, { force: true });
  await mkdir(stageRoot, { recursive: true });

  for (const file of contentFiles) {
    await copy(path.join(root, "content", file), path.join(stageRoot, "content", file));
  }

  for (const { id, originalExtension } of sources) {
    await Promise.all([
      copy(
        path.join(releaseRoot, "originals", `${id}${originalExtension}`),
        path.join(stageRoot, "artwork", "originals", `${id}${originalExtension}`),
      ),
      copy(
        path.join(releaseRoot, "book", "images", `${id}.jpg`),
        path.join(stageRoot, "artwork", "book-images", `${id}.jpg`),
      ),
      copy(
        path.join(releaseRoot, "web", "640", `${id}.webp`),
        path.join(stageRoot, "artwork", "web", "640", `${id}.webp`),
      ),
      copy(
        path.join(releaseRoot, "web", "1920", `${id}.webp`),
        path.join(stageRoot, "artwork", "web", "1920", `${id}.webp`),
      ),
    ]);
  }

  for (const [archiveFile, stagedFile] of Object.entries(officialEditions)) {
    await copy(
      path.join(publishingRoot, "editions", stagedFile),
      path.join(stageRoot, "editions", archiveFile),
    );
  }

  const publishingFiles = await discoverPublishingFiles(publishingRoot);
  for (const relative of publishingFiles) {
    await copy(
      path.join(publishingRoot, relative),
      path.join(stageRoot, "publishing", relative),
    );
  }

  const epubAssets = path.join(stageBase, ".epub-assets");
  await mkdir(epubAssets, { recursive: true });
  await run(
    "unzip",
    [
      "-qq",
      path.join(publishingRoot, "editions", "REVELATION_reflowable.epub"),
      "OEBPS/plates/ebook_front.jpg",
      "OEBPS/plates/ebook_back.jpg",
      "-d",
      epubAssets,
    ],
    root,
  );
  await Promise.all(
    ["ebook_front.jpg", "ebook_back.jpg"].map((file) =>
      copy(
        path.join(epubAssets, "OEBPS", "plates", file),
        path.join(stageRoot, "artwork", "book-images", file),
      ),
    ),
  );

  const { renderMarkdownBook } = await import("../../lib/markdown-book.ts");
  const markdown = renderMarkdownBook({
    chapters,
    scenes,
    imageSource: { kind: "bundle", imageRoot: "artwork/book-images" },
  });
  const readme = `# REVELATION master ${version}\n\nThis self-contained archive includes the official 182-page PDF, fixed-layout and reflowable EPUBs, DOCX, canonical content, artwork, portable IDML/INDD sources, fonts, licences, generators, and publishing instructions.\n\nStart with \`publishing/README.md\`. Rebuild commands use only paths inside this extracted directory; Pandoc, Python, Playwright/Chromium, Pillow, WeasyPrint, and Adobe InDesign remain external prerequisites where documented.\n`;
  await Promise.all([
    writeFile(path.join(stageRoot, "README.md"), readme),
    writeFile(path.join(stageRoot, "export.md"), markdown),
    writeFile(path.join(stageRoot, "manifest.json"), `${JSON.stringify(manifest, null, 2)}\n`),
  ]);

  const payloadFiles = await filesBelow(stageRoot);
  const sums = [];
  for (const relative of payloadFiles) {
    sums.push(`${sha256(await readFile(path.join(stageRoot, relative)))}  ${relative}`);
  }
  await writeFile(path.join(stageRoot, "SHA256SUMS.txt"), `${sums.join("\n")}\n`);

  const actualEntries = (await filesBelow(stageRoot)).map(
    (relative) => `${archiveRootName}/${relative}`,
  ).sort();
  const expectedEntries = masterEntryPaths(
    sources,
    version,
    publishingFiles,
  );
  if (JSON.stringify(actualEntries) !== JSON.stringify(expectedEntries)) {
    const actual = new Set(actualEntries);
    const expected = new Set(expectedEntries);
    const missing = expectedEntries.filter((entry) => !actual.has(entry));
    const unexpected = actualEntries.filter((entry) => !expected.has(entry));
    throw new Error(
      `Master staging inventory mismatch; missing=${missing.join(",")}; unexpected=${unexpected.join(",")}`,
    );
  }

  await run("zip", ["-q", "-X", archivePath, ...actualEntries], stageBase);
  await rm(stageBase, { recursive: true, force: true });
  return { archivePath, entries: actualEntries };
}
