# Project ideas — the portfolio after orbit

> Nine future projects that build on the stack this curriculum teaches
> (k3s, LocalStack, Terraform, Prometheus/Grafana, local AI agents), each buildable solo at zero
> cloud cost. [Orbit](../orbit/) — the autonomous SRE agent with a live incident dashboard — stays
> #1 and in flight; these are what comes after it.

## The rules this list was written under

**Every idea carries a novelty check.** Before an idea earned a place here, the landscape was
actually searched (queries listed per idea), the nearest existing project or product is named
with a link, and the delta is stated specifically. Where the delta is *architectural* — the
nearest neighbor could not become this without being rebuilt — it is labelled so. Where it is
positioning (open vs SaaS, local vs cloud, packaging), it is labelled that, honestly. Nothing
here claims "never been done" without showing what was looked at.

**Novelty decays.** The AI-for-operations space is moving
monthly — re-run the searches before committing to build anything below.

**Ranking is impressiveness-to-effort**: how hard the demo moment lands, divided by how much solo
work stands between here and that moment. Not "best idea wins" — best *ratio* wins.

| Rank | Project | One line | Delta type |
|---|---|---|---|
| 1 | [hindsight](#1-hindsight) | Backtest alert rules against recorded history, like trading strategies | **Architectural** |
| 2 | [relight](#2-relight) | The internet's most famous outages, rebuilt as runnable local incidents | Content + packaging |
| 3 | [firedrill](#3-firedrill) | An AI adversary that reads your infra code and attacks the weakest point | **Architectural** |
| 4 | [understudy](#4-understudy) | Every Terraform change rehearsed — including the rollback — before merge | Positioning + one architectural piece |
| 5 | [blackbox](#5-blackbox) | A flight recorder for your cluster: scrub back to any moment, replay it | **Architectural** |
| 6 | [night-shift](#6-night-shift) | An on-call flight simulator: generated incidents, an AI playing the panicking stakeholder | Architectural (solo angle) |
| 7 | [evergreen](#7-evergreen) | CI for runbooks: every step executed nightly against a clone, rot flagged like failing tests | Architectural (small) |
| 8 | [journeyman](#8-journeyman) | Watch real traces, propose the SLOs — instead of compiling hand-written specs | Moderate |
| 9 | [failure-atlas](#9-failure-atlas) | A knowledge graph of how systems fail, that new incidents get matched against | Positioning |

---

## 1. hindsight

**Backtest your alert rules against recorded history, the way traders backtest strategies.**

**The real problem.** Alert rules are deployed on faith. `promtool` can unit-test a rule against
*synthetic* data you type by hand, but nothing answers the questions that matter: *would this
rule have caught last month's real incident? How many false pages would it have cost me at this
threshold? What `for:` duration would have paged fastest without flapping?* Teams tune thresholds
by folklore and find out at 2 a.m.

**Why an SRE org cares.** Alert noise is the top cited cause of on-call burnout, and missed
alerts are the top cited cause of slow detection. This turns both from folklore into a measured,
repeatable report — and it produces an **alert-debt score** per service: rules that never fire,
rules that fire and get ignored, rules orphaned from any runbook.

**MVP, solo, zero cloud cost.** Prometheus TSDB snapshots from orbit's k3s cluster as the
corpus; a Python engine that replays candidate rules over the recorded range via the Prometheus
API (or a throwaway Prometheus started against the snapshot); a report comparing rule variants:
pages fired, incidents caught/missed, lead time. Grafana dashboard for the sweep results.

**The demo moment.** Load six months of recorded history, show a proposed alert change, and say:
*"this version would have missed two of your last five incidents and woken you eleven extra
times. Here's the variant that catches all five with three fewer pages."* Room stops.

**Unlocked by.** Phase 5 (Python) + Phase 6 (Prometheus/Grafana, topics 47–48). Phase 2's k3s
work provides the live system that generates the history.

**Novelty check.** Searched: *Prometheus alert rule backtesting historical data testing alerts
before deploying.* Nearest neighbors: `promtool`'s
[unit-testing framework](https://prometheus.io/docs/prometheus/latest/configuration/unit_testing_rules/)
(synthetic series only, by design) and ScyllaDB's
[backfilling write-up](https://www.scylladb.com/2021/02/23/prometheus-backfilling-recording-rules-and-alerts/)
(a manual, one-off technique). Testing rules against *historical* data is an explicitly open gap —
requested in [prometheus/prometheus#15545](https://github.com/prometheus/prometheus/issues/15545)
and acknowledged as unsupported. **Delta: architectural** — a backtesting *engine* with variant
sweeps and incident-labelled scoring does not exist in the ecosystem; the upstream project's own
issue tracker documents the hole this fills.

---

## 2. relight

**The internet's most famous outages — Cloudflare's regex, the S3 typo, GitHub's split brain —
rebuilt as runnable incidents on your laptop. An executable museum.**

**The real problem.** Every engineer has *read* the famous postmortems; almost none have *felt*
them. Reading "a WAF rule caused catastrophic backtracking" teaches a fact. Watching CPU pin to
100% on a cluster you're responsible for, with the same symptom pattern, teaches a reflex. The
postmortems are public; the experience isn't.

**Why an SRE org cares.** It's incident training with built-in narrative gravity — everyone
already knows these stories, so onboarding juniors with them lands immediately. Run one per
game-day, zero cloud spend, no risk to anything real.

**MVP, solo, zero cloud cost.** Three scenarios on k3s + LocalStack, each one: a `docker compose
up`-grade bring-up of the vulnerable topology, a trigger script, the real symptom signature
reproduced in Prometheus/Grafana, and a guided debrief mapping what you saw to the real
postmortem, paragraph by paragraph. Cloudflare-2019 (regex backtracking in a proxy tier),
S3-2017 (a fat-fingered capacity removal cascading through dependent subsystems, on LocalStack),
GitHub-2018 (split brain after a 43-second network partition, on a two-node database).

**The demo moment.** "This dashboard is about to have the worst 27 minutes of 2019." Hit enter,
watch the CPU graph reproduce the shape from Cloudflare's actual postmortem, side by side with
the original chart.

**Unlocked by.** Phase 2 (k8s, compose) for the topologies, Phase 3 (AWS via LocalStack) for the
S3 scenario, Phase 6 for symptom-faithful dashboards.

**Novelty check.** Searched: *reproduce famous outages hands-on lab postmortem recreation
training.* Nearest neighbors: [danluu/post-mortems](https://github.com/danluu/post-mortems) (a
reading list), annotated report sites, Gremlin's
[S3 retrospective](https://www.gremlin.com/blog/the-2017-amazon-s-3-outage) (recreates *one*
outage, on their SaaS), scenario platforms like SadServers/KillerCoda (original puzzles, not
historic recreations). **Delta: content + packaging, honestly** — the pieces all exist; a curated,
free, local, *faithful-to-the-real-postmortem* collection does not. Novelty is not the moat here;
execution and taste are. Ranked #2 anyway because the demo/shareability-to-effort ratio is the
best on this list.

---

## 3. firedrill

**You built fire alarms. This hires the arsonist to test them: an AI agent that reads your
Terraform and manifests, hypothesizes your weakest point, attacks it — then grades whether your
observability actually noticed.**

**The real problem.** Chaos engineering tools execute experiments *you* design, which means they
test what you already suspected. The failures that hurt are the ones nobody suspected. And no
chaos tool closes the loop on the question that actually matters: *when this broke, did your
alerts fire? Did your dashboard show it? Would on-call have found it?*

**Why an SRE org cares.** It converts chaos engineering from a quarterly ritual someone has to
design into a standing adversary, and it reframes the output: not "the pod restarted" but "your
p99 alert stayed green through a 40-second outage — here's the blind spot." That's an
observability-coverage report, which is a deliverable managers understand.

**MVP, solo, zero cloud cost.** A local agent (Ollama or Claude on the orbit repo) that ingests
`terraform graph` output + k8s manifests, produces ranked failure hypotheses with reasoning,
executes the top one via LitmusChaos on k3s, then queries Prometheus/Alertmanager to grade
detection: caught / degraded-silently / missed. Report per round; the loop iterates toward
uncovered territory.

**The demo moment.** The agent reads orbit's own infra, says *"the readiness probe on the app
masks a dependency failure — killing the database connection pool will degrade silently,"* does
it, and the dashboard stays green while error rates climb. Then it writes the missing alert.

**Unlocked by.** Phase 2 (k8s, topics 12–14), Phase 6 (the grading loop needs Alertmanager),
Phase 7 (agents). This is the idea most likely to feed components back into orbit.

**Novelty check.** Searched: *AI-generated chaos engineering experiments from infrastructure
code.* Nearest neighbors: [LitmusChaos](https://litmuschaos.io/) now ships an MCP server —
natural-language *triggering* of experiments exists today;
[Steadybit](https://steadybit.com/blog/top-chaos-engineering-tools-worth-knowing-about-2025-guide/)
offers experiment *advice*; industry writing names "autonomous chaos agents" as a forward
direction — named, not shipped. **Delta: architectural** — generation of experiments *from the
IaC itself* plus the closed grading loop against alert/dashboard response is a different machine
from NL-triggered execution of human-designed experiments. The window is open but visibly
closing; this is the idea to build early or not at all.

---

## 4. understudy

**Every Terraform change gets a full dress rehearsal before merge — the apply, the smoke tests,
and the part nobody ever rehearses: the rollback.**

**The real problem.** `terraform plan` tells you what will change, not what will *break* — and
no stage of any standard pipeline answers "if this apply goes wrong at 5 p.m., does the revert
actually return us to a working state?" Rollback paths are assumed, never exercised; state
surgery at midnight is how teams find out.

**Why an SRE org cares.** Change failure rate and time-to-restore are DORA metrics — the numbers
platform teams are graded on. A PR comment that says "apply rehearsed ✅, rollback rehearsed ✅,
blast radius: these 4 resources" moves both.

**MVP, solo, zero cloud cost.** A CI job (GitHub Actions) that, per PR: spins an ephemeral
LocalStack, applies `main`, applies the PR branch, runs smoke tests, then applies `main` again to
rehearse the revert, and diffs the end state against the original — flagging anything that
doesn't return (the classic irreversibles: renames-that-are-really-replacements, deletions,
data-bearing resources). Posts the three-verdict report as a PR comment.

**The demo moment.** A PR that looks trivially safe — a rename — and the bot comments: *"rollback
rehearsal failed: this rename is a destroy-and-recreate; reverting will destroy the bucket
contents. You'd have found out during the incident."*

**Unlocked by.** Phase 4 (Terraform, topics 34–39, especially state and drift), Phase 3
(LocalStack AWS), Phase 2 topic 15 (Actions CI).

**Novelty check.** Searched: *Terraform ephemeral environment LocalStack simulate apply before
merge.* Nearest neighbor is strong and must be named plainly:
[LocalStack's own ephemeral application previews](https://docs.localstack.cloud/aws/tutorials/ephemeral-application-previews/)
deploy your stack per-PR for testing today, and Atlantis/Digger run plan/apply workflows.
**Delta: positioning plus one architectural piece** — preview environments answer "does the new
version work?"; nothing in the pipeline answers "**does the way back work?**" The
rollback-rehearsal stage and the irreversibility diff are the novel machine; the rest is honest
assembly of existing parts.

---

## 5. blackbox

**A flight recorder for your cluster: state, telemetry, and deploys co-recorded on one timeline —
scrub back to the moment before the incident, then replay it in a sandbox.**

**The real problem.** Post-incident, the evidence is scattered across systems that don't share a
clock or a lifespan: events expire in an hour, the pod that crashed no longer exists, metrics
show *that* something happened but not what the cluster state *was*. Reconstructing "what did the
world look like at 14:32?" is manual archaeology.

**Why an SRE org cares.** Faster, calmer root-cause on transient failures — the ones that
"resolved on their own," never get explained, and always come back. And replay turns a postmortem
from a document into a *demonstration*: here is the incident, running again, in a sandbox.

**MVP, solo, zero cloud cost.** A recorder on k3s: watch-stream of resource changes into an
event log (with periodic full-state snapshots), Prometheus TSDB snapshots on the same clock, git
deploy log correlated in. A timeline UI to scrub. Replay v1 is deliberately narrow: restore the
recorded state into a scratch k3s namespace at T-minus-5-minutes and re-drive the recorded
change sequence, watching it unfold live.

**The demo moment.** Scrubbing a cluster like video. Pause at 14:31, point at the config change
that landed 40 seconds before the error-rate cliff on the *same* timeline, then hit "replay" and
watch the incident happen again in a sandbox.

**Unlocked by.** Phase 2 (k8s API depth), Phase 5 (Python, the recorder), Phase 6 (TSDB
mechanics). Latest-unlocking idea on the list; also the hardest.

**Novelty check.** Searched: *Kubernetes cluster history timeline replay tool.* Nearest
neighbors: [salesforce/sloop](https://github.com/salesforce/sloop) — k8s resource-history
*visualization*, the closest single project, no metrics correlation, no replay;
[Komodor](https://komodor.com/) — SaaS change timeline, no re-execution. **Delta: architectural**
— co-recording state + telemetry + deploys on one clock, and actually *re-driving* the recorded
window in a sandbox, is a recorder-and-simulator, not a viewer. Honesty note: full-fidelity
replay is a research-grade problem; v1 replays the change sequence, not the workload traffic —
that scope line is what keeps this solo-buildable.

---

## 6. night-shift

**An on-call flight simulator: it breaks a real (local) system in a generated way, pages you,
plays the panicking stakeholder in chat — and afterwards grades both your debugging *and* your
incident command.**

**The real problem.** The first time most engineers experience incident command — the timeline
discipline, the "what do I tell the VP in 30 seconds" pressure, the tunnel-vision trap — is
during a real incident, on a real system, with real stakes. Every other high-stakes profession
simulates first; on-call mostly doesn't, because existing options need either a team exercise or
a SaaS contract.

**Why an SRE org cares.** On-call readiness is currently binary and discovered in production.
A solo, repeatable simulator makes it trainable and *assessable* — "cleared 12 scenarios, mean
detection 4 minutes" is a legible signal for promoting someone into the rotation.

**MVP, solo, zero cloud cost.** Scenario templates that break orbit's k3s/LocalStack deployment
in parameterized ways (fault type × location × timing, so runs don't repeat); Alertmanager pages
you for real; a local AI plays two roles in a chat window — the stakeholder demanding updates and
the teammate who answers only what's asked precisely; afterwards, a graded debrief against the
recorded timeline: detection time, hypothesis quality, communication cadence.

**The demo moment.** A live audience watches someone get paged, triage under a chattering
stakeholder, and fix it — then the simulator reads out its grade and the one habit to fix.
(Ignite already proved the pedagogy: same-session interview-style examination, applied to
incidents instead of topics.)

**Unlocked by.** Phase 2 + 3 (the breakable system), Phase 6 (paging), Phase 7 (the role-playing
and grading agents).

**Novelty check.** Searched: *incident response training simulation platform SRE.* Nearest
neighbors: [Uptime Labs](https://www.uptimelabs.io/) — the category leader, SaaS, team-drill
oriented; [Wheel of Misfortune](https://github.com/dastergon/wheel-of-misfortune) — the classic
manual role-play; SadServers/KillerCoda — static single-player puzzles without the incident-command
layer. **Delta: architectural for the solo case** — generative scenarios + AI-played stakeholders
+ graded incident command, self-hosted and free, is a different product from team drills or
static puzzles. Uptime Labs proves the market; this is its open, solo, laptop-sized counterpart.

---

## 7. evergreen

**CI for runbooks: every step in every runbook is executable, and a nightly job runs them all
against an ephemeral clone. Rotten runbooks show up like failing tests — before the incident,
not during it.**

**The real problem.** Runbook rot is universal and silently deadly: the doc says step 3 is
`kubectl -n legacy ...` but the namespace was renamed two quarters ago, and the discovery happens
at 3 a.m., mid-incident, when the runbook is the only thing between a tired engineer and a wrong
guess. "Review your runbooks regularly" is advice in every best-practices post; nothing enforces
it.

**Why an SRE org cares.** A runbook that fails its nightly run gets fixed during business hours
by whoever broke the assumption — the same social contract as a failing build. "All runbooks
green" becomes an auditable statement, which compliance and management both love.

**MVP, solo, zero cloud cost.** Runbooks as markdown with fenced, annotated steps (assert /
mutate / observe); a nightly GitHub Actions job that stands up orbit's stack fresh on k3s +
LocalStack, executes each runbook's steps against it, and opens an issue per failure with the
diff between expected and observed. A badge per runbook: last verified date.

**The demo moment.** Rename a namespace in a PR; by morning there's an issue titled *"runbook
'db-failover' broke: step 3 targets a namespace that no longer exists"* — filed by the repo
itself, before any human noticed.

**Unlocked by.** Phase 2 topic 15 (Actions), Phase 5 (Python runner). Earliest fully-unlockable
idea here.

**Novelty check.** Searched: *runbook automation continuously verified executable runbooks.*
Nearest neighbors: [Rundeck](https://www.rundeck.com/) / PagerDuty Process Automation —
*execution* platforms for humans running procedures, not verification of doc truth;
incident.io's 2026 guidance lists "regularly test automated runbooks" as a best *practice* —
i.e., advice, not a shipped mechanism. **Delta: architectural but small** — the inversion
(runbooks verified against infra nightly, docs-as-tests) is genuinely absent as a product; the
build is modest. High ratio, low glamour.

---

## 8. journeyman

**Watch the system's real traces, then propose its SLOs — instead of compiling SLOs someone had
to be senior enough to write.**

**The real problem.** Sloth and Pyrra generate beautiful recording rules and burn-rate alerts —
*from a spec a human wrote*. Writing that spec (which journeys matter, which SLIs represent
them, what targets are achievable) is exactly the part most teams can't staff. The tooling
automated the easy 80% and left the hard 20% as prose.

**Why an SRE org cares.** SLO adoption stalls at the blank-YAML stage in most orgs. A tool that
says "here are your five real user journeys, the SLIs that represent them, and targets set at
your actual 30-day p95 — accept/edit/reject" converts a quarter-long consulting exercise into a
review meeting.

**MVP, solo, zero cloud cost.** OTel instrumentation on orbit; a Python analyzer that clusters
trace paths into journeys, computes candidate SLIs (availability, latency at meaningful
percentiles) with historically-achievable targets, and emits **Sloth/OpenSLO specs** as a PR —
generating the input format of the existing ecosystem rather than competing with it.

**The demo moment.** Point it at a system it has never seen; twenty minutes of traces later it
opens a PR: five journeys, five SLOs, dashboards and burn-rate alerts included, every target
justified by the data ("99.2% proposed; you've delivered 99.4% for 30 days").

**Unlocked by.** Phase 6 (topics 47–50, especially OTel at topic 50), Phase 5 (Python).

**Novelty check.** Searched: *generate SLO SLI definitions automatically from OpenTelemetry
traces.* Nearest neighbors: [Sloth](https://sloth.dev/) and
[Pyrra](https://github.com/pyrra-dev/pyrra) — spec-to-rules compilers, explicitly not
data-to-spec; [Nobl9](https://www.nobl9.com/) — commercial SLO platform, still spec-first.
**Delta: moderate** — "propose from observed data" vs "compile from written spec" is a real gap
but an incremental one, and the incumbents could add it. Ranked accordingly.

---

## 9. failure-atlas

**A knowledge graph of how systems fail — public postmortems and your own incidents, one schema —
that every new incident gets matched against: "this looks like GitHub 2018, here's what worked."**

**The real problem.** The industry writes thousands of postmortems and then never queries them.
Each incident is treated as novel even when its *shape* — saturation cascade, thundering herd,
split brain, config-push blast — has occurred publicly dozens of times, with known mitigations
attached.

**Why an SRE org cares.** Mid-incident pattern matching ("shape: cache stampede, 78% match, three
documented mitigations") shortcuts the most expensive phase of response — hypothesis formation.
Post-incident, it turns the org's own history into something searchable by structure, not
keywords.

**MVP, solo, zero cloud cost.** A failure-pattern schema (trigger, propagation mechanism, symptom
signature, mitigations); a local-LLM pipeline that extracts it from ~100 public postmortems into
a graph; a matcher that takes a live incident description (or orbit's alert payloads) and returns
ranked pattern matches with provenance. Ignite's own field atlas — a sourced,
confidence-rated map of the field — is the editorial prototype for the discipline this needs.

**The demo moment.** Paste a raw, messy incident description mid-firefight; get back "split
brain following network partition — 82% — GitHub 2018, Cloudflare 2020; mitigation that worked
both times: fence writes before reconciling" with links.

**Unlocked by.** Phase 7 (local LLM pipelines), Phase 5 (Python). Content work can start any
time.

**Novelty check.** Searched: *AI postmortem timeline reconstruction knowledge graph incident.*
Nearest neighbors: [Rootly AI](https://rootly.com/) and [incident.io](https://incident.io/) —
mature SaaS that auto-drafts postmortems and reconstructs timelines from *your* incident's data;
danluu's list — corpus without structure. **Delta: positioning, honestly the thinnest here** —
the cross-incident *pattern graph over public + private corpora*, queried mid-incident, is the
novel piece; the per-incident tooling is commodity. Ranked last for exactly that reason, kept on
the list because the corpus work compounds with everything above (night-shift scenarios, relight
candidates, firedrill hypotheses all draw on it).

---

## How this list gets used

One at a time, after orbit, chosen by what the roadmap has just unlocked — never more than one
in flight next to the curriculum. Each project starts by **re-running its novelty check** (the
queries are recorded above precisely so they can be re-run), and inherits ignite's standing
rules: real measurements over adjectives, failures logged where they happen, and nothing in the
repo the whole world can't read.
