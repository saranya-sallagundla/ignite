# Repo audits

Audit findings are filed by **subject**, not by the audit that found them — four files, one per
kind of problem. Each finding's ID says which audit found it, and every audit adds to these four
files instead of creating new ones. Create each file the first time an audit has a finding for it.

## Where findings live

| File | Holds |
|---|---|
| `privacy-and-publishing.md` | Is it safe to make public — identity in files and history, secrets, licences, the right to publish |
| `accuracy-and-currency.md` | Is what's written true and up to date — technical claims, stale facts, the living reference, pacing numbers |
| `consistency-and-structure.md` | Does it read as one system — naming, formats, layout, rendering, links, hygiene files, process rules |
| `project-and-engine.md` | Are the outward-facing products ready — the parallel project, anything meant to be reused, root presentation, CI |

Each file opens with a short "How findings are recorded here" section, then its findings, then a
*Verified clean — negative results* section. Every finding follows this shape:

```text
### <ID> — <short title>
> From: <audit name>, <date> · Original section: <section> · Severity: <tier> · Status: <status>

<the finding: what was found, why it matters, the fix>
```

- **ID** — a short prefix for the audit (e.g. `T10-` for the Topic 10 audit) plus the finding's
  own number.
- **Severity** — critical / important / minor / cosmetic. Left out when the audit didn't grade it.
- **Status** — `open`, `fixed <date>`, `held for Topic N`, `left as is on purpose`, `closed <date>`,
  `superseded`, or `not re-checked since`. When a later audit re-checks a finding, update its
  Status line rather than repeating the finding.

## Index

The source of truth for which audit covers which milestone — check it before assuming an audit
has or hasn't run for a given topic.

| Date | Type | Milestone | ID prefix |
|---|---|---|---|
| — | — | — | — |

Two kinds of audits:

- **Periodic professionalism audits** — every N topics (`MISSION.md`'s audit cadence, default
  10), before starting the next topic. Purpose: catch the kind of drift that accumulates quietly
  across many sessions (inconsistent naming, stale placeholder text, factual errors in
  notebooks, missing repo hygiene files) before the record is shown to anyone.
- **One-time named audits** — cover something other than a topic milestone: a public-readiness
  audit, triggered by the repo's visibility changing; an organization pass, triggered by a direct
  request to check overall consistency; or a final sign-off audit, before pointing the repo to
  anyone or forking it further. Same rules, same four files.

## How an audit is run

The process — findings before fixes, severity triage, batched commits, deferring topic-specific
items, indexing the result — lives in [`rules.md`](../rules.md) §8. It is not restated here, so
there is only ever one copy to keep true.

Two things worth repeating at the point of use:

- **Audit fresh, every time.** A past audit's findings record what that one audit surfaced. They
  are not a checklist a later audit is confined to re-checking.
- **Each audit also re-checks the standing rules** in `rules.md` §7, not only new issues.

### Saving a new audit

1. Pick a short ID prefix for it and add a row to the Index.
2. Add its header — date, trigger, scope, method, headline — to Audit history below.
3. File each finding in the matching subject file, in the shape above.
4. Update the Status line of any older finding the new audit re-checked, instead of repeating it.

## Audit history

<!-- One entry per audit: its header, headline, plan and follow-up notes. The findings themselves
     go in the four subject files. -->
