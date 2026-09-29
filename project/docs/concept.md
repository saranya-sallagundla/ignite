# Capstone Concept — Autonomous SRE Agent + Mission Control

> **Status: current working idea, not a locked decision.** This is the vehicle used to drive
> hands-on learning through the roadmap. Revisit at the end of the learning journey (all 53
> topics complete) and decide then whether to keep building this or replace it, informed by
> everything learned by that point.

## What it is
A local AI agent (Ollama + CrewAI, Phase 7) watches Prometheus/Grafana/ELK signals (Phase 6) on
a running containerized app. When something breaks, it diagnoses root cause by correlating
metrics, logs, traces, and recent deploys, then either auto-remediates via Boto3 (Phase 5) or
escalates with an auto-written incident report.

The whole thing is wrapped in a live "Mission Control" dashboard — a node-graph visualization
showing an incident being detected, diagnosed, and resolved in real time. Chosen specifically so
the demo lands with both technical and non-technical audiences (onsite interviews).

## Zero-cost architecture
To guarantee the project costs nothing regardless of AWS Free Tier limits, the pieces that are
NOT actually free even on Free Tier (EKS control plane, Load Balancer, NAT Gateway, Route 53) are
avoided entirely:
- Kubernetes runs locally via **k3s/kind** instead of EKS.
- The project's own AWS-shaped infrastructure (S3, Lambda, DynamoDB, IAM, CloudWatch, SQS/SNS)
  runs against **LocalStack** (a Docker-hosted AWS API emulator) instead of a live account —
  identical Terraform/Boto3/CLI code, pointed at localhost.

Phase 3's hands-on AWS learning (Topics 20-33) still uses a real personal AWS account for the
services that genuinely are free (EC2, S3, Lambda, IAM, basic CloudWatch) — only the capstone's
own deployed infrastructure moves to LocalStack/k3s, since that's where the non-free services
would otherwise be required.

This also resolves the org-vs-personal-account portability question: since the live project runs
on LocalStack/k3s (no cloud account of any kind involved), nothing tied to an account needs to
move if the org repo is deleted — only code moves to a personal GitHub repo.

## Supersedes
An earlier "learning progress tracker" idea (modeling this repo's own tracking system as a
deployable app), considered and dropped before Topic 9 began.
