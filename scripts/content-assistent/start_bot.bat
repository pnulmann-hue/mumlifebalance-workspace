@echo off
REM Patricia's Story-Render-Bot — Lokaler Start
REM Doppelklick startet den Bot. Konsole offen lassen, sonst stoppt er.

cd /d "%~dp0"
echo ============================================================
echo   Story-Render-Bot startet ...
echo   Konsole NICHT schliessen — sonst stoppt der Bot.
echo   Strg+C zum Beenden.
echo ============================================================
echo.

python bot.py

echo.
echo Bot beendet. Druecke eine Taste zum Schliessen.
pause >nul
