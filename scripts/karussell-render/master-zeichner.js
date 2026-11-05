/* MASTER-VORLAGE-ANFANG
   Der eine Zeichner der Karussell-Master-Vorlage. Laeuft im Cockpit (eingesetzt mit
   scripts/cockpit/patch-master-vorlage.py) und in folien.mjs, damit Vorschau und Export
   nie auseinanderlaufen. Regeln und Felder: context/karussell-framework.md. */
var MASTER = (function () {
  var W = 1080, H = 1350;
  var SERIF = "Philosopher, Georgia, serif";
  var SANS = "'Source Sans 3', 'Trebuchet MS', sans-serif";
  var HAND = "'Silver South Script', cursive";
  var api = { basis: "assets/" };

  var CREME = { flaeche: "#f1ecdd", oben: "#f1ecdd", unten: "#f1ecdd", schrift: "#0c1c30",
    zart: "#29556d", rand: "rgba(41,85,109,.55)", wort: "#dc822e", akzent: "#dc822e", glow: null,
    schild: "#29556d", schildS: "#f1ecdd", kachel: "#fffdf8" };
  var AKZENT = {
    mlb_dark: { flaeche: "#29556d", oben: "#34687f", unten: "#1f4659", schrift: "#f1ecdd",
      zart: "rgba(241,236,221,.82)", wort: "#f8c896", akzent: "#f2a55c", glow: [0.35, 0.6, 0.85],
      schild: "#f1ecdd", schildS: "#29556d", kachel: "#f1ecdd" },
    mlb_light: CREME,
    mlb_teal: { flaeche: "#12828c", oben: "#1b95a0", unten: "#0e6f78", schrift: "#fffaf0",
      zart: "rgba(255,250,240,.88)", wort: "#fff0d4", akzent: "#ffe0b0", glow: [0.4, 0.7, 0.95],
      schild: "#f1ecdd", schildS: "#29556d", kachel: "#f1ecdd" },
    oele: { flaeche: "#2f4a3c", oben: "#3a5a49", unten: "#263d31", schrift: "#f5f0e6",
      zart: "rgba(245,240,230,.82)", wort: "#f0d98a", akzent: "#e5c965", glow: [0.3, 0.5, 0.75],
      schild: "#f5f0e6", schildS: "#2f4a3c", kachel: "#f5f0e6" }
  };

  api.FARBNAME = { mlb_dark: "Dunkelblau", mlb_light: "Beige", mlb_teal: "Petrol", oele: "Öle / doTERRA" };
  api.LAYOUTS = {
    "m-titel": "Vorlage: Cover",
    "m-liste": "Vorlage: Karten-Liste",
    "m-text": "Vorlage: ein Gedanke",
    "m-auftrag": "Vorlage: zum Abtippen",
    "m-aufruf": "Vorlage: letzte Folie"
  };
  api.ist = function (slide) { return !!slide && /^m-/.test(slide.layout || ""); };
  api.istKarussell = function (car) { return !!(car && car.slides && car.slides.some(api.ist)); };

  // Ein Stichwort im Aufruf macht den Beitrag zum Lead-Post, dort ist Petrol verboten.
  api.istLead = function (car) {
    var aufruf = (car.slides || []).filter(function (s) { return s.layout === "m-aufruf"; })[0];
    if (aufruf && /kommentier/i.test(aufruf.oben == null ? "Kommentier" : aufruf.oben)) return true;
    return /kommentier\w*\s+\*{0,2}[A-ZÄÖÜ0-9]{3,}/i.test(car.caption || "");
  };

  api.felder = function (layout) {
    return {
      "m-titel": [["oben", "Kleine Zeile ganz oben", 1],
        ["headline", "Hook, das grosse Wort in *Sternchen*", 3]],
      "m-liste": [["oben", "Etikett oben, z.B. 01 – 03 · zum Antippen", 1],
        ["body", "Eine Karte je Zeile: Titel | Text | Etikett\nEine Zeile ohne | wird Fliesstext darunter", 5],
        ["notiz", "Handschrift, nur ganz kurz", 1]],
      "m-text": [["oben", "Etikett oben", 1], ["headline", "Satz, betontes Wort in *Sternchen*", 2],
        ["body", "Text", 3], ["notiz", "Handschrift, nur ganz kurz", 1]],
      "m-auftrag": [["oben", "Etikett oben", 1], ["headline", "Überschrift", 2],
        ["body", "Aufträge, je einer mit Leerzeile dazwischen. [Platzhalter] wird farbig", 6]],
      "m-aufruf": [["oben", "Handschrift, z.B. Kommentier", 1], ["headline", "Stichwort", 1],
        ["body", "Was sie dafür bekommt", 2], ["schild", "Kleines Schild unten", 1]]
    }[layout] || null;
  };

  // Bestehendes Karussell auf die Vorlage umstellen, Texte bleiben
  api.umstellen = function (car) {
    var n = car.slides.length;
    car.slides.forEach(function (s, i) {
      if (api.ist(s)) return;
      if (i === 0) { s.layout = "m-titel"; if (s.foto == null) s.foto = "s03.jpg"; }
      else if (i === n - 1 || s.layout === "cta") {
        s.layout = "m-aufruf";
        if (s.keyword) s.headline = s.keyword;
      } else s.layout = "m-text";
    });
  };

  /* ---------- Laden ---------- */
  var geladen = {}, schriften = null;
  function bild(name, cb) {
    if (!name) { cb(null); return; }
    if (geladen[name] !== undefined) { cb(geladen[name]); return; }
    var im = new Image();
    im.onload = function () { geladen[name] = im; cb(im); };
    im.onerror = function () { geladen[name] = null; cb(null); };
    im.src = api.basis + name;
  }
  function schriftenLaden() {
    if (schriften) return schriften;
    var hand = new FontFace("Silver South Script", "url(" + api.basis + "silversouth.otf)");
    schriften = hand.load().then(function (f) { document.fonts.add(f); }).catch(function () {})
      .then(function () {
        return Promise.all(["100px Philosopher", "italic 100px Philosopher",
          "400 40px 'Source Sans 3'", "600 40px 'Source Sans 3'"]
          .map(function (s) { return document.fonts.load(s).catch(function () {}); }));
      });
    return schriften;
  }
  // Ruft cb mit dem Vorlagen-Foto der Folie, sobald Schriften und Bilder bereit sind
  api.bereit = function (slide, cb) {
    schriftenLaden().then(function () {
      bild(slide.layout === "m-aufruf" ? "favicon.png" : null, function () {
        bild(slide.layout === "m-titel" ? slide.foto : null, cb);
      });
    });
  };

  /* ---------- Werkzeuge ---------- */
  function rgba(hex, a) {
    var n = parseInt(hex.slice(1), 16);
    return "rgba(" + (n >> 16) + "," + ((n >> 8) & 255) + "," + (n & 255) + "," + a + ")";
  }
  function sperren(ctx, em) { try { ctx.letterSpacing = em + "px"; } catch (e) {} }
  function rund(ctx, x, y, w, h, r) {
    ctx.beginPath();
    if (ctx.roundRect) ctx.roundRect(x, y, w, h, r); else ctx.rect(x, y, w, h);
  }
  function grund(ctx, t) {
    var g = ctx.createLinearGradient(0, 0, 0, H);
    g.addColorStop(0, t.oben); g.addColorStop(0.45, t.flaeche); g.addColorStop(1, t.unten);
    ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
  }
  // Zerlegt in Woerter mit Stil: *betont*, [Platzhalter]
  function woerter(text) {
    var aus = [], re = /\*([^*]+)\*|(\[[^\]]+\])|([^*\[]+|[*\[])/g, m;
    while ((m = re.exec(String(text || "")))) {
      var stil = m[1] != null ? "em" : m[2] != null ? "platz" : "";
      (m[1] || m[2] || m[3]).split(/(\s+)/).forEach(function (w) {
        if (w) aus.push({ t: w, stil: stil });
      });
    }
    return aus;
  }
  function setzen(ctx, text, maxW, font) {
    var zeilen = [], z = [], b = 0;
    function neu() { while (z.length && !z[z.length - 1].t.trim()) z.pop(); zeilen.push(z); z = []; b = 0; }
    woerter(text).forEach(function (w) {
      if (/\n/.test(w.t)) { neu(); return; }
      ctx.font = font(w.stil);
      var breite = ctx.measureText(w.t).width;
      if (!w.t.trim()) { if (z.length) { z.push({ t: w.t, stil: w.stil, b: breite }); b += breite; } return; }
      if (b + breite > maxW && z.length) neu();
      z.push({ t: w.t, stil: w.stil, b: breite }); b += breite;
    });
    if (z.length) neu();
    return zeilen;
  }
  function zeileZeichnen(ctx, zeile, x, y, ausricht, font, farbe) {
    var ges = zeile.reduce(function (s, w) { return s + w.b; }, 0);
    var px = ausricht === "mitte" ? x - ges / 2 : x;
    ctx.textAlign = "left";
    zeile.forEach(function (w) {
      ctx.font = font(w.stil); ctx.fillStyle = farbe(w.stil);
      ctx.fillText(w.t, px, y); px += w.b;
    });
  }
  function leuchtend(ctx, text, x, y, t) {
    if (t.glow) {
      [[110, t.glow[0]], [60, t.glow[1]], [22, t.glow[2]]].forEach(function (s) {
        ctx.save();
        ctx.shadowColor = "rgba(220,130,46," + s[1] + ")"; ctx.shadowBlur = s[0];
        ctx.fillStyle = t.wort; ctx.fillText(text, x, y);
        ctx.restore();
      });
    }
    ctx.fillStyle = t.wort; ctx.fillText(text, x, y);
  }
  function kopf(ctx, slide, index, total, t) {
    var y = 76;
    if (slide.oben) {
      ctx.font = "600 25px " + SANS; sperren(ctx, 3);
      var text = String(slide.oben).toUpperCase(), b = ctx.measureText(text).width + 60;
      ctx.strokeStyle = t.rand; ctx.lineWidth = 2;
      rund(ctx, 62, y, b, 62, 31); ctx.stroke();
      ctx.fillStyle = t.schrift; ctx.textAlign = "left"; ctx.fillText(text, 92, y + 40);
      sperren(ctx, 0);
    }
    ctx.font = "400 25px " + SANS; sperren(ctx, 2); ctx.fillStyle = t.zart; ctx.textAlign = "right";
    function zwei(n) { return (n < 10 ? "0" : "") + n; }
    ctx.fillText(zwei(index + 1) + "/" + zwei(total), W - 62, y + 40);
    sperren(ctx, 0); ctx.textAlign = "left";
  }
  function weiter(ctx, t) {
    ctx.font = "400 54px " + SANS; ctx.fillStyle = t.zart; ctx.textAlign = "right";
    ctx.fillText("→", W - 62, H - 52); ctx.textAlign = "left";
  }
  function karteFlaeche(ctx, x, y, w, h) {
    ctx.save();
    ctx.shadowColor = "rgba(12,28,48,.16)"; ctx.shadowBlur = 34; ctx.shadowOffsetY = 14;
    ctx.fillStyle = "#fffdf8"; rund(ctx, x, y, w, h, 26); ctx.fill();
    ctx.restore();
  }
  function textBlock(ctx, text, maxW, groesse, lh, gewicht, t) {
    function font(st) { return (st === "platz" ? "600 " : gewicht + " ") + groesse + "px " + SANS; }
    var z = setzen(ctx, text, maxW, font);
    return { h: z.length * groesse * lh, zeichne: function (x, y, aus) {
      z.forEach(function (zeile, i) {
        zeileZeichnen(ctx, zeile, x, y + groesse * 0.95 + i * groesse * lh, aus, font,
          function (st) { return st === "em" ? t.akzent : st === "platz" ? "#0d666e" : t.schrift; });
      });
    } };
  }
  function titelBlock(ctx, text, maxW, groesse, t) {
    function font(st) { return (st === "em" ? "italic 400 " : "400 ") + groesse + "px " + SERIF; }
    var z = setzen(ctx, text, maxW, font), lh = 1.1;
    return { h: z.length * groesse * lh, zeichne: function (x, y, aus) {
      z.forEach(function (zeile, i) {
        zeileZeichnen(ctx, zeile, x, y + groesse * 0.9 + i * groesse * lh, aus, font,
          function (st) { return st === "em" ? t.akzent : t.schrift; });
      });
    } };
  }
  function notizBlock(ctx, text, groesse, t) {
    return { h: groesse * 1.25, zeichne: function (x, y) {
      ctx.save();
      ctx.translate(x, y + groesse); ctx.rotate(-0.035);
      ctx.font = groesse + "px " + HAND; ctx.fillStyle = t.schrift; ctx.textAlign = "left";
      ctx.fillText(text, 0, 0);
      ctx.restore();
    } };
  }
  // Baut mit Faktor f die Bloecke und nimmt den groessten, der in die Hoehe passt
  function passend(hoehe, bauen) {
    for (var f = 1; f > 0.66; f -= 0.04) {
      var bl = bauen(f), summe = bl.reduce(function (s, b) { return s + b.h + (b.luft || 0); }, 0);
      if (summe <= hoehe) return { bloecke: bl, summe: summe };
    }
    return { bloecke: bl, summe: summe };
  }
  function stapeln(erg, von, bis, x) {
    var y = von + Math.max(0, (bis - von - erg.summe) / 2);
    erg.bloecke.forEach(function (b) { y += b.vor || 0; b.zeichne(x, y); y += b.h + ((b.luft || 0) - (b.vor || 0)); });
  }

  /* ---------- Folien ---------- */
  function titel(ctx, s, car, t, foto) {
    var teile = /^([\s\S]*?)\*([^*]+)\*([\s\S]*)$/.exec(s.headline || "");
    var z1 = teile ? teile[1].trim() : (s.headline || ""), wort = teile ? teile[2].trim() : "",
      z2 = teile ? teile[3].trim() : "";
    function zFont() { return "400 58px " + SERIF; }
    var br = W - 112, l1 = setzen(ctx, z1, br, zFont), l2 = setzen(ctx, z2, br, zFont);
    var wg = 142;
    while (wort && wg > 60) {
      ctx.font = "italic 400 " + wg + "px " + SERIF;
      if (ctx.measureText(wort).width <= br) break;
      wg -= 4;
    }
    var obenH = s.oben ? 87 : 0, blockH = obenH + l1.length * 66 + (wort ? wg * 1.1 + 14 : 0) + l2.length * 66;
    var start = foto ? 96 : Math.max(96, (H - blockH) / 2 - 20);
    var ende = start + blockH;

    grund(ctx, t);
    if (foto) {
      var fy = Math.round(Math.max(510, ende - 25) + (s.oy || 0) * 6);
      var fw = W * (s.zoom || 1), fh = fw * foto.height / foto.width;
      ctx.drawImage(foto, (W - fw) / 2 + (s.ox || 0) * 6, fy, fw, fh);
      var von = fy + 30, bis = fy + 300;
      var g = ctx.createLinearGradient(0, von, 0, bis);
      [[0, 1], [0.2, 0.86], [0.5, 0.55], [0.8, 0.2], [1, 0]].forEach(function (p) {
        g.addColorStop(p[0], rgba(t.flaeche, p[1]));
      });
      // Eine Flaeche von oben bis zum Verlaufsende: zwei aneinanderstossende ergaeben einen Strich
      ctx.fillStyle = g; ctx.fillRect(0, 0, W, bis);
      if (t.oben !== t.flaeche) {
        var ob = ctx.createLinearGradient(0, 0, 0, Math.min(300, von));
        ob.addColorStop(0, rgba(t.oben, 0.9)); ob.addColorStop(1, rgba(t.oben, 0));
        ctx.fillStyle = ob; ctx.fillRect(0, 0, W, Math.min(300, von));
      }
      var u = ctx.createLinearGradient(0, H - 340, 0, H);
      u.addColorStop(0, "rgba(12,28,48,0)"); u.addColorStop(1, "rgba(12,28,48,.72)");
      ctx.fillStyle = u; ctx.fillRect(0, H - 340, W, 340);
    }

    var y = start;
    ctx.textAlign = "center";
    if (s.oben) {
      ctx.font = "600 25px " + SANS; sperren(ctx, 5); ctx.fillStyle = t.schrift;
      ctx.fillText(String(s.oben).toUpperCase(), W / 2, y + 26); sperren(ctx, 0);
      y += obenH;
    }
    function zeilen(ls) {
      ls.forEach(function (z) {
        y += 66;
        zeileZeichnen(ctx, z.map(function (w) { return w; }), W / 2, y - 12, "mitte", zFont, function () { return t.schrift; });
      });
    }
    zeilen(l1);
    if (wort) {
      ctx.font = "italic 400 " + wg + "px " + SERIF; ctx.textAlign = "center";
      y += wg * 1.1 + 4;
      leuchtend(ctx, wort, W / 2, y - wg * 0.22, t);
      y += 10;
    }
    zeilen(l2);

    var hell = !!foto, handFarbe = hell ? "#fff" : t.schrift;
    function hand(text, rechts) {
      if (!text) return;
      ctx.save();
      ctx.font = "72px " + HAND; ctx.fillStyle = handFarbe;
      if (hell) { ctx.shadowColor = "rgba(12,28,48,.7)"; ctx.shadowBlur = 14; ctx.shadowOffsetY = 2; }
      if (rechts) { ctx.textAlign = "right"; ctx.fillText(text, W - 62, H - 58); }
      else { ctx.translate(62, H - 52); ctx.rotate(-0.1); ctx.textAlign = "left"; ctx.fillText(text, 0, 0); }
      ctx.restore();
    }
    hand(s.links == null ? "speicher dir das" : s.links, false);
    hand(s.rechts == null ? "wisch weiter →" : s.rechts, true);
  }

  function karten(ctx, s, car, index, t) {
    var zeilen = String(s.body || "").split("\n").map(function (z) { return z.trim(); }).filter(Boolean);
    var karten = zeilen.filter(function (z) { return z.indexOf("|") >= 0; });
    var absatz = zeilen.filter(function (z) { return z.indexOf("|") < 0; }).join(" ");
    var nr = 0;
    car.slides.slice(0, index).forEach(function (a) {
      if (a.layout === "m-liste") nr += String(a.body || "").split("\n").filter(function (z) { return z.indexOf("|") >= 0; }).length;
    });
    return { karten: karten, absatz: absatz, nr: nr };
  }

  function liste(ctx, s, car, index, total, t) {
    grund(ctx, t); kopf(ctx, s, index, total, t);
    var d = karten(ctx, s, car, index, t), x = 62, kw = W - 124;
    var erg = passend(H - 66 - 180, function (f) {
      var bl = [];
      if (s.headline) { var ti = titelBlock(ctx, s.headline, kw, 70 * f, t); ti.luft = 30; bl.push(ti); }
      d.karten.forEach(function (z, i) {
        var teile = z.split("|").map(function (p) { return p.trim(); });
        var tag = (teile[2] || "").toUpperCase();
        ctx.font = "600 22px " + SANS; sperren(ctx, 1.8);
        var tb = tag ? ctx.measureText(tag).width + 40 : 0; sperren(ctx, 0);
        var nb = 138 * Math.max(f, 0.85);
        var inhalt = kw - 64 - nb - (tag ? tb + 20 : 0);
        var kt = textBlock(ctx, teile[0], inhalt, 41 * f, 1.15, 600, CREME);
        var kb = textBlock(ctx, teile[1] || "", inhalt, 31 * f, 1.28, 400,
          { schrift: "#29556d", akzent: "#dc822e" });
        var h = 60 * f + kt.h + 6 + kb.h;
        bl.push({ h: h, luft: 24, zeichne: function (x0, y) {
          karteFlaeche(ctx, x0, y, kw, h);
          var nummer = String(d.nr + i + 1); if (nummer.length < 2) nummer = "0" + nummer;
          ctx.font = "italic 400 " + 86 * Math.max(f, 0.85) + "px " + SERIF;
          ctx.fillStyle = "#12828c"; ctx.textAlign = "left";
          ctx.fillText(nummer, x0 + 34, y + h / 2 + 30 * Math.max(f, 0.85));
          kt.zeichne(x0 + 32 + nb, y + 30 * f, "links");
          kb.zeichne(x0 + 32 + nb, y + 30 * f + kt.h + 6, "links");
          if (tag) {
            var tx = x0 + kw - 32 - tb, ty = y + h / 2 - 25;
            ctx.fillStyle = "rgba(18,130,140,.12)"; rund(ctx, tx, ty, tb, 50, 25); ctx.fill();
            ctx.font = "600 22px " + SANS; sperren(ctx, 1.8); ctx.fillStyle = "#0d666e";
            ctx.fillText(tag, tx + 20, ty + 33); sperren(ctx, 0);
          }
        } });
      });
      if (d.absatz) { var ab = textBlock(ctx, d.absatz, kw, 38 * f, 1.36, 400, t); ab.vor = 10; ab.luft = 20; bl.push(ab); }
      if (s.notiz) bl.push(notizBlock(ctx, s.notiz, 72 * f, t));
      return bl;
    });
    stapeln(erg, 180, H - 66, x);
    if (index < total - 1) weiter(ctx, t);
  }

  function gedanke(ctx, s, index, total, t) {
    grund(ctx, t); kopf(ctx, s, index, total, t);
    var kw = W - 124;
    var erg = passend(H - 66 - 180, function (f) {
      var bl = [];
      var ti = titelBlock(ctx, s.headline, kw, 96 * f, t); ti.luft = 36; bl.push(ti);
      if (s.body) { var ab = textBlock(ctx, s.body, kw, 38 * f, 1.36, 400, t); ab.luft = 20; bl.push(ab); }
      if (s.notiz) bl.push(notizBlock(ctx, s.notiz, 72 * f, t));
      return bl;
    });
    stapeln(erg, 180, H - 66, 62);
    if (index < total - 1) weiter(ctx, t);
  }

  function auftrag(ctx, s, index, total, t) {
    grund(ctx, t); kopf(ctx, s, index, total, t);
    var kw = W - 124;
    var bloecke = String(s.body || "").split(/\n\s*\n/).map(function (b) { return b.trim(); }).filter(Boolean);
    var erg = passend(H - 66 - 170, function (f) {
      var bl = [];
      if (s.headline) { var ti = titelBlock(ctx, s.headline, kw, 70 * f, t); ti.luft = 40; bl.push(ti); }
      bloecke.forEach(function (text, i) {
        var tb = textBlock(ctx, text, kw - 76, 34 * f, 1.36, 400, CREME);
        var h = 64 * f + 39 + tb.h;
        bl.push({ h: h, luft: 24, zeichne: function (x0, y) {
          karteFlaeche(ctx, x0, y, kw, h);
          ctx.font = "600 25px " + SANS; sperren(ctx, 3); ctx.fillStyle = "#0d666e"; ctx.textAlign = "left";
          ctx.fillText((bloecke.length > 1 ? "AUFTRAG " + (i + 1) : "AUFTRAG"), x0 + 38, y + 32 * f + 24);
          sperren(ctx, 0);
          tb.zeichne(x0 + 38, y + 32 * f + 39, "links");
        } });
      });
      return bl;
    });
    stapeln(erg, 170, H - 66, 62);
    if (index < total - 1) weiter(ctx, t);
  }

  function aufruf(ctx, s, t) {
    grund(ctx, t);
    var wort = "„" + String(s.headline || "").replace(/[„“"*]/g, "").trim() + "“";
    var wg = 150;
    while (wg > 60) {
      ctx.font = "italic 400 " + wg + "px " + SERIF;
      if (ctx.measureText(wort).width <= W - 140) break;
      wg -= 4;
    }
    var ab = null;
    if (s.body) {
      // Gleich lange Zeilen: enger setzen, solange die Zeilenzahl gleich bleibt
      var breit = 860;
      ab = textBlock(ctx, s.body, breit, 42, 1.36, 400, t);
      while (breit > 500) {
        var enger = textBlock(ctx, s.body, breit - 30, 42, 1.36, 400, t);
        if (enger.h > ab.h) break;
        ab = enger; breit -= 30;
      }
    }
    var obenText = s.oben == null ? "Kommentier" : s.oben;
    var hoehe = 170 + 64 + (obenText ? 120 : 0) + wg * 1.15 + 34 + (ab ? ab.h + 64 : 0) + (s.schild ? 68 : 0);
    var y = (H - hoehe) / 2;

    ctx.save();
    ctx.shadowColor = "rgba(220,130,46,.45)"; ctx.shadowBlur = 50;
    ctx.fillStyle = t.kachel; rund(ctx, W / 2 - 85, y, 170, 170, 40); ctx.fill();
    ctx.restore();
    if (geladen["favicon.png"]) ctx.drawImage(geladen["favicon.png"], W / 2 - 60, y + 25, 120, 120);
    y += 170 + 64;

    ctx.textAlign = "center";
    if (obenText) {
      ctx.font = "96px " + HAND; ctx.fillStyle = t.schrift;
      ctx.fillText(obenText, W / 2, y + 86);
      y += 120;
    }
    ctx.font = "italic 400 " + wg + "px " + SERIF;
    leuchtend(ctx, wort, W / 2, y + wg * 0.92, t);
    y += wg * 1.15 + 34;
    if (ab) {
      ab.zeichne(W / 2, y, "mitte");
      y += ab.h + 64;
    }
    if (s.schild) {
      var text = String(s.schild).toUpperCase();
      ctx.font = "600 26px " + SANS; sperren(ctx, 3.6);
      var b = ctx.measureText(text).width + 80;
      ctx.fillStyle = t.schild; rund(ctx, W / 2 - b / 2, y, b, 68, 34); ctx.fill();
      ctx.fillStyle = t.schildS; ctx.textAlign = "center"; ctx.fillText(text, W / 2, y + 44);
      sperren(ctx, 0);
    }
    ctx.textAlign = "left";
  }

  api.zeichne = function (canvas, slide, car, index, total, foto) {
    canvas.width = W; canvas.height = H;
    var ctx = canvas.getContext("2d");
    ctx.textBaseline = "alphabetic";
    var akzent = AKZENT[car.brand] || AKZENT.mlb_dark;
    if (slide.layout === "m-titel") titel(ctx, slide, car, akzent, foto);
    else if (slide.layout === "m-aufruf") aufruf(ctx, slide, akzent);
    else if (slide.layout === "m-liste") liste(ctx, slide, car, index, total, CREME);
    else if (slide.layout === "m-auftrag") auftrag(ctx, slide, index, total, CREME);
    else gedanke(ctx, slide, index, total, CREME);
  };
  return api;
})();
/* MASTER-VORLAGE-ENDE */
