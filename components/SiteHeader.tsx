import Link from "next/link";

export function SiteHeader() {
  return (
    <header className="site-header">
      <Link className="wordmark" href="/" aria-label="Revelation home">
        <span>Revelation</span>
        <small>A Divergent World exhibition</small>
      </Link>
      <nav aria-label="Primary navigation">
        <Link href="/tapestries/1/">Movements</Link>
        <Link href="/print-edition/">Print Edition</Link>
        <Link href="/remix/">Remix</Link>
        <Link href="/revelation/">Read</Link>
      </nav>
    </header>
  );
}
