# DevOps/SRE Field Atlas — Topic Map

> One section per topic group cleared so far, in a fixed five-point shape: the real problem → why
> it matters → how it connects → the alternatives → production reality. Each section ends with a
> case from this repo, where you'll meet the idea, and a question to check yourself. The state of
> the field, and the rules for maintaining the atlas, are in the [field map](field-map.md); the
> sub-disciplines referred to below as §1.5 live there.

---

## Table of Contents

- [Linux](#linux)
- [Git](#git)
- [GitHub](#github)
- [Docker](#docker)

---

## Part 2 — Topics Covered So Far

### Linux

> **In one line:** the floor everything else in this file stands on.

**The real problem.** Before a shared, standardized OS with an open toolset, "the server" meant
whatever proprietary Unix variant or early Windows Server setup a specific vendor sold you —
inconsistent tooling, licensing costs at scale, and no common baseline of commands/scripts that
worked the same way everywhere. Linux (plus the broader open-source toolchain around it) became
the thing that let "how do I check disk usage" or "how do I find what's eating memory" have one
answer that works on a $5/month VPS and a fleet of ten thousand cloud servers alike.

**Why it matters for DevOps/SRE.** It's not a topic *among* the skill stack — it's closer to the
floor everything else stands on. Every container is (in Orbit's case) built on a Linux base image;
every cloud VM you'll provision later runs Linux; every `kubectl` command eventually resolves down
to Linux processes on a node. Not knowing Linux well enough means every layer above it — Docker,
Kubernetes, CI/CD runners — becomes a black box you can't actually debug when it breaks, only
follow tutorials for when it works.

**How it connects.** Everything since Topic 1 has referenced it directly: the WSL corporate-proxy
investigation used the exact filesystem/permission/networking fundamentals from Topics 1-5; the
Docker topics (9-11) are built entirely on Linux process/user/filesystem concepts (the `chown`/
copy-up bug in Topic 11 is fundamentally a Linux filesystem-layering concept, not a Docker-specific
one); Kubernetes (Topic 12 onward) runs Linux containers on Linux nodes — the "process
states," "signals," and "resource limits" concepts from Topics 2 and 4 reappear directly as
Kubernetes concepts (a container's exit code, a Pod being OOMKilled).

It also connects directly to several §1.5 sub-disciplines, not just to later topics: **SRE**'s
entire numeric reliability model (SLOs, error budgets) is meaningless without someone able to
actually diagnose *why* a system is unhealthy at the systems level — that diagnostic skill is
Linux fundamentals, full stop. **DevSecOps**'s "run as a non-root user, least-privilege" practice
(which Topic 11 applied directly to Orbit's container) isn't a Docker-specific idea at all — it's
literally the Linux user/permission model from Topic 1, applied one layer up. And every **Platform
Engineering** team's slick self-service tooling still ultimately provisions and runs on real Linux
hosts underneath every abstraction — the platform hides Linux from the end user, it doesn't
replace it.

**The alternatives.** For servers specifically, there isn't a real alternative in modern cloud/
DevOps practice — Windows Server still exists for specific enterprise/.NET-heavy shops, but the
overwhelming majority of cloud-native infrastructure, containers, and Kubernetes nodes run Linux.
The real "alternative" question that comes up in practice is *which* Linux distribution and how
minimal (Ubuntu/Debian-family vs. RHEL/Alma/Rocky-family vs. minimal/distroless images for
containers specifically).

**Production reality.** At 2am, Linux fundamentals are the difference between "the disk is full, I
know exactly which command tells me what's actually eating it and I can free space safely" and
paging someone else because you don't trust yourself to touch a production filesystem.

> **From this repo:** the Topic 1 proxy investigation and Topic 4's `df`-timeout-as-liveness-issue
> (not corruption) are exactly this kind of real, non-tutorial situation — a plausible-looking
> symptom that needs real fundamentals to diagnose correctly instead of guessing and making it
> worse.

**Where you'll meet this:** in every "the container won't start" or "the disk is full" moment, one
layer below whichever tool you were actually using.

<details>
<summary><b>Check yourself:</b> a Pod shows <code>OOMKilled</code>. Which Linux idea is that, and from which topics?</summary>

Resource limits and signals (Topics 2 and 4). The kernel kills the process with SIGKILL when it
goes past its memory limit, and the container's exit code (137 = 128 + 9) reports it. Same
mechanics as a Linux process, one layer up.
</details>

### Git

> **In one line:** the substrate CI/CD, GitOps and Infrastructure as Code are all built on.

**The real problem.** Before version control like Git, "collaborating on code" commonly meant
emailing files around, naming things `final_v2_REALLY_FINAL.py`, or using centralized systems
(like Subversion/CVS) that required constant network access to a central server and made branching
so painful that teams mostly avoided it. Losing history, overwriting someone else's work
accidentally, and having no real way to experiment safely on a copy of the code were all normal,
accepted risks.

**Why it matters for DevOps/SRE.** Git isn't just "how developers store code" — it's the substrate
CI/CD, GitOps, and Infrastructure as Code are all built on top of. A pipeline triggers *because* of
a Git push; a GitOps controller reconciles a cluster *against* a Git repo's state; Terraform state
and configuration live in Git. If you don't actually understand Git's model (not just the handful
of commands you use daily), you can't reason correctly about *why* a CI/CD pipeline behaves the
way it does when something unexpected happens.

**How it connects.** Topic 6 (fundamentals) → Topic 7 (rebase/cherry-pick, real conflict
resolution) → Topic 8 (GitHub-specific collaboration: PRs, Actions) form one continuous thread —
and this thread directly feeds GitOps (§1.5): the entire premise of GitOps is that Git history
*is* the deployment record, so understanding Git deeply here pays off again later when Kubernetes
deployment gets covered through a GitOps lens.

Beyond GitOps specifically, Git is genuinely load-bearing infrastructure for several other §1.5
sub-disciplines: **DevSecOps** hangs a large share of its automated scanning directly off Git
events — pre-commit hooks and secret-detection tools run *at commit time*, before code ever
leaves a laptop, which is the literal mechanism behind "shift-left." **Platform Engineering**'s
"golden path" self-service templates are, in practice, almost always delivered as a Git repo
template a new service gets scaffolded from — the platform *is*, mechanically, a curated set of
Git repositories and the automation wired to them. And **DataOps** applies this exact same
version-everything discipline to data pipelines instead of application code — same underlying
tool, same reasoning, different artifact being tracked.

**The alternatives.** Git effectively won this space — Subversion and Mercurial still exist in
legacy contexts, but essentially no new project in 2026 chooses them over Git. The real "which
tool" decision that still exists in practice is the **hosting/collaboration layer on top of Git**
(GitHub vs. GitLab vs. Bitbucket) — covered next.

**Production reality.** The real 2am Git moment isn't "I forgot the commit command" — it's "we
need to recover from a bad deploy *right now*, and knowing whether to revert, reset, or roll
forward with a fix matters, because picking wrong can make history confusing for the whole team or
even lose work."

> **From this repo:** Topic 7's real cherry-pick mistake (conflict markers left in a file despite
> `git add`+`--continue` appearing to succeed) is exactly the kind of "it looked done but wasn't"
> trap that matters far more under real incident pressure than in a calm tutorial.

**Where you'll meet this:** in every pipeline that runs because of a push, and in the first bad
deploy you have to undo.

<details>
<summary><b>Check yourself:</b> a bad commit is already on <code>main</code> and deployed. Revert, reset, or roll forward: which is safe on a shared branch, and why?</summary>

Revert (a new commit that undoes the change) or roll forward with a fix: both add to history.
Reset rewrites history that others already have, so their clones disagree with `main` and it takes
a force-push to land, which can lose work.
</details>

### GitHub

> **In one line:** review, merge rules and automation, layered on top of Git.

**The real problem.** Git itself is a distributed version-control *tool* — it has no concept of
"a pull request," "who's allowed to merge," or "run this automatically when code changes." Before
platforms like GitHub existed, teams using raw Git still needed a separate, often informal process
for code review (emailing patches, or nothing at all) and had to build or buy separate systems for
running tests/automation on new code.

**Why it matters for DevOps/SRE.** GitHub (and platforms like it) is where the actual *workflow*
of software delivery lives: pull requests are where code review and quality gates happen; branch
protection rules are a real, load-bearing safety mechanism (Topic 8's discovery about admins,
under Production reality below); GitHub Actions is many teams' actual CI/CD engine, not a
separate tool bolted on.

**How it connects.** Directly extends Git (above) with collaboration and automation layered on
top, and GitHub Actions specifically is the same category of tool as the CI/CD systems that will
come up again later in the roadmap (Topic 15) — the concepts (triggers, runners, secrets scoping)
transfer directly.

This is also where several §1.5 sub-disciplines become concretely visible rather than abstract:
**DevSecOps** in practice is very often "a GitHub Action running a scanner on every PR" (Dependabot
alerts, CodeQL, container-image scanning) — the pipeline *is* the security gate, not a separate
process. **ChatOps** frequently rides on top of GitHub's own webhook/bot ecosystem — a Slack
notification on a failed Action run, a bot commenting build status directly on a PR. And
**Platform Engineering**'s internal developer platforms (tools like Backstage) commonly use GitHub
itself as their underlying service catalog and template source — the "platform" is often a layer
of automation and UI wrapped around GitHub, not a replacement for it.

**The alternatives.** GitLab (which also bundles CI/CD, container registry, and more into one
product) and Bitbucket (more common in Atlassian-centric shops using Jira) are the real
competitors. The honest trade-off: GitHub has the largest ecosystem and community/Action
marketplace; GitLab's single-product approach appeals to teams that want fewer separate tools to
integrate and operate.

**Production reality.** The `GITHUB_TOKEN` security considerations from Topic 8 (scope, lifespan,
real risks) aren't academic — a misconfigured Action with excessive token permissions is a real,
current class of supply-chain security incident.

> **From this repo:** Topic 8's discovery that branch protection doesn't apply to admins by
> default, silently, until explicitly configured otherwise, is exactly the kind of thing that looks
> fine in every test until the one time someone with admin access pushes directly to `main` under
> time pressure and nothing stops them.

**Where you'll meet this:** in every pull request you open, and the first time a required check
blocks a merge you were sure about.

<details>
<summary><b>Check yourself:</b> a workflow needs to push a tag. What's wrong with giving <code>GITHUB_TOKEN</code> <code>write-all</code>, and what should it get instead?</summary>

Least privilege. `write-all` lets any step, including third-party actions the workflow pulls in,
write to everything the token can reach; that is the supply-chain risk. Give the job a
`permissions:` block with only `contents: write`, and nothing else.
</details>

### Docker

> **In one line:** the packaging unit everything else in modern DevOps assumes already exists.

**The real problem.** "Works on my machine" was one of software delivery's most expensive,
recurring failure modes — an app running fine in development, then breaking in production because
of a different OS version, a missing system library, or a mismatched dependency version that
nobody had pinned down precisely. Fixing this by hand meant painstakingly replicating an exact
environment on every target machine — slow, error-prone, and constantly drifting out of sync.

**Why it matters for DevOps/SRE.** Docker (and the OCI container-image standard it popularized)
is the packaging unit almost everything else in modern DevOps assumes exists: CI/CD pipelines
build and test container images; Kubernetes schedules and runs containers; GitOps tools deploy new
container image versions. Skipping real Docker fluency to jump straight to Kubernetes is a common
mistake — Kubernetes is fundamentally an orchestrator *of* containers, and half its behavior only
makes sense once you understand what a container actually is and isn't.

**How it connects.** This mission's own Topics 9-11 built this up directly: architecture and image/
container semantics (9), networking and persistent storage (10), and production-readiness — non-
root users, a real WSGI server instead of a dev server, multi-stage builds (11). Every one of
those threads reappears almost immediately in Kubernetes: a Pod is fundamentally a wrapper around
one or more containers; Kubernetes Services solve the same "how do containers find each other"
problem Topic 10 solved manually with Docker networks, just at cluster scale; a Deployment's
rolling update behavior depends on the same image-tagging discipline Topic 9 covered.

The container is also the literal unit several §1.5 sub-disciplines organize themselves around,
not just a Kubernetes prerequisite: **Platform Engineering**'s self-service platforms almost
always manage *containers* as the standard deployable unit their golden paths produce — the
platform's whole value proposition assumes this packaging problem is already solved. **MLOps**
depends on the exact same packaging idea applied to a trained model plus its runtime dependencies,
which is why "just put the model in a container" is usually step one of any real ML deployment
pipeline. **FinOps** cares about containers directly because a container's declared resource
requests/limits are what actually drives cluster-level cost — rightsizing those requests is a
concrete, everyday FinOps practice, not an abstract cost conversation. And **GitOps** controllers
reconcile against container image tags specifically — Topic 9's tagging discipline (`:latest`
going stale, `v1`/`v2` proving rollback) is exactly the mechanism a GitOps tool depends on to know
whether the cluster's current state actually matches what Git says it should be.

**The alternatives.** Podman (daemonless, often rootless, generally considered more secure by
default, uses the same OCI image format so images are largely interchangeable) is the most direct
alternative for building/running containers. Below Docker's own level, **containerd** and
**CRI-O** are the runtimes that actually matter for Kubernetes specifically — and one fact worth
being precise about: **Kubernetes has not run Docker directly since dockershim was removed in
v1.24 (May 2022)**; it talks to a CRI-compliant runtime, in practice usually containerd
(reportedly the default in a large majority of clusters — exact figures vary by source and should
be treated as directional). Docker itself is still the dominant tool for local development and
image-building — and, not coincidentally, modern Docker releases run containerd underneath as
well — it's simply not what a Kubernetes *node* uses to run your containers.

**Production reality.** The non-root user and real production server (gunicorn, not Flask's dev
server) aren't cosmetic — they're precisely the two things a security review or a
production-readiness checklist would flag first.

> **From this repo:** Topic 11's real bug (a `chown -R` after `COPY --from=builder` silently
> duplicating an entire virtual environment into a new image layer via filesystem copy-up, proven
> with a measured 231MB → 204MB fix) is exactly the kind of thing that never shows up in a basic
> tutorial Dockerfile, but absolutely shows up in a real image-size or build-time review once
> someone asks "why is this image so much bigger than it should be."

**Where you'll meet this:** in every CI pipeline that builds an image, and in the first image-size
or security review of one you wrote.

<details>
<summary><b>Check yourself:</b> if Kubernetes doesn't run Docker any more, why learn Docker at all?</summary>

Because Docker still builds the images, and they're standard OCI images that containerd or CRI-O
run unchanged on a Kubernetes node. Docker is also how you run and debug them locally. And a Pod
is a wrapper around containers, so layers, users, ports and storage behave the way Topics 9-11
showed, one level up.
</details>

**Numbers to remember from Part 2:**
- **v1.24 (May 2022)**: the Kubernetes release that removed dockershim; nodes run containerd or
  CRI-O, not Docker.
- **231MB → 204MB**: the image-size fix from removing Topic 11's `chown -R` copy-up bug.

---
