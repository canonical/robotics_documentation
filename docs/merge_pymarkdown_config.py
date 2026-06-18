#!/usr/bin/env python3
"""Merge base and project-specific pymarkdown JSON config files.

Usage:
    python3 merge_pymarkdown_config.py BASE_JSON OVERRIDES_JSON OUTPUT_JSON
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


def deep_merge(base: Any, override: Any) -> Any:
    if isinstance(base, dict) and isinstance(override, dict):
        merged = dict(base)
        for key, value in override.items():
            if key in merged:
                merged[key] = deep_merge(merged[key], value)
            else:
                merged[key] = value
        return merged
    return override


def main() -> int:
    if len(sys.argv) != 4:
        print(
            "Usage: merge_pymarkdown_config.py BASE_JSON OVERRIDES_JSON OUTPUT_JSON",
            file=sys.stderr,
        )
        return 2

    base_path = Path(sys.argv[1])
    overrides_path = Path(sys.argv[2])
    output_path = Path(sys.argv[3])

    base = json.loads(base_path.read_text(encoding="utf-8"))
    overrides = json.loads(overrides_path.read_text(encoding="utf-8"))
    merged = deep_merge(base, overrides)

    output_path.write_text(json.dumps(merged, indent=4) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
