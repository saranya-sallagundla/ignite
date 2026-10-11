# Quickstart — your own mission in five minutes

What you need: [Claude Code](https://claude.com/claude-code), git, a POSIX-style shell (Git
Bash, WSL, macOS/Linux Terminal — not PowerShell/cmd.exe, which don't accept every command below
as written), and a subject you actually want to learn, broken into topics. The five minutes
covers the setup; writing a good topic table deserves longer thought — you can start with two
phases and refine before Day 1, but once the mission starts, the baseline freezes.

## 1. Get the engine (~1 min)

Clone ignite once, anywhere — you only need it as the source to copy from:

```bash
git clone https://github.com/saranya-sallagundla/ignite.git
```

## 2. Create your mission repo (~1 min)

Create an empty repo first — on GitHub or wherever you host — and note its URL. The protocol
commits and pushes after every session starting Day 1, so a remote needs to exist before then;
without one, the first push fails outright.

```bash
mkdir my-mission && cd my-mission
git init
git remote add origin <your-new-repo-url>

cp ../ignite/engine/CLAUDE.template.md   CLAUDE.md
cp ../ignite/engine/MISSION.template.md  MISSION.md

mkdir -p learning/notes
mkdir -p audits
cp ../ignite/engine/templates/progress.md         learning/
cp ../ignite/engine/templates/handbook_status.md  learning/
cp ../ignite/engine/templates/session_notes.md    learning/
cp ../ignite/engine/templates/notes/README.md     learning/notes/
cp ../ignite/engine/templates/audits/README.md    audits/
```

`CLAUDE.md` is copied **unedited**, and the name is not optional — Claude Code auto-loads a file
by that exact name from the folder it's launched in, which is the whole mechanism that makes the
protocol load every session without you asking for it. It is the protocol, and nothing in it is
specific to any mission. If you change how it works, you are running your own variant, which is
allowed but should be deliberate.

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

Delete the template comments as you go. Commit and push — the remote you added in step 2 is what
makes this work:

```bash
git add -A && git commit -m "Mission start: <name>, Day 1 <date>"
git push -u origin main
```

## 4. Start (~10 seconds)

Open Claude Code in the folder and say:

> start session 1

The protocol takes it from there: it reads `MISSION.md` and `learning/progress.md`, teaches
Topic 1, and — when the topic's final day ends — quizzes you on it, interview-style, the same
session. Expect the quiz to push back on vague answers. That is the product working.

## Alternative: fork ignite instead

If you would rather keep mission #1's record alongside yours as a worked example, fork the whole
repo instead of step 2's fresh `git init`. You're already inside it, with a remote already
configured (GitHub's fork), so the commands change shape slightly — run these from the fork's own
root, not against a `../ignite` sibling that won't exist:

```bash
cp engine/CLAUDE.template.md   CLAUDE.md
cp engine/MISSION.template.md  MISSION.md
```

Then clear everything specific to mission #1 before your Day 1, not just `learning/`:
- `learning/` — `progress.md`, `handbook_status.md`, `session_notes.md`, `notes/`, `roadmap.md`,
  `field_atlas.md` (replace with the blank `templates/` versions, same as step 2).
- `orbit/` — mission #1's own project. Repurpose it for yours, rename it, or delete it; nothing
  here transfers to a different subject.
- `audits/` — three DevOps-specific audit records. Clear them and start your own index (the blank
  `templates/audits/README.md` has the format).
- `CONTRIBUTING.md`, `docs/project_ideas.md` — both describe mission #1's specific project;
  rewrite or delete rather than leaving them describing something you didn't build.

A fresh repo is cleaner; the fork is more self-documenting once cleared. Either works.

## What to expect from the first week

Session 1 will feel slower than self-study — being made to execute everything live and defend
answers out loud is slower than reading. That is the point; speed was never the bottleneck,
retention was. By the first multi-day topic you will have a feel for the rhythm: teach, do,
overwrite the status line, commit. If a quiz fails, the re-teach *must* come at the topic
differently — if it feels like the same explanation again, say so and demand another angle. The
protocol is on your side there.
