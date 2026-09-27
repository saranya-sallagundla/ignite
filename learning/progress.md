# Progress log

> Read by Claude Code at the start of every session — this is the live state of the plan.
> All dates are IST (UTC+5:30), format YYYY-MM-DD. Day 1 = 2026-07-06.

## Current status

> One line, overwritten every session — not appended to. This is what gets read first.

Topic 1 — COMPLETE (90/100). Topic 2 — COMPLETE (84/100). Topic 3 — COMPLETE (80/100, cleared
in 2 attempts). Topic 4 — COMPLETE (88/100). Topic 5 — COMPLETE (82/100). Topic 6 — COMPLETE
(84/100). Topic 7 — COMPLETE (82/100). Topic 8 — COMPLETE (94/100). **PHASE 1 (Linux, Git &
Version Control) COMPLETE.** Topic 8 covered remotes, PRs (incl. a real mis-based-branch mistake
diagnosed via `git log`/`merge-base` and fixed), GitHub Actions (incl. watching a real runner
execute), and branch protection (incl. the bypass-by-default gotcha, self-approval block, and
linear history restricting merge options). SSH live connection still deferred to AWS sandbox VM.

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

## Session 7 — 2026-07-12
- Topic in progress: Topic 4 — Linux Deep Dive, Process/Log/Disk Management (day 1 of 2)
- Covered: process states (R/S/D/Z/T + modifiers), `awk` column extraction/filtering (new tool),
  the `/proc` filesystem (per-process info, file descriptors — directly explaining Topic 3's
  `2>&1` syntax), `pstree` process hierarchy, `nice`/`renice` process priority (incl. a real
  sudo-password recovery via `wsl -u root`), and log management (`/var/log` rotation seen live,
  `journalctl`). Real discovery: the corporate-network block from Topic 1 reappeared in
  `systemd-timesyncd` NTP timeout log entries. Combined exercise closed with a genuine lesson
  about keyword-limited log searching (a real issue missed by one search term, caught by another).
- Quiz: N/A (day 1 of 2, non-final day — quiz scheduled for Day 2)
- Check-in: 2026-07-12 22:35 IST — Check-out: 2026-07-13 01:17 IST

## Session 8 — 2026-07-13 / 2026-07-14
- Topic completed: Topic 4 — Linux Deep Dive, Process/Log/Disk Management (day 2 of 2, FINAL DAY)
- Covered: partitions/mounting concepts (land/lot/driveway analogy), `lsblk`/UUIDs, a real
  discovery that WSL2's `sda`/`sdb` disks are internally busy/read-only in a hidden namespace
  (`sda: Can't mount, would change RO state` — the same "busy/blocked isn't always visible to
  you" lesson as Topic 1's proxy discovery), a loop-mounted virtual practice disk built fully
  hands-on (`fallocate` → `losetup` → `mkfs.ext4` → `mount`), `fsck` vs `df` (incl. a real
  production alert — `df` timing out — correctly reinterpreted as a liveness/stale-mount issue,
  not filesystem corruption), a persistent `/etc/fstab` entry written independently (correct on
  first attempt) and verified via `mount -a` without rebooting, and a combined inode-vs-block
  exhaustion scenario reasoned through correctly with minimal hinting.
- Quiz: **PASS, attempt 1** — 5 interview-style questions covering both days (zombie process
  reaping, inode/block exhaustion, `fstab`/UUID persistence and boot-failure risk, `nice`/`renice`
  fairness reasoning, and the `df`-timeout production scenario), two of five needed a follow-up
  push for full precision but were ultimately correct. Full record in
  `learning/notes/topic-04-process-log-disk-management.md`. **Topic 4 CLEARED, 88/100
  (Quiz 34/40, Hands-on 28/30, Depth 26/30).**
- Check-in: 2026-07-13 23:50 IST — Check-out: 2026-07-14 05:17 IST

## Session 9 — 2026-07-14 / 2026-07-16
- Topic completed: Topic 5 — Linux Networking Fundamentals (both days, single session)
- Covered: IP addressing/private-vs-public ranges, CIDR notation (full table reasoned through
  down to `/1`), ports and `ss -tuln`, DNS resolution (`dig`) and round-robin load balancing
  (incl. installing `bind9-dnsutils` — succeeded fully, unlike Topic 1's blocked SSH install,
  with an unresolved theory that a separate Ubuntu Pro/ESM background check, not the main package
  mirrors, produced the harmless timeout messages seen), routing (`ip route`), firewalls at a
  conceptual level, and a combined unreachable-service diagnostic scenario (ping → `ss -tuln` →
  bind address → firewall). Both days were intentionally kept high-level/faster-paced at the
  user's request. After Attempt 1 passed but "didn't click," did a full voluntary revision pass:
  a simplified mail-analogy recap table, extended concept-check questions, real-world scenarios
  (subnet sizing, DNS record migration, single-IP tradeoffs), and live `curl -v` verification
  distinguishing "connection refused" / "no route to host" / "timed out" failure signatures —
  genuinely clarified the `0.0.0.0`/`127.0.0.1`/reserved-address distinction that didn't land the
  first time. Full record in
  `learning/notes/phase-1-linux-git-version-control/topic-05-linux-networking-fundamentals.md`.
- Quiz: **Attempt 1 — PASS, 74/100** — 4 interview-style questions, 3 of 4 needed a follow-up
  nudge. Followed by a **voluntary full retest after the revision pass — PASS, 82/100** — 5
  fresh questions, stronger hands-on-verified answers. **Topic 5 CLEARED — official score
  82/100 (Quiz 30/40, Hands-on 26/30, Depth 26/30)**, the retest score used as the record since
  it reflects the deeper understanding reached after revision.
- Check-in: 2026-07-14 23:47 IST — Check-out: 2026-07-16 05:02 IST (session spanned across days
  with breaks; not continuous active work time)

## Session 10 — 2026-07-16
- Topic completed: Topic 6 — Git Fundamentals: Commits, Branches, Merges (both days, single
  session, practiced from Windows PowerShell/VS Code directly, not WSL, matching the user's
  actual GitHub workflow)
- Covered: the three-stage model (working directory/staging/committed history), `git init`/
  `add`/`commit`/`log`, `HEAD` and branch switching, a fast-forward merge (and a second one,
  after realizing the first "conflict" setup didn't actually diverge and correctly re-doing it),
  a genuine merge conflict deliberately set up and resolved via VS Code's built-in merge UI,
  `.gitignore`, `git diff` (incl. reading hunk headers), and a combined shared-file merge
  scenario. Full record in
  `learning/notes/phase-1-linux-git-version-control/topic-06-git-fundamentals.md`.
- Quiz: **PASS, attempt 1** — 5 interview-style questions covering both days (staging-area
  purpose, `HEAD` behavior, fast-forward conditions, conflict marker order/meaning, and the
  branches-vs-direct-commits problem), 2 of 5 needed a real follow-up correction. **Topic 6
  CLEARED, 84/100 (Quiz 30/40, Hands-on 28/30, Depth 26/30).**
- Check-in: 2026-07-16 23:38 IST — Check-out: 2026-07-17 01:45 IST

## Session 11 — 2026-07-18 / 2026-07-19
- Topic completed: Topic 7 — Git Deep Dive: Rebase, Cherry-Pick, Branching Strategies
  (single-day topic per the roadmap)
- Covered: rebase (incl. a real conflict during `git rebase master`, resolved via Accept Both
  Changes, and confirmed via hash change that rebase creates brand-new commits rather than moving
  originals), cherry-pick (incl. a real mistake — conflict markers left in the file despite
  `git add`+`--continue` succeeding, caught by checking `cat` afterward and fixed via
  `git commit --amend --no-edit`, needing two attempts since the first fix left a stray leftover
  fragment), verification methods beyond `cat` (`git diff --check`, PowerShell's `Select-String`
  as the non-WSL equivalent of `grep`), and branching strategies (Git Flow/trunk-based/GitHub
  Flow, incl. a hotfix scenario walked through under all three, and the `develop`-branch
  distinction which took real back-and-forth to land). A real unrecognized commit found via
  `git log --graph` was investigated with `git show` rather than ignored — traced to leftover
  content from Topic 6's `git diff` demo, accidentally committed later via VS Code's Source
  Control panel. Full record in
  `learning/notes/phase-1-linux-git-version-control/topic-07-git-deep-dive.md`.
- Quiz: **PASS, attempt 1** — 4 interview-style questions (merge vs. rebase mechanics,
  safe conflict-resolution habits, cherry-pick tradeoffs, and the Git Flow/GitHub Flow
  `develop`-branch distinction), 3 of 4 needed a real follow-up push, including one full redirect.
  **Topic 7 CLEARED, 82/100 (Quiz 28/40, Hands-on 30/30, Depth 24/30).**
- Check-in: 2026-07-18 00:56 IST — Check-out: 2026-07-19 11:11 IST (session spanned across days
  with breaks; not continuous active work time)

## Session 12 — 2026-07-19 / 2026-07-20
- Topic completed: Topic 8 — GitHub: PRs, Actions Intro, Repo Management (single-day topic per
  the roadmap, final topic in Phase 1)
- Covered: remotes (`git remote add`/`push`/`pull`), a real self-diagnosed PR mistake (a branch
  accidentally created off the wrong base after a session-start branch mix-up, diagnosed via
  `git log --graph --all`/`git merge-base` rather than guessed, then deleted and correctly
  recreated), merge strategy choice reasoning, GitHub Actions (a real workflow written, pushed,
  and its actual run inspected in full log detail — runner OS/region, `GITHUB_TOKEN`
  permissions, step output, teardown), a from-scratch explanation of what a "runner" is (grounded
  in Topic 1's VM concept per explicit user feedback to never assume outside tech knowledge), why
  `ubuntu-latest` is the default choice over `windows-latest`/`macos-latest` (cost, licensing,
  hardware constraints, speed), real GitHub Actions security considerations (`GITHUB_TOKEN`
  scope/lifespan, three real risks, mitigations), and branch protection rules — including three
  genuine real discoveries: classic branch protection doesn't apply to repo admins by default
  (bypassed silently until "Do not allow bypassing" was enabled), a self-approval block genuinely
  preventing merge on a solo repo, and "Require linear history" actually removing "Create a merge
  commit" from the available merge options. Full record in
  `learning/notes/phase-1-linux-git-version-control/topic-08-github.md`.
- Quiz: **PASS, attempt 1** — 4 interview-style questions (Git vs. GitHub, the PR mistake's root
  cause, merge/squash/rebase strategies tied to linear history, and `GITHUB_TOKEN` security),
  1 of 4 needed real redirection (root-cause reasoning), the other 2 follow-ups were quick
  extensions of already-correct, comprehensive answers rather than corrections — score reassessed
  upward after the user pushed back on treating all follow-ups as one flat category, a fair and
  correct correction. **Topic 8 CLEARED, 94/100 (Quiz 36/40, Hands-on 30/30, Depth 28/30).**
  **PHASE 1 (Linux, Git & Version Control) COMPLETE.**
- Check-in: 2026-07-19 22:11 IST — Check-out: 2026-07-20 01:27 IST

## Quiz record index

> A topic clears with one passed attempt. Three failed attempts triggers deferred mastery
> (see CLAUDE.md's 3-attempt mastery rule).

| Topic # | Topic name | Attempt 1 | Attempt 2 | Attempt 3 | Status |
|---|---|---|---|---|---|
| 1 | Linux Fundamentals — Filesystem, SSH, VMs | PASS | — | — | Cleared |
| 2 | Linux — Top 50 Shell Commands | PASS | — | — | Cleared |
| 3 | Linux — Shell Scripting Basics | FAIL (functions) | PASS | — | Cleared |
| 4 | Linux Deep Dive — Process, Log, Disk Management | PASS | — | — | Cleared |
| 5 | Linux — Networking Fundamentals | PASS (74/100) | PASS, voluntary retest (82/100, official) | — | Cleared |
| 6 | Git Fundamentals — Commits, Branches, Merges | PASS | — | — | Cleared |
| 7 | Git Deep Dive — Rebase, Cherry-Pick, Branching Strategies | PASS | — | — | Cleared |
| 8 | GitHub — PRs, Actions Intro, Repo Management | PASS | — | — | Cleared |

## Deferred mastery topics

> Topics that hit 3 failed attempts. Each must be revisited within 3 sessions of being deferred
> and cleared with one passed retest — before any project step or later topic that assumes that
> knowledge, and regardless of whether anything depends on it yet.

| Topic # | Topic name | Deferred on (session #) | Revisit deadline (session #) | Revisited on | Cleared? |
|---|---|---|---|---|---|

## Light days log

| Date | Reason given |
|---|---|
