# sync.ps1 — posodobi spletno stran iz ERP podatkov
# Poženi iz korena projekta: .\scripts\sync.ps1
# Za osvezitev zive baze dodaj: .\scripts\sync.ps1 --api http://100.77.108.53:3000

param(
    [string]$api = "",
    [switch]$noAlergeni
)

$root = Split-Path $PSScriptRoot -Parent
Set-Location $root
$env:PYTHONIOENCODING = "utf-8"

# 1. Osvezi dump iz ERP (ce je podan --api)
if ($api) {
    Write-Host "Osvezujem dump iz ERP: $api ..." -ForegroundColor Cyan
    py -3 -I scripts/alergeni_dump.py $api
    if ($LASTEXITCODE -ne 0) { Write-Host "NAPAKA pri alergeni_dump.py" -ForegroundColor Red; exit 1 }
} else {
    $dumpDate = (Get-Content scripts/alergeni-dump.json -Raw | ConvertFrom-Json).datum
    Write-Host "Dump: $dumpDate (lokalni) — za sveze podatke dodaj: -api http://100.77.108.53:3000" -ForegroundColor Yellow
}

# 2. Posodobi HTML datoteke
$extraArgs = if ($noAlergeni) { "--no-alergeni" } else { "" }
py -3 -I scripts/sync.py $extraArgs
if ($LASTEXITCODE -ne 0) { Write-Host "NAPAKA pri sync.py" -ForegroundColor Red; exit 1 }

# 3. Pokazi spremembe
Write-Host ""
Write-Host "Spremembe:" -ForegroundColor Cyan
git diff --stat HEAD

Write-Host ""
Write-Host "Naslednji koraki:" -ForegroundColor Green
Write-Host "  1. Preveri v brskalniku: py -3 -m http.server 8765 --bind 127.0.0.1"
Write-Host "  2. git add ponudba/index.html alergeni/index.html scripts/alergeni-dump.json"
Write-Host "  3. git commit -m `"sync: posodobi iz ERP $(Get-Date -f yyyy-MM-dd)`""
Write-Host "  4. git push origin master:live --force"
