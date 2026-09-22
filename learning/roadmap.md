# Roadmap

> Source: DevOps/SRE Project Preferences, Section 16.
> The baseline below is FIXED — never edited during recalibration.
> Only the "Pacing Layer" section at the bottom changes.

## Fixed Baseline — 53 Topics, 120 Days

### Phase 1 — Linux, Git & Version Control (8 topics, 17 days: 14 + 3 buffer)
| # | Topic | Days | Type |
|---|---|---|---|
| 1 | Linux Fundamentals — Filesystem, SSH, VMs | 2 | Core |
| 2 | Linux — Top 50 Shell Commands | 2 | Core |
| 3 | Linux — Shell Scripting Basics | 2 | Core |
| 4 | Linux Deep Dive — Process, Log, Disk Management | 2 | Core |
| 5 | Linux — Networking Fundamentals | 2 | Core |
| 6 | Git Fundamentals — Commits, Branches, Merges | 2 | Core |
| 7 | Git Deep Dive — Rebase, Cherry-Pick, Branching Strategies | 1 | Core |
| 8 | GitHub — PRs, Actions Intro, Repo Management | 1 | Core |

### Phase 2 — Containers, Kubernetes & CI/CD (11 topics, 24 days: 21 + 3 buffer)
| # | Topic | Days | Type |
|---|---|---|---|
| 9 | Docker — Architecture, Images, Containers | 2 | Core |
| 10 | Docker — Networking, Volumes, Docker Compose | 2 | Core |
| 11 | Docker — Multi-Stage Builds & Best Practices | 1 | Core |
| 12 | Kubernetes — Architecture & Core Concepts | 2 | Core |
| 13 | Kubernetes — Pods, Deployments, Services | 2 | Core |
| 14 | Kubernetes — ConfigMaps, Secrets, Ingress, Helm | 2 | Core |
| 15 | CI/CD — GitHub Actions (CI Pipeline) | 2 | Core |
| 16 | CI/CD — Argo CD (GitOps Continuous Delivery) | 2 | Core |
| 17 | Ansible — Configuration Management Fundamentals | 2 | Core |
| 18 | Terraform — Fundamentals (Intro) | 2 | Core |
| 19 | SDLC & DevOps Culture | 2 | Core |

### Phase 3 — AWS Cloud Platform (14 topics, 28 days: 24 + 4 buffer)
| # | Topic | Days | Type |
|---|---|---|---|
| 20 | AWS Fundamentals — Console, CLI, Regions, AZs | 1 | Core |
| 21 | IAM — Users, Groups, Policies | 2 | Core |
| 22 | IAM — Roles, Instance Profiles, STS | 2 | Core |
| 23 | EC2 — Launch, SSH, Security Groups | 2 | Core |
| 24 | EC2 — Auto Scaling & Load Balancers | 2 | Core |
| 25 | VPC — Subnets, Route Tables, Internet Gateway | 2 | Core |
| 26 | VPC — Security Groups, NACLs, VPC Peering | 2 | Core |
| 27 | Route 53 — DNS Basics and Routing Policies | 1 | Core |
| 28 | S3 — Buckets, Policies, Versioning, Lifecycle | 2 | Core |
| 29 | RDS & DynamoDB — Managed Database Basics | 1 | Advanced |
| 30 | ECR & ECS — Container Services | 2 | Core |
| 31 | EKS — Managed Kubernetes | 2 | Core |
| 32 | Lambda & Serverless Basics | 1 | Advanced |
| 33 | CloudWatch, CloudTrail, AWS Security Basics | 2 | Core |

### Phase 4 — Terraform Deep Dive (6 topics, 15 days: 13 + 2 buffer)
| # | Topic | Days | Type |
|---|---|---|---|
| 34 | Terraform State — Local vs Remote, State Locking | 2 | Core |
| 35 | Terraform Modules — Writing and Consuming | 3 | Core |
| 36 | Terraform Workspaces & Multi-Region | 2 | Core |
| 37 | Terraform Provisioners & Null Resources | 1 | Advanced |
| 38 | Terraform Drift Detection & Import | 2 | Core |
| 39 | Terraform at Scale — Best Practices & CI Integration | 3 | Core |

### Phase 5 — Python for DevOps (7 topics, 16 days: 14 + 2 buffer)
| # | Topic | Days | Type |
|---|---|---|---|
| 40 | Python Fundamentals — Data Types, Variables, I/O | 2 | Core |
| 41 | Python — Control Flow: Loops and Conditionals | 1 | Core |
| 42 | Python — Functions, Error Handling, Modules | 2 | Core |
| 43 | Python — File I/O and Working with JSON/YAML | 2 | Core |
| 44 | Python — Dictionaries, Lists, Comprehensions | 1 | Core |
| 45 | Python — os, subprocess, sys Modules | 2 | Core |
| 46 | Python — Boto3 for AWS Automation | 4 | Core |

### Phase 6 — Observability (5 topics, 12 days: 10 + 2 buffer)
| # | Topic | Days | Type |
|---|---|---|---|
| 47 | Prometheus — Metrics Collection & Alerting | 2 | Core |
| 48 | Grafana — Dashboards and Visualization | 2 | Core |
| 49 | ELK Stack — Log Aggregation Basics | 2 | Core |
| 50 | OpenTelemetry & Distributed Tracing Concepts | 2 | Advanced |
| 51 | Incident Management — PagerDuty + On-Call Patterns | 2 | Advanced |

### Phase 7 — AI for DevOps (2 topics, 3 days: 2 + 1 buffer)
| # | Topic | Days | Type |
|---|---|---|---|
| 52 | AI-Assisted DevOps — Prompt Engineering + AIOps Concepts | 1 | Advanced |
| 53 | Local AI & AI Agents Overview (Ollama, CrewAI) | 1 | Advanced |

**Extra Reserve Buffer:** 5 days — depth on weak topics, harder quizzes, project hardening, system design. Not new tools.

---

## Pacing Layer (LIVING — only section that changes)

- Day 1: 2026-07-06 (IST, UTC+5:30). All dates and calendar-day counts below use IST regardless
  of the timezone Claude Code's host machine defaults to.
- Outer deadline: 6 months from Day 1 (~2027-01-06). The baseline above sums to ~120 days —
  the remaining ~60 are deliberate slack for the 3-attempt mastery rule and project polish.
  Falling into that slack is normal, not falling behind.
- Last recalibrated: — (not yet due — 8 sessions completed)
- Calendar Day since Day 1: 9 (2026-07-14)
- Session count completed: 8
- Current topic: Topic 4 — COMPLETE (88/100). Topic 5 — Linux Networking Fundamentals not yet
  started.
- Pace: on track
- Buffer used: 0 of 22
- Notes: Topics 1-4 all cleared (90/100, 84/100, 80/100, 88/100). Topic 4 Day 2 covered
  partitions/mounting, a loop-mounted practice disk built end-to-end, `fsck`/`df` distinction
  (incl. a real production `df`-timeout alert correctly reasoned through), and a persistent
  `/etc/fstab` entry written independently and verified via `mount -a`. SSH hands-on (local sshd)
  still deferred — corporate network/proxy blocks outbound WSL traffic; retry via AWS sandbox VM
  once access is ready.
