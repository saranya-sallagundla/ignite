# Accuracy and currency

Is what's written true and up to date? Technical claims in notebooks, stale facts, the field atlas, pacing numbers, and claims that don't match the repo.

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

### T10-1.3 — Topic 3 notebook taught a bash syntax rule backwards
> From: Topic 10 professionalism audit, 2026-07-27 · Original section: Batch 1 — Critical (4 items) · Severity: critical · Status: fixed 2026-07-27

3. **Topic 3 notebook taught a bash syntax rule backwards** (claimed `else echo "..."` was invalid
   and `else; echo "..."` was the fix — the reverse of the truth). *Why it matters*: this is a
   technical reference document; a factually wrong rule taught as a lesson actively miseducates
   anyone who reads it, including future-you.

### T10-5 — Notebook technical accuracy
> From: Topic 10 professionalism audit, 2026-07-27 · Original section: Batch 5 — Notebook technical accuracy · Status: fixed 2026-07-27

Fixed real technical errors across all 10 notebooks — each one independently verified, not just
reworded. Highlights: the SSH authentication mechanism was described as encrypted-challenge when
real SSH key auth is signature-based; `/etc/fstab` was twice said to be read by "the kernel" at
boot (it's the init system, systemd); a "No route to host" explanation blamed a router for a
destination that was actually on the same local subnet (the real cause is a local ARP failure); a
GitHub Actions claim said secrets always appear in logs (Actions auto-masks registered secrets by
default); and Topic 10 had a few internal-timeline inconsistencies (an anecdote placed on the
wrong day, a redundant command contradicting its own surrounding explanation).

*Why it matters*: these notebooks are the actual technical reference — if someone (including
future-you, prepping for a real interview) trusts a wrong rule recorded here, it fails at exactly
the moment it's relied on.

### PR-C-7 — Pacing reported "on track" while 20 days behind
> From: Public-readiness audit, 2026-08-13 · Original section: C — CRITICAL · Severity: critical · Status: fixed — Pacing Layer recalibrated (last on 2026-09-21)

| # | Finding |
|---|---|
| **C-7** | **Pacing reports "on track"; it is 20 days behind.** `roadmap.md:101-110` reads Calendar Day 20 (2026-07-25), `Pace: on track`, `Last recalibrated: — (not yet due)`. Verified: Day 1 = 2026-07-06, today = 2026-08-13 → **Calendar Day 39** against 19 roadmap days used. That is four times past `CLAUDE.md:199-201`'s 5-day recalibration trigger. **19 calendar days have no logged session.** Five files disagree about "now" (07-24 / 07-25 / 07-27 / 07-29 / 07-31). |
**C-7 is a bookkeeping failure, not a discipline one.** The gap is a documented personal absence —
exactly what `roadmap.md`'s buffer and the ~60 days of deliberate slack exist to absorb. Against the
6-month outer deadline the plan still fits comfortably: ~145 calendar days remain against ~101
roadmap days of work, leaving roughly 44 days of slack. The finding is that **the files say
otherwise** — `Pace: on track` and `Last recalibrated: — (not yet due)` are both untrue, and
`CLAUDE.md:199-201`'s own 5-day trigger fired weeks ago and was never acted on.

**Privacy note on the fix**: log the absence with a neutral reason (e.g. "unplanned absence — slack
consumed"). Do **not** record medical detail in this repo. It is a public repo, health information is
the most sensitive category in it, and the Light Days log's stated purpose is to keep the *pacing
trade-off* visible — which a neutral reason does just as well.

**Demo relevance.** If the director asks "are you on track?", the repo currently answers *yes* on
stale data. Recalibrated and openly accounted for, this is a non-issue and arguably a credibility
point — the tracking system caught its own gap. Left stale, a reviewer disproves it with one
subtraction.

### PR-H-10 — Scores presented as objective measurement
> From: Public-readiness audit, 2026-08-13 · Original section: H — HIGH · **Presentation** · Severity: high · Status: fixed — scores relabelled as self-assessed (confirmed by FS)

- **H-10. The grader graded its own teaching, presented as objective measurement.** `handbook_status.md` publishes scores out of 100 for 11 topics where the same AI designed the quiz, judged the answers and assigned the number — no published rubric anchors, no external validation. A senior engineer spots this in seconds and it retroactively taints the parts that *are* real. All 11 notebooks also open with an identical first-person line and no AI-provenance label. Fix: per-notebook provenance header; relabel scores as *self-assessed, AI-graded, not externally validated* **everywhere they appear** — the honest framing is more impressive than the number; and write `docs/METHOD.md`. **That document is the actual forkable asset, more than the notebooks are.**

### PR-H-12 — Captured output edited after the fact
> From: Public-readiness audit, 2026-08-13 · Original section: H — HIGH · **Presentation** · Severity: high · Status: not re-checked since

- **H-12. Retroactively edited "real captured output" — an integrity issue.** `CLAUDE.md:148-150` and `audits/README.md`'s captured-data rule state captured data is the one thing whose value depends on being real. The `project/` → `orbit/` rename was applied **backwards**: captured output *was* edited (`topic-10:317,323,326,327` now show post-rename names for an event observed before the rename — and `progress.md:308` still shows the original, so **two files disagree about the same observed event**), while narrative prose was left stale (`progress.md:289,308`; `topic-09:277,306` — the latter contradicting itself inside one sentence and citing a path that does not exist). Also `topic-10:319` records a version string for Session 16 that only existed from Session 17. Fix: restore captured output to its real historical values with a one-line "the folder was named `project/` at the time" note, and rename the four prose references.

### PR-H-15 — `container_name: orbit-app` breaks copy-pasteable commands
> From: Public-readiness audit, 2026-08-13 · Original section: H — HIGH · **Presentation** · Severity: high · Status: left as is on purpose (RO-2.4)

- **H-15. `container_name: orbit-app` breaks ~10 copy-pasteable commands** and is mentioned in no notebook. `topic-10:321` asserts "nothing here needed a manual `--name`" and `:324` gives the auto-generated name; every `docker exec` using it (`topic-10:367,374,375,423,437,439`; `topic-11:224,233,251`) now fails with the exact error `topic-10:432-434` teaches about.

### PR-H-16 — Notebooks 10 and 11 document incompatible compose files
> From: Public-readiness audit, 2026-08-13 · Original section: H — HIGH · **Presentation** · Severity: high · Status: not re-checked since

- **H-16. Notebooks 10 and 11 document two mutually incompatible compose files** and the deletion is recorded nowhere. `topic-10:330-347` has two services and a named volume, proves shared-volume behaviour at `:372-378`, and uses it as **quiz Q5's evidence** at `:467-470`; `topic-11:197-204` has one service and no volumes, while `:195` frames the change as purely additive. Topic 10's volume lesson and its Hands-on score now rest on artifacts that are gone.

### PR-M-3 — Sourcing
> From: Public-readiness audit, 2026-08-13 · Original section: M — MEDIUM (grouped) · Severity: medium · Status: not re-checked since

**Sourcing** — `field_atlas.md:113` makes an **unsourced factual claim about a named financial-services firm** inside a sentence marked high-confidence. A public unsourced claim about a named third party is a different risk category from a wrong adoption percentage: **cite it or cut the company name.** More broadly the file has **zero hyperlinks in 502 lines** and no legend defining its confidence tiers — yet its *conventions* are excellent (it self-flags secondary-source-only figures, separates confidence-in-direction from confidence-in-figure, and records a **negative** result where no signal was found). That is better epistemic hygiene than most published tech writing and is a real differentiator; adding URLs is the cheapest high-value fix in the repo, moving it from "thoughtful" to "auditable."

### PR-M-8 — Technical claims needing correction
> From: Public-readiness audit, 2026-08-13 · Original section: M — MEDIUM (grouped) · Severity: medium · Status: not re-checked since

**Technical claims needing correction** — these matter more than their tier suggests, because notebooks are interview-recital text. Load average is defined as processes "waiting for CPU time" when Linux counts R *and* D — contradicted by this repo's own topic-04, and it is *the* standard interview follow-up. A `No route to host` table row contradicts the same file's own correct on-link/ARP prose, and the wrong version is the memorizable one. Git is said to have "traditionally used something close to Git Flow" (Git Flow postdates Git's `maint`/`next`/`seen` model by years) and to have "no way of recognizing a cherry-picked commit as the same change" (patch-ids, `git cherry`, `--cherry-mark` and rebase's default skip all exist). `docker build --target builder` is said to prove an earlier build's stage persists as an image — build cache is not an image, and this is recorded as a *correct* quiz answer. A claim implies `pip install` can pull in gcc, when the slim image has none and the build **fails** — which is the actual motivation for the technique being taught. Plus a warning against a tag convention Actions do not use, a Recycle Bin explanation with the right conclusion and wrong mechanism, a bind-mount claim asserted from output that cannot distinguish it, a cross-reference to an exercise in the wrong topic, and one "Real discovery" header over text that concedes it is an unconfirmed working theory.

### RO-3.3 — Claims about `.github/` that didn't match the repo
> From: Repo organization audit, 2026-08-26 · Original section: Batch 3 — root and governance · Status: fixed 2026-08-20

**Claims that didn't match the repo**: the README's tree annotated `.github/` with "CI workflows,
issue forms, dependency policy" — none of the three existed. `.github/workflows/README.md`
described checks in the present tense over an empty folder. `SECURITY.md`'s scope table listed
`.github/` workflows as in-scope with none present. All three reworded to match reality, and
`.github/ISSUE_TEMPLATE/.gitkeep` was removed — GitHub parses `.md` files in that folder as
selectable issue-template choices, so it can't carry a placeholder README like the repo's other
reserved folders the way `.gitkeep` implied it eventually would.

### RO-4.1 — Gap-day arithmetic error in `roadmap.md`
> From: Repo organization audit, 2026-08-26 · Original section: Batch 4 — learning/ tracking hygiene · Status: fixed 2026-08-20

**A real arithmetic error**: `roadmap.md` flagged 2026-07-17 as the pacing layer's one "gap day"
(a session's past-midnight spillover with no new session starting that day) but didn't apply the
identical rule to 2026-07-15 or 2026-07-25, which have the same pattern. Verified against every
session's actual check-in/check-out timestamp in `progress.md`. Corrected to one explicit rule
and the honest count: **17 of 20 active days**, three gaps named, not "19 of 20 (1 gap)."

### RO-4.2 — Session 17 vs the Topic 10 audit date
> From: Repo organization audit, 2026-08-26 · Original section: Batch 4 — learning/ tracking hygiene · Status: fixed 2026-08-20

**A sequencing question, resolved by checking git history rather than guessing**: Session 17
(narratively dated 2026-07-24) credits work to the Topic 10 audit, which is dated 2026-07-27 —
three days later, despite its own title claiming to precede Topic 11. Traced the real commit
history: both were authored during the same later catch-up period already disclosed as
`public-readiness.md`'s C-7 finding. Neither date was altered — a short header note (a 5-line
blockquote, not literally one line) was added to the audit's own header explaining that "before
Topic 11" describes scope, not calendar order.

### FS-I-3 — The audit index mischaracterized the public-readiness audit
> From: Final sign-off audit, 2026-08-31 · Original section: Important · **`audits/` self-consistency** (found by this audit's dedicated cross-check of all three prior audit files against each other and the live repo) · Severity: important · Status: fixed — the index row reads 'repo already public, pre-remediation'

- **`audits/README.md`'s index — its own stated "source of truth" — mischaracterizes
  `public-readiness.md`.** The Milestone column calls it "pre-publish, Stage 1," but that audit's
  own headline finding is *"the repo is already public"* — the opposite claim — and its Gate 0
  even suggests taking the repo private during remediation. No "Stage 2" exists anywhere to make
  "Stage 1" meaningful. A reader who trusts only the index (which is the whole point of the
  index) comes away believing the opposite of that audit's actual finding.

### FS-I-5 — The repo organization audit's "one continuous session" claim
> From: Final sign-off audit, 2026-08-31 · Original section: Important · **`audits/` self-consistency** (found by this audit's dedicated cross-check of all three prior audit files against each other and the live repo) · Severity: important · Status: fixed 2026-08-31 — header corrected

- **`repo-organization.md` claims its five fix batches happened in "one continuous session";** its
  own cited commit list shows batches 1–4 committed 2026-08-20 and batch 5 committed 2026-08-26 —
  a 6-day gap, not one session.

### FS-I-7 — The Topic 10 audit's agent count didn't add up
> From: Final sign-off audit, 2026-08-31 · Original section: Important · **`audits/` self-consistency** (found by this audit's dedicated cross-check of all three prior audit files against each other and the live repo) · Severity: important · Status: fixed — it now reads '17-agent audit'

- **`topic-10-professionalism.md`'s own stated agent count doesn't match its own breakdown** (says
  "14-agent audit," breakdown sums to 17) — already flagged by `public-readiness.md`'s M-tier and
  still uncorrected through two further audit passes, including one that edited this exact file's
  header.

### FS-I-11 — Topic 1 — `/etc/.pwd.lock`
> From: Final sign-off audit, 2026-08-31 · Original section: Important · **Notebook technical accuracy** (each verified by direct reproduction or against primary documentation, not just read for plausibility) · Severity: important · Status: not re-checked since

- **Topic 1** (`/etc/.pwd.lock`, lines 104–105): states the file's mere presence signals an
  in-progress password edit. In reality it's a permanent lock *target* for `lckpwdf()`, present on
  essentially every Linux system at all times — presence alone means nothing; only an active
  advisory lock would.

### FS-I-12 — Topic 2 — load average
> From: Final sign-off audit, 2026-08-31 · Original section: Important · **Notebook technical accuracy** (each verified by direct reproduction or against primary documentation, not just read for plausibility) · Severity: important · Status: not re-checked since

- **Topic 2** (load average, lines 359–362): defines it as processes waiting for CPU only. Per
  `proc(5)`, load average counts both run-queue (R, CPU-wait) *and* uninterruptible-sleep (D,
  I/O-wait) processes — the omission erases the classic "high load, idle CPU" I/O-bottleneck
  scenario, a standard interview follow-up.

### FS-I-13 — Topic 2 — Day 1 intro vs Day 2
> From: Final sign-off audit, 2026-08-31 · Original section: Important · **Notebook technical accuracy** (each verified by direct reproduction or against primary documentation, not just read for plausibility) · Severity: important · Status: not re-checked since

- **Topic 2** (lines 11–16 vs. its own Day 2): the Day 1 intro names `ps`/`top`/`kill`/`ss` as
  examples of tools *not* covered in this topic — then teaches all four, with full hands-on
  detail, later in the same file's Day 2.

### FS-I-14 — Topic 3 — "deferred on functions" heading
> From: Final sign-off audit, 2026-08-31 · Original section: Important · **Notebook technical accuracy** (each verified by direct reproduction or against primary documentation, not just read for plausibility) · Severity: important · Status: fixed — the heading now says re-taught and re-passed the same session

- **Topic 3** (Day 2 heading, line 225): the heading says the quiz was "deferred on functions," but
  the file's own body shows it was re-taught and re-passed the *same session*, and Topic 3 is
  listed everywhere else as fully "Cleared" — never in the repo's distinct, formally-defined
  Deferred Mastery table. The wording risks colliding with that formal term.

### FS-I-15 — Topic 4 — `df` and `/proc`
> From: Final sign-off audit, 2026-08-31 · Original section: Important · **Notebook technical accuracy** (each verified by direct reproduction or against primary documentation, not just read for plausibility) · Severity: important · Status: not re-checked since

- **Topic 4** (line 96–97): claims `df` reads `/proc` the same way `ps`/`top`/`free` do. `df`'s
  usage stats come from `statfs()`/`statvfs()` against the mounted filesystem directly, not from a
  `/proc` read the way the others work.

### FS-I-16 — Topic 5 — "refused" and firewalls
> From: Final sign-off audit, 2026-08-31 · Original section: Important · **Notebook technical accuracy** (each verified by direct reproduction or against primary documentation, not just read for plausibility) · Severity: important · Status: not re-checked since

- **Topic 5** (lines 327–330, 445–453 — an official quiz answer): states that a `refused`
  response universally rules out a firewall in the path. That's only true of a silently-*dropping*
  firewall; a `REJECT`-configured one (common, not just DROP-by-default cloud security groups)
  also sends an active refusal, indistinguishable from "nothing listening."

### FS-I-17 — Topic 7 — the `-graph` claim
> From: Final sign-off audit, 2026-08-31 · Original section: Important · **Notebook technical accuracy** (each verified by direct reproduction or against primary documentation, not just read for plausibility) · Severity: important · Status: not re-checked since

- **Topic 7** (lines 59–63): claims `-graph` (single-dash) decomposes into a short-flag cluster
  `-g -r -a -p -h`, the same mechanism proven for `-all`. Reproduced directly: `git log --oneline
  -graph` in isolation returns `fatal: unrecognized argument: -graph` — it never actually reaches
  that decomposition; the combined command's real error aborts on `-all` first, so the `-graph`
  claim was never actually tested.

### FS-I-18 — Topic 7 — rebase insertion count
> From: Final sign-off audit, 2026-08-31 · Original section: Important · **Notebook technical accuracy** (each verified by direct reproduction or against primary documentation, not just read for plausibility) · Severity: important · Status: not re-checked since

- **Topic 7** (line 143, inside a section literally titled "Verified hands-on"): a rebase-continue
  commit is captured as `1 file changed, 4 insertions(+)`. Reproducing the exact described
  resolution (keep both lines via "Accept Both Changes") gives `1 insertion(+)` — the only count
  the described scenario supports.

### FS-I-19 — Topic 9 — Windows host path
> From: Final sign-off audit, 2026-08-31 · Original section: Important · **Notebook technical accuracy** (each verified by direct reproduction or against primary documentation, not just read for plausibility) · Severity: important · Status: not re-checked since

- **Topic 9** (lines 286–288, 317–319): the Windows host path is given as
  `C:\CloudOps\ignite\project\app\` — the folder is `orbit\app\` everywhere else in the repo,
  including the very same sentence's own `cd orbit/app` command.

### FS-I-20 — Topic 9 — `docker logs` timestamp note
> From: Final sign-off audit, 2026-08-31 · Original section: Important · **Notebook technical accuracy** (each verified by direct reproduction or against primary documentation, not just read for plausibility) · Severity: important · Status: closed — decided against 2026-08-31 (FS-m-2)

- **Topic 9** (lines 387–399): a `docker logs` timestamp lands a full calendar day past the Day
  1 heading's date, with no note anywhere in the file explaining raw output can show the
  machine's real clock rather than the narrative's IST dates (the repo's own standing rule
  requires this note once per file; six of the eleven notebooks — Topics 1, 2, 4, 6, 7, 9 — are
  missing it entirely).

### FS-I-21 — Topic 10 — `app-a` / `app-b` mounts
> From: Final sign-off audit, 2026-08-31 · Original section: Important · **Notebook technical accuracy** (each verified by direct reproduction or against primary documentation, not just read for plausibility) · Severity: important · Status: addressed — editorial note added to the notebook 2026-08-31

- **Topic 10** (lines 226–271): Day 2 states containers `app-a` and `app-b` already have specific
  bind mounts / volumes, and shows "verified" `docker inspect` output confirming it — but Day 1's
  own record creates both containers bare, with no mount, and the actual mount demonstration in
  Day 1 was on a separate, distinctly-named container (`app-c`). No command anywhere shows `app-a`
  or `app-b` actually acquiring these mounts.

### FS-I-23 — Topic 11 — `orbit-app-1` vs `orbit-app`
> From: Final sign-off audit, 2026-08-31 · Original section: Important · **Notebook technical accuracy** (each verified by direct reproduction or against primary documentation, not just read for plausibility) · Severity: important · Status: addressed — note added to the notebook 2026-08-31

- **Topic 11 / `orbit/docker-compose.yml`**: the notebook's "combined scenario" addresses the
  container throughout as `orbit-app-1` (the Compose-default auto-generated name), but the real,
  current `docker-compose.yml` sets `container_name: orbit-app` explicitly — so the actual
  container is named `orbit-app`, with no numeric suffix. Re-running the notebook's exact commands
  against today's file would fail with "No such container: orbit-app-1." This is a fresh instance
  of the same class of problem `public-readiness.md`'s H-15/H-16 already found and considered
  resolved elsewhere in this same file.

### FS-I-24 — FinOps statistic a report-cycle stale
> From: Final sign-off audit, 2026-08-31 · Original section: Important · **`field_atlas.md` currency** (see the dedicated section below — summarized here as findings) · Severity: important · Status: fixed — now in `field_atlas.md` (checked 2026-09-25)

- The FinOps statistic (63% tracking AI spend) is a full report-cycle stale: the FinOps
  Foundation's newer *State of FinOps 2026* report (published Feb 2026, before this file's own
  last fact-check date) reports 98%.

### FS-I-25 — IBM–HashiCorp acquisition missing
> From: Final sign-off audit, 2026-08-31 · Original section: Important · **`field_atlas.md` currency** (see the dedicated section below — summarized here as findings) · Severity: important · Status: fixed — now in `field_atlas.md` (checked 2026-09-25)

- The Terraform-vs-OpenTofu section never mentions IBM's completed ~$6.4B acquisition of
  HashiCorp (closed February 2025) — arguably the single biggest structural fact behind the
  adoption trend the section is trying to describe.

### FS-I-26 — AgentOps not listed
> From: Final sign-off audit, 2026-08-31 · Original section: Important · **`field_atlas.md` currency** (see the dedicated section below — summarized here as findings) · Severity: important · Status: fixed — now in `field_atlas.md` (checked 2026-09-25)

- **AgentOps** — operating/governing autonomous AI agents in production, distinct from AIOps — has
  real 2026 survey backing (LangChain's State of Agent Engineering report, a Futurum Group
  enterprise survey) and isn't listed anywhere in §1.5, including the "emerging" tier.

### FS-I-27 — GreenOps confidence dated
> From: Final sign-off audit, 2026-08-31 · Original section: Important · **`field_atlas.md` currency** (see the dedicated section below — summarized here as findings) · Severity: important · Status: fixed — now in `field_atlas.md` (checked 2026-09-25)

- The GreenOps entry's "confidence: low that this has crystallized" is now dated: the Green
  Software Foundation's SCI spec became an accredited ISO standard (ISO/IEC 21031:2024) and gained
  a follow-on framework in late 2025 — comparable institutional weight to several already-listed
  entries.

### FS-m-5 — Small technical overstatements
> From: Final sign-off audit, 2026-08-31 · Original section: Minor · Severity: minor · Status: not re-checked since

- **A few small, verified technical overstatements**: Topic 1's `mysql -p` example doesn't
  actually reach `.bash_history` the way described (only the space-less inline form does); Topic
  5's private/public IP heuristic omits a few other reserved ranges (link-local, multicast, CGNAT)
  while explicitly framing itself as covering exceptions; Topic 11's "effectively existed twice"
  claim about the venv duplication bug doesn't reconcile with its own measured 27MB delta (a
  ~50MB venv would produce ~50MB, not 27MB); Topic 11's "no compile step, ever" for `python app.py`
  overstates it — CPython always compiles to bytecode, just not ahead-of-time to a standalone
  binary.

### FS-m-6 — `field_atlas.md` refresh opportunities
> From: Final sign-off audit, 2026-08-31 · Original section: Minor · Severity: minor · Status: not re-checked since

- **`field_atlas.md` refresh opportunities below the "stale/wrong" bar**: the FinOps bullet
  paraphrases its source as "tracking AI-specific cloud spend" where the report's actual wording is
  "managing AI spend" (a real but small difference); OpenTofu's CNCF status is stated without
  noting it's still Sandbox-tier, not Incubating; the GitOps adoption figure now has a better
  primary source available (CNCF's own July 2025 announcement) than the secondary-source hedge
  currently used.

### FS-c-1 — Topic 8 — `@latest` as an Actions example
> From: Final sign-off audit, 2026-08-31 · Original section: Cosmetic · Severity: cosmetic · Status: not re-checked since

- Topic 8's quiz answer restates a mitigation using `@latest` as its floating-tag example where
  the body text (and the actual GitHub Actions ecosystem) uses `@v4`/`@main` — `@latest` is a
  Docker/npm convention, not one Actions pins against.

### FS-c-2 — Repo organization audit called a 5-line note "one-line"
> From: Final sign-off audit, 2026-08-31 · Original section: Cosmetic · Severity: cosmetic · Status: fixed — its text now says a 5-line blockquote

- `repo-organization.md` describes its own header addition to `topic-10-professionalism.md` as "a one-line
  note"; the actual insertion is a 5-line blockquote.

### FS-A — `field_atlas.md` — currency check and the anti-drift mechanism
> From: Final sign-off audit, 2026-08-31 · Original section: `field_atlas.md` — currency check and the anti-drift mechanism · Status: mechanism built 2026-08-31; stall defect found and fixed 2026-09-21

#### What's actually still true, and what's drifted

A dedicated fact-check agent verified `field_atlas.md`'s five most checkable, dateable claims
against live web research (2026-08-31). One holds up completely as written: the dockershim/v1.24
removal (May 2022) needed no change. The other four have real, dateable drift, detailed under
Important above — a stale FinOps statistic (one full report-cycle behind), a missing structural
fact in the Terraform/OpenTofu section (the IBM acquisition), an under-confident GreenOps entry,
and a missing sub-discipline candidate (AgentOps) with genuine 2026 survey backing. None of this
is a quality problem with the file's methodology — its sourcing discipline and confidence-tiering
are still exactly as rigorous as the file's own stated standard demands. It's a **currency**
problem: the file was last checked 2026-07-29, today is 2026-08-31, and in the 33 days between,
the field moved in checkable, sourceable ways nothing caught.

#### Why it went stale, and why that's not a one-off

`field_atlas.md`'s "Last sub-discipline check" mechanism has exactly one trigger:
`CLAUDE.md`'s "Daily session shape," step 1 — which only runs when a **teaching session**
happens. No teaching session has run since Session 17 (2026-07-24). Two audit sessions ran in that
gap (2026-08-13, 2026-08-26) — neither is a "daily session" under that heading, and neither
triggered the check. The date simply never came up again until this audit went looking for it.

**This is the identical root cause behind `public-readiness.md`'s C-7 finding** — the Pacing
Layer in `learning/roadmap.md` still reads "Calendar Day 20 (2026-07-25), Pace: on track, Last
recalibrated: — (not yet due)" today, unchanged since that audit flagged it a month ago at Day 39
(it's now Day 57). Both mechanisms rely entirely on a teaching session happening to notice they've
gone stale. When teaching sessions stop — for any reason, including entirely legitimate ones like
running audits instead — nothing else in the repo notices, for as long as that gap lasts. A
40-day gap and a 400-day gap would look identical to this system: silent, until someone happens to
check by hand, which is exactly what this audit just did for both files independently.

#### A concrete mechanism, not just a flag

Two layers, because a fix that only lives inside a Claude Code session inherits the exact failure
mode it's meant to solve — it can't fire if no session opens.

**Layer 1 — inside the repo, but no longer gated on session type.** Move the `field_atlas.md` /
Pacing Layer staleness check out of "Daily session shape" (which reads, and is used, as
teaching-specific) and into an unconditional step that runs at the start of **any** session opened
in this repo — teaching, audit, or otherwise. Replace the soft "if it isn't today" check with a
hard threshold: if either date is more than 14 real calendar days old, say so immediately, before
addressing whatever the session actually opened to do — exactly what should have happened at the
top of this very audit, and didn't, because the current wording scopes the check to teaching
sessions specifically. Add a single visible staleness stamp (e.g., a one-line "repo last opened:
`<date>`" at the top of `progress.md`) updated by *any* session, so the gap is visible on sight
without doing date arithmetic.

**Layer 2 — outside the repo, independent of whether a session ever opens.** Layer 1 still can't
fire during a month where nobody opens Claude Code in this folder at all — which is exactly what
happened here. That requires a trigger that doesn't live inside a conversation: either (a) a
Claude Code-native scheduled task (`mcp__scheduled-tasks__create_scheduled_task` or `CronCreate`
appear available as tools in this environment — worth testing directly, since `CLAUDE.md`
currently states only that "routines" specifically are disabled at the org level, which may or may
not be the same restriction), or, if that's blocked the same way, (b) a plain Windows Task
Scheduler job running `claude -p "check field_atlas.md and roadmap.md staleness, flag if over 14
days"` non-interactively on a weekly cadence, writing its result somewhere the user will see it
next time they're at the machine — independent of Claude Code's own policy entirely. This is the
layer that actually makes the guarantee real; Layer 1 alone is the same design that already failed
once.

**Note on scope**: this only applies to Part 1 of `field_atlas.md` (the state-of-the-field
sections and the §1.5 sub-discipline list) — calendar-time-sensitive content with no other trigger
to revisit it. Part 2 ("Topics Covered So Far") already has a safe, event-driven update path: it
grows exactly when a topic clears, which is already tracked elsewhere and can't silently lag.

#### What was actually built (2026-08-31), and where it departed from the proposal above

**Layer 2 resolved empirically, and the answer changed the design.** Both candidate schedulers
were tested rather than assumed:

- **`CronCreate` is unusable for this**, per its own contract: jobs are "session-only (in-memory,
  gone when this Claude session ends)" and recurring ones "auto-expire after 7 days." It
  reproduces the exact failure mode the backstop exists to prevent, so it was rejected outright.
  Worth recording explicitly, since it's the more obvious-looking of the two tools.
- **The `scheduled-tasks` MCP server is live and functional** — it responded normally, with no
  permission error. So **`CLAUDE.md`'s standing claim that "Claude Code routines are disabled at
  the organization level" was outdated**, and option (a) was available all along. This is itself a
  finding: a capability assumption written into the rules months ago had quietly stopped being
  true, and nothing re-tested it. Both `CLAUDE.md` and `field_atlas.md`'s header carried that
  stale claim and have been corrected.

Built: a persisted task `ignite-field-atlas-check`
(`~/.claude/scheduled-tasks/ignite-field-atlas-check/SKILL.md`, verified on disk and enabled),
running `47 8 1,15 * *` — twice monthly, at an off-minute deliberately, and firing on next app
launch if the app was closed when due. Its prompt is fully self-contained (a scheduled run has no
memory of this session): it checks the date first and **no-ops if the atlas is 14 days fresh or
newer**, scopes itself to Part 1, restates the file's own sourcing conventions, updates the date
even on a no-change result, pushes to `origin` only, and refuses to commit if the working tree is
dirty or mid-merge.

**Departure 1 — the `progress.md` staleness stamp was deliberately not built.** The proposal above
suggested mirroring a "last opened" date into `progress.md` so the gap is visible without
arithmetic. On implementation this looked like the wrong instrument: it invents a *third* date that
itself needs maintaining and comparing, in a repo that has already been bitten repeatedly by
duplicated facts drifting apart (this same audit found four rotted line-number citations). The
actual mechanical gap was narrower and more fixable — `field_atlas.md`'s date lives in a file a
non-teaching session has no reason to open, so the failing session never saw it. Fixed by naming
`field_atlas.md`'s header in `CLAUDE.md`'s mandatory every-session read list instead, alongside
`roadmap.md` and `progress.md`. No new duplicated state, and the date is now in front of every
session by construction.

**Departure 2 — the Pacing Layer check tests the written data, not `Pace`.** The proposal said to
check "if either date is more than 14 days old." For the Pacing Layer specifically that's the
wrong test, because `Pace` is a *derived verdict* and a stale layer keeps reporting the old one
cheerfully — the file read `Pace: on track` while sitting 19 days behind, so a check that trusted
`Pace` would have confirmed the error rather than caught it. The implemented check recomputes
Calendar Day from Day 1 and compares it against the figure actually written in the file; any
difference is both the detection signal and the exact size of the drift.

**Departure 3 — no Windows Task Scheduler fallback, on purpose.** Option (b) is not built, and
shouldn't be. Its only advantage over the task above is firing when Claude Code is never opened at
all — but a job whose output lands in a file nobody opens isn't a notification, and it adds real
fragility (headless auth, PATH, and MCP servers that may be absent in non-interactive runs). If
Claude Code is never opened in this folder again, the repo isn't being worked on and atlas
staleness is moot. Recorded here as a considered rejection rather than an oversight, so a future
audit doesn't re-propose it as a gap.

**Generalized into the engine.** `engine/CLAUDE.template.md` received the same restructure — an
unconditional "Every session, before anything else" section, the written-data-not-derived-verdict
rule, the 14-day-not-daily threshold with its reasoning, and an instruction to add an automated
backstop **only** after checking a scheduler's actual persistence contract, with an explicit
warning not to assume scheduling is unavailable without testing it. That last point is the durable
lesson from this fix: the untested capability assumption was as much the root cause as the
misplaced check.

#### Follow-up, 2026-09-21 — the backstop's first real test, and a defect in it

The mechanism above shipped 2026-08-31. Its record over the next three weeks:

- **2026-09-01 run — correct.** Found the atlas 2 days old, reported "not due," changed nothing.
- **2026-09-15 run — stalled, and misreported.** The atlas was 15 days old, so the check was due.
  The run issued one `Read` and one `Bash`, then froze: `started_at` identical to
  `last_activity_at` to the millisecond, no result, no closing report. The runner recorded it as
  **"succeeded."** Root cause: a tool-permission prompt with nobody present to approve it — the
  exact scenario the task-creation tool warned about, and one this audit didn't act on when the
  task was built.
- **Caught 2026-09-21 by Layer 1**, when a session opened and the every-session check flagged the
  atlas at 21 days. So the two-layer design held — but only because a session happened to open.
  Had the gap run longer, Layer 2 would have kept reporting success while doing nothing.

Stated plainly: **Layer 2, as originally built, had a silent-failure mode of the same class it was
meant to eliminate.** A backstop that reports success while stalled is worse than no backstop,
because it's trusted.

**Fix applied 2026-09-21**, in two parts. Procedural: the task was run once by hand with the user
present to approve each prompt; those approvals persist on the task, so unattended runs now
inherit them. That run then completed and did real work — including updating a Platform
Engineering citation from the 2024 report to the July 2026 edition that the **2026-08-31 manual
fact-check itself had missed**, which is the clearest possible evidence the backstop is worth
keeping. Rule: `CLAUDE.md`'s backstop paragraph and `engine/CLAUDE.template.md` now both say a
run's status is not evidence — verify by output (`list_task_runs` for zero-activity runs, the
transcript for a closing report), and run any new scheduled task once attended before trusting
it. Recorded here rather than quietly patched so the mechanism's writeup doesn't overstate what
it guaranteed on the day it was built.

## Verified clean — negative results

**From the public-readiness audit, 2026-08-13:**

- **All 11 topics' score arithmetic correct and matching across four files — 33 individual figures, zero discrepancies.**
- Repo hygiene files all present; committed line endings uniformly LF; `field_atlas.md`'s TOC anchors all resolve. Spot-verified correct: the full CIDR table including `/1` and `/0`, the on-link/ARP explanation, a hunk-header decode, a rebase-hash proof, a `merge-base` result independently re-derived, and Actions secret-masking and fork-PR token behaviour.
