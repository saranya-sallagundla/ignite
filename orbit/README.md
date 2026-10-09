# Orbit — DevOps Capstone Project

This is the real, demo-able DevOps project built alongside the 6-month learning plan in
`../learning/`. It's built incrementally, topic by topic, not written all at once at the end —
so its structure fills in over time rather than existing complete from day one.

## What it will be, end to end
A containerized application, deployed through a CI/CD pipeline, running on Kubernetes, on
infrastructure provisioned by Terraform, with monitoring and alerting in place — all of it running
locally at zero cost (kind while learning and k3s for the finished system, LocalStack for the AWS
services). Each of those pieces gets added as the corresponding phase of the learning plan is
reached. See
[`docs/concept.md`](docs/concept.md) for the specific project concept and architecture.

## How to run it
From `orbit/`: `docker compose up --build`, then verify with `curl http://localhost:5000/health`
(expect `{"status":"ok",...}`). Stop with `docker compose down`.

## Parts

### `app/` — the Flask service everything else deploys
- Status: built · rewritten from first principles in Topics 40-46
- Files: `app.py`, `requirements.txt`, `Dockerfile`, `.dockerignore`
- What was done:
  - Session 13 · Topic 9 — first `app.py`: a Flask app with a `/health` endpoint. First
    Dockerfile written line by line (`FROM` / `WORKDIR` / `COPY` / `RUN` / `CMD`), built as
    `orbit-app`, run on port 5000; `/health` answered `{"status":"ok"}`.
  - Session 14 · Topic 9 — Dockerfile reordered so dependencies install before the code is
    copied: a code-only rebuild dropped from 13.3 s to 2.3 s. Added `/ready`. Images tagged
    `v1` / `v2`, both run side by side to prove rollback.
  - Session 17 · Topic 11 — rebuilt as a multi-stage build: the builder stage creates a
    virtualenv in `/opt/venv`, and the final stage copies only that. Runs as non-root `appuser`,
    served by gunicorn, with `EXPOSE 5000` and a `HEALTHCHECK`. A layer bug (`chown -R` after
    `COPY --from` duplicated the venv) was fixed with `COPY --chown=` — 231 MB → 204 MB.
  - Maintenance — a scan reported three critical CVEs (CVE-2026-8376, CVE-2026-42496,
    CVE-2026-13221) in `perl-base 5.40.1-6`, in the Debian layer of the base image. The fix is
    `5.40.1-6+deb13u1`, which the current `python:3.12-slim` already ships; the image was rebuilt
    on it and checked with `dpkg -s`. The final stage also runs
    `apt-get install --only-upgrade perl-base`, so a build on an older cached base can't regress.
    That layer is 20.5 kB; the image still runs as non-root `appuser`.
  - Maintenance — a Dependabot alert (CVE-2026-27205, low) flagged Flask below 3.1.3: sessions
    didn't add a `Vary: Cookie` header in some access patterns. Bumped to `3.1.3`; rebuilt and
    checked with `importlib.metadata`.
- Installed & used:
  - Docker Desktop 4.58.0 (engine 29.1.5) — builds the image and runs the container
  - `python:3.12-slim` — the base image for both build stages
  - Flask 3.1.3 — the web framework the endpoints are written in
  - gunicorn 23.0.0 — the production server that runs the app, in place of Flask's dev server
  - `perl-base` 5.40.1-6+deb13u1 — the Perl runtime Debian's own tools need (it can't be removed);
    comes with the base image, and the final stage also upgrades it as a safeguard
- Next: Topic 15 adds `tests/`, so CI has something real to run.

### `app/tests/` — not built yet
Application tests, so the CI pipeline has something real to run. Built in Topic 15.

### `docker-compose.yml` — one-command local bring-up
- Status: built
- Files: `docker-compose.yml`
- What was done:
  - Session 16 · Topic 10 — first Compose file: builds and runs `orbit-app` with one command
    instead of manual `docker run` flags. A second service and a named volume were added to
    prove Compose's automatic networking and shared storage, then removed so the committed file
    runs the single `app` service.
  - Session 17 · Topic 11 — pinned to the version-tagged image `orbit-app:2.1`.
- Installed & used:
  - Docker Compose (part of Docker Desktop) — starts the app's containers from one file
- Next: deployment moves onto Kubernetes from Topic 13.

### `k8s/` — Kubernetes manifests
- Status: started · Deployments and Services in Topic 13; config, secrets, Ingress and Helm in 14
- Files: `kind-config.yaml`
- What was done:
  - Session 18 · Topic 12 — `kind-config.yaml` defines a two-node local cluster (one
    control-plane, one worker). Created with `kind create cluster`; `kubectl get nodes` showed
    both roles. Nothing deployed onto it yet.
- Installed & used:
  - kind v0.33.0 (via `winget`) — runs a Kubernetes cluster locally, each node as a Docker container
  - kubectl v1.34.1 (bundled with Docker Desktop) — the command-line client for the cluster's
    API server
- Next: Topic 13 deploys `orbit-app` onto the cluster.

### `k8s/helm/` — not built yet
Helm charts packaging the deployment, once the raw manifests work. Built in Topic 14.

### `argocd/` — not built yet
Argo CD Applications — GitOps delivery of the `k8s/` manifests. Built in Topic 16.

### `ansible/` — not built yet
Configuration-management playbooks. Built in Topic 17.

### `terraform/` — not built yet
AWS-shaped infrastructure, run against LocalStack rather than a live account. Introduced in
Topic 18, deepened in Topics 34-39.

### `terraform/modules/` — not built yet
Reusable modules, factored out of the root configuration once it works. Built in Topic 35.

### `terraform/environments/` — not built yet
Per-environment configuration and workspaces. Built in Topic 36.

### `monitoring/` — not built yet
Prometheus, Grafana and ELK configuration, then distributed tracing and on-call tooling. Built in
Topics 47-51.

### `scripts/` — not built yet
Shell utilities, then Python/Boto3 AWS automation. Shell utilities can land any time; Boto3
automation arrives in Topic 46.

### `docs/` — project concept and architecture
- Status: started
- Files: `concept.md`
- What was done:
  - `concept.md` — the capstone concept (an autonomous SRE agent) and its zero-cost architecture.
    Written alongside the build rather than in one session.
- Next: architecture decisions and runbooks, added as the parts they describe are built.

## Note
- Parts marked "not built yet" have no folder yet — each is created when its topic begins.
- `terraform/environments/` will be named that, not `env/`, so the root `.gitignore`'s
  virtualenv rule can't hide real infrastructure config.
- Topics 1-8 (Phase 1) added no project code, by design — `app/` starts at Topic 9.
