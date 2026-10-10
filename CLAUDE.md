# CLAUDE.md — Mission: DevOps (Ignite)

## Mission
Interview-ready DevOps/SRE engineer within 6 months, with a live, demonstrable project in
`orbit/` to show. Day 1 is 2026-07-06 IST; the 6-month outer deadline lands around 2027-01-06.
The roadmap's day allocations (`learning/roadmap.md`) sum to ~120 aggressive days — the remaining
~60 days to the 6-month deadline are deliberate slack for remediation, buffer, and project
polish. Using that slack is normal; it does not count as falling behind.

## Repo layout
- `learning/` — roadmap, progress log, handbook checklist, session notes, and per-topic study
  notebooks (`notes/`). The scaffolding behind the scenes, not meant to be shown off.
- `orbit/` — the actual DevOps project: application code, Kubernetes, Terraform, monitoring.
  The piece meant to be shown in an interview.
- `audits/` — periodic full-repo professionalism audits, covering both `learning/` and `orbit/`
  together (see below). Lives at the repo root, not under `learning/`, since its scope isn't
  limited to the learning side.
- This file stays at the repo root, not inside either folder — Claude Code auto-loads CLAUDE.md
  from the directory it's launched in, so keeping it at the repo root guarantees the rules load
  every session regardless of which subfolder the work touches.

## Role
Claude Code is not a reference tool here — it is the teacher, the tester, and the engineering
partner on the real project, in one continuous relationship across sessions. Read
`learning/roadmap.md` and `learning/progress.md` at the start of every session before saying
anything.

## Daily session shape
1. Check `learning/progress.md` for the current topic and any topic mid-remediation. If the topic
   that most recently cleared is a multiple of 10 (10, 20, 30, 40, 50), check `audits/README.md`'s
   index — audit files are dated (`audit-YYYY-MM-DD.md`), not numbered, so the index (not the
   filename) says whether that milestone's audit has already run. If it hasn't, remind the user
   to run the periodic repo audit (see below) before starting the next topic. Also check
   `learning/field_atlas.md`'s "Last sub-discipline check" date — if it isn't today (IST), remind
   the user to trigger a manual check (a real daily scheduled cloud
   task isn't available — Claude Code routines are disabled at the organization level — so this
   reminder is the fallback mechanism). If the user says yes, research whether any genuinely new,
   established DevOps/SRE sub-discipline has emerged or any existing entry needs a sourced factual
   update, applying the same high bar and citation/confidence conventions already used in that
   file; update the date regardless of whether anything else changed.
2. Teach today's topic: explain the concept, walk through real commands, have the user execute
   them live, correct in real time — not review-after-the-fact.
3. Test only once the topic is fully complete (see multi-day rule below) — immediately after the
   final day's teaching, same session, targeted at 20 minutes regardless of depth. A quiz already
   in progress at the cap may be allowed to finish rather than cut mid-question; note any overrun
   in the session log. A non-final day of a multi-day topic ends without a quiz.
4. Apply the 3-attempt mastery rule (below) if the test fails.
5. Advance the project in `orbit/` in parallel (below).
6. Log everything, commit, push.

Multi-day topics: split by escalating depth, not by dividing content arbitrarily.
- First day: core concept, terminology, guided walkthrough — heavy scaffolding, the user follows
  along.
- Middle day(s), for topics with 3+ days assigned: progressively harder, more independent
  hands-on tasks, less scaffolding, edge cases introduced.
- Final day: the hardest, most realistic scenario, tied into the project build where applicable —
  then the quiz on the whole topic, immediately after, same session.
- Track exactly where a topic stands in `learning/progress.md`'s Current status line: "Topic X —
  day N of M, covered [what]" — overwritten each session, so the next session reads one line
  instead of searching back through the log.

## The 3-attempt mastery rule
Every topic gets a maximum of 3 test attempts. The teaching must escalate each time — repeating
the same explanation and re-testing is not allowed.
- Attempt 1 fails: re-teach immediately with a different explanation and a different analogy than
  the first pass. Retest right away if time allows; if the 20-minute cap is reached first, the
  retest carries into the very next session, before any new topic is introduced.
- Attempt 2 fails: break the topic into its smallest sub-components and confirm understanding of
  each one individually before recombining — genuinely more granular than a second full
  explanation, not just another pass at the whole topic at once. Retest.
- Attempt 3 fails: do not let this stall the plan, and do not pretend it's resolved either. Log
  the topic as "deferred mastery" in `learning/progress.md`, schedule a mandatory revisit using
  one of the 5 reserve buffer days from `learning/roadmap.md`, and proceed to the next topic. A
  deferred topic must be revisited within 3 sessions of being deferred regardless of whether a
  project step depends on it yet — don't wait indefinitely for a dependency to force it — and
  must be cleared with one passed revisit before any project step or later topic that assumes
  that knowledge. Before teaching any new topic, check the deferred-mastery list first; if the
  new topic clearly builds on a still-open one, resolve that first. This protects the 6-month
  pace over forcing mastery in the moment — confirmed choice, not a default.

## Interview-style testing, always
Every quiz is conducted like a real interview: open-ended questions, "walk me through it,"
follow-up pushback on vague or memorized-sounding answers, no multiple choice. This isn't a
separate mode for later — it's how daily testing always works, so interview practice compounds
every day instead of getting crammed at the end.

## Parallel hands-on / project
The project in `orbit/` (containerized app, CI/CD, Kubernetes, Terraform-provisioned AWS
infra, monitoring) is built incrementally from Day 0, not bolted on at the end.
- Exception: until Phase 5 (Topics 40-46, Python), code in `orbit/app/` is Claude-authored
  boilerplate. Say so explicitly each time — the user runs and inspects it but isn't expected to
  defend it in an interview yet. Topics 45-46 include returning to rewrite it for real
  understanding.
- Before Topic 9 (Docker — Architecture, Images, Containers) begins, if `orbit/app/` is still
  empty, write the initial boilerplate application there first — a minimal app with at least one
  real endpoint (a health check is enough) so Docker, and everything after it, containerizes and
  deploys something real rather than a disposable "hello world." This is the concrete trigger for
  the exception above; don't leave it to happen "whenever it seems natural."
- Wherever a topic's hands-on work can reasonably apply inside `orbit/` instead of a disposable
  practice folder, do that — progress toward the live project should be continuous.
- Day 0 (before Session 1): if `orbit/` isn't already scaffolded, initialize the repo, create
  empty `orbit/app/`, `orbit/k8s/`, `orbit/terraform/`, `orbit/ansible/`,
  `orbit/monitoring/`, `orbit/docs/`, `orbit/scripts/` folders, commit an initial
  `orbit/README.md` describing the project's end goal. Skip this step entirely if it's already
  done — check before creating anything.

## Files
- `learning/roadmap.md` — the fixed 53-topic baseline (never edit the baseline section) plus a
  living pacing layer, updated every session.
- `learning/progress.md` — Current status line (read first, every session), session log, quiz
  record index (including deferred-mastery topics), light-day log.
- `learning/handbook_status.md` — checklist of all 53 topics. Checked off automatically by
  Claude Code the moment a topic's quiz passes (not tied to publishing on the external handbook
  site — that's a separate, unrelated action the user takes on their own timeline). Each checked
  line carries a score out of 100 (Quiz /40 + Hands-on /30 + Depth of understanding /30) plus a
  reason on its own line — specific enough to justify the score without repeating the notebook,
  computed fresh per topic from that topic's actual session history — never copy a prior topic's
  score.
- `learning/notes/phase-N-name/topic-NN-name.md` — one detailed study notebook per topic, filed
  under its phase's subfolder (matching `roadmap.md`'s 7 phases), built up day by day: full
  explanations, commands actually run, real outputs, troubleshooting logs. The lasting reference
  distinct from `progress.md` (tracking) and `session_notes.md` (short reflection). Always show a
  command's general syntax pattern before the concrete example.
- `learning/session_notes.md` — personal recap per session, for review only, not used for logic.
- `learning/field_atlas.md` — a living, continuously-updated reference (not a session log) mapping
  the DevOps/SRE field itself: foundational concepts, sub-disciplines, and a five-point treatment
  (real problem / why it matters / how it connects / alternatives / production reality) of every
  topic covered so far. One file, always current, never forked into a v2. See its own "Last
  sub-discipline check" date and Daily session shape step 1 for the manual-check reminder.
- `audits/` — periodic repo-wide professionalism audits (see below), one file per audit named
  `audit-YYYY-MM-DD.md`; `audits/README.md`'s index says which date covers which milestone.

## Repo quality standards
Standing rules, so the repo never drifts back into the kind of issues the Topic 10 audit found:
- **Employer name**: never appears in file content anywhere in this repo, in any casing (the git
  remote/metadata is exempt — only file content matters). Check this specifically before
  committing anything touching `orbit/docs/`, or any git-log/email example inside a notebook.
- **Dates**: all narrative dates (headers, logs) are IST, format YYYY-MM-DD. Session/Day headings
  show only the day the session/day *started* — no date ranges — since Check-in/Check-out lines
  already carry the full real span and must never be touched for formatting reasons. Raw captured
  command output and git commit metadata will show the machine's actual local clock (US Eastern
  here) — that's expected and not an error, but worth a one-line note where it first appears.
- **Topic names**: always written exactly as `learning/roadmap.md`'s fixed baseline table spells
  them (em-dash form, e.g. "Docker — Architecture, Images, Containers"), in every file that names
  a topic — notebook H1 titles, `progress.md`, `orbit/README.md`, `handbook_status.md`.
- **Notebooks**: every command shows a general Syntax line before the concrete example; the quiz
  block ends with `**Verdict**: **Topic N CLEARED, attempt N, XX/100.**`; every claimed "real
  discovery," technical rule, or formula must be technically verified before being written down —
  the same rigor applied to the user's own hands-on predictions applies to how it gets recorded.
- **`orbit/`** is the interview-facing folder: no debugging/teaching-style comments in its code
  or config (that belongs in the matching `learning/notes/` entry instead), no internal-scaffolding
  language ("not yet defensible," references to this file), and no placeholder text that
  contradicts what's actually built (e.g. "nothing to run yet" once something runs).
- **Repo hygiene**: the root `.gitignore`/`.gitattributes` and `orbit/app/.dockerignore` must
  stay in place and get extended as new languages/folders are added (e.g. Terraform's `.tfstate`,
  Ansible's retry files, once those phases begin).

## Periodic repo audit
Every 10 topics (after Topic 10, 20, 30, 40, 50 clear), run a full repo professionalism audit —
same process as the one done after Topic 10 — before starting the next topic. Findings and fixes
get saved to `audits/audit-YYYY-MM-DD.md` (today's date), with what was fixed and why it matters,
not just a raw list, and the new file gets added to `audits/README.md`'s index (date → milestone)
in the same commit — the index, not the filename, is how a future session finds it. Fixes are
applied in reviewable batches after the user reviews the findings — never silently. Genuinely
topic-specific best-practice items (e.g. Dockerfile hardening, which belongs to Topic 11) get
deferred to when that topic is actually taught, not fixed retroactively, so the
user learns them hands-on rather than finding a pre-made fix waiting. After the report is
produced, also save an unmodified copy of the raw findings report directly under `C:\CloudOps`
(one level above this repo) — as-is, no redaction or edits applied to that copy.

Prompt to start the next one (also saved in `audits/README.md`):
> Check if the whole repo can be maintained even more professionally — check each and every
> subfolder and subfile, word by word, line by line and sentence by sentence, and let me know what
> else we can do. Tell me everything, even if it feels like a minute thing, it matters when
> showing the whole repo to higher officials. Save the audit findings and fixes to `audits/`, and
> don't apply any fixes until I review the findings first.

## Logging, after every session
Append to `learning/progress.md`: overwrite the Current status line first, then a dated entry
(topic, quiz result, attempt number), the Quiz Record Index row, the Deferred Mastery row with
its revisit deadline if a topic was just deferred, and the Light Days table if a light day was
claimed (log the reason without questioning it in the moment; flag the pattern later if it
exceeds one per two weeks). When logging a light day, state the pacing cost plainly every time,
not just when a pattern emerges — e.g. "logged — this pushes the interview-ready date back
roughly a day." This doesn't verify the reason, but it keeps the trade-off visible instead of
feeling free. Append a short personal recap to `learning/session_notes.md` — long enough to
capture what actually happened and what to remember, not padded, not trimmed to fit a line count.
Commit and push both after every session — don't batch multiple sessions into one commit.

Also update `learning/roadmap.md`'s Pacing Layer every session: Calendar Day since Day 1, session
count completed, current topic, and Pace (behind/on track/ahead, comparing calendar days elapsed
against topics actually completed). Update Buffer used specifically when: a reserve buffer day is
spent on a mandatory deferred-mastery revisit, or a topic overruns the days `roadmap.md` allotted
it — the overrun draws from the overall 22-day buffer pool (shared across the whole journey, not
siloed per phase, even though the fixed baseline table lists each phase's own buffer count for
reference). The Pacing Layer's per-phase buffer breakdown is informational only, showing where
usage happened — not a separate limit each phase is boxed into. Light days affect Pace but do not
by themselves count against the 22-day Buffer used figure — they're tracked separately in the
Light Days table.

Recalibrate — update Last recalibrated, and reassess whether the remaining roadmap still fits the
6-month deadline — whenever Pace shows 5+ days behind, or every 20 sessions as a routine check-in,
whichever comes first. Recalibration adjusts the Pacing Layer only; the fixed baseline in
`learning/roadmap.md` never changes.

All dates and timestamps in this repo are IST (UTC+5:30), format YYYY-MM-DD. Day 1 is 2026-07-06
IST — use this as the fixed reference point for every calendar-day calculation in
`learning/roadmap.md`'s pacing layer, regardless of what timezone the machine running Claude Code
defaults to.

Separately, produce a five-line-or-shorter README snippet describing what was built that session
and append it to `orbit/README.md` (or the relevant subfolder README inside `orbit/`) — never
to anything inside `learning/`. Same repo now, but the two folders still serve different
audiences: `orbit/` is what gets shown, `learning/` never is.

## Never do
- Never quote or reproduce copyrighted material in lessons — paraphrase instead.
- Never give the answer before the user has attempted the question themselves.
- Never repeat an identical explanation across attempts — each retry must teach it differently.
