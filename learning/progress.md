# Progress log

> Read by Claude Code at the start of every session — this is the live state of the plan.
> All dates are IST (UTC+5:30), format YYYY-MM-DD. Day 1 = 2026-07-06. Raw command output and
> git commit metadata reflect the machine's local clock (US Eastern), not IST.

## Current status

> One line, overwritten every session — not appended to. This is what gets read first.

Topic 1 — COMPLETE (90/100). Topic 2 — COMPLETE (84/100). Topic 3 — COMPLETE (80/100, cleared
in 2 attempts). Topic 4 — COMPLETE (88/100). Topic 5 — COMPLETE (82/100). Topic 6 — COMPLETE
(84/100). Topic 7 — COMPLETE (82/100). Topic 8 — COMPLETE (94/100). **PHASE 1 (Linux, Git &
Version Control) COMPLETE.** Topic 9 — COMPLETE (86/100). Topic 10 — COMPLETE (92/100). Next:
Topic 11 (Docker — Multi-Stage Builds & Best Practices). SSH live connection still deferred to
AWS sandbox VM.

## Session log

<!-- Append one entry per session, in order. Day 1 is 2026-07-06 IST. -->
### Session 1 — 2026-07-06
- Topic in progress: Topic 1 — Linux Fundamentals — Filesystem, SSH, VMs (day 1 of 2)
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

### Session 2 — 2026-07-07
- Topic completed: Topic 1 — Linux Fundamentals — Filesystem, SSH, VMs (day 2 of 2, FINAL DAY)
- Covered: permission troubleshooting solved independently (`chmod` on a non-executable script),
  hard links vs symlinks via the inode/link-count model — proven hands-on including two real
  discoveries (a hard link to a symlink is itself a symlink; `ln -f` can silently free the last
  copy of real data), SSH key generation (`ssh-keygen -t ed25519`), `known_hosts` and
  `~/.ssh/config` concepts, and a VM/container multi-tenant isolation scenario tied directly to
  the project's future EC2→Kubernetes architecture.
- Quiz: **PASS, attempt 1** — 6 interview-style questions, open-ended, no multiple choice. Full
  question-by-question record in
  `learning/notes/phase-1-linux-git-version-control/topic-01-linux-fundamentals.md`; attempt
  status tracked in the Quiz record index below.
  **Topic 1 CLEARED**
  **90/100 (Quiz 36/40, Hands-on 27/30, Depth 27/30)**
- Check-in: 2026-07-07 22:19 IST — Check-out: 2026-07-08 05:25 IST (quiz itself ran ~32 minutes,
  over the 20-minute cap — allowed to finish in progress rather than cut mid-question)

### Session 3 — 2026-07-08
- Topic in progress: Topic 2 — Linux — Top 50 Shell Commands (day 1 of 2)
- Covered: file viewing (`head`, `tail`, `less`), search (`grep` with case-sensitivity and `-v`
  gotchas, `find` vs `grep` content-vs-filename distinction), text processing (`sort`, `uniq`,
  `wc`, `cut`), and a combined real-world log-analysis pipeline exercise built incrementally
  (`grep | cut | sort | uniq -c | sort -nr | head`).
- Quiz: N/A (day 1 of 2, non-final day — quiz scheduled for Day 2)
- Check-in: 2026-07-08 22:35 IST — Check-out: 2026-07-09 05:58 IST

### Session 4 — 2026-07-09
- Topic completed: Topic 2 — Linux — Top 50 Shell Commands (day 2 of 2, FINAL DAY)
- Covered: process/signal handling (`ps aux`, `top`, `kill`/`kill -9`, SIGTERM vs SIGKILL
  catchability), system resource commands (`df -h`, `du -sh`, `free -h`, `uptime`/load average),
  networking (`ping`, `ss -tuln`) including a real discovery that ICMP (ping) and TCP (curl/apt)
  are independently firewalled — resolving an apparent contradiction with Topic 1's proxy
  findings — and archiving (`tar -czvf`/`-xzvf`/`-tzvf`).
- Quiz: **PASS, attempt 1** — 5 interview-style questions covering both days. Full record in
  `learning/notes/phase-1-linux-git-version-control/topic-02-top-50-shell-commands.md`.
  **Topic 2 CLEARED**
  **84/100 (Quiz 34/40, Hands-on 26/30, Depth 24/30)**
- Check-in: 2026-07-09 23:24 IST — Check-out: 2026-07-10 05:39 IST (quiz ran ~28 minutes, over
  the 20-minute cap — allowed to finish in progress)

### Session 5 — 2026-07-10
- Topic in progress: Topic 3 — Linux — Shell Scripting Basics (day 1 of 2)
- Covered: shebang line, variables, positional arguments (`$1`/`$#`), conditionals (`if`/`elif`/
  `else`/`fi`, string and numeric operators), arithmetic expansion (`$(( ))`, modulo), and a
  combined `classify.sh` exercise (sign + odd/even) written entirely from scratch — including
  real, independently-debugged syntax errors (missing `else`/`fi` separators, merged `fi`/`if`
  blocks, and a `nano`-vs-`printf` `\n` handling mixup that briefly broke the shebang line).
- Quiz: N/A (day 1 of 2, non-final day — quiz scheduled for Day 2)
- Check-in: 2026-07-10 22:02 IST — Check-out: 2026-07-11 04:14 IST

### Session 6 — 2026-07-11
- Topic completed: Topic 3 — Linux — Shell Scripting Basics (day 2 of 2, FINAL DAY)
- Covered: loops (`for`, `while`, incl. a real self-debugged infinite-loop bug), functions
  (definition + invocation), exit codes/error handling (`$?`, redirecting output to suppress it),
  and a combined `checkall.sh` exercise (function + loop + exit code, tied to `project/scripts/`
  use later).
- Quiz: **Attempt 1 — FAIL** (functions: invocation and `$1` scoping; all other areas —
  conditionals, loops, exit codes — passed cleanly). Re-taught functions using concrete tracing
  (a real script printing `$1` at three points) instead of another analogy, then **Attempt 2 —
  full retest, all-new questions — PASS**, same session, after a short break. Full record in
  `learning/notes/phase-1-linux-git-version-control/topic-03-shell-scripting-basics.md`.
  **Topic 3 CLEARED, in 2 attempts**
  **80/100 (Quiz 30/40, Hands-on 28/30, Depth 22/30)**
- Check-in: 2026-07-11 22:26 IST — Check-out: 2026-07-12 10:02 IST (long session incl. a
  fatigue-driven pause partway through; Attempt 1 quiz ran ~32 minutes, Attempt 2 retest ~23
  minutes, both over the 20-minute cap but allowed to finish in progress)

### Session 7 — 2026-07-12
- Topic in progress: Topic 4 — Linux Deep Dive — Process, Log, Disk Management (day 1 of 2)
- Covered: process states (R/S/D/Z/T + modifiers), `awk` column extraction/filtering (new tool),
  the `/proc` filesystem (per-process info, file descriptors — directly explaining Topic 3's
  `2>&1` syntax), `pstree` process hierarchy, `nice`/`renice` process priority (incl. a real
  sudo-password recovery via `wsl -u root`), and log management (`/var/log` rotation seen live,
  `journalctl`). Real discovery: the corporate-network block from Topic 1 reappeared in
  `systemd-timesyncd` NTP timeout log entries. Combined exercise closed with a genuine lesson
  about keyword-limited log searching (a real issue missed by one search term, caught by another).
- Quiz: N/A (day 1 of 2, non-final day — quiz scheduled for Day 2)
- Check-in: 2026-07-12 22:35 IST — Check-out: 2026-07-13 01:17 IST

### Session 8 — 2026-07-13
- Topic completed: Topic 4 — Linux Deep Dive — Process, Log, Disk Management (day 2 of 2, FINAL DAY)
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
  fairness reasoning, and the `df`-timeout production scenario), 2 of 5 needed a follow-up
  push for full precision but were ultimately correct. Full record in
  `learning/notes/phase-1-linux-git-version-control/topic-04-process-log-disk-management.md`.
  **Topic 4 CLEARED**
  **88/100 (Quiz 34/40, Hands-on 28/30, Depth 26/30)**
- Check-in: 2026-07-13 23:50 IST — Check-out: 2026-07-14 05:17 IST

### Session 9 — 2026-07-14
- Topic completed: Topic 5 — Linux — Networking Fundamentals (both days, single session)
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
  fresh questions, stronger hands-on-verified answers. The retest score is used as the record
  since it reflects the deeper understanding reached after revision.
  **Topic 5 CLEARED, official score**
  **82/100 (Quiz 30/40, Hands-on 26/30, Depth 26/30)**
- Check-in: 2026-07-14 23:47 IST — Check-out: 2026-07-16 05:02 IST (session spanned across days
  with breaks; not continuous active work time)

### Session 10 — 2026-07-16
- Topic completed: Topic 6 — Git Fundamentals — Commits, Branches, Merges (both days, single
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
  branches-vs-direct-commits problem), 2 of 5 needed a real follow-up correction.
  **Topic 6 CLEARED**
  **84/100 (Quiz 30/40, Hands-on 28/30, Depth 26/30)**
- Check-in: 2026-07-16 23:38 IST — Check-out: 2026-07-17 01:45 IST

### Session 11 — 2026-07-18
- Topic completed: Topic 7 — Git Deep Dive — Rebase, Cherry-Pick, Branching Strategies
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
  **Topic 7 CLEARED**
  **82/100 (Quiz 28/40, Hands-on 30/30, Depth 24/30)**
- Check-in: 2026-07-18 00:56 IST — Check-out: 2026-07-19 11:11 IST (session spanned across days
  with breaks; not continuous active work time)

### Session 12 — 2026-07-19
- Topic completed: Topic 8 — GitHub — PRs, Actions Intro, Repo Management (single-day topic per
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
  genuine discoveries: classic branch protection doesn't apply to repo admins by default
  (bypassed silently until "Do not allow bypassing" was enabled), a self-approval block genuinely
  preventing merge on a solo repo, and "Require linear history" actually removing "Create a merge
  commit" from the available merge options. Full record in
  `learning/notes/phase-1-linux-git-version-control/topic-08-github.md`.
- Quiz: **PASS, attempt 1** — 4 interview-style questions (Git vs. GitHub, the PR mistake's root
  cause, merge/squash/rebase strategies tied to linear history, and `GITHUB_TOKEN` security),
  1 of 4 needed real redirection (root-cause reasoning), the other 2 follow-ups were quick
  extensions of already-correct, comprehensive answers rather than corrections.
  **Topic 8 CLEARED**
  **94/100 (Quiz 36/40, Hands-on 30/30, Depth 28/30)**
  **PHASE 1 (Linux, Git & Version Control) COMPLETE.**
- Check-in: 2026-07-19 22:11 IST — Check-out: 2026-07-20 01:27 IST

### Session 13 — 2026-07-20
- Topic in progress: Topic 9 — Docker — Architecture, Images, Containers (day 1 of 2, per the
  roadmap)
- Parallel hands-on: `project/app/` boilerplate written just before Topic 9 began per
  `CLAUDE.md`'s trigger rule — a minimal Flask app (`app.py`) with a real `/health` endpoint plus
  `requirements.txt`, replacing the empty placeholder. Claude-authored per the Phase 5 exception;
  not yet defensible in an interview.
- Covered: client/daemon/registry/image/container terms (taught basics-first, then connected to
  real output per explicit user feedback); the client/server split in `docker version`; the full
  pull → image → container flow traced line-by-line against real `docker run hello-world` output;
  images vs. containers proven hands-on (`docker images`, `docker ps -a` showing one image with
  two separate containers after running `hello-world` twice); where images/containers actually
  live (Docker Desktop's Linux VM backend, tied back to Topic 1's VM concept); wrote a real
  5-instruction Dockerfile (`FROM`/`WORKDIR`/`COPY`/`RUN`/`CMD`) for `project/app/` line by line;
  built it (`docker build -t mission-control-app .`) and ran it (`docker run -d -p 5000:5000`),
  verified live via `http://localhost:5000/health` returning `{"status":"ok"}`; container
  lifecycle commands (`docker logs`, `docker stop`, `docker ps -a`); a real discovered detail —
  `mission-control-app`'s container exited with code 137 (`128 + SIGKILL`) after `docker stop`,
  vs. `hello-world`'s clean `Exited (0)`, tied directly back to Topic 2's signals/`kill -9`
  content. Full record in
  `learning/notes/phase-2-containers-kubernetes-ci-cd/topic-09-docker-architecture-images-containers.md`.
- Quiz: N/A (day 1 of 2, non-final day — quiz scheduled for Day 2 per multi-day topic rule)
- Check-in: 2026-07-20 22:37 IST — Check-out: 2026-07-21 10:50 IST

### Session 14 — 2026-07-21
- Topic completed: Topic 9 — Docker — Architecture, Images, Containers (day 2 of 2, FINAL DAY)
- Covered: layer/cache-invalidation edge case — proved that changing `app.py` forced an
  unnecessary `RUN pip install` rerun because `COPY . .` bundled it with `requirements.txt` into
  one layer, and that once a layer's cache breaks, every layer after it reruns regardless of its
  own actual inputs; independently rewrote the Dockerfile to `COPY requirements.txt .` →
  `RUN pip install` → `COPY app.py .`, self-caught the missing final `COPY` step, then proved the
  fix with real build logs (13.3s → 2.3s, `RUN pip install` showing `CACHED`); image tagging —
  `docker tag`, proved `:latest` only moves when a build/tag explicitly assigns it — it silently
  stayed on an older image once builds were tagged `v1`/`v2` instead, so it wasn't necessarily the
  newest content — by running `v1`/`v2` simultaneously on different ports and seeing both real,
  distinct versions; harder independent task — added a `/ready` endpoint (liveness vs. readiness
  previewed ahead of Kubernetes), self-caught a real Python string-vs-boolean bug
  (`ready="true"` vs. `ready=True`); safely deleted a buggy image using `stop`→`rm`→`rmi` after
  identifying the exact dependent container blocking it. Full record in
  `learning/notes/phase-2-containers-kubernetes-ci-cd/topic-09-docker-architecture-images-containers.md`.
- Quiz: **PASS, attempt 1** — 5 interview-style questions covering both days (architecture flow,
  image/container semantics, cache invalidation, tagging, exit codes/signals); 2 needed a quick
  follow-up to surface an already-understood detail, 1 left "why it matters" unaddressed until
  asked, 1 had a genuine two-round factual mix-up (`docker stop` vs. `hello-world`'s self-exit);
  tagging was answered flawlessly.
  **Topic 9 CLEARED**
  **86/100 (Quiz 32/40, Hands-on 29/30, Depth 25/30)**
- Check-in: 2026-07-21 23:44 IST — Check-out: 2026-07-22 04:47 IST

### Session 15 — 2026-07-22
- Topic in progress: Topic 10 — Docker — Networking, Volumes, Docker Compose (day 1 of 2)
- Covered: the bridge network concept via a roads/neighborhoods analogy, `docker network ls`
  (bridge/host/none), `docker network inspect bridge` (real discovery: 3 IPs already "in use" on
  an empty network — the network address, gateway, and broadcast address, none of them
  containers — verified against Topic 5's CIDR math, `2^16 = 65536` total addresses, matching
  `DynamicIPsAvailable: 65533`); container-to-container communication proven hands-on with two
  real `mission-control-app` containers — name resolution genuinely failed on the default bridge
  (`socket.gaierror: Name or service not known`), succeeded by IP, then succeeded by name too once
  both were connected to a custom network (`docker network create`/`docker network connect`);
  port publishing recap tied back to Topic 5's private/public IP and NAT concepts. Volumes
  introduced: proved container storage is temporary by writing a file, deleting the container, and
  showing it was gone; fixed with a bind mount (`-v C:\CloudOps\ignite\project\data:/app/data`),
  proving persistence across container deletion by reading the file back from a brand-new
  container. Full record in
  `learning/notes/phase-2-containers-kubernetes-ci-cd/topic-10-docker-networking-volumes-compose.md`.
- Quiz: N/A (day 1 of 2, non-final day — quiz scheduled for Day 2 per multi-day topic rule)
- Check-in: 2026-07-22 22:53 IST — Check-out: 2026-07-23 02:12 IST

### Session 16 — 2026-07-23
- Topic completed: Topic 10 — Docker — Networking, Volumes, Docker Compose (day 2 of 2, FINAL DAY)
- Covered: named volumes (`docker volume create`, `docker volume ls`) proven to persist data
  across container deletion the same way bind mounts do, using a real named volume; the rule that
  a running container's mounts can never be changed in place (only at creation) reinforced via a
  safe duplicate-then-swap technique — creating a verified duplicate container with the added
  mount, confirming its contents were correct, then only deleting/renaming the original once
  proven safe, rather than deleting first and hoping; a full consistency audit of both containers
  and the volume before moving on. Docker Compose introduced from scratch — YAML structure,
  writing a real `docker-compose.yml` for `mission-control-app` (`services`, `build`, `ports`),
  running it with `docker compose up -d`, and verifying `http://localhost:5000/health` live; the
  file then extended with a second service, proving Compose automatically creates its own network
  (`project_default`) with built-in name-based resolution between services (no manual
  `docker network create` needed), and a named volume proving shared persistence — plus that
  `docker compose up` automatically recreates a service whose config changed while creating new
  services fresh. Full record in
  `learning/notes/phase-2-containers-kubernetes-ci-cd/topic-10-docker-networking-volumes-compose.md`.
- Quiz: **PASS, attempt 1** — 5 interview-style questions covering both days (default bridge vs.
  custom network DNS resolution, bind mount vs. named volume, volume lifecycle independence from
  containers, why Compose recreated one service but not the other, and how Compose services find
  each other by name without manual network setup); all 5 answered correctly with genuine
  reasoning, one minor mix-up on a follow-up (attributing a path-collision reason to a container
  that never had one) corrected in the moment.
  **Topic 10 CLEARED**
  **92/100 (Quiz 36/40, Hands-on 30/30, Depth 26/30)**
- Check-in: 2026-07-23 23:06 IST — Check-out: 2026-07-24 04:39 IST

## Quiz record index

> A topic clears with one passed attempt. Three failed attempts trigger deferred mastery
> (see `CLAUDE.md`'s 3-attempt mastery rule).

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

## Deferred mastery topics

> Topics that hit 3 failed attempts. Each must be revisited within 3 sessions of being deferred
> and cleared with one passed retest — before any project step or later topic that assumes that
> knowledge, and regardless of whether anything depends on it yet.

| Topic # | Topic name | Deferred on (session #) | Revisit deadline (session #) | Revisited on | Cleared? |
|---|---|---|---|---|---|

## Light days log

| Date | Reason given |
|---|---|
| 2026-07-17 | Already ahead of schedule — Sessions 9 and 10 had efficiently covered Topic 5 and Topic 6 (each a 2-day topic in the baseline) within continuous sessions starting 2026-07-14 and 2026-07-16, so this day was taken as a rest day without falling behind. Logged retroactively during a later review, since it wasn't captured in the moment. Pacing cost: none — Topics 1-8 still landed at exactly their planned 14 roadmap days total, zero overrun. |
