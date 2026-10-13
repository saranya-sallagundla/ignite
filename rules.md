# Rules

The single source of truth for how this repo is run. `CLAUDE.md` imports this file, so it loads
automatically every session. If a rule appears anywhere else in the repo and disagrees with this
file, **this file wins** — and the other copy should be deleted, not reconciled.

## 0. How to read this file

1. **An explicit instruction from me overrides anything written here.** If I ask for something
   this file discourages, do it. Say once that it departs from the default, then proceed — don't
   argue it, don't ask twice, don't quietly do the default instead.
2. **These are defaults, not laws.** Almost everything below is "this is the sensible thing unless
   there's a reason." Changing a default is normal. Record the change here in the same commit so
   the file stays true.
3. **§9 is what Claude never does on its own.** Those rules protect the honesty of the
   record. If I explicitly ask to break one, say once which §9 rule it breaks and what that
   costs the record, then do it — it's my record.
4. **If this file is wrong, fix it.** A rule written early on that no longer fits is a bug, not a
   constraint.

## 1. The mission and its fixed points

Interview-ready DevOps/SRE engineer in 6 months, with a working system in `orbit/` to demonstrate.

| | |
|---|---|
| Day 1 | 2026-09-14 |
| Outer deadline | ~2027-03-14 |
| Timezone | IST (UTC+5:30) for every narrative date |
| Date format | `YYYY-MM-DD` |
| Curriculum | 53 topics across 7 phases, in `learning/roadmap.md` |
| Day budget | 120 baseline = 98 core + 22 buffer |

Day 1 is the reference point for every calendar-day calculation, whatever timezone the machine
running Claude Code is set to. Raw captured command output and git metadata show the machine's
real local clock (US Eastern) — that difference is expected and needs no note.

This is the only place these numbers are written. Everything else derives from them.

## 2. Start of every session

Before anything else, work out today's real date in IST, then run both checks. They apply to
**every** session — teaching, audit, or a one-off question. Scoping them to teaching days lets them
go unnoticed whenever teaching pauses.

1. **Field atlas currency.** Read the "Last sub-discipline check" date in
   `learning/field_atlas/field-map.md`. More than 14 days old: say so up front and offer to run
   the check. The threshold is 14 days because a reminder that fires every session gets ignored.
2. **Pacing currency.** Recompute Calendar Day from Day 1 and compare it against the figure
   written in `learning/roadmap.md`'s Pacing Layer. If they differ, `Pace` and `Last recalibrated`
   are stale by exactly that much. Check the written number, never the derived verdict — a verdict
   like `Pace: on track` can stay written long after the numbers behind it have moved.

Report both, then get on with the session. Neither check blocks anything.

**Backstop.** Neither check fires if nobody opens Claude Code here at all. A scheduled task
(`ignite-field-atlas-check`, under `~/.claude/scheduled-tasks/`) runs the atlas check on the 1st
and 15th monthly, independent of any session. A run reporting "succeeded" is not proof it did
anything — a run can stall on a permission prompt with nobody present and still report success.
Verify by output via `list_task_runs`, not by status. `CronCreate` is unsuitable here: its jobs
are in-memory and expire after 7 days, reproducing the exact failure this backstop prevents.

## 3. Teaching a session

1. Read `learning/progress.md` — the Current status line, the tables, and the last session entry.
   Not the whole log; the full history stays in the file for reference. Check whether a periodic
   audit is due (§8) or a deferred topic is open.
2. Teach: explain, run real commands, have me execute them live, correct in real time.
3. Quiz once the topic is fully complete — same session as the final day's teaching, never the
   next day. Target ~20 minutes; let one already running finish rather than cutting it
   mid-question, and note the overrun.
4. If the quiz fails, escalate (below).
5. Advance `orbit/` in parallel.
6. Log, commit, push.

**Multi-day topics** split by escalating depth, not by chopping content:
- Day 1 — core concepts, heavy scaffolding, guided.
- Middle days — harder, more independent, edge cases.
- Final day — hardest realistic scenario, tied into `orbit/`, then the quiz.
- A non-final day ends without a quiz. Track position in the Current status line:
  "Topic X — day N of M, covered [what]", overwritten each session.

**When a quiz fails.** Three attempts is the default before deferring; extend it if the topic is
worth the days. What matters is that the *teaching* changes every time — re-explaining the same
way and retesting is the one thing that doesn't count as an attempt.
- Attempt 2: a different explanation and a different analogy.
- Attempt 3: break the topic into its smallest parts, confirm each alone, then recombine.
- Still not solid: log it as deferred mastery in `learning/progress.md`, fund the revisit from
  the buffer, and move on. Revisit within about 3 sessions, and clear it before any topic or
  project step that builds on it. Protecting the 6-month pace over forcing mastery in the moment
  is a deliberate choice, not a fallback.

**Every quiz is an interview.** Open-ended, "walk me through it," follow-up pushback on anything
vague or memorised. No multiple choice. This is how daily testing always works, so interview
practice compounds instead of being crammed at the end.

**Scoring.** Out of 100: Quiz /40 + Hands-on /30 + Depth /30. Computed fresh per topic from that
topic's real session history — never copied from another topic. Each score gets a one-line reason
specific enough to justify it without repeating the notebook.

## 4. The project — `orbit/`

Built incrementally from Day 0, not bolted on at the end. Wherever a topic's hands-on work can
land in `orbit/` instead of a disposable practice folder, put it there.

- Until Phase 5 (Topics 40-46, Python), code in `orbit/app/` is Claude-authored boilerplate. Say
  so each time — I run and inspect it but am not expected to defend it in an interview yet.
  Topics 45-46 return to rewrite it properly.
- `orbit/` is interview-facing. No teaching-style comments in its code or config, no internal
  scaffolding language, no placeholder text contradicting what actually runs.
- `orbit/README.md` is the only README in `orbit/`. It has one section per part — a folder, or a
  root file like `docker-compose.yml` — in this shape:

  ```text
  ### `folder/` — one-line purpose
  - Status: built | started | not built yet — and what's next
  - Files: what's in it now
  - What was done:
    - Session N · Topic N — what was built, how, and the measured result
  - Installed & used:
    - tool + version — what it's for
  - Next: what the next topic adds
  ```

  A part not built yet gets one line: what it will hold and which topic builds it. After a
  session that changes `orbit/`, update that part's section — never anything under `learning/`.
- Create a folder in `orbit/` when the topic that fills it begins, not before. No placeholder
  READMEs.
- Voice for `orbit/README.md`: engineering, not teaching — what was built, how, and the measured
  result. No quizzes, scores, analogies or day counts; those live in `learning/`. No dates —
  `Session N · Topic N` only; `progress.md` has the dates. Every installed tool gets its version
  and what it's for.

## 5. Where things get written

| File | Holds |
|---|---|
| `learning/roadmap.md` | Fixed 53-topic baseline + the living Pacing Layer |
| `learning/progress.md` | Current status line, quiz index, deferred mastery, open items, light days, and the full session log — one detailed entry per session (§6) |
| `learning/handbook_status.md` | Per-topic checklist with score and reason |
| `learning/notes/phase-N/topic-NN-*.md` | The detailed study notebook — the lasting reference |
| `learning/field_atlas/` | Living map of the field itself, in two files: `field-map.md` (the field, plus the atlas's maintenance rules) and `topic-map.md` (topics covered). Not a session log |
| `audits/` | Findings filed by subject in four files; index, history and prompts in `audits/README.md` |

The roadmap's baseline table is the plan of record. Change it deliberately if the curriculum
should change — update the table and say why in the Pacing Layer. It isn't frozen; it's just not
something to edit casually, because a moving baseline makes "am I on track?" unanswerable.

**The field atlas.** Part 2 (topics covered) grows when a topic clears, so it can't silently lag.
Part 1 (the state of the field) has no such trigger — that half is what the currency check in §2
exists for. The sub-discipline check researches whether a genuinely new sub-discipline has emerged
or an existing entry needs a sourced update: a named primary source beats a secondary summary, say
plainly when nothing reliable was found, and separate confidence-in-direction from
confidence-in-figure. Update the check date even when nothing changed, so a no-change result reads
as a real check. It's two files: `field-map.md` holds Part 1 and the maintenance rules,
`topic-map.md` holds Part 2.

## 6. Logging, after every session

Append to `learning/progress.md`: overwrite the Current status line first, then add the session
entry (shape below), the Quiz Record Index row, a Deferred Mastery row if one was just opened, and
the Light Days table if a light day was claimed. Log a light day's reason without questioning it
in the moment, and state the pacing cost plainly every time — e.g. "this pushes the
interview-ready date back roughly a day."


**Open items.** A session's Carry-forward becomes a row in the Open items table. An audit item held
for a later topic goes in too. When one is done, set its Status to `done — Session N`; don't delete
the row.

**Session entry shape.** Same labels, same order, every time. Lines marked "if any" are left out
when there is nothing to say.

```text
### Session N — YYYY-MM-DD — Short title
- Topic: Topic N — Exact Name — day X of Y — in progress | completed | revisit of deferred topic
- Covered:
  - Learned: every concept taught
  - Taught with: the analogy or method used (if any)
  - Hands-on: what was built or run
  - Setup: environment, tools installed + versions (if any)
  - Problems & fixes: issue → cause → fix, or "not fixed" (if any)
  - Discovery: something unexpected found (if any)
  - Revision: what was re-taught, and how (if any)
  - Orbit: what changed in orbit/ (if any)
- Quiz: none — day X of Y | PASS / FAIL, attempt N — N questions
- Score: XX/100 (Quiz x/40 · Hands-on y/30 · Depth z/30)          ← final day only
- Status: Topic N CLEARED | in progress — Day N next | DEFERRED — revisit by Session N
- Notebook: `learning/notes/…`
- Went well: …
- Do better: …
- Lesson: one neutral takeaway
- Carry-forward: pending items (if any)
- Notes: pace, gaps, overruns, teaching changes (if any)
- Check-in: YYYY-MM-DD HH:MM IST — Check-out: YYYY-MM-DD HH:MM IST (short note)
```

- **Day phrasing** — only these four: `day 1 of 2 — in progress`, `day 2 of 2 — completed`,
  `days 1–2 of 2, one session — completed`, `day 1 of 1 — completed`.
- **Voice** — plain and factual, like a log. No subject: "Installed `kind`", not "I installed".
  The Lesson is a neutral takeaway.
- **Tone** — no praise or hype (genuinely, great, best moment, good instinct, the right call).
  "Real" only means actual, not simulated. No personal life (sleep, shifts, health, feelings).
  Mistakes and failed attempts are written in, stated flatly.
- **Detail** — everything that happened in the session goes here. Question-by-question quiz
  detail goes in the notebook, not here.
- **Consistency** — the Score must match `handbook_status.md` and the Quiz Record Index exactly.

Update the Pacing Layer in `learning/roadmap.md`: Calendar Day, session count, current topic,
Pace. Buffer used moves when a reserve day funds a deferred-mastery revisit or a topic overruns
its allotted days — the 22-day pool is shared across the whole journey, not siloed per phase. The
per-phase breakdown is informational. Light days affect Pace but not Buffer used.

Recalibrate — update Last recalibrated and reassess whether the remaining roadmap still fits the
deadline — when Pace shows 5+ days behind, or every 20 sessions, whichever comes first.
Recalibration moves the Pacing Layer only.

One commit per session is the default; it keeps the log and the history telling the same story.

## 7. Repo standards

- **Employer name** never appears in file content, in any casing. Git remote metadata is exempt —
  only file content matters. Check before committing anything touching `orbit/docs/` or any
  git-log or email example in a notebook.
- **Topic names** are written exactly as `learning/roadmap.md`'s baseline table spells them
  (em-dash form), everywhere they appear.
- **Usernames and emails** in captured output are redacted to `devuser` / `user@example.com`. The
  commands and output are otherwise unmodified.
- **Notebooks**: show a general Syntax line before each concrete example; end a quiz block with
  `**Verdict**: **Topic N CLEARED, attempt N, XX/100.**`; verify every claimed discovery,
  technical rule, or formula before writing it down. Current style (Topic 12 onward): bare
  commands with no prompt marker, captured output marked `# → output` on its own line, language
  tags on fences. Old notebooks keep their own style by default — restyling them is fine, but
  don't rewrite what a command actually printed.
- **Session and Day headings** show the start date only. Check-in/check-out lines carry the real
  span.
- **Hygiene files** (`.gitignore`, `.gitattributes`, `orbit/app/.dockerignore`) get extended as
  new languages and folders arrive.
- **`engine/`** is the forkable copy of this protocol with the DevOps removed. When a rule here
  changes, update `engine/rules.template.md` in the same commit — or say plainly that you didn't.
- **`main` is protected on GitHub.** Only the owner pushes to it directly; everyone else works on
  a branch and opens a pull request, which needs 1 approval. The rule covers administrators and
  lives in GitHub's Settings → Branches, not in a file — check it there. Force-pushes are off:
  switch them on only for a deliberate history rewrite, then off again. Don't add anyone to the
  bypass list or the push list without the owner's say-so.

## 8. Audits

Full-repo audit every 10 topics (after 10, 20, 30, 40, 50 clear) and once more after Topic 53 —
that last one because nothing else is scheduled between Topic 50 and the repo being shown. One-off
audits happen whenever there's a reason. The reusable prompts and the index live in
`audits/README.md`.

**When a periodic audit is due:** the highest cleared topic has reached or passed the next
multiple of 10 that has no audit in `audits/README.md`'s index. Not "the topic that just cleared
is exactly a multiple of 10" — that misses the trigger when a milestone topic and the next one
clear close together, which happened with Topics 10 and 11.

Process:
- Findings first. Fixes only after I review them — never applied silently.
- Categorize by severity: critical / important / minor / cosmetic.
- Fix in small, individually committed batches.
- Audit fresh every time. A past audit's findings are a record, not a checklist to re-verify.
- Defer genuinely topic-specific items (e.g. Dockerfile hardening → Topic 11) to the session that
  teaches them, flagged clearly, so I learn them hands-on instead of finding a fix waiting. This
  doesn't apply to audits with no teaching timeline left to defer into.
- File each finding in the matching subject file under `audits/`, in that file's shape, with an ID
  prefix for the audit. Add the audit to `audits/README.md`'s index and history in the same
  commit — never a new file per audit.
- **Audit records live only in the repo, in `audits/`.** No local copies, raw or otherwise, saved
  anywhere outside it.
- **Write settled questions down, in a committed file.** Session memory doesn't survive a new
  session or a different account; a committed resolution does. A finding that looks open but was
  actually closed weeks ago gets re-litigated forever otherwise.
- **Ownership is settled.** This is a self-created personal project, not employer work — closed in
  `audits/privacy-and-publishing.md`, FS-2. Don't reopen it.

## 9. Never done without an explicit ask

Everything above is a default. These go further: Claude never does them on its own, and does
them only when explicitly asked — after saying which rule it breaks (§0.3).

- Never mark a topic cleared without a passed quiz logged to show for it.
- Never change a recorded score, or backdate or invent a session that didn't happen. Editing a
  timestamp's formatting is fine; editing it to make the record look better is not.
- Never delete an unflattering entry — the failed quiz, the gaps, the light days. A record with no
  failures in it isn't a record.
- Never give the answer before I've attempted it myself.
- Never repeat an identical explanation across attempts.
- Never quote or reproduce copyrighted material — paraphrase.
- Never write a technical claim that hasn't been verified.
