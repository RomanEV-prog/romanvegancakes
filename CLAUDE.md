# Roman's Cakes — spletna stran

Statična stran (HTML/CSS/JS, brez ogrodja in brez build koraka) za vegansko
slaščičarno **Roman Adler s.p.**, Maribor. Komunikacija v slovenščini.

## Gostovanje

- GitHub Pages streže **vejo `live`** (mapa `/`) na lastni domeni **https://romancakes.com**
  (datoteka `CNAME`, HTTPS vsiljen; stari naslov romanev-prog.github.io/romanvegancakes/ preusmerja).
- **`live` = začasna stran »v pripravi«** (samo index.html, logo, favicon, CNAME; noindex), od 12. 10. 2026.
  Roman je odločil, da prava vsebina ne sme biti javna, dokler ni urejena.
- **`master` = delovna veja**, push nanjo NIČESAR ne objavi. Preverjanje lokalno (`http.server`).
- Objava prave strani, ko Roman potrdi: `git push origin master:live --force` (veja `live` je orphan,
  zato je force potreben) ali pa Pages source nazaj na `master` prek `gh api -X PUT …/pages`.
  Oboje = produkcija → **vprašaj prej**.
- Povezave ostanejo **relativne** (`../assets/…`, `./`), nikoli absolutne `/…` —
  stran mora delovati tudi pod podpotjo, če se domena kdaj odklopi.
- DNS: zona je v **cPanelu gostovanja adlerhub.eu pri Neoservu** (sh37.neoserv.si, romancakes.com
  je tam dodana domena; vstop prek moj.neoserv.si → Modri paket → cPanel → Zone Editor).
  Domena je registrirana pri **Domenci** (isti račun adlerrroman@gmail.com), ne v Neoserv panelu.
  Apex A → 185.199.108–111.153 (GitHub Pages), `www` CNAME → romanev-prog.github.io.
  MX/mail/webmail/cpanel zapisi ostajajo na 152.89.235.155 (pošta info@romancakes.com je pri Neoservu).
  SPF: `v=spf1 ip4:152.89.235.155 include:_spf.mail-neoserv.si +mx ~all` (brez `+a`, 12. 10. 2026).
- `git push` na `master` je varen (ni objava); objava je samo prek veje `live`.
- Privzeta veja na GitHubu je `master` (od 12. 10. 2026). Veja `main` je stara (le README + prvotni index) in se ne uporablja.

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

`kontakt/` pošilja prek FormSubmit (`https://formsubmit.co/info@romancakes.com`),
brez captche, s honeypotom, `_next` nazaj na `kontakt/?poslano=1`. **Prva oddaja sproži
aktivacijski e-mail** na ta naslov — dokler Roman ne klikne potrditve, sporočila ne pridejo.

## Preverjanje

Lokalno: `py -3 -m http.server 8765 --bind 127.0.0.1` v korenu, nato brskalnik.
Preveri vseh 7 strani (namizje + 390 px), konzolo brez napak, skok na sidra (`ponudba/#cenik`).
V živo: `curl -sI https://romancakes.com/` (200), `gh api repos/RomanEV-prog/romanvegancakes/pages`.

## Pravni sklop (stanje 11. 10. 2026)

- `pogoji/` — splošni pogoji (ZVPot-1: brez odstopa za pokvarljivo blago po meri, čl. 135;
  izjava ZIsRPS: ne priznava IRPS; EU ODR platforma je ukinjena od 20. 7. 2025 → brez povezave)
- `zasebnost/` — GDPR; brez piškotkov/analitike (zato brez pasice — izrecno zapisano)
- noga vseh strani = ZEPT identiteta (ime, naslov, matična, ID za DDV, e-pošta)
- Roman JE zavezanec za DDV (SI43849164) → cene »vključujejo DDV«, ne klavzula malega zavezanca
- obrazec: kljukica »seznanjen s pogoji + soglasje zasebnost« (required)
- ob uvedbi analitike/Meta piksla → pasica s privolitvijo PREJ

## Skilli

- `.claude/commands/github-pages-domena.md` — selitev domene, veja `live`, objava prave strani
- `~/.claude/commands/neoserv-domenca-dns.md` — kje so domene (Domenca) in DNS zona (cPanel Neoserv), UAPI recepti
