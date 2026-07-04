#!/usr/bin/env python3
"""Record a Windows/Codex pitfall occurrence in a workspace artifact."""

from __future__ import annotations

import argparse
import datetime as dt
import re
from pathlib import Path


VALID_CATEGORIES = {
    "powershell",
    "path",
    "quoting",
    "encoding",
    "sandbox",
    "git-ssh",
    "network",
    "filesystem",
    "line-endings",
    "process",
    "environment",
    "git",
    "other",
}


def one_line(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip())


def next_id(text: str) -> str:
    ids = [int(match) for match in re.findall(r"^### P(\d{3}):", text, flags=re.MULTILINE)]
    return f"P{(max(ids) + 1) if ids else 1:03d}"


def normalize(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def existing_entries(text: str) -> list[tuple[str, str, str, str]]:
    pattern = re.compile(
        r"^### (P\d{3}): (?P<title>.+?)\n(?P<body>.*?)(?=^### P\d{3}:|\Z)",
        flags=re.MULTILINE | re.DOTALL,
    )
    entries: list[tuple[str, str, str, str]] = []
    for match in pattern.finditer(text):
        pid = match.group(1)
        title = match.group("title").strip()
        symptom_match = re.search(r"^- Symptom: (.+)$", match.group("body"), flags=re.MULTILINE)
        symptom = symptom_match.group(1).strip() if symptom_match else ""
        entries.append((pid, title, symptom, match.group(0)))
    return entries


def likely_duplicates(text: str, title: str, symptom: str) -> list[tuple[str, str]]:
    title_norm = normalize(title)
    symptom_norm = normalize(symptom)
    matches: list[tuple[str, str]] = []
    for pid, existing_title, existing_symptom, _entry in existing_entries(text):
        existing_title_norm = normalize(existing_title)
        existing_symptom_norm = normalize(existing_symptom)
        if title_norm and title_norm == existing_title_norm:
            matches.append((pid, f"title: {existing_title}"))
            continue
        if symptom_norm and symptom_norm == existing_symptom_norm:
            matches.append((pid, f"symptom: {existing_symptom}"))
            continue
        title_words = set(title_norm.split())
        existing_words = set(existing_title_norm.split())
        shared = title_words & existing_words
        if len(shared) >= 4 and len(shared) >= min(len(title_words), len(existing_words)) / 2:
            matches.append((pid, f"similar title: {existing_title}"))
    return matches


def increment_existing_artifact(text: str, pid: str, source: str, today: str) -> tuple[str, bool]:
    pattern = re.compile(
        rf"(^### {re.escape(pid)}: .+?\n)(.*?)(?=^### P\d{{3}}:|\Z)",
        flags=re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(text)
    if not match:
        return text, False
    header, body = match.group(1), match.group(2)
    count_match = re.search(r"^- Count: (\d+)$", body, flags=re.MULTILINE)
    if count_match:
        count = int(count_match.group(1)) + 1
        body = re.sub(r"^- Count: \d+$", f"- Count: {count}", body, count=1, flags=re.MULTILINE)
    else:
        body = body.rstrip() + "\n- Count: 2\n"
    occurrence = f"- Occurrence: {one_line(source)}; recorded {today}."
    if occurrence not in body:
        body = body.rstrip() + "\n" + occurrence + "\n"
    return text[: match.start()] + header + body + text[match.end() :], True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--file", type=Path, default=Path.cwd() / ".codex-windows-pitfalls.md")
    parser.add_argument("--title", required=True)
    parser.add_argument("--category", required=True)
    parser.add_argument("--symptom", required=True)
    parser.add_argument("--cause", required=True)
    parser.add_argument("--prefer", required=True)
    parser.add_argument("--avoid", required=True)
    parser.add_argument("--source", required=True)
    args = parser.parse_args()

    category = one_line(args.category).lower()
    if category not in VALID_CATEGORIES:
        allowed = ", ".join(sorted(VALID_CATEGORIES))
        raise SystemExit(f"unknown category {category!r}; use one of: {allowed}")

    path = args.file
    text = path.read_text(encoding="utf-8") if path.exists() else "# Pending Codex Windows Pitfalls\n\n"
    today = dt.date.today().isoformat()
    title = one_line(args.title)
    symptom = one_line(args.symptom)
    artifact_matches = likely_duplicates(text, title, symptom)
    if artifact_matches:
        pid = artifact_matches[0][0]
        updated_text, updated = increment_existing_artifact(text, pid, args.source, today)
        if updated:
            path.write_text(updated_text.rstrip() + "\n", encoding="utf-8", newline="\n")
            print(f"Updated {pid} count in {path}")
            return 0

    pid = next_id(text)

    entry = f"""
### {pid}: {title}

- Category: `{category}`
- Symptom: {symptom}
- Cause: {one_line(args.cause)}
- Prefer: {one_line(args.prefer)}
- Avoid: {one_line(args.avoid)}
- Count: 1
- Source: {one_line(args.source)}; recorded {today}.
"""

    path.write_text(text.rstrip() + "\n" + entry, encoding="utf-8", newline="\n")
    print(f"Recorded {pid} in {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
