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
      <div className={styles.controls} data-carousel-controls>
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
      <figcaption>
        <span>Movement {current.tapestry} · {current.id}</span>
        <strong>{current.title}</strong>
        <small>{current.displayReference}</small>
      </figcaption>
    </figure>
  );
}
