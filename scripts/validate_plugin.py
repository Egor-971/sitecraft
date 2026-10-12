#!/usr/bin/env python3
"""Validate the repository and portable Sitecraft package without modifying it."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit
from urllib.request import urlopen

SCHEMA_URL = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK = re.compile(r"\[[^\]\n]*\]\(([^)\n]+)\)")
EXPECTED_SKILLS = {
    "sitecraft-create", "sitecraft-redesign", "sitecraft-review",
    "sitecraft-elevate", "sitecraft-product",
}


def read_json(path: Path, errors: list[str]) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError("expected a JSON object")
        return data
    except (OSError, ValueError) as exc:
        errors.append(f"{path.name}: {exc}")
        return {}


def inside(root: Path, path: Path) -> bool:
    return path.resolve().is_relative_to(root.resolve())


def mapping(value: object, label: str, errors: list[str]) -> dict:
    if not isinstance(value, dict):
        errors.append(f"{label} must be an object")
        return {}
    return value


def package_path(root: Path, value: str, errors: list[str]) -> Path | None:
    if not isinstance(value, str) or not value.startswith("./"):
        errors.append(f"package path must start with ./: {value!r}")
        return None
    path = (root / value).resolve()
    if not inside(root, path) or not path.exists():
        errors.append(f"missing or escaping package path: {value!r}")
        return None
    return path


def parse_frontmatter(path: Path, strict: bool, errors: list[str]) -> dict:
    content = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---(?:\n|$)", content, re.S)
    if not match:
        errors.append(f"{path.parent.name}: missing frontmatter")
        return {}
    try:
        if strict:
            import yaml

            result = yaml.safe_load(match.group(1))
        else:
            # The package deliberately uses simple scalar frontmatter.
            result = {}
            for line in match.group(1).splitlines():
                key, separator, value = line.partition(":")
                if not separator or key in result:
                    raise ValueError("invalid or duplicate metadata key")
                value = value.strip()
                result[key] = json.loads(value) if value.startswith('"') else value
        if not isinstance(result, dict):
            raise ValueError("metadata must be a mapping")
        return result
    except (ImportError, ValueError) as exc:
        errors.append(f"{path.parent.name}: {exc}")
        return {}
    except Exception as exc:
        # Includes YAML parser errors without a hard dependency in basic mode.
        errors.append(f"{path.parent.name}: invalid YAML: {exc}")
        return {}


def check_links(repo: Path, plugin: Path, errors: list[str]) -> None:
    for path in repo.rglob("*.md"):
        if any(part in {".git", ".venv", "work", "__pycache__"} for part in path.parts):
            continue
        text = path.read_text(encoding="utf-8")
        for raw in LINK.findall(text):
            target = raw.strip().split(' "', 1)[0].strip("<>")
            if not target or target.startswith("#") or urlsplit(target).scheme:
                continue
            destination = (path.parent / unquote(target.split("#", 1)[0])).resolve()
            boundary = plugin if inside(plugin, path) else repo
            if not inside(boundary, destination) or not destination.exists():
                errors.append(f"{path.relative_to(repo)}: broken or escaping link {target!r}")


def validate_repo(repo: Path, *, strict: bool = False, schema_path: Path | None = None) -> list[str]:
    repo = repo.resolve()
    errors: list[str] = []
    marketplace = read_json(repo / ".agents/plugins/marketplace.json", errors)
    plugin = repo / "plugins/sitecraft"
    portable = read_json(plugin / "plugin.json", errors)
    compatibility = read_json(plugin / ".codex-plugin/plugin.json", errors)

    if marketplace.get("name") != "sitecraft-marketplace":
        errors.append("unexpected marketplace name")
    entries = marketplace.get("plugins", [])
    if not isinstance(entries, list) or len(entries) != 1:
        errors.append("expected one marketplace entry")
    else:
        entry = entries[0]
        if not isinstance(entry, dict):
            errors.append("marketplace entry must be an object")
        else:
            source = entry.get("source", {})
            if not isinstance(source, dict) or source.get("source") != "local":
                errors.append("expected a local source within the marketplace checkout")
            elif package_path(repo, source.get("path"), errors) != plugin.resolve():
                errors.append("marketplace source does not resolve to Sitecraft")
            if entry.get("name") != portable.get("name"):
                errors.append("marketplace and package names differ")
            policy = entry.get("policy", {})
            if not isinstance(policy, dict) or policy.get("installation") != "AVAILABLE" or policy.get("authentication") != "ON_INSTALL":
                errors.append("marketplace policy is incomplete")
            if entry.get("category") != "Productivity":
                errors.append("marketplace category is missing")

    if portable.get("$schema") != SCHEMA_URL:
        errors.append("portable manifest schema identifier is incorrect")
    if portable.get("name") != "sitecraft":
        errors.append("package name must be sitecraft")
    version = portable.get("version", "")
    if not isinstance(version, str) or not re.fullmatch(r"\d+\.\d+\.\d+", version):
        errors.append("package version is not stable semver")
    if portable.get("license") != "MIT" or not (repo / "LICENSE").is_file() or not (plugin / "LICENSE").is_file():
        errors.append("MIT license must accompany both repository and installable plugin")
    for field in ("name", "version", "description", "license", "keywords", "author", "repository", "homepage"):
        if portable.get(field) != compatibility.get(field):
            errors.append(f"portable and compatibility manifests disagree on {field}")
    if compatibility.get("skills") != "./skills/":
        errors.append("compatibility skill path is incorrect")
    extensions = mapping(portable.get("extensions", {}), "extensions", errors)
    extension = mapping(extensions.get("com.openai", {}), "com.openai extension", errors)
    interface = mapping(extension.get("interface", {}), "plugin interface", errors)
    if interface != compatibility.get("interface"):
        errors.append("portable and compatibility presentation disagree")
    for field in ("composerIcon", "logo"):
        package_path(plugin, interface.get(field), errors)
    # This package promises no server, hooks, external connections or activation script.
    for field in ("apps", "hooks", "mcpServers"):
        if field in extension or field in compatibility:
            errors.append(f"unexpected active component: {field}")

    found = {p.name for p in (plugin / "skills").iterdir() if p.is_dir()} if (plugin / "skills").exists() else set()
    if found != EXPECTED_SKILLS:
        errors.append(f"unexpected skill set: {sorted(found)}")
    for name in sorted(EXPECTED_SKILLS & found):
        directory = plugin / "skills" / name
        skill_file = directory / "SKILL.md"
        if not skill_file.is_file():
            errors.append(f"{name}: SKILL.md missing")
            continue
        metadata = parse_frontmatter(skill_file, strict, errors)
        if metadata.get("name") != name or not NAME.fullmatch(name) or len(name) > 64:
            errors.append(f"{name}: skill identity is invalid")
        description = metadata.get("description", "")
        if not isinstance(description, str) or not 20 <= len(description) <= 1024:
            errors.append(f"{name}: description is missing or invalid")
        ui_file = directory / "agents/openai.yaml"
        if not ui_file.is_file():
            errors.append(f"{name}: UI metadata missing")
            continue
        if strict:
            try:
                import yaml

                ui = yaml.safe_load(ui_file.read_text(encoding="utf-8"))
                ui_interface = ui.get("interface", {})
                if not 25 <= len(ui_interface.get("short_description", "")) <= 64:
                    errors.append(f"{name}: UI short description length is invalid")
                if f"${name}" not in ui_interface.get("default_prompt", ""):
                    errors.append(f"{name}: UI prompt does not invoke its skill")
                if ui.get("policy", {}).get("allow_implicit_invocation") is not True:
                    errors.append(f"{name}: implicit discovery must remain enabled")
            except Exception as exc:
                errors.append(f"{name}: invalid UI YAML: {exc}")

    check_links(repo, plugin, errors)
    for path in plugin.rglob("*"):
        if path.is_symlink():
            errors.append(f"symlink is not portable: {path.relative_to(plugin)}")
        if path.is_file() and (path.name == "discussion-archive.txt" or path.name == ".env" or path.name.startswith(".env.") and path.name != ".env.example"):
            errors.append(f"private runtime material must not ship: {path.relative_to(plugin)}")

    if strict:
        try:
            import jsonschema

            if schema_path:
                schema = json.loads(schema_path.read_text(encoding="utf-8"))
            else:
                with urlopen(SCHEMA_URL, timeout=15) as response:
                    raw = response.read(100_001)
                if len(raw) > 100_000:
                    raise ValueError("schema response unexpectedly large")
                schema = json.loads(raw)
            jsonschema.Draft202012Validator(schema).validate(portable)
        except Exception as exc:
            errors.append(f"official JSON Schema validation failed: {exc}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--strict", action="store_true", help="parse YAML and validate against the official schema")
    parser.add_argument("--schema", type=Path, help="use a downloaded schema for offline strict validation")
    args = parser.parse_args()
    errors = validate_repo(args.root, strict=args.strict, schema_path=args.schema)
    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print(f"PASS: manifests, marketplace, {len(EXPECTED_SKILLS)} skills, links and package paths" + ("; YAML and official JSON Schema" if args.strict else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
