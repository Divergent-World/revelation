from playwright.sync_api import sync_playwright
import pathlib
u = pathlib.Path("cover.html").resolve().as_uri()
W_PT, H_PT = 1951.354, 836.496
CSSW, CSSH = W_PT*96/72, H_PT*96/72
with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page(viewport={"width":int(CSSW)+2,"height":int(CSSH)+2})
    pg.goto(u, wait_until="load"); pg.wait_for_timeout(2500)
    pg.pdf(path="_cover_raw.pdf", width="27.1021in", height="11.6180in",
           print_background=True, margin={"top":"0","bottom":"0","left":"0","right":"0"})
    pg2 = b.new_page(viewport={"width":int(CSSW)+2,"height":int(CSSH)+2}, device_scale_factor=300/96)
    pg2.goto(u, wait_until="load"); pg2.wait_for_timeout(2500)
    pg2.screenshot(path="REVELATION_cover_300dpi.png", clip={"x":0,"y":0,"width":CSSW,"height":CSSH})
    b.close()
print("rendered")
