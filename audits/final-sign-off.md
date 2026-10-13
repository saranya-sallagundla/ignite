# Final Sign-Off Audit — 2026-08-31

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

---

## Headline

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

---

## Critical

### 1. The actual public repository is still the pre-remediation, exposed snapshot from a month ago

Verified live, today, via `git fetch` against both remotes and `gh api`:

| | `origin` (private org copy) | `personal` (**public**, the actual product) |
|---|---|---|
| Visibility | Private | **Public** (`isPrivate: false`) |
| Last pushed | 2026-08-31 (today) | **2026-07-31** — 31 days stale |
| Commit lineage | Rewritten/clean (76 commits) | **Original, unrewritten** (58 commits) — shares **zero** common ancestor with the clean lineage; `git merge-base` returns nothing |
| Employer name/email in commit history | 0 occurrences (verified: `git log -p origin/main \| grep -ci <employer>` → 0) | **72 occurrences** across ~35+ commits, as the Author/Committer identity, publicly readable via GitHub's commits API with no login |
| `claude-memory/` folder (AI notes about the author) | Absent — removed from the current lineage entirely | **Present**, 5 files, still live |
| `LICENSE` / `SECURITY.md` / `CONTRIBUTING.md` / `audits/` / `engine/` / `docs/` | All present | **None of them exist yet** |

None of this is a new discovery — `public-readiness.md` diagnosed the identity exposure in
exhaustive detail (its C-1 through C-6, H-1 through H-5) and prescribed the exact fix: "**One**
history rewrite covering the corporate email, the org name, and the user ID... Publish as a
**fresh, unforked** repo under the personal account — never by flipping visibility on the
org-hosted copy." That rewrite happened — but only on `origin`, the private copy nobody outside
the org can see. `SECURITY.md`'s current claim — "Git history was rewritten to remove identity
metadata that a working-tree-only check would have missed" — is true of `origin` and **false of
the repository the public actually visits**, since that repository doesn't even contain a
`SECURITY.md` yet to make the claim.

**Why it matters**: this isn't a future risk to prevent before "going public" — the exposure has
been live for 31 days already. Every day it stays this way is 31 more days of a real name and a
real corporate email address sitting in a public commit history, searchable and scrapeable, plus
an AI-generated behavioral characterization of the account holder sitting in a folder next to it.

**Fix**: execute Gate 1 of `public-readiness.md`'s own remediation sequence, specifically against
the `personal` remote — not `origin`. The clean lineage already exists locally (`main`, 76
commits, verified free of the employer string). Force-pushing that lineage to `personal` (after
setting repo-local commit identity to a personal name/no-reply address, per that audit's step 6)
would resolve C-1 through C-6 and bring the public copy current with a month of hygiene work in
one action — but see Critical Finding 2 first; that audit's own Gate 0 says nothing else is worth
doing until it's answered.

### 2. B-1 — the right-to-publish question is still open, per the repo's own last review of it

`public-readiness.md`'s B-1 finding — whether an employment agreement's IP-assignment terms mean
the repo's author isn't actually free to grant the MIT/CC BY licenses this repo publishes — is
explicitly listed as still open in `repo-organization.md`'s own "What was deliberately left
unfixed" section: *"The right-to-publish question (`public-readiness.md`'s B-1) — unaffected by
any wording fix."* Nothing in the repo shows this has been resolved since (it wouldn't
necessarily show in a committed file either way, which is exactly why it needs a direct answer
rather than a file-based check).

**Why it matters**: `public-readiness.md` put this ahead of everything else for a reason —
"Publishing a licence you cannot back is worse than publishing none." Every fix elsewhere in this
report, including Finding 1's remediation, is worth doing regardless of the answer, but a public
LICENSE grant only means what it says if this question has an actual yes behind it.

**Fix**: this needs a direct answer from you, not a repo change — see the question at the end of
this report.

> **Resolved 2026-08-31.** Confirmed directly: no employer written confirmation is needed — this
> is a self-created personal learning project, not employer work. This matches what was already
> settled on 2026-08-13 (the org GitHub is used only because org-provisioned Claude Code can't
> integrate with a personal account; no approvals were required then either) — that resolution
> just never made it into a committed audit file, only into session memory, which is why B-1 kept
> reappearing as an open finding across two subsequent audits. **B-1 is closed. Do not re-raise
> it in a future audit** — if a later session is unsure, this note is the durable record, not
> memory.

### 3. `engine/` — the entire "fork this" pitch — carries no license grant at all

Independently found by this audit's own direct review of the two license files and confirmed by
the dedicated `engine/`-simulation agent. `README.md`'s License section is explicit and exhaustive
about scope: *"MIT — the software: `orbit/`, `.github/`, and any scripts or configuration
elsewhere in the tree... CC BY 4.0 — the written material: `learning/`, `docs/`, `audits/`, and
the Markdown documents at the repository root (this file, `CONTRIBUTING.md`, `SECURITY.md`,
`CLAUDE.md`)."* `learning/LICENSE` repeats the identical closed list. `engine/` is none of those
things — it isn't `orbit/`, isn't `.github/`, isn't `learning/`/`docs/`/`audits/`, and its own
Markdown files sit one level below the repository root, not at it. There is no `LICENSE` inside
`engine/` itself. A search for the word "license" anywhere in `engine/`'s eight files returns
zero matches. Two prior audits (2026-08-13's H-6 licensing review and 2026-08-26's root-governance
batch) both worked on licensing and neither one caught this.

**Why it matters**: `CONTRIBUTING.md` calls forking `engine/` "the intended reuse... packaged."
`README.md` calls it "the whole system with the DevOps removed... copy unedited." Under a literal
reading of both license grants, a stranger who does exactly what the repo invites them to do —
copy `CLAUDE.template.md`, `MISSION.template.md`, the `templates/` files — has no stated
permission to do so. That's real, avoidable legal ambiguity sitting directly inside the one folder
whose entire purpose is to be copied.

**Fix**: add `engine/` explicitly to the CC BY 4.0 grant (the natural fit — it's template/written
material, not software) in both `README.md`'s License section and `learning/LICENSE`'s enumerated
path list, or place a standalone, maximally permissive license (CC0 or MIT) inside `engine/`
itself so a forker never has to reason about which grant applies. Given `engine/`'s purpose,
the standalone license is probably cleaner.

### 4. `QUICKSTART.md`'s default setup path breaks at the very first mandatory step

Verified directly by the `engine/`-simulation agent: `QUICKSTART.md`'s primary path is `mkdir
my-mission && cd my-mission` then `git init` — a fresh local repo with **no remote configured
anywhere** in the five-minute setup. `CLAUDE.template.md` (copied "unedited," per its own
instructions) hard-requires *"Commit and push after every session — never batch sessions into one
commit"* as step 7 of every day's session shape. No file in `engine/` (`QUICKSTART.md`,
`CLAUDE.template.md`, `MISSION.template.md`, `README.md`) ever instructs creating a remote or
running `git remote add origin`. Reproduced directly: a fresh `git init` + first commit + `git
push` fails immediately with `fatal: No configured push destination.`

**Why it matters**: this is the exact persona the audit brief asked to simulate — a total
stranger following the documented default path — hitting a hard failure at the mandatory first
logging step of their very first session, with the protocol itself insisting push is not
optional.

**Fix**: add a step to `QUICKSTART.md`'s "Create your own mission repo" section instructing the
reader to create an empty remote (GitHub or otherwise) and run `git remote add origin <url>`
before Day 1, or explicitly state that push is a no-op/skippable until a remote exists.

### 5. `CLAUDE.md`'s git-metadata exemption — the policy that let Finding 1 happen — was never removed

`public-readiness.md`'s own "Rule changes this audit recommends" list, item 1: *"Remove the
git-metadata exemption. It was correct for a private repo and is now the largest exposure in a
public one."* Verified today: `CLAUDE.md` line 136 still reads *"the git remote/metadata is
exempt — only file content matters."* `engine/CLAUDE.template.md` line 134 carries the identical,
never-updated exemption. Neither file was changed following that recommendation, in the more than
two weeks and one further audit (2026-08-26) since it was made.

**Why it matters**: this is the standing rule that made Finding 1's exposure acceptable-by-policy
in the first place, for a repo that has been publicly visible (Finding 1) for the entire time this
rule has gone unamended. Leaving it in place is an active decision to keep tolerating exactly the
class of exposure Finding 1 describes, going forward, in both the real repo and the fork template
everyone else will inherit it from.

**Fix**: remove the exemption from both `CLAUDE.md` and `engine/CLAUDE.template.md` now, matching
the audit's own recommendation, and add repo-local git identity + commit signing (already
recommended in that audit's Gate 1, step 6) so no future commit adds a new instance of the same
problem.

---

## Important

Grouped by area. Each is independently verified — either by this audit directly or by a dedicated
review agent whose specific claim I checked before including it here.

**`CLAUDE.md` / process integrity**
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
- **`CLAUDE.md`'s "Repo layout" section doesn't describe most of the repo.** It lists only
  `learning/`, `orbit/`, and `audits/`. It never mentions `engine/`, `docs/`, `.github/`, or any
  of the root hygiene files (`README.md`, `CONTRIBUTING.md`, `SECURITY.md`, `LICENSE`,
  `.gitignore`, `.gitattributes`) — all of which exist, are substantial, and are exactly the kind
  of thing a session-start orientation section exists to explain. `README.md`'s own repo-tree
  diagram, by contrast, documents the full structure accurately. **Fix**: extend `CLAUDE.md`'s
  Repo layout section to name every top-level folder and the root hygiene files, matching what
  `README.md` already does correctly.

**`audits/` self-consistency** (found by this audit's dedicated cross-check of all three prior
audit files against each other and the live repo)
- **`audits/README.md`'s index — its own stated "source of truth" — mischaracterizes
  `public-readiness.md`.** The Milestone column calls it "pre-publish, Stage 1," but that audit's
  own headline finding is *"the repo is already public"* — the opposite claim — and its Gate 0
  even suggests taking the repo private during remediation. No "Stage 2" exists anywhere to make
  "Stage 1" meaningful. A reader who trusts only the index (which is the whole point of the
  index) comes away believing the opposite of that audit's actual finding.
- **`public-readiness.md`'s own line-number citations into `topic-10-professionalism.md` have rotted.**
  `repo-organization.md`'s Batch 4 inserted a 6-line blockquote into that file's header, shifting
  every line after it down by 6 — including the four places `public-readiness.md` cites by line
  number, one of which (C-5) is specifically the citation to where the employer-name disclosure
  lived. Ironically, `repo-organization.md`'s own Batch 1 claims to have already fixed "two
  line-number citations [that] had rotted when the new index table shifted the file they pointed
  at" — the identical bug class, reintroduced later in the same audit session, uncaught since.
- **`repo-organization.md` claims its five fix batches happened in "one continuous session";** its
  own cited commit list shows batches 1–4 committed 2026-08-20 and batch 5 committed 2026-08-26 —
  a 6-day gap, not one session.
- **That same audit fixed the root `LICENSE` file's GitHub-detectability** (so the license facet
  now correctly shows "MIT" instead of "Other/NOASSERTION") while listing B-1 as explicitly
  gating all licensing work ("Gate 3... blocked on B-1"). Making the license cleanly
  machine-readable is precisely the public-facing signal that gate exists to hold back until B-1
  resolves — the fix and the gate point in opposite directions.
- **`topic-10-professionalism.md`'s own stated agent count doesn't match its own breakdown** (says
  "14-agent audit," breakdown sums to 17) — already flagged by `public-readiness.md`'s M-tier and
  still uncorrected through two further audit passes, including one that edited this exact file's
  header.

**`orbit/` accuracy**
- **`orbit/README.md`'s Status section misdescribes the roadmap it's summarizing.** It says
  Kubernetes, CI/CD, and Terraform "follow in the later phases" — but per `learning/roadmap.md`'s
  own fixed baseline, Kubernetes (12–14), CI/CD (15–16), Ansible (17) and Terraform's introduction
  (18) are the *remaining topics of the current phase* (Phase 2, "now underway" per the roadmap's
  own Pacing Layer), not later phases. Only Terraform's deepening (Phase 4) and observability
  (Phase 6) are genuinely later.
- **`orbit/docs/concept.md` still reads as curriculum scaffolding rather than a standalone project
  vision**, in the one folder `CLAUDE.md` explicitly bans that from ("no internal-scaffolding
  language... references to this file"). It calls itself "the vehicle used to drive hands-on
  learning through the roadmap," times its own revisit to "the end of the learning journey (all 53
  topics complete)," and dates a design decision to "before Topic 9 began." Found independently by
  two separate review agents (the `docs/` and `orbit/` passes). `repo-organization.md` flagged "the
  `docs/concept.md` reword" as a known open item and deliberately left it as "the user's call" —
  this is likely the same underlying item, not a new regression, but it remains unresolved in the
  file today and the specific curriculum-language framing doesn't appear to have been spelled out
  before.
- **`docs/README.md` claims content that doesn't exist.** It describes `docs/` as covering *"the
  teaching and testing method, future project ideas, and cross-cutting architecture decisions"* —
  a third thing no file in the folder actually covers, and the root `README.md`'s own tree comment
  describes this same folder with only two things. The two README files describing one folder
  disagree with each other.

**Notebook technical accuracy** (each verified by direct reproduction or against primary
documentation, not just read for plausibility)
- **Topic 1** (`/etc/.pwd.lock`, lines 104–105): states the file's mere presence signals an
  in-progress password edit. In reality it's a permanent lock *target* for `lckpwdf()`, present on
  essentially every Linux system at all times — presence alone means nothing; only an active
  advisory lock would.
- **Topic 2** (load average, lines 359–362): defines it as processes waiting for CPU only. Per
  `proc(5)`, load average counts both run-queue (R, CPU-wait) *and* uninterruptible-sleep (D,
  I/O-wait) processes — the omission erases the classic "high load, idle CPU" I/O-bottleneck
  scenario, a standard interview follow-up.
- **Topic 2** (lines 11–16 vs. its own Day 2): the Day 1 intro names `ps`/`top`/`kill`/`ss` as
  examples of tools *not* covered in this topic — then teaches all four, with full hands-on
  detail, later in the same file's Day 2.
- **Topic 3** (Day 2 heading, line 225): the heading says the quiz was "deferred on functions," but
  the file's own body shows it was re-taught and re-passed the *same session*, and Topic 3 is
  listed everywhere else as fully "Cleared" — never in the repo's distinct, formally-defined
  Deferred Mastery table. The wording risks colliding with that formal term.
- **Topic 4** (line 96–97): claims `df` reads `/proc` the same way `ps`/`top`/`free` do. `df`'s
  usage stats come from `statfs()`/`statvfs()` against the mounted filesystem directly, not from a
  `/proc` read the way the others work.
- **Topic 5** (lines 327–330, 445–453 — an official quiz answer): states that a `refused`
  response universally rules out a firewall in the path. That's only true of a silently-*dropping*
  firewall; a `REJECT`-configured one (common, not just DROP-by-default cloud security groups)
  also sends an active refusal, indistinguishable from "nothing listening."
- **Topic 7** (lines 59–63): claims `-graph` (single-dash) decomposes into a short-flag cluster
  `-g -r -a -p -h`, the same mechanism proven for `-all`. Reproduced directly: `git log --oneline
  -graph` in isolation returns `fatal: unrecognized argument: -graph` — it never actually reaches
  that decomposition; the combined command's real error aborts on `-all` first, so the `-graph`
  claim was never actually tested.
- **Topic 7** (line 143, inside a section literally titled "Verified hands-on"): a rebase-continue
  commit is captured as `1 file changed, 4 insertions(+)`. Reproducing the exact described
  resolution (keep both lines via "Accept Both Changes") gives `1 insertion(+)` — the only count
  the described scenario supports.
- **Topic 9** (lines 286–288, 317–319): the Windows host path is given as
  `C:\CloudOps\ignite\project\app\` — the folder is `orbit\app\` everywhere else in the repo,
  including the very same sentence's own `cd orbit/app` command.
- **Topic 9** (lines 387–399): a `docker logs` timestamp lands a full calendar day past the Day
  1 heading's date, with no note anywhere in the file explaining raw output can show the
  machine's real clock rather than the narrative's IST dates (the repo's own standing rule
  requires this note once per file; six of the eleven notebooks — Topics 1, 2, 4, 6, 7, 9 — are
  missing it entirely).
- **Topic 10** (lines 226–271): Day 2 states containers `app-a` and `app-b` already have specific
  bind mounts / volumes, and shows "verified" `docker inspect` output confirming it — but Day 1's
  own record creates both containers bare, with no mount, and the actual mount demonstration in
  Day 1 was on a separate, distinctly-named container (`app-c`). No command anywhere shows `app-a`
  or `app-b` actually acquiring these mounts.
- **Topic 11** (H1, line 1): titled "...Best Practices" with an ampersand; the fixed topic-name
  list spells it "...Best Practices" with the word "and" — a topic-name exact-wording violation.
- **Topic 11 / `orbit/docker-compose.yml`**: the notebook's "combined scenario" addresses the
  container throughout as `orbit-app-1` (the Compose-default auto-generated name), but the real,
  current `docker-compose.yml` sets `container_name: orbit-app` explicitly — so the actual
  container is named `orbit-app`, with no numeric suffix. Re-running the notebook's exact commands
  against today's file would fail with "No such container: orbit-app-1." This is a fresh instance
  of the same class of problem `public-readiness.md`'s H-15/H-16 already found and considered
  resolved elsewhere in this same file.

**`field_atlas.md` currency** (see the dedicated section below — summarized here as findings)
- The FinOps statistic (63% tracking AI spend) is a full report-cycle stale: the FinOps
  Foundation's newer *State of FinOps 2026* report (published Feb 2026, before this file's own
  last fact-check date) reports 98%.
- The Terraform-vs-OpenTofu section never mentions IBM's completed ~$6.4B acquisition of
  HashiCorp (closed February 2025) — arguably the single biggest structural fact behind the
  adoption trend the section is trying to describe.
- **AgentOps** — operating/governing autonomous AI agents in production, distinct from AIOps — has
  real 2026 survey backing (LangChain's State of Agent Engineering report, a Futurum Group
  enterprise survey) and isn't listed anywhere in §1.5, including the "emerging" tier.
- The GreenOps entry's "confidence: low that this has crystallized" is now dated: the Green
  Software Foundation's SCI spec became an accredited ISO standard (ISO/IEC 21031:2024) and gained
  a follow-on framework in late 2025 — comparable institutional weight to several already-listed
  entries.

---

## Minor

Grouped by theme rather than listed individually — each recurs across several files rather than
being a one-off.

- **Notebook filename slugging is systemically inconsistent.** `CLAUDE.md`'s stated rule requires
  both the topic's title and subtitle in the filename. Topic 1 keeps only the title; Topics 2, 3,
  4, 6, 7, 8 each keep only one half (inconsistently, not the same half every time); only Topics 5,
  9, 10, 11 comply with both halves. This is a repo-wide pattern, not an isolated slip in any one
  file — worth resolving once, either by renaming all eight non-compliant notebooks or by amending
  the stated rule to match the abbreviated convention actually in use everywhere going forward.
- ~~The required "raw output may show the machine's local clock, not IST" note is missing from
  most notebooks that need it~~ — **decided against, 2026-08-31**: added to Topics 1, 2, 4, 6, 7,
  and 9, then explicitly reverted per direct feedback that these notes aren't wanted in the
  notebooks. `CLAUDE.md`'s and `engine/CLAUDE.template.md`'s Dates rules were both amended the
  same day to drop the "worth a one-line note" clause entirely — this is now a closed decision,
  not an unaddressed gap, in both the real rules and the fork template. A future audit shouldn't
  re-raise this.
- **The "Syntax: line before the concrete example" rule has scattered gaps** — `cat`/`pwd`/`seq`
  (Topic 1/2), `sed`/`chmod +x` (Topic 4), `git branch -D/-d`/`git reset --hard` (Topic 8), `docker
  exec` used 9 times with no Syntax line ever given (Topic 10), and `HEALTHCHECK`/`COPY
  --chown=`/`docker start -a` (Topic 11). Not universal misses — most commands in every file do
  get the line — just inconsistent application worth a pass once notebooks stop being written
  and only need a formatting sweep.
- **`orbit/` minor accuracy nits**: `orbit/docs/concept.md` groups EC2/S3 with IAM/Lambda as
  uniformly "genuinely free," but EC2/S3's free tier is limited to a new account's first 12
  months, unlike IAM/Lambda; `orbit/scripts/README.md` ties "general shell utilities" to Phase 5
  even though shell scripting was already taught in Topic 3 (Phase 1) with no roadmap reason to
  wait.
- **A few small, verified technical overstatements**: Topic 1's `mysql -p` example doesn't
  actually reach `.bash_history` the way described (only the space-less inline form does); Topic
  5's private/public IP heuristic omits a few other reserved ranges (link-local, multicast, CGNAT)
  while explicitly framing itself as covering exceptions; Topic 11's "effectively existed twice"
  claim about the venv duplication bug doesn't reconcile with its own measured 27MB delta (a
  ~50MB venv would produce ~50MB, not 27MB); Topic 11's "no compile step, ever" for `python app.py`
  overstates it — CPython always compiles to bytecode, just not ahead-of-time to a standalone
  binary.
- **`field_atlas.md` refresh opportunities below the "stale/wrong" bar**: the FinOps bullet
  paraphrases its source as "tracking AI-specific cloud spend" where the report's actual wording is
  "managing AI spend" (a real but small difference); OpenTofu's CNCF status is stated without
  noting it's still Sandbox-tier, not Incubating; the GitOps adoption figure now has a better
  primary source available (CNCF's own July 2025 announcement) than the secondary-source hedge
  currently used.
- **A carryover from `public-readiness.md`'s M-tier that's still present**: `session_notes.md`'s
  Session 1 entry and `progress.md`'s Session 1 Check-in note both still name a "night-shift"
  personal-schedule detail, which that audit recommended removing or reframing as neutral. Not
  re-litigated here as a fresh finding — flagged only because it's still live, unlike most of that
  audit's other M-tier items.

## Cosmetic

- Topic 8's quiz answer restates a mitigation using `@latest` as its floating-tag example where
  the body text (and the actual GitHub Actions ecosystem) uses `@v4`/`@main` — `@latest` is a
  Docker/npm convention, not one Actions pins against.
- `repo-organization.md` describes its own header addition to `topic-10-professionalism.md` as "a one-line
  note"; the actual insertion is a 5-line blockquote.
- Placeholder `README.md` files under `orbit/`'s not-yet-built folders (nine of them, plus
  `app/tests/`) are single untitled paragraphs, while every folder with real content opens with an
  H1 — a consistent split, but one nobody's documented as intentional.
- `engine/MISSION.template.md`'s own instructional comment says "two example rows are shown" where
  three actually are.

---

## `field_atlas.md` — currency check and the anti-drift mechanism

### What's actually still true, and what's drifted

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

### Why it went stale, and why that's not a one-off

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

### A concrete mechanism, not just a flag

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

### What was actually built (2026-08-31), and where it departed from the proposal above

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

### Follow-up, 2026-09-21 — the backstop's first real test, and a defect in it

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

---

## Prior-audit status check

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

---

## Verified clean — negative results

- **No secrets or credentials anywhere, on any ref.** Re-verified independently this audit: zero
  matches across `main`, `origin/main`, and `personal/main`'s full history for AWS key prefixes,
  private-key headers, GitHub/Slack tokens, or password/secret/token assignments with real values.
- **No broken internal links.** 28 local Markdown links checked programmatically across all 50
  Markdown files in the repo — zero broken.
- **All 11 notebook `Verdict` lines present and correctly formatted** — checked mechanically
  against every notebook.
- **Topic naming is exact and consistent** across `roadmap.md`, `progress.md`,
  `handbook_status.md`, and all 11 notebook H1 titles (one single exception: Topic 11's "&" vs.
  "and," listed under Important) — checked directly, character for character.
- **The redaction convention is genuinely followed in captured output** — spot-checked
  `devuser`/`devuser` placeholders in Topic 1's filesystem listings; consistent with
  `CONTRIBUTING.md`'s stated convention.
- **The public-readiness audit's own required raw-copy rule was followed** — `public-readiness.md`
  did produce and preserve an unredacted external copy under `C:\CloudOps`, as its own redaction
  note promises; `repo-organization.md` correctly stated no such copy was needed and said so
  explicitly, matching the standing rule.
- **`orbit/app/`'s code and Dockerfile carry no debugging or teaching-style comments**, and no
  reference to `CLAUDE.md` — the interview-facing-folder rule is genuinely held to in the code
  itself (the violations found are in prose files, not code).
- **Every placeholder README under `orbit/`'s not-yet-built folders correctly names its populating
  topic**, cross-checked against `roadmap.md`'s real topic numbers — including
  `.github/workflows/README.md`'s Topic 15/16 framing.

---

## Recommended sequence (not applied — for your review)

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

---

## Resolved since this report was first written

Critical Finding 2 (B-1) was answered directly on 2026-08-31: this is a self-created personal
learning project, not employer work, so no written employer confirmation is needed. See the
resolution note under Critical Finding 2 above — that note, not this section, is the durable
record for any future audit.
