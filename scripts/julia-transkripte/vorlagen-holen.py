"""Julias Kursvorlagen (Google Docs/Sheets/Drive) in den Julia-Ordner holen.

    python scripts/julia-transkripte/vorlagen-holen.py

Die Links stehen als Knöpfe in den Lektionen und sind öffentlich freigegeben; gelesen am
27.10.2026 aus Patricias Zugang (siehe reference/julia-trost/downloads-abgleich-2026-10-27.md).
Docs kommen als .txt, Sheets als .xlsx, Drive-Dateien im Original. Bestehende Dateien bleiben.
Ablage: reference/julia-trost/Vorlagen/<Kurs>/ — gitignored (gekauftes Fremdmaterial).
"""
import importlib.util, os, re, sys, urllib.request

HIER = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("holen", os.path.join(HIER, "holen.py"))
holen = importlib.util.module_from_spec(spec)
spec.loader.exec_module(holen)
ZIEL = os.path.join(holen.WURZEL, "reference", "julia-trost", "Vorlagen")

# kurs, art (d=Doc, s=Sheet, f=Drive-Datei), id, Name
LISTE = """
60337|d|1viMFtJm000FVYzcB9rm0Tsv9bQB-yOyE2AIXRRJb_RM|Gute Hooks
60337|s|1_CsOYoMWkUFVOOs-G52uk9_5T5WFkjsw5lzs5ryof6M|Der Weg zu 1000 Euro
60337|s|1kqNU7YjNZ9_l_f2bPQNeviNqiFr-YqPNLFdpZQ8Sqls|Der Weg zu 5000 Euro
60337|s|1Iwu6Ewk_LaIy5WfS4PnWOXfay-5LHFoZYeFkdKGujfg|Der Weg zu 10000 Euro
60337|s|1G_2xbR1GEobSf3YXH0FgXRMB9khxEjE7YEOt-84s_cY|Der Weg zu 30000 Euro
64688|s|19YMWSTluSeNuEV2p-8Q0rUNJHfe86YQv1pSQeihgc7I|200+ Ideen
67073|f|1V3ar-Joqj5RryNvk88k9jRLMq6ncKJsx|Checkout Vorlagen
67073|f|1VI3ZR0wGEwcxnAHlIG0BQ-VtuWcxJhGa|Email Vorlagen
70675|f|1T14t5eX0oiJTX9cjN1nrUUTMVxdtsfqH|Hook Vorlagen
70675|f|171Vxm_WjVUDUMkjNIfk67nlRPDIDr5Rh|Sequenz Minikurs verkaufen
70675|f|1q7rQXapvz0XwBS_ahabarHvRj-CXgKg7|Email Vorlagen
74289|d|1aXWk0ni7C3YzZjgjKoEBFPVKhelcLq9lQfTXKGMNnxk|Cheatsheet Produktfotos
74289|d|1ORpsemHKNHO35FMDt_83Aw-ZTXbAIk_DJOOj_mNdxCo|Cheatsheet Kommunikation
74289|d|1322d8xBgh-0BhZuJ-ofR_gWzD0MTN445lq4Gbc-sPtY|Cheatsheet Pricing
74289|f|1GKs9S-DhFRUeBtxdvRLoCDHUNpzYu-6-|Offerbump Vorlagen
74289|f|1DICAammIR3FRUKX8BSQkZk7JWUpcGivt|Upsell Vorlagen
112946|s|1TrCRnc3-1RZxMH6edvxTlXRiNF6Onjj3L6uWwy8B6us|Dein Launchplan
112946|f|1lSy0XdETmsuNAQmZDUy2NXQzoKuhbkQt|Kaeufertypen x Launchphasen
112946|f|16CMqzmb0i6im1o63aiMRxWlnME4PkTUz|Offerbump Vorlage
112946|d|1vVW4lhDxVx1n7wtTSVs-FDByMqvxzGppM4YMzGVzT7w|Email Vorlagen Minikurs zu grossem Kurs
112946|f|1P5UNwtVW4-Nqnd5RKnTnIvdCEzphZgG8|Webinar Aufbau
133269|f|19C5dDEhI0u8kwgjjh5BNIYn_NeSIGC3Q|Monat 1
133269|f|1ZyGBKQerM1qhQA1BM1iaQZNgkX6JlVVB|Monat 2
133269|f|1p8c_7ODauWiraN-lblrTZiwkrGq-tXxb|Monat 3
133269|d|1l9xjOsi-kTkXEvv6vbjZR0U70X7ZH8h3Q9ey37woWQ4|E-Mail Vorlagen
154216|f|1qwVWsFFFMBuEQDLUyTRZ1bL6c_I_LSoI|Test Reels
154216|d|1DU7SrWHOLvgXKjRKFU8XV1Ho9dSKhJT8QojO5cBws-A|E-Mails fuer Minikurse
165653|s|1GoHcoRr0igWGFT80kZskh1nS7p3dWGFW-S_mEptIbdA|200 Story Ideen
165653|d|1RZKtDaLrNcbZREQ-jvHKwJK91jdXyIneHJsTcbyscuQ|Hook-Checkliste
165654|d|1uDtznfZRI5fB096da9sTIbZuB3cPtWU_ip6Cn9XnlM8|Schritt-fuer-Schritt-Anleitung Launch
165654|d|13moU3WzXb0MsjGCbHGFRrT4Z88i-sEgnxIE5gH289oA|Uebersicht Launchphasen
213147|d|1sjfgP5TNw_fLMkLEiqHPcCEX39rV1--FOQAZ4ONtT1Y|Up- und Downsell Vorlagen
213147|d|1IMzHg8xhpSK3E2L6M2mwV9--yBrPcG7cg2kHX037W2s|Email Vorlagen
213147|d|1MrRG_D0CbRap1vhnfXEqw4AQQzW6IwgDAVlYZnb1mes|Emails vor und nach dem Webinar
"""

ADRESSE = {
    "d": ("https://docs.google.com/document/d/%s/export?format=txt", ".txt"),
    "s": ("https://docs.google.com/spreadsheets/d/%s/export?format=xlsx", ".xlsx"),
    "f": ("https://drive.google.com/uc?export=download&id=%s", None),
}
ENDUNG = {b"%PDF": ".pdf", b"PK\x03\x04": ".xlsx"}


def main():
    for zeile in LISTE.strip().splitlines():
        kurs, art, nummer, name = zeile.split("|")
        ordner = os.path.join(ZIEL, holen.KURS[int(kurs)])
        os.makedirs(ordner, exist_ok=True)
        url, endung = ADRESSE[art]
        bitte = urllib.request.Request(url % nummer, headers={"User-Agent": "Mozilla/5.0"})
        try:
            with urllib.request.urlopen(bitte, timeout=120) as antwort:
                daten = antwort.read()
                typ = antwort.headers.get("Content-Type", "")
        except Exception as e:
            print("FEHLER", name, e)
            continue
        if "text/html" in typ:
            print("KEIN ZUGRIFF", name)
            continue
        if not endung:
            endung = next((e for k, e in ENDUNG.items() if daten.startswith(k)), "")
            if "wordprocessingml" in typ:
                endung = ".docx"
        pfad = os.path.join(ordner, name + endung)
        if os.path.exists(pfad):
            print("schon da", pfad)
            continue
        with open(pfad, "wb") as f:
            f.write(daten)
        print("geholt", round(len(daten) / 1024), "KB", pfad)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
