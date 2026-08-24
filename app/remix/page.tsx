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
