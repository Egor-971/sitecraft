"""Test publication boundaries and archive content, not generated prose."""

import importlib.util
import shutil
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
SPEC = importlib.util.spec_from_file_location("release_builder", ROOT / "scripts/build_release.py")
assert SPEC and SPEC.loader
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)


class ReleaseTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "source"
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns(".git", ".venv", "__pycache__"))
        self.output = Path(self.temporary.name) / "release"

    def test_archive_is_complete_and_reproducible(self):
        first = BUILDER.build_release(self.root, self.output)
        second = BUILDER.build_release(self.root, self.output)
        self.assertEqual(first["sha256"], second["sha256"])
        with zipfile.ZipFile(first["archive"]) as archive:
            self.assertIsNone(archive.testzip())
            for path in (self.root / "plugins/sitecraft").rglob("*"):
                if path.is_file():
                    self.assertEqual(archive.read("sitecraft/" + path.relative_to(self.root).as_posix()), path.read_bytes())

    def test_local_environment_and_work_files_do_not_ship(self):
        for relative in (".env", "docs/.env.local", "docs/work/private.md", "scripts/__pycache__/cache.pyc"):
            path = self.root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("private fixture")
        result = BUILDER.build_release(self.root, self.output)
        with zipfile.ZipFile(result["archive"]) as archive:
            names = archive.namelist()
            self.assertFalse(any(".env" in name or "/work/" in name or "__pycache__" in name for name in names))

    def test_public_symlink_is_rejected(self):
        target = Path(self.temporary.name) / "outside.txt"
        target.write_text("private fixture")
        (self.root / "docs/outside.md").symlink_to(target)
        with self.assertRaisesRegex(ValueError, "symlink"):
            BUILDER.build_release(self.root, self.output)

    def test_private_value_is_rejected_without_logging_it(self):
        secret = "ghp_" + "A" * 30
        (self.root / "docs/accidental-token.md").write_text(secret)
        with self.assertRaisesRegex(ValueError, "credential-like literal") as raised:
            BUILDER.build_release(self.root, self.output)
        self.assertNotIn(secret, str(raised.exception))


if __name__ == "__main__":
    unittest.main()
