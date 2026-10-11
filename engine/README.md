# The Ignition Engine

The teaching and examination protocol that runs this repository, extracted into a reusable form.
Everything specific to DevOps has been pulled out of it — what remains is a set of rules about how
to be taught and tested by an AI, and they work for any subject you can break into topics.

Ignite itself is **mission #1 running on this engine**. The record in [`learning/`](../learning/)
— 17 sessions, 11 topics cleared, one visible failure, every quiz logged — is what the engine
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
| [`CLAUDE.template.md`](CLAUDE.template.md) | The protocol — session shape, quiz rules, the 3-attempt mastery rule, logging | Copy to your repo root as `CLAUDE.md`, **unedited** |
| [`MISSION.template.md`](MISSION.template.md) | The mission — your goal, deadline, timezone, topic table, optional project | Copy to your repo root as `MISSION.md`, then **edit — this is the only file you touch** |
| [`templates/`](templates/) | Blank starting state for the record files | Copy into `learning/` |
| [`QUICKSTART.md`](QUICKSTART.md) | The whole setup, walked through | Follow it — under five minutes |

The split is deliberate. The protocol file never contains anything about *your* mission, so it is
copied verbatim — no find-and-replace across a rules file, no placeholder you forget to fill. All
parameters live in `MISSION.md`, and the protocol reads them from there at the start of every
session. One file to edit is what makes "five minutes to first session" honest.

## What the protocol actually enforces

- **Teach, then test the same session.** Every topic ends in an interview-style quiz — open-ended,
  "walk me through it," pushback on memorised-sounding answers, no multiple choice, ever.
- **The 3-attempt mastery rule.** A failed quiz forces the teaching to escalate: a different
  explanation the second time, decomposition into smallest parts the third. Repeating an
  explanation is explicitly disallowed. Still not solid after three: logged as deferred mastery
  with a hard revisit deadline — it never quietly slides forward.
- **A record that stays real.** One commit per session, scores computed fresh against a fixed
  rubric, check-in/check-out timestamps never edited, failures logged where they happened.
- **Pacing you can trust.** A fixed baseline that never changes, a living pacing layer that does,
  an explicit buffer pool, and forced recalibration when the plan drifts 5+ days.
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
what a fresh fork gets: ignite keeps its parameters in [`CLAUDE.md`](../CLAUDE.md) and
[`learning/roadmap.md`](../learning/roadmap.md) rather than a root `MISSION.md`. The rules are the
same rules; the engine is those rules with the DevOps removed. Ignite is not being migrated onto
the template mid-run — a record's files should not be reshuffled while the record is being written.
