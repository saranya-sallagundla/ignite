# Handbook Status

> Checked off automatically by Claude Code the moment a topic's quiz passes — separate from
> publishing to the handbook site, which the user does manually, on their own timeline.
> Score out of 100: Quiz /40 + Hands-on /30 + Depth of understanding /30, computed fresh per
> topic, with a compact one-line reason on its own line below (end the score line with two
> trailing spaces for a real markdown line break, not a lazy-continuation wrap).
> Site: https://saranya-sallagundla.github.io/ignite/handbook

- [x] 1. Linux Fundamentals — Filesystem, SSH, VMs — **90/100**  
  Quiz 36/40 · Hands-on 27/30 · Depth 27/30 — solved permission & proxy issues solo; VM/container took 2 passes; quiz needed nudges to sharpen vague answers.
- [x] 2. Linux — Top 50 Shell Commands — **84/100**  
  Quiz 34/40 · Hands-on 26/30 · Depth 24/30 — passed attempt 1, but more syntax slips than Topic 1 (`grep -r` placement, `find` scope); strong independent reasoning on the ICMP-vs-TCP firewall discovery.
- [x] 3. Linux — Shell Scripting Basics — **80/100**  
  Quiz 30/40 · Hands-on 28/30 · Depth 22/30 — cleared in 2 attempts; functions didn't land until re-taught via concrete tracing instead of analogy, then passed a full fresh retest cleanly.
- [x] 4. Linux Deep Dive — Process, Log, Disk Management — **88/100**  
  Quiz 34/40 · Hands-on 28/30 · Depth 26/30 — passed attempt 1; excellent hands-on (loop-mounted practice disk, real `fstab` entry) and strong production reasoning on the `df`-timeout scenario; 2 answers needed a follow-up nudge for full precision.
- [x] 5. Linux — Networking Fundamentals — **82/100**  
  Quiz 30/40 · Hands-on 26/30 · Depth 26/30 — first pass (74/100) was kept intentionally light and didn't fully land; a voluntary revision pass with real `curl` verification (refused/no-route/timeout) and a retest raised the score to 82/100 — the official record used here.
- [x] 6. Git Fundamentals — Commits, Branches, Merges — **84/100**  
  Quiz 30/40 · Hands-on 28/30 · Depth 26/30 — passed attempt 1; excellent hands-on including a real merge conflict deliberately set up and resolved via VS Code's UI; 2 of 5 quiz answers needed a real follow-up correction.
- [x] 7. Git Deep Dive — Rebase, Cherry-Pick, Branching Strategies — **82/100**  
  Quiz 28/40 · Hands-on 30/30 · Depth 24/30 — passed attempt 1; excellent hands-on (real rebase conflict, a real conflict-resolution mistake caught and fixed via `git commit --amend`); 3 of 4 quiz answers needed a real follow-up push, one a full redirect.
- [x] 8. GitHub — PRs, Actions Intro, Repo Management — **94/100**  
  Quiz 36/40 · Hands-on 30/30 · Depth 28/30 — passed attempt 1; the richest hands-on session yet (a real self-diagnosed PR mistake fixed via `git log`/`merge-base`, a working GitHub Actions run inspected in full, three genuine branch-protection discoveries); only 1 of 4 quiz answers needed real redirection. **Phase 1 complete.**
- [x] 9. Docker — Architecture, Images, Containers — **86/100**  
  Quiz 32/40 · Hands-on 29/30 · Depth 25/30 — passed attempt 1; Day 2's independent task (Dockerfile layer reorder proved with real build logs, `v1`/`v2` tagging with a live rollback proof, safe `stop`→`rm`→`rmi` cleanup) needed very little steering; quiz had 2 quick one-round clarifications, one real unaddressed gap, and a two-round factual mix-up on exit-code signals; tagging was answered flawlessly.
- [x] 10. Docker — Networking, Volumes, Docker Compose — **92/100**  
  Quiz 36/40 · Hands-on 30/30 · Depth 26/30 — passed attempt 1; exceptional hands-on across both days (real bridge/DNS-resolution proof, bind mount and named volume persistence both proven, a safe duplicate-and-swap technique for updating a running container, and a real multi-service Compose file with a shared volume and automatic networking), all 5 quiz answers correct with genuine reasoning.
- [x] 11. Docker — Multi-Stage Builds & Best Practices — **90/100**  
  Quiz 36/40 · Hands-on 29/30 · Depth 25/30 — passed attempt 1; heavy foundational teaching needed first (compiler/interpreter/WSGI concepts were all new), but real hands-on rigor followed — a genuine bug found and proven (a `chown -R` after `COPY --from` duplicating a layer via copy-up, fixed with `COPY --chown`, verified with a measured before/after size comparison) and independent recovery from a stuck "Created" container state; quiz needed 2 corrections (an interpret/compile word slip, a root-vs-sudo mix-up) but every core mechanism was genuinely understood.
- [ ] 12. Kubernetes — Architecture & Core Concepts
- [ ] 13. Kubernetes — Pods, Deployments, Services
- [ ] 14. Kubernetes — ConfigMaps, Secrets, Ingress, Helm
- [ ] 15. CI/CD — GitHub Actions (CI Pipeline)
- [ ] 16. CI/CD — Argo CD (GitOps Continuous Delivery)
- [ ] 17. Ansible — Configuration Management Fundamentals
- [ ] 18. Terraform — Fundamentals (Intro)
- [ ] 19. SDLC & DevOps Culture
- [ ] 20. AWS Fundamentals — Console, CLI, Regions, AZs
- [ ] 21. IAM — Users, Groups, Policies
- [ ] 22. IAM — Roles, Instance Profiles, STS
- [ ] 23. EC2 — Launch, SSH, Security Groups
- [ ] 24. EC2 — Auto Scaling & Load Balancers
- [ ] 25. VPC — Subnets, Route Tables, Internet Gateway
- [ ] 26. VPC — Security Groups, NACLs, VPC Peering
- [ ] 27. Route 53 — DNS Basics and Routing Policies
- [ ] 28. S3 — Buckets, Policies, Versioning, Lifecycle
- [ ] 29. RDS & DynamoDB — Managed Database Basics
- [ ] 30. ECR & ECS — Container Services
- [ ] 31. EKS — Managed Kubernetes
- [ ] 32. Lambda & Serverless Basics
- [ ] 33. CloudWatch, CloudTrail, AWS Security Basics
- [ ] 34. Terraform State — Local vs Remote, State Locking
- [ ] 35. Terraform Modules — Writing and Consuming
- [ ] 36. Terraform Workspaces & Multi-Region
- [ ] 37. Terraform Provisioners & Null Resources
- [ ] 38. Terraform Drift Detection & Import
- [ ] 39. Terraform at Scale — Best Practices & CI Integration
- [ ] 40. Python Fundamentals — Data Types, Variables, I/O
- [ ] 41. Python — Control Flow: Loops and Conditionals
- [ ] 42. Python — Functions, Error Handling, Modules
- [ ] 43. Python — File I/O and Working with JSON/YAML
- [ ] 44. Python — Dictionaries, Lists, Comprehensions
- [ ] 45. Python — os, subprocess, sys Modules
- [ ] 46. Python — Boto3 for AWS Automation
- [ ] 47. Prometheus — Metrics Collection & Alerting
- [ ] 48. Grafana — Dashboards and Visualization
- [ ] 49. ELK Stack — Log Aggregation Basics
- [ ] 50. OpenTelemetry & Distributed Tracing Concepts
- [ ] 51. Incident Management — PagerDuty + On-Call Patterns
- [ ] 52. AI-Assisted DevOps — Prompt Engineering + AIOps Concepts
- [ ] 53. Local AI & AI Agents Overview (Ollama, CrewAI)
