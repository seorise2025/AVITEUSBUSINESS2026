Aviteus Business is a firm of chartered accountants in Harrow serving SMEs and startups across the UK. This system is called **The Pulse Ledger**. It keeps the brand's orange, navy and logo exactly as they are, and gives them a new shape language taken from the logo itself: rising bars with cut tops, a heartbeat line, and small circuit nodes.

Three ideas run through everything:

1. **The Notch.** One corner cut at 45 degrees, always top right. It comes from the angled tops of the logo's bars.
2. **The Pulse Line.** A 2px `ember` line with one heartbeat spike. It comes from the line that runs through the logo, and from the firm's roots in healthcare.
3. **Ledger figures.** Every number, date and form code is set in a monospaced face, so money always looks like money.

---

## Content fundamentals

Content is the demand engine. Every page, card and email must give the reader a reason to call. Design only carries the words.

### Voice

- **Plain.** Short sentences. Common words. One idea per sentence.
- **Direct.** Talk to "you". Speak as "we". Never "the client" or "our customers".
- **Specific.** Names, numbers, dates and forms beat adjectives. "Filed by 31 January" beats "timely filing".
- **Calm.** No hype, no exclamation marks, no emoji.
- **Proof first.** If a line makes a claim, the next line proves it.

### Rewrite examples from the live site

| Live site today | Use instead | Why |
|---|---|---|
| "Let's discuss about how we can help make your insurance better" | "Ready for an accountant who calls you back?" | Wrong service, broken grammar. |
| "Nostra proin fusce hendrerit viverra nisl torquent." | "One monthly fee, in writing, within 48 hours." | Placeholder text is live on the home page. |
| "85% Business Awards" | "£0 surprise fees on a fixed plan" | A claim with no base or source. |
| "Lets Work Together" | "Book a free consultation" | Vague, and missing an apostrophe. |
| "Expert accounting, tax planning, and business advisory services to help your business thrive." | "Books, tax and payroll for UK SMEs. One fixed fee. One named manager." | Says what you get, not how good we are. |

Keep these lines from the live site. They already work:

- "You want numbers you can trust and advice you can use."
- "Focused on Clarity. Driven by Trust. Built for Growth."
- "No hidden fees or surprise bills."

### Headline formulas

- **Outcome + proof:** "Your books, done by the 5th of every month."
- **Pain + fix:** "Stop guessing your VAT bill."
- **Question the reader answers yes to:** "Ready for an accountant who calls you back?"
- **Deadline:** "31 January is 68 days away. Is your return started?"

### Calls to action

Verb first, max 4 words, sentence case. Approved set:

- Book a free consultation (main action, site-wide)
- Get my fixed quote
- See our services
- Send my question
- Read more (cards only)

### Numbers, dates and money

- Set every figure in the `figures` family with tabular numbers (`.av-num`, `figure`, `figure-xl`, `code`).
- Money: "£1,240", "£0". Never "GBP" in body copy.
- Dates in running text: "31 January 2027". In tags and tables: "31 JAN 27".
- Time: 24-hour, "09:00 to 17:00".
- Every stat carries a source line. No source, no stat.

### Words we never use

- Hype words: world-class, cutting-edge, seamless, best-in-class, game-changing.
- Filler nouns: "solutions", "offerings", "synergy".
- The house banned-word list kept by the content lead. Check every draft against it before it goes live.

No em dashes in any copy. Use a full stop or a comma.

### Page structure that brings enquiries

Every service page follows the same order: Hero promise, three proof points (StatColumns), what is included (ServiceCard grid), how it works (ProcessSteps), key tax dates (DeadlineTag), one CTABand, FAQ, Footer. Each section answers one question a buyer has, in the order they ask it.

---

## Visual foundations

### Colour

The colour set is the brand's own. Every value comes from the live site's CSS or is sampled from the logo file. Nothing is new; only the roles are.

| Role | Token | Value | Where it is used |
|---|---|---|---|
| Brand orange | `ember` | #D55D00 | Primary buttons, Pulse Line, stat columns, node dots |
| Orange for small text | `ember-ink` | #B04D00 / #FF8C42 | Links and eyebrows (5.4:1 on white) |
| Light orange | `ember-glow` | #FF8C42 | Accent word on night, second chart series |
| Warm tint | `ember-wash` | #FFF4EC | Callouts, newsletter, light form panel |
| Navy | `night` | #0E1422 | Hero, CTA band, dark theme ground |
| Deep navy | `night-deep` | #0C1019 | Top bar, footer |
| Heading ink | `ink` | #2B2B2B | Titles |
| Body grey | `ink-body` | #5D666F | Running text |
| Logo slate | `slate` | #385C7C | Data series next to ember |

Rules:

- **Ember is a fill, not a text colour.** On white it reads 3.9:1, so orange text under 24px uses `ember-ink`.
- **Ember buttons carry night ink.** `on-ember` (#0E1422) on `ember` reads 4.7:1. White on ember reads only 3.9:1. Hover swaps to `ember-deep` with white text (5.4:1).
- **One orange moment per screen.** One ember button, one accent word, one Pulse Line. Orange that is everywhere stops meaning "act here".
- **Alternate bands.** Long pages run `ground`, `ground-alt`, `ground`, then a `night` band. Never two `night` bands in a row.
- **Charts:** `ember`, then `slate`, then `ember-glow`. Blue next to orange stays clear for colour-blind readers.
- **Status colours** (`success`, `warning`, `danger`) are kept from the source CSS but are weak on white. Always pair them with a word and an icon. Error text itself is `ink`.

Two themes: **Daylight** (default) and **Night Ledger**, built on the site's own hero navy.

### Type

| Family | Face | Role |
|---|---|---|
| `display` | Bricolage Grotesque (variable, with optical sizes) | Headlines and titles |
| `text` | Instrument Sans | Body, labels, buttons |
| `figures` | JetBrains Mono | Numbers, dates, form codes, hours |

- Headlines are tight (`letterSpacing` -0.02em at `display-xl`) and short. Max 9 words in a hero.
- Body copy is `body` (16/26) in `ink-body`, max 68 characters a line.
- The eyebrow is the only uppercase text style, plus the `code` style for dates.
- Fallbacks keep the old site faces: Red Hat Display for display, DM Sans for text.

### Spacing and layout

- Base unit 4px (`space-1`), from the source CSS. Steps run 4, 8, 12, 16, 24, 32, 48, 64, 96, 120.
- Section padding: `space-10` desktop, `space-9` tablet, `space-8` mobile.
- Content width 1200px. Page gutter `space-6` desktop, `space-4` mobile.
- Card grids use `space-5` gaps. A heading block sits `space-7` above its content.

### Shape: the Notch and radii

- Cut corners (`cut-s` 10px, `cut-m` 18px, `cut-l` 32px) go on cards, badges, deadline tags and the CTA band. Always top right.
- Service cards show an `ember` fold in the cut corner.
- Rounded shapes are for things you touch: buttons and the menu toggle are pills (`radius-pill`); inputs use `radius-m`; large panels use `radius-l`.
- A component is either notched or rounded. Never both.

### The Pulse Line

- Short form (160px with an end node) under section titles.
- Wide form across the hero base and the CTA band. It draws once on load.
- Max two per screen. Always `ember`, always `stroke-pulse`.

### Depth and shadow

- Flat by default. Surfaces are told apart by fill (`ground`, `ground-alt`, `night`), not shadow.
- `shadow-lift` appears only on hover (cards) and on floating panels.

### Imagery

- Real photos of the real team and office in Harrow. Natural light. People at work, not posing.
- Never put text over a photo. The hero is a solid `night` band.
- Crop photos with the `cut-l` notch to tie them to the system.
- No stock handshakes, no lightbulbs, no piles of coins.

### Motion

- Calm and short: 150 to 250ms, ease out.
- Allowed: Pulse Line draw-in (once), card lift on hover (4px), arrow nudge on hover (3px), link underline draw.
- Nothing loops. `prefers-reduced-motion` turns all of it off.

### States

- **Focus:** 2px solid `focus-ring` with a 2px gap. On night bands the ring is `ember-glow`.
- **Hover:** ember to `ember-deep`; outline buttons fill with `ink`; links draw an underline.
- **Disabled:** `ground-sunk` fill, `ink-body` text, no pointer.
- **Error:** `danger` border and dot, message in `ink`.

---

## Iconography

- Use the site's own icon set in `assets/Icons`. Each icon is a single round `blush` tile with line art in `icon-ink` (#FA360A), as drawn for the live site.
- Show icons at 56px in lists and 64px in cards. Always decorative (`alt=""`) next to a visible title.
- The live site reuses one icon for both "Taxation and VAT" and "Payroll and Pensions" (`service-tax-payroll.svg`). A separate payroll icon is still needed.
- UI glyphs (arrow, menu) are simple 2px line icons drawn with `currentColor` inside components.
- No emoji, ever.

## Logo

Use `assets/Logos/aviteus-business-logo.png` exactly as supplied. On `night` grounds and in Night Ledger, place it on the white `plate` (`.av-logo--plate`). Minimum width 120px. Never recolour, redraw or crop it.

## Accessibility

- Every text pair in this system meets WCAG AA (4.5:1) in both themes, except `ember` as small text, which is why `ember-ink` exists.
- Status colours from the source fail on white and must never carry meaning alone.
- All inputs have visible labels. All buttons are at least 40px tall.
