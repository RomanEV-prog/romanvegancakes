# Batch posodobitev navigacije na vseh statičnih HTML straneh

Nastalo v seji romancakes 2026-10-29, ko smo dodali "Za podjetja" v nav na
9 straneh. Uporabi, ko dodajaš ali preimenujuješ nav postavko na vseh
statičnih straneh hkrati.

## Zakaj / arhitektura

Stran nima build sistema — vsaka stran ima nav HTML dobesedno vgrajen. Sprememba
nav pomeni ročno urejanje 9+ datotek. Python skripta poišče vzorec in ga zamenja.

**Kritično:** Nav in footer pogosto vsebujeta ISTI `<li><a href="...">` niz.
`re.sub` zamenja VSE pojavitve v datoteki — brez omejitve na nav blok torej
zamenja tudi footer. Rezultat: podvojen vnos v footerju z napačnim HTML.

## Konkretni recept

**Varni pristop — ločeni koraki za nav in footer:**

```python
import re, glob

files = glob.glob("*/index.html") + ["index.html"]

for path in files:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    orig = content

    # Subpage href (npr. ../b2b/)
    href = '../b2b/' if path != 'index.html' else 'b2b/'
    kontakt_href = '../kontakt/' if path != 'index.html' else 'kontakt/'

    # 1. Desktop nav: vstavi NOVO postavko pred Kontakt v <ul class="nav-links">
    #    Vzorec: samo <li> znotraj ul.nav-links — dodaj class="active" za
    #    trenutno stran posebej.
    nav_pattern = r'(<ul class="nav-links">.*?)(<li><a href="' + re.escape(kontakt_href) + r'">Kontakt</a></li>)(.*?</ul>)'
    nav_repl = r'\1<li><a href="' + href + r'">Za podjetja</a></li>\2\3'
    content = re.sub(nav_pattern, nav_repl, content, flags=re.DOTALL)

    # 2. Mobilni nav: <div id="mnav"> — preprosta zamenjava (tu ni footerja)
    mnav_pattern = r'(<div id="mnav">.*?)(<a href="' + re.escape(kontakt_href) + r'">Kontakt</a>)'
    mnav_repl = r'\1<a href="' + href + r'">Za podjetja</a>\2'
    content = re.sub(mnav_pattern, mnav_repl, content, flags=re.DOTALL)

    # 3. Footer Info stolpec — ločena zamenjava z .replace() (natančen niz)
    old_footer = '<li><a href="' + kontakt_href + '">Kontakt</a></li>'
    new_footer = '<li><a href="' + href + '">Za podjetja</a></li>' + old_footer
    content = content.replace(old_footer, new_footer)

    if content != orig:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"OK {path}")
```

**Preveri po zagonu** — poišči morebitne dvojnike:
```bash
grep -n "Za podjetja" */index.html index.html | grep -v "^Binary"
```

Vsaka datoteka mora imeti točno 3 pojavitve: nav-links, mnav, footer.

## E2E verifikacija

```bash
py -3 -m http.server 8765 --bind 127.0.0.1
# odpri vsako stran → nav mora imeti novo postavko med Dogodki in Kontakt
# mobilni pogled → hamburger menu mora vsebovati novo postavko
# footer → Info stolpec mora imeti nov link
```

## Gotchas

**`re.sub` zamenja vse** — Ne uporabljaj enostavnega `re.sub('<li><a href="kontakt/">Kontakt</a></li>', ...)` brez zakoreninjenja v nav blok. Ker je isti `<li>` niz v footerju, ga zamenja dvakrat. Simptom: footer prikaže podvojen link, drugi brez `</li>` ločnika.

**Repair pass** — Če se to zgodi, poišči napačni vzorec in ga popravi z `.replace()`:
```python
bad = '<li><a href="../b2b/">Za podjetja</a></li><li><a href="../b2b/">Za podjetja</a><a href="../kontakt/">Kontakt</a></li>'
good = '<li><a href="../b2b/">Za podjetja</a></li><li><a href="../kontakt/">Kontakt</a></li>'
content = content.replace(bad, good)
```

**Homepage ima drugačne href-e** — Subpages: `../b2b/`, `../kontakt/`. Homepage `index.html`: `b2b/`, `kontakt/`. Skripta mora ločiti ta dva primera.

**Footer Ponudba stolpec** ima drugačne href-e kot Info stolpec — na ponudba/index.html so to lokalni sidri (`#okusi`), ne `../ponudba/#okusi`. Zamenjava z `../ponudba/#xyz` ne bo delovala na tej strani.
