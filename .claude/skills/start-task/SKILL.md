---
name: start-task
description: Avvia un task su un branch dedicato dentro un worktree isolato. Usala SEMPRE prima di modificare file del sito (feature, fix, contenuti, restyling, docs), anche per modifiche piccole.
---

# Avviare un task: un task = un branch = un worktree

Il checkout principale è in sola lettura per gli agenti, su qualunque branch si trovi, e nessuno
lavora mai su `main` o `deploy`: l'hook `.claude/hooks/guard_protected_branches.py` blocca edit,
commit e push diretti. Ogni task ha il suo branch e il suo worktree in `.claude/worktrees/`.

Ogni blocco di codice qui sotto è autonomo: eseguilo in una sola chiamata Bash. Le variabili non
sopravvivono da una chiamata all'altra, per questo `MAIN` viene ricalcolato in ogni blocco.
Con `$VAR` o backtick in `cd` o `git -C` l'hook non sa in che cartella sei: lascia passare solo git in
lettura, `fetch`, `worktree add/remove`, `branch -d` e `merge --ff-only origin/main` e blocca commit, merge, rebase, `reset --hard`, cherry-pick, revert, checkout/switch e push
senza branch esplicito. Per quei comandi scrivi il percorso assoluto per esteso.

## 1. Nome del branch

`<tipo>/<slug>` con `tipo` tra `feat`, `fix`, `content`, `design`, `chore`, `docs`.
Lo slug è breve, in kebab-case, in inglese: `content/parma-2026`, `design/tokens`, `fix/events-unclosed-div`.
Se sei un subagente, branch ed eventuale dipendenza sono nel prompt.

## 2. Dove sei

```bash
git rev-parse --path-format=absolute --git-dir --git-common-dir --show-toplevel
git branch --show-current
```

- Le prime due righe sono uguali: sei nel **checkout principale** → 2a.
- Sono diverse e la terza riga contiene `/.claude/worktrees/`: sei in un **worktree creato da Claude
  Code** (subagente con `isolation: worktree`, `claude --worktree`, EnterWorktree) → 2b. Se il branch
  è già `<tipo>/<slug>` di questo task, il task è già avviato: vai al punto 3.
- Altri casi: fermati e chiedi all'utente.

### 2a. Dal checkout principale: crea il worktree

```bash
MAIN="$(dirname "$(git rev-parse --path-format=absolute --git-common-dir)")"
git -C "$MAIN" fetch origin --prune
[ "$(git -C "$MAIN" branch --show-current)" = main ] && git -C "$MAIN" merge --ff-only origin/main
git -C "$MAIN" worktree add --no-track -b <tipo>/<slug> "$MAIN/.claude/worktrees/<slug>" origin/main
echo "worktree: $MAIN/.claude/worktrees/<slug>"
```

Il `merge --ff-only` riallinea il `main` locale del checkout principale a `origin/main`: il file
dell'hook vale subito, impostazioni, skill e `CLAUDE.md` dopo il riavvio di Claude Code. È l'unica modifica ammessa ai file del checkout principale.
Se fallisce, non correggere nulla: dillo all'utente.

`--no-track` evita che il branch segua `origin/main`: un `git push` senza argomenti non deve mai
puntare a `main`.

Poi spostati nel worktree con il percorso stampato, scritto per esteso:
`cd /percorso/assoluto/.claude/worktrees/<slug>`. Edit e Write sempre con percorsi assoluti dentro
il worktree, mai sui file del checkout principale.

**Task dipendente** (parte da un branch non ancora in `main`, per esempio la pagina Parma dal design
system): nella riga `git worktree add` sostituisci `origin/main` con `origin/<branch-dipendenza>`.

### 2b. Già in un worktree creato da Claude Code: rinomina il branch

```bash
git fetch origin --prune
git merge-base --is-ancestor origin/main HEAD && echo "base aggiornata" || echo "base vecchia"
git branch --unset-upstream 2>/dev/null
git branch -m <tipo>/<slug>
```

Qui non usare `git -C` verso il checkout principale: la pulizia la fa una sessione avviata lì
(punto 5).
Se stampa "base vecchia" e il worktree non ha ancora commit né modifiche (`git status --short` e
`git log --oneline origin/main..HEAD` vuoti): `git reset --hard origin/main`. Se ci sono già modifiche,
fermati e chiedi.

**Task dipendente**: prima di qualsiasi modifica, `git reset --hard origin/<branch-dipendenza>`.

In entrambi i casi, per un task dipendente scrivi nella PR da quale branch parti: finché quel branch
non è in `main`, la PR ne mostra anche i commit.

## 3. Lavoro

- Più agenti in parallelo toccano file diversi. Se due task devono modificare lo stesso file
  (CSS globale, layout, dati comuni), vanno in sequenza oppure uno parte dal branch dell'altro.
- Commit piccoli e atomici, messaggio in inglese all'imperativo (`Add Parma 2026 key dates`).
  Come autore è preferibile l'indirizzo noreply di GitHub: se `git config user.email` è un indirizzo
  personale, segnalalo all'utente senza cambiarlo.
- Prima di ogni commit: skill `preview` (`scripts/check.sh` con i test web e mobile, e controllo
  visivo degli screenshot in `_screenshots/`).
- Regole sui contenuti in `CLAUDE.md`: niente fatti inventati, placeholder onesti.

## 4. Push e Pull Request verso `main`

Push e PR sono azioni visibili all'esterno. Chiedi conferma all'utente prima di ogni push e prima di
ogni apertura di PR: un'autorizzazione precedente non vale per l'azione successiva.
Un subagente non fa push né PR: restituisce branch, percorso assoluto del worktree ed esito dei
controlli alla sessione principale, che chiede conferma all'utente.

```bash
git push -u origin <tipo>/<slug>
gh pr create --base main --head <tipo>/<slug> --title "<titolo>" --body-file <file fuori dal repository>
```

Il body della PR contiene: cosa cambia e perché, come verificarlo, l'esito di `scripts/check.sh`
(solo exit code e conteggi, mai le righe trovate dai controlli; test web e mobile compresi), le
larghezze di cui hai guardato gli screenshot, i placeholder introdotti e le domande aperte per il
team. Il controllo `check` su GitHub ripete i test sulla PR.

## 5. Pulizia dopo il merge

Da una sessione avviata nel checkout principale: il `cd` riporta la shell lì prima di rimuovere il
worktree (non farlo da una sessione `claude --worktree`: rimuoveresti la cartella in cui lavora). Il percorso del worktree è quello stampato al punto 2a o riportato dal
subagente; `git worktree list` li elenca tutti.

```bash
MAIN="$(dirname "$(git rev-parse --path-format=absolute --git-common-dir)")"
cd "$MAIN"
git -C "$MAIN" fetch origin --prune
[ "$(git -C "$MAIN" branch --show-current)" = main ] && git -C "$MAIN" merge --ff-only origin/main
git -C "$MAIN" worktree remove "<percorso assoluto del worktree>"
git -C "$MAIN" branch -d <tipo>/<slug>
```

Se `branch -d` rifiuta perché il branch non risulta unito (per esempio una PR chiusa con squash),
non usare `-D`: dillo all'utente.
