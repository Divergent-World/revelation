import type { Metadata } from "next";
import Image from "next/image";
import localFont from "next/font/local";

import { ArtworkImage } from "@/components/ArtworkImage";
import {
  blurbBookUrl,
  blurbPreviewUrl,
  getScene,
  type Scene,
} from "@/lib/content";
import coverArtwork from "@/publishing/indesign/cover_bg.jpg";
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

const gallery = ["T1-B04", "T3-T07", "T5-B02", "T6-B05"].map(requiredScene);

const coverCinzel = localFont({
  src: [
    {
      path: "../../publishing/indesign/Fonts/Cinzel-Regular.ttf",
      weight: "400",
    },
    {
      path: "../../publishing/indesign/Fonts/Cinzel-SemiBold.ttf",
      weight: "600",
    },
  ],
});
const coverGaramond = localFont({
  src: "../../publishing/indesign/Fonts/EBGaramond-Italic.ttf",
  style: "italic",
});
const coverGrotesk = localFont({
  src: "../../publishing/indesign/Fonts/SpaceGrotesk-Medium.ttf",
  weight: "500",
});

function EditionCover() {
  return (
    <figure className={styles.cover} data-edition-cover>
      <div className={styles.coverFace}>
        <Image
          src={coverArtwork}
          alt="Front cover of Revelation: An Illuminated Prophecy by Ali Rahman"
          fill
          priority
          sizes="(max-width: 760px) 82vw, 36vw"
        />
        <div className={styles.coverType} aria-hidden="true">
          <strong className={coverCinzel.className}>Revelation</strong>
          <span className={coverCinzel.className}>An Illuminated Prophecy in Six Movements</span>
          <i className={coverGaramond.className}>After the Apocalypse Tapestry of Angers</i>
          <small className={coverGrotesk.className}>Ali Rahman</small>
        </div>
      </div>
      <figcaption>The collector&apos;s edition cover</figcaption>
    </figure>
  );
}

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
            and gathered into a large-format landscape volume made for close,
            unhurried reading.
          </p>
          <dl className={styles.productMeta}>
            <div><dt>Price</dt><dd>$310</dd></div>
            <div><dt>Edition</dt><dd>Hardcover ImageWrap</dd></div>
            <div><dt>Extent</dt><dd>182 pages</dd></div>
          </dl>
          <a className="button button-primary" href={blurbBookUrl}>View on Blurb</a>
        </div>
        <EditionCover />
      </section>

      <section className={styles.story} aria-labelledby="edition-story">
        <p className="eyebrow">The complete sequence</p>
        <h2 id="edition-story">A work made to be encountered at the scale of a book.</h2>
        <p>
          Designed as an illuminated journey rather than a catalogue, the
          edition rebuilds all ninety Apocalypse tapestry compartments in
          sequence. Each image is set beside the text that animates it and
          marked as surviving, fragmentary, or reconstructed.
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
          <p>Turn through the book, then visit Blurb for current availability.</p>
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
