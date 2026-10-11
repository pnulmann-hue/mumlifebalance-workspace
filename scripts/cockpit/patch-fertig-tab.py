# -*- coding: utf-8 -*-
"""Reiter „Fertig zum Posten" — was sofort freigegeben werden kann.

Anlass (Patricia, 18.09.2026): „kannst du noch einen reiter machen fertig zum
posten, dass ich sehe, was ich direkt freigeben kann?"

Die Wochen-Vorschau zeigt ALLES nebeneinander — 68 Karten, die meisten mit
einer Lücke. Wer freigeben will, muss sich durch die halbfertigen durchscrollen.
Dieser Reiter dreht es um: er zeigt nur, was schon steht.

Drei Gruppen, und die mittlere ist die wichtige:

  1. **Kann raus** — nichts fehlt, Zeitpunkt liegt in der Zukunft.
  2. **Fertig, aber das Datum ist durch** — nichts fehlt, aber der Zeitpunkt
     ist vorbei. 🚨 Das ist der Fall, der sonst untergeht: die Karte sieht
     fertig aus, die Freigabe meldet „abgelegt", und der Einplan-Lauf um 20:00
     überspringt sie stillschweigend, weil Blotato nichts in der Vergangenheit
     annimmt. Hier steht es mit Ansage dran.
  3. **Schon freigegeben** — als kompakte Liste, damit sie sieht, was auf den
     20:00-Lauf wartet und was sie selbst posten muss (B-Roll).

Gebaut aus denselben Karten wie die Wochen-Vorschau (`wochenKarte`), nicht als
zweite Ansicht — Freigeben, Datum, Uhrzeit und Profil funktionieren dort also
genauso. Eine zweite Bauart hätte beim nächsten Umbau auseinandergelebt.

Wiederholbar. Schreibt erst daneben und ersetzt danach.
"""
import io
import os
import sys

ZIEL = os.path.join("outputs", "cockpit", "mlb-cockpit.html")


# ---------------------------------------------- 1. Beitragsliste teilen

# Bisher baute `renderWoche` die Liste selbst. Der neue Reiter braucht
# dieselbe — also einmal an einer Stelle.
LISTE_ANKER = """  function renderWoche(main) {
    var beitraege = [];
    state.reels.forEach(function (r) {
      beitraege.push({ art: "reels", id: r.id, obj: r, format: "Reel",
                       titel: r.name, hook: r.hook || "", unter: r.unter || "",
                       caption: r.caption || "", datei: r.videodatei || "",
                       videourl: r.videourl || "" });
    });
    state.karussells.forEach(function (c) {
      var s1 = (c.slides && c.slides[0]) || {};
      beitraege.push({ art: "karussells", id: c.id, obj: c, format: "Karussell",
                       titel: c.name, hook: s1.headline || "",
                       unter: (c.slides ? c.slides.length : 0) + " Folien",
                       caption: c.caption || "", datei: "" });
    });
    // Die taeglichen Storys gehoeren hierher, nicht nur in den Bild-Editor —
    // hier prueft Patricia am Freitag.
    state.storys.forEach(function (s) {
      var f1 = (s.frames && s.frames[0]) || {};
      beitraege.push({ art: "storys", id: s.id, obj: s, format: "Story",
                       titel: s.name, hook: f1.text || "",
                       unter: (s.frames ? s.frames.length : 0) + " Folien",
                       caption: "", datei: "" });
    });
"""

LISTE_NEU = """  /* Alle Beitraege in einer Form. Die Wochen-Vorschau und der Reiter
     „Fertig zum Posten" lesen dieselbe Liste — zwei Bauarten waeren beim
     naechsten Umbau auseinandergelaufen. */
  function alleBeitraege() {
    var beitraege = [];
    state.reels.forEach(function (r) {
      beitraege.push({ art: "reels", id: r.id, obj: r, format: "Reel",
                       titel: r.name, hook: r.hook || "", unter: r.unter || "",
                       caption: r.caption || "", datei: r.videodatei || "",
                       videourl: r.videourl || "" });
    });
    state.karussells.forEach(function (c) {
      var s1 = (c.slides && c.slides[0]) || {};
      beitraege.push({ art: "karussells", id: c.id, obj: c, format: "Karussell",
                       titel: c.name, hook: s1.headline || "",
                       unter: (c.slides ? c.slides.length : 0) + " Folien",
                       caption: c.caption || "", datei: "" });
    });
    // Die taeglichen Storys gehoeren dazu, nicht nur in den Bild-Editor —
    // hier prueft Patricia am Freitag.
    state.storys.forEach(function (s) {
      var f1 = (s.frames && s.frames[0]) || {};
      beitraege.push({ art: "storys", id: s.id, obj: s, format: "Story",
                       titel: s.name, hook: f1.text || "",
                       unter: (s.frames ? s.frames.length : 0) + " Folien",
                       caption: "", datei: "" });
    });
    return beitraege;
  }

  /* Ein leerer Entwurf ist kein Beitrag — weder eine Aufgabe noch etwas,
     das man freigeben koennte. */
  function istLeer(b) {
    return !(b.hook || "").trim() && !(b.caption || "").trim() &&
           !((b.obj.slides || []).length) && !((b.obj.frames || []).length);
  }

  /* 🚨 Blotato lehnt jeden Zeitpunkt in der Vergangenheit ab, und der
     Einplan-Lauf ist erst um 20:00. Ein Beitrag, dessen Zeitpunkt durch ist,
     sieht fertig aus und geht trotzdem nie raus. */
  function zeitpunktVorbei(b) {
    if (!b.obj.datum) return false;
    var zeit = (b.obj.blotato && b.obj.blotato.zeit) ||
               vorgabeZeit(b.art, kartenProfil(b.obj));
    var wann = new Date(b.obj.datum + "T" + zeit);
    return !isNaN(wann) && wann.getTime() < Date.now();
  }

  /* Fertig heisst: nichts fehlt und noch nicht freigegeben. */
  function istFertig(b) {
    return !istLeer(b) && !b.obj.textfrei && !wasFehlt(b).length;
  }

  function fertigAnzahl() {
    return alleBeitraege().filter(function (b) {
      return istFertig(b) && !zeitpunktVorbei(b);
    }).length;
  }

  function renderWoche(main) {
    var beitraege = alleBeitraege();
"""


# ----------------------------------------------------- 2. renderFertig

FERTIG_ANKER = """  function renderNav() {
"""

FERTIG_NEU = '''  /* Reiter „Fertig zum Posten": nur das, was schon steht. */
  function renderFertig(main) {
    var alle = alleBeitraege().filter(function (b) { return !istLeer(b); });
    alle.forEach(function (b) { wochenBildHolen(b.art, b.id); });

    function nachDatum(x, y) {
      var a = x.obj.datum || "9999", c = y.obj.datum || "9999";
      return a < c ? -1 : (a > c ? 1 : 0);
    }
    var fertig = alle.filter(istFertig);
    var kannRaus = fertig.filter(function (b) { return !zeitpunktVorbei(b); }).sort(nachDatum);
    var durch = fertig.filter(zeitpunktVorbei).sort(nachDatum);
    var frei = alle.filter(function (b) { return b.obj.textfrei; }).sort(nachDatum);
    var offen = alle.filter(function (b) {
      return !b.obj.textfrei && wasFehlt(b).length;
    }).length;

    main.innerHTML =
      '<div class="page-head"><div><h1>Fertig zum Posten</h1>' +
      '<p>Nur was schon steht \\u2014 Video da, Caption da, Datum da. ' +
      'Freigeben geht hier genauso wie in der Wochen-Vorschau: Datum und ' +
      'Uhrzeit pr\\u00fcfen, Profil pr\\u00fcfen, freigeben. Um 20:00 wird ' +
      'eingeplant, was bis dahin freigegeben ist.</p></div></div>' +
      '<div class="tiles">' +
      tile("Kann raus", kannRaus.length, kannRaus.length ? "wartet auf dein Go" : "gerade nichts") +
      tile("Datum ist durch", durch.length,
           durch.length ? "fertig, aber neu datieren" : "keiner") +
      tile("Schon freigegeben", frei.length, "wartet auf 20:00") +
      tile("Noch nicht fertig", offen, "steht unter „Was zu tun ist“") +
      '</div>' +
      '<div id="fliste"></div>';

    var box = main.querySelector("#fliste");

    function gruppe(titel, unter, liste) {
      if (!liste.length) return;
      var kopf = document.createElement("div");
      kopf.className = "wt-kopf";
      kopf.innerHTML = '<span class="wt-name">' + esc(titel) + '</span>' +
                       '<span class="wt-datum">' + liste.length + '</span>';
      box.appendChild(kopf);
      if (unter) {
        var n = document.createElement("p");
        n.className = "note";
        n.style.margin = "0 0 10px";
        n.textContent = unter;
        box.appendChild(n);
      }
      liste.forEach(function (b) { box.appendChild(wochenKarte(b)); });
    }

    if (!kannRaus.length && !durch.length && !frei.length) {
      box.innerHTML = '<div class="panel"><div class="empty">Noch ist nichts ' +
        'fertig. Was fehlt, steht in der Wochen-Vorschau unter ' +
        '\\u201eWas zu tun ist\\u201c.</div></div>';
      return;
    }

    gruppe("Kann raus", "", kannRaus);
    gruppe("Fertig, aber das Datum ist durch",
           "Hier steht alles. Nur der Zeitpunkt ist vorbei, und Instagram nimmt "
           + "keinen Zeitpunkt in der Vergangenheit. Setz ein neues Datum, dann "
           + "kannst du freigeben.", durch);

    // Freigegebenes nur als Liste — die vollen Karten braucht hier niemand mehr.
    if (frei.length) {
      var kopf = document.createElement("div");
      kopf.className = "wt-kopf";
      kopf.innerHTML = '<span class="wt-name">Schon freigegeben</span>' +
                       '<span class="wt-datum">' + frei.length + '</span>';
      box.appendChild(kopf);
      var panel = document.createElement("div");
      panel.className = "panel tuliste";
      var h = "";
      frei.forEach(function (b) {
        var bl = b.obj.blotato || {};
        var stand = bl.status === "gepostet-von-hand" ? "selbst gepostet"
                  : bl.status === "selber-posten" ? "postest du selbst (Musik)"
                  : bl.status === "geplant" ? "eingeplant"
                  : bl.status === "zeitpunkt-vorbei" ? "Zeitpunkt vorbei"
                  : b.art === "storys" ? "Story \\u2014 postest du selbst"
                  : "wartet auf 20:00";
        h += '<div class="tuzeile">' +
          '<span class="tudatum">' +
            (b.obj.datum ? esc(tagName(b.obj.datum).slice(0, 2) + " " +
                               fmtDate(b.obj.datum)) : "ohne Datum") +
            (bl.zeit ? " " + esc(bl.zeit) : "") + '</span>' +
          '<span class="tuwas"><strong>' + esc(b.titel) + '</strong> <span>\\u00b7 ' +
            esc(kartenProfil(b.obj) === "doterra" ? "doTERRA" : "Mentoring") +
            '</span></span>' +
          '<span class="tuwer ' +
            (stand === "wartet auf 20:00" || stand === "eingeplant" ? "ich" : "du") +
            '">' + esc(stand) + '</span>' +
          '</div>';
      });
      panel.innerHTML = h;
      box.appendChild(panel);
    }
  }

  function renderNav() {
'''


# ------------------------------------------------------- 3. Reiter + Zahl

TAB_ANKER = """    { id: "woche", label: "Wochen-Vorschau" },"""
TAB_NEU = """    { id: "woche", label: "Wochen-Vorschau" },
    { id: "fertig", label: "Fertig zum Posten" },"""

ZAHL_ANKER = """      var cnt = t.id === "karussell" ? state.karussells.length"""
ZAHL_NEU = """      // Die Zahl am Reiter ist die eigentliche Antwort auf „was kann raus".
      var cnt = t.id === "fertig" ? fertigAnzahl()
        : t.id === "karussell" ? state.karussells.length"""

DISPATCH_ANKER = """    else if (activeTab === "woche") renderWoche(main);"""
DISPATCH_NEU = """    else if (activeTab === "woche") renderWoche(main);
    else if (activeTab === "fertig") renderFertig(main);"""


# --------------------------- 3b. Storys aus „Kann raus" heraushalten

# 🚨 Beim ersten Lauf stand „Kann raus: 27" da — darin steckten 20 Storys.
# Eine Story geht nie ueber Blotato, die postet Patricia selbst vom Handy.
# Die Frage „was kann ich direkt freigeben" meint den Feed. Also getrennt
# zaehlen, sonst ist die Zahl am Reiter groesser als die Arbeit dahinter.
SPLIT_ANKER = """  function fertigAnzahl() {
    return alleBeitraege().filter(function (b) {
      return istFertig(b) && !zeitpunktVorbei(b);
    }).length;
  }"""

SPLIT_NEU = """  function fertigAnzahl() {
    return alleBeitraege().filter(function (b) {
      return b.art !== "storys" && istFertig(b) && !zeitpunktVorbei(b);
    }).length;
  }"""

GRUPPEN_ANKER = """    var fertig = alle.filter(istFertig);
    var kannRaus = fertig.filter(function (b) { return !zeitpunktVorbei(b); }).sort(nachDatum);
    var durch = fertig.filter(zeitpunktVorbei).sort(nachDatum);"""

GRUPPEN_NEU = """    var fertig = alle.filter(istFertig);
    // Feed und Story sind zwei verschiedene Handlungen: den Feed gibst du
    // frei und der 20:00-Lauf plant ihn ein, die Story postest du selbst.
    var feed = fertig.filter(function (b) { return b.art !== "storys"; });
    var kannRaus = feed.filter(function (b) { return !zeitpunktVorbei(b); }).sort(nachDatum);
    var durch = feed.filter(zeitpunktVorbei).sort(nachDatum);
    // Eine Story mit einem Datum von gestern ist vorbei, nicht offen.
    var storys = fertig.filter(function (b) {
      return b.art === "storys" && !zeitpunktVorbei(b);
    }).sort(nachDatum);"""

KACHEL_ANKER = """      tile("Kann raus", kannRaus.length, kannRaus.length ? "wartet auf dein Go" : "gerade nichts") +
      tile("Datum ist durch", durch.length,
           durch.length ? "fertig, aber neu datieren" : "keiner") +
      tile("Schon freigegeben", frei.length, "wartet auf 20:00") +"""

KACHEL_NEU = """      tile("Kann raus", kannRaus.length,
           kannRaus.length ? "Feed \\u2014 wartet auf dein Go" : "gerade nichts") +
      tile("Datum ist durch", durch.length,
           durch.length ? "fertig, aber neu datieren" : "keiner") +
      tile("Storys bereit", storys.length, "die postest du selbst") +
      tile("Schon freigegeben", frei.length, "wartet auf 20:00") +"""

LEERTEXT_ANKER = """    if (!kannRaus.length && !durch.length && !frei.length) {"""
LEERTEXT_NEU = """    if (!kannRaus.length && !durch.length && !frei.length && !storys.length) {"""

GRUPPE3_ANKER = """    gruppe("Fertig, aber das Datum ist durch",
           "Hier steht alles. Nur der Zeitpunkt ist vorbei, und Instagram nimmt "
           + "keinen Zeitpunkt in der Vergangenheit. Setz ein neues Datum, dann "
           + "kannst du freigeben.", durch);"""

GRUPPE3_NEU = """    gruppe("Fertig, aber das Datum ist durch",
           "Hier steht alles. Nur der Zeitpunkt ist vorbei, und Instagram nimmt "
           + "keinen Zeitpunkt in der Vergangenheit. Setz ein neues Datum, dann "
           + "kannst du freigeben.", durch);
    gruppe("Storys \\u2014 die postest du selbst",
           "Storys gehen nie \\u00fcber Blotato. Folien im Bild-Editor bauen, "
           + "herunterladen, vom Handy posten.", storys);"""


# ------------------------------- 4. leere Entwuerfe ueber istLeer pruefen

# Der Aufgaben-Block hatte seine eigene Kopie der Pruefung. Jetzt gibt es
# `istLeer` — eine Stelle statt zwei.
DOPPEL_ANKER = """      // Ein leerer Entwurf ist keine Aufgabe.
      var leer = !(b.hook || "").trim() && !(b.caption || "").trim() &&
                 !((b.obj.slides || []).length) && !((b.obj.frames || []).length);
      if (leer) return;"""

DOPPEL_NEU = """      if (istLeer(b)) return;   // ein leerer Entwurf ist keine Aufgabe"""


def main():
    if not os.path.isfile(ZIEL):
        sys.exit("Nicht gefunden: " + ZIEL)
    with io.open(ZIEL, encoding="utf-8") as f:
        text = f.read()

    getan, offen = [], []

    def tausche(alt, neu, name):
        nonlocal text
        if neu in text:
            getan.append(name + " (war schon gesetzt)")
            return
        if text.count(alt) != 1:
            offen.append("%s — Anker %dx gefunden" % (name, text.count(alt)))
            return
        text = text.replace(alt, neu)
        getan.append(name)

    tausche(LISTE_ANKER, LISTE_NEU, "alleBeitraege() + istFertig() + zeitpunktVorbei()")
    tausche(FERTIG_ANKER, FERTIG_NEU, "renderFertig()")
    tausche(TAB_ANKER, TAB_NEU, "Reiter in der Navigation")
    tausche(ZAHL_ANKER, ZAHL_NEU, "Zahl am Reiter")
    tausche(DISPATCH_ANKER, DISPATCH_NEU, "Reiter im Dispatcher")
    tausche(SPLIT_ANKER, SPLIT_NEU, "Zahl am Reiter: nur Feed")
    tausche(GRUPPEN_ANKER, GRUPPEN_NEU, "Storys als eigene Gruppe")
    tausche(KACHEL_ANKER, KACHEL_NEU, "Kachel „Storys bereit“")
    tausche(LEERTEXT_ANKER, LEERTEXT_NEU, "Leertext beruecksichtigt Storys")
    tausche(GRUPPE3_ANKER, GRUPPE3_NEU, "Gruppe Storys anzeigen")
    tausche(DOPPEL_ANKER, DOPPEL_NEU, "doppelte Leer-Pruefung zusammenlegen")

    for z in getan:
        print("  ok    " + z)
    for z in offen:
        print("  OFFEN " + z)
    if offen:
        sys.exit("\nAbgebrochen — nichts geschrieben.")

    tmp = ZIEL + ".neu"
    with io.open(tmp, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    os.replace(tmp, ZIEL)
    print("\nGeschrieben: %s (%d Zeichen)" % (ZIEL, len(text)))


if __name__ == "__main__":
    main()
