#!/bin/bash
# Pipeline: render 8 talking-head reels sequentially + send each via Telegram
set -e

WORKSPACE="C:/Users/pnulm/Desktop/Mein Business"
PROJECT="$WORKSPACE/scripts/hyperframes-test/mumlife-reel"

# Reihenfolge: kürzeste zuerst (Patricia sieht früh Output)
SLUGS=(
  "2026-06-24-liebe-kinder-mein-ding"
  "2026-06-09-bio-niemand-klickt"
  "2026-06-17-sponsorin-poste-mehr"
  "2026-06-30-mein-mittwoch"
  "2026-06-25-bootcamp-sommer-postest"
  "2026-06-10-story-story-idee-dms"
  "2026-06-19-webinar-bootcamp-pivot"
  "2026-06-22-bootcamp-was-passiert"
)

LABELS=(
  "Kinder (Mi 24.6.)"
  "BIO (Di 9.6.)"
  "Sponsorin (Mi 17.6.)"
  "Mein Mittwoch (Di 30.6.)"
  "5 Tage Sommer (Do 25.6.)"
  "STORY (Mi 10.6.)"
  "Webinar-Pivot (Fr 19.6.)"
  "Bootcamp (Mo 22.6.)"
)

# Load Telegram bot creds
TOKEN=$(grep TELEGRAM_BOT_TOKEN "$WORKSPACE/scripts/garten-telegram-bot/.env" | cut -d= -f2- | tr -d "\"'" | tr -d '[:space:]')
CHAT_ID=$(grep TELEGRAM_CHAT_ID "$WORKSPACE/scripts/garten-telegram-bot/.env" | cut -d= -f2- | tr -d "\"'" | tr -d '[:space:]')

for i in "${!SLUGS[@]}"; do
  slug="${SLUGS[$i]}"
  label="${LABELS[$i]}"
  step=$((i + 1))

  echo ""
  echo "============================================"
  echo "[$step/8] Rendering: $label ($slug)"
  echo "============================================"

  cd "$PROJECT"
  python build-talking-head.py "$slug"

  # Note timestamp before render
  before=$(date +%s)

  # Render
  npx --yes hyperframes@0.6.81 render 2>&1 | tail -3

  # Find newest mp4 in renders/
  newest=$(ls -t renders/mumlife-reel_*.mp4 2>/dev/null | head -1)

  if [ -f "$newest" ]; then
    # Copy to output folder
    cp "$newest" "$WORKSPACE/outputs/reels/$slug/final.mp4"
    # Rename in renders/
    mv "$newest" "renders/${slug}.mp4"

    # Send via Telegram
    cd "$WORKSPACE"
    SIZE_MB=$(du -m "outputs/reels/$slug/final.mp4" | cut -f1)
    curl -s -X POST "https://api.telegram.org/bot${TOKEN}/sendDocument" \
      -F "chat_id=${CHAT_ID}" \
      -F "document=@outputs/reels/$slug/final.mp4;type=video/mp4" \
      -F "caption=🎬 [$step/8] ${label}" \
      | head -c 200
    echo ""
    echo "✓ $label sent to Telegram (${SIZE_MB} MB)"
  else
    echo "✗ Render failed for $slug"
  fi
done

# Final summary message
curl -s -X POST "https://api.telegram.org/bot${TOKEN}/sendMessage" \
  -d "chat_id=${CHAT_ID}" \
  -d "text=✅ Alle 9 Reels fertig! (1 Cart-Open vorher + 8 jetzt) → schau in den Reels-Ordnern unter outputs/reels/" \
  -d "parse_mode=Markdown" > /dev/null

echo ""
echo "=== ALL 8 RENDERS COMPLETE ==="
