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
          <p className="eyebrow">Collector&apos;s print edition · 182 pages</p>
          <h1 id="edition-title">Revelation: An Illuminated Prophecy</h1>
          <p className={styles.byline}>By Ali Rahman</p>
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

      <section className={styles.details} aria-labelledby="edition-details" data-edition-details>
        <div>
          <p className="eyebrow">Edition details</p>
          <h2 id="edition-details">The physical edition</h2>
        </div>
        <dl>
          <div><dt>Extent</dt><dd>182 pages</dd></div>
          <div><dt>Binding</dt><dd>Hardcover, ImageWrap</dd></div>
          <div><dt>Format</dt><dd>Large-format landscape</dd></div>
          <div><dt>Dimensions</dt><dd>13 × 11 in / 33 × 28 cm</dd></div>
          <div><dt>Contents</dt><dd>Ninety illuminated compartments · six movements · twenty-two chapters</dd></div>
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
