#!/bin/bash
# obsidian-reindex.sh
#
# Idempotente Pflege des Obsidian-Vaults:
# 1. Regeneriert alle _INDEX.md in outputs/* (Wiki-Links zu allen MD-Files)
# 2. Stellt sicher, dass alle outputs/**/*.md Frontmatter-Tags haben
#
# Sicher zu jeder Zeit ausführbar. Ändert nichts, was schon korrekt ist.
#
# Verwendung:
#   bash scripts/obsidian-reindex.sh                 # Run + Status
#   bash scripts/obsidian-reindex.sh --dry-run       # Nur prüfen, nichts schreiben
#
# Aufgerufen von:
#   - Patricia manuell wenn sie aufräumen will
#   - .github/workflows/obsidian-reindex.yml täglich 23:00

set -e
cd "$(dirname "$0")/.."  # Repo root

DRY_RUN=0
if [ "$1" = "--dry-run" ]; then
  DRY_RUN=1
  echo "DRY RUN — keine Schreibvorgänge"
fi

CHANGES=0

# ============================================================
# Schritt 1: _INDEX.md pro Output-Ordner generieren
# ============================================================

make_index() {
  local dir="$1"; local title="$2"; local moc="$3"; local tags="$4"
  [ -d "$dir" ] || return
  local out="$dir/_INDEX.md"
  local tmp="${out}.new"
  {
    printf -- "---\ntags: [%s]\n---\n\n" "$tags"
    echo "# $title — Index"
    echo ""
    echo "Auto-Index aller Files in \`$dir/\`. Siehe [[${moc}]] für den thematischen Überblick."
    echo ""
    echo "## Dateien"
    echo ""
    # Top-level .md files (alphabetisch, _INDEX und README separat)
    for f in $(find "$dir" -maxdepth 1 -name "*.md" 2>/dev/null | sort); do
      name=$(basename "$f" .md)
      [ "$name" = "_INDEX" ] && continue
      [ "$name" = "README" ] && continue
      echo "- [[$name]]"
    done
    # README first if exists
    if [ -f "$dir/README.md" ]; then
      echo "- 📘 [[README]]"
    fi
    # Subdirectories
    for sub in $(find "$dir" -mindepth 1 -maxdepth 1 -type d 2>/dev/null | sort); do
      subname=$(basename "$sub")
      case "$subname" in
        renders|slides-png|fotos|_uploads|png|node_modules) continue ;;
      esac
      has_md=$(find "$sub" -maxdepth 2 -name "*.md" 2>/dev/null | head -1)
      [ -z "$has_md" ] && continue
      echo ""
      echo "### 📁 $subname"
      echo ""
      for f in $(find "$sub" -maxdepth 2 -name "*.md" 2>/dev/null | sort); do
        name=$(basename "$f" .md)
        echo "- [[$name]]"
      done
    done
  } > "$tmp"

  if [ -f "$out" ] && diff -q "$tmp" "$out" >/dev/null 2>&1; then
    rm "$tmp"
  else
    if [ "$DRY_RUN" = "1" ]; then
      echo "[would update] $out"
      rm "$tmp"
    else
      mv "$tmp" "$out"
      echo "✓ updated $out"
    fi
    CHANGES=$((CHANGES+1))
  fi
}

echo "=== Schritt 1: _INDEX.md regenerieren ==="
make_index "outputs/karussells" "🎨 Karussells" "_MOCs/MOC-Content-Engine" "moc, content, karussell"
make_index "outputs/reels" "🎬 Reels" "_MOCs/MOC-Content-Engine" "moc, content, reels"
make_index "outputs/stories" "📱 Stories" "_MOCs/MOC-Content-Engine" "moc, content, story"
make_index "outputs/freitag" "📅 Freitag-Hooks" "_MOCs/MOC-Content-Engine" "moc, content, freitag-hooks"
make_index "outputs/montag" "🚀 Montag-Builds" "_MOCs/MOC-Content-Engine" "moc, content, montag-build"
make_index "outputs/mealplans" "🥗 Mealplans" "_MOCs/MOC-Mealplan" "moc, mealplan"
make_index "outputs/funnels" "🎯 Funnels" "_MOCs/MOC-Produkte-Funnels" "moc, funnel"
make_index "outputs/produkte" "🪜 Produkte" "_MOCs/MOC-Produkte-Funnels" "moc, produkt"
make_index "outputs/salespages" "💰 Sales-Pages" "_MOCs/MOC-Produkte-Funnels" "moc, produkt, salespage"
make_index "outputs/marktrecherche" "🔍 Marktrecherche" "_MOCs/MOC-Markt-Research" "moc, research"
make_index "outputs/zielgruppen-research" "🎯 Zielgruppen-Research" "_MOCs/MOC-Markt-Research" "moc, research"
make_index "outputs/doterra-strategie" "🌿 doTERRA-Strategie" "_MOCs/MOC-doTERRA" "moc, doterra"
make_index "outputs/ads" "📢 Ads" "_MOCs/MOC-Produkte-Funnels" "moc, ads"
make_index "outputs/monatsplaene" "📅 Monatspläne" "_MOCs/MOC-Produkte-Funnels" "moc, monatsplan"
make_index "outputs/content-kalender" "📆 Content-Kalender" "_MOCs/MOC-Content-Engine" "moc, content"
make_index "outputs/calls" "📞 Calls" "_MOCs/MOC-Produkte-Funnels" "moc, call"
make_index "outputs/garten" "🌱 Garten" "_MOCs/MOC-Garten" "moc, garten"
make_index "outputs/sonstige" "📦 Sonstige" "_MOCs/MOC-Brand-Voice" "moc, misc"
make_index "outputs/julia-trost-sync" "📚 Julia-Trost Sync" "_MOCs/MOC-Externe-Wissensbasen" "moc, externe-wissen, julia-trost"
make_index "outputs/telegram-posts" "📣 Telegram-Posts" "_MOCs/MOC-Content-Engine" "moc, content, telegram"
make_index "outputs/praesentationen" "📊 Präsentationen" "_MOCs/MOC-Produkte-Funnels" "moc, produkt"
make_index "outputs/samples" "🧪 Samples" "_MOCs/MOC-Content-Engine" "moc, content, samples"
make_index "outputs/bio-check-bot" "🤖 Bio-Check Bot" "_MOCs/MOC-Tools-Skripte" "moc, tools, bot"

# Optional bio-update Ordner (datums-gestempelt)
for d in outputs/bio-update-*; do
  [ -d "$d" ] || continue
  make_index "$d" "👤 $(basename "$d")" "_MOCs/MOC-Brand-Voice" "moc, brand"
done

# ============================================================
# Schritt 2: Frontmatter-Tags auf alle outputs/**/*.md sicherstellen
# ============================================================

echo ""
echo "=== Schritt 2: Frontmatter-Tags prüfen ==="

ensure_fm() {
  local file="$1"; local tags="$2"
  [ -f "$file" ] || return
  [ "$(basename "$file")" = "_INDEX.md" ] && return
  if [ "$(head -1 "$file" 2>/dev/null)" = "---" ]; then
    return  # Schon Frontmatter da
  fi
  if [ "$DRY_RUN" = "1" ]; then
    echo "[would tag] $file → [$tags]"
  else
    { printf -- "---\ntags: [%s]\n---\n\n" "$tags"; cat "$file"; } > "${file}.tmp" && mv "${file}.tmp" "$file"
    echo "✓ tagged $file → [$tags]"
  fi
  CHANGES=$((CHANGES+1))
}

tag_dir() {
  local pattern="$1"; local tags="$2"; local recursive="${3:-0}"
  if [ "$recursive" = "1" ]; then
    find $pattern -name "*.md" 2>/dev/null | while read f; do ensure_fm "$f" "$tags"; done
  else
    for f in $pattern/*.md; do ensure_fm "$f" "$tags"; done
  fi
}

tag_dir "outputs/karussells" "content, karussell"
tag_dir "outputs/reels" "content, reels"
tag_dir "outputs/freitag" "content, freitag-hooks"
tag_dir "outputs/montag" "content, montag-build"
tag_dir "outputs/mealplans" "mealplan"
tag_dir "outputs/marktrecherche" "research"
tag_dir "outputs/zielgruppen-research" "research"
tag_dir "outputs/doterra-strategie" "doterra"
tag_dir "outputs/ads" "ads"
tag_dir "outputs/monatsplaene" "monatsplan"
tag_dir "outputs/content-kalender" "content"
tag_dir "outputs/garten" "garten"
tag_dir "outputs/sonstige" "misc"
tag_dir "outputs/telegram-posts" "content, telegram"
tag_dir "outputs/samples" "content, samples"
tag_dir "outputs/calls" "call"

for d in outputs/bio-update-*; do
  [ -d "$d" ] || continue
  tag_dir "$d" "brand"
done

# Recursive folders
find outputs/produkte -maxdepth 5 -name "*.md" 2>/dev/null | while read f; do ensure_fm "$f" "produkt"; done
find outputs/stories -maxdepth 5 -name "*.md" 2>/dev/null | while read f; do ensure_fm "$f" "content, story"; done
find outputs/funnels -maxdepth 5 -name "*.md" 2>/dev/null | while read f; do ensure_fm "$f" "funnel"; done
find outputs/salespages -maxdepth 5 -name "*.md" 2>/dev/null | while read f; do ensure_fm "$f" "produkt, salespage"; done
find outputs/julia-trost-sync -maxdepth 5 -name "*.md" 2>/dev/null | while read f; do ensure_fm "$f" "externe-wissen, julia-trost"; done
find outputs/bio-check-bot -maxdepth 5 -name "*.md" 2>/dev/null | while read f; do ensure_fm "$f" "tools, bot"; done
find outputs/praesentationen -maxdepth 5 -name "*.md" 2>/dev/null | while read f; do ensure_fm "$f" "produkt"; done

# ============================================================
# Zusammenfassung
# ============================================================

echo ""
echo "================================"
if [ "$DRY_RUN" = "1" ]; then
  echo "DRY RUN: $CHANGES Datei(en) würden geändert"
else
  if [ "$CHANGES" = "0" ]; then
    echo "✓ Alles bereits sauber — keine Änderungen"
  else
    echo "✓ $CHANGES Datei(en) geändert"
  fi
fi
echo "================================"
