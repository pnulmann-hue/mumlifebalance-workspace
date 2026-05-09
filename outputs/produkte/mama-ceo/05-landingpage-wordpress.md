# Mama-CEO — WordPress-Landing-Page

> **Hosting:** mumlifebalance.ch/mama-ceo · **Slug:** `mama-ceo` · **Stand:** 2026-05-09
> **Brand-Layout:** Creme #f1ecdd · Philosopher (Headlines) · Source Sans 3 (Body) · Schaufenster-Metapher
> **CTA-Button-Ziel:** ThriveCart-Checkout (URL einfügen sobald angelegt: `https://mumlifebalance.thrivecart.com/mama-ceo/`)
> **Architektur:** WordPress = öffentliche Sales-Page (SEO + Brand-Look) · ThriveCart = nur Checkout-Backend
>
> **Deployment:** Patricia ruft `/wp` auf und bittet: „Erstelle die Mama-CEO-Landing-Page als Draft aus `outputs/produkte/mama-ceo/05-landingpage-wordpress.md`." → Skript legt Page mit Status `draft` an, Patricia prüft + publiziert selbst.

---

## SEO-Meta

- **Title:** Mama-CEO · Live-Cohort für Mamas im Network · Start 1. Juni 2026 · Mum Life Balance
- **Meta-Description:** 8 Wochen Live-Cohort. Du baust dein eigenes KI-Team auf — damit du wieder bei den Menschen bist, statt im Backend. Cart-Open 20. Mai 2026.
- **Featured Image:** Foto Patricia am Schreibtisch mit 3 Monitoren (aus `context/Shootingbilder/`)

---

## SEKTION 1 — HERO (Above the Fold · Creme-Hintergrund · 100vh)

```html
<!-- wp:html -->
<section style="background:#f1ecdd; padding:6rem 1.5rem; text-align:center; min-height:90vh; display:flex; flex-direction:column; justify-content:center;">
  <p style="font-family:'Source Sans 3',sans-serif; font-size:1rem; letter-spacing:0.15em; text-transform:uppercase; color:#3a3a3a; margin-bottom:1rem;">
    Live-Cohort · Start 1. Juni 2026 · 15 Plätze
  </p>
  <h1 style="font-family:'Philosopher',serif; font-size:clamp(2.5rem, 6vw, 4.5rem); font-weight:700; color:#1a1a1a; line-height:1.15; max-width:900px; margin:0 auto 1.5rem;">
    Mama-CEO.<br>
    In 8 Wochen vom „Ich tu alles selbst" zum<br>
    <em style="font-style:italic; color:#2a4d4a;">„Mein KI-Team baut, ich entscheide."</em>
  </h1>
  <p style="font-family:'Source Sans 3',sans-serif; font-size:1.25rem; color:#3a3a3a; max-width:700px; margin:0 auto 2.5rem; line-height:1.6;">
    Du bist nicht Anfängerin. Du bist seit 1, 2, 3 Jahren im Network. Aber du hast keine Zeit mehr, dein Business überhaupt zu führen. Genau dafür ist Mama-CEO.
  </p>
  <a href="https://mumlifebalance.thrivecart.com/mama-ceo/" style="display:inline-block; background:#1a1a1a; color:#f1ecdd; padding:1.25rem 2.5rem; font-family:'Source Sans 3',sans-serif; font-size:1.15rem; font-weight:600; text-decoration:none; border-radius:4px; letter-spacing:0.05em;">
    🔥 Early Bird 249 CHF sichern (nur 72h)
  </a>
  <p style="font-family:'Source Sans 3',sans-serif; font-size:0.95rem; color:#5a5a5a; margin-top:1.5rem;">
    🇨🇭 Schweiz · 👩‍👧‍👦 4-fach-Mama · 🤖 13 KI-Assistenten · 18h-Wochenarbeit · Kein Monat ohne Verkauf seit Mai 2025
  </p>
</section>
<!-- /wp:html -->
```

---

## SEKTION 2 — DAS PROBLEM (Weiss-Hintergrund · Pain-Stack)

```html
<!-- wp:html -->
<section style="background:#ffffff; padding:5rem 1.5rem;">
  <div style="max-width:800px; margin:0 auto;">
    <h2 style="font-family:'Philosopher',serif; font-size:clamp(2rem, 4vw, 3rem); color:#1a1a1a; text-align:center; margin-bottom:2rem;">
      Du erkennst dich gerade wieder.
    </h2>
    <blockquote style="font-family:'Philosopher',serif; font-style:italic; font-size:1.5rem; color:#2a4d4a; border-left:4px solid #2a4d4a; padding-left:1.5rem; margin:2rem 0;">
      „Wie finde ich Kunden?"<br>
      „Wo soll ich überhaupt anfangen?"<br>
      „Was poste ich jetzt?"
    </blockquote>
    <p style="font-family:'Source Sans 3',sans-serif; font-size:1.1rem; line-height:1.8; color:#2a2a2a;">
      Diese drei Fragen kriege ich jeden Tag in die DMs. Von Mamas im Network, die seit einer Weile dabei sind. Frustriert. Viele Follower. Null Anfragen.<br><br>
      <strong>Und dazu der ehrliche Hintergrund, den niemand schreibt:</strong>
    </p>
    <ul style="font-family:'Source Sans 3',sans-serif; font-size:1.1rem; line-height:2; color:#2a2a2a; margin:1.5rem 0; padding-left:1.5rem;">
      <li>Du arbeitest noch 60–80% in deinem alten Job. Das frisst dich auf.</li>
      <li>Dein Mann schaut dein Business als Hobby an. Als „Instagram-Ding".</li>
      <li>Du machst alles selbst. Posten. Antworten. Strategie. Reels. Bis es 22 Uhr ist und du nicht weisst, was du heute „erreicht" hast.</li>
      <li>Du sagst dir: <em>„Diesen Monat können wir nicht auswärts essen."</em> Und etwas in dir fragt: <em>„Oh shit, wie viel hab ich noch auf dem Konto?"</em></li>
    </ul>
    <p style="font-family:'Source Sans 3',sans-serif; font-size:1.25rem; line-height:1.7; color:#1a1a1a; text-align:center; margin-top:2.5rem; font-weight:600;">
      Du bist nicht faul. Du hast nur ein <em style="color:#2a4d4a;">System-Problem</em>.<br>Das ist der Unterschied.
    </p>
  </div>
</section>
<!-- /wp:html -->
```

---

## SEKTION 3 — REFRAME & STORY (Creme-Hintergrund · Patricia-Stimme)

```html
<!-- wp:html -->
<section style="background:#f1ecdd; padding:5rem 1.5rem;">
  <div style="max-width:800px; margin:0 auto;">
    <h2 style="font-family:'Philosopher',serif; font-size:clamp(2rem, 4vw, 3rem); color:#1a1a1a; margin-bottom:2rem;">
      Jetzt mal ganz ehrlich:
    </h2>
    <p style="font-family:'Source Sans 3',sans-serif; font-size:1.15rem; line-height:1.8; color:#2a2a2a;">
      <strong>Mental Load ist kein persönliches Versagen.</strong> Du bist nicht „nicht diszipliniert genug". Du hast einfach kein System gebaut. Genau wie 95% der Mamas im Network.<br><br>
      Niemand hat es dir gezeigt, weil die meisten Mentorinnen, die du auf Instagram siehst, <strong>kein eigenes Backend haben</strong>. Sie haben ein Team. Au-Pairs. VAs. Geld für Personal.<br><br>
      <strong>Ich nicht.</strong> Kein Au-Pair, keine Putzfrau, keine VA. Mein Mann arbeitet 80% auswärts. 4 Kinder. 18 Stunden pro Woche fürs Business. Mehr nicht.<br><br>
      Und trotzdem: <strong>Kein Monat ohne Verkauf seit Mai 2025.</strong> Vierstellig pro Monat aus Mentoring. Vierstellig aus doTERRA.
    </p>
    <p style="font-family:'Philosopher',serif; font-style:italic; font-size:1.5rem; color:#2a4d4a; text-align:center; margin:3rem 0;">
      „Mein Erfolg ist nicht Bali. Mein Erfolg ist eine Alp."
    </p>
    <p style="font-family:'Source Sans 3',sans-serif; font-size:1.1rem; line-height:1.8; color:#2a2a2a;">
      Wie ich dahin gekommen bin: ich hab aufgehört, manuell zu arbeiten. Hab angefangen, mir KI-Mitarbeiter zu bauen. Erst einen. Dann fünf. Heute 13 Slash-Commands + 3 Telegram-Bots + 3 Kunden-Bots. Solo gebaut, ohne Tech-Hintergrund.<br><br>
      <strong>Genau das baue ich mit dir. In 8 Wochen.</strong>
    </p>
  </div>
</section>
<!-- /wp:html -->
```

---

## SEKTION 4 — DIE 4 MODULE + 1 BONUS (Weiss-Hintergrund · 4-Spalten-Grid auf Desktop, 1-Spalte mobil)

```html
<!-- wp:html -->
<section style="background:#ffffff; padding:5rem 1.5rem;">
  <div style="max-width:1100px; margin:0 auto;">
    <h2 style="font-family:'Philosopher',serif; font-size:clamp(2rem, 4vw, 3rem); color:#1a1a1a; text-align:center; margin-bottom:1rem;">
      Was du in 8 Wochen aufbaust
    </h2>
    <p style="font-family:'Source Sans 3',sans-serif; font-size:1.1rem; color:#5a5a5a; text-align:center; margin-bottom:3rem;">
      4 Hauptmodule + 1 Bonus-Modul · 23 Lektionen · 4 Live-Calls · Telegram-Community
    </p>
    <div style="display:grid; grid-template-columns:repeat(auto-fit,minmax(240px,1fr)); gap:2rem;">

      <div style="background:#f1ecdd; padding:2rem; border-radius:8px;">
        <p style="font-family:'Philosopher',serif; font-size:1.1rem; color:#2a4d4a; margin-bottom:0.5rem;">Modul 1 · Wo. 1–2</p>
        <h3 style="font-family:'Philosopher',serif; font-size:1.5rem; color:#1a1a1a; margin-bottom:1rem;">Mindset-Reset für Mama-CEO</h3>
        <p style="font-family:'Source Sans 3',sans-serif; font-size:1rem; line-height:1.6; color:#2a2a2a;">Du kennst deine 5 CEO-Aufgaben — alles andere wird delegiert oder automatisiert. Wochenrhythmus, der zu deinem Mama-Alltag passt.</p>
        <p style="font-family:'Source Sans 3',sans-serif; font-size:0.9rem; color:#5a5a5a; margin-top:1rem;">+ Live-Call 1: Hot-Seat Wochenrhythmus (90 Min)</p>
      </div>

      <div style="background:#f1ecdd; padding:2rem; border-radius:8px;">
        <p style="font-family:'Philosopher',serif; font-size:1.1rem; color:#2a4d4a; margin-bottom:0.5rem;">Modul 2 · Wo. 3–4</p>
        <h3 style="font-family:'Philosopher',serif; font-size:1.5rem; color:#1a1a1a; margin-bottom:1rem;">Dein KI-System: Architektur</h3>
        <p style="font-family:'Source Sans 3',sans-serif; font-size:1rem; line-height:1.6; color:#2a2a2a;">Notion als dein Business-Brain. Erster KI-Mitarbeiter ist live. Du briefst KI wie ein Team-Mitglied — nicht wie ein Tool.</p>
        <p style="font-family:'Source Sans 3',sans-serif; font-size:0.9rem; color:#5a5a5a; margin-top:1rem;">+ Live-Call 2: Q&A „KI-Architektur" (60 Min)</p>
      </div>

      <div style="background:#f1ecdd; padding:2rem; border-radius:8px;">
        <p style="font-family:'Philosopher',serif; font-size:1.1rem; color:#2a4d4a; margin-bottom:0.5rem;">Modul 3 · Wo. 5–6</p>
        <h3 style="font-family:'Philosopher',serif; font-size:1.5rem; color:#1a1a1a; margin-bottom:1rem;">Akquise-KI: DMs auf Autopilot</h3>
        <p style="font-family:'Source Sans 3',sans-serif; font-size:1rem; line-height:1.6; color:#2a2a2a;">Dein Funnel läuft: Keyword → Bot → Mail-Sequenz → Verkauf. ManyChat + ActiveCampaign + Blotato. End-to-End live getestet.</p>
        <p style="font-family:'Source Sans 3',sans-serif; font-size:0.9rem; color:#5a5a5a; margin-top:1rem;">+ Live-Call 3: Werkstatt Funnel-Bau (120 Min)</p>
      </div>

      <div style="background:#f1ecdd; padding:2rem; border-radius:8px;">
        <p style="font-family:'Philosopher',serif; font-size:1.1rem; color:#2a4d4a; margin-bottom:0.5rem;">Modul 4 · Wo. 7–8</p>
        <h3 style="font-family:'Philosopher',serif; font-size:1.5rem; color:#1a1a1a; margin-bottom:1rem;">Service-KI: Skalierung ohne Burn-out</h3>
        <p style="font-family:'Source Sans 3',sans-serif; font-size:1rem; line-height:1.6; color:#2a2a2a;">FAQ-Bot, Onboarding-Flow, E-Mail-Assistent. Deine Kundinnen werden begleitet — auch wenn du nicht in der Inbox bist.</p>
        <p style="font-family:'Source Sans 3',sans-serif; font-size:0.9rem; color:#5a5a5a; margin-top:1rem;">+ Live-Call 4: Hot-Seat Kundinnen-Reise (90 Min)</p>
      </div>

    </div>
    <div style="background:#2a4d4a; padding:2rem; border-radius:8px; margin-top:2rem; color:#f1ecdd;">
      <p style="font-family:'Philosopher',serif; font-size:1.1rem; margin-bottom:0.5rem;">🎁 Bonus-Modul · jederzeit zugänglich</p>
      <h3 style="font-family:'Philosopher',serif; font-size:1.5rem; margin-bottom:1rem;">Content-KI Quick-Setup</h3>
      <p style="font-family:'Source Sans 3',sans-serif; font-size:1rem; line-height:1.6;">Hook-Bot + Karussell-Bot + Content-Wochen-Bot. Content-Wochenpipeline in 30 Min — wenn du schon weisst, WAS du sagen willst.</p>
    </div>
  </div>
</section>
<!-- /wp:html -->
```

---

## SEKTION 5 — BONUS-PACK (Creme-Hintergrund · Tabelle)

```html
<!-- wp:html -->
<section style="background:#f1ecdd; padding:5rem 1.5rem;">
  <div style="max-width:800px; margin:0 auto;">
    <h2 style="font-family:'Philosopher',serif; font-size:clamp(2rem, 4vw, 3rem); color:#1a1a1a; text-align:center; margin-bottom:1rem;">
      Dein Bonus-Pack
    </h2>
    <p style="font-family:'Source Sans 3',sans-serif; font-size:1.15rem; color:#2a4d4a; text-align:center; margin-bottom:2.5rem;">
      <strong>692 CHF Wert · im Preis enthalten</strong>
    </p>
    <ul style="list-style:none; padding:0; font-family:'Source Sans 3',sans-serif; font-size:1.1rem; line-height:2.2; color:#2a2a2a;">
      <li>🎁 <strong>Notion-Master-Template für Mama-CEOs</strong> · 99 CHF</li>
      <li>🎁 <strong>ManyChat-Template-Pack</strong> (3 fertige Funnel-Vorlagen) · 79 CHF</li>
      <li>🎁 <strong>Q&A-Custom-GPT-Vorlage + 5-Mail-Onboarding-Sequenz</strong> · 59 CHF</li>
      <li>🎁 <strong>Hook-Bot + Karussell-Bot Custom-GPT-Vorlagen</strong> · 59 CHF</li>
      <li>🎁 <strong>8 Wochen Telegram-Community-Zugang</strong> · unbezahlbar</li>
      <li>🎁 <strong>4 Live-Calls</strong> (2× Hot-Seat + 1× Q&A + 1× Werkstatt) · 396 CHF</li>
    </ul>
  </div>
</section>
<!-- /wp:html -->
```

---

## SEKTION 6 — FÜR WEN / FÜR WEN NICHT (Weiss · 2-Spalten)

```html
<!-- wp:html -->
<section style="background:#ffffff; padding:5rem 1.5rem;">
  <div style="max-width:1000px; margin:0 auto;">
    <h2 style="font-family:'Philosopher',serif; font-size:clamp(2rem, 4vw, 3rem); color:#1a1a1a; text-align:center; margin-bottom:3rem;">
      Ist Mama-CEO für dich?
    </h2>
    <div style="display:grid; grid-template-columns:repeat(auto-fit,minmax(300px,1fr)); gap:2rem;">

      <div style="background:#f1ecdd; padding:2rem; border-radius:8px;">
        <h3 style="font-family:'Philosopher',serif; font-size:1.5rem; color:#2a4d4a; margin-bottom:1rem;">✅ JA, wenn …</h3>
        <ul style="font-family:'Source Sans 3',sans-serif; font-size:1rem; line-height:1.8; color:#2a2a2a; padding-left:1.2rem;">
          <li>Du seit mind. 6 Monaten im Network bist und schon erste Kundinnen hast — aber nicht durchbrichst.</li>
          <li>Du dein Thema schon weisst (zumindest grob).</li>
          <li>Du bereit bist, in 8 Wochen aktiv mitzubauen.</li>
          <li>Du Notion + KI einsetzen willst, auch wenn du gerade nicht weisst wie.</li>
          <li>Du ehrlich zu dir bist: dein Backend ist Chaos und genau das hält dich auf.</li>
        </ul>
      </div>

      <div style="background:#fef5f0; padding:2rem; border-radius:8px;">
        <h3 style="font-family:'Philosopher',serif; font-size:1.5rem; color:#a85a3a; margin-bottom:1rem;">❌ NEIN, wenn …</h3>
        <ul style="font-family:'Source Sans 3',sans-serif; font-size:1rem; line-height:1.8; color:#2a2a2a; padding-left:1.2rem;">
          <li>Du noch nicht weisst, was du anbietest. → <a href="https://mumlifebalance.ch/instagram-kundenmaschine" style="color:#2a4d4a;">Insta-Kundenmaschine</a> zuerst.</li>
          <li>Du sofort 6-stellig verdienen willst.</li>
          <li>Du erwartest, dass ich dein Business für dich baue.</li>
          <li>Du Tech-Verweigerin bist und „eigentlich nichts Digitales" willst.</li>
          <li>Du seit 5 Jahren Kurse buchst und nichts umsetzt.</li>
        </ul>
      </div>

    </div>
  </div>
</section>
<!-- /wp:html -->
```

---

## SEKTION 7 — PREIS & URGENCY (Creme · Zentral · Pricing-Box)

```html
<!-- wp:html -->
<section style="background:#f1ecdd; padding:5rem 1.5rem;">
  <div style="max-width:700px; margin:0 auto; text-align:center;">
    <h2 style="font-family:'Philosopher',serif; font-size:clamp(2rem, 4vw, 3rem); color:#1a1a1a; margin-bottom:1.5rem;">
      Pilot-Preis · nur erste Cohort
    </h2>
    <p style="font-family:'Source Sans 3',sans-serif; font-size:1.1rem; line-height:1.7; color:#2a2a2a; margin-bottom:2.5rem;">
      Du zahlst jetzt den Pilot-Preis, weil ich's noch nicht 5× geteacht hab. Beim 2. Mal weiss ich, wo's klemmt. Dann kostet es 444 CHF. Das hier ist die Mit-Bauerinnen-Cohort.
    </p>

    <div style="background:#ffffff; padding:2.5rem; border-radius:12px; margin-bottom:2rem;">
      <p style="font-family:'Source Sans 3',sans-serif; font-size:0.95rem; letter-spacing:0.1em; text-transform:uppercase; color:#a85a3a; margin-bottom:0.5rem;">🔥 Early Bird · 72 Stunden</p>
      <p style="font-family:'Philosopher',serif; font-size:3rem; color:#1a1a1a; font-weight:700; margin:0.5rem 0;">249 CHF</p>
      <p style="font-family:'Source Sans 3',sans-serif; font-size:1rem; color:#5a5a5a;">20.5. 09:00 — 22.5. 23:59</p>
    </div>

    <div style="background:#ffffff; padding:2.5rem; border-radius:12px; margin-bottom:2.5rem; opacity:0.85;">
      <p style="font-family:'Source Sans 3',sans-serif; font-size:0.95rem; letter-spacing:0.1em; text-transform:uppercase; color:#5a5a5a; margin-bottom:0.5rem;">Final Pilot-Preis</p>
      <p style="font-family:'Philosopher',serif; font-size:2.5rem; color:#1a1a1a; font-weight:700; margin:0.5rem 0;">333 CHF</p>
      <p style="font-family:'Source Sans 3',sans-serif; font-size:1rem; color:#5a5a5a;">23.5. 00:00 — 31.5. 23:59 (Cart-Close)</p>
    </div>

    <p style="font-family:'Source Sans 3',sans-serif; font-size:1.1rem; color:#2a2a2a; margin-bottom:2rem;">
      <strong>Cohort-Start:</strong> 1. Juni 2026<br>
      <strong>Plätze:</strong> 15 (strikt limitiert wegen Hot-Seat-Live-Calls)<br>
      <strong>Runde 2 (Herbst 2026):</strong> 444 CHF
    </p>

    <a href="https://mumlifebalance.thrivecart.com/mama-ceo/" style="display:inline-block; background:#1a1a1a; color:#f1ecdd; padding:1.5rem 3rem; font-family:'Source Sans 3',sans-serif; font-size:1.2rem; font-weight:600; text-decoration:none; border-radius:4px; letter-spacing:0.05em;">
      Platz sichern →
    </a>
  </div>
</section>
<!-- /wp:html -->
```

---

## SEKTION 8 — FAQ (Weiss · Accordion mit Gutenberg-Details-Block)

```html
<!-- wp:html -->
<section style="background:#ffffff; padding:5rem 1.5rem;">
  <div style="max-width:800px; margin:0 auto;">
    <h2 style="font-family:'Philosopher',serif; font-size:clamp(2rem, 4vw, 3rem); color:#1a1a1a; text-align:center; margin-bottom:3rem;">
      Häufige Fragen
    </h2>

    <details style="font-family:'Source Sans 3',sans-serif; border-bottom:1px solid #d0d0d0; padding:1.5rem 0;">
      <summary style="font-size:1.15rem; font-weight:600; cursor:pointer; color:#1a1a1a;">Ich hab keine Zeit für noch einen Kurs.</summary>
      <p style="margin-top:1rem; font-size:1.05rem; line-height:1.7; color:#2a2a2a;">Genau deshalb baust du Mama-CEO. Du brauchst NICHT „mehr Zeit fürs Lernen" — du brauchst „weniger Zeit fürs Tun". Modul 1 zeigt dir den Wochenrhythmus, der ab Tag 1 für dich arbeitet. Lektionen sind in 8–28 Min portioniert. Hör es beim Spazieren, beim Bügeln, beim Auto-Fahren.</p>
    </details>

    <details style="font-family:'Source Sans 3',sans-serif; border-bottom:1px solid #d0d0d0; padding:1.5rem 0;">
      <summary style="font-size:1.15rem; font-weight:600; cursor:pointer; color:#1a1a1a;">Ich bin nicht techie.</summary>
      <p style="margin-top:1rem; font-size:1.05rem; line-height:1.7; color:#2a2a2a;">Ich war auch nicht techie. Bis Mai 2025 wusste ich nicht, was ein Custom GPT ist. Heute hab ich 13 Slash-Commands. Das Programm ist genau für Mamas, die NICHT techie sind. Schritt für Schritt. Mit Vorlagen. Mit Hot-Seats, wenn es klemmt.</p>
    </details>

    <details style="font-family:'Source Sans 3',sans-serif; border-bottom:1px solid #d0d0d0; padding:1.5rem 0;">
      <summary style="font-size:1.15rem; font-weight:600; cursor:pointer; color:#1a1a1a;">Ist das nicht das Gleiche wie deine Insta-Kundenmaschine?</summary>
      <p style="margin-top:1rem; font-size:1.05rem; line-height:1.7; color:#2a2a2a;">Nein. Insta-Kundenmaschine lehrt dich <strong>WAS</strong> du sagst (Thema, Positionierung, Reels, Captions). Mama-CEO lehrt dich <strong>WIE</strong> du es tust ohne dich zu zerreissen (KI, Notion, Wochenrhythmus, Automation). Wer noch nicht weiss WAS sie verkauft → Insta-Kundenmaschine zuerst. Wer's weiss aber keine Zeit hat → Mama-CEO.</p>
    </details>

    <details style="font-family:'Source Sans 3',sans-serif; border-bottom:1px solid #d0d0d0; padding:1.5rem 0;">
      <summary style="font-size:1.15rem; font-weight:600; cursor:pointer; color:#1a1a1a;">Was, wenn ich mich nicht zu den Live-Calls schalten kann?</summary>
      <p style="margin-top:1rem; font-size:1.05rem; line-height:1.7; color:#2a2a2a;">Aufzeichnungen kommen alle ins Telegram. Hot-Seat-Fragen kannst du vorab schicken — ich nehme sie für dich auf. Aber: Live ist Live. Wenn du kannst, komm.</p>
    </details>

    <details style="font-family:'Source Sans 3',sans-serif; border-bottom:1px solid #d0d0d0; padding:1.5rem 0;">
      <summary style="font-size:1.15rem; font-weight:600; cursor:pointer; color:#1a1a1a;">Was, wenn es bei mir nicht funktioniert?</summary>
      <p style="margin-top:1rem; font-size:1.05rem; line-height:1.7; color:#2a2a2a;">Ehrlich: wenn du nicht implementierst, funktioniert nichts. Mama-CEO ist für Frauen, die TUN. Wenn du in den 8 Wochen die Mastery-Lektionen machst, an den Live-Calls teilnimmst und in der Telegram-Gruppe aktiv bist — dann hast du das System. Wenn du konsumierst, hast du nichts. <strong>Es liegt an dir. 100%.</strong></p>
    </details>

  </div>
</section>
<!-- /wp:html -->
```

---

## SEKTION 9 — FINAL-CTA & P.S. (Dunkel · Final-Push)

```html
<!-- wp:html -->
<section style="background:#1a1a1a; color:#f1ecdd; padding:5rem 1.5rem; text-align:center;">
  <div style="max-width:700px; margin:0 auto;">
    <h2 style="font-family:'Philosopher',serif; font-size:clamp(2rem, 4vw, 3rem); margin-bottom:2rem;">
      Plätze sichern.
    </h2>
    <p style="font-family:'Source Sans 3',sans-serif; font-size:1.15rem; line-height:1.8; margin-bottom:2.5rem;">
      Die erste Runde startet am 1. Juni. Cart öffnet am 20. Mai um 09:00 Uhr. Early Bird läuft 72 Stunden.<br><br>
      Wenn du das hier zu Ende gelesen hast — <strong>du bist die richtige Frau für diese Cohort.</strong>
    </p>
    <a href="https://mumlifebalance.thrivecart.com/mama-ceo/" style="display:inline-block; background:#f1ecdd; color:#1a1a1a; padding:1.5rem 3rem; font-family:'Source Sans 3',sans-serif; font-size:1.2rem; font-weight:600; text-decoration:none; border-radius:4px; letter-spacing:0.05em;">
      Komm rein →
    </a>
    <p style="font-family:'Philosopher',serif; font-style:italic; font-size:1.3rem; color:#f1ecdd; margin-top:3rem;">
      „Funktionieren war gestern."<br>
      <span style="font-size:1rem; opacity:0.7;">— Patricia</span>
    </p>
  </div>
</section>
<!-- /wp:html -->
```

---

## DEPLOYMENT-ANWEISUNG (für `/wp`-Skill)

```
Erstelle WordPress-Page:
- Slug: mama-ceo
- Title: Mama-CEO · Live-Cohort für Mamas im Network
- Status: draft
- Content: Inhalt aus 05-landingpage-wordpress.md (alle 9 Sektionen, in Reihenfolge)
- Featured Image: aus context/Shootingbilder/ (Patricia am Schreibtisch, 3 Monitore — falls vorhanden)
- SEO-Meta: Title + Description (siehe oben)
- Patricia prüft + publiziert selbst (Brand-Memory-Regel)
```

**Brand-Farben verwendet:**
- Creme #f1ecdd (Hintergrund)
- Dunkelgrau #1a1a1a (Headlines + Final-CTA)
- Petrol #2a4d4a (Akzent + „Mein Erfolg ist nicht Bali"-Zitat)
- Source Sans 3 + Philosopher (mumlifebalance.ch-Standard)

**Compliance-Check:**
- ✅ Keine Mentor-Namen
- ✅ Keine doTERRA-Heilversprechen
- ✅ Keine erfundenen Zahlen
- ✅ Brand-Manifest-Filter bestanden
- ✅ Patricia-Wortschatz an Schlüsselstellen
- ✅ Repel-Markt-Filter klar
- ✅ Cross-Sell-Brücke zur Insta-Kundenmaschine in Sektion 6
