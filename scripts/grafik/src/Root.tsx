import React from "react";
import { CalculateMetadataFunction, Composition } from "remotion";
import { Reel, ReelProps } from "./Reel";

const FPS = 30;

/** Die Laenge kommt aus der Projektdatei (grafik.json → `dauer`), nicht aus dem Code. */
const metadaten: CalculateMetadataFunction<ReelProps> = async ({ props }) => ({
  durationInFrames: Math.max(1, Math.ceil(props.dauer * FPS)),
});

const beispiel: ReelProps = {
  dauer: 6,
  clips: [],
  woerter: [
    { text: "So", startMs: 4300, endMs: 4500 },
    { text: "sieht", startMs: 4500, endMs: 4750 },
    { text: "ein", startMs: 4750, endMs: 4900 },
    { text: "Untertitel", startMs: 4900, endMs: 5500 },
    { text: "aus.", startMs: 5500, endMs: 5900 },
  ],
  hook: { fein: "Zwei Jahre lang war mein Gedanke:", kraeftig: "einfach mehr arbeiten." },
  betont: ["Untertitel"],
  einblendungen: [],
  stil: { hook: "A", untertitel: "A" },
};

export const RemotionRoot: React.FC = () => (
  <Composition
    id="Reel"
    component={Reel}
    durationInFrames={beispiel.dauer * FPS}
    fps={FPS}
    width={1080}
    height={1920}
    defaultProps={beispiel}
    calculateMetadata={metadaten}
  />
);
