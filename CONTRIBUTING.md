# Contributing

This repository is an unusual shape, so it is worth two minutes of reading before you open anything.
The short version: **`orbit/` takes pull requests, `learning/` does not.**

## Why the two halves are treated differently

`learning/` is a dated, first-person record of how a specific person learned a specific curriculum —
including the wrong turns, the failed quiz, and the sessions where nothing got built. Its value comes
entirely from being an unedited account. A pull request that improves the prose in a notebook, tidies
the reasoning, or fills in a gap does not make it better; it stops it being a record.

`orbit/` is ordinary software and is treated as such.

## What is genuinely welcome

**Factual errors in a notebook or in `field_atlas.md` — open an issue.**
This is the most useful thing you can do here. Notebooks are technical reference material, and a wrong
rule recorded confidently is worse than no rule at all. Please include:

- the file and line
- what is stated
- what is actually correct
- **a source that shows it**

The source matters because every technical claim in this repo is supposed to be verified before being
written down. With one, the correction gets made and re-verified through the same process everything
else went through. Without one, it becomes a debate.

**Bugs or improvements in `orbit/` — open a pull request.** Normal rules. Keep it scoped, say what you
changed and why.

**Questions about the method itself — open an issue.** How the mastery rule works in practice,
how the quizzes are structured, how to adapt `rules.md` to a different subject. These get asked a
lot and the answers are useful to more than one person.

## What will be closed, and why

Not out of rudeness — just so nobody spends effort on something that cannot be merged:

- **Rewrites, restructures, or style edits to anything under `learning/`.** See above.
- **Edits to `learning/progress.md` or `learning/handbook_status.md`.**
  These are the log. Only the person who lived the sessions can write them.
- **Changes to `learning/roadmap.md`'s baseline table.** It is the plan of record, and changing it
  is the author's call alone; only the pacing layer beneath it moves session to session. Keeping
  it still is what makes "am I on track?" answerable at all.
- **New topics added to the curriculum.** The 53 are the plan of record for this run, and changing
  them is the author's call. If you want a different curriculum, fork it — that is explicitly
  encouraged, see below.
- **Edits to recorded scores, session dates, or check-in / check-out timestamps.** These are the
  record. Their value depends on being real.

## Forking it for your own curriculum

This is the intended reuse, and it is packaged: [`engine/`](engine/) holds the whole teaching and
examination protocol with everything DevOps-specific removed — a portable `rules.md` you copy
unedited, the short `CLAUDE.md` that loads it, a `MISSION.md` template where your own topics,
phases and deadline go, and blank templates for the record files. [`engine/README.md` → Quickstart](engine/README.md#quickstart) walks the whole
setup in about five minutes.

You do not need to credit the fork, though a link back is appreciated. If you build something
interesting with it, an issue saying so would genuinely be welcome.

## Conventions, if you do end up touching files

Every convention this repo follows — dates, topic naming, redaction, notebook formatting — is
written once, in [`rules.md`](rules.md). Read §7 before editing anything. Nothing is restated here,
deliberately: a convention documented in two places is a convention that will eventually
contradict itself.

## Reporting something sensitive

If you find a security problem — including an example in this repo that teaches an insecure pattern
other people might copy — please read [`SECURITY.md`](SECURITY.md) rather than opening a public issue.
