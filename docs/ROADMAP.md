# Roadmap: ritorno su github.io, Parma 2026, restyling

Piano di 2-3 giorni di lavoro, scritto il 20 ottobre 2026 dopo l'audit (`docs/AUDIT.md`).
Le attività marcate **[team]** richiedono una persona del team; le altre sono svolte da agenti in
branch e worktree separati (regole in `CLAUDE.md`), con conferma umana per push, PR e impostazioni.

## Obiettivi

1. Sito servito da `https://fosteringresearchsynergies.github.io/` in HTTPS, pubblicato dal branch `deploy`.
2. Pagina dell'edizione 2026 a Parma, con placeholder onesti dove mancano i contenuti.
3. Contenuti puliti: via testi inventati, dati personali e informazioni scadute.
4. Codice e grafica rifatti: design system, componenti, ogni fatto in un solo file di dati.
5. Lavoro degli agenti ripetibile: branch per task, worktree, controlli automatici, release tramite PR.

## Decisioni da prendere (Giorno 0)

| # | Decisione | Raccomandazione | Alternativa |
| --- | --- | --- | --- |
| D1 | Generatore del sito | **Eleventy 3** (Nunjucks, dati in YAML), build e deploy con GitHub Actions | Jekyll nativo di GitHub Pages |
| D2 | Direzione visiva | **D3 "Motifs"** (`docs/DESIGN.md`) | D1 "Field Notes", D2 "Phase Space" |
| D3 | Dominio | canonico `fosteringresearchsynergies.github.io`; `frs-workshop.imtlucca.it` redirige lì | dominio IMT dismesso |
| D4 | Chi approva le release `main` → `deploy` | una persona del team con permessi di admin | due persone a turno |
| D5 | Lingua del sito | solo inglese | inglese e italiano (fuori dai 2-3 giorni) |

Perché Eleventy: si installa e gira in locale con Node, senza permessi di amministratore (Jekyll su
questa macchina richiede `sudo apt install ruby-dev` o l'accesso a Docker), ogni agente ha l'anteprima
nel proprio worktree e si pubblica solo l'output del build, quindi `CLAUDE.md`, `docs/` e `.claude/`
non finiscono mai online. Struttura dati e template restano gli stessi in entrambe le opzioni: se il
team preferisce Jekyll cambia solo il Giorno 1.

## Domande per il team

Bloccano i contenuti, non il lavoro tecnico: finché mancano, la pagina usa i placeholder.

1. **Parma 2026**: date, ente ospitante, sede (edificio, sala, indirizzo), nome e numerazione ufficiale
   ("FRS 2026", "v4.0", "4th edition"? v1.X Vienna conta?).
2. **Call e iscrizione**: la call è già uscita? Scadenze (abstract, notifica, iscrizione) e link esterni
   (Google Form o altro).
3. **Costi e fondi**: partecipazione gratuita? Cosa è coperto (alloggio, pasti, cena sociale, viaggio)?
   Chi finanzia Parma, e ci sono loghi o diciture obbligatorie?
4. **Programma e keynote**: speaker confermati (nome, affiliazione, titolo) o "program not yet available"?
5. **Organizzatori**: chi è nel comitato di Parma e nel team FRS, con consenso a essere elencati?
6. **Edizioni passate**: anno, sede e contenuti di v1.0 Lucca e v1.X Vienna. Pagine d'archivio o solo
   voci nella timeline?
7. **Roma 2024**: quali testi di `events/frs2024-winter.html` avete scritto voi? Si possono togliere
   battute, statistiche non verificate e il paragrafo "Museum Drama"?
8. **Dominio**: `frs-workshop.imtlucca.it` è stato stampato su materiali di Lucca 2025?
9. **Contatti**: `frscrefimt@gmail.com` resta l'unico contatto pubblico? Esistono account social o una
   mailing list reali?
10. **Foto**: consenso per la foto di gruppo e originale ad alta risoluzione? Foto con licenza di Parma
    o della sede?
11. **Workflow**: va bene modificare i contenuti via file YAML/Markdown dall'interfaccia web di GitHub
    (con controllo automatico sulla PR) invece che via HTML?

## Modello di pubblicazione

- `main`: integrazione. Si entra solo con PR; il controllo `check` (= `scripts/check.sh` in GitHub Actions)
  deve passare.
- `deploy`: ciò che è online. Si entra solo con una PR di release da `main` (skill `release`), con un merge
  commit, approvata da chi ha il ruolo D4.
- Pubblicazione: workflow `pages.yml` su push a `deploy` → build → upload di `_site/` → GitHub Pages.
  L'environment `github-pages` accetta deploy solo da `deploy`.
- Rollback: rimettere Pages in modalità "Deploy from branch" (`main`, root), oppure fare revert del merge
  su `deploy` con una nuova PR.

## Giorno 0 (mezza giornata): decisioni, urgenze, migrazione

1. **[team]** Decisioni D1-D5 e, se possibile, risposte alle domande 1-3.
2. Merge di questa PR (`chore/agentic-setup`): regole per gli agenti, hook, script, documenti.
   Il file `_config.yml` impedisce che il build attuale pubblichi `CLAUDE.md`, `docs/` e `scripts/`.
3. **Hotfix urgenti** (`fix/urgent-content`, `content-editor`), rilasciati subito:
   - via il numero di telefono personale da `events/frs2024-winter.html`;
   - via le email `@phdnetwork.org` (dominio reale di terzi), il form di contatto e il box "Subscribe"
     finti da `contact.html`; al loro posto un link `mailto:` al contatto reale e un box `unbuilt`;
   - eliminare `events/winter-2024.html` (evento inventato) ed `events/event-template.html`;
   - Lucca 2025 non più "Upcoming";
   - recuperare dal branch `mfessina-patch-1` i titoli dei keynote di Lucca 2025 mancanti in `main`.
4. **Migrazione della pubblicazione** (agente con conferma dell'utente per ogni passo):
   1. **[team]** email all'IT di IMT Lucca: il record DNS `frs-workshop.imtlucca.it` punta a un host
      sbagliato; chiedere di farlo puntare a `fosteringresearchsynergies.github.io.` (così il vecchio
      indirizzo può redirigere in HTTPS) oppure di rimuoverlo.
   2. Il dominio IMT non viene lasciato libero: passa a un piccolo repository di redirect
      nell'organizzazione, che manda ogni vecchio URL su github.io.
   3. Push di `deploy`, environment `github-pages` aperto a `deploy`, Pages in modalità "Deploy from
      branch" su `deploy` (root) finché il generatore non è pronto, senza dominio custom, HTTPS obbligatorio.
   4. Regole del repository: PR obbligatoria su `main` e `deploy`, niente force push né cancellazione,
      cancellazione automatica dei branch dopo il merge.
   5. Verifica: `https://fosteringresearchsynergies.github.io/` risponde 200 con HTTPS, i vecchi URL
      redirigono.

## Giorno 1: fondamenta (3 worktree in parallelo, file separati)

| Branch | Agente | Contenuto | File toccati |
| --- | --- | --- | --- |
| `feat/scaffold` | frontend-dev | Eleventy 3, layout `base`/`page`/`edition`, include `head`/`nav`/`footer`/`placeholder`, `npm run build`/`dev`, workflow `check.yml` e `pages.yml` (inattivo fino al Giorno 3), porting delle pagine attuali senza cambiare i testi | `package.json`, `eleventy.config.js`, `src/_includes/`, `.github/workflows/` |
| `design/tokens` | frontend-dev | design system D3: token, base, componenti (card, timeline, programma, banda fondi, placeholder), font ospitati nel sito, set minimo di icone a motivi in SVG | `src/assets/css/`, `src/assets/fonts/`, `src/assets/icons/` |
| `content/data` | content-editor | dati estratti dalle pagine attuali: `site.yml`, `editions.yml` (Parma con campi `null` = TBA), `programs/2024-rome.yml`, `programs/2025-lucca.yml`; elenco dei testi da tenere, eliminare o verificare | `src/_data/` |

Ordine dei merge: `feat/scaffold`, poi `design/tokens` e `content/data` (adattati alla struttura).
Verifica: `scripts/check.sh` passa sul sito portato, nessuna differenza di contenuto visibile.

## Giorno 2: pagine (3 worktree in parallelo)

| Branch | Agente | Contenuto |
| --- | --- | --- |
| `content/parma-2026` | frontend-dev + content-editor | layout `edition` completo e pagina `/editions/2026-parma/`: hero, stato, date chiave, about (lorem), call e iscrizione (TBA o `unbuilt`), programma "not yet available", sede, alloggio, contatti; sezioni senza dati nascoste |
| `feat/archive` | frontend-dev | `/editions/` (timeline e schede), Roma 2024 e Lucca 2025 dai dati, stub per v1.0 e v1.X, redirect dai vecchi URL (`/events.html`, `/events/lucca.html`, `/events/frs2024-winter.html`) |
| `feat/core-pages` | frontend-dev | home (prossima edizione, cos'è FRS, timeline, foto di gruppo), about, contact (solo contatto reale), 404, favicon, meta description e Open Graph |

Ognuno con revisione `qa-reviewer` prima della PR. Le modifiche ai layout condivisi passano da un solo branch per volta.

## Giorno 3: QA, release, verifica

1. `qa-reviewer` su tutto il sito: accessibilità, resa a 320/375/768/1280px, contenuti, link.
   Correzioni in branch `fix/qa-<slug>`.
2. Immagine Open Graph per Parma, `sitemap.xml`, `robots.txt`.
3. **[team]** Revisione dei placeholder rimasti (report di `scripts/check.sh`) e risposte alle domande aperte.
4. Release (skill `release`): Pages passa a "GitHub Actions" **prima** del merge della PR di release su
   `deploy`; poi merge, verifica del deploy e dei redirect.
5. README aggiornato con la guida per modificare i contenuti dall'interfaccia web.

## Definizione di "fatto"

- Il sito live è su github.io in HTTPS e viene da `deploy`; i vecchi URL redirigono.
- Nessun testo inventato, nessun dato personale, nessun form o link finto; ogni contenuto mancante è un
  placeholder visibile e contato da `scripts/check.sh`.
- `scripts/check.sh` passa; nessuno scroll orizzontale a 320px; contrasti AA.
- Ogni edizione, data e contatto sta in un solo file di dati.
- `.claude/` contiene solo regole condivise; niente file locali nel repository.

## Rischi

| Rischio | Mitigazione |
| --- | --- |
| L'IT di IMT non risponde in tempo | il repository di redirect copre il vecchio dominio; HTTPS su quel dominio arriva quando il DNS è corretto |
| Dati di Parma non disponibili | la pagina esce con placeholder; i dati si aggiungono dopo con una modifica a `editions.yml` |
| Conflitti tra agenti in parallelo | file separati per branch, layout condivisi in sequenza, ordine dei merge fissato sopra |
| Il build fallisce dopo una modifica dal web | controllo `check` obbligatorio sulle PR; `deploy` riceve solo PR di release |
| Il deploy da Actions fallisce al primo giro | rollback a "Deploy from branch" (vedi sopra) |
