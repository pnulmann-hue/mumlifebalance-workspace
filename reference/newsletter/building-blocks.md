# Newsletter-Bausteine für mumlifebalance

Alle HTML-Snippets die der Newsletter-Generator flexibel in `{{BODY_HTML}}` einsetzen kann.

## Brand Colors
- `#f4f0e6` Body-Background (leicht heller als brand-creme)
- `#f1ecdd` Creme (Pull-Quote BG, Text hell auf dunkel)
- `#ffffff` Body-BG
- `#0c1c30` Dunkelstblau (Footer, Haupttext)
- `#29556d` Dunkelblau-Teal
- `#12828c` Petrol (Info-Box Akzent)
- `#dc822e` Orange (Badge, Pull-Quote Akzent)
- `#e4f3f4` Helles Petrol (Info-Box BG)

## Schriften
- Überschriften: Georgia serif (bold)
- Pull-Quote: Georgia serif italic
- Body: Arial (line-height 1.85)

---

## Baustein: Absatz (Standard)

```html
<p style="margin:0 0 16px 0;font-family:Arial,sans-serif;font-size:16px;color:#0c1c30;line-height:1.85;">
{{TEXT}}
</p>
```

## Baustein: Fett-Absatz (z.B. Kernbotschaft am Ende)

```html
<p style="margin:0;font-family:Arial,sans-serif;font-size:16px;color:#0c1c30;line-height:1.85;">
<strong>{{TEXT}}</strong>
</p>
```

## Baustein: Pull Quote (emotional, mit Orange-Akzent)

```html
<table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:28px 0;">
  <tbody>
    <tr>
      <td style="background-color:#f1ecdd;border-left:4px solid #dc822e;border-radius:0 12px 12px 0;padding:20px 24px;">
        <p style="margin:0;font-family:Georgia,serif;font-style:italic;font-size:20px;color:#0c1c30;line-height:1.6;">
        "{{ZITAT}}"
        </p>
      </td>
    </tr>
  </tbody>
</table>
```

## Baustein: Info-Box (mit Label + Petrol-Akzent)

```html
<table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:28px 0;">
  <tbody>
    <tr>
      <td style="background-color:#e4f3f4;border-left:4px solid #12828c;border-radius:0 12px 12px 0;padding:20px 24px;">
        <p style="margin:0 0 8px 0;font-family:Arial,sans-serif;font-size:11px;font-weight:bold;color:#12828c;text-transform:uppercase;letter-spacing:2px;">{{LABEL}}</p>
        <p style="margin:0;font-family:Arial,sans-serif;font-size:15px;color:#0c1c30;line-height:1.7;">
        {{TEXT}}
        </p>
      </td>
    </tr>
  </tbody>
</table>
```

## Baustein: CTA-Button (Monats-Aktion)

```html
<table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:32px 0;">
  <tbody>
    <tr>
      <td align="center">
        <a href="{{LINK}}" style="display:inline-block;background-color:#dc822e;color:#ffffff;font-family:Arial,sans-serif;font-size:16px;font-weight:bold;text-decoration:none;padding:14px 32px;border-radius:30px;letter-spacing:1px;">
        {{CTA_TEXT}}
        </a>
      </td>
    </tr>
  </tbody>
</table>
```

## Baustein: Sektions-Trenner (zwischen Storytelling und Aktionen)

```html
<hr style="border:none;border-top:1px solid #e4dfd0;margin:32px 0;" />
<p style="margin:0 0 16px 0;font-family:Georgia,serif;font-size:20px;font-weight:bold;color:#0c1c30;">
{{SEKTIONSTITEL}}
</p>
```

---

## Newsletter-Struktur (empfohlen)

1. **Preheader** (versteckt, nur in Inbox-Vorschau sichtbar)
2. **Header** (H1-Titel + Subtitle)
3. **Body:**
   - Anrede `Hey %FIRSTNAME%,`
   - Einleitungs-Absatz (Hook)
   - Story-Absätze
   - Pull-Quote (emotionaler Höhepunkt)
   - Weitere Absätze
   - Info-Box (klarer Unterschied/Erkenntnis)
   - Abschluss mit Ausblick
   - Gruss `Bis morgen, Patricia`
   - Kernbotschaft (fett)
4. **Footer**

## Variablen im Template

| Platzhalter | Beispiel | Quelle |
|---|---|---|
| `{{EMAIL_TITLE}}` | "Ich hab alles richtig gemacht..." | Bot generiert |
| `{{PREHEADER}}` | "Das Problem war nicht mein Fleiss..." | Bot generiert |
| `{{H1_TITLE}}` | wie EMAIL_TITLE | Bot generiert |
| `{{SUBTITLE}}` | "Der Moment der alles verändert hat." | Bot generiert |
| `{{BODY_HTML}}` | Zusammengebaut aus Bausteinen | Bot generiert |
| `%FIRSTNAME%` | Vorname der Empfängerin | ActiveCampaign |

## Stil-Regeln (Patricias Voice)

- **Du-Form** durchgängig
- **ß wird zu ss** (Schweizer Schreibweise)
- **Ich-Perspektive** mit persönlichen Storys
- **Konkrete Momente** ("Und dann kam der Moment...")
- **Emotionale Sprache**, aber nicht übertrieben
- **Kurze Sätze** abwechselnd mit längeren
- **Kein Verkaufsdruck** — Geschichte statt Pitch
