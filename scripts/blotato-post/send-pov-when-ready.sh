#!/bin/bash
# Wait for POV render + send to Telegram
WORK_DIR="C:/Users/pnulm/Desktop/Mein Business/scripts/hyperframes-test/mumlife-reel/renders"
TOKEN=$(grep TELEGRAM_BOT_TOKEN "C:/Users/pnulm/Desktop/Mein Business/scripts/garten-telegram-bot/.env" | cut -d= -f2- | tr -d "\"'" | tr -d '[:space:]')
CHAT_ID=$(grep TELEGRAM_CHAT_ID "C:/Users/pnulm/Desktop/Mein Business/scripts/garten-telegram-bot/.env" | cut -d= -f2- | tr -d "\"'" | tr -d '[:space:]')

# Wait for new mp4
while true; do
  newest=$(ls -t "$WORK_DIR"/mumlife-reel_*.mp4 2>/dev/null | head -1)
  if [ -f "$newest" ]; then
    mv "$newest" "$WORK_DIR/pov-dorf-reel.mp4"
    mkdir -p "C:/Users/pnulm/Desktop/Mein Business/outputs/reels/2026-06-28-pov-dorf-schnauzer"
    cp "$WORK_DIR/pov-dorf-reel.mp4" "C:/Users/pnulm/Desktop/Mein Business/outputs/reels/2026-06-28-pov-dorf-schnauzer/final.mp4"
    echo "✓ POV-Reel ist da"
    SIZE_MB=$(du -m "$WORK_DIR/pov-dorf-reel.mp4" | cut -f1)
    curl -s -X POST "https://api.telegram.org/bot${TOKEN}/sendDocument" \
      -F "chat_id=${CHAT_ID}" \
      -F "document=@$WORK_DIR/pov-dorf-reel.mp4;type=video/mp4" \
      -F "caption=🎬 POV-Dorf-Reel (tonlos, 15s) — für Sa 28.6. Cover-PNG separat. Du fügst Trending-Sound im Insta App dazu." \
      > /tmp/telegram-resp.txt
    cat /tmp/telegram-resp.txt | head -c 200
    echo ""
    break
  fi
  sleep 30
done
