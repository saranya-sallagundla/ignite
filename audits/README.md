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
| 2026-08-26 | Repo organization audit (one-time) | not tied to a topic milestone | [`audit-2026-08-26.md`](audit-2026-08-26.md) |
| 2026-08-31 | Final sign-off audit (one-time) | not tied to a topic milestone — pre-fork/public-facing review | [`audit-2026-08-31.md`](audit-2026-08-31.md) |

Two kinds of audits live here, both under the same naming scheme:

- **Periodic professionalism audits** — every 10 topics (after Topic 10, 20, 30, 40, 50 clear),
  before starting the next topic. Purpose: catch the kind of drift that accumulates quietly
  across many sessions (inconsistent naming, stale placeholder text, factual errors in
  notebooks, missing repo hygiene files) before the repo is shown to anyone. Each one records
  what was checked, what was found, what was actually fixed, and why each fix mattered — not
  just a raw findings dump.
- **One-time named audits** — cover something other than a topic milestone: a public-readiness
  audit, triggered by the repo's visibility changing; a repo organization audit, triggered by a
  direct request to check overall consistency; or a final sign-off audit, triggered by a direct
  request to review the repo as a whole before it's pointed to publicly or forked by strangers
  (broadest scope of the three — includes the pre-build/`engine/` material and a live check of
  every git remote, not just the one currently being worked from). Same filename convention, same
  rules below, just not tied to the every-10-topics cadence.

## Prompts to start each kind of audit

Every prompt below is meant to be reused verbatim next time that kind of audit is due.

### The next periodic audit

> Check if the whole repo can be maintained even more professionally — check each and every
> subfolder and subfile, word by word, line by line and sentence by sentence, and let me know what
> else we can do. Tell me everything, even if it feels like a minute thing, it matters when
> showing the whole repo to higher officials. Save the audit findings and fixes to `audits/`, and
> don't apply any fixes until I review the findings first.

### The next public-readiness audit

> Before this repo's visibility changes again, or as a periodic re-check since exposure and
> novelty both decay: check every file, every commit — not just the working tree — and the live
> GitHub state, for anything that shouldn't be public: secrets, credentials, personal
> identifiers, employer references, or claims the repo can't actually back, such as a license it
> doesn't hold clear rights to grant. Verify against GitHub's API directly rather than trusting
> local files. Save findings to `audits/`, and don't apply any fixes until I review them.

### The next repo organization audit

> Check the whole repo and tell me if it could look more organized — as if you have OCD and want
> everything consistent: file naming, formatting, structure, and any claim that doesn't match
> reality, however small. Not tied to a topic milestone. Save findings to `audits/`, and don't
> apply any fixes until I review them.

### The next final sign-off audit

> Act as a senior software architect with 30+ years at top tech companies. You are meticulous,
> skeptical, and known for catching the smallest gap everyone else misses. This repo has been
> submitted to you for final sign-off before it's released publicly / pointed to for others to
> fork. Read every file, every subfolder, every notebook, word by word — including the pre-build
> material (`MISSION.md`/`CLAUDE.md`/`engine/` and anything a fork would rely on) — and check it
> for accuracy, internal consistency, and whether it's usable by someone with no prior context.
> Verify the live state of every git remote, not just the one currently being worked from —
> a clean local/private copy doesn't mean the actual public destination is clean. Check
> `field_atlas.md` (or the mission's equivalent living reference, if it has one) for currency, and
> propose a concrete, repeatable mechanism for keeping it current going forward, not just a note
> that it could drift. Save findings to `audits/`, and don't apply any fixes until I review them.

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
- **Periodic and final sign-off audits**: defer genuinely topic-specific best-practice items (e.g.
  Dockerfile hardening → Topic 11) to when that topic is actually taught, rather than fixing them
  retroactively — the user should learn them hands-on, not find a pre-made fix waiting. Flag the
  item clearly so the next session teaching that topic knows it's already diagnosed, without
  pre-solving it. Public-readiness and organization audits have no topic-teaching timeline left to
  defer into, so this rule doesn't apply to them.
- Check-in/Check-out timestamps are never touched for formatting/consistency reasons — they're
  the one thing in this repo whose value depends entirely on being real.
- The full standing rules this process enforces live in `CLAUDE.md`'s "Repo quality standards"
  section — each audit should check the repo still holds to those, not just find new issues.
- **If the in-repo record redacts anything** (e.g. employer-name instances, per the
  public-readiness audit), also save an unmodified copy of the raw, pre-redaction findings
  directly under `C:\CloudOps` — not just the scratchpad/temp location it was originally written
  to, and not just the permanent `audits/audit-YYYY-MM-DD.md` record. Copy it as-is, no
  redaction. If nothing needed redacting, skip this — there's no raw version distinct from the
  permanent record to preserve — but say so explicitly in the audit file, as
  `audit-2026-08-26.md` does, so the absence reads as a decision, not an oversight.
- **Ownership is settled — do not re-raise the right-to-publish question.** `audit-2026-08-13.md`
  raised B-1 (whether an employment agreement blocks publishing this repo under an
  individually-held license); `audit-2026-08-31.md` closed it — this is a self-created personal
  learning project, not employer work, confirmed directly and durably recorded there. A future
  audit should not reopen this; if genuinely uncertain, read that resolution note first rather
  than asking again.
- **Add the new file to the index table above** in the same commit — no audit is discoverable by
  filename alone under this naming scheme, so one that isn't indexed is effectively invisible:
  to a future session checking whether a periodic milestone is already covered, and to anyone
  just trying to find out what's in this folder at all.
