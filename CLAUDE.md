# Roman's Cakes — spletna stran

Statična stran (HTML/CSS/JS, brez ogrodja in brez build koraka) za vegansko
slaščičarno **Roman Adler s.p.**, Maribor. Komunikacija v slovenščini.

## Gostovanje

- GitHub Pages iz veje `master`, mapa `/`: https://romanev-prog.github.io/romanvegancakes/
- Stran živi pod podpotjo `/romanvegancakes/` → **vse povezave so relativne**
  (`../assets/…`, `./`), nikoli absolutne `/…`.
- `git push` na `master` = objava na produkcijo → **vprašaj prej**.
- Veja `main` na GitHubu je stara (le README + prvotni index) in se ne uporablja.

## Struktura

- `index.html`, `ponudba/`, `narocilo/`, `o-nas/`, `kontakt/`, `zasebnost/` — vsaka stran svoj `index.html`
- `assets/site.css` + `assets/site.js` — skupni slog in logika (navigacija, kazalec, zrno, prehodi, `.rv` razkrivanje, skok na sidro). Stran-specifičen CSS ostane inline v `<style>`.
- `slike/web/` — **edine slike, ki gredo na splet** (WebP ≤ 1400 px, ~40–100 KB; `logo-gold.png`, `icon-512.png`, `apple-touch-icon.png`).
- `slike/*` (izvorne fotke, 800+ MB, PDF-ji z internimi dokumenti) in korenski PDF/PNG so v `.gitignore`. Nove slike pretvori s Pillow (`py -3`, glej vzorec v zgodovini) in jih poimenuj po vsebini (`torta-lesnik.webp`).

## Vir podatkov o izdelkih

Okusi, cene, alergeni prihajajo iz ERP-ja `C:\Users\adler\Desktop\proizvodnja\ze program\romans-cake`
(Electron + Express + SQLite prek sql.js). Produkcijska baza teče na kuhinjskem PC-ju
`romanscakes` (Tailscale 100.77.108.53), API `/api/artikli`, `/api/okusi`, `/api/recepture`
zahteva PIN (mobil login). Zadnja lokalna kopija: `C:\Users\adler\Desktop\ARHIV-romans-cake-podatki-20260908\db\romans-cake.db`
(beri z `py -3 -I`, `sqlite3.connect('file:...?mode=ro', uri=True)`).

Kaj je iz baze (stanje 8. 9. 2026):
- cenik `receptura_variante.cena_prevzem` za 8/10/12/16/24 kosov: čokoladna 24/30/36/46/66 €, lešnikova in orehova 26/32/38/48/68 €
- okusi + `doplacilo` (premium +4 € Snickers/Kinder/Kinder Bueno/Rafaelo*, +5 € pistacija/pasijonka/mango)
- rezine 4,50–6 € / kos; DDV 9,5 %
- alergeni v bazi so vneseni le za moko (gluten) — oreščki na strani so dodeljeni po imenu okusa, ne iz baze

Kaj je **predpostavka** (preveri z Romanom): beli biskvit po isti ceni kot čokoladni;
rok naročila 3/5 dni; plačilo ob prevzemu; spremembe do 2 dni pred prevzemom.

## Obrazec za naročilo

`kontakt/` pošilja prek FormSubmit (`https://formsubmit.co/romansvegancakes@gmail.com`),
brez captche, s honeypotom, `_next` nazaj na `kontakt/?poslano=1`. **Prva oddaja sproži
aktivacijski e-mail** na ta naslov — dokler Roman ne klikne potrditve, sporočila ne pridejo.

## Preverjanje

Lokalno: `py -3 -m http.server 8765 --bind 127.0.0.1` v korenu, nato brskalnik.
Preveri vseh 6 strani (namizje + 390 px), konzolo brez napak, skok na sidra (`ponudba/#cenik`).
