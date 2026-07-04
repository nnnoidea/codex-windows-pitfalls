# Codex Windows Pitfalls

Codex on Windows can run into the same small problems again and again: PowerShell quirks, backslash escaping, non-ASCII paths, line-ending noise, sandbox approvals, and Git/SSH network workarounds.

`codex-windows-pitfalls` is a Codex skill for remembering those lessons. The skill tells Codex how to look up and update a pitfall database. The database itself is a separate Markdown file:

```text
.codex-windows-pitfalls.md
```

That file is the important part to keep and share.

## What You Do

- Install or enable the `codex-windows-pitfalls` skill in Codex.
- Keep `.codex-windows-pitfalls.md` in the workspace where Codex can find it.
- Share `.codex-windows-pitfalls.md` when you want another workspace or person to reuse the lessons.
- Review the file occasionally to remove private details, merge weak entries, or promote important patterns.

You do not need to run the recording scripts by hand during normal use.

## What Codex Does

When the skill is triggered, Codex should:

- Find `.codex-windows-pitfalls.md`.
- Generate a short startup summary from it, up to 20 entries sorted by `Count`.
- Read that summary before doing Windows shell, filesystem, Git/SSH, encoding, or sandbox-sensitive work.
- Search the full pitfall file only when the summary does not cover the current symptom.
- Record durable new pitfalls back into `.codex-windows-pitfalls.md`.
- Increment `Count` instead of creating duplicate entries for the same lesson.

## The Pitfall File

Each entry records the symptom, cause, safer pattern, pattern to avoid, source, and `Count`.

`Count` is used for priority. Frequent pitfalls rise into the startup summary; lower-frequency pitfalls stay in the full file for targeted lookup.

Keep secrets, credentials, private raw logs, and long transcripts out of the file.

## Sharing

To share the learned lessons, share `.codex-windows-pitfalls.md`.

The recipient can read it directly. If they also install this skill, Codex can generate summaries from it and keep extending it during future work.

