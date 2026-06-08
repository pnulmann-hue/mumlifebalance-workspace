"""Standalone-Test des Morgen-Briefings — simuliert was Railway um 06:30 macht."""

import asyncio
import sys
from pathlib import Path

if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

# .env aus Workspace-Root
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parent.parent.parent / ".env", override=True)

import config  # noqa: E402
from telegram.ext import Application  # noqa: E402

app = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()


async def main():
    from bot import task_morgen_briefing
    print(f"Token: ...{config.TELEGRAM_BOT_TOKEN[-8:]}")
    print(f"Chat-ID: {config.TELEGRAM_CHAT_ID}")
    print("=== TEST: Morgen-Briefing ===")
    await task_morgen_briefing()
    print("Briefing: OK gesendet (oder still beendet)")


if __name__ == "__main__":
    asyncio.run(main())
