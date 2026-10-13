# DevOps/SRE Field Atlas — Field Map

> A living reference, not a session log. `progress.md` tracks *what happened and when*; the
> per-topic notebooks under `notes/` capture *the hands-on teaching detail*. The atlas is
> different: it's the connected map of the field itself — what each piece actually is, why it
> exists, how it connects to everything else, and where the field is moving. Two files, always
> current: this one holds the state of the field and the atlas's maintenance rules; the
> [topic map](topic-map.md) holds the topics covered so far.
>
> **A note on currency**: anywhere a claim is about something fast-moving (adoption numbers, what
> counts as "standard" right now, tool version behavior), it's marked with a confidence level and,
> where possible, a source. Treat percentages from secondary/blog sources as directional, not
> precise.
>
> **Last sub-discipline check: 2026-10-04** (IST).

---

## Table of Contents

**Part 1 — The Field, Right Now**
- [The Field in One Minute](#the-field-in-one-minute)
- [1.1 What DevOps and SRE Actually Mean Today](#11-what-devops-and-sre-actually-mean-today)
- [1.2 What's Changed Recently](#12-whats-changed-recently)
- [1.3 A Real Day in the Life](#13-a-real-day-in-the-life)
- [1.4 The Real Skill Stack](#14-the-real-skill-stack)
- [1.5 The Sub-Disciplines That Have Branched Off](#15-the-sub-disciplines-that-have-branched-off)

**Part 2 — Topics Covered So Far** → [`topic-map.md`](topic-map.md)

**Part 3 — What Comes Next**
- [Maintenance Rules](#maintenance-rules)

---

## Part 1 — The Field, Right Now

### The Field in One Minute

- DevOps didn't merge dev and ops into one team. Specialization came back as Platform, SRE and
  embedded DevOps roles.
- Kubernetes, Infrastructure as Code and GitOps are now baseline. Docker Swarm, SSH-and-deploy and
  Jenkins-by-default are legacy.
- Still in flux: Terraform vs. OpenTofu, AI-assisted operations, and platform tooling.
- The day job is interrupt-driven: toil, on-call, and negotiating with product teams using data.
- Platform Engineering is the leading conversation; AgentOps is the newest sub-discipline worth
  watching.

### 1.1 What DevOps and SRE Actually Mean Today

> **Myth** (the 2015 *Phoenix Project* image): developers and ops merge into one happy team that
> does everything together.
>
> **Reality:** that's not what happened at scale. Specialization re-formed around new lines.

**Three roles, not one.** Most engineering orgs past a certain size now have some combination of:

| Role | What it does |
|---|---|
| **Platform team** | Builds the internal tooling/paved road other engineers use — CI/CD templates, a self-service way to spin up infra, a service catalog |
| **SRE team** | Owns production reliability for specific services, with actual numeric targets |
| **Embedded DevOps/infra engineers** | Sit inside product teams and own that team's pipelines, cloud resources, and deploy process specifically |

"DevOps engineer" as a job title still exists constantly in postings, but it usually means
"whoever on this team owns the infra/CI/CD/cloud stuff," not "a person who has abolished the
boundary between writing code and running it."

**SRE is the version with numbers that can stop a release.** SRE (Site Reliability Engineering)
is Google's specific, more rigorous formalization of similar ideas, and it's the one with an actual
measurement discipline attached: **SLOs** (Service Level Objectives — a target like "99.9% of
requests succeed in under 300ms"), **error budgets** (the allowed amount of unreliability before
it's spent — burn through it, and new feature releases get paused in favor of reliability work),
and blameless postmortems as a formal, required practice, not just a nice idea. Where DevOps is
closer to a culture-plus-toolchain description of a role, SRE is a specific operating model with
numbers attached that actually gate what a team is allowed to ship.

**In practice, almost everyone mixes the two.** Most companies are not "pure DevOps" or "pure
SRE" — they borrow whichever pieces solve their actual pain: a startup adopts DevOps culture and
CI/CD without ever writing a formal SLO; a larger company runs a real SRE model with error budgets
for its most critical services while everything else just gets "normal" DevOps treatment. The
idealized version where every developer is equally fluent in Kubernetes, on-call, and writing
Terraform never really materialized.

**Where you'll meet this:** in any team-structure conversation, and in the question "what's the
difference between DevOps and SRE?"

<details>
<summary><b>Check yourself:</b> your service has burned half its error budget this quarter, and product wants a big release on Friday. What happens?</summary>

Less risk, not a flat "no": ship behind a feature flag or as a staged rollout, or pause feature
work for reliability fixes until the budget recovers. The error budget is the agreed rule that
decides this, so the pushback comes with data, not one person's opinion.
</details>

### 1.2 What's Changed Recently

| Now standard | Now legacy | Still in flux |
|---|---|---|
| Containers + Kubernetes · Infrastructure as Code · GitOps · Platform Engineering | Docker Swarm · manual SSH-and-deploy · Jenkins as the default CI · config management as the main deploy tool | Terraform vs. OpenTofu · AI-assisted operations · platform tooling |

**Went from niche to standard/expected:**
- **Containers + Kubernetes.** Cutting-edge circa 2016-2018, now close to a baseline expectation
  for any infrastructure role. Managed Kubernetes (EKS/GKE/AKS) is now the default way most
  companies run containerized workloads in production.
- **Infrastructure as Code**, specifically Terraform. Manually clicking around a cloud console
  to provision infrastructure ("**ClickOps**") went from normal to actively discouraged — it's
  now treated as a real reliability/audit risk, not just a style preference.
- **GitOps for Kubernetes deployment.** Per the CNCF's July 2025 End User Survey announcement, 91%
  of cloud-native organizations have adopted GitOps, and Argo CD runs in roughly 60% of Kubernetes
  clusters (97% of Argo CD users report running it in production, up from 93% in 2023) — Argo CD
  leads adoption, with Flux as the other CNCF-graduated option, over manual `kubectl apply` or ad
  hoc scripts. **Confidence: medium-high.**
- **Platform Engineering.** Went from "an emerging idea a few thoughtful teams were trying" around
  2021-2022 to the point where Puppet/Perforce's State of DevOps report is now *published as* a
  platform engineering report rather than merely themed around one. The current edition, "State
  of DevOps Report: Platform Engineering 2026" (Perforce, **8 July 2026**, 820 respondents),
  reframes the discipline as the governance layer under AI adoption: 73% of organizations with
  mature platform engineering call that maturity a critical or significant factor in their AI
  success, against 44% of less mature ones. **Confidence: medium-high.** Blog claims of up to
  ~90% adoption are unverified.

> **Myth:** Jenkins, Chef, Puppet and Ansible are dead.
>
> **Reality:** they're still widely run. What shrank is their role as the *default* choice for
> something new.

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
- **Terraform vs. OpenTofu.** A real, dateable split:
  - **August 2023** — HashiCorp changes Terraform's license from open-source (MPL-2.0) to the more
    restrictive BSL. OpenTofu forks from the last open-source release in response and joins the
    Linux Foundation.
  - **February 2025** — IBM completes its ~$6.4B acquisition of HashiCorp; Terraform is now an
    IBM-owned product.
  - **April 2025** — OpenTofu is accepted into the CNCF at the Sandbox tier (not yet Incubating or
    Graduated).
  - **March 2026** — HCP Terraform ends its free tier.

  That backdrop is why the split has kept widening rather than settling. Adoption is real (named
  enterprises like Fidelity Investments have migrated, and secondary sources put OpenTofu at
  roughly 12% adoption among IaC practitioners as of April 2026 with strong, ~300% year-over-year
  download growth) but still a minority of the installed base as of mid-2026. One newer data
  point: Spacelift reports that over half of all runs on its platform are now OpenTofu runs (~58%
  of its Terraform-stack runs over a trailing 30-day window). Spacelift is a founding OpenTofu
  member reporting on its own customers, so read it as directional. **Confidence: high** on the
  timeline, **lower** on adoption share.
- **AI-assisted operations.** Genuinely new capability (AI copilots for incident triage, log
  analysis, even proposed remediations), but real production trust in *autonomous* AI action
  during incidents remains limited. That gap now has a number: the 2026 Platform Engineering
  report above finds roughly
  two-thirds of organizations using AI somewhere in their infrastructure workflows, but only 31%
  reporting *fully autonomous* AI — and trust in AI output tracks governance rather than tooling
  (94% where formal governance exists, 51% under ad hoc approaches). Google Cloud's DORA team has
  also moved into this space with two named reports — "State of AI-assisted Software Development"
  (the 2025 edition, published February 2026) and a follow-on "ROI of AI-assisted Software
  Development" (last updated April 2026) — whose central claim is that AI acts as an amplifier of
  an organization's existing strengths and weaknesses rather than a uniform uplift. **Confidence:
  medium-high** on direction, **medium** on the specific percentages.
- **Platform engineering's own tooling** (Backstage vs. Port vs. building it yourself) — not
  settled; teams are still actively disagreeing about the right way to build an internal
  developer platform.

**Where you'll meet this:** in every "which tool do we pick for the new service?" decision, and in
legacy systems that still run the declining tools.

<details>
<summary><b>Check yourself:</b> what started the Terraform vs. OpenTofu split, and why is it still unsettled?</summary>

HashiCorp moved Terraform from MPL-2.0 to the BSL license in August 2023 and OpenTofu forked the
last open-source release. IBM's purchase of HashiCorp (February 2025) and the end of HCP
Terraform's free tier (March 2026) kept the gap widening. OpenTofu adoption is real but still a
minority, and no neutral, field-wide source has measured the exact share.
</details>

### 1.3 A Real Day in the Life

**The honest version: a meaningful chunk of the job is interrupt-driven, not planned.** You come
in intending to work on an automation project, and a page fires, or someone from a product team
pings asking why their deploy is stuck, or a routine cloud cost alert needs triage. **Toil**
(repetitive manual work that doesn't get permanently eliminated, like fielding "can you rotate
this credential" tickets) constantly competes with the automation work that would actually reduce
future toil — and toil usually wins the day-to-day battle for time, because it's urgent and
automation work is merely important. Teams with real SRE discipline explicitly cap toil (Google's
own guidance was historically "no more than 50% of an SRE's time on toil") and protect time for
engineering work against that cap — but plenty of teams don't enforce this, and toil quietly eats
the whole week.

**On-call: a week where you're the first line of response, day or night.** It means carrying a
pager (PagerDuty, Opsgenie, or similar) for a rotation. A page firing means: triage fast (is this
actually urgent, or noise?), decide whether you can fix it yourself or need to escalate,
communicate status clearly while under real time pressure, and — critically — resist the urge to
make a risky "fix" you're not sure about at 2am just to make the page stop. After the incident is
actually resolved, mature teams write a **blameless postmortem**: what happened, what the actual
root cause was (often several contributing factors, not one), and what changes prevent recurrence
— without assigning individual blame, because blame makes people hide information instead of
surfacing it.

**Working with product teams is a negotiation, not a handoff.** Product wants a feature shipped by
Friday; the infra/SRE side is watching an error budget that's already half-spent this quarter and
needs to push back on risky changes, or negotiate a feature flag / staged rollout instead of a
big-bang release. A decent chunk of the actual skill in this job is being able to have that
conversation credibly — with data, not just "no."

**Where you'll meet this:** in your first on-call rotation, and in every week where the automation
project slips because tickets won.

<details>
<summary><b>Check yourself:</b> it's 2am, a page fires, and you have a fix you're not sure about. What do you do, and what happens after the incident?</summary>

Triage first (urgent, or noise?), then fix it only if you're confident; otherwise escalate, and
keep communicating status. Don't make a risky change just to make the page stop. Once it's
resolved, write a blameless postmortem: what happened, the root cause (often several contributing
factors), and what prevents a repeat, without blaming a person.
</details>

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

**Where you'll meet this:** the moment a real outage stops matching the tutorial.

<details>
<summary><b>Check yourself:</b> a deploy is failing at 3am and the only person who knows the system is asleep. Which two skills on this list decide whether that's a crisis?</summary>

Writing and judgment under pressure. A runbook someone else can follow at 3am turns "only one
person knows" into a documented path, and judgment under pressure is what lets you say "I don't
know yet, here's what I'm checking next" instead of guessing.
</details>

### 1.5 The Sub-Disciplines That Have Branched Off

Every entry below explains the *actual* distinguishing practice or technology that split it off
from plain DevOps — not just the surface-level "X tacked onto DevOps" gloss.

Not listed, because each restates an entry below: "agentic DevOps" and "AI platform engineering"
(AgentOps plus Platform Engineering), and "FinOps for AI" (token spend as an operational cost
line; inside FinOps, whose 2026 report already tracks AI spend as its headline figure).

**At a glance** (details for each below):

| Sub-discipline | What split it off | Confidence |
|---|---|---|
| **DevSecOps** | Security moved from a late gate into every commit/PR | medium (AI-triage figure) |
| **GitOps** | Git is the source of truth; a controller keeps the cluster matching it | medium-high |
| **AIOps** | ML/AI to correlate more ops data than humans can | low (market figures) |
| **MLOps** | The trained model became a versioned artifact with its own pipeline | — |
| **Platform Engineering** | Internal developer platforms, run as a product | medium-high |
| **FinOps** | Cloud cost became a monitored engineering metric | medium-high |
| **ChatOps** | Ops actions run from the incident chat, via bots | — |
| **DataOps** | CI/CD discipline applied to data pipelines | low (momentum) |
| **NoOps** | The aim of no dedicated ops at all; mostly aspirational | low-medium |
| *Emerging:* **DevEx** · **AgentOps** · **GreenOps** | Developer experience as a measured discipline · operating AI agents · sustainability | — · medium (practice), low (adoption) · low-medium |

- **DevSecOps** — split off because security review as a separate, late-stage gate (a security
  team reviewing a finished release right before ship) was too slow and too easy to skip under
  deadline pressure. The actual distinguishing practice is **"shift-left" automated security
  built directly into the pipeline** — dependency/SCA scanning, SAST/DAST, container image
  scanning, and secrets-detection running on every commit/PR, not as a separate late review.
  Still very active; increasingly AI-assisted for triage (2025 industry surveys cite a majority
  of security practitioners viewing AI as a genuine copilot for this work — **confidence:
  medium**).

- **GitOps** — split off specifically for Kubernetes/cloud-native deployment, where "deploy" used
  to mean someone running `kubectl apply` from their own laptop with whatever local state they
  happened to have. The actual distinguishing practice: **a Git repository is the single source of
  truth for desired system state, and an automated controller (Argo CD, Flux) continuously
  reconciles the live cluster to match it** — not a person manually pushing changes. Now close to
  the default for Kubernetes CD (figures and confidence in §1.2).

- **AIOps** — split off to handle a scale problem: modern systems generate far more
  logs/metrics/alerts than a human can manually correlate during an incident. The distinguishing
  practice is **using ML/AI specifically for anomaly detection and event correlation across huge
  volumes of operational data** — not "we use ChatGPT sometimes." Genuinely growing (market-size
  estimates commonly cited in the tens of billions of dollars by 2030 — **confidence: low** on
  exact figures, market-sizing reports are frequently unreliable), though trust in fully
  autonomous remediation is still limited (see §1.2).

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
  the platform team treating internal developers as their actual customers. The dominant
  DevOps-adjacent theme right now (see §1.2; **confidence: medium-high**). Caveat: some sources
  suggest most platform investments don't yet show measurable productivity gains — adoption has
  outpaced maturity.

- **FinOps** — split off because cloud bills became large and unpredictable enough that
  engineering, finance, and business stakeholders needed a shared practice for reasoning about
  cost, instead of finance simply being surprised by the bill after the fact. The distinguishing
  practice: **treating cloud cost as a first-class, continuously-monitored engineering metric**
  (cost-per-request, cost anomaly alerting, rightsizing) with joint ownership across eng and
  finance, not a finance-only concern. The FinOps Foundation's own **"State of FinOps 2026"**
  report (February 2026, 1,192 respondents) reports **98% of organizations now managing AI spend**
  (31% → 63% → 98% across the 2024/2025/2026 editions) and majority adoption of the **FOCUS**
  cost-data standard within the next year. **Confidence: medium-high.**

- **ChatOps** — split off from the idea that operational actions (deploys, rollbacks, running a
  diagnostic) should happen *inside the same chat tool where the team is already discussing the
  incident*, via bots, instead of context-switching to a separate dashboard/terminal mid-incident.
  Still practiced, though less hyped than several years ago — it's become a normal feature
  (Slack/Teams bots) rather than its own hot trend.

- **DataOps** — the data-pipeline equivalent of DevOps: applying CI/CD-style automated testing,
  version control, and monitoring discipline to data pipelines and data quality, instead of
  treating data pipeline changes as a manual, unversioned, untested process. Real, but no strong
  2025/2026 signal on its direction was found: a live but slower-moving discipline (**confidence:
  low** on momentum; absence of data isn't evidence of decline).

- **NoOps** — the (mostly aspirational) idea that infrastructure becomes so fully automated and
  managed that a dedicated ops function isn't needed at all. In practice this remains more of a
  narrative than an achieved end-state for most companies — serverless and fully-managed
  platforms get you closer for specific workloads, but incident response, security, and cost
  management don't fully disappear just because servers are managed by someone else.
  **Confidence: low-medium** on the "X% revert from NoOps" claims online; the general point
  (full NoOps is rare) is more solid.

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
    (guardrails, evals, cost controls, agent-specific observability). The
    distinguishing practice is genuinely different from AIOps: **AIOps uses AI/ML to analyze IT
    operations data; AgentOps operates the AI agents themselves** once they're taking autonomous
    actions in production — also distinct from MLOps, which concerns a trained model's own
    accuracy drift rather than an agent's decisions and actions. Backed by real, if very recent,
    survey data: LangChain's "State of Agent Engineering" report (1,300+ respondents — 57.3% now
    have agents in production, 89% have implemented agent-specific observability) and a January
    2026 Futurum Group survey of 628 enterprise IT leaders (60% actively using AI to build/deploy
    software). The *practice* is clear, but the adoption numbers contradict each other: some 2026
    surveys put enterprises with at least one agent in
    production near 31%, against LangChain's 57.3%, and a widely-recirculated claim that 88% of
    agent pilots never reach production traces back to vendor-adjacent research rather than a
    neutral one. **Confidence: medium** that it's a distinct practice, **low** on any adoption
    percentage, because the evidence is all from 2026.
  - **GreenOps / sustainability engineering** — carbon-aware scheduling, optimizing for
    performance-per-watt, often framed as an extension of FinOps rather than a fully separate
    discipline yet. The Green Software Foundation's **Software Carbon
    Intensity (SCI)** specification became an accredited **ISO standard (ISO/IEC 21031:2024)** in
    March 2024, the GSF ratified a follow-on **"SOFT"** organizational framework in late 2025, and
    new Scope 3 emissions-reporting requirements taking effect for large enterprises in 2026 are
    creating a real regulatory driver. **Confidence: low-medium** that it's a distinct discipline
    yet, since there's no foundation-run adoption survey like FinOps has.

**Where you'll meet this:** in team names and job titles ("Platform", "FinOps", "SRE"), and in
deciding which of these a problem actually belongs to.

<details>
<summary><b>Check yourself:</b> AIOps and AgentOps both involve AI. What's the one-sentence difference?</summary>

AIOps uses AI/ML to *analyze* IT operations data (anomalies, event correlation); AgentOps
*operates* the AI agents themselves once they take autonomous actions in production (guardrails,
evals, cost controls, agent-specific observability).
</details>

**Numbers to remember from Part 1:**
- **91%** of cloud-native organizations have adopted GitOps; Argo CD runs in about **60%** of
  Kubernetes clusters (CNCF, July 2025).
- **73%** of organizations with mature platform engineering call it a critical or significant
  factor in their AI success, against **44%** of less mature ones (Perforce, July 2026).
- About **two-thirds** of organizations use AI somewhere in infrastructure work, but only **31%**
  report fully autonomous AI; trust is **94%** with formal governance, **51%** without.
- **August 2023**: Terraform's license change, the start of the OpenTofu split. OpenTofu is at
  roughly **12%** adoption among IaC practitioners (April 2026, secondary sources).
- **50%**: Google's historical cap on how much of an SRE's time may go to toil.
- **98%** of organizations now manage AI spend, up from **31%** two editions earlier (State of
  FinOps 2026).
- **57.3%** against **31%**: the two contradicting figures for enterprises with an AI agent in
  production.

---

## Part 3 — What Comes Next

Every future topic — starting with Kubernetes (Topics 12-14) and continuing through CI/CD,
Ansible, Terraform, AWS, Python, observability, and AI-for-DevOps — gets appended to the
[topic map](topic-map.md) using the same five-point structure as the sections already there (the
real problem → why it matters → how it connects → the alternatives → production reality), so this
stays one continuous, cross-referenced map of the field rather than a stack of disconnected
notes. The topic map's Table of Contents gets a new entry each time a section is added.

### Maintenance Rules

- **Two files, edited in place.** This field map and the [topic map](topic-map.md). Never fork a
  v2/v3.
- **Table of Contents always current** — each file's own, updated in the same edit that adds a
  new section.
- **Full prose under headers, not bullet-fragment soup** — matching the quality bar this file
  opened with.
- **Time-sensitive claims get a confidence note and, where possible, a source** — especially
  adoption percentages, "what's standard now," and anything version-specific. Absence of a source
  is stated explicitly rather than presented with false confidence.
- **New sub-disciplines get added to §1.5 as they emerge and gain real traction** — not every new
  buzzword, but anything that develops the kind of distinct practice/tooling/metric the existing
  entries have (see the "emerging, worth watching" entries above for the current bar).
