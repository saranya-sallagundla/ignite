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

**Extra Reserve Buffer**: 5 days — depth on weak topics, harder quizzes, project hardening, system design. Not new tools.

---

## Pacing Layer (LIVING — only section that changes)

- **Day 1**: 2026-07-06 (IST, UTC+5:30). All dates and calendar-day counts below use IST
  regardless of the timezone Claude Code's host machine defaults to.
- **Outer deadline**: 6 months from Day 1 (~2027-01-06). The baseline above sums to ~120 days —
  the remaining ~60 are deliberate slack for the 3-attempt mastery rule and project polish.
  Using that slack is normal; it does not count as falling behind.
- **Last recalibrated**: 2026-08-31 — triggered by the 5+ days behind rule, which had in fact
  fired weeks earlier and gone unacted-on while this layer sat stale (see Notes). The staleness
  check that now catches this lives in `CLAUDE.md`'s "Every session, before anything else."
- **Calendar Day since Day 1**: 57 (2026-08-31), of a 184-day total span to the outer deadline
- **Session count completed**: 17 teaching sessions. Non-teaching sessions (audits on 2026-08-13,
  2026-08-26 and 2026-08-31) are deliberately not counted here — they don't advance the roadmap —
  but they are why the 37-day teaching gap below went unnoticed for so long: sessions were
  happening, just not ones the old staleness check was scoped to look at.
- **Active calendar days**: 17 of 57 — a day counts active if a session's heading is dated that
  day (matching the rule that Session/Day headings show only the start date). Inside the first 20
  days there were 3 gaps (2026-07-15, 2026-07-17, 2026-07-25), each a calendar day touched only by
  a session's past-midnight spillover with no new session starting on it. The remaining 37
  (2026-07-25 → 2026-08-31) are the unplanned absence recorded in Notes.
- **Roadmap days used**: 19 of 98 **core** days (Topics 1-11 complete, per fixed baseline
  allocation) — 79 core days remain. Stated against the 98-day core figure deliberately, not
  against the 120-day total: 120 includes the 22 buffer days tracked separately below, so
  "19 of 120" mixed two different bases and could never diverge from the baseline, making it
  useless as a pace signal.
- **Topic state**: Topic 11 — COMPLETE (90/100). Next: Topic 12 (Kubernetes — Architecture &
  Core Concepts).
- **Pace**: **behind — roughly 11 core days.** 30% of the calendar span is consumed (Day 57 of
  184) against 19% of the core work delivered (19 of 98 days); a linear pace would have ~30 core
  days done by now. Honest and not alarming: the deadline still fits (see Slack), but the comfort
  margin it used to have is gone.
- **Slack remaining**: **27 of 64 days.** 128 calendar days remain to 2027-01-06 against 101
  roadmap days still to spend (79 core + 22 buffer). Cross-checks the other way too: 64 days of
  starting slack minus the 37-day absence = 27. This — not "Buffer used" — is now the binding
  constraint, and it is the number to watch. One more absence of the same size would consume it
  outright and start moving the 6-month date.
- **Buffer used** (the 22-day pool inside the baseline): 0 of 22 — genuinely untouched. Per
  `CLAUDE.md`, this figure moves only when a reserve day funds a deferred-mastery revisit or a
  topic overruns its allotted days; neither has happened (no deferred-mastery topics, and Topics
  1-11 landed at exactly their allotted 19 days, zero overrun). The 37-day absence drew on the
  separate slack pool above, which is why this line correctly still reads 0 — the two pools are
  not interchangeable, and conflating them would hide the real signal.
- **Buffer used per phase**: informational only, see note below.
    - `Phase 1 (Linux, Git & Version Control)`: 0 of 3 — not used
    - `Phase 2 (Containers, Kubernetes & CI/CD)`: 0 of 3 — not used
    - `Phase 3 (AWS Cloud Platform)`: 0 of 4 — not started yet
    - `Phase 4 (Terraform Deep Dive)`: 0 of 2 — not started yet
    - `Phase 5 (Python for DevOps)`: 0 of 2 — not started yet
    - `Phase 6 (Observability)`: 0 of 2 — not started yet
    - `Phase 7 (AI for DevOps)`: 0 of 1 — not started yet
    - Note: the 22-day pool above is shared across all phases, not siloed — this breakdown just
      shows where any usage happened, not a separate limit per phase. The 7 figures sum to 17,
      matching each phase's own buffer count in the fixed baseline table — not 22; the remaining
      5 days are the cross-cutting "Extra Reserve Buffer" from the baseline's closing note, not
      tied to any single phase. The baseline table's own "+N buffer" wording per phase is kept
      as-is but should not be read as a phase-locked limit — this note is the authoritative
      interpretation, matching `CLAUDE.md`'s rule.
- **Notes** (pacing-relevant items only — deferrals and phase transitions; full topic narrative
  lives in `progress.md`'s session log and each topic's notebook, not here):
  - **Unplanned absence, 2026-07-25 → 2026-08-31 (37 days), no teaching sessions.** Reason not
    recorded here by design — this is a public repo and the Light Days rule exists to keep the
    *pacing trade-off* visible, which a neutral entry does just as well. Pacing cost, stated
    plainly: 37 days drawn from the 64-day slack pool, leaving 27. This is the single largest
    pacing event of the mission so far and the reason Pace moved from "on track" to "behind."
    Logged here rather than in the Light Days table because that table is for single claimed days,
    not a multi-week gap.
  - **Why it wasn't caught sooner** (kept as a pacing note because it's a process fact, not a
    topic one): this layer read `Pace: on track` and `Last recalibrated: — (not yet due)`
    throughout the absence, so the file actively asserted the opposite of the truth. Three audits
    ran during it; the first flagged the drift on 2026-08-13, and it still went unrecalibrated for
    another 18 days. Root cause was that the staleness check was scoped to teaching sessions only.
    Fixed 2026-08-31 — see `CLAUDE.md`'s "Every session, before anything else."
  - Phase 1 (Linux, Git & Version Control) is now fully complete. Phase 2 (Containers,
    Kubernetes & CI/CD) is now underway.
  - SSH hands-on (local sshd) still deferred — corporate network/proxy blocks outbound WSL
    traffic; retry via AWS sandbox VM once access is ready.
- **Recalibration verdict, 2026-08-31**: the remaining roadmap still fits the 6-month deadline
  without changing the fixed baseline — 101 roadmap days of work against 128 calendar days. No
  topics dropped, no day allocations altered, nothing rescheduled. What has changed is the margin:
  slack is down from 64 days to 27, so the plan is no longer robust to another long gap the way it
  was in July. Two honest options if another absence happens: accept the 6-month date moving, or
  compress by using the 22-day buffer pool for real overruns only and keeping single-day light
  days rare. Next routine check-in at session 37 (20 sessions after the last), or immediately if
  Pace slips another 5 days — whichever comes first.
