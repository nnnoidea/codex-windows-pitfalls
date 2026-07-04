---
name: codex-windows-pitfalls
description: Capture, retrieve, deduplicate, and update hard-won Codex-on-Windows operational pitfalls. Use before running or debugging Windows shell commands, PowerShell, cmd.exe, path handling, backslash or quote escaping, "parameter not found" errors, command failures, blocked or rejected commands, sandbox/escalation requests, Git/SSH on Windows, encoding or mojibake issues, line ending churn, environment-variable reads, or any repeated local failure that should become durable agent memory.
---

# Codex Windows Pitfalls

Use this skill to avoid repeating Windows-specific operational mistakes and to maintain a standalone pitfall knowledge file that can be shared independently of the skill.

## Startup

1. Locate the pitfall knowledge file. Prefer a user-provided path; otherwise look for `.codex-windows-pitfalls.md` in the current workspace or current working directory.
2. If the file exists, generate a startup summary and read that first. The summary contains up to 20 entries, sorted by `Count`; high-frequency entries are prioritized, and lower-frequency entries fill the remaining slots when fewer than 20 entries meet the threshold:

```powershell
python C:\Users\Administrator\.codex\skills\codex-windows-pitfalls\scripts\summarize_pitfalls.py `
  --file .\.codex-windows-pitfalls.md `
  --output .\.codex-windows-pitfalls.frequent.md
```

3. Read `.codex-windows-pitfalls.frequent.md` before planning Windows shell, filesystem, Git, SSH, download, encoding, or approval-sensitive work.
4. Search the full `.codex-windows-pitfalls.md` only when the startup summary does not cover the concrete tool or symptom and the full file has more entries than the summary limit.
5. If no pitfall file exists, continue carefully and create one only when a durable pitfall occurs.
6. Apply the matching "Prefer" guidance before running commands.
7. If a pitfall occurs, record the occurrence to `.codex-windows-pitfalls.md`. Do not modify the installed skill during ordinary task work.

## Recording A New Pitfall

Record only durable, reusable lessons:

- A command failed for a Windows-specific shell, path, quoting, encoding, sandbox, or toolchain reason.
- The same class of mistake is likely to recur.
- There is a safer command pattern, validation step, or escalation rule to use next time.

Do not record transient network outages, private credentials, raw tokens, long logs, or vague "be careful" notes.

Prefer the helper script so the standalone knowledge file stays consistent:

```powershell
python C:\Users\Administrator\.codex\skills\codex-windows-pitfalls\scripts\record_pitfall.py `
  --title "Short symptom" `
  --category shell-quoting `
  --symptom "What failed" `
  --cause "Why it failed" `
  --prefer "Safer repeatable pattern" `
  --avoid "Pattern to avoid" `
  --source "Session, file, or command evidence"
```

By default, the helper writes to `.codex-windows-pitfalls.md` in the current working directory. It never writes to the installed skill and never needs permission to edit the skill package.

If the occurrence matches an existing entry, the helper increments that entry's `Count` and adds the new source instead of appending a duplicate. The `.codex-windows-pitfalls.md` file is the portable pitfall database; it is not part of the skill package and can be copied or shared by itself.

## Growth Hygiene

Keep the standalone knowledge file self-growing but not noisy:

- Search before appending; prefer improving an existing entry over adding a near-duplicate.
- Use `Count` to identify frequent pitfalls. Read the generated top-20 startup summary first.
- When the full file grows beyond the summary limit, leave lower-frequency entries in the full file for targeted lookup after the startup summary misses.
- Periodically merge duplicates and remove entries that are too narrow to guide future work.

## Entry Quality

Each pitfall should be short and operational:

- **Title**: symptom or decision rule, not a story.
- **Category**: one of `powershell`, `path`, `quoting`, `encoding`, `sandbox`, `git-ssh`, `network`, `filesystem`, `line-endings`, `process`, or `other`.
- **Prefer**: the exact safer pattern to try first.
- **Avoid**: the risky pattern that caused or could cause the failure.
- **Count**: occurrence count used to decide Quick Index promotion.
- **Source**: a local session, command output, or artifact reference without secrets.

## When Delivering Work

Mention newly recorded pitfalls in the final response only when relevant to the user's request. Keep the main outcome first; the pitfall note is supporting context.
