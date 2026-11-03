  /* =========================================================
     Team-Funke (03.11.2026) — die Wochennachricht fürs doTERRA-Team
     Patricia: „gleichzeitig würde ich gerne damit auch mein Team motivieren.
     ich muss da wieder mehr leben reinbringen.“
     Sie trägt Erfolge und Aktion der Woche ein, hakt an, wer kurz vor dem nächsten
     Schritt steht, wählt die Wochen-Challenge — Claude schreibt über `sample` die
     Gruppennachricht und je eine kurze persönliche Nachricht. Verschickt wird nichts:
     sie kopiert, passt an, schickt selbst.
     Daten in daten/rising-leaders (gehört Patricia): funke = { entwurf, verlauf: [] }
     ========================================================= */
  var TF_CHALLENGES = [
    { id: "plaetze", titel: "Drei-Plätze-Story", wie: "Eine Story posten: „Ich nehme diesen Monat drei Menschen mit, die neu starten möchten.“ Einfaches Foto, wer antwortet, bekommt die Infos per Nachricht." },
    { id: "sprachnachricht", titel: "Eine Sprachnachricht", wie: "Einer Kundin, von der ihr länger nichts gehört habt, eine kurze Sprachnachricht schicken: einfach fragen, wie es ihr geht." },
    { id: "moeglich", titel: "Was es mir möglich macht", wie: "Einmal diese Woche in Story oder Status erzählen, was euch das Business möglich macht. Ein echter Moment reicht." },
    { id: "treue", titel: "Drei Mal Treueprogramm", wie: "Drei Kundinnen fragen, ob sie ihre Öle jeden Monat zum besten Preis bekommen möchten." },
    { id: "zuhoeren", titel: "Nur zuhören", wie: "Eine Kundin fragen, wie es ihr mit ihren Ölen geht. Kein Angebot, nur zuhören." },
    { id: "aktion", titel: "Aktion persönlich", wie: "Die Aktion der Woche zwei Kundinnen persönlich schicken, mit einem Satz, warum ihr an sie gedacht habt." },
    { id: "business", titel: "Eine Person fürs Business", wie: "Eine Person ansprechen, die viel bestellt oder die Öle schon von sich aus weitergibt. Nur die Möglichkeit ins Feld geben." },
    { id: "flamme", titel: "Jeder Erfolg zählt", wie: "Jeden Erfolg der Woche mit 🔥 in die Gruppe posten: jede Einschreibung, jede Treueprogramm-Bestellung, jedes gute Gespräch." }
  ];
  var tfLaeuft = false, tfFehler = "";

  function tfDaten() {
    var F = dtRising.funke || (dtRising.funke = {});
    if (!F.entwurf) F.entwurf = { erfolge: "", aktion: "", fastda: {}, challenge: "", gruppe: "", persoenlich: [] };
    if (!F.verlauf) F.verlauf = [];
    return F;
  }
  function tfVorname(name) {
    var p = String(name || "").split(",");
    return (p.length > 1 ? p[1] : p[0]).trim().split(" ")[0];
  }
  // Wer steht kurz vor dem nächsten Schritt? Nur als Hinweis für Patricia — Zahlen gehen nie in die Nachricht.
  function tfFastDa() {
    var out = [];
    if (!doterra || !doterra.beine) return out;
    doterra.beine.forEach(function (b) {
      var ov = (b.zu_naechstem || []).filter(function (x) { return x.was === "OV"; })[0];
      if (ov && ov.fehlt <= 800 && (b.zu_naechstem || []).length === 1) {
        out.push({ id: b.name, vorname: tfVorname(b.name), was: b.naechster, fehlt: ov.fehlt });
      }
      (b.leute || []).forEach(function (p) {
        var z = (p.zu_executive || []).filter(function (x) { return x.was === "OV"; })[0];
        if (z && z.fehlt <= 600) out.push({ id: p.name, vorname: tfVorname(p.name), was: "Executive", fehlt: z.fehlt });
      });
    });
    return out;
  }
  function tfNaechsteChallenge() {
    var F = tfDaten();
    var zuletzt = F.verlauf.slice(-4).map(function (v) { return v.challenge; });
    var frei = TF_CHALLENGES.filter(function (c) { return zuletzt.indexOf(c.id) < 0; });
    return (frei[0] || TF_CHALLENGES[0]).id;
  }
  // Fällig ab Sonntag, solange in den letzten sechs Tagen keine verschickt wurde.
  function tfFaellig() {
    var F = dtRising.funke || {};
    var letzte = (F.verlauf || []).slice(-1)[0];
    var heute = trHeute();
    if (letzte && letzte.datum >= trVerschoben(heute, -6)) return false;
    var tag = new Date(heute + "T12:00:00").getDay();
    return tag === 0 || tag === 1 || tag === 2;
  }

  function tfHtml() {
    var F = tfDaten(), E = F.entwurf;
    if (!E.challenge) E.challenge = tfNaechsteChallenge();
    var fast = tfFastDa();
    var ch = TF_CHALLENGES.filter(function (c) { return c.id === E.challenge; })[0] || TF_CHALLENGES[0];
    var letzte = F.verlauf.slice(-1)[0];

    var h = '<details class="panel tf"' + (tfFaellig() || E.gruppe ? " open" : "") + '>' +
      '<summary><span class="tf-titel">✨ Team-Funke</span>' +
      '<span class="note">' + (tfFaellig() ? "für diese Woche fällig" :
        (letzte ? "zuletzt am " + esc(dtDatum(letzte.datum)) : "die Wochennachricht für dein Team")) + '</span></summary>' +
      '<p class="note">Einmal die Woche, am besten sonntags: Du trägst ein, was gelaufen ist, ich schreibe die Nachricht für eure Gruppe. Verschickt wird nichts, das machst du selbst.</p>' +
      '<label class="tf-feld"><span>Was lief diese Woche gut?</span>' +
      '<textarea data-tf="erfolge" rows="3" placeholder="Mit Vornamen, z. B.: zwei Kundinnen neu im Treueprogramm, ein erster Öle-Abend">' + esc(E.erfolge) + '</textarea></label>' +
      '<label class="tf-feld"><span>Aktion oder Termin der Woche (optional)</span>' +
      '<input data-tf="aktion" value="' + esc(E.aktion) + '" placeholder="z. B. BOGO bis Freitag · Social-Media-Call Do 12.11., 12:00" autocomplete="off"></label>';

    if (fast.length) {
      h += '<div class="tf-feld"><span>Kurz vor dem nächsten Schritt <em class="note">nur für dich, Stand ' + esc(monatKlar(doterra.monat)) +
        '. In der Nachricht stehen keine Zahlen.</em></span><div class="tf-fast">';
      fast.forEach(function (p) {
        h += '<label class="tf-person"><input type="checkbox" data-tffast="' + esc(p.id) + '"' + (E.fastda[p.id] ? " checked" : "") + '> ' +
          '<b>' + esc(p.vorname) + '</b> <span class="note">→ ' + esc(p.was) + ', fehlt ' + zahlKurz(p.fehlt) + ' OV</span></label>';
      });
      h += '</div></div>';
    }

    h += '<label class="tf-feld"><span>Challenge der Woche</span><select data-tf="challenge">' +
      TF_CHALLENGES.map(function (c) {
        return '<option value="' + c.id + '"' + (c.id === E.challenge ? " selected" : "") + '>' + esc(c.titel) + '</option>';
      }).join("") + '</select><em class="note">' + esc(ch.wie) + '</em></label>' +
      '<div class="tf-los"><button class="btn primary" type="button" id="tf-los"' + (tfLaeuft || !sampler ? " disabled" : "") + '>' +
      (tfLaeuft ? "Ich schreibe …" : (E.gruppe ? "Neu schreiben" : "Nachricht schreiben")) + '</button>' +
      (!sampler ? '<span class="note">Geht nur im Cockpit auf claude.ai.</span>' : "") +
      (tfFehler ? '<span class="note tf-fehler">Hat nicht geklappt (' + esc(tfFehler) + '). Nochmal versuchen.</span>' : "") + '</div>';

    if (E.gruppe) {
      h += '<div class="tf-ergebnis"><h3>Für die Gruppe</h3>' +
        '<textarea data-tf="gruppe" rows="12">' + esc(E.gruppe) + '</textarea>' +
        '<div class="dt-knoepfe"><button class="btn primary" type="button" data-tfkopie="gruppe">Kopieren</button></div>';
      (E.persoenlich || []).forEach(function (p, i) {
        h += '<h3>Persönlich an ' + esc(p.name) + '</h3><textarea data-tfp="' + i + '" rows="4">' + esc(p.text) + '</textarea>' +
          '<div class="dt-knoepfe"><button class="btn" type="button" data-tfkopie="p' + i + '">Kopieren</button></div>';
      });
      h += '<div class="tf-fertig"><button class="btn" type="button" id="tf-raus">Hab ich verschickt</button>' +
        '<span class="note">Legt sie in den Verlauf, damit die Challenge nächste Woche wechselt.</span></div></div>';
    }

    if (F.verlauf.length) {
      h += '<details class="tf-verlauf"><summary>' + F.verlauf.length + ' verschickt</summary>' +
        F.verlauf.slice().reverse().slice(0, 12).map(function (v) {
          var c = TF_CHALLENGES.filter(function (x) { return x.id === v.challenge; })[0];
          return '<div class="tf-vz"><span>' + esc(dtDatum(v.datum)) + '</span><span>' + esc(c ? c.titel : v.challenge) + '</span></div>';
        }).join("") + '</details>';
    }
    return h + '</details>';
  }

  function tfSchreiben() {
    var F = tfDaten(), E = F.entwurf;
    if (!sampler || tfLaeuft) return;
    var fast = tfFastDa().filter(function (p) { return E.fastda[p.id]; });
    var ch = TF_CHALLENGES.filter(function (c) { return c.id === E.challenge; })[0] || TF_CHALLENGES[0];
    var p = "Du schreibst für Patricia Ulmann die Wochennachricht an ihr doTERRA-Team (Telegram- oder WhatsApp-Gruppe, " +
      "Beraterinnen und Kundinnen, die teilen; es sind auch Männer dabei).\n\n" +
      "ZIEL: wieder Leben ins Team bringen. Die Leute sollen sich gesehen fühlen, Lust bekommen, diese Woche eine kleine Sache zu tun, und in der Gruppe antworten.\n\n" +
      "STIMME: wie eine Freundin, warm, direkt, ehrlich. Ganze, ruhige Sätze, kein Stakkato. Du-Form an alle mit „ihr“. " +
      "Begrüssung, die alle meint (z. B. „Ihr Lieben“), nie „Mädels“ oder „Ladies“. Schweizer Rechtschreibung mit ss. Echte Umlaute. " +
      "Höchstens vier Emojis in der ganzen Nachricht. Für WhatsApp darf ein Wort mit *Sternchen* fett sein, sonst kein Markdown.\n\n" +
      "VERBOTEN: Heilversprechen oder Wirkaussagen zu Ölen · Einkommens- oder Rangversprechen · Zahlen zu Volumen, OV, PV oder Geld · " +
      "erfundene Erfolge, Namen, Szenen oder Zahlen · die Satzform „nicht X, sondern Y“ und jedes „sondern“ · " +
      "KI-Floskeln wie „Lass uns gemeinsam“, „Reise“, „Gamechanger“, „Mindset-Shift“ · Druck oder schlechtes Gewissen.\n\n" +
      "AUFBAU der Gruppennachricht (120 bis 180 Wörter):\n" +
      "1. Ein warmer Einstieg, ein Satz.\n" +
      "2. Die Erfolge feiern, genau mit den Namen und Dingen, die Patricia aufgeschrieben hat. Steht dort nichts, feiere allgemein, dass ihr dranbleibt, ohne etwas zu erfinden.\n" +
      "3. Falls Namen unter „kurz vor dem nächsten Schritt“ stehen: sie ermutigend erwähnen („ihr seid so nah dran“), ohne Rang und ohne Zahlen.\n" +
      "4. Die Challenge der Woche, konkret, so dass man sofort weiss, was zu tun ist.\n" +
      "5. Falls eine Aktion oder ein Termin da ist: ein Satz dazu.\n" +
      "6. Schluss: eine einfache Bitte zu antworten, z. B. mit 🔥, sobald man die Challenge gemacht hat.\n\n" +
      "Dazu für JEDE Person unter „kurz vor dem nächsten Schritt“ eine kurze persönliche Nachricht (2 bis 4 Sätze, per Vorname, " +
      "ohne Zahlen): ehrlich anerkennen, was sie macht, und anbieten, gemeinsam zu schauen, was diesen Monat noch geht.\n\n" +
      "PATRICIAS ANGABEN\n" +
      "Erfolge dieser Woche: " + (E.erfolge.trim() || "(nichts eingetragen)") + "\n" +
      "Aktion oder Termin: " + (E.aktion.trim() || "(keine)") + "\n" +
      "Kurz vor dem nächsten Schritt: " + (fast.length ? fast.map(function (x) { return x.vorname; }).join(", ") : "(niemand)") + "\n" +
      "Challenge: " + ch.titel + " — " + ch.wie + "\n\n" +
      'Antworte als JSON: {"gruppe": "die Gruppennachricht, Absätze mit Zeilenumbruch", "persoenlich": [{"name": "Vorname", "text": "…"}]}';
    tfLaeuft = true; tfFehler = ""; render();
    sampler.json(p, { modelTier: "complex", cache: false }).then(function (r) {
      E.gruppe = (r && r.gruppe) || "";
      E.persoenlich = (r && Array.isArray(r.persoenlich)) ? r.persoenlich.filter(function (x) { return x && x.text; }) : [];
      if (!E.gruppe) tfFehler = "leer zurückgekommen";
      dtRisingSpeichern();
    }).catch(function (e) {
      tfFehler = (e && e.code) || "Fehler";
    }).then(function () { tfLaeuft = false; render(); });
  }

  function tfBinden(main) {
    var F = tfDaten(), E = F.entwurf;
    main.querySelectorAll("[data-tf]").forEach(function (f) {
      var feld = f.dataset.tf;
      if (feld === "challenge") {
        f.onchange = function () { E.challenge = f.value; dtRisingSpeichern(); render(); };
      } else {
        f.oninput = function () { E[feld] = f.value; dtRisingSpeichern(); };
      }
    });
    main.querySelectorAll("[data-tfp]").forEach(function (f) {
      f.oninput = function () { var x = E.persoenlich[Number(f.dataset.tfp)]; if (x) { x.text = f.value; dtRisingSpeichern(); } };
    });
    main.querySelectorAll("[data-tffast]").forEach(function (c) {
      c.onchange = function () { E.fastda[c.dataset.tffast] = c.checked; dtRisingSpeichern(); };
    });
    var los = main.querySelector("#tf-los");
    if (los) los.onclick = tfSchreiben;
    main.querySelectorAll("[data-tfkopie]").forEach(function (b) {
      b.onclick = function () {
        var k = b.dataset.tfkopie;
        var text = k === "gruppe" ? E.gruppe : ((E.persoenlich[Number(k.slice(1))] || {}).text || "");
        dtKopieren(text, b);
      };
    });
    var raus = main.querySelector("#tf-raus");
    if (raus) raus.onclick = function () {
      F.verlauf.push({ datum: trHeute(), challenge: E.challenge, gruppe: E.gruppe, erfolge: E.erfolge });
      F.entwurf = { erfolge: "", aktion: "", fastda: {}, challenge: "", gruppe: "", persoenlich: [] };
      dtRisingSpeichern(); render();
      toast("Im Verlauf. Nächste Woche kommt eine neue Challenge ✨");
    };
  }
