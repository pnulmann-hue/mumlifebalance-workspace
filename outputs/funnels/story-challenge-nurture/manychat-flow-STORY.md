---
tags: [funnel, story-challenge]
---

# ManyChat-Flow: Keyword `STORY`

**Funnel:** Story-Challenge (7 Tage) · **Profil:** Mentoring (@mumlifebalance_patricia_ulmann)
**Status:** ✏️ Entwurf vom 23.10.2026. In ManyChat läuft bereits ein Flow (über STORY sind
Eintragungen gekommen), den Text kann die ManyChat-Schnittstelle aber nicht auslesen.
Wenn dein Flow anders lautet, kopier ihn hier hinein, dann ist das die Quelle.

---

## Aufbau

```
Trigger: Kommentar ODER DM ODER Story-Antwort mit „STORY“ (Exact match)
  ↓
1. Öffentliche Antwort auf den Kommentar
  ↓
2. DM mit zwei Knöpfen: Anmeldung (Challenge) · Kundenmaschine
  ↓
3. Erinnerung nach 3 Stunden, wenn nicht geklickt
```

🚨 **Exact match**: „Story“ steht in vielen normalen Kommentaren („tolle Story!“).

---

## 1 · Öffentliche Antwort (ManyChat wechselt zufällig)

```
Schau in deine Nachrichten 📩
```
```
Ist unterwegs, schau in deine DMs 💌
```
```
Hab dir geschrieben 🙌
```

## 2 · DM

```
Hey {{first name}} 📲

Schön, dass du mitmachst! In der Story-Challenge baust du sieben Tage lang Storys, auf die
jemand antwortet, jeden Tag mit einer kleinen Aufgabe aus dem Workbook und mit einer
Telegram-Gruppe, in der wir uns austauschen.

Trag dich hier ein, dann kommt das Workbook direkt in dein Postfach ⬇️
```

- **Knopf 1:** `Zur Story-Challenge 📲` → https://mumlifebalance.ch/story-challenge/
- **Knopf 2:** `Gleich das ganze System 🧲` → https://mumlifebalance.thrivecart.com/instagram-kundenmaschine/
  *(Die Verkaufsseite der Kundenmaschine ist die ThriveCart-Seite, eine eigene unter
  mumlifebalance.ch gibt es nicht. Ohne Gutschein = 333, den 199er-Preis gibt es nur auf der Danke-Seite.)*

## 3 · Erinnerung nach 3 Stunden (nur wenn Knopf 1 nicht geklickt)

```
Kurze Erinnerung: Dein Workbook für die Story-Challenge wartet noch auf dich.
Tag 1 ist deine eigene Geschichte, und die kennst du ja schon 😊
```

- **Knopf:** `Zur Story-Challenge 📲` → https://mumlifebalance.ch/story-challenge/

---

## Was danach passiert

Formular 45 → direkt nach dem Absenden `/danke-story-challenge/` (199er-Angebot
Kundenmaschine, ⚠️ Stand 23.10. noch Entwurf) → Bestätigungsmail → AC-Automation „0€ Story Challenge“ (45),
Mailreise in [[story-challenge-mails]].
