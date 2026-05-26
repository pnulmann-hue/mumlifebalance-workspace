#!/usr/bin/env bash
# Auto-Sync — committet Aenderungen aus outputs/, context/, plans/, reference/
# automatisch ins Repo, damit Patricia ueberall (Desktop + Mobile App) auf den
# aktuellen Stand zugreifen kann.
#
# Wird vom Stop-Hook in .claude/settings.json nach jeder Claude-Antwort
# getriggert. Ist absichtlich tolerant: schlaegt nie hart fehl, blockiert
# Claude nie laenger als noetig.

set +e

# In Repo-Root wechseln (relativ zum Skript-Pfad)
cd "$(dirname "$0")/../.." || exit 0

# Schnell-Check: gibt's ueberhaupt was zu syncen?
NEED_SYNC=0
for path in outputs context plans reference; do
  if [ -d "$path" ]; then
    # Modified-Files in dem Pfad?
    if ! git diff --quiet -- "$path" 2>/dev/null; then
      NEED_SYNC=1
      break
    fi
    # Untracked-Files in dem Pfad?
    if [ -n "$(git ls-files --others --exclude-standard -- "$path" 2>/dev/null | head -1)" ]; then
      NEED_SYNC=1
      break
    fi
  fi
done

if [ "$NEED_SYNC" -eq 0 ]; then
  exit 0
fi

# Stagen + committen
git add outputs/ context/ plans/ reference/ 2>/dev/null

# Falls trotz dirty-check nichts staged (z.B. nur gitignored) -> raus
if git diff --staged --quiet; then
  exit 0
fi

STAMP=$(date '+%Y-%m-%d %H:%M')

# Datei-Count fuer Commit-Message
COUNT=$(git diff --staged --name-only | wc -l | tr -d ' ')
COUNT_STR="${COUNT} files"

git commit -m "auto-sync: ${STAMP} (${COUNT_STR})" --quiet >/dev/null 2>&1

# Push mit Rebase-Fallback (falls parallel GitHub-Actions gepushed haben)
if ! git push origin main --quiet >/dev/null 2>&1; then
  # Konflikt? Pull mit autostash + retry
  if git pull --rebase --autostash origin main --quiet >/dev/null 2>&1; then
    git push origin main --quiet >/dev/null 2>&1 || \
      echo "[auto-sync] Push fehlgeschlagen nach Rebase. Bitte manuell pruefen mit 'git status'." >&2
  else
    echo "[auto-sync] Rebase fehlgeschlagen. Aenderungen sind lokal committed, aber nicht gepusht." >&2
  fi
fi

exit 0
