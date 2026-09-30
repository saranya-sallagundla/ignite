# The project

This is the real, demo-able DevOps project built alongside the 6-month learning plan in
`../learning/`. It's built incrementally, topic by topic, not written all at once at the end —
so its structure fills in over time rather than existing complete from day one.

## What it will be, end to end
A containerized application, deployed through a CI/CD pipeline, running on Kubernetes, on
infrastructure provisioned by Terraform, with monitoring and alerting in place. Each of those
pieces gets added as the corresponding phase of the learning plan is reached. See
[`docs/concept.md`](docs/concept.md) for the specific project concept and architecture.

## Folder guide
- `app/` — the application itself. Until the Python phase of the learning plan, code here is
  Claude-authored boilerplate — functional, but not yet something to defend in an interview.
  It gets rewritten from real understanding once Python is covered, and this note gets removed
  once that happens.
- `k8s/` — Kubernetes manifests: Deployments, Services, ConfigMaps, Secrets, Ingress, Helm charts.
- `terraform/` — Terraform configuration provisioning the AWS infrastructure this runs on.
- `ansible/` — configuration management playbooks.
- `monitoring/` — Prometheus, Grafana, and ELK stack configuration for observability.
- `docs/` — architecture decisions and runbooks, written as the project grows.
- `scripts/` — automation scripts, including Python/Boto3 AWS automation.

## How to run it
Filled in here once there's an application to actually run.

## Status
`app/` has a Flask boilerplate (`/health`, `/ready` endpoints) and a properly-layered Dockerfile,
built, tagged (`v1`/`v2`), and run as real containers with proven rollback. 14 learning sessions
in, Phase 1 complete and Topic 9 (Docker: Architecture, Images, Containers) cleared; check
`../learning/progress.md` for current progress through the learning plan, which drives what gets
added here next.

### Session 1 — 2026-07-06
Day 1 of Topic 1 (Linux Fundamentals) — no project code changes yet, this phase is foundational
Linux/SSH/VM learning ahead of Docker (Topic 9), where `app/` boilerplate gets written first.

### Session 2 — 2026-07-07
Topic 1 complete (quiz passed) — still no project code yet, but the VM/container isolation
reasoning covered here directly informs why this project's future architecture runs containers
on EC2 (VMs) rather than bare metal, once Topics 9+ (Docker) and 20+ (AWS) are reached.

### Session 3 — 2026-07-08
Topic 2 Day 1 (Top 50 Shell Commands) — no project code yet, still pre-Docker. The
`grep | cut | sort | uniq -c | sort -nr | head` log-analysis pipeline practiced here is directly
reusable later for real log triage once `monitoring/` and actual app logs exist.

### Session 4 — 2026-07-09
Topic 2 complete (quiz passed) — no project code yet, but `ps`/`kill`/signals, `df`/`du`/`free`,
and `tar` are exactly the toolkit for operating this project's future EC2 instances and
Kubernetes nodes day-to-day, once Topics 20+ (AWS) and 12+ (Kubernetes) are reached.

### Session 5 — 2026-07-10
Topic 3 Day 1 (Shell Scripting Basics) — no project code yet, but this is the first topic that
feeds `scripts/` directly: the conditional/variable fundamentals practiced today are exactly
what real automation scripts in that folder will be built from.

### Session 6 — 2026-07-11 / 2026-07-12
Topic 3 complete (quiz cleared in 2 attempts) — no project code yet, but the `checkall.sh`
pattern built today (function + loop + exit code, checking multiple folders at once) is directly
the shape of a real pre-deployment sanity-check script for `scripts/` later.

### Session 7 — 2026-07-12
Topic 4 Day 1 (Process/Log/Disk Management) — no project code yet, but `journalctl`/`/var/log`
log-searching skills practiced today are exactly what `monitoring/`'s future log aggregation
setup will build on, and `nice`/`renice` will matter once real workloads run on shared EC2/K8s
compute later.

### Session 8 — 2026-07-13 / 2026-07-14
Topic 4 complete, quiz passed (Process/Log/Disk Management) — no project code yet, but disk
partitioning/mounting and `fsck`/`df` health checks practiced today are exactly what operating
this project's future EC2 storage and EKS persistent volumes will require later.

### Session 9 — 2026-07-14 / 2026-07-16
Topic 5 complete, quiz passed (Linux Networking Fundamentals) — no project code yet, but IP/CIDR,
DNS, ports, and routing practiced today are exactly what configuring this project's future VPC,
security groups, and service-to-service networking on AWS will require later.

### Session 10 — 2026-07-16
Topic 6 complete, quiz passed (Git Fundamentals) — no project code yet, but branching/merging
practiced today (incl. a real resolved conflict) is exactly the workflow this project's own repo
will use once multiple features/phases are being built and merged going forward.

### Session 11 — 2026-07-18 / 2026-07-19
Topic 7 complete, quiz passed (Git Deep Dive) — no project code yet, but rebase/cherry-pick and
branching-strategy reasoning practiced today are exactly what keeping this project's own repo
history clean will require once real feature work starts landing here.

### Session 12 — 2026-07-19 / 2026-07-20
Topic 8 complete, quiz passed (GitHub: PRs, Actions, Repo Management) — **Phase 1 complete.** No
project code yet, but PRs, GitHub Actions, and branch protection practiced today are exactly the
workflow this project's own repo will use for CI/CD once Phase 2 (Docker/Kubernetes/CI-CD) begins.

### Session 13 — 2026-07-20 / 2026-07-21
Topic 9 Day 1 (Docker: Architecture, Images, Containers) — `app/` got its first real code (Flask
+ `/health`) and its first Dockerfile, built into `mission-control-app:latest` and run as a live
container, verified serving `{"status":"ok"}` over HTTP. Day 2 still ahead before Topic 9 clears.

### Session 14 — 2026-07-21 / 2026-07-22
Topic 9 Day 2 — Dockerfile reordered so app-code changes no longer force an unnecessary dependency
reinstall (proved with real build timings), `app/` gained a `/ready` endpoint, and the image is now
properly version-tagged (`v1`/`v2`) with rollback proven by running both simultaneously. **Topic 9
CLEARED, 86/100.**
