#!/usr/bin/env bash
# Serve the site locally for review.
#
#   scripts/preview.sh             # port derived from the checkout path, so parallel worktrees don't collide
#   PORT=8123 scripts/preview.sh   # force a port
#
# With a package.json it runs `npm run dev -- --port=N` (Eleventy), with a Gemfile `jekyll serve`;
# otherwise it serves the raw files.
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
PORT="${PORT:-$((8000 + $(printf '%s' "$ROOT" | cksum | cut -d' ' -f1) % 900))}"
cd "$ROOT"

echo "Preview: http://127.0.0.1:$PORT  (Ctrl+C to stop)" >&2
if [[ -f package.json ]]; then
    [[ -d node_modules ]] || npm ci --no-audit --no-fund
    exec npm run dev -- --port="$PORT"
elif [[ -f Gemfile ]]; then
    exec bundle exec jekyll serve --host 127.0.0.1 --port "$PORT" --livereload-port "$((PORT + 27000))"
fi
exec python3 -m http.server "$PORT" --bind 127.0.0.1
