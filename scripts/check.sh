#!/usr/bin/env bash
# QA gate run before every PR: HTML validation, internal links, fake links, personal data,
# plus a report of the honest placeholders still on the site.
#
#   scripts/check.sh               # exit code 0 = OK
#
# With a package.json (Eleventy) or a Gemfile (Jekyll) it builds first and checks _site/;
# otherwise it checks the raw files.
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"
SITE="$ROOT"
if [[ -f package.json ]]; then
    [[ -d node_modules ]] || npm ci --no-audit --no-fund
    npm run build
    SITE="$ROOT/_site"
elif [[ -f Gemfile ]]; then
    bundle exec jekyll build --quiet
    SITE="$ROOT/_site"
fi

status=0
mapfile -t pages < <(cd "$SITE" && find . -name '*.html' -not -path './node_modules/*' -not -path './.claude/*' -not -path './_site/*' | sort)
grep_site() {
    grep -rnE "$@" --include='*.html' "$SITE" --exclude-dir=node_modules --exclude-dir=.claude --exclude-dir=_site
}

echo "== HTML validation (${#pages[@]} pages)"
(cd "$SITE" && npx --yes html-validate@9 --formatter text "${pages[@]}") || status=1

echo "== Internal links"
npx --yes linkinator@6 "$SITE" --recurse --verbosity error --skip '^(?!http://localhost)https?://' --skip 'node_modules|\.claude' || status=1

echo "== Fake links (href=\"#\")"
if grep_site 'href="#"'; then
    status=1
fi

echo "== Personal data (phone numbers)"
if grep_site '\+[0-9]{2}[ .]?[0-9]{2,4}[ .]?[0-9]{3,4}[ .]?[0-9]{3,4}'; then
    status=1
fi

echo "== Placeholders still on the site (report only)"
for kind in lorem tba unbuilt; do
    printf '  %-8s %s\n' "$kind" "$( (grep_site "data-placeholder=\"$kind\"" || true) | wc -l)"
done
printf '  %-8s %s\n' "TODO" "$( (grep_site 'TODO\(team\)' || true) | wc -l)"

exit $status
