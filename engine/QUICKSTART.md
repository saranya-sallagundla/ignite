# Quickstart — your own mission in five minutes

What you need: [Claude Code](https://claude.com/claude-code), git, and a subject you actually
want to learn, broken into topics. The five minutes covers the setup; writing a good topic table
deserves longer thought — you can start with two phases and refine before Day 1, but once the
mission starts, the baseline freezes.

## 1. Get the engine (~1 min)

Clone ignite once, anywhere — you only need it as the source to copy from:

```bash
git clone https://github.com/saranya-sallagundla/ignite.git
```

## 2. Create your mission repo (~1 min)

```bash
mkdir my-mission && cd my-mission
git init

cp ../ignite/engine/CLAUDE.template.md   CLAUDE.md
cp ../ignite/engine/MISSION.template.md  MISSION.md

mkdir -p learning/notes audits
cp ../ignite/engine/templates/progress.md         learning/
cp ../ignite/engine/templates/handbook_status.md  learning/
cp ../ignite/engine/templates/session_notes.md    learning/
cp ../ignite/engine/templates/notes/README.md     learning/notes/
```

`CLAUDE.md` is copied **unedited** — it is the protocol, and nothing in it is specific to any
mission. If you change how it works, you are running your own variant, which is allowed but
should be deliberate.

## 3. Edit MISSION.md — the only editing there is (~3 min)

Open `MISSION.md` and fill in, top to bottom:

1. **Mission** — one sentence stating the end condition.
2. **Parameters** — Day 1, timezone, outer deadline. Keep the quiz cap, attempt limit and audit
   cadence defaults unless you have a reason.
3. **Redaction** — what must never appear in file content, and its placeholder.
4. **The topic table** — your phases, topics, and day allocations. This is the part worth real
   thought: topic names are copied verbatim everywhere, day counts should be honest for your
   actual free hours, and the table freezes when the mission starts.
5. **Parallel project** — define one, or delete the section.

Delete the template comments as you go. Commit:

```bash
git add -A && git commit -m "Mission start: <name>, Day 1 <date>"
```

## 4. Start (~10 seconds)

Open Claude Code in the folder and say:

> start session 1

The protocol takes it from there: it reads `MISSION.md` and `learning/progress.md`, teaches
Topic 1, and — when the topic's final day ends — quizzes you on it, interview-style, the same
session. Expect the quiz to push back on vague answers. That is the product working.

## Alternative: fork ignite instead

If you would rather keep mission #1's record alongside yours as a worked example, fork the whole
repo and do steps 2–3 *inside* the fork: the copies overwrite `CLAUDE.md` with the template
version, and you clear `learning/` of mission #1's record (`progress.md`, `handbook_status.md`,
`session_notes.md`, `notes/`, `roadmap.md`, `field_atlas.md`) before your Day 1. A fresh repo is
cleaner; the fork is more self-documenting. Either works.

## What to expect from the first week

Session 1 will feel slower than self-study — being made to execute everything live and defend
answers out loud is slower than reading. That is the point; speed was never the bottleneck,
retention was. By the first multi-day topic you will have a feel for the rhythm: teach, do,
overwrite the status line, commit. If a quiz fails, the re-teach *must* come at the topic
differently — if it feels like the same explanation again, say so and demand another angle. The
protocol is on your side there.
