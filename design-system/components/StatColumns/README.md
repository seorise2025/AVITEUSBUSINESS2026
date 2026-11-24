# StatColumns

Three proof points shown as rising columns with cut tops: the logo's bars, turned into a chart.

**Consumer provides:** 3 stats, each with a value, a label (max 7 words), a source line and a column height.

- Values use `figure-xl` (JetBrains Mono, tabular). Labels use `body-s`.
- Columns rise left to right in `slate`, `ember-glow`, then `ember` (set `--bar` and `--h`). The tallest column is always the last.
- Every stat carries a source line in the `code` style. No source, no stat.

**Do not** show percentages without a base ("90% of what?"), invent awards, or use more than 3 columns.
