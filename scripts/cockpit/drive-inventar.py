"""
Schritt 4: die Google-Drive-Ablage als Inventar — Dateien, nicht nur Ordner.

Patricia: „ich habe da so viel zeugs und vieles ist mir gar nicht mehr bewusst.
ich brauch da ne übersicht."

`fundstellen-bauen.py` legt die **Ordner** als Wegweiser in die Suche. Das hier
geht eine Ebene tiefer: jede einzelne Datei mit Titel, Art und Direktlink. Damit
findet die Cockpit-Suche „Storytelling-Checkliste" oder „Reels eBook", auch wenn
Patricia nicht mehr weiss, in welchem Ordner das lag.

Kopiert wird nichts. Was hier steht, ist ein Verzeichnis mit Klick ins Original.

**Die Daten kommen ueber den Drive-Connector herein** (`search_files` mit
`parentId = '<ordner>'`) und werden hier eingetragen. Ein Skript kommt an Drive
nicht heran, deshalb steht das als Tabelle. Neue Ordner: Connector fragen,
Zeilen unten ergaenzen, Skript laufen lassen.

🚨 **Fremdes Material ist als solches markiert** (`fremd=True`). Es erscheint im
Cockpit orange umrandet und darf nie in einem Kundendokument landen.

Was bewusst draussen bleibt: „09 - Admin & Logins" (Zugangsdaten), Rezepte,
Menuplanung, alles Private.

Aufruf:
  python scripts/cockpit/drive-inventar.py [zielordner]
"""
import json
import sys
from datetime import date
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[2]

# Kurzform der Art -> was im Cockpit steht und wie der Link gebaut wird.
ARTEN = {
    "doc":      ("Google Doc", "https://docs.google.com/document/d/%s/edit"),
    "sheet":    ("Google Sheet", "https://docs.google.com/spreadsheets/d/%s/edit"),
    "slide":    ("Google Slides", "https://docs.google.com/presentation/d/%s/edit"),
    "form":     ("Google Formular", "https://docs.google.com/forms/d/%s/edit"),
    "pdf":      ("PDF", "https://drive.google.com/file/d/%s/view"),
    "docx":     ("Word-Datei", "https://drive.google.com/file/d/%s/view"),
    "xlsx":     ("Excel-Datei", "https://drive.google.com/file/d/%s/view"),
    "pptx":     ("PowerPoint", "https://drive.google.com/file/d/%s/view"),
    "bild":     ("Bild", "https://drive.google.com/file/d/%s/view"),
    "video":    ("Video", "https://drive.google.com/file/d/%s/view"),
    "audio":    ("Audio", "https://drive.google.com/file/d/%s/view"),
    "zip":      ("Archiv", "https://drive.google.com/file/d/%s/view"),
    "ordner":   ("Unterordner", "https://drive.google.com/drive/folders/%s"),
    "verweis":  ("Verknüpfung", "https://drive.google.com/file/d/%s/view"),
    "datei":    ("Datei", "https://drive.google.com/file/d/%s/view"),
}

# Die Ordner, in denen gesucht wurde. Schluessel -> (Anzeigename, fremd?)
ORDNER = {
    "01": ("01 · Zielgruppe & Positionierung", False),
    "02": ("02 · Content-Erstellung & Strategie", False),
    "03": ("03 · Prompts & KI-Tools", False),
    "04": ("04 · Angebote, Verkauf & Funnels", False),
    "05": ("05 · Freebies & Lead Magnets", False),
    "05s": ("05 · Story-Challenge", False),
    "06": ("06 · Learnings & Notizen", False),
    "07": ("07 · Bücher & Nachschlagewerke", False),
    "prod": ("Produkte", False),
    "ikm": ("Produkte · Instagram-Kundenmaschine", False),
    "ikmt": ("Produkte · IKM Transkripte", False),
    "mceo": ("Produkte · Mama-CEO", False),
    "mceo4": ("Produkte · Mama-CEO Säule 4", False),
    "pw": ("Produkte · Vom Networkwissen zur digitalen Produktwelt", False),
    "pw2": ("Produkte · ältere Produktwelt-Ablage", False),
    "dot": ("doTERRA", False),
    "oel": ("Öl-Wissen", False),
    "story": ("Story", False),
    "free": ("Freebies (ältere Ablage)", False),
    "mag": ("Produkte · Magnet-Ich", False),
    "dotw": ("doTERRA · Themenwochen", False),
    "enj": ("Öl-Wissen · Enjoils", False),
    "jt": ("Fremd · Content der verkauft", True),
}

# --------------------------------------------------------------------------
# Die Dateien.  (ordner, art, titel, drive-id[, "fremd"])
#
# Stand 16.09.2026: sechs Dokumente wurden gelesen und sind zweifelsfrei
# Kursmaterial (fremde Preisbeispiele wie „9000 € bei mir", Verweis auf den
# Content-GPT einer Mentorin, deutsches ss, Zielgruppe „Coaches" statt
# Network-Mamas). Die uebrigen stammen aus denselben Sammel-Importen und tragen
# dieselben Merkmale. Im Zweifel gilt fremd — eine falsch als „meins"
# ausgezeichnete Datei landet sonst in einem Kundendokument.
#
# 🚨 Fremdes Material steht in denselben Ordnern wie Patricias eigenes — die
# Julia-Trost-Transkripte liegen mitten in „04 Angebote". Deshalb haengt die
# Kennzeichnung an der DATEI, nicht am Ordner. Belegt ueber den Namen (nennt die
# Mentorin), ueber bekannte Kursnamen oder ueber
# memory/reference_julia-trost-drive-vorlagen.md.
# --------------------------------------------------------------------------
DATEIEN = [
    # ---- 01 Zielgruppe & Positionierung ----
    ("01", "doc", "Die Verbindung finden", "1WXLv-lgVijAjdIV5Vp_ySD9LJck1tF3JTwplHRbN7bI", "fremd"),
    ("01", "doc", "Zielgruppenrecherche", "17slu2ZPS6i3HlgZ0vftOZ_tpjtRfxLV4BzRpUx7N5nQ", "fremd"),
    ("01", "doc", "Profi-Version: Zielgruppe vertiefen & psychologisch schärfen", "1He2uWSJxhDLmFqsuN_TB0FJ92q6xCWZSswwuJ6TfEBY", "fremd"),
    ("01", "doc", "MARKENPROFIL Network / MUM LIFE BALANCE", "1RfzytOm6-2r8hd5iZ3SUst0oabFxc9DCNA6UQ8y-msc"),
    ("01", "doc", "Anfänger-Version: Zielgruppe verstehen", "1jiGd3rQ_iZRA5wq6AFGSjbI71hQRPZhwuYmajOqP1H4", "fremd"),
    ("01", "doc", "Zielgruppenanalyse — Deep-Dive für Network-Mamas", "1o0WCH1QZ8Y0OqjdisJOCNX5jeUQvGw9-au5QMkNw4ME"),
    ("01", "doc", "Arbeitsblatt Lektion 0.1 — Mein Warum", "13wCg5BJIDe0K9RY_3C9Fjivp5Cbu-LRZm81AMAVCcOM"),

    # ---- 02 Content-Erstellung & Strategie ----
    ("02", "doc", "STORYTELLING-CHECKLISTE", "1lhetSSXTJHFnHpntUBZg4Qng6b1kjo_h-UGd5YppfFA", "fremd"),
    ("02", "doc", "Hook-Checkliste", "1VmX0zN7tgn3VmG79BrmSfDBez60-rXEImbwvJeCt5Kw", "fremd"),
    ("02", "doc", "Hooks: Gut vs. Schlecht", "1R7hTpAmu2W2MvfuTU-6gPVDIAYfWfXc8iyfdy9mjgpo"),
    ("02", "doc", "Checkliste Content", "19idty_Z4g-f2YDEqngrWdTkZqLa-8W-4yx4k0vo65uY", "fremd"),
    ("02", "doc", "Checkliste: So baust du deine Beiträge auf", "1Y3Ng0trZScKWdwZ4XMSE2yCdAFWo-UoGKxWKsN-Ovqk", "fremd"),
    ("02", "doc", "Checkliste: Verbindung aufbauen", "1SZ-3gTB0LqvbAbmF_18iuH7iK1EjzeZdreQd1tlyJuA", "fremd"),
    ("02", "doc", "Umsetzungs-Checkliste: Sichtbarkeit aufbauen", "1zPUyiyZszQdRNoBtaMGuAu9p5MAOrFD1OIv5oa922uk", "fremd"),
    ("02", "doc", "Feed Content Spickzettel", "120jrKkupF2VFnsAd4p91Lhw4i4LPFUnViaIZoszRki0", "fremd"),
    ("02", "doc", "Content-Ideen entwickeln", "1AWZcR1e-VG8WxChFZHkeHxJ2RLuXmBqWarGDHMmsgBA", "fremd"),
    ("02", "doc", "Content-System Starter-Kit", "1IhpXZRD87U6rfctG4zQgz9pdqZr5ICAzYCtLGR-ADb0"),
    ("02", "doc", "ARIA Content Framework", "1dwJSwPbK-fMHty4F3z6pTPtm48xUieOLieb35hjbcsc", "fremd"),
    ("02", "doc", "Floskeln-Blacklist (optimiert)", "1j_6Ss--qIMycvrSPkCtBzbz4pB3u_WS9roMni4DJaCw"),
    ("02", "doc", "Vermeide diese Wörter in Reels", "1tFsh3duP_mpff27mT3w10-JPJZcWNIJOFMgOADrEr64"),
    ("02", "doc", "Dascha virale Reels 25.02.2026", "1jCquGYNZUywjvca-CvkV5QQcBp85CwM1G8pvs5m6w0A", "fremd"),
    ("02", "doc", "Content-Kalender Januar 25", "1Aq1kd4z6wMHE-Mw7ieOhzDxt4V6bGeZGZEGBVUu22U8", "fremd"),
    ("02", "doc", "eCCC Challenge Verkaufsstory", "1F1p_S6xMG86xmHX-3Jzb3KLn7-_J06_xFpxwqRnWxUc", "fremd"),
    ("02", "sheet", "+200 Story-Ideen", "1SDWZ_iljJsWQ2oHwgamFoFh88dymhRbYBar_Xv5Cu0E", "fremd"),
    ("02", "docx", "Story Cheatsheet", "1_Xj64ccygeiXQJv_UxqOTzoNVyJ4BCRa", "fremd"),
    ("02", "pdf", "150 Content-Ideen Teil 1", "10Y4pfT0_nQCDAcyFH24twd7fD8NiDBiU", "fremd"),
    ("02", "pdf", "150 Content-Ideen Teil 2", "1kle1NjhgSRSPJcBAPt9Ir3Jt4Cur70iU", "fremd"),
    ("02", "pdf", "150 Content-Ideen Teil 3", "1lwS8xIa5bai53pcIfIEymXDwnzRkbOyT", "fremd"),
    ("02", "pdf", "Story-Bibliothek 2021", "1L5zjwtAVKgQ-jIqD8oNnYuhyiMUbgQlK", "fremd"),
    ("02", "pdf", "Story-Bibliothek 2022", "1wV-H8qo03xv2xLkY3qhMjHrIKlpjS36-", "fremd"),
    ("02", "pdf", "Story-Bibliothek 2023 Teil 1", "1k0QN5VIRaLHcuri4FkaywcdadSlThTbf", "fremd"),
    ("02", "pdf", "Story-Bibliothek 2023 Teil 2", "1uudD7esrIdtaUBlmNEKhE_nGywZ-WSHu", "fremd"),
    ("02", "pdf", "Story-Bibliothek 2023 Teil 3", "1JRq-z5vVU8uuRatBoSCXuaD84SFG8i9T", "fremd"),
    ("02", "pdf", "Reels eBook", "1v44ns72hS59Py7x4pSPtmS6jjTBqA5j5", "fremd"),
    ("02", "verweis", "Schritt 1: Nische finden", "1B1gjTy28S8odU0SuoCkaDAGIKWCJ8sFf", "fremd"),
    # ---- 03 Prompts & KI-Tools ----
    ("03", "doc", "GPT-Prompt: Themen- und Zielgruppenanalyse mit Tiefgang", "1UAQE6MqXJBc5yUiFOk-gHGu7V2ssUarN7H6p7gbt-Xk", "fremd"),
    ("03", "doc", "Prompt für die Jahresplanung", "1MyS49Mk1q-unIMMDyiPhb04K33-g7F0pdl3qZ5QfD0Q", "fremd"),
    ("03", "doc", "Prompt für Minikurs-Erstellung", "1Rww60bonPYv2HdMfQqY8K30dHCnUlYrwotggqQ0-8Ow", "fremd"),
    ("03", "doc", "Prompts für KI-Tools", "1Qd9xfkhxc5l00ioNT4jLwbBVhlw_da1DnX6eMwJYIKw", "fremd"),
    ("03", "doc", "Eigenen GPT erstellen", "1doTueswZJ7vzsys60SiaV2T8z7jODBksZ3o4ojEsWhw", "fremd"),
    ("03", "doc", "Zwei KI-Assistenten selbst aufsetzen", "1nMH2qwtwcTOf5ti42VGY2iox4nkbqvR5is7y0FcVynA"),
    ("03", "doc", "Automatisiertes Karussell erstellen", "1_yOxGCPZYrvckB5az2j8SV0YH4RTUFP1Canqxf7-NZ0", "fremd"),
    ("03", "doc", "Canva-Karussells mit Claude Code — Anleitung für Kundinnen", "1K95qcCLkUEc4biL6gCKI90DmGWZsv5lh9P0UcwB4Bbk"),
    ("03", "doc", "Claude-Code-Anleitung für Einsteiger", "1VKZkU_XKVAwTnPhl9f_08pZfezARSWC5BF98Q21sz7M"),
    ("03", "sheet", "Anwendungsfälle und Prompts", "1jQMFE9ppbBjT4xMVBEgbcYw_-tC4la584oeKEEZn_tU", "fremd"),
    ("03", "pdf", "Produkttreppe-Skill für Network-Mamas", "1rAk9jbo5IFx1m0M0RLa0EBPSI3_4vU2Z"),
    ("03", "pdf", "Claude Business-Brain — Anleitung", "1Ul7GTgx5TJto7oo9eGVlGRBFUjh2Dcw3"),
    ("03", "pdf", "Claude Business-Brain — Anleitung Produktwelt", "1yN0Yfpjkg_orRHq4LVrvGjCdGDuQ9A_U"),
    ("03", "pdf", "Content-KI-Ablauf: Fahrplan", "1UNtkd9X5CM47mKf7MtCDBRM1qdDMseqT"),
    ("03", "datei", "Wissensgrundlage Instagram-Kundenmaschine (Text)", "1VhdaLmN0zSym1YY0xZeGtw8D2Gbl0lFE"),
    ("03", "datei", "Wissensgrundlage digitale Produktwelt (Text)", "1fuff0V3vC4V-2DBWCy8Nel6TdI3uEU7-"),
    ("03", "ordner", "Claude Code Mastery Transkripte", "1IzMut1f_QAkuCjJWCVvy2CGWkf0MFgid"),
    ("03", "verweis", "PE: Schritt 3.1 Angebot", "1qCA4YNZTfwgW_GcAFrI_XjoxrrrRtZjn", "fremd"),
    ("03", "verweis", "Schritt 1 — Prompts", "1C64zB0fvioaOOXVkhLUwMGrKT-8iS8A3", "fremd"),
    ("03", "verweis", "Eigenes KI-Tool mit Claude bauen (Hook-/Salespage-Generator)", "17SRqdRcaGxB_lEFEGuyjhq68ImDlg73-", "fremd"),

    # ---- 05 Freebies & Lead Magnets ----
    ("05", "doc", "Starterguide für Network-Mamas", "19bl5PoDFk-DqWcIqofRc-kZqb8_v-a3fJvqv69dHEQQ"),
    ("05", "pdf", "KI-Strategie-Prompts (Patricia Ulmann)", "1ha9RR4FluxaIlIObFP-DeQGvvurApik7"),
    ("05", "ordner", "Story-Challenge", "1_vqer0RRALsbDOJUfoJU6BOeh2VanQmH"),

    # ---- 04 Angebote, Verkauf & Funnels ----
    ("04", "doc", "Verkaufs-Checkliste", "1t5vJlLSvR2xqsfryTHbaYGElsm_xp7ShnEM85Eezvbs", "fremd"),
    ("04", "doc", "So kommst du auf Produktideen", "17KChMPofX-tR82SekFSKeiVpCq215fOUUy-XRxfBeoE", "fremd"),
    ("04", "doc", "Anleitung zur Erstellung von Mini-Kursen", "1Uf0rEHMNmCn18RekLTXfPvk1Lv84dr9TuCCAXeT1QAA", "fremd"),
    ("04", "doc", "Minikurse — Ideen", "14w57MXn_ThwQiD3EbdaS8wkdGWzT7_xkqMLmZMJd8IU", "fremd"),
    ("04", "doc", "Produktkommunikation", "1eZcVztSARWxzIH-oN6DsVDdslVlTktcM_SHDYx0kOQ8", "fremd"),
    ("04", "doc", "Preisstrategie-Cheatsheet", "1bsUgKSKJRAsvsHk5PTRiT3SSo4GN6ZtfAmGgx1wYX8k", "fremd"),
    ("04", "doc", "Wiederkehrendes Einkommen — Strategien im Überblick", "1MsONF4ZlzDhYB5INSoUq-_f0764cbRAmb3ymm--Z_cg", "fremd"),
    ("04", "doc", "Vorlage Anmeldeseite für Webinar", "1ViwRDcUwkTXV652d33e7H9oog4sQ1Tb9-4X4PIaxGHc", "fremd"),
    ("04", "doc", "Vorlage Dankesseite Webinar-Anmeldung", "148FkhPnKCuO-LB3hLxkYSQlgG1nypDf44z4K70GUOTk", "fremd"),
    ("04", "doc", "E-Mail-Reminder für Lives", "18u9AqUuA4doTQ8QdubHJzZcrcnKP86EtlopG20bnQOM", "fremd"),
    ("04", "doc", "Upsell-Seite (lange Fassung)", "12QYejVJgDByESiUmplLmTjYxIyZaDnVFhQBje7QfcaU", "fremd"),
    ("04", "doc", "eCCC Challenge Verkaufsstory", "1maPZ-5GbWmGa583mGicVxcoLZkKIdtzRF5M13O_kw1A"),
    ("04", "docx", "20 E-Mail-Vorlagen (Paket)", "1gnCMyitJMJ4_R8_H8XkhCcG-0RpZjxIG", "fremd"),
    ("04", "sheet", "Schritt 1: Nische finden", "1uxvLwDDcEveA5LIs7MlUioHXUKJrfHTF4xnqjYbVAZo"),
    ("04", "verweis", "PE-Schritt 3.2 Recherche-Dokument", "11o7-byC6gNFPfMuSdf9_nUf2oT-0f-JO", "fremd"),
    ("04", "pdf", "doTERRA Summer BOGOs 2026", "1VvYLpdWqjAbYkPbz85_n4nSCffbGDBFc"),
    ("04", "pdf", "doTERRA Aktionen Juli 2026", "1FB53TpDLhrVLcEq2417MpnASxyKMklD2"),
    ("04", "doc", "Digitale Produktwelt — Transkription", "1MUX3vg1M_DsDVlOy3N6-cu6ikDmIdzLzOJ6x3sZi310", "fremd"),
    ("04", "doc", "Magnetisch verkaufen — Transkription", "1AyD4VTtmlQLhmjvVpxeADeA205TgDt2KmklgiIxfhpE", "fremd"),
    ("04", "pdf", "Automatisiere Webinar-Funnel", "1iiq2kA1uEGJkkQANb1v9UBKoQellaBMf", "fremd"),
    ("04", "pdf", "Automatisiere Copywriting", "1oPRwAQfheN8tio1IM5HfwkAF_y3-2lN8", "fremd"),
    ("04", "pdf", "Automatisiere Salespages", "1jKmtvoH-dAXMHio5wLiw7j48bf9blnuv", "fremd"),
    ("04", "pdf", "Verkaufs-Workbook", "1imKmrYdIAdzUnyVZLSYDRBRlbcItLeUR", "fremd"),
    ("04", "pdf", "Minikurse — so launchst du", "1eK4MiKXnfHbu3BiKB5rdgdVXsWE-sSRA", "fremd"),

    # ---- 05 Story-Challenge ----
    ("05s", "doc", "Mail evergreen (Story-Challenge)", "1rxbaQFDAyvhUm7dchMTnvLggSdLKulxD4FOpEGexALE"),

    # ---- 06 Learnings & Notizen ----
    ("06", "doc", "Tag 1 (Challenge-Mitschrift)", "1UaQpweyi3Hyts0P5am0VJLs_GNjqfbSHNAhr_n3lzbU", "fremd"),
    ("06", "sheet", "Erfolgreich ins neue Jahr", "1ZWx2rpv1vLXQE0wzaHZgc6egX0rscomWFyoFwS4be3w", "fremd"),
    ("06", "doc", "Learnings aus Calls", "1F0_ggsETMDI5E-7UPUNJ7wzgLyIFSQNXEXfoFit2DjU", "fremd"),

    # ---- 07 Bücher & Nachschlagewerke (fremde Fachbücher) ----
    ("07", "doc", "Jahn: Kinder sanft und natürlich begleiten", "1snhWRpS1I4Pe7L2mOaM27bfETcWzCDAvp1V6VwLVBlU", "fremd"),
    ("07", "doc", "Schasteen: Schlafstörungen — besser schlafen", "1rTtwG5M-fnfcBmipm8RdrFph1v_fSA0NGI0KT4updr8", "fremd"),
    ("07", "doc", "Herber: Aromatherapie für Kinder", "1YSU94juh6gLn-CVfet3YOz9TpWZ75Fh7-3dXvFRcYv4", "fremd"),

    # ---- Produkte (Oberordner) ----
    ("prod", "pdf", "90 Storyideen für Networkerinnen", "1ZyMrSkozq194biG4N3LfXXhhOna4e76k"),
    ("prod", "pdf", "Content-Box — Hookvorlage", "1IppowZ4PyvcAFnExL7bAnmX3WkjUh7dT"),
    ("prod", "pdf", "Von 0 auf echt", "14V8ev42G5aPfFwpnl1g9c_o0XojWaUYF"),
    ("prod", "docx", "Fahrplan: von Produktposts zu doppeltem Einkommen", "1EkNcSbx3nXAexoW8oqjfhQIazoDRWLsl"),
    ("prod", "ordner", "Instagram-Kundenmaschine", "1t7Nf8BVfQLCUGJ_TmZUl7-HJcIQY-VsZ"),
    ("prod", "ordner", "Mama-CEO", "1LFGlsY28dP3ZVQnDF_2EBEYCGubjTh7e"),
    ("prod", "ordner", "Vom Networkwissen zur digitalen Produktwelt", "1qFMuKUyNi8VnQErlMkW6d29lP4oOZU9J"),
    ("prod", "ordner", "Magnet-Ich", "10e_5DS2ls-_ZWj-u5GnxEBNNvJkgvxuW"),

    # ---- Freebies (ältere Ablage) ----
    ("free", "pdf", "Starterguide für Network-Mamas", "1AHPvD7LM8f4EtM5gF6bdhTWQNKhjvOyA"),
    ("free", "pdf", "Workbook Story-Challenge", "12l8gjwhK4495Eax7NwCFMU30pksda0G3"),
    ("free", "pdf", "Lead-Challenge Workbook", "1Aip9iHvGkgN4DmGBMSB5P55tMFvRX5da"),
    ("free", "doc", "Dein Start in eine klare Positionierung", "1bOR3o-TPkZqFrx6Pm_b74_kkw44NUQB-lFkFetLiQ8g", "fremd"),
    ("free", "doc", "Prompts für Minikurs-Erstellung", "1eZ3hUky6Y8cDGbbHecV3IELePNGTj0tNoJEOv-dMDvc"),
    ("free", "doc", "Checkliste: Macht dein Content den Unterschied", "1WtOAA5l80A_6za2bYjC6qZGE9jdFhk__W09nRNv1AYw", "fremd"),

    # ---- Produkte · Instagram-Kundenmaschine ----
    ("ikm", "doc", "PE-Schritt 3.2 Recherche-Dokument IG-Kundenmaschine", "1F0kQhSWBdMk-2B_yk5cYCQHd2J-N6QA1rpOjtcn6hGE"),
    ("ikm", "ordner", "Transkripte der Calls", "10hUlE1-JzEBRU_ssdCsf8gKKwQ2CV_26"),

    # ---- Produkte · Mama-CEO ----
    ("mceo", "docx", "Mama-CEO Arbeitsblatt Säule 1", "1fjDR8QRrGpGZdW-r5Daice4k209GeYFW"),
    ("mceo", "docx", "Mama-CEO Arbeitsblatt Säule 2", "1z8kEQeqffBLuHOS8L_AgH1SyL6cqZsex"),
    ("mceo", "docx", "Mama-CEO Arbeitsblatt Säule 3", "1c8GXeI6GOR2L1FvUZ5M5YDATwrbkCioD"),
    ("mceo", "docx", "Mama-CEO Arbeitsblatt Säule 4", "1e3VvD2VSQRSoT2z5QhaSbT9AsJgKvboq"),
    ("mceo", "docx", "Mama-CEO Arbeitsblatt Säule 5", "12xWSSYQ0sHQI0gvZDhp6QxaNh6VdRjr9"),
    ("mceo", "verweis", "Mama-CEO Mini-Workbook · 3 Sachen zum Abgeben", "1_5cB9F4vRENhIEoDUHGm4sbXiVp-SWxr"),

    # ---- Produkte · Mama-CEO Säule 4 (die Bonus-Vorlagen zum Weitergeben) ----
    ("mceo4", "doc", "Haushalts-Helfer-Vorlage", "1ER51llHy33luKbNw4QwGpXJz-SmN--WHdqQQ9N3PoRw"),
    ("mceo4", "doc", "Notion-Haushaltsliste-Vorlage", "1sJSU6YIn1UoyZlyD3rTc2K4jqkBo366HDg1yrgN45XY"),
    ("mceo4", "doc", "Cockpit-Bot-Vorlage", "1YBXq8nEpjEQSUob64kLmIv9g8-LkIWE2y7Uh0L88_7w"),
    ("mceo4", "doc", "Kochassistent-Vorlage", "1KTC4yTw09rwZWFPOSazNaxtrusuHHaUtMYbkHMphDSo"),
    ("mceo4", "doc", "Kochassistent-Vorlage (ausführlich)", "18dq-SjAjwXudfgmh9KU7siGufejpzXieonZ-qUg7Z-8"),
    ("mceo4", "doc", "Business-Brief erarbeiten — Prompt", "1nPUh44WM5y8p1NkqypVfIYxyfZpo3GKdovMOtzF3JIU"),
    ("mceo4", "doc", "Gratis-Chat One-Shot", "1MmutD69t6hcajTkCuoJvbVQgou4z7XmZdfOB2v8q-ns"),
    ("mceo4", "doc", "Claude Code aktivieren — Anleitung", "1osqJy-mCN_AksIl4D9hQBGZgmGdEhknJGOsyiTFrSfs"),
    ("mceo4", "doc", "Cowork einrichten — Anleitung", "1b3mHMYT47nO2HqhDFXvXIRxeSI4ED-unqbioRk1yJYE"),

    # ---- Produkte · Magnet-Ich ----
    ("mag", "pdf", "Onboarding Magnet-Ich (ausfüllbar)", "13LIn7eqdQ7csQR3E_E-Vr-stQZufT4ZG"),
    ("mag", "ordner", "Magnet-Ich · Kundinnen-Ablage", "12XXYpMg3IDe3EBIBLZxw5a3t8TtRCww0"),

    # ---- Produkte · Vom Networkwissen zur digitalen Produktwelt ----
    ("pw", "docx", "Prompt 21: Salespage für mehrere Plattformen", "18kx0U-bAJI9xu-C71OCL9Ay8b0kmGK6O"),
    ("pw", "docx", "Prompt 22: Upsell, Bumps, Bundle, Downsell", "1rjhksSvBuiH9UxFq172zzl7w0AugGw3z"),

    # ---- Produkte · Arbeitsblätter des Kurses ----
    # 🚨 In diesem Ordner liegen dieselben Arbeitsblaetter mehrfach (3.2 vier
    # Mal, 3.4 vier Mal, 2.2 zwei Mal, 6.1/6.2 je zwei Mal). Hier steht je
    # Lektion nur die zuletzt geaenderte Fassung — sonst sucht man im Cockpit
    # zwischen Dubletten statt im Drive.
    ("pw2", "docx", "Arbeitsblatt Lektion 0.1 Mein Warum", "1K0AKBkVXOhkvzp5dONYUOs58KHyVC578"),
    ("pw2", "docx", "Arbeitsblatt Lektion 1.1", "14llmNEHz9PLlCxjgmIJfWLFkktRqfbsS"),
    ("pw2", "docx", "Arbeitsblatt Lektion 1.2", "18s6FmeciyocSVQQnCsyfdZYjZjC-1WPB"),
    ("pw2", "docx", "Arbeitsblatt Lektion 1.3", "1BAtisrpViLfI1PU2VwdjHM7f1b6doNXM"),
    ("pw2", "docx", "Arbeitsblatt Lektion 2.1", "1CiLYfKEtmebHHfhhpmp2PyIsy5HPqE6V"),
    ("pw2", "docx", "Arbeitsblatt Lektion 2.2", "1JFsm6JsgLYZ2k7bYIilsLW5yq7IbknZY"),
    ("pw2", "docx", "Arbeitsblatt Lektion 2.3", "1pKDvDIbOPlEqoKiIWQwMUWTHTF-jdCFo"),
    ("pw2", "docx", "Arbeitsblatt Lektion 3.1", "1jj2RF49M5UZDP3XN9fHg_LtofzamR4f1"),
    ("pw2", "doc", "Arbeitsblatt Lektion 3.2", "1BIpDzNPe-AEEsSNLsaNhx0WJuYM7wl8CLI-9C6Hv_F8"),
    ("pw2", "doc", "Arbeitsblatt Lektion 3.3", "19qeP1PaRLh8kdC_S96ARcgktgFiPbK_MxOBskhhcMJk"),
    ("pw2", "doc", "Arbeitsblatt Lektion 3.4", "1VLvOfd4hW3iAdwIakc-kFu3_MuXsJ9OqIVJvCVJAEoo"),
    ("pw2", "doc", "Arbeitsblatt Lektion 3.5", "16AeNBv1eLkBugPq_iOmEj7iOLpO6cHAHA_RKBuIGY4w"),
    ("pw2", "doc", "Arbeitsblatt Lektion 4.1", "1Xf3tu5mSmRDWGorYpDFPdRAC2UgaSwu1CqCP4mjwBiw"),
    ("pw2", "doc", "Arbeitsblatt Lektion 4.2", "1mV2TrEGiwjLf_G1jFxOjwwoFEMdavo50pgv76MvNGn4"),
    ("pw2", "doc", "Arbeitsblatt Lektion 4.3", "1H0AbMbOPVRBiIyhOQe1-HK_mJAUWyEMLlRjheifvA_w"),
    ("pw2", "doc", "Arbeitsblatt Lektion 4.4", "183X987SUhik0zKdohZ4Gi5qlnD_wLikiMUDH3S5tqUs"),
    ("pw2", "doc", "Arbeitsblatt Lektion 5.1", "13gJMYYZpX4PsPzz8wJCzcGxBI-LyKYjp4zEOBHqAej8"),
    ("pw2", "doc", "Arbeitsblatt Lektion 5.2", "1Wgla_kpTwjpX7yLqhfqX_kF01a7TUB-2BA3NlXNpri8"),
    ("pw2", "doc", "Arbeitsblatt Lektion 5.3", "1xzdnoPO4eafrk6n5rugjsnrlet72WGasLkrKJRORWJA"),
    ("pw2", "doc", "Arbeitsblatt Lektion 5.4", "18hC-zR0s4HNYBxlF_vM7GkBLoRuBA6b9RVIT1pIHAFY"),
    ("pw2", "doc", "Arbeitsblatt Lektion 6.1", "1RKy7-3M-RthIdgS5z548er3-0Av8hQblsH-sIXoY49U"),
    ("pw2", "doc", "Arbeitsblatt Lektion 6.2", "1g-so9kECckZjbD6PAy1zWch1DHfMVg0CqKdYkLxanxk"),

    # ---- Story (nur Verknüpfungen auf fremdes Material) ----
    ("story", "verweis", "Stories 2023 Teil 1 (Jan–Apr)", "1B8g6KHdBkaXOq-soxngyL7RmlApz7TH0", "fremd"),
    ("story", "verweis", "Stories 2023 Teil 2 (Apr–Jul)", "1k8wMdVabDEDythTNHRlJvWFppokTn5aZ", "fremd"),
    ("story", "verweis", "Stories 2023 Teil 3 (Jul–Okt)", "1NAYUsK5wtmNONWF864vhvD-YV1QLavwN", "fremd"),
    ("story", "verweis", "Stories 2023 Teil 3 (Okt–Dez)", "1Sh-ZNzWtkexYKa1haFRr8vgHSnMJ8wOA", "fremd"),
    ("story", "verweis", "Story-Ideen (3-Säulen-Ideenbank)", "1LSkQB2vqoY3kxxbYSEvNqtaS7u4CBJgD", "fremd"),
    ("story", "verweis", "Story Cheatsheet", "1CFNJg7aM1kzUB6c_NyX4UfZHUb555z3C", "fremd"),

    # ---- doTERRA ----
    ("dot", "pdf", "doTERRA Aktionen Juni 2026", "1TVCerw-wJlCBAIbFnLS0dbY-hbBK9rEE"),
    ("dot", "ordner", "Themenwochen", "1V2eUZ_-MtzWD1sug0ZEFj2DcUPOGjUia"),

    # ---- Öl-Wissen ----
    # Die Fachbuecher gehoeren anderen Autorinnen. Sie stehen hier als
    # Nachschlagewerk, nicht als Material zum Weitergeben.
    ("oel", "pdf", "doTERRA Aktionen August 2026", "1PvZPySU8dxLFSiqikhmDxqJEjRkL-cTx"),
    ("oel", "ordner", "Enjoils", "1kTt3QWwV9IlIfPcEXRAyxSg9QTEZKj2A"),
    ("oel", "pdf", "wendepunkt-story", "10-HREnLnuBJAgqff1rtO_ttno3WzWRbP"),
    ("oel", "pdf", "Lead-Guide", "1aKXGr51FEjqBQYhvhN3pBjb-eejBiBi1"),
    ("oel", "pdf", "Praxis-Aromatherapie (Werner)", "1UMUYIUbEHlz-0Py3f0R-O8hkkbwd1vP1", "fremd"),
    ("oel", "pdf", "Kinder sanft und natürlich (Jahn)", "1xECCuZlwZmpr0v_7gIRbdrzGdMJyvvEa", "fremd"),
    ("oel", "pdf", "Schlafstörungen (Schasteen)", "17w0g4E_1xJpHUaCOuY9ZkuVbT7oCr8_0", "fremd"),
    ("oel", "pdf", "Aromatherapie für Kinder (Herber)", "1UOyKTs9tlQxrPIhW2e8334_ot3j4I-Zm", "fremd"),
    ("oel", "pdf", "Duftmedizin mit Zitrone (Schasteen)", "1pnvTuCezt9m5fiZkTocmINPJtACXwavx", "fremd"),
    ("oel", "pdf", "Duftmedizin: Das Praxisbuch (Schasteen)", "1oKR4YujWKy9piG5ZpOdAMdoO9QxfrQPI", "fremd"),
    ("oel", "pdf", "Duftmedizin für Kinder (Schasteen)", "1GdcErlvoZ5X2amqRdKFWU8VH02sgL07s", "fremd"),
    ("oel", "pdf", "Erkältung (Schasteen)", "1aZZ0k_9_d2VEsuiWIKh2sadWspwKCNmy", "fremd"),
    ("oel", "pdf", "Öle, die die Seele heilen (Warner)", "1B8ET78pLqNTAdi0rwDuUHFuVCp5u9L3r", "fremd"),
    ("oel", "pdf", "Holistische Aromatherapie (Mock/Hanika)", "1gVhGdd0e8g5HiedfBo0vNw_hYlRk6f_d", "fremd"),
    ("oel", "pdf", "Spiritual Leadership (Mahlow)", "1sFpoh-osYh6BJuAwxm2iW5gTVUMX0vRu", "fremd"),
    ("oel", "pdf", "Go Pro (Eric Worre)", "15w1P9u3oKQ4pt_eYM3kDNijNpf6O4LsJ", "fremd"),
    ("oel", "pdf", "Unbox your Network", "1tBBCyPkx-uw0CjowYhnQ2JuFyU8TW26F", "fremd"),
    ("oel", "pdf", "Leitfaden sichere Anwendung ätherischer Öle", "1oabtAN9z9e9nw5lEfozOk_5eamfI6Ii6", "fremd"),
    ("oel", "pdf", "Wirkstoffwissen: Oxide", "1oiBoeVQsBfpOtV-Bm0njJi_xn5TCKx-n", "fremd"),
    ("oel", "pdf", "Zimt", "1xJ00ZUP1OhHo_tphwF-kCt4xxYTxSboN", "fremd"),
    ("oel", "pdf", "Myrrhe", "1MvB5h46-lzPbglZKz856HIGKl4m0YcS-", "fremd"),
    ("oel", "pdf", "Thymian", "1wD2VoCHsXkUZrzjrBi0SLQJMsh5YBbtv", "fremd"),
    ("oel", "pdf", "Gesund im Winter", "1iVOKlHCaED5YanXvO64N-x08Pl7F2Xit", "fremd"),
    ("oel", "pdf", "Winter 2024", "1TSdYqnBj4iE0iGhcje4bq1p-Lj_ybEir", "fremd"),
    ("oel", "pdf", "Winterzeit, Feiertage, Rauhnächte", "1q4L9645Qm4AQ1DI4iLJlh7vpckWHdiRJ", "fremd"),
    ("oel", "pdf", "Ätherische Öle und Sauna", "1f-qx4tyz1q9DEVKBv06fjHkvXOQGtg2U", "fremd"),
    ("oel", "pdf", "Suppen und Eintopf mit ätherischen Ölen", "1dFjzIK1CEB0GaM-8ZNMZ4WNobcQdfDcd", "fremd"),
    ("oel", "pdf", "Schlaf gut", "115r1uQFuAxXcM4h7BXW4frzqg-bY0UMg", "fremd"),
    ("oel", "pdf", "Selbstliebe-Duftmischung", "18xpugtJ4bJUNSECndemkOMJ3CXsn-MgZ", "fremd"),
    ("oel", "pdf", "Innehalten", "1KM1tbf3TI97SFvZZ6ML8rNMRgIyoIMiY", "fremd"),
    ("oel", "pdf", "Solfeggio", "1MqZY1kg8qX0iBZnkmUHvQlA-aZ7YHTuB", "fremd"),

    # ---- Produkte · IKM-Transkripte ----
    # 🚨 Nur als Ordner-Wegweiser. Die 20 Lektions-Transkripte stecken schon
    # im Kurs-Index (kurse-indexieren.py) — zweimal dasselbe in der Suche
    # macht sie schlechter, nicht besser.
    ("ikmt", "ordner", "Instagram-Kundenmaschine · 20 Lektions-Transkripte", "10hUlE1-JzEBRU_ssdCsf8gKKwQ2CV_26"),

    ("jt", "doc", "Transkripte „Content der verkauft“", "1ROS2IMw9Pvn_C7qy7H3ZCh9hRvMhPce4yjcSOOMp0Nw"),
]


def main():
    ziel = Path(sys.argv[1]) if len(sys.argv) > 1 else \
        ROOT / "outputs" / "cockpit" / "abgleich"
    ziel.mkdir(parents=True, exist_ok=True)

    eintraege, unbekannt = [], set()
    for zeile in DATEIEN:
        ordner, art, titel, kennung = zeile[:4]
        if ordner not in ORDNER:
            unbekannt.add(ordner)
            continue
        name, fremd = ORDNER[ordner]
        if len(zeile) > 4 and zeile[4] == "fremd":
            fremd = True
        artname, muster = ARTEN.get(art, ARTEN["datei"])
        eintraege.append({
            "d": muster % kennung,
            "t": titel,
            "a": artname + " in " + name,
            "b": "Fremd · Drive" if fremd else "Drive",
        })

    if unbekannt:
        sys.exit("Unbekannte Ordner-Kuerzel: %s" % ", ".join(sorted(unbekannt)))

    heute = date.today().isoformat()
    (ziel / "drive-dateien.json").write_text(json.dumps(
        {"items": eintraege, "stand": heute}, ensure_ascii=False),
        encoding="utf-8")

    from collections import Counter
    zaehler = Counter(z[0] for z in DATEIEN)
    fremde = sum(1 for e in eintraege if e["b"].startswith("Fremd"))
    print("  %d Dateien aus %d Ordnern · davon %d fremd"
          % (len(eintraege), len(zaehler), fremde))
    for k, (name, fremd) in ORDNER.items():
        if zaehler[k]:
            print("    %-52s %3d%s" % (name, zaehler[k], "  (fremd)" if fremd else ""))
    print("\nAbgelegt in: %s" % (ziel / "drive-dateien.json"))


if __name__ == "__main__":
    main()
