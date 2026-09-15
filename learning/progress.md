# Progress log

> Read by Claude Code at the start of every session — this is the live state of the plan.
> All dates are IST (UTC+5:30), format YYYY-MM-DD. Day 1 = 2026-07-06.

## Current status

> One line, overwritten every session — not appended to. This is what gets read first.

Topic 1 — day 1 of 2, covered: filesystem hierarchy & permissions (rwx/octal, ownership, stat
timestamps), navigation/manipulation (cd, mkdir -p, cp/mv/rm, no-trash concept), SSH concepts
(key-based challenge-response auth, key-swap risk), VM core concepts (Type 1 vs Type 2
hypervisors, VM vs container kernel sharing, reboot blast radius, speed/resource tradeoffs).
SSH hands-on (local sshd install) deferred — corporate network/proxy blocks outbound WSL traffic;
retry against AWS sandbox VM once available. Day 2 covers harder scenarios + quiz on whole topic.

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

## Quiz record index

> A topic clears with one passed attempt. Three failed attempts triggers deferred mastery
> (see CLAUDE.md's 3-attempt mastery rule).

| Topic # | Topic name | Attempt 1 | Attempt 2 | Attempt 3 | Status |
|---|---|---|---|---|---|

## Deferred mastery topics

> Topics that hit 3 failed attempts. Each must be revisited within 3 sessions of being deferred
> and cleared with one passed retest — before any project step or later topic that assumes that
> knowledge, and regardless of whether anything depends on it yet.

| Topic # | Topic name | Deferred on (session #) | Revisit deadline (session #) | Revisited on | Cleared? |
|---|---|---|---|---|---|

## Light days log

| Date | Reason given |
|---|---|
