# Direzione visiva e struttura del sito

Direzione decisa dal team il 20 ottobre 2026: **Swiss editorial**, scelta dopo il confronto di tre prototipi. Sostituisce le tre proposte dell'audit (Field Notes, Phase Space, Motifs); "Motifs" (PR #7, branch `design/tokens`) è stata scartata. La mappa del sito e la tabella delle sezioni vengono dalla proposta dell'audit e restano nella lingua originale (inglese); stati e note aggiunti dopo sono in italiano.

Plugin e sintassi Jekyll citati qui (`_layouts`, `{% include %}`, `redirect_from`, `jekyll-sitemap`, `jekyll-seo-tag`) valgono solo se D1 = Jekyll. Con Eleventy (raccomandato in `docs/ROADMAP.md`) si usano gli equivalenti: `src/_includes`, `src/_data`, pagine di redirect statiche. Per i placeholder vale `CLAUDE.md`.

## Direzione decisa: Swiss editorial

Riferimento: il prototipo della home approvato dal team, riprodotto in `src/index.njk`. Il design system è in `src/assets/css/`: `main.css` importa font, token (`tokens.css`), base, layout e un file per componente (`components/`).

### Principi

- Pagina bianca, inchiostro quasi nero e un solo accento per tutto il sito: il blu elettrico. Nessun colore per edizione.
- La gerarchia la fanno la tipografia e i filetti: titoli molto grandi, etichette piccole in maiuscolo spaziato, filetti da 1px sopra sezioni e righe. Niente ombre, card, gradienti, pattern, icone o emoji.
- Sezioni numerate (01, 02, ...): filetto, numero in blu, titolo. Nella home il footer chiude la numerazione.
- Griglia a 12 colonne da 64rem (1024px), una colonna sotto. Breakpoint: 48rem e 64rem.
- Due sole superfici piene: la banda blu della prossima edizione (una per pagina) e il footer nero.
- Foto in bianco e nero, mai più larghe del file e mai ritagliate.
- Mobile first: nessuno scroll orizzontale a 320px; i titoli grandi usano `clamp()` o si adattano alla larghezza della colonna.

### Palette e contrasti

| Token | Valore | Uso | Contrasto (WCAG 2.2) |
| --- | --- | --- | --- |
| `--color-paper` | #FFFFFF | sfondo | |
| `--color-ink` | #0A0A0B | testo, filetti, footer | 19.8:1 su bianco |
| `--color-ink-2` | #55555C | testo secondario, etichette | 7.4:1 su bianco |
| `--color-accent` | #1F3BFF | iniziali, numeri di sezione, prossima edizione, link con freccia, focus; fondo della banda blu | 6.7:1 su bianco |
| `--color-on-accent` | #FFFFFF | testo sul blu | 6.7:1 |
| `--color-on-accent-2` | #D9DEFF | etichette sul blu | 5.1:1 |
| `--color-on-ink` | #FFFFFF | testo sul nero | 19.8:1 |
| `--color-on-ink-2` | #A3A3AB | testo secondario sul nero | 7.9:1 |
| `--color-rule-soft` | #DCDCE0 | separatori leggeri | decorativo |

Il blu sul nero (2.9:1) non si usa mai. I separatori leggeri non sono mai l'unico confine di un controllo.

### Tipografia

- **Inter Tight** per titoli, etichette, numeri e navigazione; **Inter** per il testo. Entrambi variabili (pesi 100-900), licenza OFL, ospitati in `src/assets/fonts/`: woff2 di Fontsource 5.3.0, subset latin e latin-ext, con `OFL.txt`. `font-display: swap` e preload di Inter Tight (latin) nell'include `head`. Nessuna richiesta a Google Fonts o a CDN.
- Dimensioni fisse per etichette e interfaccia (`--size-*`), passi fluidi con `clamp()` per testo e titoli (`--step-*`). Titoli in peso 600-700 con spaziatura negativa; etichette in maiuscolo, 13px, spaziatura 0.06em.
- Le frecce dei link sono caratteri del font: ↓ (U+2193) e ↑ (U+2191) sono nel subset, → no.

### Componenti

| File | Componente |
| --- | --- |
| `layout.css` | contenitore, griglia a 12 colonne, header con il marchio ("FRS" e il nome per esteso, separati da un filetto; link alla home, non `h1`), navigazione nell'HTML con `aria-current` (sotto 48rem su una riga sotto il marchio), intestazioni di sezione numerate (include `section-head.njk`), footer nero con l'email da `site.yml` in grande |
| `components/masthead.css` | titolo della home molto grande con le iniziali F, R, S in blu, frase introduttiva, link alla prossima edizione |
| `components/next-edition.css` | banda blu "Next edition": anno, città da bordo a bordo (classe `chars-N` dal filtro `fitChars`), quattro fatti (Dates, Venue, Call for abstracts, Registration) |
| `components/edition-list.css` | le edizioni come lista tipografica: versione o "Next", città e anno in grande, dettagli in mezzo; la prossima in blu |
| `components/point-list.css` | punti brevi con filetto, titolo e paragrafo (About); variante `is-numbered` con 01, 02, ... |
| `components/arrow-link.css` | link con filetto, etichetta, titolo in blu e freccia; solo verso destinazioni reali |
| `components/photo.css` | foto in bianco e nero; `.split` affianca foto e testo |
| `components/funding-band.css` | banda dei finanziamenti: dicitura del finanziatore alla lettera e striscia dei loghi nei colori originali (banner EFC obbligatorio di Lucca 2025) |
| `components/program.css` | programma di un'edizione: una tabella per giorno, tutti i giorni visibili, un `id` per ogni slot; tipo di sessione in `data-type` (keynote in blu, pause e momenti sociali attenuati), senza icone |
| `components/placeholder.css` | i tre placeholder (sotto) |

`edition.css`, `archive.css` e `pages.css` sono quasi vuoti: li riempiono i task paralleli del Giorno 2, uno per file. `src/styles.css` contiene solo le classi delle pagine portate dal vecchio sito (about, contact, events, Roma 2024, Lucca 2025), ridisegnate con i token; il Giorno 2 lo elimina.

### Placeholder

Si scrivono solo con l'include `placeholder` (tipo, testo), che `scripts/check.sh` conta. Ogni tipo ha un'etichetta testuale, non solo un colore:

- **`tba`**: la sigla "TBA" (`<abbr title="To be announced">`) in Inter Tight 600, al posto e nel corpo del valore che manca. Lettere a contorno nelle misure grandi (da 24px, testo grande per le WCAG: fatti della banda blu, anno nella lista delle edizioni, classe `tba-hollow`), piene sotto. Il contorno prende il colore del testo, quindi ha lo stesso contrasto del testo vero su bianco, sul blu e sul nero.
- **`lorem`**: testo nel colore secondario con un filetto blu a sinistra e l'etichetta "Placeholder text · " in maiuscolo, generata dal CSS.
- **`unbuilt`**: box sobrio con filetto da 1px e l'etichetta "Not developed yet:" in maiuscolo blu. Niente righe a pericolo.

Sul blu e sul nero filetti ed etichette prendono il colore del testo.

### Note di implementazione

- Colori, font, dimensioni, spaziature, filetti e focus solo dai token di `tokens.css`. Niente stili inline, `<style>` per pagina o `!important`.
- Focus visibile ovunque: contorno di 3px, nel blu sul bianco e nel colore del testo sulle superfici piene. Il primo elemento di ogni pagina è lo skip link verso `#main`.
- Il nome di una città che deve riempire la sua colonna (banda blu, lista delle edizioni) porta la classe `chars-N`, con N = `{{ città | fitChars }}` (da 4 a 12): la dimensione è la larghezza della colonna divisa per il numero di lettere.
- La foto di gruppo (`pictures/cover.png`, 641x486) ha `width`/`height`, `loading="lazy"` e il filtro `grayscale`; consenso, didascalia e testo alternativo restano da verificare con il team (`docs/AUDIT.md`, content-55).

## Mappa del sito proposta

- /  (Home: next-edition hero for FRS 2026 Parma, one-line 'what is FRS', edition timeline, group photo, contact strip)
- /editions/  (Archive: typographic list of every edition, as on the home; redirect_from /events.html)
- /editions/2026-parma/  (NEW: current edition page; sections below)
- /editions/2025-lucca/  (IMT Lucca, 18-20 Dec 2025: past-tense archive, final program from YAML, mandatory EFC/PNRR funding band; redirect_from /events/lucca.html)
- /editions/2024-rome/  (v2.0 CREF Rome, 20-22 Nov 2024: real program and talk list, AI filler and phone number removed; redirect_from /events/frs2024-winter.html)
- /editions/vienna/  (v1.X CSH Vienna: stub with a lorem block (data-placeholder="lorem") and the year as TBA until the team supplies them; slug becomes <year>-vienna once known)
- /editions/lucca-v1/  (v1.0 Lucca: stub as above; slug becomes <year>-lucca once known)
- /about/  (what FRS is, how editions are self-organized, how to propose or host the next one; team-written text or labelled lorem; redirect_from /about.html)
- /people/  (NEW: organizers by edition from _data/people.yml, consent-gated)
- /contact/  (real email only, no fake form or socials; redirect_from /contact.html)
- /404.html  (custom: links to the current edition and the archive)
- /sitemap.xml  (auto, jekyll-sitemap)
- REMOVED: /events/winter-2024.html (fabricated event), /events/event-template.html, /QUICK-START.html; README.md and CONTRIBUTING.md excluded from the build

## Sezioni della pagina di un'edizione (Parma 2026)

| Sezione | Scopo | Dati richiesti al team | Placeholder |
| --- | --- | --- | --- |
| Hero / masthead | Identify the edition at a glance: name, number, city, dates, host, status chip, one primary CTA. | Official name and numbering (e.g. 'FRS 2026 · Parma', 'v4.0' or '4th edition'?), exact dates, host institution(s), current status (save-the-date / call open / registration open / program out / closed). | Nulls in editions.yml render as a TBA chip (data-placeholder="tba", e.g. 'Dates TBA'). No stock photo of Parma: the blue field with the city name set edge to edge is the design until a licensed photo is supplied with credit. No lorem in the hero. |
| Status bar / primary CTA | Tell visitors the one thing they can do now (submit, register, read program). | Which phase is active today, and the external URL for it (Google Form or other). | Show the button only when a real URL exists in the data. Otherwise a plain status line such as 'Registration not open yet' (a real status, not a placeholder; no disabled or fake button). Never use href="#". |
| Key dates timeline | Deadlines in one glance: call opens, abstract deadline, notification, registration deadline, workshop days. | Each milestone date and whether it has passed. | Render from _data with `date: null` shown as TBA (data-placeholder="tba"). Past, open and closed states are set explicitly in YAML (no build-time 'today' logic). Hide the section entirely if no milestone is known. |
| About this edition | Two short paragraphs: why Parma, who it brings together, what is different this year. | Text written by the organizers (it can reuse the team-written line in lucca.html:113 about CREF and IMT as sister institutions). | Lorem ipsum through the placeholder include (data-placeholder="lorem"; the include renders the visible label), counted by scripts/check.sh. No AI-written stand-in prose. |
| Topics / scientific scope | Signals fit for the call (networks, economic complexity, social dynamics, etc.). | A list of 4-8 topics confirmed by organizers. | Hidden until the list exists. Topics are factual claims, so lorem would be misleading. |
| Call for abstracts | Who can submit, format (talk length, poster?), how selection works, deadline, submission link. | Eligibility, talk/poster format, selection criteria, deadline, submission URL. | Explanatory text as a lorem block (data-placeholder="lorem"). Deadline as a TBA chip (data-placeholder="tba"). Submission: real link button, or a plain status line 'Submission not open yet'. If the team plans an on-site submission form that does not exist, an unbuilt box (data-placeholder="unbuilt", 'Not developed yet: abstract submission form') with no fake input fields. |
| Registration & costs | Fee (free?), what is covered (accommodation, meals, social dinner, travel support), capacity, how to register. | Fee policy, coverage, travel-support rules, capacity, registration URL and deadline. | Coverage and fee facts are TBA (data-placeholder="tba"; never lorem, since they are commitments). The registration button follows the same rule as the CTA. Any on-site form is an unbuilt box (data-placeholder="unbuilt"). |
| Program | Day-by-day schedule with all days visible and linkable slots; session types as text, with no icons. | _data/programs/2026-parma.yml: days, slots (start, end, type, title, speakers, affiliations), session themes. | Until data exists, one line: 'Program: TBA' (data-placeholder="tba"). Show day columns only if dates are known. Never invent times, session titles or speakers, and never use lorem for names. |
| Keynotes / invited speakers | Credibility and draw: names, affiliations, talk titles, optional photos. | Confirmed speakers with affiliation, title and photo consent. | Hidden until at least one speaker is confirmed. No silhouette avatars or 'Speaker TBA' cards. |
| Venue & getting to Parma | Where exactly (building, room, address) and how to arrive (train via Bologna/Milan, station-to-venue route). | Venue name, room, address, access instructions (badges, entrances), travel notes the team has verified. | Address shown as 'Venue TBA' (data-placeholder="tba") until confirmed. Travel prose as a lorem block (data-placeholder="lorem") until the team writes or verifies it. Map: a plain OpenStreetMap link once the address is known, with no embedded map widget (if the team later wants one, it is an unbuilt box). |
| Accommodation | Whether rooms are provided and booked by organizers, check-in/out, or suggestions. | Policy (covered / block booking / self-booked), hotel or residence names, dates, booking procedure. | A TBA status line (data-placeholder="tba") plus a lorem block (data-placeholder="lorem") for the explanatory text. No invented hotel names. |
| Organizers | Who runs this edition, with affiliations, and how it connects to the FRS team. | Names, affiliations, roles, optional link/photo, explicit consent (_data/people.yml). | One line 'Organizing committee: TBA' (data-placeholder="tba") until data exists. Never list placeholder people. |
| Partners & funding | Host institution and funder logos, plus mandatory acknowledgement text (as with the PNRR banner for Lucca 2025). | Confirmed partners/funders, official logo files, required acknowledgement wording and placement rules. | Hidden until confirmed. No placeholder logos ever (legal and branding implications). If funding is PNRR/EU, the funding band component is mandatory and reused from Lucca 2025. |
| FAQ | Practical questions (language, slides, posters, dietary needs, remote participation). | At least 3 real Q&A pairs. | Hidden until at least 3 real entries exist. Lorem Q&A would look fake. |
| Contact | A single, real point of contact for the edition. | Confirm frscrefimt@gmail.com (from site.yml) or a Parma-specific address; optional local contact name. | Always shown with the real address from site.yml. No phone numbers and no contact form (an unbuilt box only if the team explicitly wants a form later). |
| Previous editions strip | Continuity: links to Lucca 2025, Rome 2024 and earlier stubs. | None beyond editions.yml. | Generated automatically. Stub editions show a lorem block (data-placeholder="lorem") in place of the archive text. |
| After the event (photos, slides, highlights) | Turns the page into an archive after December. | Photos with consent and credits, optional slides links, final participant count. | Hidden until status becomes 'past' and content exists. |

## Problemi di architettura dell'informazione

- **ia-01** · critical · `index.html:45`: Home page never shows the next edition; the only news is a stale Oct-2025 teaser. *Stato: **in parte**: notizia scaduta sostituita nell'hotfix; manca la home generata dai dati.* Make the home hero data-driven: render the edition with `status: upcoming` from _data/editions.yml (FRS 2026 Parma) with dates, city, status and primary CTA. Replace the 'Latest News' block with the edition timeline.
- **ia-02** · critical · `events.html:32`: Lucca Dec 2025 still badged 'Upcoming' with a 'View Details & Register' CTA. *Stato: **risolto nell'hotfix**: Lucca 2025 tra le edizioni passate, Parma 2026 come prossima.* Drive badges and CTAs from one status field per edition (upcoming/past). Move Lucca 2025 to past with an 'Archive' CTA and add Parma 2026 as the only upcoming edition.
- **ia-03** · high · `events.html:41`: v1.0 Lucca and v1.X Vienna are missing from the events list; they only appear in prose on the Rome page. Create _data/editions.yml with all editions (v1.0 Lucca, v1.X Vienna, v2.0 Rome 2024, Lucca 2025, Parma 2026). Render a timeline on home and on /editions/. Editions with no archive content get a timeline entry plus a stub page with a lorem block (data-placeholder="lorem") in place of the archive text.
- **ia-04** · high · `events.html:49`: Inconsistent naming ('events' vs editions, version numbers vs years) and ambiguous URLs. Make 'Edition' the primary concept (nav label 'Editions'). Use one canonical label 'FRS <year> · <City>', with the version tag (v2.0, v4.0...) as an optional secondary label, and one URL scheme /editions/<year>-<city>/. Keep old URLs alive with redirect_from.
- **ia-05** · medium · `events/lucca.html:113`: Edition count and frequency claims contradict each other. Ask the team for the official numbering (is Parma '4th edition' / 'v4.0'?) and frequency, store it in editions.yml, and stop hard-coding it in prose.
- **ia-06** · critical · `events/winter-2024.html:14`: An entirely fabricated event ('Winter Conference 2024') is publicly reachable. *Stato: **risolto nell'hotfix**: events/winter-2024.html eliminato.* Delete the file. Do not redirect it. Let it return 404.
- **ia-07** · high · `events/event-template.html:6`: The authoring template is published as a public page. *Stato: **risolto nell'hotfix**: events/event-template.html eliminato.* Delete it. Its role moves to _layouts/edition.html plus a commented example entry in _data/editions.yml.
- **ia-08** · high · `README.md:1`: Generic template README and QUICK-START; QUICK-START is rendered publicly by Jekyll. *Stato: **risolto**: QUICK-START.md eliminato nell'hotfix, README riscritto ed escluso dal build.* Delete QUICK-START.md. Rewrite README.md as a short editor guide (how to edit editions.yml or an edition page in the web UI, and how a change reaches 'deploy'). Add both to `exclude:` in _config.yml.
- **ia-09** · critical · `contact.html:31`: Contact page lists fake email addresses; the real address appears only on other pages. *Stato: **in parte**: indirizzi finti sostituiti nell'hotfix; manca la fonte unica (`site.yml`).* Store the single real address in _data/site.yml and render it everywhere (contact page, footer, edition pages).
- **ia-10** · high · `contact.html:40`: Fake social handles that link nowhere. *Stato: **risolto nell'hotfix**: link social rimossi.* Remove them. List a social link only if the team confirms a real account (driven from site.yml).
- **ia-11** · high · `contact.html:59`: Mailing-list box and contact form do nothing, and a developer note is shown to the public. *Stato: **risolto nell'hotfix**: box `unbuilt` al posto di form e mailing list, nota rimossa.* Replace the form with a mailto link to the real address. If the team wants a mailing list, show a box clearly labelled 'Mailing list: not developed yet', with no input field and no button.
- **ia-12** · medium · `events/lucca.html:268`: Dead 'Submit Abstract' button on an edition that is already over. *Stato: **risolto nell'hotfix**: link finto rimosso, la call risulta chiusa.* Remove the box from the archive page. On the Parma page, show the submission CTA only when a real URL is in the data; otherwise show 'Submission not open yet'.
- **ia-13** · medium · `contact.html:90`: No organizers/people page; the 'Organizing Committee' box names nobody. Add /people/ driven by _data/people.yml (name, affiliation, editions, role, optional link), and an organizers section on each edition page. Publish only names the team has confirmed with consent.
- **ia-14** · medium · `navbar.js:2`: Navigation is injected client-side, uses the site name as h1 everywhere, and has no entry for the current edition. Render the nav from a server-side include (_includes/nav.html): brand (not h1) \| 'Parma 2026' highlighted \| Editions \| About \| People \| Contact. Add a skip link, a mobile menu, and one h1 per page.
- **ia-15** · high · `about.html:47`: Home and About copy is generic AI filler that misstates FRS's complex-systems focus. Replace with lorem blocks (data-placeholder="lorem") until the team writes the text. Keep only team-written facts (e.g. lucca.html:113 on CREF and IMT as sister institutions, complex systems).
- **ia-16** · medium · `events.html:35`: Generic description of the Lucca 2025 edition. *Stato: **in parte**: descrizione sostituita nell'hotfix; mancano le card generate dai dati.* Generate edition cards from editions.yml (`summary` field). Where the team has not written a summary, render a lorem block (data-placeholder="lorem").
- **ia-17** · high · `events/frs2024-winter.html:87`: Rome 2024 archive is padded with AI jokes and made-up stats. Delete the filler sections (Numbers Game, Why FRS Matters, Fun Fact, tagline). Keep the real program (lines 140-334: talk titles and speakers) by moving it to _data/programs/2024-rome.yml, and keep the real organizers' quote (:357).
- **ia-18** · high · `events/frs2024-winter.html`: A personal mobile number is published on an archived page. *Stato: **risolto nell'hotfix**: riga eliminata.* Remove it. Never publish phone numbers in edition data; logistics contacts go by email.
- **ia-19** · medium · `events/frs2024-winter.html:367`: Aneddoto che nomina terzi. Chiedere al team. Di default eliminarlo: non è adatto a una pagina istituzionale.
- **ia-20** · low · `events/frs2024-winter.html:96`: Commented-out invited-speakers block. Delete it. Speaker names and titles already live in the program and move to programs/2024-rome.yml.
- **ia-21** · medium · `events/lucca.html:116`: Lucca 2025 page is still in future tense and contradicts itself. Convert to a past-tense archive (/editions/2025-lucca/): factual summary, final program from YAML, real participant count if known. Drop the registration, accommodation and call boxes.
- **ia-22** · medium · `events/lucca.html:121`: Venue copy has unverified, AI-sounding claims. Keep only the verified address (:124 `Sagrestia IMT, Piazza San Francesco 17, Lucca`). Remove the facility and parking claims unless organizers confirm them.
- **ia-23** · high · `events/lucca.html:292`: Mandatory NextGenerationEU/PNRR funding banner must survive the migration; it currently has poor alt text and a fragile file name. Keep it on /editions/2025-lucca/ as a full-width 'funding band' (background #2A65AF, sampled from the banner). Rename it to assets/img/editions/2025-lucca/efc-pnrr-banner.png and use alt text that lists the funders. Ask whether Parma 2026 has similar obligations.
- **ia-24** · medium · `events/lucca.html:304`: Programs are hidden in fragile JS tabs, duplicated in three files. Render programs from _data/programs/<edition>.yml with one include. Show all days stacked (or a CSS grid), add anchor ids per day and slot, and treat tabs as progressive enhancement only.
- **ia-25** · high · `CNAME:1`: No canonical URL or redirect plan: the site lives on an HTTP-only IMT subdomain and old links will break when it moves. *Stato: **in parte**: CNAME rimosso nell'hotfix; il sito è servito da https://fosteringresearchsynergies.github.io/ e il vecchio dominio frs-workshop.imtlucca.it appartiene al repository FosteringResearchSynergies/frs-workshop-redirect, che reindirizza ogni percorso su github.io.* Prima di togliere il dominio dal repository di redirect o di disattivarne Pages, verificarlo a livello di organizzazione (record TXT `_github-pages-challenge-FosteringResearchSynergies.frs-workshop.imtlucca.it`, da chiedere all'IT di IMT): senza verifica chiunque può rivendicarlo. Il dominio custom non torna in questo repository. Restano da fare: url canonico nel generatore, redirect dai vecchi percorsi (/events.html, /events/lucca.html, /events/frs2024-winter.html, /about.html, /contact.html) e una 404 personalizzata.
- **ia-26** · high · `(GitHub Pages settings)`: Every commit to main is published immediately; there is no deploy branch. *Stato: **in parte**: Pages pubblica da `deploy` dal 20 ottobre 2026; mancano le regole di protezione dei branch.* Make `deploy` the Pages source branch and protect it (PR-only, required build check). Keep `main` as the integration branch and use feature branches/worktrees for agents.
- **ia-27** · medium · `styles.css:237`: No design system: template purple leftovers, inline-style sprawl, emoji as icons. Rebuild CSS around tokens (assets/css/tokens.css) with zero inline styles. Replace emoji with an SVG motif icon set, and use a per-edition `--accent` variable.
- **ia-28** · medium · `styles.css:62`: Low-resolution photos used full-bleed. Ask for originals. Meanwhile use the group photo contained or duotone-treated, not as a stretched cover background. Add width/height attributes and use WebP/AVIF.
- **ia-29** · low · `index.html:6`: No meta description, Open Graph image or favicon, and inconsistent titles. Use jekyll-seo-tag with a title pattern '<Page> · FRS', a per-edition og:image (an important share preview when announcing Parma), a favicon and a sitemap (jekyll-sitemap).
- **ia-30** · low · `events.html:21`: Unclosed container div on events page. *Stato: **risolto nell'hotfix**: div chiuso; `scripts/check.sh` valida l'HTML.* The page is replaced by /editions/ from a layout. HTML validation runs in scripts/check.sh (html-validate).
- **ia-31** · low · `index.html:59`: Footer is stale, carries 'All rights reserved' and lists no institutions or contact. One footer include: institutions involved (from data), the real contact email, a link to the GitHub repo and a dynamic year.
- **ia-32** · low · `index.html:26`: Home cards duplicate the About page. Home: one-line tagline, next edition, timeline. Keep the long-form text only on /about/.
- **ia-33** · low · `(local toolchain)`: Strumenti per l'anteprima locale. Jekyll in locale richiede Ruby con gli header di sviluppo e gem native; Eleventy richiede solo Node.
- **ia-34** · low · `QUICK-START.md:1`: The site already goes through Jekyll 3.10 on Pages, so a Jekyll restructure is incremental. Adopt Jekyll layouts, includes and _data deliberately instead of relying on it by accident. Dot-folders such as .claude/ are ignored by Jekyll; with GitHub Actions only the build output (_site/) is uploaded.
