# Issues

## Open — decisions for Kristijan

- **Palette: Ember chosen (2026-10-31), not on the site yet.** Ember is Ember AA (today's ground and copper, with text-muted lifted) plus Patina's verdigris. The three hues have three jobs: copper `#c8956a` for actions, swoosh blue `#4ab8e8` for in-text links, verdigris `#5fb8a8` for emphasis. It's a theme in the Design System artifact https://claude.ai/artifact/GJVvbDtksc7cQhuwC9H6LY. Decision needed: apply it as the new default theme, or add it as a sixth switcher theme.
- **Fonts: pick a pairing** (2026-10-31). The artifact's TypeOptions card recommends Archivo Expanded for headings only, to echo the Eurostile Extended wordmark, with Inter and JetBrains Mono kept. The alternatives are Geist + Geist Mono and IBM Plex Sans + Plex Mono. All are OFL and on Google Fonts, and none needs installing for the site.
- **`--color-text-muted` fails WCAG AA in all 5 themes** (2.0–3.1:1 on bg). Ember lifts default `#5c5c6e` → `#80808f` (≥4.5:1).
- **No dark-ink logo** for a light theme (Paper). Suggested inks: wordmark `#26242a`, swoosh `#1b6d8f` / `#5a5a66`.
- **Bold theme contact button**: white on `#ff6b35` is 2.9:1 (fails AA).
- **New variables Ember needs in `global.css`**:
  - `--color-second` and `--color-third`, the two counter-hues;
  - `--color-on-accent` for text on accent fills;
  - the status colors `--color-success|warning|danger|info`;
  - `--chart-1…6`;
  - the `--copper-*` and `--swoosh-*` ramps.

  The values are in the artifact's `tokens.json`, contrast-checked for all themes.
