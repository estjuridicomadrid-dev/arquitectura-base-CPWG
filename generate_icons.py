#!/usr/bin/env python3
"""Generate the package's scalable vector icon without external dependencies."""

import argparse
from pathlib import Path


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


def generate_icon(output_dir: Path) -> Path:
    """Write the package icon to output_dir and return its path."""
    output_dir.mkdir(parents=True, exist_ok=True)
    icon_path = output_dir / "icon.svg"
    icon_path.write_text(SVG_ICON, encoding="utf-8")
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
