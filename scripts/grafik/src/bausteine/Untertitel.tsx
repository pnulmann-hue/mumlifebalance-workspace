import React, { useMemo } from "react";
import { AbsoluteFill, Sequence, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { theme } from "../theme";
import { H, SCHATTEN, philosopher, sourceSans, ss } from "./schrift";

export type Wort = { text: string; startMs: number; endMs: number };
export type UntertitelVariante = "A" | "B" | "C";
type Seite = { startMs: number; endMs: number; tokens: Wort[] };

/**
 * Baustein „Untertitel" — wortgenau aus dem Transkript.
 *
 *   A · Zwei Schriften — Seiten bis zwei Zeilen, betonte Woerter Source Sans Black orange
 *   B · Aktives Wort   — 2–3 Woerter, das gerade gesprochene leuchtet orange
 *   C · Balken         — dunkler Balken, ruhige Schrift, 3–4 Woerter
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
}> = ({ woerter, betont, variante = "A", frei, abSek, hoehe = 0.56 }) => {
  const { fps } = useVideoConfig();
  const seiten = useMemo(
    () => (variante === "A" ? seitenA(woerter, betont) : seitenFest(woerter, variante === "B" ? 3 : 4)),
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
        return (
          <Sequence key={i} from={von} durationInFrames={Math.max(ende - von, 1)}>
            <SeiteBild seite={s} betont={betont} variante={variante} hoehe={hoehe} versatzMs={von * 1000 / fps} />
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
