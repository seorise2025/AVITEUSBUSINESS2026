# ServiceCard

A notched card for one service: the top-right corner is cut at 45 degrees and filled with an `ember` fold, like the angled tops of the logo's bars.

**Consumer provides:** an index label ("01 / TAX"), an icon from Icons, a title (max 6 words), 1 to 2 lines of text (max 25 words), and a link.

- Card fill is `ground-alt` on `ground`, or `ground` inside an `.av-alt` band. No border, no resting shadow.
- Cut size is `cut-m`. The fold is always top right.
- Hover lifts 4px and adds `shadow-lift`. The whole card is not a link: only the "Read more" link is.
- Lay cards out with `.av-card-row` (min 240px columns, `space-5` gap). Use 3 or 6 cards, never 4 or 5 in one row.
- The index label uses the `code` style: it gives the grid a ledger feel.

**Do not** put a button inside a card, mix icon styles, or write card copy over 25 words.
