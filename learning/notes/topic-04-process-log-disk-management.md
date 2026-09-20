# Topic 4 — Linux Deep Dive: Process, Log, Disk Management

> Personal study notebook — full teaching content, commands, outputs, and explanations.
> Distinct from `progress.md` (tracking) and `session_notes.md` (short personal reflection).

---

## Day 1 — 2026-07-12 (process states, /proc, nice/renice, log basics)

Goes deeper than Topic 2's `ps`/`top` basics.

### 1. Process states

Every process is always in one specific state:

| Code | State | Meaning |
|---|---|---|
| `R` | Running | Actively executing on CPU right now |
| `S` | Sleeping | Waiting for something — not using CPU |
| `D` | Uninterruptible sleep | Waiting on disk/IO — can't even be killed until it returns |
| `Z` | Zombie | Finished, but exit status not yet collected by its parent |
| `T` | Stopped | Paused (e.g. `Ctrl+Z`) |

**Modifier characters** appended to the base letter:
- `+` — in the **foreground** of its terminal
- `s` — a **session leader** (the "head" process of a group)
- `l` — **multi-threaded**
- `<` — **higher priority** than normal

### 2. `awk` — column extraction and filtering (new tool, introduced here)

**Syntax**: `awk '{print $N}'` — print column N of each line (columns are whitespace-separated
by default)
**Syntax**: `awk 'CONDITION {print ...}'` — condition comes **before** the action block; only
matching lines get the action applied
**Syntax**: `awk '$N ~ /PATTERN/ {print ...}'` — `~` means "matches"; `/^X/` = starts with X
(same `^` anchor meaning as `grep`)

**Verified hands-on — full breakdown by STAT category**:
```
$ ps aux | awk '{print $8}' | sort | uniq -c
      2 R+
      4 S
      5 S+
      1 S<s
      1 STAT          <- header row leaked through (its own text "STAT" got counted)
      2 Sl
      4 Sl+
     12 Ss
      3 Ss+
      3 Ssl
      2 Ssl+
```

**Verified hands-on — filtering by state/modifier** (special regex chars need escaping, e.g.
`+` → `\+`; `s`, `l`, `<` are plain, no escaping needed):
```
$ ps aux | awk '$8 ~ /^R/ {print $1 $8 $11}'          # running only
$ ps aux | awk '$8 ~ /^S/ {print $1 $8 $11}'          # sleeping only — header "STAT" leaked
                                                         # through too, since "STAT" itself
                                                         # starts with "S" — filter noise isn't
                                                         # immune to coincidental header matches
$ ps aux | awk '$8 ~ /s/ {print $1 $8 $11}'           # session leaders
$ ps aux | awk '$8 ~ /l/ {print $1 $8 $11}'           # multi-threaded
$ ps aux | awk '$8 ~ /</ {print $1 $8 $11}'           # higher priority
$ ps aux | awk '$8 ~ /\+/ {print $1 $8 $11}'          # foreground — correctly matched the exact
                                                         # commands run interactively (ps, bash,
                                                         # awk, sort, uniq)
```

**Counting**: `sort | uniq -c` gives grouped counts per unique value; add `| wc -l` afterward to
get the **total number of distinct groups** instead of per-group counts.

### 3. The `/proc` filesystem

A **virtual (pseudo) filesystem** — nothing in it is real data on disk; the kernel generates its
contents **live**, the instant you read them. Every command so far (`ps`, `top`, `free`, `df`)
is really just reading and formatting `/proc` under the hood.

**Kernel recap**: the core part of the OS that directly manages hardware (CPU, memory, disk) and
mediates between hardware and every other program — deciding CPU time allocation, memory,
disk IO, and process lifecycle. `/proc` is the kernel exposing its own internal bookkeeping as a
readable filesystem.

**Structure**:
- `/proc/<PID>/` — one folder per running process: `status` (summary), `cmdline` (exact start
  command), `environ`, `fd/` (open file descriptors)
- `/proc/cpuinfo`, `/proc/meminfo` — system-wide info (literally what `free`/`lscpu` read from)

**Verified hands-on**:
```
$ echo $$
44720
$ cat /proc/44720/status | head -10
Name:   bash
State:  S (sleeping)
Pid:    44720
PPid:   44675
...
$ cat /proc/44720/cmdline
/bin/bash--init-file/home/.../shellIntegration-bash.sh
$ cat /proc/meminfo | head -5
MemTotal:        7971040 kB
...
```
- `PPid` (parent PID) — every process except PID 1 has a parent. Directly tied to the **Zombie**
  state: a zombie is a finished child whose exit status the parent hasn't collected yet.
- `cmdline` prints with no spaces between arguments — it actually stores them separated by
  **null bytes**, which `cat` doesn't render as visible spaces; the real command had normal
  spacing, just not shown that way here.
- `meminfo`'s `MemTotal: 7971040 kB` matches exactly what `free -h` reported in Topic 2 (`7.6Gi`)
  — direct confirmation `free` reads this same file.

**File descriptors** — `/proc/<PID>/fd/` is a directory, not a file (needs `ls`, not `cat`):
```
$ ls -l /proc/44720/fd/
lrwx------ 1 devuser devuser 64 ... 0 -> /dev/pts/5
lrwx------ 1 devuser devuser 64 ... 1 -> /dev/pts/5
lrwx------ 1 devuser devuser 64 ... 2 -> /dev/pts/5
lrwx------ 1 devuser devuser 64 ... 255 -> /dev/pts/5
```
Every process gets three standard file descriptors: **`0` = stdin**, **`1` = stdout**,
**`2` = stderr**. **This directly explains Topic 3's `2>&1` syntax**: it means "redirect file
descriptor 2 (stderr) to wherever file descriptor 1 (stdout) currently points" — merging error
output into the normal output stream. (`255` is bash's own internal bookkeeping fd, not something
to manage directly.)

### 4. `pstree` — visualizing parent-child relationships

**Syntax**: `pstree [-p]` — `-p` shows PIDs alongside each process name (not "parent" — the tree
*shape itself* is what shows parent-child relationships, regardless of any flag)

**Verified hands-on**: confirmed the exact chain `systemd(1)` → ... → `MainThread(44675)` →
`bash(44720)` → `pstree(...)`, matching precisely the `PPid: 44675` seen in `/proc/44720/status`
— `ps`'s STAT column, `/proc`, and `pstree` all confirmed as different views of the identical
underlying process relationships.

### 5. `nice` and `renice` — process priority

Niceness ranges **-20** (highest priority) to **19** (lowest priority, most "nice" to others),
default `0`.

**Syntax**: `nice -n VALUE COMMAND` — start a new command with a given niceness
**Syntax**: `renice VALUE -p PID` — change niceness of an already-running process

**Key rule, confirmed via a real permission-denied error**: a regular user can only **increase**
niceness (lower priority — e.g. `0→10`, `10→19`), never **decrease** it (raise priority — e.g.
`10→5`), even toward still-positive numbers. Decreasing requires `sudo`/root, regardless of
starting point — otherwise anyone could incrementally boost their own priority.

**Verified hands-on**:
```
$ nice -n 10 sleep 300 &
$ ps -o pid,ni,cmd -p 70478
    PID  NI CMD
  70478  10 sleep 300

$ renice 19 -p 70478                    # increase, no sudo needed — succeeded
70478 (process ID) old priority 10, new priority 19

$ sudo renice 0 -p 70478                # decrease, sudo required — succeeded
70478 (process ID) old priority 19, new priority 0

$ renice 5 -p 70478                     # decrease, no sudo — failed as expected
renice: failed to set priority for 70478 (process ID): Permission denied
```
`$!` — special variable holding the PID of the most recently backgrounded process, a shortcut
for checking a process you just started with `&` without needing to look up its number manually.

**Forgot sudo password mid-session** — resolved via WSL-specific recovery (run from Windows
PowerShell, not WSL bash): `wsl -u root` (opens a root session bypassing sudo/password entirely,
since WSL trusts the launching Windows account) → `passwd <username>` to set a new password.
Confirmed: resetting the password only changes the login credential — zero effect on files,
permissions, installed packages, or any other settings.

### 6. Log management

**`/var/log`** — traditional plain-text logs, one (or more) file per service/subsystem. Recall
Topic 1: `/var` holds data that grows over time.

**Verified hands-on — log rotation, seen for real**:
```
$ ls -l /var/log | head -10
...
-rw-r--r--  1 root   root    178 Jul 10 13:44 alternatives.log
-rw-r--r--  1 root   root  29315 Jun 27 06:04 alternatives.log.1
...
-rw-r-----  1 syslog adm    5310 Jul 12 15:17 auth.log
-rw-r-----  1 syslog adm   21120 Jul 11 23:17 auth.log.1
-rw-r-----  1 syslog adm    2673 Jul  6 13:50 auth.log.2.gz
```
Current log, previous rotation (`.1`), and an older one already compressed (`.2.gz`, using
gzip from Topic 2) — log rotation happening for real, not just a described concept.

**`journalctl`** — the modern, unified, structured systemd log (`journald`), covering most of
what used to be scattered across separate plain-text files.
- `journalctl -n N` — last N entries
- `journalctl -f` — follow live (like `tail -f`)
- `journalctl -u SERVICE_NAME` — filter to one service

**Verified hands-on — real entries recognized from earlier work**:
```
$ journalctl -n 10
Jul 12 15:15:35 ... sudo[70805]: pam_unix(sudo:session): session closed for user root
Jul 12 15:17:01 ... CRON[71176]: pam_unix(cron:session): session opened for user root...
Jul 12 15:17:01 ... CRON[71177]: (root) CMD (cd / && run-parts --report /etc/cron.hourly)
Jul 12 15:20:35 ... systemd-timesyncd[114]: Timed out waiting for reply from ... (ntp.ubuntu.com)
```
- The `sudo` entry is literally the `renice` command from earlier, showing up in the real log.
- **`cron(175)` vs. `CRON[71176]`**: `cron(175)` (seen in `pstree` output) is the persistent
  background **daemon** always watching the clock; `CRON[71176]` is a **short-lived child
  process** spawned each time a scheduled task actually runs, exiting once done. One watcher,
  many temporary instances.
- **`systemd-timesyncd` timeout messages** — the system failing to reach an NTP time server.
  Almost certainly the **same corporate network/firewall block** from Topic 1's SSH
  troubleshooting, now showing up in a completely different context (system logs vs. a failed
  `apt install`) — same root cause, different symptom.

**Log rotation, the concept**: logs would grow forever and eventually fill the disk if left
unchecked (ties to Topic 2's `df`/disk-usage concerns). `logrotate` (config in
`/etc/logrotate.d/`) periodically archives/compresses old logs automatically.

### 7. Analogies used

- **`systemd`** = hotel general manager — starts every department in order, watches over them,
  restarts anything that fails, shuts everything down properly at close.
- **`journalctl`** = the hotel's unified digital logbook — search/filter everything centrally,
  instead of hunting through each department's own separate paper logbook.
- **`/var/log`** = each department's own separate paper logbook (the pre-unified-system state) —
  still coexists alongside the journal, since some software still writes its own plain-text files.

### 8. Combined exercise — "the system feels slow" troubleshooting scenario

**Step 1** — find active (`R`-state) processes:
```
$ ps aux | awk '$8 ~ /^R/'
devuser 75904  0.0  0.0  8284  4224 pts/5  R+  15:39  0:00 ps aux
```
Only match: `ps aux` itself — makes sense, since running `ps` briefly *is* the actively-executing
process capturing this exact snapshot. Confirms a healthy, non-slow system at that moment — no
actual CPU hog found.

**Step 2** — check recent logs for explicit errors/failures:

**Syntax**: `grep -iE "PATTERN1|PATTERN2"` — `-E` enables extended regex, where `|` means
**OR** between patterns (plain `grep -i "error fail"` would search for that exact literal phrase
as one string, not either word independently).
```
$ journalctl -n 50 | grep -iE "error|fail"
(no output)
```

**Real lesson, confirmed by testing directly**: this empty result initially looked like "nothing
wrong," but the `systemd-timesyncd` timeout messages from earlier are a genuine real problem —
they just don't contain the literal words "error" or "fail," they say "Timed out" instead:
```
$ journalctl -n 50 | grep "Time"
Jul 12 15:20:35 ... systemd-timesyncd[114]: Timed out waiting for reply from ...
Jul 12 15:20:45 ... systemd-timesyncd[114]: Timed out waiting for reply from ...
...
```
**Takeaway**: log searching is only as good as the keywords chosen — a real issue can exist in
logs without matching the specific words guessed first. Real troubleshooting often searches
multiple related terms at once (`"error|fail|timeout|denied|refused"`), precisely because you
don't always know in advance how a problem will be phrased.

---

## Day 2 — TBD

_To be filled in as Day 2 progresses._
