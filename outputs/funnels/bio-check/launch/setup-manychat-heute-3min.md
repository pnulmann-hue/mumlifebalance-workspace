# 🚀 ManyChat-Setup `BIO` — 3-Minuten-Version

**Ziel:** Keyword `BIO` auf Instagram Mentoring-Profil scharf schalten → bei jeder DM/jedem Kommentar mit `BIO` geht automatisch DM mit Link zu deiner Homepage raus.

**Landing-URL (die in der DM drin steht):**
```
https://mumlifebalance.ch/bio-check?utm_source=instagram&utm_medium=manychat&utm_campaign=bio-check-launch&utm_content=dm-keyword-bio
```

---

## Schritt 1 — DM-Flow bauen (90 Sek)

1. ManyChat Dashboard öffnen → dein **Mentoring-Account** auswählen (oben rechts)
2. Links Sidebar → **Automation** → **Flows**
3. Button oben rechts: **+ New Flow**
4. Name: `Bio-Check DM-Auslieferung`
5. Channel: **Instagram**
6. Im Canvas: Starter-Block ist da. Rechts daneben klicken → **+ Add Step** → **Send Message**

**Nachrichten-Block 1 (Begrüssung):**

Textfeld füllen mit (copy-paste):

```
Hey {{first name}}! 🎯

Du willst deine Instagram-Bio einmal richtig durchchecken?
Kurze Fragen beantworten — und raus kommt:

✓ Dein Experten-Satz (3 Varianten)
✓ 5 fertige Bio-Vorschläge (copy-paste-ready)
✓ 3 Ideen für deine Pinned Posts
✓ Alles als PDF per Mail

Dauert ca. 3 Minuten. Kostet 0 CHF.

Hier geht's los ⬇️
```

**Nachrichten-Block 2 (Button zur Homepage):**

Unter dem Text → **+ Add Button** (im selben Message-Block)

- Button-Typ: **URL** (oder „Open Website")
- Button-Text: `Zum Bio-Check 🚀`
- URL (copy-paste):
```
https://mumlifebalance.ch/bio-check?utm_source=instagram&utm_medium=manychat&utm_campaign=bio-check-launch&utm_content=dm-keyword-bio
```

**Action-Block 3 (Tag setzen):**

Rechts vom Message-Block → **+ Add Step** → **Action** → **Add Tag**
- Tag-Name: `bio-check-lead-manychat` (wird beim Eintippen angelegt, falls nicht existiert)

Oben rechts: **Publish** (grüner Button)

---

## Schritt 2 — Keyword-Rule setzen (45 Sek)

1. Links Sidebar → **Automation** → **Keywords**
2. Button oben rechts: **+ New Keyword**
3. Channel: **Instagram**
4. Feld „Keywords" (Komma-getrennt):
```
BIO, bio, Bio
```
5. Match-Type: **Exact Match** (wichtig — sonst triggert es auf „Biografie" etc.)
6. Section **Response** → **Send Flow** → den grad gebauten Flow `Bio-Check DM-Auslieferung` auswählen
7. **Save**

---

## Schritt 3 — Comment-Auto-Reply scharf (45 Sek)

Wenn jemand öffentlich `BIO` unter deinem Reel kommentiert → soll ein kurzer öffentlicher Reply + DM kommen.

1. Links Sidebar → **Automation** → **Growth Tools** (oder: „Instagram Automation → Comments" — je nach ManyChat-Version)
2. **+ New Tool** → **Instagram Comment Auto-Reply**
3. Post wählen: dein **Bio-Check-Launch-Reel von heute** (musst du nach dem Posten auswählen)
4. Trigger-Keyword: `BIO`
5. **Public Reply** (öffentlich, 3 Varianten rotieren lassen):
   - `Hab dir grad geschickt ✨`
   - `Check deine DMs 👀`
   - `Gleich in deinen Nachrichten 💌`
6. **Then send DM** → Flow `Bio-Check DM-Auslieferung` auswählen
7. **Activate**

---

## Schritt 4 — Selber testen (30 Sek)

Bevor du den Reel postest:
1. Öffne Instagram mit einem Zweit-Account (oder bitte eine Freundin)
2. Schreib `BIO` per DM an dein Mentoring-Profil
3. Du solltest in 1–3 Sek die Begrüssung + Button bekommen
4. Button klicken → landet auf `mumlifebalance.ch/bio-check`

Wenn's NICHT klappt:
- Flow-Status prüfen: muss **Published** sein (grün)
- Keyword-Match muss **Exact** sein
- Instagram-Connection in ManyChat prüfen (Settings → Channels → Instagram → ist dort „Connected"?)

---

## ✅ Done-Check nach Setup

Alles fertig wenn:

- [ ] Flow `Bio-Check DM-Auslieferung` existiert und ist **Published**
- [ ] Keyword-Rule `BIO` triggert diesen Flow
- [ ] Tag `bio-check-lead-manychat` existiert (wird beim ersten Trigger automatisch angelegt)
- [ ] Test-DM kommt in < 5 Sekunden an
- [ ] Button-Link geht zu `https://mumlifebalance.ch/bio-check`
- [ ] Comment-Auto-Reply unter dem Launch-Reel aktiviert (nach Reel-Post)

---

## 🤖 Optional: Api-Script für Tag-Check später

Wenn du deinen ManyChat-API-Key hast (ManyChat → Settings → API → Generate Token, **Pro-Plan erforderlich**):

1. Key eintragen in `/home/user/mumlifebalance-workspace/scripts/manychat/.env`:
```
MANYCHAT_API_KEY=dein-echter-key-hier
```

2. Ich kann dann per Script:
- Tag-Counts prüfen (wie viele `bio-check-lead-manychat` bisher)
- Subscriber-Daten taggen (z.B. bei AC-Überführung)
- Flow-Send an bestimmte Subscriber senden

Die **Keyword-Rule + Flow-Logik** bleibt trotzdem im UI — das ist ManyChat-seitig fest.

---

## ⚠️ Warum nicht alles per API

ManyChat hat bewusst entschieden: **Keyword-Setup = UI-only.** Grund laut offizieller Doku: Spam-Schutz + Flow-Builder-Komplexität. Auch Zapier, Make.com etc. können keine Keywords per API anlegen.

Das ist keine Sache, die wir umgehen können — nur akzeptieren. Deshalb: UI-Setup einmal (3 Min), danach läuft's evergreen.
