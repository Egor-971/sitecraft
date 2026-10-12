#!/usr/bin/env python3
"""Build a deterministic, checked public archive without local working files."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path

from validate_plugin import validate_repo

PUBLIC_DIRECTORIES = (".agents", ".github", "docs", "plugins", "scripts", "tests")
PUBLIC_FILES = ("README.md", "LICENSE", "CHANGELOG.md", "CONTRIBUTING.md", "requirements-dev.txt", ".gitignore")
EXCLUDED_DIRECTORIES = {".git", ".venv", "__pycache__", "node_modules", "work"}
PRIVATE_VALUES = {
    "local home or clipboard path": re.compile(r"/Users/|/home/|codex-clipboard-[a-f0-9]"),
    "credential-like literal": re.compile(r"\b(?:sk-[A-Za-z0-9_-]{20,}|gh[pousr]_[A-Za-z0-9]{25,}|AIza[A-Za-z0-9_-]{25,})"),
}


def release_files(root: Path) -> list[Path]:
    """Select the public repository, never an arbitrary sibling/work directory."""
    candidates = [root / name for name in PUBLIC_FILES if (root / name).is_file()]
    for directory in PUBLIC_DIRECTORIES:
        start = root / directory
        if not start.exists():
            continue
        for path in start.rglob("*"):
            relative = path.relative_to(root)
            if any(part in EXCLUDED_DIRECTORIES for part in relative.parts):
                continue
            if path.is_symlink():
                raise ValueError(f"symlink cannot be published: {relative}")
            if not path.is_file():
                continue
            if path.name == ".DS_Store" or path.suffix in {".pyc", ".zip"}:
                continue
            if path.name.startswith(".env") and path.name != ".env.example":
                continue
            if path.name == "discussion-archive.txt":
                raise ValueError(f"raw conversation cannot be published: {relative}")
            candidates.append(path)
    return sorted(candidates, key=lambda path: path.relative_to(root).as_posix())


def check_public_text(root: Path, files: list[Path]) -> None:
    """Catch specific accidental disclosures; this is not a security audit."""
    for path in files:
        if path.suffix not in {".md", ".txt", ".json", ".yaml", ".yml"}:
            continue
        text = path.read_text(encoding="utf-8")
        for category, pattern in PRIVATE_VALUES.items():
            if pattern.search(text):
                # Never include the matching value in diagnostics.
                raise ValueError(f"{path.relative_to(root)}: {category}")


def build_release(root: Path, output_directory: Path) -> dict:
    root = root.resolve()
    errors = validate_repo(root)
    if errors:
        raise ValueError("package validation failed: " + "; ".join(errors))
    files = release_files(root)
    check_public_text(root, files)
    version = json.loads((root / "plugins/sitecraft/plugin.json").read_text())["version"]
    output_directory.mkdir(parents=True, exist_ok=True)
    archive_path = output_directory / f"sitecraft-{version}.zip"
    with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in files:
            name = (Path("sitecraft") / path.relative_to(root)).as_posix()
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    with zipfile.ZipFile(archive_path) as archive:
        if archive.testzip() is not None:
            raise ValueError("archive CRC validation failed")
        expected = {(Path("sitecraft") / p.relative_to(root)).as_posix(): p for p in files}
        if set(archive.namelist()) != set(expected):
            raise ValueError("archive file list differs from selected public files")
        for name, path in expected.items():
            if archive.read(name) != path.read_bytes():
                raise ValueError(f"archive differs from source: {name}")
    digest = hashlib.sha256(archive_path.read_bytes()).hexdigest()
    sums_path = output_directory / f"sitecraft-{version}.sha256"
    sums_path.write_text(f"{digest}  {archive_path.name}\n", encoding="utf-8")
    return {"version": version, "archive": str(archive_path), "files": len(files), "sha256": digest}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = build_release(args.root, args.output_dir)
    except (OSError, ValueError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
