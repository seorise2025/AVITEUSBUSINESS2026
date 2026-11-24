# Header

The site header: a thin `night-deep` top bar with contact details, then a white bar with the logo, menu links and the main action.

**Consumer provides:** the logo link, 4 to 5 menu links with the current page marked `aria-current="page"`, one ember button, the menu toggle.

- Top bar: `body-s`, `on-night-muted`; the phone number is set in figures so it is easy to read.
- The current link gets a 2px `ember` underline. Hover shows the same line.
- In Night Ledger the logo sits on its `plate`.
- Below 1100px, hide the links and keep the logo, button and toggle.

**Do not** add a search icon until search exists, or more than one button.
