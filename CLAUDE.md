# Fostering Research Synergies: regole per gli agenti

Sito statico del workshop **Fostering Research Synergies (FRS)**, organizzato da dottorandi e postdoc
che lavorano su sistemi complessi (CREF Roma, IMT Lucca, CSH Vienna). Pubblicato con GitHub Pages su
`https://fosteringresearchsynergies.github.io/`. Il sito è in **inglese**; documentazione, istruzioni
per gli agenti e comunicazioni con il team sono in **italiano**.

Contesto: `docs/ROADMAP.md` (piano e decisioni), `docs/AUDIT.md` (inventario dei problemi),
`docs/DESIGN.md` (direzione visiva e struttura delle pagine).

## Branch e worktree

| Branch | Ruolo | Come ci si arriva |
| --- | --- | --- |
| `main` | integrazione, sempre funzionante | solo PR da branch di task |
| `deploy` | ciò che è online (sorgente di GitHub Pages) | solo PR di release `main` → `deploy` (skill `release`) |
| `<tipo>/<slug>` | un task | worktree in `.claude/worktrees/<slug>` (skill `start-task`) |

- Un task = un branch = un worktree. Mai modificare file nel checkout principale, né su `main` o `deploy`.
  L'hook `.claude/hooks/guard_protected_branches.py` blocca edit, commit e push diretti su quei branch.
  Non aggirarlo con `sed -i`, redirect della shell o `FRS_ALLOW_PROTECTED` (quella variabile è riservata agli umani).
- Tipi di branch: `feat`, `fix`, `content`, `design`, `chore`, `docs`.
- Agenti in parallelo toccano file diversi. File condivisi (CSS globale, layout, dati comuni) vanno
  modificati da un task alla volta, oppure un task parte dal branch dell'altro.
- Commit piccoli, messaggi in inglese all'imperativo (`Add Parma 2026 key dates`).

## Azioni che richiedono conferma esplicita dell'utente

Push, apertura o merge di PR, commenti su GitHub, `gh api` in scrittura, modifiche alle impostazioni del
repository o di GitHub Pages, email o messaggi a terzi, cancellazione di branch, worktree o stash che non
hai creato tu. Anche se l'utente ha già approvato un'azione simile, l'approvazione non vale per la successiva.

## Contenuti: niente invenzioni, placeholder onesti

1. **Non inventare nulla**: nomi, date, numeri, citazioni, testimonianze, affiliazioni, titoli di talk,
   indirizzi email, link. Un fatto che non è nel repository e non viene dall'utente non esiste.
2. **Niente testo "verosimile"** scritto per riempire: niente frasi promozionali generiche, superlativi,
   battute, emoji decorative. Tono sobrio, frasi brevi.
3. Quando manca qualcosa, usa i placeholder qui sotto. Devono essere riconoscibili a colpo d'occhio
   (lo stile è nel design system) e contabili da `scripts/check.sh`.

| Cosa manca | Markup | Esempio |
| --- | --- | --- |
| Testo che deve scrivere il team | `data-placeholder="lorem"` | `<p data-placeholder="lorem">Lorem ipsum dolor sit amet…</p>` |
| Dato puntuale (data, sede, speaker) | `data-placeholder="tba"` | `<span data-placeholder="tba">TBA</span>` |
| Funzionalità non sviluppata (form, iscrizione, newsletter, social, mappa) | `data-placeholder="unbuilt"` | `<div data-placeholder="unbuilt" role="note"><strong>Not developed yet:</strong> registration form</div>` |

- Lorem ipsum solo per prosa. Mai per impegni concreti (costi, coperture, scadenze): lì `TBA`.
- Email, URL o handle d'esempio solo su domini riservati (`example.org`, `.invalid`), mai su domini reali.
- Mai bottoni, form o link finti che sembrano funzionare (`href="#"`, form senza `action`, icone social senza account).
- Sezioni che non hanno senso senza dati reali (keynote, partner, FAQ, topics) restano **nascoste**,
  non riempite.
- Contenuto esistente dubbio (forse vero, forse inventato): non toccarlo, aggiungi
  `<!-- TODO(team): verificare ... -->` e riportalo nelle domande aperte della PR.
- Dati personali: niente numeri di telefono, indirizzi privati o email personali. Persone elencate solo
  con consenso confermato dal team.
- Loghi e diciture di finanziamento (es. banner EFC/NextGenerationEU sulla pagina di Lucca 2025) sono
  obbligatori dove già presenti: non rimuoverli né alterarli.

## Codice

- HTML semantico (`header`, `nav`, `main`, `section`, `footer`), un solo `h1` per pagina, navigazione
  presente nell'HTML (non iniettata da JavaScript).
- Niente stili inline, niente `<style>` per pagina, niente `!important` nuovi. Colori, font, spaziature,
  raggi e ombre solo tramite le custom properties del design system.
- Componenti riusabili (layout, include, partial) invece di markup copiato tra pagine. Fatti ripetuti
  (date, stato di un'edizione, email di contatto) in un solo posto (file di dati).
- JavaScript solo dove serve davvero e come miglioramento progressivo: senza JS il contenuto si legge.
  Nessuna libreria, font o servizio esterno nuovo senza approvazione.
- Accessibilità WCAG 2.2 AA: contrasto, focus visibile, uso da tastiera, `alt` significativi.
- Mobile first: nessuno scroll orizzontale a 320px; verifica a 375, 768 e 1280px.
- Immagini: nomi in kebab-case senza spazi, dimensioni adeguate all'uso, `width`/`height` espliciti.
- Con un generatore (vedi ROADMAP): `npm run build` produce `_site/`, `npm run dev -- --port=N` avvia
  l'anteprima. Si pubblica solo l'output del build.

## Verifica prima di ogni PR

```bash
scripts/check.sh     # HTML valido, link interni, niente href="#", niente telefoni, conteggio placeholder
scripts/preview.sh   # anteprima locale; porta diversa per ogni worktree
```

Un errore preesistente fuori dallo scopo del task non si corregge: si segnala nella PR. Il body della PR
elenca cosa cambia, come verificarlo, i placeholder introdotti e le domande aperte per il team.

## Uso del browser

Chrome si può usare (headless da terminale o estensione Claude in Chrome), ma **prima** di aprirlo scrivi
in una riga a cosa serve e quali pagine o URL aprirai. Alla fine dici cosa hai fatto e chiudi schede e
processi aperti. Chrome headless sempre con un profilo temporaneo (`--user-data-dir` in una cartella
temporanea), mai con il profilo dell'utente. Nessun login, nessun sito esterno non necessario al task.

## Cosa non va mai nel repository

`.claude/settings.local.json`, `CLAUDE.local.md`, `.claude/worktrees/`, output di build (`_site/`),
dipendenze (`node_modules/`, `vendor/`), segreti o token, percorsi o configurazioni della macchina locale.
`.claude/` contiene solo regole condivise: agenti, skill, hook e permessi del progetto.

## Agenti e skill del progetto

- Agenti: `frontend-dev` (layout, CSS, componenti, build), `content-editor` (testi e dati, placeholder),
  `qa-reviewer` (sola lettura, verifica prima di PR e release).
- Skill: `start-task` (branch e worktree), `preview` (controlli e anteprima),
  `release` (PR `main` → `deploy`, solo su richiesta esplicita).
