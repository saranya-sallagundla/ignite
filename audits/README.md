# Repo audits

Every audit in this folder is named `audit-YYYY-MM-DD.md` — the date it ran, not a topic number
or a description. Because the filename alone doesn't say what an audit covers, **the index below
is the source of truth** for which file covers which milestone — check it before assuming a file
does or doesn't exist for a given topic.

## Index

| Date | Type | Milestone | File |
|---|---|---|---|
| 2026-07-27 | Periodic professionalism audit | after Topic 10 | [`audit-2026-07-27.md`](audit-2026-07-27.md) |
| 2026-08-13 | Public-readiness audit (one-time) | pre-publish, Stage 1 | [`audit-2026-08-13.md`](audit-2026-08-13.md) |

Two kinds of audits live here, both under the same naming scheme:

- **Periodic professionalism audits** — every 10 topics (after Topic 10, 20, 30, 40, 50 clear),
  before starting the next topic. Purpose: catch the kind of drift that accumulates quietly
  across many sessions (inconsistent naming, stale placeholder text, factual errors in
  notebooks, missing repo hygiene files) before the repo is shown to anyone. Each one records
  what was checked, what was found, what was actually fixed, and why each fix mattered — not
  just a raw findings dump.
- **One-time named audits** — cover something other than a topic milestone (e.g. the
  public-readiness audit above, triggered by the repo going public). Same filename convention,
  same rules below, just not tied to the every-10-topics cadence.

## Prompt to start the next periodic audit

> Check if the whole repo can be maintained even more professionally — check each and every
> subfolder and subfile, word by word, line by line and sentence by sentence, and let me know what
> else we can do. Tell me everything, even if it feels like a minute thing, it matters when
> showing the whole repo to higher officials. Save the audit findings and fixes to `audits/`, and
> don't apply any fixes until I review the findings first.

## Rules for every audit
- **Not limited to the categories/items a past audit already found.** `audit-2026-07-27.md`'s
  (the Topic 10 audit's) findings (A-E, plus the batch structure) are a record of what that
  specific audit surfaced, not a fixed checklist future audits are confined to re-checking. Each
  new audit should look at the repo fresh, word by word, and add whatever new issues actually
  turn up as its own findings — an audit means checking everything, not re-verifying a
  predefined list.
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
  and not just the permanent `audits/audit-YYYY-MM-DD.md` record). Copy it as-is — do not redact
  or edit anything (e.g. employer-name instances) in this copy.
- **Add the new file to the index table above** in the same commit — a periodic audit is not
  discoverable by filename alone, so an audit that isn't indexed is effectively invisible to the
  next session's check for whether that milestone's audit has already run.
