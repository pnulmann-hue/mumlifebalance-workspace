#!/usr/bin/env python3
"""Tagesplan raus, Varianten rein: die Wochen-Vorschau wird der eine Ort.

Patricia am 19.09.2026: *„kannst du mir bitte den tagesplan streichen? ich will
im wochenplan fuer jeden tag einen button wo ich die verschiedenen varianten pro
tag umstellen kann. […] dann habe ich am schluss eine uebersicht mit den
beitraegen die an welchem tag gepostet werden und eine uebersicht mit den
beitraegen die in der ideenliste stehen"* — und nachgeschoben: *„wochenvorschau
passt schon. da muessen einfach noch die verschiedenen varianten rein."*

Der Tagesplan vom selben Morgen war eine zweite Ansicht derselben Sache. Zwei
Ansichten auf dieselben Daten laufen beim naechsten Umbau auseinander, und man
sucht jedes Mal, in welcher man gerade steht. Also: eine.

Was dazukommt:

* **Fester Rhythmus** Mo/Mi/Fr Reel, Di/Do Karussell, beide Profile
  (Patricias Entscheid). Der Tag sagt das Format, das spart pro Tag eine Frage.
* **Ein Platz je Tag und Profil** mit Knopf „Wechseln" — die Varianten stehen
  darunter, ein Tipp legt eine drauf, die bisherige faellt in die Ideenliste.
* **Soll/Ist doppelt:** 3 Reels / 2 Karussells UND 3 Lead / 2 Reichweite.
  🚨 Die Formatzahl sagt ueber Konversion nichts. Die CTA-Verteilung schon.
* **Loeschen** mit Rueckfrage (zwei Klicks, kein confirm() — ein Artifact-Rahmen
  darf Modals blocken) und **Anderes Datum** direkt auf der Karte.
* **Zwei Uebersichten unten:** was wann rausgeht (ueber alle Wochen) und die
  Ideenliste.

🚨 Lead/Reichweite wird **abgelesen, nicht gepflegt** — ein Stichwort in
Grossbuchstaben im CTA macht den Beitrag zum Lead-Post. Das steht so auf jeder
Karte, damit ein Fehlschluss auffaellt. Ein neues Feld waere sauberer und wuerde
nie gepflegt; eine Ableitung, die man sieht, ist ehrlicher als eine Angabe, der
man nicht ansieht, dass sie fehlt.

🚨 Der Platz wird NICHT getrennt gespeichert. Umschalten setzt `datum` am neuen
Beitrag und leert es am alten — der Beitrag bleibt die einzige Wahrheit.
Freigabe, Aufgabenliste und „Fertig zum Posten" lesen alle `datum`.

Wiederholbar: bricht ab, wenn ein Anker nicht genau einmal vorkommt, prueft mit
`node --check` und schreibt erst nach `<datei>.neu`.
"""
from __future__ import annotations

import argparse
import os
import pathlib
import re
import subprocess
import sys
import tempfile

WURZEL = pathlib.Path(__file__).resolve().parents[2]
STANDARD = WURZEL / "outputs" / "cockpit" / "mlb-cockpit.html"


# ==========================================================================
# 1 · Reiter „Tagesplan" aus der Navigation
# ==========================================================================
ERSETZUNGEN = [
    (
        "Reiter aus der Navigation",
        '''    { g: "Planen" },
    { id: "tagesplan", label: "Tagesplan" },
    { id: "woche", label: "Wochen-Vorschau" },''',
        '''    { g: "Planen" },
    { id: "woche", label: "Wochen-Vorschau" },''',
    ),
    (
        "Zahl am Reiter",
        '''      var cnt = t.id === "tagesplan" ? tagesplanZahl()
        : t.id === "fertig" ? fertigAnzahl()''',
        '''      var cnt = t.id === "fertig" ? fertigAnzahl()''',
    ),
    (
        "Weiche in render()",
        '''    else if (activeTab === "tagesplan") renderTagesplan(main);
    else if (activeTab === "woche") renderWoche(main);''',
        '''    else if (activeTab === "woche") renderWoche(main);''',
    ),
    # ----------------------------------------------------------------------
    # 2 · Der tp-Block heisst nicht mehr Tagesplan, und die zwei Merker
    #     bekommen sprechende Namen. Das Soll um die Job-Verteilung ergaenzt.
    # ----------------------------------------------------------------------
    (
        "Kopf des Wochenrasters",
        '''  /* =========================================================
     Tagesplan: ein Platz je Tag und Profil
     ========================================================= */

  /* Fuenf Tage, zwei Profile — zehn Plaetze in der Woche. Das Soll je Profil
     ist Patricias Entscheid vom 19.09.2026: 3 Reels, 2 Karussells. */
  var TP_SOLL = { reels: 3, karussells: 2 };
  var TP_PROFILE = [
    { id: "mentoring", label: "Mum Life Balance" },
    { id: "doterra", label: "doTERRA" }
  ];
  var tagesplanOffset = null;   // null = noch nicht bestimmt, 0 = diese Woche
  var tagesplanOffen = null;    // "iso|profil" — welcher Platz seine Liste zeigt''',
        '''  /* =========================================================
     Wochenraster: ein Platz je Tag und Profil
     Gehoert zur Wochen-Vorschau. Der frueher eigene Reiter „Tagesplan" war
     eine zweite Ansicht auf dieselben Daten und ist am 19.09.2026 raus.
     ========================================================= */

  /* Fuenf Tage, zwei Profile — zehn Plaetze in der Woche. Das Soll je Profil
     ist Patricias Entscheid vom 19.09.2026: 3 Reels, 2 Karussells. */
  var TP_SOLL = { reels: 3, karussells: 2 };

  /* 🚨 Die zweite Zahl, und die wichtigere: 3 Lead-Posts mit Keyword-CTA,
     2 Reichweiten-Posts mit Share-CTA (3+2-Regel seit 15.09.2026). Wie viele
     Reels eine Woche hat, sagt ueber Konversion nichts — wie viele davon in
     einen Funnel fuehren, schon. */
  var TP_SOLL_JOB = { lead: 3, reichweite: 2 };

  /* Welcher Tag welches Format traegt. Patricia am 19.09.2026: „montag,
     mittwoch, freitag ist reeltag und dienstag und donnerstag karussell" —
     fuer beide Profile. Ein fester Rhythmus spart pro Tag eine Entscheidung. */
  var WOCHENRHYTHMUS = ["reels", "karussells", "reels", "karussells", "reels"];

  var TP_PROFILE = [
    { id: "mentoring", label: "Mum Life Balance" },
    { id: "doterra", label: "doTERRA" }
  ];
  var wochenOffset = null;   // null = noch nicht bestimmt, 0 = diese Woche
  var slotOffen = null;      // "iso|profil" — welcher Platz seine Liste zeigt

  /* Lead oder Reichweite — abgelesen aus dem CTA, nicht gepflegt.
     Ein Stichwort in Grossbuchstaben (STANDBEIN, ENERGIE …) macht den Beitrag
     zum Lead-Post, alles andere zaehlt als Reichweite.
     🚨 Das ist eine Ableitung und keine Angabe. Sie steht deshalb sichtbar auf
     jeder Karte — ein Fehlschluss soll auffallen, nicht still in der Bilanz
     mitlaufen. */
  function ctaStichwort(b) {
    var text = b.caption || "";
    if (b.art === "karussells") {
      (b.obj.slides || []).forEach(function (s) {
        text += " " + (s.headline || "") + " " + (s.body || "") + " " + (s.keyword || "");
      });
    }
    var worte = text.split(/[^A-Za-z0-9\\u00c4\\u00d6\\u00dc\\u00e4\\u00f6\\u00fc\\u00df]+/);
    for (var i = 0; i < worte.length; i++) {
      var w = worte[i];
      if (w.length < 4) continue;
      if (w !== w.toUpperCase()) continue;
      if (!/[A-Z\\u00c4\\u00d6\\u00dc]/.test(w)) continue;   // reine Zahlen raus
      if (TP_KEINWORT[w]) continue;
      return w;
    }
    return "";
  }

  /* Woerter in Grossbuchstaben, die kein Stichwort sind. Kurz halten: jeder
     Eintrag hier kann einen echten Lead-Post unsichtbar machen. */
  var TP_KEINWORT = { ABER: 1, AUCH: 1, DANN: 1, DEIN: 1, DEINE: 1, MEIN: 1,
                      MEINE: 1, NICHT: 1, ODER: 1, ALLE: 1, OHNE: 1, JEDE: 1 };

  function jobVonBeitrag(b) { return ctaStichwort(b) ? "lead" : "reichweite"; }''',
    ),
    (
        "Startwoche merken",
        '''    if (tagesplanOffset === null) {
      tagesplanOffset = (!tpBelegteTage(0) && tpBelegteTage(1)) ? 1 : 0;
    }
    return tagesplanOffset;''',
        '''    if (wochenOffset === null) {
      wochenOffset = (!tpBelegteTage(0) && tpBelegteTage(1)) ? 1 : 0;
    }
    return wochenOffset;''',
    ),
    (
        "Merker beim Umschalten",
        '''    tpSpeichern(neu);
    tagesplanOffen = null;''',
        '''    tpSpeichern(neu);
    slotOffen = null;''',
    ),
    # ----------------------------------------------------------------------
    # 3 · Zwei Knoepfe in die Fusszeile der Karte
    # ----------------------------------------------------------------------
    (
        "Knoepfe in der Fusszeile",
        '''          '<button class="btn wk-ablehnen">Abgelehnt</button>' +
        '</div>' +''',
        '''          '<button class="btn wk-ablehnen">Abgelehnt</button>' +
          // Anderes Datum: das Feld links setzt den Tag auch, aber wer einen
          // Beitrag verschiebt, will danach wissen, dass die Freigabe weg ist.
          // Das sagt nur dieser Weg.
          '<button class="btn wk-umplan">Anderes Datum</button>' +
          '<span class="wk-umplanbox" hidden>' +
            '<input type="date" class="wk-neudatum" value="' + esc(b.obj.datum || "") + '">' +
            '<button class="btn primary wk-neuok">\\u00dcbernehmen</button>' +
          '</span>' +
          // 🚨 Zwei Klicks statt confirm(): ein Artifact-Rahmen darf Modals
          // blockieren, und ein lautlos wirkungsloser Loeschknopf waere
          // schlimmer als keiner.
          '<button class="btn wk-loeschen">L\\u00f6schen</button>' +
        '</div>' +''',
    ),
]


# ==========================================================================
# 4 · Blockweise: alte Funktionen raus, neue rein
# ==========================================================================

NEU_RENDERWOCHE = '''  /* =========================================================
     Wochen-Vorschau — der eine Ort zum Pruefen, Umstellen und Freigeben
     ========================================================= */

  function renderWoche(main) {
    var alleMit = alleBeitraege();
    var abgelehnt = alleMit.filter(istAbgelehnt);
    var beitraege = alleMit.filter(function (b) { return !istAbgelehnt(b); });

    beitraege.forEach(function (b) { wochenBildHolen(b.art, b.id); });

    var tage = tpTage(tpOffset());
    var belegt = tpBelegung();
    var frei = beitraege.filter(function (b) { return b.obj.textfrei; }).length;

    main.innerHTML =
      '<div class="page-head"><div><h1>Wochen-Vorschau</h1>' +
      '<p>Pro Tag und Profil ein Platz. \\u00dcber \\u201eWechseln\\u201c legst du die ' +
      'Variante drauf, die rausgehen soll \\u2014 die andere f\\u00e4llt zur\\u00fcck in die ' +
      'Ideenliste ganz unten. Storys stehen im Bild-Editor unter ' +
      '\\u201eAus deiner Planung\\u201c.</p></div>' +
      '<div class="head-actions">' +
        '<button class="btn" id="w-zurueck">\\u2190 Woche</button>' +
        '<span class="tp-kw">KW ' + tpKw(tage[0].datum) + ' \\u00b7 ' +
          wKurz(tage[0].datum) + '\\u2013' + wKurz(tage[4].datum) + '</span>' +
        '<button class="btn" id="w-vor">Woche \\u2192</button>' +
        (tpOffset() ? '<button class="btn ghost" id="w-heute">Diese Woche</button>' : "") +
        '<span class="chip">' + frei + ' von ' + beitraege.length + ' freigegeben</span>' +
      '</div></div>' +
      bilanzBlock(tage, belegt) +
      aufgabenBlock(beitraege) +
      '<div id="wliste"></div>' +
      '<div id="wunten"></div>';

    main.querySelector("#w-zurueck").onclick = function () {
      wochenOffset = tpOffset() - 1; slotOffen = null; render();
    };
    main.querySelector("#w-vor").onclick = function () {
      wochenOffset = tpOffset() + 1; slotOffen = null; render();
    };
    var heuteKnopf = main.querySelector("#w-heute");
    if (heuteKnopf) heuteKnopf.onclick = function () {
      wochenOffset = 0; slotOffen = null; render();
    };

    var liste = main.querySelector("#wliste");
    tage.forEach(function (t, i) {
      var soll = WOCHENRHYTHMUS[i] || "reels";
      var kopf = document.createElement("div");
      kopf.className = "wt-kopf";
      kopf.innerHTML = '<span class="wt-name">' + esc(tagName(t.iso)) + '</span>' +
        '<span class="wt-datum">' + esc(fmtDate(t.iso)) + '</span>' +
        '<span class="wt-soll">' +
          (soll === "reels" ? "Reel-Tag" : "Karussell-Tag") + '</span>';
      liste.appendChild(kopf);
      TP_PROFILE.forEach(function (p) {
        liste.appendChild(slotBlock(t, p, soll, belegt));
      });
    });

    main.querySelector("#wunten").appendChild(unterBlock(beitraege, abgelehnt));
  }

  function wKurz(d) {
    return String(d.getDate()).padStart(2, "0") + "." +
           String(d.getMonth() + 1).padStart(2, "0") + ".";
  }

  /* Soll/Ist je Profil — zwei Zeilen, weil zwei Dinge stimmen muessen:
     der Format-Mix und die CTA-Verteilung. */
  function bilanzBlock(tage, belegt) {
    var karten = TP_PROFILE.map(function (p) {
      var n = { reels: 0, karussells: 0 }, j = { lead: 0, reichweite: 0 };
      tage.forEach(function (t) {
        var l = belegt[t.iso + "|" + p.id] || [];
        if (l.length) { n[l[0].art]++; j[jobVonBeitrag(l[0])]++; }
      });
      var formOk = n.reels === TP_SOLL.reels && n.karussells === TP_SOLL.karussells;
      var jobOk = j.lead === TP_SOLL_JOB.lead && j.reichweite === TP_SOLL_JOB.reichweite;
      return '<div class="tp-bilanz' + (formOk && jobOk ? " ok" : "") + '">' +
        '<b>' + esc(p.label) + '</b>' +
        '<span' + (formOk ? ' class="ok"' : '') + '>' +
          n.reels + ' von ' + TP_SOLL.reels + ' Reels \\u00b7 ' +
          n.karussells + ' von ' + TP_SOLL.karussells + ' Karussells</span>' +
        '<span' + (jobOk ? ' class="ok"' : '') + '>' +
          j.lead + ' von ' + TP_SOLL_JOB.lead + ' Lead \\u00b7 ' +
          j.reichweite + ' von ' + TP_SOLL_JOB.reichweite + ' Reichweite</span>' +
        '</div>';
    }).join("");
    return '<div class="tp-bilanzen">' + karten + '</div>' +
      '<p class="note wbilanz-note">Lead oder Reichweite ist aus dem CTA ' +
      'abgelesen: ein Stichwort in Grossbuchstaben macht den Beitrag zum ' +
      'Lead-Post. Es steht auf jeder Karte \\u2014 wenn dort etwas Falsches ' +
      'steht, stimmt die Zahl oben auch nicht.</p>';
  }

  /* Ein Platz: Kopfzeile mit Wechseln-Knopf, darunter die volle Karte. */
  function slotBlock(t, p, soll, belegt) {
    var schluessel = t.iso + "|" + p.id;
    var alle = belegt[schluessel] || [];
    var drauf = alle[0] || null;
    var weitere = alle.slice(1);
    var vorrat = tpVorrat(p.id);
    var offen = slotOffen === schluessel;
    var anzahl = weitere.length + vorrat.length;

    var box = document.createElement("div");
    box.className = "wslot" + (drauf ? "" : " leer");

    var kopf = document.createElement("div");
    kopf.className = "wslot-kopf";
    var job = drauf ? jobVonBeitrag(drauf) : "";
    kopf.innerHTML =
      '<span class="wslot-profil">' + esc(p.label) + '</span>' +
      (drauf
        ? '<span class="wslot-job ' + job + '">' +
          (job === "lead" ? "Lead \\u00b7 " + esc(ctaStichwort(drauf)) : "Reichweite") +
          '</span>'
        : "") +
      (drauf && drauf.art !== soll
        ? '<span class="wslot-warn">heute w\\u00e4re ' +
          (soll === "reels" ? "ein Reel" : "ein Karussell") + ' dran</span>'
        : "") +
      '<button class="btn ghost wslot-auf">' +
        (offen ? "Liste zu" : (drauf ? "Wechseln" : "Ausw\\u00e4hlen")) +
        (anzahl ? ' <span class="tp-anz">' + anzahl + '</span>' : "") +
      '</button>';
    kopf.querySelector(".wslot-auf").onclick = function () {
      slotOffen = offen ? null : schluessel;
      render();
    };
    box.appendChild(kopf);

    if (offen) box.appendChild(variantenListe(schluessel, weitere, vorrat, soll, t, p));

    if (drauf) {
      box.appendChild(wochenKarte(drauf));
    } else {
      var leer = document.createElement("div");
      leer.className = "wslot-leer";
      leer.textContent = "Noch nichts geplant. Hier geh\\u00f6rt " +
        (soll === "reels" ? "ein Reel" : "ein Karussell") +
        " hin \\u2014 \\u00fcber \\u201eAusw\\u00e4hlen\\u201c aus der Ideenliste holen.";
      box.appendChild(leer);
    }
    return box;
  }

  /* Die Varianten zu einem Platz: was noch am selben Tag liegt, dann der
     Vorrat ohne Datum. Das passende Format zuerst — bei zehn Eintraegen ist
     die Reihenfolge die halbe Bedienung. */
  function variantenListe(schluessel, weitere, vorrat, soll, t, p) {
    var box = document.createElement("div");
    box.className = "tp-alts";

    var eintraege = weitere.map(function (b) {
      return { b: b, hinweis: "liegt auch an diesem Tag" };
    }).concat(vorrat.map(function (b) {
      return { b: b, hinweis: "" };
    }));

    if (!eintraege.length) {
      box.innerHTML = '<div class="tp-keine">Nichts im Vorrat f\\u00fcr dieses ' +
        'Profil. Was ohne Datum dasteht, findest du unten in der Ideenliste.</div>';
      return box;
    }

    eintraege.sort(function (x, y) {
      return (x.b.art === soll ? 0 : 1) - (y.b.art === soll ? 0 : 1);
    });

    eintraege.forEach(function (e) {
      var j = jobVonBeitrag(e.b);
      var k = document.createElement("button");
      k.className = "tp-alt";
      k.innerHTML =
        '<span class="tp-format">' + esc(e.b.format) + '</span>' +
        '<span class="tp-althook">' + esc(e.b.hook || e.b.titel) + '</span>' +
        '<span class="tp-job ' + j + '">' + (j === "lead" ? "Lead" : "Reichweite") + '</span>' +
        (e.hinweis ? '<span class="tp-hinweis">' + esc(e.hinweis) + '</span>' : "");
      k.onclick = function () {
        var alt = (tpBelegung()[schluessel] || [])[0] || null;
        tpBelegen(e.b, alt, t.iso, p.id);
      };
      box.appendChild(k);
    });
    return box;
  }

  /* Neu einplanen. 🚨 War der Beitrag schon freigegeben oder eingeplant, wird
     das zurueckgesetzt — sonst laesst der 20:00-Lauf ihn liegen, weil er als
     erledigt gilt, und sie wartet auf einen Post, der nie kommt. */
  function umplanen(b, neu) {
    if (!/^\\d{4}-\\d{2}-\\d{2}$/.test(neu)) {
      toast("Das war kein Datum.");
      return;
    }
    b.obj.datum = neu;
    var zurueck = false;
    if (b.obj.textfrei) { b.obj.textfrei = false; zurueck = true; }
    if (b.obj.blotato && b.obj.blotato.status) { b.obj.blotato.status = ""; zurueck = true; }
    tpSpeichern(b);
    toast(b.titel + " liegt jetzt auf " + tagName(neu) + ", " + fmtDate(neu) +
      (zurueck ? " \\u2014 Freigabe ist zur\\u00fcckgenommen, gib ihn neu frei." : "."));
    render();
  }

  /* Endgueltig weg. Patricias Entscheid 19.09.2026 auf die Rueckfrage, ob
     „Loeschen" in die Ideenliste legen oder wirklich loeschen soll.
     🚨 Das Artifact hat keine Historie — was hier weg ist, ist weg. Deshalb
     zwei Klicks, und deshalb steht der Beitrags-Text zusaetzlich als Datei in
     outputs/content/ (scripts/cockpit/inhalte-sichern.py). */
  function beitragLoeschen(b) {
    if (b.art === "reels") {
      state.reels = state.reels.filter(function (x) { return x.id !== b.id; });
      lsSet("reelliste", state.reels.map(function (x) { return x.id; }));
      if (db) db.collection("reels").doc(b.id).delete().catch(function () {});
    } else if (b.art === "karussells") {
      state.karussells = state.karussells.filter(function (x) { return x.id !== b.id; });
      lsSet("karliste", state.karussells.map(function (x) { return x.id; }));
      if (db) db.collection("karussells").doc(b.id).delete().catch(function () {});
    } else {
      state.storys = state.storys.filter(function (x) { return x.id !== b.id; });
      lsSet("storyliste", state.storys.map(function (x) { return x.id; }));
      if (db) db.collection("storys").doc(b.id).delete().catch(function () {});
    }
    toast(b.titel + " ist gel\\u00f6scht.");
    render();
  }

  /* ---- die zwei Uebersichten am Schluss ---------------------------------
     Die Wochenansicht oben zeigt nur die laufende Woche. Damit nichts aus dem
     Blick faellt, stehen hier ALLE Termine ueber alle Wochen, und daneben
     alles ohne Datum. */
  function unterBlock(beitraege, abgelehnt) {
    var box = document.createElement("div");

    var echte = beitraege.filter(function (b) { return !istLeer(b); });
    var mitDatum = echte.filter(function (b) { return b.obj.datum; })
      .sort(function (a, c) { return a.obj.datum < c.obj.datum ? -1 : 1; });
    var ohneDatum = echte.filter(function (b) { return !b.obj.datum; });

    // --- Was wann rausgeht ---------------------------------------------
    var plan = document.createElement("div");
    plan.className = "panel uebersicht";
    plan.innerHTML = '<h2>Was wann rausgeht</h2>' +
      '<p class="note">Alle ' + mitDatum.length + ' Beitr\\u00e4ge mit Datum, ' +
      '\\u00fcber alle Wochen \\u2014 auch die, die oben gerade nicht im Bild sind.</p>';
    if (!mitDatum.length) {
      plan.innerHTML += '<div class="empty">Noch nichts eingeplant.</div>';
    } else {
      var letzte = "";
      mitDatum.forEach(function (b) {
        var s = tpStand(b), j = jobVonBeitrag(b);
        var z = document.createElement("div");
        z.className = "uezeile" + (b.obj.datum !== letzte ? " neu" : "");
        letzte = b.obj.datum;
        z.innerHTML =
          '<span class="uedatum">' + esc(tagName(b.obj.datum).slice(0, 2) + " " +
            fmtDate(b.obj.datum)) + '</span>' +
          '<span class="uepro">' +
            (kartenProfil(b.obj) === "doterra" ? "doTERRA" : "Mum Life") + '</span>' +
          '<span class="tp-format">' + esc(b.format) + '</span>' +
          '<span class="tp-job ' + j + '">' + (j === "lead" ? "Lead" : "Reichweite") + '</span>' +
          '<span class="uehook">' + esc(b.hook || b.titel) + '</span>' +
          '<span class="tp-stand ' + s.art + '">' + esc(s.text) + '</span>';
        plan.appendChild(z);
      });
    }
    box.appendChild(plan);

    // --- Ideenliste ------------------------------------------------------
    var ideen = document.createElement("div");
    ideen.className = "panel uebersicht";
    ideen.innerHTML = '<h2>Ideenliste</h2>' +
      '<p class="note">' + ohneDatum.length + ' Beitr\\u00e4ge ohne Datum. Sie kommen ' +
      '\\u00fcber \\u201eWechseln\\u201c oben auf einen Platz \\u2014 oder du setzt hier ' +
      'direkt einen Tag.</p>';
    if (!ohneDatum.length) {
      ideen.innerHTML += '<div class="empty">Leer \\u2014 alles ist eingeplant.</div>';
    } else {
      ohneDatum.sort(function (a, c) {
        return (a.format + a.titel) < (c.format + c.titel) ? -1 : 1;
      }).forEach(function (b) {
        var j = jobVonBeitrag(b);
        var z = document.createElement("div");
        z.className = "uezeile idee";
        z.innerHTML =
          '<span class="uepro">' +
            (kartenProfil(b.obj) === "doterra" ? "doTERRA" : "Mum Life") + '</span>' +
          '<span class="tp-format">' + esc(b.format) + '</span>' +
          '<span class="tp-job ' + j + '">' + (j === "lead" ? "Lead" : "Reichweite") + '</span>' +
          '<span class="uehook">' + esc(b.hook || b.titel) + '</span>' +
          '<input type="date" class="uedat">';
        z.querySelector(".uedat").onchange = function () {
          if (this.value) umplanen(b, this.value);
        };
        ideen.appendChild(z);
      });
    }
    box.appendChild(ideen);

    // --- Aussortiertes, klein und unten, mit Rueckweg --------------------
    if (abgelehnt.length) {
      var ab = document.createElement("div");
      ab.className = "panel abliste";
      ab.innerHTML = '<h2>Abgelehnt (' + abgelehnt.length + ')</h2>' +
        '<p class="note">Aus allen Arbeitsansichten raus, aber nicht gel\\u00f6scht.</p>';
      abgelehnt.sort(function (x, y) {
        return (y.obj.abgelehntStand || "") < (x.obj.abgelehntStand || "") ? -1 : 1;
      }).forEach(function (b) {
        var z = document.createElement("div");
        z.className = "abzeile2";
        z.innerHTML = '<span class="tudatum">' + esc(b.format) + '</span>' +
          '<span>' + esc(b.titel) + '</span>';
        var zurueck = document.createElement("button");
        zurueck.className = "btn";
        zurueck.textContent = "Zur\\u00fcckholen";
        zurueck.onclick = function () {
          b.obj.abgelehnt = false;
          if (b.art === "reels") saveReel(b.obj);
          else if (b.art === "storys") saveStory(b.obj);
          else saveCarousel(b.obj);
          toast("Wieder da.");
          render();
        };
        z.appendChild(zurueck);
        ab.appendChild(z);
      });
      box.appendChild(ab);
    }

    return box;
  }

'''


BLOECKE = [
    (
        "renderWoche ersetzen",
        "  function renderWoche(main) {",
        "  /* Was an einem Beitrag fehlt, und wer dafuer zustaendig ist.",
        NEU_RENDERWOCHE + "  /* Was an einem Beitrag fehlt, und wer dafuer zustaendig ist.",
    ),
    (
        "tagesplanZahl entfernen",
        "  /* Wie viele der zehn Plaetze belegt sind",
        "  /* Ein Satz zum Zustand",
        "  /* Ein Satz zum Zustand",
    ),
    (
        "tpMini, tpZeile und renderTagesplan entfernen",
        "  function tpMini(b) {",
        "  function renderNav() {",
        "  function renderNav() {",
    ),
]


# ==========================================================================
# 5 · Die Handler fuer die zwei neuen Knoepfe, ans Ende von wochenKarte
# ==========================================================================
ANKER_HANDLER = '''    var freigabeKnopf = karte.querySelector(".wk-frei");'''
NEU_HANDLER = '''    // Anderes Datum: Feld einblenden, dann uebernehmen.
    var umplanKnopf = karte.querySelector(".wk-umplan");
    if (umplanKnopf) {
      var umplanBox = karte.querySelector(".wk-umplanbox");
      umplanKnopf.onclick = function () {
        umplanBox.hidden = !umplanBox.hidden;
        if (!umplanBox.hidden) umplanBox.querySelector(".wk-neudatum").focus();
      };
      karte.querySelector(".wk-neuok").onclick = function () {
        umplanen(b, karte.querySelector(".wk-neudatum").value);
      };
    }

    // 🚨 Loeschen in zwei Klicks. Kein confirm() — im Artifact-Rahmen kann ein
    // Modal blockiert sein, und dann taete der Knopf lautlos nichts. Der
    // zweite Klick faellt nach acht Sekunden wieder zurueck, damit ein
    // scharfer Knopf nicht stehen bleibt.
    var loeschKnopf = karte.querySelector(".wk-loeschen");
    if (loeschKnopf) {
      var scharf = null;
      loeschKnopf.onclick = function () {
        if (scharf) {
          clearTimeout(scharf);
          beitragLoeschen(b);
          return;
        }
        loeschKnopf.classList.add("scharf");
        loeschKnopf.textContent = "Wirklich l\\u00f6schen? Das bleibt weg.";
        scharf = setTimeout(function () {
          scharf = null;
          loeschKnopf.classList.remove("scharf");
          loeschKnopf.textContent = "L\\u00f6schen";
        }, 8000);
      };
    }

    var freigabeKnopf = karte.querySelector(".wk-frei");'''


# ==========================================================================
# 6 · CSS
# ==========================================================================
ANKER_CSS = '''  /* ---------- Wochen-Vorschau ---------- */'''
NEU_CSS = '''  /* ---------- Wochenraster: Platz je Tag und Profil ---------- */
  .wt-kopf .wt-soll {
    font-size: 10px; letter-spacing: 0.09em; text-transform: uppercase;
    color: var(--ink-soft); background: var(--surface-2);
    padding: 2px 9px; border-radius: 999px;
  }
  .wslot { margin-bottom: 6px; }
  .wslot-kopf {
    display: flex; align-items: center; gap: 9px; flex-wrap: wrap;
    padding: 4px 2px 7px;
  }
  .wslot-profil {
    font-size: 10px; letter-spacing: 0.09em; text-transform: uppercase;
    color: var(--ink-soft);
  }
  .wslot-job, .tp-job {
    font-size: 10px; letter-spacing: 0.04em; padding: 2px 9px;
    border-radius: 999px; white-space: nowrap;
  }
  .wslot-job.lead, .tp-job.lead { background: var(--teal-soft); color: var(--teal); }
  .wslot-job.reichweite, .tp-job.reichweite { background: var(--orange-soft); color: var(--orange); }
  .wslot-warn { font-size: 12px; color: var(--orange); }
  .wslot-kopf .btn { margin-left: auto; font-size: 12px; padding: 5px 10px; }
  .wslot-leer {
    border: 1px dashed var(--line-strong); border-radius: var(--r);
    padding: 18px 16px; color: var(--ink-soft); font-style: italic;
    font-size: 13px; margin-bottom: 12px;
  }
  .wbilanz-note { margin: -12px 0 18px; }
  .tp-bilanz span.ok { color: var(--good); }
  .tp-bilanz { flex-direction: column; align-items: flex-start; gap: 2px; }
  .tp-bilanz b { margin-bottom: 2px; }

  /* Die zwei Uebersichten am Schluss der Wochen-Vorschau */
  .uebersicht { margin-top: 24px; }
  .uezeile {
    display: grid; grid-template-columns: 104px 74px 76px 86px 1fr 150px;
    gap: 10px; padding: 6px 0; border-top: 1px solid var(--line);
    font-size: 13px; align-items: center;
  }
  .uezeile.idee { grid-template-columns: 74px 76px 86px 1fr 142px; }
  .uezeile.neu { border-top-color: var(--line-strong); }
  .uedatum { font-size: 12px; color: var(--ink-soft); font-variant-numeric: tabular-nums; }
  .uepro { font-size: 11px; color: var(--ink-soft); }
  .uehook { min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .uedat {
    background: var(--ground); border: 1px solid var(--line); border-radius: 7px;
    padding: 5px 7px; font-size: 12px; width: 100%;
  }
  .uedat:focus { border-color: var(--teal); outline: none; }
  @media (max-width: 860px) {
    .uezeile, .uezeile.idee { grid-template-columns: 1fr auto; }
    .uehook { grid-column: 1 / -1; white-space: normal; }
  }

  /* Anderes Datum und Loeschen auf der Karte */
  .wk-umplanbox { display: inline-flex; gap: 6px; align-items: center; }
  .wk-umplanbox input[type="date"] {
    background: var(--ground); border: 1px solid var(--line);
    border-radius: 7px; padding: 6px 8px; font-size: 12px;
  }
  .wk-loeschen.scharf {
    background: var(--crit); border-color: var(--crit); color: #fbf8f1;
  }
  .wk-loeschen.scharf:hover { color: #fbf8f1; filter: brightness(1.08); }

  /* ---------- Wochen-Vorschau ---------- */'''


def block_ersetzen(html: str, name: str, start: str, ende: str, neu: str) -> str:
    """Schneidet von `start` bis `ende` heraus und setzt `neu` ein."""
    if html.count(start) != 1:
        sys.exit(f"Anker-Start „{name}“ kommt {html.count(start)}x vor (erwartet: 1).")
    i = html.index(start)
    j = html.find(ende, i)
    if j < 0:
        sys.exit(f"Anker-Ende „{name}“ nicht hinter dem Start gefunden.")
    return html[:i] + neu + html[j + len(ende):]


def js_pruefen(html: str) -> None:
    """node --check ueber das eingebettete Skript.

    🚨 Pflicht vor jedem Publish: ein deutsches Anfuehrungszeichen in einer
    JS-Zeichenkette hat schon einmal die ganze Seite totgelegt.
    """
    bloecke = re.findall(r"<script>(.*?)</script>", html, re.S)
    if not bloecke:
        sys.exit("Kein <script>-Block gefunden — das kann nicht stimmen.")
    grosse = max(bloecke, key=len)
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False,
                                     encoding="utf-8") as f:
        f.write(grosse)
        pfad = f.name
    try:
        r = subprocess.run(["node", "--check", pfad], capture_output=True, text=True)
        if r.returncode:
            sys.exit("node --check schlaegt fehl:\n" + (r.stderr or r.stdout))
    finally:
        os.unlink(pfad)
    print("  node --check: in Ordnung")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("datei", nargs="?", type=pathlib.Path, default=STANDARD)
    a = p.parse_args()
    if not a.datei.exists():
        sys.exit(f"Nicht gefunden: {a.datei}")

    html = a.datei.read_text(encoding="utf-8")
    if "WOCHENRHYTHMUS" in html:
        print("Der Umbau steckt schon drin — nichts zu tun.")
        return 0
    if "renderTagesplan" not in html:
        sys.exit("Kein Tagesplan gefunden — laeuft dieses Skript gegen die "
                 "richtige Datei?")

    for name, alt, neu in ERSETZUNGEN:
        n = html.count(alt)
        if n != 1:
            sys.exit(f"Anker „{name}“ kommt {n}x vor (erwartet: 1) — nichts geaendert.")
        html = html.replace(alt, neu)
        print(f"  gesetzt: {name}")

    for name, start, ende, neu in BLOECKE:
        html = block_ersetzen(html, name, start, ende, neu)
        print(f"  gesetzt: {name}")

    for name, alt, neu in [("Handler fuer die neuen Knoepfe", ANKER_HANDLER, NEU_HANDLER),
                           ("CSS", ANKER_CSS, NEU_CSS)]:
        n = html.count(alt)
        if n != 1:
            sys.exit(f"Anker „{name}“ kommt {n}x vor (erwartet: 1) — nichts geaendert.")
        html = html.replace(alt, neu)
        print(f"  gesetzt: {name}")

    # Gegenprobe: nichts vom Tagesplan darf uebrig bleiben.
    for rest in ("renderTagesplan", "tagesplanZahl", "tagesplanOffset",
                 "tagesplanOffen", "tpMini", "tpZeile"):
        if rest in html:
            sys.exit(f"„{rest}“ steht noch in der Datei — der Umbau ist halb.")
    print("  Gegenprobe: kein Tagesplan-Rest")

    js_pruefen(html)

    # 🚨 Nie in die Zieldatei schreiben, solange etwas schiefgehen kann:
    # open(pfad, "w") leert sie sofort, und ein Fehler danach laesst nichts
    # uebrig. Erst daneben schreiben, dann umbenennen.
    neben = a.datei.with_suffix(a.datei.suffix + ".neu")
    neben.write_text(html, encoding="utf-8")
    os.replace(neben, a.datei)
    print(f"\nFertig: {a.datei}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
