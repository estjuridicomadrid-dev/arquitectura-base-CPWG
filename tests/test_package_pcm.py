import tempfile
import unittest
import zipfile
from pathlib import Path

from package_pcm import build_package, validate_package


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class PackageTests(unittest.TestCase):
    def test_archive_contains_installable_pcm_layout(self):
        with tempfile.TemporaryDirectory() as directory:
            archive_path = build_package(
                PROJECT_ROOT, Path(directory) / "plugin.zip"
            )

            with zipfile.ZipFile(archive_path) as archive:
                names = set(archive.namelist())

            self.assertIn("metadata.json", names)
            self.assertIn("plugins/architecture_base_cpwg.py", names)
            self.assertIn("plugins/rf_discontinuity_analyzer.py", names)
            self.assertIn("resources/icon.svg", names)
            self.assertNotIn("architecture_base_cpwg.py", names)

    def test_rejects_archive_missing_pcm_manifest(self):
        with tempfile.TemporaryDirectory() as directory:
            archive_path = Path(directory) / "invalid.zip"
            with zipfile.ZipFile(archive_path, "w") as archive:
                archive.writestr("plugins/plugin.py", "pass")

            with self.assertRaisesRegex(ValueError, "missing files"):
                validate_package(archive_path)


if __name__ == "__main__":
    unittest.main()
