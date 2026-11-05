import React from "react";
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { theme } from "../theme";
import { H, philosopher, sourceSans, ss } from "./schrift";

export type TafelDaten = {
  abSek: number; bisSek: number; titel: string;
  zeilen: { text: string; abSek: number }[];
};

const KOPF = 58;
const ZEILE = 80;
const RAND = 68;

/** Hoehe wird gerechnet, weil der Untertitel direkt darunter sitzt. */
export const tafelHoehePx = (t: Pick<TafelDaten, "zeilen">) => RAND + KOPF + t.zeilen.length * ZEILE;

/**
 * Baustein „Tafel" — waechst beim Reden: erst der Titel, dann jede Zeile auf ihrem gesprochenen Wort.
 * Angesehen bei islazul.ch (04.11.2026): die Tafel haelt die Leute, weil man sehen will, was noch dazukommt.
 * Hoechstens drei Zeilen, je bis 28 Zeichen (prueft vorschau.py, ein Ueberlauf in der Tafel faellt
 * der Randpruefung nicht auf). Unter dem Kinn, die Haende bleiben durch die Flaeche sichtbar.
 * `nurText`: heller Grund, damit Rand- und Gesichtspruefung die Flaeche mitmessen.
 */
export const Tafel: React.FC<{ tafel: TafelDaten; hoehe?: number; nurText?: boolean }> = ({ tafel, hoehe = 0.56, nurText }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const s = spring({ frame, fps, config: theme.spring.smooth });
  const raus = interpolate(frame, [durationInFrames - 8, durationInFrames], [1, 0], {
    easing: theme.ease.in, extrapolateLeft: "clamp", extrapolateRight: "clamp",
  });
  return (
    <AbsoluteFill style={{ alignItems: "center", opacity: s * raus }}>
      <div style={{
        position: "absolute", top: H * hoehe, width: "84%", height: tafelHoehePx(tafel), boxSizing: "border-box",
        padding: "26px 44px 0", borderRadius: 12,
        background: nurText ? "#888" : "rgba(12,28,48,0.74)", border: "1px solid rgba(241,236,221,0.22)",
        transform: `translateY(${interpolate(s, [0, 1], [18, 0])}px)`,
      }}>
        <div style={{
          fontFamily: sourceSans.fontFamily, fontWeight: 700, fontSize: 42, lineHeight: `${KOPF}px`,
          letterSpacing: "0.14em", color: theme.colors.textDim, whiteSpace: "nowrap",
        }}>{ss(tafel.titel).toUpperCase()}</div>
        {tafel.zeilen.map((z, i) => {
          const ab = Math.round((z.abSek - tafel.abSek) * fps);
          // Wisch von links: die Zeile entsteht sichtbar, statt einfach dazustehen.
          const w = interpolate(frame, [ab, ab + 12], [0, 100], {
            easing: theme.ease.out, extrapolateLeft: "clamp", extrapolateRight: "clamp",
          });
          return (
            <div key={i} style={{
              display: "flex", alignItems: "center", gap: 22, height: ZEILE, whiteSpace: "nowrap",
              clipPath: `inset(0 ${100 - w}% 0 0)`,
            }}>
              <span style={{ width: 16, height: 16, borderRadius: 8, flex: "none", background: theme.colors.accent }} />
              <span style={{ fontFamily: philosopher.fontFamily, fontStyle: "italic", fontSize: 62, color: theme.colors.text }}>{ss(z.text)}</span>
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
