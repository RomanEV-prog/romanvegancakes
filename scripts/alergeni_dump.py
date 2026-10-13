# -*- coding: utf-8 -*-
"""Potegne aktivne torte in njihove deklaracije iz ERP API-ja v scripts/alergeni-dump.json.

Uporaba:
  py -3 -I scripts/alergeni_dump.py http://127.0.0.1:3031            # lokalni ERP (brez PIN-a)
  py -3 -I scripts/alergeni_dump.py https://romanscakes.tail3c9ebd.ts.net --token <x-auth-token>

Vir resnice je GET /api/deklaracije/preview?receptura_id= (isti izračun kot tiskana deklaracija):
sestavine_text, alergeni_text, alergeni_kode, alergeni_nepotrjeni, sestava_nepopolna, opozorila.
Nato: py -3 -I scripts/alergeni_gen.py
"""
import json, sys, urllib.request, os, datetime

base = sys.argv[1].rstrip('/')
token = None
if '--token' in sys.argv:
    token = sys.argv[sys.argv.index('--token') + 1]

def get(path):
    req = urllib.request.Request(base + path)
    if token:
        req.add_header('x-auth-token', token)
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode('utf-8'))

def norm(s):
    return ' '.join(str(s or '').lower().replace('–', '-').split())

artikli = [a for a in get('/api/artikli') if a.get('tip') == 'torta' and a.get('aktiven')]
recepture = [r for r in get('/api/recepture') if r.get('aktivna') and r.get('tip') == 'torta']
by_art = {r['artikel_id']: r for r in recepture if r.get('artikel_id')}
by_name = {norm(r['ime']): r for r in recepture}

out = {'vir': base, 'datum': datetime.date.today().isoformat(), 'torte': []}
for a in sorted(artikli, key=lambda x: norm(x['ime'])):
    rec = by_art.get(a['id']) or by_name.get(norm(a['ime']))
    t = {'artikel_id': a['id'], 'ime': a['ime'], 'brezglutensko': 1 if a.get('brezglutensko') else 0,
         'cena_kos': a.get('cena_kos'), 'receptura_id': rec['id'] if rec else None, 'receptura_ime': rec['ime'] if rec else None,
         'artikel_alergeni': a.get('alergeni'), 'artikel_alergeni_potrjeno': a.get('alergeni_potrjeno')}
    if rec:
        d = get('/api/deklaracije/preview?receptura_id=%d' % rec['id'])
        t.update({k: d.get(k) for k in ('sestavine_text', 'alergeni_text', 'alergeni_kode', 'alergeni_nepotrjeni',
                                        'sestava_nepopolna', 'opozorila', 'bg_opozorilo')})
        t['sestavine'] = [{'ime': s.get('ime'), 'alergeni': s.get('alergeni') or []} for s in d.get('sestavine') or []]
    out['torte'].append(t)

dst = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'alergeni-dump.json')
with open(dst, 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print('zapisano', dst, '-', len(out['torte']), 'tort')
