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

  // ── WhatsApp gumb (vstavi in pokaži po 3s) ──
  var wa = document.createElement('a');
  wa.id = 'wa-btn'; wa.href = 'https://wa.me/38640758582'; wa.target = '_blank'; wa.rel = 'noopener noreferrer';
  wa.setAttribute('aria-label', 'Pišite na WhatsApp');
  wa.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>';
  document.body.appendChild(wa);
  setTimeout(function () { wa.classList.add('show'); }, 3000);
})();
