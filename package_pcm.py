#!/usr/bin/env python3
"""Build and validate the KiCad PCM plugin archive."""

import argparse
import json
from pathlib import Path, PurePosixPath
import tempfile
import zipfile

from generate_icons import generate_icon


PACKAGE_FILES = {
    "metadata.json": "metadata.json",
    "LICENSE": "LICENSE",
    "plugins/__init__.py": "plugins/__init__.py",
    "plugins/architecture_base_cpwg.py": "architecture_base_cpwg.py",
    "plugins/rf_discontinuity_analyzer.py": "rf_discontinuity_analyzer.py",
}


def validate_package(archive_path: Path) -> None:
    """Raise ValueError if the archive lacks the expected PCM package layout."""
    with zipfile.ZipFile(archive_path) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)):
            raise ValueError("package archive contains duplicate paths")
        for name in names:
            path = PurePosixPath(name)
            if path.is_absolute() or ".." in path.parts:
                raise ValueError(f"unsafe package path: {name}")

        required_files = set(PACKAGE_FILES) | {"resources/icon.png"}
        missing = required_files - set(names)
        if missing:
            raise ValueError(f"package archive is missing files: {sorted(missing)}")
        png = archive.read("resources/icon.png")
        if (
            not png.startswith(b"\x89PNG\r\n\x1a\n")
            or len(png) < 24
            or int.from_bytes(png[16:20], "big") != 64
            or int.from_bytes(png[20:24], "big") != 64
        ):
            raise ValueError("package icon must be a 64x64 PNG")

        metadata = json.loads(archive.read("metadata.json"))
        required = {
            "name",
            "description",
            "description_full",
            "identifier",
            "type",
            "author",
            "license",
            "resources",
            "versions",
        }
        if required - metadata.keys():
            raise ValueError("package metadata is missing required PCM fields")
        if metadata["type"] != "plugin" or not metadata["versions"]:
            raise ValueError("package metadata must describe a versioned plugin")
        version = metadata["versions"][0]
        if not all(version.get(key) for key in ("version", "status", "kicad_version")):
            raise ValueError("package version needs version, status, and kicad_version")


def build_package(project_root: Path, archive_path: Path) -> Path:
    """Build the PCM ZIP from repository sources and return its path."""
    archive_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as temporary_directory:
        icon_path = generate_icon(Path(temporary_directory) / "resources")
        with zipfile.ZipFile(
            archive_path, "w", compression=zipfile.ZIP_DEFLATED
        ) as archive:
            for package_file, source_file in PACKAGE_FILES.items():
                source = project_root / source_file
                if not source.is_file():
                    raise FileNotFoundError(f"required package file not found: {source}")
                archive.write(source, package_file)
            archive.write(icon_path.with_suffix(".png"), "resources/icon.png")
        validate_package(archive_path)
    return archive_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("arquitectura_base_cpwg_pcm.zip"))
    parser.add_argument("--project-root", type=Path, default=Path(__file__).parent)
    args = parser.parse_args()
    print(build_package(args.project_root, args.output))


if __name__ == "__main__":
    main()
