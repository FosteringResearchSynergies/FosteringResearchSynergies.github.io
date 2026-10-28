#!/usr/bin/env bash
# Serve the site locally for review, at http://127.0.0.1:PORT.
# The Eleventy dev server (3.1) has no host option and also answers on the other network interfaces:
# use it on a trusted network.
#
#   scripts/preview.sh             # port derived from the checkout path, so parallel worktrees don't collide
#   PORT=8123 scripts/preview.sh   # force a port
#
# Works from any directory: it serves the checkout that contains this script.
# With a package.json it runs `npm run dev -- --port=N` (Eleventy), with a Gemfile `jekyll serve`;
# otherwise it serves the raw files.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
PORT="${PORT:-$((8000 + $(printf '%s' "$ROOT" | cksum | cut -d' ' -f1) % 900))}"
cd "$ROOT"

case "$PORT" in
    '' | *[!0-9]*) echo "PORT must be a number, got '$PORT'" >&2; exit 1 ;;
esac
PORT=$((10#$PORT))   # no octal surprises with a leading zero
if [[ $PORT -lt 1024 || $PORT -gt 65535 ]]; then
    echo "PORT must be between 1024 and 65535, got $PORT" >&2
    exit 1
fi
# Fail now if the port is taken: Eleventy would silently move to another port and the URL below would be wrong.
if ! python3 -c 'import socket, sys
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("127.0.0.1", int(sys.argv[1])))' "$PORT" 2>/dev/null; then
    echo "Port $PORT is busy: stop the other server or run PORT=<free port> scripts/preview.sh" >&2
    exit 1
fi

echo "Preview: http://127.0.0.1:$PORT  (Ctrl+C to stop)" >&2
if [[ -f package.json ]]; then
    [[ -d node_modules ]] || npm ci --no-audit --no-fund
    exec npm run dev -- --port="$PORT"
elif [[ -f Gemfile ]]; then
    lr=$((PORT + 27000)); [[ $lr -le 65535 ]] || lr=$((PORT - 27000))
    exec bundle exec jekyll serve --host 127.0.0.1 --port "$PORT" --livereload-port "$lr"
fi
exec python3 -m http.server "$PORT" --bind 127.0.0.1
