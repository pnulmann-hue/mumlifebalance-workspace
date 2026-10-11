  /* Fokus-Ansicht (08.10.2026, Version 94). Patricia am Handy: „das ganze ist etwas
     fummelig“ — zehn schmale Karten nebeneinander, die Vorschau scrollte weg, während
     sie unten an den Reglern zog. Jetzt: oben Miniaturen zum Antippen, darunter EINE
     Folie gross, die Vorschau bleibt beim Scrollen stehen. */
  var aktiveFolie = {};

  /* 🚨 An jeder Folie hängen zur Laufzeit __draw (Funktion) und __mini (Canvas).
     Die Datenbank nimmt nur reines JSON — vorher gingen sie mit und die Seite
     meldete „nur lokal gespeichert“. Alles mit __ bleibt draussen. */
  function framesSauber(frames) {
    return JSON.parse(JSON.stringify(frames || [], function (k, v) {
      return k.indexOf("__") === 0 ? undefined : v;
    }));
  }

  function renderStoryStrip(strip, st) {
    strip.innerHTML = "";
    strip.className = "storystrip st-neu";
    var n = st.frames.length;
    var i0 = Math.max(0, Math.min(aktiveFolie[st.id] || 0, n - 1));
    aktiveFolie[st.id] = i0;
    var leiste = document.createElement("div");
    leiste.className = "st-leiste";
    st.frames.forEach(function (fr, i) {
      var b = document.createElement("button");
      b.type = "button";
      b.className = "st-mini" + (i === i0 ? " an" : "");
      b.title = "Folie " + (i + 1);
      var c = document.createElement("canvas");
      b.appendChild(c);
      var nr = document.createElement("span");
      nr.textContent = i + 1;
      b.appendChild(nr);
      fr.__mini = c;
      renderStoryFrame(c, fr, st, i, n);
      b.onclick = function () { aktiveFolie[st.id] = i; renderStoryStrip(strip, st); };
      leiste.appendChild(b);
    });
    var add = document.createElement("button");
    add.type = "button";
    add.className = "st-mini st-neue";
    add.textContent = "+ Folie";
    add.onclick = function () {
      st.frames.push({ id: uid("fr"), layout: "text", text: "", zoom: 1, ox: 0, oy: 0 });
      aktiveFolie[st.id] = st.frames.length - 1;
      saveStory(st); renderStoryStrip(strip, st);
    };
    leiste.appendChild(add);
    strip.appendChild(leiste);
    strip.appendChild(storyCard(st, st.frames[i0], i0));
    setTimeout(function () {
      var an = leiste.querySelector(".an");
      if (an && an.scrollIntoView) an.scrollIntoView({ block: "nearest", inline: "center" });
    }, 0);
  }

  /* Eine Folie in der Story-Bibliothek: Vorschau oben, darunter Text und
     „Gestalten“ (Schrift · Ausrichtung · Balken · Hintergrund · Foto ·
     Höhe · Grösse · Sticker). Alles wird an der Folie gespeichert. */
  function storyCard(st, fr, i) {
    var card = document.createElement("div");
    card.className = "storycard";
    var head = document.createElement("div");
    head.className = "sc-head";
    head.innerHTML = '<span class="sc-num">Folie ' + (i + 1) + '</span>';
    var tools = document.createElement("div");
    tools.className = "sc-tools";
    [["‹", -1], ["›", 1]].forEach(function (t) {
      var b = document.createElement("button");
      b.className = "btn ghost"; b.textContent = t[0];
      b.onclick = function () {
        var j = i + t[1];
        if (j < 0 || j >= st.frames.length) return;
        var tmp = st.frames[i]; st.frames[i] = st.frames[j]; st.frames[j] = tmp;
        aktiveFolie[st.id] = j;
        saveStory(st); renderStoryStrip(card.parentNode, st);
      };
      tools.appendChild(b);
    });
    var kp = document.createElement("button");
    kp.className = "btn ghost"; kp.textContent = "⧉"; kp.title = "Folie kopieren";
    kp.onclick = function () {
      var neu = tief(Object.assign({}, fr)); delete neu.__draw;
      neu.id = uid("fr");
      st.frames.splice(i + 1, 0, neu); aktiveFolie[st.id] = i + 1;
      saveStory(st); renderStoryStrip(card.parentNode, st);
    };
    tools.appendChild(kp);
    var rm = document.createElement("button");
    rm.className = "btn ghost"; rm.textContent = "×";
    rm.onclick = function () {
      if (st.frames.length === 1) { toast("Eine Sequenz braucht mindestens eine Folie."); return; }
      st.frames.splice(i, 1); saveStory(st); renderStoryStrip(card.parentNode, st);
    };
    tools.appendChild(rm);
    head.appendChild(tools);
    card.appendChild(head);

    var cv = document.createElement("canvas");
    cv.className = "sc-gross";
    card.appendChild(cv);

    var body = document.createElement("div");
    body.className = "sc-body";
    card.appendChild(body);

    if (fr.notiz) {
      var nz = document.createElement("div");
      nz.className = "sc-notiz";
      nz.textContent = "✏️ " + fr.notiz;
      body.appendChild(nz);
    }

    function feld(ph, key, zeilen) {
      var el = document.createElement(zeilen ? "textarea" : "input");
      if (zeilen) el.rows = zeilen;
      el.placeholder = ph;
      el.value = Array.isArray(fr[key]) ? fr[key].join("\n") : (fr[key] || "");
      el.oninput = function () { fr[key] = el.value; saveStory(st); draw(); };
      (feldZiel || body).appendChild(el);
      return el;
    }

    var lay = document.createElement("select");
    Object.keys(STORY_LAYOUTS).forEach(function (k) {
      var o = document.createElement("option");
      o.value = k; o.textContent = STORY_LAYOUTS[k];
      if ((fr.layout || "text") === k) o.selected = true;
      lay.appendChild(o);
    });
    lay.onchange = function () {
      fr.layout = lay.value;
      // Gestaltung auf die Vorgabe des neuen Layouts zurücksetzen
      ["hg", "schrift", "align", "balken", "pos", "groesse", "sticker"].forEach(function (k) { delete fr[k]; });
      saveStory(st); renderStoryStrip(card.parentNode, st);
    };
    body.appendChild(lay);

    /* Ein Feld steht da, sobald es am Beitrag existiert (auch leer) — so
       bleibt ein über „+ Text“ angelegtes Feld sichtbar, bis es weg soll. */
    function da(k) { return fr[k] !== undefined && fr[k] !== null; }

    /* Je Textblock dieselben Knöpfe (V94, Patricia: „ich will jeden einzelnen
       textblock einzeln bearbeiten“). Schreibt in `obj` — die Folie selbst für
       Textblock 1, den Eintrag in fr.extra für alle weiteren. */
    var SCHRIFT_WERTE = [["philo", "Aa", "font-family:Philosopher;font-weight:700"],
      ["philo-k", "Aa", "font-family:Philosopher;font-style:italic"],
      ["sans", "Aa", "font-family:'Source Sans 3';font-weight:300"],
      ["sans-b", "Aa", "font-family:'Source Sans 3';font-weight:700"]];
    var ALIGN_WERTE = [["left", "links"], ["center", "Mitte"], ["right", "rechts"]];
    var FARB_WERTE = [["", "Auto"], ["creme", "", "background:#f1ecdd"], ["weiss", "", "background:#ffffff"],
      ["dunkel", "", "background:#29556d"], ["petrol", "", "background:#12828c"], ["orange", "", "background:#dc822e"]];
    function knopfReihe(ziel, titel, obj, key, werte, jetzt) {
      var w = document.createElement("div");
      w.className = "sc-seg";
      w.innerHTML = "<span>" + titel + "</span>";
      var reihe = document.createElement("div");
      werte.forEach(function (v) {
        var b = document.createElement("button");
        b.type = "button"; b.textContent = v[1];
        if (v[2]) b.style.cssText = v[2];
        b.title = v[0] || "automatisch";
        b.setAttribute("aria-pressed", String((jetzt || "") === v[0]));
        b.onclick = function () {
          obj[key] = v[0];
          Array.prototype.forEach.call(reihe.children, function (x) { x.setAttribute("aria-pressed", "false"); });
          b.setAttribute("aria-pressed", "true");
          saveStory(st); draw();
        };
        reihe.appendChild(b);
      });
      w.appendChild(reihe);
      ziel.appendChild(w);
    }
    function schieber(ziel, titel, obj, key, min, max, step, wert) {
      var row = document.createElement("div");
      row.className = "sliderow";
      var lb = document.createElement("span"); lb.textContent = titel;
      var rg = document.createElement("input");
      rg.type = "range"; rg.min = min; rg.max = max; rg.step = step; rg.value = wert;
      rg.oninput = function () { obj[key] = parseFloat(rg.value); draw(); };
      rg.onchange = function () { saveStory(st); };
      row.appendChild(lb); row.appendChild(rg);
      ziel.appendChild(row);
    }
    var sB = stilVon(fr);
    var block1 = document.createElement("div");
    block1.className = "sc-extra sc-block";
    block1.innerHTML = '<div class="sc-extrakopf"><span>Textblock 1</span></div>';
    body.appendChild(block1);
    var feldZiel = block1;
    if (fr.layout === "kurs" || fr.layout === "bonus" || da("eyebrow")) feld("Kleine Zeile oben (z.B. DER KURS)", "eyebrow");
    if (fr.layout === "bonus" || da("pille")) feld("Pille (z.B. Bonus bis Samstag, 21 Uhr)", "pille");
    feld("Text auf der Folie", "text", 3);
    if (fr.layout === "kurs" || da("punkte")) feld("Haken-Liste, ein Punkt pro Zeile", "punkte", 4);
    feld("Kleine Zeile unten (optional)", "klein");
    knopfReihe(block1, "Schrift", fr, "schrift", SCHRIFT_WERTE, sB.schrift);
    knopfReihe(block1, "Ausrichtung", fr, "align", ALIGN_WERTE, sB.align);
    knopfReihe(block1, "Balken", fr, "balken", [["aus", "ohne"], ["zeilen", "Balken"], ["karte", "Karte"]], sB.balken);
    knopfReihe(block1, "Farbe (mit Balken: Fläche · ohne: Schrift)", fr, "farbe", FARB_WERTE, fr.farbe || "");
    schieber(block1, "Höhe", fr, "pos", 12, 88, 1, sB.pos);
    schieber(block1, "Grösse", fr, "groesse", 0.6, 1.5, 0.05, sB.groesse);
    feldZiel = null;

    // ---- Freie Textblöcke: eigene Höhe, Grösse, Balken (wie „+ Balken“ im Bild-Editor)
    if (!Array.isArray(fr.extra)) fr.extra = fr.extra ? [].concat(fr.extra) : [];
    fr.extra.forEach(function (e, n) {
      var box = document.createElement("div");
      box.className = "sc-extra";
      var kopf = document.createElement("div");
      kopf.className = "sc-extrakopf";
      kopf.innerHTML = "<span>Textblock " + (n + 2) + "</span>";
      var weg = document.createElement("button");
      weg.type = "button"; weg.className = "btn ghost"; weg.textContent = "×"; weg.title = "Textblock entfernen";
      weg.onclick = function () { fr.extra.splice(n, 1); saveStory(st); renderStoryStrip(card.parentNode, st); };
      kopf.appendChild(weg);
      box.appendChild(kopf);
      var ta = document.createElement("textarea");
      ta.rows = 2; ta.placeholder = "Weiterer Text"; ta.value = e.text || "";
      ta.oninput = function () { e.text = ta.value; saveStory(st); draw(); };
      box.appendChild(ta);
      [["Höhe", "pos", 10, 90, 1, e.pos != null ? e.pos : 78], ["Grösse", "groesse", 0.5, 1.6, 0.05, e.groesse || 1]]
        .forEach(function (r) {
          var row = document.createElement("div");
          row.className = "sliderow";
          var lb = document.createElement("span"); lb.textContent = r[0];
          var rg = document.createElement("input");
          rg.type = "range"; rg.min = r[2]; rg.max = r[3]; rg.step = r[4]; rg.value = r[5];
          rg.oninput = function () { e[r[1]] = parseFloat(rg.value); draw(); };
          rg.onchange = function () { saveStory(st); };
          row.appendChild(lb); row.appendChild(rg);
          box.appendChild(row);
        });
      knopfReihe(box, "Schrift", e, "schrift", SCHRIFT_WERTE, e.schrift || "sans-b");
      knopfReihe(box, "Ausrichtung", e, "align", ALIGN_WERTE, e.align || sB.align);
      knopfReihe(box, "Balken", e, "balken", [["aus", "ohne"], ["zeilen", "Balken"]], e.balken || "zeilen");
      knopfReihe(box, "Farbe (mit Balken: Fläche · ohne: Schrift)", e, "farbe", FARB_WERTE, e.farbe || "");
      body.appendChild(box);
    });

    // ---- „+ Text“: was noch fehlt, dazulegen
    var plus = document.createElement("div");
    plus.className = "sc-plus";
    [["eyebrow", "+ Zeile oben", ""], ["pille", "+ Pille", ""], ["punkte", "+ Haken-Liste", ""],
     ["extra", "+ Textblock", null]].forEach(function (v) {
      if (v[0] !== "extra" && (da(v[0]) || (v[0] === "punkte" && fr.layout === "kurs") ||
          (v[0] === "eyebrow" && (fr.layout === "kurs" || fr.layout === "bonus")) ||
          (v[0] === "pille" && fr.layout === "bonus"))) return;
      var b = document.createElement("button");
      b.type = "button"; b.className = "btn ghost"; b.textContent = v[1];
      b.onclick = function () {
        if (v[0] === "extra") {
          var letzte = fr.extra[fr.extra.length - 1];
          fr.extra.push({ text: "", pos: letzte ? Math.min(88, (letzte.pos || 78) + 8) : 78, groesse: 1 });
        } else fr[v[0]] = v[2];
        saveStory(st); renderStoryStrip(card.parentNode, st);
      };
      plus.appendChild(b);
    });
    body.appendChild(plus);

    var gest = document.createElement("details");
    gest.className = "sc-gestalten";
    gest.innerHTML = "<summary>Hintergrund, Foto & Sticker</summary>";
    body.appendChild(gest);
    var s0 = stilVon(fr);

    function seg(titel, key, werte, jetzt) {
      var w = document.createElement("div");
      w.className = "sc-seg";
      w.innerHTML = "<span>" + titel + "</span>";
      var reihe = document.createElement("div");
      werte.forEach(function (v) {
        var b = document.createElement("button");
        b.type = "button"; b.textContent = v[1];
        if (v[2]) b.style.cssText = v[2];
        b.setAttribute("aria-pressed", String(jetzt === v[0]));
        b.onclick = function () {
          fr[key] = v[0];
          Array.prototype.forEach.call(reihe.children, function (x) { x.setAttribute("aria-pressed", "false"); });
          b.setAttribute("aria-pressed", "true");
          saveStory(st); draw();
          if (key === "hg") fotoZeile.style.display = v[0] === "foto" ? "" : "none";
        };
        reihe.appendChild(b);
      });
      w.appendChild(reihe);
      gest.appendChild(w);
    }
    seg("Hintergrund", "hg", [
      ["foto", "Foto"], ["dunkel", "", "background:#29556d"], ["creme", "", "background:#f1ecdd"],
      ["petrol", "", "background:#12828c"], ["orange", "", "background:#dc822e"]], s0.hg);

    // Shootingbilder + eigenes Foto
    var fotoZeile = document.createElement("div");
    fotoZeile.className = "sc-fotos";
    fotoZeile.style.display = s0.hg === "foto" ? "" : "none";
    (typeof COVERFOTOS !== "undefined" ? COVERFOTOS : []).forEach(function (name) {
      var t = document.createElement("img");
      t.src = "assets/" + name; t.loading = "lazy"; t.title = name;
      if (fr.foto === name && (fr.eigenesFoto === false || !images[fr.id])) t.className = "sel";
      t.onerror = function () { t.remove(); };
      t.onclick = function () {
        fr.foto = name; fr.hg = "foto";
        fr.eigenesFoto = false;
        Array.prototype.forEach.call(fotoZeile.querySelectorAll("img"), function (x) { x.className = ""; });
        t.className = "sel";
        saveStory(st); draw();
      };
      fotoZeile.appendChild(t);
    });
    var fb = document.createElement("label");
    fb.className = "btn filebtn";
    fb.innerHTML = "<span>" + (images[fr.id] ? "Eigenes Foto ersetzen" : "Eigenes Foto") + "</span>";
    var fi = document.createElement("input");
    fi.type = "file"; fi.accept = "image/*";
    fi.onchange = function () {
      if (!fi.files || !fi.files[0]) return;
      compressImage(fi.files[0], function (u) {
        fr.hg = "foto"; fr.eigenesFoto = true; saveImage("storys/" + st.id, fr.id, u); saveStory(st); draw();
      });
    };
    fb.appendChild(fi);
    fotoZeile.appendChild(fb);
    gest.appendChild(fotoZeile);

    function regler(titel, key, min, max, step, wert) {
      var row = document.createElement("div");
      row.className = "sliderow";
      var lb = document.createElement("span"); lb.textContent = titel;
      var rg = document.createElement("input");
      rg.type = "range"; rg.min = min; rg.max = max; rg.step = step; rg.value = wert;
      rg.oninput = function () { fr[key] = parseFloat(rg.value); draw(); };
      rg.onchange = function () { saveStory(st); };
      row.appendChild(lb); row.appendChild(rg);
      gest.appendChild(row);
    }
    regler("Schleier", "verlauf", 0, 85, 1, s0.verlauf);
    regler("Foto-Zoom", "zoom", 1, 3, 0.02, fr.zoom || 1);
    regler("Foto ↔", "ox", -50, 50, 1, fr.ox || 0);
    regler("Foto ↕", "oy", -50, 50, 1, fr.oy || 0);

    // Sticker: nur Platzhalter in der Vorschau, im Export leer
    var sk = document.createElement("div");
    sk.className = "sc-seg";
    sk.innerHTML = "<span>Platz für Sticker</span>";
    var sel = document.createElement("select");
    Object.keys(STICKER).forEach(function (k) {
      var o = document.createElement("option");
      o.value = k; o.textContent = STICKER[k];
      if (s0.sticker === k) o.selected = true;
      sel.appendChild(o);
    });
    sel.onchange = function () { fr.sticker = sel.value; saveStory(st); draw(); };
    sk.appendChild(sel);
    var stx = document.createElement("input");
    stx.placeholder = "Was in den Sticker kommt (nur für dich)";
    stx.value = s0.stickerText;
    stx.oninput = function () { fr.stickerText = stx.value; if (fr.sticker === undefined) fr.sticker = s0.sticker; saveStory(st); draw(); };
    sk.appendChild(stx);
    gest.appendChild(sk);
    regler("Sticker-Höhe", "stickerPos", 15, 85, 1, fr.stickerPos !== undefined && fr.stickerPos !== "" ? fr.stickerPos : 70);

    var one = document.createElement("button");
    one.className = "btn ghost"; one.textContent = "Folie als PNG";
    one.onclick = function () { exportStoryFrame(st, fr, i, one); };
    body.appendChild(one);

    function draw() {
      renderStoryFrame(cv, fr, st, i, st.frames.length);
      if (fr.__mini) renderStoryFrame(fr.__mini, fr, st, i, st.frames.length);
    }
    fr.__draw = draw;
    setTimeout(draw, 0);
    return card;
  }

  function redrawStory(st) { st.frames.forEach(function (f) { if (f.__draw) f.__draw(); }); }

  function storyBlob(st, fr, i) {
    var cv = document.createElement("canvas");
    return renderStoryFrame(cv, fr, st, i, st.frames.length, { export: true }).then(function () {
      return new Promise(function (res) { cv.toBlob(function (b) { res(b); }, "image/png"); });
    });
  }

  function exportStoryFrame(st, fr, i, btn) {
    if (!downloads) { toast("Speichern ist in dieser Ansicht nicht möglich."); return; }
    btn.disabled = true;
    storyBlob(st, fr, i).then(function (b) {
      return downloads.save({ filename: safeName(st.name) + "-story-" + (i + 1) + ".png", data: b });
    }).then(function () { toast("Folie " + (i + 1) + " gespeichert."); })
      .catch(function (e) { if (e && e.code !== "declined") toast("Hat nicht geklappt."); })
      .then(function () { btn.disabled = false; });
  }

  function exportStory(st, btn) {
    if (!downloads) { toast("Speichern ist in dieser Ansicht nicht möglich."); return; }
    btn.disabled = true;
    var i = 0;
    function next() {
      if (i >= st.frames.length) { btn.disabled = false; btn.textContent = "Alle Folien als Bilder"; toast("Fertig."); return; }
      var idx = i++;
      storyBlob(st, st.frames[idx], idx).then(function (b) {
        btn.textContent = "Folie " + (idx + 1) + " von " + st.frames.length + " …";
        return downloads.save({ filename: safeName(st.name) + "-story-" + (idx + 1) + ".png", data: b });
      }).then(next).catch(function () {
        btn.disabled = false; btn.textContent = "Alle Folien als Bilder";
      });
    }
    next();
  }

