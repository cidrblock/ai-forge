#!/usr/bin/env python3
"""Validate that every command .md file has valid YAML frontmatter.

Checks all ``*/module/commands/*.md`` files for:
- Presence of YAML frontmatter (file starts with ``---``)
- A ``description`` field in the frontmatter
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml


def extract_frontmatter(path: Path) -> dict | None:
    """Return parsed frontmatter dict, or None if missing/invalid."""
    content = path.read_text(encoding="utf-8")
    if not content.startswith("---"):
        return None

    parts = content.split("---", 2)
    if len(parts) < 3:
        return None

    try:
        return yaml.safe_load(parts[1])
    except yaml.YAMLError:
        return None


def main() -> int:
    root = Path(".")
    command_files = sorted(root.glob("*/module/commands/*.md"))

    if not command_files:
        print("No command files found")
        return 0

    errors: list[str] = []
    for cmd_file in command_files:
        fm = extract_frontmatter(cmd_file)
        if fm is None:
            errors.append(f"{cmd_file}: missing or invalid frontmatter")
            continue
        if "description" not in fm:
            errors.append(f"{cmd_file}: missing 'description' field")

    if errors:
        print("Command frontmatter errors:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(f"All {len(command_files)} command files have valid frontmatter")
    return 0


if __name__ == "__main__":
    sys.exit(main())
