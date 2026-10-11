# -*- coding: utf-8 -*-
"""Repariert die Blotato-Freigabe für Karussells (14.09.2026).

Was ich kaputt gemacht habe: Die Freigabe für Blotato hing im Karussell-Editor
(`setupBlotato`, aufgerufen aus `renderEditor` aus `renderKarussell`). Als der Editor
rausflog, war sie nicht mehr erreichbar — Karussells hatten keinen Weg mehr zu Blotato.

Die Reparatur macht es zugleich einfacher, statt es nur wiederherzustellen: Der Knopf
**Freigeben** auf der Wochenkarte legt jetzt beides ab — die Texte stehen, und die
fertigen Folien plus Caption, Datum und Profil landen in der Sammlung `freigaben`.

Das ist noch kein Einplanen. Eingeplant wird erst, wenn Patricia es im Chat sagt und
`scripts/cockpit/freigabe-zu-blotato.mjs` läuft — die Regel „nie ohne ausdrückliches Go"
bleibt unangetastet.

Wiederholbar.
"""
import io, os

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
PFAD = "outputs/cockpit/mlb-cockpit.html"
t = io.open(PFAD, encoding="utf-8").read()
vorher = t
getan, schon = [], []


def setze(alt, neu, was, marker):
    global t
    if alt in t:
        t = t.replace(alt, neu, 1)
        getan.append(was)
    elif marker in t:
        schon.append(was)
    else:
        print("!! Anker nicht gefunden:", was)


# Profil-Auswahl auf die Wochenkarte, damit Blotato weiss wohin
setze("""          '<input type="date" value="' + esc(b.obj.datum || "") + '">' +
          '<button class="btn">Caption kopieren</button>' +""",
      """          '<input type="date" value="' + esc(b.obj.datum || "") + '">' +
          '<select class="btn wk-profil">' +
            '<option value="mentoring"' + ((b.obj.blotato && b.obj.blotato.profil) === "doterra" ? "" : " selected") + '>Mentoring</option>' +
            '<option value="doterra"' + ((b.obj.blotato && b.obj.blotato.profil) === "doterra" ? " selected" : "") + '>doTERRA</option>' +
          '</select>' +
          '<button class="btn">Caption kopieren</button>' +""",
      "Profil-Auswahl auf der Wochenkarte",
      marker='wk-profil')

# Der Freigabe-Knopf legt die Folien mit ab
setze("""    var freigabeKnopf = felder[felder.length - 1];
    freigabeKnopf.onclick = function () {
      b.obj.textfrei = !b.obj.textfrei;
      if (b.art === "reels") saveReel(b.obj); else saveCarousel(b.obj);
      toast(b.obj.textfrei ? "Freigegeben" : "Freigabe zurückgenommen");
      render();
    };""",
      """    var profilWahl = karte.querySelector(".wk-profil");
    if (profilWahl) {
      profilWahl.onchange = function () {
        var bl = b.obj.blotato || (b.obj.blotato = {});
        bl.profil = this.value;
        if (b.art === "reels") saveReel(b.obj); else saveCarousel(b.obj);
      };
    }

    var freigabeKnopf = felder[felder.length - 1];
    freigabeKnopf.onclick = function () {
      var an = !b.obj.textfrei;
      b.obj.textfrei = an;
      if (b.art === "reels") saveReel(b.obj); else saveCarousel(b.obj);

      // Zurueckgenommen: nur den Vermerk setzen, nichts loeschen.
      if (!an) {
        if (db) {
          db.collection("freigaben").doc(b.id).set({
            name: b.titel, status: "zurueckgezogen",
            updatedAt: new Date().toISOString()
          }).catch(function () {});
        }
        toast("Freigabe zurückgenommen");
        render();
        return;
      }

      if (!db) { toast("Freigegeben — aber ohne Datenbank nur lokal."); render(); return; }
      if (!b.obj.datum) { toast("Freigegeben. Setz noch ein Datum, sonst kann ich es nicht einplanen."); render(); return; }
      if (!(b.caption || "").trim()) { toast("Freigegeben. Ohne Caption kann ich es aber nicht einplanen."); render(); return; }

      var bl = b.obj.blotato || (b.obj.blotato = {});
      var profil = bl.profil || "mentoring";
      var zeit = bl.zeit || (b.art === "reels" ? "18:00" : "07:30");
      var wann = new Date(b.obj.datum + "T" + zeit);

      function steuerSchreiben(anzahl) {
        db.collection("freigaben").doc(b.id).set({
          name: b.titel,
          typ: b.art === "reels" ? "reel" : "karussell",
          caption: b.caption || "",
          videodatei: b.obj.videodatei || "",
          profil: profil,
          datum: b.obj.datum,
          zeit: zeit,
          zeitpunktISO: isNaN(wann) ? "" : wann.toISOString(),
          anzahl: anzahl,
          status: "wartet",
          updatedAt: new Date().toISOString()
        }).then(function () {
          bl.status = "wartet";
          if (b.art === "reels") saveReel(b.obj); else saveCarousel(b.obj);
          toast("Freigegeben und abgelegt. Sag es mir im Chat, dann plane ich es ein.");
          render();
        }).catch(function () { toast("Das Ablegen hat nicht geklappt."); render(); });
      }

      // Beim Karussell wandern die fertigen Folien mit — genau so, wie sie hier aussehen.
      if (b.art === "karussells" && b.obj.slides && b.obj.slides.length) {
        var i = 0, gesamt = b.obj.slides.length;
        freigabeKnopf.disabled = true;
        (function naechste() {
          if (i >= gesamt) { freigabeKnopf.disabled = false; steuerSchreiben(gesamt); return; }
          var nr = i++;
          freigabeKnopf.textContent = "lege Folie " + (nr + 1) + " von " + gesamt + " ab …";
          slideJpeg(b.obj, b.obj.slides[nr], nr, function (dataUrl) {
            db.doc("freigaben/" + b.id).collection("bilder")
              .doc("slide-" + String(nr + 1).padStart(2, "0"))
              .set({ dataUrl: dataUrl, nr: nr + 1 })
              .then(naechste)
              .catch(function () {
                freigabeKnopf.disabled = false;
                toast("Folie " + (nr + 1) + " liess sich nicht ablegen.");
                render();
              });
          });
        })();
        return;
      }
      steuerSchreiben(1);
    };""",
      "Freigeben legt Folien, Caption und Termin ab",
      marker="Freigegeben und abgelegt")

if t != vorher:
    io.open(PFAD, "w", encoding="utf-8", newline="\n").write(t)

print("Geaendert:")
for z in getan:
    print("  +", z)
if schon:
    print("Schon so:")
    for z in schon:
        print("  =", z)
if not getan:
    print("  (nichts zu tun)")
