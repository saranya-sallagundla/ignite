# Privacy and publishing

Is it safe to make public? Identity in files and git history, the public mirror, secrets, licences, and the right to publish.

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

### T10-1.1 — Employer org name in `orbit/docs/concept.md`
> From: Topic 10 professionalism audit, 2026-07-27 · Original section: Batch 1 — Critical (4 items) · Severity: critical · Status: fixed 2026-07-27

1. **Employer org name in `orbit/docs/concept.md`** — the actual employer name appeared directly
   in file content (as part of a GitHub org reference). *Why it matters*: house rule (now in `CLAUDE.md`) forbids the employer name in
   any file content, in any casing — this is the one rule with zero tolerance, since it's the
   difference between a personal project and an accidental leak of employer affiliation.

### PR-B-1 — The right to publish is unresolved
> From: Public-readiness audit, 2026-08-13 · Original section: B — BLOCKING (resolve before anything else) · Severity: blocking · Status: closed 2026-08-31 (FS-2)

`orbit/docs/concept.md:37` states the work was built on a work laptop, not a personal one; `:43-44`
states the repo lives under a corporate GitHub org accessed via a corporate-provisioned identity.
All 60 commits are authored under a corporate identity.

A LICENSE file is an affirmative assertion that you hold the copyright and are granting rights. If
an employment agreement assigns IP created on company equipment or systems, that grant cannot be
made. **Publishing a licence you cannot back is worse than publishing none** — no licence is
ambiguity, a false licence is a misrepresentation every forker relies on.

This is not a legal opinion and must not be treated as one. Action: obtain **written** confirmation
through the employer's open-source-contribution process. Move future work to personal hardware and a
personal git identity regardless.

**Nothing in the H tier below is worth doing until B-1 is answered.**

### PR-C-1 — The repo is already public
> From: Public-readiness audit, 2026-08-13 · Original section: C — CRITICAL · Severity: critical · Status: open — the public mirror is still the old copy (FS-1)

| # | Finding |
|---|---|
| **C-1** | **The repo is already public.** Verified via unauthenticated API: `private: false`, `license: null`, 0 stars, 0 forks, created 2026-07-03, last pushed 2026-07-31. The corporate-org copy correctly returns 404 unauthenticated. The 0/0 count is the only good news and it is time-limited. |

### PR-C-2 — Corporate email and legal name on all 60 commits
> From: Public-readiness audit, 2026-08-13 · Original section: C — CRITICAL · Severity: critical · Status: fixed on the org repo 2026-08-13; the public mirror still has the old history (FS-1)

| # | Finding |
|---|---|
| **C-2** | **Corporate work email + full legal name on all 60 commits**, author *and* committer fields, confirmed **publicly readable** via the unauthenticated commits API. No repo-local `user.email` override, so every future commit keeps adding it. **Zero commits are signed.** `CLAUDE.md:136-137` exempts git metadata — that exemption was correct for a private repo and is now the single largest exposure. |

### PR-C-3 — Employer email in git history file content
> From: Public-readiness audit, 2026-08-13 · Original section: C — CRITICAL · Severity: critical · Status: fixed on the org repo 2026-08-13; the public mirror still has the old history (FS-1)

| # | Finding |
|---|---|
| **C-3** | **The employer email is in git history file content**, inside pasted `git log` output in one notebook — 6 occurrences, added in two commits and removed in a later one. HEAD is clean, so it reads as fixed until history is checked. |

### PR-C-4 — Employer org name in git history file content
> From: Public-readiness audit, 2026-08-13 · Original section: C — CRITICAL · Severity: critical · Status: fixed on the org repo 2026-08-13; the public mirror still has the old history (FS-1)

| # | Finding |
|---|---|
| **C-4** | **The employer org name is in git history file content**, in the pre-rename path of `orbit/docs/concept.md`, removed by the Topic 10 audit's own critical-fix commit. |

### PR-C-5 — The repo publishes a signpost to its own leak
> From: Public-readiness audit, 2026-08-13 · Original section: C — CRITICAL · Severity: critical · Status: fixed on the org repo 2026-08-13; the public mirror still has the old history (FS-1)

| # | Finding |
|---|---|
| **C-5** | **The repo publishes a signpost to its own leak.** `topic-10-professionalism.md`'s own opening summary and its Batch 1 first critical item record that the employer name appeared in file content and name the file *(citation de-lined 2026-08-31 after the original line numbers rotted once — see that audit's own note on this)*. `CLAUDE.md`'s employer-name rule, `claude-memory/MEMORY.md:4` and two `claude-memory/` files all state that an employer name is being deliberately redacted. `CLAUDE.md`'s periodic-audit raw-copy rule + `audits/README.md`'s own raw-copy rule further document that an **unredacted** copy is retained outside the repo. Rewording is cosmetic — only the history purge fixes this. |

### PR-C-6 — The `claude-memory/` sync rule
> From: Public-readiness audit, 2026-08-13 · Original section: C — CRITICAL · Severity: critical · Status: fixed on the org repo 2026-08-13; the public mirror still has the old history (FS-1)

| # | Finding |
|---|---|
| **C-6** | **The `claude-memory/` sync rule is a live time bomb.** `claude-memory/README.md:9-10` and `project_ignite_learning_mission.md:21` mandate copying **every** ignite-related memory file into this repo "in the same turn." Verified against the live memory directory: it holds **20 files**; `claude-memory/` holds **5**. **Three of the unsynced files contain the employer org name in plain text** (12 occurrences total; the file whose subject *is* employer-name redaction contains it eight times). If that rule is ever followed correctly, the name lands in a public repo. `CLAUDE.md:136-138` calls this "the one rule with zero tolerance" — and another standing rule in the same repo mandates violating it. **Do not "fix the sync."** Remove the folder. |
**C-6 note, for the record.** This session created two new memory files and did **not** copy them
into `claude-memory/` — i.e. did not follow the sync rule. That omission is the only reason no new
leak occurred this session.

### PR-H-1 — Corporate user ID in the working tree
> From: Public-readiness audit, 2026-08-13 · Original section: H — HIGH · **Identity and disclosure** · Severity: high · Status: fixed — placeholders confirmed by FS, 2026-08-31

- **H-1. The corporate user ID appears 55 times in the working tree** — 38 in topic-01, 8 in topic-02, 5 in topic-04, 2 in topic-09, plus 2 in `claude-memory/`. Most consequential, `topic-01:45-46` shows symlinks revealing that both AWS and Azure credential directories exist on the machine at a known path. Paired with C-2 this maps a named individual to a corporate account namespace. Also present in history — needs the same rewrite pass. Replace with a neutral username.

### PR-H-2 — Full legal name left in notebook content
> From: Public-readiness audit, 2026-08-13 · Original section: H — HIGH · **Identity and disclosure** · Severity: high · Status: not re-checked since

- **H-2. The full legal name was left in notebook content** at `topic-06:63,158,164,242,248,254`. The **email on those exact lines was sanitised** to a placeholder; the name was not. The `Surname, Given Middle` rendering is a corporate-directory form, which is itself a tell.

### PR-H-3 — Notebooks map the employer's egress controls
> From: Public-readiness audit, 2026-08-13 · Original section: H — HIGH · **Identity and disclosure** · Severity: high · Status: not re-checked since

- **H-3. Five notebooks together publish a working map of the employer's egress controls.** `topic-01:341-392` (proxy state, WPAD auto-detect, and the conclusion that the control is a network-level firewall/DPI appliance filtering non-browser traffic differently from browser TLS); `topic-02:377-390,437,506-511` (ICMP permitted, direct TCP 80/443 blocked); `topic-04:250-253` (outbound NTP blocked); `topic-05:185-194` (allowlist granularity, with the text noting the block is "more surgical than a blanket block"); `topic-10:99-106` (VPN vs `docker network create`, "a known failure mode on this network"). Individually harmless; collectively this describes one identifiable employer's security posture, and C-2/C-3/C-4 make it identifiable. **Keep the lesson, drop the specific allow/deny findings.**

### PR-H-4 — `orbit/docs/concept.md` states the employer relationship
> From: Public-readiness audit, 2026-08-13 · Original section: H — HIGH · **Identity and disclosure** · Severity: high · Status: not re-checked since

- **H-4. `orbit/docs/concept.md` states the employer relationship in plain language** — in the interview-facing folder. Delete the environment/portability paragraph; keep the architecture.

### PR-H-5 — `claude-memory/` is a behavioural dossier
> From: Public-readiness audit, 2026-08-13 · Original section: H — HIGH · **Identity and disclosure** · Severity: high · Status: fixed on the org repo 2026-08-13; the public mirror still has the old history (FS-1)

- **H-5. `claude-memory/` is an AI behavioural dossier on a named person.** It contains the corporate Windows profile path, three internal session UUIDs, verbatim quotes of the user's own self-assessments including two phrases that characterise the learner in terms no public repo should carry, and four separate statements that an employer name is being hidden. The pitch is "fork my method"; this ships a clinical characterisation of a named individual alongside it. Readers will not infer transparency — they will infer the author did not know what was in their own repo. **Remove from the repo and from history.** If the methodology should be public, hand-write `docs/METHOD.md` in third person with no assessments of the learner.

### PR-H-6 — No LICENSE
> From: Public-readiness audit, 2026-08-13 · Original section: H — HIGH · **Legal and community** · Severity: high · Status: fixed (confirmed by FS, 2026-08-31)

- **H-6. No LICENSE — the widely-forked goal is currently impossible.** Unlicensed public code is all-rights-reserved; GitHub's terms grant only view-and-fork within GitHub. Corporate scanners flag it unusable, and the `license:` search facet and sidebar badge are forfeited. Recommended split, **blocked on B-1**: **MIT** at the root (individual author, no patent portfolio, lowest friction) and **CC BY 4.0** for `learning/`. MIT over ~6,900 lines of prose is a category error — its operative terms ("the Software") do not map onto essays. Not BY-NC (fails OSD, blocked by many corporate policies), not BY-SA (forces copyleft on anyone quoting a notebook, suppressing citation). Creative Commons itself recommends against CC for software, so one CC licence over everything is equally wrong. Add a one-sentence `## License` section — GitHub's detector shows only the root licence, so readers will assume it covers everything — plus SPDX headers on `orbit/` sources and `CITATION.cff`. Include one honest sentence that AI-generated material without meaningful human authorship is not copyrightable under current US Copyright Office guidance, so the grants apply "to the extent copyright subsists." That is far more credible to a senior reader than ignoring the question.

### PR-H-7 — `.gitignore` has no credential patterns
> From: Public-readiness audit, 2026-08-13 · Original section: H — HIGH · **Legal and community** · Severity: high · Status: open — none of these patterns are in `.gitignore` yet (checked 2026-09-25)

- **H-7. `.gitignore` has no credential patterns — becomes critical on a known date.** Correct today: `.env`, `*.env`, `*.tfstate`, `.terraform/`, and notably `.terraform.lock.hcl` is *not* ignored, which most people get backwards. Missing every file type that actually carries secrets, each arriving on the roadmap: `*.tfvars` (Topics 18, 34-39 — the canonical Terraform leak), `*.pem`/`*.key`/`id_rsa*`/`*.p12` (Topic 23), `credentials`/`.aws/`/`*accessKeys*.csv` (Topics 21-22 — **AWS keys**), `kubeconfig*`/`.kube/` (Topics 12-14, 31), `*.retry`/`.vault_pass*` (Topic 17), and `.env.*` (today — `*.env` matches `prod.env` but **not** `.env.local`). Use `!*.tfvars.example` / `!.env.example` negations so config *shape* stays committable. **This becomes genuinely critical the day Topic 21 starts** — public repo plus a stray access-key file is the canonical catastrophic incident. Must land before Phase 3. Separately, `env/` at `:7` is unanchored and will silently swallow `orbit/terraform/env/` (Topic 36 is Workspaces & Multi-Region) — anchor to `/env/`.

### PR-M-1 — Disclosure
> From: Public-readiness audit, 2026-08-13 · Original section: M — MEDIUM (grouped) · Severity: medium · Status: not re-checked since

**Disclosure** — `CLAUDE.md:38` / `field_atlas.md:15` reveal an org-level tooling restriction (reword to "not available in this setup"). `session_notes.md:76-77` and `progress.md:121` cite a real production alert the author's own team receives (reframe as hypothetical). `session_notes.md:13` and `progress.md:33` disclose a night-shift rota (remove). `topic-05:87,89,249,301-306` and `topic-09:380-384` expose host-local NAT addressing of a corporate-managed endpoint — real severity is capped because these are host-local ranges, but mask the octets. `handbook_status.md:8` links a personal site, bridging the personal identity to the corporate-authored history — decide deliberately (that link also currently 404s). `audits/topic-10-professionalism.md:54` documents job-hunting publicly.

### PR-M-2 — Candour
> From: Public-readiness audit, 2026-08-13 · Original section: M — MEDIUM (grouped) · Severity: medium · Status: not re-checked since

**Candour** — `session_notes.md` publishes frustration and memory-difficulty statements verbatim and `handbook_status.md` publishes a per-topic weakness list. This is genuinely the most distinctive material in the repo and is arguably its strongest differentiator — but it is irreversible after the first fork, and shipping it *alongside* H-5's characterisations is what tips it from admirably honest into oversharing. Make it a deliberate decision. Drop `claude-memory/` either way.

### RO-3.1 — GitHub didn't detect the LICENSE as MIT
> From: Repo organization audit, 2026-08-26 · Original section: Batch 3 — root and governance · Status: fixed 2026-08-20

**The real defect, verified externally**: queried the GitHub API before touching anything —
the repo's license was being detected as `"Other" / NOASSERTION`, not MIT. The scope paragraph
inserted before the MIT body and the note appended after it had broken GitHub's license
detection. `LICENSE` is now byte-identical to canonical MIT (checked programmatically); the scope
split and the "not production-hardened" note moved to README's License section.

### RO-3.2 — Root prose files fell under neither licence
> From: Repo organization audit, 2026-08-26 · Original section: Batch 3 — root and governance · Status: fixed 2026-08-20

**A real gap, not just a defect**: the root prose files (`README.md`, `CONTRIBUTING.md`,
`SECURITY.md`, `CLAUDE.md`) fell under **neither** license grant — not `learning/`, `docs/`, or
`audits/`, so not CC BY; not plausibly "scripts or configuration," so not MIT. Both license files
and the README now place root prose under CC BY 4.0.

### FS-1 — The actual public repository is still the pre-remediation, exposed snapshot from a month ago
> From: Final sign-off audit, 2026-08-31 · Original section: Critical · Severity: critical · Status: open — the public mirror was last updated 2026-07-29 (checked 2026-09-25)

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

### FS-2 — B-1 — the right-to-publish question is still open, per the repo's own last review of it
> From: Final sign-off audit, 2026-08-31 · Original section: Critical · Severity: critical · Status: closed 2026-08-31

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

### FS-3 — `engine/` — the entire "fork this" pitch — carries no license grant at all
> From: Final sign-off audit, 2026-08-31 · Original section: Critical · Severity: critical · Status: fixed — `engine/` is now in the CC BY 4.0 grant

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

### FS-5 — `CLAUDE.md`'s git-metadata exemption — the policy that let Finding 1 happen — was never removed
> From: Final sign-off audit, 2026-08-31 · Original section: Critical · Severity: critical · Status: partly done — repo-local identity is set to the personal no-reply address; the exemption is still in `rules.md` §7

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

### FS-I-6 — The LICENSE fix and the B-1 gate pointed opposite ways
> From: Final sign-off audit, 2026-08-31 · Original section: Important · **`audits/` self-consistency** (found by this audit's dedicated cross-check of all three prior audit files against each other and the live repo) · Severity: important · Status: closed — B-1 is closed (FS-2)

- **That same audit fixed the root `LICENSE` file's GitHub-detectability** (so the license facet
  now correctly shows "MIT" instead of "Other/NOASSERTION") while listing B-1 as explicitly
  gating all licensing work ("Gate 3... blocked on B-1"). Making the license cleanly
  machine-readable is precisely the public-facing signal that gate exists to hold back until B-1
  resolves — the fix and the gate point in opposite directions.

### FS-m-7 — Night-shift schedule detail still present
> From: Final sign-off audit, 2026-08-31 · Original section: Minor · Severity: minor · Status: fixed 2026-09-25 — Session 1 note shortened; `session_notes.md` removed

- **A carryover from `public-readiness.md`'s M-tier that's still present**: `session_notes.md`'s
  Session 1 entry and `progress.md`'s Session 1 Check-in note both still name a "night-shift"
  personal-schedule detail, which that audit recommended removing or reframing as neutral. Not
  re-litigated here as a fresh finding — flagged only because it's still live, unlike most of that
  audit's other M-tier items.

## Verified clean — negative results

**From the public-readiness audit, 2026-08-13:**

- **No secrets or credentials, tree or full history.** Zero matches across all 41 files and all 60 commits on all refs for GitHub tokens, AWS key prefixes, private-key headers, Slack tokens, JWTs, or any high-entropy token. Pickaxe search confirms none were ever added-then-removed. The 60+ hits for `password`/`secret`/`token` are **all** educational prose with no assigned values.
- **No credential-bearing file type ever committed.** No key, cert, keystore, `.env` or credentials file in the tree or in the full add-history. No ignored-but-present sensitive files in the working directory.
- **No SSH key material.** The topic that teaches `ssh-keygen` explicitly notes private key contents are never shown.
- **Employer name in current file content: 0 occurrences.** Only false positives from `mm-` inside `YYYY-MM-DD` format strings. **The standing rule is genuinely upheld in the working tree** — the exposure is entirely metadata and history.
- **Emails in the tree: only the deliberate placeholder.** GitHub org references in notebooks: consistently the intended placeholder.
- **Single author identity**, no co-authors, no bot commits, no third-party PII. No phone numbers, addresses, DOBs or government IDs.
- **Git internals clean** — no stash, no custom hooks, no orphaned branches carrying different content, clean linear history, working tree clean.
- **No internal hostnames or corporate domains** — no intranet FQDNs, machine names, proxy-vendor references, PAC URLs or CA-bundle values. No routable public IPs beyond a public DNS answer and a documentation placeholder.
- **`orbit/` app code clean** — no credentials, no env-var secrets, no internal registries, no hardcoded hosts.
- **Original writing.** Idiosyncratic first-person prose narrating the author's own mistakes — not liftable from documentation. No man-page excerpts, no `--help` dumps, no book quotations; the `**Syntax**` convention is simplified original rewriting, not man-page SYNOPSIS. The one book reference invokes a title **in order to disagree with it**, quoting nothing. All diagrams hand-drawn ASCII. `CLAUDE.md:215`'s paraphrase-only rule visibly held, with a single exception noted in L.

**From the final sign-off audit, 2026-08-31:**

- **No secrets or credentials anywhere, on any ref.** Re-verified independently this audit: zero
  matches across `main`, `origin/main`, and `personal/main`'s full history for AWS key prefixes,
  private-key headers, GitHub/Slack tokens, or password/secret/token assignments with real values.
- **The redaction convention is genuinely followed in captured output** — spot-checked
  `devuser`/`devuser` placeholders in Topic 1's filesystem listings; consistent with
  `CONTRIBUTING.md`'s stated convention.
- **The public-readiness audit's own required raw-copy rule was followed** — `public-readiness.md`
  did produce and preserve an unredacted external copy under `C:\CloudOps`, as its own redaction
  note promises; `repo-organization.md` correctly stated no such copy was needed and said so
  explicitly, matching the standing rule.
