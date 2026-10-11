import { loadFont as loadPhilosopher } from "@remotion/google-fonts/Philosopher";
import { loadFont as loadSourceSans } from "@remotion/google-fonts/SourceSans3";

// Nur die Schnitte, die gebraucht werden — sonst laedt Remotion 112 Dateien je Bild.
export const philosopher = loadPhilosopher("italic", { weights: ["400"], subsets: ["latin"] });
loadPhilosopher("normal", { weights: ["400", "700"], subsets: ["latin"] });
export const sourceSans = loadSourceSans("normal", { weights: ["600", "700", "800", "900"], subsets: ["latin"] });

// Sichere Zonen 9:16 — Instagram legt oben und unten eigene Elemente drueber.
export const H = 1920;
export const W = 1080;
export const ZONE_TOP = H * 0.125;
export const ZONE_BOTTOM = H * 0.82;

/** Schatten, damit heller Text auch auf hellem Grund lesbar bleibt (Regel 4). */
export const SCHATTEN = "0 2px 12px rgba(12,28,48,0.8), 0 6px 40px rgba(12,28,48,0.5)";

/** Schweizer ss — Whisper liefert das deutsche Zeichen. */
export const ss = (t: string) => t.replace(/ß/g, "ss");
