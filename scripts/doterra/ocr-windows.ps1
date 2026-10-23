# Texterkennung mit der in Windows eingebauten OCR (Windows.Media.Ocr), Sprache Deutsch.
#   powershell -ExecutionPolicy Bypass -File scripts/doterra/ocr-windows.ps1 <ordner-mit-png>
# Schreibt neben jedes Bild eine .txt mit dem erkannten Text. Bereits erkannte Bilder werden übersprungen.
param([Parameter(Mandatory = $true)][string]$Ordner, [string]$Filter = '*.png')   # Öl-App: '*.jpg' für Telegram-Bilder
Add-Type -AssemblyName System.Runtime.WindowsRuntime
$null = [Windows.Storage.StorageFile, Windows.Storage, ContentType = WindowsRuntime]
$null = [Windows.Media.Ocr.OcrEngine, Windows.Foundation, ContentType = WindowsRuntime]
$null = [Windows.Graphics.Imaging.BitmapDecoder, Windows.Foundation, ContentType = WindowsRuntime]
$asTask = ([System.WindowsRuntimeSystemExtensions].GetMethods() | Where-Object {
    $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 -and $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1' })[0]
function Warte($op, [Type]$typ) { $t = $asTask.MakeGenericMethod($typ).Invoke($null, @($op)); $t.Wait(-1) | Out-Null; $t.Result }

# Sprache des Windows-Profils (bei Patricia Deutsch) — liest Umlaute korrekt.
$engine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromUserProfileLanguages()
if (-not $engine) { Write-Error 'Keine OCR-Sprache installiert'; exit 1 }

Get-ChildItem -Path $Ordner -Filter $Filter -Recurse | ForEach-Object {
    $txt = [IO.Path]::ChangeExtension($_.FullName, '.txt')
    if (Test-Path $txt) { return }
    $file = Warte ([Windows.Storage.StorageFile]::GetFileFromPathAsync($_.FullName)) ([Windows.Storage.StorageFile])
    $stream = Warte ($file.OpenAsync([Windows.Storage.FileAccessMode]::Read)) ([Windows.Storage.Streams.IRandomAccessStream])
    $decoder = Warte ([Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($stream)) ([Windows.Graphics.Imaging.BitmapDecoder])
    $bitmap = Warte ($decoder.GetSoftwareBitmapAsync()) ([Windows.Graphics.Imaging.SoftwareBitmap])
    $ergebnis = Warte ($engine.RecognizeAsync($bitmap)) ([Windows.Media.Ocr.OcrResult])
    $zeilen = $ergebnis.Lines | ForEach-Object { $_.Text }
    [IO.File]::WriteAllText($txt, ($zeilen -join "`n"), [Text.Encoding]::UTF8)
    $stream.Dispose()
}
