  /* ---------- Content-Kalender mit Instagram-Abgleich (16.10.2026) ----------
     Patricia: „ich will im contentkalender, dass das abgeglichen wird.“
     7 Tage zurück, 14 voraus. Je Tag: was geplant war, ob es auf Instagram
     wiedergefunden wurde (mit Zahlen), und was direkt in der App rausging.
     Quelle: daten/gepostet-zuordnung (gepostet-zuordnen.py, täglicher Abgleich). */
  function kaPostVon(igId) {
    var l = (igZuordnung && igZuordnung.letzte_posts) || [];
    for (var i = 0; i < l.length; i++) if (l[i].igId === igId) return l[i];
    return null;
  }
  function kaZahlen(p, z) {
    var reach = (p && p.reach != null) ? p.reach : (z && z.reach);
    if (reach == null) return "gepostet";
    var t = reach + " erreicht";
    if (p && p.rate) t += " · " + String(p.rate).replace(".", ",") + " %";
    else if (p && p.rate === 0) t += " · keine Reaktion";
    if (p && p.saved) t += " · " + p.saved + "× gespeichert";
    if (p && !p.reif) t += " · noch nicht ausgereift";
    return t;
  }
  function tiContent(el, heute, beitraege) {
    var von = new Date(heute + "T12:00:00"); von.setDate(von.getDate() - 7);
    var bis = new Date(heute + "T12:00:00"); bis.setDate(bis.getDate() + 14);
    var vonIso = tiIso(von), bisIso = tiIso(bis);
    var alle = alleBeitraege().filter(function (b) { return !(b.obj || b).abgelehnt; });
    var tage = {};
    function tag(d) { return tage[d] || (tage[d] = { geplant: [], spontan: [] }); }
    alle.forEach(function (b) {
      // Was gepostet ist, steht an dem Tag, an dem es wirklich rausging —
      // nicht am alten Plandatum.
      var ig = igPost(b);
      var d = (ig && ig.datum) || datumVon(b);
      if (d && d >= vonIso && d <= bisIso && b.art !== "storys") tag(d).geplant.push(b);
    });
    ((igZuordnung && igZuordnung.letzte_posts) || []).forEach(function (p) {
      if (!p.beitrag && p.datum >= vonIso && p.datum <= bisIso) tag(p.datum).spontan.push(p);
    });
    var ohne = beitraege.filter(function (b) { return !datumVon(b); }).length;
    var stand = igZuordnung && igZuordnung.stand;
    el.innerHTML = '<span class="ti-chip">Content-Kalender · 7 Tage zurück, 14 voraus</span>' +
      '<div class="ti-klein">Abgleich mit Instagram: ' + (stand ? "Stand " + esc(fmtDate(stand)) : "noch keiner") +
      ' · doTERRA hängt nicht an der Schnittstelle</div><div id="ti-cl"></div>';
    var box = el.querySelector("#ti-cl");
    var keys = Object.keys(tage).sort();
    if (!keys.length) box.innerHTML = '<div class="ti-leer">In diesem Zeitraum ist nichts geplant.</div>';
    keys.forEach(function (d) {
      var dt = new Date(d + "T12:00:00"), vorbei = d < heute;
      var t = tage[d];
      t.geplant.sort(function (a, b) { return a.format < b.format ? -1 : 1; });
      t.geplant.forEach(function (b) {
        var o = b.obj, ig = igPost(b), s;
        if (ig) {
          s = { art: "gut", text: "✅ gepostet · " + kaZahlen(kaPostVon(ig.igId), ig), link: ig.link };
        } else if (vorbei && nichtPruefbar(b)) {
          s = { art: "info", text: "doTERRA · nicht prüfbar" };
        } else if (vorbei) {
          s = { art: "warn", text: istDraussen(b) ? "⚠️ eingeplant, aber auf Instagram nicht gefunden"
                                                  : "⚠️ nicht rausgegangen" };
        } else {
          s = tpStand(b);
        }
        box.appendChild(kaZeile(d, dt, b.format, kartenProfil(o) === "doterra" ? "doTERRA" : "Mentoring",
          b.titel || b.format, b.hook && b.hook !== b.titel ? b.hook : "", s, b, vorbei));
      });
      t.spontan.forEach(function (p) {
        box.appendChild(kaZeile(d, dt, p.typ === "REELS" ? "Reel" : "Beitrag", "Mentoring",
          p.anfang, "", { art: "info", text: "📌 direkt auf Instagram · " + kaZahlen(p), link: p.link }, null, vorbei));
      });
    });
    if (ohne) {
      var v = document.createElement("div");
      v.className = "ti-klein"; v.style.marginTop = "10px";
      v.textContent = ohne + (ohne === 1 ? " Beitrag liegt" : " Beiträge liegen") + " ohne Datum im Vorrat.";
      el.appendChild(v);
    }
  }
  function kaZeile(d, dt, format, profil, titel, hook, s, b, vorbei) {
    var p = document.createElement("div");
    p.className = "ti-post" + (vorbei ? " ka-vorbei" : "") + (d === tiIso(new Date()) ? " ka-heute" : "");
    p.innerHTML = '<div class="ti-datum">' + WOCHENTAGE[dt.getDay()].slice(0, 2) + '<b>' + dt.getDate() + '</b>' +
      dt.toLocaleDateString("de-CH", { month: "short" }) + '</div><div>' +
      '<span class="ti-mini">' + esc(format) + '</span> <span class="ti-mini">' + esc(profil) + '</span> ' +
      '<span class="ti-stand ' + s.art + '">' + esc(s.text) + '</span>' +
      '<h4>' + esc(titel) + '</h4>' + (hook ? '<div class="hook">' + esc(hook) + '</div>' : "") +
      '<div class="ti-knoepfe"></div></div>';
    var k = p.querySelector(".ti-knoepfe");
    if (s.link) {
      var a = document.createElement("a");
      a.className = "ti-btn"; a.href = s.link; a.target = "_blank"; a.rel = "noopener";
      a.textContent = "Auf Instagram ansehen";
      k.appendChild(a);
    }
    if (b) {
      var an = document.createElement("button");
      an.className = "ti-btn" + (vorbei ? "" : " voll"); an.textContent = "In der Woche ansehen";
      an.onclick = function () { springeZuBeitrag(b); };
      k.appendChild(an);
      if (!vorbei && !istDraussen(b) && istFertig(b) && !zeitpunktVorbei(b)) {
        var fr = document.createElement("button");
        fr.className = "ti-btn orange"; fr.textContent = "Freigeben";
        fr.onclick = function () { activeTab = "fertig"; render(); };
        k.appendChild(fr);
      }
    }
    return p;
  }
