import { mkdtemp, mkdir, readFile, rm } from "node:fs/promises";
import { tmpdir } from "node:os";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { spawn } from "node:child_process";

import { masterArchiveName } from "./lib/master-release.mjs";

const projectRoot = path.resolve(import.meta.dirname, "..");
const markdownFormat =
  "markdown+yaml_metadata_block+bracketed_spans+link_attributes";

export function rebuildCommands(root) {
  const cwd = path.resolve(root);
  return [
    {
      name: "docx",
      command: "pandoc",
      cwd,
      args: [
        "export.md",
        `--from=${markdownFormat}`,
        "--standalone",
        "--toc",
        "--reference-doc=publishing/reference/red-letter-reference.docx",
        "--resource-path=.",
        "--output=build/verify/revelation.docx",
      ],
      output: "build/verify/revelation.docx",
    },
    {
      name: "pandoc-epub",
      command: "pandoc",
      cwd,
      args: [
        "export.md",
        `--from=${markdownFormat}`,
        "--standalone",
        "--toc",
        "--split-level=2",
        "--resource-path=.",
        "--output=build/verify/revelation-pandoc.epub",
      ],
      output: "build/verify/revelation-pandoc.epub",
    },
    {
      name: "pandoc-pdf",
      command: "pandoc",
      cwd,
      args: [
        "export.md",
        `--from=${markdownFormat}`,
        "--to=html5",
        "--standalone",
        "--toc",
        "--resource-path=.",
        "--pdf-engine=weasyprint",
        "--output=build/verify/revelation-pandoc.pdf",
      ],
      output: "build/verify/revelation-pandoc.pdf",
    },
    {
      name: "designed-pdf",
      command: "python3",
      cwd,
      args: ["publishing/book-source/render.py"],
      output: "build/REVELATION_web.pdf",
    },
    {
      name: "idml",
      command: "python3",
      cwd,
      args: ["publishing/book-source/build_idml.py"],
      output: "build/REVELATION_13x11.idml",
    },
    {
      name: "fixed-epub",
      command: "python3",
      cwd,
      args: [
        "publishing/book-source/make_epub_fixed.py",
        "build/epub_pages",
      ],
      output: "build/REVELATION_iPad_fixed.epub",
    },
    {
      name: "reflowable-epub",
      command: "python3",
      cwd,
      args: ["publishing/book-source/make_epub_reflow.py"],
      output: "build/REVELATION_reflowable.epub",
    },
  ];
}

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

async function requireCommand(command) {
  try {
    await run("which", [command], projectRoot, true);
  } catch {
    throw new Error(`Required rebuild command is missing: ${command}`);
  }
}

async function requirePythonModules() {
  try {
    await run("python3", ["-c", "import PIL, playwright"], projectRoot, true);
  } catch {
    throw new Error(
      "Required Python modules are missing: install Pillow and Playwright, then install Playwright Chromium",
    );
  }
}

export function assertPlateStatuses(html) {
  const registerRows = [
    ...html.matchAll(
      /<div class="reg"><span class="k">([^<]+)<\/span>[\s\S]*?<span class="s (survives|frag|lost)">/g,
    ),
  ];
  if (registerRows.length !== 90) {
    throw new Error(
      `Rebuilt designed edition requires 90 survival labels, received ${registerRows.length}`,
    );
  }
  const labels = new Map(registerRows.map((match) => [match[1], match[2]]));
  if (labels.get("T1-T01") !== "survives") {
    throw new Error("Rebuilt designed edition lost the tracked T1-T01 survival label");
  }
}

function inside(root, relative) {
  const resolvedRoot = path.resolve(root);
  const output = path.resolve(resolvedRoot, relative);
  if (!output.startsWith(`${resolvedRoot}${path.sep}`)) {
    throw new Error(`Rebuild output escapes the extraction root: ${relative}`);
  }
  return output;
}

async function pdfPages(file) {
  const output = await run("pdfinfo", [file], undefined, true);
  const match = output.match(/^Pages:\s+(\d+)$/m);
  if (!match) throw new Error(`Could not read PDF page count: ${file}`);
  return Number(match[1]);
}

async function assertDocx(docx) {
  const entries = await run("unzip", ["-Z1", docx], undefined, true);
  const media = entries
    .split("\n")
    .filter((entry) => /^word\/media\/.*\.jpg$/i.test(entry));
  if (media.length !== 90) {
    throw new Error(`Rebuilt DOCX requires 90 JPEGs, received ${media.length}`);
  }
  const styles = await run(
    "unzip",
    ["-p", docx, "word/styles.xml"],
    undefined,
    true,
  );
  if (!/w:styleId="WordsofJesus"/.test(styles) || !/w:color w:val="9B1C31"/.test(styles)) {
    throw new Error("Rebuilt DOCX is missing the crimson Words of Jesus style");
  }
}

export async function verifyMasterRebuild({
  root = projectRoot,
  version = "v1",
  keep = false,
} = {}) {
  for (const command of ["pandoc", "weasyprint", "python3", "pdfinfo"]) {
    await requireCommand(command);
  }
  await requirePythonModules();
  const temporary = await mkdtemp(path.join(tmpdir(), "revelation-rebuild-"));
  const resolvedTmp = path.resolve(tmpdir());
  const resolvedTemporary = path.resolve(temporary);
  if (!resolvedTemporary.startsWith(`${resolvedTmp}${path.sep}`)) {
    throw new Error(`Refusing unsafe temporary directory: ${resolvedTemporary}`);
  }

  let extractionRoot;
  try {
    const archive = path.join(
      root,
      "dist",
      "releases",
      version,
      masterArchiveName(version),
    );
    await run("unzip", ["-q", archive, "-d", temporary], root);
    extractionRoot = path.join(temporary, `REVELATION-master-${version}`);
    await mkdir(inside(extractionRoot, "build/verify"), { recursive: true });
    const commands = rebuildCommands(extractionRoot);
    for (const command of commands) inside(extractionRoot, command.output);

    for (const command of commands.slice(0, 3)) {
      await run(command.command, command.args, command.cwd);
    }

    await run(
      "python3",
      ["publishing/book-source/build.py"],
      extractionRoot,
    );
    assertPlateStatuses(
      await readFile(inside(extractionRoot, "build/book.html"), "utf8"),
    );
    await run(
      commands[3].command,
      commands[3].args,
      commands[3].cwd,
    );

    await run(
      commands[4].command,
      commands[4].args,
      commands[4].cwd,
    );
    await run(
      "python3",
      ["publishing/book-source/build_cover_idml.py", "164"],
      extractionRoot,
    );
    for (const file of ["REVELATION_13x11.idml", "REVELATION_cover.idml"]) {
      await run(
        "python3",
        [
          "publishing/book-source/validate_idml.py",
          `build/${file}`,
          "--archive-root",
          ".",
        ],
        extractionRoot,
      );
    }

    await run(
      "python3",
      ["publishing/book-source/render_pages.py", "1560"],
      extractionRoot,
    );
    await run(
      commands[5].command,
      commands[5].args,
      commands[5].cwd,
    );
    await run(
      "python3",
      [
        "publishing/book-source/validate_epub.py",
        "build/REVELATION_iPad_fixed.epub",
        "fixed",
      ],
      extractionRoot,
    );

    await run(
      commands[6].command,
      commands[6].args,
      commands[6].cwd,
    );
    await run(
      "python3",
      [
        "publishing/book-source/validate_epub.py",
        "build/REVELATION_reflowable.epub",
        "reflowable",
      ],
      extractionRoot,
    );

    await assertDocx(inside(extractionRoot, commands[0].output));
    await run(
      "unzip",
      ["-tq", inside(extractionRoot, commands[1].output)],
      extractionRoot,
    );
    const designedPages = await pdfPages(
      inside(extractionRoot, commands[3].output),
    );
    if (designedPages !== 182) {
      throw new Error(
        `Rebuilt designed PDF requires 182 pages, received ${designedPages}`,
      );
    }
    await pdfPages(inside(extractionRoot, commands[2].output));

    const observed = await Promise.all(
      ["pandoc", "weasyprint", "python3", "pdfinfo"].map(async (command) => ({
        command,
        path: (await run("which", [command], extractionRoot, true)).trim(),
      })),
    );
    console.log(
      `Offline rebuild verified at ${extractionRoot}: DOCX (90 images + red letters), Pandoc EPUB/PDF, 182-page designed PDF, portable IDML, fixed EPUB, and reflowable EPUB.`,
    );
    console.log(`Tool paths: ${observed.map(({ command, path: value }) => `${command}=${value}`).join("; ")}`);
    return { extractionRoot, commands };
  } finally {
    if (!keep) await rm(resolvedTemporary, { recursive: true, force: true });
    else if (extractionRoot) console.log(`Kept verification extraction: ${extractionRoot}`);
  }
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  await verifyMasterRebuild({ keep: process.argv.includes("--keep") });
}
