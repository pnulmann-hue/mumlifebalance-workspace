# Instagram-Zahlen holen

Holt Reichweite, Speicherungen und Geteilt-Zahlen pro Beitrag über die Meta
Graph API — die Zahlen, die sonst nur in der Instagram-App stehen und deshalb
nie in der Notion-Content-DB landen.

```bash
python scripts/instagram-insights/holen.py              # letzte 25 Beiträge
python scripts/instagram-insights/holen.py --anzahl 50
python scripts/instagram-insights/holen.py --storys     # nur die aktiven Storys
```

Ergebnis landet in `outputs/instagram-insights/JJJJ-MM-TT.md` (lesbar, mit
Obsidian-Tags) und `.json` (zum Weiterverarbeiten).

Nur Python-Standardbibliothek, keine Installation nötig.

---

## 🚨 Storys laufen nach 24 Stunden ab

Instagram gibt Story-Zahlen **nur heraus, solange die Story aktiv ist.** Wer
zwei Tage später nachschaut, bekommt sie nie mehr — es gibt kein Archiv über
die API.

Für Beiträge gilt das nicht, die kann man auch Wochen später abfragen.

Wenn Story-Zahlen dauerhaft mitlaufen sollen, muss das Skript **täglich**
laufen, am besten abends, wenn die Storys des Tages noch stehen. Dafür wäre
eine GitHub Action der passende Ort (Muster: `.github/workflows/apify-scrape.yml`).
Dann muss der Token allerdings als Repo-Secret liegen und alle 60 Tage
erneuert werden — siehe unten.

---

## Zugang

Der Token kommt aus `scripts/meta-ads/.env`, Variable `META_ACCESS_TOKEN`
(gitignored). **Im Skript steht kein Schlüssel.** Fehlt der Token, bricht es
mit einem Hinweis ab statt weiterzulaufen.

Benötigte Berechtigungen am Token:

```
instagram_basic
instagram_manage_insights
pages_show_list
pages_read_engagement
```

Dazu die bestehenden `ads_management`, `ads_read`, `business_management` —
die müssen beim Erzeugen eines neuen Tokens **mitangehakt** werden, sonst
stehen die Werbeanzeigen-Skripte still.

### Token erneuern (alle 60 Tage)

1. [Graph API Explorer](https://developers.facebook.com/tools/explorer/984115153982698/) öffnen
2. Alle sieben Berechtigungen anhaken → **Generate Access Token**
3. Im Dialog **alle Seiten und alle Instagram-Konten** auswählen
4. Token in `scripts/meta-ads/.env` bei `META_ACCESS_TOKEN=` eintragen
5. In einen langlebigen tauschen:

```bash
cd scripts/meta-ads && set -a && . ./.env && set +a && \
curl -s "https://graph.facebook.com/v21.0/oauth/access_token?grant_type=fb_exchange_token&client_id=${META_APP_ID}&client_secret=${META_APP_SECRET}&fb_exchange_token=${META_ACCESS_TOKEN}"
```

Den zurückgegebenen Token wieder in die `.env` schreiben. Laufzeit prüfen geht
über `debug_token`.

---

## Zwei Stolpersteine, die beim Einrichten Zeit gekostet haben

**1. `instagram_business_account` kommt nur mit dem Seiten-Token.**
Fragt man `me/accounts` mit dem Nutzer-Token ab, ist das Feld leer — auch wenn
die Verknüpfung besteht. Man muss erst den Seiten-Token holen und damit die
Seite erneut abfragen. Das Skript macht das in `konten()` automatisch.

**2. Eine Facebook-Seite trägt genau ein Instagram-Konto.**
Für zwei Profile braucht es zwei Seiten. Vorhanden sind *Patricia Ulmann*
(→ @mumlifebalance_patricia_ulmann) und *Mama.energise*, an der das
doTERRA-Profil @patricia_ulmann noch nicht hängt.

---

## Offen

- **doTERRA-Profil fehlt noch.** Die Seite *Mama.energise* kam im
  Freigabe-Dialog nicht mit, und @patricia_ulmann ist nicht als
  Professional-Account an ihr hinterlegt. Sobald beides steht, holt das
  Skript ohne Änderung auch dieses Konto — es läuft über alle freigegebenen
  Seiten.
- **Notion-Übertrag.** Die Zahlen in die Content-Management-DB schreiben
  (Felder `Ansichten / Reichweite`, `Gefällt mir`, `Gespeichert`,
  `Kommentare`). Dafür muss jeder Beitrag einem Notion-Eintrag zugeordnet
  werden — am ehesten über das Veröffentlichungsdatum.
- **Rückwirkende Follower-Stände** gibt es nicht. Die Lücken in der
  Reichweiten-DB für Februar bis August bleiben leer.
