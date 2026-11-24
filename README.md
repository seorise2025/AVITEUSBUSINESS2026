# Aviteus Business Solutions: website (first build)

The seven launch pages from the Copy Deck (24 Nov 2026), plus a 404 page and a free UK deadline finder. Built on **The Pulse Ledger** design system, in its quieter form: ruled rows, orange only on buttons and due dates.

**Status: staging build. Not ready to go live.** See "Launch blockers" below.

## What is here

| Path | What it is |
|---|---|
| `site/` | The finished website. Upload this folder to the host. Plain HTML, no build needed to serve it. |
| `src/pages.py` | Every page's copy, word for word from the Copy Deck. |
| `src/layout.py` | Shared header, footer, mobile bar, cookie banner, SEO tags and structured data. |
| `src/data.json` | CMS-style facts: team, AML supervisor, PI insurer, cut-off day and more. Empty = hidden. |
| `src/site.css`, `src/site.js`, `src/finder.js` | Site styles, site behaviour, deadline finder. |
| `src/static/` | Logo (PNG and WebP), favicon, app icon, social share image, `llms.txt`. |
| `design-system/` | The Pulse Ledger design system: tokens, components, fonts, brand book. |

## Build

```bash
python3 src/build.py
```

The build writes `site/` from scratch. Edit files in `src/` or `design-system/`, never in `site/`.

## Pages

| URL | File | Notes |
|---|---|---|
| `/` | `index.html` | Home |
| `/services` | `services.html` | Services hub |
| `/services/bookkeeping` | `services/bookkeeping.html` | |
| `/services/payroll` | `services/payroll.html` | |
| `/services/vat-tax` | `services/vat-tax.html` | |
| `/about-us` | `about-us.html` | |
| `/contact` | `contact.html` | Review booking and enquiry form |
| `/deadline-finder` | `deadline-finder.html` | Free tool. New copy, not in the deck |
| `/terms-and-conditions` | `terms-and-conditions.html` | Word for word from the live site, until Vikas reviews it |
| `/privacy-policy` | `privacy-policy.html` | **Draft for adviser review.** `noindex`, not in the sitemap. "To confirm" items need answers |
| `/cookies` | `cookies.html` | **Draft for adviser review.** Describes exactly what the site stores today. `noindex` |
| any unknown path | `404.html` | Real 404, `noindex` |

Files are named `page.html` so Cloudflare Pages and Netlify serve them at clean URLs with no trailing slash, matching the canonical tags.

## Preview on claude.ai

Private staging preview: https://claude.ai/artifact/LGLR7cbpy2X8yz8Y4PSvyf

```bash
python3 src/build.py
python3 src/build_artifact.py <folder>
```

The preview copy uses file names for links (`contact.html`), keeps the light look whatever the viewer's theme, and offers "Copy these dates" in the finder because claude.ai blocks downloads. The `site/` folder is the real website and is not changed by this step.

## SEO built in

- Every page is full HTML from the server. Nothing needs JavaScript to be read by Google or AI tools.
- Titles 47 to 60 characters, descriptions 135 to 152, one H1, self-canonical, Open Graph and social image on every page.
- Structured data: `AccountingService` + `LocalBusiness` (address, phone, hours, company number, founding date), `WebSite`, `Service` on each service page, `FAQPage` only where the FAQ is visible, `BreadcrumbList`, `ContactPage`, `AboutPage`, `ItemList`, `WebApplication` for the finder. No `SearchAction` (there is no site search).
- Answer-first sections on each service page, written so AI answer tools can quote them.
- Internal links with the anchor text the strategy pack specifies.
- `sitemap.xml` (8 URLs), `robots.txt` with the sitemap line, `llms.txt` summary for AI tools.
- `_redirects`: `/contactus` and `/contactus.html` to `/contact` (301). `_headers`: security headers and caching.
- Fonts self-hosted and preloaded. Logo served as WebP. Whole site about 700 KB, most of it fonts that are cached after the first page.

## Analytics and consent

- Nothing third-party loads until a visitor accepts analytics. Reject is as easy as accept.
- Set the Tag Manager ID in `src/site.js` (`CONFIG.gtmId`) and rebuild. Consent Mode defaults are already set to denied.
- Events pushed to `dataLayer`, never with personal data: `generate_lead` (only after the server returns a reference), `book_review_click`, `whatsapp_click`, `phone_click`, `form_error`, `deadline_finder_used`, `deadline_calendar_download`.

## The enquiry form: what the backend must do

The form posts JSON to `POST /api/enquiries`. **That endpoint does not exist yet.** Until it does, every submit shows the honest failure message with the WhatsApp fallback. The form never pretends to work.

The backend must follow section 13 of the strategy pack. The page sends: `name`, `email`, `company`, `service`, `message`, `reply_method`, `phone`, `newsletter`, `website` (honeypot, must be empty), `submission_id` (for duplicate checks), `elapsed_ms` (reject under 3000), and the attribution fields `page_url`, `page_title`, `referrer`, `utm_source`, `utm_medium`, `utm_campaign`, `utm_term`, `utm_content`, `gclid`, `first_landing`, `form_version`.

It must answer with:

| Status | Body | Page shows |
|---|---|---|
| 201 | `{"reference": "AV-0042"}` | Thank you message with the reference |
| 422 | `{"errors": {"email": "message"}}` | Error summary and field messages |
| 429 | anything | "Please wait a minute" with WhatsApp |
| anything else | anything | "We could not send your enquiry just now" with Try again and WhatsApp. All entries kept |

Add the Turnstile site key in `src/site.js` (`CONFIG.turnstileSiteKey`) and load the Turnstile script once the backend checks it.

## Hidden until real (from the deck's editor notes)

Fill these in `src/data.json` and rebuild. Each block appears only when its data exists.

- Team members (name, role, qualification, body, membership number, photo, LinkedIn, consent): Home team strip, About team section, `Person` structured data.
- AML supervisor and PI insurer: Home facts strip, About "Details you can check".
- Management pack delivery day: Bookkeeping scope table "When" cell (blank until set).
- Payroll cut-off day: shows "Cut-off day" until set.
- Sample management pack: the Bookkeeping "See what a monthly pack looks like" section and its hero link.
- Where the work is done (Option A or B): About page section.
- LinkedIn company page: footer.

## Additions beyond the deck (for approval)

- The free UK deadline finder page, its copy, menu and footer links, and links to it from the Payroll and VAT pages.
- A short "Related pages" link row on each service page, using the exact anchor texts from the deck's internal link plan.
- "Cookie settings" link in the footer, so visitors can change their choice (PECR).
- Payroll month table: "Cut-off day" shown in place of the `{Cut-off day}` field until a day is agreed.

## Launch blockers (from the strategy pack)

- [ ] `/api/enquiries` endpoint, database, notification and Zoho push working, with one approved test enquiry received
- [ ] Privacy notice at `/privacy-policy`: draft is built, adviser must complete and approve it, then remove `noindex` and add it to the sitemap
- [ ] Cookie details at `/cookies`: draft is built, adviser must approve it
- [ ] Terms at `/terms-and-conditions` reviewed by Vikas
- [ ] Team, AML supervisor and PI insurer confirmed in writing
- [ ] Vikas approves: the "Done and due" report as standard, the free review, the "we're new" wording, the origin story, referring poor-fit leads
- [ ] Accounting reviewer signs off every deadline on the Payroll, VAT and finder pages
- [ ] WhatsApp link tested on iPhone, Android and desktop
- [ ] Non-www to www redirect set at DNS or host level
- [ ] Tag Manager ID added, Search Console verified, sitemap submitted
