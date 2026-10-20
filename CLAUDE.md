# Fostering Research Synergies: regole per gli agenti

Sito statico del workshop **Fostering Research Synergies (FRS)**, organizzato da dottorandi e postdoc
che lavorano su sistemi complessi (CREF Roma, IMT Lucca, CSH Vienna). GitHub Pages lo pubblica dal
branch `deploy` su `https://fosteringresearchsynergies.github.io/`. Il sito è in **inglese**;
documentazione, istruzioni per gli agenti e comunicazioni con il team sono in **italiano**.

Contesto: `docs/ROADMAP.md` (piano e decisioni), `docs/AUDIT.md` (inventario dei problemi),
`docs/DESIGN.md` (direzione visiva e struttura delle pagine). Per placeholder e CTA vale questo file:
le correzioni dell'audit dicono cosa cambiare, non come.

## Avvio

- Avvia Claude Code dalla root del checkout principale (da una sottocartella hook, permessi e skill non
  si caricano). Serve `python3` nel PATH, su Windows anche Git Bash: senza, l'hook di guardia non gira.
- Hook, permessi, skill e questo file si leggono dal checkout principale. Dopo il merge di una PR che li
  modifica: `git pull --ff-only` nel checkout principale, poi riavvia Claude Code.

## Branch e worktree

| Branch | Ruolo | Come ci si arriva |
| --- | --- | --- |
| `main` | integrazione, sempre funzionante | solo PR da branch di task |
| `deploy` | ciò che è online (sorgente di Pages) | solo PR di release `main` → `deploy` o PR di revert `fix/revert-<slug>`, con merge commit (skill `release`) |
| `<tipo>/<slug>` | un task | worktree in `.claude/worktrees/<slug>` (skill `start-task`) |

- Un task = un branch = un worktree. Tipi di branch: `feat`, `fix`, `content`, `design`, `chore`, `docs`.
- Il checkout principale è in sola lettura per gli agenti, su qualunque branch sia. Lì sono ammessi solo
  git in lettura, `git fetch origin [--prune]`, `git merge --ff-only origin/main` o `git pull --ff-only`
  (per riallinearlo), `git worktree add|remove|prune|list` e `git branch -d`.
- L'hook `.claude/hooks/guard_protected_branches.py` blocca modifiche e commit nel checkout principale e
  su `main`/`deploy`, il passaggio a quei branch, i push verso di loro, i force push e le cancellazioni
  remote. Non aggirarlo con `sed -i`, redirect della shell o `FRS_ALLOW_PROTECTED` (riservata agli umani).
- Con `$VAR` o backtick in `cd`/`git -C` l'hook blocca commit, merge, reset, checkout e push: scrivi il
  percorso per esteso (checkout principale: `dirname` di `git rev-parse --path-format=absolute --git-common-dir`).
- Agenti in parallelo toccano file diversi; i file condivisi (CSS globale, layout, dati) un task alla volta.
- Commit piccoli, messaggi in inglese all'imperativo (`Add Parma 2026 key dates`). Come autore è
  preferibile l'indirizzo noreply di GitHub (`<id>+<login>@users.noreply.github.com`).

## Azioni che richiedono conferma esplicita dell'utente

Chiedi conferma prima di **ogni** push e prima di aprire **ogni** PR: un'autorizzazione precedente non
vale per l'azione successiva. Lo stesso per merge di PR, commenti su GitHub, `gh api` in scrittura,
email o messaggi a terzi, cancellazione di branch o worktree che non hai creato tu. Gli agenti non fanno
mai push su `main` o `deploy`. Creare `deploy` o cambiare impostazioni di Pages, ruleset ed environment
spetta a una persona del team, o si fa sotto la sua supervisione esplicita.

## Contenuti: niente invenzioni, placeholder onesti

1. **Non inventare nulla** (nomi, date, numeri, citazioni, affiliazioni, titoli, email, link): un fatto che
   non è nel repository e non viene dall'utente non esiste.
2. **Niente testo "verosimile"** per riempire: niente frasi promozionali, superlativi, battute, emoji
   decorative. Tono sobrio, frasi brevi.
3. Quando manca qualcosa usa solo questi tre placeholder: si riconoscono a colpo d'occhio e
   `scripts/check.sh` li conta. Nessun'altra stringa segnaposto ("coming soon", "to be added", ...).

| Cosa manca | Tipo | Markup oggi (HTML statico) |
| --- | --- | --- |
| Testo che deve scrivere il team | `lorem` | `<p data-placeholder="lorem">Lorem ipsum…</p>` (l'etichetta "Placeholder text · " la aggiunge il CSS) |
| Dato puntuale (data, sede, speaker) | `tba` | `<span data-placeholder="tba">Dates TBA</span>` |
| Funzionalità non sviluppata (form, iscrizione, social, mappa) | `unbuilt` | `<div data-placeholder="unbuilt" role="note"><strong>Not developed yet:</strong> mailing list.</div>` |

Dopo lo scaffold del generatore i placeholder si scrivono solo con l'include `placeholder` (tipo, testo),
che genera anche l'etichetta visibile: niente markup scritto a mano.

- Sempre `TBA`, mai `TBD`. Lorem ipsum solo per la prosa, mai per nomi o impegni concreti (costi,
  coperture, scadenze): lì `TBA`.
- **Metadati** (meta description, `og:*`, JSON-LD, `alt`): solo testo del team o fatti del repository, mai
  lorem né testo scritto da te; se manca, ometti il tag (`alt=""` solo per immagini decorative).
- Email, URL o handle d'esempio solo su domini riservati (`example.org`, `.invalid`).
- Mai bottoni, form o link finti, nemmeno disabilitati (`href="#"`, `javascript:`, form senza `action`,
  icone social senza account). Uno stato reale ("Registration not open yet") è testo normale.
- Sezioni che non hanno senso senza dati reali (keynote, partner, FAQ, topics) restano **nascoste**.
- Contenuto esistente dubbio: non toccarlo, aggiungi `<!-- TODO(team): verificare ... -->` e segnalalo nella PR.
- Niente dati personali (telefoni, indirizzi privati, email personali); persone solo con consenso del team.
- Loghi e diciture di finanziamento già presenti (es. banner EFC di Lucca 2025) sono obbligatori: non toccarli.

## Codice

- HTML semantico, un solo `h1` per pagina, navigazione nell'HTML (non iniettata da JavaScript).
- Niente stili inline, `<style>` per pagina o `!important` nuovi: colori, font, spaziature, raggi e
  ombre solo con le custom properties del design system.
- Componenti riusabili (layout, include) invece di markup copiato; ogni fatto ripetuto (date, stato di
  un'edizione, contatti) in un solo file di dati.
- JavaScript solo come miglioramento progressivo; librerie, font o servizi esterni nuovi solo se approvati.
- WCAG 2.2 AA (contrasto, focus visibile, tastiera). Nessuno scroll orizzontale a 320px; verifica a 375,
  768 e 1280px. Immagini in kebab-case, dimensionate per l'uso, con `width`/`height`.
- Con il generatore: `npm run build` → `_site/` (l'unica cosa pubblicata), `npm run dev -- --port=N` per l'anteprima.

## Verifica prima di ogni PR

```bash
scripts/check.sh     # HTML, link, link e form finti, telefoni, CNAME, file interni; conta i placeholder. Exit 0 = OK
scripts/preview.sh   # server che non termina: avvialo in background e fermalo alla fine
```

Nel body della PR e nei log riporta di `check.sh` solo exit code e conteggi, mai le righe trovate.
Un errore preesistente fuori dallo scopo del task non si corregge: si segnala nella PR. Il body della PR
elenca cosa cambia, come verificarlo, i placeholder introdotti e le domande aperte per il team.

## Uso del browser

Chrome (headless o Claude in Chrome) si può usare, ma **prima** scrivi in una riga a cosa serve e quali
pagine aprirai; alla fine di' cosa hai fatto e chiudi schede e processi. Headless sempre con un profilo
temporaneo (`--user-data-dir`), mai con quello dell'utente. Nessun login, nessun sito esterno superfluo.

## Cosa non va mai nel repository

`.claude/settings.local.json`, `CLAUDE.local.md`, `.claude/worktrees/`, output di build (`_site/`),
dipendenze (`node_modules/`, `vendor/`), segreti o token, percorsi o configurazioni della macchina locale,
un file `CNAME` (il vecchio dominio IMT è gestito dal repository `frs-workshop-redirect`).
`.claude/` contiene solo regole condivise: agenti, skill, hook e permessi del progetto.

## Agenti e skill del progetto

- Agenti: `frontend-dev` (layout, CSS, build) e `content-editor` (testi, dati) lavorano in un worktree
  isolato; `qa-reviewer` è in sola lettura e riceve nel prompt il percorso assoluto del worktree.
- Skill: `start-task` (branch e worktree), `preview` (controlli e anteprima), `release` (PR `main` →
  `deploy`, solo su richiesta esplicita).
