from playwright.sync_api import sync_playwright
from PIL import Image
import io, os, sys, time
from paths import BUILD

OUT = BUILD / "epub_pages"
TARGET_W = int(sys.argv[1]) if len(sys.argv) > 1 else 2048
BUILD.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)
t0 = time.time()
with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page(viewport={"width": 1200, "height": 900}, device_scale_factor=2)
    pg.goto((BUILD / "book.html").as_uri(),
            wait_until="load", timeout=240000)
    pg.wait_for_function("document.documentElement.getAttribute('data-ready')==='1'",
                         timeout=240000)
    pg.wait_for_timeout(3000)
    n = pg.evaluate("document.querySelectorAll('.page').length")
    els = pg.query_selector_all(".page")
    for i, el in enumerate(els, 1):
        dst = OUT / ("p%03d.jpg" % i)
        if dst.exists(): continue
        classes = set((el.get_attribute("class") or "").split())
        image_led = bool(
            classes.intersection(
                {"ebookcover", "backcover", "bleed", "mvpage", "platepage"}
            )
        )
        quality = 76 if image_led else 88
        raw = el.screenshot(type="png")
        im = Image.open(io.BytesIO(raw)).convert("RGB")
        if im.width != TARGET_W:
            im = im.resize((TARGET_W, round(im.height * TARGET_W / im.width)), Image.LANCZOS)
        im.save(dst, "JPEG", quality=quality, optimize=True, progressive=True)
        if i % 40 == 0: print("  %d/%d  %.0fs" % (i, n, time.time()-t0))
    b.close()
tot = sum(path.stat().st_size for path in OUT.iterdir())
print("rendered %d pages, %.1f MB, %.0fs" % (len(list(OUT.iterdir())), tot/1e6, time.time()-t0))
