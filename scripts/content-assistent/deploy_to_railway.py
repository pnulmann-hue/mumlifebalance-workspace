"""Railway-Deploy-Helper für Patricia.

Workflow:
    1. Railway-CLI installieren (einmalig): https://docs.railway.app/develop/cli
    2. railway login (einmalig)
    3. python deploy_to_railway.py

Was macht das Skript:
    - Erstellt ein neues Railway-Service falls noch nicht da
    - Linkt das aktuelle Verzeichnis
    - Setzt alle nötigen Environment-Variablen aus .env
    - Triggert Deploy

ALTERNATIV (manuell):
    1. https://railway.app → New Project → Empty Service
    2. Settings → Connect GitHub Repo (mumlifebalance-workspace)
    3. Service-Root: /scripts/content-assistent/
    4. Environment-Variablen aus .env in Railway-UI eintragen
    5. Deploy startet automatisch
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent  # workspace-root
ENV_FILE = ROOT / ".env"

REQUIRED_ENV_VARS = [
    "TELEGRAM_CONTENT_BOT_TOKEN",
    "TELEGRAM_CHAT_ID",
    "ANTHROPIC_API_KEY",
    "OPENAI_API_KEY",
    "NOTION_API_KEY",
    "PEXELS_API_KEY",
]


def check_railway_cli():
    if not shutil.which("railway"):
        print("❌ Railway-CLI nicht gefunden.")
        print("   Installation: https://docs.railway.app/develop/cli")
        print("   macOS:   brew install railway")
        print("   Windows: scoop install railway  (oder Winget)")
        print("   Linux:   curl -fsSL https://railway.app/install.sh | sh")
        sys.exit(1)
    print("✅ Railway-CLI gefunden.")


def parse_env() -> dict[str, str]:
    if not ENV_FILE.exists():
        print(f"❌ {ENV_FILE} fehlt.")
        sys.exit(1)
    env = {}
    for line in ENV_FILE.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip("'\"")
    missing = [k for k in REQUIRED_ENV_VARS if k not in env or not env[k]]
    if missing:
        print(f"❌ Fehlende Env-Vars in .env:")
        for m in missing:
            print(f"   - {m}")
        sys.exit(1)
    return {k: env[k] for k in REQUIRED_ENV_VARS}


def deploy(env: dict[str, str]):
    print("\n📤 Setze Environment-Variablen in Railway…")
    for k, v in env.items():
        subprocess.run(
            ["railway", "variables", "set", f"{k}={v}"],
            check=True,
            cwd=ROOT / "scripts" / "content-assistent",
        )
        print(f"   ✓ {k}")

    print("\n🚀 Deploy auf Railway…")
    subprocess.run(
        ["railway", "up", "--detach"],
        check=True,
        cwd=ROOT / "scripts" / "content-assistent",
    )
    print("\n✅ Deploy gestartet. Logs ansehen mit: railway logs")


if __name__ == "__main__":
    print("🔧 Patricia's Story-Render-Bot — Railway-Deploy\n")
    check_railway_cli()
    env = parse_env()
    print(f"\n📝 .env gefunden, alle {len(REQUIRED_ENV_VARS)} Vars OK.")

    confirm = input("\nWeiter mit Deploy? (y/N): ").lower().strip()
    if confirm != "y":
        print("Abgebrochen.")
        sys.exit(0)

    deploy(env)
