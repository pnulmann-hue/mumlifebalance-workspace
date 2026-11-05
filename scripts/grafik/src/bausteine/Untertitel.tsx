import React, { useMemo } from "react";
import { AbsoluteFill, Sequence, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { theme } from "../theme";
import { H, SCHATTEN, philosopher, sourceSans, ss } from "./schrift";
import { TafelDaten, tafelHoehePx } from "./Tafel";

export type Wort = { text: string; startMs: number; endMs: number };
export type UntertitelVariante = "A" | "B" | "C" | "D";
type Seite = { startMs: number; endMs: number; tokens: Wort[] };

/**
 * Baustein „Untertitel" — wortgenau aus dem Transkript.
 *
 *   A · Zwei Schriften — Seiten bis zwei Zeilen, betonte Woerter Source Sans Black orange
 *   B · Aktives Wort   — 2–3 Woerter, das gerade gesprochene leuchtet orange
 *   C · Balken         — dunkler Balken, ruhige Schrift, 3–4 Woerter
 *   D · Serifen-Wort   — 2–3 Woerter Source Sans, je Seite EIN Wort gross in Philosopher, eine Zeile
 *
 * Gemeinsam: pausiert, solange eine Einblendung steht (nie zwei Texte uebereinander),
 * startet erst nach dem Hook, Umbruch nur zwischen Woertern (Flex, nie inline).
 */

// Zeilenbreite wird GERECHNET, nie geschaetzt. Wer Schriftgroessen aendert, aendert diese mit.
const BREITE_FEIN = 30;
const BREITE_BETONT = 56;
const ABSTAND = 14;
const ZEILE_MAX = 1080 * 0.86;

const rein = (w: string) => w.toLowerCase().replace(/[^a-zäöüß]/g, "");
const istBetont = (w: string, betont: string[]) => betont.some((b) => rein(w) === rein(b));

/** Variante D: betontes Wort aus `betont`, sonst das laengste Hauptwort (Grossbuchstabe, nicht am Seitenanfang). */
const serifenWort = (tokens: Wort[], betont: string[]): number => {
  const treffer = tokens.findIndex((t) => istBetont(t.text.trim(), betont));
  if (treffer >= 0) return treffer;
  let best = -1;
  let laenge = 4;
  tokens.forEach((t, i) => {
    const w = t.text.trim();
    const n = rein(w).length;
    if (/^[A-ZÄÖÜ]/.test(w) && n > laenge && (i > 0 || n >= 7)) { best = i; laenge = n; }
  });
  return best;
};

const seitenA = (woerter: Wort[], betont: string[]): Seite[] => {
  const seiten: Seite[] = [];
  let gruppe: Wort[] = [];
  let breite = 0;
  const platz = ZEILE_MAX * 2;
  const zu = () => {
    if (gruppe.length) seiten.push({ startMs: gruppe[0].startMs, endMs: gruppe[gruppe.length - 1].endMs, tokens: gruppe });
    gruppe = []; breite = 0;
  };
  for (const w of woerter) {
    const roh = w.text.trim();
    const bw = roh.length * (istBetont(roh, betont) ? BREITE_BETONT : BREITE_FEIN) + ABSTAND;
    if (gruppe.length && breite + bw > platz) zu();
    gruppe.push(w); breite += bw;
    if (/[.!?,;:–—]$/.test(roh)) zu();
  }
  zu();
  return seiten;
};

const seitenFest = (woerter: Wort[], max: number): Seite[] => {
  const seiten: Seite[] = [];
  let g: Wort[] = [];
  for (const w of woerter) {
    g.push(w);
    if (g.length >= max || /[.!?,;:]$/.test(w.text.trim())) {
      seiten.push({ startMs: g[0].startMs, endMs: g[g.length - 1].endMs, tokens: g }); g = [];
    }
  }
  if (g.length) seiten.push({ startMs: g[0].startMs, endMs: g[g.length - 1].endMs, tokens: g });
  return seiten;
};

export const Untertitel: React.FC<{
  woerter: Wort[]; betont: string[]; variante?: UntertitelVariante;
  frei: { abSek: number; dauer: number }[]; abSek: number; hoehe?: number;
  /** Steht eine Tafel, rutscht der Untertitel direkt darunter (Tafel und Untertitel laufen zusammen). */
  tafeln?: TafelDaten[];
}> = ({ woerter, betont, variante = "A", frei, abSek, hoehe = 0.56, tafeln = [] }) => {
  const { fps } = useVideoConfig();
  const seiten = useMemo(
    () => (variante === "A" ? seitenA(woerter, betont) : seitenFest(woerter, variante === "C" ? 4 : 3)),
    [woerter, betont, variante],
  );
  const f = (ms: number) => Math.round((ms / 1000) * fps);
  const ab = Math.round(abSek * fps);
  return (
    <>
      {seiten.map((s, i) => {
        const startSek = s.startMs / 1000;
        const endeSek = s.endMs / 1000;
        if (frei.some((e) => startSek < e.abSek + e.dauer && endeSek > e.abSek)) return null;
        const naechste = seiten[i + 1];
        const ende = naechste ? f(naechste.startMs) : f(s.endMs) + fps;
        if (ende <= ab) return null;
        const von = Math.max(f(s.startMs), ab);
        const tafel = tafeln.find((t) => startSek < t.bisSek && endeSek > t.abSek);
        const seitenHoehe = tafel ? hoehe + (tafelHoehePx(tafel) + 18) / H : hoehe;
        return (
          <Sequence key={i} from={von} durationInFrames={Math.max(ende - von, 1)}>
            <SeiteBild seite={s} betont={betont} variante={variante} hoehe={seitenHoehe} versatzMs={von * 1000 / fps} />
          </Sequence>
        );
      })}
    </>
  );
};

const SeiteBild: React.FC<{ seite: Seite; betont: string[]; variante: UntertitelVariante; hoehe: number; versatzMs: number }> = ({
  seite, betont, variante, hoehe, versatzMs,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const jetztMs = versatzMs + (frame / fps) * 1000;
  const pop = interpolate(frame, [0, 4], [0.97, 1], { easing: theme.ease.out, extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const zeile: React.CSSProperties = {
    display: "flex", flexWrap: "wrap", justifyContent: "center", alignItems: "baseline",
    columnGap: 14, rowGap: 2, width: "86%", transform: `scale(${pop})`,
    overflowWrap: "normal", wordBreak: "keep-all", hyphens: "none",
  };
  const rahmen: React.CSSProperties = { justifyContent: "flex-start", alignItems: "center", paddingTop: H * hoehe };

  if (variante === "C") {
    return (
      <AbsoluteFill style={rahmen}>
        <div style={{ ...zeile, width: "auto", maxWidth: "86%", background: "rgba(12,28,48,0.72)", borderRadius: 16, padding: "10px 26px 14px" }}>
          {seite.tokens.map((t, i) => (
            <span key={i} style={{ fontFamily: sourceSans.fontFamily, fontWeight: 600, fontSize: 64, lineHeight: 1.15, color: theme.colors.text }}>
              {ss(t.text.trim())}
            </span>
          ))}
        </div>
      </AbsoluteFill>
    );
  }

  if (variante === "D") {
    const serif = serifenWort(seite.tokens, betont);
    // Eine Zeile: Breite gerechnet, zu Langes wird kleiner statt umzubrechen.
    const breite = seite.tokens.reduce((n, t, i) => n + ss(t.text.trim()).length * (i === serif ? 46 : 37) + 22, 0);
    const k = Math.min(1, (1080 * 0.88) / breite);
    return (
      <AbsoluteFill style={rahmen}>
        <div style={{ ...zeile, flexWrap: "nowrap", width: "auto", columnGap: 22 * k, whiteSpace: "nowrap", textShadow: SCHATTEN }}>
          {seite.tokens.map((t, i) => (
            <span key={i} style={i === serif
              ? { fontFamily: philosopher.fontFamily, fontWeight: 400, fontSize: 96 * k, lineHeight: 1.1, color: theme.colors.text }
              : { fontFamily: sourceSans.fontFamily, fontWeight: 800, fontSize: 68 * k, lineHeight: 1.1, color: theme.colors.text }}>
              {ss(t.text.trim())}
            </span>
          ))}
        </div>
      </AbsoluteFill>
    );
  }

  return (
    <AbsoluteFill style={rahmen}>
      <div style={{ ...zeile, columnGap: variante === "B" ? 26 : 14, textShadow: SCHATTEN }}>
        {seite.tokens.map((t, i) => {
          const w = ss(t.text.trim());
          if (variante === "B") {
            // aktiv ist genau EIN Wort: das zuletzt begonnene (Zeitstempel ueberlappen oft)
            let aktivIdx = -1;
            seite.tokens.forEach((x, k) => { if (x.startMs <= jetztMs) aktivIdx = k; });
            const aktiv = i === aktivIdx;
            return (
              <span key={i} style={{
                fontFamily: sourceSans.fontFamily, fontWeight: 800, fontSize: 82, lineHeight: 1.1,
                letterSpacing: "-0.01em", color: aktiv ? theme.colors.accent : theme.colors.text,
                transform: `scale(${aktiv ? 1.06 : 1})`,
              }}>{w}</span>
            );
          }
          const dick = istBetont(w, betont);
          return (
            <span key={i} style={{
              fontFamily: dick ? sourceSans.fontFamily : philosopher.fontFamily,
              fontWeight: dick ? 900 : 400, fontSize: dick ? 96 : 60,
              letterSpacing: dick ? "-0.02em" : "0.01em", lineHeight: 1.14,
              color: dick ? theme.colors.accent : theme.colors.text,
            }}>{w}</span>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
