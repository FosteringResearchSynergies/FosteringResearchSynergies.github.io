#!/usr/bin/env bash
# QA gate run before every PR and before anything is published: HTML validation, internal links, fake
# links and forms, personal data, CNAME, web and mobile checks in headless Chrome (scripts/viewports.mjs),
# plus a report of the honest placeholders still on the site.
#
#   scripts/check.sh               # exit code 0 = OK; works from any directory
#
# With a package.json (Eleventy) or a Gemfile (Jekyll) it rebuilds _site/ from scratch and checks it;
# otherwise it checks the raw files. The output never contains absolute paths or matched personal data;
# PR bodies and CI summaries still carry only the exit code and the counts.
# Needs bash >= 3.2 (macOS default is fine), node/npx, python3, Google Chrome or Chromium (or CHROME=path)
# and the usual POSIX tools.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"   # physical path: tools print that one
cd "$ROOT"
case "$ROOT" in
    *[][{}]*) echo "== Result: FAILED (the checkout path contains [ ] { }, which linkinator reads as a glob)"
              exit 1 ;;
esac
export NODE_NO_WARNINGS=1

# Tool output goes through scrub, which turns local paths into repository-relative ones.
sed_escape() { printf '%s' "$1" | sed 's/[][\\.*^$|]/\\&/g'; }
scrub_args=(-e "s|$(sed_escape "$ROOT")/||g" -e "s|$(sed_escape "$ROOT")|.|g")
if [[ -n "${HOME:-}" && "$HOME" != "/" ]]; then
    scrub_args+=(-e "s|$(sed_escape "$HOME")|~|g")
fi
scrub() { sed "${scrub_args[@]}"; }
# Masks long digit runs in tool output, so a phone number in a link or an attribute never reaches a log.
redact() { sed -E 's/[0-9][0-9 .\/()%-]{6,}[0-9]/<digits>/g'; }
# Runs a build step with scrubbed output; stops the whole check if it fails.
step() { "$@" 2>&1 | scrub || { echo "== Result: FAILED ($*)"; exit 1; }; }

SITE="$ROOT"
PREFIX=""
if [[ -f package.json || -f Gemfile ]]; then
    echo "== Build"
    rm -rf "$ROOT/_site"   # generators do not clean their output: stale pages would be checked
    if [[ -f package.json ]]; then
        [[ -d node_modules ]] || step npm ci --no-audit --no-fund
        step npm run build
    else
        step bundle exec jekyll build --quiet
    fi
    SITE="$ROOT/_site"
    PREFIX="_site/"
    [[ -d "$SITE" ]] || { echo "== Result: FAILED (the build did not produce _site/)"; exit 1; }
fi

# Published files, relative to $SITE: dot entries (.git, .claude, ...), dependencies and old builds
# are skipped. Plain while-read loops instead of mapfile, for bash 3.
list_files() {
    (cd "$SITE" && find . \( -name '.?*' -o -name node_modules -o -name _site \) -prune -o -type f \( "$@" \) -print) |
        sed 's|^\./||' | LC_ALL=C sort
}
pages=()
while IFS= read -r f; do pages+=("$f"); done < <(list_files -name '*.html' -o -name '*.htm')
texts=()
while IFS= read -r f; do texts+=("$f"); done < <(list_files -name '*.html' -o -name '*.htm' \
    -o -name '*.js' -o -name '*.mjs' -o -name '*.json' -o -name '*.xml' -o -name '*.txt' -o -name '*.svg' \
    -o -name '*.webmanifest' -o -name '*.ics' -o -name '*.vcf')
if [[ ${#pages[@]} -eq 0 ]]; then
    echo "== Result: FAILED (no HTML pages in ${PREFIX:-the repository root})"
    exit 1
fi

status=0

# Prints "file:line" for each line of the given files matching an extended regex (case-insensitive).
# The matched text itself is never printed.
locate() {
    local re="$1"
    shift
    (cd "$SITE" && grep -HniE -- "$re" "$@" || true) | cut -d: -f1,2
}
# Prints a "file:line" list (if not empty) and marks the run as failed.
flag() {
    if [[ -n "$1" ]]; then
        printf '%s\n' "$1" | LC_ALL=C sort -t: -k1,1 -k2,2n -u | sed "s|^|  $PREFIX|"
        status=1
    fi
}
# Number of occurrences (not lines) of an extended regex in the given files.
count() {
    local re="$1"
    shift
    (cd "$SITE" && grep -ohE -- "$re" "$@" || true) | wc -l | tr -d ' '
}

echo "== HTML validation (${#pages[@]} pages)"
hv="$(cd "$SITE" && npx --yes html-validate@9.7.1 --formatter text "${pages[@]}" 2>&1)" || status=1
if [[ -n "$hv" ]]; then
    printf '%s\n' "$hv" | grep -v ': warning \[' | scrub | redact || true
    # Rules set to "warn" in .htmlvalidate.json for the legacy pages: summarised, not listed.
    printf '%s\n' "$hv" | grep -o ': warning \[[a-z0-9-]*\]' | sed 's/.*\[\(.*\)\]/\1/' | sort | uniq -c |
        awk '{ printf "  %s warnings: %s\n", $1, $2 }' || true
fi

echo "== Internal links (every page)"
(cd "$SITE" && npx --yes linkinator@6.3.0 "${pages[@]}" --server-root "$SITE" --recurse --verbosity error \
    --skip '^(?!http://localhost)https?://') 2>&1 | scrub | redact || status=1

echo "== Fake links and form targets (\"#\", \"\", javascript:; pages and scripts)"
flag "$(locate "(href|action)[[:space:]]*=[[:space:]]*[\"'][[:space:]]*(#|javascript:[^\"']*)?[[:space:]]*[\"']" "${texts[@]}")"

echo "== Forms without action"
# Start tags may span several lines; an empty action counts as missing.
flag "$(cd "$SITE" && awk -v q="'" '
    FNR == 1 { open = 0 }
    {
        rest = tolower($0)
        while (1) {
            if (!open) {
                if (!match(rest, "<form([ \t/>]|$)")) break
                open = 1; tag = ""; line = FNR
                rest = substr(rest, RSTART + 5)
            }
            end = index(rest, ">")
            if (!end) { tag = tag " " rest; break }
            tag = tag " " substr(rest, 1, end - 1)
            rest = substr(rest, end + 1)
            open = 0
            if (tag !~ "[ \t]action[ \t]*=" || tag ~ ("[ \t]action[ \t]*=[ \t]*(\"\"|" q q ")"))
                print FILENAME ":" line
        }
    }' "${pages[@]}")"

echo "== Personal data (phone numbers; location only)"
# International: + then at least 8 digits with short separators, or 00 + country code + separator (so
# that VAT numbers such as 00123456789 do not match). Italian mobile: 3xx xxx xxxx with consistent
# separators, 3xx/xxxxxxx or 3xx xxx xx xx. Non-breaking spaces count as spaces. Plus tel:, sms: and WhatsApp links. SVG geometry attributes (d, points, viewBox,
# transform, also across lines) are blanked first: their coordinates look like digit groups.
intl='(^|[^0-9a-z])\+[1-9]([ ./()-]{0,2}[0-9]){7,14}|(^|[^0-9a-z.])00[1-9][0-9]{0,2}[ ./()-]{1,2}[0-9]([ ./()-]{0,2}[0-9]){6,13}'
mobile='(^|[^0-9a-z_./#=-])3[0-9]{2}( ?[0-9]{3} ?[0-9]{4}|-[0-9]{3}-?[0-9]{4}|\.[0-9]{3}\.[0-9]{4}| ?/ ?[0-9]{3} ?[0-9]{4}| [0-9]{3} [0-9]{2} [0-9]{2})([^0-9]|$)'
links='(^|[^a-z])(tel|sms|callto):|wa\.me/|whatsapp\.com/send'
flag "$( (cd "$SITE" && awk '
    FNR == 1 { open = 0 }
    {
        line = tolower($0)
        gsub(/&nbsp;|&#160;|&#x0*a0;|&#8239;|&#x202f;|\302\240|\342\200\257/, " ", line)
        if (open) {
            i = index(line, "\"")
            if (!i) { print FILENAME ":" FNR ":"; next }
            line = substr(line, i + 1)
            open = 0
        }
        gsub(/(^|[ \t])(d|points|viewbox|transform)[ \t]*=[ \t]*"[^"]*"/, " ", line)
        if (match(line, /(^|[ \t])(d|points|viewbox|transform)[ \t]*=[ \t]*"/)) {
            line = substr(line, 1, RSTART)
            open = 1
        }
        print FILENAME ":" FNR ":" line
    }' "${texts[@]}") | { grep -iE "$intl|$mobile|$links" || true; } | cut -d: -f1,2)"

if [[ -n "$PREFIX" ]]; then
    echo "== Internal files in the published output (*.md, dot entries)"
    flag "$(cd "$SITE" && find . \( -name '*.md' -o -name '.?*' \) ! -name .nojekyll -print | sed 's|^\./||')"
fi

echo "== CNAME (the custom domain belongs to the redirect repository)"
if [[ -e "$SITE/CNAME" ]]; then
    echo "  ${PREFIX}CNAME"
    status=1
fi

echo "== Web and mobile (headless Chrome at 320, 375, 768 and 1280 px)"
SHOTS="$ROOT/_screenshots"
rm -rf "$SHOTS"
port="$(python3 -c 'import socket; s = socket.socket(); s.bind(("127.0.0.1", 0)); print(s.getsockname()[1])')"
python3 -m http.server "$port" --bind 127.0.0.1 --directory "$SITE" >/dev/null 2>&1 &
server=$!
trap 'kill "$server" 2>/dev/null || true' EXIT
for _ in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20; do
    python3 -c 'import sys, urllib.request; urllib.request.urlopen(sys.argv[1], timeout=1)' \
        "http://127.0.0.1:$port/" 2>/dev/null && break
    sleep 0.25
done
node "$ROOT/scripts/viewports.mjs" "http://127.0.0.1:$port/" "$SHOTS" "${pages[@]}" 2>&1 | scrub | redact || status=1
kill "$server" 2>/dev/null || true
echo "  screenshots for review: _screenshots/<viewport>/ (not committed)"

echo "== Placeholders still on the site (report only)"
for kind in lorem tba unbuilt; do
    printf '  %-12s %s\n' "$kind" "$(count "data-placeholder=[\"']?$kind[\"' >]" "${pages[@]}")"
done
printf '  %-12s %s\n' "TODO(team)" "$(count 'TODO\(team\)' "${texts[@]}")"
# "Lorem ipsum" outside an element marked data-placeholder="lorem" (it may span several lines).
stray="$(cd "$SITE" && awk -v q="'" '
    FNR == 1 { inside = 0 }
    {
        line = tolower($0); from = 1
        if (match(line, "data-placeholder=[\"" q "]?lorem")) { inside = 1; from = RSTART }
        if (!inside && line ~ /lorem ipsum/) print FILENAME ":" FNR
        if (inside && index(substr(line, from), "</")) inside = 0
    }' "${pages[@]}")"
if [[ -n "$stray" ]]; then
    printf '  %-12s %s\n' "stray lorem" "$(printf '%s\n' "$stray" | wc -l | tr -d ' ')"
    printf '%s\n' "$stray" | sed "s|^|    $PREFIX|"
else
    printf '  %-12s %s\n' "stray lorem" 0
fi

if [[ $status -eq 0 ]]; then
    echo "== Result: OK"
    # Record what passed: commit and tree (same files = same site). The guard hook lets a PR into deploy,
    # its merge or a Pages change through only for a recorded commit or tree; with uncommitted or
    # untracked files nothing is recorded.
    if sha="$(git -C "$ROOT" rev-parse --verify -q 'HEAD^{commit}' 2>/dev/null)" &&
        tree="$(git -C "$ROOT" rev-parse --verify -q 'HEAD^{tree}' 2>/dev/null)" &&
        common="$(cd "$ROOT" && cd "$(git rev-parse --git-common-dir)" && pwd -P)" &&
        [[ -z "$(git -C "$ROOT" status --porcelain 2>/dev/null)" ]]; then
        printf '%s %s %s\n' "$sha" "$tree" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" >> "$common/frs-check-passed" || true
    fi
else
    echo "== Result: FAILED"
fi
exit $status
