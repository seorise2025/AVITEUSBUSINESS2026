# PulseLine

The signature line of the system: a 2px `ember` rule with one heartbeat spike, lifted from the line that runs through the logo.

It says two things at once: the firm's roots in healthcare, and a steady check on your numbers.

**Consumer provides:** the inline SVG (copy the markup from the preview) and a width.

- Short form (160px, ends in a node dot): under section titles inside `.av-heading`.
- Wide form (`preserveAspectRatio="none"`, no dot): across the hero base and the CTA band.
- Stroke is always `stroke-pulse`. Colour is always `ember`.
- Add `.av-pulse--draw` to draw it once on load (1.6s). Reduced motion shows it already drawn.

**Do not** use more than two pulse lines per screen, add a second spike, animate it in a loop, or use it as a loading bar.
