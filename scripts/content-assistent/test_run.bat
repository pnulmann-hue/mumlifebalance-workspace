@echo off
REM Story-Render-Bot — Einmaliger Test-Lauf (kein Dauerbetrieb)
REM Generiert SOFORT eine Story und postet sie in Telegram, dann Ende.

cd /d "%~dp0"
echo ============================================================
echo   Story-Render-Bot — Einmal-Test
echo   Generiert eine Story und sendet sie an Telegram.
echo ============================================================
echo.

python task_daily_story.py %1

echo.
pause
