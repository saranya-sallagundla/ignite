# Progress log

> Read by Claude Code at the start of every session — this is the live state of the plan.
> All dates are IST (UTC+5:30), format YYYY-MM-DD. Day 1 = 2026-07-06.

## Current status

> One line, overwritten every session — not appended to. This is what gets read first.

Topic 1 — COMPLETE (90/100). Topic 2 — COMPLETE (84/100). Topic 3 — COMPLETE (80/100, cleared
in 2 attempts — attempt 1 failed on functions, re-taught via concrete tracing instead of
analogy, attempt 2 passed cleanly on all-new questions same session). Next: Topic 4 — Linux Deep
Dive, Process/Log/Disk Management (2 days). SSH live connection still deferred to AWS sandbox VM.

## Session log

<!-- Append one entry per session, in order. Day 1 is 2026-07-06 IST: -->
## Session 1 — 2026-07-06
- Topic in progress: Topic 1 — Linux Fundamentals, Filesystem, SSH, VMs (day 1 of 2)
- Covered: filesystem hierarchy & permissions (rwx/octal, ownership, `stat` timestamps),
  navigation/manipulation (`cd`, `mkdir -p`, `cp`/`mv`/`rm`, no-trash-bin concept), SSH concepts
  (asymmetric key pairs, challenge-response mechanism, danger of swapping public/private keys),
  VM core concepts (Type 1 vs Type 2 hypervisors, VM vs container kernel sharing, isolation
  boundaries and reboot blast radius, speed/resource tradeoffs) — plus real hands-on
  troubleshooting of a corporate-network/proxy block preventing local `openssh-server` install in
  WSL (root cause identified as network-level, not resolved; SSH hands-on connection deferred to
  AWS sandbox VM).
- Quiz: N/A (day 1 of 2, non-final day — quiz scheduled for Day 2 per multi-day topic rule)
- Check-in: 2026-07-06 23:00 IST — Check-out: 2026-07-07 22:01 IST (includes an overnight break
  taken mid-session due to night-shift fatigue; not continuous active work time)

## Session 2 — 2026-07-07
- Topic completed: Topic 1 — Linux Fundamentals, Filesystem, SSH, VMs (day 2 of 2, FINAL DAY)
- Covered: permission troubleshooting solved independently (`chmod` on a non-executable script),
  hard links vs symlinks via the inode/link-count model — proven hands-on including two real
  discoveries (a hard link to a symlink is itself a symlink; `ln -f` can silently free the last
  copy of real data), SSH key generation (`ssh-keygen -t ed25519`), `known_hosts` and
  `~/.ssh/config` concepts, and a VM/container multi-tenant isolation scenario tied directly to
  the project's future EC2→Kubernetes architecture.
- Quiz: **PASS, attempt 1** — 6 interview-style questions, open-ended, no multiple choice. Full
  question-by-question record in the Quiz record index below and in
  `learning/notes/topic-01-linux-fundamentals.md`.
- Check-in: 2026-07-07 22:19 IST — Check-out: 2026-07-08 05:25 IST (quiz itself ran ~32 minutes,
  over the 20-minute cap — allowed to finish in progress rather than cut mid-question)

## Session 3 — 2026-07-08
- Topic in progress: Topic 2 — Linux, Top 50 Shell Commands (day 1 of 2)
- Covered: file viewing (`head`, `tail`, `less`), search (`grep` with case-sensitivity and `-v`
  gotchas, `find` vs `grep` content-vs-filename distinction), text processing (`sort`, `uniq`,
  `wc`, `cut`), and a combined real-world log-analysis pipeline exercise built incrementally
  (`grep | cut | sort | uniq -c | sort -nr | head`).
- Quiz: N/A (day 1 of 2, non-final day — quiz scheduled for Day 2)
- Check-in: 2026-07-08 22:35 IST — Check-out: 2026-07-09 05:58 IST

## Session 4 — 2026-07-09
- Topic completed: Topic 2 — Linux, Top 50 Shell Commands (day 2 of 2, FINAL DAY)
- Covered: process/signal handling (`ps aux`, `top`, `kill`/`kill -9`, SIGTERM vs SIGKILL
  catchability), system resource commands (`df -h`, `du -sh`, `free -h`, `uptime`/load average),
  networking (`ping`, `ss -tuln`) including a real discovery that ICMP (ping) and TCP (curl/apt)
  are independently firewalled — resolving an apparent contradiction with Topic 1's proxy
  findings — and archiving (`tar -czvf`/`-xzvf`/`-tzvf`).
- Quiz: **PASS, attempt 1** — 5 interview-style questions covering both days. Full record in
  `learning/notes/topic-02-top-50-shell-commands.md`.
- Check-in: 2026-07-09 23:24 IST — Check-out: 2026-07-10 05:39 IST (quiz ran ~28 minutes, over
  the 20-minute cap — allowed to finish in progress)

## Session 5 — 2026-07-10
- Topic in progress: Topic 3 — Linux, Shell Scripting Basics (day 1 of 2)
- Covered: shebang line, variables, positional arguments (`$1`/`$#`), conditionals (`if`/`elif`/
  `else`/`fi`, string and numeric operators), arithmetic expansion (`$(( ))`, modulo), and a
  combined `classify.sh` exercise (sign + odd/even) written entirely from scratch — including
  real, independently-debugged syntax errors (missing `else`/`fi` separators, merged `fi`/`if`
  blocks, and a `nano`-vs-`printf` `\n` handling mixup that briefly broke the shebang line).
- Quiz: N/A (day 1 of 2, non-final day — quiz scheduled for Day 2)
- Check-in: 2026-07-10 22:02 IST — Check-out: 2026-07-11 04:14 IST

## Session 6 — 2026-07-11 / 2026-07-12
- Topic: Topic 3 — Linux, Shell Scripting Basics (day 2 of 2, FINAL DAY)
- Covered: loops (`for`, `while`, incl. a real self-debugged infinite-loop bug), functions
  (definition + invocation), exit codes/error handling (`$?`, redirecting output to suppress it),
  and a combined `checkall.sh` exercise (function + loop + exit code, tied to `project/scripts/`
  use later).
- Quiz: **Attempt 1 — FAIL** (functions: invocation and `$1` scoping; all other areas —
  conditionals, loops, exit codes — passed cleanly). Re-taught functions using concrete tracing
  (a real script printing `$1` at three points) instead of another analogy, then **Attempt 2 —
  full retest, all-new questions — PASS**, same session, after a short break. **Topic 3 CLEARED
  in 2 attempts.** Full record in `learning/notes/topic-03-shell-scripting-basics.md`.
- Check-in: 2026-07-11 22:26 IST — Check-out: 2026-07-12 10:02 IST (long session incl. a
  fatigue-driven pause partway through; Attempt 1 quiz ran ~32 minutes, Attempt 2 retest ~23
  minutes, both over the 20-minute cap but allowed to finish in progress)

## Quiz record index

> A topic clears with one passed attempt. Three failed attempts triggers deferred mastery
> (see CLAUDE.md's 3-attempt mastery rule).

| Topic # | Topic name | Attempt 1 | Attempt 2 | Attempt 3 | Status |
|---|---|---|---|---|---|
| 1 | Linux Fundamentals — Filesystem, SSH, VMs | PASS | — | — | Cleared |
| 2 | Linux — Top 50 Shell Commands | PASS | — | — | Cleared |
| 3 | Linux — Shell Scripting Basics | FAIL (functions) | PASS | — | Cleared |
| 3 | Linux — Shell Scripting Basics | FAIL (functions) | pending — next session | — | Retest due before Topic 4 |

## Deferred mastery topics

> Topics that hit 3 failed attempts. Each must be revisited within 3 sessions of being deferred
> and cleared with one passed retest — before any project step or later topic that assumes that
> knowledge, and regardless of whether anything depends on it yet.

| Topic # | Topic name | Deferred on (session #) | Revisit deadline (session #) | Revisited on | Cleared? |
|---|---|---|---|---|---|

## Light days log

| Date | Reason given |
|---|---|
