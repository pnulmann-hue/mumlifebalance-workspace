import React from "react";
import { AbsoluteFill, Sequence, useVideoConfig } from "remotion";
import { theme } from "./theme";
import { Clip, Clipfolge } from "./bausteine/Clipfolge";
import { Hook, HookVariante } from "./bausteine/Hook";
import { Untertitel, UntertitelVariante, Wort } from "./bausteine/Untertitel";
import { Karte, Knallwort, Look } from "./bausteine/Einblendungen";
import { LAUT, Sound, TonEreignis, Tonspur } from "./bausteine/Ton";

export type Einblendung = {
  abSek: number; dauer: number; art: "knallwort" | "karte";
  text?: string; unter?: string; zitat?: string; seite?: "links" | "rechts";
  schilder?: { emoji?: string; wort: string }[]; sound?: Sound;
};

export type ReelProps = {
  dauer: number;
  clips: Clip[];
  woerter: Wort[];
  hook: { fein: string; kraeftig: string; sound?: Sound; intro?: boolean };
  hookDauer?: number;
  betont: string[];
  einblendungen: Einblendung[];
  /** Varianten je Reel. Vorgabe B/B = Patricias Entscheid 06.10.2026 („klar Stil B“). */
  stil?: { hook?: HookVariante; untertitel?: UntertitelVariante; look?: boolean; hoehe?: number };
  /** welche Toene es gibt (setzt vorschau.py aus video/sounds/) */
  toene?: string[];
  /** nur fuer rand-pruefen.py: Video ausblenden, damit nur Text sichtbar ist */
  nurText?: boolean;
  /** nur fuer die Ton-Pruefung: Stimme aus, nur die Effekte hoerbar */
  nurEffekte?: boolean;
};

export const Reel: React.FC<ReelProps> = ({
  clips, woerter, hook, hookDauer = 4.2, betont, einblendungen, stil = {}, toene = [], nurText, nurEffekte,
}) => {
  const { fps } = useVideoConfig();
  // Oberkante des Textes in Bildhoehe; 0.56 = unter dem Kinn. Je Reel anpassbar (stil.hoehe).
  const hoehe = stil.hoehe ?? 0.56;
  return (
    <AbsoluteFill style={{ backgroundColor: nurText ? "black" : theme.colors.bg }}>
      {nurText ? null : <Clipfolge clips={clips} stumm={nurEffekte} />}

      {nurText ? null : <Tonspur ereignisse={toeneBauen({ hook, hookDauer, einblendungen, clips, stil, toene, fps })} />}

      <Sequence durationInFrames={Math.round(hookDauer * fps)}>
        <Hook fein={hook.fein} kraeftig={hook.kraeftig} variante={stil.hook ?? "B"} hoehe={hoehe} />
      </Sequence>

      <Untertitel woerter={woerter} betont={betont} variante={stil.untertitel ?? "B"}
        frei={einblendungen} abSek={hookDauer} hoehe={hoehe} />

      {einblendungen.map((e, i) => (
        <Sequence key={i} from={Math.round(e.abSek * fps)} durationInFrames={Math.round(e.dauer * fps)}>
          {e.art === "knallwort"
            ? <Knallwort text={e.text || ""} unter={e.unter} schilder={e.schilder} sound={e.sound} />
            : <Karte zitat={e.zitat || ""} seite={e.seite} sound={e.sound} />}
        </Sequence>
      ))}

      {nurText || stil.look === false ? null : <Look />}
    </AbsoluteFill>
  );
};

/**
 * Wann welcher Ton kommt — Patricias Regeln vom 06.10.2026, an EINER Stelle:
 *  · intro   Frame 0, zum Erscheinen des Hooks (Patricia 06.10.2026: „kannst du da die
 *            startanimation einblenden? tiping passt ja nur, wenn was neu geschrieben wird")
 *  · typing  NUR wenn Text sichtbar Buchstabe fuer Buchstabe geschrieben wird (hook.sound = "typing")
 *  · pop     jede Einblendung (Knallwort, Karte) — etwas Neues erscheint
 *  · whoosh  an einem Clip-Wechsel, aber hoechstens alle 8 s und nie naeher als 2 s an einem
 *            anderen Ton (Patricia: „etwas zu viele whooshs" — vorher 7 in 36 s, jetzt 3)
 * Untertitel bekommen keinen Ton: ein Pop alle 0.3 s waere Dauerrauschen.
 */
export const toeneBauen = ({ hook, hookDauer, einblendungen, clips, stil, toene, fps }: {
  hook: ReelProps["hook"]; hookDauer: number; einblendungen: Einblendung[]; clips: Clip[];
  stil: NonNullable<ReelProps["stil"]>; toene: string[]; fps: number;
}): TonEreignis[] => {
  const da = (r: string) => toene.includes(r);
  const ev: TonEreignis[] = [];
  const add = (rolle: Sound, sek: number, dauer?: number) => {
    if (rolle !== "keiner" && da(rolle)) ev.push({ rolle, frame: Math.max(0, Math.round(sek * fps)), laut: LAUT[rolle] ?? 0.5, dauer });
  };
  if (hook.sound && hook.sound !== "intro") add(hook.sound, 0.2);
  else if (hook.intro !== false) add("intro", 0, Math.round(Math.min(2.5, hookDauer) * fps));
  for (const e of einblendungen) add(e.sound ?? "pop", e.abSek);
  const WHOOSH_ABSTAND = 8;   // s zwischen zwei Whooshs
  const TON_ABSTAND = 2;      // s zu jedem anderen Ton
  let letzter = -Infinity;
  for (const c of clips.slice(1)) {
    const sek = Math.max(0, c.abSek - 0.15);
    const nah = ev.some((x) => Math.abs(x.frame / fps - sek) < TON_ABSTAND);
    if (!nah && sek - letzter >= WHOOSH_ABSTAND && da("whoosh")) { add("whoosh", sek); letzter = sek; }
  }
  return ev.sort((a, b) => a.frame - b.frame);
};
