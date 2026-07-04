#!/usr/bin/env python3
"""Generate a compact startup summary from a pitfall knowledge file."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Pitfall:
    pid: str
    title: str
    category: str
    symptom: str
    prefer: str
    avoid: str
    count: int


def field(body: str, name: str, default: str = "") -> str:
    match = re.search(rf"^- {re.escape(name)}: (.+)$", body, flags=re.MULTILINE)
    return match.group(1).strip() if match else default


def parse_pitfalls(text: str) -> list[Pitfall]:
    pattern = re.compile(
        r"^### (P\d{3}): (?P<title>.+?)\n(?P<body>.*?)(?=^### P\d{3}:|\Z)",
        flags=re.MULTILINE | re.DOTALL,
    )
    pitfalls: list[Pitfall] = []
    for match in pattern.finditer(text):
        body = match.group("body")
        count_text = field(body, "Count", "1")
        try:
            count = int(count_text)
        except ValueError:
            count = 1
        pitfalls.append(
            Pitfall(
                pid=match.group(1),
                title=match.group("title").strip(),
                category=field(body, "Category", "`other`").strip("`"),
                symptom=field(body, "Symptom"),
                prefer=field(body, "Prefer"),
                avoid=field(body, "Avoid"),
                count=count,
            )
        )
    return pitfalls


def select_pitfalls(pitfalls: list[Pitfall], min_count: int, limit: int) -> list[Pitfall]:
    ordered = sorted(pitfalls, key=lambda item: (-item.count, item.pid))
    frequent = [item for item in ordered if item.count >= min_count]
    if len(frequent) >= limit:
        return frequent[:limit]
    frequent_ids = {item.pid for item in frequent}
    fill = [item for item in ordered if item.pid not in frequent_ids]
    return (frequent + fill)[:limit]


def render(pitfalls: list[Pitfall], source: Path, min_count: int, limit: int) -> str:
    selected = select_pitfalls(pitfalls, min_count, limit)
    lines = [
        "# Startup Codex Windows Pitfalls",
        "",
        f"Source: `{source}`",
        f"Selection: up to {limit} entries, sorted by `Count`; entries with `Count >= {min_count}` are prioritized.",
        "",
    ]
    if not selected:
        lines.extend(
            [
                "No pitfall entries found.",
                "",
            ]
        )
        return "\n".join(lines)

    for item in selected:
        lines.extend(
            [
                f"## {item.pid}: {item.title}",
                "",
                f"- Count: {item.count}",
                f"- Category: `{item.category}`",
                f"- Symptom: {item.symptom}",
                f"- Prefer: {item.prefer}",
                f"- Avoid: {item.avoid}",
                "",
            ]
        )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--file", type=Path, default=Path.cwd() / ".codex-windows-pitfalls.md")
    parser.add_argument("--output", type=Path, default=Path.cwd() / ".codex-windows-pitfalls.frequent.md")
    parser.add_argument("--min-count", type=int, default=2)
    parser.add_argument("--limit", type=int, default=20)
    args = parser.parse_args()

    if args.min_count < 1:
        raise SystemExit("--min-count must be >= 1")
    if args.limit < 1:
        raise SystemExit("--limit must be >= 1")
    if not args.file.exists():
        raise SystemExit(f"pitfall file not found: {args.file}")

    pitfalls = parse_pitfalls(args.file.read_text(encoding="utf-8"))
    args.output.write_text(render(pitfalls, args.file, args.min_count, args.limit), encoding="utf-8", newline="\n")
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
