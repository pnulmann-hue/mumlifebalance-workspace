"""Neue Mail-Fassungen je Automation gezielt laden (28.09.2026).

Anlass: Patricia sah bei Nr. 42 nur die alten ActiveCampaign-Mails, weder
„neue Fassung“ noch die Kopier-Knöpfe — obwohl die zwei Entwürfe in
`mailentwuerfe` lagen. Die Sammlung wurde einmal je Seitenaufruf komplett
geholt; schlug das fehl, blieb die Liste still leer (`.catch(function(){})`).

Jetzt:
- Beim Aufklappen holt das Cockpit gezielt die Entwürfe dieser Automation
  (`where automation in ["42", 42]`), mit einem zweiten Versuch.
- Schlägt es fehl, steht der Grund auf der Karte, statt dass nichts passiert.
- Die Sammel-Abfrage bleibt für das Schild „neue Fassung“ im Kopf.

    python scripts/cockpit/patch-mailentwuerfe-gezielt.py <datei.html> [...]
"""
import sys, pathlib

ALT_FUER = """  function entwuerfeFuer(nummer) {
    return (mailEntwuerfe || []).filter(function (e) {
      return String(e.automation) === String(nummer);
    }).sort(function (a, b) { return (a.reihenfolge || 0) - (b.reihenfolge || 0); });
  }
  function mailListe(nummer) {
    var neu = entwuerfeFuer(nummer);
    if (!neu.length) return mailListeAC(nummer);"""

NEU_FUER = """  /* Je Automation gezielt geholt (28.09.2026) — die Sammel-Abfrage oben
     kam bei Patricia leer an, ohne Fehler. Jetzt sagt die Karte, was los ist. */
  var entwurfJe = {};
  function entwuerfeJeHolen(nummer) {
    var k = String(nummer);
    if (!db || (entwurfJe[k] && entwurfJe[k].status !== "fehler")) return;
    entwurfJe[k] = { status: "laedt", liste: [] };
    function versuch(nochmal) {
      db.collection("mailentwuerfe").where("automation", "in", [k, Number(k)]).limit(50).get()
        .then(function (qs) {
          entwurfJe[k] = { status: "ok", liste: qs.docs.map(function (d) {
            var x = d.data() || {}; x.id = d.id; return x; }) };
          if (activeTab === "mailings") render();
        }).catch(function (e) {
          if (nochmal) { setTimeout(function () { versuch(false); }, 1200); return; }
          entwurfJe[k] = { status: "fehler", liste: [],
            fehler: (e && (e.code || e.message)) || "unbekannt" };
          if (activeTab === "mailings") render();
        });
    }
    versuch(true);
  }
  function entwurfNachId(id) {
    var alle = (mailEntwuerfe || []).slice();
    Object.keys(entwurfJe).forEach(function (k) { alle = alle.concat(entwurfJe[k].liste || []); });
    return alle.filter(function (x) { return x.id === id; })[0];
  }
  function entwuerfeFuer(nummer) {
    var eigen = entwurfJe[String(nummer)];
    var quelle = (eigen && eigen.liste.length) ? eigen.liste : (mailEntwuerfe || []);
    return quelle.filter(function (e) {
      return String(e.automation) === String(nummer);
    }).sort(function (a, b) { return (a.reihenfolge || 0) - (b.reihenfolge || 0); });
  }
  function mailListe(nummer) {
    entwuerfeJeHolen(nummer);
    var neu = entwuerfeFuer(nummer);
    if (!neu.length) {
      var st = entwurfJe[String(nummer)];
      var hinweis = !db ? "" :
        (st && st.status === "laedt") ? '<p class="note">Ich schaue nach, ob es eine neue Fassung von mir gibt …</p>' :
        (st && st.status === "fehler") ? '<p class="note" style="color:var(--crit)">Die neuen Fassungen liessen sich gerade nicht laden (' +
          esc(st.fehler) + '). Lade das Cockpit neu und klapp die Automation nochmal auf.</p>' : "";
      return hinweis + mailListeAC(nummer);
    }"""

ALT_DRAHT = """      var e = (mailEntwuerfe || []).filter(function (x) {
        return x.id === k.getAttribute("data-entwurf");
      })[0];"""
NEU_DRAHT = """      var e = entwurfNachId(k.getAttribute("data-entwurf"));"""

for pfad in sys.argv[1:]:
    p = pathlib.Path(pfad)
    t = p.read_text(encoding="utf-8")
    if "function entwuerfeJeHolen" in t:
        print(pfad, "schon gepatcht"); continue
    for alt, neu in ((ALT_FUER, NEU_FUER), (ALT_DRAHT, NEU_DRAHT)):
        # Zeilenenden der Datei übernehmen
        if "\r\n" in t:
            alt, neu = alt.replace("\n", "\r\n"), neu.replace("\n", "\r\n")
        assert t.count(alt) == 1, (pfad, alt[:60])
        t = t.replace(alt, neu)
    p.write_text(t, encoding="utf-8")
    print(pfad, "gepatcht")
