# Repo audits

One file: the index, what is still open, what is settled, each audit's record with its findings
one row each, and the prompts to start the next audit. Each finding keeps its ID, severity and
status. Never a new file per audit.

## Index

The source of truth for which audit covers which milestone — check it before assuming an audit
has or hasn't run for a given topic.

| Date | Type | Milestone | Prefix | Findings |
|---|---|---|---|---|
| — | — | — | — | — |

Two kinds of audit, same rules: **periodic** ones every N topics (`MISSION.md`'s audit cadence,
default 10) and once more after the last topic clears; **one-time** ones with a named trigger —
visibility changing, a direct request for an organization pass, or a final sign-off before the
record is pointed to publicly.

## Open items

| ID | Item | Status |
|---|---|---|
| — | — | — |

## Settled — do not re-raise

<!-- One bullet per closed question: the finding IDs, the date, and the decision in a sentence. -->

## <Audit type> — <YYYY-MM-DD> (`<PREFIX>-`)

<!-- One section per audit, newest last. Trigger, scope and result in a few lines, then: -->

| ID | Finding | Severity | Status |
|---|---|---|---|
| — | — | — | — |

<!-- End with one "Verified clean:" line listing what was checked and found fine. -->

- **ID** — the audit's prefix (e.g. `T10-` for the Topic 10 audit) plus the finding's own number.
- **Severity** — critical / important / minor / cosmetic, or the audit's own tier. `—` when the
  audit didn't grade it.
- **Status** — `open`, `fixed <date>`, `held for Topic N`, `left as is on purpose`,
  `closed <date>`, `superseded`, or `not re-checked since`. When a later audit re-checks a
  finding, update its Status cell rather than repeating the finding.

## Running the next audit

The process — findings before fixes, severity triage, batched commits, deferring topic-specific
items, indexing the result — lives in [`rules.md`](rules.md) §8. It is not restated here, so
there is only ever one copy to keep true.

Two things worth repeating at the point of use:

- **Audit fresh, every time.** The tables above record what each audit surfaced. They are not a
  checklist a later audit is confined to re-checking.
- **Each audit also re-checks the standing rules** in `rules.md` §7, not only new issues.

### Saving a new audit

1. Pick a short ID prefix and add a row to the Index.
2. Add its section above: trigger, scope and result in a few lines, then a findings table, one
   row per finding.
3. Update the Status of any older finding the new audit re-checked instead of repeating it, and
   move items between Open items and Settled as needed.

### Prompts

<!-- Paste each kind of audit's starting prompt here, to be reused verbatim next time. -->
