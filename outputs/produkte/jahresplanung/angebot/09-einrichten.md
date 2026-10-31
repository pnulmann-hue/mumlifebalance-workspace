---
tags: [produkt, funnel, jahresplanung]
---

# 09 · Einrichten · Neustart 2027

> Alles, was von Hand angelegt wird. Nichts davon ist live. Reihenfolge und Daten: `00-bauplan.md` → Fahrplan.
> 🚨 Nichts geht ohne Patricias Go live (WP, AC, ManyChat).

## Entscheide (bis So 15.11.)

- [ ] Name „Neustart 2027 · Jahresplanungs-Workshop“ bestätigen
- [ ] Stichwort NEUSTART bestätigen
- [ ] Dauer (Vorschlag 90 Minuten) und Ort der Aufzeichnung (Vorschlag Vimeo)
- [ ] MBA: regulär 997 oder ein Preis nur für Workshop-Teilnehmerinnen (dann Rechnung im Chat zeigen)
- [ ] 1:1 Postingplan: verschieben oder leise neben dem Workshop
- [ ] Ziel: wie viele MBA-Verkäufe soll der Workshop bringen?
- [ ] „Warum mit mir“: Satz zu Schulferien und Geburtstagen stimmt so (Seite, A2, Karussell)
- [ ] Beiträge in den Weihnachtsferien ja/nein

## Einrichten

| Wo | Was | bis |
|---|---|---|
| Artifact „Mein Jahresplan“ | über das Share-Menü öffentlich teilen, Link an Claude (für E1, E2, Ablauf) | 20.11. |
| Zoom | Termin Do 17.12. 09:00, Aufzeichnung an, Link an Claude (kommt nur in AC, nie ins Repo) | 20.11. |
| WordPress | Mockup als webp hochladen (Adresse in `BILD_WP`), Seite `/neustart-2027/` und `/neustart-2027-danke/` als Entwurf (`elementor_canvas`, wie Tool-Workshop), Customizer-Block „NEUSTART-2027-EFFEKT“ aus `outputs/salespages/jahresplanung/neustart-2027-effekt.css` | 20.11. |
| ActiveCampaign | Tag „0€ Jahresplanung“ (ID in active-funnels.json) · Formular „0€ Jahresplanung“ als Kopie von 75 (Liste 2, Tag, Bestätigungsmail aus 04, Weiterleitung `/neustart-2027-danke/`, bei „Eine Liste abonnieren“ die Adresse wählen und speichern) · ID in `FORMULAR` eintragen | 20.11. |
| ActiveCampaign | Kampagnen A1 (30.11.), A2 (7.12.), A3 (15.12.) an Liste 2, ohne Tag „0€ Jahresplanung“ und ohne MBA-Käuferinnen | 23.11. |
| ActiveCampaign | Automation „0€ Jahresplanung“: Start Tag · warten bis 16.12. 18:00 → E1 · bis 17.12. 08:00 → E2 · bis 17.12. abends → E3 · E4 · E5 · Ziel „MBA gekauft“ ganz unten · multientry aus | 23.11. |
| ManyChat | Flow NEUSTART nach 07, testen mit einem Kommentar | 23.11. |
| Instagram | Bio-Link 30.11.–17.12. auf `/neustart-2027/`, Highlight „Neustart“, entscheiden ob ein Pin | 30.11. |
| Cockpit | Storys aus 05 und Beiträge aus 06 einplanen, sobald der Bauplan frei ist | 20.11. |
| nach 17.12. | Seite auf „Aufzeichnung“ umstellen oder neu bauen · Automation nach dem 20.12. stoppen | 21.12. |

## Aus der Funnel-Checkliste (⚠️ ❌ ❓)

- [ ] ❓ Im Ziel-Checkout nachgesehen, was dort als Upsell hängt — MBA-Kasse (ThriveCart 45) auf Upsell/Bump nicht geprüft (Bevor du baust)
- [ ] ❌ Ausgerechnet, wie viele Verkäufe das Ziel braucht — Wie viele MBA-Verkäufe soll der Workshop bringen? Ziel nicht festgelegt (Bevor du baust)
- [ ] ⚠️ Erste Kundenstimmen beschafft, bevor die Seite steht — Keine Stimme auf der Seite; die MBA-Stimmen von /mba/ wären freigegeben (Bevor du baust)
- [ ] ⚠️ Bei 0€: alle drei Kassen besetzt — Danke-Seite und Mails E3–E5 verkaufen; die Seite nach dem Bestätigungsklick ist dieselbe Danke-Seite (Die Kasse)
- [ ] ⚠️ Das grosse Produkt steht im Funnel nie zum Normalpreis — MBA im Pitch zu 997 (Pioneer, Liste 1347), kein eigener Workshop-Preis (🟠) (Die Kasse)
- [ ] ❓ Kopiertes Formular ganz durchgegangen: Liste, Tag, Bestätigung, Weiterleitung — Formular noch nicht angelegt (ActiveCampaign)
- [ ] ❓ Kette Formular → Tag → Automation von vorn nachgeprüft — erst nach dem Anlegen prüfbar (ActiveCampaign)
- [ ] ❓ Der Tag ist über die ID eingetragen, nicht über den Namen — Tag-ID fehlt noch in active-funnels.json (ActiveCampaign)
- [ ] ❓ multientry geprüft, bevor ein Tag nachträglich gesetzt wird — beim Anlegen der Automation prüfen (ActiveCampaign)
- [ ] ❓ Beim Eintritt wird geprüft, ob sie schon in einer anderen Automation steckt — MBA-Käuferinnen nicht mit dem Pitch anschreiben (ActiveCampaign)
- [ ] ⚠️ Einwilligung, eigene Bestätigungsmail, Ränder am Handy — Bestätigungsmail geschrieben, am Handy noch nicht angesehen (ActiveCampaign)
- [ ] ⚠️ Entschieden, was mit denen passiert, die nicht kaufen — Nach E5 (20.12.) nur Newsletter, im Januar entscheiden (ActiveCampaign)
- [ ] ❓ Auslieferung selbst getestet — mit einer echten Adresse eingetragen — Testanmeldung am 23.11. (ActiveCampaign)
- [ ] ❓ ManyChat reagiert auf alle drei Wege — geplant in 07, Flow fehlt (ActiveCampaign)
- [ ] ❌ Je Link ein eigener Klick-Tag — Klick-Tags je Link in ManyChat nicht geplant (ActiveCampaign)
- [ ] ❌ Nachgefasst, wenn 23 Stunden nichts passiert — keine Nachfass-Nachricht in ManyChat (ActiveCampaign)
- [ ] ❓ Landingpage ist erreichbar — gebaut, noch nicht in WordPress (Die Seiten)
- [ ] ⚠️ Seite nach dem Bestätigungsklick hinterlegt — dieselbe Danke-Seite, 🟠 eigene „bestätigt“-Seite? (Die Seiten)
- [ ] ⚠️ Bei einer Frist: eigene Angebotsseite und eine „abgelaufen“-Seite — Nach dem 17.12. braucht /neustart-2027/ eine Fassung „Aufzeichnung“ statt Anmeldung (Die Seiten)
- [ ] ⚠️ Der Block „Das brauchst du nicht“ steht drin — nur im FAQ (Kamera, Live), kein eigener Block (Die Seiten)
- [ ] ❓ Jemand ohne Vorwissen hat die Seite gelesen — Patricia oder eine Testleserin (Die Seiten)
- [ ] ❓ Jede Adresse einmal wirklich aufgerufen — nach dem Livegang (Die Seiten)
- [ ] ❓ Jede Mail einmal am Handy geöffnet — erst als AC-Entwurf (Die Mails)
- [ ] ⚠️ Der Link steht weit oben — in A1 erst nach drei Absätzen (Die Mails)
- [ ] ⚠️ Die Willkommensmail zeigt die ganze Welt — E1 zeigt nur die Vorbereitung, die MBA erst in E3 (Die Mails)
- [ ] ❌ Der Baustein „… und das ohne …“ ist drin — nicht drin (Die Mails)
- [ ] ⚠️ Irgendwo in der Strecke steht ein 48-Stunden-Angebot — kein 48-Stunden-Angebot, weil kein Workshop-Preis feststeht (🟠) (Die Mails)
- [ ] ⚠️ Für die, die nicht gekauft haben, läuft eine eigene Strecke — nach E5 keine eigene Strecke (Die Mails)
- [ ] ❓ Jeder Knopf führt irgendwohin — Zoom- und Aufzeichnungs-Link fehlen noch (✏️) (Die Mails)
- [ ] ⚠️ Keine festen Datumsangaben in einer Dauer-Automation — E1–E5 tragen Daten; die Automation muss nach dem 20.12. stoppen oder umgeschrieben werden (Die Mails)
- [ ] ⚠️ Der Funnel ist dauerhaft sichtbar, nicht nur in einer Story — Bio-Link und Highlight nicht geplant (Der Zulauf)
- [ ] ❓ ManyChat-Flow eingerichtet — 07 (Der Zulauf)
- [ ] ❌ Selbst Nachrichten geschrieben, nicht nur gewartet — persönliche Einladungen (Tool-Workshop-Teilnehmerinnen, MBA-Interessentinnen) nicht geplant (Der Zulauf)
- [ ] ⚠️ In der Bio steht während des Launches nur ein Link — Bio-Link 30.11.–17.12. auf /neustart-2027/ nicht geplant (Der Launch)
- [ ] ❌ Ein Highlight ist farbig markiert und vollgepackt — Highlight „Neustart“ fehlt (Der Launch)
- [ ] ⚠️ Jeden Tag wird geteilt, wer schon dabei ist — nur einmal (11.12.) und nur mit echten Zahlen (Der Launch)
- [ ] ❌ Ein Beitrag zum Launch ist angepinnt — kein Pin geplant (Pins folgen der Creme-Linie) (Der Launch)
- [ ] ⚠️ Alles zeigt in dieselbe Richtung — 1:1 Postingplan könnte im selben Fenster laufen (Der Launch)
- [ ] ❓ Bei Flaute die sechs Fragen durchgegangen — während der Anmeldung (Der Launch)
- [ ] ⚠️ Keine Lücke bis zum nächsten Launch — Januar nach den Ferien offen (Der Launch)
- [ ] ❓ Der Titel folgt einer der drei Formeln — Titel gegen die drei Formeln prüfen (Das Webinar)
- [ ] ⚠️ Die neun Blöcke stehen im Skript — 01 ist ein Arbeits-Ablauf, kein Webinar-Skript mit neun Blöcken (Das Webinar)
- [ ] ❓ Die Agenda dauert höchstens zwanzig Sekunden — im Workshop (Das Webinar)
- [ ] ❓ Frei gesprochen, mit Stichpunkten — im Workshop (Das Webinar)
- [ ] ⚠️ Zwischendurch immer wieder auf den Pitch gezeigt — bewusst nur am Schluss (Das Webinar)
- [ ] ❌ Die Zusammenfassung sagt, wie viel schon gegeben wurde — nicht im Ablauf (Das Webinar)
- [ ] ❌ Drei bis fünf Kundenstimmen, mit Bild und Namen — keine Stimmen im Ablauf (Das Webinar)
- [ ] ⚠️ Der Preisanker steht im Pitch — 1347 → 997 nicht im Pitch (Das Webinar)
- [ ] ❓ Die drei Standardfragen am Schluss beantwortet — im Workshop (Das Webinar)
- [ ] ⚠️ Nach dem Webinar läuft eine Strecke mit Frist — E3–E5 ohne Frist, nur „vor den Ferien“ (Das Webinar)
- [ ] ❓ Eintragungen je Beitrag ausgerechnet — nach dem Workshop (Nach dem Start)
- [ ] ❓ Verstanden, was die Zahl misst — nach dem Workshop (Nach dem Start)
- [ ] ❓ Geteilte Tags nicht doppelt gezählt — nach dem Workshop (Nach dem Start)
- [ ] ❓ Weiter über das Angebot reden, auch wenn der Funnel läuft — nach dem Workshop (Nach dem Start)
- [ ] ❓ Bei Flaute unterschieden: zu wenig Klicks oder zu wenig Käufe — nach dem Workshop (Nach dem Start)
- [ ] ❓ Kundenstimmen aktiv eingeholt — nach dem Workshop (Nach dem Start)
- [ ] ❓ Ein Video-Testimonial gefragt — nach dem Workshop (Nach dem Start)
- [ ] ❓ Die Stimmen liegen an einer Stelle — nach dem Workshop (Nach dem Start)
- [ ] ❓ Die Stimmen sind freigegeben — nach dem Workshop (Nach dem Start)
- [ ] ❓ Den Bestandskundinnen ein eigenes Angebot geschickt — nach dem Workshop (Nach dem Start)
- [ ] ❓ Entschieden: weiterlaufen lassen, nachschärfen oder abstellen — nach dem Workshop (Nach dem Start)
