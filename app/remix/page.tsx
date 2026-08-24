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
        <p className="eyebrow">A companion to the Print Edition</p>
        <h1>Open the making of Revelation.</h1>
        <p>
          Follow the project from scripture and image prompts to finished
          artwork and book files. The companion is an invitation to learn
          Revelation, understand a generative AI publishing practice, and make
          a new interpretation of your own.
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

      <section className={styles.contents} aria-labelledby="archive-contents">
        <div>
          <p className="eyebrow">Inside the archive</p>
          <h2 id="archive-contents">The work, its editions, and how it was made.</h2>
          <p>
            Begin with the finished book or trace any image back through the
            canonical content and editable publishing sources used to create it.
          </p>
        </div>
        <div className={styles.tree} role="region" aria-label="Master Archive contents">
          <pre><code>{`REVELATION-master-v1/
├── README.md
├── export.md
├── manifest.json
├── SHA256SUMS.txt
├── artwork/
│   ├── originals/
│   ├── book-images/
│   └── web/
│       ├── 640/
│       └── 1920/
├── content/
│   ├── revelation.web.json
│   ├── scene-metadata.json
│   ├── source-map.json
│   └── tapestries.json
├── editions/
│   ├── REVELATION_web.pdf
│   ├── REVELATION_iPad_fixed.epub
│   ├── REVELATION_reflowable.epub
│   └── revelation.docx
└── publishing/
    ├── README.md
    ├── book-source/
    ├── editions/
    ├── historical-book-build/
    ├── indesign/
    ├── instructions/
    └── reference/`}</code></pre>
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
