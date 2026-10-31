# Issues

## Open — decisions for Kristijan

- **Ember + Archivo applied to the Default theme (2026-10-31).** `default.css` and `global.css` now carry these changes:
  - muted text lifted to `#80808f`;
  - swoosh-blue in-text links (`--color-second`) and verdigris `<em>` (`--color-third`);
  - Archivo Expanded headings (`--font-display`).

  Studio, Terminal, Bold and Modern are unchanged. Design source: https://claude.ai/artifact/GJVvbDtksc7cQhuwC9H6LY
- **`--color-text-muted` still fails WCAG AA in Studio, Terminal, Bold and Modern** (2.0–3.1:1 on bg). Default is fixed. Lift the other four, or accept it as part of their look.
- **No dark-ink logo** for a light theme (Paper). Suggested inks: wordmark `#26242a`, swoosh `#1b6d8f` / `#5a5a66`.
- **Bold theme contact button**: white on `#ff6b35` is 2.9:1 (fails AA).
- **Ember tokens not yet in the site**:
  - `--color-on-accent`;
  - status colors;
  - `--chart-1…6`;
  - the copper and swoosh ramps.

  Nothing uses them yet. Add them from the artifact's `tokens.json` when a feature needs them.
