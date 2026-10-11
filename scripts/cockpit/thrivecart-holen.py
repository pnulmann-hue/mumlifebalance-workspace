"""
Holt Produkte, Order Bumps, Upsells und Downsells aus ThriveCart.

Damit steht endlich schwarz auf weiss im Cockpit, was an einem Checkout
haengt — bisher stand das nur verstreut in Funnel-Dokumenten, und die
Bump-Spalte im Cockpit war leer.

Zugang: `04-projects/thrivecart/.env` mit `TC_API_KEY=…`
  (ThriveCart → Einstellungen → API & Webhooks → API tokens)

Belegt aus dem offiziellen SDK (github.com/thrivecart/php-api, src/Api.php):
  Basis   https://thrivecart.com/api/external
  Header  Authorization: Bearer <token>
  Wege    /products · /bumps · /upsells · /downsells
          /<art>/<id>/pricing_options fuer die Preise
Das Limit liegt bei 60 Anfragen pro Minute.

Aufruf:
  python scripts/cockpit/thrivecart-holen.py [zielordner] [--preise]
"""
import json
import sys
import time
from datetime import date
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[2]
BASIS = "https://thrivecart.com/api/external"


def schluessel():
    p = ROOT / "04-projects" / "thrivecart" / ".env"
    if not p.exists():
        return ""
    for zeile in p.read_text(encoding="utf-8-sig").splitlines():
        if zeile.lstrip().startswith("#") or "=" not in zeile:
            continue
        k, v = zeile.split("=", 1)
        if k.strip() == "TC_API_KEY":
            return v.strip().strip('"').strip("'")
    return ""


def ruf(pfad, key, versuche=3):
    """Eine Anfrage, mit Geduld bei Drosselung."""
    for n in range(versuche):
        try:
            r = Request(BASIS + pfad,
                        headers={"Authorization": "Bearer " + key,
                                 "Accept": "application/json"})
            with urlopen(r, timeout=40) as a:
                return json.loads(a.read().decode("utf-8"))
        except HTTPError as e:
            if e.code == 429 and n < versuche - 1:
                time.sleep(12)
                continue
            print("  %s → HTTP %s" % (pfad, e.code))
            return None
        except (URLError, TimeoutError, OSError, ValueError) as e:
            print("  %s → %s" % (pfad, e))
            return None
    return None


def preis_von(eintrag):
    """Aus den Preisoptionen die eine Zahl ziehen, die im Cockpit stehen soll."""
    for feld in ("amount", "price", "base_price"):
        wert = eintrag.get(feld)
        if wert not in (None, "", 0, "0"):
            try:
                return round(float(wert) / 100.0, 2) if float(wert) > 1000 \
                    else round(float(wert), 2)
            except (TypeError, ValueError):
                pass
    return None


def liste(art, key, mit_preisen):
    """Eine Gattung holen und aufbereiten."""
    roh = ruf("/" + art, key)
    if not isinstance(roh, list):
        return []
    raus = []
    for x in roh:
        nummer = str(x.get(art[:-1] + "_id") or x.get("id") or "")
        eintrag = {
            "id": nummer,
            "name": x.get("name", ""),
            "art": art,
            "status": x.get("statusString") or x.get("status", ""),
            "typ": x.get("typeString") or "",
            "url": x.get("url", ""),
            "preise": [],
        }
        if mit_preisen and nummer:
            opts = ruf("/%s/%s/pricing_options" % (art, nummer), key)
            for o in (opts or []):
                eintrag["preise"].append({
                    "name": o.get("name", ""),
                    "betrag": preis_von(o),
                    "waehrung": (o.get("currency") or "").upper(),
                })
            time.sleep(1.1)          # 60 Anfragen pro Minute
        raus.append(eintrag)
    return raus


def verknuepfen(alles, key):
    """Jedem Produkt anhaengen, was an seinem Checkout haengt.

    Die Verbindung steht nicht in der Uebersicht, sondern erst im Detail:
    dort nennt das Produkt seine `upsell_ids` und `downsell_ids`. Bumps
    tragen stattdessen die Checkout-Adresse, ueber die sie zugeordnet werden.
    """
    upsells = {u["id"]: u["name"] for u in alles["upsells"]}
    downsells = {d["id"]: d["name"] for d in alles["downsells"]}

    for pr in alles["products"]:
        detail = ruf("/products/%s" % pr["id"], key) or {}
        time.sleep(1.1)
        pr["slug"] = detail.get("slug", "")
        pr["waehrung"] = (detail.get("payment_currency") or "").upper()
        pr["upsells"] = [upsells.get(str(i), "Upsell " + str(i))
                         for i in (detail.get("upsell_ids") or [])]
        pr["downsells"] = [downsells.get(str(i), "Downsell " + str(i))
                           for i in (detail.get("downsell_ids") or [])]
        pr["bumps"] = [b["name"] for b in alles["bumps"]
                       if pr["url"] and b.get("url") and
                       b["url"].rstrip("/") == pr["url"].rstrip("/")]
    return alles


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    ziel = Path(args[0]) if args else ROOT / "outputs" / "cockpit" / "abgleich"
    ziel.mkdir(parents=True, exist_ok=True)
    mit_preisen = "--preise" in sys.argv

    key = schluessel()
    if not key:
        sys.exit("Kein TC_API_KEY in 04-projects/thrivecart/.env")

    konto = ruf("/ping", key)
    if not konto:
        sys.exit("ThriveCart antwortet nicht — stimmt der Schluessel noch?")

    alles = {"konto": konto.get("account_name", ""),
             "stand": date.today().isoformat()}
    for art in ("products", "bumps", "upsells", "downsells"):
        alles[art] = liste(art, key, mit_preisen)
        print("  %-10s %3d" % (art, len(alles[art])))

    print("\n  Verbindungen holen (ein Aufruf je Produkt) …")
    verknuepfen(alles, key)
    mit = len([p for p in alles["products"]
               if p["bumps"] or p["upsells"] or p["downsells"]])
    print("  %d von %d Produkten haben Bump, Upsell oder Downsell"
          % (mit, len(alles["products"])))

    (ziel / "thrivecart.json").write_text(
        json.dumps(alles, ensure_ascii=False, indent=2), encoding="utf-8")
    print("\nAbgelegt in: %s" % (ziel / "thrivecart.json"))


if __name__ == "__main__":
    main()
