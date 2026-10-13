# The Ignition Engine

The teaching and examination protocol that runs this repository, extracted into a reusable form.
Everything specific to DevOps has been pulled out of it — what remains is a set of rules about how
to be taught and tested by an AI, and they work for any subject you can break into topics.

Ignite itself is **mission #1 running on this engine**. The record in [`learning/`](../learning/)
— 18 sessions, 11 topics cleared, one visible failure, every quiz logged — is what the engine
produces when it runs for real. You are looking at the output and the machine in the same repo.

## The idea in three sentences

You cannot fork someone's learning, but you can fork their teacher. The engine turns Claude Code
from a reference tool into a teacher and examiner in one continuous relationship: it teaches each
topic live, quizzes you interview-style the same session, escalates the teaching when you fail,
and logs everything so the record is real. You supply one file — a mission — and it supplies the
discipline.

## The pieces

| File | What it is | What you do with it |
|---|---|---|
| [`rules.template.md`](rules.template.md) | The protocol — session shape, quiz rules, the mastery rule, logging, audits | Copy to your repo root as `rules.md`, **unedited** |
| [`CLAUDE.template.md`](CLAUDE.template.md) | A short loader that imports `rules.md` so it lands in context every session | Copy to your repo root as `CLAUDE.md`, **unedited** |
| [`MISSION.template.md`](MISSION.template.md) | The mission — your goal, deadline, timezone, topic table, optional project | Copy to your repo root as `MISSION.md`, then **edit — this is the only file you touch** |
| [`templates/`](templates/) | Blank starting state for the record files | Copy into `learning/` |

The split is deliberate. The protocol file never contains anything about *your* mission, so it is
copied verbatim — no find-and-replace across a rules file, no placeholder you forget to fill. All
parameters live in `MISSION.md`, and the protocol reads them from there at the start of every
session. One file to edit is what makes "five minutes to first session" honest.

## Quickstart

Your own mission in five minutes.

What you need: [Claude Code](https://claude.com/claude-code), git, a POSIX-style shell (Git
Bash, WSL, macOS/Linux Terminal — not PowerShell/cmd.exe, which don't accept every command below
as written), and a subject you actually want to learn, broken into topics. The five minutes
covers the setup; writing a good topic table deserves longer thought — you can start with two
phases and refine before Day 1; once the mission starts, change it only deliberately.

### 1. Get the engine (~1 min)

Clone ignite once, anywhere — you only need it as the source to copy from:

```bash
git clone https://github.com/saranya-sallagundla/ignite.git
```

### 2. Create your mission repo (~1 min)

Create an empty repo first — on GitHub or wherever you host — and note its URL. The protocol
commits and pushes after every session starting Day 1, so a remote needs to exist before then;
without one, the first push fails outright.

```bash
mkdir my-mission && cd my-mission
git init
git remote add origin <your-new-repo-url>

cp ../ignite/engine/rules.template.md    rules.md
cp ../ignite/engine/CLAUDE.template.md   CLAUDE.md
cp ../ignite/engine/MISSION.template.md  MISSION.md

mkdir -p learning/notes
cp ../ignite/engine/templates/progress.md         learning/
cp ../ignite/engine/templates/handbook_status.md  learning/
cp ../ignite/engine/templates/notes/README.md     learning/notes/
cp ../ignite/engine/templates/audits.md           audits.md
```

Both are copied **unedited**, and both names matter. `CLAUDE.md` is the name Claude Code auto-loads
from the folder it's launched in; all it does is `@rules.md`, which pulls the protocol into context
every session without you asking. `rules.md` is the protocol itself, and nothing in it is specific
to any mission — that all lives in `MISSION.md`.

Keeping them apart is deliberate: rules go in one file, so there is exactly one place to edit and
no second copy to drift out of sync. If you change how the protocol works, you are running your own
variant, which is allowed but should be deliberate.

### 3. Edit MISSION.md — the only editing there is (~3 min)

Open `MISSION.md` and fill in, top to bottom:

1. **Mission** — one sentence stating the end condition.
2. **Parameters** — Day 1, timezone, outer deadline. Keep the quiz cap, attempt limit and audit
   cadence defaults unless you have a reason.
3. **Redaction** — what must never appear in file content, and its placeholder.
4. **The topic table** — your phases, topics, and day allocations. This is the part worth real
   thought: topic names are copied verbatim everywhere, day counts should be honest for your
   actual free hours, and once the mission starts the table changes only by deliberate decision.
5. **Parallel project** — define one, or delete the section.

Delete the template comments as you go. Commit and push — the remote you added in step 2 is what
makes this work:

```bash
git add -A && git commit -m "Mission start: <name>, Day 1 <date>"
git push -u origin main
```

### 4. Start (~10 seconds)

Open Claude Code in the folder and say:

> start session 1

The protocol takes it from there: it reads `MISSION.md` and `learning/progress.md`, teaches
Topic 1, and — when the topic's final day ends — quizzes you on it, interview-style, the same
session. Expect the quiz to push back on vague answers. That is the product working.

### Alternative: fork ignite instead

If you would rather keep mission #1's record alongside yours as a worked example, fork the whole
repo instead of step 2's fresh `git init`. You're already inside it, with a remote already
configured (GitHub's fork), so the commands change shape slightly — run these from the fork's own
root, not against a `../ignite` sibling that won't exist:

```bash
cp engine/rules.template.md    rules.md
cp engine/CLAUDE.template.md   CLAUDE.md
cp engine/MISSION.template.md  MISSION.md
```

Then clear everything specific to mission #1 before your Day 1, not just `learning/`:
- `learning/` — `progress.md`, `handbook_status.md`, `notes/`, `roadmap.md`,
  `field_atlas.md` (replace with the blank `templates/` versions, same as step 2).
- `orbit/` — mission #1's own project. Repurpose it for yours, rename it, or delete it; nothing
  here transfers to a different subject.
- `audits.md` — mission #1's DevOps-specific audit records. Clear them and start your own index
  (the blank `templates/audits.md` has the format).
- `CONTRIBUTING.md`, `docs/project_ideas.md` — both describe mission #1's specific project;
  rewrite or delete rather than leaving them describing something you didn't build.

A fresh repo is cleaner; the fork is more self-documenting once cleared. Either works.

### What to expect from the first week

Session 1 will feel slower than self-study — being made to execute everything live and defend
answers out loud is slower than reading. That is the point; speed was never the bottleneck,
retention was. By the first multi-day topic you will have a feel for the rhythm: teach, do,
overwrite the status line, commit. If a quiz fails, the re-teach *must* come at the topic
differently — if it feels like the same explanation again, say so and demand another angle. The
protocol is on your side there.

## What the protocol actually enforces

- **Teach, then test the same session.** Every topic ends in an interview-style quiz — open-ended,
  "walk me through it," pushback on memorised-sounding answers, no multiple choice, ever.
- **The mastery rule.** A failed quiz forces the teaching to escalate: a different explanation the
  second time, decomposition into smallest parts the third. Repeating an explanation doesn't count
  as an attempt. Still not solid: logged as deferred mastery with a revisit deadline — it never
  quietly slides forward.
- **A record that stays real.** One commit per session, scores computed fresh against a fixed
  rubric, nothing backdated or quietly improved, failures logged where they happened.
- **Pacing you can trust.** A baseline that sits apart from the day-to-day, a living pacing layer
  that moves, an explicit buffer pool, and forced recalibration when the plan drifts 5+ days.
- **A periodic whole-repo audit** every 10 topics, findings reviewed before fixes.
- **Optionally, one real project** built incrementally alongside — so hands-on work lands in a
  system that accumulates, not a folder of disposable tutorials.

Why these rules and not others — the learning-science reasoning, and its honest limits — is in
[`docs/why-this-works.md`](../docs/why-this-works.md).

## Why the engine lives inside ignite

A separate repo would collect stars of its own, but this layout was chosen deliberately: every
fork of ignite already carries its own teacher, the worked example and the machine stay in sync in
one place, and the whole thing remains one repository to audit and mirror. If the engine outgrows
this arrangement, `git subtree split -P engine` can lift it into its own repository with history
intact. Reversible decisions get made quickly.

## License

Everything in this folder is covered by CC BY 4.0 — see [`../learning/LICENSE`](../learning/LICENSE).
Copy, adapt, and run your own mission on it freely; attribution (a link back) is appreciated, not
required beyond what the license itself asks for.

## Relationship to mission #1

Ignite predates its own engine — the protocol was written for one mission first and generalised
after 17 real sessions, not designed on a whiteboard. So mission #1's layout differs slightly from
what a fresh fork gets: ignite keeps its parameters in [`rules.md`](../rules.md) and
[`learning/roadmap.md`](../learning/roadmap.md) rather than a root `MISSION.md`. The rules are the
same rules; the engine is those rules with the DevOps removed. Ignite is not being migrated onto
the template mid-run — a record's files should not be reshuffled while the record is being written.
