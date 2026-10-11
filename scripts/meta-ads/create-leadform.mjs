const T = process.env.META_ACCESS_TOKEN;
const PAGE = '100753756193662';
const post = (p, params) => fetch('https://graph.facebook.com/v20.0/' + p, { method: 'POST', body: new URLSearchParams({ ...params, access_token: T }) }).then(r => r.json());

const form = {
  name: 'Bio-Check Lead-Formular',
  locale: 'de_DE',
  // E-Mail + Vorname (beide vorausgefüllt aus dem Profil = wenig Reibung)
  questions: JSON.stringify([
    { type: 'FIRST_NAME' },
    { type: 'EMAIL' },
  ]),
  // Intro-Karte: erklärt das Angebot, bevor das Formular kommt
  context_card: JSON.stringify({
    style: 'PARAGRAPH_STYLE',
    title: 'Kostenloser Bio-Check',
    content: 'In rund 10 Minuten zeige ich dir, was deine Instagram-Bio gerade aussendet — und was sie aussenden müsste, damit die richtigen Menschen bleiben und dir schreiben. Du bekommst eine persönliche Analyse, 5 fertige Bio-Vorschläge und dein PDF per E-Mail.',
    button_text: 'Bio-Check starten',
  }),
  privacy_policy: JSON.stringify({
    url: 'https://mumlifebalance.ch/datenschutzerklaerung/',
    link_text: 'Datenschutzerklärung',
  }),
  // Danke-Seite: sagt klar „bestätige deine Mail" (Double-Opt-in)
  thank_you_page: JSON.stringify({
    title: 'Fast geschafft! 🤍',
    body: 'Schau jetzt in dein E-Mail-Postfach und bestätige deine Anmeldung — danach kommt dein Bio-Check direkt zu dir. (Bitte auch im Spam-Ordner nachschauen.)',
    button_type: 'VIEW_WEBSITE',
    button_text: 'Zu meinem Profil',
    website_url: 'https://www.instagram.com/mumlifebalance_patricia_ulmann/',
  }),
};

const res = await post(PAGE + '/leadgen_forms', form);
console.log('FORMULAR:', JSON.stringify(res));
