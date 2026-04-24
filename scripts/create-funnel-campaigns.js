// ActiveCampaign Funnel Campaign Creator
// 1:1 Begleitung "Aus Nebenbei wird Business"

const BASE = 'https://mumlifebalance.api-us1.com/admin/api.php';
const KEY = 'b3c3542991489fc766fe5f8e0f570412769b252ea525f75a33d72a8944e0fba5b0bf4e29';
const LINK = 'https://mumlifebalance.thrivecart.com/aus-nebenbei-wird-business/';

async function acv1(action, data) {
  const params = new URLSearchParams({ api_key: KEY, api_action: action, api_output: 'json', ...data });
  const res = await fetch(BASE, { method: 'POST', body: params });
  const text = await res.text();
  try { return JSON.parse(text); } catch(e) { throw new Error(`Non-JSON response: ${text.substring(0, 300)}`); }
}

function buildEmail(preheader, title, subtitle, body) {
  return `<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${title}</title>
</head>
<body style="margin:0;padding:0;background-color:#f4f0e6;font-family:Arial,sans-serif;">
  <div style="display:none;max-height:0;overflow:hidden;mso-hide:all;">${preheader}&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;</div>
  <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#f4f0e6;">
    <tr>
      <td align="center" style="padding:30px 16px;">
        <table width="620" cellpadding="0" cellspacing="0" border="0" style="max-width:620px;width:100%;">
          <!-- HEADER -->
          <tr>
            <td style="background:linear-gradient(135deg,#0c1c30 0%,#29556d 60%,#12828c 100%);border-radius:16px 16px 0 0;padding:48px 40px;">
              <table width="100%" cellpadding="0" cellspacing="0" border="0">
                <tr>
                  <td style="padding-bottom:20px;">
                    <span style="background-color:#dc822e;color:#ffffff;font-family:Arial,sans-serif;font-size:11px;font-weight:bold;letter-spacing:2px;text-transform:uppercase;padding:6px 14px;border-radius:20px;">mumlifebalance · Newsletter</span>
                  </td>
                </tr>
                <tr>
                  <td>
                    <h1 style="margin:0 0 16px 0;font-family:Georgia,serif;font-size:32px;font-weight:bold;color:#f1ecdd;line-height:1.25;">${title}</h1>
                  </td>
                </tr>
                <tr>
                  <td>
                    <p style="margin:0;font-family:Georgia,serif;font-style:italic;font-size:16px;color:rgba(241,236,221,0.72);line-height:1.5;">${subtitle}</p>
                  </td>
                </tr>
              </table>
            </td>
          </tr>
          <!-- BODY -->
          <tr>
            <td style="background-color:#ffffff;padding:40px;">
              ${body}
            </td>
          </tr>
          <!-- FOOTER -->
          <tr>
            <td style="background-color:#0c1c30;border-radius:0 0 16px 16px;padding:28px 40px;text-align:center;">
              <p style="margin:0 0 6px 0;font-family:Arial,sans-serif;font-size:13px;font-weight:bold;color:#f1ecdd;text-transform:uppercase;letter-spacing:1px;">MUMLIFEBALANCE · PATRICIA ULMANN</p>
              <p style="margin:0;font-family:Arial,sans-serif;font-size:12px;color:rgba(241,236,221,0.55);">Business aufbauen als Mama — mit System, nicht mit Stress</p>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>`;
}

function p(text) {
  return `<p style="margin:0 0 16px 0;font-family:Arial,sans-serif;font-size:16px;color:#0c1c30;line-height:1.85;">${text}</p>`;
}

function pullQuote(text) {
  return `<table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:28px 0;">
    <tr>
      <td style="background-color:#f1ecdd;border-left:4px solid #dc822e;border-radius:0 12px 12px 0;padding:20px 24px;">
        <p style="margin:0;font-family:Georgia,serif;font-style:italic;font-size:20px;color:#0c1c30;line-height:1.6;">${text}</p>
      </td>
    </tr>
  </table>`;
}

function infoBox(label, quote, text) {
  return `<table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:28px 0;">
    <tr>
      <td style="background-color:#e4f3f4;border-left:4px solid #12828c;border-radius:0 12px 12px 0;padding:24px 28px;">
        <p style="margin:0 0 8px 0;font-family:Arial,sans-serif;font-size:11px;font-weight:bold;color:#12828c;text-transform:uppercase;letter-spacing:2px;">${label}</p>
        <p style="margin:0 0 16px 0;font-family:Georgia,serif;font-style:italic;font-size:20px;color:#0c1c30;line-height:1.5;">${quote}</p>
        <p style="margin:0;font-family:Arial,sans-serif;font-size:15px;color:#0c1c30;line-height:1.7;">${text}</p>
      </td>
    </tr>
  </table>`;
}

function steps(items) {
  const rows = items.map((item, i) => `
    <tr>
      <td style="padding:8px 0;">
        <table cellpadding="0" cellspacing="0" border="0">
          <tr>
            <td style="width:34px;height:34px;background-color:#12828c;border-radius:50%;text-align:center;vertical-align:middle;">
              <span style="font-family:Arial,sans-serif;font-size:14px;font-weight:bold;color:#ffffff;">${i+1}</span>
            </td>
            <td style="padding-left:14px;font-family:Arial,sans-serif;font-size:15px;color:#0c1c30;line-height:1.6;">${item}</td>
          </tr>
        </table>
      </td>
    </tr>`).join('');
  return `<table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:24px 0;">${rows}</table>`;
}

function ctaButton(text, url) {
  return `<table cellpadding="0" cellspacing="0" border="0" style="margin:32px 0;">
    <tr>
      <td style="background-color:#dc822e;border-radius:8px;padding:16px 32px;">
        <a href="${url}" style="font-family:Arial,sans-serif;font-size:16px;font-weight:bold;color:#ffffff;text-decoration:none;">${text}</a>
      </td>
    </tr>
  </table>`;
}

function bullets(items) {
  const rows = items.map(item =>
    `<p style="margin:0 0 10px 0;font-family:Arial,sans-serif;font-size:15px;color:#0c1c30;line-height:1.7;">${item}</p>`
  ).join('');
  return `<div style="margin:20px 0;">${rows}</div>`;
}

// ─── MAIL 1: Story + Problem + Lösung ────────────────────────────────────────

const mail1Body = [
  p('Hey %FIRSTNAME%,'),
  p('ich muss dir heute etwas sagen, das ein bisschen wehtun könnte.'),
  p('Die meisten Mamas scheitern beim Businessaufbau nicht, weil sie keine guten Ideen haben.'),
  p('Sie scheitern, weil sie versuchen, alles alleine herauszufinden.'),
  p('Ich weiss das, weil ich genau diese Frau war.'),
  p('Abends die Kinder ins Bett bringen. Dann noch schnell einen Post erstellen.<br>Erschöpft. Überfordert. Und trotzdem kämpfend.'),
  p('Ich hatte den Wunsch. Ich hatte den Willen.'),
  p('Aber ich bin untergegangen an:'),
  bullets([
    '→ Was soll ich überhaupt anbieten?',
    '→ Wie finde ich mein Thema?',
    '→ Wie mache ich aus Followern echte Kundinnen?',
    '→ Wie bleibe ich dran, wenn der Alltag alles auffrisst?',
    '→ Warum passiert trotz allem nichts?',
  ]),
  p('Und ich dachte immer: „Wenn ich einfach noch mehr mache… noch mehr poste… noch mehr lerne…"'),
  p('Aber mehr bringt nichts, wenn der Weg unklar ist.'),
  pullQuote('"Genau deshalb öffne ich heute meine 1:1 Begleitung."'),
  p('<strong>3 Monate. Ich. Du. Dein Business. Persönlich.</strong>'),
  infoBox(
    'BETA-ANGEBOT',
    'CHF 777 statt CHF 1500 — nur für die ersten 3 Frauen.',
    'Du kennst mich schon. Du bist in meiner Welt. Genau für dich ist dieser Preis.'
  ),
  ctaButton('Ich will mehr wissen →', LINK),
  p('Morgen erzähle ich dir, was sich für dich in diesen 3 Monaten verändern kann.'),
  p('Herzlich,<br>Patricia'),
  p('<em>P.S. Du versuchst es schon eine Weile alleine. Wie weit hat dich das gebracht? Genau das möchte ich ändern.</em>'),
].join('');

// ─── MAIL 2: Vivid Scene + Transformation ────────────────────────────────────

const mail2Body = [
  p('Hey %FIRSTNAME%,'),
  p('diesen Moment werde ich nie vergessen.'),
  p('Es war ein ganz normaler Dienstagmorgen.<br>Kinder versorgt, Kaffee in der Hand — und dann eine Nachricht:'),
  pullQuote('"Ich bin dabei. Wann können wir starten?"'),
  p('Meine erste echte Kundin. Nicht durch Zufall — sondern weil ich endlich einen klaren Weg hatte.'),
  p('Bis dahin?'),
  bullets([
    '❌ Kein klares Angebot.',
    '❌ Kein System.',
    '❌ Niemand, der mir sagte: „Das hier ist dein nächster Schritt."',
  ]),
  p('Was sich verändert hat, war nicht ich — sondern dass ich aufgehört habe, alleine zu suchen.'),
  p('Und genau das ist, was in meiner 1:1 Begleitung passiert.'),
  p('Du hast vielleicht schon meine Inhalte gesehen, meinen Kurs gemacht, meinen Newsletter gelesen. Du hast den ersten Teil: Wissen.'),
  infoBox(
    'Der entscheidende Unterschied',
    'Ohne jemanden, der dir sagt „Ja, genau so" oder „Ändere das lieber" — dreht man sich im Kreis.',
    'Das ist der zweite Teil. Und er verändert alles. Das ist was wir in 3 Monaten gemeinsam tun.'
  ),
  p('BETA-Preis: <strong>CHF 777 statt CHF 1500</strong> — noch <strong>3 Plätze frei</strong>.'),
  ctaButton('Ich will den zweiten Teil →', LINK),
  p('Herzlich,<br>Patricia'),
  p('<em>P.S. Wissen ohne Begleitung ist wie eine Landkarte ohne jemanden, der dir zeigt, wo du gerade bist. Ich zeige es dir.</em>'),
].join('');

// ─── MAIL 3: Credibility + Was steckt drin ───────────────────────────────────

const mail3Body = [
  p('Hey %FIRSTNAME%,'),
  p('manche denken, ich hätte einfach Glück gehabt.'),
  p('Ganz so war es nicht. 😉'),
  p('Ich habe lange alles alleine gemacht. Abends, wenn die Kinder schlafen.<br>Müde. Überfordert. Ohne zu wissen, ob ich auf dem richtigen Weg bin.'),
  bullets([
    '❌ Kein Team.',
    '❌ Keine Mentorin, die schon da war.',
    '❌ Niemand, der auf meinen Content schaute und sagte: „Das ist stark — mach mehr davon."',
    '✅ Nur ich, mein Handy — und ein Wunsch, der grösser war als mein Zweifel.',
  ]),
  p('Was ich gelernt habe: Du kannst alles Wissen der Welt haben. Aber wenn du alles selbst herausfinden musst — brauchst du dreimal so lang.'),
  p('<strong>Deshalb gibt es diese Begleitung. Hier ist, was wir gemeinsam machen:</strong>'),
  steps([
    '<strong>Dein Thema und dein Angebot klären</strong> — so dass es sich wirklich nach dir anfühlt, nicht nach einem Kurs-Baukastenprinzip.',
    '<strong>Deine Instagram-Strategie aufbauen</strong> — ohne täglich Stunden zu investieren. Fokussiert, wirkungsvoll, authentisch.',
    '<strong>Deinen ersten oder nächsten Verkauf ermöglichen</strong> — mit einem System, nicht mit Glück.',
    '<strong>Wöchentliche Calls + Support zwischen den Calls</strong> — du bist nie alleine damit.',
  ]),
  infoBox(
    'BETA-ANGEBOT',
    'CHF 777 statt CHF 1500 — noch 2 Plätze frei.',
    'Dieser Preis gilt nur in der BETA-Phase. Danach steigt er auf CHF 1500.'
  ),
  ctaButton('Jetzt meinen Platz sichern →', LINK),
  p('Herzlich,<br>Patricia'),
  p('<em>P.S. Eine meiner Kundinnen sagte: „Ich wünschte, ich hätte das früher gemacht." Das wünsche ich dir nicht — deshalb schreibe ich dir heute.</em>'),
].join('');

// ─── MAIL 4: Zukunfts-Schmerz + Einwände ─────────────────────────────────────

const mail4Body = [
  p('Hey %FIRSTNAME%,'),
  p('ich muss dich etwas fragen, das sich unangenehm anfühlen könnte:'),
  pullQuote('Was ist, wenn du in 6 Monaten noch am gleichen Punkt bist wie jetzt?'),
  bullets([
    '❌ Immer noch kein klares Angebot.',
    '❌ Immer noch Content, der keine Kundinnen bringt.',
    '❌ Immer noch das Gefühl: „Ich mache irgendwas falsch."',
    '❌ Immer noch alleine damit.',
  ]),
  p('Und du schaust zurück auf genau diesen Moment — diese Mail — und denkst: <em>„Warum habe ich damals nicht einfach JA gesagt?"</em>'),
  p('Ich wünsche mir das nicht für dich. Denn ich war genau dort.'),
  p('Ich war die Mama, die sagte:<br>→ „Ich schaffe das alleine."<br>→ „Ich brauche das jetzt noch nicht."<br>→ „Erstmal schauen wie es läuft."'),
  p('Und weisst du, was passiert ist?'),
  bullets([
    '❌ Ich blieb Monate länger stecken als nötig.',
    '❌ Ich verlor Energie für Dinge, die nichts brachten.',
    '❌ Ich wollte fast aufgeben.',
  ]),
  infoBox(
    'Bis ich endlich JA sagte',
    '✅ JA zu Unterstützung. ✅ JA zu jemandem, der schon da war. ✅ JA zu einem klaren Weg.',
    'Und ab da änderte sich alles. Nicht über Nacht. Aber Schritt für Schritt — mit jemanden an meiner Seite.'
  ),
  p('Vielleicht sagst du: <em>„CHF 777 ist viel Geld."</em><br>Der Normalpreis ist CHF 1500. Das hier ist der BETA-Preis. Und mal ehrlich: Was kostet es dich, noch ein weiteres Jahr auf der Stelle zu stehen?'),
  p('Noch <strong>2 Plätze</strong> verfügbar.'),
  ctaButton('Ich sage JA →', LINK),
  p('Herzlich,<br>Patricia'),
  p('<em>P.S. Menschen, die vorwärtskommen, sind nicht die, die alles alleine machen. Sondern die, die sich Unterstützung holen, bevor sie ausbrennen.</em>'),
].join('');

// ─── MAIL 5: Letzte Chance ────────────────────────────────────────────────────

const mail5Body = [
  p('Hey %FIRSTNAME%,'),
  p('das ist der Moment.'),
  p('Das ist meine letzte Mail zur 1:1 Begleitung <strong>„Aus Nebenbei wird Business"</strong>.'),
  bullets([
    '❌ Keine Verlängerung.',
    '❌ Kein „noch eine Chance".',
    '❌ Keine Wiederholung des BETA-Preises.',
  ]),
  p('Ich sage das nicht, um Druck aufzubauen.'),
  p('Ich sage das, weil ich wirklich nicht möchte, dass du die Frau bist, die:'),
  bullets([
    '→ weiter alleine sucht, was bereits einen klaren Weg hat',
    '→ in 6 Monaten noch dieselben Fragen hat',
    '→ anderen beim Wachsen zusieht',
  ]),
  p('Du kennst mich schon. Du bist in meiner Welt.<br>Das bedeutet: Du weisst, dass ich nicht verkaufe, was nicht wirkt.'),
  infoBox(
    'Letzte Plätze',
    'CHF 777 statt CHF 1500 — sobald die 3 Plätze weg sind, ist dieser Preis vorbei.',
    'Diese Begleitung ist für Frauen, die jetzt bereit sind. Nicht irgendwann. Jetzt.'
  ),
  ctaButton('Ja, ich bin dabei →', LINK),
  p('Falls es jetzt nicht passt: kein Problem. Ich schreibe dir bald über andere Themen. 💛'),
  p('Herzlich,<br>Patricia'),
  p('<em>P.S. Frag dich: „Wie würde mein Business in 6 Monaten aussehen, wenn ich diese 3 Monate nicht alleine bin?" Das ist deine Antwort. Warte nicht.</em>'),
].join('');

// ─── CAMPAIGNS ────────────────────────────────────────────────────────────────

const mails = [
  {
    name: '[Funnel 1:1] Mail 1 – Story & Einladung',
    subject: 'Ich muss dir heute etwas sagen, das wehtun könnte…',
    preheader: 'Die meisten Mamas scheitern nicht wegen fehlender Ideen — sondern weil sie alles alleine machen.',
    title: 'Ich muss dir heute etwas sagen, das wehtun könnte…',
    subtitle: 'Warum ich jetzt meine 1:1 Begleitung öffne — und für wen.',
    body: mail1Body,
  },
  {
    name: '[Funnel 1:1] Mail 2 – Die Transformation',
    subject: 'Diesen Moment werde ich nie vergessen.',
    preheader: 'Meine erste Kundin kam nicht durch Zufall. Sie kam durch ein System.',
    title: 'Diesen Moment werde ich nie vergessen.',
    subtitle: 'Wie sich alles verändert hat — und was das mit dir zu tun hat.',
    body: mail2Body,
  },
  {
    name: '[Funnel 1:1] Mail 3 – Was steckt drin',
    subject: 'Manche denken, ich hätte einfach Glück gehabt.',
    preheader: 'Kein Glück. Kein Team. Nur ein klarer Weg — den ich jetzt mit dir gehe.',
    title: 'Manche denken, ich hätte einfach Glück gehabt.',
    subtitle: 'Was wirklich hinter meinem Business steckt — und was du in 3 Monaten bekommst.',
    body: mail3Body,
  },
  {
    name: '[Funnel 1:1] Mail 4 – Zukunfts-Schmerz',
    subject: 'Was ist, wenn du in 6 Monaten noch am gleichen Punkt bist?',
    preheader: 'Diese Frage hat mein Leben verändert. Sie könnte auch deins verändern.',
    title: 'Was ist, wenn du in 6 Monaten noch am gleichen Punkt bist?',
    subtitle: 'Eine unbequeme Frage — und eine ehrliche Antwort.',
    body: mail4Body,
  },
  {
    name: '[Funnel 1:1] Mail 5 – Letzte Chance',
    subject: 'Das ist meine letzte Mail dazu.',
    preheader: 'Keine Verlängerung. Keine zweite Chance. Aber vielleicht deine.',
    title: 'Das ist meine letzte Mail dazu.',
    subtitle: 'Für die Frauen, die bereit sind — jetzt.',
    body: mail5Body,
  },
];

// ─── AUSFÜHREN ────────────────────────────────────────────────────────────────

const results = [];

for (const mail of mails) {
  const html = buildEmail(mail.preheader, mail.title, mail.subtitle, mail.body);
  const text = `Hey %FIRSTNAME%, ${mail.preheader} → ${LINK}`;

  // 1. Nachricht erstellen
  const msgData = {
    subject: mail.subject,
    fromemail: 'info@mumlifebalance.ch',
    fromname: 'Patricia',
    reply2: 'info@mumlifebalance.ch',
    html,
    text,
  };
  msgData['p[2]'] = '2';
  msgData['format'] = 'mime';
  const msgResult = await acv1('message_add', msgData);

  if (msgResult.result_code !== 1) {
    console.log('❌ Fehler Nachricht:', mail.name, JSON.stringify(msgResult));
    continue;
  }

  const messageId = msgResult.id;

  // 2. Kampagne erstellen
  const campParams = {
    type: 'single',
    name: mail.name,
    subject: mail.subject,
    fromname: 'Patricia',
    fromemail: 'info@mumlifebalance.ch',
    status: '0',
  };
  campParams['p[2]'] = '2';
  campParams[`m[${messageId}]`] = '100';

  const campResult = await acv1('campaign_create', campParams);

  if (campResult.result_code !== 1) {
    console.log('❌ Fehler Kampagne:', mail.name, JSON.stringify(campResult));
    continue;
  }

  results.push({ name: mail.name, messageId, campaignId: campResult.id });
  console.log(`✅ ${mail.name}`);
  console.log(`   Message ID: ${messageId} | Campaign ID: ${campResult.id}`);
}

console.log(`\n✅ Fertig: ${results.length}/5 Kampagnen erstellt`);
console.log('\nKampagnen-IDs für die Automation:');
results.forEach(r => console.log(`  ${r.name}: Campaign ${r.campaignId}`));
