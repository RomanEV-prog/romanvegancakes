# Posodobitev Google recenzij na spletni strani

Nastalo iz seje romancakes 2026-11-06. Uporabi, ko je treba posodobiti
razdelek z Google recenzijami na `index.html` z novimi mnenji z Google Maps.

## Zakaj / arhitektura

Google Maps ne ponuja javnega API-ja za recenzije brez ključa. Recenzije
poberemo direktno iz DOM-a z Chrome MCP `javascript_tool`. Rezultati so
pogosto okrnjeni (besedilo se konča z `…`) — celotnih besedil ni mogoče
zanesljivo dobiti brez klika na vsako recenzijo posebej.

Recenzijski kartici na strani sta dve vrsti: `.rev-card--google` (Google) in
brez tega razreda (ostale platforme). Novo Google recenzijo dodaj kot
`.rev-card rv rev-card--google` z atributom `data-d="N"` (zamik animacije v
ms, korak 80).

## Konkretni recepti

### 1. Naloži Chrome MCP orodja

```
ToolSearch: select:mcp__claude-in-chrome__tabs_context_mcp,mcp__claude-in-chrome__navigate,mcp__claude-in-chrome__javascript_tool,mcp__claude-in-chrome__tabs_create_mcp
```

### 2. Odpri Google Maps profil

Navigiraj na Maps stran podjetja (URL iz `index.html` ali poišči po imenu).
Roman's Cakes Maribor: poišči prek `mcp__claude-in-chrome__navigate` na
Google Maps z iskanjem "Roman's Cakes Maribor".

### 3. Naloži vse recenzije

```javascript
// Klikni "Več mnenj" gumb, če obstaja
var btn = document.querySelector('[aria-label*="recenzij"], [data-value*="recenzij"]');
if (btn) btn.click();
```

Počakaj 2 sekundi, nato preberi recenzije:

```javascript
// Pridobi vse recenzije (Google Maps DOM razredi so naključni, iščemo po vzorcu)
var reviews = [];
// Besedilo recenzije
var texts = document.querySelectorAll('[class*="wiI7pd"], [class*="MyEned"], [jsname="bN97Pc"]');
// Ime avtorja
var names = document.querySelectorAll('[class*="d4r55"], [class*="AL1nh"]');
// Ocena (zvezde)
var stars = document.querySelectorAll('[class*="kvMYJc"], [aria-label*="zvezd"]');
// Kontejner recenzije
var cards = document.querySelectorAll('[class*="jftiEf"]');

cards.forEach(function(card, i) {
  var nameEl = card.querySelector('[class*="d4r55"]');
  var textEl = card.querySelector('[class*="wiI7pd"]');
  var starEl = card.querySelector('[aria-label*="zvezd"]');
  reviews.push({
    name: nameEl ? nameEl.textContent.trim() : '',
    text: textEl ? textEl.textContent.trim() : '',
    stars: starEl ? starEl.getAttribute('aria-label') : ''
  });
});
JSON.stringify(reviews);
```

### 4. HTML vzorec za novo kartico

```html
<div class="rev-card rv rev-card--google" data-d="80">
  <div class="rev-source">
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
      <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
      <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
      <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l3.66-2.84z" fill="#FBBC05"/>
      <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
    </svg>
    <span>Google</span>
  </div>
  <div class="rev-stars">★★★★★</div>
  <div class="rev-open">"</div>
  <p class="rev-q">BESEDILO RECENZIJE</p>
  <div class="rev-who">
    <span class="rev-name">IME AVTORJA</span>
    <span class="rev-occ">Google recenzija</span>
  </div>
</div>
```

`data-d` vrednosti: obstoječe kartice imajo `80, 160, 240...` — nadaljuj vzorec.

## E2E verifikacija

```
py -3 -m http.server 8765 --bind 127.0.0.1
```
Odpri `http://127.0.0.1:8765`, preveritaj razdelek MNENJA — nove kartice
vidne, animacija deluje (`.rv` razkrivanje pri scrollu), konzola brez napak.

## Gotchas

**Besedilo okrnjeno z „…"**: DOM vrne okrnjeno besedilo (`Najboljše veganske...`).
Vzrok: Google Maps privzeto skrajša dolga mnenja. Rešitev: poskusi klikniti
gumbe za razširitev (`[aria-label*="Razširi"]`), ali pa shrani skrajšano
besedilo in dodaj opombo, da je okrnjeno.

**DOM razredi so naključni**: Google Maps generira razrede kot `jftiEf`,
`d4r55`, `wiI7pd` — ti se občasno spremenijo ob posodobitvi Googla.
Simptom: `querySelectorAll` vrne prazne rezultate. Rešitev: preizkusi
alternativne selektorje (`[jsname]`, `[aria-label*="zvezd"]`, besedilne
vsebine).

**"Več mnenj" gumb**: Privzeto so vidne le 3 recenzije. Klikni gumb za
nalaganje vseh. Ime gumba v slovenščini: "Več mnenj (N)".

**Duplikati**: Pred dodajanjem novih kartic preveri obstoječe v `index.html`
(`grep rev-name`) — enako ime že obstaja? Posodobi besedilo, ne dodaj dvakrat.
