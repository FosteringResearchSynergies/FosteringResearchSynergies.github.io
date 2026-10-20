---
name: preview
description: Avvia l'anteprima locale del sito ed esegue i controlli QA (HTML valido, link interni, finti link, form senza action, dati personali, conteggio dei placeholder). Usala per verificare ogni modifica prima di un commit o di una PR.
---

# Anteprima e controlli

Usa sempre gli script del worktree che stai verificando. Se la shell non è già nella sua root
(per esempio in un subagente senza isolamento, dove `cd` non persiste), scrivi
`cd <percorso assoluto del worktree> && <comando>` in ogni chiamata.

## Controlli automatici (obbligatori prima della PR)

```bash
scripts/check.sh
```

Lo script controlla il checkout in cui si trova, qualunque sia la cartella corrente. Exit code 0 = OK.
Con un `package.json` cancella `_site/`, esegue `npm run build` e controlla `_site/`; altrimenti
controlla i file HTML così come sono. Fallisce su: errori HTML (`html-validate`), link interni rotti
(`linkinator`, su tutte le pagine), link `href="#"`, vuoti o `javascript:`, `<form>` senza `action`,
numeri di telefono (indica solo file:riga), un file `CNAME` nel sito pubblicato. Riporta senza
fallire: quanti placeholder restano per tipo (`lorem`, `tba`, `unbuilt`), quanti `TODO(team)` e il
"Lorem ipsum" fuori da `data-placeholder`.

Le regole di `html-validate` che l'HTML attuale non rispetta sono in `warn` fino al Giorno 3 della
ROADMAP: quegli avvisi sono preesistenti e non bloccano, ma non aggiungerne di nuovi nei file che tocchi.
`check.sh` li riassume per regola; per vederli riga per riga su una pagina:
`npx --yes html-validate@9.7.1 --formatter text <pagina>` (con il generatore, la pagina in `_site/`).
Un errore preesistente fuori dallo scopo del task non si corregge: si segnala nella PR.

Nel body della PR e nei log riporta solo exit code e conteggi, mai le righe trovate dai controlli.

## Anteprima nel browser

`scripts/preview.sh` è un server che resta attivo: avvialo in background (non in primo piano, la
chiamata non finirebbe mai) e annota l'URL che stampa all'avvio. La porta dipende dal percorso del
worktree, quindi più agenti possono avere un'anteprima contemporaneamente. Quando hai finito ferma il
processo che hai avviato.

## Controllo visivo minimo

Per ogni pagina toccata, a 375px, 768px e 1280px di larghezza:
- nessuno scroll orizzontale, testi leggibili, immagini non sgranate né deformate;
- menu e programma usabili da tastiera (Tab, Invio), focus visibile;
- placeholder riconoscibili a colpo d'occhio.

Se puoi, fai uno screenshot per larghezza e descrivi nella PR cosa hai verificato.

## Uso del browser

Puoi usare Chrome (headless da terminale oppure l'estensione Claude in Chrome), ma **prima** di
aprirlo scrivi in una riga a cosa ti serve e quali pagine/URL aprirai (per esempio:
"Apro Chrome headless per screenshot di index.html a 375, 768 e 1280px"). Alla fine dici cosa hai
fatto e chiudi schede e processi che hai aperto.

Chrome headless gira sempre con un profilo temporaneo, mai con quello dell'utente, e salva gli
screenshot fuori dal repository. Il binario si prende da `CHROME` oppure dal `PATH`; su macOS imposta
`CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"`.

```bash
CHROME="${CHROME:-$(command -v google-chrome || command -v chromium || command -v chromium-browser)}"
[ -n "$CHROME" ] || { echo "Chrome non trovato: imposta CHROME"; exit 1; }
URL="http://127.0.0.1:<porta>/"        # URL stampato da scripts/preview.sh
profile="$(mktemp -d)"; out="$(mktemp -d)"
for w in 375 768 1280; do
  "$CHROME" --headless=new --user-data-dir="$profile" --window-size="$w,900" \
    --screenshot="$out/page-$w.png" "$URL"
done
rm -rf "$profile"
echo "screenshot in $out"
```
