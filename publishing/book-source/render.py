from playwright.sync_api import sync_playwright
import pathlib, sys
uri = pathlib.Path("book.html").resolve().as_uri()
with sync_playwright() as pw:
    b = pw.chromium.launch(args=["--font-render-hinting=none"])
    pg = b.new_page(viewport={"width":1728,"height":1296})
    pg.goto(uri, wait_until="load", timeout=180000)
    pg.wait_for_function("document.documentElement.getAttribute('data-ready')==='1'", timeout=180000)
    pg.wait_for_timeout(4000)
    n = pg.evaluate("document.querySelectorAll('.page').length")
    over = pg.evaluate("""(()=>{let bad=[];document.querySelectorAll('.col').forEach((c,i)=>{
        if(c.scrollHeight>c.clientHeight+2) bad.push(i);});return bad.length;})()""")
    print("pages:", n, "| overflowing columns:", over)
    pg.pdf(path="REVELATION_complete_edition.pdf", width="12in", height="9in",
           print_background=True, margin={"top":"0","bottom":"0","left":"0","right":"0"})
    b.close()
