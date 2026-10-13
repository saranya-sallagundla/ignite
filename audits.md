# Repo audits

One file: the index, what is still open, what is settled, each audit's record with its findings
one row each, and the prompts to start the next audit. Each finding keeps its ID, severity and
status. The full original write-ups are in git history.

## Index

The source of truth for which audit covers which milestone — check it before assuming an audit
has or hasn't run for a given topic.

| Date | Type | Milestone | Prefix | Findings |
|---|---|---|---|---|
| 2026-10-03 | Periodic professionalism audit | after Topic 10 | `T10-` | 12 |
| 2026-10-04 | Public-readiness audit (one-time) | repo already public, pre-remediation | `PR-` | 35 |
| 2026-10-10 | Repo organization audit (one-time) | not tied to a topic milestone | `RO-` | 21 |
| 2026-10-11 | Final sign-off audit (one-time) | pre-fork, public-facing review | `FS-` | 44 |

Two kinds of audit, same rules: **periodic** ones every 10 topics (after Topic 10, 20, 30, 40, 50
clear) and once more after Topic 53; **one-time** ones with a named trigger — visibility changing,
a direct request for an organization pass, or a final sign-off before the repo is pointed to
publicly.

## Open items

| ID | Item | Status |
|---|---|---|
| FS-1 | The public mirror (`personal`) is still the pre-remediation snapshot: original history with the corporate identity on ~35 commits, `claude-memory/` present, no LICENSE, SECURITY or CONTRIBUTING. Covers PR-C-1 to C-6 and PR-H-5. | open — last updated 2026-10-02 (checked 2026-10-12) |
| FS-5 | The git-metadata exemption that allowed FS-1 is still in `rules.md` §7 | partly done — repo-local identity set to a personal no-reply address |
| PR-H-7 | `.gitignore` has no credential patterns (`*.tfvars`, `*.pem`, `.aws/`, `kubeconfig*`, `.env.*`); `env/` is unanchored | open — must land before Phase 3 (checked 2026-10-12) |
| PR-H-8 | `USER appuser` is non-numeric; `runAsNonRoot` can't resolve it | open — `progress.md` Open items #3, Topic 13 |
| PR-H-11 | No CI and no tests in a repo that teaches CI/CD | held for Topic 15 |

## Settled — do not re-raise

- **Ownership and the right to publish** (PR-B-1, FS-2): closed 2026-10-11. This is a self-created
  personal learning project, not employer work; no employer confirmation is needed. This note is
  the durable record, not memory.
- **The local-clock note in notebooks** (FS-m-2, FS-I-20): decided against 2026-10-11; the rule
  was amended the same day.
- **`container_name: orbit-app`** (RO-2.4, PR-H-15): kept, since dropping it would break captured
  `docker exec` commands.
- **British and American spelling, and the `concept.md` reword** (RO-3.5): the user's call, not
  made.
- **Historical notebooks** (RO-5.4): no retroactive changes to captured sessions; style
  conventions are forward-only from Topic 12.
- **A Windows Task Scheduler fallback for the atlas check** (FS-A): rejected on purpose; output
  nobody opens isn't a notification.

## Periodic professionalism audit — 2026-10-03 (`T10-`)

Trigger: Topic 10 cleared. It ran after Topic 11 cleared on 2026-10-02; "after Topic 10"
describes its scope, the repo as it stood once Topic 10 cleared, not calendar order. Scope: every
file, all 10 notebooks, `orbit/`, git hygiene; 17 review agents. Result: 4 critical, about 30
important, a long tail of minor and cosmetic items; all reviewed first, then fixed in 8 committed
batches.

| ID | Finding | Severity | Status |
|---|---|---|---|
| T10-1.1 | Employer org name in `orbit/docs/concept.md` | critical | fixed 2026-10-03 |
| T10-1.2 | `orbit/README.md` said there was nothing to run, contradicting its own Status section | critical | fixed 2026-10-03 |
| T10-1.3 | Topic 3 notebook taught a bash `else` syntax rule backwards | critical | fixed 2026-10-03 |
| T10-1.4 | An unescaped backtick broke Topic 7's rendering on GitHub | critical | fixed 2026-10-03 |
| T10-2 | No `.gitignore`, `.gitattributes` or `orbit/app/.dockerignore`; the README tree missed a file | — | fixed 2026-10-03 |
| T10-3 | `orbit/` polish: generic title, scaffolding language, teaching comments and a leftover demo service in Compose, odd framing in `concept.md`, uneven placeholder READMEs | — | fixed 2026-10-03 |
| T10-4 | Topic names spelled three ways across tracking files; a self-contradictory `:latest` claim; a quiz-cap rule contradicted by logged overruns | — | fixed 2026-10-03 |
| T10-5 | Technical errors in notebooks: SSH key auth called challenge-based (it is signature-based), fstab read by "the kernel" (it is systemd), a "No route to host" blamed on a router (local ARP failure), Actions secrets "always appear in logs" (they are masked) | — | fixed 2026-10-03 |
| T10-6 | Cosmetic sweep: wording, punctuation, mislabeled fences, trailing newlines | cosmetic | fixed 2026-10-03 |
| T10-7 | Dockerfile and Compose gaps: root user, dev server, no `EXPOSE` or `HEALTHCHECK`, no `--no-cache-dir`, no `PYTHONUNBUFFERED`, untagged image, Flask pin behind a patch | — | held for Topic 11 — fixed there (confirmed by PR and FS) |
| T10-8 | Session and Day headings normalized to the start date only; local-clock note added; check-in/out lines untouched | — | fixed 2026-10-03 |
| T10-9 | Topic 9 and 10 Day headings lacked content summaries; Topic 10's H1 missed the em-dash pass | — | fixed 2026-10-03 |

## Public-readiness audit — 2026-10-04 (`PR-`)

Trigger: the repo turned out to be public already. Scope: 41 tracked files, 60 commits on all
refs, git internals, live GitHub state. Result: no secrets anywhere; every blocking problem is
identity, not quality; the employer-name redaction was applied to the working tree but never to
git history. Findings only; the fixes came in later sessions. This record names no leaked string
and no commit where one lived.

| ID | Finding | Severity | Status |
|---|---|---|---|
| PR-B-1 | The right to publish was unresolved: work laptop, corporate org, corporate identity on every commit | blocking | closed 2026-10-11 (FS-2) |
| PR-C-1 | The repo is already public: `private: false`, no licence, 0 stars, 0 forks, last pushed 2026-10-02 | critical | open — the public mirror is still the old copy (FS-1) |
| PR-C-2 | Corporate email and legal name on all 60 commits, publicly readable; none signed | critical | fixed on `origin` 2026-10-04; mirror still old (FS-1) |
| PR-C-3 | Employer email in git-history file content (pasted `git log` output in one notebook) | critical | fixed on `origin` 2026-10-04; mirror still old (FS-1) |
| PR-C-4 | Employer org name in git-history file content (the pre-rename path of `concept.md`) | critical | fixed on `origin` 2026-10-04; mirror still old (FS-1) |
| PR-C-5 | The repo signposted its own leak: the audit file, the rules and the memory files all said an employer name was being redacted | critical | fixed on `origin` 2026-10-04; mirror still old (FS-1) |
| PR-C-6 | The `claude-memory/` sync rule mandated copying memory files that hold the employer name in plain text | critical | fixed on `origin` 2026-10-04 (folder removed); mirror still old (FS-1) |
| PR-C-7 | Pacing Layer not updated after Session 17; five files disagreed about "now" | critical | fixed — Pacing Layer updated (last on 2026-10-09) |
| PR-H-1 | Corporate user ID 55 times in the working tree, with symlinks revealing cloud credential paths | high | fixed — placeholders confirmed by FS 2026-10-11 |
| PR-H-2 | Full legal name left in Topic 6 notebook content | high | not re-checked since |
| PR-H-3 | Five notebooks together map the employer's egress controls | high | not re-checked since |
| PR-H-4 | `orbit/docs/concept.md` stated the employer relationship | high | not re-checked since |
| PR-H-5 | `claude-memory/` was an AI behavioural dossier on a named person | high | fixed on `origin` 2026-10-04; mirror still old (FS-1) |
| PR-H-6 | No LICENSE | high | fixed — MIT at the root, CC BY 4.0 for written material (confirmed by FS) |
| PR-H-7 | `.gitignore` has no credential patterns; `env/` unanchored | high | open — see Open items |
| PR-H-8 | `USER appuser` is non-numeric | high | open — see Open items |
| PR-H-9 | README told readers `learning/` was "not meant to be shown to anyone" and `orbit/` "not yet something to defend" | high | fixed (confirmed by FS) |
| PR-H-10 | Scores presented as objective measurement, no provenance label | high | fixed — relabelled self-assessed, AI-graded (confirmed by FS) |
| PR-H-11 | Zero CI and zero tests | high | held for Topic 15 |
| PR-H-12 | Captured output edited after the `project/` → `orbit/` rename while prose was left stale | high | not re-checked since |
| PR-H-13 | 12 topic names in non-baseline spelling in `orbit/README.md` | high | fixed 2026-10-10 (RO-2.2) |
| PR-H-14 | A stray code fence broke ~100 lines of Topic 8's rendering | high | fixed 2026-10-10 (RO-1.1) |
| PR-H-15 | `container_name: orbit-app` breaks ~10 captured `docker exec` commands | high | left as is on purpose (RO-2.4) |
| PR-H-16 | Notebooks 10 and 11 document incompatible Compose files; the deletion is recorded nowhere | high | not re-checked since |
| PR-H-17–19 | `orbit/` docs contradicted reality and each other: placeholders, a vanished second service, AWS and Helm against k3s and LocalStack | high | fixed 2026-10-10 (RO-2.2) |
| PR-M-1 | Disclosure: an org tooling restriction, a real production alert, a shift rota, NAT addresses, a personal-site link | medium | not re-checked since |
| PR-M-2 | Candour: frustration and weakness lists published verbatim; needs a deliberate decision | medium | not re-checked since |
| PR-M-3 | Sourcing: an unsourced claim about a named firm in the atlas; no hyperlinks; no confidence legend | medium | not re-checked since |
| PR-M-4 | Community files absent (`CONTRIBUTING.md`, `SECURITY.md`, PR template) | medium | fixed (confirmed by FS) |
| PR-M-5 | Container and supply chain: no Compose hardening, port on all interfaces, floating transitive deps, floating base image, gunicorn with no request log, version hardcoded in four places | medium | not re-checked since |
| PR-M-6 | Framing: `orbit/` can't yet carry "Capstone"; its README was 90 lines of diary | medium | not re-checked since |
| PR-M-7 | Consistency and arithmetic: gap-day count, mixed pacing bases, audit-trigger phrasing bug, verdict-line drift, Syntax-line gaps, Current status grown to six lines, 231 → 204 MB against a 199 MB single-stage image | medium | not re-checked since |
| PR-M-8 | Technical claims to correct: load average (R and D), a "No route to host" row, Git Flow history, cherry-pick detection, `--target` and build cache, `pip` and gcc on slim, and others | medium | not re-checked since |
| PR-L-1 | Low: local path disclosure, disk UUIDs, a recoverable deleted screenshot (benign), HEALTHCHECK `--start-period`, no security headers, no topics or tags, inconsistent slugs, no audit after Topic 53 | low | not re-checked since |
| PR-R | Rule changes recommended: drop the git-metadata exemption; delete the memory sync rule; fix the audit trigger; add a Topic 53 audit; date the raw reports; never edit captured output | — | 2, 3, 4, 6 done; 5 no longer applies; 1 open (FS-5) |

Verified clean: no secrets or credentials in the tree or in history on any ref; no
credential-bearing file type ever committed; employer name 0 in file content; one author identity;
git internals clean; no internal hostnames; `orbit/` code clean; original writing throughout; all 8
T10 deferrals resolved in Topic 11; score arithmetic correct across four files; all 53 topic names
and day sums correct; zero broken links.

## Repo organization audit — 2026-10-10 (`RO-`)

Trigger: a direct request for a whole-repo consistency pass, not tied to a milestone. Scope: every
file including `engine/`, `docs/` and the audit records, plus a git-level sweep. Five auditors,
one slice each; fixes applied in five batches and written up after the fact. Result: 97 findings
(3 critical, 20 important, 40 minor, 34 cosmetic); all critical and important ones fixed; a few
left alone on purpose and listed as such.

| ID | Finding | Severity | Status |
|---|---|---|---|
| RO-1.1 | Stray code fence in Topic 8: odd fence count, a heading swallowed | critical | fixed 2026-10-10 |
| RO-1.2 | `progress.md`'s Current status had grown into a 6-line roster | critical | fixed 2026-10-10 |
| RO-1.3 | `orbit/README.md`'s Session 16 Compose claim no longer matched the file; true when written, so a removal note was added instead of a rewrite | critical | fixed 2026-10-10 |
| RO-1.4 | Leftovers from the `audits/` rename: old naming and the trigger bug still in the engine template; two rotted citations | — | fixed 2026-10-10 |
| RO-2.1 | Internal-scaffolding language in `orbit/` | — | fixed 2026-10-10 |
| RO-2.2 | `orbit/` accuracy: `argocd/` missing from the guide, a false "empty placeholder" claim, README and `concept.md` disagreeing on the stack, 17 topic names misspelled | — | fixed 2026-10-10 |
| RO-2.3 | `orbit/README.md` build log led with 12 "no project code yet" entries; collapsed, 130 → 77 lines | — | fixed 2026-10-10 |
| RO-2.4 | `container_name: orbit-app` | — | left as is on purpose |
| RO-3.1 | GitHub detected the LICENSE as "Other", not MIT, because of text added around it | — | fixed 2026-10-10 |
| RO-3.2 | Root prose files fell under neither licence | — | fixed 2026-10-10 (CC BY 4.0) |
| RO-3.3 | README, `.github/workflows/README.md` and `SECURITY.md` described CI that didn't exist | — | fixed 2026-10-10 |
| RO-3.4 | One name for the 3-attempt rule; numerals; `.gitattributes` covers `*.md`; two long lines | — | fixed 2026-10-10 |
| RO-3.5 | British and American spelling split; `concept.md` reword | — | left as is on purpose |
| RO-4.1 | Gap-day arithmetic in `roadmap.md`: one rule, 17 of 20 active days | — | fixed 2026-10-10 |
| RO-4.2 | Session 17 (2026-10-02) credits the Topic 10 audit, dated the day after; a header note explains "after Topic 10" is scope, not order; no date altered | — | fixed 2026-10-10 |
| RO-4.3 | Tracking-file structure: summary tables ahead of the log; one H1 in the atlas; "Topic state" | — | fixed 2026-10-10 |
| RO-4.4 | Two rules reworded to match real practice (one-line reasons, 2–4 line recaps) | — | fixed 2026-10-10 |
| RO-5.1 | Verdict-line and heading formats in notebooks; Topic 5's "official score" kept on purpose | — | fixed 2026-10-10 |
| RO-5.2 | Topic 9 missing blank lines after 21 headings | — | fixed 2026-10-10 |
| RO-5.3 | Intro blockquotes for Topics 5 and 6 now say they were one-session topics | — | fixed 2026-10-10 |
| RO-5.4 | Preamble order, Phase 2 labels, prompt style: no retroactive changes to captured sessions | — | left as is on purpose |

## Final sign-off audit — 2026-10-11 (`FS-`)

Trigger: a requested final review, as a senior reviewer deciding whether the repo can be pointed
to publicly and forked. Scope: every file including `engine/` and the three prior audits, plus the
live state of both GitHub remotes. Result: the private copy is in good shape; the public copy is a
different, older, unremediated snapshot, which is the single most important finding. Findings
only; the fixes followed in batches.

| ID | Finding | Severity | Status |
|---|---|---|---|
| FS-1 | The public mirror is still the pre-remediation snapshot (see Open items) | critical | open — checked 2026-10-12 |
| FS-2 | PR-B-1 still open per the repo's own record | critical | closed 2026-10-11 — personal project, no employer confirmation needed |
| FS-3 | `engine/` carried no licence grant at all | critical | fixed — now in the CC BY 4.0 grant |
| FS-4 | `QUICKSTART.md`'s default path has no remote, so the mandatory first push fails | critical | fixed — the Quickstart adds a remote first |
| FS-5 | The git-metadata exemption was never removed | critical | partly done — see Open items |
| FS-I-1 | The audit-trigger bug was fixed in the engine template but not in `CLAUDE.md` | important | fixed 2026-10-11; lost in the 2026-10-12 rules rewrite and restored in `rules.md` §8 the same day |
| FS-I-2 | `CLAUDE.md`'s Repo layout didn't describe most of the repo | important | superseded — `CLAUDE.md` is a loader; the layout lives in `README.md` |
| FS-I-3 | The audit index called the public-readiness audit "pre-publish" | important | fixed — the row reads "repo already public, pre-remediation" |
| FS-I-4 | Line-number citations into the T10 audit rotted after a header insert | important | fixed 2026-10-11 — citations de-lined |
| FS-I-5 | The RO record misdescribed how its fix batches were sequenced | important | fixed 2026-10-11 — header corrected |
| FS-I-6 | The LICENSE fix and the B-1 gate pointed opposite ways | important | closed — B-1 is closed (FS-2) |
| FS-I-7 | The T10 audit's stated agent count (14) didn't match its breakdown (17) | important | fixed — reads "17 review agents" |
| FS-I-8 | `orbit/README.md`'s Status misdescribed which topics are "later phases" | important | fixed — replaced by the Parts section 2026-10-12 |
| FS-I-9 | `orbit/docs/concept.md` reads as curriculum scaffolding | important | not re-checked since |
| FS-I-10 | `docs/README.md` claimed content that doesn't exist | important | superseded — `docs/README.md` deleted 2026-10-12 |
| FS-I-11 | Topic 1: `/etc/.pwd.lock`'s presence doesn't signal an in-progress edit | important | not re-checked since |
| FS-I-12 | Topic 2: load average counts R and D, not CPU-wait only | important | not re-checked since |
| FS-I-13 | Topic 2: Day 1 says `ps`/`top`/`kill`/`ss` aren't covered; Day 2 teaches them | important | not re-checked since |
| FS-I-14 | Topic 3: a "deferred on functions" heading collided with the formal Deferred Mastery term | important | fixed — says re-taught and re-passed the same session |
| FS-I-15 | Topic 4: `df` uses `statfs()`, not `/proc` | important | not re-checked since |
| FS-I-16 | Topic 5: "refused" doesn't rule out a `REJECT` firewall | important | not re-checked since |
| FS-I-17 | Topic 7: the `-graph` short-flag claim was never actually tested | important | not re-checked since |
| FS-I-18 | Topic 7: a rebase commit's insertion count can't match the described resolution | important | not re-checked since |
| FS-I-19 | Topic 9: Windows host path says `project\app\` where the folder is `orbit\app\` | important | not re-checked since |
| FS-I-20 | Topic 9: a `docker logs` timestamp a day past the heading, no local-clock note | important | closed — decided against (FS-m-2) |
| FS-I-21 | Topic 10: `app-a` and `app-b` shown with mounts Day 1 never gave them | important | addressed — editorial note added 2026-10-11 |
| FS-I-22 | Topic 11: H1 uses "&" where the baseline says "and" | important | fixed 2026-10-12 |
| FS-I-23 | Topic 11: commands address `orbit-app-1` while Compose names it `orbit-app` | important | addressed — note added 2026-10-11 |
| FS-I-24 | Atlas: FinOps statistic a report cycle stale (63% → 98%) | important | fixed — in the atlas (checked 2026-10-12) |
| FS-I-25 | Atlas: IBM's HashiCorp acquisition missing from the OpenTofu section | important | fixed — in the atlas |
| FS-I-26 | Atlas: AgentOps not listed | important | fixed — in the atlas |
| FS-I-27 | Atlas: GreenOps confidence dated (SCI is an ISO standard) | important | fixed — in the atlas |
| FS-A | Atlas currency had one trigger, a teaching session opening, so it could go stale unnoticed. Built: an every-session check in the rules (recompute the Calendar Day; test the written data, not the `Pace` verdict) plus the scheduled task `ignite-field-atlas-check` on the 1st and 15th. Its unattended run then stalled on a permission prompt while reporting "succeeded"; fixed by approving the prompts once, and by the rule that a run's status is not evidence, verify by output | — | mechanism built 2026-10-11; stall defect fixed 2026-10-12 |
| FS-m-1 | Notebook filename slugging inconsistent | minor | fixed 2026-10-11 — notebooks renamed |
| FS-m-2 | Local-clock note missing from most notebooks | minor | closed — decided against 2026-10-11; rule amended |
| FS-m-3 | Syntax-line rule gaps (`cat`, `sed`, `docker exec`, `HEALTHCHECK` and others) | minor | not re-checked since |
| FS-m-4 | `orbit/` nits: EC2/S3 free tier is 12 months only; `scripts/` tied to Phase 5 for no reason | minor | not re-checked since |
| FS-m-5 | Small overstatements: `mysql -p` and history, reserved IP ranges, "existed twice" against a 27 MB delta, "no compile step" | minor | not re-checked since |
| FS-m-6 | Atlas refresh opportunities below the stale bar: FinOps wording, Sandbox tier, the CNCF primary source | minor | fixed — in the atlas (checked 2026-10-12) |
| FS-m-7 | Night-shift schedule detail still present | minor | fixed 2026-10-12 — note shortened; `session_notes.md` removed |
| FS-c-1 | Topic 8 quiz uses `@latest` as an Actions example | cosmetic | not re-checked since |
| FS-c-2 | The RO record called a 5-line note "one-line" | cosmetic | fixed |
| FS-c-3 | Placeholder READMEs had no H1 | cosmetic | superseded — placeholders removed 2026-10-12 |
| FS-c-4 | `MISSION.template.md` says two example rows, shows three | cosmetic | not re-checked since |

Verified clean: no secrets on any ref; the redaction convention is followed in captured output; the
public-readiness audit's raw-copy rule was followed; all 8 T10 deferrals resolved; PR-H-6, H-9,
H-14 and the community files resolved; the RO batches hold up on re-check; `orbit/app/` code has no
teaching comments; placeholder READMEs name their topics; no broken links across 50 Markdown
files; all 11 Verdict lines correct; topic naming exact (one exception, FS-I-22).

## Running the next audit

The process — findings before fixes, severity triage, batched commits, deferring topic-specific
items, indexing the result — lives in [`rules.md`](rules.md) §8. Two things worth repeating
at the point of use, because both have been gotten wrong before:

- **Audit fresh, every time.** The tables above record what each audit surfaced. They are not a
  checklist a later audit is confined to re-checking. Look at the repo word by word and add
  whatever actually turns up.
- **Each audit also re-checks the standing rules** in `rules.md` §7, not only new issues.

### Saving a new audit

1. Pick a short ID prefix (e.g. `T20-` for the Topic 20 audit) and add a row to the Index.
2. Add its section above: trigger, scope and result in a few lines, then a findings table in the
   same shape, one row per finding.
3. Update the Status of any older finding the new audit re-checked instead of repeating it, and
   move items between Open items and Settled as needed.

### Prompts

Each prompt is meant to be reused verbatim next time that kind of audit is due.

**The next periodic audit**

> Check if the whole repo can be maintained even more professionally — check each and every
> subfolder and subfile, word by word, line by line and sentence by sentence, and let me know what
> else we can do. Tell me everything, even if it feels like a minute thing, it matters when
> showing the whole repo to higher officials. Save the audit findings and fixes to `audits.md`, and
> don't apply any fixes until I review the findings first.

**The next public-readiness audit**

> Before this repo's visibility changes again, or as a periodic re-check since exposure and
> novelty both decay: check every file, every commit — not just the working tree — and the live
> GitHub state, for anything that shouldn't be public: secrets, credentials, personal
> identifiers, employer references, or claims the repo can't actually back, such as a license it
> doesn't hold clear rights to grant. Verify against GitHub's API directly rather than trusting
> local files. Save findings to `audits.md`, and don't apply any fixes until I review them.

**The next repo organization audit**

> Check the whole repo and tell me if it could look more organized — as if you have OCD and want
> everything consistent: file naming, formatting, structure, and any claim that doesn't match
> reality, however small. Not tied to a topic milestone. Save findings to `audits.md`, and don't
> apply any fixes until I review them.

**The next final sign-off audit**

> Act as a senior software architect with 30+ years at top tech companies. You are meticulous,
> skeptical, and known for catching the smallest gap everyone else misses. This repo has been
> submitted to you for final sign-off before it's released publicly / pointed to for others to
> fork. Read every file, every subfolder, every notebook, word by word — including the pre-build
> material (`rules.md`/`CLAUDE.md`/`MISSION.md`/`engine/` and anything a fork would rely on) — and check it
> for accuracy, internal consistency, and whether it's usable by someone with no prior context.
> Verify the live state of every git remote, not just the one currently being worked from —
> a clean local/private copy doesn't mean the actual public destination is clean. Check the
> field atlas (or the mission's equivalent living reference, if it has one) for currency, and
> propose a concrete, repeatable mechanism for keeping it current going forward, not just a note
> that it could drift. Save findings to `audits.md`, and don't apply any fixes until I review them.
