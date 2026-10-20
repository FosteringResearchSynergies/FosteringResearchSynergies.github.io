---
name: release
description: Pubblica sul sito live lo stato attuale di main, tramite una PR di release main -> deploy. Solo su richiesta esplicita dell'utente.
disable-model-invocation: true
---

# Release: `main` → `deploy`

`deploy` è il branch che GitHub Pages pubblica. Ci si arriva solo con una PR da `main`, mai con
commit o push diretti (l'hook di guardia e le regole del repository li bloccano).

## 1. Cosa sta per andare online

```bash
git fetch origin --prune
git log --oneline origin/deploy..origin/main
```

Se l'elenco è vuoto non c'è nulla da rilasciare: fermati.

## 2. Controlli su `origin/main`

In un worktree temporaneo (dalla root del checkout principale):

```bash
git worktree add --detach .claude/worktrees/release-check origin/main
(cd .claude/worktrees/release-check && scripts/check.sh)
git worktree remove --force .claude/worktrees/release-check
```

Se i controlli falliscono, non aprire la PR: riporta gli errori all'utente.

## 3. PR di release

Mostra all'utente l'elenco dei commit e il conteggio dei placeholder, poi chiedi conferma:
la release cambia il sito pubblico.

```bash
gh pr create --base deploy --head main --title "Release $(date +%F)" --body-file <changelog>
```

Il body contiene l'elenco dei commit, l'esito di `scripts/check.sh` e i placeholder ancora presenti.

## 4. Merge e verifica

Il merge lo fa un umano, oppure tu solo su conferma esplicita, con un merge commit
(mai squash o rebase: `deploy` deve restare un antenato di `main`):

```bash
gh pr merge <numero> --merge
```

Poi verifica la pubblicazione:

```bash
gh run list --branch deploy --limit 3        # deve risultare completato con successo
curl -sI https://fosteringresearchsynergies.github.io/ | head -1
```

Riporta all'utente l'URL live e l'esito. Se il deploy fallisce, il sito resta alla versione
precedente: non tentare correzioni direttamente su `deploy`, apri un task di fix su `main`.
