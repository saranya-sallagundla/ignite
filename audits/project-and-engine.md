# Project and engine

Are the outward-facing products ready? `orbit/`, `engine/`, the root presentation, and CI.

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

### T10-1.2 — `orbit/README.md` said there was nothing to run
> From: Topic 10 professionalism audit, 2026-07-27 · Original section: Batch 1 — Critical (4 items) · Severity: critical · Status: fixed 2026-07-27

2. **`orbit/README.md`'s "How to run it" section said there was nothing to run**, directly
   contradicting the Status section two lines below it (which said the app runs via Compose).
   *Why it matters*: this is the first thing a reviewer reads in the showcase folder — a
   self-contradiction there undermines trust in everything else in the repo.

### T10-3 — Showcase polish in `orbit/`
> From: Topic 10 professionalism audit, 2026-07-27 · Original section: Batch 3 — Showcase polish (`orbit/`) · Status: fixed 2026-07-27

- Renamed `orbit/README.md`'s title from the generic "The project" to "Orbit — DevOps
  Capstone Project," matching the project's actual identity elsewhere.
- Rewrote `orbit/app/README.md` to drop internal-scaffolding language ("not yet defensible in an
  interview," a direct reference to `CLAUDE.md`) that had leaked into the interview-facing folder.
- Cleaned `docker-compose.yml`: removed line-by-line teaching comments and a leftover two-service
  demo (`app2` + an unused shared volume) that served no purpose beyond the lesson it came from.
- Reworded `docs/concept.md`'s framing away from language that reads oddly to an employer reviewer
  (planning around "the org repo being deleted," anchoring the demo to "onsite interviews"), and
  corrected a wrong GitHub Codespaces quota figure (120 core-hours, not 60).
- Normalized all 5 placeholder READMEs (`k8s/`, `terraform/`, `ansible/`, `monitoring/`,
  `scripts/`) to one consistent, correctly-tensed template.

*Why it matters*: `orbit/` is explicitly the folder meant to be shown in an interview — every
item here was something that would read as unpolished, inconsistent, or (worse) revealing to
exactly the audience this repo is built for.

### T10-7 — Dockerfile and Compose items held for Topic 11
> From: Topic 10 professionalism audit, 2026-07-27 · Original section: Deferred — Batch 7 (intentionally NOT fixed in this audit) · Status: held for Topic 11 — fixed there (confirmed by PR and FS)

A set of `Dockerfile`/`docker-compose.yml` improvements that are exactly Topic 11's subject
matter (Docker: Multi-Stage Builds & Best Practices), so they're saved for when that topic is
actually taught rather than fixed retroactively:

| Item | Why it matters |
|---|---|
| Container runs as root (no `USER` instruction) | Standard container-security flag any reviewer or scanner checks first |
| Flask's dev server used in the container (`CMD ["python","app.py"]`) | Not production-grade; prints a dev-server warning on every start |
| Missing `EXPOSE 5000` | Documents which port the container uses |
| Missing `HEALTHCHECK` despite a purpose-built `/health` endpoint | Nothing currently consumes the endpoint that exists for exactly this |
| `pip install` without `--no-cache-dir` | Bloats the image with an unneeded download cache |
| Missing `PYTHONUNBUFFERED=1` | Python buffers stdout in containers by default; logs can lag during a demo |
| Compose builds an untagged image | `orbit/README.md` claims the image is "properly version-tagged"; the compose file doesn't back that up yet |
| `flask==3.1.0` slightly behind a security-patched `3.1.1` | Low real risk here, but a dependency scanner would flag the pin |

**Next audit should confirm these were actually addressed during Topic 11**, not still sitting
here unresolved.

### PR-H-8 — `USER appuser` is non-numeric
> From: Public-readiness audit, 2026-08-13 · Original section: H — HIGH · **Legal and community** · Severity: high · Status: open — `progress.md` Open items #3, Topic 13

- **H-8. `USER appuser` is non-numeric — hard-blocks Kubernetes at Topic 12.** `Dockerfile:12,17`. With `runAsNonRoot: true` and no explicit `runAsUser`, the kubelet cannot resolve a non-numeric image user and the container fails with `CreateContainerConfigError`. Topics 12-14 are next — this is a landmine directly in the path of the following three topics. Fix: `useradd --uid 10001 --shell /usr/sbin/nologin` + `USER 10001` (10001 avoids collision with host users in the 1000 range).

### PR-H-9 — The README told hiring managers not to take it seriously
> From: Public-readiness audit, 2026-08-13 · Original section: H — HIGH · **Presentation** · Severity: high · Status: fixed (confirmed by FS, 2026-08-31)

- **H-9. The repo tells hiring managers not to take it seriously.** `README.md:11` calls `learning/` *"not meant to be shown to anyone"* — the README of a public repo telling visitors that ~6,900 of its ~8,000 lines are not for them. **The single worst line in the repo for the stated goal.** Then `README.md:71-72`, `orbit/README.md:15` and `orbit/app/README.md:4-5` all carry "not yet something to defend" language, which **violates `CLAUDE.md:152-153`** — the rule was written and then broken in the very folder it protects. It is also no longer true: the Dockerfile is a genuine multi-stage non-root gunicorn build with a real image-size bug found and fixed with measured proof. Honest reframe that keeps the narrative without the apology: *a deliberately minimal service that exists to be a real deployment target — the interesting engineering is in how it is built, shipped and operated.* Other stranger-test failures: `:8` says "Two folders" while the tree below shows four; `:16-18` spends prime real estate on tool file-discovery trivia; `:83-84` closes with an instruction addressed to the owner; `:3`'s H1 is "Mission: DevOps" while the repo is named `ignite`.

### PR-H-11 — Zero CI and zero tests
> From: Public-readiness audit, 2026-08-13 · Original section: H — HIGH · **Presentation** · Severity: high · Status: held for Topic 15

- **H-11. Zero CI and zero tests in a repo that teaches CI/CD.** No `.github/` at all, no tests, no linter config, all git hooks unmodified samples — while Topic 8 (GitHub Actions, branch protection) scored 94/100. The first thing a senior engineer checks on a DevOps repo is the Actions tab. Sequenced to respect the defer-to-topic rule: **now, as repo infrastructure not lesson content** — secret scanning on push/PR (non-negotiable given C-2/C-3), markdown lint + link check over `learning/**`, Dockerfile lint. **At Topic 15, as the hands-on artifact** — build + `/health` smoke test, `ruff`, first `pytest`. **At Topics 12-14 / 18 / 34-39** — manifest, Terraform and policy linting.

### PR-H-17–19 — `orbit/` documentation contradicts reality and itself
> From: Public-readiness audit, 2026-08-13 · Original section: H — HIGH · **Presentation** · Severity: high · Status: fixed 2026-08-20 (RO-2.2)

- **H-17 / H-18 / H-19. `orbit/` documentation contradicts reality and itself.** `:25` says every folder but `app/` is an empty placeholder while `docs/concept.md` exists and `docs/README.md:3` says so. `:119-122` claims a two-service compose file with a named volume that no longer exists — the interview-facing README claiming a capability the repo cannot demonstrate. And `orbit/README.md:8-9,19` promises Terraform-provisioned AWS and Helm on Kubernetes while `docs/concept.md:22-25` says k3s locally and an AWS emulator instead of a live account — a first-time reader gets two different projects from two files, and neither mentions the actual capstone.

### PR-M-4 — Community files
> From: Public-readiness audit, 2026-08-13 · Original section: M — MEDIUM (grouped) · Severity: medium · Status: fixed — `CONTRIBUTING.md` and `SECURITY.md` exist (confirmed by FS)

**Community files** — all absent. `CONTRIBUTING.md` is the important one, and generic advice is *harmful* here: `learning/` is a dated first-person record, so a PR "improving" a notebook destroys the artifact. Draw the line explicitly — factual errors become an **issue with a source** (which feeds `CLAUDE.md:148-150`'s verify-before-writing rule); rewrites and style edits are closed with the reason stated up front; `orbit/` takes normal PRs; the tracking files and the roadmap baseline never accept external edits. `SECURITY.md`'s realistic threat is *"an example teaches something insecure and people copy it,"* not a CVE — and enable GitHub private vulnerability reporting so no email is published, since the only currently-associated address is corporate. The PR template needs a checkbox asserting no `learning/` or baseline changes. Dependabot has only two ecosystems today.

### PR-M-5 — Container / supply chain
> From: Public-readiness audit, 2026-08-13 · Original section: M — MEDIUM (grouped) · Severity: medium · Status: not re-checked since

**Container / supply chain** — all Topic 10-11 material, all already taught, so these are gaps rather than deferrals. Compose has no hardening at all (no `restart`, limits, `cap_drop: ALL`, `no-new-privileges`, `read_only` + `tmpfs`, log rotation, `stop_grace_period`); `read_only: true` is achievable **today** because `WORKDIR /app` is root-owned and the app is stateless, which most projects cannot claim. Port `"5000:5000"` publishes on all interfaces **and Docker's iptables rules bypass host firewalls** — use `127.0.0.1:5000:5000`. Transitive dependencies float (Werkzeug, Jinja2, Click, ItsDangerous, Blinker, MarkupSafe) with no hashes and no lockfile — and Werkzeug is exactly where Flask's HTTP-parsing CVEs land; fix with `pip-compile --generate-hashes` and `--require-hashes`, which is load-bearing because pip then refuses anything unhashed including transitives. `--chown=appuser` gives the runtime user write access to its own venv and source, which silently defeats `read_only`; dropping it also permanently forecloses the Session 17 copy-up size bug. The base image floats *and* is resolved independently in both stages, so the venv can be built against one patch and run on another — name the base once and derive both stages; note that a digest alone is not the answer either, since digest pinning without automated bumping is reproducible *and rotting*. **Gunicorn runs on pure defaults, so the container serves HTTP and produces no request log at all** — in a repo whose premise is observability that is the finding most likely to draw a pointed question, and it is one flag. Version `2.1` is hardcoded in four places with no source of truth. No tests exist, so a pipeline arrives at Topic 15 with nothing to run.

### PR-M-6 — Framing
> From: Public-readiness audit, 2026-08-13 · Original section: M — MEDIUM (grouped) · Severity: medium · Status: not re-checked since

**Framing** — `orbit/` cannot yet carry "Capstone": ~56 lines of real code, 5 of 7 subfolders single-line placeholders, and a concept doc promising an autonomous SRE agent with a live dashboard. `orbit/README.md` is 130 lines of which ~90 are a session diary containing twelve consecutive "no project code yet" entries — a reviewer reads a dozen admissions of nothing built before reaching a genuinely impressive Status section. Move the diary to `orbit/docs/changelog.md`; put the status at the top; mark the concept doc aspirational in its **first** line.

### RO-1.3 — `orbit/README.md`'s Session 16 claim
> From: Repo organization audit, 2026-08-26 · Original section: Batch 1 — the three criticals, plus leftovers from the audits/ rename · Status: fixed 2026-08-20

**`orbit/README.md`'s Session 16 entry** claimed Compose was "extended with a second service and
a named volume," which the committed `docker-compose.yml` contradicts (one service, no volumes).
Before rewriting a historical log entry, checked git history: the claim was **true when written**
— a second service and volume genuinely existed at Topic 10 completion (`c44bdf7`) and were
removed later by the Topic 10 audit's own cleanup commit (`3fd8fa2`). Fixed by adding a removal
note, not by rewriting an accurate historical record.

### RO-2.1 — Internal-scaffolding language in `orbit/`
> From: Repo organization audit, 2026-08-26 · Original section: Batch 2 — orbit/, the showcase folder · Status: fixed 2026-08-20

**The real defect**: `CLAUDE.md` explicitly bans internal-scaffolding language from `orbit/`
("no internal-scaffolding language... references to this file"), yet the folder guide's first
bullet and `orbit/app/README.md` both told reviewers the code was "not yet something to defend in
an interview." Removed from both.

### RO-2.2 — `orbit/` accuracy fixes
> From: Repo organization audit, 2026-08-26 · Original section: Batch 2 — orbit/, the showcase folder · Status: fixed 2026-08-20

**Accuracy fixes**: `argocd/` existed with its own README but was missing from the folder guide;
"every folder is an empty placeholder" was false for `docs/` (holds `concept.md`); the README
promised Kubernetes on Terraform-provisioned AWS while `docs/concept.md` specifies local k3s +
LocalStack — reconciled so the two showcase docs agree; 17 topic names (not the ~12 the prior
audit estimated) were in non-baseline spelling — recounted and fixed.

### RO-2.3 — `orbit/README.md` build-log structure
> From: Repo organization audit, 2026-08-26 · Original section: Batch 2 — orbit/, the showcase folder · Status: fixed 2026-08-20

**Structure**: the build log had grown to 17 entries, 12 of them "no project code yet,"
oldest-first — burying the actual Docker work under Linux filler in a showcase README. Collapsed
Sessions 1-12 to one Phase 1 line; moved the log under its own heading. README: 130 → 77 lines.

### RO-2.4 — `container_name: orbit-app` kept
> From: Repo organization audit, 2026-08-26 · Original section: Batch 2 — orbit/, the showcase folder · Status: left as is on purpose

**Deliberately not fixed**: `container_name: orbit-app` in `docker-compose.yml` — dropping it
would rename the running container to `orbit-app-1` on next `up`, which could invalidate `docker
exec` commands already captured in the notebooks. Left in place.

### FS-4 — `QUICKSTART.md`'s default setup path breaks at the very first mandatory step
> From: Final sign-off audit, 2026-08-31 · Original section: Critical · Severity: critical · Status: fixed — the Quickstart now adds a remote first

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

### FS-I-8 — `orbit/README.md`'s Status misdescribed the roadmap
> From: Final sign-off audit, 2026-08-31 · Original section: Important · **`orbit/` accuracy** · Severity: important · Status: fixed — replaced by the Parts section, 2026-09-25

- **`orbit/README.md`'s Status section misdescribes the roadmap it's summarizing.** It says
  Kubernetes, CI/CD, and Terraform "follow in the later phases" — but per `learning/roadmap.md`'s
  own fixed baseline, Kubernetes (12–14), CI/CD (15–16), Ansible (17) and Terraform's introduction
  (18) are the *remaining topics of the current phase* (Phase 2, "now underway" per the roadmap's
  own Pacing Layer), not later phases. Only Terraform's deepening (Phase 4) and observability
  (Phase 6) are genuinely later.

### FS-I-9 — `orbit/docs/concept.md` reads as curriculum scaffolding
> From: Final sign-off audit, 2026-08-31 · Original section: Important · **`orbit/` accuracy** · Severity: important · Status: not re-checked since

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

### FS-I-10 — `docs/README.md` claimed content that doesn't exist
> From: Final sign-off audit, 2026-08-31 · Original section: Important · **`orbit/` accuracy** · Severity: important · Status: superseded — `docs/README.md` deleted 2026-09-25

- **`docs/README.md` claims content that doesn't exist.** It describes `docs/` as covering *"the
  teaching and testing method, future project ideas, and cross-cutting architecture decisions"* —
  a third thing no file in the folder actually covers, and the root `README.md`'s own tree comment
  describes this same folder with only two things. The two README files describing one folder
  disagree with each other.

### FS-m-4 — `orbit/` minor accuracy nits
> From: Final sign-off audit, 2026-08-31 · Original section: Minor · Severity: minor · Status: not re-checked since

- **`orbit/` minor accuracy nits**: `orbit/docs/concept.md` groups EC2/S3 with IAM/Lambda as
  uniformly "genuinely free," but EC2/S3's free tier is limited to a new account's first 12
  months, unlike IAM/Lambda; `orbit/scripts/README.md` ties "general shell utilities" to Phase 5
  even though shell scripting was already taught in Topic 3 (Phase 1) with no roadmap reason to
  wait.

### FS-c-4 — `MISSION.template.md` says two example rows, shows three
> From: Final sign-off audit, 2026-08-31 · Original section: Cosmetic · Severity: cosmetic · Status: not re-checked since

- `engine/MISSION.template.md`'s own instructional comment says "two example rows are shown" where
  three actually are.

## Verified clean — negative results

**From the public-readiness audit, 2026-08-13:**

- **All 8 items the Topic 10 audit deferred to Topic 11 were actually resolved** — non-root `USER`, gunicorn replacing the dev server, `EXPOSE`, `HEALTHCHECK`, `--no-cache-dir`, `PYTHONUNBUFFERED`, tagged Compose image, and the Flask patch bump. **The audit cadence is working as designed.**
- **Correctly-sequenced deferrals, not gaps** — metrics endpoint → Topic 47; structured logging → 49; immutable git-SHA tags and scanning/SBOM/signing → 15-16; `securityContext` and probes → 12-14; distroless base → 11 revisit or 15; secrets management → 14, 33; multi-arch → 15.
- **Two things reviewers commonly flag *wrongly* here, both already correct.** `CMD` is exec-form, so gunicorn is PID 1 and receives `SIGTERM` directly; its master handles graceful shutdown and reaps workers, so an init wrapper is **unnecessary** — and knowing why is worth more than the flag. And the HEALTHCHECK **does** work: the check raises, Python exits non-zero, Docker counts a retry, three retries marks the container unhealthy.

**From the final sign-off audit, 2026-08-31:**

- **`orbit/app/`'s code and Dockerfile carry no debugging or teaching-style comments**, and no
  reference to `CLAUDE.md` — the interview-facing-folder rule is genuinely held to in the code
  itself (the violations found are in prose files, not code).
- **Every placeholder README under `orbit/`'s not-yet-built folders correctly names its populating
  topic**, cross-checked against `roadmap.md`'s real topic numbers — including
  `.github/workflows/README.md`'s Topic 15/16 framing.
