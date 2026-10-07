---
tags: [produkt, funnel]
---

# Masterclass-Tag · Do 8. Oktober 2026

**Webinar 09:00.** Die Aufzeichnungs-Mail geht um **16:00** automatisch raus
(Automation 84 „0€ KI Webinar", 6 Anmeldungen bisher).

---

## 🚨 Zwischen Webinar und 16:00 — sonst geht ein toter Link raus

Zwei Mails tragen den Platzhalter **`#aufzeichnung-folgt`**. Wer darauf klickt,
bleibt auf der Stelle stehen.

| ID | Mail | Automation |
|---|---|---|
| **801** | Versand Aufzeichnung | 84 · geht **heute 16:00** raus |
| **792** | 1. Mail Stimmcheck nach Masterclass | 83 · b-Zweig |

**Schritte:**
1. Zoom-Aufzeichnung exportieren
2. Auf **Vimeo** hochladen, unlisted — so läuft auch das MBA-Webinar
   (`vimeo.com/1214949645`, eingebettet auf `/mba-webinar-replay/`, WP 4025)
3. In **beiden** Mails `#aufzeichnung-folgt` durch die echte Adresse ersetzen
4. Gegenprobe: in AC auf den Link klicken, nicht nur speichern

Geprüft am 07.10.: die übrigen 13 Launch-Mails (798–809, 784–796) sind sauber.

---

## Danach — die Werbeanzeige fertig bauen

Entschieden am 07.10.: Beworben wird die **Aufzeichnung**, nicht der Stimm-Check.
Das war der Plan von Anfang an.

| Schritt | Aufwand | Stand |
|---|---|---|
| Seite `/ki-masterclass-replay/` mit dem Video | ~1 Std, Muster `/mba-webinar-replay/` | offen |
| Automation „Aufzeichnung" — 4 Mails, **nur Wartezeiten** | Texte da (801, 802, 809) | offen |
| Anzeige umhängen | 20 Min | Texte + 6 Creatives fertig |

🚨 **Warum eine neue Automation:** 84 hat **6 feste Termine** (`untilSpecificDay`,
gemessen 07.10.). Wer sich am 20.10. einträgt, rauscht durch alle sechs auf einmal
durch und bekommt die Mails in verwürfelter Folge. Für Anzeigen-Traffic unbrauchbar.
Die Stimm-Check-b-Strecke (83) läuft dagegen auf Wartezeiten und taugt als zweites
Ad-Set.

**Fertig und schaltbereit:**
`outputs/ads/facebook-ads-stimm-check-2026-10-07.md` — 10 Hooks, 3 Primärtexte,
5 Überschriften, 5 Beschreibungen, Kampagnen-Klickweg, Budget
· `outputs/ads/creatives/stimm-check/` — 6 Bilder (2 Konzepte × 1:1, 9:16, 16:9)

🚨 **Die Anzeige gehört spätestens am 17.10. gestoppt.** Die Kasse schliesst am
23.10., und die Mail-Strecke braucht bis zum Kurs-Pitch drei Tage.

---

## Preis-Umstellung nicht vergessen

- **Do 15.10. abends:** Easy KI von 277 auf **333** (Scheduled Task
  `ki-kurs-preis-auf-333` liegt)
- Auf der Kursseite `PHASE` in `ki-kurs-bauen.py` auf `regulaer`

---

## Was sonst noch offen ist

- **MBA-Seite** `/mba/` (WP 3857): Easy KI fehlt an 5 Stellen. Fertiger Inhalt in
  `_sicherung/mba-widget-neu.html` — muss **von Hand** in Elementor rein, weil die
  Firewall der Seite REST-Schreibzugriffe mit HTML blockt (510, vier Wege geprüft).
- **ThriveCart-Verkaufsseite MBA:** Easy-KI-Block im Mama-CEO-Muster, Text liegt in
  `outputs/produkte/mba-launch/easy-ki-ergaenzung-mba-seite.md`
- **Mail 0 KI-Kurs:** fertig (`scripts/ki-kurs/mails-bauen.py`), muss in Automation
  85 — die trägt noch die 7 Startklar-Mails und ist inaktiv
- **Loop 2:** Signature-Käuferinnen sollen dort einsteigen, nicht bei Tag 87
  (Loop 1 verkauft „Finde dein Thema" für 39 an jemanden, der 277 bezahlt hat).
  Braucht einen Tag „Loop 2 Start" plus Trigger in Automation 75.

---

## 🔗 Verwandte Notizen

- [[09-funnel-geruest]]
- [[facebook-ads-stimm-check-2026-10-07]]
