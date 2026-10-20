---
name: preview
description: Avvia l'anteprima locale del sito ed esegue i controlli QA (HTML valido, link interni, finti link, dati personali, conteggio dei placeholder). Usala per verificare ogni modifica prima di un commit o di una PR.
---

# Anteprima e controlli

Esegui sempre dalla root del tuo worktree.

## Controlli automatici (obbligatori prima della PR)

```bash
scripts/check.sh
```

Exit code 0 = OK. Controlla la validità HTML (`html-validate`), i link interni (`linkinator`), i finti
link `href="#"` e i numeri di telefono, poi stampa quanti placeholder (`lorem`, `tba`, `unbuilt`,
`TODO(team)`) restano nel sito. Con un `package.json` esegue prima `npm run build` e controlla `_site/`.
Un errore preesistente fuori dallo scopo del task non si corregge: si segnala nella PR.

## Anteprima nel browser

```bash
scripts/preview.sh            # in background: è un server che resta attivo
```

La porta dipende dal percorso del worktree, quindi più agenti possono avere un'anteprima
contemporaneamente. L'URL è stampato all'avvio. Ferma il server quando hai finito.

## Controllo visivo minimo

Per ogni pagina toccata, a 375px, 768px e 1280px di larghezza:
- nessuno scroll orizzontale, testi leggibili, immagini non sgranate né deformate;
- menu e programma usabili da tastiera (Tab, Invio), focus visibile;
- placeholder riconoscibili a colpo d'occhio.

Se puoi, fai uno screenshot per larghezza e descrivi nella PR cosa hai verificato.

## Uso del browser
Puoi usare Chrome (headless da terminale oppure l'estensione Claude in Chrome), ma **prima** di
aprirlo scrivi in una riga a cosa ti serve e quali pagine/URL aprirai (per esempio:
"Apro Chrome headless per screenshot di index.html a 375px e 1280px"). Alla fine dici cosa hai
fatto e chiudi schede e processi che hai aperto. Per Chrome headless usa sempre un profilo
temporaneo e salva gli screenshot fuori dal repository:

```bash
tmp="$(mktemp -d)"
google-chrome --headless=new --user-data-dir="$tmp/profile" --window-size=375,900 \
  --screenshot="$tmp/index-375.png" "http://127.0.0.1:<porta>/"
```
