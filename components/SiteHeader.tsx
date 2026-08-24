import Link from "next/link";

import { repositoryUrl } from "@/lib/content";

export function SiteHeader() {
  return (
    <header className="site-header">
      <Link className="wordmark" href="/" aria-label="Revelation home">
        <span>Revelation</span>
        <small>A Divergent World exhibition</small>
      </Link>
      <nav aria-label="Primary navigation">
        <Link href="/tapestries/1/">Movements</Link>
        <Link href="/revelation/">Read</Link>
        <a href={repositoryUrl}>Source</a>
      </nav>
    </header>
  );
}
