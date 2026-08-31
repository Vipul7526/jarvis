#!/usr/bin/env bash
set -euo pipefail

# Publish the current repository and create an immutable-by-name source archive.
# Required environment variable: JARVIS_DRIVE_PARENT_ID
# Optional: JARVIS_BRANCH (default: main)

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BRANCH="${JARVIS_BRANCH:-main}"
DRIVE_PARENT_ID="${JARVIS_DRIVE_PARENT_ID:-}"

if [[ -z "$DRIVE_PARENT_ID" ]]; then
  echo "JARVIS_DRIVE_PARENT_ID is required; no Drive upload was attempted." >&2
  exit 2
fi

cd "$ROOT_DIR"

if [[ -n "$(git status --porcelain)" ]]; then
  git add -A
  git commit -m "chore: publish J.A.R.V.I.S. updates"
fi

git push origin "$BRANCH"
COMMIT="$(git rev-parse --short HEAD)"
STAMP="$(date -u +%Y-%m-%dT%H-%M-%SZ)"
ARCHIVE="/tmp/JARVIS-source-${COMMIT}-${STAMP}.zip"

rm -f "$ARCHIVE"
zip -qr "$ARCHIVE" . \
  -x './.git/*' './**/__pycache__/*' './**/.pytest_cache/*' './*.zip'

CHECKSUM="$(sha256sum "$ARCHIVE" | awk '{print $1}')"
NAME="JARVIS-source-${COMMIT}-${STAMP}.zip"

# gws uses the active Google Workspace account selected in Manus configuration.
gws drive files create \
  --upload "$ARCHIVE" \
  --upload-content-type application/zip \
  --json "{\"name\":\"${NAME}\",\"parents\":[\"${DRIVE_PARENT_ID}\"],\"description\":\"Complete J.A.R.V.I.S. source backup for Git commit ${COMMIT}. SHA-256: ${CHECKSUM}\"}" \
  --format json

echo "Published commit: ${COMMIT}"
echo "Backup archive: ${ARCHIVE}"
echo "Backup SHA-256: ${CHECKSUM}"
