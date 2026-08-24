(function () {
  function makePage(sec, first) {
    const p = document.createElement("div");
    p.className = "page prose" + (first ? " first" : "");
    p.dataset.rt = sec.dataset.rt || "";
    const hd = first
      ? '<div class="sechd"><h2>' + sec.dataset.title + "</h2>" +
        (sec.dataset.kicker ? '<div class="seck">' + sec.dataset.kicker + "</div>" : "") +
        "</div>"
      : "";
    p.innerHTML =
      '<div class="rt">' + (sec.dataset.rt || "") + "</div>" +
      hd + '<div class="pagebody"></div><div class="folio"></div>';
    const bodyEl = p.querySelector(".pagebody");
    bodyEl.style.gridTemplateColumns = "repeat(" + sec.dataset.cols + ", 1fr)";
    const cols = [];
    for (let i = 0; i < +sec.dataset.cols; i++) {
      const c = document.createElement("div");
      c.className = "col";
      bodyEl.appendChild(c);
      cols.push(c);
    }
    sec.parentNode.insertBefore(p, sec);
    return cols;
  }

  function fits(col) {
    return col.scrollHeight <= col.clientHeight + 1;
  }

  document.querySelectorAll(".flowsec").forEach(function (sec) {
    const src = sec.querySelector(".flow-src");
    const blocks = Array.prototype.slice.call(src.children);
    let first = true;
    let cols = makePage(sec, first);
    first = false;
    let ci = 0;

    blocks.forEach(function (b) {
      cols[ci].appendChild(b);
      let guard = 0;
      while (!fits(cols[ci]) && guard++ < 40) {
        cols[ci].removeChild(b);
        ci++;
        if (ci >= cols.length) {
          cols = makePage(sec, false);
          ci = 0;
        }
        cols[ci].appendChild(b);
        if (cols[ci].childElementCount === 1) break; // block alone overflows; accept
      }
    });
    sec.remove();
  });

  // ---- folios & running heads: number every page, alternate sides ----
  const pages = Array.prototype.slice.call(document.querySelectorAll(".page"));
  let n = 0;
  pages.forEach(function (p, i) {
    const verso = i % 2 === 0; // 0-indexed: even = left-hand page
    p.classList.add(verso ? "verso" : "recto");
    n++;
    const f = p.querySelector(".folio");
    if (f) f.textContent = String(n);
    const rt = p.querySelector(".rt");
    if (rt && !rt.textContent.trim() && p.dataset.rt) rt.textContent = p.dataset.rt;
  });
  document.body.dataset.pages = String(pages.length);
  document.documentElement.setAttribute("data-ready", "1");
})();
