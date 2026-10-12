"""Observable packaging failures that would prevent correct discovery/use."""

from __future__ import annotations

import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("validator", ROOT / "scripts/validate_plugin.py")
assert SPEC and SPEC.loader
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


class PackageTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "sitecraft"
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns(".git", ".venv", "__pycache__"))

    def test_valid_package(self):
        self.assertEqual(VALIDATOR.validate_repo(self.root), [])

    def test_marketplace_cannot_escape_checkout(self):
        path = self.root / ".agents/plugins/marketplace.json"
        data = json.loads(path.read_text())
        data["plugins"][0]["source"]["path"] = "./../../outside"
        path.write_text(json.dumps(data))
        errors = VALIDATOR.validate_repo(self.root)
        self.assertTrue(any("escaping package path" in error for error in errors), errors)

    def test_missing_runtime_reference_is_rejected(self):
        (self.root / "plugins/sitecraft/references/design-rules.md").unlink()
        errors = VALIDATOR.validate_repo(self.root)
        self.assertTrue(any("broken or escaping link" in error for error in errors), errors)

    def test_runtime_reference_cannot_escape_plugin(self):
        path = self.root / "plugins/sitecraft/skills/sitecraft-create/SKILL.md"
        path.write_text(path.read_text() + "\n[External](../../../../README.md)\n")
        errors = VALIDATOR.validate_repo(self.root)
        self.assertTrue(any("escaping link" in error for error in errors), errors)

    def test_compatibility_version_cannot_drift(self):
        path = self.root / "plugins/sitecraft/.codex-plugin/plugin.json"
        data = json.loads(path.read_text())
        data["version"] = "0.9.0"
        path.write_text(json.dumps(data))
        errors = VALIDATOR.validate_repo(self.root)
        self.assertTrue(any("disagree on version" in error for error in errors), errors)

    def test_missing_skill_entrypoint_is_rejected(self):
        for name in sorted(VALIDATOR.EXPECTED_SKILLS):
            with self.subTest(skill=name):
                path = self.root / f"plugins/sitecraft/skills/{name}/SKILL.md"
                original = path.read_text()
                path.unlink()
                errors = VALIDATOR.validate_repo(self.root)
                self.assertTrue(any("SKILL.md missing" in error for error in errors), errors)
                path.write_text(original)

    def test_missing_upgrade_protocol_is_rejected(self):
        (self.root / "plugins/sitecraft/references/design-upgrade.md").unlink()
        errors = VALIDATOR.validate_repo(self.root)
        self.assertTrue(any("broken or escaping link" in error for error in errors), errors)

    def test_installable_plugin_must_include_license(self):
        (self.root / "plugins/sitecraft/LICENSE").unlink()
        errors = VALIDATOR.validate_repo(self.root)
        self.assertTrue(any("license must accompany" in error for error in errors), errors)

    def test_product_workflow_must_be_available_after_installation(self):
        for name in (
            "product-workflow.md", "product-patterns.md", "sector-research.md",
            "measured-product-study.md",
        ):
            with self.subTest(reference=name):
                path = self.root / "plugins/sitecraft/references" / name
                original = path.read_text()
                path.unlink()
                errors = VALIDATOR.validate_repo(self.root)
                self.assertTrue(any("broken or escaping link" in error for error in errors), errors)
                path.write_text(original)

    def test_malformed_manifest_returns_diagnostics(self):
        path = self.root / "plugins/sitecraft/plugin.json"
        original = path.read_text()
        for field, value in (("version", 13), ("extensions", []), ("extensions", {"com.openai": []}), ("extensions", {"com.openai": {"interface": []}})):
            with self.subTest(field=field, value=value):
                data = json.loads(original)
                data[field] = value
                path.write_text(json.dumps(data))
                self.assertTrue(VALIDATOR.validate_repo(self.root))
        path.write_text(original)

    def test_private_runtime_files_are_rejected(self):
        for name in (".env", ".env.local", "discussion-archive.txt"):
            with self.subTest(name=name):
                path = self.root / "plugins/sitecraft" / name
                path.write_text("private fixture")
                errors = VALIDATOR.validate_repo(self.root)
                self.assertTrue(any("private runtime material" in error for error in errors), errors)
                path.unlink()


if __name__ == "__main__":
    unittest.main()
