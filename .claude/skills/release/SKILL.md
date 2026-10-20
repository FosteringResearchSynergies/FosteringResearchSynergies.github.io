---
name: release
description: Pubblica sul sito live lo stato attuale di main, tramite una PR di release main -> deploy. Solo su richiesta esplicita dell'utente.
disable-model-invocation: true
---

# Release: `main` → `deploy`

`deploy` è il branch che GitHub Pages pubblica. Ci si arriva solo con una PR da `main` chiusa con un
merge commit. Gli agenti non fanno mai push su `main` o `deploy` (l'hook di guardia li blocca) e non
cambiano impostazioni di Pages, environment o regole del repository: sono passi del team.

Esegui la skill da una sessione avviata nella root del checkout principale. Ogni blocco è autonomo:
eseguilo in una sola chiamata Bash.

## 1. Cosa sta per andare online

```bash
git fetch origin --prune
echo "== da rilasciare";            git log --oneline origin/deploy..origin/main
echo "== su deploy ma non su main"; git log --oneline --no-merges origin/main..origin/deploy
```

Se il primo elenco è vuoto non c'è nulla da rilasciare: fermati. Il secondo deve essere vuoto: se non
lo è, `deploy` contiene commit che non sono in `main` (un revert, una correzione diretta) e il merge non
li gestisce da solo. Fermati e chiedi al team come procedere.

## 2. Modalità di pubblicazione

```bash
gh api repos/FosteringResearchSynergies/FosteringResearchSynergies.github.io/pages --jq .build_type
git cat-file -e origin/main:package.json 2>/dev/null && echo "main: generatore" || echo "main: HTML"
```

Le combinazioni valide sono due:
- `legacy` + HTML: Pages pubblica la root di `deploy` così com'è ("Deploy from branch");
- `workflow` + generatore: il push su `deploy` avvia `pages.yml`, che pubblica `_site/`.

`legacy` + generatore: **fermati**. Dal merge di `feat/scaffold` le release sono congelate finché il
team non passa Pages a "GitHub Actions" (ROADMAP, Giorno 3): Pages pubblicherebbe i sorgenti di
Eleventy invece del sito. Nel passaggio del Giorno 3 il team cambia `build_type` **prima** di aprire la
release, quindi non ci sono eccezioni. Qualsiasi altra combinazione: fermati e chiedi al team.

## 3. Controlli su `origin/main`

In un worktree temporaneo:

```bash
MAIN="$(dirname "$(git rev-parse --path-format=absolute --git-common-dir)")"
git -C "$MAIN" worktree add --detach "$MAIN/.claude/worktrees/release-check" origin/main
"$MAIN/.claude/worktrees/release-check/scripts/check.sh"; echo "check.sh exit: $?"
git -C "$MAIN" worktree remove --force "$MAIN/.claude/worktrees/release-check"
```

`check.sh` deve terminare con exit 0 (gli avvisi preesistenti di `html-validate` non bloccano). Se
fallisce, non aprire la PR: riporta all'utente i problemi trovati.

## 4. PR di release

Mostra all'utente l'elenco dei commit, l'esito dei controlli e il conteggio dei placeholder, poi chiedi
conferma: la release cambia il sito pubblico. Solo dopo il suo sì:

```bash
gh pr create --base deploy --head main --title "Release $(date +%F)" --body-file <file fuori dal repository>
```

Il body contiene l'elenco dei commit, la modalità di pubblicazione (`legacy` o `workflow`), l'exit
code di `scripts/check.sh` e i conteggi dei placeholder: mai le righe trovate dai controlli.

## 5. Merge

Il merge lo fa chi approva le release (decisione D4 della ROADMAP), dall'interfaccia di GitHub, con
**Create a merge commit**. Mai squash o rebase: con il merge commit `main` resta un antenato di
`deploy` e la release successiva non genera conflitti.

Aspetta che l'utente ti dica che la PR è unita.

## 6. Verifica dopo il merge

Il deploy da controllare è quello del merge commit della PR, non l'ultimo che compare in elenco.

```bash
git fetch origin --prune
git merge-base --is-ancestor origin/main origin/deploy && echo "ok: main è antenato di deploy" || echo "NO: main non è antenato di deploy"
gh pr view <numero> --json mergeCommit --jq .mergeCommit.oid
```

Se il controllo di ascendenza fallisce perché nel frattempo `main` ha ricevuto altri commit, ripetilo
con lo sha della testa della PR (`gh pr view <numero> --json headRefOid --jq .headRefOid`) al posto
di `origin/main`.

Modalità `legacy`: la build più recente di Pages deve essere `built` sullo sha del merge commit
(`building` o `queued`: riprova dopo un minuto). Se dopo qualche minuto non c'è nessuna build su quello
sha, chiedi all'utente di avviarla: `gh api -X POST repos/FosteringResearchSynergies/FosteringResearchSynergies.github.io/pages/builds`.

```bash
gh api repos/FosteringResearchSynergies/FosteringResearchSynergies.github.io/pages/builds/latest --jq '.status + " " + .commit'
```

Modalità `workflow`: segui la run di `pages.yml` di quel commit fino alla fine.

```bash
sha="$(gh pr view <numero> --json mergeCommit --jq .mergeCommit.oid)"
id="$(gh run list --workflow pages.yml --branch deploy --commit "$sha" --json databaseId --jq '.[0].databaseId')"
if [ -n "$id" ]; then gh run watch "$id" --exit-status; else echo "run non ancora partita: riprova tra poco"; fi
```

In entrambi i casi il sito deve rispondere `HTTP/2 200`, senza redirect:

```bash
curl -sI https://fosteringresearchsynergies.github.io/ | head -1
```

Riporta all'utente l'URL live, lo sha pubblicato e l'esito.

Dopo la prima release da `deploy` andata a buon fine, se l'environment `github-pages` ammette ancora
`main` tra i branch di deploy (Settings → Environments), ricorda al team di toglierlo: deve restare solo
`deploy`. È un passo umano: tu non lo fai.

## 7. Rollback

Ogni azione qui sotto è visibile all'esterno: chiedi conferma all'utente prima di ciascuna.

- **Modalità `legacy` (Pages pubblica la root di `deploy`)**: si annulla il merge di release su
  `deploy` con una PR di revert. Branch `fix/revert-<slug>` da `origin/deploy` in un worktree (skill
  `start-task`, punto 2a, con `origin/deploy` come base), `git revert -m 1 <sha del merge di release>`,
  PR verso `deploy` approvata come una release. La correzione vera va poi su `main` con un task
  normale; alla release successiva il punto 1 si ferma sul revert e la decisione passa al team.
- **Con GitHub Actions**: se il deploy fallisce resta online la versione precedente e non c'è nulla
  da annullare: apri un task di fix su `main`. Se un deploy riuscito pubblica un sito sbagliato,
  rilancia l'ultima run buona di `pages.yml` (`gh run rerun <id>`) oppure apri la PR di revert su
  `deploy` come sopra. Al primo deploy con Actions non esiste una run precedente: PR di revert e
  **[team]** ritorno di Pages a "Deploy from branch" su `deploy` (root).
- Mai rimettere Pages su `main` (root) e mai riaggiungere il dominio custom a questo repository: il
  vecchio dominio appartiene al repository di redirect `frs-workshop-redirect`.

Non tentare mai correzioni con commit o push diretti su `deploy`.
