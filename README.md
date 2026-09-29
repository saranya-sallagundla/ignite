# Mission: DevOps

A self-paced, 6-month path to interview-ready DevOps/SRE engineer, taught and tested entirely by
Claude Code, with a real, incrementally-built infrastructure project as proof of work by the end.

## How this repo is organized

Two folders, kept deliberately separate:

- **`learning/`** — everything about the learning process itself: the roadmap, session log, quiz
  history, and personal notes. Scaffolding behind the scenes, not meant to be shown to anyone.
- **`project/`** — the actual DevOps project being built: application code, Kubernetes manifests,
  Terraform infrastructure, CI/CD, monitoring. This is the piece meant to be shown in an
  interview.

`CLAUDE.md` sits at the root, not inside either folder — Claude Code only auto-reads it from the
folder it's pointed at, so it has to stay at the top level for the automation to work at all.

```
ignite/
├── CLAUDE.md              — rules Claude Code follows every session
├── README.md              — this file
├── learning/
│   ├── roadmap.md         — fixed 53-topic/120-day baseline + live pacing
│   ├── progress.md        — session log, quiz record, deferred-mastery tracker
│   ├── handbook_status.md — quiz-passed tracker per topic (separate from publishing to the
│   │                         handbook site, which happens on its own timeline)
│   ├── session_notes.md   — personal recap per session
│   └── notes/              — per-topic study notebooks, filed under phase-N-name/ subfolders
└── project/
    ├── README.md          — describes the DevOps project itself
    ├── app/
    ├── k8s/
    ├── terraform/
    ├── ansible/
    ├── monitoring/
    ├── docs/
    └── scripts/
```

## How the learning side works
Every session, Claude Code:
1. Reads `learning/roadmap.md` and `learning/progress.md` to know exactly what topic is next and
   whether anything is mid-remediation.
2. Teaches the topic live — explanation, real commands, hands-on, corrected in real time.
3. Tests immediately afterward, same session, interview-style (open-ended, follow-ups, no
   multiple choice) — never the next day.
4. If the test fails: re-teaches with a genuinely different approach, up to 3 total attempts. A
   topic still not solid after 3 attempts gets deferred and revisited later using one of the
   built-in reserve buffer days — it never just quietly slides forward unresolved.
5. Logs the session to `learning/progress.md` and `learning/session_notes.md`, commits, pushes.

Multi-day topics get progressively harder content each day (concept, then independent practice,
then the hardest real-world scenario), with the quiz happening once, on the topic's final day.

Full rules live in `CLAUDE.md` — this is the short version.

## How the project side works
The project in `project/` is built incrementally, session by session, alongside the learning
above rather than as a separate task at the end. Whatever hands-on work a topic produces gets
applied directly here wherever it reasonably can.

One deliberate exception: until the Python phase (roughly two-thirds through the plan), any
application code in `project/app/` is Claude-authored boilerplate — functional, but not yet
something to defend in an interview. That gets rewritten from real understanding once Python is
actually covered.

See `project/README.md` for what the project specifically does and how to run it, filled in as
it's actually built.

## Timeline
6 months total. The roadmap's day allocations sum to roughly 120 aggressive days — the remaining
~60 are intentional slack for remediation and polish, not contingency for falling behind.

## Picking this up on any given day
Open Claude Code in this folder and say what you're there for. It reads `learning/progress.md`
either way, resumed session or brand new one — the state lives in the files, not in chat memory.
