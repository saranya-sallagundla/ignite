# Repo audits

Audit findings are filed by **subject**, not by the audit that found them — four files, one per
kind of problem. Each finding's ID says which audit found it, and future audits add to these four
files instead of creating new ones. (Naming history, so older references make sense:
`topic-N-audit.md` originally; dated `audit-YYYY-MM-DD.md` from commit `1fb1677` in August 2026;
one descriptively named file per audit from 2026-09-21; filed by subject since 2026-09-25. The
original per-audit files are in git history, word for word.)

## Where findings live

| File | Holds |
|---|---|
| [`privacy-and-publishing.md`](privacy-and-publishing.md) | Is it safe to make public — identity in files and history, the public mirror, secrets, licences, the right to publish |
| [`accuracy-and-currency.md`](accuracy-and-currency.md) | Is what's written true and up to date — technical claims, stale facts, the field atlas, pacing numbers |
| [`consistency-and-structure.md`](consistency-and-structure.md) | Does it read as one system — naming, formats, layout, rendering, links, hygiene files, process rules |
| [`project-and-engine.md`](project-and-engine.md) | Are the outward-facing products ready — `orbit/`, `engine/`, the root presentation, CI |

Each file opens with the shape its findings follow, so a new audit files them the same way.

## Index

The source of truth for which audit covers which milestone — check it before assuming an audit
has or hasn't run for a given topic.

| Date | Type | Milestone | ID prefix | Original file (in git history) |
|---|---|---|---|---|
| 2026-07-27 | Periodic professionalism audit | after Topic 10 | `T10-` | `topic-10-professionalism.md` |
| 2026-08-13 | Public-readiness audit (one-time) | repo already public, pre-remediation | `PR-` | `public-readiness.md` |
| 2026-08-26 | Repo organization audit (one-time) | not tied to a topic milestone | `RO-` | `repo-organization.md` |
| 2026-08-31 | Final sign-off audit (one-time) | not tied to a topic milestone — pre-fork/public-facing review | `FS-` | `final-sign-off.md` |

When a finding's text names one of the original files, read it as that file's prefix —
`public-readiness.md`'s C-7 is `PR-C-7`.

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
  every git remote, not just the one currently being worked from). Same rules, same four files,
  just not tied to the every-10-topics cadence.

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
> material (`rules.md`/`CLAUDE.md`/`MISSION.md`/`engine/` and anything a fork would rely on) — and check it
> for accuracy, internal consistency, and whether it's usable by someone with no prior context.
> Verify the live state of every git remote, not just the one currently being worked from —
> a clean local/private copy doesn't mean the actual public destination is clean. Check
> `field_atlas.md` (or the mission's equivalent living reference, if it has one) for currency, and
> propose a concrete, repeatable mechanism for keeping it current going forward, not just a note
> that it could drift. Save findings to `audits/`, and don't apply any fixes until I review them.

## How an audit is run

The process — findings before fixes, severity triage, batched commits, deferring topic-specific
items, indexing the result — lives in [`rules.md`](../rules.md) §8. It is not restated here.

Two things worth repeating at the point of use, because both have been gotten wrong before:

- **Audit fresh, every time.** `topic-10-professionalism.md`'s findings (A-E, and its batch
  structure) record what that one audit surfaced. They are not a checklist a later audit is
  confined to re-checking. Look at the repo word by word and add whatever actually turns up.
- **Each audit also re-checks the standing rules** in `rules.md` §7, not only new issues.

### Saving a new audit

1. Pick a short ID prefix for it (e.g. `T20-` for the Topic 20 audit) and add a row to the Index.
2. Add its header — date, trigger, scope, method, headline — to Audit history below.
3. File each finding in the matching category file, in that file's shape.
4. Update the Status line of any older finding the new audit re-checked, instead of repeating it.

## Audit history

Each audit's own header, headline, plan and follow-up notes, word for word. The findings
themselves are in the four category files above.

### Repo Audit — after Topic 10 (before Topic 11) (`T10-`)

**Date**: 2026-07-27 · **Scope**: every file in the repo (root files, all `learning/` files, all
10 notebooks, all `orbit/` files, git history/hygiene) · **Method**: a 17-agent audit (12
parallel workflow auditors covering different files/dimensions + 5 dedicated notebook auditors,
since the first pass of notebook auditors stalled on the larger files and had to be re-run in
smaller batches — worth remembering for the next audit: split large-file auditors into 2-file
batches, not 4-file, to avoid agent stalls).

> **Title vs. date, explained.** "before Topic 11" describes this audit's *scope* — it covers the
> repo as it stood once Topic 10 cleared, before Topic 11's work began — not a calendar claim.
> This audit's own date (07-27) falls after Topic 11's session-log date (07-24) because both were
> authored during the same catch-up period; see the pacing gap `public-readiness.md`'s finding
> C-7 documents. Neither date has been altered to make the two agree.

**Overall result going in**: fundamentally strong — clean linear git history, no secrets ever
committed, one consistent author identity, scores/session counts consistent across files, no
employer name in 28 of 29 files. What surfaced was real, though: 4 critical items, ~30 important,
and a long tail of minor/cosmetic consistency issues. All were reviewed with the user before any
fix was applied, then fixed in 8 separate, reviewable, individually-committed batches.


### Public-Readiness Audit — 2026-08-13 (`PR-`)

**Scope**: all 41 tracked files, all 60 commits on all refs, git internals, live remote state
**Method**: 4 parallel scanners (sensitive-data sweep · open-source readiness · conventions &
consistency · container & supply chain) plus direct verification of every critical claim
**Status**: **FINDINGS ONLY — no fixes applied.** Per `audits/README.md`, nothing is changed until
the findings are reviewed.

> **Redaction note.** This record deliberately does not reproduce the strings it discusses, name the
> employer, or give the commit identifiers where historical instances live. Naming them here would
> re-leak them and hand a reader a recovery path — the exact mistake
> `audits/README.md`'s rules warn against. An unredacted verbatim copy is held outside this repo per
> the standing rule; its location is intentionally not recorded in a committed file.

#### Headline

Different in kind from the Topic 10 audit. That one was about polish. This one is about **identity
hygiene**, and it is triggered by a change of context: this repo is no longer private.

**There are no secrets and no credentials anywhere** — not in the working tree, not in 60 commits of
history. That was verified exhaustively and is genuinely clean.

Every blocking problem is identity, not quality. The most important one:

> The employer-name redaction was applied to the **working tree** but never to **git history**.
> The current tree is clean. **16 commits are not.** And `audits/topic-10-professionalism.md` then documents
> that the leak existed and names the file it was in — which is a recovery path for any reader.

**Two findings are irreversible after the first fork.** There are currently 0 forks and 0 stars, so
remediation is free today and expensive later.

An audit that lists only faults misleads. These were checked exhaustively and are genuinely clean.

#### Remediation sequence

**Gate 0 — before anything else**
1. **B-1**: written employer approval. Nothing else is worth doing until answered.
2. Consider taking the repo **private** while remediating — free at 0 stars / 0 forks.
3. **C-7**: recalibrate the Pacing Layer. Needed for the demo regardless of everything else.

**Gate 1 — irreversible-after-first-fork, all in one pass**
4. Scrub the tree: H-1 user ID, H-2 legal name, H-3 network specifics, H-4 concept paragraph, H-5 delete `claude-memory/`, the M-tier disclosure items, and the job-hunting-relevant "onsite interviews" line in `topic-10-professionalism.md`'s Batch 3.
5. **One** history rewrite covering the corporate email, the org name, and the user ID, plus an identity rewrite of all 60 commits to a personal name and a no-reply address. Verify both strings return empty across all refs afterwards.
6. Set repo-local identity; enable the block-email-exposing-pushes setting; start signing commits.
7. Publish as a **fresh, unforked** repo under the personal account — never by flipping visibility on the org-hosted copy.
8. Amend `CLAUDE.md:136-137`: the metadata exemption is now wrong. Add H-7's `.gitignore` patterns before Phase 3.

**Gate 2 — blocks the next three topics**
9. H-8 numeric UID. Loopback port bind.

**Gate 3 — presentation, once identity is clean**
10. H-6 licences · H-9 README rewrite · H-10 provenance and score relabelling · H-12 captured-output integrity · H-14 the one-line fence fix · H-13 topic names · H-15/16/17/18/19 `orbit/` accuracy · community files · Linguist attributes · the three infrastructure workflows · topics and description.

**Gate 4 — hands-on remediation, not handed-over code**
11. The Compose hardening, ownership, base pinning, gunicorn flags, versioning and first test are **all Topic 11 material, and Topic 11 cleared at 90/100.** Handing over finished code wastes that. Run them as a short hands-on session: inspect the implicit UID, drop all capabilities and confirm nothing breaks, load-test a single sync worker to feel head-of-line blocking. That is exactly how the Session 17 image-size bug was handled — found, measured, fixed with proof — and it remains the strongest engineering story in this repo.


### Repo Organization Audit — 2026-08-26 (`RO-`)

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

#### Headline

97 findings across five slices: 3 critical, 20 important, 40 minor, 34 cosmetic. Three were
genuine, verifiable defects, not style opinions — one of them (the LICENSE) was independently
confirmed via the GitHub API before being touched. All three critical findings, all 20 important
findings, and the great majority of the minor/cosmetic ones were fixed; a small number were
deliberately left alone after closer reading showed the "fix" would have done real damage. Those
are listed explicitly at the end — an audit that hides its own skipped items isn't trustworthy.

#### What was deliberately left unfixed (summary)

- `docker-compose.yml`'s `container_name: orbit-app` — real risk to already-captured commands.
- British vs. American spelling across public docs — the user's call, not made yet.
- The right-to-publish question (`public-readiness.md`'s B-1) — unaffected by any wording fix.
- Reordering 5 notebooks' preamble-before-agenda — would lose context in 2 of 5 cases.
- Retrofitting Phase 2 notebooks with a label or section they never had.
- Rewriting any notebook's historical commands, output, or prompts to match a new house style.

#### Fix commits

`3a62cee` (batch 1) · `3e97a01` (batch 2) · `08f252f` (batch 3) · `a31ecff` (batch 4) ·
`36636d4` (batch 5) — all reviewed with the user and pushed to `origin/main` before this record
was written.


### Final Sign-Off Audit — 2026-08-31 (`FS-`)

**Trigger**: not a periodic (every-10-topics) audit and not tied to a topic milestone — a
requested final-sign-off review, in the voice of a senior reviewer deciding whether this repo is
ready to be pointed to publicly and forked by strangers. Broadest scope of any audit run so far:
every root file, every subfolder, every notebook, the pre-build/`engine/` material, and a live
cross-check of both GitHub remotes — not just the working tree.

**Scope**: every file in the repo, word by word — root hygiene files, `CLAUDE.md`, `learning/`
(including all 11 notebooks), `orbit/`, `engine/`, `docs/`, `audits/` (including its own three
prior audits, checked against each other and against the live repo), `.github/`, plus git
history/hygiene and the live state of both `origin` (private) and `personal` (public) GitHub
remotes.

**Method**: direct review (root files, `CLAUDE.md`, `learning/roadmap.md`, `progress.md`,
`handbook_status.md`, `field_atlas.md`, `orbit/README.md`, `orbit/docs/concept.md`,
`engine/CLAUDE.template.md`, prior audit files, `.gitignore`/`.gitattributes`) plus 11 parallel
deep-review agents (one per notebook pair, one simulating a first-time fork of `engine/`, one for
`docs/`, one for `orbit/`, one cross-checking the three prior `audits/` files against each other
and the live repo, one fact-checking `field_atlas.md` against live web research) plus a direct
git/GitHub-level sweep: full history secret scan, employer-name sweep (working tree and full
history on every ref), `gh api` visibility checks on both remotes, and ancestry/diff comparison
between `origin/main`, `personal/main`, and the local `main` actually reviewed.

**Status**: **FINDINGS ONLY — no fixes applied.** Per `audits/README.md`, nothing changes until
these are reviewed.

**On redaction**: like `public-readiness.md`, this file discusses an identity exposure without
naming the employer or reproducing the leaked strings — describing them abstractly instead.
Unlike that file, nothing here required generating an unredacted version to begin with (this
audit never wrote the literal strings down anywhere, including in scratch output kept outside
this repo), so there is no separate raw, pre-redaction copy to preserve — per `audits/README.md`'s
own rule, that's stated explicitly here rather than left to look like an oversight.

#### Headline

Two different kinds of "not ready yet" are tangled together in this repo right now, and they
need to be pulled apart before anything else:

1. **What's sitting in the private, actively-maintained copy** (`origin`, this file included) is
   in genuinely good shape — well-argued, mostly self-consistent, and the product of two prior
   audits that each found and fixed real things. Most of what follows below is refinement, not
   rescue.
2. **What's actually live on the public internet right now** (`personal` — `github.com/
   saranya-sallagundla/ignite`, confirmed public) is a **different, older, worse snapshot** that
   predates almost all of that refinement, and it currently exposes the real name and corporate
   email address of the repo's author across dozens of commits, plus a folder of AI-memory notes
   about the author that the private copy has since removed entirely. This was already found and
   fully diagnosed by this repo's own `public-readiness.md` a month ago. **The fix it prescribed
   was applied to the private copy only. The public copy was never touched.**

Sign-off cannot mean "the private copy looks good." The public copy is the actual product being
signed off on, and right now it is a materially different, unremediated repo. That is this
audit's single most important finding, expanded in Critical Finding 1 below.

Grouped by area. Each is independently verified — either by this audit directly or by a dedicated
review agent whose specific claim I checked before including it here.

Grouped by theme rather than listed individually — each recurs across several files rather than
being a one-off.

#### Prior-audit status check

A audit that only lists new findings misleads about what's actually been fixed. Checked
specifically:

- **All 8 items `topic-10-professionalism.md` deferred to Topic 11 are genuinely resolved** — verified
  directly against the live `orbit/app/Dockerfile`, `requirements.txt`, and
  `orbit/docker-compose.yml`: non-root `USER`, gunicorn, `EXPOSE`, `HEALTHCHECK`,
  `--no-cache-dir`, `PYTHONUNBUFFERED=1`, tagged image, Flask patch bump. Matches the Topic 11
  notebook word for word.
- **`public-readiness.md`'s H-6 (licensing), H-9 (README rewrite), H-14 (the stray fence),
  community-files gap, and most of its M-tier presentation items are resolved** — verified: LICENSE
  is byte-identical MIT, `learning/LICENSE` is CC BY 4.0, `README.md` now states scores are
  "self-assessed and AI-graded... not externally validated," `CONTRIBUTING.md`/`SECURITY.md` now
  exist, and all 11 notebooks have even code-fence counts.
- **Still open, unchanged since 2026-08-13**: B-1 (Critical Finding 2), the public-mirror exposure
  itself (Critical Finding 1 — this audit found the fix never reached its actual target), the
  git-metadata exemption (Critical Finding 5), and H-8's non-numeric Dockerfile `USER` (still
  `useradd --create-home appuser` / `USER appuser`, no explicit UID — the audit's own warning that
  this "hard-blocks Kubernetes at Topic 12" with `CreateContainerConfigError` stands unchanged, and
  Topic 12 is the very next topic on the roadmap). Per this repo's own defer-to-topic philosophy,
  this shouldn't be silently pre-fixed — but it should be taught knowing it's already diagnosed,
  not discovered mid-session as a surprise.
- **`repo-organization.md`'s own five batches hold up well on inspection** — the LICENSE-detection
  fix, the `orbit/` reconciliation between `README.md` and `docs/concept.md`, and the
  `learning/` tracking-hygiene fixes were all independently re-verified against the live files
  during this audit and found accurate. Its self-consistency gaps are listed under Important
  above.

#### Recommended sequence (not applied — for your review)

**Gate 0 — before anything else**
1. ~~Answer B-1 directly (Critical Finding 2)~~ — **cleared 2026-08-31**, see the resolution note
   above. Gate 1 is unblocked.

**Gate 1 — the live exposure**
2. Set repo-local commit identity to a personal name/no-reply address; remove the git-metadata
   exemption from `CLAUDE.md` and `engine/CLAUDE.template.md` (Critical Finding 5).
3. Force-push the already-clean local `main` lineage to `personal`, replacing its history
   entirely (Critical Finding 1) — this single action resolves the exposed identity, drops the
   stray `claude-memory/` folder, and brings the public copy current with a month of hygiene work
   in one pass. This is a destructive, irreversible action on a live public repository and should
   only happen with your explicit go-ahead, separate from this report.

**Gate 2 — the fork-usability blockers**
4. Add a license grant for `engine/` (Critical Finding 3).
5. Add the remote-setup step to `QUICKSTART.md` (Critical Finding 4).

**Gate 3 — process integrity**
6. Fix `CLAUDE.md`'s audit-trigger phrasing and Repo-layout section (Important).
7. Reconcile the four `audits/` self-consistency issues (Important).

**Gate 4 — everything else in Important/Minor/Cosmetic** — batched and reviewed the normal way,
in small, individually-committed groups, per this repo's standing rule.

**Deliberately not included here**: the Dockerfile's non-numeric `USER` — per this repo's own
defer-to-topic philosophy, that's Topic 12 hands-on material, not a pre-fix. Flagged above so it's
taught knowing it's already diagnosed.

#### Resolved since this report was first written

Critical Finding 2 (B-1) was answered directly on 2026-08-31: this is a self-created personal
learning project, not employer work, so no written employer confirmation is needed. See the
resolution note under Critical Finding 2 above — that note, not this section, is the durable
record for any future audit.
