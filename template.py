from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


DEFAULT_RULES = "5,78,150,222,295,367,439"
CLOSING_PUNCTUATION = set("，。！？；：、）》】」』〕〉”’…％")
OPENING_PUNCTUATION = set("（《【「『〔〈“‘")


def parse_rules(value: str) -> list[int]:
    rules = [int(item.strip()) for item in value.split(",") if item.strip()]
    if len(rules) < 2:
        raise argparse.ArgumentTypeError("rules needs at least two y coordinates")
    return rules


def load_lines(text_file: Path) -> list[str]:
    lines = [line.strip() for line in text_file.read_text(encoding="utf-8").splitlines()]
    lines = [line for line in lines if line]
    if not lines:
        raise ValueError("text file does not contain any non-empty lines")
    return lines


def draw_justified_line(
    draw: ImageDraw.ImageDraw,
    line: str,
    font: ImageFont.FreeTypeFont,
    left: int,
    right: int,
    y: int,
    fill: tuple[int, int, int],
) -> None:
    widths = [draw.textlength(char, font=font) for char in line]
    natural_width = sum(widths)
    if natural_width > right - left:
        raise ValueError(f"line is too long for the configured text box: {line}")
    spacing_slots = sum(
        current not in CLOSING_PUNCTUATION
        and following not in CLOSING_PUNCTUATION
        and current not in OPENING_PUNCTUATION
        and following not in OPENING_PUNCTUATION
        for current, following in zip(line, line[1:])
    )
    extra = (right - left - natural_width) / max(1, spacing_slots)
    x = float(left)
    for index, (char, width) in enumerate(zip(line, widths)):
        draw.text((round(x), y), char, font=font, fill=fill)
        x += width
        if index < len(line) - 1 and (
            char not in CLOSING_PUNCTUATION
            and line[index + 1] not in CLOSING_PUNCTUATION
            and char not in OPENING_PUNCTUATION
            and line[index + 1] not in OPENING_PUNCTUATION
        ):
            x += extra


def render(args: argparse.Namespace) -> Path:
    image = Image.open(args.paper).convert("RGB")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(str(args.font), args.font_size)
    rules = parse_rules(args.rules)
    lines = load_lines(args.text_file)
    if len(lines) > len(rules) - 1:
        raise ValueError(f"text has {len(lines)} lines, but paper has {len(rules) - 1} writing bands")

    for index, line in enumerate(lines):
        band_top, band_bottom = rules[index], rules[index + 1]
        indent = args.first_line_indent if index == 0 else 0
        left = args.left + indent
        y = band_top + (band_bottom - band_top - font.getbbox(line)[3]) // 2 - args.baseline_adjust
        draw_justified_line(draw, line, font, left, args.right, y, args.ink)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    image.save(args.output)
    return args.output


def main() -> None:
    parser = argparse.ArgumentParser(description="Render aligned handwritten comments on ruled paper.")
    parser.add_argument("--paper", type=Path, required=True, help="Blank ruled-paper image")
    parser.add_argument("--text-file", type=Path, required=True, help="UTF-8 text file, one output line per row")
    parser.add_argument("--font", type=Path, default=Path("fonts/YShiWrittenSC-Regular.ttf"))
    parser.add_argument("--output", type=Path, default=Path("output/comment.png"))
    parser.add_argument("--rules", default=DEFAULT_RULES, help="Comma-separated horizontal rule y coordinates")
    parser.add_argument("--left", type=int, default=34)
    parser.add_argument("--right", type=int, default=520)
    parser.add_argument("--first-line-indent", type=int, default=48)
    parser.add_argument("--font-size", type=int, default=24)
    parser.add_argument("--baseline-adjust", type=int, default=2)
    parser.add_argument("--ink", type=int, nargs=3, default=(49, 49, 49), metavar=("R", "G", "B"))
    args = parser.parse_args()
    args.output = args.output.resolve()
    print(render(args))


if __name__ == "__main__":
    main()
