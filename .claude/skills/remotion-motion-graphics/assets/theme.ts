// theme.ts — single source of truth for every Remotion project.
// NEVER inline colors, easings, or spring configs in components.
import { Easing } from "remotion";

export const theme = {
  colors: {
    // Patricia Ulmann / Mum Life Balance — verbindlich.
    // Quelle: context/brand-voice.md. KEIN Gelb, kein Gold, kein Pink.
    bg: "#0c1c30",        // Dunkelblau, Grund
    bgAlt: "#29556d",     // Teal, zweiter Grund
    primary: "#12828c",   // Petrol — DIE Hauptfarbe, hoechstens ein Element je Bild
    accent: "#dc822e",    // Orange — nur Akzent, nie flaechig
    text: "#f1ecdd",      // Creme
    textDim: "rgba(241, 236, 221, 0.65)",
    glow: "rgba(18, 130, 140, 0.4)",
  },
  fonts: {
    display: "Philosopher",   // Ueberschriften
    body: "Source Sans 3",    // Fliesstext
    mono: "Source Sans 3",
  },
  // THE easing curves. Linear is forbidden.
  ease: {
    out: Easing.bezier(0.16, 1, 0.3, 1), // easeOutExpo — entrances
    inOut: Easing.bezier(0.83, 0, 0.17, 1), // easeInOutQuint — moves, Ken Burns
    in: Easing.bezier(0.7, 0, 0.84, 0), // exits only
  },
  spring: {
    snappy: { damping: 14, stiffness: 160, mass: 0.6 }, // UI pops, words
    smooth: { damping: 20, stiffness: 90, mass: 1 }, // big elements
    bouncy: { damping: 11, stiffness: 170, mass: 0.7 }, // playful accents, logos
  },
} as const;

// ---------------------------------------------------------------------------
// HARTE MARKEN-REGELN (Patricia Ulmann)
// ---------------------------------------------------------------------------
// - Nur diese vier Farben. Kein Gelb, kein Gold, kein Pink.
// - Orange ist Akzent, nie Flaeche.
// - Petrol-Vollflaechen NICHT als Cover bei Lead-Posts mit Keyword-CTA.
// - Reel und Reel-Cover sind 1080x1920. Hook gehoert in die MITTE:
//   oben 0-12.5 % und unten 82-100 % sind tote Zone (Caption + Bedienknoepfe).
// - Text gehoert ins obere Drittel, nie ganz nach unten.
// - Textblock wechselt spaetestens alle 3 Sekunden.
// - Nie mehr als zwei Textelemente gleichzeitig im Bild.
// - Nie heller Text ohne Balken oder Schatten auf hellem Grund.
// - Keine KI-generierten Szenen als Ersatz fuer echtes Material.
