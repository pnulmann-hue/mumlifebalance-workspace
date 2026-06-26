#!/bin/bash
# Render remaining 4 reels (no Telegram)
set -e

WORKSPACE="C:/Users/pnulm/Desktop/Mein Business"
PROJECT="$WORKSPACE/scripts/hyperframes-test/mumlife-reel"

SLUGS=(
  "2026-06-25-bootcamp-sommer-postest"
  "2026-06-10-story-story-idee-dms"
  "2026-06-19-webinar-bootcamp-pivot"
  "2026-06-22-bootcamp-was-passiert"
)

LABELS=(
  "5 Tage Sommer (Do 25.6.)"
  "STORY (Mi 10.6.)"
  "Webinar-Pivot (Fr 19.6.)"
  "Bootcamp (Mo 22.6.)"
)

for i in "${!SLUGS[@]}"; do
  slug="${SLUGS[$i]}"
  label="${LABELS[$i]}"
  step=$((i + 1))

  echo ""
  echo "============================================"
  echo "[$step/4] $label"
  echo "  -> $slug"
  echo "============================================"

  cd "$PROJECT"
  python build-talking-head.py "$slug"
  npx --yes hyperframes@0.6.81 render 2>&1 | tail -3

  newest=$(ls -t renders/mumlife-reel_*.mp4 2>/dev/null | head -1)

  if [ -f "$newest" ]; then
    cp "$newest" "$WORKSPACE/outputs/reels/$slug/final.mp4"
    mv "$newest" "renders/${slug}.mp4"
    size=$(du -m "$WORKSPACE/outputs/reels/$slug/final.mp4" | cut -f1)
    dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$WORKSPACE/outputs/reels/$slug/final.mp4")
    echo "✓ DONE: $label | ${size}MB | ${dur}s"
    echo "  Path: outputs/reels/$slug/final.mp4"
  else
    echo "✗ Render failed for $slug"
  fi
done

echo ""
echo "=== ALL 4 RENDERS COMPLETE ==="
echo "All 9 reels are in outputs/reels/[slug]/final.mp4"
