#!/usr/bin/env python3
"""Convert font glyphs to SVG path data for logo creation."""

from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen


def get_glyph_paths(font_path, text, font_size=44):
    """Extract SVG path data for each character in text."""
    font = TTFont(font_path)
    glyph_set = font.getGlyphSet()

    units_per_em = font["head"].unitsPerEm
    scale = font_size / units_per_em

    ascender = font["OS/2"].sTypoAscender * scale
    descender = font["OS/2"].sTypoDescender * scale

    cmap = font.getBestCmap()

    paths = []
    x_offset = 0

    for char in text:
        code_point = ord(char)
        if code_point not in cmap:
            print(f"Warning: character '{char}' not found in font")
            continue

        glyph_name = cmap[code_point]
        glyph = glyph_set[glyph_name]

        advance_width = glyph.width * scale

        pen = SVGPathPen(glyph_set)
        glyph.draw(pen)
        path_data = pen.getCommands()

        if path_data:
            paths.append({
                "char": char,
                "path": path_data,
                "x_offset": x_offset,
                "advance_width": advance_width,
                "scale": scale,
            })

        x_offset += advance_width

    return paths, scale, ascender, descender, x_offset


def build_svg_paths(paths, scale, ascender, group_x_offset=0, letter_spacing=0):
    """Build SVG path elements with transforms."""
    elements = []
    extra_spacing = 0

    for i, p in enumerate(paths):
        x = p["x_offset"] + group_x_offset + extra_spacing
        transform = f'translate({x:.2f}, {ascender:.2f}) scale({scale:.6f}, -{scale:.6f})'
        elements.append(f'    <path d="{p["path"]}" transform="{transform}"/>')
        extra_spacing += letter_spacing

    return elements


def make_swoosh(cx, top, bottom, stroke_w=7.5):
    """
    Create the swoosh mark (abstract I) between META and NTELLECT.

    Two simple arc-like curves:
    - Dark: starts upper-right, bows left, ends lower-left
    - Blue: starts upper-left, bows right, ends lower-right
    Dark is rendered first so blue appears on top at the crossing.
    """
    height = bottom - top
    mid_y = top + height * 0.5

    overshoot = height * 0.25

    # Dark/gray curve: same length as blue, but shifted UP so it doesn't hang as low
    dark_shift = -overshoot * 0.5  # shift the whole curve up
    dark_start_x = cx - 4
    dark_start_y = top + dark_shift
    dark_end_x = cx - 6
    dark_end_y = bottom + overshoot + dark_shift
    # Curvy — bows right (same radius as blue)
    dark_cp1_x = cx + 12
    dark_cp1_y = top + height * 0.45 + dark_shift
    dark_cp2_x = cx + 12
    dark_cp2_y = top + height * 0.8 + dark_shift

    # Blue curve: starts well ABOVE font top, ends at font bottom, bows LEFT
    blue_start_x = cx + 6
    blue_start_y = top - overshoot
    blue_end_x = cx + 8
    blue_end_y = bottom
    # Curvy — bows left
    blue_cp1_x = cx - 14
    blue_cp1_y = top + height * 0.2
    blue_cp2_x = cx - 14
    blue_cp2_y = top + height * 0.55

    dark_path = (
        f"M {dark_start_x:.1f} {dark_start_y:.1f} "
        f"C {dark_cp1_x:.1f} {dark_cp1_y:.1f}, "
        f"{dark_cp2_x:.1f} {dark_cp2_y:.1f}, "
        f"{dark_end_x:.1f} {dark_end_y:.1f}"
    )

    blue_path = (
        f"M {blue_start_x:.1f} {blue_start_y:.1f} "
        f"C {blue_cp1_x:.1f} {blue_cp1_y:.1f}, "
        f"{blue_cp2_x:.1f} {blue_cp2_y:.1f}, "
        f"{blue_end_x:.1f} {blue_end_y:.1f}"
    )

    # Both lean left together
    lean_angle = -30
    pivot_y = (top + bottom) / 2
    return f"""  <!-- Swoosh mark (abstract I) — leaning left -->
  <g transform="rotate({lean_angle}, {cx:.1f}, {pivot_y:.1f})">
    <path d="{dark_path}" stroke="#52525e" stroke-width="{stroke_w}" fill="none" stroke-linecap="round"/>
    <path d="{blue_path}" stroke="#4ab8e8" stroke-width="{stroke_w}" fill="none" stroke-linecap="round"/>
  </g>"""


def main():
    fonts = [
        ("/Users/x/Library/Fonts/EurostileBQ-Extended.otf", "Eurostile BQ Extended", "bq"),
        ("/Users/x/Library/Fonts/Eurostile LT Extended #2.ttf", "Eurostile LT Extended Two", "lt"),
    ]

    font_size = 44
    letter_spacing = 2.0
    swoosh_gap = 40  # space for the swoosh

    for font_path, font_name, short_name in fonts:
        print(f"\n{'='*60}")
        print(f"Font: {font_name}")
        print(f"{'='*60}")

        # META
        meta_paths, scale, ascender, descender, meta_width = get_glyph_paths(
            font_path, "META", font_size
        )
        meta_total = meta_width + letter_spacing * (len("META") - 1)

        # NTELLECT
        nt_paths, _, _, _, nt_width = get_glyph_paths(
            font_path, "NTELLECT", font_size
        )
        nt_total = nt_width + letter_spacing * (len("NTELLECT") - 1)

        nt_x_offset = meta_total + swoosh_gap
        total_width = nt_x_offset + nt_total
        total_height = ascender - descender + 10

        # Padding — extra vertical for swoosh overshoot
        pad_x = 4
        pad_y = 4
        swoosh_overshoot = total_height * 0.25

        vb_width = total_width + pad_x * 2
        vb_height = total_height + pad_y * 2 + swoosh_overshoot * 2

        print(f"  META width: {meta_total:.2f}")
        print(f"  Swoosh at x: {meta_total:.2f} to {nt_x_offset:.2f}")
        print(f"  NTELLECT offset: {nt_x_offset:.2f}")
        print(f"  Total: {vb_width:.1f} x {vb_height:.1f}")

        # Build text paths — offset down by swoosh overshoot
        text_y_offset = pad_y + swoosh_overshoot
        meta_elements = build_svg_paths(meta_paths, scale, ascender + text_y_offset, pad_x, letter_spacing)
        nt_elements = build_svg_paths(nt_paths, scale, ascender + text_y_offset, nt_x_offset + pad_x, letter_spacing)

        paths_str = "\n".join(meta_elements + nt_elements)

        # Swoosh — top/bottom aligned with text, overshoots beyond
        swoosh_cx = meta_total + swoosh_gap / 2 + pad_x
        swoosh_top = text_y_offset + 1
        swoosh_bottom = text_y_offset + total_height - 3
        swoosh_str = make_swoosh(swoosh_cx, swoosh_top, swoosh_bottom)

        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {vb_width:.1f} {vb_height:.1f}" fill="none">
  <!-- {font_name} | {font_size}px -->
  <g fill="#d0d0d6">
{paths_str}
  </g>

{swoosh_str}
</svg>'''

        output_path = f"/Users/x/src/metaintellect-site/public/logo-{short_name}.svg"
        with open(output_path, "w") as f:
            f.write(svg)
        print(f"  Saved: {output_path}")

    # Also generate a combined comparison page
    comparison = '''<!DOCTYPE html>
<html>
<head>
<style>
  body { background: #08080c; margin: 40px; font-family: sans-serif; color: #999; }
  .row { margin-bottom: 40px; }
  h3 { margin-bottom: 10px; font-weight: 300; }
  img { height: 48px; display: block; margin-bottom: 8px; }
  .original { background: white; display: inline-block; padding: 10px 20px; border-radius: 4px; margin-bottom: 8px; }
  .original img { height: 40px; }
</style>
</head>
<body>
<div class="row">
  <h3>Original (PNG on white background)</h3>
  <div class="original"><img src="/logo-original.png" alt="original"></div>
</div>
<div class="row">
  <h3>Eurostile BQ Extended</h3>
  <img src="/logo-bq.svg" alt="BQ Extended">
</div>
<div class="row">
  <h3>Eurostile LT Extended Two</h3>
  <img src="/logo-lt.svg" alt="LT Extended Two">
</div>
</body>
</html>'''

    with open("/Users/x/src/metaintellect-site/public/logo-compare.html", "w") as f:
        f.write(comparison)
    print(f"\n  Comparison page: /logo-compare.html")


if __name__ == "__main__":
    main()
