@echo off
REM Startet den Agent Lab Telegram-Bot. Wird vom Autostart (start-bot.vbs) unsichtbar aufgerufen.
cd /d "%~dp0"
"C:\Users\pnulm\AppData\Local\Programs\Python\Python312\python.exe" bot.py >> "%~dp0bot-autostart.log" 2>&1
