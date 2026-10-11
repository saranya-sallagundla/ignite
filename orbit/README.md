# Orbit — DevOps Capstone Project

This is the real, demo-able DevOps project built alongside the 6-month learning plan in
`../learning/`. It's built incrementally, topic by topic, not written all at once at the end —
so its structure fills in over time rather than existing complete from day one.

## What it will be, end to end
A containerized application, deployed through a CI/CD pipeline, running on Kubernetes, on
infrastructure provisioned by Terraform, with monitoring and alerting in place — all of it running
locally at zero cost (k3s for Kubernetes, LocalStack for the AWS services). Each of those pieces
gets added as the corresponding phase of the learning plan is reached. See
[`docs/concept.md`](docs/concept.md) for the specific project concept and architecture.

## Folder guide
- `app/` — the Flask service everything else deploys. Rewritten from first principles in Phase 5
  (Python, Topics 40-46).
- `k8s/` — Kubernetes manifests: Deployments, Services, ConfigMaps, Secrets, Ingress, Helm charts.
- `argocd/` — Argo CD Application definitions and GitOps delivery configuration.
- `terraform/` — Terraform configuration for the project's AWS-shaped infrastructure, run against
  LocalStack rather than a live account.
- `ansible/` — configuration management playbooks.
- `monitoring/` — Prometheus, Grafana, and ELK stack configuration for observability.
- `docs/` — the project concept, architecture decisions, and runbooks as they are written.
- `scripts/` — automation scripts, including Python/Boto3 AWS automation.

Other than `app/` and `docs/`, every folder above is currently a placeholder — each holds a short
README naming the phase/topic that will populate it.

## How to run it
From `orbit/`: `docker compose up --build`, then verify with `curl http://localhost:5000/health`
(expect `{"status":"ok",...}`). Stop with `docker compose down`.

## Status
`app/` serves a Flask service (`/health`, `/ready`) from a multi-stage, non-root image running
gunicorn, with a HEALTHCHECK and a version-tagged image (`orbit-app:2.1`) brought up by
`docker-compose.yml`. Phase 1 is complete; Phase 2 (Containers, Kubernetes & CI/CD) is underway —
Topics 9-11 (Docker) are cleared, with Kubernetes (12-14), CI/CD (15-16), Ansible (17) and
Terraform's introduction (18) still ahead in this same phase. Terraform is deepened in Phase 4 and
observability follows in Phase 6.

## Build log

### Sessions 1-12 — 2026-07-06 to 2026-07-19
Phase 1 (Linux, Git & Version Control), Topics 1-8 — no project code yet, by design: `app/` is
written at Topic 9, where Docker begins. The Linux, networking and Git work from this phase is
what later operates, versions and troubleshoots everything below.

### Session 13 — 2026-07-20
Topic 9 Day 1 (Docker — Architecture, Images, Containers) — `app/` gained its first real code, a
Flask app with a `/health` endpoint, and its first Dockerfile, built into
`orbit-app:latest` and run as a live container, verified serving `{"status":"ok"}`
over HTTP.

### Session 14 — 2026-07-21
Topic 9 complete, quiz passed (Docker — Architecture, Images, Containers) — Dockerfile reordered
so app-code changes no longer force an unnecessary dependency reinstall (proved with real build
timings), `app/` gained a `/ready` endpoint, and the image is now properly version-tagged
(`v1`/`v2`) with rollback proven by running both simultaneously.

### Session 15 — 2026-07-22
Topic 10 Day 1 (Docker — Networking, Volumes, Docker Compose) — no project code yet, but
container-to-container DNS resolution (bridge vs. custom network) and bind-mount persistence
proven hands-on today are exactly what this project's future multi-container setups (app +
database, app + cache) will depend on.

### Session 16 — 2026-07-23
Topic 10 complete, quiz passed (Docker — Networking, Volumes, Docker Compose) — `orbit/` gained
its first `docker-compose.yml`, building and running `orbit-app` in one command instead
of manual `docker run` flags, extended with a second service to prove Compose's automatic
networking and a named volume for shared persistence. Both were lesson-scoped demonstrations and
were removed during the Topic 10 audit cleanup — the committed file runs the single `app` service.

### Session 17 — 2026-07-24
Topic 11 complete, quiz passed (Docker — Multi-Stage Builds & Best Practices) — `app/`'s Dockerfile
rewritten as a real multi-stage, non-root build running gunicorn instead of Flask's dev server,
with a healthcheck and a properly tagged image (`orbit-app:2.1`) in
`docker-compose.yml`; a real image-size bug (a `chown -R` after `COPY --from` duplicating a layer)
was found and fixed with a measured before/after proof.
