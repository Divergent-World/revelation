from playwright.sync_api import sync_playwright
from PIL import Image
import pathlib, os, io, time
HERE = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.join(HERE, "epub_pages")
TARGET_W = 2048                      # 170 ppi across a 12 in page
t0 = time.time()
with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page(viewport={"width": 1200, "height": 900}, device_scale_factor=2)
    pg.goto(pathlib.Path(os.path.join(HERE, "book.html")).as_uri(),
            wait_until="load", timeout=240000)
    pg.wait_for_function("document.documentElement.getAttribute('data-ready')==='1'",
                         timeout=240000)
    pg.wait_for_timeout(3000)
    n = pg.evaluate("document.querySelectorAll('.page').length")
    els = pg.query_selector_all(".page")
    for i, el in enumerate(els, 1):
        dst = os.path.join(OUT, "p%03d.jpg" % i)
        if os.path.exists(dst): continue
        raw = el.screenshot(type="png")
        im = Image.open(io.BytesIO(raw)).convert("RGB")
        if im.width != TARGET_W:
            im = im.resize((TARGET_W, round(im.height * TARGET_W / im.width)), Image.LANCZOS)
        im.save(dst, "JPEG", quality=86, optimize=True, progressive=True)
        if i % 40 == 0: print("  %d/%d  %.0fs" % (i, n, time.time()-t0))
    b.close()
tot = sum(os.path.getsize(os.path.join(OUT,f)) for f in os.listdir(OUT))
print("rendered %d pages, %.1f MB, %.0fs" % (len(os.listdir(OUT)), tot/1e6, time.time()-t0))
