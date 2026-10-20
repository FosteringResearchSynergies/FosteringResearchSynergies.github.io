# Audit del sito (20 ottobre 2026)

Inventario dei problemi del sito com'era su `main` al commit `c8f1b38`. Prodotto da 12 agenti (contenuti, codice, accessibilità, pubblicazione, revisione critica), con ogni finding verificato da un secondo agente che ha cercato di confutarlo. I testi dei finding sono nella lingua originale dell'audit (inglese). Le voci su infrastruttura e impostazioni dell'organizzazione GitHub sono tenute fuori dal repository pubblico.

Uso: prima di toccare un file, cerca qui il suo nome. Le azioni sui contenuti indicano cosa è reale (tenere), cosa è inventato (eliminare), cosa manca (lorem ipsum o non sviluppato) e cosa deve confermare il team. Quando un finding è risolto, la PR lo cita con il suo ID.

## Sintesi

- **180 finding**: 1 critical, 22 high, 76 medium, 81 low.
- Per area: contenuti 78, codice 41, accessibilità 37, pubblicazione 12, revisione critica 12.
- Azioni sui contenuti: eliminare 29, verifica del team 28, sostituire con lorem ipsum 17, aggiornare (scaduto) 14, tenere 13, marcare come non sviluppato 9.

## Priorità: critici e alti

| ID | Dove | Problema | Cosa fare |
| --- | --- | --- | --- |
| content-01 | `contact.html:31` | **Fake contact emails on a real third-party domain (phdnetwork.org) with a live mail server** | Remove both addresses now. Replace them with the real address frscrefimt@gmail.com as a mailto link (or another address the team confirms). Never invent addresses: emails sent to these go to an unrelated organisation. |
| a11y-15 | `about.html:65` | **The real contact email is plain text (not tappable), while contact.html links fake addresses** | Remove the fabricated info@/events@phdnetwork.org addresses now. Render the real address (frscrefimt@gmail.com, or whatever the team confirms) from one source as a mailto: link on every page. |
| code-03 | `contact.html:31` | **Contact links point to the generator's fake domain and to href="#"** | Replace with the real address, or with a single source-of-truth include. Remove the social links unless real handles exist. Otherwise show a lorem/'not available' marker rather than a fake handle. |
| deploy-11 | `contact.html:31` | **Placeholder addresses use a real third-party domain with a working mail server, so mail meant for the team leaks to strangers** | Replace these with the real team address (frscrefimt@gmail.com), or with a marker that obviously cannot be sent to. Add a rule for agents to .claude: placeholder emails, URLs and handles must use reserved domains (example.org, .invalid) or lorem ipsum, never names that look real such as phdnetwork.org or @PhDNetwork. |
| code-02 | `contact.html:51` | **Mailing-list 'Subscribe' widget is inert: no form, no handler, no name, no label** | Delete it, or turn the box into a clearly labelled 'Mailing list: feature not developed' placeholder until a real list (Google Group or similar) exists. |
| content-08 | `contact.html:59` | **Contact form does nothing, and submitting it puts personal data in the URL** | Either connect a real backend (Formspree/Google Form) or replace the form with a visibly disabled box labelled "Feature not developed" plus a mailto:frscrefimt@gmail.com link. Until then, the form must not accept personal data. |
| code-01 | `contact.html:59` | **Contact form has no action/method: submitting sends nothing and puts personal data in the URL** | Remove the form, or replace it with an explicit 'Feature not developed' box and a mailto: link to the real address. If a form is wanted later, wire it to a real endpoint (Formspree or Google Form) and use method=POST. Delete the developer note from the public page. |
| a11y-13 | `contact.html:59` | **Contact form and mailing-list signup look functional but do nothing; the signup field has no label** | Either connect them to a real service (Google Form or Formspree link) or replace each box with an explicit 'Not developed yet' marker and disabled controls (aria-disabled, visible badge), as the team asked for honest placeholders. Remove the developer note. Give every input a <label> and borders of 3:1 or more. |
| deploy-10 | `contact.html:59` | **The contact form has no action, so it sends name, email and message as URL parameters over plain HTTP, and the message goes nowhere** | Remove the working form. Replace it with a clearly labelled box such as 'Contact form: not developed yet. Please write to frscrefimt@gmail.com', with the inputs disabled or removed. If a form service is added later (Formspree, Google Forms), it must run over HTTPS and come with a short privacy note (GDPR: who receives the data and how long it is kept). |
| content-19 | `events.html:22` | **No Parma 2026 edition anywhere on the site** | Add an Upcoming card and an events/parma-2026 page. Fill confirmed facts (Parma, 2026, organizers) and use visible lorem ipsum for the description, program and venue. Mark registration/abstract boxes "Feature not developed / opens TBD". Do not write fake-sounding copy. |
| content-18 | `events.html:32` | **Lucca Dec 2025 still listed as "Upcoming" with a "Register" button** | Move the Lucca 2025 card to Past Events with a "Past" badge and a "View Event Archive" button. The Upcoming slot should hold Parma 2026. |
| code-29 | `events.html:32` | **Event status and CTAs are hard-coded in markup and now wrong; event data lives in 3 places** | Keep editions in _data/editions.yml (slug, dates, venue, status, hero image) and render the events list, the homepage 'next edition' block and the badges from it. Add Parma 2026 as upcoming and move Lucca to past. |
| content-02 | `events/frs2024-winter.html:342` | **Personal mobile phone number published on a public archive page** | Delete the line from the page and from the deploy branch right away. The event ended in Nov 2024, so the instruction has no use. The number is also on the currently served frs-workshop.imtlucca.it host and in git history. Rewriting history is the team's call, but at least make sure the new deploy branch never contains it. |
| content-03 | `events/winter-2024.html:14` | **Entire fabricated event page ("Winter Conference 2024") is publicly reachable** | Delete the file (lines 1-158) from the repo and the deploy. Do not keep it as an example: README.md:23 refers to it as an example of a past event. |
| content-04 | `events/winter-2024.html:61` | **Fake poster-award winners (invented people)** | Delete along with the page (lines 59-64). FRS has never run poster awards as far as the repo shows. |
| content-05 | `events/winter-2024.html:69` | **Invented participant testimonials** | Delete (lines 66-74). If the team wants testimonials on the new site, they must be real quotes with consent. Otherwise leave a clearly marked lorem-ipsum slot. |
| content-06 | `events/winter-2024.html:88` | **Invented keynote speakers and sessions** | Delete (program lines 76-124) with the page. |
| code-25 | `events/winter-2024.html:88` | **Fabricated 'Winter Conference 2024' page is publicly reachable (200 on live host), though not linked** | Delete the file; it is invented generator demo content published under the group's name. |
| seo-01 | `index.html:6` | **No meta description, Open Graph or Twitter Card tags on any page: WhatsApp/Slack/LinkedIn previews show a bare title with no image** | Add one shared head include (via a build step or Jekyll _includes) to every page with a per-page meta description, og:title/og:description/og:url/og:type and og:image. og:image must be an absolute https URL on fosteringresearchsynergies.github.io, 1200x630, JPEG under about 300 KB (WhatsApp often drops larger images). Also add twitter:card=summary_large_image and og:locale. Give the Parma page … |
| content-17 | `index.html:48` | **"Latest News" is a year-old teaser** | Replace it with a Parma 2026 announcement. Use real facts only (city, year). Put lorem ipsum or "dates TBD" where details aren't decided. |
| code-05 | `index.html:57` | **No templating: head, nav include, hero and footer are hand-copied across 8 pages and have already drifted** | GitHub Pages already runs Jekyll, so use _layouts/default.html with _includes/head.html, nav.html and footer.html, and set the page title through front matter. This also removes the need for navbar.js. |
| perf-01 | `pictures/cover.png:1` | **617 KB PNG photo is about 98% of the home page weight; WebP would be about 63 KB** | Store photos as JPEG/WebP/AVIF, never PNG (PNG only for flat logos). Add an image pipeline or checklist: max about 200 KB per hero variant, generated sizes and formats. |
| a11y-01 | `styles.css:121` | **Brand accent #3498db fails WCAG AA in every use (buttons, active tab, links, schedule times, active nav)** | Define color tokens in :root. Use a darker accent for fills and text on light backgrounds, e.g. #2471a3 (5.30:1 with white). On the dark navbar use a light tint such as #85c1e9 (5.65:1) plus a non-color indicator (underline). Check each pair of the new palette with a contrast script. |

## Per file

### `events/lucca.html` (36)

- **critic-07** · low · riga 1: History shows a revert/re-revert sequence on main and a navigation feature that was dropped.
  - Correzione: Cite this in the workflow docs as the reason for the PR-only rule and the deploy branch (deploy-04). Decide explicitly whether the reverted dropdown navigation (efd25df, 7b05740) is wanted in the restyle; otherwise agents may pull it back from history or from the stash.
- **seo-08** · low · riga 6: No schema.org Event structured data on event pages.
  - Correzione: Give the Parma 2026 page (and the past editions) Event JSON-LD with name, startDate/endDate, eventStatus, eventAttendanceMode, location (Place, Parma address), organizer and url. Leave unknown fields out until the team confirms them instead of inventing values.
- **code-12** · medium · riga 30: Page-specific <style> uses 13 !important rules and attribute selectors that match literal inline-style strings.
  - Evidenza: events/lucca.html:30 `.content .grid[style*="grid-template-columns: 2fr 1fr"] { grid-template-columns: 1fr !important; }`; :74 `.content p[style*="font-size: 0.85rem"]`; :80 `.content img[alt="EFC Banner"]`; :45 `.registration-box { margin-top: 1.5rem !important; }` (only needed to beat inline `style="margin-top: 2rem;"` at :260, :265, :271). `grep -c '!important' events/lucca.html` gives 13.
  - Correzione: Delete the block and move the rules into styles.css as classes. Any reformat of the inline style (e.g. `grid-template-columns:2fr 1fr` without the space, which a web-UI edit can easily produce) silently breaks the mobile layout.
- **code-13** · low · riga 35: No-op flex/grid 'order' rules with a misleading comment, applied to every .grid on the page.
  - Correzione: Remove.
- **content-54** · low · riga 89: Venue header photos (IMT cloister, CREF building) have unknown source and license. Azione: *verifica del team*.
  - Correzione: Ask who took these photos or where they came from. Add a credit or license line if needed, or replace them with team photos. Do the same check for any Parma venue image.
- **a11y-20** · low · riga 89: White header text over the bright campus photo dips below 4.5:1 in places.
  - Correzione: Use a stronger or gradient scrim behind the text block (e.g. 0.6-0.65, or a solid text panel), and choose the background position so text sits on the darker parts of the photo.
- **code-22** · low · riga 90: Event-header overlay is an inline empty div copy-pasted per page instead of the existing ::before pattern.
  - Correzione: Create one .page-hero component with a ::before overlay and a --hero-image custom property (style="--hero-image:url(...)" or front-matter driven).
- **content-45** · low · riga 92: Lucca 2025 core facts: title, dates, venue, address, transport. Azione: *tenere*.
  - Correzione: Keep. Rephrase the transport line in past tense for the archive.
- **content-39** · medium · riga 101: "30 participants expected" on a past event. Azione: *aggiornare (scaduto)*.
  - Evidenza: `👥 <strong>30 participants expected</strong>`
  - Correzione: Ask for the actual number of participants and switch to past tense, or drop the line.
- **content-46** · low · riga 113: "About the Workshop" paragraph is team-written and concrete. Azione: *tenere*.
  - Correzione: Keep and switch to past tense. It is a good source for the about page and the Parma blurb, once the team confirms it.
- **content-40** · medium · riga 116: "over two days" contradicts the Dec 18-20 three-day program. Azione: *verifica del team*.
  - Evidenza: `This year’s edition, hosted at IMT Lucca over two days, will feature a lively mix of scientific talks, interactive brainstorming sessions, and creative challenges such as quizzes and collaborative writing activities.`
  - Correzione: Ask the team: two full days plus a half-day Saturday? Were there really "collaborative writing activities"? Then rewrite in past tense.
- **content-42** · low · riga 121: Venue sentence keeps unverified template boilerplate. Azione: *eliminare*.
  - Correzione: Keep the first sentence and delete the second (template claim, never verified).
- **critic-04** · low · riga 124: The site has no outbound links: no partner institutions, venue maps, speakers or funders.
  - Correzione: In the restyle, link the partner institutions (CREF, IMT, CSH and the Parma host), add map links for venue and dinner addresses, and link the EFC/PNRR acknowledgement to its programme page. On the Parma page, use explicit 'link TBD' placeholders where URLs are not known yet.
- **content-43** · low · riga 125: Parking line is a template leftover nobody verified. Azione: *eliminare*.
  - Correzione: Delete it. The San Francesco campus is in Lucca's historic centre; if the team knows real parking info, they can add it.
- **content-44** · medium · riga 130: "Program will be announced in early December" on a past, finalized program. Azione: *aggiornare (scaduto)*.
  - Evidenza: `<p>The detailed program will be announced in early December. Here's a preview of what to expect:</p>`
  - Correzione: Replace with a neutral archive heading ("Program").
- **a11y-07** · medium · riga 132: Program day tabs are not an accessible tab widget: no ARIA, no arrow keys, color-only selected state, fragile global-event JS duplicated in three files.
  - Evidenza: `<button class="tab-button active" onclick="showDay('day1')">` with no role/aria anywhere (grep 'aria-\|role=' -> 0). lucca.html:317 `event.target.classList.add('active');` relies on the implicit global event. Headless test: focus Day 1, press ArrowRight -> still `day1` shown. Same code copied in frs2024-winter.html:407-417 and winter-2024.html:140-156. With JS off, only day 1 is visible, and …
  - Correzione: Option 1: one shared tabs.js implementing the WAI-ARIA Tabs pattern (tablist/tab/tabpanel, aria-selected, aria-controls, roving tabindex, arrow/Home/End), with the selected state shown by more than color. Option 2 (simpler and better for print/SEO): render all days stacked with an in-page day sub-nav.
- **content-47** · low · riga 152: Lucca 2025 Day 1-2 program (keynotes, session themes) edited by the team. Azione: *tenere*.
  - Correzione: Keep. Ask the team for the per-session talk lists (speaker + title) so the archive matches the 2024 page.
- **deploy-17** · low · riga 152: Stale, diverged branch mfessina-patch-1 holds an unmerged commit; merged branches are not auto-deleted. Azione: *verifica del team*.
  - Correzione: Ask mfessina whether the talk titles in 149500d should be kept. If so, cherry-pick only those lines through a PR. Then [OUTWARD] `gh api -X DELETE repos/FosteringResearchSynergies/FosteringResearchSynergies.github.io/git/refs/heads/mfessina-patch-1` and `gh api -X PATCH repos/... -F delete_branch_on_merge=true`.
- **critic-13** · low · riga 160: Lucca 2025 cannot be archived as-is: no talk list, no keynote titles, no speaker affiliations. Azione: *verifica del team*.
  - Correzione: Ask the organizers for the final talk list, the keynote titles and the affiliations. Until they arrive, show an explicit 'Talk list to be added' placeholder per session in the archive version instead of invented titles.
- **code-35** · low · riga 206: Mixed tabs/spaces and trailing whitespace; no formatter, linter or CI to catch regressions.
  - Correzione: Add .editorconfig, Prettier and html-validate (plus stylelint), and a GitHub Action that runs them on every PR. This matters because collaborators edit through the web UI and agents will work in parallel branches.
- **content-48** · low · riga 234: Day 3 items unchanged since the initial template. Azione: *verifica del team*.
  - Correzione: Ask what actually happened on Saturday Dec 20 and fix or remove these entries.
- **code-33** · low · riga 245: Images lack width/height (layout shift); AVIF logo has no fallback.
  - Correzione: Add intrinsic width/height attributes, use <picture> with an AVIF/WebP source and a PNG/SVG fallback, and prefer SVG for logos.
- **content-49** · low · riga 250: Registration status, free participation and accommodation info (team-written). Azione: *tenere*.
  - Correzione: Keep as archive facts. Fix the typo "Accomodation" and switch to past tense (drop "Details will be shared..."). Ask whether the same coverage model applies to Parma before reusing it there.
- **critic-11** · low · riga 255: Typos and an undefined reference in the team-written Lucca text. Azione: *tenere*.
  - Correzione: Keep the team's content but fix it when turning the page into an archive: 'Accommodation', 'Participation in the workshop', and name the hotel (Albergo Moderno) or drop 'the hotel'.
- **content-50** · medium · riga 268: "Submit Abstract" button links to "#". Azione: *eliminare*.
  - Evidenza: :266 `<h4>Call for Abstracts</h4>` / :267 `We invite PhD students and postdocs to submit abstracts for oral or poster presentations.` / :268 `<a href="#" class="btn btn-secondary" ...>Submit Abstract</a>`
  - Correzione: The 2025 event is over, so remove the box from the archive. On the Parma page, any abstract/registration CTA should be a disabled button reading "Feature not developed / opens TBD" until a real form URL exists.
- **code-30** · medium · riga 268: 'Submit Abstract' CTA is a dead href="#" link on a past event. Azione: *eliminare*.
  - Evidenza: events/lucca.html:266-268 `<h4>Call for Abstracts</h4> ... <a href="#" class="btn btn-secondary" ...>Submit Abstract</a>`
  - Correzione: On the archived Lucca page, remove the box. On the Parma page, either link a real form or render a disabled button labelled 'Abstract submission: not open yet / feature not developed'.
- **a11y-06** · medium · riga 288: EFC/PNRR funding acknowledgement is small low-contrast text and shrinks to 12px on mobile.
  - Evidenza: `<p style="font-size: 0.85rem; color: #888; ...">` gives 3.54:1 on white. Mobile rule at lucca.html:74-75: `.content p[style*="font-size: 0.85rem"] { font-size: 0.75rem !important;`
  - Correzione: Make the acknowledgement at least 14px with a grey of 4.5:1 or more (e.g. #636e72). Build one reusable 'funding acknowledgement' component for the Parma page so funder text is legible and consistent.
- **content-51** · low · riga 289: EFC network funding acknowledgment (likely required wording). Azione: *tenere*.
  - Correzione: Keep the first two sentences verbatim on the 2025 page. Ask whether Parma 2026 has the same funding before copying it.
- **content-52** · low · riga 289: Last sentence of the EFC paragraph is generic filler. Azione: *verifica del team*.
  - Correzione: Ask whether the EFC/IMT acknowledgement wording (all of lucca.html:289) was supplied by the funder. If not, delete the generic last sentence. Do not put lorem ipsum inside a funding acknowledgement.
- **a11y-12** · medium · riga 292: Funding logo banner has a meaningless alt text; the hero community photo has no text alternative.
  - Evidenza: `<img src="../pictures/EFC  Fascia Loghi (1260 x 145 px).png" alt="EFC Banner" ...>`. The image text reads 'Finanziato dall'Unione europea NextGenerationEU', 'Ministero dell'Università e della Ricerca', 'Italiadomani – Piano nazionale di ripresa e resilienza', EFC, 'IMT Scuola Alti Studi Lucca'. The group photo is CSS-only (`background-image: url('pictures/cover.png');` styles.css:62).
  - Correzione: Write alt text listing the funders and logos (in Italian with lang="it", or as an English summary), or add a visible caption. Use a real <img> with alt for the community photo when it carries meaning (e.g. 'FRS participants, IMT Lucca 2025').
- **content-53** · low · riga 292: EFC/NextGenerationEU/MUR/Italiadomani/IMT funding banner and IMT logo. Azione: *tenere*.
  - Correzione: Keep both on the Lucca 2025 page only, unchanged (PNRR logo rules). Rename the files to URL-safe names and improve the alt text (e.g. "Funded by the EU NextGenerationEU, MUR, Italiadomani, EFC, IMT").
- **code-24** · low · riga 292: Image filenames with spaces, a double space and parentheses are used unencoded in URLs.
  - Correzione: Rename to kebab-case ASCII (e.g. efc-logo-strip.png, imt-san-francesco.jpg, imt-logo.avif, cref-building.jpg), organise them as assets/img/<edition>/, and update references in one PR. Spaces are not valid in URL paths per the URL spec and break shell and agent tooling.
- **perf-04** · low · riga 292: Secondary images: no width/height, no lazy loading, oversized files, AVIF without fallback, filenames with spaces.
  - Correzione: Add width/height attributes, and loading="lazy" below the fold. Wrap the AVIF in <picture> with a PNG or WebP fallback (Safari before 16 cannot show it). Re-encode the photos. Rename assets to lowercase-kebab-case without spaces (e.g. pictures/funders-efc-banner.png) and organize them by edition (assets/editions/2026-parma/).
- **deploy-20** · low · riga 292: Image file names contain spaces, double spaces and parentheses.
  - Correzione: During the restyle, move images to site/assets/img/ with kebab-case names (efc-logo-banner.png, imt-campus.jpg, imt-logo.avif) and update the references. The CI link check (deploy-13) will catch broken paths.
- **critic-05** · low · riga 292: The mandatory EU/MUR/PNRR logo banner shrinks to about 38px tall on phones and becomes unreadable. Azione: *tenere*.
  - Correzione: On small screens, show the logos stacked or in two rows: use separate logo files or a second, narrower banner (via <picture>) so the 'Finanziato dall'Unione europea / NextGenerationEU' emblem and text stay legible. Check the minimum visibility the funding rules require.
- **code-09** · medium · riga 317: showDay() relies on the implicit global window.event, is duplicated 3x and has no tab semantics.
  - Evidenza: events/lucca.html:304-318 `function showDay(dayId) { ... event.target.classList.add('active'); }`, identical in events/frs2024-winter.html:408-417 and events/winter-2024.html:141-155. Called via `onclick="showDay('day1')"` (lucca.html:133-135). `document.querySelectorAll('.tab-button')` resets every tab button on the page.
  - Correzione: Make one shared tabs.js loaded with defer, using addEventListener and e.currentTarget (not the global event), role=tablist/tab/tabpanel, aria-selected, arrow-key navigation and optional #day2 deep links, scoped to its own tab group. If a button gains inner markup (icon or span), event.target is that child and the button loses its active state.

### `events/frs2024-winter.html` (33)

- **content-56** · low · riga 16: AI tagline and joke in the 2024 header (the real facts are fine). Azione: *sostituire con lorem ipsum*.
  - Correzione: Keep title and dates. Put lorem ipsum in the tagline or drop it, and reduce the venue to "CREF, Rome (Piazza del Viminale 1)".
- **content-28** · low · riga 25: "50+ young researchers" headcount not verifiable from the repo. Azione: *verifica del team*.
  - Correzione: Ask the organizers for the real headcount. The rest of the events.html:55 blurb is factual (5 senior talks and 32 talks are confirmed by the program): keep it, but drop "epic".
- **content-57** · medium · riga 35: "What on Earth is FRS?" intro paragraphs are AI jokes. Azione: *sostituire con lorem ipsum*.
  - Evidenza: `...what happens when you give a bunch of complex systems nerds from CREF Rome, IMT Lucca, and CSH Vienna the freedom to self-organize a workshop. Spoiler alert: it actually works!`; :38 `Born from the collective wisdom (and mild chaos)... everyone argues about the best null models over espresso.`
  - Correzione: Replace with lorem ipsum. Keep only the fact that FRS is self-organized by young researchers from CREF Rome, IMT Lucca and CSH Vienna.
- **content-58** · medium · riga 41: Edition history (v1.0 Lucca, v1.X Vienna) mixed with a joke. Azione: *verifica del team*.
  - Evidenza: `After a successful debut (v1.0) in Lucca and a bonus round (v1.X) in Vienna, version 2.0 landed at CREF in Rome. Think of it as academic speed-dating, but with more Laplacian matrices and fewer awkward silences.`
  - Correzione: Confirm the v1.0 and v1.X dates and places with the team. Keep the facts, delete the speed-dating sentence, and reuse the history on the about page and editions timeline.
- **code-15** · medium · riga 44: 154 inline style attributes (142 live) with heavily repeated patterns.
  - Evidenza: `grep -o 'style="'` per file: frs2024-winter 59 (12 inside the commented-out block, so 47 live), contact 31, lucca 23, event-template 18, winter-2024 13, about 9, events 1, index 0. Repeats: `style="margin-top: 3rem;"` 19x; `style="margin-top: 1.5rem; color: #2c3e50;"` 8x on day h4s; `style="color: #3498db; margin-bottom: 0.5rem;"` 6x on stat h2s; `width: 100%; padding: 0.8rem; border: 1px solid …
  - Correzione: During the restyle, set a hard rule of zero style= attributes, enforced by html-validate's no-inline-style rule (it already flags them with the config used here). Replace them with utility or component classes.
- **content-59** · medium · riga 48: "The Mission" card is generic AI copy. Azione: *sostituire con lorem ipsum*.
  - Evidenza: `<li>Connect emerging scientists across institutions</li>` ... :51 `Discuss career stuff that matters (but nobody talks about)` / :52 `Prove that young researchers can organize cool things`
  - Correzione: Replace with lorem ipsum (lines 45-54).
- **content-60** · low · riga 58: "The Science" topic list matches the real sessions. Azione: *tenere*.
  - Correzione: Keep, and drop "(obviously)".
- **content-41** · low · riga 71: Stats 3 days / 5 senior talks / 30+ talks / 1 quiz are backed by the program, but the captions are AI jokes. Azione: *tenere*.
  - Correzione: Keep the numbers and use neutral captions ("days", "keynotes", "contributed talks", "quiz").
- **code-31** · low · riga 71: Broken heading hierarchy: <h2> used for stat numbers, page titles are h2, no <main>.
  - Correzione: Use one h1 per page (the page or edition title), with sections as h2 and cards as h3. Use <p class="stat__value"> for numbers, and wrap content in <main>.
- **content-11** · medium · riga 87: Invented joke stats: "∞ potential collaborations" and "0 regrets". Azione: *eliminare*.
  - Evidenza: :87 `<h2 ...>∞</h2>` :88 `Potential collaborations sparked`; :91 `<h2 ...>0</h2>` :92 `Regrets (except maybe that last espresso at 9 PM)`
  - Correzione: Delete both cards (lines 86-93). Only stats backed by facts should stay (see content-41).
- **content-61** · low · riga 96: Commented-out "Inspiring Seniors" block with AI quips is still in the public source. Azione: *eliminare*.
  - Correzione: Delete the dead block (lines 96-129). Its full talk titles are useful for content-63, so move them there before deleting.
- **code-28** · low · riga 96: 34-line commented-out block (with 12 inline styles, tab-indented) left in the page. Azione: *eliminare*.
  - Correzione: Delete the commented markup (git history keeps it).
- **content-62** · low · riga 132: Program intro and day-tab nicknames are jokes. Azione: *sostituire con lorem ipsum*.
  - Correzione: Use plain day labels ("Wed 20 Nov") and drop or lorem-ipsum the intro sentence.
- **code-37** · low · riga 135: <button>s missing type attribute (html-validate no-implicit-button-type).
  - Correzione: Add type="button" to all non-submit buttons (tab buttons), handled in the shared tabs component.
- **code-16** · medium · riga 143: Schedule item types are encoded as ad-hoc inline background colours (Bootstrap alert palette) with no class or legend.
  - Evidenza: events/frs2024-winter.html:143 `<div class="schedule-item" style="background: #fff3cd;">` (opening), :167/:188/:213/:247/:269/:289/:329 `background: #d1ecf1;` (breaks), :219/:301 `#f8d7da` (quiz/dinner), :295 `#e7f3e7` (panel). On lucca.html every row is identical, so keynotes, breaks and social items look the same.
  - Correzione: Add modifiers such as .schedule-item--break/--keynote/--session/--social and include a data attribute or icon. Use the same component for the Parma programme.
- **content-64** · medium · riga 146: Invented joke captions under nearly every schedule item. Azione: *eliminare*.
  - Evidenza: :146 `Coffee, awkward hellos, and "wait, are you THE person who works on...?"`; :152 `Network structure meets renormalization`; :191 `Networking over carbs (it's a scientific necessity)`; :222 `Because nothing says "teamwork" like competitive trivia about eigenvalues`; :304 `Where "one more drink" happens multiple times`; :332 `Goodbyes, LinkedIn connections, and promises to actually collaborate` …
  - Correzione: Delete all the taglines. Keep only the real data: time, title, speaker, affiliation and venue (San Lorenzo for the dinner). Ask whether the panel (:297) had a real topic or panelists.
- **content-63** · low · riga 151: Senior-talk titles differ between the program and the commented block; affiliations need confirming. Azione: *verifica del team*.
  - Correzione: Ask the organizers for the official talk titles and speaker affiliations, and use one consistent version.
- **a11y-03** · medium · riga 167: Color-coded schedule rows push text below 3:1, and the color meaning has no legend.
  - Evidenza: Inline backgrounds: `style="background: #d1ecf1;"` (breaks, line 167), `#fff3cd` (openings, 143), `#f8d7da` (quiz/dinner, 219), `#e7f3e7` (panel, 295). On these, .schedule-time #3498db falls to 2.36-2.85:1 and .schedule-speaker #7f8c8d to 2.60-3.14:1.
  - Correzione: Replace the inline background tints with class variants (.slot--break, .slot--social) whose tints keep time, title and speaker text at 4.5:1 or more. No legend is needed, because the slot titles already state the type.
- **content-65** · low · riga 178: 2024 contributed-talk lists: real names and titles. Azione: *tenere*.
  - Correzione: Keep all four session lists verbatim. They are the most valuable archive content; consider structured markup (one row per talk).
- **a11y-17** · low · riga 178: Talk lists faked with bullet characters and <br>; schedule built from bare divs.
  - Correzione: Render each session as a list item: <ol> of slots with <time datetime>, and a nested <ul> of talks (speaker + title). Ideally generate this from one data file (YAML/JSON) per edition, so the Parma program is data, not hand-written HTML.
- **content-66** · medium · riga 319: Archive shows the CREF museum visits as held, but the page later says they were postponed. Azione: *verifica del team*.
  - Evidenza: :319 `MUSEO CREF 1` / :325 `MUSEO CREF 2`; :368 `...The visit was postponed...`
  - Correzione: Ask the team what actually happened on Friday 22 Nov. Mark the slot "cancelled/postponed" or remove it.
- **content-67** · medium · riga 341: "Survival Guide" still gives live logistics for a 2024 event. Azione: *eliminare*.
  - Evidenza: `<strong>The Solution:</strong> Meet at Piazza del Viminale, 1 by 8:45 AM. A CREF member will escort you through security.`; :346 `Osteria A piedi pari, Via dei Volsci, 82 (San Lorenzo)`; :347 `When: 20:45 (Thursday)` (vs :302 `21:00 - ∞`); :349 `Because networks are better discussed over wine and carbonara.`
  - Correzione: Remove the logistics section (lines 336-351) from the archive. At most keep one line: "Social dinner at Osteria A Piedi Pari, San Lorenzo". Delete the jokes and the phone number (content-02).
- **content-02** · high · riga 342: Personal mobile phone number published on a public archive page. Azione: *eliminare*.
  - Evidenza: `<p><strong>Running Late?</strong> Text Giulio ([numero rimosso]) with your ETA and name.</p>`
  - Correzione: Delete the line from the page and from the deploy branch right away. The event ended in Nov 2024, so the instruction has no use. The number is also on the currently served frs-workshop.imtlucca.it host and in git history. Rewriting history is the team's call, but at least make sure the new deploy branch never contains it.
- **code-41** · medium · riga 342: Personal mobile number still published on an archived event page. Azione: *verifica del team*.
  - Evidenza: events/frs2024-winter.html:342 `<p><strong>Running Late?</strong> Text Giulio ([numero rimosso]) with your ETA and name.</p>`
  - Correzione: Remove day-of logistics (phone numbers, meeting times) from archived edition pages. For live editions, use a shared organisers' contact rather than a personal number.
- **seo-10** · low · riga 342: Personal mobile phone number published on an indexed page. Azione: *verifica del team*.
  - Correzione: Confirm with the owner whether it should stay public. On an archive page it no longer helps anyone; remove it or replace it with the shared mailbox.
- **critic-12** · low · riga 347: The 2024 page gives two different times for the social dinner. Azione: *verifica del team*.
  - Correzione: For the archive, keep one time confirmed by the team, or drop the logistics entirely (see content-67).
- **content-68** · low · riga 357: Real Italian quotes from the organizing committee (one under a misleading heading). Azione: *tenere*.
  - Correzione: Keep both quotes verbatim and attribute both to the committee. Rename the :355 heading, since these are the committee's words, not participant feedback.
- **a11y-16** · low · riga 357: Italian passages on lang="en" pages are not marked lang="it".
  - Correzione: Wrap Italian quotes in <span lang="it"> or <blockquote lang="it">. Decide the site language strategy (English with Italian quotes, or bilingual) before building the Parma page.
- **content-69** · low · riga 361: Unverified claim about enthusiastic responses to the call for organizers. Azione: *verifica del team*.
  - Correzione: Ask the team whether this happened. If not, delete it; if yes, state it in one neutral sentence.
- **content-70** · medium · riga 368: Museum anecdote names a real family and an unexplained incident. Azione: *verifica del team*.
  - Evidenza: `Friday's museum visit hit an unexpected snag due to events involving the Amaldi Family, leading to interviews at the museum. The visit was postponed, but hey, that's research life...`; :369 `The organizing committee promised a better museum experience for future visits. We hold them to it.`
  - Correzione: Ask the organizers whether this is accurate and appropriate to publish. The default is to delete the whole "Plot Twist" box (lines 365-370) and keep only "museum visit postponed" in the program.
- **content-71** · medium · riga 375: "Why FRS Matters" checklist is generic AI copy. Azione: *sostituire con lorem ipsum*.
  - Evidenza: `✅ Young researchers can present half-baked ideas without judgment` / `✅ "Stupid questions" are celebrated (because they're never actually stupid)` / `✅ Collaborations start over espresso, not through formal emails`
  - Correzione: Replace with lorem ipsum (lines 372-381). If the team writes a real values statement, it belongs on the about page.
- **content-72** · medium · riga 385: "Actively recruiting" call from 2024 plus filler. Azione: *eliminare*.
  - Evidenza: `From Lucca (v1.0) to Vienna (v1.X) to Rome (v2.0), FRS is building something special. The organizing committee is actively recruiting new members to keep the momentum going.`
  - Correzione: Drop it from the archive. The edition timeline belongs on the editions page (Lucca 2025 and Parma 2026 included), and any current recruitment message belongs on about/contact.
- **content-12** · medium · riga 395: Invented "Fun Fact" with jokes attributed to participants. Azione: *eliminare*.
  - Evidenza: `FRS stands for "Fostering Research Synergies," but participants joke it also means "Free Research Spirit," "Finding Research Soulmates," or "Finally, Real Science (discussions)".`
  - Correzione: Delete the whole box (lines 393-396). It attributes invented jokes to real participants.

### `styles.css` (20)

- **code-20** · medium · riga 2: Global margin:0 reset with no spacing restored, so paragraphs and headings run together.
  - Evidenza: styles.css:2-6 `* { margin: 0; padding: 0; box-sizing: border-box; }`. There is no p, ul or h* margin rule anywhere. The three consecutive <p> at frs2024-winter.html:34-42 have zero spacing (375px screenshot: "...it actually works! Born from the collective..." on the next line with no gap). Pages compensate ad hoc with 19x inline `margin-top: 3rem`.
  - Correzione: Add a flow or stack rule (e.g. `.prose > * + * { margin-top: 1em }`) and heading spacing tokens, then drop the inline margins.
- **a11y-10** · low · riga 55: No focus styles at all; hover feedback has no keyboard equivalent.
  - Correzione: Add a global :focus-visible ring (e.g. 3px solid with offset) of at least 3:1 against both the element and its background, including on photo heroes and the dark navbar. Mirror hover states on :focus-visible.
- **code-18** · medium · riga 57: Multiple text/background pairs fail WCAG AA contrast (4.5:1).
  - Evidenza: Computed ratios: nav active/hover #3498db on #2c3e50 = 3.48 (styles.css:57); .btn-secondary/active tab white on #3498db = 3.15 (:122, :352); .schedule-time #3498db on white = 3.15 (:270); .event-date/.schedule-speaker #7f8c8d on white = 3.48 (:225, :281); .badge-past white on #95a5a6 = 2.56 (:220); .badge-upcoming white on #27ae60 = 2.87 (:215); 'Fun Fact' #f39c12 on #fff9e6 = 2.08 …
  - Correzione: Choose tokens that pass AA (e.g. a darker blue such as #1f6fb2 on white) and check them with a contrast checker in CI or the design review.
- **content-55** · medium · riga 62: Group photo of ~19 identifiable people used as the hero on every page, with no alt text or credit. Azione: *verifica del team*.
  - Evidenza: `background-image: url('pictures/cover.png');` (applies to `.hero` on index.html, about.html, contact.html, events.html); the image is a real group photo taken in a frescoed room.
  - Correzione: Keep it only if the team confirms which FRS edition it shows and that all ~16 people pictured agreed to public use. Because it is a CSS background, add a caption or credit and an accessible description in the new design.
- **code-21** · medium · riga 62: Hero uses a 641x486, 617 KB PNG stretched full-width (blurry, faces cropped) on 4 pages; event headers are also upscaled. Azione: *verifica del team*.
  - Evidenza: styles.css:62 `background-image: url('pictures/cover.png');` with `background-size: cover` (:63). `file` reports `cover.png: PNG image data, 641 x 486` (617229 bytes). In the 1440px screenshot the image is upscaled about 2.25x, the top row of heads is cut off and the headline sits over faces. The event headers use Centro_Ricerche_Enrico_Fermi.jpg 1199x406 and 'Scuola IMT Campus SF.jpg' 866x238 as …
  - Correzione: Export the photos at 1920-2400px as WebP/AVIF with a JPEG fallback (~150-250 KB) and set background-position to keep faces in frame, or use an <img> with object-fit and object-position. Give each page its own hero.
- **mob-04** · medium · riga 62: Hero photos are low resolution, upscaled to full width and badly cropped (faces cut).
  - Evidenza: `background-image: url('pictures/cover.png');` is 641x486 drawn into a 1425x385 hero at 1440px (about 2.2x upscale, more on 1920px or 2x screens). The aspect ratio is 1.32:1 vs about 3.7:1, so with background-size: cover the heads of the standing people on the left are cut off in the desktop screenshot. `Scuola IMT Campus SF.jpg` (866x238) fills a 1425x202 header (1.65x).
  - Correzione: Get originals at least 2400px wide. Serve responsive variants (image-set()/srcset at 800/1600/2400 in WebP/AVIF with JPEG fallback). Set a focal point (background-position or object-position) per image, and pick hero heights and aspect ratios that suit group photos.
- **code-19** · medium · riga 102: .btn does not reset <button> styles, and .btn-primary is white on white.
  - Evidenza: styles.css:102-109 `.btn` sets padding, radius and weight but no `border`, `font: inherit` or `cursor`, so contact.html:52 'Subscribe' and :80 'Send Message' render in the user-agent font with a user-agent border. The 375px screenshot shows the smaller system font and grey bevel. :111-114 `.btn-primary { background-color: white; color: #667eea; }` is used on a white section (contact.html:80) and …
  - Correzione: Add `font: inherit; border: 0; cursor: pointer;` to .btn and .tab-button, and define primary/secondary/ghost variants with explicit contrast for each background.
- **a11y-05** · medium · riga 111: btn-primary is a white button with low-contrast purple text, and its edges are invisible on light backgrounds.
  - Evidenza: `.btn-primary { background-color: white; color: #667eea; }` gives 3.66:1 text. On contact.html:80 (`<button type="submit" class="btn btn-primary">Send Message</button>`) the button sits on the white page (1.00:1 boundary); on event-template.html:89 it sits on #ecf0f1 (1.15:1). #667eea is a leftover from the template's purple gradient.
  - Correzione: Fix the #667eea text colour (3.66:1) with a dark accent of 4.5:1 or more, and drop the template purple. Add a proper button reset to .btn (border, font: inherit, appearance) so <button> and <a> buttons render the same. Provide a solid variant for light backgrounds and an outline/white variant for photo heroes, with boundaries of at least 3:1.
- **a11y-01** · high · riga 121: Brand accent #3498db fails WCAG AA in every use (buttons, active tab, links, schedule times, active nav).
  - Evidenza: white on #3498db = 3.15:1 (.btn-secondary styles.css:121-124; .tab-button.active :351-355; about.html:62 gradient start `#3498db 0%`). #3498db text on white = 3.15:1 (.schedule-time :268-272; contact.html:31-41 links). #3498db on navbar #2c3e50 = 3.48:1 (.nav-menu a.active :55-58). Hover #2980b9 = 4.30:1.
  - Correzione: Define color tokens in :root. Use a darker accent for fills and text on light backgrounds, e.g. #2471a3 (5.30:1 with white). On the dark navbar use a light tint such as #85c1e9 (5.65:1) plus a non-color indicator (underline). Check each pair of the new palette with a contrast script.
- **code-23** · low · riga 168: Hover lift on non-interactive cards suggests they are clickable; no reduced-motion handling; transition: all.
  - Correzione: Apply hover effects only to elements that are links (e.g. a.card or .card:has(a) with the whole card clickable). Transition specific properties only, and wrap motion in @media (prefers-reduced-motion: no-preference).
- **a11y-18** · low · riga 168: Non-interactive cards lift on hover (false affordance); no prefers-reduced-motion handling.
  - Correzione: Use hover elevation only on cards that are links (make the whole event card a link). Wrap transitions and transforms in @media (prefers-reduced-motion: no-preference).
- **code-39** · low · riga 180: Card-like components redeclare identical surface styles.
  - Correzione: Use one .surface/.card base plus modifiers, with radius and shadow coming from tokens.
- **a11y-04** · medium · riga 214: Status badges 'Upcoming' and 'Past' fail even the 3:1 threshold at small size.
  - Evidenza: .badge-upcoming white on #27ae60 = 2.87:1. .badge-past white on #95a5a6 = 2.56:1 (styles.css:219-222). Both at `font-size: 0.85rem;` (styles.css:210). Used on events.html:32 and 52.
  - Correzione: Use e.g. #1e8449 (4.72:1) for upcoming and #5f6b6d (5.51:1) for past, or dark text on light tints. Generate badges from event data so a past event is never labeled 'Upcoming'.
- **a11y-02** · medium · riga 225: Secondary grey #7f8c8d (event dates, speakers, news date) is 3.48:1 on white.
  - Evidenza: `color: #7f8c8d;` in .event-date (styles.css:225), .schedule-speaker (:281) and .date (:312) gives 3.48:1. It is used for every event date (events.html:30, 50), every speaker line on events/lucca.html and index.html:49 `<p class="date">October 2025</p>`.
  - Correzione: Replace with a grey of at least 4.5:1, e.g. #5f6b6d (5.51:1) or #636e72 (5.24:1). Do not convey key facts (dates, venue) in de-emphasized grey.
- **code-17** · medium · riga 237: Leftover purple #667eea/#764ba2 from the generator alongside the flat-UI blue palette; 23 hard-coded colours and no custom properties.
  - Evidenza: styles.css:113 `.btn-primary { ... color: #667eea; }`; :237 `background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);` (the purple header is visible on events/winter-2024.html in a 1440px screenshot). There are 24x #2c3e50 and 23x #3498db (plus one `#3498DB` at frs2024-winter.html:366) and 23 distinct hex values across CSS and HTML. `grep -c -- '--' styles.css` gives 0, so there are no CSS …
  - Correzione: Define design tokens in :root (--color-primary, --color-ink, --color-surface, --radius, --shadow, --space-*) and replace every literal colour. Pick one brand palette for the restyle.
- **code-38** · low · riga 323: Footer margin-top leaves a 3rem white strip after tinted sections; magic-number spacing.
  - Correzione: Remove the footer margin, let sections own their padding, and define a spacing scale (--space-1..8) plus 2-3 named breakpoints.
- **code-10** · low · riga 357: Program days 2-3 are hidden with no JS fallback and do not print.
  - Correzione: Show all days by default and let JS add a `.js-tabs` class that enables hiding. Add @media print { .program-day { display:block } }.
- **code-14** · medium · riga 366: Mobile fixes for event headers exist only in lucca.html, so other event pages get oversized titles; tab rules are duplicated.
  - Evidenza: events/lucca.html:16-23 shrinks `.event-detail-title` to 1.8rem and stacks `.event-info` only on that page. styles.css has no such rule, and a screenshot of frs2024-winter.html at 375px shows the 2.5rem title wrapping over 3 lines and taking ~550px of the header. lucca.html:49-58 repeats styles.css:392-398 (`.program-tabs {flex-direction: column}`, `.tab-button {width:100%}`).
  - Correzione: Consolidate all responsive rules in the global stylesheet and use clamp() for heading sizes (e.g. font-size: clamp(1.75rem, 4vw, 2.75rem)).
- **mob-02** · medium · riga 366: No compact mobile nav: the sticky header stacks brand and links and covers 17-22% of the screen.
  - Evidenza: `.navbar { ... position: sticky; top: 0;` (styles.css:25-26). The mobile rule only sets `flex-direction: column;` (367-370). Measured sticky nav height: 150px at 320px (brand h1 wraps to 2 lines, 77px) and 112px at 375px, on a 667px-tall viewport. Nav links are bare text, about 26px tall.
  - Correzione: On small screens use a short brand (logo or 'FRS') and a disclosure/hamburger menu (button with aria-expanded) or a single-row scrollable link bar. Keep the header at about 56-64px or make it non-sticky / hide on scroll. Give links at least 44px tap height.
- **code-36** · low · riga 366: On mobile the sticky navbar stacks to ~110px and permanently covers ~13% of the viewport; brand is not a link.
  - Correzione: Use a compact single-row mobile header (short logo plus menu toggle), or make the navbar non-sticky below 768px. Wrap the brand in <a href="/">.

### `contact.html` (19)

- **content-38** · low · riga 15: Generic contact hero and intro copy. Azione: *sostituire con lorem ipsum*.
  - Correzione: Replace with lorem ipsum, or simply "Contact" plus the email.
- **code-04** · medium · riga 21: Inline grid-template-columns overrides the mobile media query, so contact stays two columns at 375px.
  - Evidenza: contact.html:21 `<div class="grid" style="grid-template-columns: 1fr 1fr;">` beats styles.css:388-390 `@media (max-width:768px){ .grid { grid-template-columns: 1fr; } }`. The headless Chrome screenshot at 375px shows two ~150px columns, with the form squeezed beside the contact text. The same pattern is in events/event-template.html:31 `style="grid-template-columns: 2fr 1fr;"`, which a new Parma …
  - Correzione: Remove the inline grid definitions and add layout modifier classes (.grid--2col, .grid--main-aside) in the stylesheet, each with its own mobile breakpoint.
- **mob-01** · medium · riga 21: Inline two-column grid overrides the mobile rule: squeezed form at 375px, horizontal scroll at 320px.
  - Evidenza: contact.html:21 `<div class="grid" style="grid-template-columns: 1fr 1fr;">` beats styles.css:388-390 `.grid { grid-template-columns: 1fr; }`. Headless Chrome: at 375px the columns are `172.875px 130.125px` (inputs about 130px wide); at 320px `scrollWidth 347 > 320`, with the 'Send Us a Message' column overflowing.
  - Correzione: Remove inline layout styles. Use a class such as .two-col that collapses in the stylesheet's media query. Add a CI or manual check at 320/375px for horizontal overflow.
- **content-01** · critical · riga 31: Fake contact emails on a real third-party domain (phdnetwork.org) with a live mail server. Azione: *eliminare*.
  - Evidenza: contact.html:31 `General inquiries: <a href="mailto:info@phdnetwork.org"...` / :32 `Event registration: <a href="mailto:events@phdnetwork.org"`; `dig +short phdnetwork.org MX` -> `0 phdnetwork-org.mail.protection.outlook.com.` (domain resolves to 172.67.171.89). Blame: unchanged since template commit bd3a33e.
  - Correzione: Remove both addresses now. Replace them with the real address frscrefimt@gmail.com as a mailto link (or another address the team confirms). Never invent addresses: emails sent to these go to an unrelated organisation.
- **code-03** · high · riga 31: Contact links point to the generator's fake domain and to href="#". Azione: *verifica del team*.
  - Evidenza: contact.html:31 `<a href="mailto:info@phdnetwork.org" ...>info@phdnetwork.org</a>`; :32 `mailto:events@phdnetwork.org`; :40 `Twitter: <a href="#" ...>@PhDNetwork</a>`; :41 `LinkedIn: <a href="#" ...>`. The real address used elsewhere is frscrefimt@gmail.com (about.html:65, lucca.html:276).
  - Correzione: Replace with the real address, or with a single source-of-truth include. Remove the social links unless real handles exist. Otherwise show a lorem/'not available' marker rather than a fake handle.
- **deploy-11** · high · riga 31: Placeholder addresses use a real third-party domain with a working mail server, so mail meant for the team leaks to strangers. Azione: *aggiornare (scaduto)*.
  - Evidenza: contact.html:31 `General inquiries: <a href="mailto:info@phdnetwork.org"`; :32 `mailto:events@phdnetwork.org`; `dig MX phdnetwork.org` -> `0 phdnetwork-org.mail.protection.outlook.com.`; the real address appears elsewhere: about.html:65 `frscrefimt@gmail.com`, events/lucca.html:276 `frscrefimt@gmail.com`
  - Correzione: Replace these with the real team address (frscrefimt@gmail.com), or with a marker that obviously cannot be sent to. Add a rule for agents to .claude: placeholder emails, URLs and handles must use reserved domains (example.org, .invalid) or lorem ipsum, never names that look real such as phdnetwork.org or @PhDNetwork.
- **content-10** · medium · riga 40: Fake Twitter handle from the template (@PhDNetwork) with a dead link. Azione: *eliminare*.
  - Evidenza: `Twitter: <a href="#" style="color: #3498db;">@PhDNetwork</a><br>` (blame: template commit bd3a33e)
  - Correzione: Delete. @PhDNetwork is not an FRS account and may belong to someone else. Only list social accounts the team actually runs.
- **a11y-14** · low · riga 40: Dead href="#" links (fake social handles, Submit Abstract, Register Now). Azione: *eliminare*.
  - Correzione: Delete the fake @PhDNetwork/LinkedIn links unless the team supplies real FRS accounts. Remove the 'Call for Abstracts / Submit Abstract' box from the archived Lucca 2025 page. On the new Parma page, render any not-yet-available action as a non-link element with a visible 'not developed / coming soon' marker, never href="#".
- **content-36** · medium · riga 41: LinkedIn entry links to "#". Azione: *verifica del team*.
  - Evidenza: `LinkedIn: <a href="#" style="color: #3498db;">Fostering Research Synergies</a>`
  - Correzione: Ask the team whether an FRS LinkedIn page exists. If it does, link it; if not, delete the entry.
- **code-02** · high · riga 51: Mailing-list 'Subscribe' widget is inert: no form, no handler, no name, no label. Azione: *marcare come non sviluppato*.
  - Evidenza: contact.html:51 `<input type="email" placeholder="Your email address" style="...">` (no name/label/form); line 52 `<button class="btn btn-secondary" style="margin-top: 1rem;">Subscribe</button>` (no type, no onclick, not inside a <form>)
  - Correzione: Delete it, or turn the box into a clearly labelled 'Mailing list: feature not developed' placeholder until a real list (Google Group or similar) exists.
- **content-09** · medium · riga 51: Mailing-list Subscribe box is non-functional. Azione: *marcare come non sviluppato*.
  - Evidenza: `<input type="email" placeholder="Your email address" ...>` / :52 `<button class="btn btn-secondary" style="margin-top: 1rem;">Subscribe</button>`; :48 `Join our mailing list to receive updates about upcoming events and opportunities.`
  - Correzione: Ask whether a mailing list exists. If not, remove the box or mark it "Feature not developed: mailing list" and disable the input and button.
- **deploy-12** · medium · riga 51: The mailing-list subscribe box and the social links do nothing but look real. Azione: *marcare come non sviluppato*.
  - Evidenza: contact.html:51 `<input type="email" placeholder="Your email address" ...>`; :52 `<button class="btn btn-secondary" style="margin-top: 1rem;">Subscribe</button>` (not inside any form); :40 `Twitter: <a href="#" style="color: #3498db;">@PhDNetwork</a>`; :41 `LinkedIn: <a href="#" ...>Fostering Research Synergies</a>`
  - Correzione: Mark the subscribe box as 'Mailing list: not developed yet'. Remove the social links, or mark them as not available until real accounts exist. '@PhDNetwork' may belong to someone else.
- **content-08** · high · riga 59: Contact form does nothing, and submitting it puts personal data in the URL. Azione: *marcare come non sviluppato*.
  - Evidenza: `<form style="margin-top: 2rem;">` (no action/method) ... :80 `<button type="submit" class="btn btn-primary">Send Message</button>`. Name, email, subject and message are `required` (:62-77). The default GET submit appends them to contact.html?... over plain HTTP (https not enforced).
  - Correzione: Either connect a real backend (Formspree/Google Form) or replace the form with a visibly disabled box labelled "Feature not developed" plus a mailto:frscrefimt@gmail.com link. Until then, the form must not accept personal data.
- **code-01** · high · riga 59: Contact form has no action/method: submitting sends nothing and puts personal data in the URL. Azione: *marcare come non sviluppato*.
  - Evidenza: contact.html:59 `<form style="margin-top: 2rem;">` (no action/method); line 80 `<button type="submit" class="btn btn-primary">Send Message</button>`; line 84 public dev note: "Note: This is a static form. To make it functional, you'll need to integrate with a form service like Formspree..."
  - Correzione: Remove the form, or replace it with an explicit 'Feature not developed' box and a mailto: link to the real address. If a form is wanted later, wire it to a real endpoint (Formspree or Google Form) and use method=POST. Delete the developer note from the public page.
- **a11y-13** · high · riga 59: Contact form and mailing-list signup look functional but do nothing; the signup field has no label. Azione: *marcare come non sviluppato*.
  - Evidenza: contact.html:59 `<form style="margin-top: 2rem;">` has no action/method, so Send reloads contact.html?name=... and the message is lost. contact.html:51 `<input type="email" placeholder="Your email address" ...>` has no label and no name. contact.html:52 `<button class="btn btn-secondary" ...>Subscribe</button>` has no handler. A public developer note at contact.html:84 reads `Note: This is a …
  - Correzione: Either connect them to a real service (Google Form or Formspree link) or replace each box with an explicit 'Not developed yet' marker and disabled controls (aria-disabled, visible badge), as the team asked for honest placeholders. Remove the developer note. Give every input a <label> and borders of 3:1 or more.
- **deploy-10** · high · riga 59: The contact form has no action, so it sends name, email and message as URL parameters over plain HTTP, and the message goes nowhere. Azione: *marcare come non sviluppato*.
  - Evidenza: contact.html:59 `<form style="margin-top: 2rem;">` (no action and no method, so it defaults to GET to contact.html); fields :62 `name="name"`, :67 `name="email"`, :77 `name="message"`; :84 `Note: This is a static form. To make it functional, you'll need to integrate with a form service`; the site is HTTP-only (deploy-02)
  - Correzione: Remove the working form. Replace it with a clearly labelled box such as 'Contact form: not developed yet. Please write to frscrefimt@gmail.com', with the inputs disabled or removed. If a form service is added later (Formspree, Google Forms), it must run over HTTPS and come with a short privacy note (GDPR: who receives the data and how long it is kept).
- **critic-08** · low · riga 62: Form fields use the browser's default font size (iOS zooms on focus) and the textarea renders in monospace.
  - Correzione: If a form is kept or added (e.g. Parma registration or mailing list), add a base rule: input, textarea, select, button { font: inherit; font-size: max(16px, 1rem); }. This stops iOS Safari from zooming and keeps the textarea from defaulting to monospace.
- **content-07** · medium · riga 84: Developer note shown to visitors under the contact form. Azione: *eliminare*.
  - Evidenza: `Note: This is a static form. To make it functional, you'll need to integrate with a form service like Formspree, Google Forms, or your own backend.`
  - Correzione: Delete (lines 83-85). If a form stays without a backend, use a short, honest UI marker such as "[Feature not developed: contact form not connected]" and send visitors to the email.
- **content-37** · medium · riga 92: "Organizing Committee" box names nobody. Azione: *sostituire con lorem ipsum*.
  - Evidenza: `Our events are organized by a dedicated team of PhD students and postdocs. If you're interested in joining the organizing committee or have suggestions for future events, please reach out!`
  - Correzione: Ask for the real committee per edition (names, affiliations, consent to be listed). Until then, show a lorem-ipsum people grid marked as placeholder.

### `index.html` (19)

- **code-32** · low · riga 5: No meta description, Open Graph/Twitter tags or favicon on any page.
  - Correzione: Add per-page description and og:title/og:image (Jekyll SEO tag plugin is supported on GitHub Pages) plus a favicon set. This matters for sharing the Parma page in chats and mailing lists.
- **seo-01** · high · riga 6: No meta description, Open Graph or Twitter Card tags on any page: WhatsApp/Slack/LinkedIn previews show a bare title with no image.
  - Evidenza: grep -E 'name="description"\|og:\|twitter:' over all *.html -> 0 matches. index.html:3-9 <head> contains only charset, viewport, `<title>Fostering Research Synergies</title>`, styles.css and navbar.js. index.html has no <img> at all (hero is a CSS background), so scrapers have no image to pick.
  - Correzione: Add one shared head include (via a build step or Jekyll _includes) to every page with a per-page meta description, og:title/og:description/og:url/og:type and og:image. og:image must be an absolute https URL on fosteringresearchsynergies.github.io, 1200x630, JPEG under about 300 KB (WhatsApp often drops larger images). Also add twitter:card=summary_large_image and og:locale. Give the Parma page its own og:image and description.
- **seo-04** · medium · riga 6: No canonical links, robots.txt or sitemap.xml.
  - Evidenza: Live GET /robots.txt -> 404, /sitemap.xml -> 404. grep 'rel="canonical"' in repo *.html -> 0 matches.
  - Correzione: Add rel=canonical on every page pointing to its https github.io URL. Add a sitemap.xml listing only the real pages (home, events, about, contact, each edition including Parma) and a robots.txt that points to it. Submit the sitemap in Google Search Console after the domain move.
- **deploy-19** · medium · riga 6: Old URLs will break after the move: no redirect plan, canonical URLs, sitemap, robots.txt or custom 404.
  - Evidenza: Pages `"custom_404":false`; `/nonexistent` -> `<title>Page not found &middot; GitHub Pages`; `/robots.txt` 404, `/sitemap.xml` 404; no `canonical`, `og:` or meta description in any page (grep is empty); org `"blog":null`, repo `"homepage":null`
  - Correzione: Ask IMT IT for a path-preserving 301 redirect from frs-workshop.imtlucca.it (deploy-03 step 1). Add site/404.html, site/robots.txt and site/sitemap.xml, plus `<link rel="canonical" href="https://fosteringresearchsynergies.github.io/...">` and OG tags in the restyled head. [OUTWARD] `gh api -X PATCH orgs/FosteringResearchSynergies -f blog=https://fosteringresearchsynergies.github.io/`. Ask IMT and EFC to update any news pages that link to the old host.
- **seo-06** · low · riga 7: No favicon, apple-touch-icon, theme-color or manifest.
  - Correzione: Add an SVG favicon plus 32px PNG/ICO fallback, a 180x180 apple-touch-icon and a <meta name="theme-color">. Slack and some share cards show the site icon, and browser tabs and bookmarks currently show a generic icon.
- **perf-03** · low · riga 8: Render-blocking navbar.js in <head> injects the header after DOMContentLoaded, causing layout shift.
  - Correzione: Emit the header as static HTML at build time (also fixes seo-05 and a11y-08). If any JS remains, load it with defer and never insert layout-affecting content above the fold.
- **perf-02** · low · riga 12: The likely LCP image is a CSS background, found late and not prioritized.
  - Correzione: Render the hero photo as an <img> (or <picture>) with width/height, fetchpriority="high" and decoding="async", and overlay the text with CSS. Alternatively, preload it with imagesrcset.
- **content-20** · medium · riga 14: Generic home hero with no concrete facts. Azione: *sostituire con lorem ipsum*.
  - Evidenza: `<h2>Welcome to Our Research Community</h2>` / :15 `An informal association of PhD students and postdoctoral researchers fostering collaboration and knowledge exchange through workshops and conferences.`
  - Correzione: Replace with lorem ipsum until the team writes a real one-liner. A real version would name what FRS is: a self-organized complex-systems workshop by young researchers from CREF, IMT Lucca and CSH Vienna. Also ask whether FRS should be called an "association" at all; it isn't a legal entity as far as the repo shows.
- **seo-07** · medium · riga 14: Home title and heading do not say what FRS is (no 'workshop', 'complex systems', CREF/IMT/CSH). Azione: *verifica del team*.
  - Evidenza: index.html:6 `<title>Fostering Research Synergies</title>`. index.html:14 `<h2>Welcome to Our Research Community</h2>`. The home page body never mentions complex systems or the partner institutes.
  - Correzione: The team should write a real one-line description, e.g. title 'Fostering Research Synergies – workshop for young researchers in complex systems', and reuse it for the meta description and og:description. Until it exists, use clearly marked lorem ipsum, not generic AI copy.
- **content-21** · medium · riga 16: Home CTA "View Upcoming Events" leads to a list whose only upcoming event is past. Azione: *aggiornare (scaduto)*.
  - Evidenza: `<a href="events.html" class="btn btn-primary">View Upcoming Events</a>`
  - Correzione: Point the CTA at the Parma 2026 page once it exists, otherwise at "All editions".
- **a11y-09** · medium · riga 20: No <main> landmark, no skip link, current page shown by color only.
  - Evidenza: grep '<main\|skip\|aria-' over repo -> 0 matches. Accessibility tree of events/lucca.html: only navigation, banner and contentinfo landmarks. Active nav item shown only via `.nav-menu a.active { color: #3498db; }` (styles.css:55-58), 3.15:1 against the inactive white links.
  - Correzione: Wrap page content in <main id="content">. Add a visible-on-focus 'Skip to content' link before the sticky header. Add aria-current="page" to the active nav link plus a non-color indicator (underline or bar).
- **a11y-11** · low · riga 27: 52 emoji used as icons across 8 pages, none aria-hidden, many inside headings.
  - Correzione: Replace emoji with a small inline SVG icon set marked aria-hidden="true" and focusable="false". Expose meaning as text (e.g. a <dl> with Date/Venue/Participants, or visually-hidden labels). Keep icons out of heading text.
- **content-22** · low · riga 28: "Who We Are" card is generic filler. Azione: *sostituire con lorem ipsum*.
  - Correzione: Use lorem ipsum until the team writes it.
- **content-23** · low · riga 32: Event-frequency claim "1-2 times per year" (repeated in about.html:28) does not match the known history. Azione: *verifica del team*.
  - Correzione: Ask the team for the actual cadence. The repo is ambiguous: 2023 apparently had two editions (v1.0 Lucca and v1.X Vienna, per frs2024-winter.html:41 and :357), then one per year after that, while lucca.html:113 says 'annual'. Also ask whether FRS runs 'conferences' or only the workshop. Fix index.html:32 and about.html:28 together.
- **content-24** · medium · riga 36: "Join Us" implies participation is open to any PhD/postdoc. Azione: *verifica del team*.
  - Evidenza: `Whether you're a PhD student or postdoc, you're welcome to participate in our events and become part of our growing community.`
  - Correzione: Ask the team who can attend: anyone, or affiliated institutions plus invited guests (lucca.html:113 mentions IMT Lucca and CREF 'along with other young researchers'). Until then, use lorem ipsum.
- **content-17** · high · riga 48: "Latest News" is a year-old teaser. Azione: *aggiornare (scaduto)*.
  - Evidenza: `<h4>Next Event Announcement Coming Soon</h4>` / :49 `<p class="date">October 2025</p>` / :50 `We're planning our next workshop! Details will be announced in the coming weeks. Stay tuned for registration information.`
  - Correzione: Replace it with a Parma 2026 announcement. Use real facts only (city, year). Put lorem ipsum or "dates TBD" where details aren't decided.
- **code-05** · high · riga 57: No templating: head, nav include, hero and footer are hand-copied across 8 pages and have already drifted. Azione: *aggiornare (scaduto)*.
  - Evidenza: The `<footer>` block appears in all 8 HTML files, in two variants: index.html:59 `&copy; 2025 Fostering Research Synergies. All rights reserved.` vs events/frs2024-winter.html:402 `&copy; 2024-2025 ... Self-organized by young researchers, for young researchers.` The year is stale (today is 2026-10-20). The same `<head>` boilerplate (charset/viewport/title/styles.css/navbar.js) is repeated in all …
  - Correzione: GitHub Pages already runs Jekyll, so use _layouts/default.html with _includes/head.html, nav.html and footer.html, and set the page title through front matter. This also removes the need for navbar.js.
- **critic-03** · medium · riga 59: No privacy notice anywhere, although the site publishes identifiable photos and ~40 named people and will need registration for Parma. Azione: *verifica del team*.
  - Evidenza: index.html:59 footer only: "&copy; 2025 Fostering Research Synergies. All rights reserved."; no privacy/imprint page in git ls-files; frs2024-winter.html:178-285 lists 33 named speakers; styles.css:62 hero = group photo
  - Correzione: Add a short privacy and contact notice (who runs the site, the contact address, how to ask for a photo or name to be removed, and what a Parma registration form collects and why) and link it from the footer. Add it before any registration form goes live. The team must write or approve the text; do not use lorem ipsum for legal content.
- **content-73** · low · riga 59: Footer copyright years are stale on every page. Azione: *aggiornare (scaduto)*.
  - Correzione: Use one shared footer with a computed or current year range. Keep the institution line (add Parma's host once confirmed) and drop the slogan.

### `events.html` (12)

- **critic-09** · low · riga 15: Unclassified events.html hero copy: generic, and claims 'conferences'. Azione: *sostituire con lorem ipsum*.
  - Correzione: Replace with a plain factual subtitle (e.g. the list of editions/cities) or with lorem ipsum until the team writes one. FRS runs a workshop series, not conferences.
- **deploy-13** · medium · riga 20: No CI or HTML checks: invalid markup has gone live unnoticed.
  - Evidenza: `gh api .../actions/workflows` -> only `"path":"dynamic/pages/pages-build-deployment"`; no .github/ directory; div count events.html `open=11 close=10`: events.html:20 `<div class="container">` is never closed before events.html:61 `</section>`
  - Correzione: Add .github/workflows/ci.yml that runs on pull_request to main and deploy. It should run html-validate or htmlhint on site/**/*.html and a relative link check (for example lychee --offline). It should also run a guard script that fails on: CNAME, *.md or .claude inside site/; '[EVENT NAME]' or '€[XX]'; routable placeholder domains (phdnetwork.org); and href="#" on buttons without a 'not-developed' marker. Make the job a required status check in the main and deploy rulesets.
- **code-11** · low · riga 20: Unclosed <div class="container"> in events.html.
  - Correzione: Add </div> before </section> at line 61. Add html-validate to CI so web-UI edits cannot reintroduce this.
- **a11y-19** · low · riga 20: Unclosed container <div> in events.html.
  - Correzione: Close the container. Add an HTML validation step (e.g. html-validate or the Nu checker in CI) on the deploy branch, since collaborators edit the HTML in the GitHub web UI.
- **content-19** · high · riga 22: No Parma 2026 edition anywhere on the site. Azione: *sostituire con lorem ipsum*.
  - Evidenza: `grep -rni parma` over *.html/*.md/*.js returns nothing; the Upcoming section (:22-38) only holds Lucca 2025.
  - Correzione: Add an Upcoming card and an events/parma-2026 page. Fill confirmed facts (Parma, 2026, organizers) and use visible lorem ipsum for the description, program and venue. Mark registration/abstract boxes "Feature not developed / opens TBD". Do not write fake-sounding copy.
- **code-34** · low · riga 30: Emoji used as icons are read aloud; Italian quotes lack lang="it".
  - Correzione: Use inline SVG icons with aria-hidden="true" (or wrap emoji in <span aria-hidden="true">), and mark Italian passages with lang="it" inside <blockquote>.
- **content-18** · high · riga 32: Lucca Dec 2025 still listed as "Upcoming" with a "Register" button. Azione: *aggiornare (scaduto)*.
  - Evidenza: :22 `<h3>Upcoming Events</h3>`; :32 `<span class="event-badge badge-upcoming">Upcoming</span>`; :37 `<a href="events/lucca.html" class="btn btn-secondary">View Details & Register</a>` (lucca.html:250 says `Registration closed.`)
  - Correzione: Move the Lucca 2025 card to Past Events with a "Past" badge and a "View Event Archive" button. The Upcoming slot should hold Parma 2026.
- **code-29** · high · riga 32: Event status and CTAs are hard-coded in markup and now wrong; event data lives in 3 places. Azione: *aggiornare (scaduto)*.
  - Evidenza: events.html:29 `IMT Lucca 2025` with :32 `<span class="event-badge badge-upcoming">Upcoming</span>` and :37 `View Details & Register`. The event was Dec 2025 (today is 2026-10-20), and lucca.html:250 says `Registration closed.` index.html:16 `View Upcoming Events`; index.html:49 `<p class="date">October 2025</p>`.
  - Correzione: Keep editions in _data/editions.yml (slug, dates, venue, status, hero image) and render the events list, the homepage 'next edition' block and the badges from it. Add Parma 2026 as upcoming and move Lucca to past.
- **content-25** · low · riga 35: Lucca 2025 card description is generic and contradicts the event page. Azione: *sostituire con lorem ipsum*.
  - Correzione: Rewrite as a past-tense archive blurb using real facts (Dec 18-20 2025, Sagrestia IMT, keynotes Saggese and Livan, the session themes), or put lorem ipsum there until the team writes it. Fix the two-days/three-days mismatch in lucca.html:116, not here.
- **content-26** · medium · riga 41: Past Events omits the first editions (v1.0 Lucca, v1.X Vienna). Azione: *verifica del team*.
  - Evidenza: Past Events (:41-58) lists only `Fostering Research Synergies v2.0 (FRS2024)`. frs2024-winter.html:41 mentions `After a successful debut (v1.0) in Lucca and a bonus round (v1.X) in Vienna`
  - Correzione: Ask the team for the dates and venues of v1.0 and v1.X, plus any program or photos. Add archive cards and use lorem ipsum for anything they can't supply.
- **content-27** · low · riga 49: Edition naming is inconsistent. Azione: *verifica del team*.
  - Correzione: Have the team choose one scheme (e.g. "FRS2025 · v3 · Lucca", "FRS2026 · v4 · Parma") and apply it to every edition, page title and URL.
- **critic-10** · low · riga 55: Unclassified Rome 2024 card copy on the events list: AI tone plus an unverified headcount. Azione: *verifica del team*.
  - Correzione: Keep the facts that the program confirms (dates, CREF, 5 senior talks, 30+ talks, quiz). Drop 'epic'. Confirm or remove '50+' (see content-28), and use the same edition number the edition list uses ('second' vs v1.0/v1.X/v2.0).

### `about.html` (9)

- **content-29** · low · riga 15: About hero tagline is AI filler. Azione: *sostituire con lorem ipsum*.
  - Correzione: Use lorem ipsum, or drop the tagline.
- **content-30** · medium · riga 23: "Our Mission" is the template paragraph with the name swapped in. Azione: *sostituire con lorem ipsum*.
  - Evidenza: `Fostering Research Synergies is an informal association dedicated to fostering collaboration, knowledge sharing, and professional development among early-career researchers. We believe that bringing together talented PhD students...` (template had `The PhD & Postdoc Research Network is...`, commit 3a7ad03)
  - Correzione: Use visible lorem ipsum until the team writes a mission statement.
- **content-31** · low · riga 33: Three generic "What We Do" cards. Azione: *sostituire con lorem ipsum*.
  - Correzione: Use lorem ipsum, or fill with real formats seen in the programs (contributed talk sessions, keynotes, complexity quiz, group games, panel, social dinner) once the team confirms them.
- **content-32** · medium · riga 47: "Our Community" misdescribes the scope (humanities, engineering...). Azione: *sostituire con lorem ipsum*.
  - Evidenza: `Our network brings together researchers from diverse backgrounds and disciplines. Whether you're working in natural sciences, engineering, social sciences, or humanities, you'll find a welcoming community...`
  - Correzione: Replace with lorem ipsum. Every real program is complex systems, networks and economic complexity; the current text describes a different event.
- **content-33** · low · riga 55: "Get Involved" list may promise things FRS doesn't offer (posters, open committee). Azione: *verifica del team*.
  - Correzione: Ask the team which routes are real: were there ever poster sessions (none in the 2024/2025 programs)? Is the committee open to volunteers? Keep confirmed items and put lorem ipsum for the rest.
- **a11y-15** · high · riga 65: The real contact email is plain text (not tappable), while contact.html links fake addresses. Azione: *aggiornare (scaduto)*.
  - Evidenza: about.html:65 `<p style="margin-top: 1rem;"><strong>Email:</strong> frscrefimt@gmail.com</p>`. events/lucca.html:276 `frscrefimt@gmail.com` as plain text. contact.html:31-32 link `mailto:info@phdnetwork.org` / `mailto:events@phdnetwork.org`.
  - Correzione: Remove the fabricated info@/events@phdnetwork.org addresses now. Render the real address (frscrefimt@gmail.com, or whatever the team confirms) from one source as a mailto: link on every page.
- **content-35** · low · riga 65: Real team email (also lucca.html:276), shown as plain text without a link. Azione: *tenere*.
  - Correzione: Keep, and make it a mailto link in one shared component. Use it as the single contact address on contact.html (replacing content-01).
- **code-40** · low · riga 65: Contact email shown as plain text, not a mailto link.
  - Correzione: Use one include (e.g. _includes/contact-email.html from site.email in _config.yml) that renders a mailto: link, so the address is defined once.
- **content-34** · low · riga 66: "Join the Fostering Movement!" box heading and tagline are filler. Azione: *sostituire con lorem ipsum*.
  - Correzione: Put lorem ipsum in the heading and tagline, and keep the email line (content-35).

### `README.md` (8)

- **content-16** · medium · riga 1: README is the untouched AI template and is served raw at /README.md. Azione: *aggiornare (scaduto)*.
  - Evidenza: `# PhD & Postdoc Research Network Website` / :3 `A clean, responsive website for your informal PhD and postdoc association`; :247 `- Add participant testimonials`; curl /README.md -> 200 (7810 bytes = local file)
  - Correzione: Replace it with a real project README covering what FRS is, the repo layout, the deploy branch, the branch/worktree workflow and the content policy (lorem ipsum, never invented facts or testimonials). Exclude README from the deploy artifact.
- **deploy-06** · medium · riga 1: The legacy Jekyll build publishes the whole branch root: .md files are live now, and a future CLAUDE.md or docs/*.md would be too.
  - Evidenza: `curl http://frs-workshop.imtlucca.it/QUICK-START.html` -> `200 text/html` with `<title>Quick Start Guide 🚀 \| Fostering Research Synergies</title>`; `/README.md` -> `200 text/markdown`; `/QUICK-START.md` -> `200 text/markdown`; `/assets/css/style.css` -> `200 ... 76559` (a Jekyll theme file not in the repo); `ls -a` shows no .nojekyll, _config.yml or .gitignore; Pages …
  - Correzione: Under the current setup, adding CLAUDE.md, AGENTS.md or docs/*.md to main would publish them as /CLAUDE.html and /docs/*.html, with the raw .md served as well. Jekyll skips .claude/ because it starts with a dot. But as soon as a .nojekyll file is added to a branch-served root, files are published as they are, so .claude/ could go public too. Fix: publish only an allowlisted directory (site/) through the Actions workflow (deploy-03 step 5). Keep CLAUDE.md, .claude/, docs/, README and templates outside site/. Add a CI guard that fails if site/ contains *.md, CNAME, .claude or CLAUDE*.
- **deploy-09** · medium · riga 1: README and QUICK-START are generic AI template docs with wrong deploy instructions, and both are published. Azione: *aggiornare (scaduto)*.
  - Evidenza: README.md:1 `# PhD & Postdoc Research Network Website`; README.md:22 `│   ├── summer-2025.html    # Example: upcoming event` (no such file); README.md:76 `4. Under "Branch", select **main** and folder **/root**`; QUICK-START.md:54 `1. Go to `events/summer-2025.html``; both return 200 on the live site
  - Correzione: Delete QUICK-START.md. Rewrite README.md as a short internal contributor guide covering: the branch model (feature branch or worktree -> PR to main -> PR to deploy), how to preview locally, how to add an edition page, and the placeholder rules (lorem ipsum, 'feature not developed'). Keep it outside the published directory. CLAUDE.md can point to it rather than repeating it.
- **content-74** · medium · riga 22: README file structure and branding instructions describe a different site. Azione: *aggiornare (scaduto)*.
  - Evidenza: `│   ├── summer-2025.html    # Example: upcoming event` (file never existed; lucca.html, frs2024-winter.html, navbar.js and pictures/ not listed); :87 `Find <h1>PhD & Postdoc Network</h1> in the navigation` (nav now lives in navbar.js)
  - Correzione: Rewrite as part of the new README (content-16).
- **code-27** · medium · riga 22: Generic generator README/QUICK-START are published and document files that don't exist. Azione: *eliminare*.
  - Evidenza: README.md:22 `│   ├── summer-2025.html    # Example: upcoming event` (no such file); :87 says to edit `<h1>PhD & Postdoc Network</h1>` in each HTML file (the nav actually lives in navbar.js); :95 says the hero uses a 'purple gradient' (it uses cover.png). QUICK-START.md:54 `Go to events/summer-2025.html`. Live host: /QUICK-START.html returns 200 and /README.md returns 200. There is no _config.yml …
  - Correzione: Delete QUICK-START.md and rewrite README.md for contributors (branch/worktree flow, how to add an edition). Add _config.yml with `exclude: [README.md, CLAUDE.md, AGENTS.md, .claude, docs]`, or deploy only build output from the deploy branch.
- **content-75** · medium · riga 76: Deploy instructions (main / root, "create a new repo") contradict the planned deploy-branch workflow. Azione: *aggiornare (scaduto)*.
  - Evidenza: `4. Under "Branch", select **main** and folder **/root**`; :36 `5. Make it **Public**`; :212-214 `git add .` / `git commit -m "Description of changes"` / `git push`
  - Correzione: Replace with the real workflow: feature branches/worktrees, PR to main, deploy branch or Pages action, and the custom-domain/CNAME decision for fosteringresearchsynergies.github.io.
- **content-76** · low · riga 151: README admits registration buttons and contact form are placeholders. Azione: *marcare come non sviluppato*.
  - Correzione: Turn these into tracked issues or markers in the new site ("Feature not developed"). Don't keep the template's example addresses.
- **content-77** · low · riga 259: Template license line invites reuse of a site full of third-party logos and people's photos. Azione: *verifica del team*.
  - Correzione: Ask the team which license, if any, applies to the code and which to the content. Resolve the conflict between README:259 and the 'All rights reserved' footers, and exclude the logos (EU, MUR, Italiadomani, EFC, IMT) and the photos of people from any open license.

### `events/event-template.html` (6)

- **deploy-08** · medium · riga 6: The event template is publicly served as a page full of [EVENT NAME] and €[XX]. Azione: *eliminare*.
  - Evidenza: events/event-template.html:6 `<title>[EVENT NAME] - Fostering Research Synergies</title>`; :79 `PhD Students: €[XX]<br>`; :89 `<a href="#" class="btn btn-primary" ...>Register Now</a>`; `curl .../events/event-template.html` -> `200 text/html`
  - Correzione: Move it out of the published tree, for example to templates/event.html at the repo root next to site/, or into a .claude skill or command that scaffolds a new edition page. The Parma 2026 page should start from the restyled template. Where real content is missing, it should use lorem ipsum, and boxes whose feature does not exist yet should carry an explicit 'feature not developed' marker.
- **content-13** · medium · riga 14: Bracket-placeholder template page is publicly served. Azione: *eliminare*.
  - Evidenza: `<title>[EVENT NAME] - Fostering Research Synergies</title>` (:6), `<h2 class="event-detail-title">[EVENT NAME]</h2>`, :17 `[DATE RANGE]`, :103 `[email@example.com]`, :89 `<a href="#" ...>Register Now</a>`, :95 `<a href="#" ...>Submit Abstract</a>`; live URL returns 200.
  - Correzione: Remove it from the published site. If a template is useful to agents, keep it outside the deploy (e.g. a non-published templates dir or the .claude agent docs) and build it on the new design.
- **mob-03** · low · riga 31: Event template uses an inline 2fr/1fr grid that never stacks on mobile; Lucca only works because of a page-local !important hack.
  - Correzione: Create a proper .event-layout (main + sidebar) component in the shared stylesheet with its own breakpoint. Build the Parma page and all editions from one layout instead of copying the template. Keep inline style attributes out of the markup.
- **content-14** · low · riga 79: Template invents registration fees (Early Bird/Regular), though FRS participation is free. Azione: *eliminare*.
  - Correzione: Delete the fee block so it can't be copied into the Parma page. The Parma registration box should say lorem ipsum or "TBD" until the team decides.
- **content-78** · medium · riga 89: Template's Register/Submit buttons go to "#", which would spread dead CTAs to new event pages. Azione: *marcare come non sviluppato*.
  - Evidenza: `<a href="#" class="btn btn-primary" ...>Register Now</a>`; :95 `<a href="#" class="btn btn-secondary" ...>Submit Abstract</a>`
  - Correzione: In any rebuilt template, the default CTA state should be a disabled "Feature not developed / opens TBD" button. Make a real URL required before the button is enabled.
- **code-26** · medium · riga 89: Event template is deployed as a public page with fake fees and dead CTAs. Azione: *eliminare*.
  - Evidenza: events/event-template.html:6 `<title>[EVENT NAME] - Fostering Research Synergies</title>`; :79 `PhD Students: €[XX]`; :89 `<a href="#" class="btn btn-primary" ...>Register Now</a>`; :95 `<a href="#" ...>Submit Abstract</a>`. The live host returns 200 for /events/event-template.html.
  - Correzione: Move templates out of the deployed tree (e.g. a Jekyll layout `_layouts/edition.html` plus a front-matter stub, or a docs/ folder excluded via _config.yml). Drop the fee block, since participation is free.

### `events/winter-2024.html` (6)

- **content-03** · high · riga 14: Entire fabricated event page ("Winter Conference 2024") is publicly reachable. Azione: *eliminare*.
  - Evidenza: `<h2 class="event-detail-title">Winter Conference 2024</h2>`, :17 `December 10-11, 2024`, :20 `Conference Center, Main Hall`, :23 `82 participants`, :33 `bringing together 82 PhD students...`, :41-44 `24 oral presentations / 36 poster presentations / 2 keynote speakers / 3 panel discussions`, :127-129 Thank You box. `curl http://frs-workshop.imtlucca.it/events/winter-2024.html` -> 200. Conflicts …
  - Correzione: Delete the file (lines 1-158) from the repo and the deploy. Do not keep it as an example: README.md:23 refers to it as an example of a past event.
- **content-04** · high · riga 61: Fake poster-award winners (invented people). Azione: *eliminare*.
  - Evidenza: `🥇 First Place:</strong> "Novel Approaches to Data Analysis" - Alex Thompson` / :62 `Maria Garcia` / :63 `James Wilson`
  - Correzione: Delete along with the page (lines 59-64). FRS has never run poster awards as far as the repo shows.
- **deploy-07** · medium · riga 61: Public page for a fake 'Winter Conference 2024' with invented winners and quotes (not linked, but reachable). Azione: *eliminare*.
  - Evidenza: events/winter-2024.html:61 `<p><strong>🥇 First Place:</strong> "Novel Approaches to Data Analysis" - Alex Thompson</p>`; :17 `December 10-11, 2024`; :20 `Conference Center, Main Hall`; :23 `82 participants`; `curl .../events/winter-2024.html` -> `200 text/html`; nothing links to it (`grep -rn winter-2024 *.html *.js` exit=1)
  - Correzione: Delete it from the repo. It is template sample content that was never removed. It names invented people as award winners and invents participant quotes, and there is no robots.txt to keep it out of search engines. Do not turn it into lorem ipsum: no such event took place.
- **content-05** · high · riga 69: Invented participant testimonials. Azione: *eliminare*.
  - Evidenza: `"The conference provided excellent networking opportunities and the keynote speakers were truly inspiring. I made several connections..."` and :72 `"Well-organized event with a good balance of presentations..."`
  - Correzione: Delete (lines 66-74). If the team wants testimonials on the new site, they must be real quotes with consent. Otherwise leave a clearly marked lorem-ipsum slot.
- **content-06** · high · riga 88: Invented keynote speakers and sessions. Azione: *eliminare*.
  - Evidenza: `Prof. Sarah Johnson, Distinguished Professor` (:87 `Keynote: "Emerging Trends in Research Methodology"`), :110 `Dr. Michael Chen, Senior Research Fellow`, :118 `Workshop: "Effective Science Communication"`
  - Correzione: Delete (program lines 76-124) with the page.
- **code-25** · high · riga 88: Fabricated 'Winter Conference 2024' page is publicly reachable (200 on live host), though not linked. Azione: *eliminare*.
  - Evidenza: events/winter-2024.html:88 `Prof. Sarah Johnson, Distinguished Professor`; :61 `"Novel Approaches to Data Analysis" - Alex Thompson`; :23 `82 participants`; :20 `Conference Center, Main Hall`. `curl http://frs-workshop.imtlucca.it/events/winter-2024.html` returns 200. No page links to it (grep).
  - Correzione: Delete the file; it is invented generator demo content published under the group's name.

### `navbar.js` (5)

- **code-06** · medium · riga 2: Navigation and the site's only <h1> are injected by JS after DOMContentLoaded.
  - Evidenza: navbar.js:2 `document.addEventListener('DOMContentLoaded', function() {` ... :16 `<h1>Fostering Research Synergies</h1>` ... :29 `document.body.insertAdjacentHTML('afterbegin', navbarHTML);`. It is loaded render-blocking in <head> with no defer (e.g. index.html:7 `<script src="navbar.js"></script>`). A grep for `<main`, `aria-` and `role=` finds 0 hits in any page.
  - Correzione: Render the nav server-side (Jekyll include) as real markup in <nav aria-label="Main">. Then non-JS clients, link-preview scrapers and crawlers see the navigation and h1, and the page has no insertion layout shift. Add <main> and a skip link.
- **code-07** · low · riga 5: Active-state logic compares exact filenames, so it fails on extensionless URLs that GitHub Pages serves.
  - Correzione: Do this at build time: Jekyll compares page.url and emits class="active" aria-current="page". Link Home to './' or '{{ "/" \| relative_url }}'.
- **code-08** · medium · riga 8: Hard-coded '/events/' detection with a single '../' breaks links at any other depth (e.g. a nested Parma page or a 404 page).
  - Evidenza: navbar.js:8 `const isInSubdirectory = currentPath.includes('/events/');` :9 `const pathPrefix = isInSubdirectory ? '../' : '';`. For a page at /events/parma-2026/ the links resolve to /events/index.html and /events/events.html (both 404). For a page in any other folder (e.g. /editions/parma.html) the prefix is '' and links resolve inside /editions/. A custom 404.html served at arbitrary paths …
  - Correzione: Use root-relative URLs generated by Jekyll (relative_url / site.baseurl) instead of runtime path sniffing. Decide the URL scheme for editions (e.g. /editions/2026-parma/) before building the Parma page.
- **a11y-08** · medium · riga 16: Broken heading hierarchy: JS-injected brand is the only h1, page titles are h2, and stat numbers are h2.
  - Evidenza: navbar.js:16 `<h1>Fostering Research Synergies</h1>` (identical on every page, missing without JS). Page titles are h2: index.html:14, events/lucca.html:92. frs2024-winter.html:71-91 has six `<h2 style="color: #3498db; margin-bottom: 0.5rem;">3</h2>` ... `∞` ... `0` under an h3. events.html:22 and :29 use h3 for both the section and the event title. event-template.html:75 `<h5 ...>Registration …
  - Correzione: Make the brand a plain link or logo. Give each page exactly one h1 (the page or edition title), then h2 for sections and h3 for cards and days. Render stats as <p> or <dl> styled large, not headings.
- **seo-05** · medium · riga 29: All site navigation is injected by JavaScript; about.html and contact.html have no static inbound links.
  - Evidenza: navbar.js:29 `document.body.insertAdjacentHTML('afterbegin', navbarHTML);`. grep 'href="(../)?(about\|contact).html' in *.html -> 0 matches. Headless Chrome with JS disabled on index.html: `0 nav/h1 elements; links: events.html`.
  - Correzione: Put the nav markup into the HTML at build time: a Jekyll _layouts/_includes header (GitHub Pages already runs Jekyll) or an SSG built by Actions onto the deploy branch. Repeat the key links in the footer. Drop navbar.js.

### `.gitignore` (2)

- **deploy-14** · medium · file: No .gitignore while a .claude/ folder is planned, so personal settings and worktrees could be committed.
  - Evidenza: `ls -a` in the repo root shows no .gitignore (`grep -E '^\.(gitignore\|nojekyll\|github)$'` exit=1); local config already holds editor state: `branch.main.vscode-merge-base=origin/main`
  - Correzione: Create .gitignore with: .claude/settings.local.json, .claude/worktrees/, CLAUDE.local.md, .mcp.json (if it holds tokens), .vscode/, .idea/, .DS_Store, *.swp, node_modules/, and local build/preview output. Commit only shared agent material: CLAUDE.md, .claude/settings.json (permissions only, no secrets), .claude/agents/, .claude/commands/ or skills/. Put agent worktrees outside the repo (../frs-wt/<branch>) or in the git-ignored .claude/worktrees/.
- **critic-02** · medium · file: A GitHub Actions deploy that uploads the repo root would publish .claude/, CLAUDE.md and the planning docs.
  - Evidenza: actions/upload-pages-artifact@v3 action.yml: "--exclude=.git \ --exclude=.github" (no other excludes; hidden dirs only skipped from v4 via "include-hidden-files"). Today the legacy Jekyll build skips dotfiles but publishes root .md (README.md -> 200 text/markdown).
  - Correzione: If deploy moves to Actions or a build step, put the site in its own folder (e.g. site/ or _site/) and upload only that folder, never '.'. Pin upload-pages-artifact to v4 or later by SHA. Keep agent material (.claude/, CLAUDE.md, plans) outside the published folder, and have CI fail if *.md files or dot-folders appear in the artifact.

### `QUICK-START.md` (2)

- **seo-02** · medium · riga 1: Developer docs and fake or template pages are publicly served and indexable; the only page with OG/canonical tags is the template's Quick Start guide. Azione: *eliminare*.
  - Evidenza: Live GET: /QUICK-START.html 200, Jekyll-rendered with `<title>Quick Start Guide 🚀 \| Fostering Research Synergies</title>` and `<link rel="canonical" href="http://frs-workshop.imtlucca.it/QUICK-START.html" />`. /README.md 200 text/markdown. /QUICK-START.md 200. /events/event-template.html 200 (title `[EVENT NAME] - Fostering Research Synergies`). /events/winter-2024.html 200 (fabricated 'Winter …
  - Correzione: Remove QUICK-START.md, events/event-template.html and events/winter-2024.html from the deployed tree. Keep the event template in a non-published folder: excluded in _config.yml or outside the deploy branch's build output. Replace README.md with a real contributor README and exclude it from the build.
- **content-15** · medium · riga 3: AI template quick-start guide is published as a site page. Azione: *eliminare*.
  - Evidenza: `Welcome! Your website is ready to deploy. Follow these steps to get it online quickly.`; live /QUICK-START.html -> 200 with `<title>Quick Start Guide 🚀 \| Fostering Research Synergies</title>`; :18 `PhD & Postdoc Network`; :54 `Go to events/summer-2025.html` (file does not exist); :61 `#667eea` (not in styles.css); :83 `the design is already professional`
  - Correzione: Delete QUICK-START.md from the repo, or at least exclude it from the deploy branch. Put any useful workflow notes in the new README and the .claude docs. (Leave out the claim that #667eea is missing; it is used in styles.css:113 and :237.)

### `404.html` (1)

- **seo-09** · low · riga 1: No custom 404 page (file missing); after the migration old paths land on GitHub's generic 404.
  - Correzione: Add a 404.html with the site header and footer, a link to the Parma edition and the events archive, and a note that the site moved from frs-workshop.imtlucca.it.

### `pictures/EFC  Fascia Loghi (1260 x 145 px).png` (1)

- **critic-06** · low · riga 1: Published images contain editor metadata (Canva doc and user IDs); the hero is a desktop screenshot.
  - Correzione: In the image pipeline for the restyle, strip EXIF/XMP when converting to WebP/AVIF (e.g. exiftool -all= or sharp without withMetadata). Ask the team for the original group-photo file instead of the 641x486 screenshot, and keep the originals out of the published folder.

### `pictures/cover.png` (1)

- **perf-01** · high · riga 1: 617 KB PNG photo is about 98% of the home page weight; WebP would be about 63 KB.
  - Evidenza: `cover.png: PNG image data, 641 x 486, 8-bit/color RGBA` with alpha extrema (255, 255) (fully opaque). ls: 617229 bytes vs index.html 2433 + styles.css 6350 + navbar.js 1441. Live: `Content-Length: 617229`, `Cache-Control: max-age=600`. Re-encoded in scratch: WebP q80 = 63294 B, JPEG q80 = 74513 B. The image loads on index, about, events and contact via .hero.
  - Correzione: Store photos as JPEG/WebP/AVIF, never PNG (PNG only for flat logos). Add an image pipeline or checklist: max about 200 KB per hero variant, generated sizes and formats.
