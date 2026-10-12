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

## Potrjeno z Romanom 12. 10. 2026

Ti podatki nadomestijo stare cene in predpostavke iz kopije ERP z dne 8. 9. 2026:
- Na strani so SAMO torte, aktivne v blagajni: `GET /api/artikli` (tip torta, aktiven=1) — 20 tort 12. 10. 2026.
  Cena na kos = `artikli.cena_kos` (čokoladna 4,50; 4,90; 5; 5,50; pistacija in bela malina 6 €). Tiramisu je v blagajni
  vpisan 4,00, Roman potrdil 4,90 (12. 10. 2026) — na strani 4,90, blagajno popravi Roman.
  Okusi brez artikla (Nutela, Oreo, Rafaelo, vanilija, ananas, lešnikova, orehova …) NISO na strani; ob dodajanju artikla v blagajni dodaj tudi tu.
- Torte: 8, 10 ali 12 kosov, večje po dogovoru. Brezglutenske do 10 kosov.
- BG: čokoladna 4,50 €/kos, čokolada–malina in Bounty 5 €/kos, pistacija 6 €/kos; ista cena tudi za 10 kosov.
- Biskvit in krema se izbirata poljubno. Lešnikov in orehov biskvit: doplačilo na CELO torto po dogovoru; znesek še ni določen.
- Napis brezplačen. Jedilna slika 8 € na torto. Posebna dekoracija po dogovoru.
- Plačilo z gotovino ali kartico pri vseh naročilih, tudi ob dostavi. Obvezno predplačilo nad 100 € ni potrjeno.
- Dostava po dogovoru, cena glede na lokacijo, potrjena ob naročilu.
- Odgovor na povpraševanje v treh dneh (ne le delovnih); to še ni samodejna potrditev naročila.
- Roki naročanja: 10 dni; jedilna slika, BG in posebni okusi 14 dni; večja naročila in dogodki 3 tedne.
- Brezplačna sprememba (če izvedljiva) ali odpoved najpozneje 3 dni pred prevzemom.
- Prevzem Ulica heroja Šaranoviča 36, Maribor; telefon 040 758 582.
- Vegan od 2013, peče od 2018.
- Alergeni na strani so iz ERP receptur (12. 10. 2026): `GET /api/recepture` (polje `sest`, poly → rekurzivno)
  + `GET /api/surovine` (polje `alergeni`, šifrant `GET /api/alergeni`). Oznaka pri okusu = krema/polnilo (torta minus biskvit),
  tabela `#biskviti` = alergeni biskvitov. Okusi brez oznake nimajo recepture v ERP (Čokoladna, Kinder; BG čokoladna in BG pistacija
  imata prazno sestavo). Ob spremembi receptur ponovno potegni in prepiši oznake, ne ugibaj po imenu.
- Obstojnost, temperatura hrambe in zamrzovanje po različicah še niso potrjeni. Ne objavljaj splošnih zagotovil; besedila napotujejo na deklaracijo in dogovor za konkretni izdelek.

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
