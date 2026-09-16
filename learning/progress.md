# Progress log

> Read by Claude Code at the start of every session — this is the live state of the plan.
> All dates are IST (UTC+5:30), format YYYY-MM-DD. Day 1 = 2026-07-06.

## Current status

> One line, overwritten every session — not appended to. This is what gets read first.

Topic 1 — COMPLETE (day 2 of 2). Day 2 covered: permission troubleshooting (independent),
hard links vs symlinks (inode/link-count model, proven hands-on incl. `ln -f` data-loss case),
SSH key generation (`ssh-keygen`), `known_hosts`/`~/.ssh/config`, VM/container multi-tenant
isolation tied to the project's EC2→K8s architecture. Quiz: PASS, attempt 1 (see quiz record
below). SSH live connection still deferred to AWS sandbox VM (local `sshd` install blocked by
corporate network — see Day 1 note). Next: Topic 2 — Linux Top 50 Shell Commands (2 days).

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

## Quiz record index

> A topic clears with one passed attempt. Three failed attempts triggers deferred mastery
> (see CLAUDE.md's 3-attempt mastery rule).

| Topic # | Topic name | Attempt 1 | Attempt 2 | Attempt 3 | Status |
|---|---|---|---|---|---|
| 1 | Linux Fundamentals — Filesystem, SSH, VMs | PASS | — | — | Cleared |

## Deferred mastery topics

> Topics that hit 3 failed attempts. Each must be revisited within 3 sessions of being deferred
> and cleared with one passed retest — before any project step or later topic that assumes that
> knowledge, and regardless of whether anything depends on it yet.

| Topic # | Topic name | Deferred on (session #) | Revisit deadline (session #) | Revisited on | Cleared? |
|---|---|---|---|---|---|

## Light days log

| Date | Reason given |
|---|---|
