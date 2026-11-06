#!/usr/bin/env python3
"""Generate the package's scalable vector icon without external dependencies."""

import argparse
import math
from pathlib import Path
import struct
import zlib


SVG_ICON = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">
  <rect width="128" height="128" rx="20" fill="#17324d"/>
  <path d="M18 42h28l10 12h16l10-12h28M18 86h28l10-12h16l10 12h28"
        fill="none" stroke="#f2b84b" stroke-linecap="round"
        stroke-linejoin="round" stroke-width="8"/>
  <path d="M18 64h36m20 0h36" fill="none" stroke="#fff"
        stroke-linecap="round" stroke-width="8"/>
  <circle cx="64" cy="64" r="8" fill="#f2b84b"/>
</svg>
"""

ICON_SIZE = 64
SUPERSAMPLING = 4
BACKGROUND = (23, 50, 77, 255)
ACCENT = (242, 184, 75, 255)
WHITE = (255, 255, 255, 255)


def _png_chunk(kind: bytes, data: bytes) -> bytes:
    content = kind + data
    return (
        struct.pack(">I", len(data))
        + content
        + struct.pack(">I", zlib.crc32(content) & 0xFFFFFFFF)
    )


def _write_png(pixels: list[list[tuple[int, int, int, int]]], path: Path) -> None:
    raw = b"".join(
        b"\x00" + bytes(channel for pixel in row for channel in pixel)
        for row in pixels
    )
    png = b"\x89PNG\r\n\x1a\n"
    png += _png_chunk(
        b"IHDR",
        struct.pack(">IIBBBBB", ICON_SIZE, ICON_SIZE, 8, 6, 0, 0, 0),
    )
    png += _png_chunk(b"IDAT", zlib.compress(raw))
    png += _png_chunk(b"IEND", b"")
    path.write_bytes(png)


def _generate_png(path: Path) -> None:
    scale = ICON_SIZE * SUPERSAMPLING // 128
    size = ICON_SIZE * SUPERSAMPLING
    pixels = [[(0, 0, 0, 0) for _ in range(size)] for _ in range(size)]

    for y in range(size):
        for x in range(size):
            corner_radius = 20 * scale
            corner_x = max(corner_radius - x, 0, x - (size - 1 - corner_radius))
            corner_y = max(corner_radius - y, 0, y - (size - 1 - corner_radius))
            if (
                corner_x * corner_x + corner_y * corner_y
                <= corner_radius**2
            ):
                pixels[y][x] = BACKGROUND

    def draw_line(
        start: tuple[float, float],
        end: tuple[float, float],
        color: tuple[int, int, int, int],
        width: float,
    ) -> None:
        x1, y1 = (coordinate * scale for coordinate in start)
        x2, y2 = (coordinate * scale for coordinate in end)
        radius = width * scale / 2
        min_x = max(0, math.floor(min(x1, x2) - radius))
        max_x = min(size - 1, math.ceil(max(x1, x2) + radius))
        min_y = max(0, math.floor(min(y1, y2) - radius))
        max_y = min(size - 1, math.ceil(max(y1, y2) + radius))
        dx, dy = x2 - x1, y2 - y1
        length_squared = dx * dx + dy * dy
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                projection = (
                    0
                    if length_squared == 0
                    else min(
                        1,
                        max(
                            0,
                            ((x - x1) * dx + (y - y1) * dy) / length_squared,
                        ),
                    )
                )
                distance = math.hypot(
                    x - (x1 + projection * dx), y - (y1 + projection * dy)
                )
                if distance <= radius:
                    pixels[y][x] = color

    def draw_polyline(
        points: tuple[tuple[float, float], ...],
        color: tuple[int, int, int, int],
        width: float,
    ) -> None:
        for start, end in zip(points, points[1:]):
            draw_line(start, end, color, width)

    draw_polyline(
        ((18, 42), (46, 42), (56, 54), (72, 54), (82, 42), (110, 42)),
        ACCENT,
        8,
    )
    draw_polyline(
        ((18, 86), (46, 86), (56, 74), (72, 74), (82, 86), (110, 86)),
        ACCENT,
        8,
    )
    draw_line((18, 64), (54, 64), WHITE, 8)
    draw_line((74, 64), (110, 64), WHITE, 8)

    center, radius = 64 * scale, 8 * scale
    for y in range(center - radius, center + radius + 1):
        for x in range(center - radius, center + radius + 1):
            if (x - center) ** 2 + (y - center) ** 2 <= radius**2:
                pixels[y][x] = ACCENT

    downsampled = []
    for y in range(ICON_SIZE):
        row = []
        for x in range(ICON_SIZE):
            samples = [
                pixels[sy][sx]
                for sy in range(y * scale, (y + 1) * scale)
                for sx in range(x * scale, (x + 1) * scale)
            ]
            row.append(
                tuple(
                    sum(sample[channel] for sample in samples) // len(samples)
                    for channel in range(4)
                )
            )
        downsampled.append(row)
    _write_png(downsampled, path)


def generate_icon(output_dir: Path) -> Path:
    """Write SVG and 64x64 PNG package icons; return the SVG path."""
    output_dir.mkdir(parents=True, exist_ok=True)
    icon_path = output_dir / "icon.svg"
    icon_path.write_text(SVG_ICON, encoding="utf-8")
    _generate_png(output_dir / "icon.png")
    return icon_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("resources"),
        help="directory where resources/icon.svg will be written",
    )
    args = parser.parse_args()
    print(generate_icon(args.output_dir))


if __name__ == "__main__":
    main()
