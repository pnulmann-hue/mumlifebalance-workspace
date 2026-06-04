"""Schliesst ueberfaellige Alt-Aufgaben (Status -> Abgeschlossen). Schutz-Liste bleibt erhalten.
Dry-run by default. Mit Argument 'execute' werden die Aenderungen geschrieben."""
import os, sys
from pathlib import Path
from datetime import date
from dotenv import load_dotenv
from notion_client import Client

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parent.parent.parent
load_dotenv(ROOT / ".env", override=True)
notion = Client(auth=os.getenv("NOTION_API_KEY"))
DB = "2ae7078e-8b7e-81bd-b07a-deaa99c01b71"
EXECUTE = len(sys.argv) > 1 and sys.argv[1] == "execute"

# Diese bleiben IMMER offen (Schutz-Liste, Titel-Teilstrings)
KEEP = [
    "live-call #1 kick-off",
    "premium-bundle",
    "story-service bauen",
    "doterra: intensivere begleitung",
    "active campaig", "integrationseinstellungen für liste",
    "digitale produktwelt module 3+4+5",
]

rows, cursor = [], None
while True:
    kw = {"database_id": DB, "page_size": 100}
    if cursor: kw["start_cursor"] = cursor
    resp = notion.databases.query(**kw)
    rows += resp["results"]
    if not resp.get("has_more"): break
    cursor = resp["next_cursor"]

today = date.today().isoformat()
close_list, keep_list = [], []
for r in rows:
    p = r["properties"]
    st = (p.get("Status", {}).get("select") or {}).get("name")
    if st in ("Abgeschlossen", "Vorlage"):
        continue
    name = "".join(t.get("plain_text", "") for t in p.get("Aufgabe", {}).get("title", [])) or "(ohne Titel)"
    d = (p.get("Datum", {}).get("date") or {}).get("start") or ""
    overdue = bool(d) and d[:10] < today
    protected = any(k in name.lower() for k in KEEP)
    if overdue and not protected:
        close_list.append((r["id"], d[:10], st or "(kein)", name))
    else:
        reason = "geschützt" if protected else ("zukünftig" if d and d[:10] >= today else "ohne Datum/heute")
        keep_list.append((d[:10] if d else "—", st or "(kein)", name, reason))

print(f"=== SCHLIESSEN: {len(close_list)} | BEHALTEN: {len(keep_list)} ===  (today={today})\n")
print("--- BLEIBEN OFFEN (Schutz/zukünftig) ---")
for d, st, name, reason in sorted(keep_list):
    print(f"  [{st:10}] {d:10} | {name}  ({reason})")

if EXECUTE:
    print(f"\n--- SCHLIESSE {len(close_list)} Aufgaben ... ---")
    ok = 0
    for pid, d, st, name in close_list:
        try:
            notion.pages.update(page_id=pid, properties={"Status": {"select": {"name": "Abgeschlossen"}}})
            ok += 1
        except Exception as e:
            print(f"  FEHLER bei '{name}': {e}")
    print(f"✓ {ok}/{len(close_list)} auf Abgeschlossen gesetzt.")
else:
    print(f"\n(DRY-RUN — nichts geaendert. Mit 'execute' ausfuehren.)")
