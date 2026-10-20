# Fostering Research Synergies: sito web

Sito del workshop **Fostering Research Synergies (FRS)**, organizzato da dottorandi e postdoc che
lavorano su sistemi complessi (CREF Roma, IMT Lucca, CSH Vienna).

Sito: <https://fosteringresearchsynergies.github.io/> · Contatto: frscrefimt@gmail.com

> Il sito è in fase di rifacimento (ottobre 2026): pagina dell'edizione 2026 a Parma, nuova grafica,
> generatore di siti statici. Piano e stato in [`docs/ROADMAP.md`](docs/ROADMAP.md).

## Come è organizzato il repository

| Percorso | Contenuto |
| --- | --- |
| `src/` | sorgenti del sito per [Eleventy](https://www.11ty.dev/): pagine, layout e include (`src/_includes/`), dati (`src/_data/`), file statici; il build va in `_site/`, l'unica cosa pubblicata |
| `package.json`, `package-lock.json`, `eleventy.config.js` | generatore e strumenti di controllo, con le versioni bloccate |
| `docs/` | piano (`ROADMAP.md`), inventario dei problemi (`AUDIT.md`), direzione visiva (`DESIGN.md`) |
| `scripts/` | `check.sh` (controlli e test web e mobile prima di ogni PR e di ogni pubblicazione), `viewports.mjs` (i test in Chrome, usato da `check.sh`), `preview.sh` (anteprima locale) |
| `.github/workflows/` | `check.yml`: gli stessi controlli su ogni PR verso `main` e `deploy` |
| `CLAUDE.md`, `.claude/` | regole condivise per gli agenti di Claude Code: agenti, skill, hook, permessi |

I file interni (`README.md`, `CLAUDE.md`, `docs/`, `scripts/`, `.claude/`) non vengono pubblicati.

## Pubblicazione

- GitHub Pages pubblica il branch `deploy` su `https://fosteringresearchsynergies.github.io/`.
- Il vecchio indirizzo `frs-workshop.imtlucca.it` appartiene al repository
  [`frs-workshop-redirect`](https://github.com/FosteringResearchSynergies/frs-workshop-redirect), che
  rimanda ogni vecchio URL allo stesso percorso su github.io (con JavaScript disattivato, alla home),
  anche in HTTPS. Questo
  repository non ha più un file `CNAME` e non deve riaverlo.

## Branch

- `main`: integrazione. Si modifica solo tramite pull request.
- `deploy`: ciò che è online. Ci si arriva solo con una PR di release da `main` (o, per un rollback, con
  una PR di revert), unita con un merge commit (niente squash o rebase).
- Niente va online senza test: i test locali, web e mobile (`scripts/check.sh`), devono passare sul
  commit da pubblicare, e una PR verso `deploy` si unisce solo con il controllo `check` verde.
  Le modifiche unite in `main` non vanno online da sole: serve una release.
- Un branch per ogni modifica (`content/...`, `fix/...`, `feat/...`, `design/...`, `docs/...`, `chore/...`).

## Modificare il sito

1. Crea un branch (dall'interfaccia web: modifica il file e scegli "Create a new branch").
2. Apri una pull request verso `main` e descrivi cosa cambia.
3. Su ogni PR il controllo `check` esegue i test (HTML, link, resa su telefono, tablet e computer);
   gli screenshot di ogni pagina sono tra gli artifact della run.
4. Dopo il merge, chi gestisce le release apre la PR `main` → `deploy`.

Regole sui contenuti: niente informazioni inventate. Dove manca qualcosa si usa un placeholder visibile:
lorem ipsum per i testi, `TBA` per date e altri dati, un box "Not developed yet" per le funzioni che
non esistono ancora. I dettagli sono in [`CLAUDE.md`](CLAUDE.md).

## Anteprima e controlli in locale

Servono `bash`, `python3`, Node.js 20 o successivo con npm e Google Chrome o Chromium (se non è nel
PATH: `CHROME=/percorso/di/chrome`). Su Windows usa Git Bash, con `python3` nel PATH.

```bash
npm ci                      # installa Eleventy, html-validate e linkinator alle versioni di package-lock.json
npm run build               # cancella _site/ e lo ricostruisce da src/
npm run dev -- --port=8080  # anteprima con ricarica automatica; se la porta è occupata dà errore
scripts/preview.sh   # come npm run dev, con una porta ricavata dal percorso del checkout (Ctrl+C per fermarlo)
scripts/check.sh     # build, HTML valido, link, link finti, dati personali, test web e mobile, placeholder rimasti
```

`scripts/check.sh` apre ogni pagina in Chrome headless a 320, 375 e 768px (come su telefono e tablet) e a
1280px, e salva gli screenshot in `_screenshots/` (non va nel repository): guardali prima di pubblicare.

## Lavorare con Claude Code

Avvia Claude Code dalla root del checkout principale: le regole sono in [`CLAUDE.md`](CLAUDE.md) e in
`.claude/`. L'hook che protegge `main` e `deploy` richiede `python3` nel PATH (su Windows anche Git Bash).
Dopo il merge di modifiche a `CLAUDE.md` o `.claude/`, aggiorna il checkout principale con
`git pull --ff-only` e riavvia Claude Code.
