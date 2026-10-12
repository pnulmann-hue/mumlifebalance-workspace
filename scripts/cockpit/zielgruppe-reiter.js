  /* ======================================================================
     Reiter "Zielgruppe & Markt" — Instagram -> Zielgruppe & Markt
     (seit 12.10.2026, patch-zielgruppe.py)

     Zeigt das Dokument daten/zielgruppe: fuenf Teile aus den
     Content-Shortcut-Analysen, je als aufklappbare Karte. Der Inhalt ist
     Markdown und wird hier mit einem kleinen Leser in HTML verwandelt —
     Ueberschriften, Tabellen, Listen, Zitate, fett und kursiv. Mehr braucht
     es nicht, und alles wird vorher maskiert.

     Die Quelle sind die Markdown-Dateien im Workspace, nicht das Cockpit.
     Erzeugt von zielgruppe-bauen.py.
     ====================================================================== */
  function zgInline(s) {
    var t = esc(s);
    t = t.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
    t = t.replace(/(^|[^*\w])\*([^*\n]+)\*(?!\w)/g, "$1<em>$2</em>");
    t = t.replace(/`([^`]+)`/g, "<code>$1</code>");
    return t;
  }

  function zgZellen(zeile) {
    var z = zeile.trim();
    if (z.charAt(0) === "|") z = z.slice(1);
    if (z.charAt(z.length - 1) === "|") z = z.slice(0, -1);
    return z.split("|").map(function (c) { return c.trim(); });
  }

  function zgMarkdown(md) {
    var zeilen = String(md || "").replace(/\r/g, "").split("\n");
    var aus = [];
    var absatz = [];
    var i = 0;

    function absatzZu() {
      if (absatz.length) {
        aus.push("<p>" + zgInline(absatz.join(" ")) + "</p>");
        absatz = [];
      }
    }

    while (i < zeilen.length) {
      var z = zeilen[i];
      var leer = !z.trim();

      if (leer) { absatzZu(); i++; continue; }

      if (/^---+\s*$/.test(z)) { absatzZu(); aus.push("<hr>"); i++; continue; }

      var h = z.match(/^(#{2,4})\s+(.*)$/);
      if (h) {
        absatzZu();
        var stufe = h[1].length + 1;
        aus.push("<h" + stufe + ">" + zgInline(h[2]) + "</h" + stufe + ">");
        i++; continue;
      }

      if (/^\s*\|/.test(z) && i + 1 < zeilen.length && /^\s*\|[\s:|-]+\|?\s*$/.test(zeilen[i + 1])) {
        absatzZu();
        var kopf = zgZellen(z);
        i += 2;
        var html = '<div class="zg-tab"><table><thead><tr>' +
          kopf.map(function (c) { return "<th>" + zgInline(c) + "</th>"; }).join("") +
          "</tr></thead><tbody>";
        while (i < zeilen.length && /^\s*\|/.test(zeilen[i])) {
          html += "<tr>" + zgZellen(zeilen[i]).map(function (c) {
            return "<td>" + zgInline(c) + "</td>";
          }).join("") + "</tr>";
          i++;
        }
        aus.push(html + "</tbody></table></div>");
        continue;
      }

      if (/^>\s?/.test(z)) {
        absatzZu();
        var zitat = [];
        while (i < zeilen.length && /^>\s?/.test(zeilen[i])) {
          zitat.push(zeilen[i].replace(/^>\s?/, ""));
          i++;
        }
        aus.push("<blockquote>" + zgMarkdown(zitat.join("\n")) + "</blockquote>");
        continue;
      }

      if (/^\s*[-*]\s+/.test(z) || /^\s*\d+\.\s+/.test(z)) {
        absatzZu();
        var nummer = /^\s*\d+\.\s+/.test(z);
        var punkte = [];
        while (i < zeilen.length && (nummer ? /^\s*\d+\.\s+/ : /^\s*[-*]\s+/).test(zeilen[i])) {
          punkte.push(zeilen[i].replace(/^\s*([-*]|\d+\.)\s+/, ""));
          i++;
        }
        var tag = nummer ? "ol" : "ul";
        aus.push("<" + tag + ">" + punkte.map(function (p) {
          return "<li>" + zgInline(p) + "</li>";
        }).join("") + "</" + tag + ">");
        continue;
      }

      absatz.push(z.trim());
      i++;
    }
    absatzZu();
    return aus.join("\n");
  }

  function renderZielgruppe(main) {
    var doc = zgDaten || {};
    var teile = doc.teile || [];

    main.innerHTML =
      '<div class="page-head"><div><h1>Zielgruppe &amp; Markt</h1>' +
      '<p>Was deine Zielgruppe denkt, fragt und sucht, was die anderen in deiner ' +
      'Nische machen und wohin der Markt geht. Zum Nachschlagen beim Schreiben ' +
      'von Hooks, Captions und Kurslektionen.</p></div></div>' +
      '<div class="tiles">' +
        tile("Stand", doc.stand ? fmtDate(doc.stand) : "—", "Content-Shortcut-Analyse") +
        tile("Nächste Prüfung", esc(doc.naechste_pruefung || "—"), "mit eigenen Insights") +
      '</div>' +
      '<div class="panel zg-hinweis"><strong>Abgeleitet, nicht erfragt.</strong> ' +
      'Fragen und Begriffe kommen aus Google-Suchvorschlägen, Erfahrungsberichten ' +
      'und den Beiträgen von vier Konten. Persona, Gedanken und Sehnsüchte sind ' +
      'daraus abgeleitet und keine Zitate. Vor einem Hook gegen deine Regeln lesen ' +
      '(siehe „Auf einen Blick“).</div>' +
      '<div id="zgliste"></div>';

    var box = main.querySelector("#zgliste");
    if (!teile.length) {
      box.innerHTML = '<div class="panel"><div class="empty">Noch nichts da. ' +
        'Bauen mit <code>python scripts/cockpit/zielgruppe-bauen.py</code>, ' +
        'dann in die Datenbank unter daten/zielgruppe.</div></div>';
      return;
    }

    teile.forEach(function (t, n) {
      var d = document.createElement("details");
      d.className = "panel zg-teil";
      if (n === 0) d.open = true;
      d.innerHTML =
        '<summary><span class="zg-titel">' + esc(t.titel) + '</span>' +
        '<span class="zg-kurz">' + esc(t.kurz || "") + '</span></summary>' +
        '<div class="zg-inhalt"></div>';
      var gemalt = false;
      function malen() {
        if (gemalt || !d.open) return;
        d.querySelector(".zg-inhalt").innerHTML = zgMarkdown(t.md);
        gemalt = true;
      }
      d.addEventListener("toggle", malen);
      malen();
      box.appendChild(d);
    });
  }
