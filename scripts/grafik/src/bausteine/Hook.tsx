import React from "react";
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { theme } from "../theme";
import { H, SCHATTEN, philosopher, sourceSans, ss } from "./schrift";

export type HookVariante = "A" | "B" | "C";

/**
 * Schriftgroesse, bei der das LAENGSTE Wort noch in 86 % Breite passt.
 * Ein Wort wird nie zerbrochen — passt es nicht, wird die Schrift kleiner
 * (gefunden 06.10.2026: „Selbststaendigkeitsversprechungen" lief rechts aus dem Bild).
 * `em` = mittlere Zeichenbreite der Schrift im Verhaeltnis zur Groesse.
 */
const passend = (text: string, basis: number, em: number) => {
  const laengstes = Math.max(...text.split(/\s+/).map((w) => w.length), 1);
  return Math.min(basis, Math.floor((1080 * 0.86) / (laengstes * em)));
};

/**
 * Baustein „Hook" — die ersten Sekunden. Zwei Zeilen: `fein` fuehrt hin,
 * `kraeftig` ist die Aussage. Oberkante bei 56 % der Hoehe, also unter dem Kinn (Patricia 06.10.2026: „verdeckt etwas
 * mein kinn" — vorher 43 %). Unten bleibt Luft bis zur toten Zone bei 82 %.
 *
 *   A · Zwei Schriften  — Philosopher kursiv fein, darunter Source Sans Black gross
 *   B · Kelsie          — kraeftige Zeile baut sich Wort fuer Wort auf, Verlauf im Buchstaben
 *   C · Balken          — Story-Stil: Creme-Balken mit dunkelblauer Schrift
 */
export const Hook: React.FC<{ fein: string; kraeftig: string; variante?: HookVariante; hoehe?: number }> = ({
  fein, kraeftig, variante = "A", hoehe = 0.56,
}) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const raus = interpolate(frame, [durationInFrames - 9, durationInFrames], [1, 0], {
    easing: theme.ease.in, extrapolateLeft: "clamp", extrapolateRight: "clamp",
  });
  const s1 = spring({ frame, fps, config: theme.spring.smooth });
  const s2 = spring({ frame: frame - 6, fps, config: theme.spring.snappy });
  const box: React.CSSProperties = {
    justifyContent: "flex-start", alignItems: "center", paddingTop: H * hoehe, opacity: raus,
  };
  const umbruch: React.CSSProperties = { overflowWrap: "normal", wordBreak: "keep-all", hyphens: "none" };

  if (variante === "B") {
    const woerter = ss(kraeftig).split(/\s+/);
    return (
      <AbsoluteFill style={box}>
        <div style={{ width: "88%", textAlign: "center", ...umbruch }}>
          <div style={{
            opacity: s1, transform: `translateX(${interpolate(s1, [0, 1], [-40, 0])}px)`,
            fontFamily: philosopher.fontFamily, fontStyle: "italic", fontSize: 58, lineHeight: 1.05,
            color: theme.colors.text, textShadow: SCHATTEN,
          }}>{ss(fein)}</div>
          <div style={{ display: "flex", flexWrap: "wrap", justifyContent: "center", columnGap: 22, marginTop: -4 }}>
            {woerter.map((w, i) => {
              const s = spring({ frame: frame - 8 - i * 5, fps, config: theme.spring.snappy });
              return (
                <span key={i} style={{
                  opacity: s * 0.92,
                  transform: `translateY(${interpolate(s, [0, 1], [26, 0])}px) scale(${interpolate(s, [0, 1], [0.9, 1])})`,
                  fontFamily: sourceSans.fontFamily, fontWeight: 900, fontSize: passend(kraeftig, 138, 0.6), lineHeight: 0.95,
                  letterSpacing: "-0.035em",
                  backgroundImage: `linear-gradient(180deg, ${theme.colors.text} 10%, ${theme.colors.accent} 100%)`,
                  WebkitBackgroundClip: "text", backgroundClip: "text", color: "transparent",
                  filter: "drop-shadow(0 3px 6px rgba(12,28,48,0.9)) drop-shadow(0 6px 26px rgba(12,28,48,0.7))",
                }}>{w}</span>
              );
            })}
          </div>
        </div>
      </AbsoluteFill>
    );
  }

  if (variante === "C") {
    const balken = (text: string, gross: boolean, s: number, i: number) => (
      <div key={i} style={{
        display: "inline-block", opacity: s,
        transform: `scale(${interpolate(s, [0, 1], [0.94, 1])})`,
        background: gross ? "rgba(241,236,221,0.96)" : "rgba(12,28,48,0.82)",
        color: gross ? theme.colors.bg : theme.colors.text,
        fontFamily: gross ? sourceSans.fontFamily : philosopher.fontFamily,
        fontStyle: gross ? "normal" : "italic",
        fontWeight: gross ? 800 : 400, fontSize: gross ? passend(text, 92, 0.58) : passend(text, 52, 0.5), lineHeight: 1.1,
        padding: gross ? "10px 28px 14px" : "8px 24px 10px", borderRadius: 14,
        boxShadow: "0 12px 34px rgba(12,28,48,0.35)", margin: "6px 0",
      }}>{ss(text)}</div>
    );
    return (
      <AbsoluteFill style={box}>
        <div style={{ width: "88%", textAlign: "center", ...umbruch }}>
          {balken(fein, false, s1, 0)}
          <div />
          {balken(kraeftig, true, s2, 1)}
        </div>
      </AbsoluteFill>
    );
  }

  // A · Zwei Schriften (Stand 15.09.2026)
  return (
    <AbsoluteFill style={box}>
      <div style={{ width: "90%", textAlign: "center", ...umbruch }}>
        <div style={{
          opacity: s1 * 0.93, transform: `translateY(${interpolate(s1, [0, 1], [22, 0])}px)`,
          fontFamily: philosopher.fontFamily, fontStyle: "italic", fontSize: 66, lineHeight: 1.02,
          color: theme.colors.text, textShadow: SCHATTEN,
        }}>{ss(fein)}</div>
        <div style={{
          opacity: s2,
          transform: `translateY(${interpolate(s2, [0, 1], [30, 0])}px) scale(${interpolate(s2, [0, 1], [0.92, 1])})`,
          fontFamily: sourceSans.fontFamily, fontWeight: 900, fontSize: passend(kraeftig, 132, 0.6), lineHeight: 0.94,
          letterSpacing: "-0.03em", marginTop: 4, color: theme.colors.text,
          textShadow: "0 3px 16px rgba(12,28,48,0.8), 0 8px 48px rgba(12,28,48,0.55)",
        }}>{ss(kraeftig)}</div>
      </div>
    </AbsoluteFill>
  );
};
