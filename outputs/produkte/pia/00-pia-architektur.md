---
tags: [produkt, pia, mba, intern]
---

# PIA — Architektur & erstes Modul

**Erstellt:** 2026-06-08 · **Was das ist:** Wie alle Wissens-Layer in PIAs Hirn zusammenkommen + das Tag-1-Modul (Bio/Positionierung) als erster Baustein. Das ist die Vorlage, aus der der Code (Next.js + Supabase + Claude) entsteht.

---

## 1. PIAs Hirn — die Schichtung (System-Prompt-Stack)

Jede PIA-Generierung bekommt diese Layer in den System-Prompt (in dieser Priorität):

```
1. 🟦 PATRICIA-WISSEN (Hauptteil, ihre Stimme)
   patricia-vollprofil.md · brand-voice.md · hook-framework.md ·
   content-formel-5-typen.md · content-radar-*.md · reichweiten-formel-*.md ·
   caption-formeln.md · reels-/karussell-framework.md · job-saeulen.md ·
   Bio-Check-Logik · 3 Kurse (IG-Kundenmaschine/Mama-CEO/Digitale Produktwelt)
2. 🟪 JULIA-METHODIK (Strategie, NUR intern — nie namentlich im Output)
   reference/julia-trost/methodik.md + Funnel/Salespage/Launch/E-Mail
3. 🟧 NETWORK-LAYER
   context/network-wissensbasis.md (Go Pro + Unbox, destilliert + gefiltert)
4. 🛡️ FILTER (über allem, nicht verhandelbar)
   keine Stakkato · keine erfundenen Zahlen · keine Einkommens-Claims ·
   doTERRA keine Heilversprechen · Schweizer ss/Umlaute · DU-Anrede ·
   kein „Julia"-Name + keine Autoren-Namen im Kunden-Output ·
   Mentee-Output klingt nach der MENTEE, nicht nach Patricia/ChatGPT
```

→ + das **Mentee-Profil** (ihre Onboarding-Antworten aus Supabase) = personalisierte Ausgabe.

---

## 2. Datenmodell (Supabase) — sauberes Speichern + Zugangs-Steuerung

```
mentees
  id · email (Schlüssel) · name · telegram_id (optional)
  tier            ('bootcamp' | 'mba' | 'abgelaufen')
  access_until    (Datum; bootcamp → 2026-07-06)
  created_at

mentee_profile         (1 pro Mentee — die Onboarding-Antworten, strukturiert)
  mentee_id · network_firma · thema · zielgruppe · status · lebensrealitaet ·
  story_rohmaterial · updated_at

mentee_library         (die „Bibliotheken" — pro Output 1 Zeile)
  id · mentee_id · modul ('bio'|'hooks'|'leadmagnet'|'funnel'|'roter-faden')
  titel · inhalt (jsonb) · created_at
```

- **Pro Schritt speichern**, strukturiert, mit Bestätigung zurück → Bibliothek wächst sichtbar.
- **Zugang:** App prüft bei jedem Aufruf `tier` + `access_until`. ThriveCart-Kauf-Webhook (setzt Tag `mba-kauf` 79) flippt `tier='mba'` per E-Mail-Match. Abgelaufen → Upgrade-Screen, Bibliothek bleibt sichtbar (Verlust-Aversion).

---

## 3. Tag-1-Modul: Bio / Positionierung (erster Baustein)

**PIA-Persona-Intro:** „Hi, ich bin PIA 👋 Lass uns in ein paar Minuten dein Thema so klar kriegen, dass fremde Frauen dich anschreiben. Ich frag dich was — du antwortest, ich bau."

**Onboarding (5 Fragen, mit Rückfrage-Logik):**
1. In welchem Network bist du (Firma) — oder baust du was Eigenes?
2. Worum geht's bei dir — dein Thema / deine Transformation in 1-2 Sätzen?
3. Für wen — wen willst du erreichen?
4. Wo stehst du — ganz am Anfang / ein paar Followerinnen / läuft schon was?
5. Deine Lebensrealität — wie viele Kinder, wie viel Zeit wirklich?

**Rückfrage-Logik (Qualitäts-Gate):** Ist eine Antwort zu dünn/„weiss nicht"/off-topic → PIA generiert NICHT, sondern stellt **eine** warme, konkrete Rückfrage mit Beispiel (siehe Network-Layer: Story-Coaching). „weiss nicht" → wird zum Mini-Coaching. Entmutigt → Empathie in Patricia-Voice. Erst ab genug Signal wird generiert.

**Output (in Mentee-Voice, gespeichert in `mentee_library`):**
- 1 **Bio-Vorschlag** (Experten-Satz + wofür sie steht + für wen) nach Bio-Check-Logik
- 2-3 **Positionierungs-Varianten** zur Auswahl
- 1 kurzer **„Warum das zieht"** (mit Network-Story-Layer aus Beck)

→ Quick Win: sie kann ihre IG-Bio sofort updaten = screenshot-bar.

---

## 4. Tech & Wo (wie ARIA)

- **Code:** neues Next.js-Repo `pia` (lokal `C:\Users\pnulm\pia`, GitHub `pnulmann-hue/pia`)
- **Hosting:** Vercel · **URL:** `pia.mumlifebalance.ch` (übergangsweise `…vercel.app`)
- **Daten:** Supabase · **Hirn:** Claude API
- **UI-Beschleuniger:** v0/Lovable für den ARIA-Look

---

## 5. Build-Reihenfolge

1. Repo + Supabase-Schema (oben) + Auth (E-Mail-Login)
2. **Tag-1-Modul Bio** end-to-end (Onboarding → Rückfrage → Generierung → Bibliothek) ← erster klickbarer Screen
3. Tag-2 Hooks · dann 3-5
4. Zugangs-Logik + ThriveCart-Webhook
5. Bootcamp-Polish + Testrunde

---

## Was ich von dir brauche, um den Code zu starten
- **Supabase:** neues Projekt für PIA — oder das Kochbot-Projekt mitnutzen? (Empfehlung: eigenes PIA-Projekt, sauber getrennt)
- **Anthropic-Key** (hast du) · **DNS-Subdomain** kommt später
- **Go** für „Repo anlegen + Tag-1-Bio bauen"

## 🔗 Verwandte Notizen
- [[../../../context/network-wissensbasis|Network-Wissensbasis]]
- [[../../../reference/aria-tool-mentee-konzept|PIA-Konzept]]
- [[../mba-launch/challenge-launch-plan|Bootcamp-Bauplan]]
