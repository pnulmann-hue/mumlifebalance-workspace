"""Listet alle offenen Aufgaben (nicht Abgeschlossen/Vorlage) zum Durchgehen."""
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

rows, cursor = [], None
while True:
    kw = {"database_id": DB, "page_size": 100}
    if cursor:
        kw["start_cursor"] = cursor
    resp = notion.databases.query(**kw)
    rows += resp["results"]
    if not resp.get("has_more"):
        break
    cursor = resp["next_cursor"]

today = date.today().isoformat()
out = []
counts = {}
for r in rows:
    p = r["properties"]
    st = (p.get("Status", {}).get("select") or {}).get("name")
    if st in ("Abgeschlossen", "Vorlage"):
        continue
    name = "".join(t.get("plain_text", "") for t in p.get("Aufgabe", {}).get("title", [])) or "(ohne Titel)"
    d = (p.get("Datum", {}).get("date") or {}).get("start") or ""
    prio = (p.get("Priorität", {}).get("select") or {}).get("name") or ""
    counts[st] = counts.get(st, 0) + 1
    overdue = bool(d) and d[:10] < today
    out.append((d or "9999", st or "(kein)", d[:10] if d else "—", prio, name, r["id"][:8], overdue))

out.sort(key=lambda x: x[0])
print(f"=== OFFENE AUFGABEN GESAMT: {len(out)} ===")
print("Nach Status: " + ", ".join(f"{k}={v}" for k, v in sorted(counts.items(), key=lambda kv: str(kv[0]))))
print(f"Heute: {today}\n")
for i, (_, st, d, prio, name, pid, od) in enumerate(out, 1):
    mark = " ⚠ÜBERFÄLLIG" if od else ""
    print(f"{i:2}. [{st:10}] {d:10} {prio:9} | {name}{mark}  #{pid}")
