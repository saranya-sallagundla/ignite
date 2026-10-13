# Progress log

> Read by Claude Code at the start of every session — this is the live state of the plan.
> Dates here are IST (UTC+5:30), `YYYY-MM-DD`; raw command output and git metadata show the
> machine's local clock (US Eastern). Mission anchors and logging rules: [`rules.md`](../rules.md).

## Current status

> One line, overwritten every session — not appended to. This is what gets read first.

Topic 12 — Kubernetes — Architecture & Core Concepts — day 1 of 2 done (Session 18, 2026-09-22:
architecture taught, local 2-node `kind` cluster set up and verified); Day 2 + quiz next. Topics
1-11 cleared; Phase 2 at 3 of 11. Behind by ~25 core days; the deadline still fits with 3 days of
slack (roadmap.md's Pacing Layer). 5 open items below.

## Quiz record index

> A topic clears with one passed attempt. Failing all attempts (three by default — see
> `rules.md` §3) triggers deferred mastery.

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
| 9 | Docker — Architecture, Images, Containers | PASS | — | — | Cleared |
| 10 | Docker — Networking, Volumes, Docker Compose | PASS | — | — | Cleared |
| 11 | Docker — Multi-Stage Builds & Best Practices | PASS | — | — | Cleared |

## Deferred mastery topics

> Topics that failed all their attempts. Each is revisited within about 3 sessions of being deferred
> and cleared with one passed retest — before any project step or later topic that assumes that
> knowledge, and regardless of whether anything depends on it yet.

| Topic # | Topic name | Deferred on (session #) | Revisit deadline (session #) | Revisited on | Cleared? |
|---|---|---|---|---|---|

## Open items

> Work pushed to later — from sessions or audits. Read at the start of every session with the
> other tables. When one is done, set its Status to `done — Session N`; don't delete the row.

| # | Item | From | Do it when | Status |
|---|---|---|---|---|
| 1 | SSH connection hands-on — local `sshd` is blocked by the corporate network | Session 1 | AWS sandbox VM access is ready | open |
| 2 | Reuse `checkall.sh` in `orbit/scripts/` | Session 6 | `orbit/scripts/` is created | open |
| 3 | Dockerfile's `USER appuser` has no numeric UID — Kubernetes `runAsNonRoot` rejects it (`CreateContainerConfigError`) | Public-readiness audit, PR-H-8 | Topic 13, when `orbit-app` is first deployed | open |
| 4 | Field atlas Kubernetes entry — written once, not per topic | Session 18 | After Topic 14 clears | open |
| 5 | Add credential patterns to `.gitignore` (AWS keys, `*.tfvars`, `kubeconfig`, `.env.*`) and anchor `env/` | Public-readiness audit, PR-H-7 | Before Phase 3 (Topic 20) | open |

## Light days log

| Date | Reason given |
|---|---|
| 2026-07-17 | Already ahead of schedule — Sessions 9 and 10 had efficiently covered Topic 5 and Topic 6 (each a 2-day topic in the baseline) within continuous sessions starting 2026-07-14 and 2026-07-16, so this day was taken as a rest day without falling behind. Logged retroactively during a later review, since it wasn't captured in the moment. Pacing cost: none — Topics 1-8 still landed at exactly their planned 14 roadmap days total, zero overrun. |

## Session log

<!-- Append one entry per session, in order. Shape and voice: rules.md §6. -->
### Session 1 — 2026-07-06 — Linux filesystem, permissions, SSH & VM basics
- Topic: Topic 1 — Linux Fundamentals — Filesystem, SSH, VMs — day 1 of 2 — in progress
- Covered:
  - Learned: filesystem hierarchy (one tree, drives mounted into it); permissions (rwx, octal,
    ownership, `stat` timestamps); SSH key pairs and challenge-response, and why swapping
    public/private keys is dangerous; Type 1 vs Type 2 hypervisors; VM vs container kernel
    sharing, isolation, reboot blast radius, speed and resource trade-offs
  - Taught with: land / apartment building / room (server, VM, container); foundation vs a
    backyard shed (Type 1 vs Type 2 hypervisor)
  - Hands-on: navigating and changing files (`cd`, `mkdir -p`, `cp`, `mv`, `rm` — no trash bin)
  - Setup: WSL2 Ubuntu on Windows
  - Problems & fixes: `openssh-server` install in WSL failed behind a corporate network/proxy
    block. Cause is network-level; not fixed.
- Quiz: none — day 1 of 2
- Status: in progress — Day 2 + quiz next
- Notebook: `learning/notes/phase-1-linux-git-version-control/topic-01-linux-fundamentals-filesystem-ssh-vms.md`
- Went well: double-checked before running `chmod` / `rm`, even on own files; stayed with the
  proxy dead-end long enough to find its cause.
- Do better: VM vs container took two passes — the first explanation was too abstract. Very long
  session; split into shorter sessions next time.
- Lesson: When one explanation doesn't land, switch to a concrete analogy.
- Carry-forward: SSH connection hands-on — retry on an AWS sandbox VM once access is ready.
- Check-in: 2026-07-06 23:00 IST — Check-out: 2026-07-07 22:01 IST (overnight break; not continuous)

### Session 2 — 2026-07-07 — Hard vs soft links, SSH keys + Topic 1 quiz
- Topic: Topic 1 — Linux Fundamentals — Filesystem, SSH, VMs — day 2 of 2 — completed
- Covered:
  - Learned: hard links vs symlinks (inode and link-count model); SSH keys (`ssh-keygen -t
    ed25519`), `known_hosts`, `~/.ssh/config`; VM/container isolation for multi-tenant systems,
    tied to Orbit's future EC2 → Kubernetes design
  - Taught with: library catalog card (hard link) vs a sticky note saying "go check shelf 12B"
    (symlink)
  - Hands-on: fixed a permission problem alone (`chmod` on a non-executable script); created,
    broke and force-overwrote real links to watch what happens to the data
  - Discovery: a hard link to a symlink is itself a symlink; `ln -f` can silently free the last
    copy of real data
  - Revision: links re-taught with the library analogy after confusion came back following the
    `ln -f` experiments
- Quiz: PASS, attempt 1 — 6 questions
- Score: 90/100 (Quiz 36/40 · Hands-on 27/30 · Depth 27/30)
- Status: Topic 1 CLEARED
- Notebook: `learning/notes/phase-1-linux-git-version-control/topic-01-linux-fundamentals-filesystem-ssh-vms.md`
- Went well: kept pushing own answers until precise ("kernel", not "privacy") instead of
  settling for a vague one.
- Do better: quiz ran ~32 min, over the 20-min cap; a few answers needed a nudge to sharpen.
- Lesson: Break it, then fix it — links only stuck after watching real data disappear.
- Carry-forward: SSH connection hands-on still pending (AWS sandbox VM).
- Check-in: 2026-07-07 22:19 IST — Check-out: 2026-07-08 05:25 IST (quiz ~32 min, over 20-min cap)

### Session 3 — 2026-07-08 — Viewing, searching & text processing commands
- Topic: Topic 2 — Linux — Top 50 Shell Commands — day 1 of 2 — in progress
- Covered:
  - Learned: file viewing (`head`, `tail`, `less`); search (`grep` for content, `find` for
    filenames); text processing (`sort`, `uniq`, `wc`, `cut`)
  - Hands-on: built a log-analysis pipeline one stage at a time
    (`grep | cut | sort | uniq -c | sort -nr | head`)
  - Problems & fixes: `grep -v` missed matches because of case sensitivity; `uniq` misread as
    comparing words instead of whole lines — both fixed by testing directly
- Quiz: none — day 1 of 2
- Status: in progress — Day 2 + quiz next
- Notebook: `learning/notes/phase-1-linux-git-version-control/topic-02-linux-top-50-shell-commands.md`
- Went well: built the pipeline stage by stage, checking each output before adding the next.
- Do better: check case sensitivity first when a `grep` result looks wrong.
- Lesson: Test a prediction against real output before trusting it.
- Check-in: 2026-07-08 22:35 IST — Check-out: 2026-07-09 05:58 IST

### Session 4 — 2026-07-09 — Processes, networking, archives + Topic 2 quiz
- Topic: Topic 2 — Linux — Top 50 Shell Commands — day 2 of 2 — completed
- Covered:
  - Learned: processes and signals (`ps aux`, `top`, `kill` / `kill -9`, SIGTERM vs SIGKILL);
    system resources (`df -h`, `du -sh`, `free -h`, `uptime` and load average)
  - Taught with: tenant/landlord — SIGTERM knocks and asks, SIGKILL removes
  - Hands-on: networking (`ping`, `ss -tuln`); archiving (`tar -czvf` / `-xzvf` / `-tzvf`)
  - Discovery: ICMP (`ping`) and TCP (`curl`, `apt`) are firewalled separately — this explains
    Topic 1's proxy block
- Quiz: PASS, attempt 1 — 5 questions
- Score: 84/100 (Quiz 34/40 · Hands-on 26/30 · Depth 24/30)
- Status: Topic 2 CLEARED
- Notebook: `learning/notes/phase-1-linux-git-version-control/topic-02-linux-top-50-shell-commands.md`
- Went well: reasoned through the ICMP-vs-TCP firewall result independently.
- Do better: exact syntax (`grep -r` flag placement, `find` scope); quiz ran ~28 min, over the cap.
- Lesson: Not remembering every command after a dense session is normal — the notebook holds the
  detail, and repetition in later topics builds recall.
- Check-in: 2026-07-09 23:24 IST — Check-out: 2026-07-10 05:39 IST (quiz ~28 min, over 20-min cap)

### Session 5 — 2026-07-10 — Shell scripts: variables, arguments, conditionals
- Topic: Topic 3 — Linux — Shell Scripting Basics — day 1 of 2 — in progress
- Covered:
  - Learned: shebang, variables, positional arguments (`$1`, `$#`), conditionals (`if` / `elif` /
    `else` / `fi`, string and numeric tests), arithmetic (`$(( ))`, modulo)
  - Hands-on: wrote `classify.sh` from scratch (sign + odd/even)
  - Problems & fixes: several syntax errors, all debugged alone — missing `else` / `fi`
    separators, merged `fi` / `if` blocks, and a `nano` vs `printf` `\n` mix-up that broke the
    shebang; the last one fixed by reading the line number bash reported
- Quiz: none — day 1 of 2
- Status: in progress — Day 2 + quiz next
- Notebook: `learning/notes/phase-1-linux-git-version-control/topic-03-linux-shell-scripting-basics.md`
- Went well: wrote and debugged the whole script without being handed the answer.
- Do better: read the error's line number first, before guessing.
- Lesson: A slow debugging grind is often where the learning happens — stay with it.
- Check-in: 2026-07-10 22:02 IST — Check-out: 2026-07-11 04:14 IST

### Session 6 — 2026-07-11 — Loops, functions + Topic 3 quiz
- Topic: Topic 3 — Linux — Shell Scripting Basics — day 2 of 2 — completed
- Covered:
  - Learned: loops (`for`, `while`), functions (define + call), exit codes (`$?`), silencing
    output with redirection
  - Taught with: office/tray analogy and step-by-step tracing for functions (didn't land); then a
    real script printing `$1` at three points (landed)
  - Hands-on: `checkall.sh` combining a function, a loop and exit codes
  - Problems & fixes: an infinite `while` loop, found and fixed alone
  - Revision: functions re-taught by concrete tracing instead of another analogy, then a full
    retest
- Quiz: attempt 1 FAIL (function calls and `$1` scoping; everything else passed); attempt 2 PASS —
  5 new questions, same session
- Score: 80/100 (Quiz 30/40 · Hands-on 28/30 · Depth 22/30)
- Status: Topic 3 CLEARED
- Notebook: `learning/notes/phase-1-linux-git-version-control/topic-03-linux-shell-scripting-basics.md`
- Went well: said clearly when functions weren't landing instead of pretending; asked for a full
  retest rather than only the weak spot; took a break before the retest.
- Do better: switch to "run it and watch" sooner — several analogies were tried first.
- Lesson: When an explanation isn't landing, run real code and watch the values.
- Carry-forward: reuse `checkall.sh` in `orbit/scripts/`.
- Check-in: 2026-07-11 22:26 IST — Check-out: 2026-07-12 10:02 IST (with a pause; quizzes ~32 + ~23 min, over 20-min cap)

### Session 7 — 2026-07-12 — Process states, /proc, nice & log basics
- Topic: Topic 4 — Linux Deep Dive — Process, Log, Disk Management — day 1 of 2 — in progress
- Covered:
  - Learned: process states (R/S/D/Z/T and modifiers); `awk` for extracting and filtering columns;
    the `/proc` filesystem (per-process info, file descriptors — this explains Topic 3's `2>&1`);
    `pstree`; `nice` / `renice` priority; logs (`/var/log` rotation, `journalctl`)
  - Taught with: a hotel — `systemd` is the general manager, `journalctl` the unified logbook,
    `/var/log` each department's own paper logbook
  - Hands-on: filtered `ps` output by STAT modifiers with `awk`; explored `/proc/<pid>/fd`; changed
    priority with `renice`; watched log rotation live; a "the system feels slow" troubleshooting drill
  - Problems & fixes: forgot the sudo password — recovered it via `wsl -u root` without touching
    any files
  - Discovery: Topic 1's corporate network block showed up again as `systemd-timesyncd` NTP
    timeout entries; one search term missed it, a different one caught it
- Quiz: none — day 1 of 2
- Status: in progress — Day 2 + quiz next
- Notebook: `learning/notes/phase-1-linux-git-version-control/topic-04-linux-deep-dive-process-log-disk-management.md`
- Went well: filtered by more STAT modifiers than asked; re-searched the logs with a different
  keyword instead of accepting an empty result.
- Do better: search logs with more than one keyword from the start — one term missed a real issue.
- Lesson: Account and credential problems usually feel riskier than they are — ask what a fix
  will touch, then fix it calmly.
- Check-in: 2026-07-12 22:35 IST — Check-out: 2026-07-13 01:17 IST

### Session 8 — 2026-07-13 — Disks, mounting, fstab + Topic 4 quiz
- Topic: Topic 4 — Linux Deep Dive — Process, Log, Disk Management — day 2 of 2 — completed
- Covered:
  - Learned: partitions, filesystems and mounting; `lsblk` and UUIDs; `fsck` vs `df` — a `df`
    timeout is a liveness / stale-mount problem, not corruption (tied to a real production alert);
    inodes vs blocks, and how each can run out
  - Taught with: land / lots / driveway (partition, filesystem, mount); a hotel that only rents
    whole rooms (4K blocks)
  - Hands-on: built a loop-mounted practice disk (`fallocate` → `losetup` → `mkfs.ext4` →
    `mount`); wrote a persistent `/etc/fstab` entry alone, correct first time, verified with
    `mount -a` instead of rebooting
  - Discovery: WSL2's `sda` / `sdb` are busy and read-only in a hidden namespace (`Can't mount,
    would change RO state`) — same "blocked isn't always visible" lesson as Topic 1's proxy
- Quiz: PASS, attempt 1 — 5 questions
- Score: 88/100 (Quiz 34/40 · Hands-on 28/30 · Depth 26/30)
- Status: Topic 4 CLEARED
- Notebook: `learning/notes/phase-1-linux-git-version-control/topic-04-linux-deep-dive-process-log-disk-management.md`
- Went well: reasoned through inode-vs-block exhaustion with only a small hint; `fstab` entry
  right first time.
- Do better: got confused re-reading a command sequence mid-session — ask for a plain
  step-by-step retrace sooner.
- Lesson: Tie a concept to a real alert from work — it lands faster than an invented scenario.
- Check-in: 2026-07-13 23:50 IST — Check-out: 2026-07-14 05:17 IST

### Session 9 — 2026-07-14 — IP, CIDR, DNS, ports + Topic 5 quiz
- Topic: Topic 5 — Linux — Networking Fundamentals — days 1–2 of 2, one session — completed
- Covered:
  - Learned: IP addressing, private vs public ranges, CIDR (worked down to `/1`), ports, DNS and
    round-robin load balancing, routing, firewalls (concept level)
  - Taught with: the mail system — expanded into a recap table with real examples in the revision
  - Hands-on: `ss -tuln`, `dig`, `ip route`; an unreachable-service drill (`ping` → `ss -tuln` →
    bind address → firewall)
  - Setup: installed `bind9-dnsutils` — worked, unlike Topic 1's blocked SSH install
  - Problems & fixes: harmless timeout messages during the install — likely an Ubuntu Pro/ESM
    background check, not the package mirrors; not confirmed
  - Discovery: `0.0.0.0` and `127.0.0.1` are neither private nor public — a third, reserved category
  - Revision: the first pass was fast and didn't land; re-taught with the recap table, extra
    concept checks, real scenarios (subnet sizing, DNS migration) and live `curl -v` tests showing
    refused vs no-route vs timed out
- Quiz: attempt 1 PASS, 74/100 — 4 questions; retest after revision PASS, 82/100 — 5 new questions
- Score: 82/100 (Quiz 30/40 · Hands-on 26/30 · Depth 26/30) — the retest score is official
- Status: Topic 5 CLEARED
- Notebook: `learning/notes/phase-1-linux-git-version-control/topic-05-linux-networking-fundamentals.md`
- Went well: said openly that the fast pass hadn't landed and asked to loop back; asked why
  `127.0.0.1` / `0.0.0.0` weren't public, which surfaced the missing reserved category.
- Do better: don't compress two days into one fast session.
- Lesson: Speed and depth trade off. When a topic is rushed and it shows, say so and loop back.
- Notes: both days were kept high-level and fast on request.
- Check-in: 2026-07-14 23:47 IST — Check-out: 2026-07-16 05:02 IST (spanned days, with breaks)

### Session 10 — 2026-07-16 — Git commits, branches, merges + Topic 6 quiz
- Topic: Topic 6 — Git Fundamentals — Commits, Branches, Merges — days 1–2 of 2, one session — completed
- Covered:
  - Learned: the three-stage model (working directory, staging, history); `git init` / `add` /
    `commit` / `log`; `HEAD` and switching branches; fast-forward merges; merge conflicts;
    `.gitignore`; `git diff` and reading hunk headers
  - Taught with: save points (commits); packing a box before sealing and shipping it (stage,
    then commit)
  - Hands-on: two fast-forward merges; a real merge conflict set up and resolved in VS Code's
    merge editor; a combined shared-file merge scenario
  - Setup: Windows PowerShell and VS Code, not WSL — matches the real GitHub workflow
  - Problems & fixes: the first "conflict" setup never diverged — worked out why (branching then
    merging straight away can't conflict) and rebuilt it with edits on both sides
- Quiz: PASS, attempt 1 — 5 questions
- Score: 84/100 (Quiz 30/40 · Hands-on 28/30 · Depth 26/30)
- Status: Topic 6 CLEARED
- Notebook: `learning/notes/phase-1-linux-git-version-control/topic-06-git-fundamentals-commits-branches-merges.md`
- Went well: worked out alone why the first conflict setup couldn't conflict.
- Do better: plan a conflict scenario before building it — both sides must change after the
  branch point.
- Lesson: Practise in the environment the job uses — VS Code's merge editor made conflicts easier
  to read than raw markers.
- Check-in: 2026-07-16 23:38 IST — Check-out: 2026-07-17 01:45 IST

### Session 11 — 2026-07-18 — Rebase, cherry-pick, branching + Topic 7 quiz
- Topic: Topic 7 — Git Deep Dive — Rebase, Cherry-Pick, Branching Strategies — day 1 of 1 — completed
- Covered:
  - Learned: rebase (creates new commits — confirmed by the hash change); cherry-pick; checking
    for leftover conflict markers (`git diff --check`, PowerShell `Select-String`); branching
    strategies (Git Flow, trunk-based, GitHub Flow) and the `develop` branch
  - Taught with: merge joins two roads at an intersection; rebase re-lays one road further down
    the other, so no intersection shows
  - Hands-on: a hotfix scenario walked through under all three strategies
  - Setup: same PowerShell / VS Code practice folder as Topic 6
  - Problems & fixes: a conflict during `git rebase master`, resolved with Accept Both Changes; a
    cherry-pick left conflict markers in the file even though `git add` + `--continue` succeeded —
    caught with `cat`, fixed with `git commit --amend --no-edit` on the second try
  - Discovery: an unknown commit in `git log --graph`, traced with `git show` to leftover Topic 6
    demo content committed by accident from VS Code's Source Control panel
- Quiz: PASS, attempt 1 — 4 questions
- Score: 82/100 (Quiz 28/40 · Hands-on 30/30 · Depth 24/30)
- Status: Topic 7 CLEARED
- Notebook: `learning/notes/phase-1-linux-git-version-control/topic-07-git-deep-dive-rebase-cherry-pick-branching-strategies.md`
- Went well: checked the file after `--continue` instead of trusting it; kept asking about the
  `develop` branch until it was clear.
- Do better: clean conflict markers fully in one pass — the first fix left a stray fragment.
- Lesson: `git add` doesn't check your work — verify the file, not the command's success.
- Check-in: 2026-07-18 00:56 IST — Check-out: 2026-07-19 11:11 IST (spanned days, with breaks)

### Session 12 — 2026-07-19 — GitHub PRs, Actions, branch protection + Topic 8 quiz
- Topic: Topic 8 — GitHub — PRs, Actions Intro, Repo Management — day 1 of 1 — completed
- Covered:
  - Learned: remotes (`git remote add`, `push`, `pull`); pull requests and choosing a merge
    strategy; GitHub Actions — what a runner is, why `ubuntu-latest` is the default (cost,
    licensing, hardware, speed), `GITHUB_TOKEN` scope and lifespan, three real risks and their
    mitigations; branch protection rules
  - Taught with: a runner explained as a full virtual machine, built on Topic 1's VM concept
  - Hands-on: wrote and pushed a workflow, then read its full run log (runner OS and region, token
    permissions, step output, teardown); set up branch protection
  - Problems & fixes: a branch was created off the wrong base after a mix-up at session start —
    diagnosed with `git log --graph --all` and `git merge-base`, then deleted and recreated
  - Discovery: classic branch protection silently skips repo admins until "Do not allow
    bypassing" is on; a self-approval block stops merges even on a solo repo; "Require linear
    history" removes the merge-commit option
- Quiz: PASS, attempt 1 — 4 questions
- Score: 94/100 (Quiz 36/40 · Hands-on 30/30 · Depth 28/30)
- Status: Topic 8 CLEARED — Phase 1 complete
- Notebook: `learning/notes/phase-1-linux-git-version-control/topic-08-github-prs-actions-intro-repo-management.md`
- Went well: diagnosed the wrong-base PR from the history instead of guessing; challenged a quiz
  score that seemed unfair, and it was revised after re-checking.
- Do better: confirm which branch you're on at session start.
- Lesson: Test a protection before trusting it — branch protection looked on but didn't apply to
  admins.
- Notes: two standing changes from this session — explain every tech term from scratch, never
  assume it; keep the employer name out of all notebooks.
- Check-in: 2026-07-19 22:11 IST — Check-out: 2026-07-20 01:27 IST

### Session 13 — 2026-07-20 — Docker basics, first Dockerfile, Orbit app
- Topic: Topic 9 — Docker — Architecture, Images, Containers — day 1 of 2 — in progress
- Covered:
  - Learned: client, daemon, registry, image, container; the client/server split in
    `docker version`; the pull → image → container flow, traced line by line against
    `docker run hello-world`; where images and containers live (Docker Desktop's Linux VM,
    tied to Topic 1's VMs); container lifecycle (`docker logs`, `stop`, `ps -a`)
  - Taught with: a recipe card vs the dish cooked from it (image vs container); phoning a
    restaurant instead of cooking yourself (client → daemon)
  - Hands-on: ran `hello-world` twice — one image, two containers; wrote a 5-instruction
    Dockerfile line by line (`FROM` / `WORKDIR` / `COPY` / `RUN` / `CMD`); built it
    (`docker build -t orbit-app .`), ran it (`docker run -d -p 5000:5000`), and got
    `{"status":"ok"}` from `http://localhost:5000/health`
  - Setup: Docker Desktop 4.58.0 (engine 29.1.5)
  - Discovery: `orbit-app` exited with code 137 (128 + SIGKILL) after `docker stop`, while
    `hello-world` exited 0 — worked out from Topic 2's signals
  - Orbit: first app in `orbit/app/` — a minimal Flask `app.py` with a `/health` endpoint, plus
    `requirements.txt` and the Dockerfile. The app is Claude-written boilerplate until Phase 5.
- Quiz: none — day 1 of 2
- Status: in progress — Day 2 + quiz next
- Notebook: `learning/notes/phase-2-containers-kubernetes-ci-cd/topic-09-docker-architecture-images-containers.md`
- Went well: reasoned through exit code 137 alone, before being told the formula.
- Do better: new terms came too fast at first — introduce them one at a time before connecting them.
- Lesson: Learn each term on its own before linking it to the bigger picture.
- Notes: two standing changes from this session — slower pace for new terms, and a same-day
  agenda up front.
- Check-in: 2026-07-20 22:37 IST — Check-out: 2026-07-21 10:50 IST

### Session 14 — 2026-07-21 — Layer caching, image tags + Topic 9 quiz
- Topic: Topic 9 — Docker — Architecture, Images, Containers — day 2 of 2 — completed
- Covered:
  - Learned: layer caching — once one layer's cache breaks, every later layer reruns; image
    tagging (`docker tag`) — `:latest` only moves when a build or tag assigns it; liveness vs
    readiness (a preview for Kubernetes)
  - Hands-on: reordered the Dockerfile (`COPY requirements.txt` → `RUN pip install` →
    `COPY app.py`) and proved it with build logs — 13.3 s → 2.3 s, `pip install` showing
    `CACHED`; ran `v1` and `v2` side by side on different ports; deleted a buggy image safely
    (`stop` → `rm` → `rmi`)
  - Problems & fixes: a missing final `COPY app.py .`, caught alone; a Python string-vs-boolean
    bug (`ready="true"` vs `ready=True`); an image that wouldn't delete until its dependent
    container was found and removed
  - Orbit: Dockerfile reordered for caching; a `/ready` endpoint added to the app
- Quiz: PASS, attempt 1 — 5 questions
- Score: 86/100 (Quiz 32/40 · Hands-on 29/30 · Depth 25/30)
- Status: Topic 9 CLEARED
- Notebook: `learning/notes/phase-2-containers-kubernetes-ci-cd/topic-09-docker-architecture-images-containers.md`
- Went well: the most independent hands-on so far — caught both bugs alone and proved the cache
  fix with real timings.
- Do better: keep `docker stop` (SIGTERM, then SIGKILL) and a program exiting on its own clearly
  apart — they got mixed up.
- Lesson: Prove a fix with a measurement, not a feeling — the build timings settled it.
- Check-in: 2026-07-21 23:44 IST — Check-out: 2026-07-22 04:47 IST

### Session 15 — 2026-07-22 — Docker networking & bind mounts
- Topic: Topic 10 — Docker — Networking, Volumes, Docker Compose — day 1 of 2 — in progress
- Covered:
  - Learned: bridge networks, default vs custom; `docker network ls` (bridge / host / none) and
    `docker network inspect`; container-to-container communication; port publishing, tied to
    Topic 5's private / public IPs and NAT; container storage is temporary without a volume
  - Taught with: two neighborhoods with no road between them (containers on separate networks)
  - Hands-on: two `orbit-app` containers — name lookup failed on the default bridge
    (`socket.gaierror: Name or service not known`), worked by IP, then worked by name on a custom
    network (`docker network create` / `connect`); wrote a file, deleted the container, saw it
    gone; then a bind mount (`-v` to a host folder) kept the file across a brand-new container
  - Discovery: an empty bridge network already shows 3 IPs in use — the network address, gateway
    and broadcast, not containers; checked against Topic 5's CIDR math (65,536 total,
    `DynamicIPsAvailable: 65533`)
- Quiz: none — day 1 of 2
- Status: in progress — Day 2 + quiz next
- Notebook: `learning/notes/phase-2-containers-kubernetes-ci-cd/topic-10-docker-networking-volumes-compose.md`
- Went well: asked why an empty network had 3 IPs in use, and tied it back to CIDR.
- Do better: the pace was too fast at first — say so as soon as it happens.
- Lesson: Seeing the real error first makes the fix mean something.
- Notes: teaching slowed further on request — treat as a total beginner, same-day agenda,
  "shall I move on?" checks before each new step.
- Check-in: 2026-07-22 22:53 IST — Check-out: 2026-07-23 02:12 IST

### Session 16 — 2026-07-23 — Named volumes, Docker Compose + Topic 10 quiz
- Topic: Topic 10 — Docker — Networking, Volumes, Docker Compose — day 2 of 2 — completed
- Covered:
  - Learned: named volumes (`docker volume create`, `ls`) persist like bind mounts; a container's
    mounts are fixed at creation and can't be changed in place; Docker Compose — YAML structure
    and indentation, `services` / `build` / `ports`; Compose creates its own network with
    name-based lookup, and recreates a service only when its config changes
  - Hands-on: added a mount to an existing container by duplicate-then-swap — built a copy with
    the mount, verified it, then removed the original; checked all containers and the volume
    before moving on; ran `docker compose up -d` and verified `/health`; added a second service
    and a shared named volume
  - Orbit: `orbit/docker-compose.yml` created for `orbit-app`
- Quiz: PASS, attempt 1 — 5 questions
- Score: 92/100 (Quiz 36/40 · Hands-on 30/30 · Depth 26/30)
- Status: Topic 10 CLEARED
- Notebook: `learning/notes/phase-2-containers-kubernetes-ci-cd/topic-10-docker-networking-volumes-compose.md`
- Went well: refused to delete first and hope — verified the copy before touching the original;
  linked Compose's recreate behaviour to the "mounts are fixed at creation" rule alone.
- Do better: YAML indentation needed explaining before Compose made sense — learn a file format
  before the tool that uses it.
- Lesson: Never delete the working thing until its replacement is proven.
- Check-in: 2026-07-23 23:06 IST — Check-out: 2026-07-24 04:39 IST

### Session 17 — 2026-07-24 — Multi-stage builds, non-root, gunicorn + Topic 11 quiz
- Topic: Topic 11 — Docker — Multi-Stage Builds & Best Practices — day 1 of 1 — completed
- Covered:
  - Learned: compiler vs interpreter, binaries, build toolchains, native code (why `pip install`
    sometimes needs a C compiler); multi-stage builds (`FROM … AS <stage>`, `COPY --from=`); a
    virtual environment as the handoff between stages; root vs `sudo`; Flask (framework) vs
    gunicorn (WSGI server); `EXPOSE`, `HEALTHCHECK`, `--no-cache-dir`, `PYTHONUNBUFFERED=1`
  - Taught with: a translator working ahead of time vs live (compiler vs interpreter); a workshop
    vs the finished chair (builder stage vs final image); a master key (root); chef vs host stand
    (Flask vs gunicorn)
  - Hands-on: compared a builder-only image (`docker build --target builder`) with the final one
  - Problems & fixes: a container stuck in `Created` after an interrupted `docker compose up` —
    diagnosed with `docker ps -a` / `docker logs`, fixed with `docker start -a`; the final image
    (231 MB) was bigger than the builder (210 MB) — a `RUN chown -R` after `COPY --from` copied
    the whole venv into a new layer; fixed with `COPY --chown=`, measured 231 MB → 204 MB
  - Revision: a full recap before the quiz, on request
  - Orbit: rewrote `orbit/app/Dockerfile` — multi-stage with a `/opt/venv` handoff, non-root
    `appuser`, gunicorn, `EXPOSE`, `HEALTHCHECK`; `docker-compose.yml` pinned to `orbit-app:2.1`
- Quiz: PASS, attempt 1 — 5 questions
- Score: 90/100 (Quiz 36/40 · Hands-on 29/30 · Depth 25/30)
- Status: Topic 11 CLEARED
- Notebook: `learning/notes/phase-2-containers-kubernetes-ci-cd/topic-11-docker-multi-stage-builds-best-practices.md`
- Went well: found the `chown` / copy-up bug once it was framed as a puzzle, and proved the fix
  with real sizes; asking for a recap before the quiz paid off.
- Do better: keep root (the account) and `sudo` (a way to act as root) clearly apart; watch the
  interpret / compile wording.
- Lesson: When a result looks impossible — a final image bigger than its builder — treat it as a
  bug to trace, not a fluke.
- Notes: needed ground-up teaching — none of compiler, binary or WSGI was assumed. Closed every
  Dockerfile item deferred from the Topic 10 audit.
- Check-in: 2026-07-24 22:56 IST — Check-out: 2026-07-25 02:04 IST

### Session 18 — 2026-09-22 — Kubernetes architecture, first kind cluster
- Topic: Topic 12 — Kubernetes — Architecture & Core Concepts — day 1 of 2 — in progress
- Covered:
  - Learned: what Kubernetes solves (self-healing, rescheduling, scaling) and its alternatives
    (Docker Swarm, Nomad, ECS/Fargate, Cloud Run, managed Kubernetes); control plane (API server,
    etcd, scheduler, controller manager) vs worker nodes (kubelet); kubelet → CRI → container
    runtime, tied to Topic 11's WSGI pattern; the Pod as the deployable unit, not a container
  - Taught with: an airport control tower and its runways (control plane vs workers); a hotel
    front desk (the API server); a hotel room with one address (a Pod)
  - Hands-on: created a real cluster (`kind create cluster`); `kubectl get nodes` showed the
    control-plane and worker roles exactly as taught; `kubectl cluster-info` showed the control
    plane and CoreDNS endpoints
  - Setup: installed `kind` v0.33.0 via `winget` (checked against the latest GitHub release);
    `kubectl` v1.34.1 was already present with Docker Desktop
  - Orbit: `orbit/k8s/kind-config.yaml` — a two-node cluster (1 control-plane, 1 worker)
- Quiz: none — day 1 of 2
- Status: in progress — Day 2 + quiz next
- Notebook: `learning/notes/phase-2-containers-kubernetes-ci-cd/topic-12-kubernetes-architecture-core-concepts.md`
- Went well: asked for the API server explanation again when it didn't fully land; asked how the
  field atlas should cover Kubernetes before assuming.
- Do better: nothing flagged this session.
- Lesson: Ask again when an explanation only half lands.
- Carry-forward: the field atlas's Kubernetes entry is written once, after Topic 14 finishes.
- Notes: first session after a 58-day gap.
- Check-in: 2026-09-22 04:50 IST — Check-out: 2026-09-22 05:09 IST
