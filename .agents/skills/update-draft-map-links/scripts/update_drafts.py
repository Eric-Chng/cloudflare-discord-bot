#!/usr/bin/env python3
"""Update draft image links without disturbing other draft metadata."""

from __future__ import annotations

import argparse
import json
import os
import re
import tempfile
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse


REPO_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_DRAFTS_PATH = REPO_ROOT / "data" / "drafts.json"


def normalize_map_name(name: str) -> str:
    """Match the lowercase, punctuation-free keys used by the draft command."""
    normalized = name.lower().replace("_", "")
    normalized = re.sub(r"[^a-z0-9\s]", "", normalized)
    return re.sub(r"\s+", " ", normalized).strip()


def current_date() -> str:
    """Return dates in the existing drafts.json style, such as Aug 16, 2026."""
    return datetime.now().astimezone().strftime("%b %d, %Y").replace(" 0", " ")


def validate_url(url: str) -> None:
    parsed = urlparse(url)
    if parsed.scheme != "https" or not parsed.netloc:
        raise ValueError(f"Draft link must be an absolute HTTPS URL: {url!r}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Update map image links and last_updated in data/drafts.json."
    )
    parser.add_argument(
        "--map-link",
        action="append",
        nargs=2,
        required=True,
        metavar=("MAP_NAME", "URL"),
        help="Map name and its exact image URL; repeat for multiple maps.",
    )
    parser.add_argument(
        "--drafts",
        type=Path,
        default=DEFAULT_DRAFTS_PATH,
        help=f"Draft JSON path (default: {DEFAULT_DRAFTS_PATH}).",
    )
    parser.add_argument(
        "--date",
        default=current_date(),
        help="Date stored in last_updated (default: local current date).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate and report changes without writing the file.",
    )
    return parser.parse_args()


def write_json_atomically(path: Path, data: dict[str, object]) -> None:
    serialized = json.dumps(data, indent=4, ensure_ascii=False) + "\n"
    mode = path.stat().st_mode
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", dir=path.parent, delete=False
    ) as handle:
        temporary_path = Path(handle.name)
        handle.write(serialized)
    os.chmod(temporary_path, mode)
    os.replace(temporary_path, path)


def main() -> int:
    args = parse_args()
    drafts_path = args.drafts.resolve()

    with drafts_path.open(encoding="utf-8") as handle:
        drafts = json.load(handle)
    if not isinstance(drafts, dict):
        raise ValueError(f"Expected a JSON object in {drafts_path}")

    requested: dict[str, str] = {}
    display_names: dict[str, str] = {}
    for map_name, url in args.map_link:
        key = normalize_map_name(map_name)
        if not key:
            raise ValueError(f"Map name becomes empty after normalization: {map_name!r}")
        validate_url(url)
        if key in requested and requested[key] != url:
            raise ValueError(f"Conflicting URLs supplied for map key {key!r}")
        requested[key] = url
        display_names[key] = map_name

    changes: list[tuple[str, str]] = []
    for key, url in requested.items():
        status = "updated" if key in drafts else "created"
        existing = drafts.setdefault(key, {})
        if not isinstance(existing, dict):
            raise ValueError(f"Expected object for existing map key {key!r}")
        existing["link"] = url
        existing["last_updated"] = args.date
        changes.append((status, key))

    if not args.dry_run:
        write_json_atomically(drafts_path, drafts)

    mode = "Would change" if args.dry_run else "Changed"
    print(f"{mode} {len(changes)} map entr{'y' if len(changes) == 1 else 'ies'} in {drafts_path}")
    for status, key in changes:
        print(f"- {status}: {key} (from {display_names[key]!r})")
    print(f"- last_updated: {args.date}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
