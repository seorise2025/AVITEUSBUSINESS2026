# Button

Pill buttons for actions, with the signature pairing: an `ember` fill carrying `on-ember` night ink.

Night ink on orange reads 4.7:1. White on the same orange reads only 3.9:1, so the old white label is retired.

**Consumer provides:** a label, an `href` or `type`, an optional trailing arrow icon.

| Variant | Class | Use |
|---|---|---|
| Ember | `.av-btn--ember` | The one main action per view. Hover turns `ember-deep` with `on-ember-deep` white. |
| Outline | `.av-btn--outline` | Second action next to an ember button, on light grounds. |
| Ghost | `.av-btn--ghost` | Second action on `night` bands. |
| Small | `.av-btn--small` | Inside forms and cards. Height 40px. |
| Text link | `.av-link` | "Read more" style links. The underline draws in on hover. |

- Label: verb first, max 4 words, sentence case. "Book a free consultation", "Get my fixed quote".
- Only the ember button gets the arrow by default; the arrow slides 3px on hover.
- Height 48px (40px small), radius `radius-pill`, type `label`.

**Do not** place two ember buttons side by side, write "Click here" or "Submit" for a main action, or set a button in uppercase.
