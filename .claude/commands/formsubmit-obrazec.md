# FormSubmit obrazec: aktivacija, priloge, dostava v Gmail in kako ga pravilno testirati

Nastalo v seji Roman's Cakes 13. 10. 2026 (obrazec `kontakt/` → `https://formsubmit.co/info@romancakes.com`).
Uporabi pri vsaki spremembi obrazca ali ko »sporočila ne pridejo«. Logika polj je v `assets/order-form.js`
(opis v CLAUDE.md »Obrazec za naročilo«); ta skill je o dostavi in testiranju.

## Zakaj / arhitektura

- FormSubmit (brez računa) pošlje oddajo na naslov v `action`. **Aktivacija je enkratna, na e-naslov**:
  prva oddaja sproži »Action Required: Activate FormSubmit« → klik »Activate Form«. Testna oddaja z
  localhost je dovolj, aktivacija velja tudi za pravo domeno.
- Skriti `_cc=romanvegancakes@gmail.com`: kopija gre **neposredno** v Gmail. Brez tega je pot
  FormSubmit → Neoserv predal info@ → posredovanje → Gmail, Neoservov filter pa je oddaje dal med smeti in
  jih NI posredoval (13. 10. 2026). Neoserv predal ostane arhiv.
- `enctype="multipart/form-data"` + `<input type="file" name="Slika">` → slika pride kot priloga (skupaj ≤ 10 MB).
  Ime polja ni pomembno (`attachment` ali `Slika`).
- `_subject` nastavi JS ob oddaji (»Povpraševanje: <vrsta> · <datum> · <ime>«); imena polj naj bodo
  enobesedna, ker FormSubmit presledke zamenja s podčrtaji (`Ime_in_priimek`).
- Skrita polja so `disabled` → se ne pošljejo (v e-pošti ni praznih vrstic).

## Konkretni recepti

### Preveri, ali je obrazec aktiviran (brez brskalnika)
```
curl -s -H "Content-Type: application/json" -H "Accept: application/json" \
  -H "Origin: http://127.0.0.1:8765" -H "Referer: http://127.0.0.1:8765/kontakt/" \
  --data-binary '{"_subject":"TEST","_captcha":"false","Ime":"Test"}' https://formsubmit.co/ajax/info@romancakes.com
```
`{"success":"false","message":"This form needs Activation…"}` = ni aktiviran; `"success":"true"` = je.
(Ajax klic pošlje pravo e-pošto — označi ga kot TEST.)

### Prava testna oddaja s sliko in šumniki (headless Chrome, brez MCP)
Pomožna stran `_test-oddaja.html` v korenu (z `<meta charset="utf-8">`!), iframe `kontakt/`, v `onload`:
nastavi polja z `value` + `dispatchEvent(new w.Event('change',{bubbles:true}))`, datoteko dodaj z
`new DataTransfer()` + `dt.items.add(new File([blob],'x.png',{type:'image/png'}))` + `input.files = dt.files`,
nato `submit-btn.click()`. Drugi `onload` (po preusmeritvi) izpiše `kontakt/?poslano=1`.
```
chrome.exe --headless=new --disable-gpu --user-data-dir=<scratch>/hl-profile --window-size=900,1000 \
  --virtual-time-budget=20000 --dump-dom http://127.0.0.1:8765/_test-oddaja.html
```
Lokalni strežnik mora teči (`serve_nocache.py` ali `py -3 -m http.server 8765 --bind 127.0.0.1`). Pomožno stran po testu izbriši.

### Preverjanje dostave
Gmail MCP (račun romanvegancakes): `search_threads "in:anywhere from:formsubmit.co newer_than:1h"`, nato
`get_message` → `attachments[]` mora vsebovati datoteko, `htmlBody` tabelo z vsemi polji. Sporočila so v
zavihku **Posodobitve** (CATEGORY_UPDATES), kopija prek `_cc` pride v ~1 min.

## Gotchas
- **`curl -F` z vrednostmi s šumniki/pomišljajem → FormSubmit izgubi VSA besedilna polja**, ostane samo
  priloga, zadeva postane »New submission from …«. Brskalnik (Chrome) istih podatkov NE izgubi. Ne sklepaj
  iz curl testov, da je obrazec pokvarjen; za multipart testiraj iz brskalnika, za polja uporabi `/ajax/` z JSON.
- Gmail MCP `search_threads` z `newer_than:1h` včasih vrne `{}` tudi, ko so sporočila že v Prejetem (zamik
  indeksa); išči po `from:formsubmit.co` ali po zadevi.
- Roman gleda stran iz predpomnilnika: po spremembi `order-form.js` povečaj `?v=N` v `kontakt/index.html`
  in lokalni strežnik poganjaj s `Cache-Control: no-store` (`scripts/dev/serve_nocache.py <koren repoja>`; vzorec:
  `SimpleHTTPRequestHandler.end_headers` + `send_header('Cache-Control','no-store')`).
- V `_test-*.html` brez `<meta charset>` se vrednosti s šumniki ne ujemajo z `<option>` → `select.value` ostane
  prazen in testi lažno padejo.
