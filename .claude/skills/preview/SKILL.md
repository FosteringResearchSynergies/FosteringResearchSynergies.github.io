---
name: preview
description: Avvia l'anteprima locale del sito ed esegue i controlli QA (HTML valido, link interni, finti link, form senza action, dati personali, test web e mobile in Chrome headless, conteggio dei placeholder). Usala per verificare ogni modifica prima di un commit, di una PR o di una pubblicazione.
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
Installa le dipendenze con `npm ci` se mancano o sono vecchie, cancella `_site/`, esegue
`npm run build` e controlla `_site/`. Fallisce su: errori HTML (`html-validate`), link interni rotti
(`linkinator`, su tutte le pagine), link `href="#"`, vuoti o `javascript:`, `<form>` senza `action`,
numeri di telefono (indica solo file:riga), un file `CNAME` nel sito pubblicato e sui **test web e
mobile**: ogni pagina aperta in Chrome headless a 320, 375 e 768px (emulazione mobile, touch) e a
1280px, con errore se ci sono errori JavaScript, richieste fallite verso il sito, scroll orizzontale
(con gli elementi troppo larghi) o manca il meta viewport. Riporta senza fallire: quanti placeholder
restano per tipo (`lorem`, `tba`, `unbuilt`), quanti `TODO(team)` e il "Lorem ipsum" fuori da
`data-placeholder`.

I test web e mobile aprono Chrome headless (profilo temporaneo, solo il server locale): dillo in una
riga quando lanci `check.sh`. Servono `python3` e Chrome o Chromium (`CHROME=/percorso` se non è nel
`PATH`). Gli screenshot a pagina intera finiscono in `_screenshots/<larghezza>/<pagina>.png` (ignorata
da git, rigenerata a ogni esecuzione). Con exit 0 su un albero pulito `check.sh` registra il commit
come testato: è la condizione che l'hook chiede per pubblicare (vedi `CLAUDE.md`).

Le regole di `html-validate` che l'HTML attuale non rispetta sono in `warn` fino al Giorno 3 della
ROADMAP: quegli avvisi sono preesistenti e non bloccano, ma non aggiungerne di nuovi nei file che tocchi.
`check.sh` li riassume per regola; per vederli riga per riga su una pagina:
`npx --no-install html-validate --formatter text _site/<pagina>` (dopo `npm ci` e `npm run build`).
Un errore preesistente fuori dallo scopo del task non si corregge: si segnala nella PR.

Nel body della PR e nei log riporta solo exit code e conteggi, mai le righe trovate dai controlli.

## Anteprima nel browser

`scripts/preview.sh` è un server che resta attivo: avvialo in background (non in primo piano, la
chiamata non finirebbe mai) e annota l'URL che stampa all'avvio. La porta dipende dal percorso del
worktree, quindi più agenti possono avere un'anteprima contemporaneamente. Quando hai finito ferma il
processo che hai avviato.

## Controllo visivo minimo

Per ogni pagina toccata guarda con Read gli screenshot di `_screenshots/` a 320, 375, 768 e 1280px:
- testi leggibili e non tagliati, immagini non sgranate né deformate, nessun elemento sovrapposto;
- placeholder riconoscibili a colpo d'occhio.

Nell'anteprima del browser verifica anche che menu e programma siano usabili da tastiera (Tab, Invio)
con il focus visibile. Descrivi nella PR cosa hai verificato e a quali larghezze.

## Uso del browser

Puoi usare Chrome (headless da terminale oppure l'estensione Claude in Chrome), ma **prima** di
aprirlo scrivi in una riga a cosa ti serve e quali pagine/URL aprirai (per esempio:
"Apro Chrome headless per screenshot di index.html a 375, 768 e 1280px"). Alla fine dici cosa hai
fatto e chiudi schede e processi che hai aperto.

Chrome headless gira sempre con un profilo temporaneo, mai con quello dell'utente; gli screenshot
fatti a mano vanno fuori dal repository (quelli di `check.sh` stanno in `_screenshots/`, ignorata da
git). Il binario si prende da `CHROME` oppure dal `PATH`; su macOS `check.sh` lo trova da solo, per lo
snippet qui sotto imposta `CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"`.

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
