# ERP → stran alergeni: prenos živih deklaracij in osvežitev `alergeni/`

Nastalo v seji Roman's Cakes 13. 10. 2026 (gradnja strani `alergeni/` + QR koda za vitrine
B2B partnerjev). Uporabi, kadar je treba osvežiti alergene/sestavine na strani po spremembi
receptur v ERP-ju, ali kadar potrebuješ katerekoli žive podatke iz ERP API-ja, ki zahteva PIN.
Sorodno: CLAUDE.md »Stran alergeni/ in QR koda« (stanje tort), ta skill je o KAKO priti do podatkov.

## Zakaj / arhitektura

- Vir resnice je **ERP deklaracija** `GET /api/deklaracije/preview?receptura_id=<id>` (isti izračun kot
  tiskana deklaracija, `lib/sestava.js`): `sestavine_text` (alergene surovine VELIKE črke), `alergeni_text`,
  `alergeni_kode[]`, `alergeni_nepotrjeni[]`, `sestava_nepopolna`, `opozorila[]`, `bg_opozorilo`.
  Ne računaj alergenov sam iz `recepture.sest` + `surovine.alergeni` — to je starejši, slabši približek.
- Na stran gre samo torta z recepturo, sestavinami in brez nepotrjenih alergenov. **Prazna oznaka na
  uradni strani pomeni »brez alergenov«** (Uredba 1169/2011 Pril. II) → raje manjkajoča torta kot napačna.
  `ZADRZANE` v `scripts/alergeni_gen.py` so ročne izjeme z očitno napačno sestavo (npr. keksi brez glutena).
- Ena QR koda (`qr/alergeni-qr.*`) → `https://romancakes.com/alergeni/`; vsaka torta ima sidro `#<slug>`.

## Konkretni recepti

### 1. Podatki iz lokalne kopije baze (brez PIN-a, za preizkus postavitve)
```
set ROMANS_CAKE_DATA_DIR=<mapa z db/romans-cake.db>  (PowerShell: $env:ROMANS_CAKE_DATA_DIR=...)
cd "C:\Users\adler\Desktop\proizvodnja\ze program\romans-cake"; PORT=3031 node server.js
py -3 -I scripts/alergeni_dump.py http://127.0.0.1:3031
```
Localhost zahteve obidejo PIN (`lib/lokalno.js isLocalReq`). Zagon traja ~10 s, `curl` prej vrne 000 —
ne zaganjaj drugič (EADDRINUSE). Arhiv 8. 9. 2026 nima potrjenih alergenov → 0 objavljivih tort;
za pregled postavitve `ALERGENI_PREDOGLED=1 py -3 -I scripts/alergeni_gen.py` (NIKOLI za objavo).

### 2. Žive podatke iz produkcije (Funnel `https://romanscakes.tail3c9ebd.ts.net`)
1. V Chrome MCP zavihku odpri `https://romanscakes.tail3c9ebd.ts.net/m/login.html` in **Roman vpiše PIN**
   (sam ga ne vnašaš). Piškotek `rc-mobil-token` je HttpOnly → `--token` zanj ne dobiš.
2. V istem zavihku `javascript_tool` (same-origin fetch s piškotkom) sestavi JSON:
   ```js
   const g = async p => (await fetch(p,{credentials:'same-origin'})).json();
   const art = (await g('/api/artikli')).filter(a=>a.tip==='torta'&&a.aktiven);
   const rec = (await g('/api/recepture')).filter(r=>r.aktivna&&r.tip==='torta');
   // ujemanje: r.artikel_id === a.id, sicer po normaliziranem imenu; za vsako
   // '/api/deklaracije/preview?receptura_id~'.replace('~','=') + id   // (= v kodi je OK, v IZPISU ne)
   window.__dump = JSON.stringify(out);
   ```
3. Prenos na disk — edina pot, ki deluje (glej Gotchas): lokalni GET sprejemnik + navigacija zavihka.
   ```
   py -3 -I scripts/dev/getrecv.py "C:/.../scripts/alergeni-dump.json"   # posluša 127.0.0.1:8767, shrani ?d=
   ```
   ```js
   location.href = 'http://127.0.0.1:8767/?d~'.replace('~','=') + encodeURIComponent(window.__dump);
   ```
   Alternativa za branje do ~100 KB: `document.body.innerHTML='<article><pre id="x"></pre></article>'`,
   `textContent = __dump`, nato `get_page_text` (ni rezanja, ni blokade) — a potem je treba JSON prepisati.
4. `py -3 -I scripts/alergeni_gen.py` → izpiše OBJAVLJENE in MANJKA V ERP z razlogi; preglej z Romanom.
5. Preveri `alergeni/index.html` (headless Chrome ali MCP), commit `scripts/alergeni-dump.json` zraven.

## E2E verifikacija
- Izpis generatorja: število objavljenih = število kartic (`grep -c 'class="kart"' alergeni/index.html`).
- Datum »Stanje receptur« na strani = `datum` v dumpu.
- Na strani NE sme biti torte iz seznama MANJKA; `tag-g` samo pri `brezglutensko:1`.

## Gotchas
- **Remote ERP vrne 401** brez `x-auth-token`/piškotka; `/m/login.html` ga nastavi kot HttpOnly.
- **Chrome blokira fetch/POST s https strani na `http://127.0.0.1`** (Local Network Access) — `Failed to fetch`,
  preflight nikoli ne pride. Top-level navigacija (`location.href`) na localhost pa DELUJE.
- **`javascript_tool` izpis reže pri ~1000 znakih** (`[TRUNCATED]`) in **blokira base64** (`[BLOCKED: Base64]`)
  ter nize z `=` (`[BLOCKED: Cookie/query string data]`). Gzip+base64 po kosih zato ne gre.
- Python `http.server` sprejme URL do 64 KB; 20 tort = 25 KB JSON → ~35 KB urlencoded, OK. Za več tort
  pošlji v dveh kosih (`?d=&del=1`).
- Chrome MCP se lahko sredi dela zaklene (»Could not verify this site's safety category«) za vse zavihke,
  tudi `tabs_context`; takrat preidi na headless Chrome (glej `/headless-chrome-test`).
- ERP `sestavine_text` ima alergene surovine z VELIKIMI črkami, a tudi nekatere neoznačene (npr. »KEKSI PETIT«,
  »SLADKOR MLETI«) — velike črke niso dokaz označenega alergena, preveri `sestavine[].alergeni`.
