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
        <div className={styles.heroCopy}>
          <p className="eyebrow">A companion to the Print Edition</p>
          <h1>Open the making of Revelation.</h1>
          <p>
            Follow the project from scripture and source imagery to finished
            artwork and book files. This companion is an invitation to study
            the work, understand a generative AI publishing practice, and make
            a new interpretation of your own.
          </p>
          <div className={styles.actions} data-remix-actions>
            <a className="button button-primary" href={masterArchiveUrl}>
              Download Master Archive
            </a>
            <a className="button" href={repositoryUrl}>
              View Source on GitHub
            </a>
          </div>
          <p className={styles.note}>
            1.6 GB · 182-page PDF · EPUB editions · editable publishing source
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
        </div>
        <p className={styles.archiveAside}>
          Start with a finished edition, or move backward through its sources
          until you reach the image, passage, or production decision you want
          to reconsider.
        </p>
      </section>

      <section className={styles.contents} aria-labelledby="archive-contents">
        <div className={styles.contentsIntro}>
          <p className="eyebrow">Inside the archive</p>
          <h2 id="archive-contents">A working kit for study and reinterpretation.</h2>
          <p>
            The archive keeps the canon, imagery, metadata, and bookmaking
            sources together so the path from a biblical passage to a finished
            page remains visible—and open to another reading.
          </p>
        </div>
        <div className={styles.workflow}>
          <article>
            <span>01</span>
            <h3>Begin with the canon</h3>
            <p>
              Use the scripture, scene metadata, and source map to see which
              verses animate each of the ninety illuminated compartments.
            </p>
          </article>
          <article>
            <span>02</span>
            <h3>Study the construction</h3>
            <p>
              Compare the artwork, publication files, and finished editions to
              understand how a long visual sequence becomes a physical book.
            </p>
          </article>
          <article>
            <span>03</span>
            <h3>Build a new interpretation</h3>
            <p>
              Bring a selected source image and passage into GPT or Nano Banana,
              develop a new prompt language, and assemble the results into a
              personal visual reading of Revelation.
            </p>
          </article>
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
