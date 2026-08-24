# Revelation Print Edition, Remix, and Homepage Hero Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add an editorial Print Edition route, an open-source Remix route, and an accessible rotating homepage hero while making **Revelation** the singular project name everywhere.

**Architecture:** Keep all pages server-rendered except one focused `HomeHeroCarousel` client boundary. Reuse canonical `Scene` data and the existing `ArtworkImage` delivery path for both the homepage and Print Edition imagery; keep outbound URLs in `lib/content.ts`. Preserve the current release pipeline while renaming its project artifacts and public storage contract to singular names.

**Tech Stack:** Next.js 16 App Router, React 19, TypeScript 5.9, CSS Modules, Node's built-in test runner, Playwright, existing R2 release tooling.

**Spec:** `docs/superpowers/specs/2026-08-24-print-edition-remix-and-hero-design.md`

## Global Constraints

- Work on the existing `codex/print-edition-remix` branch in the current checkout; do not create a worktree.
- The canonical title is **Revelation**, singular. Project-name, repository, artifact, storage, generated-graph, and documentation references must contain no pluralized project name.
- Use `/print-edition/` with nav label **Print Edition** and `/remix/` with nav label **Remix**.
- Blurb remains the source of truth for price; do not display a price or add checkout.
- Keep the archive download direct for now; do not add an email form or provider.
- Do not add Amazon until a real listing URL exists.
- Use canonical source artwork, not PDF-derived images or simulated book photography.
- Add no dependencies, CMS, carousel library, analytics funnel, or new license.
- Keep the homepage and new routes server components; only the carousel is a client component.
- Preserve the pre-existing unstaged `next-env.d.ts` change and do not include it in task commits.
- Prefix shell commands with `rtk`, per `/Users/alirahman/.codex/RTK.md`.
- Follow the bundled Next.js 16 guidance already reviewed under `node_modules/next/dist/docs/01-app/`: pages use App Router `page.tsx`, static metadata stays in server components, interactive state lives behind a narrow `"use client"` boundary, and route-specific styling uses CSS Modules.

---

### Task 1: Establish the singular branding and release contract

**Files:**
- Modify: `package.json`
- Modify: `package-lock.json`
- Modify: `.env.example`
- Modify: `app/layout.tsx`
- Modify: `components/SiteHeader.tsx`
- Modify: `lib/content.ts`
- Modify: `scripts/build-release.mjs`
- Modify: `scripts/lib/master-release.mjs`
- Modify: `scripts/validate-release.mjs`
- Modify: `scripts/verify-master-rebuild.mjs`
- Modify: `test/release-lib.test.mjs`
- Modify: `test/master-release.test.mjs`
- Rename ignored source artifact: the current pluralized DOCX filename → `publishing/editions/revelation.docx`

**Interfaces:**
- Produces: `repositoryUrl: string`, `blurbBookUrl: string`, singular `archiveUrl`, and unchanged `masterArchiveUrl` from `lib/content.ts`.
- Produces: `officialEditions["revelation.docx"] === "revelation.docx"`.
- Produces: artwork archive `revelation-artwork-v1.zip`; the master archive remains `REVELATION-master-v1.zip`.

- [ ] **Step 1: Change the release tests first**

Update `test/release-lib.test.mjs` so the attachment assertion requires the singular archive:

```js
assert.equal(
  contentDispositionFor("releases/v1/revelation-artwork-v1.zip"),
  'attachment; filename="revelation-artwork-v1.zip"',
);
```

Import `officialEditions` in `test/master-release.test.mjs` and add:

```js
test("master archive uses the singular editable edition name", () => {
  assert.equal(officialEditions["revelation.docx"], "revelation.docx");
});
```

- [ ] **Step 2: Run the focused tests and verify they fail**

Run:

```bash
rtk node --disable-warning=MODULE_TYPELESS_PACKAGE_JSON --test test/release-lib.test.mjs test/master-release.test.mjs
```

Expected: FAIL because the release path and `officialEditions` still use the old plural artifact.

- [ ] **Step 3: Apply the minimal singular release and branding changes**

Use these exact shared constants in `lib/content.ts`:

```ts
export const archiveUrl = assetUrl(
  `releases/${contentVersion}/revelation-artwork-${contentVersion}.zip`,
);
export const masterArchiveUrl = assetUrl(
  `releases/${contentVersion}/REVELATION-master-${contentVersion}.zip`,
);
export const blurbPreviewUrl =
  "https://www.blurb.com/bookshare/app/index.html?bookId=12978394";
export const blurbBookUrl =
  "https://www.blurb.com/b/12978394-revelation";
export const repositoryUrl =
  "https://github.com/Divergent-World/Revelation";
```

Make the root metadata singular:

```ts
export const metadata: Metadata = {
  title: {
    default: "Revelation — A Prophecy in Six Movements",
    template: "%s — Revelation",
  },
  description:
    "An illuminated reading of the Book of Revelation as a prophecy in six movements by Ali Rahman / Divergent World.",
};
```

Make the header wordmark and accessible name singular, while leaving the existing three-link navigation structure for Task 2:

```tsx
<Link className="wordmark" href="/" aria-label="Revelation home">
  <span>Revelation</span>
  <small>A Divergent World exhibition</small>
</Link>
```

Import `repositoryUrl` from `@/lib/content` and point the temporary **Source** link at `href={repositoryUrl}`; Task 2 will replace that external nav item with **Remix**.

Change the package name to `"revelation"` in both package files. Change the example bucket to `R2_BUCKET=revelation-artwork`.

In the release scripts, replace every project artifact path with:

```js
"revelation-artwork-v1.zip"
"revelation.docx"
"build/verify/revelation.docx"
"build/verify/revelation-pandoc.epub"
"build/verify/revelation-pandoc.pdf"
```

Update the generated artwork archive README heading to `Revelation Artwork v1`. Do not rename the already-singular uppercase `REVELATION_*` designed-edition artifacts.

Rename the ignored binary without copying it:

```bash
rtk mv publishing/editions/revelation"s".docx publishing/editions/revelation.docx
```

- [ ] **Step 4: Run the focused tests and confirm the core code has no plural name**

Run:

```bash
rtk node --disable-warning=MODULE_TYPELESS_PACKAGE_JSON --test test/release-lib.test.mjs test/master-release.test.mjs
rtk rg -n -i "revelation[s]" package.json package-lock.json .env.example app/layout.tsx components/SiteHeader.tsx lib/content.ts scripts test
```

Expected: tests PASS; the search exits 1 with no matches.

- [ ] **Step 5: Commit only Task 1 files**

```bash
rtk git add package.json package-lock.json .env.example app/layout.tsx components/SiteHeader.tsx lib/content.ts scripts test
rtk git commit -m "chore: make Revelation the canonical project name"
```

Do not stage `next-env.d.ts` or the ignored DOCX.

---

### Task 2: Move the open-source material to the Remix route

**Files:**
- Create: `app/remix/page.tsx`
- Create: `app/remix/page.module.css`
- Modify: `components/SiteHeader.tsx`
- Modify: `app/page.tsx`
- Modify: `app/page.module.css`
- Modify: `e2e/exhibition.spec.ts`

**Interfaces:**
- Consumes: `masterArchiveUrl` and `repositoryUrl` from Task 1.
- Produces: static server route `/remix/`.
- Produces: global nav order `Movements · Read · Print Edition · Remix`.
- Produces: homepage with no archive, source, Blurb, or export section.

- [ ] **Step 1: Replace the old homepage archive E2E expectations with Remix expectations**

Replace the first two archive-focused tests in `e2e/exhibition.spec.ts` with:

```ts
test("moves archive and source access to Remix", async ({ page }) => {
  await page.goto("/");
  await expect(
    page.getByRole("link", { name: "Download Master Archive" }),
  ).toHaveCount(0);
  await expect(page.getByTitle("Preview Revelation on Blurb")).toHaveCount(0);
  await expect(page.locator("section[aria-labelledby='archive-title']")).toHaveCount(0);

  await page.getByRole("link", { name: "Remix" }).click();
  await expect(page).toHaveURL(/\/remix\/$/);
  await expect(
    page.getByRole("link", { name: "Download Master Archive" }),
  ).toHaveAttribute("href", /releases\/v1\/REVELATION-master-v1\.zip$/);
  await expect(
    page.getByRole("link", { name: "View Source on GitHub" }),
  ).toHaveAttribute(
    "href",
    "https://github.com/Divergent-World/Revelation",
  );
  await expect(
    page.getByRole("link", { name: "Download the scripture manuscript" }),
  ).toHaveAttribute("href", "/export.md");
});

test("keeps Remix actions aligned without overflow", async ({ page }) => {
  await page.goto("/remix/");
  const actions = page.locator("[data-remix-actions]");
  const geometry = await actions.evaluate((node) => {
    const buttons = [...node.querySelectorAll<HTMLElement>("a.button")].map(
      (button) => {
        const { width, height } = button.getBoundingClientRect();
        return { width, height };
      },
    );
    return {
      buttons,
      overflow: document.documentElement.scrollWidth - window.innerWidth,
    };
  });
  expect(geometry.buttons).toHaveLength(2);
  expect(
    Math.max(...geometry.buttons.map(({ height }) => height)) -
      Math.min(...geometry.buttons.map(({ height }) => height)),
  ).toBeLessThanOrEqual(1);
  expect(geometry.overflow).toBeLessThanOrEqual(1);
});
```

- [ ] **Step 2: Run the targeted E2E tests and verify they fail**

Run:

```bash
rtk npm run build
rtk npx playwright test e2e/exhibition.spec.ts --grep "Remix|archive and source"
```

Expected: FAIL because `/remix/` and the Remix nav link do not exist.

- [ ] **Step 3: Add the Remix page and its scoped styles**

Create `app/remix/page.tsx` as a server component with static metadata:

```tsx
import type { Metadata } from "next";

import { masterArchiveUrl, repositoryUrl } from "@/lib/content";
import styles from "./page.module.css";

export const metadata: Metadata = {
  title: "Remix",
  description:
    "Study, rebuild, and remix the Revelation artwork, canonical content, and publishing sources.",
};

export default function RemixPage() {
  return (
    <div className={styles.page}>
      <header className={styles.hero}>
        <p className="eyebrow">Open source · Edition v1</p>
        <h1>Study the work. Rebuild it. Make something new.</h1>
        <p>
          Revelation is published as more than a finished exhibition. Its
          canonical content, artwork, and publishing sources are available for
          study and reuse under the terms included with the project.
        </p>
      </header>

      <section className={styles.archive} aria-labelledby="remix-archive">
        <div>
          <p className="eyebrow">Master archive</p>
          <h2 id="remix-archive">The complete project, in one place.</h2>
          <p>
            The self-contained archive includes the official 182-page book,
            fixed and reflowable EPUB editions, editable DOCX, all ninety
            artworks, canonical content, portable InDesign sources, fonts, and
            rebuild instructions.
          </p>
          <p className={styles.note}>
            1.6 GB · 182-page PDF · fixed and reflowable EPUB · editable
            publishing source
          </p>
        </div>
        <div className={styles.actions} data-remix-actions>
          <a className="button button-primary" href={masterArchiveUrl}>
            Download Master Archive
          </a>
          <a className="button" href={repositoryUrl}>
            View Source on GitHub
          </a>
        </div>
      </section>

      <section className={styles.manuscript} aria-labelledby="remix-manuscript">
        <p className="eyebrow">Smaller export</p>
        <h2 id="remix-manuscript">Only need the manuscript?</h2>
        <p>
          The standalone Markdown edition keeps the scripture text and all
          ninety canonical artwork references in a portable text-first format.
        </p>
        <a href="/export.md" download>
          Download the scripture manuscript
        </a>
      </section>
    </div>
  );
}
```

In `app/remix/page.module.css`, define actual route-scoped layout rules:

```css
.page { overflow: clip; }
.hero, .archive, .manuscript {
  width: min(100%, 92rem);
  margin: auto;
  padding-inline: clamp(1rem, 7vw, 7rem);
}
.hero { padding-block: clamp(6rem, 12vw, 11rem); }
.hero h1 { max-width: 12ch; }
.hero > p:last-child, .archive p, .manuscript p {
  max-width: 48rem;
  color: var(--muted);
  font: 1.15rem/1.7 var(--font-display), serif;
}
.archive {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(18rem, 28rem);
  gap: clamp(3rem, 7vw, 7rem);
  align-items: center;
  padding-block: clamp(5rem, 10vw, 9rem);
  border-block: 1px solid var(--line);
}
.actions { display: grid; gap: .8rem; }
.actions a { width: 100%; padding-inline: 1rem; }
.note { font-size: .67rem !important; letter-spacing: .1em; text-transform: uppercase; }
.manuscript { padding-block: clamp(5rem, 9vw, 8rem); }
.manuscript a { color: var(--gold); text-decoration: underline; text-underline-offset: .25em; }
@media (max-width: 760px) {
  .archive { grid-template-columns: 1fr; }
}
```

- [ ] **Step 4: Update global navigation and remove the homepage block**

Use internal `Link` components in `SiteHeader.tsx`:

```tsx
<nav aria-label="Primary navigation">
  <Link href="/tapestries/1/">Movements</Link>
  <Link href="/revelation/">Read</Link>
  <Link href="/print-edition/">Print Edition</Link>
  <Link href="/remix/">Remix</Link>
</nav>
```

From `app/page.tsx`, remove the archive section and its `blurbPreviewUrl` and `masterArchiveUrl` imports. From `app/page.module.css`, remove every `.archive*`, `.blurb*`, `.exportNote`, and `.compatibilityNote` rule, and remove `.archive` from shared selector lists and media-query declarations.

Add this narrow-header rule in `app/globals.css` so all four links remain usable on phones:

```css
@media (max-width: 640px) {
  .site-header { align-items: flex-start; flex-direction: column; gap: 1rem; }
  .site-header nav { width: 100%; gap: .7rem 1.2rem; flex-wrap: wrap; }
}
```

- [ ] **Step 5: Run the focused E2E tests and commit**

Run:

```bash
rtk npm run build
rtk npx playwright test e2e/exhibition.spec.ts --grep "Remix|archive and source"
```

Expected: PASS in Chromium and mobile.

Commit:

```bash
rtk git add app/page.tsx app/page.module.css app/remix components/SiteHeader.tsx app/globals.css e2e/exhibition.spec.ts
rtk git commit -m "feat: add open-source Remix route"
```

---

### Task 3: Build the editorial Print Edition route with canonical artwork

**Files:**
- Create: `app/print-edition/page.tsx`
- Create: `app/print-edition/page.module.css`
- Modify: `e2e/exhibition.spec.ts`

**Interfaces:**
- Consumes: `getScene`, `Scene`, `ArtworkImage`, `blurbBookUrl`, and `blurbPreviewUrl`.
- Produces: static server route `/print-edition/`.
- Produces: one hero scene `T6-B03` and artwork sequence `T1-B04`, `T3-T07`, `T5-B02`, `T6-B05`.

- [ ] **Step 1: Add failing route, content, link, and geometry tests**

Add to `e2e/exhibition.spec.ts`:

```ts
test("presents the 182-page Print Edition without a local price", async ({ page }) => {
  await page.goto("/print-edition/");
  await expect(
    page.getByRole("heading", { name: "Revelation: An Illuminated Prophecy" }),
  ).toBeVisible();
  await expect(page.getByText("182 pages", { exact: true })).toBeVisible();
  await expect(
    page.getByRole("link", { name: "View on Blurb" }).first(),
  ).toHaveAttribute("href", "https://www.blurb.com/b/12978394-revelation");
  await expect(page.getByTitle("Preview Revelation on Blurb")).toHaveAttribute(
    "src",
    "https://www.blurb.com/bookshare/app/index.html?bookId=12978394",
  );
  await expect(page.getByText(/\$310|US \$/)).toHaveCount(0);
  await expect(page.locator("[data-edition-artwork]")).toHaveCount(5);
});

test("keeps the Print Edition preview proportional and on-screen", async ({ page }) => {
  await page.goto("/print-edition/");
  const geometry = await page.locator("[data-blurb-frame]").evaluate((frame) => {
    const preview = frame.querySelector("iframe")!.getBoundingClientRect();
    return {
      overflow: document.documentElement.scrollWidth - window.innerWidth,
      width: preview.width,
      ratio: preview.width / preview.height,
    };
  });
  expect(geometry.overflow).toBeLessThanOrEqual(1);
  expect(geometry.width).toBeLessThanOrEqual(800);
  expect(geometry.ratio).toBeCloseTo(16 / 9, 1);
});
```

- [ ] **Step 2: Run the targeted E2E tests and verify they fail**

Run:

```bash
rtk npm run build
rtk npx playwright test e2e/exhibition.spec.ts --grep "Print Edition"
```

Expected: FAIL because `/print-edition/` does not exist.

- [ ] **Step 3: Create the server-rendered Print Edition page**

Create `app/print-edition/page.tsx` with static metadata, exact scene IDs, and no price:

```tsx
import type { Metadata } from "next";

import { ArtworkImage } from "@/components/ArtworkImage";
import {
  blurbBookUrl,
  blurbPreviewUrl,
  getScene,
  type Scene,
} from "@/lib/content";
import styles from "./page.module.css";

export const metadata: Metadata = {
  title: "Print Edition",
  description:
    "The 182-page hardcover collector's edition of Revelation: An Illuminated Prophecy.",
};

function requiredScene(id: string): Scene {
  const scene = getScene(id);
  if (!scene) throw new Error(`Print Edition scene missing: ${id}`);
  return scene;
}

const hero = requiredScene("T6-B03");
const gallery = ["T1-B04", "T3-T07", "T5-B02", "T6-B05"].map(requiredScene);

function EditionArtwork({ scene, eager = false }: { scene: Scene; eager?: boolean }) {
  return (
    <figure className={styles.artwork} data-edition-artwork data-scene-id={scene.id}>
      <div><ArtworkImage scene={scene} size="reader" eager={eager} /></div>
      <figcaption>
        <span>{scene.id}</span>
        <strong>{scene.title}</strong>
        <small>{scene.displayReference}</small>
      </figcaption>
    </figure>
  );
}

export default function PrintEditionPage() {
  return (
    <div className={styles.page}>
      <section className={styles.hero} aria-labelledby="edition-title">
        <div className={styles.heroCopy}>
          <p className="eyebrow">Collector's print edition · 182 pages</p>
          <h1 id="edition-title">Revelation: An Illuminated Prophecy</h1>
          <p>
            Ninety illuminated compartments, restored to their original order
            and gathered into a large-format landscape volume.
          </p>
          <a className="button button-primary" href={blurbBookUrl}>View on Blurb</a>
        </div>
        <EditionArtwork scene={hero} eager />
      </section>

      <section className={styles.story} aria-labelledby="edition-story">
        <p className="eyebrow">The complete sequence</p>
        <h2 id="edition-story">A work made to be encountered at the scale of a book.</h2>
        <p>
          The edition rebuilds all ninety Apocalypse tapestry compartments in
          sequence and marks whether each image survives, survives in
          fragments, or has been reconstructed.
        </p>
      </section>

      <section className={styles.gallery} aria-label="Selected artwork from the edition">
        {gallery.map((scene) => <EditionArtwork key={scene.id} scene={scene} />)}
      </section>

      <section className={styles.details} aria-labelledby="edition-details">
        <div>
          <p className="eyebrow">Edition details</p>
          <h2 id="edition-details">The physical edition</h2>
        </div>
        <dl>
          <div><dt>Extent</dt><dd>182 pages</dd></div>
          <div><dt>Binding</dt><dd>Hardcover, ImageWrap</dd></div>
          <div><dt>Format</dt><dd>Large-format landscape</dd></div>
          <div><dt>Dimensions</dt><dd>13 × 11 in / 33 × 28 cm</dd></div>
        </dl>
      </section>

      <section className={styles.preview} aria-labelledby="edition-preview">
        <div>
          <p className="eyebrow">Look inside</p>
          <h2 id="edition-preview">Preview the edition on Blurb.</h2>
          <p>Blurb shows current availability and pricing.</p>
          <a className="button" href={blurbBookUrl}>View on Blurb</a>
        </div>
        <div className={styles.blurbFrame} data-blurb-frame>
          <iframe
            title="Preview Revelation on Blurb"
            src={blurbPreviewUrl}
            loading="lazy"
            allowFullScreen
          />
        </div>
      </section>
    </div>
  );
}
```

- [ ] **Step 4: Add the print page's scoped editorial CSS**

Create `app/print-edition/page.module.css` with these concrete layout invariants:

```css
.page { overflow: clip; }
.hero, .story, .gallery, .details, .preview {
  width: min(100%, 100rem);
  margin: auto;
  padding-inline: clamp(1rem, 7vw, 8rem);
}
.hero {
  display: grid;
  grid-template-columns: minmax(18rem, .8fr) minmax(0, 1.2fr);
  gap: clamp(3rem, 7vw, 8rem);
  align-items: center;
  min-height: calc(100svh - 5.5rem);
  padding-block: clamp(5rem, 10vw, 9rem);
}
.heroCopy h1 { max-width: 11ch; }
.heroCopy > p:not(.eyebrow), .story > p:last-child, .preview p {
  max-width: 46rem;
  color: var(--muted);
  font: 1.15rem/1.7 var(--font-display), serif;
}
.heroCopy .button { margin-top: 1.5rem; }
.artwork { margin: 0; min-width: 0; }
.artwork > div {
  display: grid;
  aspect-ratio: 16 / 9;
  place-items: center;
  overflow: hidden;
  background: #07090c;
  border: 1px solid rgba(214, 187, 120, .35);
}
.artwork img, .artwork > div > div { width: 100%; height: 100%; object-fit: contain; }
.artwork figcaption {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: .25rem 1rem;
  padding-top: .9rem;
}
.artwork figcaption span { grid-row: 1 / 3; color: var(--gold); font-size: .62rem; }
.artwork figcaption strong { font: 1.15rem/1.1 var(--font-display), serif; }
.artwork figcaption small { color: var(--muted); }
.story { max-width: 74rem; padding-block: clamp(6rem, 11vw, 10rem); }
.gallery {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: clamp(3rem, 7vw, 7rem) clamp(1rem, 3vw, 3rem);
  padding-bottom: clamp(6rem, 12vw, 11rem);
}
.details {
  display: grid;
  grid-template-columns: 1fr 1.2fr;
  gap: clamp(2rem, 6vw, 6rem);
  padding-block: clamp(5rem, 9vw, 8rem);
  color: #17130d;
  background: #eee7d8;
}
.details dl { margin: 0; border-top: 1px solid rgba(23, 19, 13, .25); }
.details dl div {
  display: grid;
  grid-template-columns: 10rem 1fr;
  padding-block: 1rem;
  border-bottom: 1px solid rgba(23, 19, 13, .25);
}
.details dd { margin: 0; font-family: var(--font-display), serif; }
.preview {
  display: grid;
  grid-template-columns: minmax(16rem, .6fr) minmax(0, 1fr);
  gap: clamp(3rem, 7vw, 7rem);
  align-items: center;
  padding-block: clamp(6rem, 12vw, 11rem);
}
.blurbFrame {
  width: 100%;
  max-width: 50rem;
  padding: clamp(.55rem, 1vw, .85rem);
  border: 1px solid rgba(214, 187, 120, .32);
  background: rgba(7, 9, 12, .72);
}
.blurbFrame iframe { display: block; width: 100%; aspect-ratio: 16 / 9; border: 0; background: #0b0e12; }
@media (max-width: 760px) {
  .hero, .details, .preview { grid-template-columns: 1fr; min-height: auto; }
  .gallery { grid-template-columns: 1fr; }
  .details dl div { grid-template-columns: 7rem 1fr; }
}
```

- [ ] **Step 5: Run focused tests and commit**

Run:

```bash
rtk npm run build
rtk npx playwright test e2e/exhibition.spec.ts --grep "Print Edition"
```

Expected: PASS in Chromium and mobile.

Commit:

```bash
rtk git add app/print-edition e2e/exhibition.spec.ts
rtk git commit -m "feat: add editorial Print Edition route"
```

---

### Task 4: Replace the homepage hero image with the accessible carousel

**Files:**
- Create: `components/HomeHeroCarousel.tsx`
- Create: `components/HomeHeroCarousel.module.css`
- Modify: `app/page.tsx`
- Modify: `app/page.module.css`
- Modify: `e2e/exhibition.spec.ts`

**Interfaces:**
- Consumes: serializable `Scene[]` from the homepage server component.
- Produces: `HomeHeroCarousel({ scenes }: { scenes: Scene[] })`.
- Produces: `data-active-scene` on the carousel and `data-scene-id` on each slide for deterministic E2E checks.
- Uses: fixed rotation interval `8_000` milliseconds.

- [ ] **Step 1: Add failing carousel behavior tests**

Add to `e2e/exhibition.spec.ts`:

```ts
test("rotates the six-scene homepage carousel every eight seconds", async ({ page }) => {
  await page.clock.install();
  await page.goto("/");
  const carousel = page.getByRole("region", { name: "Featured Revelation artwork" });
  await expect(carousel.locator("[data-scene-id]")).toHaveCount(6);
  await expect(carousel).toHaveAttribute("data-active-scene", "T1-B04");
  await page.clock.fastForward(8_000);
  await expect(carousel).toHaveAttribute("data-active-scene", "T2-B03");
  await page.getByRole("button", { name: "Previous artwork" }).click();
  await expect(carousel).toHaveAttribute("data-active-scene", "T1-B04");
});

test("pauses carousel rotation during interaction", async ({ page }) => {
  await page.clock.install();
  await page.goto("/");
  const carousel = page.getByRole("region", { name: "Featured Revelation artwork" });
  await carousel.hover();
  await page.clock.fastForward(16_000);
  await expect(carousel).toHaveAttribute("data-active-scene", "T1-B04");
  await page.mouse.move(0, 0);
  await page.clock.fastForward(8_000);
  await expect(carousel).toHaveAttribute("data-active-scene", "T2-B03");
});

test("disables automatic carousel motion for reduced motion", async ({ page }) => {
  await page.clock.install();
  await page.emulateMedia({ reducedMotion: "reduce" });
  await page.goto("/");
  const carousel = page.getByRole("region", { name: "Featured Revelation artwork" });
  await page.clock.fastForward(16_000);
  await expect(carousel).toHaveAttribute("data-active-scene", "T1-B04");
  await page.getByRole("button", { name: /Show artwork 6:/ }).click();
  await expect(carousel).toHaveAttribute("data-active-scene", "T6-B03");
});
```

- [ ] **Step 2: Run the carousel tests and verify they fail**

Run:

```bash
rtk npm run build
rtk npx playwright test e2e/exhibition.spec.ts --grep "carousel"
```

Expected: FAIL because the homepage still renders one static feature.

- [ ] **Step 3: Implement the minimal client carousel**

Create `components/HomeHeroCarousel.tsx`:

```tsx
"use client";

import { useEffect, useState } from "react";

import { ArtworkImage } from "@/components/ArtworkImage";
import type { Scene } from "@/lib/content";
import styles from "./HomeHeroCarousel.module.css";

const ROTATION_MS = 8_000;

export function HomeHeroCarousel({ scenes }: { scenes: Scene[] }) {
  const [active, setActive] = useState(0);
  const [hovered, setHovered] = useState(false);
  const [focused, setFocused] = useState(false);
  const [reducedMotion, setReducedMotion] = useState(false);

  useEffect(() => {
    const query = window.matchMedia("(prefers-reduced-motion: reduce)");
    const sync = () => setReducedMotion(query.matches);
    sync();
    query.addEventListener("change", sync);
    return () => query.removeEventListener("change", sync);
  }, []);

  useEffect(() => {
    if (hovered || focused || reducedMotion || scenes.length < 2) return;
    const timer = window.setInterval(
      () => setActive((index) => (index + 1) % scenes.length),
      ROTATION_MS,
    );
    return () => window.clearInterval(timer);
  }, [focused, hovered, reducedMotion, scenes.length]);

  const current = scenes[active];
  const show = (index: number) =>
    setActive((index + scenes.length) % scenes.length);

  return (
    <figure
      className={styles.carousel}
      role="region"
      aria-roledescription="carousel"
      aria-label="Featured Revelation artwork"
      data-active-scene={current.id}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
      onFocusCapture={() => setFocused(true)}
      onBlurCapture={(event) => {
        if (!event.currentTarget.contains(event.relatedTarget as Node | null)) {
          setFocused(false);
        }
      }}
    >
      <div className={styles.frame}>
        {scenes.map((scene, index) => (
          <div
            className={styles.slide}
            data-active={index === active}
            data-scene-id={scene.id}
            aria-hidden={index !== active}
            key={scene.id}
          >
            <ArtworkImage scene={scene} size="reader" eager={index === 0} />
          </div>
        ))}
      </div>
      <figcaption>
        <span>Movement {current.tapestry} · {current.id}</span>
        <strong>{current.title}</strong>
        <small>{current.displayReference}</small>
      </figcaption>
      <div className={styles.controls}>
        <button type="button" onClick={() => show(active - 1)} aria-label="Previous artwork">←</button>
        <div className={styles.dots} aria-label="Choose featured artwork">
          {scenes.map((scene, index) => (
            <button
              type="button"
              key={scene.id}
              aria-label={`Show artwork ${index + 1}: ${scene.title}`}
              aria-current={index === active ? "true" : undefined}
              onClick={() => show(index)}
            />
          ))}
        </div>
        <button type="button" onClick={() => show(active + 1)} aria-label="Next artwork">→</button>
      </div>
    </figure>
  );
}
```

- [ ] **Step 4: Add scoped carousel presentation and reduced-motion CSS**

Create `components/HomeHeroCarousel.module.css`:

```css
.carousel {
  position: relative;
  width: min(100%, 38rem);
  margin: 0 auto;
  padding: clamp(.7rem, 1.5vw, 1rem);
  border: 1px solid rgba(214, 187, 120, .4);
  box-shadow: 0 2rem 7rem rgba(0, 0, 0, .5);
}
.carousel::before {
  position: absolute;
  inset: .45rem;
  content: "";
  border: 1px solid rgba(214, 187, 120, .14);
  pointer-events: none;
}
.frame { position: relative; aspect-ratio: 16 / 9; overflow: hidden; background: #07090c; }
.slide { position: absolute; inset: 0; display: grid; place-items: center; opacity: 0; transition: opacity .8s ease; pointer-events: none; }
.slide[data-active="true"] { opacity: 1; }
.slide img, .slide > div { width: 100%; height: 100%; object-fit: contain; }
.carousel figcaption {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: .25rem 1rem;
  padding: 1rem .25rem .2rem;
}
.carousel figcaption span { grid-row: 1 / 3; color: var(--gold); font-size: .6rem; letter-spacing: .1em; text-transform: uppercase; }
.carousel figcaption strong { font: 1.2rem/1 var(--font-display), serif; }
.carousel figcaption small { color: var(--muted); }
.controls { display: grid; grid-template-columns: 2.5rem 1fr 2.5rem; gap: .75rem; align-items: center; margin-top: .9rem; }
.controls button { min-width: 2.5rem; min-height: 2.5rem; color: var(--ink); background: transparent; border: 1px solid var(--line); cursor: pointer; }
.dots { display: flex; justify-content: center; gap: .45rem; }
.dots button {
  min-width: 2.5rem;
  min-height: 2.5rem;
  padding: 0;
  color: var(--muted);
  background: radial-gradient(circle, currentColor 0 .28rem, transparent .32rem);
  border-color: transparent;
  border-radius: 50%;
}
.dots button[aria-current="true"] {
  color: var(--gold);
  border-color: var(--line);
}
@media (prefers-reduced-motion: reduce) {
  .slide { transition: none; }
}
```

- [ ] **Step 5: Pass the six required scenes from the server homepage**

In `app/page.tsx`, add:

```tsx
import { HomeHeroCarousel } from "@/components/HomeHeroCarousel";

const homeHeroSceneIds = [
  "T1-B04",
  "T2-B03",
  "T3-T07",
  "T4-B04",
  "T5-B02",
  "T6-B03",
] as const;
```

Inside `HomePage`, replace the static `feature` with:

```tsx
const features = homeHeroSceneIds.map(requiredScene);
```

and:

```tsx
<HomeHeroCarousel scenes={features} />
```

Remove the now-dead `.feature*` rules from `app/page.module.css`; keep the hero grid and make its artwork column wide enough for the new component.

- [ ] **Step 6: Run carousel and regression tests, then commit**

Run:

```bash
rtk npm run build
rtk npx playwright test e2e/exhibition.spec.ts --grep "carousel|Remix|Print Edition"
```

Expected: PASS in Chromium and mobile.

Commit:

```bash
rtk git add components/HomeHeroCarousel.tsx components/HomeHeroCarousel.module.css app/page.tsx app/page.module.css e2e/exhibition.spec.ts
rtk git commit -m "feat: add rotating homepage artwork carousel"
```

---

### Task 5: Complete the repository-wide singular sweep and final verification

**Files:**
- Modify: `README.md`
- Modify: `CONTRIBUTING.md`
- Modify: `MASTER_CONTEXT.md`
- Modify: `docs/**/*.md` where the old project or artifact name appears
- Modify: `publishing/editions/README.md`
- Modify: `publishing/instructions/PANDOC_EXPORTS.md`
- Modify: tracked `graphify-out/**` text/JSON/HTML artifacts containing the old workspace or project name
- Modify local Git remote URL
- Verify all application, test, release, publishing, package, and configuration files

**Interfaces:**
- Consumes: all functional changes from Tasks 1–4.
- Produces: zero plural project-name matches in tracked project content and non-dependency workspace files.
- Produces: local `origin` URL `https://github.com/Divergent-World/Revelation.git`.

- [ ] **Step 1: Apply the mechanical text migration to remaining tracked text files**

List matches first:

```bash
rtk git grep -n -i "revelation[s]"
```

Then apply the narrow case-aware rewrite to matched tracked text files:

```bash
rtk git grep -Il -i "revelation[s]" | rtk xargs perl -pi -e 's/Revelation[s]/Revelation/g; s/revelation[s]/revelation/g; s#Divergent-World/revelation#Divergent-World/Revelation#g; s#/Desktop/test/revelation#/Desktop/test/Revelation#g'
```

Review every changed path with `rtk git diff --stat` and `rtk git diff --check`. Do not modify third-party `node_modules`, `.git` internals, or the user's unstaged `next-env.d.ts`.

- [ ] **Step 2: Update the local remote and verify ignored/generated artifacts**

Run:

```bash
rtk git remote set-url origin https://github.com/Divergent-World/Revelation.git
rtk git remote -v
rtk ls -lh publishing/editions
```

Expected: fetch and push URLs use `Divergent-World/Revelation.git`; the editions directory contains `revelation.docx` and no plural DOCX filename.

If `dist/releases/v1` exists from earlier builds, rebuild the release so ignored generated artifacts also use the singular names:

```bash
rtk npm run assets:release
```

Do not run `assets:upload`: the user has not requested a production upload. Report the singular R2 bucket/object upload as a deployment prerequisite.

- [ ] **Step 3: Validate generated JSON and run the zero-match audits**

Run:

```bash
rtk node -e 'for (const file of process.argv.slice(1)) JSON.parse(require("node:fs").readFileSync(file, "utf8"))' package.json package-lock.json graphify-out/graph.json graphify-out/manifest.json graphify-out/cost.json
rtk git grep -n -i "revelation[s]"
rtk git ls-files "*revelation[s]*" "*Revelation[s]*"
rtk rg -n -i --hidden --glob "!node_modules/**" --glob "!.git/**" --glob "!.next/**" "revelation[s]" .
rtk find . -path ./node_modules -prune -o -path ./.git -prune -o -path ./.next -prune -o -iname "*revelation[s]*" -print
```

Expected: JSON parsing succeeds; all four name audits exit with no matches. If Graphify's own cached/generated identifiers contain the old plural string, update those generated text artifacts with the same narrow replacement and rerun JSON validation.

- [ ] **Step 4: Run the complete automated verification**

Run:

```bash
rtk npm test
rtk npm run build
rtk npx playwright test
```

Expected: all Node tests pass, Next.js production build succeeds, and Playwright passes in Chromium and mobile.

Compare `rtk git diff -- next-env.d.ts` with the pre-task diff. If a Next command rewrote it, restore the exact pre-task contents with `apply_patch`; do not stage it.

- [ ] **Step 5: Perform browser visual checks**

Start the development server only if Playwright has released its web-server port:

```bash
rtk npm run dev
```

Using the in-app browser, verify:

- Homepage at desktop and mobile widths: six-scene carousel, readable caption, working arrows/dots, no archive block, no horizontal overflow.
- Reduced-motion emulation: no auto-advance and no fade transition.
- `/print-edition/`: source artwork is presented as artwork, the 182-page details are legible, buttons wrap cleanly, iframe remains approximately 16:9 and no wider than 50rem.
- `/remix/`: two distinct equal-height actions, archive contents, manuscript link, and no email form.
- Header at desktop and mobile widths: **Movements**, **Read**, **Print Edition**, **Remix** all remain reachable.
- Page titles and visible brand text use **Revelation** only.

Stop the dev server after checks. Apply only verified CSS corrections, rerun the affected Playwright tests, and include them in the final task commit.

- [ ] **Step 6: Commit the singular sweep and any verified integration corrections**

```bash
rtk git add README.md CONTRIBUTING.md MASTER_CONTEXT.md docs publishing package.json package-lock.json .env.example app components lib scripts test e2e graphify-out
rtk git restore --staged next-env.d.ts
rtk git commit -m "docs: finish Revelation naming migration"
```

Final status must show only the pre-existing unstaged `next-env.d.ts` change. Do not upload R2 objects, push the branch, or open a pull request without a separate user request.
