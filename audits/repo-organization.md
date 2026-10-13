# Repo Organization Audit — 2026-08-26

**Date**: 2026-08-26 · **Scope**: every file in the repo (root files, all `learning/` files, all
11 notebooks, all `orbit/` files, `engine/`, `docs/`, `audits/`, git history/hygiene) ·
**Method**: 5 parallel auditors, each covering one slice (root + governance; `learning/`
tracking files; the 11 study notebooks; `orbit/`; `engine/` + `docs/` + `audits/`), plus a
direct git-level sweep (status, log, remotes, line endings, trailing whitespace, TODO/FIXME
markers) covering the one slice no file-content auditor reaches. **Status**: fixes already
applied, in five reviewable batches, one per slice — this record is written up after the fact
rather than findings-first, since the user asked for the audit and the fix batches without a
findings-review pause between them. *(Corrected 2026-08-31: batches 1–4 committed 2026-08-20,
batch 5 committed 2026-08-26 — two sessions six days apart, not the one continuous session this
line originally claimed.)*

> **Trigger.** Not a periodic (every-10-topics) or public-readiness audit — the user asked for a
> whole-repo pass "as if you have OCD and want everything organized," independent of any topic
> milestone. Recorded here anyway, per `audits/README.md`'s own rule that every audit gets saved
> and indexed, so this pass doesn't become invisible to a future session.

> **On redaction.** Unlike `public-readiness.md`, nothing found here touches identity, security,
> or anything else warranting redaction — this was an organization and consistency pass, not a
> disclosure sweep. No unredacted external copy was made; this file is the complete record.

## Headline

97 findings across five slices: 3 critical, 20 important, 40 minor, 34 cosmetic. Three were
genuine, verifiable defects, not style opinions — one of them (the LICENSE) was independently
confirmed via the GitHub API before being touched. All three critical findings, all 20 important
findings, and the great majority of the minor/cosmetic ones were fixed; a small number were
deliberately left alone after closer reading showed the "fix" would have done real damage. Those
are listed explicitly at the end — an audit that hides its own skipped items isn't trustworthy.

## Batch 1 — the three criticals, plus leftovers from the audits/ rename

**`topic-08-github-prs-actions-intro-repo-management.md:69`** *(renamed 2026-08-31; was
`topic-08-github.md` at the time)* — a stray opening code fence left the file with an odd fence
count.
Verified: fence parity broken from that point to EOF, and the `### 3. GitHub Actions` heading
was being swallowed entirely by GitHub's renderer as a result. One-line deletion; verified after
the fix that all 11 notebooks now have even fence counts and every heading in the file renders
outside a code block.

**`learning/progress.md`'s Current status "line"** had grown into a 6-line roster of all 11
completed topics with scores — a direct violation of `CLAUDE.md`'s own rule ("one line,
overwritten every session — not appended to") and a second scoreboard duplicating
`handbook_status.md`. Collapsed to one line; verified afterward that no data was lost (all 11
scores still in `handbook_status.md`, all 11 rows still in the quiz record index, Phase 1
completion still recorded in `roadmap.md`).

**`orbit/README.md`'s Session 16 entry** claimed Compose was "extended with a second service and
a named volume," which the committed `docker-compose.yml` contradicts (one service, no volumes).
Before rewriting a historical log entry, checked git history: the claim was **true when written**
— a second service and volume genuinely existed at Topic 10 completion (`c44bdf7`) and were
removed later by the Topic 10 audit's own cleanup commit (`3fd8fa2`). Fixed by adding a removal
note, not by rewriting an accurate historical record.

**Leftovers from the previous session's `audits/` rename** (`1fb1677`), found only because this
audit re-checked that work rather than assuming it was complete:
- `engine/CLAUDE.template.md` still taught forks the abandoned `topic-N-audit.md` naming in two
  places, and its audit-trigger logic still carried the exact latent bug `public-readiness.md`
  documents (a multiple-of-10 topic clearing after its successor never fires the reminder).
  Fixed to `audit-YYYY-MM-DD.md` plus the index-lookup rule, and the trigger now keys off
  "highest cleared topic ≥ next un-audited multiple" instead of guessing a filename.
- Two line-number citations inside `public-readiness.md` had rotted when the new index table
  shifted the file they pointed at. De-lined to rule names so they can't rot again.

## Batch 2 — orbit/, the showcase folder

**The real defect**: `CLAUDE.md` explicitly bans internal-scaffolding language from `orbit/`
("no internal-scaffolding language... references to this file"), yet the folder guide's first
bullet and `orbit/app/README.md` both told reviewers the code was "not yet something to defend in
an interview." Removed from both.

**Accuracy fixes**: `argocd/` existed with its own README but was missing from the folder guide;
"every folder is an empty placeholder" was false for `docs/` (holds `concept.md`); the README
promised Kubernetes on Terraform-provisioned AWS while `docs/concept.md` specifies local k3s +
LocalStack — reconciled so the two showcase docs agree; 17 topic names (not the ~12 the prior
audit estimated) were in non-baseline spelling — recounted and fixed.

**Structure**: the build log had grown to 17 entries, 12 of them "no project code yet,"
oldest-first — burying the actual Docker work under Linux filler in a showcase README. Collapsed
Sessions 1-12 to one Phase 1 line; moved the log under its own heading. README: 130 → 77 lines.

**Deliberately not fixed**: `container_name: orbit-app` in `docker-compose.yml` — dropping it
would rename the running container to `orbit-app-1` on next `up`, which could invalidate `docker
exec` commands already captured in the notebooks. Left in place.

## Batch 3 — root and governance

**The real defect, verified externally**: queried the GitHub API before touching anything —
the repo's license was being detected as `"Other" / NOASSERTION`, not MIT. The scope paragraph
inserted before the MIT body and the note appended after it had broken GitHub's license
detection. `LICENSE` is now byte-identical to canonical MIT (checked programmatically); the scope
split and the "not production-hardened" note moved to README's License section.

**A real gap, not just a defect**: the root prose files (`README.md`, `CONTRIBUTING.md`,
`SECURITY.md`, `CLAUDE.md`) fell under **neither** license grant — not `learning/`, `docs/`, or
`audits/`, so not CC BY; not plausibly "scripts or configuration," so not MIT. Both license files
and the README now place root prose under CC BY 4.0.

**Claims that didn't match the repo**: the README's tree annotated `.github/` with "CI workflows,
issue forms, dependency policy" — none of the three existed. `.github/workflows/README.md`
described checks in the present tense over an empty folder. `SECURITY.md`'s scope table listed
`.github/` workflows as in-scope with none present. All three reworded to match reality, and
`.github/ISSUE_TEMPLATE/.gitkeep` was removed — GitHub parses `.md` files in that folder as
selectable issue-template choices, so it can't carry a placeholder README like the repo's other
reserved folders the way `.gitkeep` implied it eventually would.

**Consistency**: one name for "the 3-attempt mastery rule" everywhere; numerals for recurring
quantities; `.gitattributes` declares `*.md`, the repo's dominant type; two over-long lines this
same audit had introduced in `CLAUDE.md` during batch 1 were rewrapped.

**Deliberately not resolved**: the British/American spelling split across public docs, and the
`docs/concept.md` reword — both flagged as wording-only; neither touches the open right-to-publish
question (`public-readiness.md`'s B-1, still the actual blocking item).

## Batch 4 — learning/ tracking hygiene

**A real arithmetic error**: `roadmap.md` flagged 2026-07-17 as the pacing layer's one "gap day"
(a session's past-midnight spillover with no new session starting that day) but didn't apply the
identical rule to 2026-07-15 or 2026-07-25, which have the same pattern. Verified against every
session's actual check-in/check-out timestamp in `progress.md`. Corrected to one explicit rule
and the honest count: **17 of 20 active days**, three gaps named, not "19 of 20 (1 gap)."

**A sequencing question, resolved by checking git history rather than guessing**: Session 17
(narratively dated 2026-07-24) credits work to the Topic 10 audit, which is dated 2026-07-27 —
three days later, despite its own title claiming to precede Topic 11. Traced the real commit
history: both were authored during the same later catch-up period already disclosed as
`public-readiness.md`'s C-7 finding. Neither date was altered — a short header note (a 5-line
blockquote, not literally one line) was added to the audit's own header explaining that "before
Topic 11" describes scope, not calendar order.

**Structure**: the three summary tables (quiz index, deferred mastery, light days) moved ahead of
the session log, so a session-start read hits them before 300+ lines of history; `field_atlas.md`
had four H1s, corrected to one; a mislabeled "Current topic" field describing a *finished* topic
renamed to "Topic state"; the SSH-deferral note, previously duplicated in two files, now lives
only where `CLAUDE.md` says pacing deferrals belong.

**Rules corrected to match a year of real practice**: `handbook_status.md`'s "compact one-line
reason" was never one line in 11 of 11 entries (up to ~570 characters); `session_notes.md`'s
"2-4 line recap" was exceeded in 16 of 17 entries with genuinely valuable reflection. Rewriting
either rule's *practice* to match its stale *text* would have meant deleting real, useful, honest
content. Reworded both rules instead — in `CLAUDE.md`, the live files, and the engine template's
two mirrored copies, so nothing drifts apart again.

## Batch 5 — the 11 notebooks

Checked every suggested fix against the notebooks' own recorded dates before applying anything;
two didn't survive that check and were dropped (below).

**Byte-format fixes** (the mandated `**Verdict**: **Topic N CLEARED, attempt N, XX/100.**`):
`topic-03`'s "in 2 attempts" → "attempt 2." `topic-05`'s "official score" was **kept**, not
forced into "attempt N" — Topic 5 passed attempt 1 and was voluntarily revised, never failed
under the 3-attempt rule, so "attempt N" would misrepresent what actually happened; only the
missing closing period was fixed. `topic-07`/`topic-08` day headings converted from a second
em-dash to the parenthetical form the other 9 notebooks use. `topic-10`'s Day 2 sections
continued Day 1's numbering (5-9) instead of restarting at 1, unlike every other multi-day
notebook; renumbered to 1-5 (no cross-references existed to break).

**Mechanical**: `topic-09` was missing a blank line after all 21 of its headings, the one
notebook that didn't already do this. Fixed — diff is 21 pure insertions, content otherwise
unchanged, fence parity reverified.

**Intro-blockquote consistency, checked against real Day-heading dates rather than the roadmap's
allocated day count**: caught myself here — Topics 5 and 6 both allocate 2 days in the roadmap,
but their actual Day 1/Day 2 headings share one calendar date each, meaning both were really
one-session topics. Wrote each an honest note explaining the compression instead of the generic
"two sessions" line the other multi-day topics correctly get.

**Deliberately not fixed**: reordering the 5 notebooks that put a preamble before "Today's
agenda" — two of the five have preambles that directly explain the unusual heading right above
them, so moving them would have severed context from what it explains, for a cosmetic-tier gain.
The "Verified hands-on" label missing from Phase 2, and `topic-09`'s unique wrap-up section —
both would mean inserting content into historical notebooks that wasn't there when written.
Command-prompt style and output notation, split three ways across the phases — per the user's
explicit decision, recorded as forward-only conventions (Topic 12+) in `CLAUDE.md` and the engine
template, with **zero retroactive changes** to captured historical terminal sessions.
Retroactively "fixing" a real captured session to look consistent is exactly the integrity
problem `public-readiness.md`'s C-6/H-12 findings warned about.

## What was deliberately left unfixed (summary)

- `docker-compose.yml`'s `container_name: orbit-app` — real risk to already-captured commands.
- British vs. American spelling across public docs — the user's call, not made yet.
- The right-to-publish question (`public-readiness.md`'s B-1) — unaffected by any wording fix.
- Reordering 5 notebooks' preamble-before-agenda — would lose context in 2 of 5 cases.
- Retrofitting Phase 2 notebooks with a label or section they never had.
- Rewriting any notebook's historical commands, output, or prompts to match a new house style.

## Fix commits

`3a62cee` (batch 1) · `3e97a01` (batch 2) · `08f252f` (batch 3) · `a31ecff` (batch 4) ·
`36636d4` (batch 5) — all reviewed with the user and pushed to `origin/main` before this record
was written.
