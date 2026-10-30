# -*- coding: utf-8 -*-
"""Posodobi ponudba/index.html iz scripts/alergeni-dump.json.

Zahteva obstoječ dump (potegni ga najprej z alergeni_dump.py).
Patchira tri SYNC bloke med <!-- SYNC:x --> in <!-- /SYNC:x --> markerji:
  - cenik-tbody      : vrstice cenik tabele (regularne torte, grupirane po ceni)
  - kalkulator-opts  : calc-opt divs za hitri izračun
  - okusi-grid       : ok-group divs z alergeni in cenami

Uporaba:
  py -3 -I scripts/sync.py
  py -3 -I scripts/sync.py --no-alergeni   (preskoči regeneracijo alergeni/)
"""
import json, os, re, html as ht, sys, subprocess

sys.stdout.reconfigure(encoding='utf-8')

ROOT    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, 'scripts')

dump_path = os.path.join(SCRIPTS, 'alergeni-dump.json')
if not os.path.exists(dump_path):
    sys.exit('NAPAKA: scripts/alergeni-dump.json ne obstaja — najprej poženi alergeni_dump.py')

dump = json.load(open(dump_path, encoding='utf-8'))
cfg_path = os.path.join(SCRIPTS, 'sync_config.json')
cfg = json.load(open(cfg_path, encoding='utf-8')) if os.path.exists(cfg_path) else {}

IZKLJUCI      = set(cfg.get('izkljuci', []))
KREMNE        = set(cfg.get('kremne', []))
IME_POPRAVKI  = cfg.get('ime_popravki', {})
CENA_OVERRIDE = cfg.get('cena_override', {})
KATEGORIJA    = cfg.get('kategorija', {})
KAT_OPIS      = cfg.get('kat_opis', {})
KALK_IME      = cfg.get('kalkulator_ime', {})
CENIK_OPIS    = cfg.get('cenik_opis', {})

IME_AL = {
    'gluten':   'gluten',       'soja':      'soja',
    'mandlji':  'mandlji',      'lesniki':   'lešniki',
    'orehi':    'orehi',        'arasidi':   'arašidi',
    'pistacija':'pistacija',    'oreski':    'oreški',
    'indijski': 'indijski oreščki', 'sezam': 'sezam',
    'gorcica':  'gorčica',      'sulfiti':   'sulfiti',
}
AL_VR = list(IME_AL.keys())

CAT_ORDER = ['Čokoladni okusi', 'Sadni in kremni okusi', 'Torte brez glutenskih sestavin']


def fmt_kos(c):
    """4.9 → '4,90 €'  (vedno 2 decimali, za cena na kos)"""
    return f"{c:.2f} €".replace('.', ',')


def fmt_tot(c):
    """49.0 → '49 €', 39.2 → '39,20 €'  (brez ,00)"""
    s = f"{c:.2f}".replace('.', ',')
    if s.endswith(',00'):
        s = s[:-3]
    return s + ' €'


def torte():
    """Vrne vse aktivne torte iz dumpa, popravljene in filtrirane."""
    out = []
    for t in dump['torte']:
        if t['ime'] in IZKLJUCI:
            continue
        ime = IME_POPRAVKI.get(t['ime'], t['ime'])
        cena = CENA_OVERRIDE.get(t['ime'], t.get('cena_kos') or 0)
        kode = sorted(set(t.get('alergeni_kode') or []),
                      key=lambda k: AL_VR.index(k) if k in AL_VR else 99)
        out.append({
            'ime_erp': t['ime'],
            'ime':     ime,
            'cena':    float(cena),
            'bg':      bool(t.get('brezglutensko')),
            'kremna':  t['ime'] in KREMNE,
            'kode':    kode,
        })
    return out


# ── cenik-tbody ───────────────────────────────────────────────────────────────

def gen_cenik_tbody(tt):
    regular = [t for t in tt if not t['bg'] and not t['kremna'] and t['cena'] > 0]
    by_price: dict = {}
    for t in regular:
        by_price.setdefault(t['cena'], []).append(t['ime'])

    rows = []
    for cena in sorted(by_price):
        names = sorted(by_price[cena])
        key   = f"{cena:.1f}"
        opis  = CENIK_OPIS.get(key, '')
        small = f'<small>{ht.escape(opis)}</small>' if opis else ''
        rows.append(
            f'          <tr><td>{ht.escape(", ".join(names))}{small}</td>'
            f'<td class="p">{fmt_kos(cena)}</td>'
            f'<td class="p">{fmt_tot(cena * 8)}</td>'
            f'<td class="p">{fmt_tot(cena * 10)}</td>'
            f'<td class="p">{fmt_tot(cena * 12)}</td></tr>'
        )
    return '\n'.join(rows)


# ── kalkulator-opts ───────────────────────────────────────────────────────────

def gen_kalk_opts(tt):
    non_kremne = [t for t in tt if not t['kremna'] and t['cena'] > 0]
    by_price: dict = {}
    for t in non_kremne:
        by_price.setdefault(t['cena'], []).append(t)

    divs = []
    first = True
    for cena in sorted(by_price):
        grp   = sorted(by_price[cena], key=lambda x: x['ime'])
        names = ' · '.join(KALK_IME.get(t['ime'], t['ime']) for t in grp)
        sel   = ' sel' if first else ''
        first = False
        dp    = f"{cena:.1f}"
        divs.append(
            f'          <div class="calc-opt{sel}" data-price="{dp}">'
            f'{ht.escape(names)} <small style="opacity:.65;font-size:.85em">{fmt_kos(cena)}</small></div>'
        )

    kremne = [t for t in tt if t['kremna'] and t['cena'] > 0]
    if kremne:
        krem_names = ' · '.join(KALK_IME.get(t['ime'], t['ime']) for t in kremne)
        krem_cena  = kremne[0]['cena']
        dp = f"{krem_cena:.1f}"
        divs.append(
            f'          <div class="calc-opt" data-price="{dp}">'
            f'{ht.escape(krem_names)} (kremna) <small style="opacity:.65;font-size:.85em">{fmt_kos(krem_cena)}</small></div>'
        )
    return '\n'.join(divs)


# ── okusi-grid ────────────────────────────────────────────────────────────────

def gen_okusi_grid(tt):
    cats: dict = {}
    for t in tt:
        if t['kremna']:
            continue
        if t['bg']:
            cat = 'Torte brez glutenskih sestavin'
        else:
            cat = KATEGORIJA.get(t['ime'], 'Ostalo')
        cats.setdefault(cat, []).append(t)

    order = CAT_ORDER + [c for c in cats if c not in CAT_ORDER]
    groups = []
    for i, cat in enumerate(order):
        if cat not in cats:
            continue
        products = sorted(cats[cat], key=lambda x: (x['cena'], x['ime']))
        n = len(products)
        opis = ht.escape(KAT_OPIS.get(cat, ''))
        d_attr = f' data-d="{i * 80}"' if i > 0 else ''

        items = []
        for t in products:
            tags = ''
            if t['bg']:
                tags += '<span class="tag tag-g">brez glutenskih sestavin</span>'
            tags += ''.join(
                f'<span class="tag tag-a">{ht.escape(IME_AL.get(k, k))}</span>'
                for k in t['kode']
            )
            c_fmt = fmt_kos(t['cena']) + ' / kos' if t['cena'] > 0 else 'po dogovoru'
            items.append(
                f'          <li><span class="name">{ht.escape(t["ime"])}</span>'
                f'<span class="al">{tags}<span class="pr">{c_fmt}</span></span></li>'
            )

        groups.append(
            f'      <div class="ok-group rv"{d_attr}>\n'
            f'        <div class="ok-head"><h3>{ht.escape(cat)}</h3><span>{n} okusov</span></div>\n'
            f'        <p class="ok-sub">{opis}</p>\n'
            f'        <ul class="ok-list">\n'
            + '\n'.join(items) + '\n'
            + '        </ul>\n'
            + '      </div>'
        )
    return '\n\n'.join(groups)


# ── patch ─────────────────────────────────────────────────────────────────────

def patch(filepath, key, content):
    with open(filepath, encoding='utf-8') as f:
        text = f.read()
    sm = f'<!-- SYNC:{key} -->'
    em = f'<!-- /SYNC:{key} -->'
    si, ei = text.find(sm), text.find(em)
    if si == -1 or ei == -1:
        print(f'  POZOR: marker SYNC:{key} ni najden v {filepath}')
        return False
    with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text[:si + len(sm)] + '\n' + content + '\n' + text[ei:])
    return True


# ── main ──────────────────────────────────────────────────────────────────────

tt = torte()
print(f'Dump: {dump.get("datum","?")} · {len(tt)} tort po filtriranju')

ponudba = os.path.join(ROOT, 'ponudba', 'index.html')
ok = True
ok &= patch(ponudba, 'cenik-tbody',      gen_cenik_tbody(tt))
ok &= patch(ponudba, 'kalkulator-opts',  gen_kalk_opts(tt))
ok &= patch(ponudba, 'okusi-grid',       gen_okusi_grid(tt))

if not ok:
    print('NAPAKA: nekateri SYNC markerji niso bili najdeni — preveri ponudba/index.html')
    sys.exit(1)

print('ponudba/index.html ✓')

if '--no-alergeni' not in sys.argv:
    gen = os.path.join(SCRIPTS, 'alergeni_gen.py')
    r = subprocess.run(['py', '-3', '-I', gen], cwd=ROOT)
    if r.returncode != 0:
        sys.exit(1)
