import path from "node:path";

export function releasePaths(sceneId, extension) {
  const ext = extension.toLowerCase();
  return {
    original: `releases/v1/originals/${sceneId}${ext}`,
    preview: `releases/v1/web/640/${sceneId}.webp`,
    reader: `releases/v1/web/1920/${sceneId}.webp`,
    book: `releases/v1/book/images/${sceneId}.jpg`,
  };
}

export function contentTypeFor(filePath) {
  return ({
    ".avif": "image/avif",
    ".csv": "text/csv; charset=utf-8",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ".epub": "application/epub+zip",
    ".gif": "image/gif",
    ".html": "text/html; charset=utf-8",
    ".idml": "application/vnd.adobe.indesign-idml-package",
    ".indd": "application/x-indesign",
    ".jpeg": "image/jpeg",
    ".jpg": "image/jpeg",
    ".js": "text/javascript; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".md": "text/markdown; charset=utf-8",
    ".pdf": "application/pdf",
    ".png": "image/png",
    ".py": "text/x-python; charset=utf-8",
    ".txt": "text/plain; charset=utf-8",
    ".ttf": "font/ttf",
    ".webp": "image/webp",
    ".woff2": "font/woff2",
    ".zip": "application/zip",
  })[path.extname(filePath).toLowerCase()] ?? "application/octet-stream";
}

export function contentDispositionFor(filePath) {
  const normalized = filePath.split(path.sep).join("/");
  const publishingBinary = /\.(?:docx|epub|idml|indd|pdf)$/i.test(normalized);
  if (
    !normalized.includes("/originals/") &&
    !normalized.endsWith(".zip") &&
    !publishingBinary
  ) {
    return undefined;
  }
  return `attachment; filename="${path.basename(filePath)}"`;
}

export function expectedReleaseFiles(sources) {
  return {
    originals: sources.map(({ id, originalExtension }) => `${id}${originalExtension}`).sort(),
    previews: sources.map(({ id }) => `${id}.webp`).sort(),
    readers: sources.map(({ id }) => `${id}.webp`).sort(),
    books: sources.map(({ id }) => `${id}.jpg`).sort(),
  };
}

export function validateReleaseInventory(inventory) {
  const expected = {
    originals: 90,
    previews: 90,
    readers: 90,
    books: 90,
    zipFiles: 95,
    archiveOriginals: 90,
  };
  for (const [label, count] of Object.entries(expected)) {
    if (inventory[label] !== count) {
      const readableLabel = label.replace(/([A-Z])/g, " $1").toLowerCase();
      throw new Error(`${readableLabel}: expected ${count}, received ${inventory[label]}`);
    }
  }
}
