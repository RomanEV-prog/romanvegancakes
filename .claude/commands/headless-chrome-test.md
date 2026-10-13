# Preverjanje strani s headless Chromom (ko Chrome MCP ne deluje)

Nastalo v seji Roman's Cakes 13. 10. 2026, ko je Chrome MCP razširitev za vse zavihke vračala
»Could not verify this site's safety category. Blocking as a precaution« (tudi `tabs_context_mcp`,
tudi po minutah). Uporabi za posnetke zaslona, meritve prelivanja, JS scenarije obrazcev in prave oddaje
obrazcev brez MCP-ja. Chrome: `C:\Program Files\Google\Chrome\Application\chrome.exe`.

## Recepti

### Posnetek zaslona / DOM
```
CH="/c/Program Files/Google/Chrome/Application/chrome.exe"
"$CH" --headless=new --disable-gpu --hide-scrollbars --no-first-run --user-data-dir="$SCRATCH/hl-profile" \
  --window-size=1280,1000 --virtual-time-budget=5000 --screenshot="$SCRATCH/shot.png" http://127.0.0.1:8765/ponudba/
"$CH" --headless=new --disable-gpu --no-first-run --user-data-dir="$SCRATCH/hl-profile" \
  --window-size=600,1900 --virtual-time-budget=8000 --dump-dom http://127.0.0.1:8765/_test.html | sed -n '/<pre id="r"/,/<\/pre>/p'
```
Sliko preberi z orodjem Read. `--user-data-dir` naj bo v scratchpadu (po seji izbriši).

### Mobilni pogled 390 px — prek iframe, ne prek `--window-size`
`--window-size=390,…` NE da mobilnega pogleda (okno ima minimalno širino ~500 px; stran je obrezana,
besedilo odrezano, videti je kot prelivanje). Namesto tega pomožna stran v korenu repoja (same-origin):
```html
<!doctype html><html><head><meta charset="utf-8"></head><body style="margin:0;background:#222">
<iframe id="f" src="alergeni/" style="width:390px;height:1200px;border:0"></iframe><pre id="r"></pre>
<script>document.getElementById('f').onload=function(){var d=this.contentDocument;
 d.querySelectorAll('.rv').forEach(e=>e.classList.add('in'));   // razkrij animirane bloke
 document.getElementById('r').textContent='scrollW='+d.documentElement.scrollWidth+' innerW='+this.contentWindow.innerWidth}</script>
</body></html>
```
Zaženi z `--window-size=600,1300` in `--dump-dom` (meritev) ali `--screenshot`. `scrollW ≤ innerW` = brez prelivanja.

### JS scenariji obrazca
V `onload` iframe-a: `set(id,v)` = `value` + `dispatchEvent(new w.Event('change',{bubbles:true}))` (+ `input`),
`vis(id)` = `!e.hidden && e.offsetParent!==null`; rezultate zapiši v `<pre id="r">` in preberi z `--dump-dom`.
Za pravo oddajo z datoteko glej `/formsubmit-obrazec`.

## Gotchas
- **`<meta charset="utf-8">` v pomožni strani je obvezen** — sicer se nizi s šumniki ne ujemajo z `<option>`
  vrednostmi in `select.value` ostane prazen (lažno negativni testi, izgubljenih 10 min).
- Sidro v URL (`ponudba/#presne`) + `.rv` animacija → posnetek je skoraj prazen (4 KB). Dodaj `.in` vsem `.rv`
  in `scrollIntoView` v iframe-u.
- `--virtual-time-budget` počaka na `setTimeout`/fetch, ne pa na pravo omrežje; za oddajo na zunanji servis daj ≥ 20000.
- Pomožne `_test*.html` v korenu repoja izbriši pred commitom (`git status`).
- Lokalni `http.server` dovoli predpomnjenje → uporabnik vidi stare strani; `py -3 -I scripts/dev/serve_nocache.py "<koren repoja>"` (vrata 8765, no-store).
