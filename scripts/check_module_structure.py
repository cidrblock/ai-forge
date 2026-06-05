#!/usr/bin/env python3
"""Validate that every Lola module has the required directory structure.

Auto-discovers modules by finding top-level directories that contain
a ``module/`` subdirectory.

Required layout per module::

    <module-name>/
    └── module/
        ├── AGENTS.md
        ├── mcps.json
        ├── commands/
        ├── skills/
        └── agents/
"""
from __future__ import annotations

import sys
from pathlib import Path

REQUIRED_FILES = ["AGENTS.md", "mcps.json"]
REQUIRED_DIRS = ["commands", "skills", "agents"]


def discover_modules(root: Path) -> list[Path]:
    return sorted(
        d
        for d in root.iterdir()
        if d.is_dir() and not d.name.startswith(".") and (d / "module").is_dir()
    )


def check_module(module_dir: Path) -> list[str]:
    errors: list[str] = []
    module_path = module_dir / "module"

    for filename in REQUIRED_FILES:
        if not (module_path / filename).is_file():
            errors.append(f"{module_dir.name}/module/{filename} missing")

    for dirname in REQUIRED_DIRS:
        if not (module_path / dirname).is_dir():
            errors.append(f"{module_dir.name}/module/{dirname}/ missing")

    return errors


def main() -> int:
    root = Path(".")
    modules = discover_modules(root)

    if not modules:
        print("No Lola modules found (no */module/ directories)")
        return 1

    all_errors: list[str] = []
    for module_dir in modules:
        all_errors.extend(check_module(module_dir))

    if all_errors:
        print("Module structure errors:")
        for error in all_errors:
            print(f"  - {error}")
        return 1

    print(f"All {len(modules)} modules have valid structure")
    return 0


if __name__ == "__main__":
    sys.exit(main())
