import { createHash } from "node:crypto";
import {
  mkdtemp,
  readFile,
  readdir,
  rm,
} from "node:fs/promises";
import { tmpdir } from "node:os";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { spawn } from "node:child_process";

import {
  discoverPublishingFiles,
  masterArchiveName,
  masterEntryPaths,
} from "./lib/master-release.mjs";

const projectRoot = path.resolve(import.meta.dirname, "..");

function run(command, args, cwd, capture = false) {
  return new Promise((resolve, reject) => {
    const child = spawn(command, args, {
      cwd,
      stdio: capture ? ["ignore", "pipe", "inherit"] : "inherit",
    });
    let output = "";
    if (capture) child.stdout.on("data", (chunk) => { output += chunk; });
    child.on("error", reject);
    child.on("exit", (code) =>
      code === 0
        ? resolve(output)
        : reject(new Error(`${command} exited ${code}`)),
    );
  });
}

async function walk(directory, prefix = "") {
  const entries = await readdir(directory, { withFileTypes: true });
  const files = [];
  for (const entry of entries.sort((a, b) => a.name.localeCompare(b.name))) {
    const relative = prefix ? `${prefix}/${entry.name}` : entry.name;
    if (entry.isDirectory()) {
      files.push(...(await walk(path.join(directory, entry.name), relative)));
    } else if (entry.isFile()) {
      files.push(relative);
    }
  }
  return files;
}

function sha256(buffer) {
  return createHash("sha256").update(buffer).digest("hex");
}

function assertExact(actual, expected, label) {
  const left = [...actual].sort();
  const right = [...expected].sort();
  if (JSON.stringify(left) !== JSON.stringify(right)) {
    const actualSet = new Set(left);
    const expectedSet = new Set(right);
    const missing = right.filter((item) => !actualSet.has(item));
    const unexpected = left.filter((item) => !expectedSet.has(item));
    throw new Error(
      `${label} mismatch; missing=${missing.join(",")}; unexpected=${unexpected.join(",")}`,
    );
  }
}

async function pdfPages(file) {
  const info = await run("pdfinfo", [file], undefined, true);
  const match = info.match(/^Pages:\s+(\d+)$/m);
  if (!match) throw new Error(`Could not read PDF page count: ${file}`);
  return Number(match[1]);
}

async function scanPortableSources(archiveRoot, files) {
  const textExtensions = new Set([
    ".css",
    ".csv",
    ".html",
    ".js",
    ".json",
    ".md",
    ".py",
  ]);
  const forbidden = [
    [/\/Users\/alirahman/g, "user-specific path"],
    [/Desktop\/test/g, "desktop path"],
    [/\b(?:localhost|127\.0\.0\.1)\b/g, "local server"],
    [/https?:\/\/[^\s"')]+\/(?:releases\/v1\/(?:book\/images|originals)|artwork)\//g, "required HTTP artwork"],
  ];
  for (const relative of files) {
    let text;
    const extension = path.extname(relative).toLowerCase();
    if (textExtensions.has(extension)) {
      text = await readFile(path.join(archiveRoot, relative), "utf8");
    } else if (extension === ".idml") {
      text = await run(
        "unzip",
        ["-p", path.join(archiveRoot, relative)],
        archiveRoot,
        true,
      );
    } else {
      continue;
    }
    for (const [pattern, label] of forbidden) {
      pattern.lastIndex = 0;
      if (pattern.test(text)) {
        throw new Error(`${relative} contains a non-portable ${label}`);
      }
    }
  }
}

export async function validateMasterRelease({
  root = projectRoot,
  version = "v1",
} = {}) {
  const releaseRoot = path.join(root, "dist", "releases", version);
  const archive = path.join(releaseRoot, masterArchiveName(version));
  const sources = JSON.parse(
    await readFile(path.join(root, "content", "source-map.json"), "utf8"),
  );
  const temporary = await mkdtemp(path.join(tmpdir(), "revelation-master-"));
  const resolvedTmp = path.resolve(tmpdir());
  const resolvedTemporary = path.resolve(temporary);
  if (!resolvedTemporary.startsWith(`${resolvedTmp}${path.sep}`)) {
    throw new Error(`Refusing unsafe temporary directory: ${resolvedTemporary}`);
  }

  try {
    await run("unzip", ["-q", archive, "-d", temporary], root);
    const archiveRootName = `REVELATION-master-${version}`;
    const archiveRoot = path.join(temporary, archiveRootName);
    const files = (await walk(archiveRoot)).sort();
    const publishingFiles = await discoverPublishingFiles(
      path.join(archiveRoot, "publishing"),
    );
    const expected = masterEntryPaths(sources, version, publishingFiles).map(
      (entry) => entry.slice(archiveRootName.length + 1),
    );
    assertExact(files, expected, "master archive inventory");

    const checksumText = await readFile(
      path.join(archiveRoot, "SHA256SUMS.txt"),
      "utf8",
    );
    const checksumEntries = checksumText.trimEnd().split("\n").map((line) => {
      const match = line.match(/^([a-f0-9]{64})  (.+)$/);
      if (!match) throw new Error(`Invalid checksum line: ${line}`);
      return { checksum: match[1], relative: match[2] };
    });
    assertExact(
      checksumEntries.map(({ relative }) => relative),
      files.filter((file) => file !== "SHA256SUMS.txt"),
      "checksum inventory",
    );
    for (const { checksum, relative } of checksumEntries) {
      const actual = sha256(await readFile(path.join(archiveRoot, relative)));
      if (actual !== checksum) throw new Error(`${relative}: checksum mismatch`);
    }

    const officialPdf = "editions/REVELATION_web.pdf";
    const pages = await pdfPages(path.join(archiveRoot, officialPdf));
    if (pages !== 182) {
      throw new Error(`${officialPdf}: expected 182 pages, received ${pages}`);
    }
    for (const relative of files.filter((file) => file.endsWith(".pdf"))) {
      if (/MASTER ORIGINAL/i.test(relative)) {
        throw new Error(`Prohibited PDF filename: ${relative}`);
      }
      if (relative !== officialPdf) {
        const otherPages = await pdfPages(path.join(archiveRoot, relative));
        if (otherPages === 180) throw new Error(`Prohibited 180-page PDF: ${relative}`);
      }
    }
    if (files.some((file) => /MASTER ORIGINAL/i.test(file))) {
      throw new Error("Master archive contains a prohibited MASTER ORIGINAL file");
    }

    await scanPortableSources(archiveRoot, files);

    const markdown = await readFile(path.join(archiveRoot, "export.md"), "utf8");
    const imagePaths = [...markdown.matchAll(/^!\[[^\n]+\]\((artwork\/book-images\/[^)]+\.jpg)\)/gm)]
      .map((match) => match[1]);
    if (imagePaths.length !== 90 || new Set(imagePaths).size !== 90) {
      throw new Error("export.md must contain 90 unique bundle-relative artwork paths");
    }
    for (const relative of imagePaths) {
      await readFile(path.join(archiveRoot, relative));
    }

    const python = path.join("publishing", "book-source");
    await run(
      "python3",
      [
        path.join(python, "validate_idml.py"),
        path.join("publishing", "indesign", "REVELATION_13x11.idml"),
        "--archive-root",
        ".",
      ],
      archiveRoot,
    );
    await run(
      "python3",
      [
        path.join(python, "validate_idml.py"),
        path.join("publishing", "indesign", "REVELATION_cover.idml"),
        "--archive-root",
        ".",
      ],
      archiveRoot,
    );
    await run(
      "python3",
      [
        path.join(python, "validate_epub.py"),
        path.join("editions", "REVELATION_iPad_fixed.epub"),
        "fixed",
      ],
      archiveRoot,
    );
    await run(
      "python3",
      [
        path.join(python, "validate_epub.py"),
        path.join("editions", "REVELATION_reflowable.epub"),
        "reflowable",
      ],
      archiveRoot,
    );

    console.log(
      `Master release validated: ${files.length} files, 182-page official PDF, portable IDML, two valid EPUBs, and 90 relative Markdown images.`,
    );
    return { archive, files };
  } finally {
    await rm(resolvedTemporary, { recursive: true, force: true });
  }
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  await validateMasterRelease();
}
