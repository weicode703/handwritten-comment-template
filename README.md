# Handwritten Comment Template

Render typed Chinese comments onto a ruled-paper image with a handwritten-style font. The tool aligns lines to consistent left and right edges, centers them in each ruled band, and supports a configurable first-line indent.

## Preview

![Rendered example](examples/preview.png)

## Requirements

- Python 3.10+
- Pillow

Install the dependency:

```powershell
python -m pip install -r requirements.txt
```

## Use

Create a UTF-8 text file with one line per writing row. Keep each line short enough to fit its row; the renderer distributes extra spacing between characters so each line reaches the same right edge.

```powershell
python template.py `
  --paper assets/ruled-paper.png `
  --text-file examples/comment.txt `
  --first-line-indent 48 `
  --output output/comment.png
```

Important options:

- `--first-line-indent`: extra horizontal offset for the first row, in pixels. The default is 48 px (about two characters at the default font size). Set to `0` for no indentation.
- `--left` / `--right`: shared text boundaries in image pixels.
- `--rules`: comma-separated y coordinates of the ruled lines, from top to bottom.
- `--font-size`: font size in pixels.
- `--ink R G B`: text color.

The default ruled-line coordinates and text boundaries match the included `assets/ruled-paper.png`; change them for another paper image. Lines are vertically centered within each pair of rules. Chinese commas, periods, question marks, exclamation marks, semicolons, colons, and enumeration commas render at about 62% of the main font size and stay visually close to adjacent text.

## Font

The bundled `YShiWrittenSC-Regular.ttf` is the open-source YShi-Written Simplified Chinese font. Its license is included in `fonts/OFL.txt`. The font is licensed under the SIL Open Font License 1.1; see the upstream project for attribution and reserved-name details:

- https://github.com/Steve-Yuu/YShi-Written

## License

The template code is licensed under the MIT License. The bundled font remains under its own SIL Open Font License 1.1. The sample paper image and example text are provided for demonstrating the renderer.
