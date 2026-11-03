  /* ======================================================================
     Reiter "Ölschule-Calls" — doTERRA -> Ölschule-Calls
     (seit 03.11.2026, patch-academy.py)

     Patricia: „kannst du mir die auch irgendwie als wissensdatenbank ins
     cockpit unter doTERRA ablegen?" — je Academy-Call die Learnings zum
     Nachlesen, mit Suche über alle Calls.
     Daten: Sammlung "academy", ein Dokument je Call {datum, titel, md},
     gebaut von scripts/doterra/academy-calls-pdf.mjs (dieselbe Quelle wie
     die PDFs, nur die Learnings, kein Wortlaut).
     ====================================================================== */
  var academy = null;
  var academySuche = "";

  function academyLaden(fertig) {
    if (academy) { fertig(); return; }
    var lokal = lsGet("academy", null);
    if (lokal) { academy = lokal; fertig(); }
    if (!db) {
      if (!lokal) setTimeout(function () { if (db) academyLaden(fertig); }, 1500);
      return;
    }
    db.collection("academy").limit(100).get().then(function (snap) {
      var calls = [];
      snap.docs.forEach(function (d) { calls.push(tief(d.data())); });
      calls.sort(function (a, b) { return String(b.datum).localeCompare(String(a.datum)); });
      academy = { items: calls };
      lsSet("academy", academy);
      fertig();
    }).catch(function () {
      if (!lokal) { academy = { items: [], fehler: true }; fertig(); }
    });
  }

  function renderAcademy(main) {
    main.innerHTML =
      '<div class="page-head"><div><h1>Ölschule-Calls</h1>' +
      '<p>Was in den Calls der Ölschule Academy gelehrt wurde, je Call zum Nachlesen. ' +
      'Schulungswissen mit Gesundheitsaussagen: für dich, nicht 1:1 für Kundinnen.</p></div></div>' +
      '<div class="panel ac-suche"><input type="search" placeholder="In allen Calls suchen: Öl, Thema, Stichwort …" ' +
      'value="' + esc(academySuche) + '"></div>' +
      '<div id="acinhalt"><div class="panel"><div class="empty">Lädt …</div></div></div>';
    var feld = main.querySelector(".ac-suche input");
    feld.addEventListener("input", function () {
      academySuche = feld.value;
      academyListe(main.querySelector("#acinhalt"));
    });
    academyLaden(function () { academyListe(main.querySelector("#acinhalt")); });
  }

  function academyListe(box) {
    if (!box) return;
    var alle = (academy && academy.items) || [];
    if (!alle.length) {
      box.innerHTML = '<div class="panel"><div class="empty">' +
        (academy && academy.fehler ? "Die Calls liessen sich nicht laden." : "Noch keine Calls abgelegt.") +
        '</div></div>';
      return;
    }
    var s = academySuche.trim().toLowerCase();
    var liste = alle.filter(function (c) {
      return !s || (c.titel + " " + c.md).toLowerCase().indexOf(s) >= 0;
    });
    if (!liste.length) {
      box.innerHTML = '<div class="panel"><div class="empty">Kein Call nennt „' + esc(academySuche) + '“.</div></div>';
      return;
    }
    box.innerHTML = liste.map(function (c, i) {
      var treffer = "";
      if (s) {
        var n = (c.md.toLowerCase().split(s).length - 1);
        treffer = '<span class="ac-treffer">' + n + "× gefunden</span>";
      }
      return '<details class="panel ac-call" data-i="' + i + '"><summary>' +
        '<span class="ac-datum">' + esc(c.datumText || c.datum) + '</span>' +
        '<span class="ac-titel">' + esc(c.titel) + '</span>' + treffer +
        '</summary><div class="ac-inhalt"></div></details>';
    }).join("");
    box.querySelectorAll(".ac-call").forEach(function (d) {
      d.addEventListener("toggle", function () {
        var ziel = d.querySelector(".ac-inhalt");
        if (d.open && !ziel.innerHTML) ziel.innerHTML = zgMarkdown(liste[+d.dataset.i].md);
      });
    });
  }
