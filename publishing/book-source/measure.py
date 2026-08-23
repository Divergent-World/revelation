# -*- coding: utf-8 -*-
"""Measure how each flowing section paginates at 13x11in with the IDML frame metrics.
Emits sections.json: {section_key: n_pages}."""
import json, os, html
from prose import FOREWORD, LOSSES, METHOD

HERE = os.path.dirname(os.path.abspath(__file__))
T = json.load(open(os.path.join(HERE, "tapestries.json")))
REV = json.load(open(os.path.join(HERE, "revelation.web.json")))
SCENES = {s["id"]: s for s in T["scenes"]}

import build as B   # reuse verse_html / prose_blocks / status_of

def esc(s): return html.escape(s, quote=False)

SECTIONS = []
def add(key, blocks, first_short=True):
    SECTIONS.append({"key": key, "src": "".join(blocks), "first": first_short})

add("foreword", B.prose_blocks(FOREWORD))
add("losses",   B.prose_blocks(LOSSES))
add("method",   B.prose_blocks(METHOD))

for tp in T["tapestries"]:
    blocks = []
    for i, m in enumerate(tp["movements"], 1):
        blocks.append('<h3><span class="mnum">%d</span>%s</h3>' % (i, esc(m["title"])))
        blocks.append('<p%s>%s</p>' % (' class="drop"' if i == 1 else '', esc(m["description"])))
    add("arg%d" % tp["id"], blocks)

blocks = []
for ch in REV["chapters"]:
    blocks.append('<h3 class="chap"><span>CHAPTER</span>%d</h3>' % ch["chapter"])
    run = []
    for v in ch["verses"]:
        run.append('<span class="v">%d</span>%s' % (v["number"],
                   B.verse_html(v["text"], v.get("wordsOfJesus"))))
        if len(run) == 4:
            blocks.append('<p class="sc">%s</p>' % " ".join(run)); run = []
    if run: blocks.append('<p class="sc">%s</p>' % " ".join(run))
add("text", blocks)

rows = []
for tp in T["tapestries"]:
    rows.append('<div class="reg-h">MOVEMENT %s · %s</div>' % (esc(tp["roman"]), esc(tp["title"])))
    for sid in tp["sceneIds"]:
        s = SCENES[sid]; lab, cls = B.status_of(s)
        rows.append('<div class="reg"><span class="k">%s</span><span class="t">%s</span>'
                    '<span class="a">%s</span><span class="s %s">%s</span></div>'
                    % (esc(s["id"]), esc(s["title"]),
                       esc(s["displayReference"].replace("Revelation ", "")), cls, lab))
add("register", rows)

CSS = """
@page{size:12.5in 10.625in;margin:0}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:"EB Garamond",serif;background:#555}
:root{--ink:#16120E;--ink-soft:#3B322A;--rubric:#8E2420;--gold:#A8823C;--rule:#C3B597;
--lapis:#1E3566;--wj:#9B1C31}
.page{width:12.5in;height:10.625in;background:#EAE1CE;position:relative;overflow:hidden;
  page-break-after:always}
/* frame box = 810 x 672 pt  (11.25in x 9.333in), first page 564pt (7.833in) */
.pagebody{position:absolute;left:64pt;top:50pt;width:782pt;height:653pt;
  display:grid;grid-template-columns:1fr 1fr;gap:31pt}
.page.first .pagebody{top:168pt;height:535pt}
.col{overflow:hidden}
.col > *{break-inside:avoid}
.col p{font-size:10.3pt;line-height:1.70;color:var(--ink);text-align:justify;hyphens:auto;
  margin-bottom:9.4pt}
.col p.drop::first-letter{font-family:"Cinzel",serif;font-size:26pt;line-height:.84;float:left;
  padding:2.9pt 5pt 0 0;color:var(--rubric)}
.col p.sig{font-family:"Space Grotesk",sans-serif;font-size:6.2pt;letter-spacing:.22em;
  text-transform:uppercase;margin-top:13pt;text-align:left}
.col h3{font-family:"Cinzel",serif;font-size:10.5pt;font-weight:600;letter-spacing:.07em;
  margin:14.4pt 0 7.2pt}
.col h3 .mnum{display:inline-block;width:17pt;color:var(--rubric)}
.col h3.chap{font-size:13pt;color:var(--rubric);letter-spacing:.10em;margin:18.7pt 0 8.6pt;
  border-top:.5pt solid var(--rule);padding-top:10pt}
.col h3.chap span{font-family:"Space Grotesk",sans-serif;font-size:5.6pt;letter-spacing:.26em;
  color:#8A7C66;display:block;margin-bottom:3.6pt}
.col p.sc{font-size:9.9pt;line-height:1.66;margin-bottom:7.2pt}
.col p.sc .v,.col .v{font-family:"Space Grotesk",sans-serif;font-size:5.3pt;color:var(--rubric);
  vertical-align:.42em;margin-right:2pt;font-weight:500}
.wj{color:var(--wj)}
.reg-h{font-family:"Space Grotesk",sans-serif;font-size:5.9pt;letter-spacing:.24em;
  text-transform:uppercase;color:var(--gold);margin:15.8pt 0 6.5pt;
  border-top:.5pt solid var(--rule);padding-top:8pt}
.reg{display:grid;grid-template-columns:42pt 1fr 45pt 50pt;gap:4pt;align-items:baseline;
  padding:3pt 0;border-bottom:.25pt solid #D8CCB4}
.reg .k{font-family:"Space Grotesk",sans-serif;font-size:5.8pt;color:var(--ink-soft)}
.reg .t{font-size:8.6pt;line-height:1.28}
.reg .a{font-family:"Space Grotesk",sans-serif;font-size:5.5pt;color:#8A7C66}
.reg .s{font-family:"Space Grotesk",sans-serif;font-size:5.2pt;letter-spacing:.13em;
  text-transform:uppercase;text-align:right}
.flowsec{display:none}
"""

JS = """
window.RESULT={};
document.querySelectorAll('.flowsec').forEach(function(sec){
  const blocks=Array.prototype.slice.call(sec.querySelector('.flow-src').children);
  let first=sec.dataset.first==='1', cols=null, ci=0, n=0;
  function newPage(){
    const p=document.createElement('div');
    p.className='page'+(first?' first':'');
    p.innerHTML='<div class="pagebody"></div>';
    const b=p.querySelector('.pagebody'); cols=[];
    for(let i=0;i<2;i++){const c=document.createElement('div');c.className='col';b.appendChild(c);cols.push(c);}
    sec.parentNode.insertBefore(p,sec); ci=0; first=false; n++;
  }
  newPage();
  blocks.forEach(function(b){
    cols[ci].appendChild(b);
    let g=0;
    while(cols[ci].scrollHeight>cols[ci].clientHeight+1 && g++<40){
      cols[ci].removeChild(b); ci++;
      if(ci>=cols.length){newPage();}
      cols[ci].appendChild(b);
      if(cols[ci].childElementCount===1) break;
    }
  });
  window.RESULT[sec.dataset.key]=n;
  sec.remove();
});
document.documentElement.setAttribute('data-ready','1');
"""

body = "".join('<div class="flowsec" data-key="%s" data-first="%d"><div class="flow-src">%s</div></div>'
               % (s["key"], 1 if s["first"] else 0, s["src"]) for s in SECTIONS)
open(os.path.join(HERE, "measure.html"), "w").write(
    '<!DOCTYPE html><html><head><meta charset="utf-8"><style>%s</style></head><body>%s'
    '<script>%s</script></body></html>' % (CSS, body, JS))

from playwright.sync_api import sync_playwright
import pathlib
with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page(viewport={"width": 1250, "height": 1063})
    pg.goto(pathlib.Path(os.path.join(HERE, "measure.html")).as_uri(), wait_until="load")
    pg.wait_for_function("document.documentElement.getAttribute('data-ready')==='1'", timeout=120000)
    res = pg.evaluate("window.RESULT")
    b.close()
json.dump(res, open(os.path.join(HERE, "sections.json"), "w"), indent=1)
print(json.dumps(res, indent=1))
print("total flow pages:", sum(res.values()))
