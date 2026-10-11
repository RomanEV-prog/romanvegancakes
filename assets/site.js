/* Roman's Cakes — skupna logika (navigacija, kazalec, zrno, prehodi, razkrivanje) */
(function () {
  'use strict';
  var body = document.body;
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fine = window.matchMedia('(hover: hover) and (pointer: fine)').matches;

  // ── Mobilni meni ──
  var mb = document.querySelector('.nav-mb'), mnav = document.getElementById('mnav');
  if (mb && mnav) {
    mb.addEventListener('click', function () {
      var open = mnav.classList.toggle('o');
      mb.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }
  // ── Navigacija ob drsenju ──
  var nav = document.getElementById('nav');
  function onScroll() { if (nav) nav.classList.toggle('s', window.scrollY > 40); }
  window.addEventListener('scroll', onScroll, { passive: true }); onScroll();

  // ── Kazalec po meri (samo miška) ──
  var dot = document.getElementById('cur-dot'), ring = document.getElementById('cur-ring');
  if (fine && !reduced && dot && ring) {
    body.classList.add('cur');
    var mx = 0, my = 0, rx = 0, ry = 0, seen = false;
    document.addEventListener('mousemove', function (e) {
      mx = e.clientX; my = e.clientY; if (!seen) { rx = mx; ry = my; seen = true; }
      dot.style.left = mx + 'px'; dot.style.top = my + 'px';
    });
    (function lr() { if (seen) { rx += (mx - rx) * .12; ry += (my - ry) * .12; ring.style.left = rx + 'px'; ring.style.top = ry + 'px'; } requestAnimationFrame(lr); })();
    document.querySelectorAll('a,button,label,input,select,textarea,.card-h').forEach(function (el) {
      el.addEventListener('mouseenter', function () { body.classList.add('ch'); });
      el.addEventListener('mouseleave', function () { body.classList.remove('ch'); });
    });
    document.addEventListener('mousedown', function () { body.classList.add('cc'); });
    document.addEventListener('mouseup', function () { body.classList.remove('cc'); });
  }

  // ── Zrno: en 200×200 vzorec, zamenjan nekajkrat na sekundo ──
  var grain = document.getElementById('grain');
  if (grain && !reduced) {
    var c = document.createElement('canvas'); c.width = c.height = 200;
    var ctx = c.getContext('2d'), frames = [], i;
    for (i = 0; i < 4; i++) {
      var img = ctx.createImageData(200, 200), d = img.data;
      for (var p = 0; p < d.length; p += 4) { var v = Math.random() * 255 | 0; d[p] = d[p + 1] = d[p + 2] = v; d[p + 3] = 255; }
      ctx.putImageData(img, 0, 0); frames.push('url(' + c.toDataURL() + ')');
    }
    var f = 0; setInterval(function () { f = (f + 1) % frames.length; grain.style.backgroundImage = frames[f]; }, 120);
  }

  // ── Razkrivanje ob drsenju ──
  var rv = document.querySelectorAll('.rv');
  if ('IntersectionObserver' in window && !reduced) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } });
    }, { rootMargin: '0px 0px -8% 0px', threshold: .08 });
    rv.forEach(function (el, idx) { el.style.transitionDelay = ((+el.dataset.d || 0)) + 'ms'; io.observe(el); });
  } else { rv.forEach(function (el) { el.classList.add('in'); }); }

  // ── Prehod med stranmi (zlati zastor) ──
  var ov = document.getElementById('pg-overlay');
  if (ov && !reduced) {
    document.querySelectorAll('a[href]').forEach(function (link) {
      var href = link.getAttribute('href');
      if (!href || href.charAt(0) === '#' || /^(mailto|tel|javascript):/.test(href) || link.target === '_blank' || link.hasAttribute('download')) return;
      if (link.origin !== window.location.origin) return;
      link.addEventListener('click', function (e) {
        if (e.metaKey || e.ctrlKey || e.shiftKey || e.button !== 0) return;
        e.preventDefault();
        var url = link.href;
        ov.style.transition = 'transform 380ms cubic-bezier(.65,0,.35,1)'; ov.style.transform = 'scaleX(1)';
        setTimeout(function () { window.location.href = url; }, 390);
      });
    });
    window.addEventListener('pageshow', function () { ov.style.transition = 'none'; ov.style.transform = 'scaleX(0)'; });
  }

  // ── Skok na sidro po nalaganju (gladko drsenje včasih prekine začetni skok) ──
  function jumpToHash() {
    var id = decodeURIComponent((location.hash || '').slice(1)); if (!id) return;
    var el = document.getElementById(id); if (!el) return;
    var h = document.documentElement, prev = h.style.scrollBehavior;
    h.style.scrollBehavior = 'auto';
    el.scrollIntoView({ block: 'start' });
    h.style.scrollBehavior = prev;
    // Vse, kar je nad ciljem ali v pogledu, takoj pokaži (brez animacije razkrivanja)
    var limit = el.getBoundingClientRect().top + window.scrollY + window.innerHeight;
    rv.forEach(function (r) { if (r.getBoundingClientRect().top + window.scrollY < limit) r.classList.add('in'); });
  }
  window.addEventListener('load', function () { setTimeout(jumpToHash, 60); });

  // ── Leto v nogi ──
  document.querySelectorAll('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
