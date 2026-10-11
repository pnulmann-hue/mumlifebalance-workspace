import React from "react";
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { theme } from "../theme";
import { H, philosopher, sourceSans, ss } from "./schrift";
import { Sound } from "./Ton";

/**
 * Baustein „Knallwort" — ein grosses Wort mitten im Satz, darunter wahlweise eine
 * kleine Zeile oder bis zu drei Schilder (nacheinander, 5 Frames Versatz).
 * Eine Einblendung muss SAGEN, nicht schmuecken: nur das Wort, das gerade gesprochen wird.
 */
export const Knallwort: React.FC<{
  text: string; unter?: string; schilder?: { emoji?: string; wort: string }[]; sound?: Sound;
}> = ({ text, unter, schilder }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const s = spring({ frame, fps, config: theme.spring.snappy });
  const raus = interpolate(frame, [durationInFrames - 8, durationInFrames], [1, 0], {
    easing: theme.ease.in, extrapolateLeft: "clamp", extrapolateRight: "clamp",
  });
  const atem = 1 + Math.sin(frame / 22) * 0.006;
  return (
    <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", opacity: raus }}>
      <div style={{ textAlign: "center", transform: `scale(${atem})`, width: "88%" }}>
        <div style={{
          opacity: s, transform: `scale(${interpolate(s, [0, 1], [0.86, 1])})`,
          fontFamily: sourceSans.fontFamily, fontWeight: 900, fontSize: 150, letterSpacing: "-0.04em",
          lineHeight: 0.9, color: theme.colors.accent, textShadow: "0 4px 30px rgba(12,28,48,0.85)",
          overflowWrap: "normal", wordBreak: "keep-all",
        }}>{ss(text)}</div>
        {schilder?.length ? (
          <div style={{ display: "flex", flexWrap: "wrap", gap: 14, justifyContent: "center", marginTop: 26 }}>
            {schilder.map((sch, i) => {
              const ss2 = spring({ frame: frame - 8 - i * 5, fps, config: theme.spring.snappy });
              return (
                <div key={i} style={{
                  opacity: ss2,
                  transform: `translateY(${interpolate(ss2, [0, 1], [18, 0])}px) scale(${interpolate(ss2, [0, 1], [0.9, 1])})`,
                  display: "flex", alignItems: "center", gap: 10, background: "rgba(241,236,221,0.94)",
                  borderRadius: 999, padding: "12px 24px", boxShadow: "0 10px 30px rgba(12,28,48,0.4)",
                }}>
                  {sch.emoji ? <span style={{ fontSize: 40, lineHeight: 1 }}>{sch.emoji}</span> : null}
                  <span style={{ fontFamily: sourceSans.fontFamily, fontWeight: 700, fontSize: 38, color: theme.colors.bg }}>{ss(sch.wort)}</span>
                </div>
              );
            })}
          </div>
        ) : unter ? (
          <div style={{
            opacity: spring({ frame: frame - 7, fps, config: theme.spring.smooth }) * 0.95,
            fontFamily: philosopher.fontFamily, fontStyle: "italic", fontSize: 44, marginTop: 10,
            color: theme.colors.text, textShadow: "0 2px 14px rgba(12,28,48,0.8)",
          }}>{ss(unter)}</div>
        ) : null}
      </div>
    </AbsoluteFill>
  );
};

/**
 * Baustein „Karte" — Kundenstimme faehrt von der Seite herein.
 * 🚨 Nur freigegebene Zitate, als Text gesetzt (context/kundinnen-geschichten.md).
 * Nie ins obere Drittel — dort sitzt ihr Kopf.
 */
export const Karte: React.FC<{ zitat: string; seite?: "links" | "rechts"; sound?: Sound }> = ({
  zitat, seite = "links",
}) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const s = spring({ frame, fps, config: theme.spring.smooth });
  const links = seite === "links";
  const raus = interpolate(frame, [durationInFrames - 8, durationInFrames], [1, 0], {
    easing: theme.ease.in, extrapolateLeft: "clamp", extrapolateRight: "clamp",
  });
  return (
    <AbsoluteFill style={{
      justifyContent: "flex-start", alignItems: links ? "flex-start" : "flex-end",
      paddingTop: links ? H * 0.5 : H * 0.615, paddingLeft: 48, paddingRight: 48, opacity: s * raus,
    }}>
      <div style={{
        width: "66%",
        transform: `translateX(${interpolate(s, [0, 1], [links ? -160 : 160, 0])}px) rotate(${interpolate(s, [0, 1], [links ? -6 : 6, links ? -2.5 : 2.5])}deg)`,
        background: "rgba(241,236,221,0.95)", borderRadius: 14, padding: "22px 26px",
        boxShadow: "0 18px 50px rgba(12,28,48,0.45)", borderLeft: `6px solid ${theme.colors.primary}`,
      }}>
        <div style={{ fontFamily: philosopher.fontFamily, fontStyle: "italic", fontSize: 34, lineHeight: 1.32, color: theme.colors.bg }}>
          „{ss(zitat)}“
        </div>
      </div>
    </AbsoluteFill>
  );
};

/** Baustein „Look" — Farbkorrektur, Korn, Vignette. Dezent: das Material soll echt bleiben. */
export const Look: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <>
      <AbsoluteFill style={{
        background: `linear-gradient(180deg, ${theme.colors.bg}22 0%, transparent 35%, transparent 60%, ${theme.colors.bg}66 100%)`,
        mixBlendMode: "multiply", pointerEvents: "none",
      }} />
      <AbsoluteFill style={{ opacity: 0.05, pointerEvents: "none" }}>
        <svg width="100%" height="100%">
          <filter id="g"><feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves={3} seed={frame % 11} /></filter>
          <rect width="100%" height="100%" filter="url(#g)" />
        </svg>
      </AbsoluteFill>
      <AbsoluteFill style={{ background: `radial-gradient(ellipse at 50% 42%, transparent 48%, ${theme.colors.bg}55 100%)`, pointerEvents: "none" }} />
    </>
  );
};
