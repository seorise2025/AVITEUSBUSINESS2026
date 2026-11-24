# Aviteus Business 2026

The new website for Aviteus Business Solutions, built on **The Pulse Ledger** design system.

## What is here

| Path | What it is |
|---|---|
| `index.html` | The new home page. Plain HTML and CSS, no build step. |
| `design-system/README.md` | The brand book: voice, colour, type, spacing, shape, motion and content rules. Read this first. |
| `design-system/tokens.json` | Every design value (colours, type, spacing, radii, cuts, shadows). The single source. |
| `design-system/tokens.css` | CSS variables generated from `tokens.json`. Do not edit by hand. |
| `design-system/components/bundle.css` | The component styles (`.av-*` classes). |
| `design-system/components/<Name>/` | A live preview and usage notes for each component. |
| `design-system/fonts/` | Bricolage Grotesque, Instrument Sans and JetBrains Mono (all SIL Open Font License). |
| `design-system/assets/` | The official logo and the site icons, copied from the live site. |

The live design system with previews: https://claude.ai/artifact/1DhjrEpaiavHtNLXTPwoQD

## Rules that matter most

- The brand colours and the logo are fixed. Do not change them.
- Orange buttons carry navy text (`on-ember`), not white. White on this orange fails contrast checks.
- Small orange text uses `ember-ink`, never `ember`.
- Every stat needs a source line. No source, no stat.
- No em dashes in copy.

## Before going live

- Connect the two forms (quote and newsletter) to a real form handler or CRM. They use `mailto:` for now.
- Confirm every claim on the page with the business: "1 named manager", "3 platforms", "£0 surprise fees", and the FAQ answers.
- Check the tax dates against GOV.UK.
- Add a mobile menu panel for the menu button.
- Create `/privacy-policy`.
