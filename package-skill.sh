#!/usr/bin/env bash
# Package just the Skill (SKILL.md + reference/) into an upload-ready artifact for
# claude.ai, leaving the test harness and repo meta behind.
# Works under Git Bash on Windows and on macOS/Linux. Output goes to dist/ (gitignored).
#
#   ./package-skill.sh
#   -> dist/garden-maintenance-planner/        (folder, the relative links resolve)
#   -> dist/garden-maintenance-planner.zip     (same, zipped for upload)

set -euo pipefail
cd "$(dirname "$0")"

SKILL_NAME="garden-maintenance-planner"
OUT="dist"
DEST="$OUT/$SKILL_NAME"
ZIP="$OUT/$SKILL_NAME.zip"

echo "==> Packaging skill into $DEST"
rm -rf "$DEST"
mkdir -p "$DEST"
cp SKILL.md "$DEST/"
cp -r reference "$DEST/reference"

echo "==> Creating $ZIP"
# Use Python's zipfile so this works without a `zip` binary (e.g. Git Bash on Windows).
python -c "
import os, sys, zipfile
dest, zippath, root = sys.argv[1], sys.argv[2], sys.argv[3]
if os.path.exists(zippath):
    os.remove(zippath)
with zipfile.ZipFile(zippath, 'w', zipfile.ZIP_DEFLATED) as z:
    for dirpath, _, files in os.walk(dest):
        for name in sorted(files):
            full = os.path.join(dirpath, name)
            arc = os.path.join(root, os.path.relpath(full, dest))
            z.write(full, arc)
" "$DEST" "$ZIP" "$SKILL_NAME"

echo "==> Done. Upload-ready artifact:"
echo "    folder: $DEST/"
echo "    zip:    $ZIP"
echo "==> Contents:"
find "$DEST" -type f | sort
