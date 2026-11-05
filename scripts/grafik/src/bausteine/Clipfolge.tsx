import React from "react";
import {
  AbsoluteFill, OffthreadVideo, Sequence, interpolate, staticFile,
  useCurrentFrame, useVideoConfig,
} from "remotion";
import { theme } from "../theme";

export type Clip = { datei: string; dauer: number; abSek: number; abDatei?: number; winkel?: string };

/**
 * Baustein „Clipfolge" — das Material mit Auto-Zoom.
 * Jeder zweite Abschnitt faehrt langsam hinein, dazwischen steht die Kamera.
 * Harter Schnitt, keine Blende: bei Sprechvideos frisst jede Blende Verstaendlichkeit.
 * `abDatei`: alle Abschnitte zeigen auf DIESELBE Datei (CapCut-Export).
 */
/**
 * Je Reel einstellbar (grafik.json → stil.zoom).
 * Vorgabe seit 28.10.2026 (Patricia: „kannst du den zoom über längere zeit und näher ran machen?“,
 * am fertigen Reel freigegeben): jeder Clip, bis 115 %, Ziel oberes Drittel = Gesicht.
 * Vorher nur jeder zweite Clip bis 106 %, die anderen standen auf 102 %.
 */
export type Zoom = {
  bis?: number; alle?: boolean; zentrumY?: number;
  /**
   * „fahrt" (Vorgabe) = langsame Fahrt je Clip. „sprung" = die Groesse springt an Satzteil-Grenzen
   * und steht dazwischen still, einmal je Reel ganz weit raus (angesehen bei islazul.ch, 04.11.2026).
   * Die Stellen rechnet vorschau.py einmal aus (`spruenge`), damit Render und Gesichtspruefung
   * dieselben Werte sehen. Nie von Hand in grafik.json pflegen.
   */
  modus?: "fahrt" | "sprung";
  stufen?: number[];
  /** Wortfolge, auf der das Bild weit wird. Fehlt = automatisch, false = nie. */
  weit?: string | false;
  spruenge?: { abSek: number; scale: number }[];
};

export const Clipfolge: React.FC<{ clips: Clip[]; stumm?: boolean; zoom?: Zoom }> = ({ clips, stumm, zoom = {} }) => {
  const { fps } = useVideoConfig();
  return (
    <AbsoluteFill style={{ overflow: "hidden" }}>
      {clips.map((c, i) => (
        <Sequence key={i} from={Math.round(c.abSek * fps)} durationInFrames={Math.max(1, Math.round(c.dauer * fps))}>
          <ClipBild src={staticFile(c.datei)} zoomen={(zoom.alle ?? true) || i % 2 === 0} abDatei={c.abDatei} stumm={stumm}
            bis={zoom.bis ?? 1.15} zentrumY={zoom.zentrumY ?? 30} clipAb={c.abSek}
            spruenge={zoom.modus === "sprung" ? zoom.spruenge : undefined} />
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};

const ClipBild: React.FC<{ src: string; zoomen: boolean; abDatei?: number; stumm?: boolean; bis: number; zentrumY: number; clipAb: number; spruenge?: { abSek: number; scale: number }[] }> = ({ src, zoomen, abDatei, stumm, bis, zentrumY, clipAb, spruenge }) => {
  const frame = useCurrentFrame();
  const { durationInFrames, fps } = useVideoConfig();
  const jetzt = clipAb + frame / fps;
  const scale = spruenge?.length
    ? spruenge.reduce((s, x) => (x.abSek <= jetzt ? x.scale : s), spruenge[0].scale)
    : zoomen
    ? interpolate(frame, [0, durationInFrames], [1, bis], {
        easing: theme.ease.inOut, extrapolateLeft: "clamp", extrapolateRight: "clamp",
      })
    : 1.02;
  return (
    <AbsoluteFill style={{ overflow: "hidden" }}>
      <OffthreadVideo
        src={src}
        muted={stumm}
        trimBefore={abDatei === undefined ? undefined : Math.round(abDatei * fps)}
        style={{ width: "100%", height: "100%", objectFit: "cover", transform: `scale(${scale})`, transformOrigin: `50% ${zentrumY}%` }}
      />
    </AbsoluteFill>
  );
};
