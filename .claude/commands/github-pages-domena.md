# GitHub Pages: lastna domena, HTTPS in začasna stran »v pripravi«

Iz seje 12. 10. 2026 (romancakes.com → repo RomanEV-prog/romanvegancakes). Uporabi
ob selitvi katerekoli statične strani na lastno domeno ali ko mora domena kazati
»kmalu« stran, medtem ko se vsebina še dela. DNS pri Neoservu: `/neoserv-domenca-dns`.

## Arhitektura (stanje 12. 10. 2026)

- Pages vir = **veja `live`**, mapa `/`, domena romancakes.com, HTTPS vsiljen.
- `live` je **orphan veja** samo z začasno stranjo (index.html, CNAME, favicon, logo;
  `noindex`). `master` = prava stran, push nanjo ne objavi ničesar.
- Objava prave strani (šele ko Roman potrdi, da je vsebina urejena):
  `git push origin master:live --force` (orphan → force nujen). Nato
  `gh api -X POST repos/RomanEV-prog/romanvegancakes/pages/builds` in preveri
  `curl -s https://romancakes.com/ | grep -o "<title>[^<]*"`.
- Povezave v strani ostanejo relativne, da deluje tudi pod podpotjo `/romanvegancakes/`.

## Recepti

### Vrstni red selitve (deluje, brez izpada)
1. DNS: apex `A` → 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153;
   `www` → `CNAME romanev-prog.github.io.` (TTL 300). Preveri na obeh NS.
2. Šele nato `CNAME` datoteka v repo (`printf 'romancakes.com\n' > CNAME`), commit, push.
   GitHub jo prebere sam → `gh api repos/<r>/pages --jq '{cname,status}'` pokaže cname.
3. Certifikat: GitHub ga izda sam (Let's Encrypt), tokrat v < 1 min. Preveri:
   `echo | openssl s_client -connect romancakes.com:443 -servername romancakes.com | openssl x509 -noout -issuer -dates`
4. `gh api -X PUT repos/<r>/pages -F https_enforced=true` → http:// in www
   preusmerita na https://romancakes.com/. Stari github.io naslov preusmerja sam.

### Zamenjava vira na drugo vejo
```
gh api -X PUT repos/<r>/pages --input - <<'EOF'
{"source":{"branch":"live","path":"/"}}
EOF
gh api -X POST repos/<r>/pages/builds      # brez tega ostane stara gradnja!
gh api repos/<r>/pages/builds/latest --jq '{status,commit}'
```

### Orphan veja brez poškodbe delovnega drevesa
`git checkout --orphan` v glavnem drevesu pusti vse datoteke kot untracked in
`git clean` jih požre. Uporabi **worktree**:
```
git worktree add --detach <scratch>/live master
cd <scratch>/live && git checkout --orphan live && git rm -rfq --cached . && git clean -fdxq
git show master:CNAME > CNAME   # ipd. za favicon, logo
```
Če si že zašel v glavnem drevesu: `git symbolic-ref HEAD refs/heads/master && git reset -q`.

## E2E verifikacija
```
curl -s -o /dev/null -w "%{http_code} -> %{redirect_url}\n" http://romancakes.com/     # 301 → https
curl -s -o /dev/null -w "%{http_code} -> %{redirect_url}\n" https://www.romancakes.com/ # 301 → apex
curl -s "https://romancakes.com/?$(date +%s)" | grep -o "<title>[^<]*"                   # pravi naslov
gh api repos/<r>/pages/health --jq '.domain'                                             # lahko je null tik po preklopu
```

## Gotchas
- `-F https_enforced=true` takoj po nastavitvi domene vrne 404 »certificate has not yet
  been issued« — cname se vseeno shrani; ponovi čez minuto.
- `PUT …/pages` z `-f 'source[branch]=live'` ne deluje (gh ga pošlje kot niz) → `--input` JSON.
- Sprememba vira **ne sproži gradnje**; `builds/latest` še kaže stari commit → POST builds.
- Curl brez cache-busterja lahko še vrača staro stran; dodaj `?$(date +%s)`.
- `sleep 60; …` v Bash orodju je blokiran → `until … ; do sleep 5; done` ali run_in_background.
- Pages s `CNAME` datoteko: podpot izgine, a relativne povezave delujejo naprej; absolutnih `/…` ne uvajaj.
