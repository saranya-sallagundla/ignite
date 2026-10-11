# Capstone Concept — Autonomous SRE Agent + Orbit Control

> **Status: current working idea, not a locked decision.** Revisit once the underlying skills
> (Kubernetes, Terraform, Python, observability) are all in place, and decide then whether to
> keep building this or replace it, informed by everything learned by that point.

## What it is
A local AI agent (Ollama + CrewAI, Phase 7) watches Prometheus/Grafana/ELK signals (Phase 6) on
a running containerized app. When something breaks, it diagnoses root cause by correlating
metrics, logs, traces, and recent deploys, then either auto-remediates via Boto3 (Phase 5) or
escalates with an auto-written incident report.

The whole thing is wrapped in a live "Orbit Control" dashboard — a node-graph visualization
showing an incident being detected, diagnosed, and resolved in real time. Chosen specifically so
the demo lands with both technical and non-technical audiences (live demos and walkthroughs).

## Zero-cost architecture
To guarantee the project costs nothing regardless of AWS Free Tier limits, the pieces that are
**not** actually free even on Free Tier (EKS control plane, Load Balancer, NAT Gateway, Route 53)
are avoided entirely:
- Kubernetes runs locally via **k3s/kind** instead of EKS.
- The project's own AWS-shaped infrastructure (S3, Lambda, DynamoDB, IAM, CloudWatch, SQS/SNS)
  runs against **LocalStack** (a Docker-hosted AWS API emulator) instead of a live account —
  identical Terraform/Boto3/CLI code, pointed at localhost.

Phase 3's hands-on AWS learning (Topics 20-33) still uses a real personal AWS account for the
services that genuinely are free (EC2, S3, Lambda, IAM, basic CloudWatch) — only the capstone's
own deployed infrastructure moves to LocalStack/k3s, since that's where the non-free services
would otherwise be required.

This also keeps the project portable and independent of any single environment or account: since
the live project runs on LocalStack/k3s (no cloud account of any kind involved), only code would
ever need to move to a personal GitHub repo.

## Development environment safety net (deferred)
This project's local compute is tied to a single machine today. **GitHub Codespaces** is the
planned fallback: a free monthly quota (120 core-hours — about 60 hours on a 2-core machine — plus
15 GB storage/month on a personal account) that runs Docker-based dev environments from any
browser, so k3s/LocalStack/Ollama could run entirely inside Codespaces with no local install
needed.

Codespaces would run against a personal GitHub account and a personal mirror of this repo — the
same portability move already described above.

**Not set up yet, on purpose** — deferred to the same milestone as this document's own
capstone-idea revisit above.

## Supersedes
This concept supersedes an earlier "learning progress tracker" idea (modeling this repo's own
tracking system as a deployable app), which was considered and dropped early on, before the
project's first container existed.
