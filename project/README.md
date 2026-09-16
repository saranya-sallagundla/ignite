# The project

This is the real, demo-able DevOps project built alongside the 6-month learning plan in
`../learning/`. It's built incrementally, topic by topic, not written all at once at the end —
so its structure fills in over time rather than existing complete from day one.

## What it will be, end to end
A containerized application, deployed through a CI/CD pipeline, running on Kubernetes, on AWS
infrastructure provisioned by Terraform, with monitoring and alerting in place. Each of those
pieces gets added as the corresponding phase of the learning plan is reached.

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
Day 0 — folders scaffolded, nothing built yet. Check `../learning/progress.md` for current
progress through the learning plan, which drives what gets added here next.

### Session 1 — 2026-07-06
Day 1 of Topic 1 (Linux Fundamentals) — no project code changes yet, this phase is foundational
Linux/SSH/VM learning ahead of Docker (Topic 9), where `app/` boilerplate gets written first.

### Session 2 — 2026-07-07
Topic 1 complete (quiz passed) — still no project code yet, but the VM/container isolation
reasoning covered here directly informs why this project's future architecture runs containers
on EC2 (VMs) rather than bare metal, once Topics 9+ (Docker) and 20+ (AWS) are reached.
