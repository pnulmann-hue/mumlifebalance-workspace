# Sicherung der ausgeschlossenen Dateien (alles, was .gitignore von GitHub fernhaelt)
# als verschluesseltes 7-Zip-Archiv in OneDrive.
#
#   powershell -ExecutionPolicy Bypass -File scripts\sicherung\sichern.ps1            # Kern (woechentlich)
#   powershell -ExecutionPolicy Bypass -File scripts\sicherung\sichern.ps1 -Medien    # Videos, Audio, grosse Dateien (monatlich)
#   powershell -ExecutionPolicy Bypass -File scripts\sicherung\sichern.ps1 -Probe     # nur zaehlen, nichts schreiben
#
# Das Passwort steht in scripts\sicherung\.env  (SICHERUNG_PASSWORT=...),
# die Datei ist ueber **/.env ausgeschlossen. Ohne Passwort bricht das Skript ab.
# Was auf GitHub liegt, sichert /shutdown — dieses Skript nimmt nur den Rest.

param([switch]$Medien, [switch]$Probe)

$ErrorActionPreference = 'Stop'
$Root   = (Resolve-Path "$PSScriptRoot\..\..").Path
$Ziel   = Join-Path $env:OneDrive 'Workspace-Sicherung'
$Art    = if ($Medien) { 'medien' } else { 'kern' }
$Behalten = if ($Medien) { 1 } else { 4 }   # Medien ~60 GB: nur ein Stand
$GrenzeMB = 50

# Nie sichern: temporaere Arbeitskopien, Bibliotheken, Zwischenstaende
$Nie = @(
  '^\.claude/worktrees/', '(^|/)node_modules/', '(^|/)__pycache__/', '\.pyc$',
  '(^|/)\.git/', '^scripts/hyperframes-test/.*/renders/', '\.DS_Store$', '\.tmp$'
)
# Medien-Endungen gehen in den Medien-Teil — auch Fotos: die Shootingbilder allein sind
# 7 GB und aendern sich selten, woechentlich mitgeschleppt waeren sie der halbe Kern
$MedienEndung = '\.(mp4|mov|m4v|avi|mkv|webm|mp3|m4a|wav|aac|ogg|flac|jpg|jpeg|png|heic|webp|gif|tif|tiff)$'

# 7-Zip finden
$SiebenZ = @("$env:ProgramFiles\7-Zip\7z.exe", "${env:ProgramFiles(x86)}\7-Zip\7z.exe", "$env:LOCALAPPDATA\Programs\7-Zip\7z.exe") |
  Where-Object { $_ -and (Test-Path $_) } | Select-Object -First 1
if (-not $SiebenZ -and -not $Probe) { throw "7-Zip fehlt. Installieren: winget install --id 7zip.7zip --exact --source winget" }

# Passwort lesen
$EnvDatei = Join-Path $PSScriptRoot '.env'
$Passwort = $null
if (Test-Path $EnvDatei) {
  foreach ($z in Get-Content $EnvDatei -Encoding UTF8) {
    if ($z -match '^\s*SICHERUNG_PASSWORT\s*=\s*(.+?)\s*$') { $Passwort = $Matches[1].Trim('"') }
  }
}
if ((-not $Passwort -or $Passwort -like 'HIER-*') -and -not $Probe) { throw "Kein Passwort. In scripts\sicherung\.env die Zeile SICHERUNG_PASSWORT=... mit deinem eigenen Passwort fuellen." }

# Ausgeschlossene Dateien einsammeln (git kennt die Liste genau)
Push-Location $Root
try {
  $alle = git -c core.quotepath=false ls-files --others --ignored --exclude-standard
} finally { Pop-Location }

$liste = New-Object System.Collections.Generic.List[string]
$summe = 0L
foreach ($rel in $alle) {
  if (-not $rel) { continue }
  $nie = $false
  foreach ($m in $Nie) { if ($rel -match $m) { $nie = $true; break } }
  if ($nie) { continue }
  $voll = Join-Path $Root $rel
  if (-not (Test-Path -LiteralPath $voll -PathType Leaf)) { continue }
  $groesse = (Get-Item -LiteralPath $voll -Force).Length
  $istMedium = ($rel -match $MedienEndung) -or ($groesse -gt $GrenzeMB * 1MB)
  if ($Medien -ne $istMedium) { continue }
  $liste.Add($rel)
  $summe += $groesse
}

"{0}: {1} Dateien, {2:N0} MB unkomprimiert" -f $Art, $liste.Count, ($summe / 1MB)
if ($Probe) { return }
if ($liste.Count -eq 0) { "Nichts zu sichern."; return }

New-Item -ItemType Directory -Force -Path $Ziel | Out-Null
$stempel = Get-Date -Format 'yyyy-MM-dd'
$archiv  = Join-Path $Ziel "$Art-$stempel.7z"
$listDatei = Join-Path $env:TEMP "sicherung-$Art.txt"
[System.IO.File]::WriteAllLines($listDatei, $liste, (New-Object System.Text.UTF8Encoding $false))

# Erst in TEMP bauen, dann verschieben — OneDrive soll keine halben Dateien hochladen
$tmpArchiv = Join-Path $env:TEMP "$Art-$stempel.7z"
if (Test-Path $tmpArchiv) { Remove-Item $tmpArchiv -Force }
Push-Location $Root
try {
  & $SiebenZ a -t7z -mx=3 -mhe=on "-p$Passwort" -scsUTF-8 "$tmpArchiv" "@$listDatei" | Out-Null
  if ($LASTEXITCODE -gt 1) { throw "7-Zip meldet Fehler $LASTEXITCODE" }
  & $SiebenZ t "-p$Passwort" "$tmpArchiv" | Out-Null
  if ($LASTEXITCODE -ne 0) { throw "Probe des Archivs fehlgeschlagen ($LASTEXITCODE)" }
} finally { Pop-Location; Remove-Item $listDatei -ErrorAction SilentlyContinue }

Move-Item $tmpArchiv $archiv -Force
# OneDrive: nach dem Hochladen nur online behalten, sonst belegt das Archiv die Festplatte doppelt
attrib +U -P "$archiv" 2>$null

# Alte Staende aufraeumen — nur eigene Archive dieser Art
Get-ChildItem $Ziel -Filter "$Art-*.7z" | Sort-Object Name -Descending | Select-Object -Skip $Behalten | Remove-Item -Force

$mb = [math]::Round((Get-Item $archiv).Length / 1MB)
$zeile = "{0}  {1}  {2} Dateien  {3} MB  geprueft" -f (Get-Date -Format 'yyyy-MM-dd HH:mm'), $Art, $liste.Count, $mb
Add-Content -Path (Join-Path $Ziel 'protokoll.txt') -Value $zeile -Encoding UTF8
$zeile
