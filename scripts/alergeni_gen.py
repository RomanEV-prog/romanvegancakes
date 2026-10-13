# -*- coding: utf-8 -*-
"""Iz scripts/alergeni-dump.json zgradi alergeni/index.html (stran za QR kodo v vitrinah).

Na stran gredo SAMO torte s popolno deklaracijo: receptura ima sestavine, vsi alergeni surovin
so potrjeni (tudi »brez«) in sestava ni nepopolna. Ostale skripta izpiše kot »MANJKA V ERP«
— na uradni strani z alergeni prazen seznam pomeni »brez alergenov«, kar je pravna past.
Uporaba: py -3 -I scripts/alergeni_gen.py
"""
import json, os, re, html, datetime, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dump = json.load(open(os.path.join(ROOT, 'scripts', 'alergeni-dump.json'), encoding='utf-8'))

# vrstni red in imena po Uredbi 1169/2011, Priloga II (samo rastlinski — veganski obrat)
IME = {'gluten': 'gluten (pšenica)', 'soja': 'soja', 'mandlji': 'mandlji', 'lesniki': 'lešniki', 'orehi': 'orehi',
       'indijski': 'indijski oreščki', 'pekan': 'pekan', 'brazilski': 'brazilski oreščki', 'pistacija': 'pistacija',
       'makadamija': 'makadamija', 'oreski': 'oreški', 'arasidi': 'arašidi', 'sezam': 'sezam', 'zelena': 'zelena',
       'gorcica': 'gorčica', 'sulfiti': 'žveplov dioksid in sulfiti', 'volcji_bob': 'volčji bob'}
VRSTNI_RED = list(IME.keys())

def slug(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')

PREDOGLED = os.environ.get('ALERGENI_PREDOGLED') == '1'   # samo za pregled postavitve, NIKOLI za objavo

# Torte, ki jih ERP sicer označi kot popolne, a je sestava očitno napačna. Odstrani vnos, ko Roman popravi recepturo.
ZADRZANE = {
    'Tiramisu torta': 'KEKSI PETIT in Spekulatius v ERP brez alergenov (keksi vsebujejo pšenico/gluten)',
    'Malina čokolada': 'receptura brez čokolade in moke (mandlji, orehi, kokosova moka) – verjetno zamenjana z BG različico',
}

def ok(t):
    if t['ime'] in ZADRZANE:
        return False
    if PREDOGLED:
        return bool(t.get('receptura_id')) and bool(t.get('sestavine'))
    return bool(t.get('receptura_id')) and bool(t.get('sestavine')) and not (t.get('alergeni_nepotrjeni') or []) \
        and not t.get('sestava_nepopolna')

objavljene, manjka = [], []
for t in dump['torte']:
    (objavljene if ok(t) else manjka).append(t)

datum = datetime.date.fromisoformat(dump['datum']).strftime('%d. %m. %Y').replace(' 0', ' ')

def kartica(t):
    kode = sorted(set(t.get('alergeni_kode') or []), key=lambda k: VRSTNI_RED.index(k) if k in VRSTNI_RED else 99)
    tags = ''.join('<span class="tag tag-a">%s</span>' % html.escape(IME.get(k, k)) for k in kode)
    if not kode:
        tags = '<span class="tag tag-v">brez alergenov iz Priloge II</span>'
    bg = '<span class="tag tag-g">brez glutenskih sestavin</span>' if t.get('brezglutensko') else ''
    sest = html.escape(t.get('sestavine_text') or '')
    # alergene surovine so v ERP že z VELIKIMI črkami — poudarimo jih še vizualno
    sest = re.sub(r'\b([A-ZČŠŽĆĐ][A-ZČŠŽĆĐ0-9 \-]{2,})\b', r'<b>\1</b>', sest)
    return f'''<article class="kart" id="{slug(t['ime'])}" data-ime="{html.escape(t['ime'].lower())}">
  <div class="kart-h"><h2>{html.escape(t['ime'])}</h2>{bg}</div>
  <div class="kart-al"><span class="kart-l">Vsebuje</span>{tags}</div>
  <details><summary>Sestavine</summary><p>{sest}</p></details>
</article>'''

kartice = '\n'.join(kartica(t) for t in sorted(objavljene, key=lambda x: (x.get('brezglutensko', 0), x['ime'].lower())))
n = len(objavljene)

page = f'''<!DOCTYPE html>
<html lang="sl">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Alergeni in sestavine — Roman's Cakes</title>
<meta name="description" content="Alergeni in sestavine veganskih tort Roman's Cakes po Uredbi (EU) 1169/2011. Podatki iz receptur, stanje {datum}.">
<meta name="robots" content="noindex,follow">
<meta name="theme-color" content="#080705">
<link rel="icon" href="../favicon.ico" sizes="any"><link rel="icon" href="../slike/web/icon-512.png" type="image/png"><link rel="apple-touch-icon" href="../slike/web/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;0,600;0,800;1,400;1,600&family=DM+Sans:wght@300;400;500&family=DM+Mono:wght@300;400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../assets/site.css">
<style>
.page-hero p{{max-width:620px}}
.isk{{margin:28px 0 0;position:relative;max-width:520px}}
.isk input{{width:100%;background:var(--bg2);border:1px solid var(--border2);border-radius:var(--r);color:var(--cream);font-family:var(--fb);font-size:16px;padding:14px 16px 14px 44px;outline:none;transition:border-color var(--tr)}}
.isk input:focus{{border-color:var(--gold)}}
.isk svg{{position:absolute;left:15px;top:50%;transform:translateY(-50%);width:18px;height:18px;stroke:var(--cream3);fill:none;stroke-width:1.6}}
.kart-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:12px;margin-top:36px}}
.kart{{background:var(--bg2);border:1px solid var(--border);border-radius:var(--r);padding:20px 22px;scroll-margin-top:90px}}
.kart:target{{border-color:var(--gold);box-shadow:0 0 0 1px var(--gold)}}
.kart.skrij{{display:none}}
.kart-h{{display:flex;align-items:center;justify-content:space-between;gap:10px;flex-wrap:wrap;margin-bottom:12px}}
.kart h2{{font-family:var(--fd);font-size:22px;font-weight:500;font-style:italic;color:var(--cream);line-height:1.2}}
.kart-al{{display:flex;flex-wrap:wrap;gap:6px;align-items:center}}
.kart-l{{font-family:var(--fm);font-size:9.5px;letter-spacing:.2em;text-transform:uppercase;color:var(--gold);margin-right:4px}}
.kart .tag{{font-size:10px;padding:5px 10px}}
.kart details{{margin-top:14px;border-top:1px solid var(--border);padding-top:10px}}
.kart summary{{cursor:pointer;font-family:var(--fm);font-size:10px;letter-spacing:.15em;text-transform:uppercase;color:var(--cream2);list-style:none;display:flex;align-items:center;gap:8px}}
.kart summary::-webkit-details-marker{{display:none}}
.kart summary::before{{content:'+';color:var(--gold);font-size:14px;width:12px}}
.kart details[open] summary::before{{content:'–'}}
.kart details p{{font-size:13.5px;color:var(--cream2);line-height:1.7;margin-top:10px}}
.kart details b{{color:var(--cream);font-weight:500}}
.nic{{display:none;color:var(--cream2);font-size:15px;margin-top:30px}}
.nic.pokazi{{display:block}}
.al-box{{background:var(--bg2);border:1px solid var(--border);border-left:3px solid var(--gold);border-radius:var(--r);padding:28px 32px;margin-top:48px}}
.al-box h3{{font-family:var(--fd);font-style:italic;font-size:22px;color:var(--cream);margin-bottom:12px}}
.al-box p,.al-box li{{font-size:14px;color:var(--cream2);line-height:1.75}}
.al-box ul{{margin:8px 0 0 18px}}
.al-box p+p{{margin-top:10px}}
.stanje{{font-family:var(--fm);font-size:10.5px;letter-spacing:.1em;color:var(--cream3);margin-top:14px}}
@media(max-width:700px){{.al-box{{padding:22px 20px}}.kart{{padding:18px}}}}
</style>
</head>
<body>
<div class="cursor" aria-hidden="true"></div><div class="cursor-ring" aria-hidden="true"></div>
<div class="grain" aria-hidden="true"></div>

<nav>
  <div class="nav-inner">
    <a href="../" class="nav-logo" aria-label="Roman's Cakes — domov"><img src="../slike/web/logo-gold.png" alt=""><div class="nav-logo-text">Roman's Cakes<span>Veganske torte · Maribor</span></div></a>
    <ul class="nav-links">
      <li><a href="../ponudba/">Ponudba &amp; cenik</a></li>
      <li><a href="../narocilo/">Kako naročiti</a></li>
      <li><a href="../o-nas/">O meni</a></li>
      <li><a href="../kontakt/">Kontakt</a></li>
    </ul>
    <a href="../kontakt/" class="nav-cta">Naročite torto</a>
    <button class="nav-mb" aria-label="Odpri meni" aria-expanded="false" aria-controls="mnav"><span></span><span></span><span></span></button>
  </div>
</nav>
<div id="mnav"><a href="../ponudba/">Ponudba &amp; cenik</a><a href="../narocilo/">Kako naročiti</a><a href="../o-nas/">O meni</a><a href="../kontakt/">Kontakt</a><a href="../kontakt/" class="nav-cta">Naročite torto</a></div>

<main>
<div class="page-hero">
  <div class="wrap">
    <div class="breadcrumb"><a href="../">Domov</a><span>/</span><span class="cur">Alergeni</span></div>
    <div class="lbl">Alergeni in sestavine</div>
    <h1 class="hd">Kaj je <em>v torti.</em></h1>
    <p>Vse torte so 100 % veganske: brez jajc, mleka in drugih živalskih sestavin. Spodaj so za vsako torto iz naše ponudbe navedeni alergeni po Prilogi II Uredbe (EU) 1169/2011 in popoln seznam sestavin. Podatki prihajajo neposredno iz receptur.</p>
    <div class="isk"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg><input type="search" id="isk" placeholder="Poiščite torto …" aria-label="Iskanje torte" autocomplete="off"></div>
    <div class="stanje">Stanje receptur: {datum} · {n} tort</div>
  </div>
</div>

<section class="sec" style="padding-top:40px">
  <div class="wrap">
    <div class="kart-grid" id="kartice">
{kartice}
    </div>
    <p class="nic" id="nic">Te torte ni na seznamu. Vprašajte osebje ali nas pokličite na <a href="tel:+38640758582" style="color:var(--gold)">040 758 582</a>.</p>

    <div class="al-box" id="opombe">
      <h3>Dobro je vedeti</h3>
      <ul>
        <li><strong>Sledi:</strong> vse torte nastajajo v istem obratu, kjer se uporabljajo pšenična moka, soja, arašidi in oreščki (mandlji, lešniki, orehi, pistacija). Vsak izdelek lahko vsebuje njihove sledi, tudi če niso med sestavinami.</li>
        <li><strong>Brez glutenskih sestavin:</strong> torte brez glutenskih sestavin so narejene brez žit z glutenom, v skupnem obratu s pšenično moko.</li>
        <li><strong>Dekoracija:</strong> posebna dekoracija ali jedilna slika lahko dodata sestavine, ki tu niso navedene.</li>
        <li><strong>Alergija?</strong> Pri hujši alergiji pred nakupom pokličite <a href="tel:+38640758582" style="color:var(--gold)">040 758 582</a> ali pišite na <a href="mailto:info@romancakes.com" style="color:var(--gold)">info@romancakes.com</a>, da preverimo konkretno serijo.</li>
      </ul>
      <p style="margin-top:14px">Proizvajalec: Roman Adler s.p., Radvanjska cesta 10A, 2000 Maribor · obrat: Ulica heroja Šaranoviča 36, 2000 Maribor.</p>
    </div>
  </div>
</section>
</main>

<footer>
  <div class="wrap">
    <div class="footer-grid">
      <div><div class="footer-brand"><img src="../slike/web/logo-gold.png" alt=""><b>Roman's Cakes</b></div><p class="footer-desc">Veganska proizvodnja slaščic v Mariboru. Torte po naročilu, rezine in torte brez glutenskih sestavin — brez živalskih sestavin, brez kompromisov pri okusu.</p><div style="margin-top:16px"><span class="vegan-badge">🌱 100 % vegansko</span></div></div>
      <div><div class="footer-h">Ponudba</div><ul class="footer-links"><li><a href="../ponudba/#torte">Torte po naročilu</a></li><li><a href="../ponudba/#okusi">Okusi</a></li><li><a href="../ponudba/#rezine">Rezine &amp; pecivo</a></li><li><a href="../ponudba/#brezglutensko">Brez glutenskih sestavin</a></li><li><a href="./">Alergeni</a></li></ul></div>
      <div><div class="footer-h">Info</div><ul class="footer-links"><li><a href="../narocilo/">Kako naročiti</a></li><li><a href="../o-nas/">O meni</a></li><li><a href="../kontakt/">Kontakt</a></li><li><a href="../pogoji/">Splošni pogoji</a></li><li><a href="../zasebnost/">Zasebnost</a></li></ul></div>
      <div><div class="footer-h">Kontakt</div><ul class="footer-links"><li><a href="tel:+38640758582">040 758 582</a></li><li><a href="mailto:info@romancakes.com">info@romancakes.com</a></li><li>Ulica heroja Šaranoviča 36<br>2000 Maribor</li><li><a href="https://www.facebook.com/romanvegancakes" target="_blank" rel="noopener">Facebook</a></li></ul></div>
    </div>
    <div class="footer-bottom"><div class="footer-copy">© <span data-year>2026</span> Roman Adler s.p., proizvodnja slaščic · Radvanjska cesta 10A, 2000 Maribor · matična št. 7540981000 · davčna št. 43849164 (ni zavezanec za DDV) · info@romancakes.com<br><a href="../pogoji/">Splošni pogoji</a> · <a href="../zasebnost/">Politika zasebnosti</a></div><div class="vegan-badge">🌱 Narejeno z ljubeznijo v Mariboru</div></div>
  </div>
</footer>
<script src="../assets/site.js" defer></script>
<script>
(function(){{
  var i=document.getElementById('isk'),k=document.querySelectorAll('.kart'),n=document.getElementById('nic');
  function norm(s){{return s.toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g,'');}}
  i.addEventListener('input',function(){{
    var q=norm(i.value.trim()),vid=0;
    k.forEach(function(e){{var z=!q||norm(e.dataset.ime).indexOf(q)>-1;e.classList.toggle('skrij',!z);if(z)vid++;}});
    n.classList.toggle('pokazi',vid===0);
  }});
}})();
</script>
</body>
</html>
'''

dst = os.path.join(ROOT, 'alergeni', 'index.html')
os.makedirs(os.path.dirname(dst), exist_ok=True)
with open(dst, 'w', encoding='utf-8', newline='\n') as f:
    f.write(page)
if PREDOGLED: print('!!! PREDOGLED — stran vsebuje nepotrjene podatke, NE objavljaj !!!')
print('OBJAVLJENE (%d):' % n)
for t in objavljene:
    print('  ', t['ime'], '->', t.get('alergeni_text') or 'brez')
print('MANJKA V ERP (%d) — niso na strani:' % len(manjka))
for t in manjka:
    razlog = ZADRZANE[t['ime']] if t['ime'] in ZADRZANE else 'ni recepture' if not t.get('receptura_id') else ('receptura brez sestavin' if not t.get('sestavine')
             else ('nepotrjeni alergeni: ' + ', '.join(t.get('alergeni_nepotrjeni') or []) if t.get('alergeni_nepotrjeni')
                   else 'sestava nepopolna'))
    print('  ', t['ime'], '->', razlog)
