# Repo audits

Every audit in this folder is named `audit-YYYY-MM-DD.md` — the date it ran, not a topic number
or a description. Because the filename alone doesn't say what an audit covers, **the index below
is the source of truth** for which file covers which milestone — check it before assuming a file
does or doesn't exist for a given topic.

## Index

| Date | Type | Milestone | File |
|---|---|---|---|
| — | — | — | — |

Two kinds of audits belong here, both under the same naming scheme:

- **Periodic professionalism audits** — every N topics (`MISSION.md`'s audit cadence, default
  10), before starting the next topic. Purpose: catch the kind of drift that accumulates quietly
  across many sessions (inconsistent naming, stale placeholder text, factual errors in
  notebooks, missing repo hygiene files) before the record is shown to anyone.
- **One-time named audits** — cover something other than a topic milestone: a public-readiness
  audit, triggered by the repo's visibility changing; an organization pass, triggered by a direct
  request to check overall consistency; or a final sign-off audit, before pointing the repo to
  anyone or forking it further. Same filename convention, same rules below.

## Rules for every audit

- **Not limited to the categories/items a past audit already found.** Each new audit looks at the
  repo fresh, word by word, and adds whatever new issues actually turn up — an audit means
  checking everything, not re-verifying a predefined list.
- Findings first, fixes only after the learner reviews them — never apply silently.
- Categorize by severity (critical / important / minor / cosmetic) so priority is clear at a
  glance.
- Fix in small, reviewable, individually-committed batches, not one giant commit.
- **Periodic and final sign-off audits only**: defer genuinely topic-specific best-practice items
  to when that topic is actually taught, rather than fixing them retroactively — the point is
  learning them hands-on, not finding a pre-made fix waiting. Flag the item clearly so the next
  session teaching that topic knows it's already diagnosed. Public-readiness and organization
  audits have no topic-teaching timeline to defer into, so this rule doesn't apply to them.
- Check-in/Check-out timestamps are never touched for formatting/consistency reasons — they're the
  one thing in the record whose value depends entirely on being real.
- **If the in-repo record redacts anything** (e.g. an identity placeholder `MISSION.md` defines),
  also save an unmodified copy of the raw, pre-redaction findings somewhere outside this repo —
  as-is, no redaction. If nothing needed redacting, skip this, but say so explicitly in the audit
  file so the absence reads as a decision, not an oversight.
- **Add the new file to the index table above** in the same commit — no audit is discoverable by
  filename alone under this naming scheme, so one that isn't indexed is effectively invisible.
- **Once something is genuinely settled — an ownership question, a design decision revisited and
  closed — record the resolution durably in a committed file, not only in session memory.**
  Memory doesn't carry across a fresh session or a different AI account; a committed resolution
  does. An unresolved-looking finding that was actually settled weeks ago, just never written
  down, is exactly the kind of thing that gets re-litigated forever otherwise.
