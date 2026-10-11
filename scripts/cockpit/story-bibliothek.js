  /* =========================================================
     Story-Rendering (1080 x 1920) — Story-Bibliothek (08.10.2026)
     Gebaut mit scripts/cockpit/patch-story-bibliothek.py.

     Patricia: *„ich hätte gerne, dass der erste vorschlag noch etwas schöner
     daherkommt, gerade auch die slides, wo es effektiv um den kurs geht …
     schriften nach meinem branding … texte zentriert, rechts oder links …
     mit textbalken oder ohne … sticker, umfragen etc."*

     - Jede Folie trägt ihre Gestaltung selbst: schrift, align, balken, hg,
       foto, pos, groesse, verlauf. Fehlt ein Feld, gilt die Vorgabe des
       Layouts (STORY_STIL) — ältere Folien sehen damit sofort besser aus.
     - 🚨 Sticker werden NICHT gezeichnet. Instagram-Sticker legt sie in der
       App drauf; ein gemalter Umfrage-Knopf ist nicht klickbar und sieht
       nach Vorlage aus. Die Vorschau zeigt eine gestrichelte Fläche „hier
       kommt der Sticker hin“, der Export lässt sie leer und hält den Text
       davon weg.
     - Kein gemalter Fortschrittsbalken und kein Handle mehr — beides setzt
       Instagram selbst, doppelt sieht es nach Fälschung aus.
     ========================================================= */
  var SW = 1080, SH = 1920;
  var STORY_LAYOUTS = {
    text: "Text",
    bild: "Foto mit Text",
    learning: "Learning zum Screenshotten",
    kurs: "Kurs-Karte (Liste mit Haken)",
    bonus: "Bonus / Frist",
    frage: "Frage-Sticker",
    umfrage: "Umfrage-Sticker",
    cta: "Aufruf mit Link"
  };
  var STORY_FARBEN = {
    dunkel: { bg: "#29556d", text: "#f1ecdd", soft: "rgba(241,236,221,.72)", akzent: "#dc822e" },
    creme:  { bg: "#f1ecdd", text: "#0c1c30", soft: "rgba(12,28,48,.68)",   akzent: "#12828c" },
    petrol: { bg: "#12828c", text: "#f1ecdd", soft: "rgba(241,236,221,.8)",  akzent: "#0c1c30" },
    orange: { bg: "#dc822e", text: "#0c1c30", soft: "rgba(12,28,48,.75)",    akzent: "#f1ecdd" }
  };
  var STORY_STIL = {
    text:     { hg: "dunkel", schrift: "philo",   align: "left",   balken: "aus",    pos: 46, groesse: 1 },
    bild:     { hg: "foto",   schrift: "sans-b",  align: "center", balken: "zeilen", pos: 66, groesse: 0.9 },
    learning: { hg: "creme",  schrift: "philo",   align: "center", balken: "aus",    pos: 46, groesse: 1.1 },
    kurs:     { hg: "dunkel", schrift: "philo",   align: "left",   balken: "karte",  pos: 47, groesse: 1.12 },
    bonus:    { hg: "petrol", schrift: "philo",   align: "center", balken: "aus",    pos: 44, groesse: 1 },
    frage:    { hg: "creme",  schrift: "philo",   align: "center", balken: "aus",    pos: 30, groesse: 1, sticker: "frage" },
    umfrage:  { hg: "creme",  schrift: "philo",   align: "center", balken: "aus",    pos: 30, groesse: 1, sticker: "umfrage" },
    cta:      { hg: "dunkel", schrift: "philo",   align: "center", balken: "aus",    pos: 36, groesse: 1, sticker: "link" }
  };
  var SCHRIFTEN = {
    "philo":   { l: "Philosopher", f: function (px) { return "700 " + px + "px Philosopher, Georgia, serif"; } },
    "philo-k": { l: "Kursiv",      f: function (px) { return "italic 400 " + px + "px Philosopher, Georgia, serif"; } },
    "sans":    { l: "Leicht",      f: function (px) { return "300 " + px + "px 'Source Sans 3', sans-serif"; } },
    "sans-b":  { l: "Fett",        f: function (px) { return "700 " + px + "px 'Source Sans 3', sans-serif"; } }
  };
  /* Farbe je Textblock (V94). Mit Balken/Karte ist es die Fläche, ohne Balken die
     Schrift. Die Schrift auf einer Fläche folgt KONTRAST. Keine Fremdfarben. */
  var BLOCKFARBEN = { creme: "#f1ecdd", weiss: "#ffffff", dunkel: "#29556d",
                      petrol: "#12828c", orange: "#dc822e" };
  var KONTRAST = { creme: "#0c1c30", weiss: "#0c1c30", dunkel: "#f1ecdd",
                   petrol: "#f1ecdd", orange: "#0c1c30" };
  var STICKER = {
    "": "kein Sticker", frage: "Frage-Sticker", umfrage: "Umfrage", quiz: "Quiz",
    slider: "Emoji-Slider", link: "Link-Sticker", countdown: "Countdown", dm: "„Schreib mir“-Sticker"
  };
  var STICKER_H = { frage: 300, umfrage: 260, quiz: 420, slider: 200, link: 130, countdown: 230, dm: 130 };

  /* Ältere Folien hatten den Sticker als Text im Feld `cta` — der wurde als
     orange Pille INS BILD gemalt („Link-Sticker: Verkaufsseite …"). Hier wird
     daraus die Sticker-Fläche, und nur echter Text bleibt Text. */
  function stilVon(fr) {
    var lay = STORY_STIL[fr.layout] ? fr.layout : "text";
    var d = STORY_STIL[lay], s = {};
    ["hg", "schrift", "align", "balken", "pos", "groesse"].forEach(function (k) {
      s[k] = (fr[k] !== undefined && fr[k] !== "" && fr[k] !== null) ? fr[k] : d[k];
    });
    // Ein hochgeladenes Bild oder ein gewähltes Shootingbild heisst: Foto als Hintergrund
    if ((fr.hg === undefined || fr.hg === "") && (images[fr.id] || fr.foto)) s.hg = "foto";
    s.sticker = fr.sticker !== undefined ? fr.sticker : (d.sticker || "");
    s.stickerText = fr.stickerText || "";
    s.klein = fr.klein || "";
    var c = String(fr.cta || "").trim();
    if (fr.sticker === undefined && c) {
      if (/sticker|link|dm\b|→/i.test(c) || lay === "cta" || lay === "frage" || lay === "umfrage") {
        if (!s.sticker) s.sticker = /countdown/i.test(c) ? "countdown" : /umfrage/i.test(c) ? "umfrage"
          : /frage/i.test(c) ? "frage" : /dm|tipp/i.test(c) ? "dm" : "link";
        if (!s.stickerText) s.stickerText = c;
      } else if (!s.klein) s.klein = c;
    }
    if (s.sticker === "umfrage" && !s.stickerText && (fr.optA || fr.optB))
      s.stickerText = (fr.optA || "Ja") + " / " + (fr.optB || "Nein");
    s.verlauf = fr.verlauf !== undefined ? fr.verlauf : (s.balken === "aus" ? 58 : 26);
    return s;
  }

  function roundRect(ctx, x, y, w, h, r) {
    ctx.beginPath();
    if (ctx.roundRect) { ctx.roundRect(x, y, w, h, r); }
    else {
      ctx.moveTo(x + r, y);
      ctx.arcTo(x + w, y, x + w, y + h, r);
      ctx.arcTo(x + w, y + h, x, y + h, r);
      ctx.arcTo(x, y + h, x, y, r);
      ctx.arcTo(x, y, x + w, y, r);
      ctx.closePath();
    }
  }

  var storyFotoCache = {};
  function storyFoto(fr, cb) {
    if (images[fr.id] && fr.eigenesFoto !== false) { getImageObj(fr.id, cb); return; }
    if (!fr.foto) { cb(null); return; }
    var src = /^(data:|https?:|assets\/)/.test(fr.foto) ? fr.foto : "assets/" + fr.foto;
    var c = storyFotoCache[src];
    if (c && c.ok) { cb(c.img); return; }
    var im = new Image();
    im.onload = function () { storyFotoCache[src] = { ok: true, img: im }; cb(im); };
    im.onerror = function () { cb(null); };
    im.src = src;
  }

  var storySchriftBereit = null;
  function storySchriften() {
    if (storySchriftBereit) return storySchriftBereit;
    if (!document.fonts || !document.fonts.load) return (storySchriftBereit = Promise.resolve());
    storySchriftBereit = Promise.all(Object.keys(SCHRIFTEN).map(function (k) {
      return document.fonts.load(SCHRIFTEN[k].f(60), "ÄäÖöÜü„“").catch(function () {});
    })).then(function () {}, function () {});
    return storySchriftBereit;
  }

  function storyZeilen(ctx, text, maxW) {
    var out = [];
    String(text || "").split("\n").forEach(function (para) {
      var w = para.split(/\s+/).filter(Boolean);
      if (!w.length) { out.push(""); return; }
      var line = w[0];
      for (var i = 1; i < w.length; i++) {
        var t = line + " " + w[i];
        if (ctx.measureText(t).width > maxW) { out.push(line); line = w[i]; } else line = t;
      }
      out.push(line);
    });
    return out;
  }

  /* Zeichnet eine Folie. Gibt ein Promise zurück, das erfüllt ist, wenn Foto
     und Schriften geladen sind — der Export wartet darauf, statt wie früher
     280 ms zu raten. opts.export = true lässt die Sticker-Hilfsfläche weg. */
  function renderStoryFrame(canvas, fr, st, index, total, opts) {
    opts = opts || {};
    var ctx = canvas.getContext("2d");
    canvas.width = SW; canvas.height = SH;
    var s = stilVon(fr);
    return new Promise(function (fertig) {
      storySchriften().then(function () {
        storyFoto(fr, function (img) {
          try { zeichne(img); } catch (e) { console.error("Story-Folie:", e); }
          fertig();
        });
      });
    });

    function zeichne(img) {
      var fotoHg = s.hg === "foto";
      var F = STORY_FARBEN[fotoHg ? "dunkel" : s.hg] || STORY_FARBEN.dunkel;
      var pad = 92, maxW = SW - pad * 2;

      // ---- Hintergrund
      ctx.fillStyle = F.bg; ctx.fillRect(0, 0, SW, SH);
      if (fotoHg && img) {
        drawCover(ctx, img, 0, 0, SW, SH, fr.zoom, fr.ox, fr.oy);
      } else if (fotoHg) {
        ctx.fillStyle = "#1f4458"; ctx.fillRect(0, 0, SW, SH);
        ctx.fillStyle = "rgba(241,236,221,.55)"; ctx.font = "400 40px 'Source Sans 3', sans-serif";
        ctx.textAlign = "center"; ctx.fillText("Foto wählen ↓", SW / 2, SH / 2); ctx.textAlign = "left";
      } else {
        // feine Tiefe statt flacher Fläche
        var rg = ctx.createRadialGradient(SW * 0.2, SH * 0.1, 40, SW * 0.5, SH * 0.5, SH * 0.9);
        rg.addColorStop(0, "rgba(255,255,255,.07)"); rg.addColorStop(1, "rgba(0,0,0,.06)");
        ctx.fillStyle = rg; ctx.fillRect(0, 0, SW, SH);
      }

      // ---- Textblock vermessen
      var gr = Math.max(0.6, Math.min(1.5, +s.groesse || 1));
      var schrift = SCHRIFTEN[s.schrift] || SCHRIFTEN.philo;
      var karte = s.balken === "karte";
      var innen = karte ? 64 : 0;
      var breite = maxW - innen * 2;
      var teile = [];          // {art, zeilen, font, px, lh, farbe}
      function dazu(art, text, font, px, lh, farbe, abstand) {
        if (!String(text || "").trim()) return;
        ctx.font = font;
        var z = art === "punkte" ? text : storyZeilen(ctx, text, art === "pille" ? breite - 80 : breite);
        teile.push({ art: art, zeilen: z, font: font, px: px, lh: lh, farbe: farbe, abstand: abstand || 0 });
      }
      var hpx = Math.round((fr.layout === "learning" ? 80 : fr.layout === "kurs" ? 72 : 76) * gr);
      // Überschrift so lange verkleinern, bis sie in rund 45 % der Höhe passt
      var hz;
      for (var tries = 0; tries < 12; tries++) {
        ctx.font = schrift.f(hpx);
        hz = storyZeilen(ctx, fr.text || "", breite);
        if (hz.length * hpx * 1.18 <= SH * 0.45 || hpx <= 40) break;
        hpx -= 6;
      }
      var akzent = fotoHg ? "#dc822e" : F.akzent;
      if (fr.eyebrow) dazu("eyebrow", String(fr.eyebrow).toUpperCase(), "700 32px 'Source Sans 3', sans-serif", 32, 1.3, akzent, 30);
      if (fr.pille) dazu("pille", fr.pille, "700 36px 'Source Sans 3', sans-serif", 36, 1.25, "#f1ecdd", 34);
      if (fr.text) teile.push({ art: "kopf", zeilen: hz, font: schrift.f(hpx), px: hpx, lh: 1.18, farbe: F.text, abstand: 0 });
      var punkte = Array.isArray(fr.punkte) ? fr.punkte : String(fr.punkte || "").split("\n");
      punkte = punkte.map(function (x) { return String(x).trim(); }).filter(Boolean);
      if (punkte.length) {
        var ppx = Math.round(44 * Math.min(1.15, gr));
        ctx.font = "400 " + ppx + "px 'Source Sans 3', sans-serif";
        var pz = punkte.map(function (p) { return storyZeilen(ctx, p, breite - 70); });
        teile.push({ art: "punkte", zeilen: pz, font: ctx.font, px: ppx, lh: 1.3, farbe: F.text, abstand: 44 });
      }
      if (s.klein) dazu("klein", s.klein, "400 " + Math.round(42 * Math.min(1.1, gr)) + "px 'Source Sans 3', sans-serif",
                       Math.round(42 * Math.min(1.1, gr)), 1.32, fotoHg ? "rgba(241,236,221,.9)" : F.soft, 40);

      function hoeheVon(t) {
        if (t.art === "punkte") return t.zeilen.reduce(function (a, z) { return a + z.length * t.px * t.lh + 22; }, 0);
        if (t.art === "pille") return t.zeilen.length * t.px * t.lh + 44;
        return t.zeilen.length * t.px * t.lh;
      }
      var blockH = 0;
      teile.forEach(function (t, i) { blockH += hoeheVon(t) + (i ? t.abstand : 0); });
      var gesamtH = blockH + innen * 2;

      // ---- Sticker-Fläche und Lage des Textes
      var oben = 250, unten = SH - 300;        // Instagram-Kopf und -Fuss frei
      var sticker = s.sticker && STICKER[s.sticker] ? s.sticker : "";
      var sH = sticker ? STICKER_H[sticker] || 220 : 0;
      var mitte = SH * (Math.max(10, Math.min(90, +s.pos || 50)) / 100);
      var y0 = Math.max(oben, Math.min(unten - gesamtH, mitte - gesamtH / 2));
      var sY = null;
      if (sticker) {
        var luecke = 70;
        if (fr.stickerPos !== undefined && fr.stickerPos !== "") {
          sY = SH * (+fr.stickerPos / 100) - sH / 2;
        } else {
          sY = y0 + gesamtH + luecke;                 // unter dem Text
          if (sY + sH > unten) sY = y0 - luecke - sH;  // sonst darüber
        }
        sY = Math.max(oben - 60, Math.min(SH - 240 - sH, sY));
        // Text weicht dem Sticker aus
        if (y0 < sY + sH + luecke && y0 + gesamtH > sY - luecke) {
          if (sY > mitte) y0 = Math.max(oben - 80, sY - luecke - gesamtH);
          else y0 = Math.min(SH - 200 - gesamtH, sY + sH + luecke);
        }
      }

      // ---- Lesbarkeit auf Foto: weicher Schleier rund um den Text
      if (fotoHg && img && s.verlauf > 0) {
        var a = Math.min(0.88, s.verlauf / 100);
        var cy = y0 + gesamtH / 2;
        var g = ctx.createLinearGradient(0, Math.max(0, cy - SH * 0.42), 0, Math.min(SH, cy + SH * 0.42));
        g.addColorStop(0, "rgba(12,28,48,0)");
        g.addColorStop(0.5, "rgba(12,28,48," + a + ")");
        g.addColorStop(1, "rgba(12,28,48,0)");
        ctx.fillStyle = g; ctx.fillRect(0, 0, SW, SH);
      }

      // ---- Neigung (V94, „lockerer“): der ganze Block dreht um seine Mitte
      var dreh1 = 0; // Neigung entfernt (Patricia 08.10.: „muss ich nicht einstellen“)
      ctx.save();
      if (dreh1) {
        ctx.translate(SW / 2, y0 + gesamtH / 2); ctx.rotate(dreh1); ctx.translate(-SW / 2, -(y0 + gesamtH / 2));
      }
      // ---- Karte hinter dem ganzen Block
      if (karte) {
        ctx.fillStyle = BLOCKFARBEN[fr.farbe] ||
          (fotoHg ? "rgba(241,236,221,.95)" : (s.hg === "creme" ? "#ffffff" : "rgba(241,236,221,.97)"));
        roundRect(ctx, pad, y0, maxW, gesamtH, 34); ctx.fill();
        ctx.fillStyle = "#dc822e";
        roundRect(ctx, pad, y0, 14, gesamtH, 7); ctx.fill();
      }
      var eigene = BLOCKFARBEN[fr.farbe] ? fr.farbe : "";
      var textFarbeKarte = eigene ? KONTRAST[eigene] : "#0c1c30";

      // ---- Text setzen
      var al = s.align === "center" ? "center" : s.align === "right" ? "right" : "left";
      var xA = al === "center" ? SW / 2 : al === "right" ? SW - pad - innen : pad + innen;
      var y = y0 + innen;
      ctx.textBaseline = "alphabetic";
      teile.forEach(function (t, ti) {
        if (ti) y += t.abstand;
        var farbe = karte
          ? (eigene ? textFarbeKarte
             : (t.art === "eyebrow" ? "#12828c" : t.art === "klein" ? "rgba(12,28,48,.7)" : textFarbeKarte))
          : (eigene && s.balken === "aus" ? BLOCKFARBEN[eigene] : t.farbe);
        ctx.font = t.font;
        if (t.art === "pille") {
          var pw = Math.min(breite, Math.max.apply(null, t.zeilen.map(function (z) { return ctx.measureText(z).width; })) + 80);
          var ph = t.zeilen.length * t.px * t.lh + 44;
          var px0 = al === "center" ? SW / 2 - pw / 2 : al === "right" ? xA - pw : xA;
          ctx.fillStyle = "#dc822e"; roundRect(ctx, px0, y, pw, ph, ph / 2 > 60 ? 36 : ph / 2); ctx.fill();
          ctx.fillStyle = "#f1ecdd"; ctx.textAlign = "center";
          t.zeilen.forEach(function (z, i) { ctx.fillText(z, px0 + pw / 2, y + 22 + t.px * 0.95 + i * t.px * t.lh); });
          y += ph; return;
        }
        if (t.art === "punkte") {
          t.zeilen.forEach(function (pz) {
            var punktX = al === "right" ? xA - 26 : (al === "center" ? null : xA + 26);
            var h = pz.length * t.px * t.lh;
            if (punktX !== null) {
              ctx.fillStyle = karte ? "#12828c" : akzent;
              ctx.beginPath(); ctx.arc(punktX, y + t.px * 0.62, 24, 0, Math.PI * 2); ctx.fill();
              ctx.strokeStyle = karte || !fotoHg ? "#f1ecdd" : "#0c1c30"; ctx.lineWidth = 5; ctx.lineCap = "round";
              ctx.beginPath(); ctx.moveTo(punktX - 11, y + t.px * 0.64); ctx.lineTo(punktX - 3, y + t.px * 0.64 + 8);
              ctx.lineTo(punktX + 12, y + t.px * 0.64 - 9); ctx.stroke();
            }
            ctx.fillStyle = farbe; ctx.textAlign = al;
            var tx = al === "left" ? xA + 70 : al === "right" ? xA - 70 : xA;
            pz.forEach(function (z, i) {
              if (al === "center" && i === 0) z = "✓ " + z;
              ctx.fillText(z, tx, y + t.px + i * t.px * t.lh);
            });
            y += h + 22;
          });
          return;
        }
        var zeilenBalken = s.balken === "zeilen" && t.art !== "eyebrow";
        t.zeilen.forEach(function (z, i) {
          var by = y + i * t.px * t.lh;
          if (zeilenBalken && z) {
            var w = ctx.measureText(z).width, padX = 26, hh = t.px * t.lh + 4;
            var bx = al === "center" ? SW / 2 - w / 2 - padX : al === "right" ? xA - w - padX : xA - padX;
            ctx.fillStyle = eigene ? BLOCKFARBEN[eigene]
              : (fotoHg || s.hg === "dunkel" || s.hg === "petrol" ? "rgba(241,236,221,.96)" : "rgba(12,28,48,.94)");
            roundRect(ctx, bx, by - 2, w + padX * 2, hh, 14); ctx.fill();
          }
          ctx.textAlign = al;
          var fz = zeilenBalken
            ? (eigene ? KONTRAST[eigene] : (fotoHg || s.hg === "dunkel" || s.hg === "petrol" ? "#0c1c30" : "#f1ecdd"))
            : farbe;
          if (!zeilenBalken && fotoHg && !karte) {
            ctx.shadowColor = "rgba(0,0,0,.45)"; ctx.shadowBlur = 22; ctx.shadowOffsetY = 3;
          }
          ctx.fillStyle = fz;
          ctx.fillText(z, xA, by + t.px * (t.art === "eyebrow" ? 1 : 0.98));
          ctx.shadowColor = "transparent"; ctx.shadowBlur = 0; ctx.shadowOffsetY = 0;
          if (t.art === "eyebrow" && i === t.zeilen.length - 1 && !karte) {
            // kleiner Strich unter der Kopfzeile
            var lw = 70, lx = al === "center" ? SW / 2 - lw / 2 : al === "right" ? xA - lw : xA;
            ctx.fillStyle = farbe; ctx.fillRect(lx, by + t.px * 1.35, lw, 4);
          }
        });
        y += t.zeilen.length * t.px * t.lh;
      });
      ctx.restore();

      // ---- Freie Textblöcke („+ Textblock“): je eigene Höhe, Grösse, Schrift, Balken.
      // Ausrichtung folgt der Folie, damit alles auf einer Linie steht.
      (Array.isArray(fr.extra) ? fr.extra : []).forEach(function (e) {
        var txt = String((e && e.text) || "").trim();
        if (!txt) return;
        var ex = SCHRIFTEN[e.schrift] || SCHRIFTEN["sans-b"];
        var epx = Math.round(54 * Math.max(0.5, Math.min(1.6, +e.groesse || 1)));
        ctx.font = ex.f(epx);
        var ez = storyZeilen(ctx, txt, maxW);
        var elh = 1.22, eh = ez.length * epx * elh;
        var ey = SH * (Math.max(8, Math.min(92, e.pos != null ? +e.pos : 78)) / 100) - eh / 2;
        ey = Math.max(200, Math.min(SH - 220 - eh, ey));
        var eal = e.align === "center" || e.align === "left" || e.align === "right" ? e.align : al;
        var ealX = eal === "center" ? SW / 2 : eal === "right" ? SW - pad : pad;
        var ef = BLOCKFARBEN[e.farbe] ? e.farbe : "";
        var eBalken = (e.balken || "zeilen") === "zeilen";
        var hellerGrund = !(fotoHg || s.hg === "dunkel" || s.hg === "petrol");
        var edreh = 0;
        ctx.save();
        if (edreh) {
          var emx = eal === "center" ? SW / 2 : eal === "right" ? SW - pad - 200 : pad + 200;
          ctx.translate(emx, ey + eh / 2); ctx.rotate(edreh); ctx.translate(-emx, -(ey + eh / 2));
        }
        ez.forEach(function (z, i) {
          var by = ey + i * epx * elh;
          ctx.font = ex.f(epx);
          if (eBalken && z) {
            var w = ctx.measureText(z).width, padX = 24, hh = epx * elh + 4;
            var bx = eal === "center" ? SW / 2 - w / 2 - padX : eal === "right" ? ealX - w - padX : ealX - padX;
            ctx.fillStyle = ef ? BLOCKFARBEN[ef] : (hellerGrund ? "rgba(12,28,48,.92)" : "rgba(241,236,221,.96)");
            roundRect(ctx, bx, by - 2, w + padX * 2, hh, 14); ctx.fill();
            ctx.fillStyle = ef ? KONTRAST[ef] : (hellerGrund ? "#f1ecdd" : "#0c1c30");
          } else {
            ctx.fillStyle = ef ? BLOCKFARBEN[ef] : (hellerGrund ? (s.hg === "orange" ? "#0c1c30" : "#29556d") : "#f1ecdd");
            if (fotoHg) { ctx.shadowColor = "rgba(0,0,0,.45)"; ctx.shadowBlur = 22; ctx.shadowOffsetY = 3; }
          }
          ctx.textAlign = eal;
          ctx.fillText(z, ealX, by + epx * 0.98);
          ctx.shadowColor = "transparent"; ctx.shadowBlur = 0; ctx.shadowOffsetY = 0;
        });
        ctx.restore();
      });

      // ---- Sticker-Fläche nur in der Vorschau
      if (sticker && !opts.export) {
        ctx.save();
        ctx.setLineDash([22, 16]); ctx.lineWidth = 5;
        ctx.strokeStyle = fotoHg || s.hg === "dunkel" || s.hg === "petrol" ? "rgba(241,236,221,.85)" : "rgba(12,28,48,.55)";
        var sw = sticker === "link" || sticker === "dm" ? 620 : 760;
        roundRect(ctx, SW / 2 - sw / 2, sY, sw, sH, 40); ctx.stroke();
        ctx.setLineDash([]);
        ctx.fillStyle = ctx.strokeStyle; ctx.textAlign = "center";
        ctx.font = "700 34px 'Source Sans 3', sans-serif";
        ctx.fillText("hier: " + STICKER[sticker], SW / 2, sY + sH / 2 + (s.stickerText ? -6 : 12));
        if (s.stickerText) {
          ctx.font = "400 28px 'Source Sans 3', sans-serif";
          ctx.fillText(s.stickerText.length > 46 ? s.stickerText.slice(0, 44) + "…" : s.stickerText, SW / 2, sY + sH / 2 + 40);
        }
        ctx.restore();
      }
      ctx.textAlign = "left";
    }
  }

