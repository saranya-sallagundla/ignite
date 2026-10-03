# Repo audits

Periodic, full-repo professionalism audits — every 10 topics (after Topic 10, 20, 30, 40, 50
clear), before starting the next topic. Purpose: catch the kind of drift that accumulates
quietly across many sessions (inconsistent naming, stale placeholder text, factual errors in
notebooks, missing repo hygiene files) before the repo is shown to anyone.

One file per milestone: `topic-N-audit.md`. Each records what was checked, what was found, what
was actually fixed, and why each fix mattered — not just a raw findings dump.

## Prompt to start the next one

> Check if the whole repo can be maintained even more professionally — check each and every
> subfolder and subfile, word by word, line by line and sentence by sentence, and let me know what
> else we can do. Tell me everything, even if it feels like a minute thing, it matters when
> showing the whole repo to higher officials. Save the audit findings and fixes to `audits/`, and
> don't apply any fixes until I review the findings first.

## Rules for every audit
- Findings first, fixes only after the user reviews them — never apply silently.
- Categorize by severity (critical / important / minor / cosmetic) so the user can prioritize.
- Fix in small, reviewable, individually-committed batches, not one giant commit.
- Defer genuinely topic-specific best-practice items (e.g. Dockerfile hardening → Topic 11) to
  when that topic is actually taught, rather than fixing them retroactively — the user should
  learn them hands-on, not find a pre-made fix waiting.
- Check-in/Check-out timestamps are never touched for formatting/consistency reasons — they're
  the one thing in this repo whose value depends entirely on being real.
- The full standing rules this process enforces live in `CLAUDE.md`'s "Repo quality standards"
  section — each audit should check the repo still holds to those, not just find new issues.
- After the audit report is produced, save an unmodified copy of the raw findings report directly
  under `C:\CloudOps` (not just the scratchpad/temp location the report was originally written to,
  and not just the permanent `audits/topic-N-audit.md` record). Copy it as-is — do not redact or
  edit anything (e.g. employer-name instances) in this copy.
