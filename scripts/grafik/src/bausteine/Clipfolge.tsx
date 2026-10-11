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
export const Clipfolge: React.FC<{ clips: Clip[]; stumm?: boolean }> = ({ clips, stumm }) => {
  const { fps } = useVideoConfig();
  return (
    <AbsoluteFill style={{ overflow: "hidden" }}>
      {clips.map((c, i) => (
        <Sequence key={i} from={Math.round(c.abSek * fps)} durationInFrames={Math.max(1, Math.round(c.dauer * fps))}>
          <ClipBild src={staticFile(c.datei)} zoomen={i % 2 === 0} abDatei={c.abDatei} stumm={stumm} />
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};

const ClipBild: React.FC<{ src: string; zoomen: boolean; abDatei?: number; stumm?: boolean }> = ({ src, zoomen, abDatei, stumm }) => {
  const frame = useCurrentFrame();
  const { durationInFrames, fps } = useVideoConfig();
  const scale = zoomen
    ? interpolate(frame, [0, durationInFrames], [1, 1.06], {
        easing: theme.ease.inOut, extrapolateLeft: "clamp", extrapolateRight: "clamp",
      })
    : 1.02;
  return (
    <AbsoluteFill style={{ overflow: "hidden" }}>
      <OffthreadVideo
        src={src}
        muted={stumm}
        trimBefore={abDatei === undefined ? undefined : Math.round(abDatei * fps)}
        style={{ width: "100%", height: "100%", objectFit: "cover", transform: `scale(${scale})` }}
      />
    </AbsoluteFill>
  );
};
