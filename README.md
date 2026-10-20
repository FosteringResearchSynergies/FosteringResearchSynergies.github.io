# Fostering Research Synergies: sito web

Sito del workshop **Fostering Research Synergies (FRS)**, organizzato da dottorandi e postdoc che
lavorano su sistemi complessi (CREF Roma, IMT Lucca, CSH Vienna).

Sito: <https://fosteringresearchsynergies.github.io/> · Contatto: frscrefimt@gmail.com

> Il sito è in fase di rifacimento (ottobre 2026): ritorno su github.io, pagina dell'edizione 2026 a
> Parma, nuova grafica. Piano e stato in [`docs/ROADMAP.md`](docs/ROADMAP.md).

## Come è organizzato il repository

| Percorso | Contenuto |
| --- | --- |
| `*.html`, `events/`, `pictures/`, `styles.css`, `navbar.js` | il sito attuale (HTML statico) |
| `docs/` | piano (`ROADMAP.md`), inventario dei problemi (`AUDIT.md`), direzione visiva (`DESIGN.md`) |
| `scripts/` | `check.sh` (controlli prima di ogni PR), `preview.sh` (anteprima locale) |
| `CLAUDE.md`, `.claude/` | regole condivise per gli agenti di Claude Code: agenti, skill, hook, permessi |

I file interni (`README.md`, `CLAUDE.md`, `docs/`, `scripts/`, `.claude/`) non vengono pubblicati.

## Branch

- `main`: integrazione. Si modifica solo tramite pull request.
- `deploy`: ciò che è online. Ci si arriva solo con una PR di release da `main`.
- Un branch per ogni modifica (`content/...`, `fix/...`, `feat/...`, `design/...`, `docs/...`, `chore/...`).

## Modificare il sito

1. Crea un branch (dall'interfaccia web: modifica il file e scegli "Create a new branch").
2. Apri una pull request verso `main` e descrivi cosa cambia.
3. Dopo il merge, chi gestisce le release apre la PR `main` → `deploy`.

Regole sui contenuti: niente informazioni inventate. Dove manca un testo si usa un placeholder visibile
(lorem ipsum, `TBA`, box "Not developed yet"); i dettagli sono in [`CLAUDE.md`](CLAUDE.md).

## Anteprima e controlli in locale

```bash
scripts/preview.sh   # avvia un server locale e stampa l'URL
scripts/check.sh     # HTML valido, link interni, link finti, dati personali, placeholder rimasti
```

Servono `python3` e Node.js (per `npx`).
