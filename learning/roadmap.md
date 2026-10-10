# Roadmap

> Source: DevOps/SRE Project Preferences, Section 16.
> The baseline below is the plan of record and is not touched by recalibration — only the
> "Pacing Layer" at the bottom moves. Changing the baseline itself is a deliberate decision;
> see [`rules.md`](../rules.md) §5.

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

**Extra Reserve Buffer**: 5 days — depth on weak topics, harder quizzes, project hardening, system design. Not new tools.

---

## Pacing Layer (LIVING — only section that changes)

- **Day 1**: 2026-09-14 (IST, UTC+5:30). All dates and day counts use IST, regardless of the
  machine's time zone.
- **Outer deadline**: 2027-03-14, 6 months from Day 1. The plan needs about 120 days. The other ~60
  are spare time for retries and project polish. Using spare time is normal, not falling behind.
- **Last recalibrated**: not yet due. Due at Session 20, or as soon as Pace shows 5+ days behind
  (`rules.md` §6). The check runs every session (`rules.md` §2).
- **Today**: Day 26 of 181 (2026-10-09).
- **Session**: 18 teaching sessions completed. Audits aren't counted, as they don't advance the
  roadmap.
  - **Active days**: 19 of 22 (through Session 18, 2026-10-05). A day is active if a session ran on
    it.
  - **Inactive**: 2026-09-25 (light day), 2026-10-03 to 2026-10-04.
- **Roadmap days used**: 19 of 98 **core days**, so 79 remain. This counts against the 98 core days,
  not the 120-day total, because the 120 includes the 22 buffer days tracked below.
- **Topic state**: Topic 11 complete (90/100). Topic 12 (Kubernetes — Architecture & Core Concepts):
  day 1 of 2 done (architecture taught, local 2-node `kind` cluster verified). Day 2 and the quiz
  are next.
- **Pace**: About 5 days ahead of plan.
  - *Done so far*: 19 days of topics (Topics 1 to 11).
  - *Expected by today (Day 26)*: about 14 days.
  - *Spare days used so far*: 5.
  - *Watch point*: if no new topic is finished by Day 45 (2026-10-28), the plan falls 5 days behind
    and gets recalibrated.
- **Slack remaining**: 56 of 61 days. There are 156 days left until the deadline (2027-03-14), and
  100 days of work left.
- **Buffer used**: 0 of 22. Per `rules.md` §6, it moves only when a buffer day pays for a
  deferred-topic revisit or a topic overruns its allotted days. Neither has happened. Inactive days
  come out of spare time, not the buffer.
- **Buffer used per phase**:
    - `Phase 1 (Linux, Git & Version Control)`: 0 of 3, not used
    - `Phase 2 (Containers, Kubernetes & CI/CD)`: 0 of 3, not used
    - `Phase 3 (AWS Cloud Platform)`: 0 of 4, not started yet
    - `Phase 4 (Terraform Deep Dive)`: 0 of 2, not started yet
    - `Phase 5 (Python for DevOps)`: 0 of 2, not started yet
    - `Phase 6 (Observability)`: 0 of 2, not started yet
    - `Phase 7 (AI for DevOps)`: 0 of 1, not started yet
    - Note: the 22-day pool is shared by all phases. This list only shows where any usage happened.
      The 7 figures add up to 17, matching each phase's buffer in the baseline table. The other 5
      days are the "Extra Reserve Buffer" from the baseline's closing note, not tied to any phase.
      Read each phase's "+N buffer" in the baseline the same way: a share of one pool, not a locked
      limit (`rules.md` §6).
- **Notes** (pacing items only; the full story is in `progress.md` and the notebooks):
  - Updated 2026-10-09 in a maintenance session, not a recalibration.
  - SSH hands-on (local sshd) is still deferred. The corporate network blocks outbound WSL traffic.
    Retry on an AWS sandbox VM once access is ready.
- **Recalibration verdict**: none yet. The roadmap fits the deadline with 56 days of slack.
