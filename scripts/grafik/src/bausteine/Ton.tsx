import React from "react";
import { Audio } from "@remotion/media";
import { Sequence, interpolate, staticFile } from "remotion";

/**
 * Patricias Tonregeln (06.10.2026):
 *   pop     — etwas NEUES erscheint: Wort, Einblendung, Karte
 *   intro   — Anfang des Videos, nur wenn es Sinn ergibt (hook.intro: true)
 *   typing  — Ueberschriften: waehrend sich der Hook aufbaut
 *   whoosh  — Uebergaenge: zwischen Clips, Woertern, Animationen
 * Dateien kommen aus video/sounds/ (vorschau.py legt sie als sfx/<rolle>.wav ab).
 * klick und ding sind mit ffmpeg erzeugter Ersatz.
 */
export type Sound = "pop" | "whoosh" | "typing" | "intro" | "klick" | "ding" | "keiner";

export type TonEreignis = { rolle: Sound; frame: number; laut: number; dauer?: number };

/**
 * Lautstaerke je Rolle — gemessen an Patricias Dateien und ihrer Stimme (06.10.2026):
 * Effekte sitzen UNTER der Stimme. Beim ersten Render lag das Intro bei 0.28 rund 9 dB
 * ueber ihr. Sagt sie „zu laut / zu leise", wird HIER geaendert, nicht im Reel.
 */
// Gemessen: Stimme Spitze −13 dB. Ziel: Effekte 2–6 dB darunter.
// pop 0.18 → ≈ −15 dB · typing 0.6 → ≈ −19 dB · whoosh 1.0 → ≈ −22 dB · intro 0.1 → ≈ −20 dB
export const LAUT: Record<string, number> = { pop: 0.18, whoosh: 1.0, typing: 0.6, intro: 0.1, klick: 0.5, ding: 0.4 };

export const Tonspur: React.FC<{ ereignisse: TonEreignis[] }> = ({ ereignisse }) => (
  <>
    {ereignisse.map((e, i) => (
      <Sequence key={i} from={e.frame} durationInFrames={e.dauer ?? 90} layout="none">
        <Audio
          src={staticFile(`sfx/${e.rolle}.wav`)}
          volume={(f) => e.dauer ? e.laut * interpolate(f, [e.dauer - 8, e.dauer], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }) : e.laut}
        />
      </Sequence>
    ))}
  </>
);
