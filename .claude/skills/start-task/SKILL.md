---
name: start-task
description: Avvia un task su un branch dedicato dentro un worktree isolato. Usala SEMPRE prima di modificare file del sito (feature, fix, contenuti, restyling, docs), anche per modifiche piccole.
---

# Avviare un task: un task = un branch = un worktree

Nel checkout principale non si lavora mai, e mai su `main` o `deploy`: l'hook
`.claude/hooks/guard_protected_branches.py` blocca edit, commit e push diretti su quei branch.

## 1. Nome del branch

`<tipo>/<slug>` con `tipo` tra `feat`, `fix`, `content`, `design`, `chore`, `docs`.
Lo slug è breve, in kebab-case, in inglese: `content/parma-2026`, `design/tokens`, `fix/events-unclosed-div`.

## 2. Worktree aggiornato su `origin/main`

```bash
MAIN="$(dirname "$(git rev-parse --path-format=absolute --git-common-dir)")"   # root del checkout principale
git -C "$MAIN" fetch origin --prune
git -C "$MAIN" worktree add --no-track -b <tipo>/<slug> "$MAIN/.claude/worktrees/<slug>" origin/main
cd "$MAIN/.claude/worktrees/<slug>"
```

`--no-track` evita che il branch segua `origin/main`: un `git push` senza argomenti non deve mai
puntare a `main`.

Se un task dipende da un altro non ancora in `main` (per esempio la pagina Parma dal design system),
parti dal branch dell'altro task invece che da `origin/main` e scrivilo nella PR.

Se sei un subagente avviato con isolamento `worktree`, il worktree esiste già: verifica che contenga
`origin/main` aggiornato (`git fetch origin && git merge-base --is-ancestor origin/main HEAD`) e
rinomina il branch con `git branch -m <tipo>/<slug>`.

## 3. Lavoro

- Più agenti in parallelo toccano file diversi. Se due task devono modificare lo stesso file
  (CSS globale, layout, dati comuni), vanno in sequenza.
- Commit piccoli e atomici, messaggio in inglese all'imperativo (`Add Parma 2026 key dates`).
- Prima di ogni commit: skill `preview` (`scripts/check.sh` e controllo visivo).
- Regole sui contenuti in `CLAUDE.md`: niente fatti inventati, placeholder onesti.

## 4. Push e Pull Request verso `main`

Push e PR sono azioni visibili all'esterno: falle solo se l'utente le ha chieste o autorizzate per
questo task.

```bash
git push -u origin <tipo>/<slug>
gh pr create --base main --head <tipo>/<slug> --title "<titolo>" --body-file <file>
```

Il body della PR contiene: cosa cambia e perché, come verificarlo, l'esito di `scripts/check.sh`,
i placeholder introdotti e le domande aperte per il team.

## 5. Pulizia dopo il merge

```bash
git -C "$MAIN" worktree remove "$MAIN/.claude/worktrees/<slug>"
git -C "$MAIN" branch -d <tipo>/<slug>
git -C "$MAIN" fetch origin --prune
```
