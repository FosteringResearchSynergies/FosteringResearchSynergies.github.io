# Roadmap: ritorno su github.io, Parma 2026, restyling

Piano di 2-3 giorni di lavoro, scritto il 20 ottobre 2026 dopo l'audit (`docs/AUDIT.md`) e aggiornato
lo stesso giorno, a Giorno 0 eseguito. Le attività marcate **[team]** richiedono una persona del team;
le altre le svolgono agenti in branch e worktree separati (regole in `CLAUDE.md`), che chiedono conferma
all'utente prima di ogni push e di ogni PR.

## Obiettivi

1. Sito servito da `https://fosteringresearchsynergies.github.io/` in HTTPS, pubblicato dal branch
   `deploy` (raggiunto il 20 ottobre, con il sito attuale).
2. Pagina dell'edizione 2026 a Parma, con placeholder onesti dove mancano i contenuti.
3. Contenuti puliti: via testi inventati, dati personali e informazioni scadute.
4. Codice e grafica rifatti: design system, componenti, ogni fatto in un solo file di dati.
5. Lavoro degli agenti ripetibile: branch per task, worktree, controlli automatici, release tramite PR.

## Decisioni

| # | Decisione | Raccomandazione | Alternativa |
| --- | --- | --- | --- |
| D1 | Generatore del sito | **Eleventy 3** (Nunjucks, dati in YAML), build e pubblicazione con GitHub Actions | Jekyll (build di GitHub Pages dal branch, oppure in Actions) |
| D2 | Direzione visiva | **D3 "Motifs"** (`docs/DESIGN.md`) | D1 "Field Notes", D2 "Phase Space" |
| D3 | Dominio | **in atto**: canonico `fosteringresearchsynergies.github.io`; `frs-workshop.imtlucca.it` redirige lì dal repository `frs-workshop-redirect` | dominio IMT dismesso |
| D4 | Chi approva le release `main` → `deploy` | una persona del team diversa da chi apre la PR | due persone a turno |
| D5 | Lingua del sito | solo inglese | inglese e italiano (fuori dai 2-3 giorni) |

Perché Eleventy: Jekyll in locale richiede Ruby con gli header di sviluppo; Eleventy solo Node. Ogni
agente ha quindi l'anteprima nel proprio worktree, e online va solo l'output del build: `CLAUDE.md`,
`docs/` e `.claude/` non vengono mai pubblicati. Con Jekyll cambiano i Giorni 1 e 3 (template Liquid,
cartelle `_layouts/`, `_includes/` e `_data/` alla radice, pubblicazione dal branch con `exclude` in
`_config.yml` oppure build Jekyll in Actions) e i comandi in `CLAUDE.md`; con Eleventy i dati YAML
richiedono `addDataExtension` e un pacchetto YAML.

## Domande per il team

Bloccano i contenuti, non il lavoro tecnico: finché mancano, la pagina usa i placeholder.

1. **Parma 2026**: date, ente ospitante, sede (edificio, sala, indirizzo), nome e numerazione ufficiale
   ("FRS 2026", "v4.0", "4th edition"? v1.X Vienna conta?).
2. **Call e iscrizione**: la call è già uscita? Scadenze (abstract, notifica, iscrizione) e link esterni
   (Google Form o altro).
3. **Costi e fondi**: partecipazione gratuita? Cosa è coperto (alloggio, pasti, cena sociale, viaggio)?
   Chi finanzia Parma, e ci sono loghi o diciture obbligatorie?
4. **Programma e keynote**: speaker confermati (nome, affiliazione, titolo), oppure "Program: TBA"?
5. **Organizzatori**: chi è nel comitato di Parma e nel team FRS, con consenso a essere elencati?
6. **Edizioni passate**: anno, sede e contenuti di v1.0 Lucca e v1.X Vienna. Pagine d'archivio o solo
   voci nella timeline?
7. **Roma 2024**: quali testi di `events/frs2024-winter.html` avete scritto voi? Si possono togliere
   battute, statistiche non verificate e aneddoti?
8. **Dominio**: `frs-workshop.imtlucca.it` è stato stampato su materiali di Lucca 2025?
9. **Contatti**: `frscrefimt@gmail.com` resta l'unico contatto pubblico? Esistono account social o una
   mailing list reali?
10. **Foto**: consenso per la foto di gruppo e originale ad alta risoluzione? Foto con licenza di Parma
    o della sede?
11. **Workflow**: va bene modificare i contenuti via file YAML/Markdown dall'interfaccia web di GitHub
    (con controllo automatico sulla PR) invece che via HTML?
12. **Keynote di Lucca 2025**: in `main` compaiono solo i nomi; il branch `mfessina-patch-1` contiene
    anche i titoli dei talk. Vanno aggiunti, o sono stati tolti di proposito?

## Modello di pubblicazione

- `main`: integrazione. Si entra solo con PR, che devono passare il controllo `check` (=
  `scripts/check.sh` in GitHub Actions, test web e mobile compresi; workflow `check.yml`).
- `deploy`: ciò che è online. Si entra solo con una PR di release da `main` (skill `release`), o con una
  PR di revert per il rollback, unita con un merge commit (mai squash o rebase) e approvata da chi ha il
  ruolo D4. Dopo ogni release
  `git merge-base --is-ancestor origin/main origin/deploy` deve riuscire.
- **Test prima di pubblicare** (regola del team): niente va online se i test locali, web e mobile
  (`scripts/check.sh`: HTML, link, Chrome headless a 320, 375, 768 e 1280px), non sono passati sul
  commit che si pubblica e se nessuno ha guardato gli screenshot. Vale per PR e merge verso `deploy`,
  cambi di Pages, build e deploy. Per gli agenti lo impone l'hook (registro dei commit testati scritto
  da `check.sh`), per tutti il controllo `check` sulle PR verso `deploy`.
- Le modifiche unite in `main` non vanno online da sole: serve una release `main` → `deploy`.
- Pubblicazione oggi: Pages in modalità "Deploy from branch" su `deploy` (root), con il build Jekyll di
  GitHub; `_config.yml` esclude i file interni. Dal Giorno 3: workflow `pages.yml` su push a `deploy`
  → build → upload di `_site/` → Pages (`build_type` = `workflow`).
- **Freeze delle release**: l'hotfix del Giorno 0 è l'ultima release prevista del sito attuale. Fino al
  merge di `feat/scaffold` una correzione urgente può ancora uscire con la skill `release`; da quel
  merge al Giorno 3 (passo 5) nessuna release, perché il build Jekyll di `deploy` pubblicherebbe i
  sorgenti di Eleventy. La skill `release` controlla `build_type` e si ferma se non è `workflow`.
- Gli agenti non fanno mai push su `main` o `deploy` e chiedono conferma prima di ogni push e di ogni
  PR: un'autorizzazione precedente non vale per la successiva. Creare `deploy`, cambiare le
  impostazioni di Pages, i ruleset o gli environment è un passo **[team]** (o di un agente sotto
  supervisione esplicita).
- Dominio: `frs-workshop.imtlucca.it` appartiene a `frs-workshop-redirect` e in questo repository non
  torna mai (né file `CNAME` né impostazione di Pages); `scripts/check.sh` fallisce se trova un `CNAME`
  nel sito pubblicato. Finché il record DNS punta a GitHub, il repository di redirect non va cancellato
  e il suo Pages non va spento.
- Rollback:
  - oggi (Pages da `deploy`, root): PR di revert del merge di release su `deploy`;
  - con Actions: se il deploy fallisce resta online la versione precedente e non c'è nulla da fare (la
    correzione va su `main`); se il deploy riesce ma il sito è sbagliato, `gh run rerun <id>` dell'ultimo
    run riuscito di `pages.yml`, oppure PR di revert su `deploy`;
  - la PR di revert parte da `origin/deploy` su un branch `fix/revert-<slug>` (skill `release`,
    rollback) ed è approvata come una release;
  - mai rimettere Pages su `main` (root), mai riaggiungere il dominio custom a questo repository;
  - dopo un revert su `deploy` i commit annullati non tornano da soli: la release successiva si ferma
    (skill `release`) e decide il team.

## Giorno 0: urgenze e migrazione (eseguito il 20 ottobre 2026)

Fatto:

- Hotfix `fix/urgent-content` (PR #4): via il numero di telefono personale dalla pagina di Roma 2024;
  via le email `@phdnetwork.org`, il form di contatto e i box finti di `contact.html`, sostituiti da un
  link `mailto:` a `frscrefimt@gmail.com` e da box `unbuilt`; eliminate la pagina dell'evento inventato
  e il template; Lucca 2025 tra le edizioni passate; Parma 2026 come prossima edizione, con
  placeholder; via il file `CNAME`.
- Nuovo repository pubblico `FosteringResearchSynergies/frs-workshop-redirect`: tiene il dominio
  `frs-workshop.imtlucca.it` e manda ogni percorso su github.io. Il certificato HTTPS per il vecchio
  dominio è già emesso (scade a gennaio 2027 e GitHub lo rinnova da solo).
- Branch `deploy` creato dall'hotfix (`388acb1`); Pages in modalità "Deploy from branch" su `deploy`
  (root), senza dominio custom, con HTTPS obbligatorio. HTTPS obbligatorio attivo anche su
  `frs-workshop-redirect`.
- Verifica: `https://fosteringresearchsynergies.github.io/` risponde 200 in HTTPS.

Ancora aperto, tutto **[team]**:

1. Decisioni D1, D2, D4 e D5 e, se possibile, risposte alle domande 1-3.
2. Merge della PR #4 (`fix/urgent-content` → `main`) con un merge commit, così `main` contiene `deploy`
   (`git merge-base --is-ancestor origin/deploy origin/main` deve riuscire).
3. Facoltativo, protezione in più: email all'IT di IMT (bozza pronta, non inviata). Finché esiste il
   repository di redirect nessuno può prendersi il dominio; la verifica lo protegge anche se quel
   repository sparisse. Due richieste: il CNAME di
   `frs-workshop.imtlucca.it` deve puntare a `fosteringresearchsynergies.github.io.` (oggi punta a
   `frs-workshop.github.io.`, che funziona ancora ma va sostituito); un record TXT
   `_github-pages-challenge-FosteringResearchSynergies.frs-workshop.imtlucca.it` con il valore che
   GitHub mostra nelle impostazioni dell'organizzazione (Pages → Add a domain). A DNS aggiornato:
   "Verify" nelle impostazioni dell'organizzazione (impedisce ad altri account GitHub di prendersi il
   dominio).
4. Merge di questa PR (`chore/agentic-setup`, dopo la #4): regole per gli agenti, hook, script,
   test web e mobile, workflow `check.yml`, documenti. Poi, su ogni macchina che usa Claude Code, `git -C <checkout principale> pull --ff-only`
   e riavvio di Claude Code dalla radice del checkout principale: impostazioni e hook si leggono da lì
   all'avvio. Servono `python3` e Chrome o Chromium. Lo stesso vale dopo ogni merge che cambia `.claude/`.
5. Ruleset del repository e cancellazione automatica dei branch dopo il merge (`delete_branch_on_merge`):
   - `main`: PR obbligatoria (approvazioni: 0, oppure 1 se due persone del team possono rivedere);
     niente force push né cancellazione; check `check` obbligatorio.
   - `deploy`: PR obbligatoria con 1 approvazione di una persona diversa dall'autore (le PR aperte da
     un agente risultano dell'utente che lo usa, quindi approva qualcun altro); merge consentito solo
     con merge commit; niente force push né cancellazione; check `check` obbligatorio; dal merge di
     `feat/scaffold`, anche `release-source`, un job di `check.yml` che sulle PR verso `deploy` fallisce se
     `github.head_ref` non è `main` (unica eccezione: i branch di rollback `fix/revert-<slug>`).
6. Dopo la prima release `main` → `deploy`: togliere `main` dalle regole dell'environment
   `github-pages`, che oggi accetta `deploy` e `main`.
7. Titoli dei keynote di Lucca 2025: domanda 12.

## Giorno 1: fondamenta

**Mattina, da solo: `feat/scaffold` (frontend-dev).**

- Eleventy 3 con estensione dati YAML (`addDataExtension` più un pacchetto YAML, per esempio `js-yaml`).
- Passthrough di `src/assets/` (servito come `/assets/`) e dei file statici attuali.
- Layout `base` e `page`; include `head` (collega `/assets/css/main.css`), `nav`, `footer` e
  `placeholder` (parametri: tipo e testo; stampa l'etichetta visibile). Da qui in poi i placeholder si
  scrivono solo con questo include.
- File di ingresso vuoti: `src/assets/css/main.css`, `src/_data/site.yml`.
- Schema dei dati: `src/_data/editions.yml` e `src/_data/programs/` con le chiavi e una voce d'esempio
  commentata (le chiavi le decide frontend-dev, i valori li inserisce content-editor).
- `npm run build` cancella `_site/` e poi esegue Eleventy; `npm run dev -- --port=N` per l'anteprima,
  con `setServerOptions({ portReassignmentRetryCount: 0 })` così una porta occupata dà errore invece di
  cambiare porta in silenzio.
- `html-validate` e `linkinator` come devDependencies, bloccati da `package-lock.json` alle versioni già
  fissate in `scripts/check.sh`, che da quel momento li chiama con `npx --no-install`.
- In `check.yml` (già presente con il job `check`): `npm ci` prima di `scripts/check.sh` e il nuovo
  job `release-source`. Workflow `pages.yml` (inattivo fino al Giorno 3).
- Porting delle pagine attuali in `src/` senza cambiare testi né URL.

File toccati: `package.json`, `package-lock.json`, `eleventy.config.js`, `.gitignore`, `src/`,
`scripts/check.sh`, `.github/workflows/`.

**Pomeriggio, in parallelo, entrambi da `origin/feat/scaffold`** (task dipendente, skill `start-task`):

| Branch | Agente | Contenuto | File toccati |
| --- | --- | --- | --- |
| `design/tokens` | frontend-dev | design system D3: token, base, componenti (card, timeline, programma, banda fondi, placeholder), font ospitati nel sito, set minimo di icone a motivi in SVG; `main.css` importa anche i file vuoti `edition.css`, `archive.css` e `pages.css` per il Giorno 2 | `src/assets/css/`, `src/assets/fonts/`, `src/assets/icons/` |
| `content/data` | content-editor | solo valori, con le chiavi definite da `feat/scaffold`; dati estratti dalle pagine attuali: `site.yml`, `editions.yml` (tutte le edizioni, compresi v1.0 Lucca e v1.X Vienna; campi sconosciuti `null` = TBA), `programs/2024-rome.yml`, `programs/2025-lucca.yml`; elenco dei testi da tenere, eliminare o verificare | `src/_data/` |

Ordine dei merge: `feat/scaffold`, poi `design/tokens` e `content/data`. Dal merge di `feat/scaffold`
parte il freeze delle release e **[team]** aggiunge il check obbligatorio `release-source` su
`deploy`. Verifica: `scripts/check.sh` passa sul sito portato, nessuna differenza
di contenuto visibile.

## Giorno 2: pagine

**Mattina, da solo: `design/edition-layout` (frontend-dev).** Layout `edition` completo (hero, stato,
date chiave, about, call e iscrizione, programma, sede, alloggio, contatti; sezioni senza dati
nascoste, contenuti mancanti tramite l'include `placeholder`); include condivisi per le edizioni
(scheda e timeline); `head` con meta description, Open Graph e favicon presi dai dati della pagina e
omessi quando mancano; voce "Editions" e prossima edizione nella `nav`.
File toccati: `src/_includes/` (layout `edition`, `head`, `nav`, include delle edizioni),
`src/assets/css/edition.css`.

**Poi, in parallelo, tutti da `origin/design/edition-layout`** dopo il commit del layout:

| Branch | Agente | Contenuto | File toccati |
| --- | --- | --- | --- |
| `content/parma-2026` | content-editor | voce di Parma in `editions.yml` e pagina `/editions/2026-parma/` con il layout `edition`: about in lorem, call e iscrizione TBA o `unbuilt`, programma "Program: TBA" (`tba`, tramite l'include `placeholder`) | `src/_data/editions.yml`, `src/editions/2026-parma.md` |
| `feat/archive` | frontend-dev | `/editions/` (timeline e schede), Roma 2024 e Lucca 2025 dai dati, stub per v1.0 e v1.X, redirect dai vecchi URL (`/events.html`, `/events/lucca.html`, `/events/frs2024-winter.html`) | `src/editions/` (tranne `2026-parma.md`), vecchie pagine `src/events*` sostituite dai redirect, `src/assets/css/archive.css` |
| `feat/core-pages` | frontend-dev | home (prossima edizione, cos'è FRS, timeline, foto di gruppo), about, contact (solo contatto reale), 404, favicon, meta description e Open Graph nel front matter (solo testi reali, altrimenti niente tag) | `src/index.*`, `src/about.*`, `src/contact.*`, `src/404.*`, file della favicon, `src/assets/css/pages.css` |

Proprietari unici: il layout `edition` e gli include `head` e `nav` li modifica solo
`design/edition-layout` (dopo il suo merge, un task dedicato); `editions.yml` ha un solo branch per
volta (Giorno 1 `content/data`, Giorno 2 `content/parma-2026`), gli altri lo leggono e chiedono le
modifiche nella PR. Ordine dei merge: `design/edition-layout`, poi gli altri tre in qualsiasi ordine.
Ogni branch passa da `qa-reviewer` prima della PR.

## Giorno 3: QA, release, verifica

1. `qa-reviewer` su tutto il sito: accessibilità, resa a 320/375/768/1280px, contenuti, link.
   Correzioni in branch `fix/qa-<slug>`.
2. Immagine Open Graph per Parma, `sitemap.xml`, `robots.txt`.
3. `chore/strict-html`: le regole di `.htmlvalidate.json` messe a `warn` per l'HTML attuale tornano a
   `error`; `scripts/check.sh` deve passare su `origin/main`.
4. **[team]** Revisione dei placeholder rimasti (report di `scripts/check.sh`) e risposte alle domande
   aperte.
5. Release (skill `release`), primo deploy con Actions:
   1. **[team]** Pages passa a "GitHub Actions" **prima** di aprire la release (Settings → Pages,
      oppure `gh api -X PUT repos/FosteringResearchSynergies/FosteringResearchSynergies.github.io/pages -f build_type=workflow`).
      Resta online la versione attuale: `deploy` non ha ancora `pages.yml`, quindi nulla viene
      ripubblicato fino al merge.
   2. Test web e mobile (`scripts/check.sh`) passati su `origin/main` e screenshot rivisti (skill
      `release`, punto 3); PR di release `main` → `deploy` aperta, con `check` verde, e approvata.
   3. Merge con merge commit; finisce il freeze.
   4. Verifica: il run di `pages.yml` per lo sha del merge (`gh run list --branch deploy --commit <sha>`,
      poi `gh run watch <id> --exit-status`); `curl -sI https://fosteringresearchsynergies.github.io/`
      risponde `HTTP/2 200`; i vecchi URL redirigono; `git merge-base --is-ancestor origin/main origin/deploy`
      riesce.
   5. **[team]** Se non è già stato fatto, togliere `main` dall'environment `github-pages`.
   6. Rollback come nel modello di pubblicazione. Solo in questo primo passaggio non c'è un run
      precedente di `pages.yml` da rilanciare: se il sito pubblicato è sbagliato, PR di revert su
      `deploy` e **[team]** ritorno di Pages a "Deploy from branch" su `deploy` (root).
6. README aggiornato con la guida per modificare i contenuti dall'interfaccia web.

## Definizione di "fatto"

- Il sito live è su github.io in HTTPS e viene da `deploy` tramite `pages.yml`; i vecchi URL redirigono.
- Nessun testo inventato, nessun dato personale, nessun form o link finto; ogni contenuto mancante è un
  placeholder visibile e contato da `scripts/check.sh`.
- `scripts/check.sh` passa con tutte le regole HTML a `error`, test web e mobile compresi (nessuno
  scroll orizzontale a 320px); contrasti AA.
- Ogni edizione, data e contatto sta in un solo file di dati.
- Ruleset attivi su `main` e `deploy`; dominio IMT verificato nell'organizzazione.
- `.claude/` contiene solo regole condivise; niente file locali nel repository.

## Rischi

| Rischio | Mitigazione |
| --- | --- |
| L'IT di IMT non risponde in tempo | il repository di redirect tiene il dominio (anche in HTTPS) e non va mai cancellato; senza il record TXT il dominio non è verificato nell'organizzazione, quindi il redirect va tenuto attivo |
| Dati di Parma non disponibili | la pagina esce con placeholder; i dati si aggiungono dopo con una modifica a `editions.yml` |
| Conflitti tra agenti in parallelo | ogni giorno un branch al mattino crea i file condivisi, poi branch paralleli su file separati; proprietario unico per layout, include e `editions.yml` |
| Release durante il passaggio a Eleventy | freeze dal merge di `feat/scaffold` al Giorno 3; la skill `release` controlla `build_type` |
| Sessione con hook o impostazioni vecchi | `pull --ff-only` del checkout principale e riavvio di Claude Code dopo ogni merge che cambia `.claude/`; se il file dell'hook manca, i comandi vengono bloccati |
| Il build fallisce dopo una modifica dal web | controllo `check` obbligatorio sulle PR; `deploy` riceve solo PR di release |
| Il primo deploy da Actions fallisce | resta online la versione precedente; correzione su `main` e nuova release |
| Un deploy riuscito pubblica un sito sbagliato | `gh run rerun` dell'ultimo run riuscito di `pages.yml`, oppure PR di revert su `deploy`; al primo passaggio, revert e ritorno a "Deploy from branch" su `deploy` (root) |
