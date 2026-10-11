# Ignite — Mission: DevOps

A self-designed, 6-month path from working in cloud operations to being an interview-ready
DevOps/SRE engineer — taught, tested, and graded daily by an AI engineering partner, with every
hands-on hour landing in one real system instead of a folder of disposable tutorials.

Everything here is real: the passed quizzes, the failed one, the bugs found and measured, the
sessions where nothing got built. Nothing is reconstructed after the fact.

![Code: MIT](https://img.shields.io/badge/code-MIT-FF6B35?labelColor=1A1416)
![Docs: CC BY 4.0](https://img.shields.io/badge/docs-CC%20BY%204.0-E23D7B?labelColor=1A1416)
![Curriculum: 53 topics, 7 phases](https://img.shields.io/badge/curriculum-53%20topics%20%C2%B7%207%20phases-B855D8?labelColor=1A1416)
![Method: AI-taught and AI-examined](https://img.shields.io/badge/method-AI--taught%20%26%20AI--examined-7C4DFF?labelColor=1A1416)

---

## Where this stands

**State as of Session 17 · 2026-07-24 IST.** All dates in this repo are IST (UTC+5:30), `YYYY-MM-DD`.

| | |
|---|---|
| Topics cleared | **11 of 53** — Phase 1 complete, Phase 2 in progress |
| Mean score | **86.5 / 100** across the 11 cleared topics |
| Best topic | **94 / 100** — GitHub — PRs, Actions Intro, Repo Management |
| First-attempt pass rate | **10 of 11** |
| Sessions logged | **17**, one commit per session, no batching |
| Roadmap days consumed | **19 of 120** |
| Study notebooks | **11 files, 5,914 lines** of commands actually run and real output |
| Field reference | **531 lines**, continuously updated, with per-claim confidence levels |

Next up: Topic 12 — Kubernetes — Architecture & Core Concepts.

> **On the scores.** They are self-assessed and AI-graded, against a fixed rubric
> (Quiz /40 + Hands-on /30 + Depth of understanding /30). They are not externally validated and are
> not a certification. They are useful as a consistent internal signal of which topics are solid and
> which are shaky — that is all they claim to be.

---

## Receipts

Six things that actually broke, and what closing them looked like. These are the answers to
"tell me about something you debugged" — each one has a measurement attached, not an adjective.

**A final Docker image larger than its own builder stage — 231 MB → 204 MB**
The multi-stage build produced a final image *bigger* than the builder it was supposed to slim down,
which should be impossible. Root cause: a `RUN chown -R` placed **after** `COPY --from` forced the
overlay filesystem to copy-up the entire virtualenv into a fresh layer. Fixed by moving ownership
into the copy itself with `COPY --chown=`, then proved with a measured before/after.
→ Topic 11 — Docker — Multi-Stage Builds & Best Practices

**A one-line code edit reinstalling every dependency — 13.3 s → 2.3 s**
`COPY . .` had bundled the application code and the dependency manifest into a single layer, so
touching one line of Python invalidated the cache for everything after it. Reordered to copy the
manifest first; proved with real build logs showing `CACHED` on the install step.
→ Topic 9 — Docker — Architecture, Images, Containers

**Container-to-container DNS failing three different ways**
Name resolution failed outright on Docker's default bridge (`socket.gaierror`), worked by raw IP, then
worked by name again on a user-defined network. The bridge reported `DynamicIPsAvailable: 65533` —
checked by hand against CIDR arithmetic to confirm the three missing addresses were the network,
gateway and broadcast reservations, not hidden containers.
→ Topic 10 — Docker — Networking, Volumes, Docker Compose

**Branch protection that did not protect**
Three findings in one session: classic branch protection is bypassed **silently** by repository
admins until "do not allow bypassing" is switched on; a self-approval block genuinely prevents a
merge even on a solo repository; and requiring linear history quietly removes the merge-commit option
from the UI altogether.
→ Topic 8 — GitHub — PRs, Actions Intro, Repo Management

**A timing-out `df` is not a full disk**
A production-style alert was re-read correctly as a liveness / stale-mount problem rather than
filesystem corruption. Backed by building a loop-mounted disk end to end — `fallocate` → `losetup` →
`mkfs.ext4` → `mount` → a hand-written `/etc/fstab` entry, verified with `mount -a` rather than a
hopeful reboot.
→ Topic 4 — Linux Deep Dive — Process, Log, Disk Management

**Exit code 137 = 128 + SIGKILL**
One container exited `137` where another exited `0`. Traced to signal semantics rather than dismissed
as noise, connecting Docker's container lifecycle directly back to `SIGTERM` vs `SIGKILL` from the
Linux phase. A small detail, and exactly the one interviewers push on.
→ Topic 9 — Docker — Architecture, Images, Containers

---

## The method

The curriculum is ordinary. The examination loop is not.

**An AI is the teacher *and* the examiner.** Every session: teach the topic live, run the commands
hands-on, then sit a quiz on it **the same session** — never the next day. Quizzes are conducted like
interviews: open-ended, "walk me through it," with follow-up pushback on anything that sounds
memorised. No multiple choice, ever. Interview practice therefore compounds for six months instead of
being crammed at the end.

**The 3-attempt mastery rule.** A topic gets at most three attempts, and the *teaching* must
escalate every time — repeating an explanation is explicitly disallowed. Attempt 2 uses a different
analogy; attempt 3 breaks the topic into its smallest components and confirms each one alone. A topic
still not solid after three is logged as **deferred mastery** with a hard revisit deadline, and must
be cleared before anything that depends on it. It never quietly slides forward.

**The failure is on display, deliberately.** Topic 3 — Linux — Shell Scripting Basics failed its
first quiz on function invocation and argument scoping. It was re-taught using concrete tracing
instead of another analogy, then passed a full, fresh retest in the same session. It scores 80 — the
lowest in the repo — and it stays visible. A record with no failures in it is not a record.

**A full repo audit every 10 topics.** Line by line, every subfolder. Findings are reviewed before a
single fix is applied, and genuinely topic-specific improvements are deliberately *deferred* to the
session that teaches them — so they get learned hands-on rather than found pre-fixed. Audit records
live in [`audits/`](audits/).

The rules the AI actually follows are in [`CLAUDE.md`](CLAUDE.md). It is the most interesting file
here if you want to run something like this yourself.

---

## What's in the repository

```
ignite/
├── CLAUDE.md                  the operating rules the AI teacher follows every session
├── README.md                  this file
├── CONTRIBUTING.md            which pull requests are welcome, and which are not
├── SECURITY.md                how to report a vulnerability, privately
├── LICENSE                    MIT — covers the software in this repository
├── .gitignore  .gitattributes
├── learning/                  the record — how the learning actually went
│   ├── roadmap.md             fixed 53-topic / 120-day baseline + a living pacing layer
│   ├── progress.md            session log, quiz record index, deferred-mastery tracker
│   ├── handbook_status.md     per-topic scores with a one-line reason each
│   ├── session_notes.md       short personal recap per session
│   ├── field_atlas.md         living map of the DevOps/SRE field, with sourced confidence levels
│   ├── notes/                 one detailed study notebook per topic, filed by phase
│   └── LICENSE                CC BY 4.0 — covers the written material in this repository
├── orbit/                     the project — a real system, built incrementally
│   ├── app/                   the service, its Dockerfile, and tests
│   ├── k8s/  argocd/          manifests, Helm charts, GitOps delivery
│   ├── terraform/             infrastructure, modules, per-environment config
│   ├── ansible/  monitoring/  configuration management, observability
│   ├── docs/                  architecture and the capstone concept
│   ├── scripts/               automation
│   └── docker-compose.yml
├── engine/                    the Ignition Engine — the teaching protocol, packaged to fork
├── audits/                    periodic whole-repo audits, dated, with an index
├── docs/                      the method, and future project ideas
└── .github/                   CI and issue-form scaffolding — populated from Topic 15
```

Folders tied to later phases hold a short README naming the topic that will populate them, rather
than placeholder code that pretends to work.

---

## Orbit — the project

[`orbit/`](orbit/) is a real system built alongside the learning, from day one, not bolted on at the
end. What runs today:

- A Flask service with `/health` and `/ready` endpoints
- A **multi-stage** image that hands a virtualenv between stages, drops to a non-root user, serves
  through **gunicorn** rather than the development server, and declares its own `HEALTHCHECK`
- One-command bring-up via Compose against a pinned `orbit-app:2.1` tag

```bash
cd orbit && docker compose up --build
curl http://localhost:5000/health   # {"status":"ok","version":"2.1"}
```

The application is **deliberately minimal**. It exists to be a genuine deployment target for the
containerisation, CI/CD, Kubernetes, Terraform and observability work — the engineering worth looking
at is in how it gets built, shipped and operated, not in the request handlers. Kubernetes, Terraform,
Ansible and the monitoring stack arrive as the phases that teach them are reached.

The end goal is documented in [`orbit/docs/concept.md`](orbit/docs/concept.md): an autonomous SRE
agent that watches metrics, logs and traces on the running service, correlates them against recent
deploys to reach a root cause, then either remediates or escalates with a written incident report —
engineered to cost nothing, using k3s and a local AWS emulator instead of billed cloud services.

---

## Using this yourself

The teaching protocol is packaged for exactly this. [`engine/`](engine/) — the **Ignition
Engine** — is the whole system with the DevOps removed: a portable `CLAUDE.md` you copy unedited,
a `MISSION.md` template where you define your own topics, phases and deadline, and blank record
templates. [`engine/QUICKSTART.md`](engine/QUICKSTART.md) goes from nothing to "start session 1"
in about five minutes, editing exactly one file. Ignite itself is mission #1 running on it, and
[`docs/why-this-works.md`](docs/why-this-works.md) explains the learning science behind the rules
— including their limits.

Issues pointing out a **factual error in a notebook** are genuinely welcome — include a source and it
gets corrected and re-verified. Pull requests rewriting the notebooks are not, because `learning/` is
a dated first-person record and editing it destroys the thing that makes it worth reading.
[`CONTRIBUTING.md`](CONTRIBUTING.md) has the details.

---

## License

Two grants, split by what the material is:

- **MIT** — the software: `orbit/`, `.github/`, and any scripts or configuration elsewhere in the
  tree. See [`LICENSE`](LICENSE).
- **CC BY 4.0** — the written material: `learning/`, `docs/`, `audits/`, `engine/`, and the
  Markdown documents at the repository root (this file, `CONTRIBUTING.md`, `SECURITY.md`,
  `CLAUDE.md`). See [`learning/LICENSE`](learning/LICENSE). This is what covers `engine/` — copy
  and adapt it for your own mission, with attribution, same as any other written material here.

This repository is educational reference material, not production-hardened infrastructure — do not
deploy `orbit/` as-is.

Much of the prose here was drafted by Claude and verified by a human before being written down; the
grants above apply to the extent copyright subsists in it.
