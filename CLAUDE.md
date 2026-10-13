# Roman's Cakes — spletna stran

Statična stran (HTML/CSS/JS, brez ogrodja in brez build koraka) za vegansko
proizvodnjo slaščic **Roman Adler s.p.**, Maribor (AJPES: proizvodnja slaščic, NE slaščičarna — tako tudi na strani). Komunikacija v slovenščini.

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
- Roki naročanja: vsaka torta 10 dni (tudi jedilna slika, BG, presna — Roman 13. 10. 2026); samo večja naročila in dogodki 3 tedne.
- Brezplačna sprememba (če izvedljiva) ali odpoved najpozneje 3 dni pred prevzemom.
- Prevzem Ulica heroja Šaranoviča 36, Maribor; telefon 040 758 582.
- Vegan od 2013, peče od 2018.
- Alergeni na strani so iz ERP receptur (12. 10. 2026): `GET /api/recepture` (polje `sest`, poly → rekurzivno)
  + `GET /api/surovine` (polje `alergeni`, šifrant `GET /api/alergeni`). Oznaka pri okusu = krema/polnilo (torta minus biskvit),
  tabela `#biskviti` = alergeni biskvitov. Okusi brez oznake nimajo recepture v ERP (Čokoladna, Kinder; BG čokoladna in BG pistacija
  imata prazno sestavo). Ob spremembi receptur ponovno potegni in prepiši oznake, ne ugibaj po imenu.
- **»Brez glutena« na strani NE piše** (Uredba 828/2014 zahteva ≤ 20 mg/kg, Roman tega ne zagotavlja). Od 13. 10. 2026 povsod
  »brez glutenskih sestavin« / »torte brez glutenskih sestavin« + opomba o sledeh iz skupnega obrata. Sidro `#brezglutensko` ostaja.
- **Presne torte** (13. 10. 2026, Romanova želja): sekcija `ponudba/#presne` in vrsta v obrazcu, rok 10 dni. V ERP ni artiklov ne receptur
  (le postopek »Presna sladica«), zato na strani BREZ cen, okusov in alergenov — vse »po dogovoru«. Ko Roman doda artikle, dopolni cenik.
  Sum: recepturi »Malina čokolada« in »Bounty BG« (mandlji, orehi, datelji, kokosovo olje, brez moke) sta morda presni torti.
- Obstojnost, temperatura hrambe in zamrzovanje po različicah še niso potrjeni. Ne objavljaj splošnih zagotovil; besedila napotujejo na deklaracijo in dogovor za konkretni izdelek.

## Stran `alergeni/` in QR koda (od 13. 10. 2026)

- Namen: **ena QR koda, ena nalepka** za vitrine B2B partnerjev → `https://romancakes.com/alergeni/` (noindex). Kartica na torto
  = alergeni CELE torte (biskvit + krema) in polne sestavine, vir je ERP deklaracija (`/api/deklaracije/preview`, isti izračun kot tisk).
  Pravno: nepredpakirana živila, Uredba 1169/2011 Pril. II — alergeni morajo biti pisno na prodajnem mestu; QR sam ni dovolj, partner
  naj ima tudi natisnjen list.
- Osvežitev ob spremembi receptur: `py -3 -I scripts/alergeni_dump.py <ERP-URL> [--token]` → `scripts/alergeni-dump.json`, nato
  `py -3 -I scripts/alergeni_gen.py` → `alergeni/index.html`. Skripta izpiše OBJAVLJENE in MANJKA V ERP. Na stran gre samo torta z
  recepturo, sestavinami in potrjenimi alergeni; `ZADRZANE` v gen.py so izjeme z očitno napačno sestavo (odstrani, ko ERP popravi).
  `ALERGENI_PREDOGLED=1` je samo za pregled postavitve, nikoli za objavo.
- Prenos iz žive baze: ERP mobilni piškotek je HttpOnly, Chrome blokira fetch na localhost (Local Network Access) in MCP izpis reže
  pri ~1000 znakih ter blokira base64. Deluje: v ERP zavihku `javascript_tool` sestavi JSON → `location.href = 'http://127.0.0.1:<port>/?d=' + encodeURIComponent(json)`
  na lokalni python GET sprejemnik (urlencoded, do 64 KB). Za branje gre tudi `get_page_text` po `document.body.innerHTML = '<article><pre>…'`.
- Stanje 13. 10. 2026: objavljenih 14 tort. Niso na strani: Čokoladna torta, Čokolada Malina (BG), Pistacija BG (receptura brez sestavin),
  Kinder (ni recepture), Tiramisu (KEKSI PETIT/Spekulatius brez alergenov v ERP) in Malina čokolada (receptura brez čokolade in moke, sum zamenjave z BG).
- QR: `qr/alergeni-qr.svg|.png` (črna, 740 px, korekcija H), `qr/alergeni-qr-zlata.svg`. Generirano s `segno`. Deluje šele po objavi prave strani.

## Pošta info@romancakes.com (stanje 13. 10. 2026)

- Predal je pri Neoservu (cPanel `adlerhub`, kvota 250 MB). **Posredovanje** info@ → **romanvegancakes@gmail.com**
  (cPanel UAPI `Email/add_forwarder`, 13. 10. 2026); predal hrani tudi kopijo → občasno izprazni.
- V Gmailu romanvegancakes je info@romancakes.com dodan pod »Pošlji e-poštno sporočilo kot« (SMTP mail.romancakes.com:465 SSL,
  potrjeno 13. 10. 2026) in nastavljeno »Odgovori z istega naslova, na katerega je bilo poslano sporočilo«.
  Privzeti pošiljatelj ostaja romanvegancakes@gmail.com (račun služi tudi greenheart@adlerhub.eu).
- SPF in DKIM za romancakes.com veljavna (cPanel EmailAuth); testno sporočilo iz Gmaila kot info@ pristane v Prejetem, ne v vsiljeni pošti.
- Gmail MCP v Claude Code je povezan z računom **romanvegancakes@gmail.com** (ne adlerrroman).

## Obrazec za naročilo

`kontakt/` pošilja prek FormSubmit (`https://formsubmit.co/info@romancakes.com`),
brez captche, s honeypotom, `_next` nazaj na `kontakt/?poslano=1`, `enctype=multipart/form-data`
(priloga `attachment` za jedilno sliko, skupaj do 10 MB).
- **Aktivirano 13. 10. 2026** (Roman kliknil »Activate Form«). Preverjeno z oddajo iz brskalnika (headless Chrome):
  vsa polja s šumniki + priloga slike prispejo. Sporočila pristanejo v Gmailu v zavihku **Posodobitve**.
- Skriti `_cc=romanvegancakes@gmail.com`: FormSubmit pošlje kopijo neposredno v Gmail, mimo Neoserv posredovanja
  (Neoservov filter je oddaje dal med smeti in jih ni posredoval; kopija pride v ~1 min).
- Past pri testiranju: `curl -F` z vrednostmi s šumniki → FormSubmit izgubi VSA besedilna polja (ostane le priloga).
  Brskalnik tega problema nima. Za test uporabi `formsubmit.co/ajax/...` z JSON ali pravo oddajo iz headless Chroma.
- Logika je v `assets/order-form.js` (naloženo kot `?v=N` — ob spremembi povečaj N, Chrome je držal staro skripto).
  Vrsta določa polja: torta iz ponudbe (okus, biskvit), torta po naročilu (biskvit, krema 1, krema 2),
  BG (4 okusi, ≤ 10 kosov), presna, rezine po kosih (4 vrstice okus + kosov), dogodek, vprašanje. Skrita polja so `disabled`.
  Rok: 10 dni za vse, 21 za dogodek/več kosov; opozorilo takoj ob vnosu datuma, oddaja blokirana. Dekoracija ločeno,
  polje za napis in polje za sliko se pokažeta po izbiri.
- Testiranje brez Chrome MCP: headless Chrome (`chrome.exe --headless=new --dump-dom/--screenshot`) na pomožni strani
  z iframe 390 px (`--window-size` pod ~500 px ne deluje); testna stran MORA imeti `<meta charset="utf-8">`.
  Lokalni strežnik raje z `Cache-Control: no-store` (Roman je videl stare strani iz predpomnilnika).

## Preverjanje

Lokalno: `py -3 -m http.server 8765 --bind 127.0.0.1` v korenu, nato brskalnik.
Preveri vseh 7 strani (namizje + 390 px), konzolo brez napak, skok na sidra (`ponudba/#cenik`).
V živo: `curl -sI https://romancakes.com/` (200), `gh api repos/RomanEV-prog/romanvegancakes/pages`.

## Pravni sklop (stanje 12. 10. 2026)

- `pogoji/` — splošni pogoji (ZVPot-1: brez odstopa za pokvarljivo blago po meri, čl. 135;
  izjava ZIsRPS: ne priznava IRPS; EU ODR platforma je ukinjena od 20. 7. 2025 → brez povezave)
- `zasebnost/` — GDPR; brez piškotkov/analitike (zato brez pasice — izrecno zapisano)
- noga vseh strani = ZEPT 5. člen (firma, sedež, matična, davčna št., e-pošta); pogoji §1 še UVHVVR in nadzorna organa
- reklamacije po ZVPot-1: obvestilo v 2 mesecih (84. čl.), pisni odgovor v 8 dneh če prereka (85. čl.), odstop v 30 dneh (83. čl.); rokov ni dovoljeno krajšati (79. čl.)
- »brez glutena« = Uredba (EU) 828/2014, ≤ 20 mg/kg glutena v prodanem izdelku — Roman mora to zagotoviti ali preimenovati
- Roman NI zavezanec za DDV (mali davčni zavezanec, 94. člen ZDDV-1; davčna št. 43849164, brez predpone SI) → cene so »končne«,
  klavzula »DDV ni obračunan na podlagi 1. odstavka 94. člena ZDDV-1«; NIKOLI »vključujejo DDV« ali »ID za DDV«. (Popravljeno 12. 10. 2026, prej napačno.)
- obrazec: kljukica »seznanjen s pogoji + soglasje zasebnost« (required)
- ob uvedbi analitike/Meta piksla → pasica s privolitvijo PREJ

## Skilli

- `.claude/commands/github-pages-domena.md` — selitev domene, veja `live`, objava prave strani
- `.claude/commands/erp-alergeni-dump.md` — žive deklaracije iz ERP (PIN, HttpOnly, prenos iz MCP zavihka), osvežitev `alergeni/`
- `.claude/commands/formsubmit-obrazec.md` — aktivacija, `_cc` v Gmail, priloge, prava testna oddaja; past `curl -F` + šumniki
- `.claude/commands/headless-chrome-test.md` — posnetki in testi brez Chrome MCP, mobilni pogled prek iframe
- `~/.claude/commands/neoserv-domenca-dns.md` — kje so domene (Domenca) in DNS zona (cPanel Neoserv), UAPI recepti
