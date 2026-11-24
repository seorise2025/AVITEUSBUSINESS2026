# Field

Label, input and helper text for every form: the hero enquiry form, contact page and newsletter.

**Consumer provides:** a visible label, an input `id`, optional helper text, optional error text.

- Always show a label above the input. Placeholders show an example, never the label.
- Inputs sit on `ground-sunk` with a `line` border; hover turns `line-strong`; focus turns `ember` at 2px.
- On a night panel, inputs flip to a `ground` fill so they read as light fields.
- Errors: add `.av-field--error`. The message uses `ink` text with a `danger` dot and says how to fix it.
- Group fields in `.av-panel` (`--light` for `ember-wash`, or inside `.av-night`).

**Do not** ask for more than 4 fields in a first contact form, or use red text for errors.
