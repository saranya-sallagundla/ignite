# Consistency and structure

Does it read as one system? Naming, formats, file layout, rendering, links, hygiene files, and the repo's own process rules.

## How findings are recorded here

Every audit adds its findings to the one of the four audit files that matches the subject — never
a new file per audit. Each finding follows this shape:

```text
### <ID> — <short title>
> From: <audit name>, <date> · Original section: <section> · Severity: <tier> · Status: <status>

<the finding: what was found, why it matters, the fix>
```

- **ID** — the audit's prefix plus the finding's own number: `T10-` Topic 10 audit, `PR-`
  public-readiness, `RO-` repo organization, `FS-` final sign-off. A new audit picks a new prefix
  and adds it to the index in [`README.md`](README.md).
- **Severity** — critical / important / minor / cosmetic, or the audit's own tier name. Left out
  when the audit didn't grade the item.
- **Status** — `open`, `fixed <date>`, `held for Topic N`, `left as is on purpose`, `closed <date>`,
  `superseded`, or `not re-checked since`. When a later audit re-checks a finding, update its
  Status line here rather than repeating the finding.
- **Verified clean** results — things checked and found fine — go in the last section, under the
  audit that checked them.
- Findings moved here from the original per-audit files are word for word. Where their text names
  an original file, read it as its prefix: `public-readiness.md` → `PR-`, `final-sign-off.md` →
  `FS-`, `repo-organization.md` → `RO-`, `topic-10-professionalism.md` → `T10-`.

## Findings

### T10-1.4 — Unescaped backtick broke Topic 7 rendering
> From: Topic 10 professionalism audit, 2026-07-27 · Original section: Batch 1 — Critical (4 items) · Severity: critical · Status: fixed 2026-07-27

4. **Topic 7 notebook had an unescaped backtick that broke Markdown rendering on GitHub**. *Why it
   matters*: broken rendering is immediately, visibly wrong to anyone opening the file — no reading
   required to notice something's off.

### T10-2 — Repo hygiene files were missing
> From: Topic 10 professionalism audit, 2026-07-27 · Original section: Batch 2 — Repo hygiene · Status: fixed 2026-07-27

Added a root `.gitignore`, root `.gitattributes` (normalizes line endings to LF, fixing the
recurring CRLF warnings), and `orbit/app/.dockerignore`. Also fixed the root README's ASCII
repo tree (missing `docker-compose.yml`, a one-space misalignment).

*Why it matters*: a DevOps-focused repo with no `.gitignore`/`.dockerignore` reads as a missed
fundamental to exactly the kind of reviewer this project is meant to impress — these are the
first files a technically literate person checks for.

### T10-4 — Learning-file consistency
> From: Topic 10 professionalism audit, 2026-07-27 · Original section: Batch 4 — Learning-file consistency · Status: fixed 2026-07-27

Normalized topic names to one canonical form (the em-dash form from `roadmap.md`'s fixed
baseline) across `progress.md`, `roadmap.md`, `handbook_status.md`, and notebook titles — topic
names had drifted into commas, slashes, and colons in different places. Fixed a self-contradictory
technical claim about Docker's `:latest` tag, several casing/formatting inconsistencies in
`progress.md`, and softened `CLAUDE.md`'s 20-minute quiz cap wording so it no longer directly
contradicted the (correctly logged) real overruns.

*Why it matters*: a reviewer who cross-references two files and finds the same topic named three
different ways, or a stated rule contradicted by the very next log entry, reasonably wonders what
else doesn't line up — consistency is what makes the tracking system credible as a real record
rather than a loosely-maintained diary.

### T10-6 — Final cosmetic sweep
> From: Topic 10 professionalism audit, 2026-07-27 · Original section: Batch 6 — Final cosmetic sweep · Severity: cosmetic · Status: fixed 2026-07-27

Wording fixes in `session_notes.md` (terminology drift, a hyphenation error, unformatted inline
commands), a redundant word pair in `progress.md`, quiz-heading punctuation normalized across
notebooks, a missing separator and two mislabeled code fences in Topic 10, trailing newlines
added to `Dockerfile` and `app/README.md`.

*Why it matters*: individually trivial, but a repo covered in small inconsistencies reads as
careless in aggregate even when no single item matters much on its own.

### T10-8 — Date/time normalization
> From: Topic 10 professionalism audit, 2026-07-27 · Original section: Batch 8 — Date/time normalization · Status: fixed 2026-07-27

Standardized every session/Day heading across `progress.md`, `session_notes.md`,
`orbit/README.md`, and 8 notebooks to show only the day the session/day *started* (not a date
range) — some headings showed a range when a session crossed midnight IST, others didn't, with no
consistent rule for when. Spelled out an ambiguous date shorthand in the light-days log. Added a
one-line note explaining that raw command output and git commit metadata reflect the machine's
real local clock (US Eastern), not the IST convention used for narrative dates, so a reviewer
doesn't mistake that expected difference for an inconsistency.

**Explicitly verified**: every Check-in/Check-out timestamp, in every file, was left completely
untouched by this batch — confirmed via `git diff` showing zero lines added or removed on any
Check-in/Check-out line. *Why this matters*: those lines are the one part of this repo whose
entire value depends on being real, uninvented data — the pacing math, the "am I on track for 6
months" answer, all of it is computed from them.

### T10-9 — Day headings missing their content summaries
> From: Topic 10 professionalism audit, 2026-07-27 · Original section: Follow-up fix (post-audit, same day) · Status: fixed 2026-07-27

Topics 9 and 10 were missing the descriptive content-summary parenthetical that every other
notebook's Day heading carries (e.g. Topic 3 Day 2: `(loops, functions, exit codes — quiz
deferred on functions)`) — Topic 9/10's Day 2 just said `(final day)` with no content summary, and
Day 1 had nothing. Added matching summaries to all 4 headings, and fixed Topic 10's H1 title,
which was missed during the em-dash normalization pass. *Why it matters*: a reader scanning the
table of contents for a specific topic's Day 1 vs. Day 2 content relies on this summary to jump to
the right place without opening the file.

### PR-H-13 — Topic names in non-baseline spelling in `orbit/README.md`
> From: Public-readiness audit, 2026-08-13 · Original section: H — HIGH · **Presentation** · Severity: high · Status: fixed 2026-08-26 (RO-2.2)

- **H-13. `orbit/README.md` has 12 topic names in non-baseline spelling** (colon form or truncated), plus one instance inside `topic-10-professionalism.md` itself, in its own Batch 7 deferred-items list (`Docker: Multi-Stage Builds & Best Practices`) — the audit file has the exact bug it's flagging. `CLAUDE.md`'s Topic-names rule names `orbit/README.md` explicitly, and `topic-10-professionalism.md`'s Batch 4 claims this normalization was already done — it was applied to `learning/` (`progress.md`, `roadmap.md`, `handbook_status.md`, notebook titles) and missed `orbit/`. **Resolved 2026-08-26** — `repo-organization.md`'s Batch 2 recounted (17 instances, not the 12 estimated here) and fixed all of them; the line-range citation above was removed since `orbit/README.md` was also substantially rewritten in that pass (130 → 77 lines), which would have rotted it anyway.

### PR-H-14 — A stray code fence broke ~100 lines of rendering
> From: Public-readiness audit, 2026-08-13 · Original section: H — HIGH · **Presentation** · Severity: high · Status: fixed 2026-08-20 (RO-1.1)

- **H-14. `topic-08-github-prs-actions-intro-repo-management.md:69`** *(renamed 2026-08-31; was
  `topic-08-github.md` at the time this was written)* **— a stray code fence breaks ~100 lines of
  GitHub rendering.** Verified: the file has **21 fence lines (odd)**. Consequences cascade from `:70` through `:168` — a `**Syntax**` marker renders as literal code, `git log --graph` output collapses into prose, narrative renders as code, and the `### 3. GitHub Actions — intro` heading at `:151` is swallowed entirely. **One-line deletion, ~100-line blast radius — the single highest-value fix in the notebooks.**

### PR-M-7 — Consistency / arithmetic
> From: Public-readiness audit, 2026-08-13 · Original section: M — MEDIUM (grouped) · Severity: medium · Status: not re-checked since

**Consistency / arithmetic** — `roadmap.md:103-104`'s "1 gap day" is wrong under its own definition (there are three dates with no session start). "Roadmap days used: 19 of 120" mixes bases (numerator is core allocation, denominator includes the 22 buffer days tracked separately) and can never diverge from the baseline, so it is not a pace signal at all — the only real signal is never shown. Two buffer pools (5 reserve vs 22 overall) are never reconciled. `audits/topic-10-professionalism.md:3` is dated after the topic it claims to precede, caused by a latent bug: `CLAUDE.md:34` keys the reminder off *"the most recently cleared topic is a multiple of 10"*, and Topic 11 cleared one day after Topic 10 — rephrase as *"highest cleared topic ≥ the next unaudited multiple of 10."* That file also states an agent count that does not match its own breakdown. Verdict-line form deviates in 3 of 11 notebooks (8 are byte-exact); in one, the retest is never numbered, so how many of the 3 allowed attempts were consumed is unknowable. Syntax-before-example is honoured 108 times but ~50 commands slip through with wildly uneven density, `docker exec` (~12 uses) never gets one, one notebook gives a command's syntax then demonstrates a *different* command, and two put the syntax line *after* the example. `CLAUDE.md:141-143` requires a local-clock note "where it first appears" — there are **zero** such notes in any notebook. `progress.md:11-16`'s Current Status is a 6-line accumulating roster where `CLAUDE.md:60-62` specifies one overwritten line. `topic-11` celebrates 231MB → 204MB as proof multi-stage shrinks the image, but the single-stage image it replaced was 199MB and nothing reconciles the two figures. `orbit/data` is referenced as the bind-mount target for an entire lesson and does not exist; the `/` endpoint documented in topic-09 is not in `app.py`, so following the run instructions yields an unexplained 404. `README.md`'s repo tree omits three files created by the last audit.

### PR-L-1 — Low-severity items
> From: Public-readiness audit, 2026-08-13 · Original section: L — LOW · Severity: low · Status: not re-checked since

Local `C:\CloudOps\...` path disclosure across ~20 lines (cosmetic). Host disk size and virtual-disk
filesystem UUIDs in captured output. A deleted screenshot recoverable from history — **extracted and
visually inspected: benign**, no username, path, branding or credentials; flagged only because it
proves deleted binaries persist, and it is purged automatically by the history rewrite.
`.dockerignore` could add credential globs (genuinely low: the build context is 5 files and `.git` is
outside it). HEALTHCHECK could add `--start-period` (the real gap — startup failures currently count
toward retries), an explicit inner timeout, and an IPv4 literal; note **Kubernetes ignores Docker
HEALTHCHECK entirely**, which is exactly why separate `/health` and `/ready` endpoints is correct and
pays off at Topic 13. `app.py` lacks security headers (near-theatre for a two-endpoint JSON API with
no browser surface, but reviewers grep for it and `nosniff` is genuinely right), returns Flask's HTML
error pages from a JSON API, has no `/` route, and binds its dev server broadly in dead code — while
the identical bind in the Dockerfile is **correct and must stay**; being able to explain why the same
string is right in one place and wrong in the other is a good signal. **Rate limiting is correctly
absent** — health endpoints sit behind a load balancer and rate-limiting them would be actively
wrong. One notebook reproduces a vendor's full container welcome message unattributed, where the same
corpus handles this correctly elsewhere by quoting and italicising. Discoverability is unset: no
topics, no social preview, no tags — and the `claude-code` / `ai-assisted-learning` topic pair is the
**actual differentiator**, since the AI-taught methodology is the novel thing, not another DevOps
roadmap. `roadmap.md:3` cites an external spec a stranger cannot resolve. All 11 notebook H1s produce
a double-em-dash title — consistent across all 11, so resolve with one decision in `CLAUDE.md:145`
rather than eleven edits. Filename slugs truncate inconsistently. `CLAUDE.md:160` schedules no audit
after Topic 53, so there is no final pass before the repo is actually shown. `CLAUDE.md:167-168`
gives the raw-report path no naming convention, so a second audit silently overwrites the first —
**already relevant, since one such file already exists.** Zero relative links between notebooks
despite ~34 textual cross-references. Three files are CRLF locally while the other 37 are LF —
committed content is uniformly LF, so `.gitattributes` is working; local noise only.

### PR-R — Rule changes this audit recommended
> From: Public-readiness audit, 2026-08-13 · Original section: Rule changes this audit recommends · Status: items 2, 3, 4 and 6 done; item 5 no longer applies (no local audit copies); item 1 still open (FS-5)

Not findings, but standing rules that produced findings and will produce them again:

1. **`CLAUDE.md:136-137`** — remove the git-metadata exemption. It was correct for a private repo and is the largest exposure in a public one.
2. **`claude-memory/` sync rule** — delete it. It mandates copying files that contain the very string the zero-tolerance rule forbids.
3. **`CLAUDE.md:34`** — audit trigger must be "highest cleared topic ≥ next unaudited multiple of 10," not "most recently cleared is a multiple of 10."
4. **`CLAUDE.md:160`** — add a final pre-publication audit after Topic 53.
5. **`CLAUDE.md:167-168`** — give the raw-report file a dated naming convention so audits stop overwriting each other.
6. **New rule** — no captured command output is ever edited, including for a rename. Add a dated note instead. H-12 exists because this rule was missing.

### RO-1.1 — A stray code fence in the Topic 8 notebook
> From: Repo organization audit, 2026-08-26 · Original section: Batch 1 — the three criticals, plus leftovers from the audits/ rename · Status: fixed 2026-08-20

**`topic-08-github-prs-actions-intro-repo-management.md:69`** *(renamed 2026-08-31; was
`topic-08-github.md` at the time)* — a stray opening code fence left the file with an odd fence
count.
Verified: fence parity broken from that point to EOF, and the `### 3. GitHub Actions` heading
was being swallowed entirely by GitHub's renderer as a result. One-line deletion; verified after
the fix that all 11 notebooks now have even fence counts and every heading in the file renders
outside a code block.

### RO-1.2 — `progress.md`'s Current status had grown into a roster
> From: Repo organization audit, 2026-08-26 · Original section: Batch 1 — the three criticals, plus leftovers from the audits/ rename · Status: fixed 2026-08-20

**`learning/progress.md`'s Current status "line"** had grown into a 6-line roster of all 11
completed topics with scores — a direct violation of `CLAUDE.md`'s own rule ("one line,
overwritten every session — not appended to") and a second scoreboard duplicating
`handbook_status.md`. Collapsed to one line; verified afterward that no data was lost (all 11
scores still in `handbook_status.md`, all 11 rows still in the quiz record index, Phase 1
completion still recorded in `roadmap.md`).

### RO-1.4 — Leftovers from the `audits/` rename
> From: Repo organization audit, 2026-08-26 · Original section: Batch 1 — the three criticals, plus leftovers from the audits/ rename · Status: fixed 2026-08-20

**Leftovers from the previous session's `audits/` rename** (`1fb1677`), found only because this
audit re-checked that work rather than assuming it was complete:
- `engine/CLAUDE.template.md` still taught forks the abandoned `topic-N-audit.md` naming in two
  places, and its audit-trigger logic still carried the exact latent bug `public-readiness.md`
  documents (a multiple-of-10 topic clearing after its successor never fires the reminder).
  Fixed to `audit-YYYY-MM-DD.md` plus the index-lookup rule, and the trigger now keys off
  "highest cleared topic ≥ next un-audited multiple" instead of guessing a filename.
- Two line-number citations inside `public-readiness.md` had rotted when the new index table
  shifted the file they pointed at. De-lined to rule names so they can't rot again.

### RO-3.4 — Root and governance consistency
> From: Repo organization audit, 2026-08-26 · Original section: Batch 3 — root and governance · Status: fixed 2026-08-20

**Consistency**: one name for "the 3-attempt mastery rule" everywhere; numerals for recurring
quantities; `.gitattributes` declares `*.md`, the repo's dominant type; two over-long lines this
same audit had introduced in `CLAUDE.md` during batch 1 were rewrapped.

### RO-3.5 — Spelling split and `concept.md` reword left open
> From: Repo organization audit, 2026-08-26 · Original section: Batch 3 — root and governance · Status: left as is on purpose

**Deliberately not resolved**: the British/American spelling split across public docs, and the
`docs/concept.md` reword — both flagged as wording-only; neither touches the open right-to-publish
question (`public-readiness.md`'s B-1, still the actual blocking item).

### RO-4.3 — Tracking-file structure
> From: Repo organization audit, 2026-08-26 · Original section: Batch 4 — learning/ tracking hygiene · Status: fixed 2026-08-20

**Structure**: the three summary tables (quiz index, deferred mastery, light days) moved ahead of
the session log, so a session-start read hits them before 300+ lines of history; `field_atlas.md`
had four H1s, corrected to one; a mislabeled "Current topic" field describing a *finished* topic
renamed to "Topic state"; the SSH-deferral note, previously duplicated in two files, now lives
only where `CLAUDE.md` says pacing deferrals belong.

### RO-4.4 — Rules corrected to match real practice
> From: Repo organization audit, 2026-08-26 · Original section: Batch 4 — learning/ tracking hygiene · Status: fixed 2026-08-20

**Rules corrected to match a year of real practice**: `handbook_status.md`'s "compact one-line
reason" was never one line in 11 of 11 entries (up to ~570 characters); `session_notes.md`'s
"2-4 line recap" was exceeded in 16 of 17 entries with genuinely valuable reflection. Rewriting
either rule's *practice* to match its stale *text* would have meant deleting real, useful, honest
content. Reworded both rules instead — in `CLAUDE.md`, the live files, and the engine template's
two mirrored copies, so nothing drifts apart again.

### RO-5.1 — Verdict-line and heading formats
> From: Repo organization audit, 2026-08-26 · Original section: Batch 5 — the 11 notebooks · Status: fixed 2026-08-26

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

### RO-5.2 — Missing blank lines after headings in Topic 9
> From: Repo organization audit, 2026-08-26 · Original section: Batch 5 — the 11 notebooks · Status: fixed 2026-08-26

**Mechanical**: `topic-09` was missing a blank line after all 21 of its headings, the one
notebook that didn't already do this. Fixed — diff is 21 pure insertions, content otherwise
unchanged, fence parity reverified.

### RO-5.3 — Intro-blockquote consistency
> From: Repo organization audit, 2026-08-26 · Original section: Batch 5 — the 11 notebooks · Status: fixed 2026-08-26

**Intro-blockquote consistency, checked against real Day-heading dates rather than the roadmap's
allocated day count**: caught myself here — Topics 5 and 6 both allocate 2 days in the roadmap,
but their actual Day 1/Day 2 headings share one calendar date each, meaning both were really
one-session topics. Wrote each an honest note explaining the compression instead of the generic
"two sessions" line the other multi-day topics correctly get.

### RO-5.4 — Notebook items left unfixed on purpose
> From: Repo organization audit, 2026-08-26 · Original section: Batch 5 — the 11 notebooks · Status: left as is on purpose

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

### FS-I-1 — The audit-trigger bug was never fixed in `CLAUDE.md`
> From: Final sign-off audit, 2026-08-31 · Original section: Important · **`CLAUDE.md` / process integrity** · Severity: important · Status: fixed 2026-08-31 in `CLAUDE.md`; the wording was lost in the 2026-09-25 rules rewrite — open again

- **`CLAUDE.md`'s own audit-trigger bug was never fixed in the file that actually governs this
  repo.** `public-readiness.md` recommended changing the trigger from "the topic that most
  recently cleared is a multiple of 10" to "highest cleared topic ≥ next un-audited multiple of
  10" (the phrasing bug that caused `topic-10-professionalism.md` to be dated after the topic it claims to
  precede). `repo-organization.md` says it fixed "the exact latent bug" — but its own text scopes
  that fix to `engine/CLAUDE.template.md` only. Verified today: the live root `CLAUDE.md`, line
  30, still reads the old, buggy phrasing. The fork template is now *more correct* than the file
  this repo itself reads every session. **Fix**: apply the identical phrasing fix already made in
  the template to the real `CLAUDE.md`, and add the template's Topic-53 final-audit rule (also
  never added to the real file) while there.

### FS-I-2 — `CLAUDE.md`'s Repo layout didn't describe most of the repo
> From: Final sign-off audit, 2026-08-31 · Original section: Important · **`CLAUDE.md` / process integrity** · Severity: important · Status: superseded — `CLAUDE.md` is now a loader; the layout lives in `README.md`

- **`CLAUDE.md`'s "Repo layout" section doesn't describe most of the repo.** It lists only
  `learning/`, `orbit/`, and `audits/`. It never mentions `engine/`, `docs/`, `.github/`, or any
  of the root hygiene files (`README.md`, `CONTRIBUTING.md`, `SECURITY.md`, `LICENSE`,
  `.gitignore`, `.gitattributes`) — all of which exist, are substantial, and are exactly the kind
  of thing a session-start orientation section exists to explain. `README.md`'s own repo-tree
  diagram, by contrast, documents the full structure accurately. **Fix**: extend `CLAUDE.md`'s
  Repo layout section to name every top-level folder and the root hygiene files, matching what
  `README.md` already does correctly.

### FS-I-4 — Line-number citations into the Topic 10 audit rotted
> From: Final sign-off audit, 2026-08-31 · Original section: Important · **`audits/` self-consistency** (found by this audit's dedicated cross-check of all three prior audit files against each other and the live repo) · Severity: important · Status: fixed 2026-08-31 — citations de-lined

- **`public-readiness.md`'s own line-number citations into `topic-10-professionalism.md` have rotted.**
  `repo-organization.md`'s Batch 4 inserted a 6-line blockquote into that file's header, shifting
  every line after it down by 6 — including the four places `public-readiness.md` cites by line
  number, one of which (C-5) is specifically the citation to where the employer-name disclosure
  lived. Ironically, `repo-organization.md`'s own Batch 1 claims to have already fixed "two
  line-number citations [that] had rotted when the new index table shifted the file they pointed
  at" — the identical bug class, reintroduced later in the same audit session, uncaught since.

### FS-I-22 — Topic 11 — H1 wording vs the roadmap
> From: Final sign-off audit, 2026-08-31 · Original section: Important · **Notebook technical accuracy** (each verified by direct reproduction or against primary documentation, not just read for plausibility) · Severity: important · Status: open — the H1 now says 'and' while the roadmap says '&' (checked 2026-09-25)

- **Topic 11** (H1, line 1): titled "...Best Practices" with an ampersand; the fixed topic-name
  list spells it "...Best Practices" with the word "and" — a topic-name exact-wording violation.

### FS-m-1 — Notebook filename slugging
> From: Final sign-off audit, 2026-08-31 · Original section: Minor · Severity: minor · Status: fixed 2026-08-31 — notebooks renamed

- **Notebook filename slugging is systemically inconsistent.** `CLAUDE.md`'s stated rule requires
  both the topic's title and subtitle in the filename. Topic 1 keeps only the title; Topics 2, 3,
  4, 6, 7, 8 each keep only one half (inconsistently, not the same half every time); only Topics 5,
  9, 10, 11 comply with both halves. This is a repo-wide pattern, not an isolated slip in any one
  file — worth resolving once, either by renaming all eight non-compliant notebooks or by amending
  the stated rule to match the abbreviated convention actually in use everywhere going forward.

### FS-m-2 — The local-clock note in notebooks
> From: Final sign-off audit, 2026-08-31 · Original section: Minor · Severity: minor · Status: closed — decided against 2026-08-31

- ~~The required "raw output may show the machine's local clock, not IST" note is missing from
  most notebooks that need it~~ — **decided against, 2026-08-31**: added to Topics 1, 2, 4, 6, 7,
  and 9, then explicitly reverted per direct feedback that these notes aren't wanted in the
  notebooks. `CLAUDE.md`'s and `engine/CLAUDE.template.md`'s Dates rules were both amended the
  same day to drop the "worth a one-line note" clause entirely — this is now a closed decision,
  not an unaddressed gap, in both the real rules and the fork template. A future audit shouldn't
  re-raise this.

### FS-m-3 — Gaps in the Syntax-line rule
> From: Final sign-off audit, 2026-08-31 · Original section: Minor · Severity: minor · Status: not re-checked since

- **The "Syntax: line before the concrete example" rule has scattered gaps** — `cat`/`pwd`/`seq`
  (Topic 1/2), `sed`/`chmod +x` (Topic 4), `git branch -D/-d`/`git reset --hard` (Topic 8), `docker
  exec` used 9 times with no Syntax line ever given (Topic 10), and `HEALTHCHECK`/`COPY
  --chown=`/`docker start -a` (Topic 11). Not universal misses — most commands in every file do
  get the line — just inconsistent application worth a pass once notebooks stop being written
  and only need a formatting sweep.

### FS-c-3 — Placeholder READMEs had no H1
> From: Final sign-off audit, 2026-08-31 · Original section: Cosmetic · Severity: cosmetic · Status: superseded — placeholder READMEs removed 2026-09-25

- Placeholder `README.md` files under `orbit/`'s not-yet-built folders (nine of them, plus
  `app/tests/`) are single untitled paragraphs, while every folder with real content opens with an
  H1 — a consistent split, but one nobody's documented as intentional.

## Verified clean — negative results

**From the public-readiness audit, 2026-08-13:**

- **All 53 baseline topic names, all per-phase counts (8/11/14/6/7/5/2 = 53) and all day sums (98 + 17 + 5 = 120) correct.**
- **Zero broken markdown links. Zero date-range headings.** All 16 notebook Day headings match their `progress.md` session dates exactly. Session count 17 agrees across four files.

**From the final sign-off audit, 2026-08-31:**

- **No broken internal links.** 28 local Markdown links checked programmatically across all 50
  Markdown files in the repo — zero broken.
- **All 11 notebook `Verdict` lines present and correctly formatted** — checked mechanically
  against every notebook.
- **Topic naming is exact and consistent** across `roadmap.md`, `progress.md`,
  `handbook_status.md`, and all 11 notebook H1 titles (one single exception: Topic 11's "&" vs.
  "and," listed under Important) — checked directly, character for character.
