# DevOps/SRE Field Atlas

> A living reference, not a session log. `progress.md` tracks *what happened and when*; the
> per-topic notebooks under `notes/` capture *the hands-on teaching detail*. This file is
> different: it's the connected map of the field itself — what each piece actually is, why it
> exists, how it connects to everything else, and where the field is moving. One file, always
> current, never forked into a v2.
>
> **A note on currency**: anywhere a claim is about something fast-moving (adoption numbers, what
> counts as "standard" right now, tool version behavior), it's marked with a confidence level and,
> where possible, a source. Verified 2026-07-29, re-verified 2026-08-31 via live web research —
> see the confidence notes inline. Treat percentages from secondary/blog sources as directional,
> not precise.
>
> **Last sub-discipline check: 2026-08-31** (IST). Automated daily scheduling isn't available
> (Claude Code routines are disabled at the organization level), so this is checked manually —
> `CLAUDE.md`'s Daily session shape reminds the user to trigger a check if this date isn't today.

---

## Table of Contents

**Part 1 — The Field, Right Now**
- [1.1 What DevOps and SRE Actually Mean Today](#11-what-devops-and-sre-actually-mean-today)
- [1.2 What's Changed Recently](#12-whats-changed-recently)
- [1.3 A Real Day in the Life](#13-a-real-day-in-the-life)
- [1.4 The Real Skill Stack](#14-the-real-skill-stack)
- [1.5 The Sub-Disciplines That Have Branched Off](#15-the-sub-disciplines-that-have-branched-off)

**Part 2 — Topics Covered So Far**
- [Linux](#linux)
- [Git](#git)
- [GitHub](#github)
- [Docker](#docker)

**Part 3 — What Comes Next**
- [Maintenance Rules](#maintenance-rules)

---

## Part 1 — The Field, Right Now

### 1.1 What DevOps and SRE Actually Mean Today

Forget the 2015 *Phoenix Project* image of "developers and ops merge into one happy team that
does everything together." That's not what happened at scale. What actually happened is
specialization re-formed around new lines.

Most engineering orgs past a certain size now have some combination of: a **Platform team**
(builds the internal tooling/paved road other engineers use — CI/CD templates, a self-service way
to spin up infra, a service catalog), an **SRE team** (owns production reliability for specific
services, with actual numeric targets), and **embedded DevOps/infra engineers** sitting inside
product teams (own that team's pipelines, cloud resources, and deploy process specifically).
"DevOps engineer" as a job title still exists constantly in postings, but it usually means
"whoever on this team owns the infra/CI/CD/cloud stuff," not "a person who has abolished the
boundary between writing code and running it."

**SRE (Site Reliability Engineering)** is Google's specific, more rigorous formalization of
similar ideas, and it's the one with an actual measurement discipline attached: **SLOs**
(Service Level Objectives — a target like "99.9% of requests succeed in under 300ms"), **error
budgets** (the allowed amount of unreliability before it's spent — burn through it, and new
feature releases get paused in favor of reliability work), and blameless postmortems as a formal,
required practice, not just a nice idea. Where DevOps is closer to a culture-plus-toolchain
description of a role, SRE is a specific operating model with numbers attached that actually gate
what a team is allowed to ship.

In practice, most companies are not "pure DevOps" or "pure SRE" — they borrow whichever pieces
solve their actual pain: a startup adopts DevOps culture and CI/CD without ever writing a formal
SLO; a larger company runs a real SRE model with error budgets for its most critical services
while everything else just gets "normal" DevOps treatment. The idealized version where every
developer is equally fluent in Kubernetes, on-call, and writing Terraform never really
materialized — most orgs still have people who specialize in the infra/reliability side, they're
just structured differently than "ops" was in 2010.

### 1.2 What's Changed Recently

**Went from niche to standard/expected:**
- **Containers + Kubernetes.** Cutting-edge circa 2016-2018, now close to a baseline expectation
  for any infrastructure role. Managed Kubernetes (EKS/GKE/AKS) is now the default way most
  companies run containerized workloads in production.
- **Infrastructure as Code**, specifically Terraform. Manually clicking around a cloud console
  to provision infrastructure ("**ClickOps**") went from normal to actively discouraged — it's
  now treated as a real reliability/audit risk, not just a style preference.
- **GitOps for Kubernetes deployment.** Per the CNCF's own July 2025 announcement of its End User
  Survey results ("CNCF End User Survey Finds Argo CD as Majority Adopted GitOps Solution for
  Kubernetes" — a primary source, not a secondary summary), 91% of cloud-native organizations
  have adopted GitOps, and Argo CD runs in roughly 60% of Kubernetes clusters (97% of Argo CD
  users report running it in production, up from 93% in 2023) — Argo CD leads adoption, with Flux
  as the other CNCF-graduated option, over manual `kubectl apply` or ad hoc scripts. **Confidence:
  medium-high** — a real, citable primary source, updated from the earlier "not independently
  confirmed" hedge now that the source itself is directly checkable.
- **Platform Engineering.** Went from "an emerging idea a few thoughtful teams were trying" around
  2021-2022 to *the* dominant theme in Puppet/Perforce's 2024 State of DevOps report, explicitly
  titled around platform engineering's rise. **Confidence: medium-high** (a real, named survey),
  though the specific adoption percentages circulating in blog posts (some claim as high as ~90%
  of orgs having adopted "some" platform) aren't independently verified here.

**Went from standard to declining/legacy:**
- **Docker Swarm** — Docker's own orchestrator lost the orchestration war to Kubernetes years ago
  and is essentially a dead end for new projects.
- **Manual SSH-and-deploy workflows** — still exists in plenty of legacy systems, but it's no
  longer how anyone would *design* a new deployment pipeline.
- **Standalone Jenkins as the default CI choice** — still widely run (huge installed base), but
  the default choice for a *new* project has shifted heavily toward GitHub Actions or GitLab CI,
  where the pipeline config lives next to the code and there's no separate server to babysit.
- **Configuration-management tools (Chef/Puppet/Ansible) as the primary deployment mechanism** —
  displaced by immutable infrastructure (build a new container/image instead of mutating a running
  server). Ansible specifically still has a real, live niche: configuring things that
  *aren't* containerized — network devices, bare VMs, bootstrap steps before containers even
  exist. It didn't die, its job just got narrower.

**Actively in flux right now, not settled:**
- **Terraform vs. OpenTofu.** A real, dateable split: HashiCorp changed Terraform's license from
  open-source (MPL-2.0) to the more restrictive BSL in **August 2023**. OpenTofu forked from the
  last open-source release, joined the Linux Foundation, and was accepted into the **CNCF in
  April 2025 at the Sandbox maturity tier** (not yet Incubating or Graduated). The backdrop that
  explains why this split has kept widening rather than settling: **IBM completed its ~$6.4B
  acquisition of HashiCorp in February 2025** — Terraform is now an IBM-owned product — and HCP
  Terraform ended its free tier in March 2026. Adoption is real (named enterprises like Fidelity
  Investments have migrated, and secondary sources put OpenTofu at roughly 12% adoption among IaC
  practitioners as of April 2026 with strong, ~300% year-over-year download growth) but still a
  minority of the installed base as of mid-2026 — this is genuinely unresolved, and worth tracking
  rather than assuming Terraform's position is permanent. **Confidence: high** on the license/
  CNCF/acquisition timeline (independently checkable), **lower** on exact adoption share.
- **AI-assisted operations.** Genuinely new capability (AI copilots for incident triage, log
  analysis, even proposed remediations), but real production trust in *autonomous* AI action
  during incidents remains limited — this mission's own capstone concept (an AI agent that
  diagnoses and either auto-remediates or escalates, see `orbit/docs/concept.md`) is explicitly
  built around today's actual state of that trust boundary, not a hypothetical future one.
- **Platform engineering's own tooling** (Backstage vs. Port vs. building it yourself) — not
  settled; teams are still actively disagreeing about the right way to build an internal
  developer platform.

### 1.3 A Real Day in the Life

The honest version, not the idealized one: a meaningful chunk of the job is **interrupt-driven**,
not planned. You come in intending to work on an automation project, and a page fires, or someone
from a product team pings asking why their deploy is stuck, or a routine cloud cost alert needs
triage. **Toil** (repetitive manual work that doesn't get permanently eliminated, like fielding
"can you rotate this credential" tickets) constantly competes with the automation work that would
actually reduce future toil — and toil usually wins the day-to-day battle for time, because it's
urgent and automation work is merely important. Teams with real SRE discipline explicitly cap
toil (Google's own guidance was historically "no more than 50% of an SRE's time on toil") and
protect time for engineering work against that cap — but plenty of teams don't enforce this, and
toil quietly eats the whole week.

**On-call** means carrying a pager (PagerDuty, Opsgenie, or similar) for a rotation — a week where
if something breaks, you're the first line of response, day or night. A page firing means: triage
fast (is this actually urgent, or noise?), decide whether you can fix it yourself or need to
escalate, communicate status clearly while under real time pressure, and — critically — resist the
urge to make a risky "fix" you're not sure about at 2am just to make the page stop. After the
incident is actually resolved, mature teams write a **blameless postmortem**: what happened, what
the actual root cause was (often several contributing factors, not one), and what changes prevent
recurrence — without assigning individual blame, because blame makes people hide information
instead of surfacing it.

**Interaction with dev/product teams** in the honest version is often a negotiation, not a clean
handoff: product wants a feature shipped by Friday; the infra/SRE side is watching an error budget
that's already half-spent this quarter and needs to push back on risky changes, or negotiate a
feature flag / staged rollout instead of a big-bang release. A decent chunk of the actual skill in
this job is being able to have that conversation credibly — with data, not just "no."

### 1.4 The Real Skill Stack

**Technical:**
- **Systems fundamentals** — how Linux actually works (processes, filesystem, permissions), not
  just command memorization.
- **Scripting** — bash for glue/automation, Python once things get more complex than a shell
  script should handle.
- **Networking** — DNS, ports, routing, the basics of how a request actually reaches a service, so
  "it's a networking issue" is a diagnosis, not a shrug.
- **Cloud platform depth** — not just "knows AWS exists," but actual working knowledge of the
  compute/networking/storage primitives on whichever cloud the org runs on.
- **CI/CD** — building and maintaining real pipelines, not just clicking "run" on someone else's.
- **Infrastructure as Code** — Terraform (or OpenTofu) fluency, including state management, which
  is where most real IaC pain actually lives.
- **Containers and orchestration** — Docker fluency plus real Kubernetes operating knowledge, not
  just "I deployed a YAML file once."
- **Observability** — the metrics/logs/traces triad, and specifically the judgment to know which
  one answers which kind of question during an incident.

**Non-technical (and genuinely undervalued by learners who focus only on tools):**
- **Incident communication** — calm, factual, frequent updates during an outage, to both technical
  and non-technical stakeholders, without either minimizing or catastrophizing.
- **Ownership mindset** — treating a system as yours to keep healthy, not just "I did my ticket."
- **Judgment under pressure** — making a reasonable call with incomplete information, fast, and
  being willing to say "I don't know yet, here's what I'm checking next" instead of guessing
  confidently.
- **Writing** — postmortems, runbooks, and documentation that someone else can actually follow at
  3am without you there to explain it.
- **Negotiation** — being able to push back on an unsafe deploy or timeline with actual reasoning,
  not just authority.

### 1.5 The Sub-Disciplines That Have Branched Off

Every entry below explains the *actual* distinguishing practice or technology that split it off
from plain DevOps — not just the surface-level "X tacked onto DevOps" gloss.

- **DevSecOps** — split off because security review as a separate, late-stage gate (a security
  team reviewing a finished release right before ship) was too slow and too easy to skip under
  deadline pressure. The actual distinguishing practice is **"shift-left" automated security
  built directly into the pipeline** — dependency/SCA scanning, SAST/DAST, container image
  scanning, and secrets-detection running on every commit/PR, not as a separate late review.
  Still very active; increasingly AI-assisted for triage (2025 industry surveys cite a majority
  of security practitioners viewing AI as a genuine copilot for this work — **confidence:
  medium**, figure via secondary source).

- **GitOps** — split off specifically for Kubernetes/cloud-native deployment, where "deploy" used
  to mean someone running `kubectl apply` from their own laptop with whatever local state they
  happened to have. The actual distinguishing practice: **a Git repository is the single source of
  truth for desired system state, and an automated controller (Argo CD, Flux) continuously
  reconciles the live cluster to match it** — not a person manually pushing changes. This is now
  close to the default assumption for Kubernetes CD, per the CNCF's End User Survey data
  (**confidence: medium-high** on direction, exact adoption percentage less certain).

- **AIOps** — split off to handle a scale problem: modern systems generate far more
  logs/metrics/alerts than a human can manually correlate during an incident. The distinguishing
  practice is **using ML/AI specifically for anomaly detection and event correlation across huge
  volumes of operational data** — not "we use ChatGPT sometimes." Genuinely growing (market-size
  estimates commonly cited in the tens of billions of dollars by 2030 — **confidence: low** on
  exact figures, market-sizing reports are frequently unreliable), though production trust in
  fully autonomous AIOps remediation (versus AI-assisted human decision-making) remains limited
  as of 2026.

- **MLOps** — split off because deploying and operating a machine-learning model is a genuinely
  different problem than deploying a normal application: models decay in accuracy over time as
  real-world data drifts from training data, in a way that ordinary application code doesn't. The
  distinguishing practice is **treating the trained model itself as a versioned artifact with its
  own pipeline** — training, evaluation, deployment, and *continuous accuracy monitoring for
  drift* — not just wrapping a model in a Docker container and calling it done.

- **Platform Engineering** — split off from generalist DevOps because "every team builds its own
  infra tooling from scratch" doesn't scale — it produces duplicated effort and wildly
  inconsistent reliability practices across teams. The distinguishing practice is building an
  actual **internal developer platform (IDP)** — self-service tooling (a service catalog, golden-
  path templates, one-click environment provisioning) that product teams use as a product, with
  the platform team treating internal developers as their actual customers. Multiple 2024-2025
  survey sources point to this being the dominant DevOps-adjacent theme right now (**confidence:
  medium-high** on the "this is now the leading conversation" claim; a widely-repeated caveat
  worth taking seriously — some sources suggest a majority of platform investments aren't yet
  producing measurable productivity gains, meaning adoption has outpaced actual maturity).

- **FinOps** — split off because cloud bills became large and unpredictable enough that
  engineering, finance, and business stakeholders needed a shared practice for reasoning about
  cost, instead of finance simply being surprised by the bill after the fact. The distinguishing
  practice: **treating cloud cost as a first-class, continuously-monitored engineering metric**
  (cost-per-request, cost anomaly alerting, rightsizing) with joint ownership across eng and
  finance, not a finance-only concern. This one has the best sourcing of any in this list — the
  FinOps Foundation's own **"State of FinOps 2026"** report (published February 19, 2026,
  presented at FinOps X in June 2026, 1,192 respondents) is a real, identifiable primary source,
  reporting **98% of organizations now managing AI spend** (up from 31% two years prior — the
  progression is 31% → 63% → 98% across the 2024/2025/2026 editions) and majority adoption of the
  **FOCUS** cost-data standard within the next year. **Confidence: medium-high** — a credible,
  named source; check for a 2027 edition on the next pass, since this figure has moved fast across
  every edition so far.

- **ChatOps** — split off from the idea that operational actions (deploys, rollbacks, running a
  diagnostic) should happen *inside the same chat tool where the team is already discussing the
  incident*, via bots, instead of context-switching to a separate dashboard/terminal mid-incident.
  Still practiced, though less hyped than several years ago — it's become a normal feature
  (Slack/Teams bots) rather than its own hot trend.

- **DataOps** — the data-pipeline equivalent of DevOps: applying CI/CD-style automated testing,
  version control, and monitoring discipline to data pipelines and data quality, instead of
  treating data pipeline changes as a manual, unversioned, untested process. Real, but no strong
  current 2025/2026-specific signal was found on its trajectory one way or the other — treat as
  a live but less rapidly-evolving discipline right now (**confidence: low** on current momentum
  specifically, absence of data isn't evidence of decline).

- **NoOps** — the (mostly aspirational) idea that infrastructure becomes so fully automated and
  managed that a dedicated ops function isn't needed at all. In practice this remains more of a
  narrative than an achieved end-state for most companies — serverless and fully-managed
  platforms get you closer for specific workloads, but incident response, security, and cost
  management don't fully disappear just because servers are managed by someone else.
  **Confidence: low-medium** on any "X% revert from NoOps" specific claims circulating online —
  treat those skeptically; the general point (full NoOps is rare in practice) is more solid than
  any specific statistic attached to it.

- **Emerging, worth watching (not yet as established as the above):**
  - **DevEx (Developer Experience) engineering** — treating internal developer productivity and
    happiness as a measured, strategic discipline (dedicated DevEx metrics frameworks, sometimes
    its own team), rather than an assumed side-effect of good platform engineering. This is the
    most credibly-emerging of the newer entrants as of 2026 — genuinely distinct from Platform
    Engineering in emphasis (DevEx measures and optimizes the *experience*; platform engineering
    *builds the thing being experienced*), though the two overlap heavily in practice. The
    measurement lineage now has a specific, named framework tracing back to one researcher
    (Nicole Forsgren): DORA (2018) → SPACE (2021) → DevEx (2023, ACM Queue) → **DX Core 4**
    (2024) — current sources describe DevEx as "no longer a soft concept" but an actual
    engineering discipline.
  - **AgentOps** — operating, monitoring, and governing autonomous AI agents in production
    (guardrails, evals, cost controls, agent-specific observability), added on this revisit. The
    distinguishing practice is genuinely different from AIOps: **AIOps uses AI/ML to analyze IT
    operations data; AgentOps operates the AI agents themselves** once they're taking autonomous
    actions in production — also distinct from MLOps, which concerns a trained model's own
    accuracy drift rather than an agent's decisions and actions. Backed by real, if very recent,
    survey data: LangChain's "State of Agent Engineering" report (1,300+ respondents — 57.3% now
    have agents in production, 89% have implemented agent-specific observability) and a January
    2026 Futurum Group survey of 628 enterprise IT leaders (60% actively using AI to build/deploy
    software). **Confidence: medium** — real, named surveys, but nearly all sourcing is from
    January 2026 onward, too recent to call this established the way FinOps or DevSecOps are.
  - **GreenOps / sustainability engineering** — carbon-aware scheduling, optimizing for
    performance-per-watt, often framed as an extension of FinOps rather than a fully separate
    discipline yet. Updated on revisit: the Green Software Foundation's **Software Carbon
    Intensity (SCI)** specification became an accredited **ISO standard (ISO/IEC 21031:2024)** in
    March 2024, the GSF ratified a follow-on **"SOFT"** organizational framework in late 2025, and
    new Scope 3 emissions-reporting requirements taking effect for large enterprises in 2026 are
    creating a real regulatory driver. That's comparable institutional weight to several
    already-"established" entries in this list. **Confidence: low-medium** that this has
    crystallized into a distinct, established discipline — up from "low" on the previous check —
    still short of a foundation-run adoption survey the way FinOps has one.

---

## Part 2 — Topics Covered So Far

### Linux

**The real problem.** Before a shared, standardized OS with an open toolset, "the server" meant
whatever proprietary Unix variant or early Windows Server setup a specific vendor sold you —
inconsistent tooling, licensing costs at scale, and no common baseline of commands/scripts that
worked the same way everywhere. Linux (plus the broader open-source toolchain around it) became
the thing that let "how do I check disk usage" or "how do I find what's eating memory" have one
answer that works on a $5/month VPS and a fleet of ten thousand cloud servers alike.

**Why it matters for DevOps/SRE.** It's not a topic *among* the skill stack — it's closer to the
floor everything else stands on. Every container is (in Orbit's case) built on a Linux base image;
every cloud VM you'll provision later runs Linux; every `kubectl` command eventually resolves down
to Linux processes on a node. Not knowing Linux well enough means every layer above it — Docker,
Kubernetes, CI/CD runners — becomes a black box you can't actually debug when it breaks, only
follow tutorials for when it works.

**How it connects.** Everything since Topic 1 has referenced it directly: the WSL corporate-proxy
investigation used the exact filesystem/permission/networking fundamentals from Topics 1-5; the
Docker topics (9-11) are built entirely on Linux process/user/filesystem concepts (the `chown`/
copy-up bug in Topic 11 is fundamentally a Linux filesystem-layering concept, not a Docker-specific
one); Kubernetes (starting now, Topic 12) runs Linux containers on Linux nodes — the "process
states," "signals," and "resource limits" concepts from Topics 2 and 4 reappear directly as
Kubernetes concepts (a container's exit code, a Pod being OOMKilled — the same signal/exit-code
mechanics from Topic 2, just one layer up).

It also connects directly to several §1.5 sub-disciplines, not just to later topics: **SRE**'s
entire numeric reliability model (SLOs, error budgets) is meaningless without someone able to
actually diagnose *why* a system is unhealthy at the systems level — that diagnostic skill is
Linux fundamentals, full stop. **DevSecOps**'s "run as a non-root user, least-privilege" practice
(which Topic 11 applied directly to Orbit's container) isn't a Docker-specific idea at all — it's
literally the Linux user/permission model from Topic 1, applied one layer up. And every **Platform
Engineering** team's slick self-service tooling still ultimately provisions and runs on real Linux
hosts underneath every abstraction — the platform hides Linux from the end user, it doesn't
replace it.

**The alternatives.** For servers specifically, there isn't a real alternative in modern cloud/
DevOps practice — Windows Server still exists for specific enterprise/.NET-heavy shops, but the
overwhelming majority of cloud-native infrastructure, containers, and Kubernetes nodes run Linux.
The real "alternative" question that comes up in practice is *which* Linux distribution and how
minimal (Ubuntu/Debian-family vs. RHEL/Alma/Rocky-family vs. minimal/distroless images for
containers specifically) — a distribution choice, not a Linux-vs-something-else choice.

**Production reality.** At 2am, Linux fundamentals are the difference between "the disk is full, I
know exactly which command tells me what's actually eating it and I can free space safely" and
paging someone else because you don't trust yourself to touch a production filesystem. The Topic 1
proxy investigation and Topic 4's `df`-timeout-as-liveness-issue (not corruption) are exactly this
kind of real, non-tutorial situation — a plausible-looking symptom that needs real fundamentals to
diagnose correctly instead of guessing and making it worse.

### Git

**The real problem.** Before version control like Git, "collaborating on code" commonly meant
emailing files around, naming things `final_v2_REALLY_FINAL.py`, or using centralized systems
(like Subversion/CVS) that required constant network access to a central server and made branching
so painful that teams mostly avoided it. Losing history, overwriting someone else's work
accidentally, and having no real way to experiment safely on a copy of the code were all normal,
accepted risks.

**Why it matters for DevOps/SRE.** Git isn't just "how developers store code" — it's the substrate
CI/CD, GitOps, and Infrastructure as Code are all built on top of. A pipeline triggers *because* of
a Git push; a GitOps controller reconciles a cluster *against* a Git repo's state; Terraform state
and configuration live in Git. If you don't actually understand Git's model (not just the handful
of commands you use daily), you can't reason correctly about *why* a CI/CD pipeline behaves the
way it does when something unexpected happens.

**How it connects.** Topic 6 (fundamentals) → Topic 7 (rebase/cherry-pick, real conflict
resolution) → Topic 8 (GitHub-specific collaboration: PRs, Actions) form one continuous thread —
and this thread directly feeds GitOps (Part 1.5): the entire premise of GitOps is that Git history
*is* the deployment record, so understanding Git deeply here pays off again later when Kubernetes
deployment gets covered through a GitOps lens.

Beyond GitOps specifically, Git is genuinely load-bearing infrastructure for several other §1.5
sub-disciplines: **DevSecOps** hangs a large share of its automated scanning directly off Git
events — pre-commit hooks and secret-detection tools run *at commit time*, before code ever
leaves a laptop, which is the literal mechanism behind "shift-left." **Platform Engineering**'s
"golden path" self-service templates are, in practice, almost always delivered as a Git repo
template a new service gets scaffolded from — the platform *is*, mechanically, a curated set of
Git repositories and the automation wired to them. And **DataOps** applies this exact same
version-everything discipline to data pipelines instead of application code — same underlying
tool, same reasoning, different artifact being tracked.

**The alternatives.** Git effectively won this space — Subversion and Mercurial still exist in
legacy contexts, but essentially no new project in 2026 chooses them over Git. The real "which
tool" decision that still exists in practice is the **hosting/collaboration layer on top of Git**
(GitHub vs. GitLab vs. Bitbucket) — covered next.

**Production reality.** The real 2am Git moment isn't "I forgot the commit command" — it's "we
need to recover from a bad deploy *right now*, and knowing whether to revert, reset, or roll
forward with a fix matters, because picking wrong can make history confusing for the whole team or
even lose work." Topic 7's real cherry-pick mistake (conflict markers left in a file despite
`git add`+`--continue` appearing to succeed) is exactly the kind of "it looked done but wasn't"
trap that matters far more under real incident pressure than in a calm tutorial.

### GitHub

**The real problem.** Git itself is a distributed version-control *tool* — it has no concept of
"a pull request," "who's allowed to merge," or "run this automatically when code changes." Before
platforms like GitHub existed, teams using raw Git still needed a separate, often informal process
for code review (emailing patches, or nothing at all) and had to build or buy separate systems for
running tests/automation on new code.

**Why it matters for DevOps/SRE.** GitHub (and platforms like it) is where the actual *workflow*
of software delivery lives: pull requests are where code review and quality gates happen; branch
protection rules are a real, load-bearing safety mechanism (Topic 8's real discovery that branch
protection doesn't apply to admins by default, silently, until explicitly configured otherwise, is
a genuinely dangerous default worth internalizing); GitHub Actions is many teams' actual CI/CD
engine, not a separate tool bolted on.

**How it connects.** Directly extends Git (above) with collaboration and automation layered on
top, and GitHub Actions specifically is the same category of tool as the CI/CD systems that will
come up again later in the roadmap (Topic 15) — the concepts (triggers, runners, secrets scoping)
transfer directly.

This is also where several §1.5 sub-disciplines become concretely visible rather than abstract:
**DevSecOps** in practice is very often "a GitHub Action running a scanner on every PR" (Dependabot
alerts, CodeQL, container-image scanning) — the pipeline *is* the security gate, not a separate
process. **ChatOps** frequently rides on top of GitHub's own webhook/bot ecosystem — a Slack
notification on a failed Action run, a bot commenting build status directly on a PR. And
**Platform Engineering**'s internal developer platforms (tools like Backstage) commonly use GitHub
itself as their underlying service catalog and template source — the "platform" is often a layer
of automation and UI wrapped around GitHub, not a replacement for it.

**The alternatives.** GitLab (which also bundles CI/CD, container registry, and more into one
product — a genuinely different philosophy, "one platform" vs. GitHub's more
ecosystem-of-integrations approach) and Bitbucket (more common in Atlassian-centric shops using
Jira) are the real competitors. The honest trade-off: GitHub has the largest ecosystem and
community/Action marketplace; GitLab's single-product approach appeals to teams that want fewer
separate tools to integrate and operate.

**Production reality.** The `GITHUB_TOKEN` security considerations from Topic 8 (scope, lifespan,
real risks) aren't academic — a misconfigured Action with excessive token permissions is a real,
current class of supply-chain security incident. The branch-protection defaults not applying to
admins is exactly the kind of thing that looks fine in every test until the one time someone with
admin access pushes directly to `main` under time pressure and nothing stops them.

### Docker

**The real problem.** "Works on my machine" was one of software delivery's most expensive,
recurring failure modes — an app running fine in development, then breaking in production because
of a different OS version, a missing system library, or a mismatched dependency version that
nobody had pinned down precisely. Fixing this by hand meant painstakingly replicating an exact
environment on every target machine — slow, error-prone, and constantly drifting out of sync.

**Why it matters for DevOps/SRE.** Docker (and the OCI container-image standard it popularized)
is the packaging unit almost everything else in modern DevOps assumes exists: CI/CD pipelines
build and test container images; Kubernetes schedules and runs containers; GitOps tools deploy new
container image versions. Skipping real Docker fluency to jump straight to Kubernetes is a common
mistake — Kubernetes is fundamentally an orchestrator *of* containers, and half its behavior only
makes sense once you understand what a container actually is and isn't.

**How it connects.** This mission's own Topics 9-11 built this up directly: architecture and image/
container semantics (9), networking and persistent storage (10), and production-readiness — non-
root users, a real WSGI server instead of a dev server, multi-stage builds (11). Every one of
those threads reappears almost immediately in Kubernetes: a Pod is fundamentally a wrapper around
one or more containers; Kubernetes Services solve the same "how do containers find each other"
problem Topic 10 solved manually with Docker networks, just at cluster scale; a Deployment's
rolling update behavior depends on the same image-tagging discipline Topic 9 covered.

The container is also the literal unit several §1.5 sub-disciplines organize themselves around,
not just a Kubernetes prerequisite: **Platform Engineering**'s self-service platforms almost
always manage *containers* as the standard deployable unit their golden paths produce — the
platform's whole value proposition assumes this packaging problem is already solved. **MLOps**
depends on the exact same packaging idea applied to a trained model plus its runtime dependencies,
which is why "just put the model in a container" is usually step one of any real ML deployment
pipeline. **FinOps** cares about containers directly because a container's declared resource
requests/limits are what actually drives cluster-level cost — rightsizing those requests is a
concrete, everyday FinOps practice, not an abstract cost conversation. And **GitOps** controllers
reconcile against container image tags specifically — Topic 9's tagging discipline (`:latest`
going stale, `v1`/`v2` proving rollback) is exactly the mechanism a GitOps tool depends on to know
whether the cluster's current state actually matches what Git says it should be.

**The alternatives.** Podman (daemonless, often rootless, generally considered more secure by
default, uses the same OCI image format so images are largely interchangeable) is the most direct
alternative for building/running containers. Below Docker's own level, **containerd** and
**CRI-O** are the runtimes that actually matter for Kubernetes specifically — and this is a
concrete, verified, non-obvious fact worth being precise about: **Kubernetes has not run Docker
directly since dockershim was removed in v1.24 (May 2022)**; it talks to a CRI-compliant runtime,
in practice usually containerd (reportedly the default in a large majority of clusters — exact
figures vary by source and should be treated as directional). Docker itself is still the dominant
tool for local development and image-building — and, not coincidentally, modern Docker releases
run containerd underneath as well — it's simply not what a Kubernetes *node* uses to run your
containers at the orchestration layer.

**Production reality.** Topic 11's real bug (a `chown -R` after `COPY --from=builder` silently
duplicating an entire virtual environment into a new image layer via filesystem copy-up,
proven with a measured 231MB → 204MB fix) is exactly the kind of thing that never shows up in a
basic tutorial Dockerfile, but absolutely shows up in a real image-size or build-time review once
someone asks "why is this image so much bigger than it should be." Similarly, the non-root user
and real production server (gunicorn, not Flask's dev server) aren't cosmetic — they're precisely
the two things a security review or a production-readiness checklist would flag first, and exactly
the class of finding this mission's own Topic 10 repo audit surfaced as deferred, real technical
debt rather than nice-to-haves.

---

## Part 3 — What Comes Next

Every future topic — starting with Kubernetes (Topics 12-14) and continuing through CI/CD,
Ansible, Terraform, AWS, Python, observability, and AI-for-DevOps — gets appended here using the
exact same five-point structure used above (the real problem → why it matters → how it connects →
the alternatives → production reality), so this stays one continuous, cross-referenced map of the
field rather than a stack of disconnected notes. The Table of Contents at the top gets a new entry
each time a topic section is added.

### Maintenance Rules

- **One file, forever.** Never fork a v2/v3 — this file is edited in place, every time.
- **Table of Contents always current** — updated in the same edit that adds a new section.
- **Full prose under headers, not bullet-fragment soup** — matching the quality bar this file
  opened with.
- **Time-sensitive claims get a confidence note and, where possible, a source** — especially
  adoption percentages, "what's standard now," and anything version-specific. Absence of a source
  is stated explicitly rather than presented with false confidence.
- **New sub-disciplines get added to §1.5 as they emerge and gain real traction** — not every new
  buzzword, but anything that develops the kind of distinct practice/tooling/metric the existing
  entries have (see the "emerging, worth watching" entries above for the current bar).
